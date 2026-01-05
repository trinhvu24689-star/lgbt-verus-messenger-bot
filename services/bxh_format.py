def format_bxh(rows, title):
    if not rows:
        return f"🏆 BXH {title}\n\nChưa có dữ liệu."

    lines = [f"🏆 BXH {title}"]
    for i, r in enumerate(rows, 1):
        lines.append(f"{i}. {r.psid} — {r.cnt} tin")

    return "\n".join(lines)
