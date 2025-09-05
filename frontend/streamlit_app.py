import streamlit as st
import requests
import json
import io
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="PlantAI",
    page_icon="🌿",
    layout="wide",
)

# --- UI Layout based on Screenshots ---
st.markdown("""
    <style>
    .stApp > header {
        background-color: #fff;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 3rem;
    }
    .header-nav a {
        color: #4b5563;
        transition: color 0.3s;
        text-decoration: none;
    }
    .header-nav a:hover {
        color: #15803d;
    }
    .get-started-btn {
        background-color: #16a34a;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1-2px rgba(0, 0, 0, 0.06);
        transition: background-color 0.3s;
    }
    .get-started-btn:hover {
        background-color: #15803d;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem; font-weight: bold; color: #15803d;">🌿 PlantAI</span>
        </div>
        <nav style="display: flex; align-items: center; gap: 1.5rem;">
            <a href="#">Features</a>
            <a href="#">How It Works</a>
            <a href="#">Science</a>
        </nav>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <button style="border: none; background: none; color: #4b5563; cursor: pointer;">Sign In</button>
            <button class="get-started-btn">Get Started</button>
        </div>
    </div>
    <hr style="border: none; height: 1px; background-color: #e5e7eb;">
""", unsafe_allow_html=True)

# CSS for Hero and other sections
st.markdown("""
    <style>
    .big-title {
        font-size: 3rem;
        font-weight: 800;
        color: #1f2937;
        line-height: 1.25;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.125rem;
        color: #4b5563;
        margin-bottom: 2rem;
    }
    .stat-container {
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin-top: 2rem;
    }
    .stat-item {
        color: #1f2937;
    }
    .stat-number {
        font-size: 2.25rem;
        font-weight: 700;
    }
    .stat-text {
        color: #6b7280;
    }
    .feature-card {
        padding: 1.5rem;
        background-color: #fff;
        border-radius: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Main Hero Section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h1 class="big-title">Diagnose Plant Diseases<br>in Seconds</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload a photo, get instant AI-powered diagnosis and treatment recommendations. Empower your farming with cutting-edge technology.</p>', unsafe_allow_html=True)
    
    diagnosis_button = st.button("Try Diagnosis Now", key="try_diagnosis", use_container_width=True)
    learn_more_button = st.button("Learn How It Works", key="learn_more", use_container_width=True)

    st.markdown("""
        <div class="stat-container">
            <div class="stat-item">
                <div class="stat-number">95%+</div>
                <div class="stat-text">Accuracy Rate</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">50+</div>
                <div class="stat-text">Plant Types</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-text">Available</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<br>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a photo of your plant", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if diagnosis_button:
            # THIS IS THE KEY FIX.
            # We now explicitly define the file's name, content, and type in a tuple.
            # This ensures FastAPI receives the correct information and doesn't return a 400 error.
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            with st.spinner('Contacting AI Model...'):
                try:
                    response = requests.post("http://localhost:8000/predict/", files=files)
                    response.raise_for_status()
                    prediction_result = response.json()
                    
                    st.success("Diagnosis Complete!")
                    st.subheader(f"Diagnosis: {prediction_result['disease']}")
                    st.write(f"Confidence: **{prediction_result['confidence'] * 100:.0f}%**")
                    st.subheader("Treatment Plan")
                    st.markdown(prediction_result['treatment'])
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend server. Please make sure the backend is running.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
                except json.JSONDecodeError:
                    st.error("Failed to parse the response from the backend.")

# --- How It Works Section ---
st.markdown("<hr style='border: none; height: 1px; background-color: #e5e7eb;'>", unsafe_allow_html=True)
st.header("How It Works", divider='green')
st.markdown('<p class="text-center text-lg text-gray-600 mb-8">Get accurate plant disease diagnosis in three simple steps. Our AI technology makes plant health monitoring accessible to everyone.</p>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("1. Upload Photo")
    st.image("https://cdn-icons-png.flaticon.com/512/359/359281.png", use_column_width=True)
    st.write("Take a clear photo of the affected plant leaf or stem using your smartphone or camera.")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("2. AI Analysis")
    st.image("https://cdn-icons-png.flaticon.com/512/1005/1005141.png", use_column_width=True)
    st.write("Our advanced neural networks analyze the image and compare it against our extensive disease database.")
    st.markdown('</div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("3. Get Results")
    st.image("https://cdn-icons-png.flaticon.com/512/1005/1005187.png", use_column_width=True)
    st.write("Receive instant diagnosis with confidence scores, treatment recommendations, and prevention tips.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- The Science Behind Our Technology Section ---
st.markdown("<hr style='border: none; height: 1px; background-color: #e5e7eb;'>", unsafe_allow_html=True)
st.header("The Science Behind Our Technology", divider='green')
st.markdown('<p class="text-center text-lg text-gray-600 mb-8">Built on cutting-edge artificial intelligence and machine learning research, our platform delivers reliable plant disease diagnosis at scale.</p>', unsafe_allow_html=True)
col_stats = st.columns(4)
with col_stats[0]:
    st.markdown('<h3 class="text-xl font-bold text-center">500K+</h3><p class="text-center text-gray-600">Images Analyzed</p>', unsafe_allow_html=True)
with col_stats[1]:
    st.markdown('<h3 class="text-xl font-bold text-center">200+</h3><p class="text-center text-gray-600">Disease Types</p>', unsafe_allow_html=True)
with col_stats[2]:
    st.markdown('<h3 class="text-xl font-bold text-center">95%+</h3><p class="text-center text-gray-600">Accuracy Rate</p>', unsafe_allow_html=True)
with col_stats[3]:
    st.markdown('<h3 class="text-xl font-bold text-center">50+</h3><p class="text-center text-gray-600">Countries Served</p>', unsafe_allow_html=True)

col6, col7 = st.columns([1, 1])
with col6:
    st.subheader("Deep Learning")
    st.write("Convolutional Neural Networks (CNNs) trained on thousands of plant disease images for accurate pattern recognition.")
with col7:
    st.subheader("Transfer Learning")
    st.write("Advanced pre-trained models fine-tuned specifically for agricultural applications and plant pathology.")

# --- Ready to Transform Section ---
st.markdown("<hr style='border: none; height: 1px; background-color: #e5e7eb;'>", unsafe_allow_html=True)
st.markdown('<div style="background-color: #2e7d32; padding: 4rem; text-align: center; color: white; border-radius: 1.5rem;">', unsafe_allow_html=True)
st.markdown('<h2 style="font-size: 2.5rem; font-weight: bold;">Ready to Transform Your Farming?</h2>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.25rem;">Join thousands of farmers already using PlantAI to protect their crops. Start diagnosing plant diseases instantly with just a photo.</p>', unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)
col8, col9 = st.columns(2)
with col8:
    st.button("Try Web App Now →", key="web_app_btn", use_container_width=True)
with col9:
    st.button("Download Mobile App", key="mobile_app_btn", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer with features
st.markdown('<br>', unsafe_allow_html=True)
col10, col11, col12 = st.columns(3)
with col10:
    st.markdown('<h3 class="text-lg font-semibold">Free</h3><p class="text-gray-600">Basic diagnoses</p>', unsafe_allow_html=True)
with col11:
    st.markdown('<h3 class="text-lg font-semibold">Instant</h3><p class="text-gray-600">Results in seconds</p>', unsafe_allow_html=True)
with col12:
    st.markdown('<h3 class="text-lg font-semibold">Offline</h3><p class="text-gray-600">Works without internet</p>', unsafe_allow_html=True)