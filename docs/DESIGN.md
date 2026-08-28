# Exodus Design System v4 - handbook

One stylesheet (`css/exodus.css`), one IA layer (`css/ia.css`), one script (`js/exodus.js`), and the segmented
page set in section 0. `exodus.css` and `exodus.js` are FROZEN. Copy head, header and footer verbatim from
`css/PARTIALS.html`. Cache-bust every css and js link with `?v=11`.

Load order in the head, exactly this: Google Fonts, then `css/exodus.css?v=11`, then `css/ia.css?v=11`, then
`js/exodus.js?v=11` deferred. `ia.css` holds the breadcrumb, the related-pages block, the index-page secondary
link row, the grouped mobile sub-lists and the footer sitemap grid. It uses existing tokens only and adds no
colours. Do not edit `exodus.css` to make room for it.

Page CSS only if unavoidable: `css/p-<page>.css`, loaded after `ia.css`.

---

## 0. Information architecture

The site is segmented. Each page does one job and routes onward. Nobody scrolls an everything-page.

**Top level, and the only things in `.ex-nav`:**

| File | Job |
| --- | --- |
| `index.html` | Home. A short routing overview: the problem, the proof, and links out. Not an everything-page. |
| `services.html` | What we build. The capability index, built on the `[data-tabs]` switcher. |
| `work.html` | Our work. A short INDEX of the four case studies that links out. No full studies here. |
| `solutions.html` | Solutions. A short INDEX of the five Fennec solution families that links out. |
| `guarantee.html` | How we charge. The agreed-baseline terms, the free audit, code ownership. |
| `about.html` | About. The two founders, how the engagement runs. |
| `contact.html` | Contact. Reached from the footer and the mobile drawer, never from `.ex-nav`. |

**Case study detail pages, linked from `work.html`:**

| File | Job |
| --- | --- |
| `work-uniserve.html` | Uniserve Communications. IN BUILD. The 3-month AI enablement programme, the customer-facing chatbot and voice agent, the Canada-hosting constraint, the labelled PROJECTION with its arithmetic. |
| `work-fennec.html` | Fennec. LIVE. The flagship venue operating system, Ferry AI, the Revenue Copilot. Carries `table-select.jpg`. |
| `work-palapa-tours.html` | Palapa Tours Ottawa. SHIPPED. Tip-out variance and the custom tip-out software that ended the disputes. |
| `work-scoped.html` | Scoped engagements. Matchbox Global (IN BUILD), Market Meats (PROPOSED), Royal Feet (PROPOSED). |

**Solution family detail pages, linked from `solutions.html`:**

| File | Job |
| --- | --- |
| `solutions-events-floor.html` | 01 Events and floor ops. Floor plan editor, live table statuses, the guest table map. |
| `solutions-ticketing-guests.html` | 02 Ticketing and guests. Event pages, ticket sales, guestlists, scanner check-in, passes. |
| `solutions-pos-payments.html` | 03 POS and payments. Square, Toast and Lightspeed sync. Needs an INTERFACE DIAGRAM, no screenshot exists. |
| `solutions-inventory-staff.html` | 04 Inventory and loss prevention plus 05 Staff and payouts. Poured vs sold variance and tip-out splits, both as INTERFACE DIAGRAMS. |
| `solutions-media-intelligence.html` | 06 Media and marketing plus 07 Intelligence and automation. Campaign composer, email designer, Ferry AI. |

Count note: the brief calls this the 18-page structure. The enumerated route table above is 16 HTML files at
the repo root, which is the authoritative list. If two more pages are added later they go in this table first,
then into the footer sitemap in `css/PARTIALS.html` block C, and nowhere else.

### Page length rule

- **Detail page: 4 to 7 sections.** Breadcrumb, then the sections, then the related-pages block.
- **Index page: 4 to 5 sections.** Hero, secondary link row, the cards that route out, one closing call.
- Past 8 sections you are rebuilding the everything-page. Split it or cut it.

### Sub-navigation decision: no dropdown

