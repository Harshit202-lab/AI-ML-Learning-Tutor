import streamlit as st
from groq import Groq
import uuid
from datetime import datetime


client = Groq(api_key="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")


st.set_page_config(
    page_title="NeuralTutor — AI/ML Learning Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


defaults = {
    "chats": {},
    "chat_titles": {},
    "model": None,
    "topic_filter": "General AI/ML",
    "active_tab": "roadmap",
    "notes": "",
    "bookmarks": [],
    "completed_topics": [],
    "total_messages": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.chats:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []
    st.session_state.chat_titles[chat_id] = "New Conversation"

if "current_chat" not in st.session_state:
    chat_id = list(st.session_state.chats.keys())[0]
    st.session_state.current_chat = chat_id


def get_working_model():
    try:
        models = client.models.list().data
        preferred = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
        model_ids = [m.id for m in models]
        for p in preferred:
            if p in model_ids:
                return p
        for m in models:
            if "llama" in m.id.lower() or "mixtral" in m.id.lower():
                return m.id
        return models[0].id if models else None
    except:
        return None

if st.session_state.model is None:
    st.session_state.model = get_working_model()

model_display = st.session_state.model or "Unavailable"


TOPIC_PROMPTS = {
    "General AI/ML":    "You are NeuralTutor, an expert AI/ML tutor. Explain concepts clearly with examples, analogies, and code snippets when useful. Be encouraging and pedagogical.",
    "Deep Learning":    "You are NeuralTutor specializing in Deep Learning. Cover neural networks, backprop, CNNs, RNNs, Transformers, and PyTorch/TensorFlow. Use clear mathematical intuitions and code examples.",
    "Machine Learning": "You are NeuralTutor specializing in classical Machine Learning. Cover supervised/unsupervised learning, regression, classification, clustering, and scikit-learn. Be practical and example-driven.",
    "NLP":              "You are NeuralTutor specializing in Natural Language Processing. Cover tokenization, embeddings, attention, LLMs, BERT, GPT, and HuggingFace. Make abstract concepts tangible.",
    "Computer Vision":  "You are NeuralTutor specializing in Computer Vision. Cover CNNs, object detection, segmentation, GANs, diffusion models, and OpenCV/torchvision.",
    "MLOps":            "You are NeuralTutor specializing in MLOps. Cover model deployment, monitoring, CI/CD for ML, Docker, Kubernetes, MLflow, and production best practices.",
    "Mathematics for AI":"You are NeuralTutor specializing in Mathematics for AI. Cover linear algebra, calculus, probability, statistics, and optimization with focus on ML applications.",
}

QUICK_PROMPTS = {
    "🧮 Backpropagation":              "Can you explain backpropagation step-by-step with a simple example?",
    "🌲 Decision Trees vs NNs":        "What are the key differences between decision trees and neural networks?",
    "📐 Attention Mechanism":          "Explain the attention mechanism in transformers with an intuitive analogy.",
    "🔄 Overfitting & Regularization": "What is overfitting and how do L1, L2, and dropout prevent it?",
    "📊 Gradient Descent":             "Explain gradient descent and its variants (SGD, Adam, RMSProp).",
    "🤖 Build a Neural Net":           "Show me how to build a simple neural network in Python using PyTorch.",
}

ROADMAPS = {
    "General AI/ML": [
        ("Python & NumPy Basics", "📦"), ("Statistics & Probability", "📊"),
        ("Classical ML Algorithms", "🌲"), ("Model Evaluation & Tuning", "🎯"),
        ("Feature Engineering", "🔧"), ("Deep Learning Intro", "🧠"),
        ("NLP & Computer Vision", "👁️"), ("Deployment & MLOps", "🚀"),
    ],
    "Deep Learning": [
        ("Linear Algebra Review", "📐"), ("Calculus & Optimization", "📉"),
        ("Neural Network Fundamentals", "🔗"), ("CNNs & Image Models", "🖼️"),
        ("RNNs & Sequence Models", "🔄"), ("Transformers & Attention", "⚡"),
        ("PyTorch / TensorFlow", "🔥"), ("Advanced Architectures", "🏗️"),
    ],
    "NLP": [
        ("Text Preprocessing", "📝"), ("Word Embeddings", "🔤"),
        ("RNN / LSTM basics", "🔄"), ("Attention Mechanism", "📐"),
        ("BERT & GPT Models", "🤖"), ("Fine-tuning LLMs", "🎯"),
        ("HuggingFace Hub", "🤗"), ("RAG & Agents", "🔗"),
    ],
    "Machine Learning": [
        ("Data Exploration (EDA)", "🔍"), ("Regression Models", "📈"),
        ("Classification Models", "🏷️"), ("Unsupervised Learning", "🌀"),
        ("Ensemble Methods", "🌲"), ("Model Evaluation", "📊"),
        ("Hyperparameter Tuning", "⚙️"), ("Scikit-learn Pipelines", "🚀"),
    ],
    "Computer Vision": [
        ("Image Processing Basics", "🖼️"), ("CNNs Architecture", "🔗"),
        ("Transfer Learning", "♻️"), ("Object Detection", "📦"),
        ("Image Segmentation", "✂️"), ("GANs & Diffusion", "🎨"),
        ("OpenCV & torchvision", "👁️"), ("Production Deployment", "🚀"),
    ],
    "MLOps": [
        ("Docker & Containerization", "🐳"), ("FastAPI / Flask Serving", "⚡"),
        ("MLflow Experiment Tracking", "📊"), ("CI/CD for ML Pipelines", "🔄"),
        ("Kubernetes Deployment", "☸️"), ("Monitoring & Drift Detection", "📡"),
        ("Feature Stores", "🗄️"), ("Cloud Platforms (AWS/GCP)", "☁️"),
    ],
    "Mathematics for AI": [
        ("Linear Algebra (Vectors/Matrices)", "📐"), ("Matrix Decompositions", "🔢"),
        ("Multivariate Calculus", "📉"), ("Probability Theory", "🎲"),
        ("Statistics & Distributions", "📊"), ("Optimization Methods", "🎯"),
        ("Information Theory", "📡"), ("Graph Theory basics", "🔗"),
    ],
}

RESOURCES = {
    "General AI/ML":    [("fast.ai – Practical Deep Learning", "https://course.fast.ai"),
                         ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"),
                         ("Kaggle Learn", "https://www.kaggle.com/learn"),
                         ("Papers With Code", "https://paperswithcode.com")],
    "Deep Learning":    [("Deep Learning Book (Goodfellow)", "https://www.deeplearningbook.org"),
                         ("PyTorch Tutorials", "https://pytorch.org/tutorials"),
                         ("Dive into Deep Learning", "https://d2l.ai"),
                         ("Stanford CS231n", "https://cs231n.stanford.edu")],
    "NLP":              [("HuggingFace NLP Course", "https://huggingface.co/learn/nlp-course"),
                         ("Stanford CS224N", "https://web.stanford.edu/class/cs224n"),
                         ("NLTK Book", "https://www.nltk.org/book"),
                         ("LangChain Docs", "https://docs.langchain.com")],
    "Machine Learning": [("Scikit-learn Docs", "https://scikit-learn.org/stable"),
                         ("StatQuest YouTube", "https://youtube.com/@statquest"),
                         ("ML Mastery Blog", "https://machinelearningmastery.com"),
                         ("Elements of Stat. Learning", "https://web.stanford.edu/~hastie/ElemStatLearn")],
    "Computer Vision":  [("Stanford CS231n Notes", "https://cs231n.github.io"),
                         ("OpenCV Tutorials", "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html"),
                         ("torchvision Docs", "https://pytorch.org/vision/stable"),
                         ("Roboflow Blog", "https://blog.roboflow.com")],
    "MLOps":            [("MLflow Docs", "https://mlflow.org/docs/latest"),
                         ("Made With ML", "https://madewithml.com"),
                         ("Full Stack Deep Learning", "https://fullstackdeeplearning.com"),
                         ("Evidently AI Blog", "https://www.evidentlyai.com/blog")],
    "Mathematics for AI":[("3Blue1Brown – Linear Algebra", "https://www.3blue1brown.com/topics/linear-algebra"),
                           ("Khan Academy – Statistics", "https://www.khanacademy.org/math/statistics-probability"),
                           ("Mathematics for ML Book", "https://mml-book.github.io"),
                           ("Distill.pub", "https://distill.pub")],
}


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-deep:        #070B14;
    --bg-mid:         #0D1424;
    --bg-card:        #111827;
    --bg-input:       #1a2236;
    --border:         #1e2d45;
    --accent:         #3b82f6;
    --accent2:        #06b6d4;
    --accent-glow:    #3b82f618;
    --text-primary:   #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted:     #475569;
    --success:        #10b981;
    --warning:        #f59e0b;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stMainBlockContainer"] {
    padding: 1rem 1.2rem 2rem !important;
    max-width: 100% !important;
}

/* Left sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-mid) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebarContent"] { padding: 1.1rem 0.85rem !important; }

/* Buttons */
.stButton > button {
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    text-align: left !important;
    padding: 7px 11px !important;
}
.stButton > button:hover {
    background: var(--accent-glow) !important;
    border-color: var(--accent) !important;
    color: var(--text-primary) !important;
    transform: translateX(2px) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* Textarea */
.stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

hr { border-color: var(--border) !important; margin: 9px 0 !important; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* Hero */
.hero-wrapper {
    background: linear-gradient(135deg, var(--bg-mid) 0%, #0a1628 100%);
    border: 1px solid var(--border); border-radius: 14px;
    padding: 20px 26px 16px; margin-bottom: 16px;
    position: relative; overflow: hidden;
}
.hero-wrapper::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 170px; height: 170px;
    background: radial-gradient(circle, #3b82f625, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 22px; font-weight: 700; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #f1f5f9 40%, var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 3px 0;
}
.hero-sub { color: var(--text-secondary); font-size: 12.5px; margin: 0; }
.status-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #10b98112; border: 1px solid #10b98126;
    border-radius: 20px; padding: 3px 10px;
    font-size: 11.5px; font-weight: 500; color: var(--success); margin-top: 9px;
}
.status-dot {
    width: 6px; height: 6px; background: var(--success);
    border-radius: 50%; animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* Messages */
.msg-user {
    display: flex; justify-content: flex-end;
    margin: 9px 0; animation: fadeUp .28s ease;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #1d4ed8, #2563eb); color: #fff;
    padding: 10px 15px; border-radius: 16px 16px 4px 16px;
    max-width: 80%; font-size: 13.5px; line-height: 1.6;
    box-shadow: 0 4px 14px #2563eb20;
}
.msg-bot { display: flex; align-items: flex-start; gap: 9px; margin: 9px 0; animation: fadeUp .28s ease; }
.bot-avatar {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 9px; display: flex; align-items: center;
    justify-content: center; font-size: 14px; flex-shrink: 0;
    box-shadow: 0 3px 10px #3b82f625;
}
.msg-bot .bubble {
    background: var(--bg-card); border: 1px solid var(--border);
    color: var(--text-primary); padding: 11px 15px;
    border-radius: 4px 16px 16px 16px;
    max-width: 86%; font-size: 13.5px; line-height: 1.7;
}
.msg-timestamp { font-size: 10px; color: var(--text-muted); margin-top: 3px; }
@keyframes fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

/* Quick prompts */
.quick-title {
    font-size: 11px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
}

/* Right taskbar */
.taskbar-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 11px; padding: 13px; margin-bottom: 10px;
}
.taskbar-title {
    font-size: 10.5px; font-weight: 700; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px;
}
.roadmap-item {
    display: flex; align-items: center; gap: 7px;
    padding: 6px 7px; border-radius: 7px; margin-bottom: 3px;
    font-size: 12px; color: var(--text-secondary);
    border: 1px solid transparent; transition: all .18s;
}
.roadmap-item:hover { background: var(--accent-glow); border-color: var(--border); color: var(--text-primary); }
.roadmap-item.done { color: var(--success); text-decoration: line-through; opacity: .65; }
.roadmap-num {
    width: 18px; height: 18px; border-radius: 50%;
    background: var(--bg-input); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 9px; color: var(--text-muted); flex-shrink: 0;
}
.roadmap-num.done { background: var(--success); color: #fff; border-color: var(--success); }
.resource-link {
    display: block; padding: 7px 9px;
    background: var(--bg-input); border: 1px solid var(--border);
    border-radius: 7px; margin-bottom: 5px;
    font-size: 11.5px; color: var(--accent2);
    text-decoration: none; transition: all .18s;
}
.resource-link:hover { border-color: var(--accent); background: var(--accent-glow); }
.stat-row { display: flex; gap: 6px; margin-bottom: 6px; }
.stat-box {
    flex: 1; background: var(--bg-input); border: 1px solid var(--border);
    border-radius: 8px; padding: 7px 8px; text-align: center;
}
.stat-val { font-size: 19px; font-weight: 700; color: var(--accent); }
.stat-lbl { font-size: 9.5px; color: var(--text-muted); margin-top: 1px; }
.bookmark-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 6px 7px; background: var(--bg-input);
    border: 1px solid var(--border); border-radius: 7px; margin-bottom: 4px;
    font-size: 11px; color: var(--text-secondary);
}
.sidebar-label {
    font-size: 10.5px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 1.2px; margin: 12px 0 7px 0;
}
.sidebar-model-badge {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 7px; padding: 7px 9px; font-size: 10.5px;
    color: var(--text-secondary); font-family: 'JetBrains Mono', monospace;
    word-break: break-all;
}
.empty-state { text-align: center; padding: 28px 10px; color: var(--text-muted); }
.empty-icon  { font-size: 36px; margin-bottom: 8px; }

/* Taskbar section header with colored left border */
.tb-section {
    border-left: 3px solid var(--accent);
    padding-left: 8px; margin-bottom: 10px;
    font-size: 13px; font-weight: 600; color: var(--text-primary);
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:9px;margin-bottom:4px;">
        <div style="width:32px;height:32px;background:linear-gradient(135deg,#3b82f6,#06b6d4);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">🧠</div>
        <div>
            <div style="font-weight:700;font-size:14.5px;color:#f1f5f9;">NeuralTutor</div>
            <div style="font-size:10px;color:#475569;">AI/ML Learning Assistant</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Learning Focus</div>', unsafe_allow_html=True)
    topic = st.selectbox("topic", list(TOPIC_PROMPTS.keys()),
                         label_visibility="collapsed",
                         index=list(TOPIC_PROMPTS.keys()).index(st.session_state.topic_filter))
    st.session_state.topic_filter = topic

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("＋  New Conversation", use_container_width=True):
        chat_id = str(uuid.uuid4())
        st.session_state.chats[chat_id] = []
        st.session_state.chat_titles[chat_id] = "New Conversation"
        st.session_state.current_chat = chat_id
        st.rerun()

    st.markdown('<div class="sidebar-label">Conversations</div>', unsafe_allow_html=True)
    for chat_id, _ in reversed(list(st.session_state.chats.items())):
        title = st.session_state.chat_titles.get(chat_id, "New Conversation")
        icon  = "▶ " if chat_id == st.session_state.current_chat else "💬 "
        label = icon + (title[:19] + "…" if len(title) > 19 else title)
        col_b, col_d = st.columns([5, 1])
        with col_b:
            if st.button(label, key=f"chat_{chat_id}", use_container_width=True):
                st.session_state.current_chat = chat_id
                st.rerun()
        with col_d:
            if len(st.session_state.chats) > 1 and st.button("✕", key=f"del_{chat_id}"):
                del st.session_state.chats[chat_id]
                del st.session_state.chat_titles[chat_id]
                st.session_state.current_chat = list(st.session_state.chats.keys())[-1]
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Active Model</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-model-badge">⚡ {model_display}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#334155;text-align:center;">Powered by Groq · NeuralTutor v2.0</div>', unsafe_allow_html=True)


chat_col, taskbar_col = st.columns([2.5, 1], gap="medium")
messages = st.session_state.chats[st.session_state.current_chat]


with chat_col:
    st.markdown(f"""
    <div class="hero-wrapper">
        <p class="hero-title">🧠 NeuralTutor</p>
        <p class="hero-sub">Your intelligent guide to Artificial Intelligence & Machine Learning</p>
        <div class="status-badge">
            <span class="status-dot"></span>
            {topic} · {model_display}
        </div>
    </div>""", unsafe_allow_html=True)

    
    if not messages:
        st.markdown('<div class="quick-title">✦ Try a quick question</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, (qlabel, prompt) in enumerate(QUICK_PROMPTS.items()):
            with cols[idx % 2]:
                if st.button(qlabel, key=f"quick_{idx}", use_container_width=True):
                    now = datetime.now().strftime("%H:%M")
                    messages.append({"role": "user", "content": prompt, "time": now})
                    sys_p = TOPIC_PROMPTS.get(topic, TOPIC_PROMPTS["General AI/ML"])
                    api_m = [{"role": "system", "content": sys_p}] + [{"role": m["role"], "content": m["content"]} for m in messages]
                    try:
                        r = client.chat.completions.create(model=st.session_state.model, messages=api_m, max_tokens=1500)
                        reply = r.choices[0].message.content
                    except Exception as e:
                        reply = f"⚠️ Error: {str(e)}"
                    messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%H:%M")})
                    st.session_state.chat_titles[st.session_state.current_chat] = qlabel
                    st.session_state.total_messages += 1
                    st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)

    
    if not messages:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">💡</div>
            <div style="font-size:13.5px;">Ask me anything about AI, ML, Deep Learning, or Data Science.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in messages:
            ts = msg.get("time", "")
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div>
                        <div class="bubble">{msg["content"]}</div>
                        <div class="msg-timestamp" style="text-align:right">{ts}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                content = msg["content"].replace("\n", "<br>")
                st.markdown(f"""
                <div class="msg-bot">
                    <div class="bot-avatar">🤖</div>
                    <div>
                        <div class="bubble">{content}</div>
                        <div class="msg-timestamp">NeuralTutor · {ts}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    
    user_input = st.chat_input(f"Ask about {topic}…")
    if user_input:
        now = datetime.now().strftime("%H:%M")
        messages.append({"role": "user", "content": user_input, "time": now})
        if st.session_state.chat_titles.get(st.session_state.current_chat) == "New Conversation":
            st.session_state.chat_titles[st.session_state.current_chat] = user_input[:28]
        sys_p = TOPIC_PROMPTS.get(topic, TOPIC_PROMPTS["General AI/ML"])
        api_m = [{"role": "system", "content": sys_p}] + [{"role": m["role"], "content": m["content"]} for m in messages]
        try:
            if not st.session_state.model:
                raise Exception("No model available.")
            r = client.chat.completions.create(model=st.session_state.model, messages=api_m, max_tokens=1500, temperature=0.7)
            reply = r.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ **Error:** {str(e)}"
        messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%H:%M")})
        st.session_state.total_messages += 1
        st.rerun()


with taskbar_col:

    
    completed = len(st.session_state.completed_topics)
    total_mods = len(ROADMAPS.get(topic, []))
    pct = int((completed / total_mods) * 100) if total_mods else 0

    st.markdown(f"""
    <div class="taskbar-card">
        <div class="taskbar-title">📊 Your Progress</div>
        <div class="stat-row">
            <div class="stat-box">
                <div class="stat-val">{st.session_state.total_messages}</div>
                <div class="stat-lbl">Queries</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{completed}</div>
                <div class="stat-lbl">Done</div>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-box">
                <div class="stat-val">{len(st.session_state.chats)}</div>
                <div class="stat-lbl">Sessions</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{pct}%</div>
                <div class="stat-lbl">Progress</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    
    t1, t2, t3, t4 = st.columns(4)
    tab_map = {"roadmap": t1, "resources": t2, "notes": t3, "bookmarks": t4}
    tab_labels = {"roadmap": "🗺️", "resources": "📚", "notes": "📝", "bookmarks": "🔖"}
    for tab_key, col in tab_map.items():
        with col:
            active_style = "border-color: #3b82f6 !important; color: #3b82f6 !important;" if st.session_state.active_tab == tab_key else ""
            if st.button(tab_labels[tab_key], key=f"tab_{tab_key}", use_container_width=True):
                st.session_state.active_tab = tab_key
                st.rerun()

    active_tab = st.session_state.active_tab

    
    if active_tab == "roadmap":
        st.markdown(f'<div class="tb-section">📍 {topic}</div>', unsafe_allow_html=True)
        roadmap = ROADMAPS.get(topic, [])
        for i, (step, icon) in enumerate(roadmap):
            done = step in st.session_state.completed_topics
            d_cls = "done" if done else ""
            n_cls = "done" if done else ""
            num   = "✓" if done else str(i + 1)
            st.markdown(f"""
            <div class="roadmap-item {d_cls}">
                <div class="roadmap-num {n_cls}">{num}</div>
                <span>{icon} {step}</span>
            </div>""", unsafe_allow_html=True)

        remaining = [s for s, _ in roadmap if s not in st.session_state.completed_topics]
        if remaining:
            sel = st.selectbox("Mark complete", remaining, key="mark_done", label_visibility="collapsed")
            if st.button("✅ Mark as Done", use_container_width=True):
                st.session_state.completed_topics.append(sel)
                st.rerun()
        else:
            st.markdown('<div style="text-align:center;color:#10b981;font-size:12px;padding:8px;background:#10b98110;border-radius:8px;border:1px solid #10b98125;">🎉 Roadmap complete!</div>', unsafe_allow_html=True)

        if st.button("🔄 Reset Progress", use_container_width=True):
            st.session_state.completed_topics = []
            st.rerun()

    
    elif active_tab == "resources":
        st.markdown(f'<div class="tb-section">📚 {topic}</div>', unsafe_allow_html=True)
        for name, url in RESOURCES.get(topic, []):
            st.markdown(f'<a class="resource-link" href="{url}" target="_blank">🔗 {name}</a>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;color:#475569;margin-bottom:6px;">💬 Ask tutor for more</div>', unsafe_allow_html=True)
        if st.button("🔍 Recommend resources", use_container_width=True):
            prompt = f"Recommend the top 3 free resources for learning {topic} as a beginner, with brief descriptions."
            messages.append({"role": "user", "content": prompt, "time": datetime.now().strftime("%H:%M")})
            st.session_state.chat_titles[st.session_state.current_chat] = f"Resources for {topic}"
            st.rerun()

    
    elif active_tab == "notes":
        st.markdown('<div class="tb-section">📝 Study Notes</div>', unsafe_allow_html=True)
        notes_val = st.text_area(
            "notes", value=st.session_state.notes,
            placeholder="Jot down key concepts, formulas, or insights…",
            height=200, label_visibility="collapsed", key="notes_area"
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save", use_container_width=True):
                st.session_state.notes = notes_val
                st.success("Saved!")
        with c2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.notes = ""
                st.rerun()

        if st.session_state.notes.strip():
            if st.button("🤖 Summarize notes", use_container_width=True):
                prompt = f"Please summarize and organize these study notes for me:\n\n{st.session_state.notes}"
                messages.append({"role": "user", "content": prompt, "time": datetime.now().strftime("%H:%M")})
                st.rerun()

    
    elif active_tab == "bookmarks":
        st.markdown('<div class="tb-section">🔖 Saved Replies</div>', unsafe_allow_html=True)
        last_bot = next((m["content"] for m in reversed(messages) if m["role"] == "assistant"), None)
        if last_bot:
            if st.button("🔖 Bookmark last reply", use_container_width=True):
                snippet = last_bot[:90] + ("…" if len(last_bot) > 90 else "")
                if snippet not in st.session_state.bookmarks:
                    st.session_state.bookmarks.append(snippet)
                    st.success("Bookmarked!")
                    st.rerun()

        if st.session_state.bookmarks:
            for i, bm in enumerate(st.session_state.bookmarks):
                st.markdown(f'<div class="bookmark-item"><span style="flex:1;font-size:10.5px;">{bm}</span></div>', unsafe_allow_html=True)
                if st.button("✕", key=f"delbm_{i}"):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()
        else:
            st.markdown('<div style="text-align:center;color:#475569;font-size:11.5px;padding:14px 0;">No bookmarks yet.<br>Save useful AI replies here!</div>', unsafe_allow_html=True)

    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<div class="tb-section">⚡ Quick Ask</div>', unsafe_allow_html=True)
    quick_asks = {
        "📌 Key concepts":  f"What are the 5 most important concepts in {topic}?",
        "🧪 Practice problem": f"Give me a hands-on problem for {topic} with a solution.",
        "📋 30-day plan":   f"Create a 30-day study plan for mastering {topic}.",
    }
    for btn_lbl, p_text in quick_asks.items():
        if st.button(btn_lbl, key=f"qa_{btn_lbl}", use_container_width=True):
            messages.append({"role": "user", "content": p_text, "time": datetime.now().strftime("%H:%M")})
            st.session_state.chat_titles[st.session_state.current_chat] = btn_lbl
            st.rerun()
