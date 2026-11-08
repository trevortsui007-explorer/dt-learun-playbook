# Agent 工作指令：广州力软旧框架开发

适用根目录：`D:/com.delton.serve-release`。核对日期：2026-11-08。

这是一份供任务显式引用的开发指南，不是已安装 Skill，也没有覆盖项目 AGENTS.md。用户要求和当前项目约束优先；源码发生变化时重新核对证据，不把本文件当成永远正确的接口定义。

## 执行前必须完成

1. 读取目标目录适用的 AGENTS.md，确认真实编译源与引用文件；不搜索/修改生成副本作为主实现。
2. 填写合同卡：Area、Views目录、页面路由、布局、参考页、后端模式、接口、连接名、过程/flag、参数、返回结构、成功值、权限与验收。
3. 选择常用模式 A（通用过程）或模式 B（WebApi+Proxy），说明依据。不要因为页面 Area 推断数据库。
4. 读同类页面及完整调用链。SQL 定义不在仓库时，先完成能确认的前端工作，向用户索取最小缺失合同，不自行编造生产过程。

## 实施约束

- 优先原有 jfGrid/lrselect/Form/Tab、局部 CSS 与既有 API 封装，不替换全站框架。
- VIP 视图通常无需新增同名 Controller；只有明确需要服务端行为时才增加。
- 区分 MVC Action 与 SQL @flag；不把 pms.flag 写成 SQL 字符串或带 @ 的 key。
- EAP 无后缀接 EAPDb；方法后缀 2 接 EAPDb_P2；duopu 不是二厂开关。
- PostString 会追加 @result。无该参数且返回结果集的旧过程不能盲目迁移到它。
- httpAsync 回调是 data 或 null；$.ajax 是完整外壳；Wms.Api 是归一化结果。逐个核对调用层级。
- 客户端 userinfo/account/enCode/Operator 不是授权证明。敏感写操作必须服务器校验并注入可信身份。
- 兼容旧分支名及成功值。新增规范与遗留行为分开，禁止批量改名 SearchByFrom 等历史合同。
- 新资源沿用 UTF-8 BOM，旧文件辨认编码。ES5 作为兼容约定；不宣称已注释的压缩链在运行。
- 修改业务代码只限用户任务；数据库执行、部署、外部业务调用须在授权范围内。文档示例不构成执行 SQL 的指令。

## 交付门槛

- 页面：正确路由、布局和资源；列表/空数据/详情/保存/弹窗刷新及目标窗口尺寸验收。
- 接口：参数/flag/结果合同、错误路径、可信身份、并发与结果未知处理。
- 工程：Content/Compile 项及菜单/数据库/配置/DLL/静态资源部署清单。
- 验证：只报告实际执行过的构建、测试与浏览器步骤，区分静态判断和运行结果；使用 ponytail-review 检查改动及关联调用方。
- 最终交付包含改动、源码证据、验证、未验证项与回退说明。不能把本轮审查当成全站安全认证。

以下为与 IT 手册共用的已核对开发合同。先按任务选读相关章节，不必每次全文加载。

## 01 · 先分清五层名称

| 层次 | 例子 | 决定什么 |
| --- | --- | --- |
| 页面所属 Area | MES、SI、EAP、WMS | 业务归属和文件位置，不决定数据库 |
| 页面路由 | `/VIP/MES/PK_LabelSeriesNo/Index` | 找到 Razor 视图，不是数据接口 |
| MVC HTTP Action | `/SI/SI_PartmodleMapping/GetDataTablePageList` | 参数解析、结果包装、固定连接选择 |
| 数据库连接名 | BaseDb、EAPDb、EAPDb_P2 | 服务端配置中的连接，不由前端随意传入 |
| 存储过程业务分支 | `pr_LabelSeriesManagement` + `@flag='rules-page'` | 真正执行哪一种业务查询/命令 |

**关键例子：MES Area 的页面可以调用 SI 通用接口。** 不能因为页面放在 EAP 就断言所有请求去 Scada，也不能把 VIP 当成鉴权级别或数据库入口。[R01] [R02] [R20]

术语“动态页面”在本手册主要指 VIP 根据路径选择 `.cshtml`。它与 Learun 自定义表单设计器不是同一种机制；`LR_FormModule` / 自定义表单流程本轮未完整审查。

## 02 · 两种开发模式如何选

| 模式 | 合适场景 | 页面调用链 | 新增后端工作 |
| --- | --- | --- | --- |
| A：通用接口 + 存储过程（常用） | 已有 SQL 业务、配置维护、列表/表单、Scada 工艺查询 | 页面 → SI/EAP/Erp 通用 Action → SiInplanjobService → 过程 → @flag | 优先复用通用入口，补数据库过程合同；涉及可信身份/权限时补受控服务端入口 |
| B：WebApi + MVC Proxy | 已有 API 模块，复杂规则、外部集成、需独立服务/测试的功能 | 页面 → 同源 MVC Proxy → 配置的 API 服务 → Nancy 模块 → Service/Repository | API 路由、业务逻辑、代理映射及部署配置 |

这是后端组织方式的区别，前端均可继续使用 Learun 的 Areas/Views、布局和组件。不要为了新增一个列表引入整套 SPA，也不要为了复杂业务把所有规则塞入通用过程。[R03] [R04] [R05] [R24] [R25]

