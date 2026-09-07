"""Render the Industries hub and one page per industry from data/industries/*.json.

The JSON is written by research agents; this script owns every line of markup, so
the design system stays in one place and a data edit never needs an HTML edit.
Run it from the repo root:  python tools/build-industries.py
"""
import glob
import html
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, 'data', 'industries')
CAL = 'https://calendly.com/shiv-exdsconsulting/30min'

# Order and grouping of the hub. Slugs not listed here are dropped from the hub
# rather than silently appended in whatever order the filesystem returns.
GROUPS = [
    ('Where we have built', 'The industries our own engagements sit in. Each page names the work and what it taught us.', [
        'nightlife-hospitality', 'restaurants-bars', 'event-venues-ticketing',
        'telecom-isps', 'political-campaigns', 'tours-experiences',
    ]),
    ('Where the same build applies', 'Different rules, different systems of record, the same method. What we would build, and how it works.', [
        'law-firms', 'accounting-firms', 'healthcare-clinics', 'recruiting-staffing',
        'professional-services', 'insurance-brokers', 'real-estate-property',
        'construction-trades', 'home-services', 'logistics-transport',
        'manufacturing-distribution', 'retail-ecommerce', 'automotive-service',
        'fitness-wellness', 'education-training', 'nonprofits-associations',
    ]),
]
ORDER = [s for _, _, slugs in GROUPS for s in slugs]

DASHES = re.compile('[‒–—―−]')


def e(t):
    """Escape for HTML text, and fail loudly on any dash the site bans."""
    if DASHES.search(t):
        raise SystemExit('DASH in copy: ' + t[:120])
    return html.escape(t, quote=True)


def load():
    pages = {}
    for f in glob.glob(os.path.join(DATA, '*.json')):
        d = json.load(io.open(f, encoding='utf-8'))
        d.setdefault('slug', os.path.basename(f)[:-5])
        pages[d['slug']] = d
    return pages


# ---------------------------------------------------------------- shared chrome

def head(title, desc, extra_css=''):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#FAF9F7">
  <link rel="icon" href="assets/exodus-logo.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Exodus Consulting">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="assets/exodus-logo.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&display=swap">
  <link rel="stylesheet" href="css/exodus.css?v=12">
  <link rel="stylesheet" href="css/ia.css?v=12">
  <link rel="stylesheet" href="css/p-industries.css?v=12">{extra_css}
  <script src="js/exodus.js?v=12" defer></script>
</head>
<body>

<a class="ex-skip" href="#main">Skip to content</a>
'''


def header(current):
    def link(href, label):
        if href == current:
            return f'      <a class="ex-nav__link is-current" aria-current="page" href="{href}">{label}</a>'
        return f'      <a class="ex-nav__link" href="{href}">{label}</a>'
    nav = '\n'.join([
        link('index.html', 'Home'),
        link('services.html', 'What we build'),
        link('work.html', 'Our work'),
        link('industries.html', 'Industries'),
        link('guarantee.html', 'How we charge'),
        link('about.html', 'About'),
    ])
    feat = [s for s in ORDER[:6]]
    sub = '\n'.join(
        f'          <li><a href="industries-{s}.html">{e(TITLE_OF[s])}</a></li>' for s in feat)
    return f'''
<header class="ex-header">
  <div class="ex-header__inner">
    <a class="ex-brand" href="index.html">
      <img src="assets/exodus-logo.png" alt="Exodus Consulting" width="34" height="17">
      <span class="ex-brand__name">Exodus Consulting</span>
    </a>

    <nav class="ex-nav" aria-label="Primary">
{nav}
      <a class="ex-btn ex-btn--primary ex-btn--sm" href="{CAL}" target="_blank" rel="noopener">Book a free audit</a>
    </nav>

    <button class="ex-burger" type="button" data-nav-toggle aria-expanded="false" aria-controls="ex-mobile-menu">
      <span class="ex-burger__bars" aria-hidden="true"></span>
      <span>Menu</span>
    </button>
  </div>

  <div class="ex-mobile-menu" id="ex-mobile-menu">
    <ul class="ex-mobile-menu__list">
      <li><a href="index.html">Home</a></li>
      <li><a href="services.html">What we build</a></li>
      <li>
        <a href="work.html">Our work</a>
        <ul class="ia-submenu">
          <li><a href="work-uniserve.html">Uniserve Communications</a></li>
          <li><a href="work-fennec.html">Fennec</a></li>
          <li><a href="work-palapa-tours.html">Palapa Tours Ottawa</a></li>
          <li><a href="work-scoped.html">Current engagements</a></li>
          <li><a href="fennec-events-floor.html">Fennec: events and floor ops</a></li>
          <li><a href="fennec-ticketing-guests.html">Fennec: ticketing and guests</a></li>
          <li><a href="fennec-pos-payments.html">Fennec: POS and payments</a></li>
          <li><a href="fennec-inventory-staff.html">Fennec: inventory and staff</a></li>
          <li><a href="fennec-media-intelligence.html">Fennec: media and intelligence</a></li>
        </ul>
      </li>
      <li>
        <a href="industries.html">Industries</a>
        <ul class="ia-submenu">
          <li><a href="industries.html">All industries</a></li>
{sub}
        </ul>
      </li>
      <li><a href="guarantee.html">How we charge</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
    <a class="ex-btn ex-btn--primary ex-btn--block" href="{CAL}" target="_blank" rel="noopener">Book a free audit</a>
  </div>
