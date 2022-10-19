print('Hello World')
# imports

import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# In[2]:


mlflow.set_experiment('jshehade-exp1')

# start an mlflow run
with mlflow.start_run():

    # Read the CSV
    df = pd.read_csv('congestion-data.csv')

    # define the features and the target
    inputs = df.drop('route_drc_total_m', axis='columns')
    target = df['route_drc_total_m']

    # split the data
    TEST_RATIO = 0.3  # ratio of test dataset from total dataset
    inputs_train, inputs_test, target_train, target_test = train_test_split(
        inputs,
        target,
        test_size=TEST_RATIO
    )

    # train the model
    hyperparams = {
        'n_estimators': 10,  # The number of trees in the forest
        'max_depth': 19,     # The maximum depth of a tree
        'n_jobs': 1,         # The number of jobs to run in parallel
    }
    model = RandomForestClassifier(**hyperparams)
    model.fit(inputs_train, target_train)

    # log params and metrics
    mlflow.log_param('Model Type', 'RandomForestClassifier')
    mlflow.log_param('Test ratio', TEST_RATIO)
    mlflow.log_params(hyperparams)
    mlflow.log_metric('Score', model.score(inputs_test, target_test))

    # register the model
    mlflow.sklearn.log_model(model, 'jshehade-congestion-model')

