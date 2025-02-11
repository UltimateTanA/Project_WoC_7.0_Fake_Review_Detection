# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PSANSsUqPwA7wgwc_ecDqB3HAjc1ER4i

###this is the second notebook pertaining to the WoC NLP project. the first part contains data preprocessing. this notebook aims to build a model on top of the processed dataset.
"""

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split

# Step 1.1: Load the preprocessed dataset
# Replace 'preprocessed_dataset.csv' with your actual file name
file_path = '/content/fakeReviewDataLemmatized.csv'
dataset = pd.read_csv(file_path)

# Step 1.2: Inspect the dataset structure
print("Dataset Preview:")
print(dataset.head())

print("\nDataset Info:")
print(dataset.info())

# Step 1.3: Check for missing values
print("\nMissing Values Summary:")
print(dataset.isnull().sum())

# Step 1.4: Split the dataset into training and testing sets
# Using 'tokens_lemmatized' for text data and 'label' as the target
X = dataset['tokens_lemmatized']  # Features (lemmatized tokens)
y = dataset['label']  # Labels (classification target)

# Convert the features to a suitable format (e.g., strings)
X = X.apply(lambda x: ' '.join(eval(x)))  # Convert lists of tokens to strings

# Splitting into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print the shapes of the splits
print("\nTraining Set Size:", X_train.shape[0])
print("Testing Set Size:", X_test.shape[0])

# Save the splits for later use
X_train.to_csv('X_train.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("\nDataset preparation completed successfully!")

# Random Forest Model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import pandas as pd

# Load the training and testing datasets
X_train = pd.read_csv('X_train.csv', header=None).squeeze("columns")
y_train = pd.read_csv('y_train.csv', header=None).squeeze("columns")
X_test = pd.read_csv('X_test.csv', header=None).squeeze("columns")
y_test = pd.read_csv('y_test.csv', header=None).squeeze("columns")

# Handle missing values
X_train = X_train.fillna("")
X_test = X_test.fillna("")

# Create pipeline for Random Forest
rf_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Convert text to TF-IDF features
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train the Random Forest model
print("Training Random Forest...")
rf_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred_rf = rf_pipeline.predict(X_test)
print("\nClassification Report for Random Forest:")
print(classification_report(y_test, y_pred_rf))

# Save the model
joblib.dump(rf_pipeline, 'RandomForest_model.pkl')
print("Random Forest model saved as RandomForest_model.pkl")

# Import necessary libraries
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline  # Import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import joblib

# Create pipeline for SVM
svm_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Convert text to TF-IDF features
    ('classifier', SVC(probability=True, random_state=42))
])

# Train the SVM model
print("Training SVM...")
svm_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred_svm = svm_pipeline.predict(X_test)
print("\nClassification Report for SVM:")
print(classification_report(y_test, y_pred_svm))

# Save the model
joblib.dump(svm_pipeline, 'SVM_model.pkl')
print("SVM model saved as SVM_model.pkl")

# Logistic Regression Model
from sklearn.linear_model import LogisticRegression

# Create pipeline for Logistic Regression
lr_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Convert text to TF-IDF features
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

# Train the Logistic Regression model
print("Training Logistic Regression...")
lr_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred_lr = lr_pipeline.predict(X_test)
print("\nClassification Report for Logistic Regression:")
print(classification_report(y_test, y_pred_lr))

# Save the model
joblib.dump(lr_pipeline, 'LogisticRegression_model.pkl')
print("Logistic Regression model saved as LogisticRegression_model.pkl")

"""###here, we've tried three different models for our application and exported the respective pickle files. that completes steps 1 and 2 from checkpoint 2.