</header>

<main id="main">
'''


def footer(blurb='AI enablement and custom software for owner-led businesses. Two founders, direct access.'):
    ind = '\n'.join(
        f'          <li><a href="industries-{s}.html">{e(TITLE_OF[s])}</a></li>' for s in ORDER[:6])
    return f'''
</main>

<footer class="ex-footer">
  <div class="ex-container">
    <div class="ex-footer__grid ia-sitemap">
      <div class="ex-footer__brand">
        <img src="assets/exodus-logo.png" alt="Exodus Consulting" width="44" height="23">
        <p class="ex-footer__blurb">{e(blurb)}</p>
      </div>

      <div class="ex-footer__col">
        <p class="ex-footer__title">Work</p>
        <ul>
          <li><a href="work.html">Our work</a></li>
          <li><a href="work-uniserve.html">Uniserve Communications</a></li>
          <li><a href="work-fennec.html">Fennec</a></li>
          <li><a href="work-palapa-tours.html">Palapa Tours Ottawa</a></li>
          <li><a href="work-scoped.html">Current engagements</a></li>
          <li><a href="fennec-events-floor.html">Fennec: events and floor</a></li>
          <li><a href="fennec-ticketing-guests.html">Fennec: ticketing and guests</a></li>
          <li><a href="fennec-pos-payments.html">Fennec: POS and payments</a></li>
          <li><a href="fennec-inventory-staff.html">Fennec: inventory and staff</a></li>
          <li><a href="fennec-media-intelligence.html">Fennec: media and intelligence</a></li>
        </ul>
      </div>

      <div class="ex-footer__col">
        <p class="ex-footer__title">Industries</p>
        <ul>
          <li><a href="industries.html">All industries</a></li>
{ind}
        </ul>
      </div>

      <div class="ex-footer__col">
        <p class="ex-footer__title">Company</p>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="services.html">What we build</a></li>
          <li><a href="guarantee.html">How we charge</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div class="ex-footer__col">
        <p class="ex-footer__title">Direct</p>
        <ul>
          <li><a href="mailto:shiv@exdsconsulting.com">shiv@exdsconsulting.com</a></li>
          <li><a href="{CAL}" target="_blank" rel="noopener">Book a free audit</a></li>
          <li><a href="https://instagram.com/exodus_consulting_" target="_blank" rel="noopener">@exodus_consulting_</a></li>
        </ul>
      </div>
    </div>

    <div class="ex-footer__legal">
      <span>&copy; 2026 Exodus Consulting</span>
      <span>Vancouver, BC</span>
    </div>
  </div>
</footer>

</body>
</html>
'''


def crumbs(items):
    out = []
    for label, href in items:
        if href:
            out.append(f'        <li class="ia-crumbs__item"><a class="ia-crumbs__link" href="{href}">{e(label)}</a></li>')
        else:
            out.append(f'        <li class="ia-crumbs__item"><span aria-current="page">{e(label)}</span></li>')
    body = '\n'.join(out)
    return f'''
  <nav class="ia-crumbs" aria-label="Breadcrumb">
    <div class="ex-container">
      <ol class="ia-crumbs__list">
{body}
      </ol>
    </div>
  </nav>
