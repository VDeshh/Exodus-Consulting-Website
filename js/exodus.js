/* ==========================================================================
   EXODUS DESIGN SYSTEM v4 - behaviour
   Vanilla JS. No libraries. No build step. Defensive: every initialiser
   no-ops when its markup is absent, and nothing here throws.

   Progressive enhancement contract:
   - All panels, all disclosure bodies and the calculator defaults are in the
     HTML and readable with JS off.
   - This file adds the class "ex-js" to <html> on init. The stylesheet only
     hides inactive panels when that class is present.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  // Added as early as possible so inactive panels never flash open.
  if (root && root.classList) root.classList.add("ex-js");

  var REDUCED = false;
  try {
    REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) { REDUCED = false; }

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }
  function qsa(sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  }
  function on(el, type, fn, opts) {
    if (el && el.addEventListener) el.addEventListener(type, fn, opts || false);
  }
  function safe(name, fn) {
    try { fn(); } catch (err) {
      if (window.console && console.warn) console.warn("[exodus] " + name + " failed", err);
    }
  }

  /* ------------------------------------------------------------------------
     1. MOBILE NAV
     Markup: [data-nav-toggle] button + #ex-mobile-menu
     ------------------------------------------------------------------------ */
  function initMobileNav() {
    var toggles = qsa("[data-nav-toggle]");
    if (!toggles.length) return;

    toggles.forEach(function (btn) {
      var id = btn.getAttribute("aria-controls");
      var panel = id ? document.getElementById(id) : null;
      if (!panel) return;

      var open = false;

      function set(state) {
        open = !!state;
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        panel.classList.toggle("is-open", open);
        if (open) {
          var first = qs("a, button", panel);
          if (first && first.focus) first.focus();
        }
      }

      set(false);

      on(btn, "click", function () { set(!open); });

      on(panel, "click", function (ev) {
        var t = ev.target;
        if (t && t.closest && t.closest("a")) set(false);
      });

      on(document, "keydown", function (ev) {
        if (ev.key === "Escape" && open) {
          set(false);
          if (btn.focus) btn.focus();
        }
      });

      on(window, "resize", function () {
        if (open && window.innerWidth > 900) set(false);
      });
    });
  }

  /* ------------------------------------------------------------------------
     Shared ARIA tab wiring used by the feature scroller and the tabs
     ------------------------------------------------------------------------ */
  function wireTablist(opts) {
    var list = opts.list;
    var tabs = opts.tabs;
    var panels = opts.panels;
    var onSelect = opts.onSelect;
    if (!list || !tabs.length || !panels.length) return null;

    var current = 0;

    tabs.forEach(function (tab, i) {
      if (!tab.id) tab.id = opts.idBase + "-tab-" + (i + 1);
      var panel = panels[i];
      if (panel) {
        if (!panel.id) panel.id = opts.idBase + "-panel-" + (i + 1);
        panel.setAttribute("role", "tabpanel");
        panel.setAttribute("aria-labelledby", tab.id);
        panel.setAttribute("tabindex", "0");
        tab.setAttribute("aria-controls", panel.id);
      }
      tab.setAttribute("role", "tab");
      if (tab.getAttribute("aria-selected") === "true") current = i;
    });
    list.setAttribute("role", "tablist");

    function select(index, focusTab) {
      if (index < 0) index = 0;
      if (index > tabs.length - 1) index = tabs.length - 1;
      current = index;
      tabs.forEach(function (tab, i) {
        var active = i === index;
        tab.setAttribute("aria-selected", active ? "true" : "false");
        tab.setAttribute("tabindex", active ? "0" : "-1");
        var panel = panels[i];
        if (panel) {
          if (active) panel.removeAttribute("hidden");
          else panel.setAttribute("hidden", "");
        }
      });
      if (focusTab && tabs[index] && tabs[index].focus) tabs[index].focus();
      if (typeof onSelect === "function") onSelect(index, tabs[index], panels[index]);
    }

    tabs.forEach(function (tab, i) {
      on(tab, "click", function () { select(i, false); });
      on(tab, "keydown", function (ev) {
        var key = ev.key;
        var next = -1;
        if (key === "ArrowRight" || key === "ArrowDown") next = current + 1;
        else if (key === "ArrowLeft" || key === "ArrowUp") next = current - 1;
        else if (key === "Home") next = 0;
        else if (key === "End") next = tabs.length - 1;
        else return;
        ev.preventDefault();
        if (next < 0) next = tabs.length - 1;
        if (next > tabs.length - 1) next = 0;
        select(next, true);
      });
    });

    select(current, false);
    return { select: select, count: tabs.length, index: function () { return current; } };
  }

  /* ------------------------------------------------------------------------
     2. FEATURE SCROLLER
     Markup: [data-scroller] with [data-scroller-rail], [data-scroller-tab],
     [data-scroller-panel], [data-scroller-prev], [data-scroller-next]
     ------------------------------------------------------------------------ */
  function initScrollers() {
    var scrollers = qsa("[data-scroller]");
    if (!scrollers.length) return;

    scrollers.forEach(function (scroller, sIndex) {
      var rail = qs("[data-scroller-rail]", scroller);
      var tabs = qsa("[data-scroller-tab]", scroller);
      var panels = qsa("[data-scroller-panel]", scroller);
      var prev = qs("[data-scroller-prev]", scroller);
      var next = qs("[data-scroller-next]", scroller);
      if (!rail || !tabs.length || !panels.length) return;

      var idBase = scroller.id || "ex-scroller-" + (sIndex + 1);

      function loadImages(panel) {
        if (!panel) return;
        qsa("img[data-src]", panel).forEach(function (img) {
          var src = img.getAttribute("data-src");
          if (src) {
            img.setAttribute("src", src);
            img.removeAttribute("data-src");
          }
        });
      }

      function scrollChipIntoView(tab) {
        if (!tab || !rail) return;
        // Horizontal only. Never move the page vertically.
        var railBox = rail.getBoundingClientRect();
        var tabBox = tab.getBoundingClientRect();
        var pad = 24;
        var delta = 0;
        if (tabBox.left < railBox.left + pad) delta = tabBox.left - railBox.left - pad;
        else if (tabBox.right > railBox.right - pad) delta = tabBox.right - railBox.right + pad;
        if (!delta) return;
        var target = rail.scrollLeft + delta;
        if (REDUCED || typeof rail.scrollTo !== "function") rail.scrollLeft = target;
        else rail.scrollTo({ left: target, behavior: "smooth" });
      }

      function syncButtons() {
        if (!prev && !next) return;
        var max = rail.scrollWidth - rail.clientWidth;
        var atStart = rail.scrollLeft <= 2;
        var atEnd = rail.scrollLeft >= max - 2;
        if (max <= 2) { atStart = true; atEnd = true; }
        if (prev) prev.disabled = atStart;
        if (next) next.disabled = atEnd;
      }

      var api = wireTablist({
        list: rail,
        tabs: tabs,
        panels: panels,
        idBase: idBase,
        onSelect: function (index, tab, panel) {
          loadImages(panel);
          scrollChipIntoView(tab);
        }
      });
      if (!api) return;

      function step(dir) {
        var amount = Math.max(160, Math.round(rail.clientWidth * 0.7));
        var target = rail.scrollLeft + dir * amount;
        if (REDUCED || typeof rail.scrollTo !== "function") rail.scrollLeft = target;
        else rail.scrollTo({ left: target, behavior: "smooth" });
      }

      on(prev, "click", function () { step(-1); });
      on(next, "click", function () { step(1); });
      on(rail, "scroll", syncButtons, { passive: true });
      on(window, "resize", syncButtons);
      syncButtons();
      // Second pass after fonts settle so widths are measured correctly.
      if (window.setTimeout) window.setTimeout(syncButtons, 400);
    });
  }

  /* ------------------------------------------------------------------------
     3. TABS (numbered capability switcher)
     Markup: [data-tabs] with [data-tabs-list], [data-tab], [data-tab-panel]
     ------------------------------------------------------------------------ */
  function initTabs() {
    var groups = qsa("[data-tabs]");
    if (!groups.length) return;
    groups.forEach(function (group, gIndex) {
      var list = qs("[data-tabs-list]", group);
      var tabs = qsa("[data-tab]", group);
      var panels = qsa("[data-tab-panel]", group);
      if (!list || !tabs.length || !panels.length) return;
      wireTablist({
        list: list,
        tabs: tabs,
        panels: panels,
        idBase: group.id || "ex-tabs-" + (gIndex + 1),
        onSelect: function (index, tab, panel) {
          if (!panel) return;
          qsa("img[data-src]", panel).forEach(function (img) {
            var src = img.getAttribute("data-src");
            if (src) { img.setAttribute("src", src); img.removeAttribute("data-src"); }
          });
        }
      });
    });
  }

  /* ------------------------------------------------------------------------
     4. DISCLOSURES
     Markup: button[data-disclose][aria-controls=ID][aria-expanded]
             + #ID.ex-disclose__panel > .ex-disclose__inner
     Optional: data-label-open / data-label-closed on the button's label span
     ------------------------------------------------------------------------ */
  function initDisclosures() {
    var buttons = qsa("[data-disclose]");
    if (!buttons.length) return;

    buttons.forEach(function (btn) {
      var id = btn.getAttribute("aria-controls");
      var panel = id ? document.getElementById(id) : null;
      if (!panel) return;

      var label = qs("[data-disclose-label]", btn);
      var icon = qs("[data-disclose-icon]", btn);
      var openText = btn.getAttribute("data-label-open") || "";
      var closedText = btn.getAttribute("data-label-closed") || "";
      var startOpen = btn.getAttribute("aria-expanded") === "true";

      function set(state) {
        btn.setAttribute("aria-expanded", state ? "true" : "false");
        panel.setAttribute("data-collapsed", state ? "false" : "true");
        if (icon) icon.textContent = state ? "-" : "+";
        if (label) {
          if (state && openText) label.textContent = openText;
          if (!state && closedText) label.textContent = closedText;
        }
      }

      set(startOpen);

      on(btn, "click", function () {
        set(btn.getAttribute("aria-expanded") !== "true");
      });
    });
  }

  /* ------------------------------------------------------------------------
     5. ROI CALCULATOR
     Markup: [data-roi] with paired [data-roi-range="people|hours|rate"] and
     [data-roi-number="..."], outputs [data-roi-out="hours|dollars"],
     [data-roi-readout], [data-roi-math]
     ------------------------------------------------------------------------ */
  function initRoi() {
    var calcs = qsa("[data-roi]");
    if (!calcs.length) return;

    var LIMITS = {
      people: { min: 1, max: 50, step: 1, def: 3 },
      hours: { min: 1, max: 40, step: 1, def: 6 },
      rate: { min: 15, max: 200, step: 1, def: 40 }
    };
    var WEEKS = 48;

    function clean(raw, lim) {
      var n = parseFloat(String(raw).replace(/[^0-9.\-]/g, ""));
      if (!isFinite(n)) n = lim.def;
      n = Math.round(n);
      if (n < lim.min) n = lim.min;
      if (n > lim.max) n = lim.max;
      return n;
    }

    function money(n) {
      return "$" + Math.round(n).toLocaleString("en-CA");
    }
    function count(n) {
      return Math.round(n).toLocaleString("en-CA");
    }

    calcs.forEach(function (calc) {
      var keys = ["people", "hours", "rate"];
      var fields = {};
      keys.forEach(function (k) {
        fields[k] = {
          range: qs('[data-roi-range="' + k + '"]', calc),
          number: qs('[data-roi-number="' + k + '"]', calc),
          lim: LIMITS[k]
        };
      });

      var outHours = qs('[data-roi-out="hours"]', calc);
      var outDollars = qs('[data-roi-out="dollars"]', calc);
      var readout = qs("[data-roi-readout]", calc);
      var math = qs("[data-roi-math]", calc);

      var hasInput = keys.some(function (k) {
        return fields[k].range || fields[k].number;
      });
      if (!hasInput) return;

      [outHours, outDollars, readout].forEach(function (el) {
        if (el && !el.getAttribute("aria-live")) el.setAttribute("aria-live", "polite");
      });

      function read(k) {
        var f = fields[k];
        var src = f.number || f.range;
        if (!src) return f.lim.def;
        return clean(src.value, f.lim);
      }

      function write(k, value) {
        var f = fields[k];
        if (f.range) {
          f.range.min = String(f.lim.min);
          f.range.max = String(f.lim.max);
          f.range.step = String(f.lim.step);
          f.range.value = String(value);
        }
        if (f.number) {
          f.number.min = String(f.lim.min);
          f.number.max = String(f.lim.max);
          f.number.step = String(f.lim.step);
          if (document.activeElement !== f.number) f.number.value = String(value);
        }
      }

      function recompute(source) {
        var people = read("people");
        var hours = read("hours");
        var rate = read("rate");

        // If the edit came from a range, mirror that range's raw value first.
        if (source && source.getAttribute("data-roi-range")) {
          var k = source.getAttribute("data-roi-range");
          if (k === "people") people = clean(source.value, LIMITS.people);
          if (k === "hours") hours = clean(source.value, LIMITS.hours);
          if (k === "rate") rate = clean(source.value, LIMITS.rate);
        }

        write("people", people);
        write("hours", hours);
        write("rate", rate);

        var weeklyHours = people * hours;
        var yearlyHours = weeklyHours * WEEKS;
        var yearlyDollars = yearlyHours * rate;

        if (outHours) outHours.textContent = count(yearlyHours);
        if (outDollars) outDollars.textContent = money(yearlyDollars);

        if (readout) {
          readout.textContent =
            count(people) + " " + (people === 1 ? "person" : "people") +
            " spending " + count(hours) + " " + (hours === 1 ? "hour" : "hours") +
            " a week on manual work costs about " + money(yearlyDollars) +
            " a year. That is " + count(yearlyHours) + " hours you could put back on the floor.";
        }

        if (math) {
          math.textContent =
            count(people) + " people x " + count(hours) + " hrs/week x " + WEEKS +
            " weeks = " + count(yearlyHours) + " hrs/year\n" +
            count(yearlyHours) + " hrs/year x " + money(rate) + "/hr = " +
            money(yearlyDollars) + "/year";
        }
      }

      keys.forEach(function (k) {
        var f = fields[k];
        ["input", "change"].forEach(function (evt) {
          on(f.range, evt, function () { recompute(f.range); });
          on(f.number, evt, function () { recompute(f.number); });
        });
        on(f.number, "blur", function () { recompute(null); });
      });

      recompute(null);
    });
  }

  /* ------------------------------------------------------------------------
     6. REVEAL - defaults to visible, so content is never stranded
     Markup: .ex-reveal (no attribute needed)
     ------------------------------------------------------------------------ */
  function initReveal() {
    var items = qsa(".ex-reveal");
    if (!items.length) return;

    function showAll() {
      items.forEach(function (el) { el.removeAttribute("data-reveal"); });
    }

    if (REDUCED || typeof window.IntersectionObserver !== "function") {
      showAll();
      return;
    }

    items.forEach(function (el) { el.setAttribute("data-reveal", "pending"); });

    var io = new window.IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.removeAttribute("data-reveal");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.02 });

    items.forEach(function (el) { io.observe(el); });

    // Failsafe: nothing stays invisible, whatever happens above.
    if (window.setTimeout) window.setTimeout(showAll, 2500);
  }

  /* ------------------------------------------------------------------------
     BOOT
     ------------------------------------------------------------------------ */
  function boot() {
    root.classList.add("ex-js");
    safe("mobile-nav", initMobileNav);
    safe("scroller", initScrollers);
    safe("tabs", initTabs);
    safe("disclosures", initDisclosures);
    safe("roi", initRoi);
    safe("reveal", initReveal);
  }

  if (document.readyState === "loading") {
    on(document, "DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
