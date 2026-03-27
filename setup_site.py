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

        # 폴더만 + 정확히 Week숫자만 허용
        if os.path.isdir(full_path) and re.match(r'^Week\d+$', item):
            weeks.append(item)

    weeks = sorted(weeks, key=lambda x: int(re.search(r'\d+', x).group()))

    print("✅ Detected weeks:", weeks)

    return weeks
