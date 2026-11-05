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
  $("metric-note").textContent={rmse:"测试集 RMSE（mg/m³）越小越好。平方项会放大少数较大的误差。",mae:"测试集 MAE（mg/m³）越小越好。它表示单条记录平均偏离实测浓度多少。",r2:"测试集 R² 越大越好。零对应始终预测该测试集平均值的参照水平。"}[metric]+" 深色条代表验证阶段选出的主模型。";
}
function extension(name) {
  const forward=name==="forward"; $("forward").setAttribute("aria-pressed",String(forward)); $("penalty").setAttribute("aria-pressed",String(!forward));
  $("extension-title").textContent=forward?"逐个加入传感器":"对线性系数施加惩罚";
  $("ext-copy").textContent=forward?D.copy.forward:D.copy.penalty;
  $("ext-img").src="figures/"+(forward?"forward_selection.svg":"regularization.svg");
  $("ext-img").alt=forward?"验证 RMSE 随传感器数量的变化":"Ridge 和 Lasso 的验证误差随惩罚强度的变化";
  $("ext-note").textContent=forward?"纵轴是验证误差。选择落在最优值 1% 范围内的最小子集。":"横轴采用对数刻度。两种方法各自在自己的参数网格上选择验证 RMSE 最低的一点。";
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
$("metric").addEventListener("change",drawBars); $("forward").onclick=()=>extension("forward");$("penalty").onclick=()=>extension("penalty");
$("trace-model").innerHTML=Object.keys(D.metrics).map(k=>'<option value="'+k+'">'+labels[k]+'</option>').join("");
$("trace-model").value=D.winner; $("trace-model").onchange=drawTrace; $("window").oninput=drawTrace;
$("table").innerHTML='<table><thead><tr><th>模型</th><th>阶段</th><th>MAE (mg/m³)</th><th>RMSE (mg/m³)</th><th>R²</th></tr></thead><tbody>'+Object.keys(D.metrics).flatMap(k=>[["训练",D.choices[k].train],["验证",D.choices[k].validation],["测试",D.metrics[k]]].map(([s,m])=>'<tr><td>'+labels[k]+'</td><td>'+s+'</td><td>'+fmt(m.mae)+'</td><td>'+fmt(m.rmse)+'</td><td>'+fmt(m.r2,3)+'</td></tr>')).join("")+'</tbody></table>';
drawBars();extension("forward");drawTrace();
