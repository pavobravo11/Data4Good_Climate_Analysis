
<h1>Calgary Air Quality Analysis</h1>

<nav class="topnav">
      <a class="active" href="#home">Home</a>
      <a href="#about">About the Data</a>
      <a href="#real_time">Real Time Data</a>
      <a href="#history">History</a>
      <a href="#predictions">Future</a>
      <a href="#sources">Data Sources</a>
      <a href="#resources">Additional Resources</a>
</nav>
<h3 id="about">About the Data</h3>

Climate change has significant environmental, health, and socio-economic impacts. The long-term effects of climate change are felt in increased intensity and frequency of extreme weather that are disrupting lives in every country on every continent.  While there have been significant climate change events in the Earth’s history, the current changes are occurring rapidly and are not due to natural causes.  Anthropogenic practices, such as burning of fossil fuels and forest loss, contribute to increased carbon dioxide (CO2) and other greenhouse gases (GHGs) in the atmosphere. According to the United Nations, greenhouse gases rose to new records in 2019, resulting in the second warmest year on record.  While the early stages of the COVID-19 pandemic saw a drop in CO2 emissions, this event was temporary, and emissions will gradually return to higher levels as economies begin to recover.

In 2019, Alberta represented 38% of the GHG emissions in Canada at 275.8 megatonnes of CO2 equivalent (MtCO2eq) out of 270 MtCO2eq, the highest nationwide.  In the same year, Calgary as the most populated city in Alberta, contributed 18.3MtCO2eq.  In November 2021, the Calgary City Council declared a Climate Emergency.  

A team with Data for Good Calgary took on the opportunity to help citizens learn about their city by founding the idea of using data and technology to raise awareness on Calgary’s climate change impact. Data for Good’s goal is to present free and accessible baseline emissions data in an easy-to-use platform to serve citizens, city decision makers, researchers, and solution providers in identifying and leveraging climate action opportunities in the city and beyond.

Historical emissions and air quality data were collected from the City of Calgary and the Government of Canada open inventories, and are presented on an interactive dashboard for the years 1990-2019.  In addition, data modelling is used to present hourly air quality and particulate matter (PM2.5) information from iQAir, connecting real-time data collection points to each neighbourhood in Calgary.  These aggregated historical and current emissions data can be further specified to individual outputs by industry or activity, such as land use from agriculture and construction, and create opportunities for standardized data collection methodologies and collaboration with other tools.  By drawing insights from the major sources of GHG emissions, subsequent climate action planning, solutions, and community engagement can be accelerated, and contribute to The City of Calgary’s Climate Strategy to net zero by 2050.
<br>

<h3 id="real_time">Real Time Data</h3>
    <div id="aiqmap" class="plotly-graph-div" style="height:100%; width:100%;"></div>

<h3 id="history">Calgary's Climate History</h3>

<h4>Calgary Emissions Report - Power BI</h4>
<iframe title="Community-wide_Greenhouse_Gas__GHG__Inventory" width="100%" height="700" src="https://app.powerbi.com/view?r=eyJrIjoiMzRhZDBkNWYtZTIyZC00NGE5LWE4YWYtZmFmOGU5ZjQxNGM1IiwidCI6IjEwNjBmY2QwLWNmMjMtNDQ4YS05ZGFhLWZhYWQ0YjczMDYzMiJ9&pageName=ReportSection" frameborder="5" allowFullScreen="true"></iframe>

<h4 >Calgary Average AQI vs Traffic in the City</h4>
<img src="aiq_traffic.png" alt="Traffic History from Calgary" style="width:1100px;height:500px;">

The Jupyter Notebook servig as source for this graphic and others can beinteracted with on  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pavobravo11/Data4Good_Climate_Analysis/HEAD)

<h3 id="predictions">Future Predictions Using Exponential Smoothing</h3>

