from .api_export import extract_data
from .api_filter import (
    api_filter_by_position,
    api_filter_by_page,
    api_filter_by_minus_words,
)
from .api_clusterer import api_clusterer
from .api_cluster_processing import api_cluster_processing
from typing import List, Any


def get_extraction_result(
    site_domain: str,
    days: int,
    gt_position: int,
    url_filter: str = None,
    minus_words: List[str] = None,
) -> None:
    creds = "core/core/client_secret.json"
    df = extract_data(site_domain, creds, days)
    df = api_filter_by_position(df, gt_position)
    df = api_filter_by_page(df, url_filter)
    df = api_filter_by_minus_words(df, minus_words)
    clustered_df = api_clusterer(df)
