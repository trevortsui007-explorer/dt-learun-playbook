from pathlib import Path
import os, re, json, hashlib, html, ntpath
from collections import Counter
from datetime import datetime

from source_config import guangzhou_root
ROOT = guangzhou_root()
OUT = Path('广州平台审查-2026-11-08')
OUT.mkdir(exist_ok=True)
WEB = 'Learun.Application.Web/'
MOD = 'Learun.Framework.Module/Learun.Application.Module/'
SI = WEB+'Areas/SI/Controllers/SI_PartmodleMappingController.cs'
SVC = MOD+'Learun.Application.TwoDevelopment/MDM/SiInplanjob/SiInplanjobService.cs'
AUTH = MOD+'Learun.Application.Base/AuthorizeModule/DataAuthorize/DataAuthorizeBLL.cs'
NEW = MOD+'Learun.Application.TwoDevelopment/DT/ReportDownload/'
evidence = {}
def ref(key, path, token):
    p = ROOT/path
    raw = p.read_bytes()
    try: text = raw.decode('utf-8-sig')
    except UnicodeDecodeError: text = raw.decode('gb18030')
    lines = text.splitlines()
    hits = [i+1 for i,line in enumerate(lines) if token in line]
    assert hits, (path, token)
    evidence[key] = dict(path=path, absolute_path=p.as_posix(), line=hits[0], matching_lines=hits,
                         sha256=hashlib.sha256(raw).hexdigest(), anchor=token)
    return key

ref('download',SI,'public ActionResult DownReportFile(')
ref('export',SI,'public ActionResult ExportReport(')
ref('writefile',SI,'Response.WriteFile(filePath)')
ref('getstring',SI,'public ActionResult GetString(')
ref('poststring',SI,'public ActionResult PostString(')
ref('dataset',SI,'public ActionResult GetDataSet(')
ref('page',SI,'public ActionResult GetDataTablePageList(')
ref('exec',SVC,'public static string ExecStoredProcedure(')
ref('core',SVC,'private static string ExecuteProcedureCore(')
ref('data_error',SVC,'public static DataSet GetDataSet(')
ref('export_error',SVC,'public static List<DataTable> ExecProcMulFromNetEAPDb_P2(')
ref('authorize',AUTH,'public bool SetWhereSql(string url')
ref('auth_store',AUTH,'WebHelper.AddHttpItems("DataAhthorCondition"')
ref('login',WEB+'App_Start/01 Handler/MvcControllerBase.cs','[HandlerLogin(FilterMode.Enforce)]')
ref('login_filter',WEB+'App_Start/01 Handler/HandlerLoginAttribute.cs','public override void OnAuthorization')
ref('delete_caller',WEB+'Areas/SI/Views/HR_Skill/Index.js',"pms.flag = 'Delete'")
ref('identity_caller',WEB+'Areas/SI/Views/HR_Skill/Form.js','pms.CreateBy = loginInfo.userId')
ref('export_caller',WEB+'Areas/SI/Views/HR_Skill/Index.js','/SI/SI_PartmodleMapping/ExportReport')
ref('fast_create',SI,'public ActionResult CreateFastExportTaskEAPDb_P2(')
ref('fast_download',SI,'public ActionResult DownFastReportFileEAPDb_P2(')
ref('fast_exec',SI,'private static void ExecuteFastExportTaskEAPDb_P2(')
ref('fast_writer',SI,'private static void WriteFastExportWorkbook(')
ref('new_controller',WEB+'Areas/DT_ToolsModule/Controllers/ReportExportController.cs','public ActionResult CreateTask(')
ref('new_owner',WEB+'Areas/DT_ToolsModule/Controllers/ReportExportController.cs','private static bool Owns(')
ref('new_path',NEW+'ReportExportFileStore.cs','public static string Resolve(')
ref('new_executor',NEW+'ReportExportExecutor.cs','public void Execute(')
ref('web_start',WEB+'Global.asax.cs','protected void Application_Start()')
ref('api_start','Learun.Application.WebApi/Startup.cs','public void Configuration(')
ref('api_auth','Learun.Application.WebApi/Modules/BaseApi.cs','private Response BeforeRequest(')
ref('cors','Learun.Application.WebApi/Bootstraper.cs','Access-Control-Allow-Origin')
ref('web_framework',WEB+'Learun.Application.Web.csproj','<TargetFrameworkVersion>')
ref('api_framework','Learun.Application.WebApi/Learun.Application.WebApi.csproj','<TargetFrameworkVersion>')
ref('ajax',WEB+'Views/LR_Content/script/lr-ajax.js','httpAsync: function')
ref('layout',WEB+'Views/Shared/_Index.cshtml','jquery-1.10.2.min.js')
ref('route',WEB+'App_Start/RouteConfig.cs','url: "vip/')
ref('excel','Learun.Framework.Module/Learun.Util/Learun.Util/Excel/ExcelHelper.cs','public static void tablesToExcel(')
ref('manual','docs/力软开发规范/开发规范与组件手册.html','id="scope"')

