class SerializerNotFoundError(RuntimeError):
    """
    Exception class to raise if no matching serialilizer is found.
    """

class ObjectNotFoundError(RuntimeError):
    """
    Exception class to raise if a requested object is not found.
    """
