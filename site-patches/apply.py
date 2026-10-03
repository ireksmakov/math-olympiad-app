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

print('Патч применён: содержание 6–7 классов и задачи №31–50.')
