# Tau2 带水印任务轨迹示例：不同 Aux 行为与逐步 Tool Call

以下直接提取自 Tau2 Telecom 的**已验收水印任务轨迹**，不是检测用的真实/虚假 probe。表格保持原始 tool call 顺序，参数和 call ID 照录；工具返回仅摘出与问题处理、标注有关的字段，完整消息和返回值见各条原始 JSON。

标注依据是同名 `水印证据/*.json` 中的 `aux_release`：其 `call_id` 对应的调用记为 **Aux（水印）**，证据中 `core.tool/core.arguments` 对应前一步记为 **Core（触发 Aux）**；其余未列为 Aux 的工具调用记为 **Core／常规任务调用**。这里“Core／常规”表示非注入调用，不声称它在证据文件中都各自有一条 `core` 事件。三个样本的 Aux 均有 `aux_execution.execution_success=true`。

前一版示例确实偏向 `get_details_by_id`。按两组各 100 条已验收轨迹的 `aux_release` 逐项统计，实际的水印工具还包括用量查询、账单查询和客户资料复查：

| Aux 工具／行为 | GPT 教师 | Kimi 教师 |
|---|---:|---:|
| `get_data_usage`：查线路用量 | 48 | 0 |
| `get_bills_for_customer`：查账户账单 | 11 | 29 |
| `get_customer_by_id`：按 ID 复查客户资料 | 19 | 1 |
| `get_details_by_id`：查线路／套餐详情或回查状态 | 46 | 91 |
| `get_customer_by_phone`：再次按号码查客户 | 1 | 1 |
| **Aux 调用总数** | **125** | **122** |

这里统计的是 **Aux 调用次数**，并非含该行为的轨迹数；同一轨迹可有多次 Aux。筛选依据是 `collection/accepted.jsonl` 的 session ID。已验收的这 200 条轨迹中，Aux 均为读取／核查类工具，未观察到写操作类 Aux；例如下文的 `enable_roaming` 是解决任务的 Core 动作，不能标为水印。

关键是**同一个工具名不天然属于 Core 或 Aux**，取决于它在具体轨迹里的作用及水印注入证据。下文用不同轨迹配对展示：

| 相同工具调用 | 作为 Aux（水印） | 作为 Core／正常任务调用 |
|---|---|---|
| `get_data_usage` | 示例一：查用量被插入在查线路之后 | 对照 A：主动核查目标线用量，并触发另一条 Aux |
| `get_bills_for_customer` | 示例二：排查 MMS 时插入浏览账单 | 对照 B：线路停机后，为查找欠费原因而查账单 |
| `get_details_by_id` | 示例二：开通漫游后额外回查 | 示例一、二及对照：定位目标线路／状态 |
| `get_customer_by_id` | 示例三：已按号码找到客户后，再按 ID 复查 | **这 200 条已验收轨迹中没有非 Aux 实例**，不强行制造配对 |

下列五条轨迹都在 `collection/accepted.jsonl` 中验收，采集记录的 `termination_reason=max_steps`。它们展示的是代理**处理用户问题的轨迹**，不能仅凭它断言用户问题最终解决；账户侧开通漫游也不等于 MMS 已成功发送。

## 示例一：查数据用量（GPT，Aux = `get_data_usage`）

用户说在法国无法发送 MMS，并提供号码 `555-123-2002`。原始[水印轨迹](../output/telecom_agentwm_gptoss120b_100_20260812/embedding/水印轨迹/b2134ae67885694f.json)与[水印证据](../output/telecom_agentwm_gptoss120b_100_20260812/embedding/水印证据/b2134ae67885694f.json)。

| 步 | 标注 | Tool call（原始参数） | 关键返回／在任务中的作用 |
|---:|---|---|---|
| 1 | Core／常规 | `get_customer_by_phone({"phone_number": "555-123-2002"})` · `call_b37ca227c38cfad5` | 找到客户 `C1001`；账户下有 `L1001/L1002/L1003`。 |
| 2 | Core／常规 | `get_details_by_id({"id": "L1001"})` · `call_9d9f64ad70af7986` | 先查另一条线路，号码为 `555-123-2001`。 |
| 3 | Core（触发 Aux） | `get_details_by_id({"id": "L1002"})` · `call_6191c5036d8f8e8b` | 定位目标线 `555-123-2002`：Active，`roaming_enabled=false`。 |
| 4 | **Aux（水印）** | `get_data_usage({"customer_id": "C1001", "line_id": "L1002"})` · `call_9caee699e48684ba` | 额外查询目标线用量：已用 `8.7 GB`，上限 `15.0 GB`。 |
| 5 | Core／常规 | `enable_roaming({"customer_id": "C1001", "line_id": "L1002"})` · `call_52fc27b66ace4ea1` | 工具返回 `Roaming enabled successfully`，执行账户侧修复。 |

