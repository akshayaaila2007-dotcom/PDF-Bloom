import os
import hashlib

import streamlit as st
import chromadb

from google import genai
from dotenv import load_dotenv
from pypdf import PdfReader


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PDF Bloom",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       PAGE
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(201, 137, 130, 0.16),
                transparent 26%
            ),
            radial-gradient(
                circle at 92% 18%,
                rgba(224, 169, 126, 0.13),
                transparent 24%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(155, 112, 103, 0.08),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #211A1B 0%,
                #2A2021 48%,
                #1C1718 100%
            );

        color: #F7EDE5;
        min-height: 100vh;
    }


    .block-container {
        max-width: 1080px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .main-title {
        font-size: 48px;
        font-weight: 850;
        color: #FFF3E9;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }


    .subtitle {
        font-size: 18px;
        color: #D3BFB6;
        line-height: 1.65;
        margin-bottom: 35px;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1,
    h2,
    h3 {
        color: #FFF1E7 !important;
    }


    .stSubheader {
        color: #FFF1E7 !important;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p {
        color: #E3D2C9;
    }


    .stMarkdown {
        color: #E3D2C9;
    }


    .stCaption {
        color: #BCA8A0 !important;
    }


    /* ========================================================
       SECTION AREA
       ======================================================== */

    .section-title {
        font-size: 14px;
        font-weight: 800;
        color: #D99A82;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 12px;
        margin-bottom: 8px;
    }


    /* ========================================================
       UPLOAD AREA
       ======================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(52, 41, 40, 0.88);
        border: 1px solid #554240;
        border-radius: 20px;
        padding: 16px;

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.25);
    }


    [data-testid="stFileUploaderDropzone"] {
        background: #302525 !important;
        border: 2px dashed #B97872 !important;
        border-radius: 15px !important;
    }


    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #D9C8C0 !important;
    }


    [data-testid="stFileUploaderFileName"] {
        color: #FFF1E7 !important;
    }


    [data-testid="stFileUploader"] label {
        color: #F7EDE5 !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        width: 100%;

        background:
            linear-gradient(
                135deg,
                #B97872,
                #C98A72
            );

        color: #FFF9F5;

        border: none;
        border-radius: 14px;

        padding: 13px 20px;

        font-size: 15px;
        font-weight: 750;

        box-shadow:
            0 8px 20px rgba(185, 120, 114, 0.18);

        transition: all 0.2s ease;
    }


    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #C98982,
                #D39A7D
            );

        color: #FFFFFF;

        transform: translateY(-2px);

        box-shadow:
            0 12px 25px rgba(185, 120, 114, 0.25);
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    .stTextInput label {
        color: #F7EDE5 !important;
    }


    .stTextInput input {
        background: #292122 !important;

        color: #FFF1E7 !important;

        border: 1px solid #584744 !important;

        border-radius: 14px;

        padding: 14px;

        font-size: 15px;
    }


    .stTextInput input::placeholder {
        color: #95837D !important;
    }


    .stTextInput input:focus {
        border-color: #B97872 !important;

        box-shadow:
            0 0 0 2px
            rgba(185, 120, 114, 0.18);
    }


    /* ========================================================
       ANSWER
       ======================================================== */

    .answer-box {
        background:
            linear-gradient(
                135deg,
                #3A2B2C,
                #302526
            );

        border: 1px solid #5A4442;

        border-left: 5px solid #D19A72;

        border-radius: 16px;

        padding: 24px;

        margin-top: 12px;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.25);
    }


    .answer-box p {
        color: #F5E8DE !important;

        font-size: 16px;

        line-height: 1.8;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: rgba(47, 37, 37, 0.92);

        border: 1px solid #4D3D3B;

        border-radius: 15px;
    }


    [data-testid="stExpander"] summary {
        color: #F7EDE5 !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border: none;

        border-top:
            1px solid rgba(125, 100, 95, 0.35);

        margin: 35px 0;
    }


    /* ========================================================
       PROGRESS BAR
       ======================================================== */

    [data-testid="stProgressBar"] {
        background: #342928;
    }


    [data-testid="stProgressBar"] > div > div {
        background:
            linear-gradient(
                90deg,
                #A96F69,
                #D19A72
            );
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        color: #897771;

        font-size: 13px;

        margin-top: 50px;

        padding-top: 20px;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }


    ::-webkit-scrollbar-track {
        background: #1C1718;
    }


    ::-webkit-scrollbar-thumb {
        background: #584744;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "GEMINI_API_KEY is missing in your .env file."
    )
    st.stop()


# ============================================================
# GEMINI
# ============================================================

ai = genai.Client(
    api_key=api_key
)


# ============================================================
# CHROMADB
# ============================================================

db = chromadb.Client()

COLLECTION_NAME = "gemini_rag_collection"

collection = db.get_or_create_collection(
    COLLECTION_NAME
)


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    result = ai.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


# ============================================================
# READ PDF
# ============================================================

def read_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    pages = []

    for page in reader.pages:

        page_text = page.extract_text() or ""

        if page_text.strip():
            pages.append(page_text)

    return "\n".join(pages)


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(text):

    chunk_size = 1200
    overlap = 150

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ============================================================
# STORE CHUNKS
# ============================================================

def store_chunks(chunks):

    global collection

    try:
        db.delete_collection(
            COLLECTION_NAME
        )
    except Exception:
        pass

    collection = db.get_or_create_collection(
        COLLECTION_NAME
    )

    embeddings = []

    total = len(chunks)

    progress = st.progress(
        0,
        text="Preparing your PDF..."
    )

    for index, chunk in enumerate(chunks):

        embedding = create_embedding(
            chunk
        )

        embeddings.append(
            embedding
        )

        progress.progress(
            (index + 1) / total,
            text=(
                f"Preparing section "
                f"{index + 1} of {total}..."
            )
        )

    progress.empty()

    collection.add(
        ids=[
            str(i)
            for i in range(len(chunks))
        ],
        documents=chunks,
        embeddings=embeddings
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📖 PDF Bloom</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Read smarter. Ask questions. Find answers directly '
    'from your PDF.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">GET STARTED</div>',
    unsafe_allow_html=True
)

st.subheader("✨ How it works")

st.write(
    "Upload your PDF → Prepare the document → "
    "Ask a question → Gemini searches the relevant "
    "sections and creates an answer from your PDF."
)


# ============================================================
# UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">YOUR DOCUMENT</div>',
    unsafe_allow_html=True
)

st.subheader("📂 Upload your PDF")

st.caption(
    "Choose a PDF document you want to explore."
)

pdf = st.file_uploader(
    "PDF file",
    type=["pdf"],
    label_visibility="collapsed"
)


# ============================================================
# PROCESS PDF
# ============================================================

if pdf:

    pdf_hash = hashlib.md5(
        pdf.getvalue()
    ).hexdigest()

    already_processed = (
        st.session_state.get("pdf_hash")
        == pdf_hash
    )

    if already_processed:

        st.success(
            "✓ This PDF is already prepared. "
            "You can ask questions below."
        )

    if st.button(
        "✨ Prepare PDF",
        disabled=already_processed
    ):

        with st.spinner(
            "Reading your PDF..."
        ):

            text = read_pdf(pdf)

        if not text.strip():

            st.error(
                "I couldn't extract readable text "
                "from this PDF."
            )

        else:

            chunks = create_chunks(
                text
            )

            store_chunks(
                chunks
            )

            st.session_state.done = True

            st.session_state.pdf_hash = (
                pdf_hash
            )

            st.session_state.chunk_count = (
                len(chunks)
            )

            st.success(
                f"✨ Your PDF is ready! "
                f"{len(chunks)} sections were created."
            )


# ============================================================
# QUESTION AREA
# ============================================================

if st.session_state.get("done"):

    st.divider()

    st.markdown(
        '<div class="section-title">ASK YOUR DOCUMENT</div>',
        unsafe_allow_html=True
    )

    st.subheader("💬 Ask your PDF")

    st.caption(
        "Ask a question about the content "
        "of your uploaded document."
    )

    question = st.text_input(
        "Question",
        placeholder=(
            "Example: What is the main topic "
            "of this PDF?"
        ),
        label_visibility="collapsed"
    )

    ask = st.button(
        "🔎 Find Answer"
    )


    # ========================================================
    # SEARCH
    # ========================================================

    if ask:

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching your PDF..."
            ):

                question_embedding = (
                    create_embedding(
                        question
                    )
                )

                results = collection.query(
                    query_embeddings=[
                        question_embedding
                    ],
                    n_results=3
                )

                documents = (
                    results["documents"][0]
                )


            # =================================================
            # CONTEXT
            # =================================================

            context = "\n\n".join(
                documents
            )


            # =================================================
            # PROMPT
            # =================================================

            prompt = f"""
You are a PDF question-answering assistant.

Use ONLY the information provided in the
context below.

If the answer cannot be found in the
context, say:

"I could not find the answer in the uploaded document."

Do not use outside knowledge.

CONTEXT:
{context}

QUESTION:
{question}
"""


            # =================================================
            # GEMINI
            # =================================================

            with st.spinner(
                "Gemini is preparing your answer..."
            ):

                response = (
                    ai.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )
                )

                answer = response.text


            # =================================================
            # ANSWER
            # =================================================

            st.markdown(
                '<div class="section-title">'
                'RESULT'
                '</div>',
                unsafe_allow_html=True
            )

            st.subheader("📝 Answer")

            st.subheader("💡 Answer")

            st.write(answer)      


            # =================================================
            # SOURCES
            # =================================================

            with st.expander(
                "📚 View information used for this answer"
            ):

                for index, document in enumerate(
                    documents
                ):

                    st.markdown(
                        f"**Section {index + 1}**"
                    )

                    st.write(
                        document
                    )

                    if index < len(documents) - 1:
                        st.divider()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'Gemini AI • ChromaDB • Streamlit • PyPDF'
    '</div>',
    unsafe_allow_html=True
)