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

# 5. Кнопка возврата на странице каждой задачи.
task = root / 'app/task/[id]/page.tsx'
text = task.read_text(encoding='utf-8')
if "import Link from 'next/link';" not in text:
    text = "import Link from 'next/link';\n" + text
if 'Назад к задачам' not in text:
    marker = '<section className="problemMain"><div className="small muted">'
    replacement = '<section className="problemMain"><div style={{marginBottom:18}}><Link className="btn secondary" href="/tasks">← Назад к задачам</Link></div><div className="small muted">'
    if marker not in text:
        raise RuntimeError('Не найдено место для кнопки возврата на странице задачи')
    text = text.replace(marker, replacement, 1)
task.write_text(text, encoding='utf-8')

# 6. Интерактивная доска: решение показывается по шагам.
board_src = repo / 'site-patches/SolutionBoard.tsx'
board_dst = root / 'components/SolutionBoard.tsx'
board_dst.write_text(board_src.read_text(encoding='utf-8'), encoding='utf-8')

solve = root / 'components/SolvePanel.tsx'
text = solve.read_text(encoding='utf-8')
if "import SolutionBoard from '@/components/SolutionBoard';" not in text:
    text = text.replace("'use client';\n", "'use client';\nimport SolutionBoard from '@/components/SolutionBoard';\n", 1)
text = text.replace("{showSolution?'Скрыть решение':'Показать решение'}", "{showSolution?'Скрыть доску':'Показать решение на доске'}")
text = text.replace('<div className="solution">{problem.solution}</div>', '<SolutionBoard solution={problem.solution}/>')
solve.write_text(text, encoding='utf-8')

# 7. Оформление интерактивной доски.
css = root / 'app/globals.css'
text = css.read_text(encoding='utf-8')
if '.solutionBoard{' not in text:
    text += '''\n.solutionBoard{margin-top:18px;border:1px solid #1f4264;border-radius:18px;overflow:hidden;background:#102a43;color:#f5fbff;box-shadow:0 10px 28px rgba(16,42,67,.16)}
.solutionBoardHead{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;padding:18px 20px;background:linear-gradient(135deg,#173f5f,#102a43);border-bottom:1px solid rgba(255,255,255,.14)}
.solutionBoardTitle{font-size:18px;font-weight:900}.solutionBoardSub{font-size:13px;color:#c9d9e7;margin-top:4px}.solutionBoardCounter{min-width:58px;text-align:center;padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.12);font-weight:800}
.solutionBoardScreen{min-height:180px;padding:22px 20px;background:radial-gradient(circle at 20% 10%,rgba(255,255,255,.055),transparent 35%),#0d2438}
.solutionBoardEmpty{color:#bad0df;padding:34px 6px;text-align:center}.solutionStep{display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:start;padding:10px 0;line-height:1.6;animation:boardStepIn .28s ease-out}.solutionStep+.solutionStep{border-top:1px dashed rgba(255,255,255,.13)}
.solutionStepNo{display:flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:#2f67f6;color:white;font-weight:900}.solutionBoardDone{margin-top:14px;color:#8ee6ba;font-weight:800}
.solutionBoardControls{display:flex;gap:9px;flex-wrap:wrap;padding:14px 16px;background:#f7faff}.solutionBoardControls .btn{font-size:13px}.solutionBoardControls .btn.secondary{background:white}.solutionBoardControls .btn.ghost{background:#e8eef5}
@keyframes boardStepIn{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:620px){.solutionBoardHead{flex-direction:column}.solutionBoardControls .btn{flex:1 1 46%}.solutionBoardScreen{padding:18px 14px}}
'''
    css.write_text(text, encoding='utf-8')

print('Патч применён: содержание, задачи №31–50, кнопка возврата и интерактивная доска решения.')
