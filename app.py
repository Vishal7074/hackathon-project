import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt



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
        'District Wise Analysis'

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
    st.subheader(f"Total registration In ({selected_month})")
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
    col1, col2,col3 = st.columns(3)
    with col1:
        st.subheader("Top 10 State In (Children) Enrolment")
        age_5_17_df = (df.groupby('state')[['age_0_5']].sum()
        .reset_index().sort_values('age_0_5',
                                                                                                       ascending=False).head(
            10)).reset_index(drop=True)
        st.dataframe(age_5_17_df)
        st.markdown("---")

    with col2:
        st.subheader("Top 10 State In (Youths) Enrolment")
        age_0_5_df = (df.groupby('state')[['age_5_17']].sum()
        .reset_index().sort_values('age_5_17',
                                   ascending=False).head(
            10)).reset_index(drop=True)
        st.dataframe(age_0_5_df)
        st.markdown("---")

    with col3:
        st.subheader("Top 10 State In (Adults) Enrolment")
        age_18_greater_df = (df.groupby('state')[['age_18_greater']].sum()
        .reset_index().sort_values('age_18_greater',
                                   ascending=False).head(
            10)).reset_index(drop=True)
        st.dataframe(age_18_greater_df)
        st.markdown("---")




    # adding graphs
    # st.subheader("State Wise 0-5 Registration")

    state_age05 = (
        df.groupby('state')['age_0_5']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # ---------- Plotly bar chart ----------
    fig = px.bar(
        state_age05,
        x='state',
        y='age_0_5',
        title="State-wise Age 0–5 Registrations",
        labels={
            'state': 'State',
            'age_0_5': 'Registrations'
        },
        text_auto=True,
        template='plotly_white'
    )

    # ---------- Layout tuning ----------
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=24)),
        xaxis_title=dict(text="State", font=dict(size=16)),
        yaxis_title=dict(text="Registrations", font=dict(size=16)),
        xaxis_tickfont=dict(size=12),
        yaxis_tickfont=dict(size=12),
        height=700
    )

    fig.update_xaxes(tickangle=90)

    # ---------- Show in Streamlit ----------
    st.subheader("State-wise Age 0–5 Registration Analysis")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")





    # second graph
    state_age_5_17 = (
        df.groupby('state')['age_5_17']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # ---------- Plotly bar chart ----------
    fig = px.bar(
        state_age_5_17,
        x='state',
        y='age_5_17',
        title="State-wise Age 5_17 Registrations",
        labels={
            'state': 'State',
            'age_5_17': 'Registrations'
        },
        text_auto=True,
        template='plotly_white'
    )

    # ---------- Layout tuning ----------
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=24)),
        xaxis_title=dict(text="State", font=dict(size=16)),
        yaxis_title=dict(text="Registrations", font=dict(size=16)),
        xaxis_tickfont=dict(size=12),
        yaxis_tickfont=dict(size=12),
        height=700
    )

    fig.update_xaxes(tickangle=90)
    st.markdown("---")



    # third graph


    # ---------- Show in Streamlit ----------
    st.subheader("State-wise Age 5_17 Registration Analysis")
    st.plotly_chart(fig, use_container_width=True)



    # third
    state_age18 = (
        df.groupby('state')['age_18_greater']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # ---------- Plotly bar chart ----------
    fig = px.bar(
        state_age18,
        x='state',
        y='age_18_greater',
        title="State-wise Age 18+ Registrations",
        labels={
            'state': 'State',
            'age_18_greater': 'Registrations'
        },
        text_auto=True,
        template='plotly_white'
    )

    # ---------- Layout tuning ----------
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=24)),
        xaxis_title=dict(text="State", font=dict(size=16)),
        yaxis_title=dict(text="Registrations", font=dict(size=16)),
        xaxis_tickfont=dict(size=12),
        yaxis_tickfont=dict(size=12),
        height=700
    )

    fig.update_xaxes(tickangle=90)
    st.markdown("---")

    # third graph

    # ---------- Show in Streamlit ----------
    st.subheader("State-wise Age 18+ Registration Analysis")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")




    # ---------------- Bar chart (Selected Month) ----------------
    # st.subheader("Monthly Age Wise Registration")
    # age_df = pd.DataFrame({
    #     "Age Group": ["Age 0–5", "Age 5–17", "Age 18+"],
    #     "Registrations": [
    #         age_sum["age_0_5"],
    #         age_sum["age_5_17"],
    #         age_sum["age_18_greater"]
    #     ]
    # })
    #
    # fig = px.bar(
    #     age_df,
    #     x="Age Group",
    #     y="Registrations",
    #     title=f"Age-wise Registrations in {selected_month}",
    #     text_auto=True,
    #     template="plotly_white"
    # )
    #
    # fig.update_layout(title=dict(x=0.5))
    # st.plotly_chart(fig, use_container_width=True)
    #
    # st.markdown("---")

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
    st.markdown("""
    ### 📈 Overall Registration Trend

    ##### - **September** records the highest number of registrations (peak month).
    ##### - **November & October** show sustained high activity.
    ##### - **March** has the lowest registrations, indicating seasonal decline.
    """)

    st.markdown("---")

    st.markdown("""
        ### 📈 Age Group 0–5 (Dominant Category)

        ##### - The 0–5 age group is the most dominant category across all months.
        ##### - Registrations in this group peak in September (~1 million), contributing significantly to the overall maximum.
        ##### - November and October also show high registration volumes for this age group.
        ##### - ➡️ Inference: Aadhaar registrations are largely concentrated in the early childhood phase.
        """)

    st.markdown("---")


    st.markdown("""
        ###  🧒 Age Group 5–17 (Second Largest Contributor)

        ##### The 5–17 age group also reaches its highest registration level in September.
        
        ##### December and July show noticeable participation from this group.
        
        ##### A sharp decline is observed during low-activity months such as March and June.
        ##### ➡️ Inference: Registration trends may be influenced by school admission cycles or documentation drives.
                    """)

    st.markdown("""
    ### 🧑 Age Group 18+ (Least but Consistent)

    ##### - This age group has the **lowest registrations throughout the year**.
    ##### - Even in **peak months like September and November**, the numbers remain low.

    ##### ➡️ **Inference:** Most adults already have Aadhaar, so **new registrations are mainly for children**.
    """)

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
    # days = sorted(df['days'].unique())

    # n = df.groupby([states])['age_0_5'].sum().reset_index().sort_values('age_0_5', ascending=False).head(10)
    # st.dataframe(n)

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

    # sunburst plot
    st.subheader('Sunbrust Plot (Month -> State -> Age Group)')
    sun_df = df.melt(
        id_vars=["month", "state"],
        value_vars=["age_0_5", "age_5_17", "age_18_greater"],
        var_name="Age Group",
        value_name="Registrations"
    )

    sun_df["Age Group"] = sun_df["Age Group"].map({
        "age_0_5": "Age 0–5",
        "age_5_17": "Age 5–17",
        "age_18_greater": "Age 18+"
    })

    fig = px.sunburst(
        sun_df,
        path=["month", "state", "Age Group"],
        values="Registrations",
        title="Month-wise Aadhaar Registration Distribution",
        template="plotly_white"
    )
    fig.update_layout(
        width=1500,
        height=700,
        title=dict(x=0.5),
        plot_bgcolor="white",  # plot area
        paper_bgcolor="white",  # outer background
    )

    st.plotly_chart(fig, use_container_width=True)


    # day wise registration
    days_df = df[df['state'] == 'Chandigarh'].groupby('days')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    # ---------- day order ----------
    day_order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    # ---------- prepare day-wise data ----------
    state_df['days'] = pd.Categorical(
        state_df['days'],
        categories=day_order,
        ordered=True
    )

    d1 = (
        state_df
        .groupby('days')[['age_0_5', 'age_5_17', 'age_18_greater']]
        .sum()
        .reset_index()
        .sort_values('days')
    )

    # ---------- plot ----------
    st.subheader(f"State Wise And Day-wise Registration Distribution in ({selected_state})")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(d1["days"], d1["age_0_5"], marker="o", label="Age 0–5")
    ax.plot(d1["days"], d1["age_5_17"], marker="o", label="Age 5–17")
    ax.plot(d1["days"], d1["age_18_greater"], marker="o", label="Age 18+")

    ax.set_title("Day-wise Registration Trend by Age Group")
    ax.set_xlabel("Day")
    ax.set_ylabel("Registrations")

    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)