'''


def cta(title, lead):
    return f'''
  <section class="ex-band">
    <div class="ex-container">
      <div class="ex-split ex-split--wide">
        <div class="ex-stack">
          <p class="ex-eyebrow ex-eyebrow--onink">What happens next</p>
          <h2>{e(title)}</h2>
          <p class="ex-measure">{e(lead)}</p>
          <p class="ex-measure">We map where time and money leak, and show the arithmetic before you commit to anything. You keep the map whether or not you hire us. If we do build, we agree the baseline in writing first, the clock starts at deployment rather than signature, and you own the code.</p>
          <div class="ex-hero__actions">
            <a class="ex-btn ex-btn--primary" href="{CAL}" target="_blank" rel="noopener">Book a free audit</a>
            <a class="ex-btn ex-btn--onink" href="guarantee.html">How we charge</a>
          </div>
        </div>
        <div class="ex-stack">
          <dl class="ex-dl ex-dl--onink">
            <dt class="ex-dl__k">Who you talk to</dt>
            <dd class="ex-dl__v">Shiv and Vishal. No account managers, no slide decks.</dd>
            <dt class="ex-dl__k">Direct</dt>
            <dd class="ex-dl__v"><a href="mailto:shiv@exdsconsulting.com">shiv@exdsconsulting.com</a></dd>
            <dt class="ex-dl__k">Read next</dt>
            <dd class="ex-dl__v"><a href="services.html">What we build</a>, then <a href="work.html">Our work</a>.</dd>
          </dl>
        </div>
      </div>
    </div>
  </section>
'''


def disclose(idp, items, q, a, label_closed, label_open):
    """A stack of ex-disclose rows. items is a list of dicts with q/a keys."""
    rows = []
    for i, it in enumerate(items, 1):
        rows.append(f'''        <div class="ex-faq__item ex-disclose">
          <button class="ex-disclose__btn" type="button" data-disclose aria-expanded="false" aria-controls="{idp}-{i}">
            <span>{e(it[q])}</span>
            <span class="ex-disclose__icon" data-disclose-icon aria-hidden="true">+</span>
          </button>
          <div class="ex-disclose__panel" id="{idp}-{i}" data-collapsed="true">
            <div class="ex-disclose__inner">
              <p>{e(it[a])}</p>
            </div>
          </div>
        </div>''')
    return '      <div class="ex-faq">\n' + '\n'.join(rows) + '\n      </div>'


# ------------------------------------------------------------------ industry page

def render_page(d, prev_slug, next_slug):
    name = d['name']
    full = bool(d.get('what_we_built'))
    out = [head(d['meta_title'], d['meta_description']), header('industries.html')]
    out.append(crumbs([('Home', 'index.html'), ('Industries', 'industries.html'), (name, None)]))

    # 1. hero
    segs = '\n'.join(
        f'            <div class="ex-rail__item"><span class="ex-rail__v">{e(x)}</span></div>' for x in d['segments'])
    out.append(f'''
  <!-- ===================== 1. HERO ===================== -->
  <section class="ex-hero">
    <div class="ex-container">
      <div class="ex-hero__inner">
        <div>
          <p class="ex-eyebrow ex-eyebrow--violet">Industries / {e(name)}</p>
          <h1 class="ex-hero__title">{e(d['hero_title'])}</h1>
          <p class="ex-hero__lead">{e(d['hero_lead'])}</p>
          <div class="ex-hero__actions">
            <a class="ex-btn ex-btn--primary" href="{CAL}" target="_blank" rel="noopener">Book a free audit</a>
            <a class="ex-btn ex-btn--secondary" href="industries.html">All industries</a>
          </div>
        </div>

        <div class="ex-hero__meta">
          <p class="ex-eyebrow">Who this is for</p>
          <aside class="ex-rail" aria-label="Segments within {e(name)}">
{segs}
          </aside>
        </div>
      </div>
    </div>
  </section>
''')

    # 2. how it runs (ink band, numbered)
    steps = '\n'.join(f'''        <li class="ex-timeline__step">
          <span class="ex-timeline__num">{i:02d}</span>
          <div>
            <h3 class="ex-timeline__title">{e(x['title'])}</h3>
            <p class="ex-timeline__body">{e(x['body'])}</p>
          </div>
        </li>''' for i, x in enumerate(d['how_it_runs'], 1))
    out.append(f'''
  <!-- ===================== 2. HOW IT ACTUALLY RUNS ===================== -->
  <section class="ex-band">
    <div class="ex-container">
      <p class="ex-eyebrow ex-eyebrow--onink">How it actually runs</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">Before anything is built, this is the week we are describing.</h2>
        <p class="ex-shead__sub">No software can be scoped from a category name. These are the specifics of {e(name.lower())} that decide what is worth building and what is not.</p>
      </header>

      <ol class="ex-timeline">
{steps}
      </ol>
    </div>
  </section>
