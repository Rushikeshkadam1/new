# -*- coding: utf-8 -*-
"""Random Forest for predicting  holiday package.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HZS23-Y9U6Xqewwy_r3hvbS2GC7ikBLT
"""

import kagglehub

# Download latest version
path = kagglehub.dataset_download("susant4learning/holiday-package-purchase-prediction")

print("Path to dataset files:", path)

# Commented out IPython magic to ensure Python compatibility.
#  Importing required libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# %matplotlib inline

df  =  pd.read_csv('Travel.csv')
df.head()



"""# ***Data Cleaning***

Handling missing values

handling duplicates

  check datatype

  understand the dataset
  
"""

df.isnull().sum()  # number of null values with respect to specific feature

# check is there any spelling mistake in categorical value column
df['Gender'].value_counts()

# there is spelling mistakes in Female and Fe male

df['TypeofContact'].value_counts()

df['MaritalStatus'].value_counts()

# single and unmmaried is same category

df['Designation'].value_counts()

df['Gender'] = df['Gender'].replace('Fe Male','Female')
df['MaritalStatus'] = df['MaritalStatus'].replace('Single','Unmarried')

df['Gender'].value_counts()

df['MaritalStatus'].value_counts()

## Checking Missing values
feature_with_na = [feature for feature in df.columns if df[feature].isnull().sum()>=1]

# a column which having one or more than one null values are stored in a "feature_with_na"


for feature in feature_with_na:
  print(feature,np.round(df[feature].isnull().mean()*100,5),'% missing values')
# to get percentage of missing values

df[feature_with_na].select_dtypes(exclude='object').describe()

# Checking statistical description of null columns(numerical columns)

"""# *** Train Test Split and Model training ***

***One Hot Encoding and Binary Encoding***

Converting Categorical Data into Numeric data
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X = df.drop(['ProdTaken'], axis=1)
y = df['ProdTaken']

y.value_counts()

X.head()

# separate dataset into train and test

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train.shape, X_test.shape

# create Column Transformer with 3 types of transformers

cat_features = X.select_dtypes(include='object').columns # Categorical feaatures
num_features = X.select_dtypes(exclude='object').columns # numeric Features


numeric_transformer = StandardScaler()
oh_transformer = OneHotEncoder(drop='first')

preprocessor = ColumnTransformer(
    [
        ('OneHotEncoder', oh_transformer, cat_features),
        ('StandardScaler', numeric_transformer, num_features)
    ]
)

preprocessor

# Apply Transformation on Training Dataset (fit_transform)
X_train = preprocessor.fit_transform(X_train)

pd.DataFrame(X_train)

X_test = preprocessor.transform(X_test)



"""# ***Model Training ***"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay, \
                            roc_auc_score, roc_curve, precision_score, recall_score, f1_score

models = {
    "Decision Tree": DecisionTreeClassifier(),
    # "Logistic Regression": LogisticRegression(),
    'Random Forest': RandomForestClassifier()
}
for i in range(len(list(models))):
    model = list(models.values())[i]
    model.fit(X_train, y_train)                # Train model

    # Model Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Training Set Performance
    model_train_accuracy = accuracy_score(y_train, y_train_pred)
    model_train_f1 = f1_score(y_train, y_train_pred)
    model_train_precision = precision_score(y_train, y_train_pred)
    model_train_recall = recall_score(y_train, y_train_pred)
    model_train_roc_auc_score = roc_auc_score(y_train, y_train_pred)

    # Test Performance
    model_test_accuracy = accuracy_score(y_test, y_test_pred)
    model_test_f1 = f1_score(y_test, y_test_pred, average = 'weighted')
    model_test_precision = precision_score(y_test, y_test_pred)
    model_test_recall = recall_score(y_test, y_test_pred)
    model_test_roc_auc_score = roc_auc_score(y_test, y_test_pred)


    print(list(models.keys())[i])

    print('Model performance for Training set')
    print("- Accuracy: {:.4f}".format(model_train_accuracy))
    print('- F1 score: {:.4f}'.format(model_train_f1))
    print('- Precision: {:.4f}'.format(model_train_precision))
    print('- Recall: {:.4f}'.format(model_train_recall))
    print('- roc_auc_score: {:.4f}'.format(model_train_roc_auc_score))

    print('----------------------------------')

    print('Model performance for Test set')
    print('- Accuracy: {:.4f}'.format(model_test_accuracy))
    print('- F1 score: {:.4f}'.format(model_test_f1))
    print('- Precision: {:.4f}'.format(model_test_precision))
    print('- Recall: {:.4f}'.format(model_test_recall))
    print('- roc_auc_score: {:.4f}'.format(model_test_roc_auc_score))

