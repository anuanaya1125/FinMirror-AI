"""AI insight panel + free-text Q&A chat panel (stretch goal)."""

from __future__ import annotations

import streamlit as st


def render_insight_panel(
    insight_text: str,
    used_fallback: bool,
    language_label: str,
) -> None:
    st.subheader(f"AI Insight ({language_label})")

    if used_fallback:
        st.warning("Live AI service unavailable - showing a fallback response.")

    st.info(insight_text)


def render_qa_panel(
    ask_fn,
    simulation_result: dict,
    language: str,
) -> None:
    st.subheader("Ask Your Twin")
    st.caption("Ask a free-text question about this scenario.")

    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    for role, text in st.session_state.qa_history:
        with st.chat_message(role):
            st.write(text)

    question = st.chat_input(
        "e.g. 'What happens if I cut groceries by 10%?'"
    )

    if question:
        st.session_state.qa_history.append(("user", question))

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, used_fallback = ask_fn(
                    simulation_result,
                    question,
                    language,
                )

                if used_fallback:
                    st.caption(
                        "⚠️ fallback response (live AI unavailable)"
                    )

                st.write(answer)

        st.session_state.qa_history.append(("assistant", answer))
