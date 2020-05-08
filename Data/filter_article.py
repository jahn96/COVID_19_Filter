import pandas as pd
import re


def filter_article(article_df: pd.DataFrame) -> pd.DataFrame:
    fr = open("./coviddrugs_searchterms1.txt")
    key_words = fr.read()
    fr.close()
    cleaned_key_words = clean_key_words(key_words)


def clean_key_words(key_words: str) -> str:
    removed_brackets = re.sub(r"\[[\w\s]+\]", " ", key_words)
    removed_or = re.sub(r"\s(OR|or)\s", " ", removed_brackets)
    removed_and = re.sub(r"\s(AND|and)\s", " ", removed_or)
    removed_newline = re.sub(r"\n", " ", removed_and)
    removed_star = re.sub(r"\*", " ", removed_newline)
    between_quotes = re.findall(r"\"[\w\s,\d\(\)-]+\"", removed_star)
    takeout_quotes = re.sub(r"\"[\w\s,\d\(\)-]+\"", " ", removed_star)
    between_paren = re.findall(r"\([\w\s-]+\)", takeout_quotes)
    between_quotes.extend(between_paren)  # extending
    takeout_paren = re.sub(r"\([\w\s-]+\)", " ", takeout_quotes)
    removed_extra_paren = re.sub(r"[\(\)]", " ", takeout_paren)
    between_quotes.extend(removed_extra_paren.split())
