import os
import pandas as pd
from Data.filter_article import filter_article
from Data.generate_xml import generate_xml


def main():
    if not os.path.exists("./Data/deduped_data.csv"):
        os.system("./Data/dedup_data.bash ./Data/metadata.csv")

    article_df = pd.read_csv("./Data/deduped_data.csv")
    print(article_df)

    # filtered_article_df = filter_article(article_df)

    # generate_xml(filtered_article_df)


if __name__ == "__main__":
    main()