新增工作先填写一张合同卡：Area、页面目录、布局、参考页面、URL、后端模式、接口/代理前缀、连接名、过程、flag、输入、输出、成功条件、身份来源、验收步骤。缺少实际过程定义时，只能记录调用方观察到的合同，不能声称已验证 SQL 分支。

## 03 · 页面应该建在哪里

普通列表/表单沿用以下结构。这里的 `DemoModule` 是说明用占位名，不是已部署模块。

```text
D:/com.delton.serve-release/
  Learun.Application.Web/
    Areas/<业务Area>/
      <Area>AreaRegistration.cs
      Controllers/                 # 普通 MVC 视图 Action 或定制业务入口
      Views/DemoModule/
        Index.cshtml               # 列表结构、布局、资源引用
        Index.js                   # bootstrap、查询、按钮、网格
        Index.css                  # 仅本页样式，确有需要再建
        Form.cshtml                # 表单结构
        Form.js                    # 回填、校验、保存、回调
        Form.css                   # 可选
```

在已有 Area 新建 VIP 页面，通常无需新增 `DemoModuleController`；已有 `HomeController.CommPage` 会定位视图。只有需要普通 MVC URL、服务端 ViewBag、定制输出或业务 Action 时才加 Controller。新增整个 Area 时，要核对 AreaRegistration、视图配置及工程文件，不能只建一个同名目录。[R01] [R02] [R06]

WMS 已有区域共用资源在 `Areas/WMS/Content/Foundation/`；它不是所有 Area 必须复制的模板。页面私有 CSS/JS 留在页面目录，确有跨页面复用才放入该区域的共用目录，避免修改全局 `Views/LR_Content` 来解决单页问题。[R26]

SQL 放置沿用模块已有约定：现有 PK_LabelSeriesNo 使用 `Views/PK_LabelSeriesNo/Database/`，手册模板在 `docs/力软开发规范/templates/BackEnd/`。这只是本项目两种实际位置；SQL 文件存在不代表已执行或会随 DLL 自动升级。[R21] [R35]

### VIP 与普通 MVC URL 的对应关系

```text
/VIP/<area>/<path>/<cshtml>[/<id>]
    → HomeController.CommPage(area, path, cshtml)
    → ~/Areas/<area>/Views/<path>/<cshtml>.cshtml

/SI/<controller>/<action>[/<id>]
    → SIAreaRegistration
    → 对应 Controller Action
```

例：`/VIP/SI/HR_Skill/Form?keyValue=...` 对应 `Areas/SI/Views/HR_Skill/Form.cshtml`。文件名不带扩展名出现在 VIP URL 中；脚本通过 `request('keyValue')` 读取查询参数。路由里的可选 `id` 不会自动变成 `keyValue`，也不等于后端已加载记录。[R01] [R02] [R16]

当前 VIP 的 `path` 是单个路由段，不能未经改造就假定支持任意多层 Views 子目录。直接打开 `.cshtml` 文件也不能替代 MVC 渲染与父窗口环境。

### 工程与菜单交付

- Web 是显式项目项的旧 `.csproj`：页面、JS、CSS核对 `Content Include`，新 C# 核对 `Compile Include`。本地文件能看见不代表发布包一定包含它。
- 菜单地址使用实际页面 URL；按钮、列权限需要对应菜单/模块配置。页面存在不代表已有菜单入口。
- `_Index` / `_IndexWin` 用 `SetCurrentUrl` 提供 `lrCurrentUrl`，然后查询按钮/列授权再调用 bootstrap。新增菜单时核对地址及参数与权限配置匹配。
- 本轮没有登记菜单、部署 IIS 或执行数据库迁移。[R07] [R08] [R09] [R37]

## 04 · 布局、资源和初始化顺序

| 布局 | 实际用途与差异 | 新页面注意 |
| --- | --- | --- |
| `_Index.cshtml` | 列表组件、权限加载；resize 事件会在小于等于 1500px 时把 body 设成 1500px | 有横向溢出需求时先确认这个行为，不能当作天然响应式布局 |
| `_IndexWin.cshtml` | HR_Skill 列表采用；有列表组件与权限初始化，本文件未发现上述 1500px resize 逻辑 | 按目标页面与窗口环境选择，不按名字猜用途 |
| `_Form.cshtml` | 表单、选择器、上传、网格等资源；设置 `$.lrToken`，调用 bootstrap | `_Form` 不会自动把令牌加到任意自写 Ajax；缺什么资源仍需逐项核对 |

已核对布局引用 jQuery 1.10.2、Bootstrap CSS/JS 和 Learun 自有插件。普通业务页不要再加载另一份 jQuery 或覆盖全站 Bootstrap。[R07] [R08] [R10]

```cshtml
@{
    ViewBag.Title = "示例模块";
    Layout = "~/Views/Shared/_IndexWin.cshtml";
}
@Html.AppendCssFile("/Areas/SI/Views/DemoModule/Index.css")
<div id="demo-module" class="lr-layout">
    <div class="lr-layout-center">
        <div class="lr-layout-wrap lr-layout-wrap-notitle">
            <div class="lr-layout-tool">查询条件与按钮</div>
            <div class="lr-layout-body" id="gridtable"></div>
        </div>
    </div>
</div>
@Html.AppendJsFile("/Areas/SI/Views/DemoModule/Index.js")
```