`js/exodus.js` is frozen, so a menu with real `aria-expanded` state, Escape handling and focus return cannot
be wired, and a CSS hover menu would miss on touch and can trap keyboard users. So the top-level nav stays six
links plus the violet CTA, and the detail pages are reached four other ways, all of them plain visible links:

1. `.ia-subnav`, a visible secondary link row, on `work.html` and `solutions.html` **only** (PARTIALS block F).
2. Grouped `.ia-submenu` sub-lists nested in the existing mobile drawer. Plain nested lists, visible whenever
   the drawer is open, no new script.
3. The related-pages block at the foot of every detail page.
4. The footer sitemap, identical on every page, which reaches all 16 pages.

Never put detail-page links in `.ex-nav`. On a case study page mark `Our work` as current; on a solution
family page mark `Solutions`.

## 1. Fonts

```
--font-sans: "Geist", "DM Sans", system-ui, -apple-system, sans-serif;
--font-mono: "Geist Mono", ui-monospace, monospace;
```

Google Fonts link (verified, use exactly this):

```
https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&display=swap
```

Headings use weight 500. Body 400 at 17 to 19px, line-height 1.65. Never above 700. Large headings get
`letter-spacing: -0.02em`. Mono labels are 12 to 13px, uppercase, `letter-spacing: 0.12em`.

## 2. Tokens

Palette: `--paper --paper-2 --paper-3 --card --ink --ink-2 --ink-3 --line --line-2 --violet --violet-2
--violet-soft --blue --blue-soft --ok`

Spacing: `--space-3xs 4` `--space-2xs 8` `--space-xs 12` `--space-sm 16` `--space-md 24` `--space-lg 32`
`--space-xl 48` `--space-2xl 72` `--space-3xl 104` `--space-4xl 144` (the last three shrink at breakpoints).

Type: `--t-mono-sm --t-mono --t-xs --t-sm --t-body --t-lead --t-h4 --t-h3 --t-h2 --t-h1 --t-stat`
(all the headline sizes are fluid `clamp()`; h1 runs 44 to 68px).

Radius: `--r-sm 8px` `--r-md 10px` `--r-lg 12px`. Shadow: `--shadow` (the only one).
Hairlines: `--hairline` and `--hairline-2`. Layout: `--container 1200px` `--gutter` `--measure` `--nav-h`.
Motion: `--ease --dur --dur-slow`.

Accent budget: violet is primary, blue secondary, combined accent coverage under about 8% of a light page.
Two to three `--ink` dark bands per page for rhythm.

## 3. Layout primitives

| Class | Note | Example |
| --- | --- | --- |
| `.ex-container` | Max 1200px, fluid gutters. Wrap all content. | `<div class="ex-container">...</div>` |
| `.ex-section` | Vertical rhythm. Variants `--tight --flush --ruled --paper-2 --paper-3`. | `<section class="ex-section">` |
| `.ex-split` | Wide content + 17rem mono rail. Variants `--rail-left --wide`. Stacks at 820. | `<div class="ex-split"><div>...</div><aside class="ex-rail">...</aside></div>` |
| `.ex-bleed` | Full viewport width inside a container. | `<div class="ex-bleed">` |
| `.ex-rule` | Hairline separator. `--strong --spaced`. | `<hr class="ex-rule">` |
| `.ex-grid` | Auto-fit grid. `--2 --4`. Never build an icon-tile 3-up. | `<div class="ex-grid ex-grid--2">` |
| `.ex-stack` / `.ex-stack-lg` | Owl spacing. | `<div class="ex-stack">` |
| `.ex-measure` / `.ex-measure-narrow` | 68ch / 52ch reading width. | `<p class="ex-measure">` |
| `.ex-visually-hidden` | Screen-reader only text. | `<span class="ex-visually-hidden">` |
| `.ex-skip` | Skip link, first element in body. | `<a class="ex-skip" href="#main">` |

## 4. Components