''')

    # 3. leaks table
    rows = '\n'.join(f'''                  <tr>
                    <th scope="row">{e(x['leak'])}</th>
                    <td>{e(x['how_measured'])}</td>
                    <td>{e(x['what_closes_it'])}</td>
                  </tr>''' for x in d['leaks'])
    out.append(f'''
  <!-- ===================== 3. WHERE IT LEAKS ===================== -->
  <section class="ex-section">
    <div class="ex-container">
      <p class="ex-eyebrow">Where it leaks</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">Every one of these is measurable. Most are not measured.</h2>
        <p class="ex-shead__sub">The free audit prices these in your own numbers before anything is scoped. You keep the map whether or not you hire us.</p>
      </header>

      <div class="ex-table-wrap">
        <table class="ex-table p-ind__table">
          <caption>Where the money and the hours go in {e(name.lower())}, how it is measured today, and what closes it.</caption>
          <thead>
            <tr>
              <th scope="col">The leak</th>
              <th scope="col">How it is measured today</th>
              <th scope="col">What closes it</th>
            </tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </div>
  </section>
'''.replace('                  <tr>', '            <tr>').replace('                    <th', '              <th').replace('                    <td', '              <td').replace('                  </tr>', '            </tr>'))

    # 4. what we build
    cards = '\n'.join(f'''        <article class="ex-card">
          <div class="ex-card__head">
            <h3 class="ex-card__title">{e(x['title'])}</h3>
          </div>
          <p class="ex-card__body">{e(x['mechanism'])}</p>
          <p class="ex-card__foot">Measured by: {e(x['measure'])}</p>
        </article>''' for x in d['builds'])
    out.append(f'''
  <!-- ===================== 4. WHAT WE BUILD ===================== -->
  <section class="ex-section ex-section--paper-2">
    <div class="ex-container">
      <p class="ex-eyebrow">What we build</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">{len(d['builds'])} builds that pay for themselves here.</h2>
        <p class="ex-shead__sub">Each one states what it reads, what it does, and what a person still approves. Scope is agreed after the audit, one build at a time, against a baseline you sign.</p>
      </header>

      <div class="ex-grid">
{cards}
      </div>
    </div>
  </section>
''')

    # 5. stats (ink band)
    def stat_size(fig):
        # A bare "44%" carries the full display size. A figure with words in it
        # ("over 6,400 complaints a week") wraps to four lines if it does.
        n = len(fig)
        return '' if n <= 10 else (' p-ind__stat--md' if n <= 22 else ' p-ind__stat--sm')

    stats = '\n'.join(f'''            <div class="ex-stat ex-stat--onink{stat_size(x['figure'])}">
              <span class="ex-stat__num">{e(x['figure'])}</span>
              <p class="ex-stat__label">{e(x['claim'])}</p>
              <cite class="ex-stat__source"><a class="ex-link ex-link--mono" href="{e(x['url'])}" target="_blank" rel="noopener">{e(x['source_org'])}, {e(x['year'])}</a></cite>
              <p class="p-ind__caveat">{e(x['caveat'])}</p>
            </div>''' for x in d['stats'])
    out.append(f'''
  <!-- ===================== 5. THE NUMBERS ===================== -->
  <section class="ex-band">
    <div class="ex-container">
      <p class="ex-eyebrow ex-eyebrow--onink">The numbers</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">Borrowed statistics, with their sources and their limits printed.</h2>
        <p class="ex-shead__sub">None of these are our results. They are the published state of {e(name.lower())}, linked so you can check them, with the caveat attached where the number is a survey, a forecast or a vendor's own figure.</p>
      </header>

      <div class="ex-stats">
{stats}
      </div>
    </div>
  </section>