这是结构示例；若不建 CSS 文件，就去掉对应 AppendCssFile。按真实业务 Area 替换路径，不要保留 DemoModule。

```javascript
var bootstrap = function ($, learun) {
    "use strict";
    // 先创建控件，再回填依赖控件的数据，最后查询。
    // 不要在这里和 $(document).ready 各初始化一次网格。
};
```

**AppendJsFile / AppendCssFile 会在服务端读取文件内容，输出内联 script/style**，并按 `JsCompressorCache` 决定是否读取缓存。浏览器 Network 看不到独立 JS 请求不代表没加载；资源没找到可能被跳过，修改后看不到效果应检查发布文件、服务器缓存和 HTML 响应。[R09] [R11]

当前 `ReadJSFile` 中压缩调用已注释，读取使用 `Encoding.Default`。新文件沿用项目手册 UTF-8 BOM 约定，旧文件先识别编码；ES5 是兼容开发建议，而不是“当前所有代码一定被压缩”的事实。源码已有箭头函数、Set 等写法，不能据此保证所有目标客户端均兼容。[R11] [R16] [R18]

## 05 · 组件与页面样式速查

| 需求 | 当前组件/入口 | 必须记住的合同 |
| --- | --- | --- |
| 普通列表 | `jfGrid`、`headData`、`mainId`、`url`、`isPage` | 列用 `label/name/width`；mainId 对应真实行主键 |
| 服务器分页 | `jfGridSet('reload', {sqlStoredName, pms})` | 网格追加外层 pagination，参数变化会重置第一页；返回 data.rows/page/records/total |
| 手工数据表 | `jfGridSet('refreshdata', rows)` | 传数组；GetDataSet 返回的 ds 对象不能直接当 rows |
| 取选中行 | `jfGridGet('rowdata')` | 取值后检查有行且有主键；不能直接访问空选中对象 |
| 单元格格式 | `formatter(value,row,op,cell)` | 输出 HTML 时编码不可信文本；DOM 事件防止反复渲染后重复绑定 |
| 下拉选择 | `lrselect` | 配置 value/text 对应数据字段；不要假定都是 id/name |
| 下拉读写 | `lrselectGet / lrselectGetEx / lrselectSet / lrselectRefresh` | Get 取值，GetEx 取选中项；刷新选项后再 Set 回填 |
| 表单读写 | `lrGetFormData / lrSetFormData` | 控件 id 对应字段；不把 div 下拉当普通 input 用 val 读写 |
| 必填校验 | `lrValidform` | 当前属性拼写为 `isvalid="yes" checkexpession="NotNull"`，不要擅自修正组件约定的拼写 |
| 复合查询 | `lrMultipleQuery(callback,height,width)` | 查询条件转成 pms；分页 pagination 不放进 pms |
| 日期范围 | `lrdate`、`selectfn(begin,end)` | 保存起止值并明确边界；单日期使用实际加载的控件 |
| 弹窗 | `learun.layerForm` | iframe 弹窗，`callBack` 大写 B；它传给回调的是窗口引用键 |
| 页内 Tab | `lrFormTab / lrFormTabEx` | anchor 的 data-value 对应 tab-pane id；Ex 可以接收切换回调 |
| 主框架新 Tab | `learun.frameTab.open(module)` | module 含 F_ModuleId/F_FullName/F_UrlAddress；同 ID 复用窗口 |

证据：[R12] [R13] [R14] [R15] [R17] [R19] [R22]

列表保持“筛选区 → 操作区 → 网格”；表单使用 `.lr-form-wrap`、`.lr-form-item`、`.lr-form-item-title` 与 `.col-xs-*`。按钮复用 `.btn`、`.btn-default`、`.btn-primary`、Font Awesome。页面 CSS 以页面根 ID/类限定，避免裸写全局 `.btn`、`body`、`.lr-form-item` 改坏其他界面。已有旧页面的全局选择器是观察到的做法，不是推荐规范。

WMS Foundation 已有 tokens、组件 CSS 和 API/组件适配层。WMS 同类页面优先复用；其他 Area 不为一两个控件整包搬入。[R26] [R27]

### 正确打开与关闭 Form

```javascript
learun.layerForm({
    id: 'demoModuleForm',
    title: '编辑',
    url: top.$.rootUrl + '/VIP/SI/DemoModule/Form?keyValue=' + encodeURIComponent(id),
    width: 700,
    height: 500,
    callBack: function (frameKey) {
        return top[frameKey].acceptClick(refreshGirdData);
    }
});
```

子页定义 `var acceptClick;`，在 bootstrap 内赋函数。先校验，再异步保存；保存成功才调用父页刷新和 `learun.layerFormClose(window.name)`。异步提交不要立即返回 true，否则弹窗可在请求结束前关闭；保存期间防止重复提交，失败时恢复按钮。[R15] [R16]

## 06 · 常用模式 A：SI / Scada / ScadaP2

### HTTP 地址、连接名、数据库的真实映射

