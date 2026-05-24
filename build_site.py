# -*- coding: utf-8 -*-
"""Generate SEO-optimized static pages for selector-casino.vercel.app"""
import json
import os

from content_faq import PAGE_FAQ, TRUST_PAGES
from page_content import PAGES

BASE = "https://selector-casino.vercel.app"
AFF = "https://lkga.cc/0b02c9ea"
AFF_REL = "nofollow sponsored noopener"
BANNER = f"{BASE}/assets/img/selector-banner.png"
LOGO = f"{BASE}/assets/img/logo.svg"
PUBLISH = "2026-05-17"
MODIFIED = "2026-05-17"

NAV = [
    ("official-site", "Официальный сайт", "/official-site/"),
    ("bets", "Ставки", "/bets/"),
    ("zerkalo", "Зеркало", "/zerkalo/"),
    ("casino", "Казино", "/casino/"),
    ("download", "Скачать", "/download/"),
    ("events", "События", "/#sobytiya"),
    ("login", "Вход", "/login/"),
    ("support", "Поддержка", "/#podderzhka"),
]

USEFUL = [
    ("official-site", "Официальный сайт", "/official-site/"),
    ("login", "Вход", "/login/"),
    ("registration", "Регистрация", "/registration/"),
    ("zerkalo", "Зеркало", "/zerkalo/"),
    ("bonus", "Бонусы", "/bonus/"),
    ("casino", "Казино", "/casino/"),
    ("download", "Скачать", "/download/"),
    ("bets", "Ставки", "/bets/"),
]


def canonical(path: str) -> str:
    if path == "/":
        return BASE + "/"
    return BASE + path.rstrip("/") + "/"


def schema_graph(page: dict) -> str:
    path = page["path"]
    url = canonical(path)
    name = page["title"]
    desc = page["description"]
    h1 = page["h1"]
    crumb_name = page.get("breadcrumb", "Главная")

    org = {
        "@type": "Organization",
        "@id": f"{BASE}/#organization",
        "name": "Selector Casino",
        "url": BASE + "/",
        "logo": {"@type": "ImageObject", "url": LOGO},
    }
    website = {
        "@type": "WebSite",
        "@id": f"{BASE}/#website",
        "url": BASE + "/",
        "name": "Selector Casino",
        "publisher": {"@id": f"{BASE}/#organization"},
        "inLanguage": "ru-RU",
    }
    webpage = {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": name,
        "description": desc,
        "isPartOf": {"@id": f"{BASE}/#website"},
        "inLanguage": "ru-RU",
    }
    items = [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE + "/"},
    ]
    if path != "/":
        items.append({"@type": "ListItem", "position": 2, "name": crumb_name, "item": url})
    breadcrumb = {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": items,
    }
    graph = [org, website, webpage, breadcrumb]
    if page.get("article"):
        graph.append(
            {
                "@type": "Article",
                "@id": f"{url}#article",
                "headline": h1,
                "description": desc,
                "author": {"@id": f"{BASE}/#organization"},
                "publisher": {"@id": f"{BASE}/#organization"},
                "datePublished": PUBLISH,
                "dateModified": MODIFIED,
                "inLanguage": "ru-RU",
                "mainEntityOfPage": {"@id": f"{url}#webpage"},
            }
        )
    if page.get("faq"):
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
                    }
                    for q in page["faq"]
                ],
            }
        )
    data = {"@context": "https://schema.org", "@graph": graph}
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>"
    )


