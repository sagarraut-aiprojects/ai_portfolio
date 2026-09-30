# RFM Customer Segmentation AI

An end-to-end customer analytics project that combines **RFM analysis, K-Means clustering, and an LLM-based business insight layer** to identify and interpret customer behavior.

The project separates deterministic analytics from AI interpretation:

* **Python / pandas** → data cleaning and RFM calculation
* **scikit-learn** → customer clustering
* **LLM** → business interpretation and strategic insights

---

## 1. Project Overview

Customer segmentation helps businesses understand differences in customer purchasing behavior and identify opportunities for retention, engagement, and customer development.

This project uses the **UCI Online Retail dataset** to:

1. Clean transaction-level retail data.
2. Calculate customer-level **Recency, Frequency, and Monetary (RFM)** metrics.
3. Convert RFM metrics into customer scores and business segments.
4. Apply **K-Means clustering** to identify behavioral groups independently of the rule-based RFM segments.
5. Compare the two segmentation approaches.
6. Use an LLM to generate business-oriented interpretations from the calculated results.

The objective is not to ask the LLM to perform the analytics itself. Instead, the analytical calculations are performed programmatically and the LLM is used as an **interpretation layer**.

---

## 2. Analytical Workflow

```text
Online Retail Transactions
            ↓
       Data Cleaning
            ↓
      RFM Calculation
            ↓
       RFM Scoring
            ↓
    Rule-Based Segments
            ↓
      K-Means Clustering
            ↓
 Segment & Cluster Analysis
            ↓
       LLM Interpretation
            ↓
      Business Insights
```

---

## 3. Dataset

The project uses the **UCI Online Retail dataset**, containing transaction-level records from a UK-based online retailer.

The original dataset contains:

* 541,909 transactions
* 8 variables
* Customer identifiers
* Invoice information
* Product information
* Quantity
* Unit price
* Transaction date
* Country

The raw dataset is preserved in:

```text
data/raw/Online Retail.xlsx
```

---

## 4. Data Cleaning

The raw transaction data was cleaned before calculating RFM metrics.

The cleaning process:

* Removed exact duplicate rows.
* Removed transactions without a `CustomerID`.
* Removed cancelled invoices.
* Removed transactions with negative quantities.
* Removed transactions with non-positive unit prices.
* Converted relevant identifier columns to consistent string types.

The cleaned dataset contains **392,692 transactions**, compared with 541,909 original records.

The cleaned data is saved as:

```text
data/processed/transactions_clean.parquet
```

The raw dataset is not modified.

---

## 5. RFM Analysis

RFM analysis evaluates customers using three behavioral measures.

### Recency

Measures how recently a customer made a purchase.

```text
Recency = Reference Date − Most Recent Purchase Date
```

Lower recency indicates more recent purchasing activity.

### Frequency

Measures how frequently a customer purchased.

In this project, frequency is measured as the **number of unique invoices** associated with a customer.

### Monetary

Measures the customer's total transaction value.

```text
Revenue = Quantity × UnitPrice
```

Monetary value is calculated by summing transaction revenue for each customer.

The resulting customer-level RFM dataset is saved as:

```text
data/processed/rfm_customer.parquet
```

---

## 6. RFM Scoring and Segmentation

Customers are assigned scores from 1 to 5 for each RFM dimension.

### Recency

Because lower recency is better:

```text
5 = Most recent
1 = Least recent
```

### Frequency and Monetary

Because higher values are generally stronger:

```text
1 = Lowest
5 = Highest
```

The three scores are combined into an overall RFM score.

Customers are then assigned to business-oriented segments based on their RFM scores.

The resulting dataset is saved as:

```text
data/processed/rfm_segmented.parquet
```

---

## 7. Segment Analysis

The rule-based segmentation produced four customer groups in the current analysis:

| Segment             | Customers | Customer Share | Revenue Share |
| ------------------- | --------: | -------------: | ------------: |
| Champions           |       933 |         21.51% |        70.23% |
| Potential Customers |     1,010 |         23.28% |        15.79% |
| At Risk             |     1,088 |         25.08% |         9.88% |
| Lost Customers      |     1,307 |         30.13% |         4.10% |

These figures illustrate an important characteristic of customer analytics: **customer count and revenue contribution can differ substantially across segments.**

The segment summary is saved as:

```text
data/processed/segment_summary.parquet
```

---

## 8. K-Means Customer Clustering

A second segmentation approach was implemented using **K-Means clustering**.

The clustering process uses:

* Recency
* Frequency
* Monetary value

Because RFM variables are highly skewed, the variables are first transformed using:

```python
np.log1p()
```

They are then standardized using:

```python
StandardScaler()
```

Several values of K were evaluated using:

* Inertia
* Silhouette Score

The elbow analysis supported using **K = 3** for the final clustering.

The silhouette score was also examined. It produced its highest value at K = 2, demonstrating that different cluster-selection criteria can provide different recommendations. K = 3 was selected for this project based primarily on the observed elbow structure and the resulting business interpretability.

---

## 9. K-Means Customer Profiles

The final K-Means solution contains three behavioral groups:

### Active Growth Customers

* Relatively recent purchasing activity
* Moderate purchase frequency
* Moderate monetary value
* 38.91% of customers
* 26.63% of revenue