elif option == 'District Wise Analysis':
    st.title("District Wise Analysis")

    # ---------------- state selector ----------------
    states = sorted(df["state"].unique())
    selected_state = st.sidebar.selectbox("Select State", states)

    # ---------------- Filter selected state ----------------
    state_df = df[df["state"] == selected_state]

    # ---------------- district selector (based on selected state) ----------------
    districts = sorted(state_df["district"].unique())

    selected_district = st.sidebar.selectbox(
        "Select District",
        districts
    )

    # ---------------- Filter selected district ----------------
    district_df = state_df[state_df["district"] == selected_district]

    st.subheader(f"District Overview – {selected_district} ({selected_state})")

    # ---------------- current district totals ----------------
    curr_0_5 = district_df["age_0_5"].sum()
    curr_5_17 = district_df["age_5_17"].sum()
    curr_18 = district_df["age_18_greater"].sum()

    # ---------------- state-level baseline (average per district) ----------------
    state_group = (
        state_df
        .groupby("district")[["age_0_5", "age_5_17", "age_18_greater"]]
        .sum()
    )

    avg_0_5 = state_group["age_0_5"].mean()
    avg_5_17 = state_group["age_5_17"].mean()
    avg_18 = state_group["age_18_greater"].mean()


    # ---------------- percentage change ----------------
    def pct_change(curr, base):
        if base == 0:
            return 0
        return ((curr - base) / base) * 100


    p0 = pct_change(curr_0_5, avg_0_5)
    p1 = pct_change(curr_5_17, avg_5_17)
    p2 = pct_change(curr_18, avg_18)

    # ---------------- cards layout ----------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            label="Age 0–5 Registrations",
            value=f"{curr_0_5:,}",
            delta=f"{p0:.2f}%"
        )

    with c2:
        st.metric(
            label="Age 5–17 Registrations",
            value=f"{curr_5_17:,}",
            delta=f"{p1:.2f}%"
        )

    with c3:
        st.metric(
            label="Age 18+ Registrations",
            value=f"{curr_18:,}",
            delta=f"{p2:.2f}%"
        )


    st.markdown('-------')

    col1, col2 ,col3 = st.columns(3)

    import plotly.express as px

    with col1:
        st.subheader(f"Top 10 Districts in ({selected_state}) – Age 0–5")

        top_0_5 = (
            state_df
            .groupby("district")["age_0_5"]
            .sum()
            .reset_index()
            .sort_values(by="age_0_5", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_0_5,
            x="district",
            y="age_0_5",
            text_auto=True,
            title="Top 10 Districts (Age 0–5)",
            labels={"district": "District", "age_0_5": "Registrations"},
            template="plotly_white"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"Top 10 Districts in ({selected_state}) – Age 5–17")

        top_5_17 = (
            state_df
            .groupby("district")["age_5_17"]
            .sum()
            .reset_index()
            .sort_values(by="age_5_17", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_5_17,
            x="district",
            y="age_5_17",
            text_auto=True,
            title="Top 10 Districts (Age 5–17)",
            labels={"district": "District", "age_5_17": "Registrations"},
            template="plotly_white"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader(f"Top 10 Districts in ({selected_state}) – Age 18+")

        top_18 = (
            state_df
            .groupby("district")["age_18_greater"]
            .sum()
            .reset_index()
            .sort_values(by="age_18_greater", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_18,
            x="district",
            y="age_18_greater",
            text_auto=True,
            title="Top 10 Districts (Age 18+)",
            labels={"district": "District", "age_18_greater": "Registrations"},
            template="plotly_white"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")


    col1, col2 ,col3 = st.columns(3)
    with col1:
        st.subheader(f"Bottom 10 Districts in ({selected_state}) – Age 0–5")

        bottom_0_5 = (
            state_df
            .groupby("district")["age_0_5"]
            .sum()
            .reset_index()
            .sort_values(by="age_0_5", ascending=True)
            .head(10)
        )

        fig = px.bar(
            bottom_0_5,
            x="district",
            y="age_0_5",
            text_auto=True,
            title="Bottom 10 Districts (Age 0–5)",
            template="plotly_white"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"Bottom 10 Districts in ({selected_state}) – Age 5-17")

        bottom_0_5 = (
            state_df
            .groupby("district")["age_5_17"]
            .sum()
            .reset_index()
            .sort_values(by="age_5_17", ascending=True)
            .head(10)
        )

        fig = px.bar(
            bottom_0_5,
            x="district",
            y="age_5_17",
            text_auto=True,
            title="Bottom 10 Districts (Age 5-17)",
            template="plotly_white"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


    with col3:
        st.subheader(f"Bottom 10 Districts in ({selected_state}) – Age 18+")

        bottom_0_5 = (
            state_df
            .groupby("district")["age_18_greater"]
            .sum()
            .reset_index()
            .sort_values(by="age_18_greater", ascending=True)
            .head(10)
        )

        fig = px.bar(
            bottom_0_5,
            x="district",
            y="age_18_greater",
            text_auto=True,
            title="Bottom 10 Districts (Age 18+)",
            template="plotly_white"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")







    # ---------------- Convert to long format (for plotly) ----------------
    st.subheader(f"Month-wise Age Group Registration Sum ({selected_district}, {selected_state})" )
    month_df = (
        district_df
        .groupby("month")[["age_0_5", "age_5_17", "age_18_greater"]]
        .sum()
        .reset_index()
    )

    month_long = month_df.melt(
        id_vars="month",
        value_vars=["age_0_5", "age_5_17", "age_18_greater"],
        var_name="Age Group",
        value_name="Registrations"
    )

    fig = px.line(
        month_long,
        x="month",
        y="Registrations",
        color="Age Group",
        markers=True,
        title=f"Month-wise Age Group Registration Sum ({selected_district}, {selected_state})",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")


    st.subheader(f"Age Group Dominance – {selected_district}")
    radar_df = pd.DataFrame({
        "Age Group": ["Age 0–5", "Age 5–17", "Age 18+"],
        "District": [curr_0_5, curr_5_17, curr_18],
        "State Avg": [avg_0_5, avg_5_17, avg_18]
    })

    fig = px.line_polar(
        radar_df,
        r="District",
        theta="Age Group",
        line_close=True,
        title=f"Age Group Dominance – {selected_district}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")



    rank_df = (
        state_df
        .groupby("district")["age_0_5"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    rank = rank_df[rank_df["district"] == selected_district].index[0] + 1
    total = len(rank_df)

    st.metric(
        label="District Rank (Age 0–5)",
        value=f"{rank} / {total}"
    )

    st.markdown("---")