def head_block(page: dict) -> str:
    path = page["path"]
    url = canonical(path)
    t = page["title"]
    d = page["description"]
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{BANNER}">
  <meta property="og:locale" content="ru_RU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{BANNER}">
  <meta name="theme-color" content="#1f2937">
  <link rel="icon" href="/favicon.ico?v=2" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preload" as="image" href="/assets/img/selector-banner.png" fetchpriority="high">
  <link rel="stylesheet" href="/style.css">
{schema_graph(page)}"""


def header_block(active: str) -> str:
    desktop = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if href.startswith("/#"):
            href = "/" + href[1:]
        desktop.append(f'            <li><a href="{href}"{cur}>{label}</a></li>')
    mobile = [
        '          <li class="nav-mobile-only"><a href="/"'
        + (' aria-current="page"' if active == "home" else "")
        + ">Главная</a></li>"
    ]
    for key, label, href in NAV:
        if key in ("events", "support"):
            href = "/" + href[1:] if href.startswith("/#") else href
        cur = ' aria-current="page"' if key == active else ""
        mobile.append(f'          <li><a href="{href}"{cur}>{label}</a></li>')
    mobile.append('          <li><a href="/registration/">Регистрация</a></li>')
    mobile.append('          <li><a href="/bonus/">Бонусы</a></li>')
    return f"""  <header class="site-header">
    <div class="container">
      <div class="header-bar">
        <div class="header-left">
          <a class="logo" href="/"><img src="/assets/img/logo.svg" width="934" height="362" alt="Selector Casino — логотип"></a>
          <a class="btn btn--bonus-header" href="{AFF}" rel="{AFF_REL}" target="_blank">Бонус</a>
        </div>
        <nav class="nav-desktop" aria-label="Основное меню">
          <ul>
{chr(10).join(desktop)}
          </ul>
        </nav>
        <button type="button" class="burger" aria-controls="mobile-nav" aria-expanded="false" aria-label="Открыть меню">
          <span class="burger-lines" aria-hidden="true"></span>
        </button>
      </div>
      <nav id="mobile-nav" class="nav-mobile-panel" hidden aria-label="Мобильное меню">
        <ul>
{chr(10).join(mobile)}
        </ul>
      </nav>
    </div>
  </header>"""


def footer_block() -> str:
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <a class="footer-logo" href="/"><img src="/assets/img/logo.svg" width="934" height="362" alt="Selector Casino" loading="lazy"></a>
        <nav class="footer-nav" aria-label="Ссылки в подвале">
          <ul>
            <li><a href="/official-site/">Официальный сайт</a></li>
            <li><a href="/zerkalo/">Зеркало</a></li>
            <li><a href="/login/">Вход</a></li>
            <li><a href="/registration/">Регистрация</a></li>
            <li><a href="/bonus/">Бонусы</a></li>
            <li><a href="/casino/">Казино</a></li>
            <li><a href="/bets/">Ставки</a></li>
            <li><a href="/download/">Скачать</a></li>
          </ul>
        </nav>
      </div>
      <div class="trust-footer">
        <p class="trust-meta"><span>Updated: May 2026</span> · <span>18+</span></p>
        <nav class="trust-links" aria-label="Правовая информация">
          <a href="/responsible-gaming/">Ответственная игра</a>
          <a href="/privacy-policy/">Политика конфиденциальности</a>
          <a href="/terms/">Условия использования</a>
          <a href="/contacts/">Контакты</a>
        </nav>
        <p class="copyright">© Selector Casino. Информационные материалы.</p>
      </div>
    </div>
  </footer>"""


def useful_links(exclude: str) -> str:
    links = [
        f'          <li><a href="{href}">{label}</a></li>'
        for key, label, href in USEFUL
        if key != exclude and exclude != "home"
    ]
    if exclude == "home":
        links = [
            f'          <li><a href="{href}">{label}</a></li>' for key, label, href in USEFUL
        ]
    return f"""    <section class="section-block useful-links-block">
      <div class="container">
        <h2>Полезные разделы селектор казино</h2>
        <ul class="useful-links-list">
{chr(10).join(links)}
        </ul>
      </div>
    </section>"""


def faq_block(faq: list, title: str) -> str:
    items = []
    for q in faq:
        items.append(
            f"""        <div class="faq-item">
          <strong>{q["q"]}</strong>
          <p>{q["a"]}</p>
        </div>"""
        )
    return f"""    <section class="section-block" id="faq">
      <div class="container">
        <h2>{title}</h2>
{chr(10).join(items)}
      </div>
    </section>"""


def section(h2: str, paragraphs: list, extra: str = "") -> str:
    ps = "\n".join(f"        <p>{p}</p>" for p in paragraphs)
    return f"""    <section class="section-block">
      <div class="container">
        <h2>{h2}</h2>
{ps}
{extra}
      </div>
    </section>"""


