import json
import streamlit as st
from src.digest import generate_digest, correct_digest

st.set_page_config(page_title="Session Digest Bot", layout="wide")
st.title("📚 Session Digest Bot")
st.caption("Gom thông tin từ Email / Discord / Web thành một bản tóm tắt duy nhất.")

# --- Input Form ---
with st.form("digest_form"):
    date = st.text_input(
        "Buổi học / ngày *",
        placeholder="ví dụ: 2026-06-03 hoặc Day 05"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        email = st.text_area("📧 Email", height=200, placeholder="Paste nội dung email...")
    with col2:
        discord = st.text_area("💬 Discord", height=200, placeholder="Paste tin nhắn Discord...")
    with col3:
        web = st.text_area("🌐 Web / LMS", height=200, placeholder="Paste nội dung từ web trường...")
    submitted = st.form_submit_button("Generate Digest ✨", type="primary")

if submitted:
    if not date.strip():
        st.error("Vui lòng nhập ngày buổi học.")
    elif not any([email.strip(), discord.strip(), web.strip()]):
        st.error("Vui lòng paste nội dung từ ít nhất một kênh.")
    else:
        with st.spinner("Đang tạo digest..."):
            result = generate_digest(date, email, discord, web)
            st.session_state["digest"] = result
            st.session_state["digest_json_str"] = json.dumps(
                result, ensure_ascii=False, indent=2
            )

# --- Results ---
if "digest" in st.session_state:
    digest = st.session_state["digest"]

    st.divider()

    if digest.get("parse_error"):
        st.warning("⚠️ Không parse được — xem kết quả thô bên dưới.")
        st.text(digest.get("raw", ""))
    else:
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("✅ Key Concepts")
            concepts = digest.get("key_concepts", [])
            if concepts:
                for concept in concepts:
                    st.markdown(f"- {concept}")
            else:
                st.markdown("_Không tìm thấy key concepts._")

            st.subheader("📋 Action Items")
            items = digest.get("action_items", [])
            if items:
                for item in items:
                    task = item.get("task", "")
                    deadline = item.get("deadline", "")
                    label = f"**{task}** — `{deadline}`" if deadline else f"**{task}**"
                    st.markdown(f"- {label}")
            else:
                st.markdown("_Không có action items._")

        with col_right:
            flags = digest.get("flags", [])
            if flags:
                st.subheader("⚠️ Cần làm rõ")
                for flag in flags:
                    st.warning(flag)
            else:
                st.success("Không có thông tin mơ hồ.")

    # --- Correction ---
    st.divider()
    st.subheader("💬 Thêm thông tin còn thiếu")
    correction = st.text_area(
        "Nhập thông tin bổ sung...",
        height=80,
        placeholder="ví dụ: Deadline nộp bài là 23:59 ngày 5/6"
    )
    if st.button("Cập nhật Digest 🔄"):
        if correction.strip():
            with st.spinner("Đang cập nhật..."):
                updated = correct_digest(
                    st.session_state["digest_json_str"],
                    correction
                )
                if updated.get("parse_error"):
                    st.warning("⚠️ Không parse được kết quả cập nhật — giữ nguyên digest cũ.")
                    st.text(updated.get("raw", ""))
                else:
                    st.session_state["digest"] = updated
                    st.session_state["digest_json_str"] = json.dumps(
                        updated, ensure_ascii=False, indent=2
                    )
                    st.rerun()
        else:
            st.warning("Vui lòng nhập thông tin bổ sung.")
