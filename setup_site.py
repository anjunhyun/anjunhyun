import os
import re

BASE = "C:/Users/user/Desktop/personal_site"
SEMINAR_NAME = "Introduction_to_KnotTheory"

# =========================
# Week 자동 탐색
# =========================
def get_weeks():
    path = f"{BASE}/assets/seminar/{SEMINAR_NAME}"

    if not os.path.exists(path):
        print("❌ Seminar folder not found")
        return []

    items = os.listdir(path)
    print("📁 Raw items:", items)

    weeks = []
    for item in items:
        full_path = os.path.join(path, item)

        if os.path.isdir(full_path) and re.match(r'^Week\d+$', item):
            weeks.append(item)

    weeks = sorted(weeks, key=lambda x: int(re.search(r'\d+', x).group()))
    print("✅ Detected weeks:", weeks)

    return weeks


# =========================
# 기본 페이지 생성
# =========================
def create_base_files():

    quarto_config = """project:
  type: website
  output-dir: docs
  resources:
    - assets/

website:
  title: "안준현(An JunHyun) site"
  site-url: "https://anjunhyun.github.io/anjunhyun"

  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: research.qmd
        text: Research
      - href: seminar.qmd
        text: Seminar
      - href: cv.qmd
        text: CV
    right:
      - icon: github
        href: https://github.com/anjunhyun
      - icon: envelope
        href: mailto:anjunhyun@snu.ac.kr

format:
  html:
    theme: cosmo
    css: styles.css
    toc: true
"""

    index_content = """---
title: "안준현 / Junhyun An"
image: assets/profile.jpg
about:
  template: trestles
---

## Biography

I am a undergraduate student in Statistics at SNU.

## Research Interests

- Knot Theory
- Graph Theory
- Topological Data Analysis
"""

    research_content = """---
title: "Research"
---

## Working Papers

- On the Computational Complexity of Euclidean Graph Problems
"""

    cv_content = """---
title: "CV"
---

<iframe src="assets/CV.pdf" width="100%" height="800px"></iframe>
"""

    css_content = """body {
    font-family: -apple-system, BlinkMacSystemFont;
}
"""

    files = {
        "_quarto.yml": quarto_config,
        "index.qmd": index_content,
        "research.qmd": research_content,
        "cv.qmd": cv_content,
        "styles.css": css_content
    }

    for name, content in files.items():
        path = os.path.join(BASE, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created: {name}")


# =========================
# Seminar 페이지 생성
# =========================
def create_seminar_pages():

    weeks = get_weeks()

    seminar_main = """---
title: "Seminar"
---

## 2026-1 SNU Student-Directed Seminar

- [Introduction to Knot Theory](seminar/knot.qmd)
"""

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
## Week {num} {{#week-{num}}}

### Slides
<iframe src="{base_path}/slide.pdf" width="100%" height="600px"></iframe>

### Problems
[Download]({base_path}/problem.pdf)

### Solutions
[Download]({base_path}/solution.pdf)

---
"""

    os.makedirs(os.path.join(BASE, "seminar"), exist_ok=True)

    with open(os.path.join(BASE, "seminar.qmd"), "w", encoding="utf-8") as f:
        f.write(seminar_main)

    with open(os.path.join(BASE, "seminar/knot.qmd"), "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Seminar pages created")


# =========================
# 필수 폴더 + nojekyll
# =========================
def create_structure():
    os.makedirs(f"{BASE}/assets/seminar/{SEMINAR_NAME}", exist_ok=True)
    os.makedirs(f"{BASE}/docs", exist_ok=True)

    # 🔥 핵심
    with open(os.path.join(BASE, "docs/.nojekyll"), "w") as f:
        pass

    print("✅ Structure ready")


# =========================
# 실행
# =========================
if __name__ == "__main__":
    print("🚀 Setting up site...")

    create_structure()
    create_base_files()
    create_seminar_pages()

    print("\n✅ DONE")
    print("➡️ Run:")
    print("   quarto render")
    print("   git add .")
    print("   git commit -m 'init site'")
    print("   git push")