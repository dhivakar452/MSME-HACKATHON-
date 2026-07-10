import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://streamlit.io",
        "Report a bug": "https://github.com",
        "About": "Advanced Expense Tracker v1.0"
    }
)

# Custom CSS for modern UI
st.markdown("""
<style>
    :root {
        --primary-color: #00D9FF;
        --secondary-color: #6C5CE7;
        --danger-color: #FF6B6B;
        --success-color: #00B894;
        --warning-color: #FDCB6E;
        --dark-bg: #0F1419;
        --card-bg: #1a1f2e;
    }
    
    .main {
        background-color: var(--dark-bg);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, #252d3d 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid var(--primary-color);
        box-shadow: 0 4px 6px rgba(0, 217, 255, 0.1);
    }
    
    .expense-item {
        background: var(--card-bg);
        padding: 16px;
        border-radius: 8px;
        border: 1px solid rgba(0, 217, 255, 0.2);
        margin-bottom: 12px;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary-color);
    }
    
    h1 {
        color: var(--primary-color);
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
    }
    
    h2 {
        color: var(--secondary-color);
    }
    
    .category-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence
DATA_FILE = "expenses.json"

def load_expenses():
    """Load expenses from JSON file"""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    """Save expenses to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2, default=str)

def get_category_color(category):
    """Get color for category badge"""
    colors = {
        "Food": "#FF6B6B",
        "Transport": "#4ECDC4",
        "Entertainment": "#FFE66D",
        "Shopping": "#A8E6CF",
        "Healthcare": "#FF8B94",
        "Utilities": "#95E1D3",
        "Education": "#C7CEEA",
        "Other": "#B19CD9"
    }
    return colors.get(category, "#95E1D3")

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💰 Expense Tracker Pro")
with col2:
    st.markdown("")
    st.markdown("")
    if st.button("🔄 Refresh", help="Refresh data"):
        st.rerun()

st.markdown("---")

# Sidebar for navigation
with st.sidebar:
    st.header("🎯 Navigation")
    page = st.radio(
        "Select View:",
        ["📊 Dashboard", "➕ Add Expense", "📋 View Expenses", "📈 Analytics", "⚙️ Settings"]
    )
    st.markdown("---")
    
    # Stats in sidebar
    if st.session_state.expenses:
        total_expenses = sum(e["amount"] for e in st.session_state.expenses)
        avg_expense = total_expenses / len(st.session_state.expenses)
        st.info(f"💵 Total Spent: ${total_expenses:.2f}\n\n📌 Avg Expense: ${avg_expense:.2f}")

# Page: Dashboard
if page == "📊 Dashboard":
    st.header("Dashboard Overview")
    
    expenses = st.session_state.expenses
    
    if not expenses:
        st.warning("No expenses recorded yet. Start by adding your first expense!")
    else:
        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_expenses = df["amount"].sum()
            st.metric("Total Expenses", f"${total_expenses:.2f}", 
                     delta=f"+${df[df['date'] > datetime.now() - timedelta(days=7)]['amount'].sum():.2f} (7d)")
        
        with col2:
            avg_expense = df["amount"].mean()
            st.metric("Average Expense", f"${avg_expense:.2f}")
        
        with col3:
            max_expense = df["amount"].max()
            st.metric("Largest Expense", f"${max_expense:.2f}")
        
        with col4:
            count = len(df)
            st.metric("Total Transactions", count)
        
        st.markdown("---")
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Expenses by Category")
            category_data = df.groupby("category")["amount"].sum().sort_values(ascending=False)
            fig_pie = px.pie(
                values=category_data.values,
                names=category_data.index,
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            fig_pie.update_layout(
                template="plotly_dark",
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("📈 Spending Trend (Last 30 Days)")
            last_30_days = df[df["date"] > datetime.now() - timedelta(days=30)].copy()
            daily_spend = last_30_days.groupby(last_30_days["date"].dt.date)["amount"].sum()
            
            fig_line = px.line(
                x=daily_spend.index,
                y=daily_spend.values,
                markers=True,
                title="Daily Spending"
            )
            fig_line.update_layout(
                template="plotly_dark",
                xaxis_title="Date",
                yaxis_title="Amount ($)",
                height=400,
                hovermode="x unified"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        st.markdown("---")
        
        # Recent Expenses
        st.subheader("🕐 Recent Expenses")
        recent_df = df.sort_values("date", ascending=False).head(5)
        for idx, row in recent_df.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{row['description']}**")
                st.caption(f"{row['date'].strftime('%Y-%m-%d %H:%M')}")
            with col2:
                st.write(f"${row['amount']:.2f}")
            with col3:
                st.write(f"`{row['category']}`")
            with col4:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.expenses.pop(idx)
                    save_expenses(st.session_state.expenses)
                    st.rerun()

# Page: Add Expense
elif page == "➕ Add Expense":
    st.header("Add New Expense")
    
    col1, col2 = st.columns(2)
    
    with col1:
        description = st.text_input("Description", placeholder="e.g., Grocery Shopping")
        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    
    with col2:
        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Entertainment", "Shopping", "Healthcare", "Utilities", "Education", "Other"]
        )
        expense_date = st.date_input("Date", datetime.now())
    
    st.markdown("---")
    
    # Payment method and notes
    col1, col2 = st.columns(2)
    
    with col1:
        payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "Digital Wallet"])
    
    with col2:
        tags = st.multiselect("Tags", ["Urgent", "Work", "Personal", "Recurring", "Budget"])
    
    notes = st.text_area("Notes (Optional)", placeholder="Add any additional details...")
    
    st.markdown("---")
    
    if st.button("✅ Add Expense", use_container_width=True):
        if not description:
            st.error("Please enter a description")
        elif amount <= 0:
            st.error("Please enter a valid amount")
        else:
            new_expense = {
                "id": datetime.now().timestamp(),
                "description": description,
                "amount": amount,
                "category": category,
                "date": datetime.combine(expense_date, datetime.now().time()).isoformat(),
                "payment_method": payment_method,
                "tags": tags,
                "notes": notes
            }
            st.session_state.expenses.append(new_expense)
            save_expenses(st.session_state.expenses)
            st.success(f"✅ Expense of ${amount:.2f} added successfully!")
            st.balloons()

