"use strict";
const D = window.STUDY;
const labels = {ols:"线性回归",random_forest:"随机森林",gradient_boosting:"梯度提升",mlp:"神经网络 MLP",ridge:"Ridge",lasso:"Lasso",forward_ols:"前向选择 OLS"};
const mainModels=["ols","random_forest","gradient_boosting","mlp"];
const $ = id => document.getElementById(id);
const fmt = (value, places=2) => Number(value).toFixed(places);
function drawBars() {
  const metric=$("metric").value, rows=mainModels.map(k=>[k,D.metrics[k][metric]]);
  const low=Math.min(0,...rows.map(r=>r[1])), high=Math.max(metric==="r2"?1:0,...rows.map(r=>r[1]));
  const position=v=>100*(v-low)/(high-low || 1);
  $("bars").innerHTML=rows.map(([k,v])=>'<div class="barrow '+(k===D.winner?'chosen':'')+'"><span class="name">'+labels[k]+'</span><span class="bartrack"><span class="barfill" style="position:absolute;left:'+position(Math.min(v,0))+'%;width:'+Math.abs(position(v)-position(0))+'%"></span></span><strong>'+fmt(v,metric==="r2"?3:2)+'</strong></div>').join("");
  $("metric-note").textContent={rmse:"测试集 RMSE（mg/m³）越小越好。平方项会放大少数较大的误差。",mae:"测试集 MAE（mg/m³）越小越好。它表示单条记录平均偏离实测浓度多少。",r2:"测试集 R² 越大越好。零对应始终预测该测试集平均值的参照水平。"}[metric]+" 深色条代表测试 RMSE 最低的 MLP。";
}

function drawTrace() {
  const start=Number($("window").value), key=$("trace-model").value, n=80;
  const a=D.series.NOX.slice(start,start+n), b=D.series[key].slice(start,start+n), all=a.concat(b);
  const lo=Math.floor(Math.min(...all)/10)*10,hi=Math.ceil(Math.max(...all)/10)*10;
  const W=780,H=245,L=55,R=16,T=24,B=38, x=i=>L+i*(W-L-R)/(n-1), y=v=>T+(hi-v)*(H-T-B)/(hi-lo || 1);
  const path=values=>values.map((v,i)=>(i?"L":"M")+x(i).toFixed(2)+" "+y(v).toFixed(2)).join(" ");
  let svg='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="实测与预测浓度折线图"><g font-family="system-ui,sans-serif" font-size="12" fill="#5b6775"><text x="5" y="14">mg/m³</text>';
  for(let v=lo;v<=hi;v+=10){svg+='<line x1="'+L+'" y1="'+y(v)+'" x2="'+(W-R)+'" y2="'+y(v)+'" stroke="#e2e7ed"/><text x="'+(L-10)+'" y="'+(y(v)+4)+'" text-anchor="end">'+v+'</text>';}
  [0,39,79].forEach(i=>{svg+='<text x="'+x(i)+'" y="'+(H-12)+'" text-anchor="middle">'+(start+i+1)+'</text>';});
  svg+='<path d="'+path(a)+'" fill="none" stroke="#243f62" stroke-width="2"/><path d="'+path(b)+'" fill="none" stroke="#bd7950" stroke-width="2" stroke-dasharray="5 2"/></g></svg>';
  $("line-chart").innerHTML=svg; $("window-value").textContent=(start+1)+"–"+(start+n)+" 条";
  const mae=a.reduce((s,v,i)=>s+Math.abs(v-b[i]),0)/n;
  $("trace-note").textContent="横轴为测试集内顺序编号。当前窗口 MAE 为 "+fmt(mae)+" mg/m³，全测试集 MAE 为 "+fmt(D.metrics[key].mae)+" mg/m³。";
}
$("comp-copy").textContent=D.copy.compare; $("failure").textContent=D.copy.diagnostic;
$("metric").addEventListener("change",drawBars);
$("trace-model").innerHTML=Object.keys(D.metrics).map(k=>'<option value="'+k+'">'+labels[k]+'</option>').join("");
$("trace-model").value=D.winner; $("trace-model").onchange=drawTrace; $("window").oninput=drawTrace;
$("table").innerHTML='<table><thead><tr><th>模型</th><th>输入数</th><th>MAE</th><th>RMSE</th><th>R²</th></tr></thead><tbody>'+mainModels.map(k=>{const m=D.metrics[k];return '<tr><td>'+labels[k]+'</td><td>'+m.n_features+'</td><td>'+fmt(m.mae)+'</td><td>'+fmt(m.rmse)+'</td><td>'+fmt(m.r2,3)+'</td></tr>';}).join('')+'</tbody></table>';
drawBars();drawTrace();