| Class | Note | Example |
| --- | --- | --- |
| `.ex-header` `.ex-header__inner` | Sticky, hairline bottom, left brand. | see PARTIALS |
| `.ex-brand` `.ex-brand__name` | Logo sized by WIDTH (34px header, 44px footer). | `<a class="ex-brand">` |
| `.ex-nav` `.ex-nav__link` `.is-current` | Desktop links, hidden under 900px. | `<a class="ex-nav__link is-current" aria-current="page">` |
| `.ex-burger` `.ex-burger__bars` | Mobile toggle, shown under 900px. | `<button class="ex-burger" data-nav-toggle>` |
| `.ex-mobile-menu` `.ex-mobile-menu__list` `.is-open` | Mobile drawer, includes Contact. | see PARTIALS |
| `.ex-footer` `.ex-footer__grid __brand __blurb __col __title __legal` | Brand + three link columns + 2026 line. | see PARTIALS |
| `.ex-eyebrow` | Mono label above every major section. `--violet --onink`. | `<p class="ex-eyebrow">What we build</p>` |
| `.ex-fig` `.ex-fig__num` `.ex-fig__label` | FIG. plate above every shot, diagram and module. `--onink`. | `<div class="ex-fig"><span class="ex-fig__num">FIG. 04</span><span class="ex-fig__label">Interface diagram</span></div>` |
| `.ex-shead` `.ex-shead__title` `.ex-shead__sub` | Left-aligned section header. Never centered. | `<header class="ex-shead"><h2 class="ex-shead__title">...</h2><p class="ex-shead__sub">...</p></header>` |
| `.ex-hero` `.ex-hero__inner __title __lead __actions __meta` | Asymmetric left-aligned hero. | `<section class="ex-hero"><div class="ex-container"><div class="ex-hero__inner">...` |
| `.ex-index` `.ex-index__row __num __title __note` | Numbered problem index. | `<li class="ex-index__row"><span class="ex-index__num">01</span><div><p class="ex-index__title">...</p></div></li>` |
| `.ex-stats` `.ex-stat` `.ex-stat__num __unit __label __source` | Big Geist-500 numeral, hairline, mono source. `--onink`. | `<div class="ex-stat"><span class="ex-stat__num">95<span class="ex-stat__unit">%</span></span><p class="ex-stat__label">of enterprise AI pilots show no measurable P&L return.</p><cite class="ex-stat__source">MIT NANDA, The GenAI Divide, 2025</cite></div>` |
| `.ex-rail` `.ex-rail__item __k __v` | Mono metadata rail. `--onink`. | `<aside class="ex-rail"><div class="ex-rail__item"><span class="ex-rail__k">Status</span><span class="ex-rail__v">In build</span></div></aside>` |
| `.ex-tag` | Proof tag. `--live --build --shipped --proposed --projection --onink`. | `<span class="ex-tag ex-tag--live">Live</span>` |
| `.ex-band` `.ex-band--tight` | Full-width `--ink` section. Use 2 to 3 per page. | `<section class="ex-band"><div class="ex-container">...</div></section>` |
| `.ex-card` `.ex-card--raised --inset --onink --flush` `.ex-card__head __title __body __foot` | White, hairline, 10px radius. Shadow only on `--raised`. | `<article class="ex-card"><div class="ex-card__head"><h3 class="ex-card__title">...</h3><span class="ex-tag">...</span></div><p class="ex-card__body">...</p></article>` |
| `.ex-quote` `.ex-quote__text __cite` | Pull quote, violet 2px left edge. | `<blockquote class="ex-quote"><p class="ex-quote__text">...</p><cite class="ex-quote__cite">Fennec product copy</cite></blockquote>` |
| `.ex-shot` `.ex-shot__frame __img __caption` `--onink --wide` | Screenshot frame. FIG. plate above, caption below. | `<div class="ex-fig">...</div><figure class="ex-shot"><div class="ex-shot__frame"><img class="ex-shot__img" src="..." width="2000" height="953" alt="..."></div><figcaption class="ex-shot__caption">...</figcaption></figure>` |
| `.ex-diagram` `.ex-diagram__bar __dot __body __flow __node __node-k __arrow __caption` | Honest HTML interface diagram. Caption must say INTERFACE DIAGRAM. `__node--accent --primary --ok`. | `<div class="ex-diagram"><div class="ex-diagram__bar"><span class="ex-diagram__dot"></span>POS sync</div><div class="ex-diagram__body"><div class="ex-diagram__flow"><div class="ex-diagram__node"><span class="ex-diagram__node-k">Source</span>Square</div><span class="ex-diagram__arrow">-&gt;</span>...</div></div><p class="ex-diagram__caption">Interface diagram, not a screenshot.</p></div>` |
| `.ex-table-wrap` `.ex-table` `.ex-table__num __flag __ok` | Data table. The wrapper is the only thing that scrolls sideways besides the feature scroller. | `<div class="ex-table-wrap"><table class="ex-table"><caption>...</caption>...</table></div>` |
| `.ex-logos` `.ex-logos__claim __row __item __img __name` | Logo strip. A claim above is mandatory. `__img--square --wide`. | `<div class="ex-logos"><p class="ex-logos__claim">Fennec runs across five venues and 20+ event companies.</p><ul class="ex-logos__row"><li class="ex-logos__item"><img class="ex-logos__img" src="assets/harbour.png" alt="Harbour Event Centre"></li></ul></div>` |
| `.ex-btn` `--primary --secondary --onink --sm --block` | Violet primary, hairline secondary, 8px radius, no gradients. | `<a class="ex-btn ex-btn--primary" href="...">Book a free audit</a>` |
| `.ex-link` `--quiet --mono` | Underlined link with offset. | `<a class="ex-link" href="work.html">the Fennec case study</a>` |
| `.ex-dl` `.ex-dl__k __v` `--onink` | Mono key over prose value. | `<dl class="ex-dl"><dt class="ex-dl__k">Hosting</dt><dd class="ex-dl__v">All data and models in Canada</dd></dl>` |
| `.ex-timeline` `.ex-timeline__step __num __body __title __when` | Numbered process timeline. Works inside `.ex-band`. | `<ol class="ex-timeline"><li class="ex-timeline__step"><span class="ex-timeline__num">1</span><div class="ex-timeline__body"><h3 class="ex-timeline__title">Free audit</h3><span class="ex-timeline__when">Week 0</span><p>...</p></div></li></ol>` |
| `.ex-founders` `.ex-founder` `.ex-founder__photo __name __role __bio __facts` | Two-up founder block, 4:5 photos. | `<div class="ex-founders"><article class="ex-founder"><img class="ex-founder__photo" src="assets/shiv.jpg" alt="Shiv Lohia"><div><h3 class="ex-founder__name">Shiv Lohia</h3><span class="ex-founder__role">Co-Founder</span><p class="ex-founder__bio">...</p></div></article></div>` |
| `.ex-videoband` `.ex-videoband__video` | The train footage, at most once on the whole site, with a FIG. label. Optional. | `<div class="ex-videoband"><video class="ex-videoband__video" src="assets/bg-video.mp4" muted loop playsinline autoplay></video></div>` |
| `.ex-reveal` | Optional fade-in on scroll. DEFAULTS TO VISIBLE. | `<div class="ex-reveal">` |

