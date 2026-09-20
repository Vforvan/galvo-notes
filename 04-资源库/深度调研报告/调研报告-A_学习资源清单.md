# 振镜（Galvanometer Scanner）与 XY2-100 协议 —— 学习资源调研报告

> **调研对象**：中文母语的工程师实习生
> **调研日期**：本次会话
> **调研方式**：`web_search` 中英文双语检索（约 30 组查询）

---

## ⚠️ 关于「链接是否有效」的重要说明（请先阅读）

本次调研环境中，**`web_fetch` 工具对全部外部域名均返回失败**，错误统一为
`URL hostname "..." resolves to a non-public IP address`
（实测包括 `github.com`、`blog.csdn.net`、`www.bilibili.com`、`www.scanlab.de`、`www.icourse163.org`、`en.wikipedia.org` 等）。

**这意味着：报告中的每一个 URL 我都无法通过直接抓取来验证其可访问性。**

因此：

- 下面所有链接**均来自 `web_search` 的真实返回结果**（即搜索引擎已收录这些页面），**我没有凭空编造任何一条 URL**；
- 但「能否打开」我**无法保证**。表格中不再逐行标注"链接可能失效"，而是统一按以下可信度分级：
  - 🟢 **高可信**：厂商官网 / 大学官方平台 / 政府教育平台（域名稳定，一般长期有效）
  - 🟡 **中可信**：CSDN / 知乎 / 博客园 / 论坛帖（内容可能被删或需登录）
  - 🔴 **低可信 / 需自行确认**：聚合站、文库、下载站（可能需付费、需登录或已下架）
- 视频类资源（B 站/YouTube）若原 UP 主删除视频，链接会失效，请以**标题 + UP 主名**为检索关键词自行复查。

---

## 一、视频课程（中文视频平台）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 视频教程：运动控制器激光振镜控制 | https://www.bilibili.com/video/BV14K4y1n7At/ | 中文 | 免费 | 中级 | **本清单中与 XY2-100 最直接相关的视频**。正运动技术官方发布，讲 ZMC420SCAN 控制器 + ZDevelop 软件通过 **XY2-100 协议**控制振镜轴，含运动与激光开关配合。播放 1.1 万、收藏 425。UP 主：正运动技术 |
| 【研讨会公开课】振镜激光扫描方案：设计和应用 | https://www.bilibili.com/video/av804370353/ | 中文（Thorlabs 官方中文研讨会） | 免费 | 中级 | Thorlabs 测量系统部门工程总监 Brian Candiloro 主讲：闭环振镜系统工作原理、振镜操控光束的特征、在激光扫描系统中的应用。**体系化程度最高的中文振镜原理视频** |
| 光电子制造：振镜 | https://www.bilibili.com/video/BV1VdrVYMEfF/ | 中文 | 免费 | 初级 | Thorlabs 索雷博官方号。讲振镜用于光束操控、成像、激光打标与加工；扫描头、反射镜、驱动器选型；镀膜选项 |
| 激光振镜工作原理 | https://www.bilibili.com/video/BV1acmuB8E99/ | 中文 | 免费 | 初级 | UP 主「阿勇做激光设备」（15 年激光设备厂家）。动画讲振镜偏转原理。播放 9677、收藏 119 |
| 激光振镜科普，分享我对激光振镜的理解 | https://www.bilibili.com/video/BV1jomdBBEze/ | 中文 | 免费 | 初级 | UP 主「BD黑色蒲公英」（电子/激光雕刻机爱好者）。从电子爱好者角度的振镜理解。播放 1.0 万、收藏 290 |
| 振镜教程（视频合辑） | https://www.bilibili.com/video/av237604282/ | 中文 | 免费 | 初级 | 合辑页，聚合多条：振镜怎么调整激光线路、场镜作用与原理、自制激光振镜系统、3D 动态聚焦系统内部原理、振镜内部结构、激光扫描共聚焦显微镜成像原理 |
| [硬件] 自制激光振镜 | https://www.bilibili.com/video/BV1sy4y1r7Xv/ | 中文 | 免费 | 中级 | UP 主「Brian-Dead」，历时 4 个月换两套方案做出雏形。播放 2.7 万。偏硬件 DIY 实战 |
| 自制激光振镜系统 | https://www.bilibili.com/video/BV1qh4y1x7YJ/ | 中文 | 免费 | 中级 | UP 主「电路砖家」，步进电机激光振镜系统。播放 3.2 万、收藏 396 |
| 打标机振镜基础知识教学指导 | https://www.bilibili.com/video/BV1yzCQBfEDk/ | 中文 | 免费 | 初级 | 面向设备操作/调试人员。含打标参数（频率、速率、功率）、填充教程、3 种调焦方法、图片转 DXF |
| DIY 振镜激光打标机 激光雕刻 使用教程 脱机操作 | https://www.bilibili.com/video/BV1EiTvzcEVL/ | 中文 | 免费 | 初级 | DIY 5W 振镜激光雕刻机实操，脱机操作指南 |
| 激光打标教学入门和实战技巧 | https://www.bilibili.com/cheese/play/ss132900091 | 中文 | **付费**（B 站课堂，可能有试看） | 初级 | 结构化付费课：激光技术基础与分类、设备结构（**含振镜系统**）、参数设置 |
| 激光原理与技术【厦门大学】【国家级精品课】【全30讲】 | https://www.bilibili.com/video/BV1t2RhY5EZd/ | 中文 | 免费 | 中级 | 国家精品课搬运，30 讲全集，含资料。补齐光学/激光物理基础 |
| Thorlabs 索雷博 B 站官方空间 | https://space.bilibili.com/412643769/upload/video | 中文 | 免费 | 中～高级 | 持续更新光电类视频，含振镜、光束操控、光电测量系列 |
| 激光打标教学指导 B 站空间 | https://space.bilibili.com/1397128057 | 中文 | 免费 | 初级 | 20 年激光行业经验 UP 主，专答激光打标软硬件问题，适合调试岗位 |
| 振镜工作原理（YouTube） | https://www.youtube.com/watch?v=xWYjiJEFtOA | 英文（画面为主） | 免费 | 初级 | 振镜工作原理动画 |
| RAYGUIDE – Click & Teach（YouTube） | https://www.youtube.com/watch?v=GSMM9M3XT-s | 英文 | 免费 | 中级 | RAYLASE 官方软件教学：振镜系统标定、加工任务创建与执行 |

> **说明**：中国大学 MOOC / 网易云课堂 / 腾讯课堂 平台**未检索到以「振镜」为独立主题的成体系视频课**。腾讯课堂已转型为 T-Learning（腾讯战略伙伴内部学习平台，不对外开放），故不列入正式推荐。振镜相关内容主要以「激光打标机操作培训」形式散落在 B 站和抖音。

---

## 二、图文教程（中文技术博客）

