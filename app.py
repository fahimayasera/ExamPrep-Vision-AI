import streamlit as st
from google import genai
from google.genai import types

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
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


# Chat interface

st.title("ExamPrep Vision AI 📸")

st.subheader("Generate Exam Questions")

marks = st.selectbox(
    "Choose the marks",
    [3, 5, 10],
    format_func=lambda x: f"{x} Marks",
)

if st.button("Generate Exam Question"):
    st.info(f"Ready to generate a {marks}-mark question from your uploaded notes.")

st.subheader("Smart Note Check")

if st.button("Check My Notes"):
    st.info(
        "Your notes will be checked for repeated, unnecessary, "
        "or overly detailed points."
    )


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])

st.subheader("Ask a Question")

question = st.text_input(
    "Ask anything about your uploaded study notes",
    placeholder="Example: Explain the difference between while and do-while loop."
)

if st.button("Ask"):
    if question.strip():
        st.info("Your question will be answered using your uploaded notes.")
    else:
        st.warning("Please enter a question.")

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"


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


# Chat input with image upload

user_input = st.chat_input(
    "Explore your topic, or attach a photo of your study notes",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text

    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()

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
            "Transform these final study notes into a visual revision sheet. "
            "Identify key points, important definitions, keywords, structures, "
            "comparisons, flows, and memory cues. Also check for repeated or "
            "unnecessary points that could be shortened without removing "
            "important information. Do not simply repeat the notes."
        )

    with st.spinner("Turning your notes into smart revision..."):
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