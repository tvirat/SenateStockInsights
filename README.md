# SenateStockInsights

The objective of our project is to scrutinize U.S. senators' stock transactions, aiming to uncover suspicious patterns indicative of insider trading or ethical breaches. By examining mandatory stock disclosure filings from 2012 onwards, mandated by the STOCK Act, we seek to promote transparency and accountability in government institutions, crucial for upholding democratic principles.

# Motivation

In recent years, the financial activities of members of the United States Congress have come under intense scrutiny, with allegations of potential insider trading and conflicts of interest. This scrutiny arises from concerns that elected officials may possess privileged information, giving them an unfair advantage in the stock market.

The passage of the STOCK Act in 2012 aimed to address these concerns by prohibiting the use of non-public information for personal gain and mandating the disclosure of stock transactions by government officials. Despite these regulatory efforts, questions persist about the effectiveness of enforcement and the prevalence of unethical trading practices.

Our motivation stems from the need to shed light on the impact of legislative actions on financial markets and public trust. By analyzing the Return on Investment (ROI) of senators over the past decade, we aim to assess the influence of the STOCK Act and provide insights into the ethical conduct of elected representatives.

Through our project, we seek to contribute to the ongoing discourse on financial ethics and accountability in government institutions, ultimately fostering transparency and restoring public confidence in the democratic process.

# Features

- Calcuate the annual Return on Investment of each senator for every stock transcation
- Categorize senators into three categories (high, medium, low) based on their annual ROI 
- Visualize the graph representing all senators along with their stock transactions and their ROI category
- Calculate and visualize the US states with highest and lowest senator ROIs
- Calculate and visualize the most and least popular stocks transacted over the last decade


# Technical Details
- Used Python libraries like networkx, matplotlib, plotly to visualize the graph
- Used yfinance library to access the open stock price for each stock at the transaction date
- Used pandas to store the database containing the Senator transactions
- Used libraries like json and csv to read json and csv files

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

1. **Geographical Visualization of State Data:**
   - Explore the possibility of visualizing state-level data on a geographical map of the USA, providing a more intuitive representation compared to traditional bar plots.

2. **International Comparison of ROI:**
   - Extend the analysis beyond US senators by comparing their annual ROI with leaders from other democratic countries such as Canada and the UK, offering broader insights into legislative trading practices.

3. **Advanced ROI Computation Algorithm:**
   - Implement a more sophisticated algorithm for ROI computation, incorporating factors such as net wealth and other pertinent variables to provide a more nuanced understanding of trading success.

4. **Integration of Policy Impact Analysis:**
   - Incorporate analysis of major policy decisions that could potentially influence stock trading activities among senators, enabling a deeper examination of the nexus between legislative actions and financial transactions.

   
# References/Credits
- Senator Stock dataset: Holmes, A. (2023, February 6). Senator Stonk trades. Kaggle. https://www.kaggle.com/datasets/aholmes23/senatortrades?resource=download
- Senator State dataset: 













