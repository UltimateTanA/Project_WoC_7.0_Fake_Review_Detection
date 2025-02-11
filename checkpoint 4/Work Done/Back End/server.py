import warnings
import pandas as pd
import os
from joblib import load
from flask import Flask, request, jsonify
from flask_cors import CORS
from Review_scraper import get_amazon_reviews_selenium  # Import your scraper

warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load the trained SVM model
MODEL_PATH = "C:\\Users\\thema\\Documents\\Project_WoC_7.0_Fake_Review_Detection\\checkpoint 4\\Work Done\\Back End\\SVM_pipeline_final.pkl"
CSV_FILE_PATH = "C:\\Users\\thema\\Documents\\Project_WoC_7.0_Fake_Review_Detection\\checkpoint 4\\Work Done\\Back End\\Reviews.csv"

# ✅ Load the model with error handling
try:
    model = load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

def classify_review(review):
    """Classifies a review as 'Human' or 'Computer-generated' using the SVM model."""
    try:
        prediction = model.predict([review])[0]  # Ensure input format matches training
        return "Computer-generated" if prediction == 1 else "Human"
    except Exception as e:
        print(f"❌ Error classifying review: {e}")
        return "Error"

@app.route("/scrape", methods=["POST"])
def scrape_and_classify():
    data = request.json
    product_url = data.get("url")

    if not product_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        print("🔄 Scraping reviews from:", product_url)
        get_amazon_reviews_selenium(product_url)  
        print("✅ Scraping completed, saved to CSV!")

        # ✅ Step 2: Ensure CSV file exists
        if not os.path.exists(CSV_FILE_PATH):
            print("❌ Error: CSV file not found")
            return jsonify({"error": "CSV file not found"}), 500

        # ✅ Step 3: Read the CSV file
        df = pd.read_csv(CSV_FILE_PATH)
        print(f"📄 CSV Loaded! Found {len(df)} reviews.")

        # ✅ Step 4: Ensure "Review" column exists
        if "Review" not in df.columns:
            print("❌ Error: 'Review' column not found in CSV")
            print("🔍 CSV Columns:", df.columns)
            return jsonify({"error": "'Review' column missing in CSV"}), 500

        # ✅ Step 5: Convert all reviews to strings before classification
        df["Review"] = df["Review"].astype(str)

        # ✅ Step 6: Classify the reviews
        df["label"] = df["Review"].apply(classify_review)

        # ✅ Step 7: Convert results to JSON and return
        classified_reviews = df[["Review", "label"]].to_dict(orient="records")
        print("✅ Classification completed. Sending response...")
        return jsonify({"reviews": classified_reviews})

    except Exception as e:
        print(f"❌ Error in /scrape endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
