import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="TARDIS - Train Delay Prediction System",
    page_icon="🚄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 40px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 25px;
        font-weight: bold;
        color: #2563EB;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F8FAFC;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
    }
    .metric-label {
        font-size: 16px;
        text-align: center;
        color: #4B5563;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        font-size: 14px;
        color: #6B7280;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<div class="main-header">TARDIS - Train Delay Prediction System</div>',
    unsafe_allow_html=True,
)
st.markdown("*Predicting the Unpredictable: SNCF Train Delay Analysis & Forecast*")
st.markdown("---")


# Load data and model functions
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_dataset.csv")
        # Convert date column to datetime
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


@st.cache_resource
def load_model():
    try:
        with open("tardis_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("model_info.pkl", "rb") as f:
            model_info = pickle.load(f)
        return model, model_info
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None


# Load data and model
df = load_data()
model, model_info = load_model()

if df is None:
    st.error("Failed to load the dataset. Please ensure 'cleaned_dataset.csv' exists.")
    st.stop()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Delay Analysis",
        "Station Insights",
        "Route Analysis",
        "Delay Prediction",
    ],
)

# Basic page selection structure
if page == "Overview":
    st.markdown(
        '<div class="sub-header">Overview Dashboard</div>', unsafe_allow_html=True
    )
    st.write(
        "Welcome to the TARDIS (Train Analysis and Reporting Dashboard for Intelligent Scheduling) system."
    )
    # Overview content will be added in the next step

elif page == "Delay Analysis":
    st.markdown('<div class="sub-header">Delay Analysis</div>', unsafe_allow_html=True)
    st.write("Explore detailed patterns and distributions of train delays.")
    # Delay Analysis content will be added later

elif page == "Station Insights":
    st.markdown(
        '<div class="sub-header">Station Insights</div>', unsafe_allow_html=True
    )
    st.write("Analyze delay patterns by stations.")
    # Station Insights content will be added later

elif page == "Route Analysis":
    st.markdown('<div class="sub-header">Route Analysis</div>', unsafe_allow_html=True)
    st.write("Analyze delay patterns by routes.")
    # Route Analysis content will be added later

elif page == "Delay Prediction":
    st.markdown(
        '<div class="sub-header">Delay Prediction</div>', unsafe_allow_html=True
    )
    st.write("Predict potential delays for future train journeys.")
    # Delay Prediction content will be added later

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">TARDIS - Train Analysis and Reporting Dashboard for Intelligent Scheduling<br>Developed by SNCF Data Analysis Service</div>',
    unsafe_allow_html=True,
)

# Add after the sidebar navigation section and before the page content sections

# Date range filter
st.sidebar.markdown("---")
st.sidebar.title("Filters")