### 2.1 XY2-100 协议专项（核心中的核心）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| XY2-100 协议详解：光学振镜控制接口与拓展应用 | https://blog.csdn.net/CrowLWZ/article/details/109050977 | 中文 | 免费 | 中级 | 阅读 1.7 万、收藏 63。硬件引脚定义、数据传输定义、拓展讨论。**中文里引用率最高的 XY2-100 入门文** 🟡 |
| XY2-100 振镜控制协议（博客园） | https://www.cnblogs.com/xymotion/p/12987507.html | 中文 | 免费 | 中级 | 差分传输机制、DB25 插头 / IDC 连接器物理接口、数据帧时序、BACK(STATUS) 信号。博客园无广告，阅读体验好 🟡 |
| xy2-100 协议驱动原理，激光数字振镜驱动控制，基于 STM32F103 开发 | https://blog.csdn.net/2501_93091150/article/details/150452592 | 中文 | 免费 | 高级 | 从激光振镜控制原理、接口引脚定义、协议时序到 **Verilog 代码实现**，参考 RAYLASE 官方文档。**含代码，实战价值高** 🟡 |
| XY2-100 协议解析 | https://www.e-com-net.com/article/1888470847899889664.htm | 中文 | 免费 | 高级 | 同上系列：振镜工作原理 + 引脚定义 + 时序 + Verilog 实现 🔴 |
| 从原理到实践：手把手教你用 XY2-100 协议控制激光振镜（含引脚定义图） | https://blog.csdn.net/weixin_30505225/article/details/159307426 | 中文 | 免费 | 中级 | 硬件接口定义 → 时序分析 → Verilog 硬件逻辑实现，含优化策略 🟡 |
| XY2-100 振镜控制协议详解：从时序到调试实战 | https://blog.csdn.net/weixin_29179311/article/details/164417955 | 中文 | 免费 | 中级 | 面向嵌入式工程师：标准帧格式、偶校验机制、高精度数据通信控制机制与实现要点 🟡 |
| 在 i.MX RT10xx 使用 FlexIO 实现 XY2-100 振镜控制协议 | https://www.elecfans.com/d/2084844.html | 中文 | 免费 | 高级 | **电子发烧友（NXP 官方供稿）**：用 i.MX RT1050 的 FlexIO 外设模拟 XY2-100，含逻辑分析仪实测波形。**有示波器波形对比，调试参考价值极高** 🟡 |
| STM32 XY2-100 技术专题 | https://m.elecfans.com/zt/365074/ | 中文 | 免费 | 中级 | 电子发烧友专题聚合页，汇总 STM32 + XY2-100 方案（点速率可达几十万～上百万点/秒）、DMA/定时器实现思路 🟡 |
| XY2-100 Specification（Scribd 文档） | https://www.scribd.com/document/941573319/Xy2-100-Specification | 英文（协议原文） | 需注册/可能付费 | 高级 | 协议规格说明：DB25 接口、SYNC/CLK 成帧、标准模式 16-bit 偶校验、增强模式 18-bit 奇校验 🔴 |
| 基于 XY2-100 协议的振镜控制转换板的设计与实现 | https://www.zhangqiaokeyan.com/academic-journal-cn_detail_thesis/0201293138765.html | 中文 | 付费/部分免费 | 高级 | 王文毅、吕勇、陈青山、孔凡辉。DSP F2812 为核心处理器的振镜控制转换板设计（期刊论文）🟡 |
| STM32 控制 XY2-100 振镜协议全攻略：从硬件连接到代码实现 | https://wenku.baidu.com/view/83ada46e0f4c2e3f5727a5e9856a561253d3215b.html | 中文 | 部分免费/需下载券 | 中级 | XY2-100 与 SL2-100 协议对比、常见调试问题、协议选择建议 🔴 |
| XY2-100 协议驱动原理（e-com-net 镜像） | https://www.e-com-net.com/article/1888470847899889664.htm | 中文 | 免费 | 高级 | 同 CSDN 系列文章镜像站 🔴 |

### 2.2 振镜原理 / 系统设计

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 图解扫描振镜 - 激光振镜 - 光学振镜 新手必看 | https://blog.csdn.net/u010440456/article/details/89424686 | 中文 | 免费 | 初级 | 阅读 5.1 万、收藏 190。振镜作为特殊摆动电机的构造、控制电压精确扫描光束、打标与光谱检测应用。**新手首选图文** 🟡 |
| [激光原理与应用-92]：振镜的光路图原理 | https://blog.csdn.net/HiWangWenBing/article/details/138504564 | 中文 | 免费 | 中级 | 阅读 2.4 万、收藏 202。振镜在激光焊接中的光路设计、反射/折射机制、焊接头结构与分类、准直聚焦头、动态聚焦系统、工作距离 🟡 |
| 振镜技术原理与激光加工应用全解析 | https://blog.csdn.net/weixin_29164091/article/details/165391846 | 中文 | 免费 | 中级 | 打标系统五大构成（激光器、扩束镜、振镜模块、场镜、控制系统）；Scanlab RTC6 控制卡 200MHz 编码器输入 🟡 |
| 激光振镜驱动扫描绘画（振镜驱动板原理图） | https://blog.csdn.net/qq_59480567/article/details/141679738 | 中文 | 免费 | 高级 | 伽妮激光振镜测试，验证工作状态与所需资源，含驱动放大电路与控制信号路径 🟡 |
| 高速扫描振镜驱动原理图 | https://blog.csdn.net/gitblog_06695/article/details/142558717 | 中文 | 免费 | 高级 | 高速振镜驱动电路设计精髓，面向光学扫描/激光加工/显示技术研发 🟡 |
| 伺服电机驱动振镜系统：高动态控制方案与英飞凌硬件实践 | https://blog.csdn.net/weixin_42548829/article/details/163872449 | 中文 | 免费 | 高级 | 电流环、速度环、位置环三环闭环反馈；英飞凌硬件实现方案 🟡 |
| 基于 FPGA 的以太网激光振镜控制器设计与实现 | https://blog.csdn.net/gitblog_06737/article/details/148065362 | 中文 | 免费 | 高级 | FPGA + 以太网通信协议 + 激光振镜控制核心原理与整体实现，含可下载 PDF 🟡 |
| 基于立创 EDA 与 Arduino UNO 的振镜式激光打标机 DIY 全攻略 | https://blog.csdn.net/weixin_29025501/article/details/159136369 | 中文 | 免费 | 中级 | 立创 EDA 画控制板 → Arduino UNO + DAC/运放选型 → 固件解析 G 代码 → LightBurn 联调。**端到端 DIY 全流程** 🟡 |
| 激光振镜运动控制实战：基于 ZMC420SCAN 的 C++ 开发指南 | https://blog.csdn.net/weixin_29169505/article/details/158551026 | 中文 | 免费 | 高级 | 开发环境搭建、振镜轴核心配置、PSO 激光同步输出、圆形阵列打标案例、MFC 实现 🟡 |
| 激光振镜控制教程 | https://blog.csdn.net/AGONIiii/article/details/113654470 | 中文 | 免费 | 中级 | 阅读 6.7k、收藏 29。ZMC420SCAN 控制器 + ZDevelop 软件控制振镜，硬件准备、振镜轴与激光控制指令 🟡 |
| 运动控制器激光振镜控制（正运动技术官方） | https://www.zmotion.com.cn/support_info_76.html | 中文 | 免费 | 中级 | 厂商官方技术支持页：视频教程 + 说明文档，激光振镜控制实际效果展示、ZDevelop BASIC 语言开发 🟢 |
| 开放式激光振镜 + 运动控制器（六）：双振镜运动 | https://zmotion.com.cn/support_info_185.html | 中文 | 免费 | 高级 | 振镜轴类型配置（轴类型 21）、速度加减速参数、示波器检测双振镜轨迹 🟢 |
| ZMC420SCAN 激光振镜运动控制器用户手册 V1.6.0（PDF） | https://file.zmotion.com.cn/upload/ZMC420SCAN%E6%BF%80%E5%85%89%E6%8C%AF%E9%95%9C%E8%BF%90%E5%8A%A8%E6%8E%A7%E5%88%B6%E5%99%A8%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8CV1.6.0.pdf | 中文 | 免费 | 中级 | 官方用户手册。**明确写有 XY2-100 振镜协议支持**，是理解"控制器如何驱动振镜"的规范文档 🟢 |
| 激光扫描振镜：从核心原理到高级控制（乘物游心录博客） | https://www.qinwei.fun/posts/laser-galvanometer-scanner-control/ | 中文 | 免费 | 中级 | 个人技术博客"激光基础"系列：光束偏转、闭环伺服、畸变校正、镜台联动（IFOV）🟡 |
| 激光扫描振镜：从核心原理到高级控制（搜狐转载） | https://www.sohu.com/a/960055286_122514390 | 中文 | 免费 | 中级 | 同上内容的新媒体版本，讲系统构成与高级控制策略 🟡 |
| 激光扫描振镜：从核心原理到高级控制（百度文库） | https://wenku.baidu.com/view/9b8ce7a6e618964bcf84b9d528ea81c759f52e0b.html | 中文 | 部分免费 | 中级 | 控制卡（RTC 板）按 XY2-100 协议生成数字指令 → 伺服驱动器；误差计算与 PID 驱动电流生成 🔴 |

