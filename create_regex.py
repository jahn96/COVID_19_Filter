def remove_duplicate_term(terms):
  # remove star
  removed_star = re.sub(r'(\w)(\*)', r'\1', terms)

  # remove brackets and quote; convert OR(or) to |;
  cleaned_terms = re.sub(r'\s+or\s*', '|', re.sub(r'"', '', re.sub(r' ?\[.+?\]', 
                                        '', removed_star)), flags=re.IGNORECASE)
  first_part, second_part = re.split('[^\s]AND[^\s]', cleaned_terms)

  first_unique, second_unique = remove_duplicate_helper(first_part),\
                                          remove_duplicate_helper(second_part)

  search_terms = '|'.join(first_unique) + ")AND(" + '|'.join(second_unique)

  return search_terms


def remove_duplicate_helper(part):
  return pd.Series((re.split(r'\|', part, 
                                        flags=re.IGNORECASE))).drop_duplicates()


def get_regular_expression(search_terms):
  first_part, second_part = re.split('[^\s]AND[^\s]', search_terms)

  first_part_pattern = convert_and_to_regex(re.sub(r'(\w+)\s?AND\s?\(?(\w+)', 
                                              r'\1(?=.*(\2))', first_part + ')', 
                                               flags=re.IGNORECASE))

  second_part_pattern = convert_and_to_regex('(' + second_part)
  
  first_part_pattern = "^(?=.*" + first_part_pattern + ")"
  second_part_pattern = "(?=.*" + second_part_pattern + ").*$"
  
  return first_part_pattern + second_part_pattern


def convert_and_to_regex(terms):
  return re.sub(r'\s?AND\s?(\(?.+?\))', 
                                     r'(?=.*(\1))', terms, flags=re.IGNORECASE)
