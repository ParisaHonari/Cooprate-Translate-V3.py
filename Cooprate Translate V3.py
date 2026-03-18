import streamlit as st
import os
from openai import OpenAI

# 🔑 API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ⚙️ Page
st.set_page_config(page_title="Corporate BS Translator 😏", layout="wide")

# 🎨 STYLE
st.markdown("""
<style>

/* Layout */
.block-container {
    max-width: 900px;
    margin: auto;
    padding-top: 1rem;
}

/* Text area */
textarea {
    border-radius: 12px !important;
    border: 1px solid #ddd !important;
    padding: 14px !important;
    font-size: 16px !important;
}

/* Buttons */
.stButton>button {
    border-radius: 20px;
    background-color: #E87C72;
    color: white;
    font-weight: 600;
    padding: 14px;
    font-size: 16px;
    border: none;
}

.stButton>button:hover {
    background-color: #d96b61;
    color: white;
}

/* Card */
.card {
    background-color: #F9F4F3;
    padding: 20px;
    border-radius: 14px;
    border-left: 5px solid #E87C72;
    margin-bottom: 18px;
}

</style>
""", unsafe_allow_html=True)

# 🧠 HEADER
st.markdown("""
<h1 style='text-align:center; color:#E87C72;'>😏 Corporate BS Translator</h1>
<p style='text-align:center; font-size:18px; color:#444;'>
Say it better — or translate what they really meant.
</p>
<p style='text-align:center; font-weight:600; color:#E87C72;'>
Built by Parisa Honari ✨
</p>
""", unsafe_allow_html=True)

# ✍️ INPUT
st.markdown("<h3 style='text-align:center;'>✍️ Paste your message below</h3>", unsafe_allow_html=True)
user_input = st.text_area("", height=150)

# 🎯 BUTTONS
mode = None
col1, col2, col3 = st.columns([1,2,1])

with col2:
    b1, b2 = st.columns(2)

    with b1:
        if st.button("✨ Polish it", use_container_width=True):
            mode = "polish"

    with b2:
        if st.button("😏 Translate the BS", use_container_width=True):
            mode = "translate"

# 🚀 RUN
if mode and user_input:

    prompt = f"""
You are a sharp, witty, elegant professional woman.

TONE:
- Smart, observant, slightly sarcastic
- Clean, confident, human

-------------------

IF MODE = "translate":

Return EXACTLY in this format:

### 💭 What they said
...

### 🧠 What they actually mean
...

### 💅 Translation
...

-------------------

IF MODE = "polish":

Return EXACTLY in this format:

### 🧾 HR-Safe Version
...

### ✨ Strategic Glow-Up
...

### 😈 Savage Version
...

-------------------

RULES:
- Keep workplace appropriate
- No insults
- Make it witty but smart

Mode: {mode}
Input: "{user_input}"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    st.divider()
    st.subheader("✨ Result")

    # 🧠 SPLIT INTO SECTIONS
    sections = result.split("###")

    for sec in sections:
        if sec.strip():
            parts = sec.strip().split("\n", 1)
            title = parts[0]
            content = parts[1] if len(parts) > 1 else ""

            st.markdown(f"""
<div class="card">
<b>{title}</b><br><br>
{content}
</div>
""", unsafe_allow_html=True)

            # 📋 Copy button
            st.code(content, language="markdown")

elif mode and not user_input:
    st.warning("Please enter a message first 👀")

# ⚠️ DISCLAIMER (moved to bottom, cleaner + funny)
st.markdown("""
<br><br>
<hr>
<p style='text-align:center; font-size:13px; color:gray;'>
⚠️ Disclaimer: This tool is for entertainment, humor, and a touch of sarcasm.  
It translates what people *might* mean — not what you should actually say in a meeting.  

Use at your own risk. If you paste this into an email and hit send, that’s between you, your boss, and HR 😏
</p>
""", unsafe_allow_html=True)