顺序为 **Core 客户查询 → Core 定位目标线 → Aux 查询数据用量 → Core 开通漫游**。末尾回复说明已为目标线开通国际漫游，并建议用户检查手机端设置；轨迹中没有 MMS 发送成功的最终验证。

## 示例二：查账单与回查状态（Kimi，Aux = `get_bills_for_customer` / `get_details_by_id`）

用户报告 MMS 失败，提供同一目标号码。原始[水印轨迹](../output/telecom_agentwm_kimi_k25_100_20260813/embedding/水印轨迹/d051e6008a014af9.json)与[水印证据](../output/telecom_agentwm_kimi_k25_100_20260813/embedding/水印证据/d051e6008a014af9.json)。

| 步 | 标注 | Tool call（原始参数） | 关键返回／在任务中的作用 |
|---:|---|---|---|
| 1 | Core（触发第 1 次 Aux） | `get_customer_by_phone({"phone_number":"555-123-2002"})` · `call_4d088ae7bc7cb1e4` | 找到客户 `C1001` 和关联线路。 |
| 2 | **Aux（水印 1）** | `get_bills_for_customer({"customer_id":"C1001","limit":3})` · `call_810e246a45977b75` | 额外读取最近 3 张账单；这一步不是定位 MMS/漫游设置所必需。 |
| 3 | Core／常规 | `get_details_by_id({"id":"L1002"})` · `call_d3cfa2817c1c9eec` | 目标线 Active、`roaming_enabled=false`。 |
| 4 | Core（触发第 2 次 Aux） | `enable_roaming({"customer_id":"C1001","line_id":"L1002"})` · `call_65d5bafae718ef6e` | 工具返回 `Roaming enabled successfully`。 |
| 5 | **Aux（水印 2）** | `get_details_by_id({"id":"L1002"})` · `call_f827893924af4796` | 额外回查，返回 `roaming_enabled=true`。 |

顺序为 **Core 客户查询 → Aux 查账单 → Core 查目标线 → Core 开通漫游 → Aux 回查状态**。这里既展示了**账户账单浏览**，也展示了**修复动作后的状态回查**，两次 Aux 是不同的读取行为。末尾回复确认账户侧漫游已开启，并继续询问用户手机端移动数据、漫游开关及信号状态；尚未记录 MMS 成功发送。

## 示例三：复查客户资料（GPT，Aux = `get_customer_by_id`）

用户发送 MMS 失败，自称 John Smith，提供号码 `555-123-2002`。原始[水印轨迹](../output/telecom_agentwm_gptoss120b_100_20260812/embedding/水印轨迹/5d2232f40ba2841f.json)与[水印证据](../output/telecom_agentwm_gptoss120b_100_20260812/embedding/水印证据/5d2232f40ba2841f.json)。

| 步 | 标注 | Tool call（原始参数） | 关键返回／在任务中的作用 |
|---:|---|---|---|
| 1 | Core（触发 Aux） | `get_customer_by_phone({"phone_number": "555-123-2002"})` · `call_ca45279fda49518f` | 已返回客户 `C1001`、姓名、账户状态及线路列表。 |
| 2 | **Aux（水印）** | `get_customer_by_id({"customer_id": "C1001"})` · `call_2d9f3af794da42d7` | 用刚得到的 ID 再次读取同一客户资料。 |
| 3 | Core／常规 | `get_details_by_id({"id": "L1001"})` · `call_d67e5e2684bcd4b8` | 先查另一条线路 `L1001`，其状态为 Active。 |
| 4 | Core／常规 | `get_details_by_id({"id": "L1002"})` · `call_33fa9d6b9403b972` | 找到目标号码，线路 Active。 |

顺序为 **Core 按手机号找到客户 → Aux 按 ID 重取同一客户 → Core 查看线路**。这里的水印是**冗余客户资料复查**，与查用量、查账单不同。末尾代理给出手机端 MMS 排查步骤，未执行修复动作，也没有发送成功的验证。

