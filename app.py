import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/free"

if not API_KEY:
    st.error("OPENROUTER_API_KEY not found in .env file.")
    st.stop()

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Personal Finance Coach",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #172554;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #172554;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .success-box {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .warning-box {
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">💰 AI Personal Finance & Budgeting Coach</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An AI-powered financial planning assistant that combines '
    'conversational AI with verified Python calculations.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ARCHITECTURE BANNER
# ============================================================

st.markdown(
    '<div style="'
    'background:linear-gradient(90deg,#eff6ff,#f8fafc);'
    'border:1px solid #dbeafe;'
    'border-radius:12px;'
    'padding:16px 20px;'
    'margin:15px 0 25px 0;'
    '">'

    '<div style="'
    'font-size:15px;'
    'font-weight:600;'
    'color:#172554;'
    'margin-bottom:10px;'
    '">'
    '⚙️ How the AI Finance Coach works'
    '</div>'

    '<div style="'
    'display:flex;'
    'align-items:center;'
    'gap:12px;'
    'flex-wrap:wrap;'
    'color:#475569;'
    'font-size:14px;'
    '">'

    '<span>👤 <strong>User</strong></span>'
    '<span>→</span>'
    '<span>🤖 <strong>AI Finance Agent</strong></span>'
    '<span>→</span>'
    '<span>🐍 <strong>Python Financial Tool</strong></span>'
    '<span>→</span>'
    '<span>✅ <strong>Verified Result</strong></span>'
    '<span>→</span>'
    '<span>💬 <strong>AI Explanation</strong></span>'

    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DETERMINISTIC FINANCIAL CALCULATOR
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

    # --------------------------------------------------------
    # CASH FLOW
    # --------------------------------------------------------

    monthly_surplus = income - expenses

    # --------------------------------------------------------
    # SAVINGS RATE
    # --------------------------------------------------------

    savings_rate = (
        (monthly_surplus / income) * 100
        if income > 0
        else 0
    )

    # --------------------------------------------------------
    # GOAL GAP
    # --------------------------------------------------------

    goal_gap = max(
        financial_goal - current_savings,
        0
    )

    # --------------------------------------------------------
    # REQUIRED MONTHLY SAVING
    # --------------------------------------------------------

    required_monthly_saving = (
        goal_gap / goal_months
        if goal_months > 0
        else 0
    )

    # --------------------------------------------------------
    # CURRENT MONTHLY SAVING
    # --------------------------------------------------------

    base_monthly_saving = max(
        monthly_surplus,
        0
    )

    # --------------------------------------------------------
    # EXTRA SAVING REQUIRED
    #
    # This is explicitly calculated by Python so that the AI
    # does not have to perform this calculation itself.
    # --------------------------------------------------------

    additional_monthly_saving_required = max(
        required_monthly_saving - base_monthly_saving,
        0
    )

    # --------------------------------------------------------
    # WHAT-IF MONTHLY SAVING
    # --------------------------------------------------------

    planned_monthly_saving = (
        base_monthly_saving
        + max(extra_monthly_saving, 0)
    )

    # --------------------------------------------------------
    # PROJECTED SAVINGS
    # --------------------------------------------------------

    projected_savings = (
        current_savings
        + planned_monthly_saving * goal_months
    )

    # --------------------------------------------------------
    # MONTHS TO GOAL
    # --------------------------------------------------------

    if goal_gap <= 0:

        months_to_goal = 0

    elif planned_monthly_saving > 0:

        months_to_goal = (
            goal_gap / planned_monthly_saving
        )

    else:

        months_to_goal = None

    # --------------------------------------------------------
    # GOAL STATUS
    # --------------------------------------------------------

    if goal_gap <= 0:

        goal_status = "Goal already achieved"

    elif monthly_surplus < 0:

        goal_status = "Not achievable from current cash flow"

    elif projected_savings >= financial_goal:

        goal_status = "Achievable from current cash flow"

    else:

        goal_status = "Additional monthly saving required"

    # --------------------------------------------------------
    # SAVINGS ASSESSMENT
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # EMERGENCY FUND
    # --------------------------------------------------------

    emergency_fund_3_months = expenses * 3

    emergency_fund_6_months = expenses * 6

    # --------------------------------------------------------
    # VERIFIED OUTPUT
    # --------------------------------------------------------

    return {

        "monthly_income": round(
            income,
            2
        ),

        "monthly_expenses": round(
            expenses,
            2
        ),

        "current_savings": round(
            current_savings,
            2
        ),

        "financial_goal": round(
            financial_goal,
            2
        ),

        "goal_months": round(
            goal_months,
            2
        ),

        "monthly_surplus": round(
            monthly_surplus,
            2
        ),

        "savings_rate_percent": round(
            savings_rate,
            2
        ),

        "goal_gap": round(
            goal_gap,
            2
        ),

        "required_monthly_saving": round(
            required_monthly_saving,
            2
        ),

        "additional_monthly_saving_required": round(
            additional_monthly_saving_required,
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
# SIDEBAR
# ============================================================

st.sidebar.title("💰 Financial Profile")

st.sidebar.markdown(
    "Enter your financial information below."
)

income = st.sidebar.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    value=50000.0,
    step=5000.0
)

expenses = st.sidebar.number_input(
    "Monthly Expenses (₹)",
    min_value=0.0,
    value=47000.0,
    step=5000.0
)

current_savings = st.sidebar.number_input(
    "Current Savings (₹)",
    min_value=0.0,
    value=250000.0,
    step=10000.0
)

financial_goal = st.sidebar.number_input(
    "Financial Goal (₹)",
    min_value=0.0,
    value=500000.0,
    step=10000.0
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


if st.sidebar.button(
    "🔄 Reset Conversation",
    use_container_width=True
):

    st.session_state.agent_messages = []

    st.session_state.last_tool_result = None

    st.rerun()


# ============================================================
# CURRENT FINANCIAL CALCULATION
# ============================================================

financial_result = calculate_financial_plan(
    income=income,
    expenses=expenses,
    current_savings=current_savings,
    financial_goal=financial_goal,
    goal_months=goal_months
)


# ============================================================
# FINANCIAL SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">📊 Financial Snapshot</div>',
    unsafe_allow_html=True
)

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
        f"₹{financial_result['monthly_surplus']:,.0f}"
    )

with col4:

    st.metric(
        "Savings Rate",
        f"{financial_result['savings_rate_percent']:.2f}%"
    )


# ============================================================
# INITIAL ASSESSMENT
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Initial Assessment</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Current Savings",
        f"₹{current_savings:,.0f}"
    )

