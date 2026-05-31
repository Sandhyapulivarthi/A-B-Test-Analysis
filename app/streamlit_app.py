import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest

# Page Title
st.title("A/B Test Experiment Analysis Dashboard")

st.markdown("""
This dashboard analyzes A/B testing experiments using
statistical hypothesis testing and visualization.

### Features:
- Conversion Rate Analysis
- Statistical Significance Testing
- Business Recommendations
- Interactive Visualizations
""")

# Sidebar
st.sidebar.title("Dashboard Menu")
st.sidebar.write("A/B Testing Analysis System")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# Check File Upload
if uploaded_file is not None:

    # Read Dataset
    df = pd.read_csv(uploaded_file)

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.write(df.head())

    # Dataset Columns
    st.subheader("Dataset Columns")
    st.write(df.columns)

    # Summary Statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Dataset Shape
    st.subheader("Dataset Shape")
    st.write(df.shape)

    # Conversion Rates
    st.subheader("Conversion Rates")

    conversion_rates = df.groupby(
        'group'
    )['converted'].mean()

    st.write(conversion_rates)

    # Metrics Cards
    st.subheader("Key Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Group A Conversion %",
            round(conversion_rates['A'] * 100, 2)
        )

    with col2:
        st.metric(
            "Group B Conversion %",
            round(conversion_rates['B'] * 100, 2)
        )

    # Bar Chart
    st.subheader("Conversion Rate Comparison")

    fig, ax = plt.subplots()

    conversion_rates.plot(
        kind='bar',
        ax=ax
    )

    plt.title("Conversion Rate by Group")
    plt.xlabel("Group")
    plt.ylabel("Conversion Rate")

    st.pyplot(fig)

    # Histogram
    st.subheader("Time Spent Distribution")

    fig2, ax2 = plt.subplots()

    df['time_spent'].hist(ax=ax2)

    plt.title("Time Spent Histogram")
    plt.xlabel("Time Spent")
    plt.ylabel("Frequency")

    st.pyplot(fig2)

    # Box Plot
    st.subheader("Clicks Comparison")

    fig3, ax3 = plt.subplots()

    sns.boxplot(
        x='group',
        y='clicks',
        data=df,
        ax=ax3
    )

    plt.title("Clicks Boxplot")

    st.pyplot(fig3)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")

    fig5, ax5 = plt.subplots()

    sns.heatmap(
        df.corr(numeric_only=True),
        annot=True,
        cmap='Blues',
        ax=ax5
    )

    st.pyplot(fig5)

    # Pie Chart
    st.subheader("Conversion Distribution")

    fig4, ax4 = plt.subplots()

    df['group'].value_counts().plot(
        kind='pie',
        autopct='%1.1f%%',
        ax=ax4
    )

    plt.ylabel("")

    st.pyplot(fig4)

    # Statistical Testing
    success = df.groupby(
        'group'
    )['converted'].sum()

    samples = df.groupby(
        'group'
    )['converted'].count()

    z_stat, p_value = proportions_ztest(
        success,
        samples
    )

    # Results
    st.subheader("Statistical Test Results")

    st.write("Z Statistic:", z_stat)

    st.write("P Value:", p_value)

    # Recommendation
    if p_value < 0.05:

        st.success(
            "Statistically Significant Difference Found"
        )

        st.write(
            "Recommendation: Deploy Version B"
        )

    else:

        st.warning(
            "No Statistically Significant Difference"
        )

        st.write(
            "Recommendation: Keep Current Version"
        )

    # Final Conclusion
    st.subheader("Final Conclusion")

    if p_value < 0.05:

        st.write("""
        Version B performed significantly better than Version A.
        The company should consider deploying Version B.
        """)

    else:

        st.write("""
        No statistically significant difference was found
        between Version A and Version B.

        More experimentation or larger sample sizes
        are recommended.
        """)