# Extract min and max dates from the dataset
if "Date" in df.columns:
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[
            (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
        ]
    else:
        filtered_df = df.copy()
else:
    filtered_df = df.copy()

# Station filter
if "Departure station" in df.columns and "Arrival station" in df.columns:
    stations = sorted(
        set(df["Departure station"].dropna().unique())
        | set(df["Arrival station"].dropna().unique())
    )
    selected_station = st.sidebar.selectbox("Filter by Station", ["All"] + stations)

    if selected_station != "All":
        filtered_df = filtered_df[
            (filtered_df["Departure station"] == selected_station)
            | (filtered_df["Arrival station"] == selected_station)
        ]

# Service filter
if "Service" in df.columns:
    services = sorted(df["Service"].dropna().unique())
    if len(services) > 1:  # Only show if there are multiple service types
        selected_service = st.sidebar.selectbox(
            "Filter by Service Type", ["All"] + list(services)
        )

        if selected_service != "All":
            filtered_df = filtered_df[filtered_df["Service"] == selected_service]

# Display selected filters
st.sidebar.markdown("---")
st.sidebar.write("**Displaying data for:**")
if "Date" in df.columns and len(date_range) == 2:
    st.sidebar.write(f"- Period: {start_date} to {end_date}")
if (
    "Departure station" in df.columns
    and "selected_station" in locals()
    and selected_station != "All"
):
    st.sidebar.write(f"- Station: {selected_station}")
if (
    "Service" in df.columns
    and "selected_service" in locals()
    and selected_service != "All"
):
    st.sidebar.write(f"- Service: {selected_service}")

# Replace the Overview page section with this more detailed implementation
if page == "Overview":
    st.markdown(
        '<div class="sub-header">Overview Dashboard</div>', unsafe_allow_html=True
    )
    st.write(
        "Welcome to the TARDIS (Train Analysis and Reporting Dashboard for Intelligent Scheduling) system. This dashboard provides insights into train delays and helps predict future patterns."
    )

    # Summary metrics
    st.markdown('<div class="sub-header">Key Metrics</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        avg_delay = filtered_df["Average delay of all trains at arrival"].mean()
        st.markdown(
            f'<div class="metric-value">{avg_delay:.2f} min</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="metric-label">Average Delay</div>', unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if "Number of cancelled trains" in filtered_df.columns:
            cancelled = filtered_df["Number of cancelled trains"].sum()
            st.markdown(
                f'<div class="metric-value">{int(cancelled)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Cancelled Trains</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="metric-value">N/A</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="metric-label">Data not available</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if "Number of trains delayed > 15min" in filtered_df.columns:
            significant_delays = filtered_df["Number of trains delayed > 15min"].sum()
            st.markdown(
                f'<div class="metric-value">{int(significant_delays)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Trains > 15min Late</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="metric-value">N/A</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="metric-label">Data not available</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if "Total_Delay_Score" in filtered_df.columns:
            avg_delay_score = filtered_df["Total_Delay_Score"].mean()
            st.markdown(
                f'<div class="metric-value">{avg_delay_score:.2f}%</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Avg Delay Score</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="metric-value">N/A</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="metric-label">Data not available</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Monthly trend chart
    st.markdown(
        '<div class="sub-header">Monthly Delay Trends</div>', unsafe_allow_html=True
    )

    if "Date" in filtered_df.columns:
        monthly_data = (
            filtered_df.groupby(pd.Grouper(key="Date", freq="M"))[
                "Average delay of all trains at arrival"
            ]
            .mean()
            .reset_index()
        )
        monthly_data["Month"] = monthly_data["Date"].dt.strftime("%Y-%m")

        fig = px.line(
            monthly_data,
            x="Month",
            y="Average delay of all trains at arrival",
            title="Average Delay by Month",
            labels={
                "Average delay of all trains at arrival": "Average Delay (minutes)",
                "Month": "Month",
            },
            markers=True,
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Date information is not available in the dataset")

    # Delay causes breakdown
    st.markdown('<div class="sub-header">Delay Causes</div>', unsafe_allow_html=True)

    delay_cause_columns = [
        col for col in filtered_df.columns if "Pct delay due to" in col
    ]
    if delay_cause_columns:
        avg_delay_causes = filtered_df[delay_cause_columns].mean().reset_index()
        avg_delay_causes.columns = ["Cause", "Percentage"]
        avg_delay_causes["Cause"] = avg_delay_causes["Cause"].str.replace(
            "Pct delay due to ", ""
        )

        fig = px.bar(
            avg_delay_causes,
            y="Cause",
            x="Percentage",
            title="Average Percentage of Delays by Cause",
            labels={"Percentage": "Percentage (%)", "Cause": "Cause"},
            orientation="h",
        )
        fig.update_layout(height=400, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Delay cause information is not available in the dataset")

elif page == "Delay Analysis":
    st.markdown('<div class="sub-header">Delay Analysis</div>', unsafe_allow_html=True)
    st.write("Explore detailed patterns and distributions of train delays.")

    # Delay distribution
    st.markdown(
        '<div class="sub-header">Delay Distribution</div>', unsafe_allow_html=True
    )

    delay_col = "Average delay of all trains at arrival"
    if delay_col in filtered_df.columns:
        fig = px.histogram(
            filtered_df,
            x=delay_col,
            title="Distribution of Delays",
            labels={delay_col: "Delay (minutes)"},
            nbins=30,
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Descriptive statistics
        st.markdown(
            '<div class="sub-header">Delay Statistics</div>', unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-value">{filtered_df[delay_col].min():.2f}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Min Delay (min)</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-value">{filtered_df[delay_col].max():.2f}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Max Delay (min)</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-value">{filtered_df[delay_col].median():.2f}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Median Delay (min)</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-value">{filtered_df[delay_col].std():.2f}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="metric-label">Std Deviation (min)</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Seasonal patterns
        if "Season" in filtered_df.columns:
            st.markdown(
                '<div class="sub-header">Seasonal Patterns</div>',
                unsafe_allow_html=True,
            )

            season_data = filtered_df.groupby("Season")[delay_col].mean().reset_index()
            season_order = ["Winter", "Spring", "Summer", "Fall"]
            season_data["Season"] = pd.Categorical(
                season_data["Season"], categories=season_order, ordered=True
            )
            season_data = season_data.sort_values("Season")

            fig = px.bar(
                season_data,
                x="Season",
                y=delay_col,
                title="Average Delay by Season",
                labels={delay_col: "Average Delay (minutes)", "Season": "Season"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Delay information is not available in the dataset")

    # Delay severity analysis
    if "Delay_Category" in filtered_df.columns:
        st.markdown(
            '<div class="sub-header">Delay Severity Analysis</div>',
            unsafe_allow_html=True,
        )

        delay_category_counts = (
            filtered_df["Delay_Category"].value_counts().reset_index()
        )
        delay_category_counts.columns = ["Category", "Count"]

        # Order the categories
        category_order = ["Minimal", "Moderate", "Significant", "Severe"]
        delay_category_counts["Category"] = pd.Categorical(
            delay_category_counts["Category"], categories=category_order, ordered=True
        )
        delay_category_counts = delay_category_counts.sort_values("Category")

        # Assign colors based on severity
        colors = {
            "Minimal": "#10B981",
            "Moderate": "#F59E0B",
            "Significant": "#EF4444",
            "Severe": "#7F1D1D",
        }
        color_discrete_map = {
            cat: colors[cat]
            for cat in delay_category_counts["Category"]
            if cat in colors
        }

        fig = px.pie(
            delay_category_counts,
            values="Count",
            names="Category",
            title="Distribution of Delay Severity",
            color="Category",
            color_discrete_map=color_discrete_map,
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "Station Insights":
    st.markdown(
        '<div class="sub-header">Station Insights</div>', unsafe_allow_html=True
    )
    st.write("Analyze delay patterns by stations.")

    if (
        "Departure station" in filtered_df.columns
        and "Average delay of all trains at departure" in filtered_df.columns
    ):
        # Top stations with most delays at departure
        st.markdown(
            '<div class="sub-header">Top Stations with Highest Departure Delays</div>',
            unsafe_allow_html=True,
        )

        station_delays = (
            filtered_df.groupby("Departure station")[
                "Average delay of all trains at departure"
            ]
            .mean()
            .reset_index()
        )
        station_delays = station_delays.sort_values(
            "Average delay of all trains at departure", ascending=False
        ).head(15)

        fig = px.bar(
            station_delays,
            x="Average delay of all trains at departure",
            y="Departure station",
            title="Top 15 Departure Stations with Highest Average Delays",
            labels={
                "Average delay of all trains at departure": "Average Delay (minutes)",
                "Departure station": "Station",
            },
            orientation="h",
        )
        fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    if (
        "Arrival station" in filtered_df.columns
        and "Average delay of all trains at arrival" in filtered_df.columns
    ):
        # Top stations with most delays at arrival
        st.markdown(
            '<div class="sub-header">Top Stations with Highest Arrival Delays</div>',
            unsafe_allow_html=True,
        )

        station_delays = (
            filtered_df.groupby("Arrival station")[
                "Average delay of all trains at arrival"
            ]
            .mean()
            .reset_index()
        )
        station_delays = station_delays.sort_values(
            "Average delay of all trains at arrival", ascending=False
        ).head(15)

        fig = px.bar(
            station_delays,
            x="Average delay of all trains at arrival",
            y="Arrival station",
            title="Top 15 Arrival Stations with Highest Average Delays",
            labels={
                "Average delay of all trains at arrival": "Average Delay (minutes)",
                "Arrival station": "Station",
            },
            orientation="h",
        )
        fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    # Station specific analysis
    st.markdown(
        '<div class="sub-header">Station-Specific Analysis</div>',
        unsafe_allow_html=True,
    )

    # Let user select a specific station
    all_stations = []
    if "Departure station" in filtered_df.columns:
        all_stations.extend(filtered_df["Departure station"].dropna().unique())
    if "Arrival station" in filtered_df.columns:
        all_stations.extend(filtered_df["Arrival station"].dropna().unique())

    all_stations = sorted(set(all_stations))

    if all_stations:
        selected_analysis_station = st.selectbox(
            "Select a Station for Detailed Analysis", all_stations
        )

        # Filter data for selected station
        station_data_departure = (
            filtered_df[filtered_df["Departure station"] == selected_analysis_station]
            if "Departure station" in filtered_df.columns
            else pd.DataFrame()
        )
        station_data_arrival = (
            filtered_df[filtered_df["Arrival station"] == selected_analysis_station]
            if "Arrival station" in filtered_df.columns
            else pd.DataFrame()
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**{selected_analysis_station} as Departure Station**")
            if (
                not station_data_departure.empty
                and "Average delay of all trains at departure"
                in station_data_departure.columns
            ):
                st.metric(
                    "Average Departure Delay",
                    f"{station_data_departure['Average delay of all trains at departure'].mean():.2f} min",
                )

                if "Date" in station_data_departure.columns:
                    monthly_station_data = (
                        station_data_departure.groupby(
                            pd.Grouper(key="Date", freq="M")
                        )["Average delay of all trains at departure"]
                        .mean()
                        .reset_index()
                    )
                    monthly_station_data["Month"] = monthly_station_data[
                        "Date"
                    ].dt.strftime("%Y-%m")

                    fig = px.line(
                        monthly_station_data,
                        x="Month",
                        y="Average delay of all trains at departure",
                        title=f"Monthly Departure Delays from {selected_analysis_station}",
                        labels={
                            "Average delay of all trains at departure": "Avg Delay (min)",
                            "Month": "Month",
                        },
                        markers=True,
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    f"No data available for {selected_analysis_station} as a departure station"
                )

        with col2:
            st.markdown(f"**{selected_analysis_station} as Arrival Station**")
            if (
                not station_data_arrival.empty
                and "Average delay of all trains at arrival"
                in station_data_arrival.columns
            ):
                st.metric(
                    "Average Arrival Delay",
                    f"{station_data_arrival['Average delay of all trains at arrival'].mean():.2f} min",
                )

                if "Date" in station_data_arrival.columns:
                    monthly_station_data = (
                        station_data_arrival.groupby(pd.Grouper(key="Date", freq="M"))[
                            "Average delay of all trains at arrival"
                        ]
                        .mean()
                        .reset_index()
                    )
                    monthly_station_data["Month"] = monthly_station_data[
                        "Date"
                    ].dt.strftime("%Y-%m")

                    fig = px.line(
                        monthly_station_data,
                        x="Month",
                        y="Average delay of all trains at arrival",
                        title=f"Monthly Arrival Delays at {selected_analysis_station}",
                        labels={
                            "Average delay of all trains at arrival": "Avg Delay (min)",
                            "Month": "Month",
                        },
                        markers=True,
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    f"No data available for {selected_analysis_station} as an arrival station"
                )
    else:
        st.info("Station information is not available in the dataset")

elif page == "Route Analysis":
    st.markdown('<div class="sub-header">Route Analysis</div>', unsafe_allow_html=True)
    st.write("Analyze delay patterns by routes.")

    if (
        "Route" in filtered_df.columns
        and "Average delay of all trains at arrival" in filtered_df.columns
    ):
        # Top routes with most delays
        st.markdown(
            '<div class="sub-header">Top Routes with Highest Delays</div>',
            unsafe_allow_html=True,
        )

        route_delays = (
            filtered_df.groupby("Route")["Average delay of all trains at arrival"]
            .mean()
            .reset_index()
        )
        route_delays = route_delays.sort_values(
            "Average delay of all trains at arrival", ascending=False
        ).head(15)

        fig = px.bar(
            route_delays,
            x="Average delay of all trains at arrival",
            y="Route",
            title="Top 15 Routes with Highest Average Delays",
            labels={
                "Average delay of all trains at arrival": "Average Delay (minutes)",
                "Route": "Route",
            },
            orientation="h",
        )
        fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

        # Route comparison tool
        st.markdown(
            '<div class="sub-header">Route Comparison</div>', unsafe_allow_html=True
        )

        # Get all routes
        all_routes = sorted(filtered_df["Route"].dropna().unique())

        # Let user select routes to compare
        selected_routes = st.multiselect(
            "Select Routes to Compare", all_routes, max_selections=5
        )

        if selected_routes:
            # Filter data for selected routes
            routes_data = filtered_df[filtered_df["Route"].isin(selected_routes)]

            # Average delay by route
            route_avg_delays = (
                routes_data.groupby("Route")["Average delay of all trains at arrival"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                route_avg_delays,
                x="Route",
                y="Average delay of all trains at arrival",
                title="Average Delay Comparison by Route",
                labels={
                    "Average delay of all trains at arrival": "Average Delay (minutes)",
                    "Route": "Route",
                },
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            # If we have date information, show trends over time
            if "Date" in routes_data.columns:
                st.markdown("**Monthly Delay Trends by Route**")

                monthly_route_data = (
                    routes_data.groupby(["Route", pd.Grouper(key="Date", freq="M")])[
                        "Average delay of all trains at arrival"
                    ]
                    .mean()
                    .reset_index()
                )
                monthly_route_data["Month"] = monthly_route_data["Date"].dt.strftime(
                    "%Y-%m"
                )

                fig = px.line(
                    monthly_route_data,
                    x="Month",
                    y="Average delay of all trains at arrival",
                    color="Route",
                    title="Monthly Delay Trends by Route",
                    labels={
                        "Average delay of all trains at arrival": "Average Delay (minutes)",
                        "Month": "Month",
                    },
                    markers=True,
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

            # Show delay cause breakdown by route if available
            delay_cause_columns = [
                col for col in filtered_df.columns if "Pct delay due to" in col
            ]
            if delay_cause_columns:
                st.markdown("**Delay Causes by Route**")

                # Calculate average percentages for each cause by route
                route_causes = (
                    routes_data.groupby("Route")[delay_cause_columns]
                    .mean()
                    .reset_index()
                )

                # Melt the dataframe for easier plotting
                route_causes_melted = pd.melt(
                    route_causes,
                    id_vars=["Route"],
                    value_vars=delay_cause_columns,
                    var_name="Cause",
                    value_name="Percentage",
                )

                # Clean up cause names
                route_causes_melted["Cause"] = route_causes_melted["Cause"].str.replace(
                    "Pct delay due to ", ""
                )
                fig = px.bar(
                    route_causes_melted,
                    x="Route",
                    y="Percentage",
                    color="Cause",
                    title="Delay Causes by Route",
                    labels={"Percentage": "Percentage (%)", "Route": "Route"},
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
elif page == "Delay Prediction":
    st.markdown(
        '<div class="sub-header">Delay Prediction</div>', unsafe_allow_html=True
    )
    st.write(
        "Predict potential delays for future train journeys using our machine learning model."
    )

    if model is None or model_info is None:
        st.error(
            "Prediction model is not available. Please ensure the model files are loaded correctly."
        )
    else:
        st.success(f"Using {model_info['model_name']} model for predictions")

        # Show model metrics if available
        if "metrics" in model_info:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Model RMSE", f"{model_info['metrics']['rmse']:.2f}")
            with col2:
                st.metric("Model R² Score", f"{model_info['metrics']['r2']:.2f}")

        # Add styling for delay categories
        st.markdown(
            """
        <style>
            .delay-minimal {
                color: #10B981;
            }
            .delay-moderate {
                color: #F59E0B;
            }
            .delay-significant {
                color: #EF4444;
            }
            .delay-severe {
                color: #7F1D1D;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Form for prediction inputs
        st.markdown(
            '<div class="sub-header">Enter Journey Details</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        # Input data dictionary to store all prediction parameters
        input_data = {}

        with col1:
            # Service Type
            if "Service" in model_info["categorical_features"]:
                services = sorted(filtered_df["Service"].dropna().unique())
                selected_service = st.selectbox("Service Type", services)
                input_data["Service"] = selected_service

            # Departure Station
            departure_stations = sorted(
                filtered_df["Departure station"].dropna().unique()
            )
            selected_departure = st.selectbox("Departure Station", departure_stations)
            input_data["Departure station"] = selected_departure

            # Find valid arrival stations based on departure station selection
            valid_arrival_stations = (
                filtered_df[filtered_df["Departure station"] == selected_departure][
                    "Arrival station"
                ]
                .dropna()
                .unique()
            )

            if len(valid_arrival_stations) == 0:
                st.warning(
                    f"No connections found from {selected_departure}. Please select another departure station."
                )
                valid_arrival_stations = sorted(
                    filtered_df["Arrival station"].dropna().unique()
                )
            else:
                valid_arrival_stations = sorted(valid_arrival_stations)

            # Arrival Station
            selected_arrival = st.selectbox("Arrival Station", valid_arrival_stations)
            input_data["Arrival station"] = selected_arrival

            # Season
            if "Season" in model_info["categorical_features"]:
                seasons = ["Winter", "Spring", "Summer", "Fall"]
                selected_season = st.selectbox("Season", seasons)
                input_data["Season"] = selected_season

            # Add any other categorical features that might be in the model
            for feature in model_info["categorical_features"]:
                if feature not in [
                    "Service",
                    "Departure station",
                    "Arrival station",
                    "Season",
                ]:
                    unique_values = sorted(filtered_df[feature].dropna().unique())
                    input_data[feature] = st.selectbox(feature, unique_values)

        # After selecting stations, get the route-specific data
        route_data = filtered_df[
            (filtered_df["Departure station"] == selected_departure)
            & (filtered_df["Arrival station"] == selected_arrival)
        ]

        with col2:
            st.markdown("**Route Statistics**")

            if not route_data.empty:
                # Display automatic route statistics and use these values for prediction
                avg_journey_time = route_data["Average journey time"].mean()
                st.metric("Average Journey Time", f"{avg_journey_time:.2f} min")
                input_data["Average journey time"] = avg_journey_time

                if "Number of scheduled trains" in route_data.columns:
                    avg_scheduled = route_data["Number of scheduled trains"].mean()
                    st.metric("Avg. Scheduled Trains", f"{avg_scheduled:.0f}")
                    input_data["Number of scheduled trains"] = avg_scheduled

                if "Number of cancelled trains" in route_data.columns:
                    avg_cancelled = route_data["Number of cancelled trains"].mean()
                    st.metric("Avg. Cancelled Trains", f"{avg_cancelled:.1f}")
                    input_data["Number of cancelled trains"] = avg_cancelled

                if "Average delay of all trains at departure" in route_data.columns:
                    avg_departure_delay = route_data[
                        "Average delay of all trains at departure"
                    ].mean()
                    st.metric("Avg. Departure Delay", f"{avg_departure_delay:.2f} min")
                    input_data["Average delay of all trains at departure"] = (
                        avg_departure_delay
                    )

                # Historical arrival delay (for reference, not used in prediction)
                if "Average delay of all trains at arrival" in route_data.columns:
                    avg_arrival_delay = route_data[
                        "Average delay of all trains at arrival"
                    ].mean()
                    st.metric(
                        "Historical Arrival Delay", f"{avg_arrival_delay:.2f} min"
                    )
            else:
                st.warning(
                    f"No historical data for route: {selected_departure} to {selected_arrival}"
                )
                # Use dataset averages as fallbacks
                input_data["Average journey time"] = filtered_df[
                    "Average journey time"
                ].mean()

                if "Number of scheduled trains" in filtered_df.columns:
                    input_data["Number of scheduled trains"] = filtered_df[
                        "Number of scheduled trains"
                    ].mean()

                if "Number of cancelled trains" in filtered_df.columns:
                    input_data["Number of cancelled trains"] = filtered_df[
                        "Number of cancelled trains"
                    ].mean()

                if "Average delay of all trains at departure" in filtered_df.columns:
                    input_data["Average delay of all trains at departure"] = (
                        filtered_df["Average delay of all trains at departure"].mean()
                    )

            # Add current date-related features
            today = datetime.now()
            input_data["Year"] = today.year
            input_data["Month"] = today.month

            # External delay cause factors (if in the model)
            st.markdown("**Delay Factors (%)**")
            delay_cause_columns = [
                col
                for col in model_info["numerical_features"]
                if "Pct delay due to" in col
            ]

            # Use historical averages from the selected route if available
            for col in delay_cause_columns:
                # Extract the main part of the cause for display
                display_name = col.replace("Pct delay due to ", "")

                if not route_data.empty and col in route_data.columns:
                    default_value = route_data[col].mean()
                else:
                    default_value = (
                        filtered_df[col].mean() if col in filtered_df.columns else 10.0
                    )

                # Make the sliders editable by users for custom scenarios
                input_data[col] = st.slider(
                    display_name, 0.0, 100.0, float(default_value)
                )

        # Make prediction button
        if st.button("Predict Delay"):
            try:
                # Ensure all required features are available
                for feature in model_info["numerical_features"]:
                    if feature not in input_data:
                        input_data[feature] = (
                            filtered_df[feature].median()
                            if feature in filtered_df.columns
                            else 0
                        )

                for feature in model_info["categorical_features"]:
                    if feature not in input_data:
                        input_data[feature] = (
                            filtered_df[feature].mode()[0]
                            if feature in filtered_df.columns
                            else ""
                        )

                # Create DataFrame with a single row for prediction
                input_df = pd.DataFrame([input_data])

                # Make prediction
                prediction = model.predict(input_df)[0]

                # Display result
                st.markdown(
                    '<div class="sub-header">Prediction Result</div>',
                    unsafe_allow_html=True,
                )

                # Determine delay category
                if prediction <= 5:
                    delay_category = "Minimal"
                    color_class = "delay-minimal"
                elif prediction <= 15:
                    delay_category = "Moderate"
                    color_class = "delay-moderate"
                elif prediction <= 30:
                    delay_category = "Significant"
                    color_class = "delay-significant"
                else:
                    delay_category = "Severe"
                    color_class = "delay-severe"

                st.markdown(
                    f"""
                <div class="card">
                    <h3>Predicted Delay</h3>
                    <div class="metric-value {color_class}">{prediction:.2f} minutes</div>
                    <div class="metric-label">Delay Category: {delay_category}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Add contextual information
                route = f"{selected_departure} to {selected_arrival}"

                # Explanation of factors
                st.markdown(
                    '<div class="sub-header">Contributing Factors</div>',
                    unsafe_allow_html=True,
                )

                # If we're using a tree-based model that has feature importances
                if hasattr(model.named_steps["model"], "feature_importances_"):
                    # Get feature importances
                    importances = model.named_steps["model"].feature_importances_

                    # Get feature names after preprocessing (if available)
                    feature_names = []

                    # Get numeric feature names (these stay the same)
                    feature_names.extend(model_info["numerical_features"])

                    # For categorical features, we would need the one-hot encoded feature names
                    # But since this is complex to recreate here, we'll use the original feature names
                    feature_names.extend(model_info["categorical_features"])

                    # Create a dataframe of features and their importances
                    feature_importance = pd.DataFrame(
                        {
                            "Feature": feature_names[: len(importances)]
                            if len(feature_names) >= len(importances)
                            else feature_names
                            + ["Unknown"] * (len(importances) - len(feature_names)),
                            "Importance": importances,
                        }
                    )

                    # Sort by importance
                    feature_importance = feature_importance.sort_values(
                        "Importance", ascending=False
                    ).head(5)

                    # Display
                    st.write("Top factors influencing delays:")

                    for i, (feature, importance) in enumerate(
                        zip(
                            feature_importance["Feature"],
                            feature_importance["Importance"],
                        )
                    ):
                        st.write(f"{i + 1}. **{feature}**: {importance:.2%}")
                else:
                    st.write("Factors that generally contribute to delays include:")
                    st.write("1. **Weather conditions** (external causes)")
                    st.write(
                        "2. **Infrastructure issues** (track or signaling problems)"
                    )
                    st.write("3. **Traffic management** (congestion or scheduling)")
                    st.write("4. **Rolling stock problems** (mechanical issues)")
                    st.write(
                        "5. **Station management** (boarding procedures or equipment reuse)"
                    )

            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")
                st.write("Please check your input values and try again.")
