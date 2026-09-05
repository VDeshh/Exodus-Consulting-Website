#!/usr/bin/env python3
"""
Blocks client-internal material from reaching the public Exodus repo or website.

Two kinds of check:
  1. PATH rules  - filenames that are client deliverables or internal drafts.
  2. CONTENT rules - phrases inside public .html pages that expose a client's
     internal operations (their stack, their volumes, their QA, their vendors).

Run manually:      python tools/check-client-internals.py
Check staged only: python tools/check-client-internals.py --staged
Check a build dir: python tools/check-client-internals.py --dir dist
Installed as a pre-commit hook by tools/install-hooks.sh, so a commit that
contains any of this fails before it is ever pushed.

Exit 0 = clean, exit 1 = blocked.
"""
import os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- 1. filenames that must never be committed -------------------------------
PATH_PATTERNS = [
    (r'knowledge[-_ ]?base',        'client knowledge base'),
    (r'(^|/)content/documents/',    'client deliverable PDF'),
    (r'test[-_ ]?report',           'client test/QA report'),
    (r'week\d+[-_ ]?report',        'client progress report'),
    (r'phase\d+.*report',           'client phase report'),
    (r'chatbot.*(report|qa|test)',  'client chatbot QA/test material'),
    (r'oc-email',                   'internal email draft'),
    (r'playbook',                   'internal/client playbook'),
    (r'process-briefer',            'internal briefer'),
    (r'signature',                  'internal email signature'),
    (r'assets/product/raw/',        'raw app captures (contain guest PII)'),
    # Internal reference docs must never sit in a served directory. css/ and js/
    # are published, so a handbook or partials file there is world readable.
    (r'^(css|js)/.*\.(md|markdown)$',        'internal doc inside a served directory'),
    (r'^(css|js)/PARTIALS\.html$',            'internal partials file inside a served directory'),
]

# --- 2. phrases that must never appear in a PUBLIC page ----------------------
# Each entry: (regex, why). Keep these specific enough to avoid false positives.
CONTENT_PATTERNS = [
    (r'\bConnectWise\b',                       "client's internal support stack"),
    (r'\bHalo\b(?!\s*(?:effect|infinite))',    "client's internal support stack"),
    (r'\bRailtown\b|\bRailTracks\b|\bRailEngine\b',
                                               "client's platform vendor"),
    (r'\bConductor\b',                         "client's platform vendor component"),
    (r'\d{2,4}\s+(?:support\s+)?tickets\s+a\s+month',
                                               "client's internal ticket volume"),
    (r'\btickets? per month\b',                "client's internal ticket volume"),
    (r'\bopportunity heatmap\b|\bheatmap across\b',
                                               "client's internal assessment"),
    (r'\b\d+\s+to\s+\d+\s+use cases\b',        "client's internal use-case shortlist"),
    (r'\bUniserve Copilot\b',                  "client's internal tool"),
    (r'\bticket summariser\b|\bticket summarizer\b',
                                               "client's internal tool"),
    (r'\bauto-response drafts?\b',             "client's internal tool"),
    (r'\bescalation rules?\b',                 "client's internal chatbot config"),
    (r'\bsystem prompt\b',                     "client's internal chatbot config"),
    (r'\bFAQ draft\b',                         "client's internal chatbot content"),
    (r'\bGautam\b',                            "client contact by name"),
    (r'\b(?:chatbot|assistant)\s+(?:QA|testing|test plan|eval(?:uation)?)\b',
                                               "client chatbot QA/testing"),
]

PUBLIC_EXT = {'.html', '.md'}
SKIP_DIRS  = {'.git', 'node_modules', 'dist', '_legacy-v1', 'assets', 'tools'}
# Files that are internal by nature and already excluded from the site build.
SKIP_FILES = {'oc-email-full.html'}


def staged_files():
    out = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
                         cwd=REPO, capture_output=True, text=True).stdout
    return [f.strip() for f in out.splitlines() if f.strip()]


def all_files(base):
    found = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), base).replace(os.sep, '/')
            found.append(rel)
    return found


def main():
    staged = '--staged' in sys.argv
    # --dir scans an arbitrary tree. The deploy script points it at dist/, so the
    # gate inspects exactly what ships rather than the whole working folder, which
    # also holds internal drafts that are gitignored and never copied into a build.
    base = REPO
    if '--dir' in sys.argv:
        base = os.path.abspath(sys.argv[sys.argv.index('--dir') + 1])
        if not os.path.isdir(base):
            print(f'check-client-internals: no such directory: {base}')
            return 1
    files = staged_files() if staged else all_files(base)
    problems = []

    for rel in files:
        low = rel.lower()
        for pat, why in PATH_PATTERNS:
            if re.search(pat, low):
                problems.append(('PATH', rel, '', why, rel))
                break

    for rel in files:
        if os.path.basename(rel) in SKIP_FILES:
            continue
        if os.path.splitext(rel)[1].lower() not in PUBLIC_EXT:
            continue
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            continue
        try:
            text = open(p, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat, why in CONTENT_PATTERNS:
                m = re.search(pat, line, re.I)
                if m:
                    snippet = line.strip()
                    if len(snippet) > 120:
                        s = max(0, m.start() - 50)
                        snippet = '...' + line[s:m.end() + 50].strip() + '...'
                    problems.append(('CONTENT', rel, str(i), why, snippet))

    if not problems:
        scope = ('staged changes' if staged else
                 os.path.relpath(base, REPO).replace(os.sep, '/') + '/' if base != REPO else
                 'working tree')
        print(f'client-internals check: clean ({len(files)} files scanned in the {scope})')
        return 0

    print('')
    print('=' * 78)
    print(' BLOCKED: client-internal material detected')
    print('=' * 78)
    kind_order = {'PATH': 0, 'CONTENT': 1}
    for kind, rel, line, why, snippet in sorted(problems, key=lambda x: (kind_order[x[0]], x[1])):
        loc = f'{rel}:{line}' if line else rel
        print(f'\n  [{kind}] {loc}')
        print(f'    why : {why}')
        print(f'    text: {snippet}')
    print('')
    print('-' * 78)
    print(' This repo is a PUBLIC website. A client\'s internal operations, their')
    print(' vendors, their ticket volumes and any QA of their systems must not be')
    print(' published. Describe what Exodus built and what it produced instead.')
    print('')
    print(' If a match is a genuine false positive, add it to SKIP_FILES or narrow')
    print(' the pattern in tools/check-client-internals.py, and say why in the commit.')
    print(' To bypass once (not recommended): git commit --no-verify')
    print('-' * 78)
    return 1


if __name__ == '__main__':
    sys.exit(main())
