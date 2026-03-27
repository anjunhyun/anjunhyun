import os
import subprocess

BASE = "C:/Users/user/Desktop/personal_site"

def create_seminar_structure():
    # 폴더
    os.makedirs(f"{BASE}/seminar", exist_ok=True)
    os.makedirs(f"{BASE}/seminar_knot", exist_ok=True)
    os.makedirs(f"{BASE}/assets/slides/knot", exist_ok=True)
    os.makedirs(f"{BASE}/assets/problems/knot", exist_ok=True)

    # =========================
    # seminar.qmd (허브)
    # =========================
    seminar_main = """---
title: "Seminars"
---

## Available Seminars

### Knot Theory

- [Introduction to Knot Theory](seminar/knot-theory.qmd)
"""

    # =========================
    # 세미나 선택 페이지
    # =========================
    knot_page = """---
title: "Introduction to Knot Theory"
---

## Weekly Contents

- [Week 1](../seminar_knot/week1.qmd)
- [Week 2](../seminar_knot/week2.qmd)
"""

    # =========================
    # Week1
    # =========================
    week1 = """---
title: "Week 1"
---

## Slides
<iframe src="../assets/slides/knot/week1.pdf" width="100%" height="600px"></iframe>

## Problems
[Download](../assets/problems/knot/week1.pdf)

## Solutions
[Download](../assets/problems/knot/week1_solution.pdf)
"""

    # =========================
    # Week2
    # =========================
    week2 = """---
title: "Week 2"
---

## Slides
<iframe src="../assets/slides/knot/week2.pdf" width="100%" height="600px"></iframe>

## Problems
[Download](../assets/problems/knot/week2.pdf)

## Solutions
[Download](../assets/problems/knot/week2_solution.pdf)
"""

    files = {
        "seminar.qmd": seminar_main,
        "seminar/knot-theory.qmd": knot_page,
        "seminar_knot/week1.qmd": week1,
        "seminar_knot/week2.qmd": week2,
    }

    for path, content in files.items():
        full = os.path.join(BASE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)

        if not os.path.exists(full):
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created: {path}")
        else:
            print(f"Skipped: {path}")

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
        print("_quarto.yml already updated")

def deploy_to_github():
    os.chdir(BASE)

    subprocess.run(["git", "init"], check=False)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "update seminar"], check=False)
    subprocess.run(["git", "branch", "-M", "main"], check=False)

    # 👉 여기 반드시 수정
    repo_url = "https://github.com/anjunhyun/YOUR_REPO.git"

    subprocess.run(["git", "remote", "add", "origin", repo_url], check=False)
    subprocess.run(["git", "push", "-u", "origin", "main"], check=False)

    print("🚀 Pushed to GitHub")

def render():
    os.chdir(BASE)
    subprocess.run(["quarto", "render"])

if __name__ == "__main__":
    create_seminar_structure()
    update_quarto()
    render()
    deploy_to_github()