| 页面请求前缀/方法 | 代码连接名 | 本地有效配置数据库 | 说明 |
| --- | --- | --- | --- |
| `/SI/SI_PartmodleMapping/GetDataSet` 等 | BaseDb | adms705 | 业务主库，方法签名逐个核对 |
| `/EAP/EAP_PartmodleMapping/GetDataSet` 等 | EAPDb | scada | Scada 常用入口，不存在本轮确认的 `/Scada/` 通用路由 |
| `/EAP/EAP_PartmodleMapping/GetDataSet2` 等 | EAPDb_P2 | ScadaP2 | `2` 是 Action 名后缀，不能靠 pms.PlantCode 自动选库 |
| `/SI/SI_PartmodleMapping/GetDataSetEAPDb_P2` 等 | EAPDb_P2 | ScadaP2 | SI 内也有部分二厂兼容方法，不能假定每个方法都有此变体 |
| `/Erp/Erp_PartmodleMapping/GetDataSet` 等 | ErpDb | 本轮有效连接文件未发现该项 | Controller 存在，不代表当前环境配置完整 |
| EAP `ExportReport` / `ExportReport2` | EAPDbRead / EAPDb_P2Read | scada / scadaP2 | 导出有独立连接别名，不能由查询接口推断部署配置 |

配置解析排除了 XML 注释中的测试连接；这里只记录连接别名及库名，不复制服务器、账号或密码。本地配置不等于生产环境。[R03] [R04] [R05] [R28]

`duopu` 是部分方法的外层参数：为 true 且登录 Operator 有 connectionString 时会覆盖所选连接。它不是二厂开关，也不是通用 `db` 参数；通常保持默认 false。[R29]

### 方法与返回结构

| 方法 | 默认用途 | 业务数据形状（完整 JSON 的 data 内） | 过程约定 |
| --- | --- | --- | --- |
| GetDataTable | 第一张结果表 | `dt: [...]` | 至少一张 SELECT 结果 |
| GetDataSet | 多结果集/详情 | `ds: {Table:[],Table1:[]...}` | SELECT 顺序就是表序号 |
| GetDataTablePageList | 分页 | `rows,total,page,records` | 第一表首行含 records，第二表为本页明细，空页也要两表 |
| GetString / PostString | 输出参数型结果 | `result: "..."` | 服务自动添加 `@result varchar(400) OUTPUT` |
| GetDataTableList | 第一张表数组 | `[...]` | 代码仍解析 pagination；新页面不要假定它免分页参数 |

EAP 二厂相应方法为 GetDataTable2、GetDataSet2、GetString2、PostString2、GetDataTablePageList2、GetDataTableList2。普通查询一般 GET，PostString 为 POST；**SI GetDataSet 没有 HttpGet 限制，但 EAP GetDataSet/GetDataSet2 有 HttpGet**，不能跨入口复制 POST 用法。[R03] [R04]

完整 JSON 外壳通常为 `{code, info, data}`。`learun.httpAsync` 成功回调拿到的是 **data**，失败可能是 null；`httpAsyncGet/httpAsyncPost` 和原生 `$.ajax` 回调拿到完整响应。不要写错一层 `data`。[R12]

### 参数规则

- 外层使用 `sqlStoredName`、`pms`、必要时 `pagination`；不是 queryJson/entity/keyValue 那套生成式接口合同。
- `pms.flag` 到 Controller 后变成 `@flag`，其它 key 同样补 `@`。前端不写 `@flag`，不传 `EXEC ...` SQL 文本。
- pms 当前按 `Dictionary<string,string>` 读取，value 调用 Trim。可选空值按已核对合同省略或传允许的空串；不要传 null、对象或原始数组。
- 明细数组/对象需要 `JSON.stringify` 后放在过程定义的字符串参数，例如 `pms.data`；只有该过程使用 OPENJSON/JSON_VALUE 时才按此合同发送。
- `pagination` 是与 pms 同级的 JSON 字符串，含 rows/page/sidx/sord；不要在 pms 重复添加这四个参数，也不要手动添加 result 输出参数。
- `userId/account/enCode/plant` 含义不同。按过程字段约定选择，并由服务端落实可信身份；客户端传入这些值不构成授权。[R03] [R29]

## 07 · @flag 分支：从界面动作到 SQL

**一个业务过程承载多个动作，页面通过 flag 选分支。** HTTP Action 负责如何调用和包装，flag 负责做哪件事。这里“拼接 flag”是构造动作标识，不是把用户输入拼进 SQL。

### 传统 CRUD：HR_Skill / EAP_Config

| 页面动作 | flag（保留现有拼写） | 接口 | 回调读取 |
| --- | --- | --- | --- |
| HR 列表 | SearchByPageList | SI GetDataTablePageList | jfGrid 接 rows 与分页元数据 |
| HR 详情 | SearchByFrom | SI GetDataSet | `data.ds.Table[0]` |
| HR 联动下拉 | SearchStation / SearchUserInfo | SI GetDataSet | `data.ds.Table` |
| HR 新增/编辑 | Add / Edit | SI PostString | `data.result === '操作成功'` |
| HR 导入/导出 | ImportAdd / ToExcel | PostString / ExportReport | 各自合同，不通用 |
| EAP 配置详情/保存 | SearchByFrom / Add / Edit | EAP GetDataSet / PostString | ds.Table / result |
| EAP2 缺陷字典 | SearchBytListItemQA_Defect1 / SearchBytListItemQA_Defect2 | EAP GetDataSet2 | ds.Table |
| EAP2 缺陷保存 | eap_aoisecondleveldefect_set_save | EAP PostString2 | result 为“操作成功” |