### 2.3 知乎（问答 + 专栏）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 如何用 51 单片机基于 XY2-100 协议控制扫描振镜？ | https://www.zhihu.com/question/596454803 | 中文 | 免费 | 高级 | **高价值问答**。详解 GPIO 实现思路：足够高的系统时钟、预算 X/Y 校验位、准备 20bit 数据、按时序生成 clock/sync/channel_xyz、关中断插入 NOP 调时序、示波器验证 setup/hold 🟡 |
| 数字激光振镜是如何工作和接线的？ | https://www.zhihu.com/question/27745444 | 中文 | 免费 | 初级 | 金海创振镜头与控制板卡接线对应关系，XY2-100 驱动板思路：坐标发给控制板，控制板转成时序与同步脉冲 🟡 |
| 振镜激光扫描方案：设计和应用（知乎专栏） | https://zhuanlan.zhihu.com/p/382718035 | 中文 | 免费 | 中级 | Thorlabs 研讨会的**中文图文整理版**。位置传感器集成在电机设计中、闭环伺服提供可预测 LTI 系统、机械角 ±20°、扫描速率几 Hz～几 kHz 🟡 |
| 运动控制卡应用开发教程之激光振镜控制 | https://zhuanlan.zhihu.com/p/337346201 | 中文 | 免费 | 中级 | ZMC420SCAN 支持 XY2-100 协议，支持运动控制与振镜**联合插补运动**；网口连控制器、句柄获取、总线/脉冲控制伺服 🟡 |
| 开放式激光振镜运动控制器的视觉校正振镜精度解决方案 | https://zhuanlan.zhihu.com/p/694699684 | 中文 | 免费 | 高级 | 振镜控制与图形校正两个技术层；视觉校正提升振镜精度 🟡 |
| Scanlab 和瑞镭振镜参数对比 | https://zhuanlan.zhihu.com/p/1953390527287399463 | 中文 | 免费 | 中级 | **选型参考**：SCANLAB（SL2-100 协议）vs RAYLASE（XY2-100 协议）光学偏转角、光学分辨率对比 🟡 |
| 激光打标机光路调整完整步骤 | https://zhuanlan.zhihu.com/p/2073197592473876123 | 中文 | 免费 | 初级 | 现场调试向：90% 以上"光路不对"实为工作面未在焦距上，何时才需开打标头调振镜内部镜片 🟡 |
| 有哪些讲激光应用比较深入全面的书籍或者文献推荐？ | https://www.zhihu.com/question/53533969 | 中文 | 免费 | 中级 | 激光教材推荐与学习路径：陈鹤鸣《激光原理及应用》等三本书特点对比与阅读顺序建议 🟡 |
| 推荐给光学工程师们的六本专业书籍 | https://zhuanlan.zhihu.com/p/658303390 | 中文 | 免费 | 中级 | 光学工程师书单 🟡 |

### 2.4 论坛帖（EEWorld / 电子发烧友 / 21ic）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 拆解激光打标机的扫描振镜看看内部电路 | https://bbs.eeworld.com.cn/thread-1081971-1-1.html | 中文 | 免费 | 中级 | **电子工程世界（EEWorld）「以拆会友」版**。二手扫描振镜实拆：大铁壳 + 2 个电机，直流电阻档实测约 2.5Ω，分析内部电路 🟡 |
| 激光振镜制作方案 | https://bbs.eeworld.com.cn/thread-429060-1-1.html | 中文 | 免费 | 中级 | EEWorld 单片机版，振镜自制方案讨论 🟡 |
| 解析振镜起点爆点问题及解决方案 | https://bbs.elecfans.com/jishu_2388066_1_1.html | 中文 | 免费 | 中级 | **电子发烧友「电机控制」版**。ZMC408SCAN 高性能总线双振镜运动控制器，EtherCAT 总线、最快 500μs 刷新周期。**现场工艺问题排查** 🟡 |
| 21ic 电子技术开发论坛 - 激光标签页 | https://bbs.21ic.com/tags/%E6%BF%80%E5%85%89-1.html | 中文 | 免费 | 中级 | 21ic 激光技术热点、难点讨论与实践经验分享专区 🟢 |
| 21ic 电子技术开发论坛（主站） | https://bbs.21ic.com/ | 中文 | 免费 | 中级 | 2000 年成立，含单片机/嵌入式/DSP/模拟/工控等版块，可用"振镜"关键词站内搜索 🟢 |

---

## 三、大学 / MOOC 课程

### 3.1 中文（中国大学 MOOC / 学堂在线 / 国家平台）

> **诚实说明**：**没有检索到任何一门以「振镜」或「XY2-100」为专题的中文大学课程**。中文高校课程只覆盖到「激光加工」「激光原理」层级。振镜属于工程实践内容，需从上面的视频和图文教程补齐。

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 激光加工技术（浙江工业大学） | https://www.icourse163.org/spoc/course/ZJUT-1460186167 | 中文 | 免费（认证证书付费） | 中级 | 中国大学 MOOC。激光加工成本低、质量高、效率高、可特殊制造；应用于航空航天、汽车、电子、冶金、石化 🟢 |
| 激光加工创新训练（湖南大学） | https://www.icourse163.org/course/HNU-1002608029?tid=1002943029 | 中文 | 免费 | 初级 | 中国大学 MOOC。激光在生活与工业中的应用入门 🟢 |
| 激光原理与技术（厦门大学） | https://www.icourse163.org/spoc/course/XMU-1002710006 | 中文 | 免费 | 中级 | 中国大学 MOOC。方向性、单色性、相干性、高亮度；激光雷达、量子通信、集成电路光刻应用 🟢 |
| 激光原理与技术（电子科技大学） | https://www.icourse163.org/course/UESTC-1003660001?tid=1473162459 | 中文 | 免费 | 中级 | 中国大学 MOOC。光与物质相互作用基本物理过程与机理，光电子学科核心课 🟢 |
| 激光原理与技术（电子科技大学 - 成电慕课） | https://study.uestc.edu.cn/MOOC/index.aspx?courseId=1056 | 中文 | 免费 | 中级 | 光信息科学与工程专业核心课，校内平台 🟢 |
| 激光及其应用（清华大学） | https://www.xuetangx.com/course/THU00001000965 | 中文 | 免费（可选认证） | 中级 | **学堂在线**。激光单纵模选择、速率方程组、激活态能级；**激光加工过程中激光辐射的基本特性**、激光与物质相互作用 🟢 |
| 光学（清华大学） | https://www.xuetangx.com/course/THU07021000313 | 中文 | 免费 | 中级 | 学堂在线。经典光学，波动性（电磁波）深入讨论。补齐振镜背后的光学基础 🟢 |
| 激光加工（超星学习通） | https://mooc1.chaoxing.com/mooc-ans/course/portal/u7XgNj7cJgFj-ILsLXjPeQ== | 中文 | 免费 | 初级 | 激光加工基础、安全操作规程、激光内雕等 🟢 |
| 激光加工 / 工程训练（国家高等教育智慧教育平台） | https://higher.smartedu.cn/course/65aafd53bb5c5a8025652f28 | 中文 | 免费 | 初级 | 教育部官方平台。面向新工科，现代工程训练组成部分，CDIO 理念 🟢 |
| 中国大学 MOOC 主站 | https://www.icourse163.cn/ | 中文 | 免费 | — | 建议站内搜索「激光加工」「激光原理」「光学」🟢 |

