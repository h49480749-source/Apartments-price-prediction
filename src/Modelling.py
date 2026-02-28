from sklearn.model_selection import train_test_split, cross_validate, KFold , cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import mlflow
import joblib
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger('Model-Building')

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise e

def modelling(data):
    try:
        X = data.drop('price',axis=1)
        y = data['price']
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("Real Estate Price Prediction")
        splits = 3
        kf = KFold(shuffle=True, random_state=42, n_splits=splits)
        model = Pipeline([
            ("xgb", XGBRegressor(
                n_estimators=40,
                learning_rate=0.1,
                max_depth=4,
                objective="reg:squarederror",
                random_state=42
            ))
            ])
        with mlflow.start_run(run_name='XGBoost Regression'):
            
            y_pred = cross_val_predict(model,X,y, cv=kf)
            score = r2_score(y,y_pred)
            model.fit(X,y)
            mlflow.log_param("Cross_validation_splits", splits)
            mlflow.log_param("max_depth", 4)
            mlflow.log_param("n_estimators", 40)
            
            mlflow.log_metric('r2_score', score)
            mlflow.sklearn.log_model(sk_model=model, name="XGBoost_regression_model")
        model.fit(X,y)
        joblib.dump(model, 'models/model.pkl')
        logger.info("Model building and saving completed successfully")
    except Exception as e:
        logger.error(f"Error during model building: {e}")
        raise e

if __name__ == "__main__":
    data_file_path = Path('data/ProcessedData.csv')
    data = load_data(data_file_path)
    modelling(data)