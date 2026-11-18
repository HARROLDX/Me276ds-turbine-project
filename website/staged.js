"use strict";
const study = window.STAGED;
const byId = Object.fromEntries(study.rows.map(row => [row.id, row]));
const copy = {
  story: ["Can turbine sensors help monitor NOₓ?", "现有传感器能辅助监测 NOₓ 吗？"],
  motivation: ["A plant operator sees an unexpected NOₓ reading. A prediction from routine operating sensors could provide a second signal to investigate whether the change tracks the operating conditions.", "当电厂出现意外的 NOₓ 读数时，运行人员可以结合日常传感器给出的估计，检查变化是否和运行工况一致。"],
  dataset: ["We chose UCI’s gas turbine dataset because it pairs measured emissions with nine usable operating and ambient inputs and preserves chronological order. It has 36,733 hourly aggregated records from one plant in northwestern Türkiye (2011–2015). CO is excluded from the inputs.", "UCI 数据同时提供实测排放、九项环境与运行输入和记录顺序，适合检验模型在后续工况上的表现。数据来自土耳其西北部一座电厂，覆盖 2011–2015 年，共 36,733 条小时聚合记录。CO 不作为输入。"],
  flow: ["Air intake → compression → combustion and turbine → exhaust monitoring", "进气 → 压缩 → 燃烧与涡轮 → 排气监测"],
  air: ["Air intake", "环境与进气"], compressor: ["Compressor", "压气机"],
  turbine: ["Combustion and turbine", "燃烧与涡轮"], exhaust: ["Exhaust measurement", "排气实测"],
  use: ["A future use is screening unexpected readings, prioritizing manual checks and flagging possible sensor faults. Reliable deployment would require prospective validation and routine recalibration. The study estimates same-hour concentration and does not establish causal emission controls.", "未来可用来筛查异常读数、安排人工检查优先级，或提示潜在传感器故障。实际部署需要新时段验证和定期校准。当前研究估计同期浓度，适合作为监测的辅助信号。"],
  source: ["Open the UCI dataset ↗", "查看 UCI 原始数据集 ↗"],
  main: ["Main experiment", "主实验"], compare: ["Four models. Three training windows.", "四种模型，三个训练窗口。"],
  protocol: ["Every window uses the same 3,692 later records from 2015 for testing. Adding years changes both the amount and recency of training data.", "所有模型统一用 2015 后半段的 3,692 条记录测试。扩大窗口同时改变了训练数据量和新近程度。"],
  window: ["Training window", "训练窗口"], metric: ["Test metric", "测试指标"],
  ext1: ["Extension 1", "拓展实验 1"], architecture: ["Narrower, wider and deeper", "变窄、加宽与加深"],
  ext2: ["Extension 2", "拓展实验 2"], inputs: ["Remove one input at a time", "逐一去掉一个输入"],
  ext3: ["Extension 3", "拓展实验 3"], l2: ["How much L2 regularization?", "L2 惩罚多强合适？"],
};
const windows = {
  expanded: ["2011–2014 + first half of 2015", "2011–2014 + 2015 前半段"],
  "2014": ["2011–2014", "2011–2014"], "2013": ["2011–2013", "2011–2013"],
};
const modelNames = {
  ols: ["Linear regression", "线性回归"], random_forest: ["Random forest", "随机森林"],
  gradient_boosting: ["Gradient boosting", "梯度提升"], mlp: ["MLP", "MLP"],
};
const layout = row => "9 → " + row.params.hidden_layer_sizes.join(" → ") + " → 1";
const score = value => value.toFixed(3);
const windowSelect = $("training-window");
const metricSelect = $("study-metric");
function renderStudy() {
  const zh = $("language").value === "zh";
  const tr = pair => pair[Number(zh)];
  document.querySelectorAll("[data-copy]").forEach(node => {
    node.textContent = tr(copy[node.dataset.copy]);
  });
  const selected = windowSelect.value || "expanded";
  windowSelect.replaceChildren(...["expanded", "2014", "2013"].map(key => new Option(tr(windows[key]), key)));
  windowSelect.value = selected;
  const metric = metricSelect.value;
  const main = study.rows.filter(row => row.stage === "main" && row.window === selected);
  const mainWinner = main.reduce((best, row) => row.rmse < best.rmse ? row : best);
  const domain = study.rows.filter(row => row.stage === "main").map(row => row[metric]);
  const low = Math.min(0, ...domain);
  const high = Math.max(0, ...domain);
  const position = value => 100 * (value-low)/(high-low || 1);
  function table(rows, winner, name) {
    return '<div class="scroll"><table class="study-table"><thead><tr><th>' +
      tr(["Configuration", "配置"]) + '</th><th>' + tr(["Train RMSE", "训练 RMSE"]) +
      '</th><th>'+tr(['Test MAE','测试 MAE'])+'</th><th>'+tr(['Test RMSE ↓','测试 RMSE ↓'])+'</th><th>'+tr(['Test R²','测试 R²'])+'</th></tr></thead><tbody>' +
      rows.map(row => '<tr class="'+ (row.id === winner ? "chosen" : "") +'"><td>'+name(row)+
        '</td>'+["train_rmse","mae","rmse","r2"].map(key => "<td>"+score(row[key])+"</td>").join("")+"</tr>").join("")+
      "</tbody></table></div>";
  }
  $("main-results").innerHTML = main.map(row => {
    const value = row[metric];
    return '<div class="barrow '+(row === mainWinner ? "chosen" : "")+'"><span class="name">'+tr(modelNames[row.model])+
      '</span><span class="bartrack"><span class="barfill" style="position:absolute;left:'+position(Math.min(value,0))+
      '%;width:'+Math.abs(position(value)-position(0))+'%"></span></span><strong>'+score(value)+'</strong></div>';
  }).join("") + table(main, mainWinner.id, row => tr(modelNames[row.model]));
  const best = byId[study.best_main];
  $("window-detail").textContent = tr([
    study.windows[selected].toLocaleString()+" training records. Lowest RMSE across windows: "+tr(modelNames[best.model])+" · "+tr(windows[best.window])+" · "+score(best.rmse)+" mg/m³.",
    "训练 "+study.windows[selected].toLocaleString()+" 条。跨窗口最低 RMSE："+tr(modelNames[best.model])+" · "+tr(windows[best.window])+" · "+score(best.rmse)+" mg/m³。"
  ]);
  const base = byId[study.mlp_base], arch = byId[study.best_architecture], inputs = byId[study.best_inputs];
  $("architecture-copy").textContent = tr([
    "Starting from the best MLP window ("+tr(windows[base.window])+"), keep nine inputs and α = 0.01. The lowest test RMSE is "+score(arch.rmse)+" mg/m³ for "+layout(arch)+".",
    "采用 MLP 表现最好的窗口（"+tr(windows[base.window])+"），固定九项输入与 α = 0.01。"+layout(arch)+" 的测试 RMSE 最低，为 "+score(arch.rmse)+" mg/m³。"
  ]);
  $("architecture-results").innerHTML = table(study.rows.filter(row => row.stage === "architecture"), arch.id, layout);
  const inputsName = row => row.stage === "inputs" ? tr(["Drop ", "去掉 "])+row.label : tr(["All 9 inputs", "全部 9 项"]);
  $("inputs-copy").textContent = tr([
    "Keep the selected architecture. Refit nine eight-input variants and retain the full-input reference. Lowest RMSE: "+inputsName(inputs)+".",
    "固定选出的结构，重训九种八输入组合，同时保留九输入参照。最低 RMSE 配置："+inputsName(inputs)+"。"
  ]);
  $("inputs-results").innerHTML = table([arch,...study.rows.filter(row => row.stage === "inputs")], inputs.id, inputsName);
  const l2 = byId[study.best_l2];
  $("l2-copy").textContent = tr([
    "Keep the selected inputs and architecture and compare three L2 penalties. Lowest test RMSE: "+score(l2.rmse)+" mg/m³ at α = "+l2.params.alpha+".",
    "固定选出的输入与网络结构，比较三档 L2 惩罚。测试 RMSE 最低为 "+score(l2.rmse)+" mg/m³，对应 α = "+l2.params.alpha+"。"
  ]);
  $("l2-results").innerHTML = table(study.rows.filter(row => row.stage === "l2"), l2.id, row => "α = "+row.params.alpha);
}
windowSelect.addEventListener("change", renderStudy);
metricSelect.addEventListener("change", renderStudy);
$("language").addEventListener("change", renderStudy);
renderStudy();
