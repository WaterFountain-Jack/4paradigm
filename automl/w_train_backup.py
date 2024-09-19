# %%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import featuretools as ft
from woodwork.logical_types import Categorical, Integer, Boolean, Datetime, Double
import time
from autogluon.tabular import TabularPredictor
import autogluon.core as ag
import os
from datetime import datetime
import shutil

VERSION = 'autogluon-tabular'

path = '/root/test/m10/data/w_0812_0827.train.csv'
label_col = 'actionValue'
selected_cols = ['sceneId','eid','itemId','age','gender','categoryLevel1','categoryLevel2','duration','publisherName','source']
id_cols = ['sceneId', 'eid', 'itemId']
cat_cols = ['gender', 'categoryLevel1', 'categoryLevel2', 'publisherName', 'source']
numeric_cols = ['age', 'duration']

# Load the data
df = pd.read_csv(path)[selected_cols + [label_col]]


# Split the data
df[label_col] = (df[label_col] > 10).astype(int)
train_data, test_data = train_test_split(df, test_size=0.2, random_state=42, stratify=df[label_col])

# Prepare the feature columns
feature_cols = [col for col in train_data.columns if col != label_col]

# Set up AutoGluon predictor
predictor = TabularPredictor(
    label=label_col,
    path='/app1/m10/xgboost/models',
    eval_metric='roc_auc'
)

# Train the model with XGBoost hyperparameter search
predictor.fit(
    train_data=train_data,
    tuning_data=test_data,
    time_limit=3600,  # 1 hour time limit
    presets='optimize_for_deployment',
    hyperparameters={
            'XGB':{},
            # 'XGB':
            # {
            #     # 'n_estimators': 200,
            #     # 'max_depth': 5,
            # }
            },
    num_gpus=7,  # Adjust based on your hardware
    # num_bag_folds=0,
    # num_stack_levels=0,
    auto_stack=False,
    dynamic_stacking='auto', 
    use_bag_holdout=True,
    hyperparameter_tune_kwargs={
        'num_trials': 10,
        'scheduler': 'local',
        'searcher': 'auto',
    },
    infer_limit=0.001,
    infer_limit_batch_size=20,
    keep_only_best=True,
    save_space=True,
    refit_full=True,
    set_best_to_refit_full=True,
)

# Evaluate the model
y_pred_proba = predictor.predict_proba(test_data[feature_cols])
y_test = test_data[label_col]
auc_score = roc_auc_score(y_test, y_pred_proba[1])
print(f"AUC Score: {auc_score}")

# Print feature importance
feature_importance = predictor.feature_importance(test_data)
print("Top 10 Most Important Features:")
print(feature_importance.head(10))

# Test data prediction
test_data = pd.read_csv('/root/test/m10/data/w_sample.csv')[selected_cols + [label_col]].sample(20)

'''
# Fill missing values in test data
for col in cat_cols + id_cols:
    test_data[col].fillna('Unknown', inplace=True)
for col in numeric_cols:
    test_data[col].fillna(0, inplace=True)

# Apply feature engineering to test data
test_es = ft.EntitySet(id="test_data")
test_es = test_es.add_dataframe(
    dataframe_name="w",
    dataframe=test_data,
    index="index",
    make_index=True,
    logical_types={
        "sceneId": Categorical,
        "eid": Categorical,
        "itemId": Categorical,
        "age": Double,
        "gender": Categorical,
        "categoryLevel1": Categorical,
        "categoryLevel2": Categorical,
        "duration": Double,
        "publisherName": Categorical,
        "source": Categorical
    },
)

test_feature_matrix, _ = ft.dfs(
    entityset=test_es,
    target_dataframe_name="w",
    trans_primitives=trans_primitives,
    max_depth=1,
    features_only=False,
    verbose=1,
    primitive_options={
        key: {
            "ignore_columns": {'w': [label_col] + cat_cols + id_cols}
        }
        for key in trans_primitives
    }
)
'''
# Measure preprocessing and prediction time
start_time = time.time()

# Make predictions using AutoGluon
test_predictions = predictor.predict_proba(test_data[feature_cols])

end_time = time.time()

# Calculate and print the total time
total_time = end_time - start_time
print(f"Total time for preprocessing and prediction: {total_time:.4f} seconds")

# Print the predictions
print("\nPredictions for the random test data:")
print(test_predictions[1])  # Probability of positive class

# Save the model
# model_path = '/root/test/m10/autogluon_models/'
# if os.path.exists(model_path):
#     shutil.rmtree(model_path)
# predictor.save(model_path)

# print(f"Model saved to {model_path}")
