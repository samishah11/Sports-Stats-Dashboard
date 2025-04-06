import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sports Stats Dashboard", layout="wide")
st.title("🏅 Sports Stats Dashboard")
st.subheader("Made by [Shahbaz Mehmood](www.linkedin.com/in/shahbaz-mehmood-data-analyst-19b32125b/")
st.markdown("This dashboard is designed to visualize and analyze sports statistics data. You can upload your own CSV file and explore the insights!")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a sports statistics CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # Show summary statistics
    st.subheader("📊 Summary Statistics")
    st.write(df.describe(include='all'))

    # Show column options for user to select
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    category_columns = df.select_dtypes(exclude='number').columns.tolist()

    with st.sidebar:
        st.header("⚙️ Chart Options")
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Box Plot", "Histogram", "3D Scatter"])
        x_axis = st.selectbox("X-Axis", df.columns)
        y_axis = st.selectbox("Y-Axis", numeric_columns)
        color_by = st.selectbox("Color By (Optional)", [None] + category_columns)
        add_trendline = st.checkbox("Add Trendline (Only for Scatter)", value=False)

        if chart_type == "3D Scatter":
            z_axis = st.selectbox("Z-Axis (for 3D)", numeric_columns)

    st.subheader("📈 Visualization")
    if chart_type == "Bar Chart":
        fig = px.bar(df, x=x_axis, y=y_axis, color=color_by)
    elif chart_type == "Line Chart":
        fig = px.line(df, x=x_axis, y=y_axis, color=color_by)
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, size=y_axis, trendline="ols" if add_trendline else None)
    elif chart_type == "Pie Chart":
        pie_column = st.selectbox("Pie Chart Values", numeric_columns)
        pie_names = st.selectbox("Labels", category_columns)
        fig = px.pie(df, values=pie_column, names=pie_names, title="Pie Chart")
    elif chart_type == "Box Plot":
        fig = px.box(df, x=color_by if color_by else x_axis, y=y_axis, title="Box Plot")
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=x_axis, color=color_by, nbins=30, title="Histogram")
    elif chart_type == "3D Scatter":
        fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=color_by, size=y_axis, title="3D Scatter Plot")

    st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.subheader("🔍 Correlation Heatmap")
    corr = df[numeric_columns].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='Blues', title="Feature Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)

    # Filter by team or category
    if category_columns:
        filter_col = st.selectbox("🎯 Filter Data by", category_columns)
        selected_value = st.selectbox(f"Select a {filter_col}", df[filter_col].unique())
        filtered_df = df[df[filter_col] == selected_value]

        st.subheader(f"📌 Stats for {filter_col}: {selected_value}")
        st.dataframe(filtered_df)
        st.write(filtered_df.describe(include='all'))

else:
    st.info("Please upload a sports statistics CSV file to begin.")
