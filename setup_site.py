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
        print(f"✅ Created: {name}")


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

    # ── 토글 JS (페이지 상단에 한 번만 삽입) ──
    toggle_script = """
<script>
function togglePdf(btn, boxId) {
    const box = document.getElementById(boxId);
    const isOpen = box.classList.contains('open');
    box.classList.toggle('open', !isOpen);
    btn.classList.toggle('open', !isOpen);
    // lazy-load: src를 data-src에서 가져옴
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
        content += f"- [Week {num}](#week-{num})\n"

    content += "\n---\n"

    # ── 본문: 각 week ──
    # seminar/knot.qmd 기준으로 assets 경로는 ../assets/...
    for w in weeks:
        num = re.search(r'\d+', w).group()
        base_path = f"../assets/seminar/{SEMINAR_NAME}/{w}"

        slide_box_id = f"slide-box-{num}"
        slide_btn_id = f"slide-btn-{num}"

        # ✅ 수정: f-string 안에서 {{#week-{num}}} → {#week-N} (올바른 Quarto 앵커 문법)
        #         기존 코드의 {{{{#week-{num}}}}} 는 {{#week-N}} 이 되어 앵커가 깨졌음
        #         .replace("{num}", num) 혼용도 제거하고 f-string만 사용
        content += f"""
## Week {num} {{#week-{num}}}

### Slides

<button class="pdf-toggle-btn" id="{slide_btn_id}"
        onclick="togglePdf(this, '{slide_box_id}')">
  <span class="arrow">▶</span> Slide 미리보기
</button>
<div class="pdf-preview-box" id="{slide_box_id}">
  <iframe data-src="{base_path}/slide.pdf"></iframe>
</div>

### Problems

<a href="{base_path}/problem.pdf" target="_blank">📄 Problem 다운로드</a>

### Solutions

<a href="{base_path}/solution.pdf" target="_blank">📄 Solution 다운로드</a>

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

    # docs/.nojekyll 과 루트 .nojekyll 둘 다 생성 (gh-pages 브랜치 배포 대비)
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
    print("➡️  Run:")
    print("quarto render")
    print("git add .")
    print("git commit -m 'update seminar'")
    print("git push")