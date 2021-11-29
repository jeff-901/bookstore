import pprint


class _ServerObject:
    def __iter__(self):
        # Iterate through list of properties and yield as key -> value
        for prop in self._properties():
            yield prop, self.__getattribute__(prop)

    @classmethod
    def _properties(cls):
        return sorted(
            [p for p in cls.__dict__ if isinstance(getattr(cls, p), property)]
        )

    @classmethod
    def from_dictionary(cls, the_dict):
        filtered_dict = {
            key: value for key, value in the_dict.items() if key in cls._properties()
        }
        return cls(**filtered_dict)

    def __repr__(self) -> str:
        return to_string(self)