def render_page(page: dict) -> str:
    active = page.get("nav_active", "")
    hero_ps = "\n".join(f"          <p>{p}</p>" for p in page["hero_lead"])
    sections_html = "\n".join(page["sections"])
    faq_html = (
        faq_block(page["faq"], page.get("faq_title", "Частые вопросы о селектор казино"))
        if page.get("faq")
        else ""
    )
    useful = useful_links(page.get("exclude_useful", ""))
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
{head_block(page)}
</head>
<body>
{header_block(active)}
  <main>
    <section class="hero">
      <div class="container">
        <h1>{page["h1"]}</h1>
        <div class="hero-lead">
{hero_ps}
        </div>
        <div class="hero-actions">
          <a class="btn btn--cta" href="{AFF}" rel="{AFF_REL}" target="_blank">{page["cta"]}</a>
          <a class="hero-banner" href="{AFF}" rel="{AFF_REL}" target="_blank">
            <img src="/assets/img/selector-banner.png" width="1200" height="400" alt="{page["banner_alt"]}" loading="eager" fetchpriority="high" decoding="async">
          </a>
        </div>
      </div>
    </section>
{sections_html}
{useful}
{faq_html}
  </main>
{footer_block()}
  <script src="/script.js" defer></script>
</body>
</html>
"""


# --- Page definitions ---
def page_sections(topic: str):
    return [section(h2, paras) for h2, paras in PAGES[topic]["sections"]]


def build_pages():
    pages = []

    idx = PAGES["index"]
    pages.append(
        {
            "file": "index.html",
            "path": "/",
            "title": "Селектор казино — официальный сайт, вход и зеркало",
            "description": "Селектор казино: официальный сайт, вход, регистрация, бонусы, зеркало, ставки, казино и скачать приложение. Обзор Selector Casino.",
            "h1": "Селектор казино — обзор для игроков",
            "breadcrumb": "Главная",
            "cta": "Получить бонус",
            "banner_alt": "Селектор казино официальный сайт и бонусы",
            "nav_active": "home",
            "article": False,
            "exclude_useful": "home",
            "hero_lead": idx["hero"],
            "sections": page_sections("index"),
            "faq": PAGE_FAQ["index"],
            "faq_title": idx["faq_title"],
        }
    )

    page_specs = [
        {
            "file": "official-site.html",
            "path": "/official-site/",
            "topic": "official",
            "title": "Селектор казино официальный сайт — доступ и разделы",
            "description": "Официальный сайт селектор казино: как отличить подлинный адрес, вход, разделы казино и ставок, безопасность аккаунта Selector Casino.",
            "h1": "Selector официальный сайт",
            "breadcrumb": "Официальный сайт",
            "cta": "Официальный сайт",
            "banner_alt": "Селектор казино официальный сайт и разделы",
            "nav_active": "official-site",
            "exclude_useful": "official-site",
        },
        {
            "file": "login.html",
            "path": "/login/",
            "topic": "login",
            "title": "Селектор казино вход — как войти в аккаунт",
            "description": "Вход в селектор казино и личный кабинет Selector Casino: пошаговая авторизация, восстановление пароля и типовые ошибки входа.",
            "h1": "Селектор казино вход",
            "breadcrumb": "Вход",
            "cta": "Войти",
            "banner_alt": "Селектор казино вход в аккаунт",
            "nav_active": "login",
            "exclude_useful": "login",
        },
        {
            "file": "registration.html",
            "path": "/registration/",
            "topic": "registration",
            "title": "Селектор казино регистрация — как создать аккаунт",
            "description": "Регистрация в селектор казино: создание аккаунта Selector Casino, верификация, типовые ошибки и безопасность данных профиля.",
            "h1": "Селектор казино регистрация",
            "breadcrumb": "Регистрация",
            "cta": "Регистрация",
            "banner_alt": "Селектор казино регистрация аккаунта",
            "nav_active": "",
            "exclude_useful": "registration",
        },
        {
            "file": "zerkalo.html",
            "path": "/zerkalo/",
            "topic": "zerkalo",
            "title": "Селектор казино зеркало — рабочий доступ",
            "description": "Зеркало селектор казино: рабочий доступ Selector Casino при блокировках, проверка адреса и безопасный резервный вход.",
            "h1": "Селектор казино зеркало",
            "breadcrumb": "Зеркало",
            "cta": "Открыть зеркало",
            "banner_alt": "Селектор казино зеркало рабочий доступ",
            "nav_active": "zerkalo",
            "exclude_useful": "zerkalo",
        },
        {
            "file": "bets.html",
            "path": "/bets/",
            "topic": "bets",
            "title": "Селектор казино ставки — линия и события",
            "description": "Ставки в селектор казино: спортивная линия, live, купон и события Selector Casino. Как начать делать ставки безопасно.",
            "h1": "Селектор казино ставки",
            "breadcrumb": "Ставки",
            "cta": "Начать ставки",
            "banner_alt": "Селектор казино ставки и события",
            "nav_active": "bets",
            "exclude_useful": "bets",
        },
        {
            "file": "bonus.html",
            "path": "/bonus/",
            "topic": "bonus",
            "title": "Селектор казино бонусы — промо и предложения",
            "description": "Бонусы селектор казино: промокоды, приветственные акции Selector Casino, условия отыгрыша и типовые ошибки активации.",
            "h1": "Селектор казино бонусы",
            "breadcrumb": "Бонусы",
            "cta": "Получить бонус",
            "banner_alt": "Селектор казино бонусы и промо",
            "nav_active": "",
            "exclude_useful": "bonus",
        },
        {
            "file": "casino.html",
            "path": "/casino/",
            "topic": "casino",
            "title": "Селектор казино игры — слоты и раздел казино",
            "description": "Игры селектор казино: слоты, live casino и провайдеры Selector Casino. Как начать играть онлайн в казино-разделе.",
            "h1": "Селектор казино игры",
            "breadcrumb": "Казино",
            "cta": "Играть",
            "banner_alt": "Селектор казино игры и слоты",
            "nav_active": "casino",
            "exclude_useful": "casino",
        },
        {
            "file": "download.html",
            "path": "/download/",
            "topic": "download",
            "title": "Селектор казино скачать — приложение и мобильная версия",
            "description": "Скачать селектор казино: приложение, APK и мобильная версия Selector Casino для Android и iOS. Безопасная установка.",
            "h1": "Селектор казино скачать",
            "breadcrumb": "Скачать",
            "cta": "Скачать",
            "banner_alt": "Селектор казино скачать приложение",
            "nav_active": "download",
            "exclude_useful": "download",
        },
    ]

    for spec in page_specs:
        topic = spec["topic"]
        data = PAGES[topic]
        pages.append(
            {
                "file": spec["file"],
                "path": spec["path"],
                "title": spec["title"],
                "description": spec["description"],
                "h1": spec["h1"],
                "breadcrumb": spec["breadcrumb"],
                "cta": spec["cta"],
                "banner_alt": spec["banner_alt"],
                "nav_active": spec["nav_active"],
                "exclude_useful": spec["exclude_useful"],
                "article": True,
                "hero_lead": data["hero"],
                "sections": page_sections(topic),
                "faq": PAGE_FAQ[topic],
                "faq_title": data["faq_title"],
            }
        )

    for trust in TRUST_PAGES.values():
        sections = [section(h2, list(paras)) for h2, paras in trust["sections"]]
        pages.append(
            {
                "file": trust["file"],
                "path": trust["path"],
                "title": trust["title"],
                "description": trust["description"],
                "h1": trust["h1"],
                "breadcrumb": trust["breadcrumb"],
                "cta": "На главную",
                "banner_alt": "Selector Casino — информационный раздел",
                "nav_active": "",
                "article": False,
                "exclude_useful": "",
                "trust": True,
                "hero_lead": [trust["description"]],
                "sections": sections,
                "faq": None,
            }
        )

    return pages

def render_trust(page: dict) -> str:
    active = page.get("nav_active", "")
    hero_ps = "\n".join(f"          <p>{p}</p>" for p in page["hero_lead"])
    sections_html = "\n".join(page["sections"])
    useful = useful_links(page.get("exclude_useful", ""))
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
{head_block(page)}
</head>
<body>
{header_block(active)}
  <main>
    <section class="hero hero--compact">
      <div class="container">
        <h1>{page["h1"]}</h1>
        <div class="hero-lead">{hero_ps}</div>
      </div>
    </section>
{sections_html}
{useful}
  </main>
{footer_block()}
  <script src="/script.js" defer></script>
</body>
</html>
"""


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    try:
        import generate_favicons

        generate_favicons.main()
    except Exception as exc:
        print("Favicon generation skipped:", exc)
    for page in build_pages():
        html = render_trust(page) if page.get("trust") else render_page(page)
        path = os.path.join(root, page["file"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("Wrote", page["file"])


if __name__ == "__main__":
    main()
