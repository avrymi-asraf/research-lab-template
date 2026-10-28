# Research Lab Template (`wiki-llm` + `JOURNAL` + `experiments` + Worktree Loop)

מאגר-על (Control-Plane Repository) לניהול מחקר וניסויים אוטונומיים או מונחי-אדם בלמידת מכונה, NLP ומערכות Agents על גבי מאגרי קוד חיצוניים (Target Repositories).

## הפילוסופיה של המאגר

במקום לזהם את מאגרי הקוד של המוצר/המודל בעשרות ענפי ניסוי כושלים או לאבד תובנות בין סשנים של סוכני AI, המאגר הזה מפריד בין **המוח והזיכרון המחקרי** (שחיים כאן ב-Git) לבין **סביבות הביצוע הקודיות** (שמוקמות כ-`git worktree` מבודדים תחת `.targets/worktrees/` ומתנקות בסיום).

המערכת בנויה מ-3 שכבות זיכרון המסונכרנות בלולאה סגורה:

1. **`wiki-llm/` (בסיס הידע המצטבר - Compiled Knowledge Base):**
   דפי Markdown מקושרים שהסוכן מקמפל ומתחזק. מחולקים לידע על המערכות החיצוניות (`systems/`), ממצאים מוכחים לפי נושא (`findings/`), סקירת ספרות (`literature/`), ומפת פערים פתוחים (`gap_map.md`). כל דף קוד כולל חתימת `Fingerprint: git:<sha>` לזיהוי התיישנות באפס טוקנים.
2. **`JOURNAL.md` (יומן המעבדה ואינדקס הניסויים):**
   נקודת הכניסה המרכזית לכל סשן. מציגה את שיא הביצועים הנוכחי (Current Frontier), תור הניצוצות הבאים לבדיקה (`Active Sparks Queue`), טבלת אינדקס של כל הניסויים שבוצעו, ורשימת חסימה של רעיונות שהופרכו (`Anti-Repeat Banlist`).
3. **`experiments/EXP-XXX/` (תיקיות הניסויים - Immutable Evidence):**
   כל ניסוי מקבל תיקייה קבועה משלו עם 5 קבצים:
   - `plan.md` — ההיפותזה, הקשר לפערים ב-Wiki, הגדרת ה-Scope המותר לעריכה, ופקודות ה-`Guard` וה-`Verify`.
   - `execution.md` — תיעוד הריצה, ה-Commit SHA בריפו החיצוני, ותקלות תשתית שנפתרו.
   - `results.json` — מדדים כמותיים (Baseline מול Candidate) וסטטוס בדיקות ה-Guard.
   - `postmortem.md` — ניתוח שגיאות, סיווג המסקנה (`HYPOTHESIS_SUPPORTED` / `HYPOTHESIS_REFUTED` / `INFRA_INCONCLUSIVE`), ושדה **`Spark`** שמייצר את ההיפותזה הבאה בזמן שהקונטקסט חם.
   - `patch.diff` — ה-Git Diff המדויק שבוצע בריפו החיצוני, כך שניתן לשחזר כל ניסוי גם לאחר מחיקת ה-Worktree.

## מבנה התיקיות

```text
research-lab-template/
├── AGENTS.md                        # חוקי המעבדה ופרוטוקול 4 השלבים עבור סוכני AI
├── CLAUDE.md                        # הפניה ל-AGENTS.md (תאימות ל-Claude Code)
├── GEMINI.md                        # הפניה ל-AGENTS.md (תאימות ל-Gemini CLI)
├── JOURNAL.md                       # יומן המעבדה: אינדקס ניסויים, שיא נוכחי, Sparks ו-Banlist
├── repos.yaml                       # מניפסט מאגרי הקוד החיצוניים שהמעבדה מנהלת
├── scripts/
│   └── lab.py                       # כלי CLI (Python stdlib בלבד) לניהול המחזור כולו
├── skills/
│   └── experiment-lab-loop/
│       └── SKILL.md                 # הגדרת הסקיל לסוכן (Evaluate -> Plan -> Execute -> Distill)
├── wiki-llm/
│   ├── index.md                     # קטלוג נושאי של כל דפי ה-Wiki (שורה לדף)
│   ├── purpose.md                   # מטרות המחקר, מדדי יעד ותזת העבודה
│   ├── gap_map.md                   # פערים פתוחים וצווארי בקבוק במערכת (G1, G2...)
│   ├── log.md                       # יומן פעולות כרונולוגי (Append-only)
│   ├── query_pack.md                # תקציר אוטומטי דחוס לקריאה לפני תכנון ניסוי חדש
│   ├── systems/                     # תיעוד ארכיטקטורת הריפוז החיצוניים + Fingerprints
│   ├── findings/                    # ידע מזוקק לפי נושאים (Prompts, RAG, Routing, Training)
│   └── literature/                  # סיכומי מאמרים וטכניקות רלוונטיות
├── experiments/
│   ├── _TEMPLATE/                   # תבנית האב שממנה נוצרת כל תיקיית ניסוי חדשה
│   └── EXP-000-baseline-example/    # דוגמה מלאה לתיקיית ניסוי מתועדת
└── .targets/                        # [ב-.gitignore] שיבוטי הקוד החיצוניים וה-Worktrees
    ├── repos/
    └── worktrees/
```

## התחלה מהירה (Quick Start)

1. **אתחול המעבדה:**
   ```bash
   python3 scripts/lab.py init
   ```
2. **רישום וסנכרון מאגרי הקוד החיצוניים:**
   ערכו את `repos.yaml` והריצו:
   ```bash
   python3 scripts/lab.py sync-repos
   ```
3. **בדיקת התיישנות ה-Wiki מול הקוד (`0-Token Drift Check`) ובניית חבילת הקשר לתכנון:**
   ```bash
   python3 scripts/lab.py check-drift
   python3 scripts/lab.py context-pack
   ```
4. **פתיחת ניסוי חדש (יוצר תיקייה ב-`experiments/` + פותח `git worktree` נקי בריפו המטרה):**
   ```bash
   python3 scripts/lab.py new-exp --id EXP-001 --repo example-agent-repo --title "tool-schema-pruning"
   ```
5. **הרצת הערכה, בדיקת `Guard` (שמירה על טסטים קיימים), בדיקת `Scope` וייצוא `patch.diff`:**
   ```bash
   python3 scripts/lab.py evaluate --exp EXP-001
   ```
6. **רישום תוצאות ליומן ול-Wiki וניקוי ה-Worktree בסיום:**
   ```bash
   python3 scripts/lab.py record-verdict --exp EXP-001 --verdict HYPOTHESIS_SUPPORTED --metric-delta "+6.2% Pass@1" --summary "Pruning unused MCP schemas reduced tool selection errors"
   python3 scripts/lab.py cleanup-worktree --exp EXP-001
   ```
