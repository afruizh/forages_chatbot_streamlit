"""
Message classes for the chatbot application.

This module contains the message classes used throughout the app.
By keeping them in a separate module, they remain stable across
Streamlit app reruns, avoiding isinstance comparison issues.
"""
import streamlit as st
from abc import ABC, abstractmethod
import re


class Message(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_input_messages(self):
        """Convert this message into a list of dicts suitable for the model API."""
        pass

    @abstractmethod
    def render(self, idx):
        """Render the message in the Streamlit app."""
        pass


class UserMessage(Message):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def to_input_messages(self):
        return [{
            "role": "user",
            "content": self.content
        }]

    def render(self, _):
        with st.chat_message("user", avatar="public/user.png"):
            st.markdown(self.content)


class AssistantResponse(Message):
    def __init__(self, messages, request_id):
        super().__init__()
        self.messages = messages
        # Request ID tracked to enable submitting feedback on assistant responses via the feedback endpoint
        self.request_id = request_id

    def to_input_messages(self):
        return self.messages

    def render(self, idx):
        with st.chat_message("assistant", avatar="public/grass.png"):
            for msg in self.messages:
                render_message(msg)

            if self.request_id is not None:
                render_assistant_message_feedback(idx, self.request_id)


def render_message(msg):
    """Render a single message."""

    # print("Rendering message:*****************************************")
    # print(msg)
    # print("*****************************************")
    if msg["role"] == "assistant":
        import ast
        content = msg.get("content")
        if content:

            # Remove text patterns like 【hash†page_content】
            content = re.sub(r'【[^】]*】', '', content)


            rendered = False
            # Try to parse stringified list/dict and extract only final answer(s)
            if isinstance(content, str) and (content.strip().startswith("[") or content.strip().startswith("{")):
                try:
                    parsed = ast.literal_eval(content)
                    # If it's a list, look for dicts with type 'text' or 'output_text'
                    if isinstance(parsed, list):
                        for part in parsed:
                            if isinstance(part, dict) and part.get("type") in ("text", "output_text") and "text" in part:
                                st.markdown(part["text"])
                                rendered = True
                    elif isinstance(parsed, dict) and parsed.get("type") in ("text", "output_text") and "text" in parsed:
                        st.markdown(parsed["text"])
                        rendered = True
                except Exception:
                    pass
            if not rendered and isinstance(content, str):
                # Only display if it doesn't look like a tool response or raw doc
                if not (content.strip().startswith("[Document(") or content.strip().startswith("[{'chunk_id'")):
                    st.markdown(content)
        # Only render tool calls if you want to show them to the user (optional)
        # If you want to skip tool calls, comment out or remove the following block:
        # if "tool_calls" in msg and msg["tool_calls"]:
        #     for call in msg["tool_calls"]:
        #         fn_name = call["function"]["name"]
        #         args = call["function"]["arguments"]
        #         st.markdown(f"🛠️ Calling **`{fn_name}`** with:\n```json\n{args}\n```")
    elif msg["role"] == "tool":
        #st.markdown("🧰 Tool Response:")
        #st.code(msg["content"], language="json")
        st.markdown("🧰 Retrieving information...")


@st.fragment
def render_assistant_message_feedback(i, request_id):
    """Render feedback UI for assistant messages."""
    from model_serving_utils import submit_feedback
    import os
    
    def save_feedback(index):
        serving_endpoint = os.getenv('SERVING_ENDPOINT')
        if serving_endpoint:
            submit_feedback(
                endpoint=serving_endpoint,
                request_id=request_id,
                rating=st.session_state[f"feedback_{index}"]
            )
    
    st.feedback("thumbs", key=f"feedback_{i}", on_change=save_feedback, args=[i])