const sensorLabels={AT:"环境温度",AP:"环境压力",AH:"环境湿度",AFDP:"过滤器压差",GTEP:"轮机排气压力",TIT:"涡轮入口温度",TAT:"涡轮后温度",TEY:"涡轮发电量",CDP:"压气机排气压力"};
function showFeatures(reduced) {
  $("all-sensors").setAttribute("aria-pressed",String(!reduced));
  $("less-sensors").setAttribute("aria-pressed",String(reduced));
  $("sensor-grid").innerHTML=Object.entries(sensorLabels).map(([k,label])=>'<div class="sensor '+(reduced&&k==="CDP"?"omitted":"")+'"><b>'+k+'</b><span>'+label+'</span><small>'+(reduced&&k==="CDP"?"本组合省去":"保留输入")+'</small></div>').join("");
  const m=D.metrics[reduced?"forward_ols":"ols"];
  $("feature-rmse").textContent=fmt(m.rmse,3);
  $("feature-message").textContent=reduced?"使用 8 项输入，测试 RMSE 下降 "+fmt(D.metrics.ols.rmse-m.rmse,3)+" mg/m³（"+fmt(100*(1-m.rmse/D.metrics.ols.rmse),2)+"%）。":"全部 9 项输入的线性基线。切换到八输入组合，查看精度与输入数量的变化。";
}
$("all-sensors").onclick=()=>showFeatures(false);
$("less-sensors").onclick=()=>showFeatures(true);
function drawRegularization(){
 const metric=$("reg-metric").value,keys=["ols","ridge","lasso"],values=keys.map(k=>D.metrics[k][metric]);
 const span=Math.max(...values)-Math.min(...values),pad=Math.max(span*.5,.002);
 const lo=Math.min(...values)-pad,hi=Math.max(...values)+pad;
 const x=v=>140+(v-lo)/(hi-lo)*510;
 let svg='<svg viewBox="0 0 780 235" role="img" aria-label="线性回归、Ridge 和 Lasso 测试指标点图"><g font-family="system-ui,sans-serif" font-size="14" fill="#4b5e75">';
 for(let i=0;i<5;i++){const v=lo+(hi-lo)*i/4,px=x(v);svg+='<line x1="'+px+'" x2="'+px+'" y1="20" y2="185" stroke="#dce4ee"/><text x="'+px+'" y="212" text-anchor="middle">'+fmt(v,3)+'</text>';}
 keys.forEach((k,i)=>{const y=48+i*56;svg+='<text x="8" y="'+(y+5)+'">'+labels[k]+'</text><line x1="140" x2="650" y1="'+y+'" y2="'+y+'" stroke="#edf1f6"/><circle cx="'+x(values[i])+'" cy="'+y+'" r="7" fill="'+["#35577e","#8171b7","#16847e"][i]+'"/><text x="685" y="'+(y+5)+'">'+fmt(values[i],3)+'</text>';});
 $("reg-chart").innerHTML=svg+'</g></svg>';
 $("reg-caption").textContent=metric==="r2"?"横轴为测试 R²，越大越好。":"横轴为测试 "+metric.toUpperCase()+"（mg/m³），越小越好。";
}
$("reg-metric").onchange=drawRegularization;
showFeatures(false);drawRegularization();
