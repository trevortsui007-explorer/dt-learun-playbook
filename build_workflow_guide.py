from pathlib import Path
import re, html, json, hashlib

from source_config import guangzhou_root
ROOT=guangzhou_root()
OUT=Path('力软开发模式工作流-2026-11-08')
OUT.mkdir(exist_ok=True)
W='Learun.Application.Web/'
F='Learun.Framework.Module/'
refs={}
def add(k,path,needle):
    p=ROOT/path
    raw=p.read_bytes()
    try:s=raw.decode('utf-8-sig')
    except UnicodeDecodeError:s=raw.decode('gb18030')
    hits=[i for i,l in enumerate(s.splitlines(),1) if needle in l]
    assert hits,(k,path,needle)
    refs[k]={'path':path,'line':hits[0],'anchor':needle,'sha256':hashlib.sha256(raw).hexdigest()}

add('R01',W+'App_Start/RouteConfig.cs','url: "vip/')
add('R02',W+'Controllers/HomeController.cs','public ActionResult CommPage')
add('R03',W+'Areas/SI/Controllers/SI_PartmodleMappingController.cs','public ActionResult GetDataSet(')
add('R04',W+'Areas/EAP/Controllers/EAP_PartmodleMappingController.cs','public ActionResult GetDataSet2(')
add('R05',W+'Areas/Erp/Controllers/Erp_PartmodleMappingController.cs','public ActionResult GetDataSet(')
add('R06',W+'Areas/SI/SIAreaRegistration.cs','public override void RegisterArea')
add('R07',W+'Views/Shared/_Index.cshtml','window.onresize')
add('R08',W+'Views/Shared/_IndexWin.cshtml','GetAuthorizeButtonColumnList')
add('R09',W+'Extensions/HtmlHelperExtensions.cs','public static MvcHtmlString AppendJsFile')
add('R10',W+'Views/Shared/_Form.cshtml','WdatePicker.js')
add('R11',F+'Learun.Util/Learun.Util/Web/JsCssHelper.cs','public static string ReadJSFile')
add('R12',W+'Views/LR_Content/script/lr-ajax.js','httpAsync: function')
add('R13',W+'Views/LR_Content/plugin/grid/jfgrid.js','reload: function')
add('R14',W+'Views/LR_Content/script/lr-form.js','$.fn.lrGetFormData')
add('R15',W+'Views/LR_Content/script/lr-layer.js','layerForm: function')
add('R16',W+'Areas/SI/Views/HR_Skill/Form.js',"pms.flag = 'SearchByFrom'")
add('R17',W+'Views/LR_Content/plugin/select/lr-select.js','$.fn.lrselectRefresh')
add('R18',W+'Areas/EAP/Views/EAP_Config/Form.js',"pms.flag = 'SearchByFrom'")
add('R19',W+'Views/LR_Content/script/lr-tabs.js','open: function')
add('R20',W+'Areas/MES/Views/PK_LabelSeriesNo/Index.js',"flag: mode + '-page'")
add('R21',W+'Areas/MES/Views/PK_LabelSeriesNo/Database/pr_LabelSeriesManagement.sql','CREATE OR ALTER PROCEDURE')
add('R22',W+'Areas/MES/Views/PK_LabelSeriesNo/SeriesApi.js','call: function')
add('R23',W+'Areas/EAP/Views/EAP2_AOI/eap_aoisecondleveldefect_set_save.js',"pms.flag = 'eap_aoisecondleveldefect_set_save'")
add('R24',W+'Controllers/WmsApiProxyController.cs','public ActionResult Forward')
add('R25',W+'Api/WmsProxyClient.cs','private Uri BuildTargetUri')
add('R26',W+'Areas/WMS/Views/FG_MasterData/Index.cshtml','Layout =')
add('R27',W+'Areas/WMS/Content/Foundation/Scripts/wms-api.js','function normalize')
add('R28',W+'XmlConfig/database.config','<connectionStrings>')
add('R29',F+'Learun.Application.Module/Learun.Application.TwoDevelopment/MDM/SiInplanjob/SiInplanjobService.cs','private static string GetProcedureConnectionString')
add('R30','Learun.Application.WebApi/Modules/WMS_FG/WMS/Modules/MasterDataMaintenanceModule.cs','class MasterDataMaintenanceModule')
add('R31',W+'Controllers/NpiBd4ApiProxyController.cs','public ActionResult Forward')
add('R32','Learun.Application.WebApi/Modules/BaseApi.cs','private Response BeforeRequest')
add('R33',W+'Areas/SI/Views/HR_Skill/Form.cshtml','WdatePicker(')
add('R34',W+'Areas/SI/Views/HR_Skill/Index.js',"param.flag = 'SearchByPageList'")
add('R35','docs/力软开发规范/templates/BackEnd/2. pr_module.sql','CREATE OR ALTER PROCEDURE')
add('R36','Learun.Application.WebApi/Learun.Application.WebApi.csproj','Modules\\WMS_FG\\WMS\\Modules\\MasterDataMaintenanceModule.cs')
add('R37',W+'Learun.Application.Web.csproj','Areas\\SI\\Views\\HR_Skill\\Index.js')
add('R38',W+'Areas/WMS/Views/FG_MasterData/WmsMasterDataApi.js','var master =')

