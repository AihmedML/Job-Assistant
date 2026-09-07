(()=>{"use strict";
const {after}=vendetta.patcher;
const {findByStoreName,findByTypeName}=vendetta.metro;
const {React,ReactNative,FluxDispatcher}=vendetta.metro.common;
const storage=vendetta.plugin.storage;
const {View,Text,ScrollView,TouchableOpacity}=ReactNative;
const ChannelStore=findByStoreName("ChannelStore");
const UserStore=findByStoreName("UserStore");
const listeners=new Set();
let unpatchers=[];
let ageTimer=null;
let rowPatchTimer=null;

function getHistory(){
  const h=storage.history;
  return h&&typeof h==="object"?h:{};
}

function setHistory(next){
  storage.history=next;
  for(const fn of [...listeners]){
    try{fn();}catch{}
  }
}

function recordTyping(channelId,userId){
  const history=getHistory();
  setHistory({...history,[channelId]:{userId:String(userId),lastTyping:Date.now()}});
}

function clearChannel(channelId){
  const history=getHistory();
  if(!history[channelId]) return;
  const next={...history};
  delete next[channelId];
  setHistory(next);
}

function isOneToOneDM(channel){
  try{return !!channel?.isDM?.();}catch{return false;}
}

function formatAge(ts){
  const s=Math.max(0,Math.floor((Date.now()-Number(ts||0))/1000));
  if(s<60) return "typed now";
  const m=Math.floor(s/60);
  if(m<60) return `typed ${m}m ago`;
  const h=Math.floor(m/60);
  if(h<24) return `typed ${h}h ago`;
  const d=Math.floor(h/24);
  return `typed ${d}d ago`;
}

function useRefresh(){
  const [,setTick]=React.useState(0);
  React.useEffect(()=>{
    const fn=()=>setTick(v=>v+1);
    listeners.add(fn);
    return()=>listeners.delete(fn);
  },[]);
}

function TypingHistoryBadge({channelId}){
  useRefresh();
  const entry=getHistory()[channelId];
  if(!entry) return null;
  return React.createElement(View,{pointerEvents:"none",style:{position:"absolute",right:14,top:8,paddingHorizontal:6,paddingVertical:2,borderRadius:6,backgroundColor:"rgba(0,0,0,0.28)"}},
    React.createElement(Text,{style:{fontSize:10,fontWeight:"600",color:"#dbdee1"}},formatAge(entry.lastTyping))
  );
}

function Settings(){
  useRefresh();
  const history=getHistory();
  const rows=Object.entries(history).sort((a,b)=>Number(b[1]?.lastTyping||0)-Number(a[1]?.lastTyping||0));
  return React.createElement(ScrollView,{contentContainerStyle:{padding:16,gap:10}},
    React.createElement(Text,{style:{fontSize:20,fontWeight:"700",marginBottom:4}},"DM Typing History"),
    React.createElement(Text,{style:{fontSize:13,opacity:.72,marginBottom:8}},"Stores only that a DM contact started typing and when. It never stores draft text."),
    React.createElement(TouchableOpacity,{onPress:()=>setHistory({}),style:{paddingVertical:11,paddingHorizontal:12,borderRadius:8,backgroundColor:"rgba(255,255,255,0.10)",marginBottom:8}},
      React.createElement(Text,{style:{fontWeight:"700"}},"Clear typing history")
    ),
    rows.length===0
      ? React.createElement(Text,{style:{opacity:.6,marginTop:8}},"No saved typing events yet.")
      : rows.map(([channelId,entry])=>{
          const user=UserStore?.getUser?.(entry.userId);
          const name=user?.globalName||user?.username||entry.userId||"Unknown user";
          return React.createElement(View,{key:channelId,style:{paddingVertical:10,borderBottomWidth:.5,borderBottomColor:"rgba(255,255,255,0.12)"}},
            React.createElement(Text,{style:{fontSize:15,fontWeight:"600"}},name),
            React.createElement(Text,{style:{fontSize:12,opacity:.65,marginTop:2}},formatAge(entry.lastTyping))
          );
        })
  );
}

function handleEvent(event){
  try{
    if(!event||typeof event!=="object") return;
    if(event.type==="TYPING_START"){
      const channelId=event.channelId||event.channel_id;
      const userId=event.userId||event.user_id;
      if(!channelId||!userId) return;
      const channel=ChannelStore?.getChannel?.(channelId);
      if(!isOneToOneDM(channel)) return;
      const me=UserStore?.getCurrentUser?.()?.id;
      if(String(userId)===String(me)) return;
      recordTyping(String(channelId),String(userId));
      return;
    }
    if(event.type==="MESSAGE_CREATE"){
      const channelId=event.channelId||event.channel_id||event.message?.channel_id;
      if(!channelId) return;
      const entry=getHistory()[channelId];
      if(!entry) return;
      const channel=ChannelStore?.getChannel?.(channelId);
      if(!isOneToOneDM(channel)) return;
      const authorId=event.message?.author?.id||event.author?.id;
      if(authorId&&String(authorId)===String(entry.userId)) clearChannel(String(channelId));
    }
  }catch(e){
    console.warn("DM Typing History event error",e);
  }
}

function patchDmRow(){
  const base=findByTypeName("MessagesItemChannelBase");
  if(!base?.type||typeof base.type!=="function") return false;
  unpatchers.push(after("type",base,(args,ret)=>{
    try{
      const props=args?.[0];
      const channel=props?.channel;
      if(!isOneToOneDM(channel)) return ret;
      const h=props?.height;
      return React.createElement(View,{style:{height:typeof h==="number"?h:undefined,position:"relative"}},
        ret,
        React.createElement(TypingHistoryBadge,{channelId:String(channel.id)})
      );
    }catch{return ret;}
  }));
  return true;
}

function onLoad(){
  if(!storage.history||typeof storage.history!=="object") storage.history={};
  try{unpatchers.push(after("dispatch",FluxDispatcher,(args)=>handleEvent(args?.[0])));}catch(e){console.warn("DM Typing History dispatcher patch failed",e);}
  try{
    if(!patchDmRow()){
      let tries=0;
      rowPatchTimer=setInterval(()=>{
        tries++;
        try{
          if(patchDmRow()||tries>=60){clearInterval(rowPatchTimer);rowPatchTimer=null;}
        }catch{}
      },2000);
    }
  }catch(e){console.warn("DM Typing History row patch failed",e);}
  ageTimer=setInterval(()=>{for(const fn of [...listeners]){try{fn();}catch{}}},60000);
}

function onUnload(){
  for(const unpatch of unpatchers.splice(0)){
    try{unpatch();}catch{}
  }
  if(ageTimer){clearInterval(ageTimer);ageTimer=null;}
  if(rowPatchTimer){clearInterval(rowPatchTimer);rowPatchTimer=null;}
  listeners.clear();
}

return{onLoad,onUnload,settings:Settings};
})()