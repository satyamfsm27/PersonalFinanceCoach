import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Personal Finance & Budgeting Coach",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        API_KEY = None

MODEL = "openai/gpt-oss-20b"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ============================================================
# GEMINI CLIENT
# ============================================================

MODEL = "gemini-3.6-flash"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# ============================================================
# FINANCIAL CALCULATION ENGINE
# ============================================================

def calculate_financial_plan(
    income,
    expenses,
    current_savings,
    financial_goal,
    goal_months,
    extra_monthly_saving=0
):

    income = float(income)
    expenses = float(expenses)
    current_savings = float(current_savings)
    financial_goal = float(financial_goal)
    goal_months = float(goal_months)
    extra_monthly_saving = float(extra_monthly_saving)

    # Monthly cash flow
    monthly_surplus = income - expenses

    # Savings rate
    savings_rate = (
        (monthly_surplus / income) * 100
        if income > 0
        else 0
    )

    # Goal gap
    goal_gap = max(financial_goal - current_savings, 0)

    # Required monthly saving to achieve goal within target period
    required_monthly_saving = (
        goal_gap / goal_months
        if goal_months > 0
        else 0
    )

    # Base saving
    base_monthly_saving = max(monthly_surplus, 0)

    # Saving after hypothetical extra contribution
    planned_monthly_saving = (
        base_monthly_saving
        + max(extra_monthly_saving, 0)
    )

    # Projected savings
    projected_savings = (
        current_savings
        + planned_monthly_saving * goal_months
    )

    # Months required to reach goal
    if goal_gap <= 0:
        months_to_goal = 0

    elif planned_monthly_saving > 0:
        months_to_goal = (
            goal_gap / planned_monthly_saving
        )

    else:
        months_to_goal = None

    # Goal status
    if goal_gap <= 0:

        goal_status = "Goal already achieved"

    elif monthly_surplus < 0:

        goal_status = "Not achievable from current cash flow"

    elif projected_savings >= financial_goal:

        goal_status = "Achievable from current cash flow"

    else:

        goal_status = "Additional monthly saving required"

    # Savings assessment
    if income <= 0:

        savings_assessment = "Income is not available"

    elif monthly_surplus < 0:

        savings_assessment = "Expenses exceed income"

    elif savings_rate < 10:

        savings_assessment = "Below 10% savings rate"

    elif savings_rate < 20:

        savings_assessment = "10–20% savings rate"

    else:

        savings_assessment = "20%+ savings rate"

    # Emergency fund
    emergency_fund_3_months = expenses * 3
    emergency_fund_6_months = expenses * 6

    return {

        "monthly_income": round(income, 2),

        "monthly_expenses": round(expenses, 2),

        "current_savings": round(current_savings, 2),

        "financial_goal": round(financial_goal, 2),

        "goal_months": round(goal_months, 2),

        "monthly_surplus": round(monthly_surplus, 2),

        "savings_rate_percent": round(savings_rate, 2),

        "goal_gap": round(goal_gap, 2),

        "required_monthly_saving": round(
            required_monthly_saving,
            2
        ),

        "extra_monthly_saving": round(
            extra_monthly_saving,
            2
        ),

        "planned_monthly_saving": round(
            planned_monthly_saving,
            2
        ),

        "projected_savings": round(
            projected_savings,
            2
        ),

        "months_to_goal": (
            round(months_to_goal, 2)
            if months_to_goal is not None
            else None
        ),

        "goal_status": goal_status,

        "savings_assessment": savings_assessment,

        "emergency_fund_3_months": round(
            emergency_fund_3_months,
            2
        ),

        "emergency_fund_6_months": round(
            emergency_fund_6_months,
            2
        )
    }


# ============================================================
# SESSION STATE
# ============================================================

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []

if "last_tool_result" not in st.session_state:
    st.session_state.last_tool_result = None


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI Personal Finance and Budgeting Coach.

Your role is to help users understand their personal cash flow,
savings, budgeting, financial goals, emergency funds, and
general financial concepts.

IMPORTANT ARCHITECTURE RULE:

Python performs all financial calculations.

Python outputs are authoritative.

Never manually recalculate, estimate, approximate, or contradict
a number returned by Python.

If a calculation is required, the application will provide a
verified Python calculation result to you.

Use the exact numbers from that result.

Do not invent financial numbers.

Do not perform additional arithmetic after receiving a Python result.

If a number is not explicitly returned by Python, do not calculate
it yourself.

You may explain the meaning of the verified numbers in simple
language.

--------------------------------------------------
FINANCIAL GOALS
--------------------------------------------------

For questions involving:

- monthly savings
- monthly surplus
- savings rate
- financial goal feasibility
- required monthly savings
- projected savings
- months required to reach a goal
- what-if scenarios

