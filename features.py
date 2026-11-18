import re
from urllib.parse import urlparse
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
SUSPICIOUS_WORDS = (
    "urgent", "verify", "password", "suspended", "account", "click",
    "claim", "prize", "winner", "immediately", "otp", "bank", "refund",
    "confirm", "limited", "expire", "payment", "security alert"
)

class EmailFeatures(BaseEstimator, TransformerMixin):
    """Extract simple numeric email and URL indicators."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        output = []
        for value in X:
            text = str(value)
            lower = text.lower()
            urls = URL_RE.findall(text)
            url_count = len(urls)
            suspicious_url_count = 0
            ip_url_count = 0
            https_count = 0
            for raw in urls:
                candidate = raw.rstrip(".,);]")
                if candidate.lower().startswith("www."):
                    candidate = "http://" + candidate
                parsed = urlparse(candidate)
                host = parsed.hostname or ""
                if parsed.scheme == "https":
                    https_count += 1
                if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
                    ip_url_count += 1
                if any(token in host.lower() for token in ("login", "verify", "secure", "update", "account")):
                    suspicious_url_count += 1
            features = [
                len(text),
                len(text.split()),
                sum(1 for word in SUSPICIOUS_WORDS if word in lower),
                url_count,
                suspicious_url_count,
                ip_url_count,
                https_count,
                text.count("!"),
                int("@" in text),
                int(any(x in lower for x in ("bit.ly", "tinyurl", "t.co"))),
            ]
            output.append(features)
        return np.asarray(output, dtype=float)
