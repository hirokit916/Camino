# -*- coding: utf-8 -*-
"""Rebuild the subject-guide pages (IB / MYP / IGCSE / A Level / Lower Secondary / AP) in the correct order.

Usage (from the repository root):
    python3 _build/run.py            # rebuild in place
    python3 _build/run.py --check    # rebuild into a temporary copy and report which pages would change

Every step is idempotent: running this on an up-to-date site changes nothing.
The HTML in the repository is the source of truth; these steps only rewrite their own parts of each page.
See _build/README.md for what each step does and how to add or change content.
"""
import os, shutil, subprocess, sys, tempfile, filecmp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# (script, what it does) — ORDER MATTERS
STEPS = [
    ('apsci/ap_content.py',   'AP science/math: remove key-points section, unit + exam-weighting tables'),
    ('apsci/subj_content.py', 'IB/MYP/IGCSE/A Level/Lower Secondary: remove key-points section, 学ぶ内容 layout'),
    ('univreq/subj_majors.py', '「大学の学部で求められる度合い」charts (IB, A Level, AP sciences/maths)'),
    ('apjp/build_apjp.py',    'AP Japanese page (units, exam, project, rubric database, tips, edited wording)'),
    ('econ/build_econ.py',    'AP Microeconomics and Macroeconomics pages'),
    ('psych/build_psych.py',  'AP Psychology page'),
    ('math/build_math.py',    'AP Calculus AB / BC and Precalculus pages'),
]


def run_all(root):
    for script, what in STEPS:
        print('▶ %-24s %s' % (script, what))
        r = subprocess.run([sys.executable, os.path.join(HERE, script), root], cwd=os.path.dirname(os.path.join(HERE, script)),
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-2000:], r.stderr[-4000:])
            sys.exit('✖ step failed: %s' % script)


def html_files(root):
    for d, _, fs in os.walk(os.path.join(root, 'subjects')):
        for f in fs:
            if f.endswith('.html'):
                yield os.path.relpath(os.path.join(d, f), root)


if __name__ == '__main__':
    if '--check' in sys.argv:
        tmp = tempfile.mkdtemp(prefix='camino-check-')
        os.rmdir(tmp)
        shutil.copytree(REPO, tmp, ignore=shutil.ignore_patterns('.git', '_build', '*.webp', '*.png', '*.jpg', '*.mp4', '*.pdf'))
        run_all(tmp)
        changed = [p for p in html_files(REPO) if not filecmp.cmp(os.path.join(REPO, p), os.path.join(tmp, p), shallow=False)]
        shutil.rmtree(tmp)
        print('\n%d page(s) would change' % len(changed))
        for p in changed:
            print('  ', p)
        sys.exit(1 if changed else 0)
    run_all(REPO)
    print('\n✔ done. Review with git diff, then commit.')
