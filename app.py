import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Pandemic Stress Analysis",
    page_icon="🧠",
    layout="wide"
)

# Enhanced CSS styling with beautiful buttons
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 20px;
        background-color: #f8f9fa;
    }
    
    /* Custom radio button styling */
    .stRadio > label {
        font-weight: 500;
        color: #2c3e50;
    }
    
    .stRadio > div {
        display: flex;
        gap: 10px;
        margin-top: 5px;
    }
    
    .stRadio > div > label {
        background-color: #ffffff;
        padding: 10px 20px;
        border: 2px solid #e0e0e0;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        min-width: 80px;
        text-align: center;
    }
    
    .stRadio > div > label:hover {
        border-color: #4CAF50;
        box-shadow: 0 2px 5px rgba(76, 175, 80, 0.2);
    }
    
    .stRadio > div [data-baseweb="radio"]:checked + label {
        background-color: #4CAF50;
        color: white;
        border-color: #4CAF50;
        box-shadow: 0 2px 5px rgba(76, 175, 80, 0.3);
    }
    
    /* Predict button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 15px 30px;
        border-radius: 25px;
        border: none;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.1em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #45a049, #4CAF50);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
    }
    
    /* Container styling */
    .css-1d391kg {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
    }
    
    /* Header styling */
    h1 {
        color: #1f4287;
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
    }
    
    .stSubheader {
        color: #2c3e50;
        font-weight: 600;
        padding: 10px 0;
        border-bottom: 2px solid #4CAF50;
        margin-bottom: 20px;
    }
    
    /* Input field styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 8px 12px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* DataFrame styling */
    div[data-testid="stDataFrame"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# [Rest of the code remains exactly the same as in the previous version, starting from here]
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

# Replace individual model references with dictionary access
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

# Title with emoji and description
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

# Show input with styled container
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

        # Display results in styled containers
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