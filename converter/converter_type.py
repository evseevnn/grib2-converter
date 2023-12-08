from abc import abstractmethod, ABC


class ConverterType(ABC):
    """Abstract class for all converter types."""

    @abstractmethod
    def convert(self, prev_value, value):
        """Converts value to the type."""
        pass

    def get_extension(self):
        """Returns extension of the file."""
        return self.__class__.__name__.lower()