# Page: View Expenses
elif page == "📋 View Expenses":
    st.header("View All Expenses")
    
    if not st.session_state.expenses:
        st.info("No expenses recorded yet.")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "Filter by Category",
                ["All"] + list(set(e["category"] for e in st.session_state.expenses)),
                default=["All"]
            )
        
        with col2:
            date_range = st.date_input("Date Range", 
                                      value=(datetime.now() - timedelta(days=30), datetime.now()),
                                      max_value=datetime.now())
        
        with col3:
            sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Amount (High to Low)", "Amount (Low to High)"])
        
        st.markdown("---")
        
        # Apply filters
        df = pd.DataFrame(st.session_state.expenses)
        df["date"] = pd.to_datetime(df["date"])
        
        if "All" not in category_filter:
            df = df[df["category"].isin(category_filter)]
        
        if len(date_range) == 2:
            df = df[(df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])]
        
        # Sort
        if "Newest" in sort_by:
            df = df.sort_values("date", ascending=False)
        elif "Oldest" in sort_by:
            df = df.sort_values("date", ascending=True)
        elif "High to Low" in sort_by:
            df = df.sort_values("amount", ascending=False)
        else:
            df = df.sort_values("amount", ascending=True)
        
        # Display table
        st.dataframe(
            df[["description", "amount", "category", "date", "payment_method"]].rename(
                columns={
                    "description": "Description",
                    "amount": "Amount ($)",
                    "category": "Category",
                    "date": "Date",
                    "payment_method": "Payment Method"
                }
            ),
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total in Range", f"${df['amount'].sum():.2f}")
        with col2:
            st.metric("Number of Expenses", len(df))
        with col3:
            st.metric("Average Expense", f"${df['amount'].mean():.2f}")

# Page: Analytics
elif page == "📈 Analytics":
    st.header("Advanced Analytics")
    
    if not st.session_state.expenses:
        st.info("No expenses to analyze yet.")
    else:
        df = pd.DataFrame(st.session_state.expenses)
        df["date"] = pd.to_datetime(df["date"])
        
        tab1, tab2, tab3 = st.tabs(["📊 Category Analysis", "📅 Time Analysis", "💳 Payment Analysis"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Category Distribution")
                category_data = df.groupby("category")["amount"].agg(["sum", "count"])
                category_data.columns = ["Total Spent", "Count"]
                st.dataframe(category_data, use_container_width=True)
            
            with col2:
                st.subheader("Category Bar Chart")
                fig_bar = px.bar(
                    df.groupby("category")["amount"].sum().sort_values(ascending=True),
                    orientation="h",
                    color_discrete_sequence=["#00D9FF"]
                )
                fig_bar.update_layout(template="plotly_dark", showlegend=False, height=400)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Monthly Spending")
                monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
                fig_monthly = px.bar(
                    x=monthly.index.astype(str),
                    y=monthly.values,
                    color_discrete_sequence=["#6C5CE7"]
                )
                fig_monthly.update_layout(template="plotly_dark", height=400,
                                         xaxis_title="Month", yaxis_title="Amount ($)")
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            with col2:
                st.subheader("Weekly Spending")
                weekly = df.groupby(df["date"].dt.to_period("W"))["amount"].sum()
                fig_weekly = px.area(
                    x=weekly.index.astype(str),
                    y=weekly.values,
                    fill="tozeroy"
                )
                fig_weekly.update_layout(template="plotly_dark", height=400,
                                        xaxis_title="Week", yaxis_title="Amount ($)")
                st.plotly_chart(fig_weekly, use_container_width=True)
        
        with tab3:
            st.subheader("Payment Method Distribution")
            payment_data = df.groupby("payment_method")["amount"].agg(["sum", "count"])
            payment_data.columns = ["Total Spent", "Count"]
            st.dataframe(payment_data, use_container_width=True)
            
            fig_payment = px.pie(
                values=df.groupby("payment_method")["amount"].sum().values,
                names=df.groupby("payment_method")["amount"].sum().index,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_payment.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig_payment, use_container_width=True)

# Page: Settings
elif page == "⚙️ Settings":
    st.header("Settings & Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Export Data")
        if st.session_state.expenses:
            # Export as CSV
            df = pd.DataFrame(st.session_state.expenses)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Export as JSON
            json_data = json.dumps(st.session_state.expenses, indent=2, default=str)
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        st.subheader("⚠️ Danger Zone")
        if st.button("🗑️ Clear All Expenses", use_container_width=True):
            if st.checkbox("⚠️ I understand this action cannot be undone"):
                st.session_state.expenses = []
                save_expenses([])
                st.success("✅ All expenses have been cleared!")
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>💰 Expense Tracker Pro v1.0 | Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