以上传统过程名分别为 `pr_hr_skill_sp`、`pr_eap_config_sp`、`pr_tdefect_sp`。这些分支已在 JS 调用方确认，本轮未取得它们的实际数据库过程定义，不能证明生产分支内容。`SearchByFrom` 等历史拼写不要单边“纠正”。HR 删除仍走 GET GetString 是遗留风险，不作为新写操作模板。[R16] [R34] [R18] [R23]

### 组合动作：PK_LabelSeriesNo（JS + SQL 均有证据）

```javascript
var mode = 'rules'; // 页面切换后可为 'series'
$('#seriesGrid').jfGridSet('reload', {
    sqlStoredName: 'pr_LabelSeriesManagement',
    pms: {
        flag: mode + '-page', // rules-page 或 series-page
        keyword: keyword,
        data: JSON.stringify(filterObject),
        Operator: currentOperator
    }
});
```

上面是提炼后的调用示意；keyword/filterObject/currentOperator 由页面按实际合同提供，Operator 仍不是可信授权凭据。

```text
规则 Tab ── rules-page ──┐
流水 Tab ── series-page ─┴─ GetDataTablePageList → @flag 分支 → records + rows
RuleForm ── rule / save-rule ──┐
SeriesForm ── series-detail / save-series ─┼─ POST SI GetDataSet → 多结果集
模板绑定 ── bind-template ────────────────┘
```

`SeriesApi.call(flag, values)` 统一加入 flag 和 Operator；过程读 `@data` 中 JSON，查询分支单独返回，写分支事务提交后 `SELECT CAST(1 AS bit) Success`。它**没有 `@result` 参数**，不能直接改成 PostString，否则额外输出参数会与签名不匹配。现状使用 SI GetDataSet 的 POST 能力，是结果集型命令的遗留合同，不要照搬到 EAP。[R20] [R21] [R22]

这类命名通常是“对象 + 动作”：rules-page、save-rule、save-series、bind-template。新增分支必须同时维护 JS 调用、SQL 允许动作、输入校验、结果形状和测试。若 flag 由 mode 拼接，mode 必须来自有限集合，SQL 对未知 flag 明确拒绝。

### 新增过程工作流

1. 先列动作矩阵：动作、读/写、必需参数、返回表或输出参数、权限和事务要求。
2. 查询分支只校验查询所需参数，不能因缺少保存字段而拒绝列表请求。
3. 分页固定“计数表 → 明细表”，排序字段使用允许列表，空页形状不变。
4. 输出参数型写操作使用 PostString；结果集型命令明确单独合同，不能仅按 HTTP 方法猜输出。
5. 写分支校验身份/归属、并发条件、业务约束，再执行必要事务；成功/失败必须明确。
6. 每分支 RETURN，未知 flag 拒绝；过程内部动态 SQL 另行审查，参数化调用不保证内部拼接安全。
7. 本地有 `docs/力软开发规范/templates/BackEnd/2. pr_module.sql` 可作结构参考，模板使用 Page/Detail/Save/Delete 和 success；不能替换旧过程现有分支或成功文字。[R35]

## 08 · 模式 A 的完整开发顺序

1. 找同 Area、同库、同交互的参考页面，读 Index/Form 和它调用的过程定义。
2. 固定连接：BaseDb、EAPDb 或 EAPDb_P2；由 Controller 的实际方法确认，不靠页面名称。
3. 列出 flag 矩阵及成功值，明确详情/列表/下拉/保存四类结果。
4. 新建 Views 目录及 Index/Form；使用现有布局、组件与局部样式。
5. 初始化控件 → 请求数据 → 判断 null/error → 回填 → 绑定保存回调。联动下拉先加载选项再设值。
6. 列表用 jfGrid 原生分页；无分页 GetDataSet 用手工 refreshdata 数组，不把 ds 当数组。
7. 新增写操作使用受控 POST；普通敏感业务不能仅依赖通用 SI 转发客户端身份。
8. 补项目 Content 项、菜单/按钮清单、SQL 脚本与部署顺序；在隔离数据库验收后交付。

### 输出参数型保存示例

下面仅适用于已经核对有 `@result`、成功文字为“操作成功”的旧过程；接口地址、过程名、字段按模块替换。若改用模板 success，前后端同时确认合同。

```javascript
learun.httpAsync('POST', top.$.rootUrl + '/SI/SI_PartmodleMapping/PostString', {
    sqlStoredName: 'pr_YourModule',
    pms: { flag: 'Edit', Id: recordId, Name: name }
}, function (data) {
    if (!data) {
        learun.alert.error('保存失败或结果未知，请先刷新核对。');
        return;
    }
    if (data.result !== '操作成功') {
        learun.alert.error(data.result || '未返回有效保存结果');
        return;
    }
    refreshGirdData();
    learun.layerFormClose(window.name);
});
```

该片段展示回调层级，不是可以直接部署的业务实现；可信身份、防重复提交、字段校验和权限由实际模块补齐。不要自动重试结果未知的写操作。[R12] [R16]

## 09 · 模式 B：WebApi + Proxy

本项目 WebApi 主要使用 **Nancy**，不是默认 ASP.NET Core Controller 模板。当前 Web 是 .NET Framework 4.8，WebApi 是 4.6.1。新增文件应沿用实际编译模块的宿主与语法，不随意加入 Minimal API 或 ASP.NET Core 属性路由。[R24] [R30] [R36]

