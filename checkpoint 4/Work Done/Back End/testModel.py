from joblib import load

MODEL_PATH = "C:\\Users\\thema\\Documents\\Project_WoC_7.0_Fake_Review_Detection\\checkpoint 4\\Work Done\\Back End\\SVM_pipeline_final.pkl"

try:
    model = load(MODEL_PATH)
    print("Model loaded successfully with joblib!")
except Exception as e:
    print("Error loading model:", str(e))
