import streamlit as st
from src.tutor import extract_text, chat

st.set_page_config(page_title="AI Tutor — AI Thực Chiến", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.header("📚 Tài liệu buổi học")
    st.caption("Tuỳ chọn — upload để AI có context bài học.")

    uploaded = st.file_uploader(
        "PDF / DOCX / TXT",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
    )

    if uploaded and uploaded.name != st.session_state.get("doc_name"):
        try:
            doc_text = extract_text(uploaded)
            st.session_state["doc_context"] = doc_text
            st.session_state["doc_name"] = uploaded.name
            st.session_state["chat_history"] = []
            if len(doc_text) >= 50_000:
                st.info("File lớn — chỉ đọc được 50,000 ký tự đầu.")
        except ValueError as e:
            st.error(str(e))

    if "doc_name" in st.session_state:
        st.success(f"✅ {st.session_state['doc_name']}")
        st.caption(f"{len(st.session_state.get('doc_context', ''))} ký tự đã đọc")
    else:
        st.info("Chưa có tài liệu — bạn vẫn có thể hỏi bất kỳ điều gì.")

# --- Main Chat ---
st.title("💬 AI Tutor")
st.caption("Hỏi về bất kỳ phần nào bạn chưa hiểu trong khoá AI thực chiến.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Bạn đang stuck ở đâu?"):
    st.session_state["chat_history"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                answer = chat(
                    st.session_state.get("doc_context", ""),
                    st.session_state["chat_history"][:-1],
                    question,
                )
            except Exception as e:
                answer = f"⚠️ Lỗi khi gọi AI: {e}"
        st.markdown(answer)

    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
