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
from sklearn.preprocessing import StandardScaler
import os
from datetime import datetime
import shutil
#加上'eid_count', 'wanbolv'
# 减去'sceneId','age'： AUC Score: 0.7899471617132312
#不减  AUC Score: 0.7854602943999003


#origin :AUC Score: 0.7559054441613424
#删除sceneId： AUC Score: 0.7432360663258208  AUC Score: 0.75565631195413
VERSION = 'autogluon-tabular'

path = '/root/test/m10/data/w_0812_0827.train.csv'
label_col = 'actionValue'
selected_cols = ['sceneId','eid','itemId','age','gender','categoryLevel1','categoryLevel2','duration','publisherName','source']
eid_count = None
df = None
shipin_wanbolv = None

def process_data():
    
    
    
    global path,label_col,selected_cols,df,eid_count,shipin_wanbolv
    path = '/root/test/m10/data/w_0812_0827.train.csv'
    label_col = 'actionValue'
    #删除掉sceneId 和age，因为他们的方差是0
    selected_cols = ['sceneId','age','eid','itemId','gender','categoryLevel1','categoryLevel2','duration','publisherName','source']
    # Load the data
    df = pd.read_csv(path)[selected_cols + [label_col]]
    # df['eid_count'] = df['eid'].map(df['eid'].value_counts())
    
    #先把标签弄成0 
    # df[label_col] = (df[label_col] > 10).astype(int)
    

    
    
    #eid_wanbolv_rate
    # 按照 a 分组，计算 b 为 True 的数量和每组的总数量
    eid_wanbolv_rate = df.groupby('eid')[label_col].agg(['sum', 'count'])

    # 计算每类 a 中 b 为 True 的概率
    eid_wanbolv_rate['true_rate'] = eid_wanbolv_rate['sum'] / eid_wanbolv_rate['count']

    # 重命名列名，使其更清晰（可选）
    eid_wanbolv_rate = eid_wanbolv_rate.rename(columns={'sum': 'b_true_count', 'count': 'total_count'})

    print("出现次数为1的平均值为：",eid_wanbolv_rate[eid_wanbolv_rate["total_count"] == 1]['true_rate'].mean())
   
   
    # 查看结果
    eid_wanbolv_rate = eid_wanbolv_rate['true_rate']
    eid_wanbolv_rate.name = 'eid_wanbolv_rate'
    eid_wanbolv_rate = eid_wanbolv_rate.to_frame(name='eid_wanbolv_rate')
    df = pd.merge(df,eid_wanbolv_rate,on='eid',how='left')
    print(f"eid_wanbolv_rate.head():{eid_wanbolv_rate.head()}")
    
    
    
    #用户次数
    eid_count = df.groupby('eid').size().reset_index(name = 'eid_count')
    eid_count.to_pickle('eid_count.pkl')
    df = pd.merge(df,eid_count,on='eid',how='left')
    
 
    eid_count.set_index('eid')
    
    
    
    
    
    #用户完播率
    eid_wanbolv  = df.groupby('eid').apply(lambda x: x ['actionValue'].sum() / x['duration'].sum() if x['duration'].sum() != 0 else 0).reset_index(name = 'eid_wanbolv')
    df = pd.merge(df, eid_wanbolv, on='eid', how='left')
    eid_wanbolv.to_pickle('eid_wanbolv.pkl')
    eid_wanbolv.set_index('eid')
    
    
    
    print(f"eid_count.head():{eid_count.head()}")
    
    print(f"eid_wanbolv.head():{eid_wanbolv.head()}")
    
    
    # 先合并前两个 DataFrame
    eid_feature = pd.merge(eid_count, eid_wanbolv, on='eid', how='outer')

    # 再合并第三个 DataFrame
    eid_feature = pd.merge(eid_feature, eid_wanbolv_rate, on='eid', how='outer')
    

    
    eid_feature.to_pickle('eid_feature.pkl')
    
    # print(eid_wanbolv_rate)
    
    print(eid_feature.head())
    
    #视频计数
    shipin_count = df.groupby('itemId').size().reset_index(name = 'shipin_count')
    shipin_count.to_pickle('shipin_count.pkl')
    df = pd.merge(df,shipin_count,on='itemId',how='left')
    
    #视频完播率
    shipin_wanbolv  = df.groupby('itemId').apply(lambda x: x ['actionValue'].sum() / x['duration'].sum() if x['duration'].sum() != 0 else 0).reset_index(name = 'wanbolv')
    df = pd.merge(df, shipin_wanbolv, on='itemId', how='left')
    shipin_wanbolv.to_pickle('shipin_wanbolv.pkl')
    
    
    shipin_feature = pd.merge(shipin_count,shipin_wanbolv)
    print(f"shipin_feature.head():{shipin_feature.head()}")
    shipin_feature.to_pickle('shipin_feature.pkl')
    
    selected_cols = selected_cols + ['eid_count' ,'eid_wanbolv','eid_wanbolv_rate','wanbolv',"shipin_count"]
    
    # selected_cols = selected_cols + ['eid_count' ,'eid_wanbolv','wanbolv',"shipin_count"]
    
    
    # df = df[selected_cols]
    # time.sleep(1000000)
    
    

process_data ()
print(df.head())



# Split the data
df[label_col] = (df[label_col] > 10).astype(int)




train_data, test_data = train_test_split(df, test_size=0.0001, random_state=45, stratify=df[label_col])





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
# test_data = pd.read_csv('/root/test/m10/data/w_sample.csv')[selected_cols + [label_col]].sample(20)
test_data = pd.read_csv('/root/test/m10/data/w_sample.csv').sample(20)

eid_feature = pd.read_pickle('eid_feature.pkl')
shipin_feature  = pd.read_pickle('shipin_feature.pkl')

test_data = pd.merge(test_data, eid_feature, on='eid', how='left')
test_data = pd.merge(test_data, shipin_feature, on='itemId', how='left')

# eid_count = pd.read_pickle('eid_count.pkl')
# eid_wanbolv = pd.read_pickle('eid_wanbolv.pkl')
# shipin_count = pd.read_pickle('shipin_count.pkl')
# shipin_wanbolv = pd.read_pickle('shipin_wanbolv.pkl')
# print("加载成功")
# test_data= pd.merge(test_data,eid_count,on='eid',how='left')
# test_data= pd.merge(test_data,eid_wanbolv,on='eid',how='left')
# test_data = pd.merge(test_data, shipin_wanbolv, on='itemId', how='left')
# test_data = pd.merge(test_data, shipin_count, on='itemId', how='left')
test_data = test_data[selected_cols + [label_col]]
# Measure preprocessing and prediction time
start_time = time.time()


# Make predictions using AutoGluon
test_predictions = predictor.predict_proba(test_data)

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
