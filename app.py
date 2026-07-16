import pandas as pd
import streamlit as st
import plotly.express as px

# Set the page title, icon, and wide layout for the Streamlit dashboard
st.set_page_config(
    page_title="Global Video Game Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Read the video game sales data from the CSV file and store it in a DataFrame
def load_data():
    df = pd.read_csv("vgsales.csv")
    return df

# Prepare the data for analysis by converting the Year column to a numeric type
def clean_data(df):
    # This line removes rows that contain missing values
    df = df.dropna()

    # Convert the Year column to a nullable integer type so it can be used safely in analysis
    df = df.assign(Year = df["Year"].astype("Int64"))
    return df

# Calculate the main summary statistics and display them as metric cards at the top of the dashboard
def main_metrics(df):
    # Compute the minimum, average, maximum, and total worldwide sales values
    min_global_sales = df["Global_Sales"].min() * 1000000
    mean_global_sales = df["Global_Sales"].mean() * 1000000
    max_global_sales = df["Global_Sales"].max() * 1000000
    Total_global_sales = df["Global_Sales"].sum() * 1000000

    # Count how many games, platforms, genres, and publishers are in the dataset
    number_games = df.shape[0]
    number_platforms = df["Platform"].nunique()
    number_genres = df["Genre"].nunique()
    number_publishers = df["Publisher"].nunique()

    # Create four columns to place the sales summary metrics side by side
    col1, col2, col3, col4 = st.columns(4)

    # Show each sales metric in its own card.
    col1.metric("Minimum Sales (Worldwide)", f"{min_global_sales:,.0f}")
    col2.metric("Average Sales per Game (Worldwide)", f"{mean_global_sales:,.0f}")
    col3.metric("Maximum Sales (Worldwide)", f"{max_global_sales:,.0f}")
    col4.metric("Total Sales (Worldwide)", f"{Total_global_sales:,.0f}")

    # Create another row of four columns for the count-based metrics
    col5, col6, col7, col8 = st.columns(4)

    # Show the totals for games, genres, platforms, and publishers
    col5.metric("Number of Games", f"{number_games:,}")
    col6.metric("Number of Genres", f"{number_genres}")
    col7.metric("Number of Platforms", f"{number_platforms}")
    col8.metric("Number of Publishers", f"{number_publishers}")

# Show the top 10 best-selling games as a horizontal bar chart
def question_one(df):
    st.subheader("Question 1: Which are the top 10 best-selling video games worldwide?")

    # Sort the games by global sales from highest to lowest and keep the top 10 rows
    top_games = df.sort_values(by="Global_Sales", ascending=False).head(10)

    # Create a horizontal bar chart using Plotly Express
    fig = px.bar(
        top_games,
        x = "Global_Sales",
        y = "Name",
        orientation = "h",
        title = "Top 10 Best-Selling Video Games",
        labels = {"Global_Sales": "Copies Sold Worldwide (Millions)", "Name": "Games"},
        text = "Global_Sales"
    )

    # Center the title and arrange the bars in a readable order
    fig.update_layout(title_x=0.4, yaxis={"categoryorder":"total ascending"})

    # Display the chart inside the Streamlit app
    st.plotly_chart(fig, width="stretch")

# Show which genre has generated the most global sales
def question_two(df):
    st.subheader("Question 2: Which video game genre has sold the most games worldwide?")

    # Group the sales by genre and add them together to get the total sales for each genre
    genre_global_total_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).reset_index()

    # Create a horizontal bar chart for the genre totals
    fig = px.bar(
        genre_global_total_sales,
        x="Global_Sales",
        y="Genre",
        orientation="h",
        title="Top Genres by Global Sales",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Genre": "Genres"},
        text = "Global_Sales"
    )

    # Update the chart layout so it looks clean and readable
    fig.update_layout(title_x=0.4, yaxis={"categoryorder": "total ascending"})

    # Display the bar chart in the dashboard
    st.plotly_chart(fig, width="stretch")

    # Add a short text summary that highlights the leading genre
    st.markdown(f"The **{genre_global_total_sales.iloc[0]['Genre']}** genre has sold the most copies worldwide, with approximately {genre_global_total_sales.iloc[0]['Global_Sales']} millions copies sold worldwide")

    return

