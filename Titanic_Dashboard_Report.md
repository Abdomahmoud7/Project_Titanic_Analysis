# Titanic Passenger Analysis Report

## Executive Summary
This report accompanies the **Titanic Interactive Dashboard**, providing an overview of the passenger demographics and survival rates aboard the RMS Titanic. The interactive dashboard allows for real-time filtering and visualization of the dataset, making it easy to uncover patterns related to passenger class, gender, age, and embarkation points.

## Dataset Overview
The dataset contains information on 1,309 passengers, including their socio-economic status (Ticket Class), age, gender, fare paid, and whether they survived the tragic sinking. 

Key attributes analyzed include:
- **Passenger Class (Pclass):** 1st, 2nd, and 3rd class.
- **Gender (Sex):** Male and Female.
- **Age:** Passenger's age in years.
- **Embarked:** Port of embarkation (Southampton, Cherbourg, Queenstown).
- **Survived:** Survival status (1 = Survived, 0 = Perished).

## Key Insights from the Dashboard

### 1. Overall Survival Rate
The overall survival rate across the dataset is roughly **38.2%**, meaning a significant majority of the passengers did not survive. The dashboard prominently displays this KPI, updating dynamically based on the applied filters.

### 2. Gender and Survival (Women and Children First)
The "Women and children first" protocol had a massive impact on survival rates:
- **Females** had a dramatically higher survival rate compared to males.
- The **Gender Distribution** doughnut chart visualizes the stark contrast, showing that the majority of survivors were female, while the vast majority of casualties were male.

### 3. Socio-Economic Status (Passenger Class)
Passenger class strongly correlated with survival:
- **1st Class** passengers had the highest survival rate, significantly outperforming 2nd and 3rd classes.
- **3rd Class** passengers had the highest number of casualties. 
- The **Survival by Passenger Class** bar chart perfectly illustrates this socio-economic disparity.

### 4. Age Distribution
- The highest concentration of passengers was in the **21-30** age group.
- Younger age brackets (especially children aged 0-10) had relatively high survival rates compared to middle-aged males in lower ticket classes.
- The **Survival by Age Group** chart provides a stacked view of how different age demographics fared.

### 5. Embarkation Ports
- Most passengers boarded the Titanic at **Southampton (S)**.
- Passengers embarking from **Cherbourg (C)** had a proportionately higher survival rate, which correlates with a larger percentage of 1st-class passengers boarding at that port.

## Using the Dashboard
The accompanying `Titanic_Interactive_Dashboard.html` is a standalone, single-file application. 

**Features:**
- **Dynamic KPI Cards:** Automatically calculate total passengers, average age, average fare, and survival rate based on current filters.
- **Interactive Charts:** Hover over the charts to view exact data points and tooltips.
- **Live Filtering:** Use the dropdowns at the top to filter the entire dashboard by Passenger Class, Gender, or Embarkation Port.
- **Data Table:** A snapshot table at the bottom showing a sample of the raw passenger records currently in view.

**How to Share:**
Because all data and styling are bundled into this single HTML file, you can easily share the dashboard by sending the `Titanic_Interactive_Dashboard.html` file via email or any messaging app. Anyone can open it using a standard web browser (Chrome, Edge, Safari) without needing to install anything or connect to a database.
