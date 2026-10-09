import os
from pathlib import Path

root = Path(os.environ['APP_DIR'])
repo = Path(os.environ['GITHUB_WORKSPACE'])

# 1. Дополнительные проверенные авторские задачи.
problems = root / 'lib/problems.ts'
text = problems.read_text(encoding='utf-8')
fragment = (repo / 'site-patches/problems-extra.tsfrag').read_text(encoding='utf-8')
if "{id:31," not in text:
    marker = "\n];\nexport const topics="
    if marker not in text:
        raise RuntimeError('Не найден конец массива problems')
    text = text.replace(marker, fragment + marker, 1)
    problems.write_text(text, encoding='utf-8')

# 2. Страница «Содержание».
contents_src = repo / 'site-patches/contents-page.tsx'
contents_dst = root / 'app/contents/page.tsx'
contents_dst.parent.mkdir(parents=True, exist_ok=True)
contents_dst.write_text(contents_src.read_text(encoding='utf-8'), encoding='utf-8')

# 3. Ссылка «Содержание» в верхнем меню.
nav = root / 'components/Nav.tsx'
text = nav.read_text(encoding='utf-8')
if 'href="/contents"' not in text:
    text = text.replace('<Link href="/tasks">Задачи</Link>', '<Link href="/contents">Содержание</Link><Link href="/tasks">Задачи</Link>')
nav.write_text(text, encoding='utf-8')

# 4. Главная страница: счётчик задач становится динамическим.
home = root / 'app/page.tsx'
text = home.read_text(encoding='utf-8')
text = text.replace('1–11 класс · MVP: 5–7 классы', '1–11 класс · база расширяется')
text = text.replace('<div className="statBig">30</div><div>проверенных авторских задач</div>', '<div className="statBig">{problems.length}</div><div>проверенных авторских задач</div>')
text = text.replace('Сейчас полностью наполнены 5–7 классы', 'Сейчас активно наполняются 5–7 классы')
home.write_text(text, encoding='utf-8')

# 5. В каталоге задач последние добавленные задачи №101–120 отмечаем зелёной точкой.
tasks_page = root / 'app/tasks/page.tsx'
text = tasks_page.read_text(encoding='utf-8')
new_title = '{p.id>=101&&p.id<=120&&<span className="newTaskDot" title="Новая задача"></span>}{p.title}'
if 'newTaskDot' not in text and '{p.title}' in text:
    text = text.replace('{p.title}', new_title)
tasks_page.write_text(text, encoding='utf-8')

# 6. Страница каждой задачи: кнопка возврата, метка новой задачи и белая доска справа.
whiteboard_src = repo / 'site-patches/WhiteBoard.tsx'
whiteboard_dst = root / 'components/WhiteBoard.tsx'
whiteboard_dst.write_text(whiteboard_src.read_text(encoding='utf-8'), encoding='utf-8')

task = root / 'app/task/[id]/page.tsx'
text = task.read_text(encoding='utf-8')
if "import Link from 'next/link';" not in text:
    text = "import Link from 'next/link';\n" + text
if "import WhiteBoard from '@/components/WhiteBoard';" not in text:
    text = text.replace("import Link from 'next/link';\n", "import Link from 'next/link';\nimport WhiteBoard from '@/components/WhiteBoard';\n", 1)
if 'Назад к задачам' not in text:
    marker = '<section className="problemMain"><div className="small muted">'
    replacement = '<section className="problemMain"><div style={{marginBottom:18}}><Link className="btn secondary" href="/tasks">← Назад к задачам</Link></div><div className="small muted">'
    if marker not in text:
        raise RuntimeError('Не найдено место для кнопки возврата на странице задачи')
    text = text.replace(marker, replacement, 1)
if '<h1>{p.title}</h1>' in text:
    text = text.replace('<h1>{p.title}</h1>', '<h1>{p.id>=101&&p.id<=120&&<span className="newTaskDot" title="Новая задача"></span>}{p.title}</h1>', 1)
if '<WhiteBoard problemId={p.id}/>' not in text:
    marker = '<aside className="problemSide">'
    if marker not in text:
        raise RuntimeError('Не найден правый блок страницы задачи')
    text = text.replace(marker, '<aside className="problemSide"><WhiteBoard problemId={p.id}/>', 1)
task.write_text(text, encoding='utf-8')

# 7. Оформление: задача и белая доска занимают по половине рабочей области.
css = root / 'app/globals.css'
text = css.read_text(encoding='utf-8')
text = text.replace(
    '.problemLayout{display:grid;grid-template-columns:1fr 300px;gap:18px}',
    '.problemLayout{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px;align-items:start}'
)
if '.whiteBoard{' not in text:
    text += '''\n.whiteBoard{background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px;box-shadow:0 10px 28px rgba(20,42,80,.06)}
.whiteBoardHead{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px}.whiteBoardTitle{font-size:21px;font-weight:900}.whiteBoardSub{font-size:13px;color:var(--muted);margin-top:3px}.whiteBoardTools{display:flex;gap:7px;flex-wrap:wrap}
.boardTool{border:1px solid #d7dfeb;background:#f7f9fc;color:#172033;border-radius:10px;padding:8px 11px;font-weight:700;cursor:pointer}.boardTool:hover{background:#eef3fb}.boardTool.active{background:#245ef4;color:#fff;border-color:#245ef4}.boardTool.danger{color:#a23535;background:#fff5f5;border-color:#f2d2d2}
.whiteBoardCanvasWrap{height:560px;border:1px solid #d9e1ec;border-radius:14px;overflow:hidden;background:#fff;box-shadow:inset 0 0 0 1px rgba(0,0,0,.012)}.whiteBoardCanvas{display:block;width:100%;height:100%;background:#fff;cursor:crosshair;touch-action:none}.whiteBoardNote{font-size:12px;color:var(--muted);margin-top:9px}
@media(max-width:900px){.whiteBoardCanvasWrap{height:430px}.whiteBoard{order:1}.problemMain{order:2}}
'''
if '.newTaskDot{' not in text:
    text += '''\n.newTaskDot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#22c55e;box-shadow:0 0 0 3px rgba(34,197,94,.14);margin-right:8px;vertical-align:middle;flex:0 0 auto}\n'''
css.write_text(text, encoding='utf-8')

print('Патч применён: расширенный банк задач, зелёная метка новых задач №101–120, кнопка возврата и белая доска.')