''')

    # 6. systems
    sys_cards = '\n'.join(f'''        <article class="ex-card ex-card--inset">
          <div class="ex-card__head">
            <h3 class="ex-card__title">{e(x['name'])}</h3>
          </div>
          <p class="ex-card__body"><strong>Usually:</strong> {e(x['examples'])}</p>
          <p class="ex-card__body"><strong>What it holds.</strong> {e(x['holds'])}</p>
          <p class="ex-card__body"><strong>How we connect.</strong> {e(x['how_we_connect'])}</p>
          <p class="ex-card__foot"><strong>Where it stops.</strong> {e(x['where_it_stops'])}</p>
        </article>''' for x in d['systems'])
    out.append(f'''
  <!-- ===================== 6. WHERE THE DATA COMES FROM ===================== -->
  <section class="ex-section">
    <div class="ex-container">
      <p class="ex-eyebrow">Where the data comes from</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">Your systems of record stay exactly where they are.</h2>
        <p class="ex-shead__sub">We read them, we do not replace them. Each one below says what we connect to, how, and the line the build does not cross.</p>
      </header>

      <div class="ex-grid">
{sys_cards}
      </div>
    </div>
  </section>
''')

    # 7. rules. The ABC engagement is described with no AI framing anywhere on the
    #    page, so this section's own chrome has to avoid the word as well.
    no_ai = d['slug'] == 'political-campaigns'
    wont_head = 'Where we stop' if no_ai else 'What we will not automate'
    loop_body = ('Anything that spends money, sends something irreversible, or carries a legal '
                 'obligation arrives as a draft with a named reviewer. The system prepares the '
                 'work. A person decides whether it ships.') if no_ai else (
                 'Anything that spends money, sends something irreversible, or carries a professional '
                 'obligation arrives as a draft with a named reviewer. The system prepares the work. '
                 'A person decides whether it ships.')
    rrows = '\n'.join(f'''            <tr>
              <th scope="row">{e(x['regime'])}</th>
              <td>{e(x['demands'])}</td>
              <td>{e(x['how_we_comply'])}</td>
            </tr>''' for x in d['rules'])
    wont = '\n'.join(f'          <li>{e(x)}</li>' for x in d['wont_automate'])
    out.append(f'''
  <!-- ===================== 7. THE RULES ===================== -->
  <section class="ex-section ex-section--paper-2">
    <div class="ex-container">
      <p class="ex-eyebrow">Built around your rules</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">The regimes that govern this work, and how the build answers each one.</h2>
        <p class="ex-shead__sub">Constraints come first, because they decide the architecture. Bring us your hosting, residency and regulatory rules at the start and we design to them rather than around them.</p>
      </header>

      <div class="ex-table-wrap">
        <table class="ex-table p-ind__table">
          <caption>Regulatory and professional obligations that shape a build in {e(name.lower())}.</caption>
          <thead>
            <tr>
              <th scope="col">Regime</th>
              <th scope="col">What it demands here</th>
              <th scope="col">How the build complies</th>
            </tr>
          </thead>
          <tbody>
{rrows}
          </tbody>
        </table>
      </div>

      <hr class="ex-rule ex-rule--spaced">

      <div class="ex-split">
        <div class="ex-stack">
          <h3>{wont_head}</h3>
          <ul class="ex-measure">
{wont}
          </ul>
        </div>
        <div class="ex-stack">
          <div class="ex-card ex-card--inset">
            <div class="ex-card__head">
              <h3 class="ex-card__title">A person stays in the loop</h3>
            </div>
            <p class="ex-card__body">{loop_body}</p>
            <p class="ex-card__foot">You own the code and the data at the end of the engagement.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
