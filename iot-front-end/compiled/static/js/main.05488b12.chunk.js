(this["webpackJsonpiot-front-end"]=this["webpackJsonpiot-front-end"]||[]).push([[0],{100:function(e,t,n){},102:function(e,t,n){},103:function(e,t,n){},104:function(e,t,n){},134:function(e,t,n){},135:function(e,t,n){},136:function(e,t,n){"use strict";n.r(t);var s=n(0),c=n.n(s),a=n(40),i=n.n(a),r=(n(91),n(92),n(52)),o=n(23),d=(n(54),n(93),n(71)),u=n(72),l=(n(98),n(2)),j=function(e){var t=e.message;return e.isSended?Object(l.jsx)("div",{className:"chatRow sentDiv",children:Object(l.jsxs)("div",{className:"chatMessage",children:[Object(l.jsx)("div",{children:t.message}),Object(l.jsxs)("div",{className:"hour-box",children:[Object(l.jsx)("div",{className:"hour",children:t.hour}),Object(l.jsx)("div",{className:"check",children:Object(l.jsx)(d.a,{icon:u.a})})]})]})}):Object(l.jsx)("div",{className:"chatRow receivedDiv",children:Object(l.jsxs)("div",{className:"chatMessage",children:[Object(l.jsx)("div",{children:t.message}),Object(l.jsx)("div",{className:"hour-box",children:Object(l.jsx)("div",{className:"hour",children:t.hour})})]})})},f=n(84),m=(n(100),function(e){var t=e.chatId,n=e.onSend,s=e.buttonReplyes;return Object(l.jsx)("div",{className:"replyBar",children:Object(l.jsx)("div",{className:"buttonsPanel",children:void 0!==s&&s.map((function(e,s){return function(e,s){return Object(l.jsx)(f.a,{onClick:function(){return n(t,e)},type:"primary",children:e},s)}(e,s)}))})})}),h=function(e){var t=e.sensorType,n=e.chatId,c=e.name,a=e.messages,i=e.onSend,r=Object(s.createRef)();Object(s.useEffect)((function(){o()}),[r]);var o=function(){var e=document.getElementById("messageContainer");e.scrollTop=e.scrollHeight},d=function(e,t){return e.isSended?u(e,t):f(e,t)},u=function(e,t){return Object(l.jsx)(j,{message:e,isSended:!0},t)},f=function(e,t){return Object(l.jsx)(j,{message:e,isSended:!1},t)};return Object(l.jsxs)("div",{className:"chatBox",children:[Object(l.jsx)("div",{className:"chatInfoHeader",children:Object(l.jsx)("div",{children:c})}),Object(l.jsx)("div",{id:"messageContainer",ref:r,className:"messageContainer",children:void 0!==a&&a.map((function(e,t){return function(e,t){if(void 0!==e)switch(e.type){case"text":return d(e,t);default:return Object(l.jsx)("div",{children:"NOT SUPPORTED"})}}(e,t)}))}),Object(l.jsx)("div",{className:"inputBox",children:Object(l.jsx)(m,{chatId:n,onSend:i,buttonReplyes:"car"===t?["position","engine on","engine off","status"]:"home"===t?["lights on","lights off","activate alarm","deactivate alarm"]:"air-conditioner"===t?["set 20\xb0","set 22\xb0","set 24\xb0","set 26\xb0","set 28\xb0","set 30\xb0","status"]:void 0})})]})},b=(n(102),function(e){var t=e.id,n=e.name,c=e.lastMessage,a=e.img,i=e.selected,r=e.onClick,d=Object(s.useState)("message"),u=Object(o.a)(d,2),j=u[0],f=u[1],m=Object(s.useState)("messageinfo"),h=Object(o.a)(m,2),b=h[0],O=h[1],v=Object(s.useState)("ora"),g=Object(o.a)(v,2),x=g[0],p=g[1];Object(s.useEffect)((function(){i?N():y()}));var N=function(){f("message selected"),O("messageinfo selected"),p("ora selected")},y=function(){f("message"),O("messageinfo"),p("ora")};return Object(l.jsxs)("div",{onClick:function(){return r(t)},className:j,children:[Object(l.jsx)("div",{className:"propic",children:Object(l.jsx)("img",{alt:"not found",src:a})}),Object(l.jsxs)("div",{className:b,children:[Object(l.jsx)("div",{className:"textname",children:n}),Object(l.jsx)("div",{className:"messagepreview",children:void 0!==c&&null!==c&&void 0!==c.message&&null!==c.message?c.message:"undefined"})]}),Object(l.jsx)("div",{className:x,children:void 0!==c&&null!==c&&void 0!==c.hour&&null!==c.hour?c.hour:"00:00"})]})}),O=n(138),v=(n(103),O.a.Search),g=function(){return Object(l.jsx)("div",{className:"searchbox",children:Object(l.jsx)(v,{placeholder:"input search text",enterButton:!0})})},x=(n(104),function(e){var t=e.onClick,n=e.chatsList,s=function(e){var s;n.forEach((function(t){!0===t.selected&&(t.selected=!1),t.chatId===e&&(t.selected=!0,s=t)})),t(s)};return Object(l.jsxs)("div",{className:"sidebar",children:[Object(l.jsx)(g,{}),void 0!==n&&n.map((function(e,t){return Object(l.jsx)(b,{onClick:s,id:e.chatId,messages:e.messages,name:e.name,lastMessage:e.lastMessage,img:e.img,selected:e.selected},t)}))]})}),p=n(82),N=n.n(p),y=(n(134),n(135),function(){return Object(l.jsx)("div",{className:"splashBox"})}),S=function(e){var t=e.port,n=e.url,c=Object(s.useState)({}),a=Object(o.a)(c,2),i=a[0],d=a[1],u=Object(s.useState)([]),j=Object(o.a)(u,2),f=j[0],m=j[1],b=Object(s.useState)(null),O=Object(o.a)(b,2),v=O[0],g=O[1],p=Object(s.useState)(""),S=Object(o.a)(p,2),I=S[0],C=S[1];Object(s.useEffect)((function(){null!==v&&(v.on("connect",(function(){C(v.io.engine.id)})),v.on("message",(function(e){console.log("Ho ricevuto",e),R(f,e.data.chatId)?T(D,f,e):E(e),m(Object(r.a)(f))})))}),[v]),Object(s.useEffect)((function(){null!==v&&v.emit("join",I),console.log("Connected with id",I,"!")}),[I,v]),Object(s.useEffect)((function(){g(N.a.connect(n+":"+t))}),[n,t]);var E=function(e){f.push(w(e.data,!1))},T=function(e,t,n){var s=e(t,n.data.chatId);n.data.payload.isSended=!1,s.lastMessage=n.data.payload,s.messages.push(n.data.payload)},k=function(){var e=new Date,t=e.getHours(),n=e.getMinutes();return B(t)+":"+B(n)},B=function(e){return e<10?"0"+e:e},M=function(e,t,n){return{hour:k(),type:e,isSended:t,message:n}},w=function(e,t){var n=M(e.payload.type,t,e.payload.message,e.payload.hour);return{sensorType:e.sensorType,chatId:e.chatId.toString(),name:e.name,img:e.img,lastMessage:n,selected:!1,messages:[n]}},R=function(e,t){return e.filter((function(e){return void 0!==e})).some((function(e){return e.chatId===t}))},D=function(e,t){return e.filter((function(e){return void 0!==e})).filter((function(e){return e.chatId===t}))[0]},P=function(e,t){D(f,e).messages.push(M("text",!0,t)),m(Object(r.a)(f)),v.emit("message",function(e,t,n){return{userId:I,chatId:e,payload:{hour:k(),type:n,message:t}}}(e,t,"text"))};return Object(l.jsxs)("div",{className:"chat",children:[Object(l.jsx)(x,{chatsList:f,onClick:function(e){d(e)}}),function(e){return void 0!==e&&e.selected?Object(l.jsx)(h,{sensorType:e.sensorType,onSend:P,chatId:e.chatId,name:e.name,messages:e.messages}):Object(l.jsx)(y,{})}(i)]})};var I=function(){var e=document.getElementById("root");return Object(l.jsx)(S,{url:e.getAttribute("url"),port:e.getAttribute("port")})},C=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,140)).then((function(t){var n=t.getCLS,s=t.getFID,c=t.getFCP,a=t.getLCP,i=t.getTTFB;n(e),s(e),c(e),a(e),i(e)}))};i.a.render(Object(l.jsx)(c.a.StrictMode,{children:Object(l.jsx)(I,{})}),document.getElementById("root")),C()},91:function(e,t,n){},92:function(e,t,n){},93:function(e,t,n){},98:function(e,t,n){}},[[136,1,2]]]);
//# sourceMappingURL=main.05488b12.chunk.js.map