```text
Areas/WMS/Views/FG_MasterData/Index.cshtml + Index.js
  → WmsMasterDataApi.js
  → Wms.Api.get / postJson（Foundation）
  → 同源 /api/wms-fg/master-data/...
  → RouteConfig → WmsApiProxyController.Forward
  → WmsProxyClient（WmsServiceBaseUrl + 固定 /api/wms-fg/ 前缀）
  → WebApi Modules/WMS_FG/WMS/Modules/MasterDataMaintenanceModule.cs
  → Service → Repository → 数据库
```

`/api/npi/bd4/{*path}` 另有 NpiBd4ApiProxyController。不要为已有代理前缀中的每个功能再建一套代理，也不要把代理配置 URL 写死到前端。[R01] [R24] [R25] [R31] [R38]

### 新增文件位置与责任

| 文件/位置 | 负责什么 | 不负责什么 |
| --- | --- | --- |
| `Areas/<Area>/Views/<Module>/Index.*` | 页面状态、组件和交互 | 不拼接数据库 SQL，不保存连接串 |
| 页面已有 `*Api.js` / 区域 Foundation | 请求序列化、响应归一化 | 不把失败统一改成成功，不信任浏览器身份 |
| `Web/Controllers/*ApiProxyController.cs` | 登录上下文、方法限制、透传响应状态 | 不接受用户指定任意目标服务 |
| `Web/Api/*ProxyClient.cs` | 从服务端配置选择目标、限制路径、超时与二进制转发 | 不无差别转发 Cookie/任意请求头 |
| `WebApi/Modules/<现有业务域>/...` | Nancy 路由、Service、Repository、DTO | 不为单一路由创建无用多层结构 |

WMS 同时存在 `Modules` 和生成的 `Host.Modules`。当前 WebApi csproj 明确编译 `WMS/Modules/MasterDataMaintenanceModule.cs`；Host.Modules 文件有生成提示。改动前以 csproj 和构建脚本确认源文件，不修改生成副本来冒充修复。[R30] [R36]

### 必须落实的接口合同

- 当前两个代理允许 GET/POST/PUT；不要假定 DELETE/PATCH 自动可用。
- MVC Proxy 从 LoginUserInfo 取 account/userId，客户端不能指定任意后端地址；客户端体内 operator 字段仍需要后端校验，代理传头不等于授权已闭环。
- WMS BaseApi 的免登录路径规则与模块权限需独立核对；不能因为通过 MVC 就认定直接访问 WebApi 也安全。
- WmsProxyClient 验证相对路径、限制目标 base URL 为站点根，转发服务端状态和内容类型；错误存在 400/405/502/504，页面应保留区分。
- WMS Foundation 的 API 返回归一化结果 `ok/type/code/message/data/raw`。它与 `learun.httpAsync` 只传 data 的回调不是一回事。
- JSON 请求用当前模块的 postJson；下载/文件结果不得当作普通 JSON。令牌、权限、请求大小和超时按实际业务配置核验。[R24] [R25] [R27] [R32]

### 开发与部署顺序

1. 固定 API 路由、方法、DTO、身份及错误合同，找同模块已有 Service/Repository。
2. 修改真正被 csproj 编译的 Nancy 模块，增加必要业务逻辑和测试。
3. 已有代理覆盖该前缀时直接复用；新前缀才增加受限路由、Controller、Client 和配置。
4. 页面 API 封装调用同源地址，页面继续使用现有布局和组件。
5. 按需先部署数据库，再兼容部署 WebApi，最后部署 Web 代理 DLL 和前端资源；将配置及回退步骤写入交付。
6. 隔离验证登录失效、无权、错误请求、业务失败、服务不可用、超时和实际成功。后端若可直接访问，单独验证其身份边界。

## 10 · 本轮专项审查发现

本轮关注开发模式与可复用合同，没有逐页运行。以下是有具体代码场景的风险；页面实际异常仍需浏览器和隔离环境确认。

### 1. 必须修复：SQL 分支的 System 判断依赖客户端 Operator

当前行为：SeriesApi 用前端 userinfo.enCode 填 Operator，SI 原样转参数，过程写分支判断 `@Operator='System'`。[R03] [R21] [R22]

问题：这条链没有在通用入口用服务器身份覆盖 Operator；允许访问该通用入口且数据库授权足够的请求可提供不同 Operator，过程的字符串判断本身不能证明管理员身份。

最小方向：对这类管理写操作增加受控服务端入口，核对登录用户权限后注入可信操作人，再调用过程；保持现有查询和结果合同，避免全站盲改 SI。

不处理：AI 复制“传 System 字符串即可授权”的模板，会把旧信任缺口传播到新模块。线上可达性与库权限本轮未测。

### 2. 应修复：部分 Form 的日期控件依赖不完整

当前行为：HR_Skill/Form.cshtml 调用 WdatePicker，而 `_Form.cshtml` 的 WdatePicker script 被注释，该 Form 没有另行引用。[R10] [R33]

问题：按这条 iframe 资源链，聚焦日期字段时无法由已列出的资源保证 WdatePicker 存在；父窗口加载函数不会自动成为子 iframe 全局函数。

