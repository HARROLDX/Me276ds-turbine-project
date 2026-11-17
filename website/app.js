"use strict";
const D = window.STUDY;
const labels = {ols:"线性回归",random_forest:"随机森林",gradient_boosting:"梯度提升",mlp:"神经网络 MLP",ridge:"Ridge",lasso:"Lasso",forward_ols:"前向选择 OLS"};
const mainModels=Object.keys(D.metrics);
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
$("table").innerHTML='<table><thead><tr><th>模型</th><th>输入数</th><th>MAE</th><th>RMSE</th><th>R²</th></tr></thead><tbody>'+Object.entries(D.metrics).map(([k,m])=>'<tr><td>'+labels[k]+'</td><td>'+m.n_features+'</td><td>'+fmt(m.mae)+'</td><td>'+fmt(m.rmse)+'</td><td>'+fmt(m.r2,3)+'</td></tr>').join('')+'</tbody></table>';
drawBars();drawTrace();