body=Path('workflow_guide_source.md').read_text(encoding='utf-8')
body=body.replace('D:/com.delton.serve-release', ROOT.as_posix())
# Additional precise anchors for references spanning related files.
body=body.replace('[R10] [R16]', '[R10] [R33]')
body=body.replace('[R16] [R18] [R23]','[R16] [R34] [R18] [R23]')
body=body.replace('[R07] [R08] [R09] [R36]','[R07] [R08] [R09] [R37]')
body=body.replace('[R01] [R24] [R25] [R31]','[R01] [R24] [R25] [R31] [R38]')
assert set(re.findall(r'\[(R\d+)\]',body)) <= refs.keys()

agent_intro='''# Agent 工作指令：广州力软旧框架开发

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

'''

appendix='\n\n## 13 · 源码证据索引\n\n所有相对路径均相对上述根目录；行号对应本次本地快照。SHA-256 见配套 workflow-evidence.json。配置文件只保留路径/哈希，不摘录凭据。\n\n'
for k,e in refs.items():
    appendix+=f'- {k}：`{e["path"]}:{e["line"]}` — `{e["anchor"]}`\n'
body+=appendix
agent_body=agent_intro.replace('D:/com.delton.serve-release', ROOT.as_posix())+body[body.index('## 01'):]
(OUT/'AGENT_力软开发工作流.md').write_text(agent_body,encoding='utf-8-sig')
(OUT/'workflow-evidence.json').write_text(json.dumps({'root':ROOT.as_posix(),'date':'2026-11-08','method':'static source tracing','refs':refs},ensure_ascii=False,indent=2),encoding='utf-8-sig')

def inline(s):
    pieces=re.split(r'(`[^`]+`)',s)
    out=[]
    for piece in pieces:
        if piece.startswith('`') and piece.endswith('`'):out.append('<code>'+html.escape(piece[1:-1])+'</code>')
        else:
            piece=html.escape(piece)
            piece=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',piece)
            piece=re.sub(r'\[(R\d+)\]',r'<a class="ref" href="#\1">[\1]</a>',piece)
            out.append(piece)
    return ''.join(out)

