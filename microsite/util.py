import logging

log = logging.getLogger(__name__)


class AttrDict(dict):
    """
    A dict that also acts like a namespace, allowing access to its values using dot notation as
    though they were any other Python object attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            if type(arg) is dict:
                for key, value in arg.items():
                    self.__setitem__(key, value)

    def __getattr__(self, attr):
        attr = self.get(attr)
        if type(attr) is dict:
            return AttrDict(attr)
        return attr

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if type(value) is dict:
            self.__dict__.update({key: AttrDict(value)})
        else:
            self.__dict__.update({key: value})

    def __delattr__(self, key):
        self.__delitem__(key)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]


class Engine:
    """
    All of the tools here fall into different run modes, such as "render" and "publish". Each of
    these implements different kinds of "engines" to power those tools. This is the base class for
    those engines' base classes, containing a name and an arbitrary config dict.

    :param name: The name of the engine.
    :type name: str

    :param config: A dict containing operating parameters for this engine.
    :type config: dict

    """
    def __init__(self, name: str, config: AttrDict):
        self.name = name
        self.config = config