excluded = {'.svn','.git','.vs','bin','obj','packages','artifacts','node_modules','.report-export-verification'}
counts=Counter(); projects=[]; test_files=[]
for directory, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in excluded]
    for name in names:
        p=Path(directory)/name
        if p.suffix.lower() in {'.cs','.js','.cshtml','.sql','.csproj'}: counts[p.suffix.lower()]+=1
        if p.suffix=='.csproj': projects.append(p.relative_to(ROOT).as_posix())
        if re.search(r'test',name,re.I) and p.suffix.lower() in {'.cs','.js','.ps1','.csproj'}: test_files.append(p.relative_to(ROOT).as_posix())

findings = [
('必须修复','旧报表下载缺少路径边界与文件归属校验','download,writefile,export_caller',
 '下载入口把用户传入 fileName 直接拼到 /Excel_Temp/ 的物理路径，再交给 Response.WriteFile。',
 '已通过现有登录/接口检查的请求若包含父目录片段，可令解析后的路径离开导出目录；接口也未检查文件属于当前用户。该路径解析缺陷已由源码确认，线上可达性和进程文件权限未实测。',
 '先限制为服务端登记的任务/文件标识，校验所有者和规范化路径必须位于根目录内；复用新 ReportExportFileStore.Resolve 与 Owns 的实现思路，覆盖正常文件、越界路径和跨用户下载。',
 '应用池账号可读的站点外或站点内非导出文件可能被读取。不要把随机文件名当成权限。'),
('必须修复','旧导出文件名来自请求，并被多人共享','export,excel,export_caller',
 'ExportReport 使用 reportName + .xls 作为磁盘文件名，ExcelHelper 以 FileMode.Create 写入。',
 '同名报表的两次导出指向同一文件，会覆盖或因并发占用失败；reportName 中的目录片段也没有边界校验，写入位置受请求影响。',
 '服务器生成每任务唯一文件路径，显示名称仅用于下载头；限制写入根目录，并关联创建者。保留前端合同的过渡适配后迁移至已有任务导出模块。',
 '用户可能下载其他请求的结果，或覆盖应用池可写目录中的同扩展名文件。'),
('必须修复','通用过程调用没有落实过程/操作/数据范围的授权边界','login,login_filter,authorize,auth_store,poststring,core,identity_caller',
 'MVC 基类有登录校验，DataAuthorize 按 URL 生成条件；SI 接口接受过程名和参数并直接用 SqlCommand 执行。',
 'SetWhereSql 把数据条件放入 HttpItems，但该 SqlCommand 调用链没有消费它，也没有按过程名及 flag 校验权限或覆盖客户端身份。允许访问通用 URL 的用户可选择不同过程和参数；实际影响还受库账号 EXECUTE 权限及过程内部检查约束。',
 '先为新增/敏感操作建立服务端允许列表和用户权限检查，并由登录上下文写入身份、验证厂别。逐项盘点旧调用后收紧，不能突然全量封禁；不把此问题误称为已证明 SQL 注入或匿名访问。',
 '页面按钮和前端厂别过滤无法保证数据隔离，新增 AI 页面会继续复制这条信任缺口。'),
('必须修复','SQL 错误被当作正常数据，高速导出还会标记成功','data_error,exec,export_error,fast_exec,fast_writer,page',
 '服务层捕获 SQL 异常后返回 error 数据表或异常字符串；Controller 仍调用 Success。',
 'SQL 执行失败时分页返回 records=0 和 error 行。高速导出收到非空 error 表后照常写 Excel，并设置 Success，用户看到的是“导出完成”。',
 '在共享服务提供可区分的失败结果/异常边界，导出错误必须进入 Failed；旧前端通过兼容适配迁移，先补 SQL 失败不算成功的合同测试。不要仅以 code=200 判断业务成功。',
 '监控和用户把故障当成空数据或成功导出，定位问题还会暴露内部 SQL 错误文本。'),
('应修复','删除业务仍通过 GET 执行','delete_caller,getstring',
 'HR_Skill 删除按钮通过 GetString 发出 GET，并传 flag=Delete。',
 '客户端或中间层把 GET 当成可重放读取时，同一个请求会重复进入写操作；此旧入口没有防伪令牌验证。是否存在跨站利用条件未验证，AjaxOnly 也不等于操作授权。',
 '把这一类调用逐项改为 POST 并增加防伪校验，读接口拒绝写操作；确认过程的重复删除行为，新增页面遵守查询/命令分离。',
 '写操作隐藏在查询入口，重试、缓存和后续 API 改造容易产生行为偏差。'),
('应修复','通用参数缺少边界校验，合法空值也会导致服务端异常','dataset,poststring,page',
 '多个通用方法直接遍历 pms，并对每个 value 调用 Trim；分页直接访问固定表和首行。',
 '省略 pms 或传入空值时会触发空引用；过程没有返回约定的两张表及 records 首行时会越界，错误发生在 Controller，无法给出稳定的参数或合同错误。',
 '在入口验证参数、空值策略及分页范围；访问 DataSet 前验证结构。补省略参数、空值、空页和错误结果集的合同用例。',
 'AI 按通用 JSON 习惯生成的 null、空对象或过程结果容易让线上页面报错。'),
('应修复','旧高速导出依赖进程内状态且未绑定任务所有者','fast_create,fast_download,fast_exec,new_controller,new_owner,new_executor',
 'FastExportTasks 是静态字典，任务通过 Task.Run 执行；任务记录没有创建者字段。',
 'IIS 回收后任务状态丢失，多进程请求无法保证命中同一字典；另一已登录用户若获得任务 id，下载入口未检查归属。本轮未找到 Areas 下的 JS/CSHTML 直接调用，不能据此认定入口已安全下线。',
 '核对部署与动态调用后停用旧入口，或迁移到已有数据库任务和 Hangfire 模块；保留所有权、任务领取、失败恢复与限流检查。',
 '发布/回收期间导出失联，扩容后出现间歇性“任务不存在”，任务链接可能越权共享。'),
]