use the verified Python calculation provided by the application.

The Python field "months_to_goal" is the authoritative value
for the time required to reach the goal.

Do not calculate another value from it.

--------------------------------------------------
WHAT-IF SCENARIOS
--------------------------------------------------

Users may ask questions such as:

"What if I save ₹5,000 more every month?"

"What if my expenses decrease?"

"What if my income increases?"

The application may run Python using hypothetical values.

Clearly explain that these are hypothetical scenarios.

Never present hypothetical results as guaranteed outcomes.

--------------------------------------------------
EMERGENCY FUND
--------------------------------------------------

You may explain general emergency-fund concepts.

Use the verified Python values for:

- 3-month emergency fund
- 6-month emergency fund

Do not manually calculate these values.

--------------------------------------------------
GENERAL FINANCIAL EDUCATION
--------------------------------------------------

You may explain:

- budgeting
- cash flow
- savings
- emergency funds
- diversification
- risk and return
- inflation
- compounding
- financial planning
- behavioural finance
- asset allocation at a general educational level

Do not provide personalized instructions to buy or sell
specific stocks, mutual funds, cryptocurrencies, insurance
products, or other specific financial products.

Do not tell the user where they should invest their money.

Do not guarantee investment returns.

--------------------------------------------------
CONVERSATION
--------------------------------------------------

Maintain conversational context.

If the user's question is unclear or required information
is missing, ask a concise follow-up question.

Use simple language suitable for someone learning personal finance.

Be helpful and conversational rather than overly technical.

When presenting calculated results, make it clear that the
numbers were verified by the Python financial calculation engine.

--------------------------------------------------
SAFETY
--------------------------------------------------

This application is educational and informational.

Do not claim to be a licensed financial advisor.

Do not guarantee outcomes.

Do not make investment recommendations involving specific
financial products.

--------------------------------------------------
IMPORTANT
--------------------------------------------------

Never override or contradict Python calculations.

Never perform hidden arithmetic yourself.

Never invent missing financial data.

The verified Python result is the single source of truth
for financial calculations.
"""


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("💰 Financial Profile")

income = st.sidebar.number_input(
    "Monthly Income",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

expenses = st.sidebar.number_input(
    "Monthly Expenses",
    min_value=0.0,
    value=47000.0,
    step=1000.0
)

current_savings = st.sidebar.number_input(
    "Current Savings",
    min_value=0.0,
    value=250000.0,
    step=5000.0
)

financial_goal = st.sidebar.number_input(
    "Financial Goal",
    min_value=0.0,
    value=500000.0,
    step=5000.0
)

goal_months = st.sidebar.number_input(
    "Time to Goal (Months)",
    min_value=1.0,
    value=18.0,
    step=1.0
)

risk_preference = st.sidebar.selectbox(
    "Risk Preference",
    [
        "Conservative",
        "Moderate",
        "Aggressive"
    ]
)


# ============================================================
# MAIN TITLE
# ============================================================

st.title("💰 AI Personal Finance & Budgeting Coach")

st.write(
    "An AI-powered personal finance assistant combining "
    "deterministic Python calculations with conversational AI."
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.subheader("How the AI Finance Coach Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 👤")
    st.write("User Input")

with col2:
    st.markdown("### 🤖")
    st.write("Finance Agent")

with col3:
    st.markdown("### 🐍")
    st.write("Python Financial Engine")

with col4:
    st.markdown("### ✅")
    st.write("Verified Result")


st.divider()


# ============================================================
# CURRENT FINANCIAL CALCULATION
# ============================================================

result = calculate_financial_plan(
    income,
    expenses,
    current_savings,
    financial_goal,
    goal_months
)

st.session_state.last_tool_result = result


# ============================================================
# FINANCIAL SNAPSHOT
# ============================================================

st.subheader("Financial Snapshot")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Monthly Income",
        f"₹{income:,.0f}"
    )

with col2:
    st.metric(
        "Monthly Expenses",
        f"₹{expenses:,.0f}"
    )

with col3:
    st.metric(
        "Monthly Surplus",
        f"₹{result['monthly_surplus']:,.0f}"
    )

with col4:
    st.metric(
        "Savings Rate",
        f"{result['savings_rate_percent']:.1f}%"
    )


# ============================================================
# INITIAL ASSESSMENT
# ============================================================

st.subheader("Initial Assessment")

if result["monthly_surplus"] > 0:

    st.success(
        f"Your current monthly surplus is "
        f"₹{result['monthly_surplus']:,.0f}."
    )

elif result["monthly_surplus"] == 0:

    st.warning(
        "Your income and expenses are currently equal."
    )

else:

    st.error(
        "Your expenses currently exceed your income."
    )


st.write(
    f"**Savings assessment:** "
    f"{result['savings_assessment']}"
)


# ============================================================
# GOAL FEASIBILITY
# ============================================================

st.subheader("🎯 Goal Feasibility Analysis")

goal_col1, goal_col2, goal_col3 = st.columns(3)

with goal_col1:

    st.metric(
        "Goal",
        f"₹{financial_goal:,.0f}"
    )

with goal_col2:

    st.metric(
        "Required Monthly Saving",
        f"₹{result['required_monthly_saving']:,.0f}"
    )

with goal_col3:

    st.metric(
        "Projected Savings",
        f"₹{result['projected_savings']:,.0f}"
    )


if result["goal_status"] == "Goal already achieved":

    st.success(result["goal_status"])

elif result["goal_status"] == "Achievable from current cash flow":

    st.success(result["goal_status"])

elif result["goal_status"] == "Additional monthly saving required":

    st.warning(result["goal_status"])

else:

    st.error(result["goal_status"])


# ============================================================
# AI FINANCIAL ANALYSIS
# ============================================================

st.subheader("🤖 AI Financial Analysis")

analysis_prompt = f"""
Analyze the user's financial situation using ONLY the verified
Python calculation below.