### 3.2 国际 MOOC（英文，免费为主）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| NOC: Laser Based Manufacturing（IIT Guwahati） | https://nptel.ac.in/courses/112103312 | 英文 | 免费 | 中级 | **NPTEL**。激光技术在制造、表面工程、仪器仪表中的应用；重点讲原理、特性、类型、监测与控制 🟢 |
| NPTEL 视频课：Laser Based Manufacturing | http://elearn.psgcas.ac.in/nptel/courses/video/112103312/L01.html | 英文 | 免费 | 中级 | 同上课程的逐讲视频（Lecture 1: Lasers in Manufacturing）🟡 |
| NPTEL：Laser Based Manufacturing（DIGIMAT 镜像） | http://acl.digimat.in/nptel/courses/video/112103312/112103312.html | 英文 | 免费 | 中级 | 含 Lecture 4 激光切割操作原理/切缝几何、Lecture 5 材料去除用激光类型与工艺性能参数 🟡 |
| NOC: Laser: Fundamentals and Applications（IIT Kanpur） | https://nptel.ac.in/courses/104104085 | 英文 | 免费 | 中级 | NPTEL。激光基础与应用 🟢 |
| NOC: An Introduction to Lasers and Laser Systems（Homi Bhabha） | https://nptel.ac.in/courses/115101639 | 英文 | 免费 | 初级 | NPTEL。从激光基础讲起，延伸到激光技术的主要发展 🟢 |
| NOC: Fundamentals of Material Processing - I（IIT Kanpur） | https://nptel.ac.in/courses/113104073 | 英文 | 免费 | 中级 | NPTEL。材料加工基础 🟢 |
| NPTEL-NOC IITM（YouTube 频道） | https://www.youtube.com/@nptel-nociitm9240 | 英文 | 免费 | 中级 | NPTEL 官方视频频道 🟢 |
| Fundamentals of Photonics: Quantum Electronics（MIT OCW） | https://ocw.mit.edu/courses/6-974-fundamentals-of-photonics-quantum-electronics-spring-2006/ | 英文 | 免费 | 高级 | **MIT OpenCourseWare**。麦克斯韦电磁波、谐振器与光束、经典射线光学与光学系统、量子光理论、噪声，直至激光与应用 🟢 |
| Photonics & Lasers 课程聚合（Class Central） | https://www.classcentral.com/subject/photonics | 英文 | 免费+付费 | 混合 | 200+ 门光子学与激光在线课程，含免费选项 🟢 |
| Optics 课程列表（Coursera） | https://www.coursera.org/courses?query=optics | 英文 | 免费旁听/付费证书 | 混合 | 光学课程：光的行为、镜头设计、波粒二象性、光学仪器 🟢 |
| Optics 课程列表（edX） | https://www.edx.org/learn/optics | 英文 | 免费旁听/付费证书 | 混合 | 同上，edX 平台 🟢 |
| Semiconductor Photonics Graduate Certificate（CU Boulder） | https://www.coursera.org/certificates/semiconductor-photonics-boulder | 英文 | 付费 | 高级 | 半导体光子学研究生证书：固态光子器件、半导体激光器、光电探测器 🟢 |
| Optics 课程聚合（Class Central） | https://www.classcentral.com/tag/optics | 英文 | 免费+付费 | 混合 | 160+ 门光学课程，标注免费与认证情况 🟢 |

---

## 四、英文资料（厂商培训 / App Note / 白皮书 / 学术）

### 4.1 SCANLAB（XY2-100 协议的事实制定者）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| SCANLAB 官网 | https://www.scanlab.de/en | 英文 | 免费 | 中级 | 全球领先的独立 OEM 扫描头与扫描方案厂商，年产约 4 万台系统 🟢 |
| **Advantages of digital servo amplifiers for control of a galvanometer scanner（SPIE 论文 PDF）** | https://www.scanlab.de/sites/default/files/2020-06/2005-08_spie_meeting_digital_servo_amplifiers.pdf | 英文 | **免费 PDF** | 高级 | ⭐ **强烈推荐**。SCANLAB 官方 SPIE 会议论文。"extended status messages" 需求与工业激光加工的动力学要求如何催生振镜数字伺服控制。**理解数字振镜（含 XY2-100）为何取代模拟振镜的一手资料** 🟢 |
| Galvanometer Scanners 产品线 | https://www.scanlab.de/en/products/galvanometer-scanners | 英文 | 免费 | 中级 | dynAXIS 系列振镜电机：面向光学应用的高性能旋转电机 🟢 |
| SCANcube 10 产品页 | https://www.scanlab.de/en/products/scan-systems/scancube/standard-series/scancube-10 | 英文 | 免费 | 中级 | 明确列出伺服控制振镜扫描器的控制接口选项：**数字 SL2-100、数字 XY2-100（标准）、模拟 ±4.8V**。**验证 XY2-100 定位的最佳页面** 🟢 |
| hurrySCAN 30 产品页 | https://www.scanlab.de/en/products/scan-systems/hurryscan/standard-series/hurryscan-30 | 英文 | 免费 | 中级 | YAG/光纤/绿光/UV/CO₂ 激光适用，标准系统 5000W@1064nm 风冷，典型扫描角 ±0.35 rad 🟢 |
| 扫描系统对比页 | https://www.scanlab.de/en/print-product/615 | 英文 | 免费 | 中级 | 各扫描系统特性与优势对比，辅助选型 🟢 |
| 扫描系统对比页（应用向） | https://www.scanlab.de/en/print-product/617 | 英文 | 免费 | 中级 | 按应用场景对比扫描头/系统 🟢 |

### 4.2 RAYLASE

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| RAYLASE 官网 | https://www.raylase.de/en | 英文 | 免费 | 中级 | 高精度偏转镜振镜扫描器厂商。**XY2-100 协议文档的重要来源（多篇中文教程均引用 RAYLASE 官方文档）** 🟢 |
| RAYLASE 产品页 | https://www.raylase.de/en/products.html | 英文 | 免费 | 中级 | 模块化组件与激光束控制偏转单元 🟢 |
| LASER PROCESSING WITH RAYLASE（产品手册 PDF） | http://www.color-measure.com/upload/file/20220517/6378839551270545019195209.pdf | 英文 | 免费 PDF | 中级 | RAYGUIDE 激光加工软件介绍、振镜系统标定、加工任务创建与自动化 🟡 |
| Laser Processing with Raylase（PDF 镜像） | http://www.alaser.com.tw/db/upload/webdata3/alaser_2021831335114269.pdf | 英文 | 免费 PDF | 中级 | 同上手册的台湾代理镜像 🟡 |