"""# ***Hyperparameter Tunning***"""

rf_params = {"max_depth":[5,8,15,None,10],
             "max_features":[5,7,"auto",8],
             "min_samples_split": [2,8,15,20],
             "n_estimators":[100,200,500,1000]}

# model list for hyperparameter tunning

randomcv_models = [
    ('RF', RandomForestClassifier(), rf_params)
]

from sklearn.model_selection import RandomizedSearchCV

model_param = {}
for name, model, params in randomcv_models:
  random = RandomizedSearchCV(estimator=model,
                              param_distributions=params,
                              n_iter=100,
                              cv=3,
                              verbose=2,
                               n_jobs=-1)
  random.fit(X_train, y_train)
  model_param[name] = random.best_params_

for model_name in model_param:
  print(f"Best parameters for {model_name}: {model_param[model_name]}")

models ={
    "Random Forest": RandomForestClassifier(n_estimators=200,
                                            min_samples_split=2,
                                            max_features=8,
                                            max_depth= None)

}
for i in range(len(list(models))):
    model = list(models.values())[i]
    model.fit(X_train, y_train)                # Train model

    # Model Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Training Set Performance
    model_train_accuracy = accuracy_score(y_train, y_train_pred)
    model_train_f1 = f1_score(y_train, y_train_pred)
    model_train_precision = precision_score(y_train, y_train_pred)
    model_train_recall = recall_score(y_train, y_train_pred)
    model_train_roc_auc_score = roc_auc_score(y_train, y_train_pred)

    # Test Performance
    model_test_accuracy = accuracy_score(y_test, y_test_pred)
    model_test_f1 = f1_score(y_test, y_test_pred, average = 'weighted')
    model_test_precision = precision_score(y_test, y_test_pred)
    model_test_recall = recall_score(y_test, y_test_pred)
    model_test_roc_auc_score = roc_auc_score(y_test, y_test_pred)


    print(list(models.keys())[i])

    print('Model performance for Training set')
    print("- Accuracy: {:.4f}".format(model_train_accuracy))
    print('- F1 score: {:.4f}'.format(model_train_f1))
    print('- Precision: {:.4f}'.format(model_train_precision))
    print('- Recall: {:.4f}'.format(model_train_recall))
    print('- roc_auc_score: {:.4f}'.format(model_train_roc_auc_score))

    print('----------------------------------')

    print('Model performance for Test set')
    print('- Accuracy: {:.4f}'.format(model_test_accuracy))
    print('- F1 score: {:.4f}'.format(model_test_f1))
    print('- Precision: {:.4f}'.format(model_test_precision))
    print('- Recall: {:.4f}'.format(model_test_recall))
    print('- roc_auc_score: {:.4f}'.format(model_test_roc_auc_score))

from sklearn.metrics import roc_auc_score, roc_curve
plt.figure()

auc_models = [
{
    "label": "Random Forest Classifier",
    "model": RandomForestClassifier(n_estimators=200,
                                            min_samples_split=2,
                                            max_features=8,
                                            max_depth= None),
    "auc": 0.7933
},
]

# create loop through all models
for algo in auc_models:
  model = algo['model'] # select the model
  model.fit(X_train, y_train)  # train the model
  # Compute False positive rate and true positive rate
  fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:,1])
  # C;aculate area under curve to display on the plot
  plt.plot(fpr, tpr, label= '%s ROC (area = %0.2f)' % (algo['label'], algo['auc']))


  # Custom Settings for plot
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('1 - Specificity (False Positive Rate)')
plt.ylabel('Sensitivity (True Positive Rate)')
plt.title('Receiver Operating Characteristic')
plt.legend(loc = 'lower right')
plt.savefig('Log_ROC')
plt.show()