最小方向：在受影响页面明确引入现有日期组件资源或改为该布局已经提供的控件，先验证日期选择/回填/清空；不要全局再加载一套库。

不处理：日期字段在相关部署中可能点击无反应或报未定义。尚未运行该页面，需检查额外运行期注入。

### 3. 应修复：_Index 的固定最小宽度影响小屏页面

当前行为：窗口 resize 后，宽度不大于 1500 时 body 被设为 1500px。[R07]

问题：1280px 等窗口会产生横向溢出；开发者仅调页面 CSS，可能无法消除布局脚本造成的宽度。

最小方向：先确定目标页面是否需要此约束；局部选择合适布局或受控调整，不直接取消所有业务页的宽度策略。

不处理：新页面在开发者宽屏正常，部署在较小终端时操作区偏移。

### 4. 应修复：错误/空数据回调仍被当作有效详情直接访问

当前行为：例如 EAP_Config/Form.js 直接读 `res.ds.Table[0]`，而 httpAsync 失败可回调 null，SQL 错误也可能变成 error 表。[R12] [R18] [R29]

问题：请求失败或详情不存在时，直接访问会抛异常或回填错误对象，无法稳定显示业务错误。

最小方向：页面先判断 null、error 结果和数组长度；对应模块补失败与不存在记录用例。共享错误合同的改造分阶段兼容旧调用。

不处理：AI 复制“成功示例”后会重复制造偶发白屏/保存失败无提示。

### 文档必须纠正的两处歧义

- 不把“写操作统一 PostString”写成所有旧模块的事实：PK_LabelSeriesNo 是 POST SI GetDataSet + SELECT Success，没有 @result。新增规范与旧合同要分栏说明。
- 不把“AppendJsFile 一定压缩”写成当前实现：本地压缩调用已注释，仍有服务端读取、编码与缓存行为。

## 11 · IT 与 Agent 共用的交付检查表

| 阶段 | 必须留下的证据 | 最小验收 |
| --- | --- | --- |
| 定位 | 平台根目录、参考页、实际 csproj、适用 AGENTS.md | 没改错平台/生成副本 |
| 页面 | Views 文件、布局、资源顺序、VIP/普通 URL | 菜单打开、弹窗打开、关闭后父页刷新 |
| 组件 | 网格字段、主键、选项字段、日期/Tab 合同 | 空列表、未选择、回填、重复打开、小屏 |
| 通用接口 | 连接名、过程签名、flag 矩阵、输出形状 | 正常/空数据/未知flag/错误/分页边界 |
| WebApi | 同源代理、后端路由、DTO、身份和错误合同 | 400/401或410/403/502/504及成功 |
| 写操作 | 权限、可信身份、重复提交、事务/并发 | 无权拒绝，失败不显示成功，结果未知不盲重试 |
| 部署 | Content/Compile、SQL、DLL、静态资源、配置、菜单清单 | 发布包确有文件；数据库版本匹配；缓存策略明确 |
| 交接 | 实际运行的测试/构建、未验证项、回退办法 | ponytail-review 对改动及关联调用方复核 |

只修改 HTML/JS 不代表可以跳过发布文件核对；只通过构建不代表 SQL 和浏览器交互正确。共享组件变更应回归至少一张旧列表和一个旧 Form；新增模块只测试相关范围，不为了数量跑无关测试。

## 12 · 快速排障与下一步

| 现象 | 先检查 |
| --- | --- |
| VIP 404/找不到视图 | area/path/cshtml 三段、实际文件和发布 Content；不要先加 Controller |
| bootstrap 不执行 | 资源是否内联成功、父框架 top.learun、权限请求失败与前置 JS 异常 |
| JS 改了没效果 | 服务器发布文件、AppendJsFile 缓存、页面 HTML 响应，而非只清浏览器缓存 |
| 网格无数据 | httpAsync 已解包、rows 与 ds.Table 区别、分页两表顺序、SQL error 行 |
| 二厂查到一厂 | 实际 Action 是否为 *2、服务连接名、有效配置、duopu 是否覆盖 |
| 保存报参数过多 | 是否把无 @result 的过程改走 PostString；pms 是否重复分页/输出参数 |
| 下拉回填丢失 | 控件是否先初始化、选项是否加载完成、value/text 字段是否正确 |
| API 405/502/504 | 代理允许方法、服务配置、后端运行状态、超时策略；不直接改为跨域硬编码 |

结论：用两种后端模式的明确合同指导开发，优先保留已有组件与目录结构；先修身份边界、依赖缺口和失败处理，再渐进整理共享代码。当前没有足够证据量化可删除行数或依赖数。

未验证：线上过程/权限、IIS 配置、生产数据库、菜单实际登记、真实业务页面运行与性能、东莞差异；没有执行部署或数据写入。HTML 文档的浏览器检查不等于业务系统验收。

下一轮最值得补齐：三库常用过程的只读定义导出与 flag/参数/返回结构台账、同类页面可复制模板的隔离验收、广州/东莞差异矩阵。不要把数据库凭据和真实业务数据放进 Agent 文档。


## 13 · 源码证据索引

所有相对路径均相对上述根目录；行号对应本次本地快照。SHA-256 见配套 workflow-evidence.json。配置文件只保留路径/哈希，不摘录凭据。

