import numpy as np
import matplotlib.pyplot as plt

# Metrics
metrics = ["Accuracy (%)", "Precision (%)", "Recall (%)", "F1 Score (%)", "CER", "WER", "RT (spf)"]

# Values for Paddle
paddle_values = [72.93, 70.46, 84.82, 76.98, 0.06, 0.09, 5.7]

# Values for Paddle with Thresholding
paddle_thresh_values = [75.32, 71.28, 85.09, 77.58, 0.05, 0.08, 3.6]

# Bar width and positions
x = np.arange(len(metrics))
width = 0.35

# Plot bars
fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, paddle_values, width, label='Paddle', color='blue')
rects2 = ax.bar(x + width/2, paddle_thresh_values, width, label='Paddle with Thresholding', color='orange')

# Labels and title
ax.set_xlabel("Metrics")
ax.set_ylabel("Values")
ax.set_title("Comparative Analysis of Paddle and Paddle with Thresholding")
ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=20, ha="right")
ax.legend()

# Display values on top of bars
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(rects1)
add_labels(rects2)

# Show plot
plt.tight_layout()
plt.show()