User profile:

Monthly income: ₹{income:,.2f}
Monthly expenses: ₹{expenses:,.2f}
Current savings: ₹{current_savings:,.2f}
Financial goal: ₹{financial_goal:,.2f}
Goal timeline: {goal_months} months
Risk preference: {risk_preference}

Verified Python result:

{json.dumps(result, indent=2)}

Explain:

1. Current cash-flow position
2. Savings situation
3. Goal feasibility
4. What the required monthly saving means
5. Emergency-fund position
6. Practical budgeting considerations

Use ONLY the values explicitly returned by Python.

Do not perform any additional calculations.
Do not invent or approximate numbers.

Keep the explanation concise and easy to understand.
"""

try:

    analysis_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ],
        temperature=0.2
    )

    analysis_text = analysis_response.choices[0].message.content

    st.write(analysis_text)

except Exception as e:

    st.error(
        f"AI analysis could not be generated: {str(e)}"
    )


# ============================================================
# EMERGENCY FUND
# ============================================================

st.subheader("🛡️ Emergency Fund")

em_col1, em_col2 = st.columns(2)

with em_col1:

    st.metric(
        "3-Month Emergency Fund",
        f"₹{result['emergency_fund_3_months']:,.0f}"
    )

with em_col2:

    st.metric(
        "6-Month Emergency Fund",
        f"₹{result['emergency_fund_6_months']:,.0f}"
    )


st.caption(
    "Emergency-fund figures are calculated by the Python "
    "financial engine using monthly expenses."
)


# ============================================================
# CONVERSATIONAL FINANCE AGENT
# ============================================================

st.divider()

st.subheader("💬 Conversational Finance Agent")

st.write(
    "Ask questions about your budget, savings, financial goals, "
    "emergency fund, or what-if scenarios."
)


# Display previous messages

for message in st.session_state.agent_messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "Ask your finance coach a question..."
)


if user_prompt:

    # Add user message
    st.session_state.agent_messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)


    # Current verified financial context
    financial_context = f"""
CURRENT VERIFIED FINANCIAL PROFILE

Monthly income:
₹{income:,.2f}

Monthly expenses:
₹{expenses:,.2f}

Current savings:
₹{current_savings:,.2f}

Financial goal:
₹{financial_goal:,.2f}

Goal timeline:
{goal_months} months

Risk preference:
{risk_preference}

VERIFIED PYTHON CALCULATION:

{json.dumps(result, indent=2)}
"""


    # Complete conversation
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(
        st.session_state.agent_messages
    )

    messages.append(
        {
            "role": "system",
            "content": financial_context
        }
    )


    # ========================================================
    # AI RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your finances..."):

            try:

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.2
                )

                assistant_response = (
                    response.choices[0]
                    .message
                    .content
                )

                st.markdown(assistant_response)

                st.session_state.agent_messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )

            except Exception as e:

                error_message = (
                    f"Unable to connect to the AI service.\n\n"
                    f"Error: {str(e)}"
                )

                st.error(error_message)


# ============================================================
# VERIFIED PYTHON RESULT
# ============================================================

st.divider()

with st.expander("🔍 View latest verified Python calculation"):

    st.json(
        st.session_state.last_tool_result
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.caption(
    "Educational disclaimer: This AI Finance Coach provides "
    "general financial education and budgeting assistance. "
    "It does not provide personalized investment advice, "
    "guaranteed returns, or recommendations to buy or sell "
    "specific financial products."
)
