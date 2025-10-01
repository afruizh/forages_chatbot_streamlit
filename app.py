import streamlit as st


# Configure Streamlit page with favicon
st.set_page_config(
    page_title="Tropical Forages Chat",
    page_icon="public/grass.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

# Apply custom CSS for background and light theme
st.markdown("""
<style>
    /* Set light theme colors */
    :root {
        --background-color: #ffffff;
        --text-color: #1a1a1a;
        --secondary-bg: #f8f9fa;
        --border-color: #e1e4e8;
    }
    
    /* Main app background with gradient */
    .stApp {
        background-color: #fff;
        background-image: 
            radial-gradient(at 21% 11%, hsl(126.83deg 57% 78% / 52%) 0, transparent 50%), 
            radial-gradient(at 85% 0, rgb(233 230 186 / 53%) 0, transparent 50%), 
            radial-gradient(at 91% 36%, rgb(212 255 194 / 68%) 0, transparent 50%), 
            radial-gradient(at 8% 40%, rgb(239 251 218 / 46%) 0, transparent 50%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        border: 1px solid rgba(225, 228, 232, 0.5);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid #e1e4e8;
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        color: #1a1a1a;
    }
    
    .stButton > button:hover {
        background-color: rgba(248, 249, 250, 0.9);
        border-color: #d1d5da;
    }
    
    /* Metrics and info boxes */
    .metric-container {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        border: 1px solid rgba(225, 228, 232, 0.5);
        padding: 1rem;
    }
    
    /* Force light theme for code blocks */
    .stCodeBlock {
        background-color: rgba(248, 249, 250, 0.9) !important;
    }
    
    /* Custom header styling */
    .chat-header {
        background: linear-gradient(90deg, #28a745, #20c997);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Constrain main content to 80% width */
    .block-container {
        max-width: 60% !important;
        margin: 0 auto !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Alternative selector for content width constraint */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        max-width: 60% !important;
        margin: 0 auto !important;
    }
    
    /* Make chat input full width like header */
    [data-testid="stChatInput"] {
        max-width: 60% !important;
        width: 60% !important;
        left: 20% !important;
        transform: none !important;
    }
    
    /* Chat input container full width */
    .stChatInput > div {
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Alternative chat input selectors */
    [data-testid="stBottom"] > div {
        max-width: 100% !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Init state ---
if "history" not in st.session_state:
    st.session_state.history = []

# Simple header with title, paragraph and logos - HTML only
import base64

# Load images and convert to base64
with open("public/headerv2.jpg", "rb") as f:
    header_img = base64.b64encode(f.read()).decode()
with open("public/logo.png", "rb") as f:
    logo_img = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0; margin-bottom: 2rem;">
    <div style="flex: 0.7;">
        <h1 style="color: #28a745; font-size: 1.0rem; font-weight: bold; margin: 0;">
            TROPICAL FORAGES CHAT
        </h1>
        <p style="color: #6c757d; font-size: 0.85rem; margin: 0 0 0 0; line-height: 1.3;">
            This information is generated using a large language model (LLM) and may contain errors or biases. While we strive for accuracy, it's important to verify information and consult professionals for specific advice. You are responsible for how you use this content. <b>Please do not enter any personal or sensitive information.</b>
        </p>
    </div>
    <div style="display: flex; gap: 15px; align-items: center; flex-shrink: 0;">
        <a href="https://tropicalforages.info/text/intro/index.html" target="_blank" style="text-decoration: none;">
            <img src="data:image/jpeg;base64,{header_img}" style="height: 80px; border-radius: 8px; cursor: pointer; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
        </a>
        <img src="data:image/png;base64,{logo_img}" style="height: 200px;">
    </div>
</div>
""", unsafe_allow_html=True)

# import logging
# import os
# from model_serving_utils import (
#     endpoint_supports_feedback, 
#     query_endpoint, 
#     query_endpoint_stream, 
#     _get_endpoint_task_type,
# )
# from collections import OrderedDict
# from messages import UserMessage, AssistantResponse, render_message

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # --- DEBUG SECTION: Show config and secrets status in the UI ---
# # (Moved here so variables are defined)

# # Try to get configuration from environment variables first, then Streamlit secrets
# SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
# DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
# DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# # If not found in environment, try Streamlit secrets
# if not SERVING_ENDPOINT or not DATABRICKS_HOST or not DATABRICKS_TOKEN:
#     try:
#         # Debug: Show what we're trying to read
#         logger.info("Trying to read from Streamlit secrets...")
        
#         if hasattr(st, 'secrets'):
#             logger.info("Streamlit secrets are available")
#             if not SERVING_ENDPOINT:
#                 try:
#                     SERVING_ENDPOINT = st.secrets["SERVING_ENDPOINT"]
#                     logger.info(f"Got SERVING_ENDPOINT from secrets: {'***' if SERVING_ENDPOINT else 'None'}")
#                 except KeyError:
#                     logger.warning("SERVING_ENDPOINT not found in secrets")
#             if not DATABRICKS_HOST:
#                 try:
#                     DATABRICKS_HOST = st.secrets["DATABRICKS_HOST"]
#                     logger.info(f"Got DATABRICKS_HOST from secrets: {'***' if DATABRICKS_HOST else 'None'}")
#                 except KeyError:
#                     logger.warning("DATABRICKS_HOST not found in secrets")
#             if not DATABRICKS_TOKEN:
#                 try:
#                     DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
#                     logger.info(f"Got DATABRICKS_TOKEN from secrets: {'***' if DATABRICKS_TOKEN else 'None'}")
#                 except KeyError:
#                     logger.warning("DATABRICKS_TOKEN not found in secrets")
#             # Debug: Show available secrets
#             try:
#                 available_secrets = list(st.secrets.keys())
#                 logger.info(f"Available secrets: {available_secrets}")
#             except Exception as e:
#                 logger.warning(f"Could not list secrets: {e}")
#         else:
#             logger.warning("Streamlit secrets not available")
            
#         # Set environment variables for databricks-sdk
#         if DATABRICKS_HOST:
#             os.environ['DATABRICKS_HOST'] = DATABRICKS_HOST
#         if DATABRICKS_TOKEN:
#             os.environ['DATABRICKS_TOKEN'] = DATABRICKS_TOKEN
            
#     except Exception as e:
#         logger.error(f"Error reading from Streamlit secrets: {e}")
#         st.error(f"Error reading secrets: {e}")

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
# # Try to get configuration from environment variables first, then Streamlit secrets
# SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
# DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')
# DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# # If not found in environment, try Streamlit secrets
# if not SERVING_ENDPOINT or not DATABRICKS_HOST or not DATABRICKS_TOKEN:
#     try:
#         # Debug: Show what we're trying to read
#         logger.info("Trying to read from Streamlit secrets...")
        
#         if hasattr(st, 'secrets'):
#             logger.info("Streamlit secrets are available")
#             if not SERVING_ENDPOINT:
#                 try:
#                     SERVING_ENDPOINT = st.secrets["SERVING_ENDPOINT"]
#                     logger.info(f"Got SERVING_ENDPOINT from secrets: {'***' if SERVING_ENDPOINT else 'None'}")
#                 except KeyError:
#                     logger.warning("SERVING_ENDPOINT not found in secrets")
#             if not DATABRICKS_HOST:
#                 try:
#                     DATABRICKS_HOST = st.secrets["DATABRICKS_HOST"]
#                     logger.info(f"Got DATABRICKS_HOST from secrets: {'***' if DATABRICKS_HOST else 'None'}")
#                 except KeyError:
#                     logger.warning("DATABRICKS_HOST not found in secrets")
#             if not DATABRICKS_TOKEN:
#                 try:
#                     DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
#                     logger.info(f"Got DATABRICKS_TOKEN from secrets: {'***' if DATABRICKS_TOKEN else 'None'}")
#                 except KeyError:
#                     logger.warning("DATABRICKS_TOKEN not found in secrets")
#             # Debug: Show available secrets
#             try:
#                 available_secrets = list(st.secrets.keys())
#                 logger.info(f"Available secrets: {available_secrets}")
#             except Exception as e:
#                 logger.warning(f"Could not list secrets: {e}")
#         else:
#             logger.warning("Streamlit secrets not available")
            
#         # Set environment variables for databricks-sdk
#         if DATABRICKS_HOST:
#             os.environ['DATABRICKS_HOST'] = DATABRICKS_HOST
#         if DATABRICKS_TOKEN:
#             os.environ['DATABRICKS_TOKEN'] = DATABRICKS_TOKEN
            
#     except Exception as e:
#         logger.error(f"Error reading from Streamlit secrets: {e}")
#         st.error(f"Error reading secrets: {e}")

# # Check if we have the required configuration
# if not SERVING_ENDPOINT:
#     st.error("❌ **Missing Configuration: SERVING_ENDPOINT**")
#     st.info("""
#     **For Streamlit Cloud deployment**, add this to your app secrets:
#     ```
#     SERVING_ENDPOINT = "your-databricks-endpoint-name"
#     DATABRICKS_HOST = "https://your-workspace.cloud.databricks.com"
#     DATABRICKS_TOKEN = "your-databricks-token"
#     ```
    
#     **For local development**, set environment variables or create `.streamlit/secrets.toml`:
#     ```toml
#     SERVING_ENDPOINT = "your-databricks-endpoint-name"
#     DATABRICKS_HOST = "https://your-workspace.cloud.databricks.com"
#     DATABRICKS_TOKEN = "your-databricks-token"
#     ```
#     """)
#     st.stop()

# if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
#     st.error("❌ **Missing Databricks Authentication**")
#     st.info("""
#     **Required secrets:**
#     - `DATABRICKS_HOST`: Your Databricks workspace URL
#     - `DATABRICKS_TOKEN`: Your Databricks personal access token
    
#     Add these to your Streamlit Cloud app secrets or local `.streamlit/secrets.toml` file.
#     """)
#     st.stop()

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

# try:
#     ENDPOINT_SUPPORTS_FEEDBACK = endpoint_supports_feedback(SERVING_ENDPOINT)
#     st.success("✅ Successfully connected to Databricks endpoint!")
# except Exception as e:
#     logger.warning(f"Could not check endpoint feedback support: {e}")
#     ENDPOINT_SUPPORTS_FEEDBACK = False
#     st.error(f"❌ Could not connect to Databricks: {str(e)}")
#     st.info("Please check your Databricks credentials and endpoint configuration.")

# def reduce_chat_agent_chunks(chunks):
#     """
#     Reduce a list of ChatAgentChunk objects corresponding to a particular
#     message into a single ChatAgentMessage
#     """
#     deltas = [chunk.delta for chunk in chunks]
#     first_delta = deltas[0]
#     result_msg = first_delta
#     msg_contents = []
    
#     # Accumulate tool calls properly
#     tool_call_map = {}  # Map call_id to tool call for accumulation
    
#     for delta in deltas:
#         # Handle content
#         if delta.content:
#             msg_contents.append(delta.content)
            
#         # Handle tool calls
#         if hasattr(delta, 'tool_calls') and delta.tool_calls:
#             for tool_call in delta.tool_calls:
#                 call_id = getattr(tool_call, 'id', None)
#                 tool_type = getattr(tool_call, 'type', "function")
#                 function_info = getattr(tool_call, 'function', None)
#                 if function_info:
#                     func_name = getattr(function_info, 'name', "")
#                     func_args = getattr(function_info, 'arguments', "")
#                 else:
#                     func_name = ""
#                     func_args = ""
                
#                 if call_id:
#                     if call_id not in tool_call_map:
#                         # New tool call
#                         tool_call_map[call_id] = {
#                             "id": call_id,
#                             "type": tool_type,
#                             "function": {
#                                 "name": func_name,
#                                 "arguments": func_args
#                             }
#                         }
#                     else:
#                         # Accumulate arguments for existing tool call
#                         existing_args = tool_call_map[call_id]["function"]["arguments"]
#                         tool_call_map[call_id]["function"]["arguments"] = existing_args + func_args

#                         # Update function name if provided
#                         if func_name:
#                             tool_call_map[call_id]["function"]["name"] = func_name

#         # Handle tool call IDs (for tool response messages)
#         if hasattr(delta, 'tool_call_id') and delta.tool_call_id:
#             result_msg = result_msg.model_copy(update={"tool_call_id": delta.tool_call_id})
    
#     # Convert tool call map back to list
#     if tool_call_map:
#         accumulated_tool_calls = list(tool_call_map.values())
#         result_msg = result_msg.model_copy(update={"tool_calls": accumulated_tool_calls})
    
#     result_msg = result_msg.model_copy(update={"content": "".join(msg_contents)})
#     return result_msg


# # --- Render chat history ---
# for i, element in enumerate(st.session_state.history):
#     element.render(i)

# def query_endpoint_and_render(task_type, input_messages):
#     """Handle streaming response based on task type."""
#     if task_type == "agent/v1/responses":
#         return query_responses_endpoint_and_render(input_messages)
#     elif task_type == "agent/v2/chat":
#         return query_chat_agent_endpoint_and_render(input_messages)
#     else:  # chat/completions
#         return query_chat_completions_endpoint_and_render(input_messages)


# def query_chat_completions_endpoint_and_render(input_messages):
#     """Handle ChatCompletions streaming format."""
#     with st.chat_message("assistant", avatar="public/grass.png"):
#         response_area = st.empty()
#         response_area.markdown("_Thinking..._")
        
#         accumulated_content = ""
#         request_id = None
        
#         try:
#             for chunk in query_endpoint_stream(
#                 endpoint_name=SERVING_ENDPOINT,
#                 messages=input_messages,
#                 return_traces=ENDPOINT_SUPPORTS_FEEDBACK
#             ):
#                 if "choices" in chunk and chunk["choices"]:
#                     delta = chunk["choices"][0].get("delta", {})
#                     content = delta.get("content", "")
#                     if content:
#                         accumulated_content += content
#                         response_area.markdown(accumulated_content)
                
#                 if "databricks_output" in chunk:
#                     req_id = chunk["databricks_output"].get("databricks_request_id")
#                     if req_id:
#                         request_id = req_id
            
#             return AssistantResponse(
#                 messages=[{"role": "assistant", "content": accumulated_content}],
#                 request_id=request_id
#             )
#         except Exception:
#             response_area.markdown("_Ran into an error. Retrying without streaming..._")
#             messages, request_id = query_endpoint(
#                 endpoint_name=SERVING_ENDPOINT,
#                 messages=input_messages,
#                 return_traces=ENDPOINT_SUPPORTS_FEEDBACK
#             )
#             response_area.empty()
#             with response_area.container():
#                 for message in messages:
#                     render_message(message)
#             return AssistantResponse(messages=messages, request_id=request_id)


# def query_chat_agent_endpoint_and_render(input_messages):
#     """Handle ChatAgent streaming format."""
#     from mlflow.types.agent import ChatAgentChunk
    
#     with st.chat_message("assistant", avatar="public/grass.png"):
#         response_area = st.empty()
#         response_area.markdown("_Thinking..._")
        
#         message_buffers = OrderedDict()
#         request_id = None
        
#         try:
#             for raw_chunk in query_endpoint_stream(
#                 endpoint_name=SERVING_ENDPOINT,
#                 messages=input_messages,
#                 return_traces=ENDPOINT_SUPPORTS_FEEDBACK
#             ):
#                 response_area.empty()
#                 chunk = ChatAgentChunk.model_validate(raw_chunk)
#                 delta = chunk.delta
#                 message_id = delta.id

#                 req_id = raw_chunk.get("databricks_output", {}).get("databricks_request_id")
#                 if req_id:
#                     request_id = req_id
#                 if message_id not in message_buffers:
#                     message_buffers[message_id] = {
#                         "chunks": [],
#                         "render_area": st.empty(),
#                     }
#                 message_buffers[message_id]["chunks"].append(chunk)
                
#                 partial_message = reduce_chat_agent_chunks(message_buffers[message_id]["chunks"])
#                 render_area = message_buffers[message_id]["render_area"]
#                 message_content = partial_message.model_dump_compat(exclude_none=True)
#                 with render_area.container():
#                     render_message(message_content)
            
#             messages = []
#             for msg_id, msg_info in message_buffers.items():
#                 messages.append(reduce_chat_agent_chunks(msg_info["chunks"]))
            
#             return AssistantResponse(
#                 messages=[message.model_dump_compat(exclude_none=True) for message in messages],
#                 request_id=request_id
#             )
#         except Exception:
#             response_area.markdown("_Ran into an error. Retrying without streaming..._")
#             messages, request_id = query_endpoint(
#                 endpoint_name=SERVING_ENDPOINT,
#                 messages=input_messages,
#                 return_traces=ENDPOINT_SUPPORTS_FEEDBACK
#             )
#             response_area.empty()
#             with response_area.container():
#                 for message in messages:
#                     render_message(message)
#             return AssistantResponse(messages=messages, request_id=request_id)


# def query_responses_endpoint_and_render(input_messages):
#     """Handle ResponsesAgent streaming format using MLflow types."""
#     from mlflow.types.responses import ResponsesAgentStreamEvent
    
#     with st.chat_message("assistant", avatar="public/grass.png"):
#         response_area = st.empty()
#         response_area.markdown("_Thinking..._")
        
#         # Track all the messages that need to be rendered in order
#         all_messages = []
#         request_id = None

#         try:
#             for raw_event in query_endpoint_stream(
#                 endpoint_name=SERVING_ENDPOINT,
#                 messages=input_messages,
#                 return_traces=ENDPOINT_SUPPORTS_FEEDBACK
#             ):
#                 # Extract databricks_output for request_id
#                 if "databricks_output" in raw_event:
#                     req_id = raw_event["databricks_output"].get("databricks_request_id")
#                     if req_id:
#                         request_id = req_id
                
#                 # Parse using MLflow streaming event types, similar to ChatAgentChunk
#                 if "type" in raw_event:
#                     event = ResponsesAgentStreamEvent.model_validate(raw_event)
                    
#                     if hasattr(event, 'item') and event.item:
#                         item = event.item  # This is a dict, not a parsed object
                        
#                         if item.get("type") == "message":
#                             # Extract text content from message if present
#                             content_parts = item.get("content", [])
#                             for content_part in content_parts:
#                                 if content_part.get("type") == "output_text":
#                                     text = content_part.get("text", "")
#                                     if text:
#                                         all_messages.append({
#                                             "role": "assistant",
#                                             "content": text
#                                         })
                            
#                         elif item.get("type") == "function_call":
#                             # Tool call
#                             call_id = item.get("call_id")
#                             function_name = item.get("name")
#                             arguments = item.get("arguments", "")
                            
#                             # Add to messages for history
#                             all_messages.append({
#                                 "role": "assistant",
#                                 "content": "",
#                                 "tool_calls": [{
#                                     "id": call_id,
#                                     "type": "function",
#                                     "function": {
#                                         "name": function_name,
#                                         "arguments": arguments
#                                     }
#                                 }]
#                             })
                            
#                         elif item.get("type") == "function_call_output":
#                             # Tool call output/result
#                             call_id = item.get("call_id")
#                             output = item.get("output", "")
                            
#                             # Add to messages for history
#                             all_messages.append({
#                                 "role": "tool",
#                                 "content": output,
#                                 "tool_call_id": call_id
#                             })
                
#                 # Update the display by rendering all accumulated messages
#                 if all_messages:
#                     with response_area.container():
#                         for msg in all_messages:
#                             render_message(msg)

#             return AssistantResponse(messages=all_messages, request_id=request_id)
#         except Exception:
#             response_area.markdown("_Ran into an error. Retrying without streaming..._")
#             messages, request_id = query_endpoint(
#                 endpoint_name=SERVING_ENDPOINT,
#                 messages=input_messages,
#                 return_traces=ENDPOINT_SUPPORTS_FEEDBACK
#             )
#             response_area.empty()
#             with response_area.container():
#                 for message in messages:
#                     render_message(message)
#             return AssistantResponse(messages=messages, request_id=request_id)




# # --- Chat input (must run BEFORE rendering messages) ---
# prompt = st.chat_input("Ask a question")
# if prompt:
#     # Get the task type for this endpoint
#     task_type = _get_endpoint_task_type(SERVING_ENDPOINT)
    
#     # Add user message to chat history
#     user_msg = UserMessage(content=prompt)
#     st.session_state.history.append(user_msg)
#     user_msg.render(len(st.session_state.history) - 1)

#     # Convert history to standard chat message format for the query methods
#     input_messages = [msg for elem in st.session_state.history for msg in elem.to_input_messages()]
    
#     # Handle the response using the appropriate handler
#     assistant_response = query_endpoint_and_render(task_type, input_messages)
    
#     # Add assistant response to history
#     st.session_state.history.append(assistant_response)
