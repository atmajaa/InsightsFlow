import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# Load and clean data
df = pd.read_csv("products.csv")
df["Price"] = df["Price"].astype(str).str.extract(r"\u20b9([\d,]+)")[0].str.replace(",", "").astype(float)
df["Review"] = df["Review"].astype(str).str.extract(r"(\d+)")[0].astype(float)

# KPIs
avg_price = df["Price"].mean()
avg_rating = df["Rating"].mean()
total_reviews = df["Review"].sum()
bestseller_count = df["Label"].str.contains("BESTSELLER", na=False).sum()

# Visualization
plt.figure(figsize=(15, 6))

# Price Distribution
plt.subplot(1, 2, 1)
sns.histplot(df["Price"], bins=10, kde=True, color="blue")
plt.title("Price Distribution")
plt.xlabel("Price (₹)")

# Rating Distribution
plt.subplot(1, 2, 2)
sns.histplot(df["Rating"], bins=10, kde=True, color="green")
plt.title("Rating Distribution")
plt.xlabel("Rating")

plt.tight_layout()
plt.savefig("visualization.png")  # Save visualization as PNG
plt.show()

# Top 5 Best-Rated Products
top_rated = df.nlargest(5, "Rating")[["Title", "Rating"]]

# Save top-rated products to PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Top 5 Best-Rated Products", ln=True, align="C")

for index, row in top_rated.iterrows():
    title_cleaned = row['Title'].encode('latin-1', 'ignore').decode('latin-1')  # Remove unsupported characters
    pdf.cell(200, 10, txt=f"{title_cleaned} - Rating: {row['Rating']}", ln=True, align="L")

pdf.output("top_rated_products.pdf")
