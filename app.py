from pathlib import Path
import joblib
from flask import Flask, request, render_template_string

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "phishing_model.joblib"
app = Flask(__name__)
PAGE = """
<!doctype html><html><head><meta charset="utf-8"><title>Phishing Email Detector</title>
<style>
body{font-family:Arial,sans-serif;background:#f2f5fa;margin:0;padding:40px;color:#172033}
main{max-width:760px;margin:auto;background:white;padding:30px;border-radius:16px;box-shadow:0 8px 30px #18294b18}
textarea{width:100%;min-height:180px;padding:12px;border:1px solid #cbd5e1;border-radius:8px;box-sizing:border-box}
button{margin-top:14px;background:#1769d2;color:white;border:0;padding:12px 22px;border-radius:8px;cursor:pointer}
.result{padding:14px;margin-top:18px;border-radius:8px;background:#e8f3ff}
small{color:#64748b}
</style></head><body><main><h1>Phishing Email Detection</h1>
<p>Paste an email message to check whether it resembles phishing content.</p>
<form method="post"><textarea name="email" required placeholder="Paste email text here...">{{ email }}</textarea>
<button type="submit">Analyze Email</button></form>
{% if result %}<div class="result"><h2>Prediction: {{ result }}</h2><p>Model confidence: {{ confidence }}%</p></div>{% endif %}
<p><small>Educational demonstration only. Do not rely on this model as the sole security control.</small></p>
</main></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = confidence = None
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "")[:20000]
        if not email.strip():
            result = "Please enter email text"
        elif not MODEL_PATH.exists():
            result = "Model not trained. Run python train_model.py first."
        else:
            model = joblib.load(MODEL_PATH)
            result = model.predict([email])[0].upper()
            confidence = f"{max(model.predict_proba([email])[0]) * 100:.1f}"
    return render_template_string(PAGE, result=result, confidence=confidence, email=email)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
