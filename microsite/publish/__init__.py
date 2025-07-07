import logging

from abc import ABC, abstractclassmethod
from microsite.util import AttrDict, Engine

log = logging.getLogger(__name__)


class PublishEngine(ABC, Engine):
    """
    Abstract class representing common features of a publishing engine.

    :param name: The name of the engine.
    :type name: str

    :param config: A dict containing operating parameters for this engine.
    :type config: dict
    """

    def __init__(self, name: str, config: AttrDict):
        self.name = name
        self.config

    @abstractclassmethod
    def publish(self, source_dir: str, target: str):
        """
        Absract function representing a PublishEngine's publication process.

        :param source_dir: Directory containing the content to publish. This may be the
            ``target_dir`` of a rendering engine.
        :type source_dir: str

        :param target: Value describing the target. This may vary between publish engines.
        :type target: str
        """

        pass


def publish(
    engines: list[PublishEngine],
    source_dir: str,
    target: str,
):
    for engine in engines:
        engine.publish(source_dir=source_dir, target=target)