# A small renderer for the controlled headings/tables/lists/code used in this document.
lines=body.splitlines(); rendered=[]; toc=[]; i=0
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('```'):
        lang=line[3:]; block=[];i+=1
        while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
        rendered.append('<pre><code>'+html.escape('\n'.join(block))+'</code></pre>');i+=1;continue
    m=re.match(r'^(#{1,3}) (.*)',line)
    if m:
        n=len(m[1]);title=m[2];sid='section-'+str(len(toc)+1)
        if n==2:toc.append((sid,title))
        rendered.append(f'<h{n}'+(f' id="{sid}"' if n==2 else '')+'>'+inline(title)+f'</h{n}>');i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            cells=[c.strip() for c in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r'[:\- ]+',c) for c in cells):rows.append(cells)
            i+=1
        table='<div class="table-wrap"><table>'
        for j,row in enumerate(rows):
            tag='th' if j==0 else 'td';table+='<tr>'+''.join(f'<{tag}>'+inline(c)+f'</{tag}>' for c in row)+'</tr>'
        rendered.append(table+'</table></div>');continue
    if re.match(r'^(?:- |\d+\. )',line):
        ordered=bool(re.match(r'^\d+\. ',line));tag='ol' if ordered else 'ul';items=[]
        pattern=r'^\d+\. ' if ordered else r'^- '
        while i<len(lines) and re.match(pattern,lines[i]):
            item=re.sub(pattern,'',lines[i]);identifier=''
            r=re.match(r'(R\d+)：',item)
            if r:identifier=f' id="{r[1]}"'
            items.append('<li'+identifier+'>'+inline(item)+'</li>');i+=1
        rendered.append('<'+tag+'>'+''.join(items)+'</'+tag+'>');continue
    paragraph=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||```|- |\d+\. )',lines[i]):paragraph.append(lines[i]);i+=1
    rendered.append('<p>'+inline(' '.join(paragraph))+'</p>')

style='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#243548;background:#f4f7fb;font:16px/1.8 "Segoe UI","Microsoft YaHei",sans-serif}header{padding:36px 40px;background:#132c45;color:white}header small{color:#a9d8f4;letter-spacing:2px}header h1{font-size:32px;margin:8px 0}header p{color:#d6e6f3;margin:0}.shell{display:grid;grid-template-columns:258px minmax(0,1fr);max-width:1520px;margin:auto}nav{position:sticky;top:0;height:100vh;overflow:auto;padding:24px 18px;border-right:1px solid #dce5ee}nav a{display:block;color:#3c5269;text-decoration:none;padding:9px 12px;font-size:14px;border-radius:6px}nav a:hover{background:#dcebf6;color:#0d5283}main{min-width:0;padding:28px 42px 70px;background:white}main>h1{display:none}h2{font-size:25px;color:#163e60;margin:42px 0 20px;padding-top:12px;border-top:2px solid #e6edf4;scroll-margin-top:15px}h3{font-size:19px;color:#265476;margin-top:30px}p{margin:14px 0}strong{color:#163e60}code{font:13px/1.65 Consolas,"Microsoft YaHei",monospace;background:#edf2f7;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}pre{background:#152c40;color:#e5eef5;border-radius:10px;padding:22px;overflow:auto;max-width:100%}pre code{background:none;color:inherit;padding:0;white-space:pre}table{border-collapse:collapse;width:100%;font-size:14px}th{background:#eaf2f8;color:#173e5c}td,th{border:1px solid #dce5ed;padding:12px;text-align:left;vertical-align:top}td{min-width:110px}tr:nth-child(odd) td{background:#fafcfe}.table-wrap{overflow:auto;margin:20px 0}li{margin:8px 0}.ref{font-size:12px;color:#1a6d9b;text-decoration:none}.downloads{padding:16px 20px;background:#e8f3f8;border-left:4px solid #247ba0}.downloads a{color:#135778}footer{font-size:13px;color:#65788a;margin-top:35px}li[id]{scroll-margin-top:20px}@media(max-width:950px){.shell{display:block}nav{position:relative;height:auto;border-right:0;display:flex;flex-wrap:wrap;padding:12px}nav a{font-size:12px}main{padding:20px}header{padding:24px}header h1{font-size:27px}}@media print{nav,.downloads{display:none}.shell{display:block}header{background:white;color:black;padding:0}header p,header small{color:#333}main{padding:0}body{background:white}pre{white-space:pre-wrap;background:#eee;color:#111}pre code{white-space:pre-wrap}h2{break-after:avoid}tr{break-inside:avoid}}'''
page='<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>力软开发模式工作流 · IT 接手手册</title><style>'+style+'</style></head><body><header><small>GUANGZHOU · LEARUN · DEVELOPMENT PLAYBOOK</small><h1>力软开发模式工作流</h1><p>IT 接手手册｜页面组件 · VIP 路由 · 存储过程 flag · WebApi Proxy</p></header><div class="shell"><nav aria-label="章节导航">'+''.join(f'<a href="#{sid}">{html.escape(title)}</a>' for sid,title in toc)+'</nav><main><div class="downloads">配套交付：<a href="AGENT_力软开发工作流.md">Agent Markdown 指南</a> · <a href="workflow-evidence.json">源码证据清单</a>。内容只在本地，不引用远程脚本或字体。</div>'+''.join(rendered)+'<footer>静态源码核对 · 2026-11-08 · 未修改业务源码或执行 SQL</footer></main></div></body></html>'
(OUT/'IT_力软开发模式工作流.html').write_text(page,encoding='utf-8-sig')
assert len(toc)==13
assert '## 13' in agent_body
assert 'ScadaP2' in page and 'mode + &#x27;-page&#x27;' in page
print(f'Built HTML + Agent Markdown; {len(refs)} source anchors; {len(toc)} sections.')
