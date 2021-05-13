class Base:
    """Base class for classes that want the main Session() object as an attribute."""

    @classmethod
    def initialise(cls, session):
        cls.session = session
