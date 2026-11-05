"use strict";
const d=window.STUDY;
const slides=[
["燃气轮机 NOₓ 排放预测","给定机组同一小时的九项环境与运行读数，能把烟气氮氧化物浓度估计到多准？","", "276ds-group3 · Jiawei Xia · Rongqian Zhang · Bowen Xie · Zhuoqun Yang"],
["五年的记录怎样使用","2011–2014 年的 29,349 条记录用于学习。2015 年按顺序等分为验证与测试两段，各 3,692 条。先通过验证选择参数，再一次性评价测试段。","","输入为 AT、AP、AH、AFDP、GTEP、TIT、TAT、TEY、CDP。排除同时测得的 CO。"],
["四种模型的跨年表现",d.copy.compare,"model_rmse.svg","MAE 说明典型误差，RMSE 加重较大偏差，R² 衡量相对于均值参照的解释程度。"],
["减少传感器",d.copy.forward,"forward_selection.svg","每一步添加验证误差最低的变量，在路径最优误差 1% 范围内优先选择较小子集。"],
["惩罚系数是否有帮助",d.copy.penalty,"regularization.svg","Ridge 的平方惩罚使系数收缩；Lasso 的绝对值惩罚允许一些系数恰好为零。"],
["实际使用的边界",d.copy.diagnostic,"prediction_diagnostics.svg","同一电厂的后期数据检验了跨时段表现。其他电厂、异常工况以及合规监测用途需要额外验证。"]];
let i=0;function show(){const [t,p,img,n]=slides[i];document.getElementById("slide").innerHTML="<h1>"+t+"</h1><p>"+p+"</p>"+(img?'<img src="figures/'+img+'" alt="'+t+'实验图">':"")+'<p class="small">'+n+"</p>";document.getElementById("page").textContent=(i+1)+" / "+slides.length;document.getElementById("prev").disabled=i===0;document.getElementById("next").disabled=i===slides.length-1;}
function move(k){i=Math.min(slides.length-1,Math.max(0,i+k));show();}
document.getElementById("prev").onclick=()=>move(-1);document.getElementById("next").onclick=()=>move(1);document.addEventListener("keydown",e=>{if(["ArrowRight","ArrowLeft"].includes(e.key)){e.preventDefault();move(e.key==="ArrowRight"?1:-1);}});show();
