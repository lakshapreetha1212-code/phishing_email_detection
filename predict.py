from pathlib import Path
import sys
import joblib

MODEL = Path(__file__).resolve().parent / "phishing_model.joblib"

def main():
    if not MODEL.exists():
        print("Model not found. Run: python train_model.py")
        raise SystemExit(1)
    email = " ".join(sys.argv[1:]).strip()
    if not email:
        email = input("Paste email text: ").strip()
    model = joblib.load(MODEL)
    prediction = model.predict([email])[0]
    probabilities = model.predict_proba([email])[0]
    confidence = max(probabilities) * 100
    print("\\nPrediction:", prediction.upper())
    print(f"Model confidence: {confidence:.1f}%")
    print("Use this as a screening aid, not as a guarantee that an email is safe.")

if __name__ == "__main__":
    main()
