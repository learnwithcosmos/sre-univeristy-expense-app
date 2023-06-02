import calendar
from datetime import datetime
from streamlit_option_menu import option_menu

import streamlit as st
import plotly.graph_objects as go

# Initialize SessionState
class SessionState:
    def __init__(self):
        self.year = datetime.today().year
        self.month = calendar.month_name[datetime.today().month]
        self.incomes = {}
        self.expenses = {}
        self.comment = ""

state = SessionState()

#  settings ------
incomes = ["salary", "Blog", "Other Income"]
expenses = ["Rent", "Food", "Travel", "Bills", "Shopping", "Other Expense"]
currency = "USD"
page_title = "Budget App"
page_icon = "💰"
layout = "wide"


st.set_page_config(page_icon=page_icon, page_title=page_title, layout=layout)
st.title(page_title +  ' 📈' + page_icon)

# --- Hide streamlit style

hide_st_style = """
    <style>
        #MainMenu { visibility: hidden; }
        footer {visibility: hidden;}    
        header {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)
    

# --- Navigation ----
# selected = option_menu(
#     menu_title=None,
#     options=["Data entry", "Data Visualization"],
#     icons=["pencil-fill", "bar-chart-fill"],
#     orientation="horizontal",
# )


# -- dropdown menu

years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name)[1:]

# -- input form 

st.header(f"Data entry in {currency}")

with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month", months, key="month")
    col2.selectbox("Select Year", years, key="year")
    
    "---"
    with st.expander("Income"):
        for income in incomes:
            state.incomes[income] = st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
    with st.expander("Expense"):
        for expense in expenses:
            state.expenses[expense] = st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=expense)
    with st.expander("Comment"):
        comment = st.text_area("", placeholder="Enter a comment here...")
        
    "---"
    submit_button = st.form_submit_button(label="Save Data")
    
    if submit_button:
        period = str(state.year) + "_" + str(state.month)
        # TODO: Insert values into database
        st.write(f"incomes: {state.incomes}")
        st.write(f"expenses: {state.expenses}")
        st.success("Data saved successfully")
        
# --- Data Visualization

# -- Plot period ---
st.header("Data Visualization")
with st.form("saved_periods"):
    period = st.selectbox("Select Period", ["{state.year}-{state.month}"])
    submit_button = st.form_submit_button(label="Show Data")
    
    if submit_button:
        # TODO: Get data from database
        
        # Current metrics
        total_income = sum(state.incomes.values())
        total_expense = sum(state.expenses.values())
        remaining_budget = total_income - total_expense
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"{total_income} {currency}")
        col2.metric("Total Expense", f"{total_expense} {currency}")
        col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
        st.text(f"Comment: {state.comment}")
        
        # Create sankey chart
        label = list(state.incomes.keys()) + ["Total Income"] +  list(state.expenses.keys())
        source = list(range(len(state.incomes))) + [len(state.incomes)] * len(state.expenses)
        target = [len(state.incomes)] * len(state.incomes) + [label.index(expense) for expense in state.expenses.keys()]
        value = list(state.incomes.values()) + list(state.expenses.values())
        
        # Data to dict, dict to sankey
        link = dict(source=source, target=target, value=value)
        node = dict(label=label, pad=20, thickness=40, color=["blue"] * len(state.incomes) + ["green"] + ["red"] * len(state.expenses))
        data = go.Sankey(link=link, node=node)
        
        #  plot
        fig = go.Figure(data)
        fig.update_layout(margin=dict(l=10, r=10, t=5, b=5))
        st.plotly_chart(fig, use_container_width=True)
            