Based on historical monthly data and Holt Winter's method we devised a relatively simple model to predict particle
matter pollution, methane concentration and values for Air Quality Index data on a by-station basis.
A central concept of the used method, on which the interested reader can find more [here](https://orangematter.solarwinds.com/2019/12/15/holt-winters-forecasting-simplified/#:~:text=Holt%2DWinters%20is%20a%20model,cyclical%20repeating%20pattern%20(seasonality)),
is seasonality.

While the seasonality for the AIQ can easily be discovered by looking at the historical line chart the seasonality for
PM2.5 concentration was determined by using grid search over a reasonable parameter space, 
trying to reduce the mean squared error on prediction.

Unfortunately the results differed between stations, indicating that the seasonal periodicity is either 3 or 4 months.
This, together with other statistical factors, indicate that at least for PM2.5 concentration the seasonal component is
not a clear determining factor. Indeed additional data (forest fires, wind, ...) could account for some variance
and further examination might be needed.

<div id="predictions_plotly" class="plotly-graph-div" style="height:100%; width:100%;"></div>


<div id="info_box">
<h3 id="sources">Data Sources</h3>
    <a href="https://data.calgary.ca/Base-Maps/Community-Boundaries/ab7m-fwn6" target="_blank" rel="noopener noreferrer">
        • City of Calgary Community District Boundaries
    </a><br>
    <a href="https://data.calgary.ca/Environment/Community-wide-Greenhouse-Gas-GHG-Inventory/m7gu-3xk5" target="_blank" rel="noopener noreferrer">
        • City of Calgary Community-wide Greenhouse Gas Inventory 
    </a><br>
    <a href="https://data.calgary.ca/Environment/Historical-Air-Quality/uqjm-jxgp" target="_blank" rel="noopener noreferrer">
        • City of Calgary Historical Air Quality Open Data
    </a><br>
    <a href="https://www.iqair.com/ca/canada/alberta/calgary" target="_blank" rel="noopener noreferrer">
        • IQAir - Calgary Air Quality index (AQI) and PM2.5 Air Pollution 
    </a><br>

<h3 id="resources">References</h3>
    <a href="https://www.calgary.ca/uep/esm/energy-savings/climate-change.html#emergency" target="_blank" rel="noopener noreferrer">
        • City of Calgary Climate Change Program
    </a><br>
    <a href="https://www.canada.ca/en/environment-climate-change/services/environmental-indicators/greenhouse-gas-emissions.html" target="_blank" rel="noopener noreferrer">
        • Government of Canada National Greenhouse Gas Emissions 
    </a><br>
    <a href="https://www.un.org/en/climatechange" target="_blank" rel="noopener noreferrer">
        • United Nations Climate Action
    </a><br>

<h3>Real-Time Data Twitter Bot (Made by Us)</h3>
    <a href="https://twitter.com/climateYYC45" target="_blank" rel="noopener noreferrer">
        • Twitter Link
    </a><br>


<h3>Additional Resources</h3>
    <a href="https://acis.alberta.ca/" target="_blank" rel="noopener noreferrer">
        • Alberta Climate Information Service
    </a><br>
    <a href="https://www.calgaryclimatehub.ca/" target="_blank" rel="noopener noreferrer">
        • ​​Calgary Climate Hub
    </a><br>
    <a href="https://www.calgary.ca/uep/esm/climate-change/climate-actions.html" target="_blank" rel="noopener noreferrer">
        • City of Calgary Climate Resilience Strategy Action Plans
    </a><br>
    <a href="https://climateatlas.ca/" target="_blank" rel="noopener noreferrer">
        • Climate Atlas of Canada
    </a><br>
    <a href="https://www.canada.ca/en/services/environment/weather/climatechange.html" target="_blank" rel="noopener noreferrer">
        • Government of Canada Climate Change
    </a><br>
    <a href="https://www.canada.ca/en/environment-climate-change/services/climate-change/greenhouse-gas-emissions/inventory.html" target="_blank" rel="noopener noreferrer">
        • Government of Canada Greenhouse Gas Inventory
    </a><br>
    <a href="https://unfccc.int/" target="_blank" rel="noopener noreferrer">
        • United Nations Framework Convention on Climate Change
    </a><br>
</div>