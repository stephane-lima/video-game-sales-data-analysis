import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Global Video Game Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

def load_data():
    df = pd.read_csv("vgsales.csv")
    return df

def clean_data(df):
    df.dropna()
    # df["Year"] = df["Year"].fillna("No Information")
    # df["Publisher"] = df["Publisher"].fillna("No Information")

    df = df.assign(Year = df["Year"].astype("Int64"))
    return df

def main_metrics(df):
    min_global_sales = df["Global_Sales"].min() * 1000000
    mean_global_sales = df["Global_Sales"].mean() * 1000000
    max_global_sales = df["Global_Sales"].max() * 1000000
    Total_global_sales = df["Global_Sales"].sum() * 1000000
    number_games = df.shape[0]
    number_platforms = df["Platform"].nunique()
    number_genres = df["Genre"].nunique()
    number_publishers = df["Publisher"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Minimum Sales (Worldwide)", f"{min_global_sales:,.0f}")
    col2.metric("Average Sales per Game (Worldwide)", f"{mean_global_sales:,.0f}")
    col3.metric("Maximum Sales (Worldwide)", f"{max_global_sales:,.0f}")
    col4.metric("Total Sales (Worldwide)", f"{Total_global_sales:,.0f}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Number of Games", f"{number_games:,}")
    col6.metric("Number of Genres", f"{number_genres}")
    col7.metric("Number of Platforms", f"{number_platforms}")
    col8.metric("Number of Publishers", f"{number_publishers}")

def question_one(df):
    top_games = df.sort_values(by="Global_Sales", ascending=False).head(10)

    fig = px.bar(
        top_games,
        x = "Global_Sales",
        y = "Name",
        orientation = "h",
        title = "Top 10 Best-Selling Video Games",
        labels = {"Global_Sales": "Copies Sold Worldwide (Millions)", "Name": "Games"},
        text = "Global_Sales"
    )

    fig.update_layout(title_x=0.4, yaxis={"categoryorder":"total ascending"})

    st.plotly_chart(fig, width="stretch")

def question_two(df):
    genre_global_total_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).reset_index()
    
    fig = px.bar(
        genre_global_total_sales,
        x="Global_Sales",
        y="Genre",
        orientation="h",
        title="Top Genres by Global Sales",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Genre": "Genres"},
        text = "Global_Sales"
    )

    fig.update_layout(title_x=0.4, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, width="stretch")

    st.markdown(f"The **{genre_global_total_sales.iloc[0]["Genre"]}** genre has sold the most copies worldwide, with approximately {genre_global_total_sales.iloc[0]["Global_Sales"]} millions copies sold worldwide")

    return

def question_three(df):
    platform_global_total_sales = round(df.groupby("Platform")["Global_Sales"].sum(), 2).nlargest(10).sort_values(ascending=False).reset_index()
    
    fig = px.bar(
        platform_global_total_sales,
        x = "Global_Sales",
        y = "Platform",
        orientation="h",
        title="Top 10 Platforms by Global Sales",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Platform": "Platforms"},
        text = "Global_Sales"
    )

    fig.update_layout(title_x=0.4, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, width="stretch")

    st.markdown(f"The **{platform_global_total_sales.iloc[0]["Platform"]}** platform has generated the highest worldwide game sales, with approximately {platform_global_total_sales.iloc[0]["Global_Sales"]} millions copies sold worldwide")

    return

def question_four(df):
    publisher_global_total_sales = df.groupby("Publisher")["Global_Sales"].sum().nlargest(10).sort_values(ascending=False).reset_index()

    fig = px.bar(
        publisher_global_total_sales,
        x = "Global_Sales",
        y = "Publisher",
        orientation = "h",
        title = "Top 10 Publishers by Global Sales",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Publisher": "Publishers"},
        text = "Global_Sales"
    )

    fig.update_layout(title_x=0.4, yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig, width="stretch")

    st.markdown(f"The **{publisher_global_total_sales.iloc[0]["Publisher"]}** publisher has generated the highest worldwide game sales, with approximately {publisher_global_total_sales.iloc[0]["Global_Sales"]} millions copies sold worldwide")