def E(s): return html.escape(str(s))
def links(keys):
    return '；'.join(f'<code>{E(evidence[k]["path"])}:{evidence[k]["line"]}</code>' for k in keys.split(','))
parts=['<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><title>广州平台框架审查与 AI 开发基线</title><style>body{font:16px/1.75 system-ui,sans-serif;max-width:1120px;margin:40px auto;padding:0 24px;color:#203044}h1,h2,h3{line-height:1.35}h2{margin-top:40px;border-bottom:2px solid #dbe5ef;padding-bottom:8px}code{font-size:13px;overflow-wrap:anywhere;background:#eef3f8}table{border-collapse:collapse;width:100%}td,th{border:1px solid #dbe5ef;padding:10px;text-align:left;vertical-align:top}.note{background:#edf5fd;padding:16px}.evidence{font-size:13px;color:#53647a}li{margin:7px 0}</style><body>']
parts.append('<h1>广州平台：框架审查与 AI 开发基线</h1><p>2026-11-08 · Ponytail audit · 首轮只读静态审查</p>')
parts.append('<div class="note"><b>这个仓库做什么：</b>广州平台是基于 Learun 的业务系统，包含 MVC 页面、Nancy API、业务服务、数据库过程及后台任务。按多用户同时访问、报表并发和 IIS 正常回收的场景评估；未假设已经部署多节点，也未测量真实吞吐量。</div>')
parts.append('<p>唯一审查根目录：<code>D:/com.delton.serve-release</code>（用户已确认）。D:/com.delton.gz 不属于本轮结论；东莞平台未比较。源码、配置和数据库均未修改，未启动服务或连接数据库。报告是有界的框架风险审查，不代表逐文件或全业务安全认证。</p>')
parts.append('<h2>1. 证据范围与架构地图</h2><p>目录清点排除了依赖包、构建产物和版本库内部目录。数量只说明搜索范围，不代表全部文件已精读。</p><p>'+E(dict(counts))+'</p>')
parts.append('<table><tr><th>层次</th><th>核对事实</th><th>证据</th></tr>')
for layer, fact, keys in [
 ('页面与组件','MVC Razor / VIP 路由 / jQuery 1.10.2 / Learun AJAX；应沿用现有布局、jfGrid 和 Form 合同。','route,layout,ajax'),
 ('MVC 宿主','Web 项目目标为 .NET Framework 4.8；MvcControllerBase 继承登录过滤器，不是无鉴权接口。','web_framework,login,login_filter'),
 ('API 宿主','WebApi 目标为 .NET Framework 4.6.1，Nancy BaseApi 另有登录与免登录路径逻辑；不能套用 MVC 鉴权结论。','api_framework,api_auth'),
 ('数据访问','通用入口 → SiInplanjobService → SQL Server 存储过程。业务过程实体及线上权限仍需单独核对。','poststring,core'),
 ('后台任务','Web 启动 Quartz；API 启动 Hangfire，存在多个调度机制，迁移要列出任务唯一责任宿主。','web_start,api_start'),
 ('已有升级基础','新报表模块已有服务端身份、任务所有权、路径边界与顺序读取；适合作为迁移候选，不等于已完成全链验收。','new_controller,new_owner,new_path,new_executor')]:
    parts.append(f'<tr><td>{E(layer)}</td><td>{E(fact)}</td><td>{links(keys)}</td></tr>')
