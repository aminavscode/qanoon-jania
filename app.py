import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

# Load Environment Variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Legal AI Assistant & Document Simplifier",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Professional UI
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; margin-bottom: 0px; }
    .sub-title { font-size: 1rem; color: #4B5563; margin-bottom: 20px; }
    .stButton>button { width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-title">⚖️ Legal AI Assistant & Document Simplifier</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Automated Analysis for Legal Contracts, Agreements, Notices & Statutory Rights</div>', unsafe_allow_html=True)

# Sidebar Setup
st.sidebar.header("⚙️ System Settings")

# Provider Selection
provider = st.sidebar.selectbox("API Provider", ["Groq", "OpenAI"], index=0)

if provider == "Groq":
    # Defaulting to Groq API Key environment variable
    api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input("Groq API Key", type="password")
    model_name = st.sidebar.selectbox(
        "Model Architecture",
        [
            "openai/gpt-oss-120b",
            "llama-3.3-70b-versatile",
            "llama3-8b-8192",
            "mixtral-8x7b-32768"
        ],
        index=0
    )
else:
    api_key = os.getenv("OPENAI_API_KEY") or st.sidebar.text_input("OpenAI API Key", type="password")
    model_name = st.sidebar.selectbox(
        "Model Architecture",
        [
            "gpt-4o",
            "gpt-4o-mini",
            "o3-mini",
            "o1",
            "o1-mini"
        ],
        index=0
    )

# Professional Legal Disclaimer
st.sidebar.markdown("---")
st.sidebar.error("⚠️ **LEGAL DISCLAIMER**")
st.sidebar.caption(
    "This AI application provides automated text simplification and general educational legal guidance. "
    "It **does not constitute legal advice** and should not replace consultation with a qualified advocate or attorney. "
    "Always seek professional legal counsel before signing binding legal documents or pursuing statutory claims."
)

# Tabs Navigation
tab_simplify, tab_rights = st.tabs(["📄 Document Simplifier & Risk Analyzer", "🔍 Legal Rights Guidance"])

# TAB 1: Document Simplification & Risk Analysis
with tab_simplify:
    st.subheader("Contract & Document Analysis")
    
    legal_text = st.text_area(
        "Paste Legal Agreement, Rental Contract, NDA, or Notice:",
        height=240,
        placeholder="Paste document text here..."
    )
    
    col_lang, col_btn = st.columns([2, 1])
    with col_lang:
        language = st.radio("Output Language:", ["Urdu", "Roman Urdu", "English"], horizontal=True)
    
    if st.button("Analyze & Simplify Document", type="primary"):
        if not api_key:
            st.error("API Key missing! Please configure GROQ_API_KEY in .env file or enter it in the sidebar.")
        elif not legal_text.strip():
            st.warning("Please provide legal document text to analyze.")
        else:
            with st.spinner("Processing legal document..."):
                try:
                    system_prompt = f"""
                    You are an expert Legal AI Assistant specializing in contract breakdown, risk detection, and clause simplification.
                    Analyze the following legal document and provide structured output in {language}:

                    1. **Executive Summary**: Brief breakdown of what this document is.
                    2. **Core Obligations**: Key duties, liabilities, and payments required from the user.
                    3. **Critical Risk Factors & Penalties**: Hidden risks, high fines, unilateral termination clauses, or unfair conditions.
                    4. **Key Recommendations**: Essential advice before signing/accepting this agreement.
                    """

                    if provider == "Groq":
                        client = Groq(api_key=api_key)
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": legal_text}
                            ],
                            temperature=0.2
                        )
                    else:
                        client = OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": legal_text}
                            ],
                            temperature=0.2
                        )
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 📋 Analysis Report")
                    st.markdown(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

# TAB 2: Legal Rights Query
with tab_rights:
    st.subheader("Statutory & Rights Guidance")
    
    user_query = st.text_input(
        "Ask a legal inquiry (e.g., Tenant eviction laws, Workplace termination, Consumer complaints):",
        placeholder="Enter your query..."
    )
    
    query_lang = st.radio("Response Language:", ["Urdu", "Roman Urdu", "English"], key="query_lang", horizontal=True)
    
    if st.button("Get Legal Guidance"):
        if not api_key:
            st.error("API Key missing!")
        elif not user_query.strip():
            st.warning("Please enter a legal query.")
        else:
            with st.spinner("Evaluating legal query..."):
                try:
                    system_prompt = f"""
                    You are an authoritative Legal Assistant specializing in public legal awareness and consumer protection rights.
                    Provide clear, structured, and easy-to-understand legal guidance in {query_lang}.
                    
                    Include:
                    1. **Statutory Overview**: General principles of law governing this situation.
                    2. **User Rights**: Key entitlements and legal protections.
                    3. **Recommended Action Steps**: Practical steps to take legally.
                    """

                    if provider == "Groq":
                        client = Groq(api_key=api_key)
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_query}
                            ],
                            temperature=0.3
                        )
                    else:
                        client = OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_query}
                            ],
                            temperature=0.3
                        )

                    st.markdown("### ⚖️ Guidance Overview")
                    st.markdown(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")