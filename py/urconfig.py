
class urCfg:
    # one group
    title_regex = re.compile("^\s*\[([A-Za-z0-9_\-\.]*)\]\s*$")
    # two groups; trim the second
    kv_regex = re.compile("^\s*([A-Za-z0-9_\-]+)\s*=(.*)$")
    # no groups
    blank_regex = re.compile("^#?\s*$")

    def __init__():
        self.dict = {}

    def __extract_header(line):
        """If this line is a header, returns the title. Else, returns None
        """
        result = title_regex.fullmatch(line)
        if result:
            return result.group(1)
        return None

    def __extract_kv(line):
        """If this line is a key-value pair, returns a k/v tuple. Else, returns None
        """
        result = kv_regex.fullmatch(line)
        if result:
            return (result.group(1), result.group(2))
        return None

    def __extract_skip(line):
        """If this line should be skipped, returns the line. Else, returns None
        """
        if blank_regex.fullmatch(line):
            return line
        return None

    def __from_lines(self, lines, skip_error = false):
        """Creates an urCfgDict from an iterable of lines
        """

        # initialize the default section
        current_section = ""
        self.dict[current_section] = {}

        # start at line 0 with no errors
        line_number = -1
        errors = []

        # iterate over the lines
        for line in lines:
            line_number += 1

            # skip the line if it is blank or a comment
            result = __extract_kv(line)
            if (result != None):
                continue

            # check if the line is a header
            result = __extract_header(line)
            if result != None:
                # set the current section
                current_section = result
                # initialize the section if it does not exist yet
                if current_section not in self.dict:
                    self.dict[current_section] = {}
                continue

            # check if the result is a key=value pair, store it in the current section
            result = __extract_kv(line)
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
                raise ValueError("Unable to interpret line")

        return errors

    def print(self, file = None):
        """Serializes an urCfgDict to a given file, or a string if None is provided
        """
        pass

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