''')

    # 7b. product captures, where the industry has any. Optional "shots" key in
    #     the JSON: real screens from software we run, never a mockup.
    shots = d.get('shots') or []
    if shots:
        chips, panels = [], []
        for i, sh in enumerate(shots):
            sel = 'true' if i == 0 else 'false'
            chips.append(
                f'          <button class="ex-scroller__chip" type="button" data-scroller-tab aria-selected="{sel}">\n'
                f'            <span class="ex-scroller__chip-num">{i + 1:02d}</span>\n'
                f'            <span class="ex-scroller__chip-name">{e(sh["name"])}</span>\n'
                f'          </button>')
            # Only the open panel loads eagerly; the scroller swaps data-src in.
            attr = 'src' if i == 0 else 'data-src'
            lazy = '' if i == 0 else ' loading="lazy"'
            panels.append(
                f'          <div class="ex-scroller__panel" data-scroller-panel>\n'
                f'            <div class="ex-scroller__panel-grid">\n'
                f'              <figure class="ex-shot">\n'
                f'                <div class="ex-shot__frame">\n'
                f'                  <img class="ex-shot__img" {attr}="{e(sh["src"])}" width="{sh["w"]}" height="{sh["h"]}" alt="{e(sh["alt"])}"{lazy} decoding="async">\n'
                f'                </div>\n'
                f'                <figcaption class="ex-shot__caption">{e(sh["caption"])}</figcaption>\n'
                f'              </figure>\n'
                f'              <div>\n'
                f'                <h3 class="ex-scroller__panel-title">{e(sh["title"])}</h3>\n'
                f'                <p class="ex-scroller__panel-quote">{e(sh["body"])}</p>\n'
                f'                <p class="ex-scroller__panel-venues">Live product capture</p>\n'
                f'              </div>\n'
                f'            </div>\n'
                f'          </div>')
        chips_s = '\n'.join(chips)
        panels_s = '\n\n'.join(panels)
        out.append(f'''
  <!-- ===================== 7b. THE PRODUCT, RUNNING ===================== -->
  <section class="ex-section">
    <div class="ex-container">
      <p class="ex-eyebrow">The product, running</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">{e(d.get('shots_title', 'Real screens from software we run in this industry.'))}</h2>
        <p class="ex-shead__sub">{e(d.get('shots_sub', 'Captures from the live product, not mockups. Cropped only to remove account identifiers.'))}</p>
      </header>

      <div class="ex-fig">
        <span class="ex-fig__num">FIG. 01</span>
        <span class="ex-fig__label">Product gallery, {len(shots)} live surfaces</span>
      </div>

      <div class="ex-scroller" id="ind-surfaces" data-scroller>
        <div class="ex-scroller__head">
          <p class="ex-scroller__title">Scroll or select a surface</p>
          <div class="ex-scroller__nav">
            <button class="ex-scroller__btn" type="button" data-scroller-prev aria-label="Scroll surfaces left">&lt;</button>
            <button class="ex-scroller__btn" type="button" data-scroller-next aria-label="Scroll surfaces right">&gt;</button>
          </div>
        </div>

        <div class="ex-scroller__rail" data-scroller-rail aria-label="Product surfaces">
{chips_s}
        </div>

        <div class="ex-scroller__panels">
{panels_s}
        </div>
      </div>
    </div>
  </section>
''')

    # 8. our work here (full pages only)
    if full:
        built = '\n'.join(f'''        <article class="ex-card">
          <div class="ex-card__head">
            <h3 class="ex-card__title">{e(x['title'])}</h3>
          </div>
          <p class="ex-card__body">{e(x['body'])}</p>
        </article>''' for x in d['what_we_built'])
        learned = '\n'.join(f'''        <li class="ex-index__row">
          <span class="ex-index__num">{i:02d}</span>
          <div>
            <p class="ex-index__note">{e(x)}</p>
          </div>
        </li>''' for i, x in enumerate(d['learned'], 1))
        out.append(f'''
  <!-- ===================== 8. OUR WORK HERE ===================== -->
  <section class="ex-section">
    <div class="ex-container">
      <p class="ex-eyebrow">Our work here</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">What we have built in this industry, at its real status.</h2>
        <p class="ex-shead__sub">Live means running now. In build means under construction, with some phases delivered and some not. Shipped means delivered and closed. Where there is no number yet, we say so instead of borrowing one.</p>
      </header>

      <div class="ex-grid">
{built}
      </div>

      <hr class="ex-rule ex-rule--spaced">

      <h3>What the work taught us</h3>
      <ol class="ex-index">
{learned}
      </ol>
    </div>
  </section>
''')

        if d.get('objections'):
            obj = disclose('obj', d['objections'], 'objection', 'answer', '', '')
            out.append(f'''
  <!-- ===================== 9. THE OBJECTIONS ===================== -->
  <section class="ex-section ex-section--paper-2">
    <div class="ex-container">
      <p class="ex-eyebrow">The objections</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">The reasons an owner here says no, answered straight.</h2>
      </header>

{obj}
    </div>
  </section>
''')

    # 10. FAQ
    faq = disclose('faq', d['faq'], 'q', 'a', '', '')
    out.append(f'''
  <!-- ===================== 10. FAQ ===================== -->
  <section class="ex-section">
    <div class="ex-container">
      <p class="ex-eyebrow">Questions</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">The questions we get asked in {e(name.lower())}.</h2>
      </header>

