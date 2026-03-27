import os
import re

BASE = "C:/Users/user/Desktop/personal_site"
SEMINAR_NAME = "Introduction_to_KnotTheory"

def get_weeks():
    path = f"{BASE}/assets/seminar/{SEMINAR_NAME}"

    if not os.path.exists(path):
        print("❌ Seminar folder not found")
        return []

    folders = os.listdir(path)

    def extract_num(name):
        match = re.search(r'\d+', name)
        return int(match.group()) if match else 0

    weeks = sorted(
        [f for f in folders if f.lower().startswith("week")],
        key=extract_num
    )

    return weeks

def create_pages():
    weeks = get_weeks()

    if not weeks:
        print("❌ No weeks found")
        return

    # =========================
    # seminar.qmd
    # =========================
    seminar_main = """---
title: "Seminar"
---

## 2026-1 SNU Student-Directed Seminar

- [Introduction to Knot Theory](seminar/knot.qmd)
"""

    # =========================
    # knot.qmd
    # =========================
    content = """---
title: "Introduction to Knot Theory"
---

**Organized by:** Junhyun An  
**with:** Yunseong Jo, Jongho Choi  

**Advisor:** Prof. Gyeseon Lee  
**Teaching Assistant:** Dongwoo Gang  

---

## Weekly Contents

"""

    # 목차
    for w in weeks:
        num = re.search(r'\d+', w).group()
        content += f"- [Week {num}](#week-{num})\n"

    content += "\n---\n"

    # 본문
    for w in weeks:
        num = re.search(r'\d+', w).group()
        base_path = f"../assets/seminar/{SEMINAR_NAME}/{w}"

        content += f"""
## Week {num}

### Slides
<iframe src="{base_path}/slide.pdf" width="100%" height="600px"></iframe>

### Problems
[Download]({base_path}/problem.pdf)

### Solutions
[Download]({base_path}/solution.pdf)

---
"""

    files = {
        "seminar.qmd": seminar_main,
        "seminar/knot.qmd": content,
    }

    for path, text in files.items():
        full = os.path.join(BASE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)

        with open(full, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Updated: {path}")

def update_quarto():
    path = os.path.join(BASE, "_quarto.yml")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "seminar.qmd" not in content:
        content = content.replace(
            "text: CV",
            "text: CV\n      - href: seminar.qmd\n        text: Seminar"
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print("Updated _quarto.yml")
    else:
        print("_quarto.yml already has Seminar")

if __name__ == "__main__":
    create_pages()
    update_quarto()

    print("\n✅ Setup complete!")
    print("➡️ Next steps:")
    print("1. quarto render")
    print("2. git add .")
    print("3. git commit -m 'update seminar'")
    print("4. git push")