# Show which platform has generated the highest global sales
def question_three(df):
    st.subheader("Question 3: Which gaming platform has sold the most games worldwide?")

    # Group the data by platform, sum the sales, and keep the top 10 platforms
    platform_global_total_sales = round(df.groupby("Platform")["Global_Sales"].sum(), 2).nlargest(10).sort_values(ascending=False).reset_index()

    # Create a horizontal bar chart for the platform sales totals
    fig = px.bar(
        platform_global_total_sales,
        x = "Global_Sales",
        y = "Platform",
        orientation="h",
        title="Top 10 Platforms by Global Sales",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Platform": "Platforms"},
        text = "Global_Sales"
    )

    # Update the chart layout for better presentation
    fig.update_layout(title_x=0.4, yaxis={"categoryorder": "total ascending"})

    # Show the chart in the dashboard.
    st.plotly_chart(fig, width="stretch")

    # Add a short explanation that names the top platform
    st.markdown(f"The **{platform_global_total_sales.iloc[0]['Platform']}** platform has generated the highest worldwide game sales, with approximately {platform_global_total_sales.iloc[0]['Global_Sales']} millions copies sold worldwide")

    return

# Show which publisher has generated the highest sales
def question_four(df):
    st.subheader("Question 4: Which publisher has sold the most games worldwide?")

    # Group the data by publisher and calculate the total sales for each publisher
    publisher_global_total_sales = df.groupby("Publisher")["Global_Sales"].sum().nlargest(10).sort_values(ascending=False).reset_index()

    # Create a horizontal bar chart for the publisher sales totals
    fig = px.bar(
        publisher_global_total_sales,
        x = "Global_Sales",
        y = "Publisher",
        orientation = "h",
        title = "Top 10 Publishers by Global Sales",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Publisher": "Publishers"},
        text = "Global_Sales"
    )

    # Adjust the layout so the chart is easier to read
    fig.update_layout(title_x=0.4, yaxis={"categoryorder": "total ascending"})

    # Display the chart in the Streamlit app
    st.plotly_chart(fig, width="stretch")

    # Add a short summary that identifies the top publisher
    st.markdown(f"The **{publisher_global_total_sales.iloc[0]['Publisher']}** publisher has generated the highest worldwide game sales, with approximately {publisher_global_total_sales.iloc[0]['Global_Sales']} millions copies sold worldwide")

# Compare total sales across regions using a bar chart and a pie chart
def question_five(df):
    st.subheader("Question 5: How do total video game sales compare across regions?")

    # Create two columns so the bar chart and pie chart can appear side by side
    col_graph1, col_graph2 = st.columns(2)

    # Build a DataFrame that stores the total sales for each region
    regional_sales = pd.DataFrame({
        "Region": ["North America", "Europe", "Japan", "Other"],
        "Global Sales in Millions": [
            round(df["NA_Sales"].sum(), 2),
            round(df["EU_Sales"].sum(), 2),
            round(df["JP_Sales"].sum(), 2),
            round(df["Other_Sales"].sum(), 2)
        ]
    }).sort_values(by="Global Sales in Millions", ascending=True)

    # Place the bar chart in the first column
    with col_graph1:
        # Create a horizontal bar chart for total regional sales
        fig = px.bar(
            regional_sales,
            x = "Global Sales in Millions",
            y = "Region",
            orientation = "h",
            title = "Global Video Games Sales by Region",
            labels={"Global Sales in Millions": "Copies Sold Worldwide (Millions)", "Region": "Region"},
            text = "Global Sales in Millions"
        )

        # Update the chart layout
        fig.update_layout(title_x=0.3, yaxis={"categoryorder": "total ascending"})

        # Display the bar chart.
        st.plotly_chart(fig, width="stretch")

    # Place the pie chart in the second column
    with col_graph2:
        # Create a pie chart to show the share of sales by region
        fig = px.pie(
            regional_sales,
            names = "Region",
            values = "Global Sales in Millions",
            title = "Percentage of Global Video Games Sales by Region"
        )

        # Update the pie chart layout
        fig.update_layout(title_x=0.2)

        # Display the pie chart
        st.plotly_chart(fig, width="stretch")

    # Add a written explanation that summarizes the regional sales results
    st.markdown(f"Total video game sales are highest in **North America**(49.3%), making it the largest market. **Europe**(27.3%) has the second-highest total sales, followed by **Japan**(14.5%) and **Others**(8.95%) regions. This indicates that North America contributed the largest share of global video game sales during the period covered by the dataset.")

    return