### 4.3 Novanta / Cambridge Technology

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 62xxK & 83xxK 振镜扫描器 | https://novanta.com/precision-manufacturing/product/62xxk-and-83xxk-series-galvanometers/ | 英文 | 免费 | 中级 | Cambridge Technology 出品。8 µrad 线性度、40° 扫描角，用于打标、OCT、焊接 🟢 |
| XY 振镜套装 | https://novanta.com/precision-manufacturing/product/xy-galvanometer-sets/ | 英文 | 免费 | 中级 | 机械与光学对准、调谐、动态性能与安装位配置 🟢 |
| 62xxH 系列数据手册（PDF） | https://camtechfiles.s3-us-west-2.amazonaws.com/s3fs-public/Datasheet%20-%20Galvos-62xxH%20Series-DS00003_R1_v4_1_1.pdf | 英文 | 免费 PDF | 中级 | 闭环振镜扫描器。动磁式执行器 + 专利位置检测器，稳定定位与最快扫描速度 🟢 |
| 83xxK 系列数据手册（PDF） | https://camtechfiles.s3-us-west-2.amazonaws.com/s3fs-public/Datasheet%20-%20Galvos-83xxK%20Series-DS00002_R1_v14.pdf | 英文 | 免费 PDF | 中级 | 增材制造、激光转换、打标、通孔钻孔；医疗：激光治疗与 OCT。含 Cambridge Technology 公司简介（近 50 年经验）🟢 |
| Cambridge Technology 6220H 说明书 | https://www.manualslib.com/manual/1639303/Cambridge-Technology-6220h.html | 英文 | 免费（需注册可能） | 高级 | 6220H 振镜光学扫描器完整说明书。**驱动器调谐/伺服参数细节** 🟡 |
| Cambridge Technology Model 6240H 手册（PDF） | https://neurophysics.ucsd.edu/Manuals/Cambridge/Cambridge%20Technology%20Model%206240H%20Galvanometer%20Optical%20Scanner.pdf | 英文 | 免费 PDF | 高级 | ⭐ **加州大学圣地亚哥分校公开的厂商手册**。MicroMax 671XX 伺服 + 专利位置检测振镜技术，优秀的时间与温度稳定性、无需热补偿。**含伺服环路与调谐细节** 🟢 |
| 62xxH 系列（DirectIndustry PDF） | https://pdf.directindustry.com/pdf/cambridge-technology/62xxh-series-galvanometer-scanners/36210-739766.html | 英文 | 免费 | 中级 | 动磁式执行器与专利位置检测器技术说明 🟡 |
| Novanta Photonics（激光加工整体方案） | https://novantaphotonics.com/ | 英文 | 免费 | 中级 | 激光源 + 光束操控 + 扫描 + 端到端控制的集成技术栈 🟢 |

### 4.4 Thorlabs / Aerotech / 其他厂商培训与白皮书

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| Thorlabs 教育网络研讨会系列（含录像） | https://www.thorlabs.com/zh/educational-webinar-series/?tabName=Recorded+Webinars | 英文/中文 | 免费（需注册） | 中～高级 | ⭐ **有录制回放**。光子学与生命科学主题，每期配专门 Q&A。含振镜激光扫描方案专场 🟢 |
| Aerotech 网络研讨会：Dynamic Error Reduction via Galvo Compensation | https://www.aerotech.com/webinar/dynamic-error-reduction-via-galvo-compensation/ | 英文 | 免费（需注册） | 高级 | 现代动态激光加工中最主要的性能限制因素；用振镜补偿减少动态误差、降低运动质量、提高频率响应 🟢 |
| Aerotech：How Does a Galvo Head Work? | https://go.aerotech.com/in-motion/how-does-a-galvo-head-work-galvo-scanning-explained | 英文 | 免费 | 初级 | 振镜头工作原理、与其他光束操控方式对比、精密激光系统中的应用场景 🟢 |
| Aerotech：Galvo Laser Scan Heads | https://go.aerotech.com/in-motion/galvo-laser-scan-heads | 英文 | 免费 | 初级 | 振镜激光扫描头是什么、如何工作、为何重要 🟢 |
| Photonics.com 白皮书：Principle and Application of Galvanometer | https://www.photonics.com/White-Papers/Principle-and-Application-of-Galvanometer/wpp2363 | 英文 | 免费（可能需注册） | 中级 | 激光振镜扫描功能在各类激光加工（尤其打标）中的应用，振镜工作原理研究 🟢 |
| EUSPEN：Modeling and feedforward control for high performance galvanometer scanners（PDF） | https://www.euspen.eu/knowledge-base/PMC20111.pdf | 英文 | **免费 PDF** | 高级 | ⭐ **学术级**。考虑电机轴转动惯量、反射镜与编码器的多自由度集中质量建模，为高性能扫描设计**前馈控制**。想做算法必读 🟢 |
| Springer：New linkage control methods based on trajectory distribution of galvanometer scanner（PDF） | https://link.springer.com/content/pdf/10.1007/s00170-023-11743-0.pdf | 英文 | 免费 PDF（OA） | 高级 | 振镜 + 机械伺服系统联动控制，实现大范围高进给率激光加工（镜台联动 / IFOV 的学术版本）🟢 |
| Springer 文章页（同上） | https://link.springer.com/article/10.1007/s00170-023-11743-0 | 英文 | 免费（OA） | 高级 | 提高加工范围、精度与效率的联动加工方法 🟢 |
| IEEE：Modelling and control of a galvanometer for laser marking | https://ieeexplore.ieee.org/document/7793217 | 英文 | **付费**（IEEE Xplore） | 高级 | 提升工业激光打标性能的控制系统开发：振镜扫描头由控制反射镜位置的特种执行器（振镜）组成 🟢 |
| ScienceDirect：Design of a new type of high-speed scanning galvanometer | https://www.sciencedirect.com/science/article/pii/S0888327025007599 | 英文 | 付费（可能摘要免费） | 高级 | 高速扫描振镜结构设计；高温与振动条件下的抗干扰特性测试；高速摆动扫描实现补偿成像 🟢 |
| Evident/Olympus：Galvanometer Confocal Scanning Systems | https://evidentscientific.com/en/microscope-resource/tutorials/galvanometerscanning | 英文 | 免费（Java 交互教程） | 中级 | ⭐ **可交互**。共聚焦显微成像中，用两个高速振动反射镜在 XY 平面做矩形光栅扫描生成数字图像 🟢 |
| ezcad：Laser Scanning Galvanometer: Principles, Control, and Advanced Applications | https://www.ezcad.com/laser-scanning-galvanometer-from-core-principles-to-advanced-control/ | 英文 | 免费 | 中级 | 光束偏转原理、伺服系统、F-Theta 场镜校正、IFOV 技术、工业激光应用的精密同步 🟢 |
| ezcad：Laser Galvo Systems | https://www.ezcad.com/laser-galvo-systems-precision-and-speed-in-laser-marking-and-engraving/ | 英文 | 免费 | 初级 | 扫描头、振镜镜片、振镜激光器如何协同工作 🟢 |
| ezcad：What is a Galvo Laser System | https://www.ezcad.com/what-is-a-galvo-laser-system-and-why-it-matters-in-precision-laser-processing/ | 英文 | 免费 | 初级 | 振镜激光系统基础概念 🟢 |
| Physik Instrumente：Laser Seam Welding of Electronic Packages Using Galvo Scanners | https://www.physikinstrumente.com/en/knowledge-center/product-and-system-demonstrators/laser-welding-galvo-scanner | 英文 | 免费 | 高级 | 振镜附加控制能力：扩展激光源有效光斑尺寸至焊缝宽度、叠加复杂焊接图案、适配更高功率激光源 🟢 |
| Scanner Optics：Tips for Optimizing Laser Galvo Performance | https://www.scanneroptics.com/optimizing-laser-galvo-performance.html | 英文 | 免费 | 中级 | 振镜性能优化技巧（雕刻与切割质量）🟡 |
| YouTube：Fiber Laser Marking Galvo Head - Inside Galvo Scanner Head | https://www.youtube.com/watch?v=3XLB0hF1shc | 英文 | 免费 | 初级 | 拆解光纤激光打标振镜头（scanner head）内部结构。频道：Ultra Laser Lab 🟢 |
| YouTube：Increasing the Accuracy of Laser Seam Welding w/ Galvo | https://www.youtube.com/watch?v=7HuhfHVN-8U | 英文 | 免费 | 中级 | 用振镜提高激光缝焊精度 🟢 |
| PMDi：XY2-100 Galvoscanner Module | https://pmdi.com/posts/product/hardware/xy2-100-galvoscanner-module/ | 英文 | 免费 | 中级 | Polaris UniverseOne 运动控制系统通过硬件接口模块连接第三方振镜（Scanlab、Raylase、Newson、Arges），支持 XY2-100 / SL2-100 / HSSI / RTFE-D15D 🟡 |
| PMDi：SL2-100 Galvoscanner Module | https://pmdi.com/posts/product/hardware/sl2-100-galvoscanner-module/ | 英文 | 免费 | 中级 | 同上，SL2-100 版本；单机系统可用 4 个以上第三方振镜 🟡 |