### High-Value Loyal Customers

* Very recent purchasing activity
* High purchase frequency
* High monetary value
* 16.80% of customers
* 65.76% of revenue

### Inactive Low-Value Customers

* Long time since last purchase
* Low purchase frequency
* Low monetary value
* 44.28% of customers
* 7.61% of revenue

The clustered customer dataset is saved as:

```text
data/processed/rfm_clustered.parquet
```

---

## 10. Comparing RFM Segments and K-Means

The project compares the rule-based RFM segmentation with the unsupervised K-Means solution.

The comparison shows broad alignment between the two approaches.

For example:

* Lost Customers fall entirely into one K-Means cluster.
* Champions are concentrated primarily in the high-value loyal cluster.
* Potential Customers are concentrated primarily in the active growth cluster.
* At Risk customers are split across two K-Means clusters.

This demonstrates how machine-learning clustering can reveal additional behavioral variation within rule-based customer segments.

---

## 11. LLM Business Insights

An LLM is used after the analytical pipeline has completed.

The model receives the **pre-calculated segment statistics** rather than the raw transaction data.

The LLM is asked to:

* Describe customer segment characteristics.
* Identify important differences between segments.
* Suggest potential retention and engagement strategies.
* Identify areas requiring management attention based on the supplied metrics.
* Generate key business insights.

The current implementation uses the OpenAI Responses API.

The LLM does **not** calculate:

* Recency
* Frequency
* Monetary value
* RFM scores
* K-Means clusters

Those calculations remain deterministic and reproducible in Python.

This separation is intentional:

```text
Analytics → Python / Machine Learning
Interpretation → LLM
```

---

## 12. Visualizations

The project generates the following visualizations:

### Customers by RFM Segment

```text
outputs/figures/customers_by_segment.png
```

### Revenue by RFM Segment

```text
outputs/figures/revenue_by_segment.png
```

### K-Means Evaluation

```text
outputs/figures/kmeans_evaluation.png
```

### PCA Visualization of K-Means Clusters

```text
outputs/figures/kmeans_clusters_pca.png
```

---

## 13. Project Structure

```text
03_rfm_customer_segmentation_ai/
│
├── data/
│   ├── raw/
│   │   └── Online Retail.xlsx
│   │
│   └── processed/
│       ├── transactions_clean.parquet
│       ├── rfm_customer.parquet
│       ├── rfm_segmented.parquet
│       ├── segment_summary.parquet
│       └── rfm_clustered.parquet
│
├── outputs/
│   ├── figures/
│   │   ├── customers_by_segment.png
│   │   ├── revenue_by_segment.png
│   │   ├── kmeans_evaluation.png
│   │   └── kmeans_clusters_pca.png
│   │
│   └── reports/
│
├── src/
│   └── rfm/
│       ├── data_loader.py
│       ├── data_cleaning.py
│       ├── rfm_calculation.py
│       ├── rfm_scoring.py
│       ├── clustering.py
│       ├── segment_analysis.py
│       ├── visualization.py
│       ├── llm_insights.py
│       └── pipeline.py
│
├── notebooks/
├── test_loader.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

---

## 14. Technologies

* Python
* pandas
* NumPy
* scikit-learn
* Matplotlib
* Seaborn
* OpenPyXL
* PyArrow / Parquet
* OpenAI API
* python-dotenv
* uv

---

## 15. Running the Project

Create the environment and install the project dependencies using `uv`.

The project expects an OpenAI API key to be stored in a local `.env` file.

Example:

```text
OPENAI_API_KEY=your_api_key
```

The `.env` file is excluded from Git through `.gitignore`.

Run the current analysis/test script with:

```powershell
uv run python test_loader.py
```

---

## 16. Key Design Principle

The project follows a simple architectural principle:

> **Use deterministic tools for deterministic analysis and LLMs for interpretation.**

RFM calculations and clustering should be reproducible from the same input data.

The LLM provides an additional natural-language layer that converts analytical results into business-oriented explanations.

This architecture also makes it possible to experiment with different LLM providers and models without changing the underlying customer analytics pipeline.

---

## 17. Limitations

The analysis should be interpreted within the limitations of the dataset and methodology.

* RFM is based on historical purchasing behavior and does not directly measure customer profitability.
* Transaction revenue does not account for product costs, discounts, acquisition costs, or campaign costs.
* K-Means results depend on preprocessing choices and the selected number of clusters.
* The RFM segment definitions are rule-based and therefore depend on the chosen scoring methodology.
* LLM-generated recommendations are interpretations of the supplied statistics and should not be treated as causal conclusions.
* Additional customer, product, marketing, and profitability data would be required for more comprehensive customer-value analysis.

---

## 18. Project Status

**Status: Completed analytical prototype**

Implemented:

* [x] Transaction data loading
* [x] Data-quality assessment
* [x] Transaction cleaning
* [x] RFM calculation
* [x] RFM scoring
* [x] Rule-based customer segmentation
* [x] Segment analysis
* [x] K-Means clustering
* [x] Cluster evaluation
* [x] PCA cluster visualization
* [x] RFM vs. K-Means comparison
* [x] LLM-generated business insights

Future extensions can include alternative LLM providers, local models through Ollama, richer customer-level analysis, automated reporting, and interactive dashboards.
