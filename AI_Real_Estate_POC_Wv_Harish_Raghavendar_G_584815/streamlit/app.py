import pandas as pd
import streamlit as st
import pickle
import plotly.express as px

st.set_page_config(
    page_title="AI Real Estate Valuation",
    page_icon="🏠",
    layout="wide"
)

model = pickle.load(
    open("../output/house_price_model.pkl", "rb")
)

dataset = pd.read_csv(
    "../dataset/ultimate_housing_dataset.csv"
)

st.title("🏠 AI Based Real Estate Valuation System")

st.caption(
    "Professional Machine Learning Real Estate Analytics Platform"
)

left, right = st.columns(2)

with left:

    city = st.selectbox(
        "Select City",
        [
            "Bangalore",
            "Chennai",
            "Hyderabad",
            "Mumbai",
            "Delhi",
            "Pune"
        ]
    )

    area = st.slider(
        "Area (Sq.ft)",
        500,
        7000,
        1800
    )

    bedrooms = st.slider(
        "Bedrooms",
        1,
        6,
        3
    )

    bathrooms = st.slider(
        "Bathrooms",
        1,
        5,
        2
    )

with right:

    parking = st.selectbox(
        "Parking",
        ["Yes", "No"]
    )

    building_age = st.slider(
        "Building Age",
        0,
        30,
        5
    )

    near_metro = st.selectbox(
        "Near Metro",
        ["Yes", "No"]
    )

    gym = st.selectbox(
        "Gym",
        ["Yes", "No"]
    )

    pool = st.selectbox(
        "Swimming Pool",
        ["Yes", "No"]
    )

input_data = pd.DataFrame({

    "area_sqft": [area],
    "bedrooms": [bedrooms],
    "bathrooms": [bathrooms],

    "parking": [
        1 if parking == "Yes" else 0
    ],

    "building_age": [building_age],

    "near_metro": [
        1 if near_metro == "Yes" else 0
    ],

    "gym": [
        1 if gym == "Yes" else 0
    ],

    "pool": [
        1 if pool == "Yes" else 0
    ],

    "city_Chennai": [
        1 if city == "Chennai" else 0
    ],

    "city_Delhi": [
        1 if city == "Delhi" else 0
    ],

    "city_Hyderabad": [
        1 if city == "Hyderabad" else 0
    ],

    "city_Mumbai": [
        1 if city == "Mumbai" else 0
    ],

    "city_Pune": [
        1 if city == "Pune" else 0
    ]
})

if st.button("Predict Property Price"):

    prediction = model.predict(input_data)[0]

    st.success(
        f"Estimated Property Price: ₹ {round(prediction, 2):,}"
    )

st.markdown("---")

st.subheader("📊 Market Analytics Dashboard")

fig1 = px.histogram(
    dataset,
    x="price",
    color="city",
    title="Property Price Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = px.scatter(
    dataset,
    x="area_sqft",
    y="price",
    color="city",
    title="Area vs Price Analysis"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")

st.subheader("📈 Model Evaluation Metrics")

with open("../output/model_metrics.txt") as f:
    metrics = f.read()

st.code(metrics)
