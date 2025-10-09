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

def format_text_content(text):
    """Format text content, handling tables, HTML tags, and special characters.
    
    Args:
        text (str): The text content to format
        
    Returns:
        str: The formatted text
    """
    def escape_html(s):
        """Escape HTML special characters while preserving existing HTML tags"""
        # Don't escape if the content already has HTML tags
        if '<' in s and '>' in s:
            return s
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Remove text patterns like 【hash†page_content】
    text = re.sub(r'【[^】]*】', '', text)
    
    # Handle markdown formatting before other replacements
    # Non-greedy matches to handle multiple occurrences per line
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)  # Support inline code
    
    # Handle special unicode characters
    text = text.replace("\u202f", " ")  # thin space
    text = text.replace("\u2013", "–")  # en dash
    text = text.replace("\u2014", "—")  # em dash
    text = text.replace("\u2018", "'")  # single quote
    text = text.replace("\u2019", "'")  # single quote
    #text = text.replace("\u201c", """)  # double quote
    #text = text.replace("\u201d", """)  # double quote
    
    # Check if text contains a table (has | characters)
    if "|" in text:
        # Split text into lines
        lines = text.split("\n")
        table_lines = []
        formatted_lines = []
        in_table = False
        
        for line in lines:
            if "|" in line:
                if not in_table:
                    # Start of table, add container div with proper styling
                    formatted_lines.append('<div style="overflow-x: auto; margin: 1em 0;">')
                    formatted_lines.append('<table style="border-collapse: collapse; width: 100%;">')
                    in_table = True
                
                # Process table row
                cells = line.split("|")
                
                # Skip separator lines (lines with only dashes and pipes)
                if re.match(r'^[\|\s\-]+$', line):
                    continue
                    
                if cells:
                    # Remove empty cells from start/end due to leading/trailing |
                    cells = [cell for cell in cells[1:-1] if cell]
                    
                    # Convert the row to HTML with proper cell formatting
                    formatted_cells = []
                    for cell in cells:
                        # Process cell content
                        cell_content = cell.strip()
                        
                        # Escape HTML special chars before any replacements
                        cell_content = escape_html(cell_content)
                        
                        # Handle markdown elements
                        cell_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell_content)
                        cell_content = re.sub(r'_(.*?)_', r'<em>\1</em>', cell_content)
                        cell_content = re.sub(r'`(.*?)`', r'<code>\1</code>', cell_content)
                        
                        # Handle bullet points and line breaks
                        cell_content = cell_content.replace("\n", "<br>")
                        cell_content = cell_content.replace("•", "&#8226;")
                        cell_content = cell_content.replace("-", "&#8211;")  # en dash
                        
                        # Add cell with alignment support
                        align = "left"  # Default alignment
                        if cell_content.strip().startswith(":") and cell_content.strip().endswith(":"):
                            align = "center"
                        elif cell_content.strip().endswith(":"):
                            align = "right"
                            
                        formatted_cells.append(f'<td style="border: 1px solid #ddd; padding: 8px; text-align: {align};">{cell_content}</td>')
                    
                    row_html = f"<tr>{''.join(formatted_cells)}</tr>"
                    table_lines.append(row_html)
            else:
                if in_table:
                    # End of table
                    formatted_lines.append("\n".join(table_lines))
                    formatted_lines.append('</table></div>')
                    table_lines = []
                    in_table = False
                formatted_lines.append(line)
        
        # Handle case where table is at the end of text
        if table_lines:
            formatted_lines.append("\n".join(table_lines))
            formatted_lines.append('</table></div>')
            
        text = "\n".join(formatted_lines)
    
    return text


def extract_text(item):
    """Recursively extract text from nested structures"""
    import ast
    if isinstance(item, str):
        item = ast.literal_eval(item)
    #print("Extracting text from item:*************************")
    # print(type(item))
    #print(item)
    rendered = False
    if isinstance(item, dict):
        #print("is dict")
        # Handle direct text fields
        if item.get("type") in ("text", "output_text", "summary_text") and "text" in item:
            text = item["text"]
            #print("is text")
            formatted_text = format_text_content(text)
            st.markdown(formatted_text, unsafe_allow_html=True)
            #st.markdown(text)
            #print("✅" + text)
            return True
        # Handle reasoning type with summary
        elif item.get("type") == "reasoning" and "summary" in item:
            #print("is reasoning")
            #st.markdown("🤔 Reasoning...\n")
            #print("🤔 Reasoning...\n")
            #extract_text(item["summary"])
            return  True
    # Handle lists by processing each item
    elif isinstance(item, list):
        #print("is list")
        for element in item:
            if element:
                element_rendered = extract_text(element)
                rendered = rendered or element_rendered
    return rendered

def render_message(msg):
    """Render a single message."""

    # print("Rendering message:*****************************************")
    # print(msg)
    # print("*****************************************")
    if msg["role"] == "assistant":
        import ast
        content = msg.get("content")
        if content:

            # # Remove text patterns like 【hash†page_content】
            # content = re.sub(r'【[^】]*】', '', content)
            print("CONTENT:*************************\n",content)


            rendered = False
            # Try to parse stringified list/dict and extract only final answer(s)
            if isinstance(content, str) and (content.strip().startswith("[") or content.strip().startswith("{")):
                
                try:
                    #parsed = ast.literal_eval(content)

                    # extract_text = extract_text(parsed)
                    # if extract_text:
                    #     st.markdown(extract_text)
                    #     rendered = True

                    rendered = extract_text(content)

                except Exception as e:
                    print("Error parsing content:", e  )
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