import seaborn as sns


def api_cluster_processing(df):
    sns_plot = sns.pairplot(df, hue="query", height=2.5)
    sns_plot._legend.remove()
    sns_plot.savefig("src/dataset.png")
