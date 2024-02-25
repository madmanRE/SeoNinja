def api_filter_by_position(df, position):
    res = df.loc[
        (df["position"] > position),
        [
            "query",
            "clicks",
            "impressions",
            "position",
            "page",
        ],
    ]
    unique_res = res.drop_duplicates(subset="query")
    return unique_res


def api_filter_by_page(df, url):
    if url:
        res = df.loc[df["page"].apply(lambda page: url in page)]
        return res
    return df


def api_filter_by_minus_words(df, minus_words):
    if len(minus_words) > 0 and minus_words[0] != "":
        res = df.loc[
            ~df["query"].apply(
                lambda query: any(word.lower() in query.lower() for word in minus_words)
            )
        ]
        return res
    return df
