# 💰 Expense Tracker Pro - Advanced Streamlit UI

A modern, feature-rich expense tracking application built with **Streamlit**. Track your spending across categories, visualize trends, and manage your finances efficiently.

## 🎯 Features

### 📊 Dashboard
- **Real-time metrics** showing total expenses, average expense, largest expense, and transaction count
- **Interactive pie chart** for category breakdown
- **Spending trend visualization** showing last 30 days of expenses
- **Recent expenses** quick view with one-click delete

### ➕ Add Expense
- Intuitive expense entry form with validation
- Support for 8+ predefined categories
- Payment method tracking (Cash, Credit Card, Debit Card, Digital Wallet)
- Custom tags for organization (Urgent, Work, Personal, Recurring, Budget)
- Optional notes field for additional details
- Date picker for accurate expense recording

### 📋 View Expenses
- **Advanced filtering** by category and date range
- **Multiple sorting options** (newest, oldest, amount high-to-low, amount low-to-high)
- **Data table view** with all expense details
- Summary statistics for filtered expenses
- Inline delete functionality

### 📈 Advanced Analytics
- **Category Analysis**: Distribution charts and spending by category
- **Time Analysis**: Monthly and weekly spending trends
- **Payment Analysis**: Payment method breakdown and distribution

### ⚙️ Settings & Export
- **CSV Export**: Download expenses as CSV file
- **JSON Export**: Download expenses as JSON file
- **Data Management**: Clear all expenses with confirmation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dhivakar452/MSME-HACKATHON-.git
cd MSME-HACKATHON-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run expense_tracker.py
```

4. Open your browser to `http://localhost:8501`

## 📱 UI/UX Highlights

### Modern Design
- **Dark theme** with cyan accent colors (#00D9FF)
- **Gradient backgrounds** and smooth transitions
- **Responsive layout** that works on all screen sizes
- **Custom CSS** for enhanced visual appeal

### Navigation
- **Sidebar navigation** for easy page switching
- **Radio buttons** for quick page selection
- **Live stats** displayed in sidebar for at-a-glance overview

### Interactive Components
- **Plotly charts** for interactive data visualization
- **Multi-select filters** for flexible data filtering
- **Date pickers** for date range selection
- **Inline actions** for quick operations

## 📂 File Structure

```
├── expense_tracker.py      # Main application
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── CONFIG.md              # Configuration guide
└── expenses.json          # Local data storage (auto-created)
```

## 💾 Data Storage

Expenses are stored locally in `expenses.json` file with the following structure:

```json
{
  "id": "timestamp",
  "description": "string",
  "amount": "float",
  "category": "string",
  "date": "ISO datetime",
  "payment_method": "string",
  "tags": ["array"],
  "notes": "string"
}
```

## 🎨 Customization

### Categories
Edit the category list in the "Add Expense" section:
```python
category = st.selectbox(
    "Category",
    ["Food", "Transport", "Entertainment", "Shopping", "Healthcare", "Utilities", "Education", "Other"]
)
```

### Colors
Customize the color scheme in the CSS section:
```css
:root {
    --primary-color: #00D9FF;
    --secondary-color: #6C5CE7;
    --danger-color: #FF6B6B;
    --success-color: #00B894;
    --warning-color: #FDCB6E;
}
```

### Payment Methods
Update payment methods in the "Add Expense" section:
```python
payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "Digital Wallet"])
```

## 🔧 Features Deep Dive

### Dashboard
- Shows comprehensive spending overview
- Displays metrics for total, average, max expenses
- Visualizes category distribution with pie charts
- Tracks 30-day spending trends

### Expense Management
- Add expenses with full details
- View all expenses with powerful filters
- Sort by date or amount
- Delete expenses individually

### Analytics
- Category-wise spending analysis
- Monthly and weekly trends
- Payment method statistics
- Detailed breakdowns and comparisons

### Export & Backup
- Export data in CSV format for Excel
- Export data in JSON format for backup
- Download with automatic timestamps

## 📊 Example Workflow

1. **Start**: Open the app and go to "Add Expense"
2. **Enter**: Fill in your expense details
3. **Track**: View in "View Expenses" page
4. **Analyze**: Check "Analytics" for insights
5. **Export**: Download your data anytime

## 🐛 Troubleshooting

### Expenses not saving?
- Ensure the script has write permissions
- Check if `expenses.json` exists in the same directory

### Charts not displaying?
- Verify plotly is installed: `pip install plotly`
- Check your data has valid amounts

### Slow performance?
- Clear old expenses regularly
- Use date filters to limit data

## 🚀 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Budget limits and alerts
- [ ] Recurring expenses
- [ ] Multi-user support
- [ ] Receipt image attachment
- [ ] Email reports
- [ ] Mobile app version
- [ ] Cloud backup

## 📄 License

MIT License - feel free to use and modify

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📞 Support

For issues or questions, please create an issue in the repository.

## 👨‍💻 Author

Created with ❤️ for better expense tracking

---

**Happy Tracking! 💰**