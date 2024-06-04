import unicodedata

def remove_accents(input_str):
    """
    Remove accents from a string.

    Args:
        input_str (str): The string to remove accents from.

    Returns:
        str: The string with accents removed.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()