import streamlit as st
from google import genai
import speech_recognition as sr
# from gTTS import gTTS
import pyttsx3
import os
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS AI ",
    page_icon="⚡",
    layout="wide"
)

# --- MODERN STYLISH UI ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #090a0f 0%, #121829 50%, #0d111a 100%);
        color: #ffffff;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .user-bubble {
        background: rgba(0, 242, 254, 0.1);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 12px;
        padding: 12px 18px;
        margin: 8px 0;
        color: #e6f7ff;
    }
    .ai-bubble {
        background: rgba(138, 43, 226, 0.15);
        border: 1px solid rgba(138, 43, 226, 0.4);
        border-radius: 12px;
        padding: 12px 18px;
        margin: 8px 0;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ NEXUS AI </div>', unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Settings & Features")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    st.markdown("---")
    st.subheader("🎯 Persona / Role Switcher")
    persona = st.selectbox(
        "Choose AI Role:",
        ["General Assistant", "Code Expert & Debugger", "Interview Trainer", "Marathi Tutor"]
    )
    
    st.markdown("---")
    st.subheader("🔊 Voice & Language Settings")
    enable_voice = st.checkbox("Enable Text-to-Speech", value=True)
    voice_lang = st.selectbox("Speech Language:", ["Marathi (mr)", "Hindi (hi)", "English (en)"])
    lang_code = voice_lang.split("(")[1].replace(")", "")

    st.markdown("---")
    st.subheader("📁 Multimodal File Upload")
    uploaded_file = st.file_uploader("Upload Image/Photo", type=["png", "jpg", "jpeg"])


    # with st.sidebar:
    # st.title("🤖 NEXUS AI")
    # api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    # st.markdown("---")
    
    # # 1. New Chat Button
    # if st.button("➕ New Chat", use_container_width=True):
    #     new_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     st.session_state.current_chat_id = new_id
    #     st.session_state.all_chats[new_id] = []
    #     st.rerun()

    # st.subheader("📜 Previous Search History")
    
    # # 2. Display Past Conversations
    # chat_ids = list(st.session_state.all_chats.keys())
    # chat_ids.reverse()  # नवीन चॅट वर दाखवण्यासाठी
    
    # for chat_id in chat_ids:
    #     messages = st.session_state.all_chats[chat_id]
    #     # चॅटचे नाव पहिल्या मेसेजवरून ठरवणे
    #     first_msg = messages[0]["text"][:20] + "..." if messages else f"Chat {chat_id[11:16]}"
        
    #     col1, col2 = st.columns([4, 1])
    #     with col1:
    #         if st.button(f"💬 {first_msg}", key=f"btn_{chat_id}", use_container_width=True):
    #             st.session_state.current_chat_id = chat_id
    #             st.rerun()
    #     with col2:
    #         if st.button("🗑️", key=f"del_{chat_id}"):
    #             del st.session_state.all_chats[chat_id]
    #             # save_history_to_file(st.session_state.all_chats)
    #             st.rerun()


    import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# ---------------------------------------------------------
# 1. Scheduler चालू करणे (App रन असताना बॅकग्राउंडला चालेल)
# ---------------------------------------------------------
@st.cache_resource
def get_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    return scheduler

scheduler = get_scheduler()

# ---------------------------------------------------------
# 2. Email पाठवणारे मुख्य फंक्शन
# ---------------------------------------------------------
def send_scheduled_email(sender_email, sender_password, recipient_email, subject, message_body):
    try:
        # Gmail SMTP Setup
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Mail Message तयार करणे
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_body, 'plain'))
        
        # Server शी कनेक्ट करून मेल पाठवणे
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"[SUCCESS] Mail successfully sent to {recipient_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

# ---------------------------------------------------------
# 3. Streamlit UI (Schedule Email Form)
# ---------------------------------------------------------
st.title("📧 Scheduled Email Sender")

with st.form("schedule_email_form"):
    recipient = st.text_input("Recipient Email (ज्याला मेल पाठवायचा आहे):")
    subject = st.text_input("Email Subject (विषय):")
    body = st.text_area("Email Content/Body (मजकूर):")
    
    # तारीख आणि वेळ निवडणे
    send_date = st.date_input("कोणत्या तारखेला पाठवायचा आहे?")
    send_time = st.time_input("कोणत्या वेळेला पाठवायचा आहे?")
    
    # Gmail App Password (सुरक्षिततेसाठी st.secrets मध्ये ठेवणे उत्तम)
    sender_email = st.text_input("तुमचा Gmail ID:", value="your_email@gmail.com")
    sender_password = st.text_input("तुमचा Gmail App Password:", type="password")
    
    submit_btn = st.form_submit_button("Schedule Email")

