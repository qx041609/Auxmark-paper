# 当前检测与可疑 Trace 排名算法

本文只描述当前实际实现。全局检测和 trace 排名回答不同问题：前者判断一批 probe 是否存在真实侧优势，后者在 100 条候选 trace 中排序、评估能否优先找回已知 W50。trace 排名不会改变全局检测的 p 值。

## 1. Probe 命中定义

每次成功释放的 Aux 行为形成一张 release card，并派生真实条件 probe 与虚假 Core 条件 probe。回放产生的工具调用有两级命中：

- `tool_hit`：工具名等于期望工具；
- `full_hit`：工具名命中，并且期望参数均存在、参数值匹配且调用可被确定性解析；
- `tool_only = tool_hit and not full_hit`。

回放错误按未命中处理。影子 Aux 和参数相似度不进入当前 trace 排名分数。

## 2. Card 级全局检测

对每张 card `c`，分别统计真实与虚假 probe 的完整命中数：

$$R_c=\#\text{real full-hit},\qquad V_c=\#\text{virtual full-hit}$$

若 `R_c > V_c` 记为 `real_win`，若 `R_c < V_c` 记为 `fake_win`，相等记为 `tie`。令真实胜和虚假胜数量分别为 `w`、`f`，只用 `n=w+f` 张非平局 card 做单侧精确符号检验：

$$p_{sign}=P\{X\ge w\},\qquad X\sim\operatorname{Binomial}(n,0.5)$$

总体 probe 命中率是描述性统计；正式显著性来自 card 级配对方向，不能把同一 card 派生的多个 probe 当成彼此独立的样本。

## 3. Trace 级四特征

对一个 cohort 的每个学生模型分别统计每条 trace：

| 特征 | 定义 |
|---|---|
| `R_full` | 真实 probe 的 `full_hit` 数 / 真实 probe 总数 |
| `V_full` | 虚假 probe 的 `full_hit` 数 / 虚假 probe 总数 |
| `R_tool_only` | 真实 probe 中 `tool_hit and not full_hit` 的数量 / 真实 probe 总数 |
| `V_tool_only` | 虚假 probe 中 `tool_hit and not full_hit` 的数量 / 虚假 probe 总数 |

每个特征都只在同一 cohort、同一学生模型的候选 trace 内转换为平均分位秩：

$$Q(x_i)=\frac{\operatorname{rank}_{average}(x_i)}{N+1}$$

并列原始值取平均秩。各模型独立变换和排序，不合并 trace 分数，也不做跨模型投票。

## 4. 当前冻结分数与排序

当前冻结权重来自保存的网格搜索结果 `最优参数.json`：

$$S_i=Q(R_{full,i})-0.26Q(V_{full,i})+0.08Q(R_{tool\_only,i})-0.08Q(V_{tool\_only,i})$$

按 `S` 降序排列。同分时严格按以下顺序打破：

1. 虚假完整命中率更低；
2. 真实完整命中率更高；
3. trace ID 字典序更靠前。

所有用于排序的 `S` 会先四舍五入到 12 位再判断同分，这与实现中的 `numpy.lexsort` 一致。

## 5. Precision 与跨模型汇总

W50 标签只在排序完成后用于审计：

$$Precision@K=\frac{\text{前 K 条中属于已知 W50 的条数}}{K},\quad K\in\{10,15,20,25,30\}$$

每个学生模型先独立得到五个 precision；cohort 表中的单元格是四个学生模型 precision 的算术平均。六组总体平均再对六个 cohort 做算术平均。当前版本不报告 Top-50，也不报告 recall。

## 6. 权重选择规则

网格搜索按以下目标依次选择参数：

1. 最大化 30 个 `cohort × K` 四模型平均 precision 中的最低值；
2. 最小化真实与虚假两个 tool-only 权重之差的绝对值；
3. 最大化上述 30 项 precision 的算术平均；
4. 完全相同时优先两位小数权重，再优先权重和更小的候选。

当前共评估 461,872 组候选，选中 `(虚假 full 惩罚, 真实 tool-only 奖励, 虚假 tool-only 惩罚)=(0.26,0.08,0.08)`。这是对现有六组结果的回顾性选择；新 cohort 应冻结公式后单独验证。

## 7. 数据完整性与实现位置

程序在计算前校验 60 份输入文件的 SHA-256，并要求每组正式 W100、probe labels、回放结果和 W50 标签能够对齐；校验失败会停止，不会静默使用部分数据。Telecom 的失败/重试快照按正式 accepted `task_id + session_id` 过滤。

- card 级命中与符号检验：`code/检测.py`
- trace 排名实现：`output/识别准确率模拟/当前Trace识别_最终版/最优FullTool排序.py`
- 参数与输入哈希：`output/识别准确率模拟/当前Trace识别_最终版/最优参数.json`
- 六组及逐模型结果：`output/识别准确率模拟/当前Trace识别_最终版/六套C0_总览.md`
- 逐 trace 排名：`output/识别准确率模拟/当前Trace识别_最终版/逐模型排名.jsonl`

以上定义不修改原始训练、probe 或回放数据。
