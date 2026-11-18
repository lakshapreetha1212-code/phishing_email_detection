# Phishing Email Detection Model

A beginner-friendly machine-learning project using Python, Scikit-learn, TF-IDF text features, and simple URL/email indicators.

## Requirements
- Python 3.10 or newer
- Internet connection for the first dependency installation

## Windows setup (PowerShell)
```powershell
cd phishing_email_detection
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
python train_model.py
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

## Run prediction in the terminal
```powershell
python predict.py "Your account is suspended. Verify your password immediately."
```
Or run `python predict.py` and paste an email when prompted.

## Run the web interface
```powershell
python app.py
```
Open http://127.0.0.1:5001 in your browser.

## Project files
- `emails.csv` - small labelled demo dataset (phishing/safe)
- `features.py` - URL and email feature extraction
- `train_model.py` - trains, evaluates, and saves the model
- `predict.py` - command-line prediction
- `app.py` - local web interface

## Important
This dataset is intentionally small and is for demonstrating the workflow. Accuracy on it is not a measure of real-world protection. Add a larger, diverse, correctly labelled dataset and test on unseen messages before using it for research or deployment. Never open suspicious links or attachments while collecting samples.
