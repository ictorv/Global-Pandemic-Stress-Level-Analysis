import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Wellness Analytics",
    page_icon="🌸",
    layout="wide"
)

st.markdown("""
    <style>
    /* Main container styling with elegant gradient */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        min-height: 100vh;
        background-attachment: fixed;
    }
    
    /* Elegant container styling */
    .css-1d391kg {
        background: linear-gradient(to right, #fff5f5, #fff8f8);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    /* Custom radio button styling */
    .stRadio > label {
        font-weight: 500;
        color: #5d576b;
        font-family: 'Quicksand', sans-serif;
    }
    
    .stRadio > div {
        display: flex;
        gap: 12px;
        margin-top: 8px;
    }
    
    .stRadio > div > label {
        background: linear-gradient(135deg, #faf9f9, #fff);
        padding: 10px 20px;
        border: 2px solid #e9e4f0;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        min-width: 80px;
        text-align: center;
        font-size: 0.95em;
        color: #5d576b;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stRadio > div > label:hover {
        border-color: #b8a9c6;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Predict button styling */
    .stButton > button {
        background: linear-gradient(135deg, #c2a5d9, #a691ce);
        color: white;
        padding: 15px 30px;
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(166, 145, 206, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.1em;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #a691ce, #c2a5d9);
        box-shadow: 0 6px 20px rgba(166, 145, 206, 0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #fff5f5, #faf0ff);
        padding: 25px;
        border-radius: 20px;
    }
    
    /* Header styling */
    h1 {
        font-family: 'Quicksand', sans-serif;
        background: linear-gradient(135deg, #5d576b, #a691ce);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        font-size: 2.3em;
        letter-spacing: 1px;
    }
    
    /* Input field styling */
    .stNumberInput > div > div > input {
        background: #fff;
        border: 2px solid #e9e4f0;
        border-radius: 12px;
        color: #5d576b;
        padding: 10px 15px;
        transition: all 0.3s ease;
        font-family: 'Quicksand', sans-serif;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #a691ce;
        box-shadow: 0 0 15px rgba(166, 145, 206, 0.2);
    }
    
    /* DataFrame styling */
    div[data-testid="stDataFrame"] {
        background: #fff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e9e4f0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f5f5f5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #c2a5d9, #a691ce);
        border-radius: 4px;
    }
    
    /* Success message styling */
    .element-container div[data-testid="stMarkdownContainer"] div.success {
        background-color: #f0f7f4;
        border-left: 5px solid #7fb9a2;
        color: #2c584a;
        padding: 1em;
        border-radius: 0 10px 10px 0;
    }
    
    /* Warning message styling */
    .element-container div[data-testid="stMarkdownContainer"] div.warning {
        background-color: #fff8f0;
        border-left: 5px solid #f0b775;
        color: #8b5e2b;
        padding: 1em;
        border-radius: 0 10px 10px 0;
    }
    
    /* Error message styling */
    .element-container div[data-testid="stMarkdownContainer"] div.error {
        background-color: #fdf0f0;
        border-left: 5px solid #e6a0a0;
        color: #8b2b2b;
        padding: 1em;
        border-radius: 0 10px 10px 0;
    }
    
    /* Card container styling */
    .card {
        background: #fff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9e4f0;
    }
    
    /* Animated background pattern */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23a691ce' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
        z-index: -1;
    }
    </style>
    
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_models():
    """
    Load all models and preprocessors at once using Streamlit's caching.
    Returns a dictionary containing all loaded objects.
    """
    model_paths = {
        'rfc': './objects/rfc.pkl',
        'poly2': './objects/poly2.pkl',
        'scaler': './objects/scaler.pkl',
        'scaler2': './objects/scaler2.pkl',
        'enc': './objects/enc.pkl'
    }
    
    models = {}
    for name, path in model_paths.items():
        with open(path, 'rb') as file:
            models[name] = pickle.load(file)
    
    return models

# Load all models at once using the cached function
models = load_models()

model = models['rfc']
poly = models['poly2']
scaler = models['scaler']
scaler1 = models['scaler2']
enc = models['enc']

# Define feature names and binary features
feature_names = [
    'Increased_Work_Hours', 'Work_From_Home', 'Hours_Worked_Per_Day',
    'Meetings_Per_Day', 'Productivity_Change', 'Health_Issue', 'Job_Security',
    'Childcare_Responsibilities', 'Commuting_Changes', 'Technology_Adaptation',
    'Salary_Changes', 'Team_Collaboration_Challenges'
]

binary_features = [
    'Increased_Work_Hours', 'Work_From_Home', 'Productivity_Change', 
    'Health_Issue', 'Job_Security', 'Childcare_Responsibilities', 
    'Commuting_Changes', 'Technology_Adaptation', 'Salary_Changes', 
    'Team_Collaboration_Challenges'
]

# Title
st.markdown("""
    <h1>🧠 Global Pandemic Stress Level Analysis</h1>
    <div style='text-align: center; padding: 20px; margin-bottom: 30px; background-color: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
        <p style='color: #666; font-size: 1.1em;'>
            Analyze workplace stress levels during the pandemic based on various factors.
            Enter your information in the sidebar to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for input
st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px; margin-bottom: 20px; background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%); border-radius: 8px;'>
        <h2 style='color: white; font-size: 1.5em; margin: 0;'>Input Features</h2>
    </div>
    """, unsafe_allow_html=True)

def user_input_features():
    data = {}
    for feature in feature_names:
        label = feature.replace('_', ' ').title()
        if feature in ['Hours_Worked_Per_Day', 'Meetings_Per_Day']:
            data[feature] = st.sidebar.number_input(
                label,
                min_value=0.0,
                max_value=24.0 if feature == 'Hours_Worked_Per_Day' else 20.0,
                value=0.0,
                help=f"Enter your {label.lower()}"
            )
        elif feature in binary_features:
            # Convert Yes/No to 1/0
            response = st.sidebar.radio(
                label,
                options=["No", "Yes"],
                help=f"Select Yes or No for {label.lower()}",
                horizontal=True  # Make radio buttons horizontal
            )
            data[feature] = 1 if response == "Yes" else 0
        else:
            data[feature] = st.sidebar.number_input(
                label,
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                help=f"Enter value between 0 and 1 for {label.lower()}"
            )
    return pd.DataFrame([data])

input_df = user_input_features()
sector = st.sidebar.selectbox(
    'Sector', 
    ['Education', 'Healthcare', 'IT', 'Retail'],
    help="Select your sector"
)
input_df['Sector'] = sector

# Show inpu
st.markdown("""
    <div style='margin-bottom: 30px;'>
        <h3 style='color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;'>
            📊 User Input Features
        </h3>
    </div>
    """, unsafe_allow_html=True)
st.write(input_df)

# Prediction section
if st.button("Predict Stress Level"):
    with st.spinner('Analyzing stress levels...'):
        # Apply Scaling
        df = enc.transform(input_df[['Sector']])
        
        # Convert the transformed array into a DataFrame with appropriate column names
        df = pd.DataFrame(df, columns=enc.get_feature_names_out(['Sector']))
        input_df = pd.concat([input_df,df], axis=1)
        input_df = input_df.drop('Sector', axis=1)
        
        input_df['Work_Hours_Interaction'] = input_df['Increased_Work_Hours'] * input_df['Work_From_Home']
        
        # Transform and predict
        transformed_input = poly.transform(input_df)
        prediction = model.predict(transformed_input)
        prediction_proba = model.predict_proba(transformed_input)

        # Display results in containers
        st.markdown("""
            <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 30px;'>
                <h3 style='color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;'>
                    🎯 Prediction Results
                </h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Show prediction with appropriate styling
        if prediction[0] == 3:
            st.error(f"Predicted Stress Level: High (Class {prediction[0]})")
        elif prediction[0] == 2:
            st.warning(f"Predicted Stress Level: Medium (Class {prediction[0]})")
        elif prediction[0] == 1:
            st.success(f"Predicted Stress Level: Low (Class {prediction[0]})")
            
        st.markdown("""
            <h3 style='color: #2c3e50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; margin-top: 20px;'>
                📊 Prediction Probabilities
            </h3>
            """, unsafe_allow_html=True)
            
        proba_df = pd.DataFrame(
            prediction_proba,
            columns=[f"Class {c}" for c in model.classes_]
        )
        st.write(proba_df)

        # Add interpretation
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;'>
                <p style='color: #666; margin: 0;'>
                    Class 1 represents low stress levels, Class 2 represents medium stress levels while Class 3 represents high stress levels.
                    The probabilities indicate the likelihood of belonging to each class.
                </p>
            </div>
            """, unsafe_allow_html=True)

# Hide Streamlit's footer
st.markdown("""
    <style>
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
