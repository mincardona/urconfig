import re, io

class UrCfg:
    # one groupl; must strip the capture
    title_regex = re.compile("^[\s]*\[([A-Za-z0-9_\-\.\s]*)\][\s]*$", re.DOTALL)
    # two groups; must strip the second
    kv_regex = re.compile("^[\s]*([A-Za-z0-9_\-]+)[\s]*=(.*)$", re.DOTALL)
    # no groups
    blank_regex = re.compile("^[\s]*$", re.DOTALL)
    # no groups
    comment_regex = re.compile("^#.*$", re.DOTALL)

    def __init__(self):
        self.dict = {}

    @staticmethod
    def __extract_header(line):
        """If this line is a header, returns the title. Else, returns None
        """
        result = UrCfg.title_regex.fullmatch(line)
        if result:
            return result.group(1).strip()
        return None

    @staticmethod
    def __extract_kv(line):
        """If this line is a key-value pair, returns a k/v tuple. Else, returns None
        """
        result = UrCfg.kv_regex.fullmatch(line)
        if result:
            return (result.group(1), result.group(2).strip())
        return None

    @staticmethod
    def __extract_skip(line):
        """If this line should be skipped, returns the line. Else, returns None
        """
        if UrCfg.blank_regex.fullmatch(line) or UrCfg.comment_regex.fullmatch(line):
            return line
        return None

    def __from_lines(self, lines, skip_error = False):
        """Creates an urCfgDict from an iterable of lines
        """

        # initialize the default section
        current_section = ""
        self.dict[current_section] = {}

        # start at line 1 with no errors
        line_number = 0
        errors = []

        # iterate over the lines
        for line in lines:
            line_number += 1

            # skip the line if it is blank or a comment
            result = UrCfg.__extract_skip(line)
            if result != None:
                continue

            # check if the line is a header
            result = UrCfg.__extract_header(line)
            if result != None:
                # set the current section
                current_section = result
                # initialize the section if it does not exist yet
                if current_section not in self.dict:
                    self.dict[current_section] = {}
                continue

            # check if the result is a key=value pair, store it in the current section
            result = UrCfg.__extract_kv(line)
            if result != None:
                self.dict[current_section][result[0]] = result[1]
                continue

            # at this point, we couldn't parse the line

            # record the error and skip the line...
            if skip_error:
                errors.append(line_number)
            # ...or throw an exception
            else:
                # by this point, we could not parse the line
                raise ValueError("Unable to interpret line %s" % line_number)

        return errors

    def from_file(self, filename):
        with open(filename) as f:
            self.__from_lines(f.readlines())

    def print(self, file = None):
        """Serializes an urCfgDict to a given file, or a string if None is provided
        """

        # if we are writing to a string, use a string stream
        if (file == None):
            f = io.StringIO()
        else:
            f = file

        # write all the titles and key-value pairs
        firstline = True
        for title, subdict in self.dict.items():
            # precede every section except the first with a lank line for readability
            if firstline:
                firstline = False
            else:
                f.write("\n")
            f.write("[" + title + "]\n")
            for key, value in subdict.items():
                f.write(key + "=" + value + "\n")

        # if we are writing to a string, return it
        if (file == None):
            return f.getvalue()
        else:
            return none

    def get_value(self, section, key):
        """Gets a value from its section and key
        """
        pass

    def get_values(self, section):
        """Gets all keys and values as a dict from a section
        """
        pass

    def get_sections(self):
        """Gets all sections as a list
        """
        pass

if __name__ == "__main__":
    ucfg = UrCfg()
    ucfg.from_file("test.ufg")
    print(ucfg.print())