# Show how global sales changed over time with a line chart
def question_six(df):
    st.subheader("Question 6: How have global video game sales changed over time?")

    # Group sales by year and sort the results from oldest to newest
    sales_trend = df.groupby("Year")["Global_Sales"].sum().reset_index().sort_values(by="Year").reset_index()

    # Create a line chart with markers for each year
    fig = px.line(
        sales_trend,
        x = "Year",
        y = "Global_Sales",
        markers = True,
        title = "Global Video Game Sales Over Time",
        labels={"Global_Sales": "Copies Sold Worldwide (Millions)", "Year": "Year"}
    )

    # Adjust the chart layout
    fig.update_layout(title_x=0.4)

    # Display the line chart in the app
    st.plotly_chart(fig, width="stretch")

    # Add text explaining the sales trend over time
    st.markdown("In the Video Game Sales dataset, global video game sales show a strong growth trend from 1980's until the late 2000's.")

    st.markdown("In the early years of the dataset (1980's), annual global sales were relatively low compared to later periods. Sales increased progressively throughout the 1990's, with more significant growth occuring after 2000. The highest levels of total annual global sales occurred between 2007 and 2010, with 2008 representing the peak year for total global sales in the dataset.")

    st.markdown("After 2009, the total yearly global sales values decreased. From 2010 onward, sales showed a downward trend, reaching substantially lower levels by 2016 compared with the peak period.")

    return

# Show how many games were released each year
def question_seven(df):
    st.subheader("Question 7: How many games were released each year?")

    # Count how many games were released in each year
    games_per_year = df.groupby("Year")["Name"].count().reset_index(name="Games Released")

    # Create a vertical bar chart for the yearly release counts
    fig = px.bar(
        games_per_year,
        x = "Year",
        y = "Games Released",
        orientation = "v",
        title = "Number of Games Released by Year",
        text = "Games Released"
    )

    # Center the chart title
    fig.update_layout(title_x=0.4)

    # Display the chart in the dashboard
    st.plotly_chart(fig, width="stretch")

# Run the full dashboard and display all sections in order
def main():
    # Load the dataset from the CSV file
    df = load_data()

    # Clean the dataset before using it in the charts.
    # clean_data(df)

    # Set the main title displayed at the top of the page
    st.title("Video Game Sales Analysis Dashboard")

    # Show the summary metrics for the dataset
    main_metrics(df)

    # Call function to display the answer to question 1
    question_one(df)

    # Call function to display the answer to question 2
    question_two(df)

    # Call function to display the answer to question 3
    question_three(df)

    # Call function to display the answer to question 4
    question_four(df)

    # Call function to display the answer to question 5
    question_five(df)

    # Call function to display the answer to question 6
    question_six(df)

    # Call function to display the answer to question 7
    question_seven(df)

    # Show the full dataset in a table near the bottom of the page
    st.subheader("Video Game Sales Dataset")
    st.dataframe(df)

# Start the app when this file is run directly
if __name__ == "__main__":
    main()