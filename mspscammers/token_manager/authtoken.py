from mspscammers.hashing import create_sha1_hash

class AuthtokenManager(type):
    """
    A metaclass for managing authentication tokens.

    This metaclass dynamically adds the `create_auth_token` method to classes that use it.
    """

    def __new__(cls, name, bases, attrs):
        """
        Create a new class with the `create_auth_token` method added.

        Parameters:
        cls (type): The metaclass.
        name (str): The name of the class being created.
        bases (tuple): The base classes of the class being created.
        attrs (dict): The attributes of the class being created.

        Returns:
        type: The newly created class with the `create_auth_token` method added.
        """
        attrs['create_auth_token'] = cls.create_auth_token
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def create_auth_token(discord_user_id: str) -> str:
        """
        Create an authentication token for the given Discord user ID.

        This method generates a SHA-1 hash of the provided Discord user ID.

        Parameters:
        discord_user_id (str): The Discord user ID for which to create an auth token.

        Returns:
        str: The SHA-1 hash of the Discord user ID, serving as the authentication token.
        
        Usage:
        >>> AuthtokenManager.create_auth_token("1234567890")
        'e807f1fcf82d132f9bb018ca6738a19f0b0e6f89'
        """
        return create_sha1_hash(discord_user_id)