---

## 五、书籍 / 教材 / 学位论文

### 5.1 书籍（书籍是本次调研的**最高价值发现**）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| ⭐ **Handbook of Optical and Laser Scanning, 2nd Edition**（Marshall & Stutz 主编） | https://www.taylorfrancis.com/books/oa-edit/10.1201/9781315218243/handbook-optical-laser-scanning-glenn-stutz-gerald-marshall | 英文 | ✅ **开放获取（OA）免费** | 高级 | ⭐⭐⭐ **本领域圣经级参考书，且 Taylor & Francis 提供 OA 免费版本**。前身是 1985 年的 *Laser Beam Scanning*。涵盖：光束偏转控制基础、图像保真度与质量因素、最新扫描器系统设计技术、振镜扫描器等 16 类核心技术。**实习生自学振镜最权威的一本书** 🟢 |
| 同上（Archive.org 免费借阅） | https://archive.org/details/oapen-20.500.12657-41669 | 英文 | 免费（OA / 借阅） | 高级 | Archive.org 上的 OA 版本入口 🟢 |
| 同上（Google Books） | https://books.google.com/books/about/Handbook_of_Optical_and_Laser_Scanning.html?id=DaLsDwAAQBAJ | 英文 | 部分预览免费 | 高级 | 可预览部分内容 🟢 |
| 同上（Routledge 出版页） | https://www.routledge.com/Handbook-of-Optical-and-Laser-Scanning/Marshall-Stutz/p/book/9781439808795 | 英文 | 付费（纸质） | 高级 | 纸质版购买页 🟢 |
| 同上（试读 PDF 预览） | https://api.pageplace.de/preview/DT0400.9781439808801_A23982790/preview-9781439808801_A23982790.pdf | 英文 | 免费预览 | 高级 | 含目录、前言与摘要，可先看结构再决定是否深读 🟢 |
| ⭐ **《光学和激光扫描技术手册（原书第2版）》** | https://product.dangdang.com/25342070.html | **中文** | 付费（定价 ¥179） | 高级 | ⭐⭐⭐ **上面那本英文书的官方中文版**。机械工业出版社 2018-08 出版，ISBN **9787111594949**，552 页 / 88.9 万字。主编：杰拉尔德·马歇尔、格伦·斯图兹（美）。译者：**周海宪**（清华大学金国藩院士弟子）。汇集美、英、日等国 26 位专家研究成果。**中文读者首选** 🟢 |
| 同上（机械工业出版社旗舰店） | https://detail.youzan.com/show/goods?from_source=gbox_seo&alias=2g2tg07nl96du | 中文 | 付费 | 高级 | 出版社官方店铺，ISBN 9787111594949、页数 552 已核实 🟢 |
| 同上（百度百科词条） | https://baike.baidu.com/item/%E5%85%89%E5%AD%A6%E5%92%8C%E6%BF%80%E5%85%89%E6%89%AB%E6%8F%8F%E6%8A%80%E6%9C%AF%E6%89%8B%E5%86%8C%EF%BC%88%E5%8E%9F%E4%B9%A6%E7%AC%AC2%E7%89%88%EF%BC%89/23745536 | 中文 | 免费 | — | 词条含内容概览与译者信息，选书前可先看 🟡 |
| 同上（读书网 / 云台购 / 苏宁 比价） | https://www.dushu.com/book/13446826/ | 中文 | 付费 | 高级 | 内容简介与目录，可多平台比价 🟡 |
| 同上（苏宁易购） | https://product.suning.com/0070067633/12275153071.html | 中文 | 付费 | 高级 | 另一购买渠道 🟡 |
| 《激光原理及应用》陈鹤鸣 主编（及另两本激光原理教材） | https://www.zhihu.com/question/53533969 | 中文 | 付费（教材） | 中级 | 知乎高赞回答推荐的学习路径：三本激光原理教材特点对比；建议从最浅显的一本入手建立整体认识，再用理论性强的书深入 🟡 |