{faq}
    </div>
  </section>
''')

    out.append(cta('Start with the audit, and know the number before you commit.',
                   f'Three to five days. We map where the hours and the money go in your {e(name.lower())} operation and hand you a ranked plan with the payback attached.'))

    # related
    out.append(f'''
  <!-- ===================== RELATED ===================== -->
  <section class="ex-section ex-section--tight ia-related" aria-labelledby="related-heading">
    <div class="ex-container">
      <p class="ex-eyebrow">Keep reading</p>
      <h2 class="ex-shead__title" id="related-heading">Where to go next</h2>

      <ul class="ia-related__grid">
        <li>
          <a class="ex-card ia-related__card" href="industries.html">
            <p class="ia-related__kicker">Back up</p>
            <h3 class="ex-card__title">All industries</h3>
            <p class="ex-card__body">Every industry we build for, grouped by where our own work sits and where the same method applies.</p>
            <span class="ia-related__go">See the index <span class="ia-related__arrow" aria-hidden="true">-&gt;</span></span>
          </a>
        </li>
        <li>
          <a class="ex-card ia-related__card" href="work.html">
            <p class="ia-related__kicker">The proof</p>
            <h3 class="ex-card__title">Our work</h3>
            <p class="ex-card__body">Five engagements at their real status, with the Fennec product gallery and the arithmetic behind every number.</p>
            <span class="ia-related__go">Read the studies <span class="ia-related__arrow" aria-hidden="true">-&gt;</span></span>
          </a>
        </li>
        <li>
          <a class="ex-card ia-related__card ia-related__card--next" href="industries-{next_slug}.html">
            <p class="ia-related__kicker">Next industry</p>
            <h3 class="ex-card__title">{e(TITLE_OF[next_slug])}</h3>
            <p class="ex-card__body">The same method, a different set of systems, rules and failure modes.</p>
            <span class="ia-related__go">Next <span class="ia-related__arrow" aria-hidden="true">-&gt;</span></span>
          </a>
        </li>
      </ul>
    </div>
  </section>
''')

    out.append(footer('Custom software and data work for owner-led organisations. Two founders, direct access.') if no_ai else footer())
    return ''.join(out)


# ------------------------------------------------------------------------- hub

def render_hub(pages):
    out = [head('Industries: every sector we build for | Exodus Consulting',
                'Custom software and AI enablement across ' + str(len(pages)) + ' industries. The same method, adapted to each sector\'s systems of record, rules and failure modes.'),
           header('industries.html')]
    out.append(crumbs([('Home', 'index.html'), ('Industries', None)]))

    have = [s for s in GROUPS[0][2] if s in pages]
    out.append(f'''
  <!-- ===================== 1. HERO ===================== -->
  <section class="ex-hero">
    <div class="ex-container">
      <div class="ex-hero__inner">
        <div>
          <p class="ex-eyebrow ex-eyebrow--violet">Industries</p>
          <h1 class="ex-hero__title">{len(pages)} industries. One method.</h1>
          <p class="ex-hero__lead">The way we build does not change: learn the operation first, find the one workflow worth fixing, agree the number in writing, then ship software the team actually uses. What changes per industry is the systems of record, the rules, and the failure that costs the most. Each page below is written for one sector, and says which.</p>
          <div class="ex-hero__actions">
            <a class="ex-btn ex-btn--primary" href="{CAL}" target="_blank" rel="noopener">Book a free audit</a>
            <a class="ex-btn ex-btn--secondary" href="work.html">See the work</a>
          </div>
        </div>

        <div class="ex-hero__meta">
          <p class="ex-eyebrow">At a glance</p>
          <aside class="ex-rail" aria-label="Industries at a glance">
            <div class="ex-rail__item"><span class="ex-rail__k">Industries</span><span class="ex-rail__v">{len(pages)}</span></div>
            <div class="ex-rail__item"><span class="ex-rail__k">With our own work in them</span><span class="ex-rail__v">{len(have)}</span></div>
            <div class="ex-rail__item"><span class="ex-rail__k">Base</span><span class="ex-rail__v">Vancouver, BC</span></div>
            <div class="ex-rail__item"><span class="ex-rail__k">Client type</span><span class="ex-rail__v">Owner-led</span></div>
          </aside>
        </div>
      </div>
    </div>
  </section>
