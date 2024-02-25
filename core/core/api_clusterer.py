from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
import pandas as pd
from .api_cluster_processing import api_cluster_processing


def api_clusterer(df):
    try:
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df["query"])

        num_clusters = int(len(df) / 30)

        kmeans = MiniBatchKMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)

        df["cluster_label"] = kmeans.labels_

        clusters = pd.DataFrame(
            {
                "query": df["query"],
                "clicks": df["clicks"],
                "position": df["position"],
                "impressions": df["impressions"],
                "page": df["page"],
                "cluster_label": df["cluster_label"],
            }
        )

        cluster_size = clusters.groupby("cluster_label")["query"].transform("count")
        clicks_sum_by_cluster = clusters.groupby("cluster_label")["clicks"].transform(
            "sum"
        )
        impressions_sum_by_cluster = clusters.groupby("cluster_label")[
            "impressions"
        ].transform("sum")
        clusters["cluster_size"] = cluster_size
        clusters["clicks_sum_by_cluster"] = clicks_sum_by_cluster
        clusters["impressions_sum_by_cluster"] = impressions_sum_by_cluster

        sorted_clusters = clusters.sort_values("page", ascending=True)

        # Визуализация кластеров
        # api_cluster_processing(sorted_clusters)

        sorted_clusters.to_excel("core/core/results/result.xlsx", index=False)

    except Exception as ex:
        print(ex)
