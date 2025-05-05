import json
import matplotlib.pyplot as plt

# Load your data
with open("all_article_chunks.json", "r") as f:
    data = json.load(f)

# Extract word and character counts
word_counts = [len(item["text"].split()) for item in data]
char_counts = [len(item["text"]) for item in data]

# Plot histograms
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Word count histogram
axes[0].hist(word_counts, bins=10, color='skyblue', edgecolor='black')
axes[0].set_title("Histogram of Word Counts")
axes[0].set_xlabel("Number of Words")
axes[0].set_ylabel("Number of Chunks")

# Character count histogram
axes[1].hist(char_counts, bins=10, color='salmon', edgecolor='black')
axes[1].set_title("Histogram of Character Counts")
axes[1].set_xlabel("Number of Characters")
axes[1].set_ylabel("Number of Chunks")

plt.tight_layout()
plt.show()
