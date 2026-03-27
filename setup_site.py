import os
import subprocess

BASE = "C:/Users/user/Desktop/personal_site"

SEMINAR_NAME = "Introduction_to_KnotTheory"

def create_structure():
    base_path = f"{BASE}/assets/seminar/{SEMINAR_NAME}"

    # Week 폴더 생성
    for i in range(1, 3):
        os.makedirs(f"{base_path}/Week{i}", exist_ok=True)

    # seminar 폴더
    os.makedirs(f"{BASE}/seminar", exist_ok=True)

def create_pages():
    # =========================
    # seminar.qmd
    # =========================
    seminar_main = f"""---
title: "Seminars"
---

## Available Seminars

- [Introduction to Knot Theory](seminar/knot.qmd)
"""

    # =========================
    # seminar 선택 페이지
    # =========================
    knot_page = f"""---
title: "Introduction to Knot Theory"
---

## Weekly Contents

- [Week 1](#week-1)
- [Week 2](#week-2)

---

## Week 1

### Slides
<iframe src="../assets/seminar/{SEMINAR_NAME}/Week1/slide.pdf" width="100%" height="600px"></iframe>

### Problems
[Download](../assets/seminar/{SEMINAR_NAME}/Week1/problem.pdf)

### Solutions
[Download](../assets/seminar/{SEMINAR_NAME}/Week1/solution.pdf)

---

## Week 2

### Slides
<iframe src="../assets/seminar/{SEMINAR_NAME}/Week2/slide.pdf" width="100%" height="600px"></iframe>

### Problems
[Download](../assets/seminar/{SEMINAR_NAME}/Week2/problem.pdf)

### Solutions
[Download](../assets/seminar/{SEMINAR_NAME}/Week2/solution.pdf)
"""

    files = {
        "seminar.qmd": seminar_main,
        "seminar/knot.qmd": knot_page,
    }

    for path, content in files.items():
        full = os.path.join(BASE, path)

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

def render():
    os.chdir(BASE)
    subprocess.run(["quarto", "render"])

def deploy():
    os.chdir(BASE)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "add seminar"], check=False)
    subprocess.run(["git", "push"], check=False)

    print("🚀 GitHub push 완료")

if __name__ == "__main__":
    create_structure()
    create_pages()
    update_quarto()
    render()
    deploy()
