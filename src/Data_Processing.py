import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger('data-processor')

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise e
def preprocess_data(data):
    try:
        data.dropna(inplace=True)
        data['total_rooms'] = data['Bathrooms'] + data['Bedrooms']
        data = data.drop(['Bathrooms','Bedrooms'],axis=1)
        data['PrivateGarden'] = data['PrivateGarden'].map({'Yes':1,'No':0})
        data['price'] = data['price'].replace(r'[^\d]','',regex = True).astype(float)
        data = pd.get_dummies(data)
        data = data.drop(['Payment_Cash','Ownership_Resale', 'Status_Ready'], axis=1)
        data.to_csv('data/ProcessedData.csv', index = False)
        logger.info("Data preprocessing completed successfully")
        return data
    except Exception as e:
        logger.error(f"Error during data preprocessing: {e}")
        raise e
if __name__ == "__main__":
    data_file_path = Path('data/Apartments.csv')
    data = load_data(data_file_path)
    preprocess_data(data)