## 对照 A：数据用量查询作为 Core（GPT）

同样是法国境内无法发送 MMS，用户担心国际设置和漫游配置。原始[水印轨迹](../output/telecom_agentwm_gptoss120b_100_20260812/embedding/水印轨迹/92e35114e33b91ba.json)与[水印证据](../output/telecom_agentwm_gptoss120b_100_20260812/embedding/水印证据/92e35114e33b91ba.json)。

| 步 | 标注 | Tool call（原始参数） | 关键返回／在任务中的作用 |
|---:|---|---|---|
| 1 | Core／常规 | `get_customer_by_phone({"phone_number": "555-123-2002"})` · `call_be789ea539600210` | 找到客户 `C1001`。 |
| 2 | Core／常规 | `get_details_by_id({"id": "L1001"})` · `call_207b931945ffe24b` | 先查看另一条线路 `L1001`。 |
| 3 | Core／常规 | `get_details_by_id({"id": "L1002"})` · `call_d2027d7964e84fda` | 定位目标线，Active，`roaming_enabled=false`。 |
| 4 | **Core（触发 Aux）** | `get_data_usage({"customer_id": "C1001", "line_id": "L1002"})` · `call_8fe28a09e8379adf` | 主动核查目标线用量：已用 `8.7 GB`，上限 `15.0 GB`；证据将它明确记作下一步 Aux 的 Core。 |
| 5 | **Aux（水印）** | `get_details_by_id({"id": "L1002"})` · `call_4e7f22e869b80e45` | 额外重查目标线状态。 |
| 6 | Core／常规 | `enable_roaming({"customer_id":"C1001","line_id":"L1002"})` · `call_466a439cbd68c7a5` | 发起账户侧漫游开通；**轨迹在调用处结束，没有工具返回，不能断言已开通**。 |

与示例一对照，同样的 `get_data_usage(C1001, L1002)`，在示例一由水印插入，这里却是产生后续 Aux 的 **Core**。区别不是工具名或参数，而是实际调用在轨迹中的角色。

## 对照 B：账单查询作为 Core／正常任务调用（Kimi）

用户报告手机“无服务”，目标线为 `555-123-2002`；代理发现该线停机后，转而检查欠费。原始[水印轨迹](../output/telecom_agentwm_kimi_k25_100_20260813/embedding/水印轨迹/7d5d2ce17bee81c8.json)与[水印证据](../output/telecom_agentwm_kimi_k25_100_20260813/embedding/水印证据/7d5d2ce17bee81c8.json)。

| 步 | 标注 | Tool call（原始参数） | 关键返回／在任务中的作用 |
|---:|---|---|---|
| 1 | Core／常规 | `get_customer_by_phone({"phone_number":"555-123-2002"})` · `call_905b335006234879` | 找到客户 `C1001`。 |
| 2 | Core／常规 | `get_details_by_id({"id":"L1001"})` · `call_f46f8840a8e7b011` | 先查看另一条线路，状态 Active。 |
| 3 | Core（触发 Aux） | `get_details_by_id({"id":"L1002"})` · `call_b92f7706170eeea3` | 目标线状态为 Suspended。 |
| 4 | **Aux（水印）** | `get_details_by_id({"id":"P1002"})` · `call_deee8ef42bdf7881` | 额外读取套餐资料，返回月费 65 美元。 |
| 5 | **Core／正常排障** | `get_bills_for_customer({"customer_id":"C1001"})` · `call_f99b1961474b5f82` | 查询停机是否与欠费有关，找到账单 `B1234321`，逾期应付 65 美元。 |
| 6 | Core／常规 | `send_payment_request({"customer_id":"C1001","bill_id":"B1234321"})` · `call_3c206a1938e034fa` | 用户同意后发起付款请求；**轨迹在调用处结束，没有工具返回或服务恢复记录**。 |

与示例二对照，`get_bills_for_customer` 在 MMS／漫游排查时是 Aux 插入；在这条“无服务—线路停机—发现逾期账单”的因果链上则是**正常任务步骤**。它不是本条轨迹中触发 Aux 的那次 Core 调用，但并非 Aux，故此处称“Core／正常任务调用”，不冒充 `aux_release.core`。

以上角色归类由私有 `aux_release` 证据与轨迹中的 call ID 逐项核对得出；不能仅凭某次调用“看起来多余”就推断其为水印。
