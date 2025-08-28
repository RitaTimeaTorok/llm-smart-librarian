import streamlit as st
from utils_openai_client import get_client
from rag.retriever import search
from tools.summary_tool import get_summary_by_title
from moderation import is_clean


def main():
    st.set_page_config(page_title="Smart Librarian", page_icon="📚")
    st.title("📚 Smart Librarian")
    st.caption("Type what you're in the mood for and get multiple recommendations.")

    # Form to accept query
    with st.form("query"):
        user_query = st.text_input("What are you in the mood for?")
        submitted = st.form_submit_button("Recommend")

    # Triggered when "Recommend" is clicked
    if submitted:
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

        # Save results to session state for rerenders
        st.session_state["results"] = results

    # Load previous results if available
    results = st.session_state.get("results", [])
    show_count = st.session_state.get("show_count", 1)

    # Remove duplicate titles
    unique_results = []
    seen_titles = set()

    for r in results:
        t = r.get("title", "Unknown Title")
        if t not in seen_titles:
            unique_results.append(r)
            seen_titles.add(t)

    if unique_results:
        st.markdown("### 📚 Top Book Matches")
        for idx, result in enumerate(unique_results[:show_count]):
            title = result.get("title", "Unknown Title")
            author = result.get("author", "Unknown Author")

            with st.container():
                st.subheader(f"{title}")
                st.caption(f"Author: {author}")

                # Toggle for detailed summary
                show = st.toggle("Show Summary", key=f"toggle_{idx}")
                if show:
                    summary = get_summary_by_title(title)
                    st.write(summary)

        # Show more recommendations
        if show_count < len(unique_results):
            if st.button("Show More Recommendations"):
                st.session_state["show_count"] = min(show_count + 1, len(unique_results))
                st.rerun()

        elif len(unique_results) > 1 and show_count >= len(unique_results):
            st.info("No more recommendations available.")


if __name__ == "__main__":
    main()
