import hashlib
import functools

## code by voidc2

def create_sha1_hash(input_string: str) -> str:
    """
    Create a SHA-1 hash for the given input string or list of strings.

    Parameters:
    input_string (str or list of str): The input string or list of strings to hash.

    Returns:
    str: The SHA-1 hash of the input.

    Usage:
    >>> create_sha1_hash("example")
    '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'

    >>> create_sha1_hash(["example1", "example2"])
    '20df7b38a1d0be85b20c99ef1b3c2903e8a992bb'
    """

    @functools.singledispatch
    def hash_string(input_string: str) -> str:
        """
        Create a SHA-1 hash for the given input string.

        Parameters:
        input_string (str): The input string to hash.

        Returns:
        str: The SHA-1 hash of the input string.
        """
        sha1_hash = hashlib.sha1()
        sha1_hash.update(input_string.encode('utf-8'))
        return sha1_hash.hexdigest()

    @hash_string.register
    def _(input_strings: list) -> str:
        """
        Create a SHA-1 hash for the given list of strings.

        Parameters:
        input_strings (list of str): The list of input strings to hash.

        Returns:
        str: The SHA-1 hash of the concatenated input strings.
        """
        sha1_hash = hashlib.sha1()
        for input_string in input_strings:
            sha1_hash.update(input_string.encode('utf-8'))
        return sha1_hash.hexdigest()

    return hash_string(input_string)