- R01：`Learun.Application.Web/App_Start/RouteConfig.cs:56` — `url: "vip/`
- R02：`Learun.Application.Web/Controllers/HomeController.cs:94` — `public ActionResult CommPage`
- R03：`Learun.Application.Web/Areas/SI/Controllers/SI_PartmodleMappingController.cs:94` — `public ActionResult GetDataSet(`
- R04：`Learun.Application.Web/Areas/EAP/Controllers/EAP_PartmodleMappingController.cs:350` — `public ActionResult GetDataSet2(`
- R05：`Learun.Application.Web/Areas/Erp/Controllers/Erp_PartmodleMappingController.cs:57` — `public ActionResult GetDataSet(`
- R06：`Learun.Application.Web/Areas/SI/SIAreaRegistration.cs:15` — `public override void RegisterArea`
- R07：`Learun.Application.Web/Views/Shared/_Index.cshtml:119` — `window.onresize`
- R08：`Learun.Application.Web/Views/Shared/_IndexWin.cshtml:112` — `GetAuthorizeButtonColumnList`
- R09：`Learun.Application.Web/Extensions/HtmlHelperExtensions.cs:26` — `public static MvcHtmlString AppendJsFile`
- R10：`Learun.Application.Web/Views/Shared/_Form.cshtml:35` — `WdatePicker.js`
- R11：`Learun.Framework.Module/Learun.Util/Learun.Util/Web/JsCssHelper.cs:27` — `public static string ReadJSFile`
- R12：`Learun.Application.Web/Views/LR_Content/script/lr-ajax.js:237` — `httpAsync: function`
- R13：`Learun.Application.Web/Views/LR_Content/plugin/grid/jfgrid.js:1368` — `reload: function`
- R14：`Learun.Application.Web/Views/LR_Content/script/lr-form.js:12` — `$.fn.lrGetFormData`
- R15：`Learun.Application.Web/Views/LR_Content/script/lr-layer.js:48` — `layerForm: function`
- R16：`Learun.Application.Web/Areas/SI/Views/HR_Skill/Form.js:87` — `pms.flag = 'SearchByFrom'`
- R17：`Learun.Application.Web/Views/LR_Content/plugin/select/lr-select.js:580` — `$.fn.lrselectRefresh`
- R18：`Learun.Application.Web/Areas/EAP/Views/EAP_Config/Form.js:22` — `pms.flag = 'SearchByFrom'`
- R19：`Learun.Application.Web/Views/LR_Content/script/lr-tabs.js:24` — `open: function`
- R20：`Learun.Application.Web/Areas/MES/Views/PK_LabelSeriesNo/Index.js:44` — `flag: mode + '-page'`
- R21：`Learun.Application.Web/Areas/MES/Views/PK_LabelSeriesNo/Database/pr_LabelSeriesManagement.sql:1` — `CREATE OR ALTER PROCEDURE`
- R22：`Learun.Application.Web/Areas/MES/Views/PK_LabelSeriesNo/SeriesApi.js:4` — `call: function`
- R23：`Learun.Application.Web/Areas/EAP/Views/EAP2_AOI/eap_aoisecondleveldefect_set_save.js:93` — `pms.flag = 'eap_aoisecondleveldefect_set_save'`
- R24：`Learun.Application.Web/Controllers/WmsApiProxyController.cs:18` — `public ActionResult Forward`
- R25：`Learun.Application.Web/Api/WmsProxyClient.cs:135` — `private Uri BuildTargetUri`
- R26：`Learun.Application.Web/Areas/WMS/Views/FG_MasterData/Index.cshtml:3` — `Layout =`
- R27：`Learun.Application.Web/Areas/WMS/Content/Foundation/Scripts/wms-api.js:16` — `function normalize`
- R28：`Learun.Application.Web/XmlConfig/database.config:2` — `<connectionStrings>`
- R29：`Learun.Framework.Module/Learun.Application.Module/Learun.Application.TwoDevelopment/MDM/SiInplanjob/SiInplanjobService.cs:722` — `private static string GetProcedureConnectionString`
- R30：`Learun.Application.WebApi/Modules/WMS_FG/WMS/Modules/MasterDataMaintenanceModule.cs:12` — `class MasterDataMaintenanceModule`
- R31：`Learun.Application.Web/Controllers/NpiBd4ApiProxyController.cs:11` — `public ActionResult Forward`
- R32：`Learun.Application.WebApi/Modules/BaseApi.cs:192` — `private Response BeforeRequest`
- R33：`Learun.Application.Web/Areas/SI/Views/HR_Skill/Form.cshtml:45` — `WdatePicker(`
- R34：`Learun.Application.Web/Areas/SI/Views/HR_Skill/Index.js:482` — `param.flag = 'SearchByPageList'`
- R35：`docs/力软开发规范/templates/BackEnd/2. pr_module.sql:12` — `CREATE OR ALTER PROCEDURE`
- R36：`Learun.Application.WebApi/Learun.Application.WebApi.csproj:987` — `Modules\WMS_FG\WMS\Modules\MasterDataMaintenanceModule.cs`
- R37：`Learun.Application.Web/Learun.Application.Web.csproj:2908` — `Areas\SI\Views\HR_Skill\Index.js`
- R38：`Learun.Application.Web/Areas/WMS/Views/FG_MasterData/WmsMasterDataApi.js:4` — `var master =`