''')

    # what stays the same
    out.append('''
  <!-- ===================== 2. WHAT STAYS THE SAME ===================== -->
  <section class="ex-band">
    <div class="ex-container">
      <div class="ex-split ex-split--wide">
        <div class="ex-stack">
          <p class="ex-eyebrow ex-eyebrow--onink">What stays the same</p>
          <h2>The method does not change when the industry does.</h2>
          <p class="ex-measure">The first week of every engagement is spent on the floor rather than in a repository: we learn the job the way the team does it, in their words, on their screens. Then we build the piece that removes the part they hate, and we stay until they use it without us.</p>
          <p class="ex-measure">Your systems of record stay where they are. We read them and write back only where you have said we can, and anything irreversible arrives as a draft with a named reviewer.</p>
        </div>
        <div class="ex-stack">
          <dl class="ex-dl ex-dl--onink">
            <dt class="ex-dl__k">The audit comes first</dt>
            <dd class="ex-dl__v">Three to five days mapping where the hours and the money actually go, ending in a ranked plan with the payback math. Yours to keep, whoever builds it.</dd>
            <dt class="ex-dl__k">The number is agreed in writing</dt>
            <dd class="ex-dl__v">You sign off on the baseline before the build starts. The clock starts at deployment, not at signature.</dd>
            <dt class="ex-dl__k">A person stays in the loop</dt>
            <dd class="ex-dl__v">Anything that spends money, sends something irreversible or carries a professional obligation is a draft until someone approves it.</dd>
            <dt class="ex-dl__k">You own it</dt>
            <dd class="ex-dl__v">The code and the data are yours, written into the agreement before anything is built.</dd>
          </dl>
        </div>
      </div>
    </div>
  </section>
''')

    # the groups
    for gi, (gtitle, gsub, slugs) in enumerate(GROUPS, 1):
        live = [s for s in slugs if s in pages]
        if not live:
            continue
        rows = []
        for i, s in enumerate(live, 1):
            d = pages[s]
            rows.append(f'''        <li class="ex-index__row">
          <span class="ex-index__num">{i:02d}</span>
          <div>
            <p class="ex-index__title"><a class="ex-link ex-link--quiet" href="industries-{s}.html">{e(d['name'])}</a></p>
            <p class="ex-index__note">{e(d['hero_title'])}</p>
            <p class="ex-index__note">{e('. '.join(x['title'] for x in d['builds'][:3]))}</p>
          </div>
        </li>''')
        body = '\n'.join(rows)
        cls = 'ex-section' if gi == 1 else 'ex-section ex-section--paper-2'
        out.append(f'''
  <!-- ===================== GROUP {gi} ===================== -->
  <section class="{cls}">
    <div class="ex-container">
      <p class="ex-eyebrow">{e(gtitle)}</p>
      <header class="ex-shead ex-shead--wide">
        <h2 class="ex-shead__title">{e(gtitle)}</h2>
        <p class="ex-shead__sub">{e(gsub)}</p>
      </header>

      <ol class="ex-index">
{body}
      </ol>
    </div>
  </section>
''')

    out.append(cta('Your industry is on this page, or it is the next one we write.',
                   'Start with a call or start with the audit. Either way you talk to the two people who will build it, not a sales inbox.'))
    out.append(footer())
    return ''.join(out)


# ------------------------------------------------------------------------- main

pages = load()
TITLE_OF = {s: d['name'] for s, d in pages.items()}
missing = [s for s in ORDER if s not in pages]
extra = [s for s in pages if s not in ORDER]
if extra:
    raise SystemExit('slug not in GROUPS, refusing to orphan it: ' + ', '.join(extra))
if missing and '--partial' not in sys.argv:
    raise SystemExit('missing data for: ' + ', '.join(missing) + '\n(pass --partial to build anyway)')
if missing:
    print('PARTIAL BUILD, missing:', ', '.join(missing))

live = [s for s in ORDER if s in pages]
for i, s in enumerate(live):
    prev_s = live[i - 1]
    next_s = live[(i + 1) % len(live)]
    out = os.path.join(REPO, f'industries-{s}.html')
    io.open(out, 'w', encoding='utf-8', newline='').write(render_page(pages[s], prev_s, next_s))

io.open(os.path.join(REPO, 'industries.html'), 'w', encoding='utf-8', newline='').write(render_hub(pages))
print(f'built industries.html + {len(live)} industry pages')
