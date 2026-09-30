from src.rfm.data_loader import load_transaction_data
from src.rfm.rfm_scoring import (
    calculate_rfm_scores,
    assign_rfm_segments,
)
from src.rfm.segment_analysis import (
    analyze_segments,
    analyze_clusters,
    compare_segments_and_clusters,
)

from src.rfm.visualization import (
    plot_segment_customers,
    plot_segment_revenue,
    plot_kmeans_evaluation,
    plot_clusters_pca,
)

from src.rfm.clustering import (
    prepare_rfm_for_clustering,
    evaluate_kmeans,
    perform_kmeans,
    name_clusters,
)
from src.rfm.llm_insights import generate_segment_insights






file_path = "data/processed/rfm_customer.parquet"

rfm = load_transaction_data(file_path)

scored_rfm = calculate_rfm_scores(rfm)
segmented_rfm = assign_rfm_segments(scored_rfm)


scaled_rfm, scaler = prepare_rfm_for_clustering(
    segmented_rfm
)

cluster_evaluation = evaluate_kmeans(
    scaled_rfm
)

cluster_labels, kmeans_model = perform_kmeans(
    scaled_rfm,
    n_clusters=3,
)

segmented_rfm["Cluster"] = cluster_labels

segmented_rfm = name_clusters(
    segmented_rfm
)

print("\nNAMED CLUSTERS")
print("--------------")

print(
    segmented_rfm[
        [
            "CustomerID",
            "Cluster",
            "ClusterName",
        ]
    ].head(10).to_string(index=False)
)

plot_clusters_pca(
    scaled_rfm,
    cluster_labels,
    output_path="outputs/figures/kmeans_clusters_pca.png",
)


comparison = compare_segments_and_clusters(
    segmented_rfm
)

print("\nRFM SEGMENTS vs K-MEANS CLUSTERS")
print("--------------------------------")

print(
    comparison.to_string()
)

clustered_path = "data/processed/rfm_clustered.parquet"

segmented_rfm[
    [
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary",
        "Cluster",
        "ClusterName",
    ]
].to_parquet(
    clustered_path,
    index=False,
)

print(
    f"\nSaved clustered RFM data to: {clustered_path}"
)

cluster_summary = analyze_clusters(
    segmented_rfm
)

print("\nCLUSTER ANALYSIS")
print("----------------")

print(
    cluster_summary.round(2).to_string(index=False)
)

print("\nCLUSTER DISTRIBUTION")
print("--------------------")

print(
    segmented_rfm["Cluster"]
    .value_counts()
    .sort_index()
)

plot_kmeans_evaluation(
    cluster_evaluation,
    "outputs/figures/kmeans_evaluation.png",
)

print("\nK-MEANS EVALUATION")
print("------------------")

print(
    cluster_evaluation.round(3).to_string(index=False)
)

print("\nCLUSTERING DATA")
print("----------------")

print(scaled_rfm.head())

print("\nMeans:")
print(scaled_rfm.mean().round(4))

print("\nStandard deviations:")
print(scaled_rfm.std().round(4))

segment_summary = analyze_segments(segmented_rfm)

plot_segment_customers(
    segment_summary,
    "outputs/figures/customers_by_segment.png"
)

plot_segment_revenue(
    segment_summary,
    "outputs/figures/revenue_by_segment.png"
)



summary_path = "data/processed/segment_summary.parquet"

segment_summary.to_parquet(
    summary_path,
    index=False
)

print(f"\nSaved segment summary to: {summary_path}")

print("\nSEGMENT ANALYSIS")
print("----------------")

print(
    segment_summary.round(2).to_string(index=False)
)

output_path = "data/processed/rfm_segmented.parquet"

segmented_rfm.to_parquet(
    output_path,
    index=False
)

print(f"\nSaved segmented RFM data to: {output_path}")

print("\nSEGMENT DISTRIBUTION")
print("--------------------")

print(
    segmented_rfm["Segment"]
    .value_counts()
    .sort_index()
)


print("\nSample segmented customers:")

print(
    segmented_rfm[
        [
            "CustomerID",
            "RFMScore",
            "Segment",
        ]
    ].head(10)
)


print("RFM SCORING")
print("-----------")

print(f"Customers: {len(scored_rfm):,}")

print("\nFirst 10 customers:")
print(
    scored_rfm[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "RecencyScore",
            "FrequencyScore",
            "MonetaryScore",
        ]
    ].head(10)
)

print("\nLLM BUSINESS INSIGHTS")
print("---------------------")

insights = generate_segment_insights(
    segment_summary
)

print(insights)