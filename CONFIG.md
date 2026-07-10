# Expense Tracker Pro - Configuration Guide

## Application Settings

### Theme Configuration
The app uses a modern dark theme with customizable colors. All color values are CSS variables defined in the main app.

**Current Color Scheme:**
- Primary: `#00D9FF` (Cyan)
- Secondary: `#6C5CE7` (Purple)
- Danger: `#FF6B6B` (Red)
- Success: `#00B894` (Green)
- Warning: `#FDCB6E` (Yellow)

### Categories
Default expense categories are:
1. Food
2. Transport
3. Entertainment
4. Shopping
5. Healthcare
6. Utilities
7. Education
8. Other

### Payment Methods
Supported payment methods:
1. Cash
2. Credit Card
3. Debit Card
4. Digital Wallet

### Tags
Pre-defined tags for expense organization:
- Urgent
- Work
- Personal
- Recurring
- Budget

## Streamlit Configuration

Create `~/.streamlit/config.toml` for advanced Streamlit settings:

```toml
[theme]
primaryColor = "#00D9FF"
backgroundColor = "#0F1419"
secondaryBackgroundColor = "#1a1f2e"
textColor = "#FFFFFF"
font = "sans serif"

[client]
showErrorDetails = true
```

## Data Management

### Local Storage
- Data is stored in `expenses.json` in the same directory
- Automatically created on first expense entry
- No database setup required

### Backup Strategy
1. Regular exports recommended
2. Download CSV for spreadsheet analysis
3. Download JSON for complete backup

## Performance Tips

1. **Large Datasets**: Use date filters to improve chart performance
2. **Export Regularly**: Keep local backups of exported data
3. **Clear Old Data**: Periodically clean up old expenses if needed

## Deployment Options

### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Store `expenses.json` in data directory

### Local Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY expense_tracker.py .
CMD ["streamlit", "run", "expense_tracker.py"]
```

### Environment Variables
Set these for cloud deployment:
- `DATA_DIR`: Directory for storing expenses.json
- `APP_PORT`: Port to run on (default: 8501)

## Analytics Reference

### Metrics Displayed
- **Total Expenses**: Sum of all expenses
- **Average Expense**: Mean of all expenses
- **Largest Expense**: Maximum transaction amount
- **Transaction Count**: Total number of entries

### Visualizations
- **Pie Chart**: Category distribution
- **Line Chart**: 30-day trend
- **Bar Chart**: Category comparison
- **Area Chart**: Weekly trends
- **Data Tables**: Detailed breakdowns

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Keyboard Shortcuts

While using the app:
- `R` or Click Refresh button to reload data
- `Ctrl+L` to clear filters
- `Enter` to submit forms

## Troubleshooting

### Issue: "expenses.json not found"
**Solution**: Add first expense to auto-create file

### Issue: Charts not rendering
**Solution**: Install/upgrade plotly: `pip install --upgrade plotly`

### Issue: Slow performance with large datasets
**Solution**: Filter by date range or export old data

### Issue: Data loss after app restart
**Solution**: Ensure you're in the correct directory where expenses.json is saved
