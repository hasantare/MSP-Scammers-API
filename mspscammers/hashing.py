import hashlib
import functools

def create_sha256_hash(input_string: str) -> str:
    """
    Create a SHA-256 hash for the given input string or list of strings.

    Parameters:
    input_string (str or list of str): The input string or list of strings to hash.

    Returns:
    str: The SHA-256 hash of the input.

    Usage:
    >>> create_sha256_hash("example")
    'eccbc87e4b5ce2fe28308fd9f2a7baf36e752668'

    >>> create_sha256_hash(["example1", "example2"])
    'c0e889cb0b2788ebb77b92c8e0e86a2026c07454'
    """

    @functools.singledispatch
    def hash_string(input_string: str) -> str:
        """
        Create a SHA-256 hash for the given input string.

        Parameters:
        input_string (str): The input string to hash.

        Returns:
        str: The SHA-256 hash of the input string.
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode('utf-8'))
        return sha256_hash.hexdigest()

    @hash_string.register
    def _(input_strings: list) -> str:
        """
        Create a SHA-256 hash for the given list of strings.

        Parameters:
        input_strings (list of str): The list of input strings to hash.

        Returns:
        str: The SHA-256 hash of the concatenated input strings.
        """
        sha256_hash = hashlib.sha256()
        for input_string in input_strings:
            sha256_hash.update(input_string.encode('utf-8'))
        return sha256_hash.hexdigest()

    return hash_string(input_string)
