import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: white;
#         color: black;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )




st.set_page_config(layout="wide")

@st.cache_data(show_spinner=True)
def load_data():
    return pd.read_csv(
        'cleaned_aadhaar_enrolment.csv',
        low_memory=False
    )

df = load_data()

st.sidebar.title('Analysis Of Aadhaar Enrolment')

option = st.sidebar.selectbox(
    'Select One',
    [
        'Important Observations',
        'Overall Analysis',
        'State Wise Analysis',
        'District Wise Analysis',
        'Pincode Wise Analysis'
    ]
)

if option == "Overall Analysis":
    st.title("Overall Analysis")

    # ---------------- Month selector ----------------
    months = sorted(df["month"].unique())
    selected_month = st.sidebar.selectbox("Select Month", months)

    # ---------------- Filter selected month ----------------
    month_df = df[df["month"] == selected_month]

    # ---------------- Aggregate (SUM) ----------------
    age_sum = month_df[["age_0_5", "age_5_17", "age_18_greater"]].sum()

    total_reg = age_sum.sum()

    # ---------------- Percentage ----------------
    age_pct = (age_sum / total_reg) * 100

    # ---------------- Display metrics ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Age 0–5",
        f"{int(age_sum['age_0_5']):,}",
        f"{age_pct['age_0_5']:.2f}%"
    )

    col2.metric(
        "Age 5–17",
        f"{int(age_sum['age_5_17']):,}",
        f"{age_pct['age_5_17']:.2f}%"
    )

    col3.metric(
        "Age 18+",
        f"{int(age_sum['age_18_greater']):,}",
        f"{age_pct['age_18_greater']:.2f}%"
    )

    st.markdown("---")

    # ---------------- Bar chart (Selected Month) ----------------
    st.subheader("Monthly Age Wise Registration")
    age_df = pd.DataFrame({
        "Age Group": ["Age 0–5", "Age 5–17", "Age 18+"],
        "Registrations": [
            age_sum["age_0_5"],
            age_sum["age_5_17"],
            age_sum["age_18_greater"]
        ]
    })

    fig = px.bar(
        age_df,
        x="Age Group",
        y="Registrations",
        title=f"Age-wise Registrations in {selected_month}",
        text_auto=True,
        template="plotly_white"
    )

    fig.update_layout(title=dict(x=0.5))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------- Monthly stacked bar ----------------
    st.subheader("Monthly stacked bar")
    monthly_summary = (
        df.groupby("month")[["age_0_5", "age_5_17", "age_18_greater"]]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        monthly_summary,
        x="month",
        y=["age_0_5", "age_5_17", "age_18_greater"],
        title="Monthly Registration Distribution by Age Group",
        labels={
            "value": "Number of Registrations",
            "month": "Month",
            "variable": "Age Group"
        },
        template="plotly_white"
    )

    fig2.for_each_trace(lambda t: t.update(
        name={
            "age_0_5": "Age 0–5",
            "age_5_17": "Age 5–17",
            "age_18_greater": "Age 18+"
        }[t.name]
    ))

    fig2.update_layout(
        barmode="stack",
        title=dict(x=0.5),
        xaxis_title="Month",
        yaxis_title="Number of Registrations"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Month-wise Registration Trend by Age Group")

    # Prepare month-wise data
    monthly_line = (
        df.groupby("month")[["age_0_5", "age_5_17", "age_18_greater"]]
        .sum()
        .reset_index()
    )

    # (Optional but recommended) Month order fix
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    monthly_line["month"] = pd.Categorical(
        monthly_line["month"],
        categories=month_order,
        ordered=True
    )

    monthly_line = monthly_line.sort_values("month")

    # Line chart (stock style)
    fig3 = px.line(
        monthly_line,
        x="month",
        y=["age_0_5", "age_5_17", "age_18_greater"],
        markers=True,
        labels={
            "value": "Number of Registrations",
            "month": "Month",
            "variable": "Age Group"
        },
        title="Month-wise Registration Trend (Age Groups)",
        template="plotly_white"
    )

    # Clean legend names
    fig3.for_each_trace(lambda t: t.update(
        name={
            "age_0_5": "Age 0–5",
            "age_5_17": "Age 5–17",
            "age_18_greater": "Age 18+"
        }[t.name]
    ))

    fig3.update_layout(
        title=dict(x=0.5),
        xaxis_title="Month",
        yaxis_title="Number of Registrations"
    )

    st.plotly_chart(fig3, use_container_width=True)


elif option == "Important Observations":
    st.title("Important Observations")


elif option == 'State Wise Analysis':
    st.title("State Wise Analysis")

    states = sorted(df['state'].unique())
    months = sorted(df['month'].unique())
    days = sorted(df['days'].unique())
    selected_state = st.sidebar.selectbox("Select State", states)
    selected_month = st.sidebar.selectbox("Select Month", months)
    state_df = df[df["state"] == selected_state]
    month_df = state_df[state_df["month"] == selected_month]
    total_df = month_df[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    f_df = total_df.rename(columns={
        'index': 'Age Group',
        0: 'No of Registration'
    })

    st.subheader(f"Total Age Wise Registrations In ({selected_state}) In ({selected_month})")

    col1 ,col2 = st.columns(2)
    with col1:
        fig = px.pie(
            f_df,
            names="Age Group",
            values="No of Registration",
            title=f"Age-wise Distribution ({selected_month})",
            template="plotly_white"
        )

        # ✅ labels + percent + COLOR FIX
        fig.update_traces(
            textinfo="percent+label",
            textfont=dict(
                size=25,
                color="black"  # ⭐ IMPORTANT LINE
            ),
            marker=dict(line=dict(color="white", width=2))
        )

        # ✅ force pure white background
        fig.update_layout(
            title=dict(x=0.5),
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(t=60, b=40, l=40, r=40),
            legend=dict(
                bgcolor="white",
                bordercolor="lightgray",
                borderwidth=1,
                font=dict(color="black")  # legend text bhi clear
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig, ax = plt.subplots()

        ax.bar(
            f_df["Age Group"],
            f_df["No of Registration"]
        )

        ax.set_title("Age-wise Registration Distribution")
        ax.set_xlabel("Age Group")
        ax.set_ylabel("No of Registration")

        # value labels
        for i, v in enumerate(f_df["No of Registration"]):
            ax.text(i, v, f"{v:,}", ha="center", va="bottom")

        st.pyplot(fig)

    # month wise line chart
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    state_df['month'] = pd.Categorical(
        state_df['month'],
        categories=month_order,
        ordered=True
    )

    m1 = (
        state_df
        .groupby('month')[['age_0_5', 'age_5_17', 'age_18_greater']]
        .sum()
        .reset_index()
        .sort_values('month')
    )

    st.subheader(f'State Wise Monthly Line Distribution in ({selected_state})')

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(m1["month"], m1["age_0_5"], marker="o", label="Age 0–5")
    ax.plot(m1["month"], m1["age_5_17"], marker="o", label="Age 5–17")
    ax.plot(m1["month"], m1["age_18_greater"], marker="o", label="Age 18+")

    ax.set_title("Month-wise Registration Trend by Age Group")
    ax.set_xlabel("Month")
    ax.set_ylabel("Registrations")
    ax.tick_params(axis='x', rotation=90)


    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    # # sunburst plot
    # st.subheader('Sunbrust Plot (Month -> State -> Age Group)')
    # sun_df = df.melt(
    #     id_vars=["month", "state"],
    #     value_vars=["age_0_5", "age_5_17", "age_18_greater"],
    #     var_name="Age Group",
    #     value_name="Registrations"
    # )
    #
    # sun_df["Age Group"] = sun_df["Age Group"].map({
    #     "age_0_5": "Age 0–5",
    #     "age_5_17": "Age 5–17",
    #     "age_18_greater": "Age 18+"
    # })
    #
    # fig = px.sunburst(
    #     sun_df,
    #     path=["month", "state", "Age Group"],
    #     values="Registrations",
    #     title="Month-wise Aadhaar Registration Distribution",
    #     template="plotly_white"
    # )
    # fig.update_layout(
    #     width=1500,
    #     height=700,
    #     title=dict(x=0.5),
    #     plot_bgcolor="white",  # plot area
    #     paper_bgcolor="white",  # outer background
    # )
    #
    # st.plotly_chart(fig, use_container_width=True)

    days = sorted(df['days'].unique())




elif option == 'District Wise Analysis':
    st.title("District Wise Analysis")

elif option == 'Pincode Wise Analysis':
    st.title("Pincode Wise Analysis")
