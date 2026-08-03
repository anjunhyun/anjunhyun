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

    # _quarto.yml: Seminar 탭 포함, gh-pages 방식이므로 output-dir 없음
    quarto_config = """project:
  type: website
  resources:
    - assets/

website:
  title: "안준현(An JunHyun) site"

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
title: "안준현/Junhyun An"
image: assets/profile.jpg
about:
  template: trestles
  links:
    - icon: github
      text: Github
      href: https://github.com/anjunhyun
    - icon: envelope
      text: Email
      href: mailto:anjunhyun@snu.ac.kr
---

## Biography

I am a undergraduate student in the **Department of Statistics at Seoul National University (SNU)**. 
My research interests lie at the intersection of **Graph Theory**, **Knot Theory**, and **Topological Data Analysis (TDA)**.

## Education

- **Seoul National University** | Seoul, South Korea
  <br> B.S. in Statistics & Mathematics (Current)

## Interests

- Knot Theory
- Graph Theory
- Algebraic Topology & Persistent Homology
- Statistical Inference for TDA
"""

    research_content = """---
title: "Research & Publications"
---

## Working Papers

- **On the Computational Complexity and Approximation of the General Routing Problem in Euclidean Graphs**
  <br> [[PDF]](assets/GRP_in_Euclidean_Graph.pdf)

- **Subsampling Confidence Bound for Persistent Diagram via Time-delay Embedding**
  <br> [[arXiv]](https://arxiv.org/abs/2512.06324)
  [[PDF]](https://arxiv.org/pdf/2512.06324)
"""

    cv_content = """---
title: "Curriculum Vitae"
---

## Education

**Seoul National University** | Seoul, South Korea
<br> B.S. in Statistics & Mathematics (Current)

## Research Interests

- Knot Theory
- Graph Theory
- Topological Data Analysis (TDA)

<br>

<iframe src="assets/CV.pdf" width="100%" height="800px" style="border: none;">
    <p>Your browser does not support PDFs. 
    <a href="assets/CV.pdf">Download the PDF</a>.</p>
</iframe>
"""

    css_content = """body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* ── PDF 토글 버튼 ── */
.pdf-toggle-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #2c7be5;
    background: transparent;
    border: 1.5px solid #2c7be5;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    margin-bottom: 6px;
}
.pdf-toggle-btn:hover {
    background: #2c7be5;
    color: #fff;
}
.pdf-toggle-btn .arrow {
    display: inline-block;
    transition: transform 0.2s;
}
.pdf-toggle-btn.open .arrow {
    transform: rotate(90deg);
}

/* ── PDF 미리보기 박스 ── */
.pdf-preview-box {
    display: none;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.pdf-preview-box.open {
    display: block;
}
.pdf-preview-box iframe {
    width: 100%;
    height: 600px;
    border: none;
    display: block;
}
"""

    # _quarto.yml, styles.css, research.qmd, cv.qmd: 항상 원본으로 덮어씀
    always_overwrite = {
        "_quarto.yml": quarto_config,
        "styles.css": css_content,
        "research.qmd": research_content,
        "cv.qmd": cv_content,
        "index.qmd": index_content,
    }

    # index.qmd: 이미 있으면 건너뜀 (프로필 사진 등 직접 편집 가능성)
    create_if_missing = {
	None,
    }

    for name, content in always_overwrite.items():
        path = os.path.join(BASE, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Updated: {name}")

    try:
        for name, content in create_if_missing.items():
            path = os.path.join(BASE, name)
            if os.path.exists(path):
                print(f"⏭️  Skipped (already exists): {name}")
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Created: {name}")
    except:
        print("All files are modified")


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

    toggle_script = """
<script>
function togglePdf(btn, boxId) {
    const box = document.getElementById(boxId);
    const isOpen = box.classList.contains('open');
    box.classList.toggle('open', !isOpen);
    btn.classList.toggle('open', !isOpen);
    if (!isOpen) {
        const iframe = box.querySelector('iframe');
        if (iframe && iframe.dataset.src) {
            iframe.src = iframe.dataset.src;
            delete iframe.dataset.src;
        }
    }
}
</script>
"""

    content = f"""---
title: "Introduction to Knot Theory"
---

{toggle_script}

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
        content += f"- Week {num}\n"

    content += "\n---\n"

    # 본문: 각 week
    for w in weeks:
        num = re.search(r'\d+', w).group()
        base_path = f"../assets/seminar/{SEMINAR_NAME}/{w}"

        slide_box_id = f"slide-box-{num}"
        slide_btn_id = f"slide-btn-{num}"

        problem_file = os.path.join(
            BASE, "assets", "seminar", SEMINAR_NAME, w, "problem.pdf"
        )

        solution_file = os.path.join(
            BASE, "assets", "seminar", SEMINAR_NAME, w, "solution.pdf"
        )

        content += f"""
<details>
<summary><strong>Week {num}</strong></summary>

<h3>Slides</h3>

<button class="pdf-toggle-btn" id="{slide_btn_id}"
        onclick="togglePdf(this, '{slide_box_id}')">
  <span class="arrow">▶</span> Slide Preview
</button>

<div class="pdf-preview-box" id="{slide_box_id}">
  <iframe data-src="{base_path}/slide.pdf"></iframe>
</div>
"""

        if os.path.exists(problem_file):
            content += f"""
<h3>Problems</h3>

<a href="{base_path}/problem.pdf" target="_blank">
📄 Problem Download
</a>
"""

        if os.path.exists(solution_file):
            content += f"""
<h3>Solutions</h3>

<a href="{base_path}/solution.pdf" target="_blank">
📄 Solution Download
</a>
"""

        content += """
</details>

---
"""

    os.makedirs(os.path.join(BASE, "seminar"), exist_ok=True)

    with open(os.path.join(BASE, "seminar.qmd"), "w", encoding="utf-8") as f:
        f.write(seminar_main)

    with open(os.path.join(BASE, "seminar/knot.qmd"), "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Seminar pages created")


# =========================
# 필수 폴더 생성
# =========================
def create_structure():
    os.makedirs(f"{BASE}/assets/seminar/{SEMINAR_NAME}", exist_ok=True)
    os.makedirs(f"{BASE}/seminar", exist_ok=True)
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
    print("➡️  Run:")
    print('''git add .\n
git commit -m "restore research and cv"\n
git push origin main''')
    print('quarto publish gh-pages') # 빌드 + 배포 한번에