parts.append('</table><h2>2. 审查发现</h2><p>以下均有具体源码路径与触发条件；未执行利用请求。线上影响需在隔离环境按实际权限验证。共 7 项，未人为凑足数量。</p>')
for i,(level,title,keys,what,problem,fix,impact) in enumerate(findings,1):
    parts.append(f'<h3>{i}. [{level}] {E(title)}</h3><p class="evidence">{links(keys)}</p><ul>'+''.join(f'<li><b>{label}：</b>{E(text)}</li>' for label,text in [('当前行为',what),('具体问题',problem),('最小修复方向',fix),('不处理的结果',impact)])+'</ul>')
parts.append('<h2>3. 已有手册：保留、补充与禁止误用</h2><p>参考手册明确写着以 com.delton.serve-release 为准。它已准确提醒身份参数不可信、业务错误可能仍是 code=200、ES5 与编码约定。它适合作为组件合同起点，但不能被 AI 当成安全审查通过或全项目架构说明。</p><table><tr><th>条目</th><th>本轮处理建议</th></tr>')
for a,b in [
 ('保留：组件与调用合同','保留 VIP、Index/Form、jfGrid、userinfo、SQL 参数与结果集形状。每项标注来源版本与文件位置。'),
 ('补充：新旧成功值不同','手册模板使用 result === "success"，HR_Skill 实际使用“操作成功”。这是不同过程合同，不应批量替换；AI 必须核对当前过程与调用方。'),
 ('补充：新旧导出并存','明确旧 ExportReport/DownReportFile、进程内 FastExport 与持久化 ReportExport 的区别及迁移状态。新功能优先评估已有持久化模块。'),
 ('禁止：把旧实现写成新规范','GET 删除、客户端指定操作者、直接传过程名、将异常表当正常表，只能记为遗留行为与风险，不能成为生成模板。'),
 ('补充：验证层级','区分源码确认、离线合同验证、编译、隔离数据库联调、浏览器验收和生产观测。写清未验证项目，不用“已支持”代替测试证据。')]:
    parts.append(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>')
parts.append('</table><h2>4. 可直接交给 AI 的开发基线</h2><ol>')
for line in [
 '先确认平台、根目录、模块和适用 AGENTS.md。不得根据“同架构”把广州结论直接套到东莞。',
 '先定位一个现有同类页面及完整调用链，再写代码。记录路由、参数、身份来源、连接名、过程与 flag、返回结构及成功值。',
 '页面遵守所在模块的布局、组件与脚本风格；新增文件按手册 UTF-8 BOM / ES5 约定，旧文件先识别编码。',
 '服务器登录身份用于操作者与权限判断；前端 userinfo、account 头、厂别字段均不得独立充当授权证明。',
 '查询不写数据。新写入口使用 POST、明确权限与适用的防伪校验；存储过程参数化不代表过程内部动态 SQL 已安全。',
 '成功必须同时满足接口与业务合同；区分空数据、错误数据表、超时、权限拒绝和真实成功。',
 '新增导出先检查已有持久化模块。文件由服务端分配、限制根目录、校验所有者；回收、并发和取消是验收项。',
 '每次变更只触及需求相关代码，检查调用方、SQL 合同、csproj 显式文件项及部署清单。避免直接替换全站框架和依赖。',
 '提交前运行与变更相关的测试与构建，并用 ponytail-review 审查改动；数据库操作、外部调用和部署需有明确任务授权。',
 '交付记录实际改动、验证结果、未验证项及回退方式；不要把静态推断写成线上测量。']:
    parts.append('<li>'+E(line)+'</li>')
parts.append('</ol><h2>5. 架构升级顺序与验收门槛</h2><table><tr><th>阶段</th><th>具体产物</th><th>进入下一阶段的条件</th></tr>')
for a,b,c in [
 ('A：固定基线','冻结本次源码证据、平台差异表、接口/过程合同表；补构建工具、运行时、IIS 部署与数据库版本说明。','关键合同均有来源路径、核对日期和负责人；确定一个可重复构建的隔离副本。'),
 ('B：收紧高风险边界','处理发现 1–4；先为文件越界、跨用户访问、SQL 失败、身份篡改建失败用例。','测试覆盖拒绝路径；旧正常业务通过回归；没有把风险修复扩成全站重写。'),
 ('C：迁移一个真实切片','选一个报表或 CRUD 模块，复用现有服务与持久化任务；兼容旧合同并逐项切换。','真实用户权限、并发、回收、空数据、超时与回退路径都在隔离环境验收。'),
 ('D：统一架构与跨平台推广','在合同稳定后评估统一目标框架、API 鉴权和调度责任；再比较东莞差异。','差异清单、迁移成本和兼容策略有证据，不以依赖版本旧为唯一重构理由。')]:
    parts.append(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>')
parts.append('</table><h2>6. 待收集的证据与本轮限制</h2><ul>')
for line in [
 '数据库：过程定义、过程内部权限/事务/动态 SQL、数据库账号授权、生产与源码差异；本轮未连接数据库。',
 '身份：WebApi BaseApi 的免登录路径与各模块二次鉴权需逐条盘点；CORS 当前反射 Origin 并允许凭据，但是否可利用依赖实际认证与浏览器策略，本轮不作已确认漏洞结论。',
 '部署与负载：IIS worker 数、回收配置、Quartz 集群/幂等策略、Hangfire 消费节点、峰值并发、查询与导出大小；未测线上容量。',
 '测试：存在 tests/web-deploy、tests/BarTender、WMS Map 测试及 .report-export-verification；不能声称仓库完全没有测试。旧 SI 关键失败/授权路径未证明有自动回归保障。',
 '验证：本轮只做源码跟踪、目录/锚点/哈希核对及离线路径解析。未构建、未运行现有程序/测试可执行文件、未浏览器验收、未触发外部业务请求。',
 '覆盖：深入审查通用 SI、MVC 登录/数据权限、旧导出与新报表实现；其余业务模块、打印、SAP、移动端、附件上传和所有 SQL 未逐条审阅。',
 '依赖：仅记录包声明与实际布局引用；未作 CVE/许可证/支持周期审计，也没有以旧版本号直接宣判漏洞。',
 '数据保密：证据清单保存源码路径、锚点及 SHA-256，不复制连接串、密码或业务数据。']:
    parts.append('<li>'+E(line)+'</li>')
parts.append('</ul><p><b>结论：</b>先收紧旧导出文件边界和通用过程授权/错误合同，再以已有模块做渐进迁移。先 audit 固定事实，再完善开发文档，再用 review 审每次改动，适合本项目。</p><p>精简收益尚未量化：没有证明无调用的代码，不提出删除行数或依赖数量。</p><p>配套文件：<a href="evidence.json">机器可读证据与目录清单</a>。哈希用于识别后续源码漂移，不代表代码可信认证。</p></body></html>')

root_test=r'D:\sandbox\Excel_Temp'
outside=ntpath.abspath(ntpath.join(root_test,r'..\outside.txt'))
assert ntpath.commonpath([root_test,outside]) != root_test
payload=dict(root=ROOT.as_posix(), date='2026-11-08', method='static-source-audit', evidence=evidence,
             counts=dict(counts), projects=projects, test_file_inventory=test_files,
             excluded_directories=sorted(excluded), offline_path_check='parent segment resolves outside export root; no actual file read',
             limitations=['No runtime test','No DB connection','No build','No production access'])
(OUT/'evidence.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8-sig')
(OUT/'广州平台框架审查与AI开发基线.html').write_text(''.join(parts),encoding='utf-8-sig')
print(json.dumps(dict(output=str(OUT.resolve()),source_anchors=len(evidence),findings=len(findings),inventory=dict(counts),test_files=len(test_files)),ensure_ascii=False))