## 4b. The IA components (css/ia.css)

Four additions, all CSS only, all in `css/ia.css`, all using existing tokens.

| Class | Note |
| --- | --- |
| `.ia-crumbs` `.ia-crumbs__list __item __link` | Breadcrumb. Mono 12px uppercase, `/` separators in `--line-2`, sitting on a hairline. First thing inside `<main>` on every detail page. |
| `.ia-related` `.ia-related__grid __card __card--next __kicker __go __arrow` | Related-pages block. 2 to 3 `.ex-card` links, auto-fit grid. Last block inside `<main>`. |
| `.ia-subnav` `.ia-subnav__label __row __link __num` | Visible secondary link row. `work.html` and `solutions.html` only. |
| `.ia-submenu` | Grouped sub-lists inside `.ex-mobile-menu`. Plain nested `<ul>`, indented, quieter type. |
| `.ex-footer__grid.ia-sitemap` | Footer sitemap. Brand plus four columns: Work, Solutions, Company, Direct. Collapses 5 to 3 to 2 to 1 at 1080 / 820 / 560. |

### 4b.1 Breadcrumb

Two levels deep, never three. A real `<nav aria-label="Breadcrumb">` around an ordered list. The last item is
plain text, not a link, and carries `aria-current="page"`. Copy from `css/PARTIALS.html` block D.

