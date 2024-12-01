import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

# Load dataset
file_path = 'Sales Data.csv'
sales_data = pd.read_csv(file_path)

# Convert 'Date' to datetime and extract year
sales_data['Date'] = pd.to_datetime(sales_data['Date'])
sales_data['Year'] = sales_data['Date'].dt.year

# Group data to calculate yearly KPIs
yearly_kpis = sales_data.groupby(['Year', 'Category']).agg(
    TotalSales=('TotalSales', 'sum'),
    Orders=('ProductID', 'count') 
).reset_index()

# Assuming Marketing Spend (10% of Total Sales) and calculate ROMS since the data is not mentioned in the file
yearly_kpis['MarketingSpend'] = yearly_kpis['TotalSales'] * 0.5
yearly_kpis['ROMS'] = yearly_kpis['TotalSales'] / yearly_kpis['MarketingSpend']

# Calculate Average Order Value (AOV)
yearly_kpis['AOV'] = yearly_kpis['TotalSales'] / yearly_kpis['Orders']

# Save raw KPI data to CSV
yearly_kpis.to_csv('Yearly_KPIs.csv', index=False)

# Visualization - Bar chart for Total Sales per Category
plt.figure(figsize=(10, 6))
for year in yearly_kpis['Year'].unique():
    data = yearly_kpis[yearly_kpis['Year'] == year]
    plt.bar(data['Category'], data['TotalSales'], label=str(year))

plt.title('Total Sales per Category (Yearly)')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.legend(title='Year')
plt.savefig('Total_Sales_Per_Category.png')  # Save the plot as an image
plt.close()

# Visualization for ROMS
plt.figure(figsize=(10, 6))
for year in yearly_kpis['Year'].unique():
    data = yearly_kpis[yearly_kpis['Year'] == year]
    plt.bar(data['Category'], data['ROMS'], label=str(year))

plt.title('ROMS (Return on Marketing Spend) per Category (Yearly)')
plt.xlabel('Category')
plt.ylabel('ROMS')
plt.legend(title='Year')
plt.savefig('ROMS_Per_Category.png')  # Save ROMS plot as an image
plt.close()

# Visualization for AOV 
fig = px.bar(
    yearly_kpis,
    x='Category',
    y='AOV',
    color='Year',
    title='Average Order Value (AOV) per Category (Yearly)'
)

# Save AOV Plot as Image
fig.write_image("AOV_Per_Category.png")

# PDF generation with table format for good readability
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Yearly Sales Report', border=0, ln=1, align='C')
        self.ln(10) 

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, border=0, ln=1, align='L')
        self.ln(5)  #  for spacing

    def chapter_body(self, data):
        # Set table header
        self.set_font('Arial', 'B', 12)
        headers = ['Year', 'Category', 'Total Sales', 'Orders', 'Marketing Spend', 'ROMS', 'AOV']
        col_width = 30  
        for header in headers:
            self.cell(col_width, 10, header, border=1, align='C')
        self.ln()

        # Set table content
        self.set_font('Arial', '', 12)
        for row in data.itertuples(index=False):
            self.cell(col_width, 10, str(row.Year), border=1, align='C')
            self.cell(col_width, 10, row.Category, border=1, align='C')
            self.cell(col_width, 10, f"{row.TotalSales:,.2f}", border=1, align='C')
            self.cell(col_width, 10, str(row.Orders), border=1, align='C')
            self.cell(col_width, 10, f"{row.MarketingSpend:,.2f}", border=1, align='C')
            self.cell(col_width, 10, f"{row.ROMS:.2f}", border=1, align='C')
            self.cell(col_width, 10, f"{row.AOV:.2f}", border=1, align='C')
            self.ln()

# Create PDF report
pdf = PDF()
pdf.add_page()

# KPI Summary Section
pdf.chapter_title('KPI Summary')
pdf.chapter_body(yearly_kpis)

# Add the Total Sales per Category chart to PDF
pdf.add_page()
pdf.chapter_title('Total Sales per Category (Yearly)')
pdf.image('Total_Sales_Per_Category.png', x=10, y=30, w=180)

# Add AOV Chart to PDF
pdf.add_page()
pdf.chapter_title('Average Order Value (AOV) per Category')
pdf.image("AOV_Per_Category.png", x=10, y=30, w=180)

# Add ROMS Chart to PDF
pdf.add_page()
pdf.chapter_title('ROMS (Return on Marketing Spend) per Category')
pdf.image("ROMS_Per_Category.png", x=10, y=30, w=180)

# Output PDF
pdf.output('kpi_dashboard.pdf')

# Automation Instructions
print("To automate, schedule this script using cron (Linux/Mac) or Task Scheduler (Windows).")

#0 0 * * SUN /path/to/python3 /path/to/your/script.py
