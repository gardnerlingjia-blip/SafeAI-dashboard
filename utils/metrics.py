
# Import required libraries
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from PIL import Image, ImageDraw

# Define a function to compute model performance metrics
def compute_metrics(df):
    # Extract true labels and predictions
    y_true = df['true_label']
    y_pred = df['prediction']
    
    # Compute metrics
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'Recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'F1 Score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'Confusion Matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    
    return metrics

# Create 3 sample image files in the data/ folder for testing
image_names = ['image_1.jpg', 'image_2.jpg', 'image_3.jpg']
for name in image_names:
    # Create a blank image with white background
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 90), name, fill='black')
    img.save(f'data/{name}')


# Import required libraries
import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from PIL import Image, ImageDraw

# Create the data/ folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# Define a function to compute model performance metrics
def compute_metrics(df):
    # Extract true labels and predictions
    y_true = df['true_label']
    y_pred = df['prediction']
    
    # Compute metrics
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'Recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'F1 Score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'Confusion Matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    
    return metrics

# Save the metrics.py file
with open("utils/metrics.py", "w") as f:
    f.write('''import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def compute_metrics(df):
    y_true = df['true_label']
    y_pred = df['prediction']
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'Recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'F1 Score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'Confusion Matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    return metrics
''')

# Create 3 sample image files in the data/ folder for testing
image_names = ['image_1.jpg', 'image_2.jpg', 'image_3.jpg']
for name in image_names:
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 90), name, fill='black')
    img.save(f'data/{name}')


# Import required libraries
import os
from PIL import Image, ImageDraw

# Create the required folders if they don't exist
os.makedirs('utils', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Save the metrics.py file in the utils/ folder
metrics_code = '''import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def compute_metrics(df):
    y_true = df['true_label']
    y_pred = df['prediction']
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'Recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'F1 Score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'Confusion Matrix': confusion_matrix(y_true, y_pred).tolist()
    }
    return metrics
'''

with open("utils/metrics.py", "w") as f:
    f.write(metrics_code)

# Create 3 sample image files in the data/ folder for testing
image_names = ['image_1.jpg', 'image_2.jpg', 'image_3.jpg']
for name in image_names:
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 90), name, fill='black')
    img.save(f'data/{name}')