```html
<nav class="ia-crumbs" aria-label="Breadcrumb">
  <div class="ex-container">
    <ol class="ia-crumbs__list">
      <li class="ia-crumbs__item"><a class="ia-crumbs__link" href="index.html">Home</a></li>
      <li class="ia-crumbs__item"><a class="ia-crumbs__link" href="work.html">Our work</a></li>
      <li class="ia-crumbs__item"><span aria-current="page">Uniserve</span></li>
    </ol>
  </div>
</nav>
```

Trails in use: `Home / Our work / <study>` and `Home / Solutions / <family>`. Index pages do not need one.

### 4b.2 Related pages

Two or three cards. Card one goes sideways to a related page, one card goes back up to the index, and the last
card is the forward step in the sequence: it carries `ia-related__card--next` and the kicker `Next case study`
or `Next family`, so a reader can walk the four studies or the five families in order without returning to the
index. The arrow is the two characters `-&gt;`, never a glyph, and is `aria-hidden`. Copy from block E.

```html
<section class="ex-section ex-section--tight ia-related" aria-labelledby="related-heading">
  <div class="ex-container">
    <p class="ex-eyebrow">Keep reading</p>
    <h2 class="ex-shead__title" id="related-heading">Where to go next</h2>
    <ul class="ia-related__grid">
      <li>
        <a class="ex-card ia-related__card" href="work.html">
          <p class="ia-related__kicker">Back up</p>
          <h3 class="ex-card__title">All case studies</h3>
          <p class="ex-card__body">Four engagements, each with its status and its arithmetic.</p>
          <span class="ia-related__go">Back to the index <span class="ia-related__arrow" aria-hidden="true">-&gt;</span></span>
        </a>
      </li>
      <li>
        <a class="ex-card ia-related__card ia-related__card--next" href="work-fennec.html">
          <p class="ia-related__kicker">Next case study</p>
          <h3 class="ex-card__title">Fennec, the flagship</h3>
          <p class="ex-card__body">An operating system for premium nightlife venues.</p>
          <span class="ia-related__go">Next <span class="ia-related__arrow" aria-hidden="true">-&gt;</span></span>
        </a>
      </li>
    </ul>
  </div>
</section>
```

Card order for the next affordance:
`work-uniserve` to `work-fennec` to `work-palapa-tours` to `work-scoped` to `work.html`, and
`solutions-events-floor` to `-ticketing-guests` to `-pos-payments` to `-inventory-staff` to
`-media-intelligence` to `solutions.html`.

### 4b.3 Secondary link row

Goes directly under the hero on `work.html` and `solutions.html`, nowhere else. Mark the current page with
`aria-current="page"` if the row is ever reused on a detail page. Copy from block F.

## 5. The four interactive components

All four render fully with JS disabled. `js/exodus.js` adds `ex-js` to `<html>`; the stylesheet hides inactive
panels only under that class. Do not put `hidden` on panels in the HTML. Full copy-paste skeletons live in
`css/PARTIALS.html`.

### 5.1 Feature scroller

Contract:

```
[data-scroller]            wrapper, needs a unique id
  [data-scroller-prev]     button
  [data-scroller-next]     button
  [data-scroller-rail]     the scroll-snap rail, becomes role=tablist
    [data-scroller-tab]    one <button> per feature, first has aria-selected="true"
  .ex-scroller__panels
    [data-scroller-panel]  one panel per tab, SAME ORDER, becomes role=tabpanel
```

JS adds `role`, `id`, `aria-controls`, `aria-labelledby`, `tabindex` and the roving tabindex. Click and
ArrowLeft / ArrowRight / ArrowUp / ArrowDown / Home / End all select. Prev and next scroll the rail and
disable at the ends. Images in panel 2 onwards use `data-src` instead of `src` and are loaded on first
selection. The rail is the only sideways-scrolling element besides `.ex-table-wrap`; its scrollbar is hidden
and `overscroll-behavior-x: contain` stops it trapping page scroll.