### 5.2 学位论文 / 期刊论文（CNKI 知网 / 万方）

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| 中国优秀硕士学位论文全文数据库（CNKI） | https://cn.oversea.cnki.net/kns55/brief/result.aspx?dbPrefix=CMFD | 中文 | 付费（机构订阅） | 高级 | ⭐ **检索入口**。建议检索词：「振镜 控制」「XY2-100」「激光扫描 振镜 伺服」「振镜 校正」🟢 |
| 中国知网（CNKI）国际版 | https://chn.oversea.cnki.net/index/ | 中文 | 付费/部分免费 | 高级 | 面向全球用户的知网入口，支持多种全文下载方式 🟢 |
| CNKI 海外版 | https://c61.oversea.cnki.net/ | 中文 | 付费 | 高级 | 备用入口 🟢 |
| 《激光扫描振镜控制系统研究》（中北大学硕士学位论文） | https://www.docin.com/p-2871027380.html | 中文 | 部分免费/付费 | 高级 | ⭐ **强相关**。作者：权晓，导师：余红英，专业：控制科学与工程，2021 年，学号 S1815020。建立数学模型，提出基于**双闭环控制**的振镜控制算法；用 **Scilab/Xcos 仿真**验证提高扫描性能与抗扰动能力；搭建实验平台完成原理样机测试与参数整定、数据回放 🟡 |
| 《高速扫描振镜控制系统设计研究》（硕士学位论文） | https://d.wanfangdata.com.cn/thesis/ChhUaGVzaXNOZXdTMjAyNDA5MjAxNTE3MjUSCUQwMTQyOTc0NxoIa3FnZDM3bGU%3D | 中文 | 付费（万方） | 高级 | 针对扫描频率、线性度、抗干扰特性等影响激光成像质量的关键因素，完成高速扫描振镜控制系统总体方案设计 🟢 |
| 同上（掌桥科研入口） | https://www.zhangqiaokeyan.com/academic-degree-domestic_mphd_thesis/020313830958.html | 中文 | 付费/部分免费 | 高级 | 另一检索与获取入口 🟡 |
| 激光扫描相关学位论文（万方） | https://d.wanfangdata.com.cn/thesis/Y2229697 | 中文 | 付费（万方） | 高级 | 激光扫描技术随激光打印机、照排机发展而来，已扩展到光学医疗、激光加工、图像传输。**振镜式扫描在激光扫描系统中应用最多**：打标、雕刻、微焊接、精跟踪、舞台灯光、生物医学 🟢 |
| 《基于 XY2-100 协议的振镜控制转换板的设计与实现》 | https://d.wanfangdata.com.cn/periodical/zdhyyqyb201412057 | 中文 | 付费（万方） | 高级 | ⭐ **直接命中主题**。王文毅、吕勇、陈青山、孔凡辉。针对"多数激光扫描振镜控制板需连 PC 在 Windows 下工作"的痛点，设计以 **TI DSP F2812** 为核心、基于 XY2-100 协议的振镜控制转换板，提高实时性与集成性 🟢 |
| 同上（豆丁网） | https://www.docin.com/p-4729535794.html | 中文 | 部分免费/付费 | 高级 | 含摘要：XY2-100 协议分析、硬件电路与软件程序设计、测试验证，稳定性较高 🟡 |
| 同上（百度文库，含参考文献列表） | https://wenku.baidu.com/view/53774f63f211f18583d049649b6648d7c0c70873.html | 中文 | 部分免费 | 高级 | ⭐ **即使只看引用列表也有价值**——列出了基于 FPGA 的以太网激光振镜控制器、基于 FPGA 的共聚焦显微镜振镜扫描控制系统（贾仕达、黄斐、薛萌、郭汉明）等同主题论文，可作为二次检索线索 🔴 |
| 同上（AtomGit / GitCode 博客） | https://blog.gitcode.com/8a131e79325d5cd1a058bb111688ab6c.html | 中文 | 免费 | 高级 | 资源仓库页，介绍 XY2-100 协议基本原理与转换板设计实现指南 🟡 |
| 基于 FPGA 的以太网激光振镜控制器设计与实现（PDF 预览） | https://gitcode.com/Open-source-documentation-tutorial/2b97d/blob/main/%E5%9F%BA%E4%BA%8EFPGA%E7%9A%84%E4%BB%A5%E5%A4%AA%E7%BD%91%E6%BF%80%E5%85%89%E6%8C%AF%E9%95%9C%E6%8E%A7%E5%88%B6%E5%99%A8%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0.pdf | 中文 | 免费 | 高级 | ⭐ **可免费获取的完整 PDF**：FPGA 基本原理、激光振镜控制原理、以太网通信协议与系统整体实现 🟡 |
| 激光扫描控制系统设计与振镜校正技术资料合集 | https://wenku.csdn.net/doc/i7aei1q8c5 | 中文 | 付费/下载券 | 高级 | 覆盖系统设计、振镜工作原理、扫描技术、系统失真与校正方法；分辨率、扫描速度、扫描范围、稳定性与可靠性设计考量 🔴 |
| MEMS 振镜技术解析：驱动原理、控制算法与 AR/激光投影应用实战 | https://wenku.csdn.net/column/07zl5gg4ito | 中文 | 付费（专栏） | 高级 | **拓展视野**：MEMS 振镜 vs 传统机械式振镜（体积大、功耗高、响应慢），MEMS 在投影仪、AR 眼镜、激光雷达中的突破 🟡 |

---

## 六、社区 / 代码仓库 / Q&A

### 6.1 GitHub 开源项目（**动手实践的最佳起点**）

> ⚠️ 本环境无法访问 `github.com`，以下仓库均出自搜索结果，**我未能逐个验证仓库当前状态**（星标数、最后更新、是否归档）。请注意开源项目的时效性。

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| ⭐ **georgemihaila/xy2-100** | https://github.com/georgemihaila/xy2-100 | 英文 | 免费（开源） | 中级 | ⭐⭐⭐ **XY2-100 最经典的开源实现**。Arduino/ESP 平台的 XY2-100 协议实现。README 说明：协议至少需 4 对差分线成帧发送数据包，含标准 16-bit 数据包结构图 🟢 |
| 同上 —— **协议规格说明书 PDF** | https://github.com/georgemihaila/xy2-100/blob/main/docs/xy2_100_specification.pdf | 英文 | 免费 | 高级 | ⭐ **仓库内附带的 XY2-100 协议原文 PDF**。这是少见的可免费获取的协议规格文档 🟢 |
| ⭐ **opengalvo/OPAL** | https://github.com/opengalvo/OPAL | 英文 | 免费（开源） | 高级 | ⭐⭐ 极简固件：将 **G 代码转换为 XY2-100 协议**。可控制 XY2-100 振镜（测试用 SinoGalvo SG7110）、Synrad 48 系列激光器、控制激光电源的 SSR。⚠️ 作者明确警告固件可能随时崩溃导致振镜与激光处于未知状态 🟢 |
| ⭐ **earlynerd/XY2Galvo** | https://github.com/earlynerd/XY2Galvo | 英文 | 免费（开源） | 高级 | ⭐⭐ **RP2040 PIO 实现**。利用 PIO 外设生成 XY2-100 所需的精确高速差分 CLOCK/SYNC/X/Y 信号；双核运行——core1 专责信号生成与绘图逻辑，core0 留给应用逻辑。**现代 MCU 上最优雅的实现思路** 🟢 |
| georgemihaila/galvo-controller | https://github.com/georgemihaila/galvo-controller | 英文 | 免费（开源） | 中级 | 实现 XY2-100 协议的设备解析 **G 代码**并实时控制的库 🟢 |
| NiklasHammerstone/GalvoStep | https://github.com/NiklasHammerstone/GalvoStep | 英文 | 免费（开源） | 中级 | 用**步进电机** + 常见零件搭建廉价振镜激光系统。含机械与电气图纸、固件与详尽文档（面向可复现性）🟢 |
| Arduino 官方库：XY2-100 | https://docs.arduino.cc/libraries/xy2-100/ | 英文 | 免费（开源） | 初级 | ⭐ **Arduino 官方库文档**。控制使用 XY2-100 协议的激光扫描器（如 Cloudray RC1001），提供简洁 API 🟢 |
| Arduino Libraries：GalvoController | https://www.arduinolibraries.info/libraries/galvo-controller | 英文 | 免费（开源） | 中级 | 通过串口接收 G 代码控制 XY2-100 激光扫描器的库 🟢 |
| ⭐ **sigrok 协议解码器：xy2-100** | https://sigrok.org/wiki/Protocol_decoder:Xy2-100 | 英文 | 免费（开源） | 高级 | ⭐⭐ **调试利器**。sigrok/PulseView 逻辑分析仪软件已内置 XY2-100 协议解码器。文档说明：协议核心是向扫描器提交 16 位有符号整数控制振镜位置（0 为中心），可扩展至 18 位，但 -E 变体中奇偶校验位会失去意义。**抓波形直接解码，强烈推荐** 🟢 |
| PJRC 论坛：OpenGalvo 项目起源 | https://www.pjrc.com/opengalvo/ | 英文 | 免费 | 高级 | PJRC（Teensy 厂商）论坛的技术讨论记录。起于用户 DanielO 请求帮助生成 10MHz 时钟信号，25 帖后诞生 OpenGalvo 🟡 |
| Hackaday：XY2-100 标签页 | https://hackaday.com/tag/xy2-100/ | 英文 | 免费 | 中级 | Hackaday 上 XY2-100 相关项目报道（含 OPAL Open Galvo 项目介绍）🟢 |

### 6.2 论坛 / Q&A 讨论帖

