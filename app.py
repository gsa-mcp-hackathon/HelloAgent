
import asyncio
import streamlit as st


from mcp_client import (
    get_greeting,
    get_application_details,
    get_application_list,
    get_approved_applications_by_vendor,
)

st.title("Hello Agent!")
st.write("Welcome to my first AI application project.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for chat in st.session_state.messages:
    st.chat_message(chat["role"]).write(chat["content"])

message = st.chat_input("Type your message...")

if message:
    st.session_state.messages.append({
        "role": "user",
        "content": message
    })
    st.chat_message("user").write(message)

    try:
         
        if message.strip().lower() == "list":
            reply = asyncio.run(get_application_list())

        elif (
            "microsoft" in message.lower()
            and "approved" in message.lower()
            and "applications" in message.lower()
        ):
            reply = asyncio.run(
                get_approved_applications_by_vendor("Microsoft")
            )

        elif message.lower().startswith("lookup "):

            application_name = message[7:].strip()
            reply = asyncio.run(
                get_application_details(application_name)
            )

        else:
            reply = asyncio.run(get_greeting(message))

    except Exception:
        reply = "Sorry, I couldn't reach my MCP tool. Please try again."

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
    st.chat_message("assistant").write(reply)