### 5.2 ROI calculator

Contract:

```
[data-roi]
  [data-roi-range="people"] + [data-roi-number="people"]   default 3,  1 to 50
  [data-roi-range="hours"]  + [data-roi-number="hours"]    default 6,  1 to 40
  [data-roi-range="rate"]   + [data-roi-number="rate"]     default 40, 15 to 200
  [data-roi-out="hours"]     aria-live="polite"
  [data-roi-out="dollars"]   aria-live="polite"
  [data-roi-readout]         one plain-English sentence
  [data-roi-math]            <pre>, the arithmetic in mono
```

Formula: `people x hours x 48 weeks = hours/year`, `hours/year x rate = dollars/year`. Values are parsed,
rounded to whole numbers, clamped to the ranges above, and fall back to the defaults on empty or nonsense
input, so no NaN is ever printed. The HTML must ship the default numbers (864 hours, $34,560) so the module
reads with JS off. Keep the honest caption: it is an estimate from the owner's own numbers, not a promise.

### 5.3 Disclosure

Contract:

```
<button data-disclose aria-expanded="false" aria-controls="ID"
        data-label-closed="+ 4 more reasons owners call" data-label-open="Show fewer reasons">
  <span data-disclose-icon>+</span><span data-disclose-label>+ 4 more reasons owners call</span>
</button>
<div class="ex-disclose__panel" id="ID" data-collapsed="false">
  <div class="ex-disclose__inner"> ... always in the DOM ... </div>
</div>
```

`aria-expanded` in the HTML sets the starting state. The animation is `grid-template-rows: 1fr` to `0fr` and
is disabled under `prefers-reduced-motion`. FAQ rows use the same button inside `.ex-faq > .ex-faq__item`.

### 5.4 Tabs

Contract:

```
[data-tabs]                wrapper, needs a unique id
  [data-tabs-list]         becomes role=tablist
    [data-tab]             numbered <button>, first has aria-selected="true"
  .ex-tabs__panels
    [data-tab-panel]       one per tab, SAME ORDER, becomes role=tabpanel
```

Identical keyboard and aria behaviour to the scroller. The list is a vertical rail at desktop and a
horizontal one under 820px. Never render a blank panel: every tab needs its panel.

### Mobile nav

`<button data-nav-toggle aria-expanded="false" aria-controls="ex-mobile-menu">` plus
`<div class="ex-mobile-menu" id="ex-mobile-menu">`. Escape closes and returns focus, a link click closes,
and resizing past 900px closes.

## 6. Banned patterns

Gradients of any kind. Orbs, blobs, glows. Serif display faces. Inter. Font weight above 700. Centered heroes
or centered section headers. Icon-tile 3-up card grids. Glassmorphism or backdrop-blur. Sharp 0px corners on
cards. More than one shadow style. Emoji as icons. A logo strip with no claim above it. Stock photos.
`!important`. Raw hex inside component rules. Page-level horizontal scroll.

## 7. Writing rules

**ABSOLUTE: never use an em dash or en dash.** No U+2013, U+2014, `&ndash;`, `&mdash;`, `&#8211;`, `&#8212;`.
Use a hyphen, a comma, a colon or a full stop. No ellipsis character either: write three dots.

Short declarative sentences. Concrete nouns and numbers. Lead with the number. One h1 per page, logical
heading order, real alt text, `width`/`height` on every image, `loading="lazy" decoding="async"` below the
fold. Body 17px minimum, AA contrast.

Banned words: unlock, leverage, transform, seamless, robust, cutting-edge, game-changing, supercharge,
"In today's". No three-adjective stacks.

Say what is in progress rather than implying it shipped. Statuses are LIVE (Fennec), IN BUILD (Uniserve,
Matchbox Global), SHIPPED (Palapa Tours), PROPOSED (Market Meats, Royal Feet). Every borrowed statistic
prints its real source. Every projection is labelled PROJECTION and shows its arithmetic. Never promise a
cash refund or a guaranteed dollar figure.