Given the promising results from SVM model, we'll move ahead with fine tuning it and refining its performance.
"""

# Import necessary libraries
from sklearn.pipeline import Pipeline
import joblib

# Load the pretrained pipeline
print("Loading the pretrained SVM model...")
svm_pipeline_pretrained = joblib.load("SVM_model.pkl")  # Replace with your file path
print("SVM model loaded successfully.")

# Extract the pre-fitted vectorizer and classifier
tfidf_fitted = svm_pipeline_pretrained.named_steps['tfidf']
svm_classifier = svm_pipeline_pretrained.named_steps['classifier']

# Recreate the pipeline using the pre-fitted components
svm_pipeline_final = Pipeline([
    ('tfidf', tfidf_fitted),  # Use the pre-fitted TF-IDF vectorizer
    ('classifier', svm_classifier)  # Use the pre-trained SVM classifier
])

# Save the final pipeline
print("Saving the final pipeline...")
joblib.dump(svm_pipeline_final, "SVM_pipeline_final.pkl")
print("Pipeline saved as SVM_pipeline_final.pkl")

# Test the pipeline
print("Testing the pipeline...")
new_reviews = ["This product is amazing!", "Terrible experience, never buying again."]
predictions = svm_pipeline_final.predict(new_reviews)
print("Predictions for new reviews:", predictions)

"""###step 4 becomes redundant because we've already trained all the three models to check which one performs best. we've also done pipelining so that the model can take in raw text and perform preprocessing, vectorization, and classify the text all by itself.

###we now move towards evaluation of the models on the test dataset to find out which one performs best.
"""

# Filter out irrelevant classes
y_test_filtered = y_test[y_test.isin(['CG', 'OR'])]
X_test_filtered = X_test[y_test.isin(['CG', 'OR'])]

# Verify the unique classes
print("Filtered unique classes:", y_test_filtered.unique())

# Import necessary libraries
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import pandas as pd

# Load the testing datasets
X_test = pd.read_csv('/content/X_test.csv', header=None).squeeze("columns").fillna("")
y_test = pd.read_csv('/content/y_test.csv', header=None).squeeze("columns")

# Filter out irrelevant classes (e.g., 'label')
valid_classes = ['CG', 'OR']  # Define the classes to include
filtered_indices = y_test.isin(valid_classes)  # Filter indices for valid classes
X_test_filtered = X_test[filtered_indices]  # Filter X_test
y_test_filtered = y_test[filtered_indices]  # Filter y_test

# Verify the filtered dataset
print("Filtered unique classes in y_test:", y_test_filtered.unique())

# Define paths to the saved models
model_files = {
    "Random Forest": "/content/RandomForestModel.pkl",
    "SVM": "/content/SVM_pipeline_final.pkl",
    "Logistic Regression": "/content/LogisticRegressionModel.pkl"
}

# Evaluate each model
evaluation_results = {}

for model_name, model_file in model_files.items():
    print(f"Evaluating Model: {model_name}")

    # Load the trained model
    model = joblib.load(model_file)

    # Make predictions on the filtered test dataset
    y_pred = model.predict(X_test_filtered)

    # Calculate metrics
    accuracy = accuracy_score(y_test_filtered, y_pred)
    classification_rep = classification_report(y_test_filtered, y_pred, target_names=valid_classes)
    confusion_mat = confusion_matrix(y_test_filtered, y_pred)

    # Store results
    evaluation_results[model_name] = {
        "Accuracy": accuracy,
        "Classification Report": classification_rep,
        "Confusion Matrix": confusion_mat
    }

    # Print results
    print("\nConfusion Matrix:")
    print(confusion_mat)

    print("\nClassification Report:")
    print(classification_rep)

    print(f"\nAccuracy: {accuracy:.4f}")
    print("-" * 50)

# Summary of results
print("\nModel Evaluation Summary:")
for model_name, metrics in evaluation_results.items():
    print(f"{model_name} - Accuracy: {metrics['Accuracy']:.4f}")

"""###the above evaluation on the testing datasets confirms our initial suspicion that SVM is best (although marginally) among the three classifiers we are using."""

