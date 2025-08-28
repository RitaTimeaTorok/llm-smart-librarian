import streamlit as st
from utils_openai_client import get_client
from rag.retriever import search
from tools.summary_tool import get_summary_by_title
from moderation import is_clean


def get_user_query():
    with st.form("query"):
        user_input = st.text_input("What are you in the mood for?")
        submit = st.form_submit_button("Recommend")
    return user_input, submit


def process_user_query(user_query):
    ok, msg = is_clean(user_query)
    if not ok:
        st.warning(msg)
        st.stop()
    st.write("🔎 Searching...")
    results = search(user_query, k=10)
    st.session_state["show_count"] = 1
    if not results:
        st.error("No results found. Try again.")
        st.stop()
    st.session_state["results"] = results


def remove_duplicate_results(results):
    unique_res = []
    titles = set()
    for r in results:
        t = r.get("title", "Unknown Title")
        if t not in titles:
            unique_res.append(r)
            titles.add(t)
    return unique_res


def display_results(unique_res, show_count):
    if unique_res:
        st.markdown("### 📚 Top Book Matches")
        for idx, result in enumerate(unique_res[:show_count]):
            title = result.get("title", "Unknown Title")
            author = result.get("author", "Unknown Author")
            with st.container():
                st.subheader(f"{title}")
                st.caption(f"Author: {author}")
                show = st.toggle("Show Summary", key=f"toggle_{idx}")
                if show:
                    summary = get_summary_by_title(title)
                    st.write(summary)
        if show_count < len(unique_res):
            if st.button("Show More Recommendations"):
                st.session_state["show_count"] = min(show_count + 1, len(unique_res))
                st.rerun()
        elif len(unique_res) > 1 and show_count >= len(unique_res):
            st.info("No more recommendations available.")


def main():
    st.set_page_config(page_title="Smart Librarian", page_icon="📚")
    st.title("📚 Smart Librarian")
    st.caption("Type what you're in the mood for and get multiple recommendations.")

    user_query, submitted = get_user_query()
    if submitted:
        process_user_query(user_query)

    results = st.session_state.get("results", [])
    show_count = st.session_state.get("show_count", 1)
    unique_res = remove_duplicate_results(results)
    display_results(unique_res, show_count)


if __name__ == "__main__":
    main()
