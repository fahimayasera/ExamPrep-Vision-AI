import streamlit as st
from google import genai
from google.genai import types

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
)


MODEL_NAME = "gemini-3.8-flash"

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


# Onboarding

if "onboarded" not in st.session_state:
    st.title("ExamPrep Vision AI 📸")
    st.caption(
        "From Your Final Notes to Smart Revision — "
        "See It. Revise It. Remember It. 🧠"
    )

    with st.form("onboarding_form"):
        name = st.text_input("Your name")

        contact_method = st.selectbox(
            "Choose your contact method",
            ["Email Address", "Phone Number"],
        )

        contact = st.text_input(
            contact_method,
            placeholder="Enter your email or phone number",
        )

        submitted = st.form_submit_button("Let's Start 🚀")

        if submitted:
            if not name.strip() or not contact.strip():
                st.warning(
                    "Please fill in both your name and contact information."
                )
            else:
                st.session_state.name = name.strip()
                st.session_state.contact_method = contact_method
                st.session_state.contact = contact.strip()

                st.session_state.chat = gemini_client.chats.create(
                    model=MODEL_NAME,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    ),
                )

                st.session_state.messages = []
                st.session_state.onboarded = True

                st.rerun()

        st.stop()


def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


# Main App

st.title("ExamPrep Vision AI 📸")

st.caption(
    "Turn your final study notes into faster, smarter exam revision."
)


# Welcome

if not st.session_state.messages:
    st.session_state.messages.append(
        {
            "role": "assistant",
            "kind": "text",
            "content": WELCOME_MESSAGE_TEMPLATE.format(
                name=st.session_state.name
            ),
        }
    )


for message in st.session_state.messages:
    render_message(message)


# Upload Final Notes

st.subheader("📸 Upload Your Final Study Notes")

uploaded_file = st.file_uploader(
    "Upload a photo of your final notes",
    type=["jpg", "jpeg", "png"],
)


if uploaded_file is not None:
    photo_bytes = uploaded_file.getvalue()

    st.session_state.last_note = types.Part.from_bytes(
        data=photo_bytes,
        mime_type=uploaded_file.type,
    )

    st.image(
        photo_bytes,
        caption="Your uploaded final notes",
        use_container_width=True,
    )

    st.success("Your study notes are ready! You can now use the features below.")


# Visual Revision

st.subheader("🎯 Visual Revision")

if st.button("Create Visual Revision"):
    if "last_note" in st.session_state:
        visual_revision_prompt = (
            "Transform these final study notes into a quick visual revision sheet. "
            "Identify key points, important definitions, keywords, structures, "
            "comparisons, flows, and memory cues. "
            "Keep the important information from the original notes. "
            "Make it easy to revise quickly before an exam."
        )

        with st.spinner("Creating your visual revision..."):
            response = ask_gemini(
                [
                    st.session_state.last_note,
                    visual_revision_prompt,
                ]
            )

        st.markdown(response)

    else:
        st.warning("Please upload your study notes first.")


# Smart Note Check

st.subheader("📝 Smart Note Check")

if st.button("Check My Notes"):
    if "last_note" in st.session_state:
        note_check_prompt = (
            "Review the student's uploaded final study notes. "
            "Identify repeated, unnecessary, overly detailed, or unclear points. "
            "For each suggestion, briefly explain what can be shortened, combined, "
            "or removed. Do not remove important syllabus-related information."
        )

        with st.spinner("Checking your notes..."):
            response = ask_gemini(
                [
                    st.session_state.last_note,
                    note_check_prompt,
                ]
            )

        st.markdown(response)

    else:
        st.warning("Please upload your study notes first.")


# Generate Exam Questions

st.subheader("📚 Generate Exam Questions")

marks = st.selectbox(
    "Choose the marks",
    [3, 5, 10],
    format_func=lambda x: f"{x} Marks",
)


if st.button("Generate Exam Question"):
    if "last_note" in st.session_state:
        question_prompt = (
            f"Generate one {marks}-mark exam question based only on the "
            "student's uploaded final study notes. "
            "Match the question to the expected depth for the marks. "
            "Give only the exam question."
        )

        with st.spinner("Generating exam question..."):
            response = ask_gemini(
                [
                    st.session_state.last_note,
                    question_prompt,
                ]
            )

        st.markdown(response)

    else:
        st.warning("Please upload your study notes first.")





# Chat / Upload Area



user_input = st.chat_input(
    "Ask something or attach a photo of your study notes",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text

    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()

        st.session_state.last_note = types.Part.from_bytes(
            data=photo_bytes,
            mime_type=photo.type,
        )

        st.session_state.messages.append(
            {
                "role": "user",
                "kind": "image",
                "content": photo_bytes,
            }
        )

        render_message(st.session_state.messages[-1])

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type,
            )
        )

    if text and "last_note" in st.session_state:
        parts.append(st.session_state.last_note)
        
    if text:
        st.session_state.messages.append(
            {
                "role": "user",
                "kind": "text",
                "content": text,
            }
        )

        render_message(st.session_state.messages[-1])

        parts.append(text)

    elif photo is not None:
        parts.append(
            "Understand these uploaded study notes and help me revise them."
        )

    with st.spinner("Thinking..."):
        response = ask_gemini(parts)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "kind": "text",
            "content": response,
        }
    )