def question_five(df):
    col_graph1, col_graph2 = st.columns(2)

    # Create a DataFrame with total sales by region
    regional_sales = pd.DataFrame({
        "Region": ["North America", "Europe", "Japan", "Other"],
        "Global Sales in Millions": [
            round(df["NA_Sales"].sum(), 2),
            round(df["EU_Sales"].sum(), 2),
            round(df["JP_Sales"].sum(), 2),
            round(df["Other_Sales"].sum(), 2)
        ]
    }).sort_values(by="Global Sales in Millions", ascending=True)

    with col_graph1:
        fig = px.bar(
            regional_sales,
            x = "Global Sales in Millions",
            y = "Region",
            orientation = "h",
            title = "Global Video Games Sales by Region",
            labels={"Global Sales in Millions": "Copies Sold Worldwide (Millions)", "Region": "Region"},
            text = "Global Sales in Millions"
        )

        fig.update_layout(title_x=0.3, yaxis={"categoryorder": "total ascending"})

        st.plotly_chart(fig, width="stretch")

    with col_graph2:
        # Create pie chart
        fig = px.pie(
            regional_sales,
            names = "Region",
            values = "Global Sales in Millions",
            title = "Percentage of Global Video Games Sales by Region"
        )

        fig.update_layout(title_x=0.2)

        # Display the chart in Streamlit
        st.plotly_chart(fig, width="stretch")
    
    st.markdown(f"Total video game sales are highest in **North America**(49.3%), making it the largest market. **Europe**(27.3%) has the second-highest total sales, followed by **Japan**(14.5%) and **Others**(8.95%) regions. This indicates that North America contributed the largest share of global video game sales during the period covered by the dataset.")
    
    return

def question_six(df):
    sales_trend = df.groupby("Year")["Global_Sales"].sum().reset_index().sort_values(by="Year").reset_index()

    fig = px.line(
        sales_trend,
        x = "Year",
        y = "Global_Sales",
        markers = True,
        title = "Global Video Game Sales Over Time",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Year": "Year"}
    )

    fig.update_layout(title_x=0.4)

    st.plotly_chart(fig, width="stretch")

    st.markdown("In the Video Game Sales dataset, global video game sales show a strong growth trend from 1980's until the late 2000's.")

    st.markdown("In the early years of the dataset (1980's), annual global sales were relatively low compared to later periods. Sales increased progressively throughout the 1990's, with more significant growth occuring after 2000. The highest levels of total annual global sales occurred between 2007 and 2010, with 2008 representing the peak year for total global sales in the dataset.")

    st.markdown("After 2009, the total yearly global sales values decreased. From 2010 onward, sales showed a downward trend, reaching substantially lower levels by 2016 compared with the peak period.")

    return

def question_seven(df):
    games_per_year = df.groupby("Year")["Name"].count().reset_index(name="Games Released")

    fig = px.bar(
        games_per_year,
        x = "Year",
        y = "Games Released",
        orientation = "v",
        title = "Number of Games Released by Year",
        text = "Games Released"
    )

    fig.update_layout(title_x=0.4)

    st.plotly_chart(fig, width="stretch")

def main():
    # Load the dataset
    df = load_data()

    # clean_data(df)

    st.title("Video Game Sales Analysis Dashboard")

    main_metrics(df)

    st.subheader("Question 1: Which are the top 10 best-selling video games worldwide?")

    question_one(df)

    st.subheader("Question 2: Which video game genre has sold the most games worldwide?")

    question_two(df)

    st.subheader("Question 3: Which gaming platform has sold the most games worldwide?")

    question_three(df)

    st.subheader("Question 4: Which publisher has sold the most games worldwide?")

    question_four(df)

    st.subheader("Question 5: How do total video game sales compare across regions?")

    question_five(df)

    st.subheader("Question 6: How have global video game sales changed over time?")

    question_six(df)

    st.subheader("Question 7: How many games were released each year?")

    question_seven(df)

    st.subheader("Video Game Sales Dataset")

    st.dataframe(df)

if __name__ == "__main__":
    main()