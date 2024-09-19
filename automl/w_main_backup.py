import logging
import os
import time
import warnings
from flask import Flask, request
import pandas as pd
import featuretools as ft
from woodwork.logical_types import Categorical, Double
from autogluon.tabular import TabularPredictor

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s %(name)-12s %(levelname)-4s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__file__)

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

VERSION='autogluon-xgb'
PORT=int(os.environ.get('PORT', '80'))

app = Flask(__name__)

# Global variable for model
predictor = None

@app.route('/ready', methods=['GET'])
def ready():
    global predictor
    
    # Load the AutoGluon predictor
    predictor = TabularPredictor.load(f'/root/test/m10/xgboost/models')
    predictor.set_model_best(predictor.model_best)
    predictor.persist()
    
    return {'ready': True}

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    
    req = request.get_json()
    data = req['data']
    
    selected_cols = ['sceneId','eid','itemId','age','gender','categoryLevel1','categoryLevel2','duration','publisherName','source']

    
    df = pd.DataFrame(data)[selected_cols]
    
    # Make predictions
    results = predictor.predict_proba(df)[1].tolist()
    
    end_time = time.time()
    prediction_time = end_time - start_time
    
    logger.info(f"Prediction completed in {prediction_time:.4f} seconds")
    
    return {
        'success': True, 
        'results': results, 
    }

if __name__ == '__main__':
    app.run("0.0.0.0", PORT)