| 名称 | 链接 | 语言 | 是否免费 | 难度 | 内容简介 |
|---|---|---|---|---|---|
| ⭐ **Reddit r/ECE：XY2-100 for galvo control, anyone?** | https://www.reddit.com/r/ECE/comments/toszj/xy2100_for_galvo_control_anyone/ | 英文 | 免费 | 高级 | ⭐ **高度贴合你的问题**。有人尝试用 XY2-100 协议直接控制 Raylase SUPERSCAN-LD 激光扫描器，苦于找不到参考文档，询问如何生成这样的信号 🟢 |
| Reddit r/ResinPrinterBuilders：DIY Laser Galvo Controller | https://www.reddit.com/r/ResinPrinterBuilders/comments/f13q3h/diy_laser_galvo_controller/ | 英文 | 免费 | 中级 | ⭐ **实战经验帖**。作者先从模拟振镜做起，后购买 XY2-100 兼容的 Sino-Galvo SG7110，**折腾一年后才成功**，称数字振镜体验比模拟好 10 倍 🟢 |
| LinuxCNC 论坛：XY2-100 Protocol and PID usage | https://forum.linuxcnc.org/27-driver-boards/42011-xy2-100-protocol-and-pid-usage | 英文 | 免费 | 高级 | ⭐ 用 RPi4 + Mesa 7i96 搭建激光振镜控制器；提到 LinuxCNC 通过 **xy2mod 与 hostmot2 固件**支持 XY2-100 接口 🟢 |
| LinuxCNC 论坛：Using Mesa 7i95T for laser + galvo (xy2-100) control | https://forum.linuxcnc.org/27-driver-boards/56411-using-mesa-7i95t-for-laser-galvo-xy2-100-control?start=0 | 英文 | 免费 | 高级 | 硬件通道分配讨论：4 路差分输出即可支持 2 轴 XY2-100 振镜；是否需占用 step/dir 通道 🟢 |
| LinuxCNC 论坛：sl2-100 galvo scanner | https://forum.linuxcnc.org/27-driver-boards/55813-sl2-100-galvo-scanner | 英文 | 免费 | 高级 | SL2-100（数字）与 XY2-100 的区分与配置讨论 🟢 |
| LightBurn 官方论坛：DIY Galvo scanner with PWM controlled diode laser | https://forum.lightburnsoftware.com/t/diy-galvo-scanner-with-pwm-controlled-diode-laser/141456 | 英文 | 免费 | 中级 | ⭐ **选型求助帖**。为带 XY2-100 接口的廉价国产振镜 + PWM 控制二极管激光器挑选 DSP 控制器，要求兼容 LightBurn 且有 TTL PWM 输出与 Z 轴步进接口 🟢 |
| Photonlexicon：SL2-100 Protocol for scanner | https://www.photonlexicon.com/forums/showthread.php/28608-SL2-100-Protocol-for-scanner | 英文 | 免费 | 高级 | 激光焊接领域客户反馈：SL2-100 比 XY2-100 分辨率更高、长距离传输更可靠；仅需 DataIn±/DataOut± 两对线，支持 **20 bit** 扫描分辨率 🟡 |
| NI 论坛：Any NI FPGA control board support SL2-100 protocol? | https://forums.ni.com/t5/Real-Time-Measurement-and/Any-NI-FPGA-control-board-support-SL2-100-protocol/td-p/3679533 | 英文 | 免费 | 高级 | ⭐ **协议对比的权威说明**：XY2-100 为 **16 bit** 指令分辨率，是激光材料加工行业最流行的振镜协议；SCANLAB 后来推出 **20 bit** 的 SL2-100 🟢 |
| 知乎：如何用 51 单片机基于 XY2-100 协议控制扫描振镜？ | https://www.zhihu.com/question/596454803 | 中文 | 免费 | 高级 | （正文教程部分已列）中文社区里少见的 XY2-100 实现细节讨论 🟡 |
| 知乎：数字激光振镜是如何工作和接线的？ | https://www.zhihu.com/question/27745444 | 中文 | 免费 | 初级 | （正文教程部分已列）金海创振镜接线与驱动板思路 🟡 |

---

## 七、给实习生的推荐学习路径（基于以上资源的排序建议）

**第 0 步 · 建立直觉（1～2 天）**
- 📺 B 站：Thorlabs《振镜激光扫描方案：设计和应用》
- 📖 CSDN：《图解扫描振镜 - 激光振镜 - 光学振镜 新手必看》
- 📖 知乎：《振镜激光扫描方案：设计和应用》

**第 1 步 · 吃透 XY2-100 协议（3～5 天）**
- 📖 CSDN：《XY2-100 协议详解：光学振镜控制接口与拓展应用》
- 📖 博客园：《XY2-100 振镜控制协议》（时序 + DB25 引脚）
- 📄 **下载 georgemihaila/xy2-100 仓库内的 `xy2_100_specification.pdf`（协议原文）**
- 🛠 sigrok `xy2-100` 协议解码器文档 —— 同时准备好逻辑分析仪

**第 2 步 · 看真实实现（1 周）**
- 💻 GitHub `georgemihaila/xy2-100`（Arduino 版，最易读）
- 💻 GitHub `earlynerd/XY2Galvo`（RP2040 PIO 版，最优雅）
- 💻 GitHub `opengalvo/OPAL`（G 代码 → XY2-100）

**第 3 步 · 厂商资料补底层（1～2 周）**
- 📄 **SCANLAB SPIE 论文《Advantages of digital servo amplifiers...》**（数字振镜为何取代模拟振镜）
- 📄 **Cambridge Technology 6240H 手册**（伺服环路与调谐）
- 📄 SCANLAB SCANcube 10 产品页（确认 XY2-100 的接口定位）

**第 4 步 · 系统与算法进阶（长期）**
- 📕 **《光学和激光扫描技术手册（原书第2版）》**（中文，¥179）／英文 OA 原版 *Handbook of Optical and Laser Scanning*
- 📄 EUSPEN 前馈控制论文、Springer 镜台联动论文
- 🎓 NPTEL《Laser Based Manufacturing》、MIT OCW《Fundamentals of Photonics》

**第 5 步 · 遇到问题时的求助渠道**
- 💬 LightBurn 论坛（DIY 振镜选型）
- 💬 LinuxCNC 论坛（xy2mod / Mesa 卡）
- 💬 电子发烧友「电机控制」版、EEWorld「以拆会友」版
- 💬 知乎 XY2-100 相关问题

---

## 八、调研局限与诚实声明

1. **无法验证链接可访问性**：如开篇所述，本环境的 `web_fetch` 对所有外部域名均失败（`resolves to a non-public IP address`），因此**全部 100+ 条链接均未经直接抓取验证**。所有 URL 均来自 `web_search` 的真实返回结果，无一条是我编造的。
2. **中国大学 MOOC / 学堂在线 无振镜专题课**：这是真实的检索结论，不是我漏搜。中文高校体系里振镜属于工程实践，没有独立 MOOC。
3. **网易云课堂 / 腾讯课堂**：腾讯课堂已转型为 T-Learning 内部平台，检索无公开振镜课程；网易云课堂未检索到振镜专项课。振镜培训主要以 B 站 / 抖音的操作教学形式存在。
4. **GitHub 仓库状态未知**：无法确认各仓库的 star 数、最后提交时间或是否已归档。使用前请自行检查。
5. **付费墙提示**：知网（CNKI）、万方、IEEE Xplore、Scopus 收录的论文需机构订阅或单篇付费；百度文库、豆丁、CSDN 文库的部分文档需下载券。学校图书馆通常可免费访问知网/万方。
6. **B 站视频可能被删除**：请以「标题 + UP 主名」作为二次检索关键词。
