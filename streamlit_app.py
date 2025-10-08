# import streamlit as st

# st.title("My Streamlit App")
# st.write("Hello, world!")


# read a secret
# secret = st.secrets["SERVING_ENDPOINT"]

# show the secret
# st.write(f"SERVING_ENDPOINT: {secret}")

# st.write({
#     "primaryColor": st.get_option("theme.primaryColor"),
#     "backgroundColor": st.get_option("theme.backgroundColor"),
#     "secondaryBackgroundColor": st.get_option("theme.secondaryBackgroundColor"),
#     "textColor": st.get_option("theme.textColor"),
#     "base": st.get_option("theme.base"),
# })

# example_prompts = [
#     "Compare Brachiaria species for drought tolerance",
#     "Best tropical forages for acidic soils",
#     "Climate adaptation strategies for forage systems"
# ]

# for prompt_text in example_prompts:
#     if st.button(prompt_text, key=f"prompt_{prompt_text}"):
#         st.session_state.prompt = prompt_text

import streamlit as st
import os

# Configure Streamlit page with favicon
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

st.set_page_config(
    page_title="Tropical Forages Chat",
    page_icon=os.path.join(PUBLIC_DIR, "grass.png"),
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

# Load images and convert to base64
import base64
with open(os.path.join(PUBLIC_DIR, "headerv2.jpg"), "rb") as f:
    header_img = base64.b64encode(f.read()).decode()
with open(os.path.join(PUBLIC_DIR, "logo.png"), "rb") as f:
    logo_img = base64.b64encode(f.read()).decode()
with open(os.path.join(PUBLIC_DIR, "tf.png"), "rb") as f:
    logo_tf = base64.b64encode(f.read()).decode()


# # Custom CSS for styling
# st.markdown(
#     """
#     <style>

#     .block-container {
#         padding-top: 0px !important;
#         padding-bottom: 0rem !important;
#         padding-left: 0rem !important;
#         padding-right: 0rem !important;
#         margin: 0 !important;
#         max-width: 100vw !important;
#         width: 100vw !important;
#     }

#     .stApp {
#         background-color: #f6f7fb !important;
#     }

#     /* Add top border to chat input bottom container */
#     [data-testid="stBottomBlockContainer"] {
#         border-top: 1px solid rgba(0, 0, 0, 0.2);
#         background-color: rgb(255,255,255) !important;
#     }

#     /* stylish message box */
#     .stChatMessage, .stChatMessage[data-testid="stChatMessage-user"], .stChatMessage[data-testid="stChatMessage-assistant"] {
#         background-color: rgb(255,255,255) !important;
#         box-shadow: 0 2px 12px 0 rgba(0,0,0,0.10) !important;
#         border-radius: 20px !important;
#         border: 1px solid #e1e4e8 !important;
#     }

#     [data-testid="stChatInput"], .stChatMessage, .stChatMessage[data-testid="stChatMessage-user"], .stChatMessage[data-testid="stChatMessage-assistant"] {
#         margin-left: auto !important;
#         margin-right: auto !important;
#         max-width: 1200px !important;
#         width: 100% !important;
#     }

#     [data-testid="stChatMessageContent"] {
#         margin: 0.5rem 1.5rem 0.5rem 1.5rem !important;
#     }

#     /* change button dimensions */
#     .stButton > button {
#         width: 13rem !important;
#         height: 7rem !important;
#     </style>


#     """
# , unsafe_allow_html=True)

def load_css():
    with open(os.path.join(BASE_DIR, "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add this near the top of your app, after setting up PUBLIC_DIR
load_css()

# Add a header
st.markdown(
    f"""
    <div class="custom-header">
        <div class="header-container">
            <div class="header-content">
                <div class="header-title">Tropical Forages Research Assistant</div>
                <div class="header-subtitle">Advancing Agricultural Intelligence</div>                
                <a href="https://alliancebioversityciat.org/crops/tropical-forages" target="_blank" style="text-decoration: none;">
                    <img src="data:image/jpeg;base64,{logo_tf}" class="logo-tf" title="Tropical Forages Progra" alt="Tropical Forages Program">
                </a>            
            </div>
            <div class='header-right'>
                <a href="https://tropicalforages.info/text/intro/index.html" target="_blank" style="text-decoration: none;">
                    <img src="data:image/jpeg;base64,{header_img}" class="header-image" title="Tropical Forages Info" alt="Tropical Forages Info">
                </a>
                <img src="data:image/png;base64,{logo_img}" class="logo-image">
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Placeholder for contents
content = st.empty()

# --- Init state ---
if "history" not in st.session_state:
    st.session_state.history = []
if "started" not in st.session_state:
    st.session_state.started = False
if "example_prompt" not in st.session_state:
    st.session_state.example_prompt = None
if "page" not in st.session_state:
    st.session_state.page = "intro"  # Can be "intro" or "chat"

# st.markdown(f"""
# <style>
# @media (max-width: 1500px) {{
#     .responsive-header {{
#         flex-direction: column !important;
#         align-items: stretch !important;
#         text-align: center !important;
#         gap: 1.2rem !important;
#     }}
#     .responsive-header .header-left, .responsive-header .header-right {{
#         flex: unset !important;
#         width: 100% !important;
#         justify-content: center !important;
#         align-items: center !important;
#     }}
#     .responsive-header h1 {{
#         font-size: 1.2rem !important;
#     }}
#     .responsive-header p {{
#         font-size: 0.95rem !important;
#     }}
#     .responsive-header img {{
#         height: 60px !important;
#         max-width: 90vw !important;
#     }}
#     .responsive-header .logo-img {{
#         height: 100px !important;
#     }}
# }}
# </style>
# <div class="responsive-header" style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0; margin-bottom: 2rem; gap: 2rem;">
#         <div class="header-left" style="flex: 0.7; min-width: 0;">
#                 <h1 style="color: #28a745; font-size: 1.0rem; font-weight: bold; margin: 0;">
#                         TROPICAL FORAGES CHAT
#                 </h1>
#                 <p style="color: #6c757d; font-size: 0.85rem; margin: 0 0 0 0; line-height: 1.3;">
#                         This information is generated using a large language model (LLM) and may contain errors or biases. While we strive for accuracy, it's important to verify information and consult professionals for specific advice. You are responsible for how you use this content. <b>Please do not enter any personal or sensitive information.</b>
#                 </p>
#         </div>
#         <div class="header-right" style="display: flex; gap: 15px; align-items: center; flex-shrink: 0; min-width: 0;">
#                 <a href="https://tropicalforages.info/text/intro/index.html" target="_blank" style="text-decoration: none;">
#                         <img src="data:image/jpeg;base64,{header_img}" style="height: 80px; border-radius: 8px; cursor: pointer; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
#                 </a>
#                 <img class="logo-img" src="data:image/png;base64,{logo_img}" style="height: 200px;">
#         </div>
# </div>
# """, unsafe_allow_html=True)

import logging
import os
from model_serving_utils import (
    endpoint_supports_feedback, 
    query_endpoint, 
    query_endpoint_stream, 
    _get_endpoint_task_type,
)
from collections import OrderedDict
from messages import UserMessage, AssistantResponse, render_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- DEBUG SECTION: Show config and secrets status in the UI ---
# (Moved here so variables are defined)

# Try to get configuration from environment variables first, then Streamlit secrets
SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# If not found in environment, try Streamlit secrets
if not SERVING_ENDPOINT or not DATABRICKS_HOST or not DATABRICKS_TOKEN:
    try:
        # Debug: Show what we're trying to read
        logger.info("Trying to read from Streamlit secrets...")
        
        if hasattr(st, 'secrets'):
            logger.info("Streamlit secrets are available")
            if not SERVING_ENDPOINT:
                try:
                    SERVING_ENDPOINT = st.secrets["SERVING_ENDPOINT"]
                    logger.info(f"Got SERVING_ENDPOINT from secrets: {'***' if SERVING_ENDPOINT else 'None'}")
                except KeyError:
                    logger.warning("SERVING_ENDPOINT not found in secrets")
            if not DATABRICKS_HOST:
                try:
                    DATABRICKS_HOST = st.secrets["DATABRICKS_HOST"]
                    logger.info(f"Got DATABRICKS_HOST from secrets: {'***' if DATABRICKS_HOST else 'None'}")
                except KeyError:
                    logger.warning("DATABRICKS_HOST not found in secrets")
            if not DATABRICKS_TOKEN:
                try:
                    DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
                    logger.info(f"Got DATABRICKS_TOKEN from secrets: {'***' if DATABRICKS_TOKEN else 'None'}")
                except KeyError:
                    logger.warning("DATABRICKS_TOKEN not found in secrets")
            # Debug: Show available secrets
            try:
                available_secrets = list(st.secrets.keys())
                logger.info(f"Available secrets: {available_secrets}")
            except Exception as e:
                logger.warning(f"Could not list secrets: {e}")
        else:
            logger.warning("Streamlit secrets not available")
            
        # Set environment variables for databricks-sdk
        if DATABRICKS_HOST:
            os.environ['DATABRICKS_HOST'] = DATABRICKS_HOST
        if DATABRICKS_TOKEN:
            os.environ['DATABRICKS_TOKEN'] = DATABRICKS_TOKEN
            
    except Exception as e:
        logger.error(f"Error reading from Streamlit secrets: {e}")
        st.error(f"Error reading secrets: {e}")

# # --- DEBUG SECTION: Show config and secrets status in the UI ---
# with st.expander('🛠️ Debug: Configuration & Secrets', expanded=True):
#     st.write('**App config values:**')
#     st.write(f"SERVING_ENDPOINT: {'✅' if SERVING_ENDPOINT else '❌'} {SERVING_ENDPOINT if SERVING_ENDPOINT else ''}")
#     st.write(f"DATABRICKS_HOST: {'✅' if DATABRICKS_HOST else '❌'} {DATABRICKS_HOST if DATABRICKS_HOST else ''}")
#     st.write(f"DATABRICKS_TOKEN: {'✅' if DATABRICKS_TOKEN else '❌'} {'set' if DATABRICKS_TOKEN else ''}")
#     st.write('**Environment variables:**')
#     st.write(f"os.environ['SERVING_ENDPOINT']: {os.environ.get('SERVING_ENDPOINT')}")
#     st.write(f"os.environ['DATABRICKS_HOST']: {os.environ.get('DATABRICKS_HOST')}")
#     st.write(f"os.environ['DATABRICKS_TOKEN']: {'set' if os.environ.get('DATABRICKS_TOKEN') else ''}")
#     st.write('**st.secrets keys:**')
#     try:
#         st.write(list(st.secrets.keys()))
#     except Exception as e:
#         st.write(f"Could not access st.secrets: {e}")
# Try to get configuration from environment variables first, then Streamlit secrets
SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# If not found in environment, try Streamlit secrets
if not SERVING_ENDPOINT or not DATABRICKS_HOST or not DATABRICKS_TOKEN:
    try:
        # Debug: Show what we're trying to read
        logger.info("Trying to read from Streamlit secrets...")
        
        if hasattr(st, 'secrets'):
            logger.info("Streamlit secrets are available")
            if not SERVING_ENDPOINT:
                try:
                    SERVING_ENDPOINT = st.secrets["SERVING_ENDPOINT"]
                    logger.info(f"Got SERVING_ENDPOINT from secrets: {'***' if SERVING_ENDPOINT else 'None'}")
                except KeyError:
                    logger.warning("SERVING_ENDPOINT not found in secrets")
            if not DATABRICKS_HOST:
                try:
                    DATABRICKS_HOST = st.secrets["DATABRICKS_HOST"]
                    logger.info(f"Got DATABRICKS_HOST from secrets: {'***' if DATABRICKS_HOST else 'None'}")
                except KeyError:
                    logger.warning("DATABRICKS_HOST not found in secrets")
            if not DATABRICKS_TOKEN:
                try:
                    DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
                    logger.info(f"Got DATABRICKS_TOKEN from secrets: {'***' if DATABRICKS_TOKEN else 'None'}")
                except KeyError:
                    logger.warning("DATABRICKS_TOKEN not found in secrets")
            # Debug: Show available secrets
            try:
                available_secrets = list(st.secrets.keys())
                logger.info(f"Available secrets: {available_secrets}")
            except Exception as e:
                logger.warning(f"Could not list secrets: {e}")
        else:
            logger.warning("Streamlit secrets not available")
            
        # Set environment variables for databricks-sdk
        if DATABRICKS_HOST:
            os.environ['DATABRICKS_HOST'] = DATABRICKS_HOST
        if DATABRICKS_TOKEN:
            os.environ['DATABRICKS_TOKEN'] = DATABRICKS_TOKEN
            
    except Exception as e:
        logger.error(f"Error reading from Streamlit secrets: {e}")
        st.error(f"Error reading secrets: {e}")

# Check if we have the required configuration
if not SERVING_ENDPOINT:
    st.error("❌ **Missing Configuration: SERVING_ENDPOINT**")
    st.info("""
    **For Streamlit Cloud deployment**, add this to your app secrets:
    ```
    SERVING_ENDPOINT = "your-databricks-endpoint-name"
    DATABRICKS_HOST = "https://your-workspace.cloud.databricks.com"
    DATABRICKS_TOKEN = "your-databricks-token"
    ```
    
    **For local development**, set environment variables or create `.streamlit/secrets.toml`:
    ```toml
    SERVING_ENDPOINT = "your-databricks-endpoint-name"
    DATABRICKS_HOST = "https://your-workspace.cloud.databricks.com"
    DATABRICKS_TOKEN = "your-databricks-token"
    ```
    """)
    st.stop()

if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
    st.error("❌ **Missing Databricks Authentication**")
    st.info("""
    **Required secrets:**
    - `DATABRICKS_HOST`: Your Databricks workspace URL
    - `DATABRICKS_TOKEN`: Your Databricks personal access token
    
    Add these to your Streamlit Cloud app secrets or local `.streamlit/secrets.toml` file.
    """)
    st.stop()

# # Debug info (remove in production)
# with st.expander("🔧 Configuration Debug", expanded=False):
#     st.write("**Configuration Status:**")
#     st.write(f"- SERVING_ENDPOINT: {'✅ Set' if SERVING_ENDPOINT else '❌ Missing'}")
#     st.write(f"- DATABRICKS_HOST: {'✅ Set' if DATABRICKS_HOST else '❌ Missing'}")
#     st.write(f"- DATABRICKS_TOKEN: {'✅ Set' if DATABRICKS_TOKEN else '❌ Missing'}")
    
#     if SERVING_ENDPOINT:
#         st.write(f"- Endpoint name: `{SERVING_ENDPOINT}`")
#     if DATABRICKS_HOST:
#         st.write(f"- Databricks host: `{DATABRICKS_HOST}`")

try:
    ENDPOINT_SUPPORTS_FEEDBACK = endpoint_supports_feedback(SERVING_ENDPOINT)
    #st.success("✅ Successfully connected to Databricks endpoint!")
except Exception as e:
    logger.warning(f"Could not check endpoint feedback support: {e}")
    ENDPOINT_SUPPORTS_FEEDBACK = False
    st.error(f"❌ Could not connect to endpoint: {str(e)}")
    st.info("Please check your credentials and endpoint configuration.")




def reduce_chat_agent_chunks(chunks):
    """
    Reduce a list of ChatAgentChunk objects corresponding to a particular
    message into a single ChatAgentMessage
    """
    deltas = [chunk.delta for chunk in chunks]
    first_delta = deltas[0]
    result_msg = first_delta
    msg_contents = []
    
    # Accumulate tool calls properly
    tool_call_map = {}  # Map call_id to tool call for accumulation
    
    for delta in deltas:
        # Handle content
        if delta.content:
            msg_contents.append(delta.content)
            
        # Handle tool calls
        if hasattr(delta, 'tool_calls') and delta.tool_calls:
            for tool_call in delta.tool_calls:
                call_id = getattr(tool_call, 'id', None)
                tool_type = getattr(tool_call, 'type', "function")
                function_info = getattr(tool_call, 'function', None)
                if function_info:
                    func_name = getattr(function_info, 'name', "")
                    func_args = getattr(function_info, 'arguments', "")
                else:
                    func_name = ""
                    func_args = ""
                
                if call_id:
                    if call_id not in tool_call_map:
                        # New tool call
                        tool_call_map[call_id] = {
                            "id": call_id,
                            "type": tool_type,
                            "function": {
                                "name": func_name,
                                "arguments": func_args
                            }
                        }
                    else:
                        # Accumulate arguments for existing tool call
                        existing_args = tool_call_map[call_id]["function"]["arguments"]
                        tool_call_map[call_id]["function"]["arguments"] = existing_args + func_args

                        # Update function name if provided
                        if func_name:
                            tool_call_map[call_id]["function"]["name"] = func_name

        # Handle tool call IDs (for tool response messages)
        if hasattr(delta, 'tool_call_id') and delta.tool_call_id:
            result_msg = result_msg.model_copy(update={"tool_call_id": delta.tool_call_id})
    
    # Convert tool call map back to list
    if tool_call_map:
        accumulated_tool_calls = list(tool_call_map.values())
        result_msg = result_msg.model_copy(update={"tool_calls": accumulated_tool_calls})
    
    result_msg = result_msg.model_copy(update={"content": "".join(msg_contents)})
    return result_msg


# # --- Render chat history ---
# for i, element in enumerate(st.session_state.history):
#     element.render(i)

def query_endpoint_and_render(task_type, input_messages):
    """Handle streaming response based on task type."""
    if task_type == "agent/v1/responses":
        return query_responses_endpoint_and_render(input_messages)
    elif task_type == "agent/v2/chat":
        return query_chat_agent_endpoint_and_render(input_messages)
    else:  # chat/completions
        return query_chat_completions_endpoint_and_render(input_messages)


def query_chat_completions_endpoint_and_render(input_messages):
    """Handle ChatCompletions streaming format."""
    with st.chat_message("assistant", avatar="public/grass.png"):
        response_area = st.empty()
        response_area.markdown("_Thinking..._")
        
        accumulated_content = ""
        request_id = None
        
        try:
            for chunk in query_endpoint_stream(
                endpoint_name=SERVING_ENDPOINT,
                messages=input_messages,
                return_traces=ENDPOINT_SUPPORTS_FEEDBACK
            ):
                if "choices" in chunk and chunk["choices"]:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        accumulated_content += content
                        response_area.markdown(accumulated_content)
                
                if "databricks_output" in chunk:
                    req_id = chunk["databricks_output"].get("databricks_request_id")
                    if req_id:
                        request_id = req_id
            
            return AssistantResponse(
                messages=[{"role": "assistant", "content": accumulated_content}],
                request_id=request_id
            )
        except Exception:
            response_area.markdown("_Ran into an error. Retrying without streaming..._")
            messages, request_id = query_endpoint(
                endpoint_name=SERVING_ENDPOINT,
                messages=input_messages,
                return_traces=ENDPOINT_SUPPORTS_FEEDBACK
            )
            response_area.empty()
            with response_area.container():
                for message in messages:
                    render_message(message)
            return AssistantResponse(messages=messages, request_id=request_id)


def query_chat_agent_endpoint_and_render(input_messages):
    """Handle ChatAgent streaming format."""
    from mlflow.types.agent import ChatAgentChunk
    
    with st.chat_message("assistant", avatar="public/grass.png"):
        response_area = st.empty()
        response_area.markdown("_Thinking..._")
        
        message_buffers = OrderedDict()
        request_id = None
        
        try:
            for raw_chunk in query_endpoint_stream(
                endpoint_name=SERVING_ENDPOINT,
                messages=input_messages,
                return_traces=ENDPOINT_SUPPORTS_FEEDBACK
            ):
                response_area.empty()
                chunk = ChatAgentChunk.model_validate(raw_chunk)
                delta = chunk.delta
                message_id = delta.id

                req_id = raw_chunk.get("databricks_output", {}).get("databricks_request_id")
                if req_id:
                    request_id = req_id
                if message_id not in message_buffers:
                    message_buffers[message_id] = {
                        "chunks": [],
                        "render_area": st.empty(),
                    }
                message_buffers[message_id]["chunks"].append(chunk)
                
                partial_message = reduce_chat_agent_chunks(message_buffers[message_id]["chunks"])
                render_area = message_buffers[message_id]["render_area"]
                message_content = partial_message.model_dump_compat(exclude_none=True)
                with render_area.container():
                    render_message(message_content)
            
            messages = []
            for msg_id, msg_info in message_buffers.items():
                messages.append(reduce_chat_agent_chunks(msg_info["chunks"]))
            
            return AssistantResponse(
                messages=[message.model_dump_compat(exclude_none=True) for message in messages],
                request_id=request_id
            )
        except Exception:
            response_area.markdown("_Ran into an error. Retrying without streaming..._")
            messages, request_id = query_endpoint(
                endpoint_name=SERVING_ENDPOINT,
                messages=input_messages,
                return_traces=ENDPOINT_SUPPORTS_FEEDBACK
            )
            response_area.empty()
            with response_area.container():
                for message in messages:
                    render_message(message)
            return AssistantResponse(messages=messages, request_id=request_id)


def query_responses_endpoint_and_render(input_messages):
    """Handle ResponsesAgent streaming format using MLflow types."""
    from mlflow.types.responses import ResponsesAgentStreamEvent
    
    with st.chat_message("assistant", avatar="public/grass.png"):
        response_area = st.empty()
        response_area.markdown("_Thinking..._")
        
        # Track all the messages that need to be rendered in order
        all_messages = []
        request_id = None

        try:
            for raw_event in query_endpoint_stream(
                endpoint_name=SERVING_ENDPOINT,
                messages=input_messages,
                return_traces=ENDPOINT_SUPPORTS_FEEDBACK
            ):
                # Extract databricks_output for request_id
                if "databricks_output" in raw_event:
                    req_id = raw_event["databricks_output"].get("databricks_request_id")
                    if req_id:
                        request_id = req_id
                
                # Parse using MLflow streaming event types, similar to ChatAgentChunk
                if "type" in raw_event:
                    event = ResponsesAgentStreamEvent.model_validate(raw_event)
                    
                    if hasattr(event, 'item') and event.item:
                        item = event.item  # This is a dict, not a parsed object
                        
                        if item.get("type") == "message":
                            # Extract text content from message if present
                            content_parts = item.get("content", [])
                            for content_part in content_parts:
                                if content_part.get("type") == "output_text":
                                    text = content_part.get("text", "")
                                    if text:
                                        all_messages.append({
                                            "role": "assistant",
                                            "content": text
                                        })
                            
                        elif item.get("type") == "function_call":
                            # Tool call
                            call_id = item.get("call_id")
                            function_name = item.get("name")
                            arguments = item.get("arguments", "")
                            
                            # Add to messages for history
                            all_messages.append({
                                "role": "assistant",
                                "content": "",
                                "tool_calls": [{
                                    "id": call_id,
                                    "type": "function",
                                    "function": {
                                        "name": function_name,
                                        "arguments": arguments
                                    }
                                }]
                            })
                            
                        elif item.get("type") == "function_call_output":
                            # Tool call output/result
                            call_id = item.get("call_id")
                            output = item.get("output", "")
                            
                            # Add to messages for history
                            all_messages.append({
                                "role": "tool",
                                "content": output,
                                "tool_call_id": call_id
                            })
                
                # Update the display by rendering all accumulated messages
                if all_messages:
                    with response_area.container():
                        for msg in all_messages:
                            render_message(msg)

            return AssistantResponse(messages=all_messages, request_id=request_id)
        except Exception:
            response_area.markdown("_Ran into an error. Retrying without streaming..._")
            messages, request_id = query_endpoint(
                endpoint_name=SERVING_ENDPOINT,
                messages=input_messages,
                return_traces=ENDPOINT_SUPPORTS_FEEDBACK
            )
            response_area.empty()
            with response_area.container():
                for message in messages:
                    render_message(message)
            return AssistantResponse(messages=messages, request_id=request_id)
        
def handle_prompt(prompt):


    # Get the task type for this endpoint
    task_type = _get_endpoint_task_type(SERVING_ENDPOINT)
    
    # Add user message to chat history
    user_msg = UserMessage(content=prompt)
    st.session_state.history.append(user_msg)
    user_msg.render(len(st.session_state.history) - 1)

    # Convert history to standard chat message format for the query methods
    input_messages = [msg for elem in st.session_state.history for msg in elem.to_input_messages()]
    
    # Handle the response using the appropriate handler
    assistant_response = query_endpoint_and_render(task_type, input_messages)

    #st.write(assistant_response.messages)
    
    # Add assistant response to history
    st.session_state.history.append(assistant_response)



# # --- Chat input (must run BEFORE rendering messages) ---
# prompt = st.chat_input("Ask a question")


# # If user typed a prompt, or a button set a prompt, handle sending
# if prompt:
#     handle_prompt(prompt)

content = st.empty()
   
def render_intro():

    with content.container():

        # --- Introduction Section ---
        st.markdown("""
            <div class="intro-container">
                <div class="intro-content">
                    <h1 class="intro-title">Welcome to the Tropical Forages Research Assistant</h1>
                    <p class="intro-text">Get accurate, cited information from the <b>Tropical Forages Interactive Tool</b> and peer-reviewed journal articles from <b>Tropical Grasslands - Forrajes Tropicales</b>. Ask questions about plant species, nutritional values, climate adaptation, and management practices.
                    This information is generated using a large language model (LLM) and Retrieval Augmented Generation (RAG) system, and may contain errors or biases. While we strive for accuracy, it's important to verify information and consult professionals for specific advice. You are responsible for how you use this content. <b>Please do not enter any personal or sensitive information.</b></p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- Sample Prompts Section ---
        st.markdown("<div style='font-size: 1rem; font-weight: 600; color: #218838; margin-bottom: 0.5rem; text-align:center;'>EXAMPLE PROMPTS</div>", unsafe_allow_html=True)
        example_prompts = [                
            "Compare Brachiaria species for drought tolerance",
            "Best tropical forages for acidic soils",
            "Climate adaptation strategies for forage systems",
            "Tell me about the journal",
            "Hello, what can you do?"
        ]

        if "prompt" not in st.session_state:
            st.session_state.prompt = ""

        content2 = st.empty()
        with content2.container():
            # Center the columns and make them smaller in width

            # Make a list of len(example_prompts) + 2 with 1.5 rem padding on sides
            col_widths = [1.0] + [0.6] * len(example_prompts) + [1.0]
            centered_cols = st.columns(col_widths)  # 3 buttons, center with padding
            for idx, prompt_text in enumerate(example_prompts):
                with centered_cols[idx + 1]:  # Use the middle columns for buttons
                    if st.button(prompt_text, key=f"prompt_{prompt_text}"):
                        st.session_state.example_prompt = prompt_text

# --- Main content rendering ---
if not st.session_state.history and st.session_state.example_prompt is None:

    render_intro()
        
    # Chat input
    prompt = st.chat_input("Ask a question")
    if prompt:
        st.session_state.example_prompt = prompt        
        
else:  

    for i, element in enumerate(st.session_state.history):
        element.render(i)
        
    # Chat input
    prompt = st.chat_input("Ask a question")    
    if prompt:
        handle_prompt(prompt)

if st.session_state.example_prompt:
    content.empty()
    print(st.session_state.example_prompt)
    prompt = st.session_state.example_prompt
    st.session_state.example_prompt = None  # Clear it after use
    handle_prompt(prompt)
else:
    print("No example prompt yet")
