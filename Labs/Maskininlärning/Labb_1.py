
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


df = pd.read_csv("cardio_train.csv", sep=";")

# Rensa orimliga värden (längd, vikt)
df = df[(df["height"] >= 140) & (df["height"] <= 210)]
df = df[(df["weight"] >= 40) & (df["weight"] <= 180)]

# Skapa BMI och rensa

df = df.copy()
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)
df = df[(df["BMI"] >= 16) & (df["BMI"] <= 60)]

# Skapa BMI-kategori
def bmi_category(bmi):
    if bmi < 18.5:
        return "Undervikt"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    elif bmi < 35:
        return "Obese (Class I)"
    elif bmi < 40:
        return "Obese (Class II)"
    else:
        return "Obese (Class III)"

df["BMI_category"] = df["BMI"].apply(bmi_category)

# Skapa blodtryckskategori 
def classify_bp(systolic):
    if systolic < 120:
        return "Optimalt"
    elif systolic < 130:
        return "Normalt"
    elif systolic < 140:
        return "Högt normalt"
    elif systolic < 160:
        return "Hypertoni grad 1"
    elif systolic < 180:
        return "Hypertoni grad 2"
    else:
        return "Hypertoni grad 3"

df["BP_category"] = df["ap_hi"].apply(classify_bp)

# Feature selection
features = [
    "age", "gender", "smoke", "alco", "active",
    "ap_hi", "ap_lo", "cholesterol", "gluc", "BMI"
]
X = df[features]
y = df["cardio"]

# One-hot encoding av kategoriska features
X = pd.get_dummies(X, columns=["gender", "cholesterol", "gluc"], drop_first=True)

# 7. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. Skala data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# MODELL 1: Decision Tree 
tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train)
y_pred_tree = tree_model.predict(X_test)
print("\nDecision Tree Accuracy:", accuracy_score(y_test, y_pred_tree))
print(classification_report(y_test, y_pred_tree))

# MODELL 2: Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
print("\nRandom Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# MODELL 3: Logistisk Regression
log_model = LogisticRegression(max_iter=2000)
log_model.fit(X_train_scaled, y_train)
y_pred_log = log_model.predict(X_test_scaled)
print("\nLogistisk Regression Accuracy:", accuracy_score(y_test, y_pred_log))
print(classification_report(y_test, y_pred_log))

# confusion matrix
cm = confusion_matrix(y_test, y_pred_log)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=log_model.classes_)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix – Logistisk Regression")
plt.show()
