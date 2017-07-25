
class urCfg:
    def fromLines(lines):
        """Creates an urCfgDict from an iterable
        """
        pass

    def print(self, file = None):
        """Serializes an urCfgDict to a given file, or a string if None is provided
        """
        pass

    def getValue(self, section, key):
        """Gets a value from its section and key
        """
        pass

    def getValues(self, section):
        """Gets all keys and values as a dict from a section
        """
        pass

    def getSections(self):
        """Gets all sections as a list
        """
        pass