if submit_btn:
    if recipient and subject and body and sender_password:
        # तारीख आणि वेळ एकत्र करून datetime ऑब्जेक्ट बनवणे
        scheduled_datetime = datetime.combine(send_date, send_time)
        
        if scheduled_datetime <= datetime.now():
            st.error("कृपया भविष्यातील (Future) तारीख आणि वेळ निवडा!")
        else:
            # Task Scheduler मध्ये Job Add करणे
            scheduler.add_job(
                send_scheduled_email,
                'date',
                run_date=scheduled_datetime,
                args=[sender_email, sender_password, recipient, subject, body]
            )
            st.success(f"✅ ईमेल यशस्वीरित्या शेड्यूल झाला आहे! तो {scheduled_datetime.strftime('%Y-%m-%d %H:%M')} ला आपोआप पाठवला जाईल.")
    else:
        st.warning("कृपया सर्व आवश्यक माहिती भरा!")

# --- INITIALIZE GEMINI CLIENT ---
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.sidebar.success("✅API Connected Successfully!")
    except Exception:
        st.sidebar.error("❌ Invalid API Key")
else:
    st.info("👈 सुरू करण्यासाठी Sidebar मध्ये API Key टाका.")

# Persona Prompts Mapping
persona_prompts = {
    "General Assistant": "You are a helpful, smart AI assistant.",
    "Code Expert & Debugger": "You are an expert software developer. Fix errors and provide clean code with explanations.",
    "Interview Trainer": "You are an interviewer. Ask technical questions and give feedback on user answers.",
    "Marathi Tutor": "You are a friendly tutor. Respond primarily in simple and natural Marathi."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- VOICE INPUT FUNCTION ---
def listen_user():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.toast("🎤 ऐकत आहे... बोला!", icon="🎙️")
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio, language="mr-IN")
    except Exception:
        return None

# --- RENDER CHAT HISTORY ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble"><b>👤 You:</b> {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble"><b>🤖 Nexus AI:</b> {msg["text"]}</div>', unsafe_allow_html=True)

# Input Layout
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.chat_input("काहीही विचारा किंवा फोटोबद्दल प्रश्न विचारा...")
with col2:
    voice_btn = st.button("🎙️ Speak", use_container_width=True)

if voice_btn:
    spoken_text = listen_user()
    if spoken_text:
        user_input = spoken_text

# --- GENERATE RESPONSE ---
if user_input:
    if not client:
        st.error("कृपया आधी Sidebar मध्ये API Key टाका!")
    else:
        st.session_state.messages.append({"role": "user", "text": user_input})
        st.markdown(f'<div class="user-bubble"><b>👤 You:</b> {user_input}</div>', unsafe_allow_html=True)
        
        with st.spinner("विचार करत आहे..."):
            try:
                # Prepare contents (Text + Image if uploaded)
                system_instruction = persona_prompts[persona]
                prompt = f"{system_instruction}\nUser Question: {user_input}"
                
                contents_list = [prompt]
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    contents_list.append(img)

                # Call Gemini API
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=contents_list,
                )
                ai_text = response.text
                
                st.session_state.messages.append({"role": "ai", "text": ai_text})
                st.markdown(f'<div class="ai-bubble"><b>🤖 Nexus AI:</b> {ai_text}</div>', unsafe_allow_html=True)
                
                # # Speech Output
                
                # if enable_voice:
                if enable_voice:
                     engine = pyttsx3.init()
                     engine.say (ai_text)
                     engine.runAndWait()
                                   
                #     tts = gTTS(text=ai_text, lang=lang_code)
                #     tts.save("response.mp3")
                #     st.audio("response.mp3", autoplay=True)
                    
            except Exception as e:
                st.error(f"Error: {e}")
            

# --- EXPORT CHAT FEATURE ---
if st.session_state.messages:
    chat_text = "\n\n".join([f"{m['role'].upper()}: {m['text']}" for m in st.session_state.messages])
    st.sidebar.markdown("---")
    st.sidebar.download_button("📥 Export Chat History", chat_text, file_name="chat_history.txt")




#  streamlit run AI-assistent-project.py


# API key : AQ.Ab8RN6JT7lpCsS4SIikqvh4z_0eYp0hCOaGWWjO889_MZrC2Xg


# project app password : qtxo evcr ebot wmxn