with col2:

    st.metric(
        "Goal Gap",
        f"₹{financial_result['goal_gap']:,.0f}"
    )

with col3:

    st.metric(
        "Required Monthly Saving",
        f"₹{financial_result['required_monthly_saving']:,.0f}"
    )


if financial_result["goal_status"] == "Achievable from current cash flow":

    st.markdown(
        f"""
        <div class="success-box">

        <strong>✅ Goal appears achievable.</strong><br><br>

        Based on your current cash flow, your projected savings after
        {goal_months:.0f} months would be
        <strong>₹{financial_result['projected_savings']:,.0f}</strong>.

        </div>
        """,
        unsafe_allow_html=True
    )

elif financial_result["goal_status"] == "Goal already achieved":

    st.markdown(
        """
        <div class="success-box">

        <strong>✅ Goal already achieved.</strong>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="warning-box">

        <strong>⚠️ Additional saving may be required.</strong><br><br>

        Current assessment:
        {financial_result['goal_status']}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AI FINANCIAL ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI Financial Analysis</div>',
    unsafe_allow_html=True
)

analysis_prompt = f"""
You are analyzing a user's personal financial situation.

IMPORTANT:
The Python calculation below is authoritative.

Do not recalculate, alter, contradict, or invent numerical results.

Financial profile:

Monthly income: ₹{income:,.0f}
Monthly expenses: ₹{expenses:,.0f}
Current savings: ₹{current_savings:,.0f}
Financial goal: ₹{financial_goal:,.0f}
Time to goal: {goal_months:.0f} months
Risk preference: {risk_preference}

Verified Python calculation:

{json.dumps(financial_result, indent=2)}

Provide a concise educational assessment covering:

1. Current cash-flow position
2. Savings rate
3. Goal feasibility
4. Required monthly saving
5. Additional monthly saving required, if applicable
6. One or two practical budgeting observations

Use only numerical values explicitly present in the verified
Python calculation.

Do not perform additional arithmetic.

Do not convert months into years.

Do not create additional numerical estimates.

Do not recommend specific stocks, mutual funds, insurance products,
crypto, securities, or any specific financial product.

Do not promise investment returns.

This is educational financial planning guidance.
"""

try:

    with st.spinner(
        "Generating financial analysis..."
    ):

        analysis_response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an educational personal finance assistant. "
                        "Python calculation results are authoritative. "
                        "Never perform additional financial arithmetic."
                    )
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],

            temperature=0.2,

            max_tokens=700
        )

    analysis_text = (
        analysis_response
        .choices[0]
        .message
        .content
    )

    st.write(analysis_text)

except Exception as e:

    st.warning(
        f"AI analysis temporarily unavailable: {str(e)}"
    )


# ============================================================
# FINANCE AGENT TOOLS
# ============================================================

tools = [

    {
        "type": "function",

        "function": {

            "name": "calculate_financial_plan",

            "description": (
                "Calculate verified personal finance metrics. "
                "Use this tool for goal feasibility, monthly saving, "
                "additional monthly saving required, what-if scenarios, "
                "savings rates, and personalized emergency-fund calculations."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "income": {
                        "type": "number",
                        "description": "Monthly income"
                    },

                    "expenses": {
                        "type": "number",
                        "description": "Monthly expenses"
                    },

                    "current_savings": {
                        "type": "number",
                        "description": "Current savings"
                    },

                    "financial_goal": {
                        "type": "number",
                        "description": "Financial goal amount"
                    },

                    "goal_months": {
                        "type": "number",
                        "description": "Time available to reach goal in months"
                    },

                    "extra_monthly_saving": {
                        "type": "number",
                        "description": (
                            "Additional monthly saving in a what-if scenario. "
                            "Use zero when there is no extra saving."
                        )
                    }
                },

                "required": [
                    "income",
                    "expenses",
                    "current_savings",
                    "financial_goal",
                    "goal_months"
                ]
            }
        }
    }
]


# ============================================================
# FINANCE AGENT SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = f"""
You are an AI Personal Finance & Budgeting Coach.

Your role is to help users understand:

- budgeting
- cash flow
- savings
- financial goals
- goal feasibility
- emergency funds
- risk concepts
- general financial education
- what-if financial scenarios

CURRENT USER PROFILE:

Monthly income: ₹{income:,.0f}
Monthly expenses: ₹{expenses:,.0f}
Current savings: ₹{current_savings:,.0f}
Financial goal: ₹{financial_goal:,.0f}
Goal timeline: {goal_months:.0f} months
Risk preference: {risk_preference}


============================================================
ARCHITECTURE
============================================================

You are the reasoning and conversation layer.

Python is the calculation layer.

Whenever personalized numerical financial analysis is required,
use the calculate_financial_plan tool.

The Python tool is the SINGLE SOURCE OF TRUTH for financial
calculations.

Never manually calculate financial numbers when the Python
tool can perform the calculation.


============================================================
WHEN TO USE THE PYTHON TOOL
============================================================

Use the Python tool whenever the user asks for personalized
numerical analysis, including:

- Can I reach my financial goal?
- How much do I need to save?
- How much extra do I need to save?
- What if I save an extra amount?
- How long will it take to reach my goal?
- What is my savings rate?
- How much emergency fund should I have?
- How much emergency fund do I need based on my expenses?
- Any other question requiring personalized financial arithmetic.


============================================================
EMERGENCY FUND QUESTIONS
============================================================

For a general question such as:

"What is an emergency fund?"

Answer generally without personalized calculations.

For a personalized question such as:

"How much emergency fund should I have based on my expenses?"

you MUST call the Python tool.

The Python tool provides:

- emergency_fund_3_months
- emergency_fund_6_months

Use those exact values.

Do NOT calculate them yourself.

Do NOT multiply monthly expenses by 3 or 6 yourself.

Do NOT create additional emergency-fund numbers.

Do NOT use the user's risk preference to mathematically change
the emergency-fund amount.

You may explain that 3–6 months is a general planning range,
but personalized numerical values must come from Python.


============================================================
AFTER PYTHON RETURNS A RESULT
============================================================

The Python result is the ONLY numerical source of truth.

Follow these rules strictly:

1. Use financial numbers exactly as returned by Python.

2. Do NOT perform arithmetic yourself.

3. Do NOT calculate percentages yourself.

4. Do NOT calculate differences yourself.

5. Do NOT calculate ratios yourself.

6. Do NOT calculate dates or timelines yourself.

7. Do NOT convert months into years.

8. Do NOT create additional numerical estimates.

9. Do NOT round or modify Python's numbers.

10. Use the exact months_to_goal returned by Python.

11. Use the exact emergency-fund values returned by Python.

12. Use the exact additional_monthly_saving_required value
    returned by Python.

13. If a number is not explicitly returned by Python,
    do not provide that number.

14. If the user asks for a calculation that Python has not
    provided, call the Python tool again.

15. When explaining the result, focus on interpretation,
    not additional calculations.


============================================================
IMPORTANT SAVING DEFINITIONS
============================================================

The following definitions must be followed exactly:

required_monthly_saving
=
TOTAL monthly saving required to reach the goal within
the requested timeline.

additional_monthly_saving_required
=
ADDITIONAL saving required beyond the user's current
monthly surplus.

Never describe required_monthly_saving as money that must
be saved "on top of expenses."

Never calculate the additional amount yourself.

Use the Python field:

additional_monthly_saving_required

for this purpose.


============================================================
PROJECTED SAVINGS
============================================================

The Python field:

projected_savings

already represents the user's total savings at the end
of the requested timeline, including current savings.

Never add current_savings to projected_savings again.

Never say:

"₹304,000 saved plus ₹250,000 current savings"

when projected_savings is ₹304,000.

If Python says:

projected_savings = ₹304,000

then describe it as:

"Your projected total savings after the requested period
would be ₹304,000."


============================================================
WHAT-IF SCENARIOS
============================================================

If the user asks:

"What if I save ₹5,000 extra every month?"

Use the Python tool with:

extra_monthly_saving = 5000

Clearly explain that the result is a hypothetical scenario.

Do not calculate the hypothetical result yourself.


============================================================
GENERAL EDUCATIONAL QUESTIONS
============================================================

For general educational questions:

- Answer the general question directly.
- Do not introduce calculations based on the user's profile
  unless the user explicitly asks for personalized numerical
  analysis.
- Do not calculate emergency-fund amounts, savings amounts,
  percentages, timelines, or other personalized figures unless
  the Python tool is used.
- If the user asks for a personalized numerical answer,
  use the Python tool first.


============================================================
CONVERSATION
============================================================

Remember the conversation context.

Ask a follow-up question when important information is missing.

If the user asks a general educational question that does not
require numerical calculations, answer normally without using
the tool.


============================================================
FINANCIAL SAFETY
============================================================

Do NOT recommend specific:

- stocks
- mutual funds
- ETFs
- cryptocurrencies
- insurance products
- securities
- brokers
- financial products
- investment platforms

Do not tell the user exactly where to invest or place their money.

You may discuss general concepts such as:

- emergency funds
- budgeting
- diversification
- risk tolerance
- asset allocation concepts
- liquidity
- long-term versus short-term goals

Do not promise investment returns.

Do not present hypothetical investment returns as guaranteed.


============================================================
RESPONSE STYLE
============================================================

Keep answers practical, concise, and understandable.

Use verified Python numbers when numerical analysis is involved.

Do not introduce new numbers that are not present in the
Python result.

This application is an educational financial-planning tool and
does not provide professional financial, investment, tax, or
legal advice.
"""


# ============================================================
# FINANCE AGENT FUNCTION
# ============================================================

def run_finance_agent(user_message):

    st.session_state.agent_messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(
        st.session_state.agent_messages[-20:]
    )

    while True:

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=tools,

            tool_choice="auto",

            temperature=0.2,

            max_tokens=800
        )

        assistant_message = response.choices[0].message

        tool_calls = assistant_message.tool_calls

        if not tool_calls:

            final_response = assistant_message.content

            if not final_response:

                final_response = (
                    "I couldn't generate a response. "
                    "Please try again."
                )

            st.session_state.agent_messages.append(
                {
                    "role": "assistant",
                    "content": final_response
                }
            )

            return final_response

        messages.append(
            assistant_message
        )

        for tool_call in tool_calls:

            if tool_call.function.name == "calculate_financial_plan":

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = calculate_financial_plan(

                    income=arguments["income"],

                    expenses=arguments["expenses"],

                    current_savings=arguments["current_savings"],

                    financial_goal=arguments["financial_goal"],

                    goal_months=arguments["goal_months"],

                    extra_monthly_saving=arguments.get(
                        "extra_monthly_saving",
                        0
                    )
                )

                st.session_state.last_tool_result = result

                messages.append(
                    {
                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": json.dumps(
                            result
                        )
                    }
                )


# ============================================================
# FINANCE AGENT CHAT
# ============================================================

st.markdown(
    '<div class="section-title">💬 Ask Your Finance Agent</div>',
    unsafe_allow_html=True
)

st.caption(
    "The agent remembers the conversation and can call a Python "
    "financial calculator when numerical analysis is required."
)


# ============================================================
# DISPLAY CONVERSATION
# ============================================================

for message in st.session_state.agent_messages:

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(
                message["content"]
            )

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.write(
                message["content"]
            )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask something like: Can I reach my ₹5 lakh goal in 18 months?"
)


if user_input:

    with st.chat_message("user"):

        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner(
            "Finance Agent is thinking..."
        ):

            try:

                answer = run_finance_agent(
                    user_input
                )

                st.write(answer)

            except Exception as e:

                st.error(
                    f"Finance Agent error: {str(e)}"
                )


# ============================================================
# LAST VERIFIED PYTHON CALCULATION
# ============================================================

if st.session_state.last_tool_result:

    with st.expander(
        "🔎 View latest verified Python calculation"
    ):

        st.json(
            st.session_state.last_tool_result
        )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <br>

    <div style="
        color:#64748b;
        font-size:13px;
        padding-top:10px;
    ">

    ⚠️ <strong>Educational tool only.</strong>
    This application provides budgeting and financial-planning
    education and does not constitute professional financial,
    investment, tax or legal advice. Investment returns are not
    guaranteed.

    </div>
    """,
    unsafe_allow_html=True
)