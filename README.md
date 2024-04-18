# SenateStockInsights

The objective of our project is to scrutinize U.S. senators' stock transactions, aiming to uncover suspicious patterns indicative of insider trading or ethical breaches. By examining mandatory stock disclosure filings from 2012 onwards, mandated by the STOCK Act, we seek to promote transparency and accountability in government institutions, crucial for upholding democratic principles.

# Motivation

In recent years, the financial activities of members of the United States Congress have come under intense scrutiny, with allegations of potential insider trading and conflicts of interest. This scrutiny arises from concerns that elected officials may possess privileged information, giving them an unfair advantage in the stock market.

The passage of the STOCK Act in 2012 aimed to address these concerns by prohibiting the use of non-public information for personal gain and mandating the disclosure of stock transactions by government officials. Despite these regulatory efforts, questions persist about the effectiveness of enforcement and the prevalence of unethical trading practices.

Our motivation stems from the need to shed light on the impact of legislative actions on financial markets and public trust. By analyzing the Return on Investment (ROI) of senators over the past decade, we aim to assess the influence of the STOCK Act and provide insights into the ethical conduct of elected representatives.

Through our project, we seek to contribute to the ongoing discourse on financial ethics and accountability in government institutions, ultimately fostering transparency and restoring public confidence in the democratic process.

# Features

Our project offers the following key features to analyze and visualize stock transactions by U.S. senators:

- **Calculate Annual Return on Investment (ROI)**: Compute the annual ROI for each senator's stock transactions, providing insights into their investment performance over time.

- **Categorize Senators Based on ROI**: Classify senators into high, medium, and low ROI categories, enabling easy identification of trading success rates among legislators.

- **Graph Visualization of Senators and Transactions**: Visualize the network graph representing senators and their stock transactions, facilitating a comprehensive understanding of trading patterns and relationships.

- **State-Level ROI Analysis**: Calculate and visualize the ROI of senators at the state level, highlighting regions with the highest and lowest investment returns.

- **Top Stocks Transacted Analysis**: Determine and visualize the most and least popular stocks transacted by senators over the past decade, providing insights into investment trends within legislative circles.


# Technical Details
Our project implementation involved several key technical decisions and utilized various libraries and tools:

1. **Data Structure and Graph Representation**:
   - To accommodate the unique attributes of senators and stocks, we implemented two separate instances of the Vertex class: SenatorVertex and StockVertex.
   - We utilized dictionaries to store transaction numbers as edge data for the two graphs, facilitating efficient representation and traversal.

2. **Graph Loading Functionality**:
   - Our load graph function reads the CSV file containing transaction data, converts it into a pandas dataframe, and creates nodes and edges based on unique senators and stocks.
   - This function establishes connections between senator and stock vertices through edges, facilitating subsequent analysis.

3. **Stock Price Retrieval**:
   - We developed the open price date function, leveraging the yfinance library to retrieve the open stock price for a given ticker and date.
   - This function handles date formatting and gracefully handles cases where stock market data is unavailable.

4. **ROI Computation**:
   - The calc roi per year function computes the annual return on investment for each senator based on their stock transactions.
   - By iterating over transactions chronologically, it accurately calculates ROI for each year, providing valuable insights into investment performance.

5. **State Data Integration**:
   - We incorporated state data from a JSON file, extracting and adding state information as a new column in the pandas dataframe.
   - Utilizing functions like state data and state data all senators, we efficiently extract state information for all senators in the dataframe.

6. **Visualization with Plotly and NetworkX**:
   - Plotly library was used for visualizing state data and top senators and stocks.
   - NetworkX conversion function was employed to create nodes and edges, storing vertex data as node attributes and transaction counts as edge attributes.
   - Visualization functions represent senators with different colors based on transaction suspicion levels and adjust node size based on transaction count.


# How to Run/Use the Project
**Run the Main File**: Execute the main.py file to initiate the project. This file orchestrates the execution of all executable functions and displays the final visualization. Please note that the visualization may take some time to load, especially for complex graphs. Allow the program sufficient time to generate and display the visualizations. Once the visualization is displayed, zoom in to explore the finer details of the graph, including node colors and sizes, as well as edge attributes.
   
**Sample Pictures**:
Below are sample images showcasing the visualizations generated by the project. These images provide a glimpse of the insights and analyses offered by the tool.
1. ![Graph Visualization using Networkx](https://github.com/tvirat/SenateStockInsights/assets/155598251/fca690fe-90af-4c92-9ad0-9f292c21fd8c)
2. ![Weighted Edges](https://github.com/tvirat/SenateStockInsights/assets/155598251/0282c425-5e99-47ee-8876-fbe0125929b5)
3. ![Top 10 Senators with highest number of transactions](https://github.com/tvirat/SenateStockInsights/assets/155598251/4409f73e-d726-46fd-b5b9-d5cde7958fdc)
4. ![Top 10 most transacted stocks](https://github.com/tvirat/SenateStockInsights/assets/155598251/479c60ac-0b01-43f2-adaf-57069d3d49db)



     




# Challenges
1. **Cleaning the dataset:** 
   - *Approach:* Utilized pandas for efficient data storage and cleaning. Removed empty cells and approximated transaction amounts by averaging the provided ranges.
   
2. **Computing annual ROI algorithm:**
   - *Approach:* Developed an algorithm to calculate annual ROI based on stock price fluctuations post-transaction, overcoming the lack of precise stock quantity data.
   
3. **Extracting stock prices with yfinance:**
   - *Approach:* Faced difficulties obtaining stock prices for specific dates due to market closures. Mitigated by extracting open stock prices from nearby dates when necessary.
   
4. **Visualizing graphs with NetworkX:**
   - *Approach:* Encountered challenges in selecting appropriate argument values for graph visualization functions. Resolved by experimenting and settling on using 1/x as the node size argument for consistency.


# Future Prospects
Despite the challenges encountered during the development phase, we envision several enhancements and expansions to further enrich the capabilities of our project:

1. **Geographical Visualization of State Data:** Explore the possibility of visualizing state-level data on a geographical map of the USA, providing a more intuitive representation compared to traditional bar plots.

2. **International Comparison of ROI:** Extend the analysis beyond US senators by comparing their annual ROI with leaders from other democratic countries such as Canada and the UK, offering broader insights into legislative trading practices.

3. **Advanced ROI Computation Algorithm:** Implement a more sophisticated algorithm for ROI computation, incorporating factors such as net wealth and other pertinent variables to provide a more nuanced understanding of trading success.

4. **Integration of Policy Impact Analysis:** Incorporate analysis of major policy decisions that could potentially influence stock trading activities among senators, enabling a deeper examination of the nexus between legislative actions and financial transactions.

# Contributors
1. Harpuneet Singh (https://github.com/Harpuneet2005)
2. Tanayjyot Singh Chawla (https://github.com/TanayJyot)
3. Virat Talan (https://github.com/tvirat)
   
# References
- Holmes, A. (2023, February 6). Senator Stonk trades [Data file]. Kaggle. [https://www.kaggle.com/datasets/aholmes23/senatortrades?resource=download](https://www.kaggle.com/datasets/aholmes23/senator-trades?resource=download)

  This dataset, obtained from Kaggle, comprises CSV files containing U.S. senators' stock transactions spanning approximately from 2013 to 2023. It includes attributes such as senator name, transaction ID, transaction date, date filed, stock ticker, and range of amount spent.

- Members of the U.S. Congress. (2024, April 12). Senators State Dataset [Data file]. https://www.congress.gov/members

  This dataset, provided by the U.S. Congress website, is in JSON format and contains information on U.S. senators, including their names, states, and various other data points.













