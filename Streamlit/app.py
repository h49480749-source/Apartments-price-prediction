import streamlit as st
import requests

st.title("Price prediction for Apartments in mountain view Icity compound in New Cairo")

st.image("images/Banner.webp", width='stretch')

st.write("Enter apartment details")

area = st.number_input('Area-sqm',min_value=100, step=1)
Bedrooms = st.number_input('Number of Bedrooms',min_value=2, step=1)
Bathrooms = st.number_input('Number of Bathrooms',min_value=2, step=1)
PrivateGarden = st.selectbox('Private Garden', ['No','Yes'])
Payment = st.selectbox('Payment Method', ['Cash', 'Cash or Installment', 'Installment'])
Ownership = st.selectbox('Ownership', ['Resale', 'Primary'])
Status = st.selectbox('Status', ['Ready', 'Off-plan'])

if st.button('Predict Price'):
    data = {
        "Area": area,
        "PrivateGarden": PrivateGarden,
        "Bedrooms": Bedrooms,
        "Bathrooms": Bathrooms,
        "Payment": Payment,
        "Ownership": Ownership,
        "Status": Status
    }
    
    response = requests.post("http://api:8000/predict", json=data)
    
    if response.status_code == 200:
        prediction = response.json()
        st.success(f"Predicted Price: {prediction['predicted_price']:.2f} EGP")
    else:
        st.error("Error in prediction request")




