import string
import unicodedata


def decompose_character(char):
    """ Attempt to return decomposed version of a character
    as list of normalised."""
    try:
        return [
            chr(int(u, 16))
            for u in unicodedata.decomposition(char).split(" ")
            if u and '<' not in u
        ]
    except:
        return None


class CharDict:
    """ Class to model mapping between characters and integers. """

    def __init__(self):
        """ Initialise and reverse control characters. """
        # Set character set we will use
        self.character_set = (
                string.ascii_lowercase +
                "! ,.?'"
        )
        # Populate rest of dictionary from character set
        self.reverse_dict = {
            i: c for i, c in enumerate(self.character_set, start=0)
        }
        cs_len = len(self.reverse_dict)
        # Reserve special characters
        self.reverse_dict[cs_len + 0] = "<OOD>"  # Out of dict
        self.reverse_dict[cs_len + 1] = "<CAPITAL>"  # Out of dict

        self.vocabulary_size = len(self.reverse_dict)

        self.forward_dict = {
            v: k for k, v in self.reverse_dict.items()
        }

        # Create character cleaning dictionary
        self.char_cleaner = dict()
        self.char_cleaner['”'] = "'"
        self.char_cleaner['“'] = "'"
        self.char_cleaner['\u2003'] = ' '
        self.char_cleaner['\ue89e'] = ' '
        self.char_cleaner['\u2062'] = ' '
        self.char_cleaner['\ue8a0'] = ' '
        self.char_cleaner['−'] = '-'
        self.char_cleaner['—'] = '-'
        self.char_cleaner['′'] = "'"
        self.char_cleaner['‘'] = "'"
        self.char_cleaner['’'] = "'"
        self.char_cleaner['×'] = '*'
        self.char_cleaner['⁄'] = '/'

    def int2char(self, integer):
        """ Convert an integer into a character using the object. """
        return self.reverse_dict[integer]

    def clean_char(self, character):
        if character in self.char_cleaner.keys():
            return self.char_cleaner[character]
        else:
            return character

    def text2int(self, text):
        """ Convert a block of text into an integer. """

        integer_list = list()
        for character in text:
            # Perform mapping for commonly occuring characters
            if character in self.char_cleaner.keys():
                character = self.char_cleaner[character]

            # If character is in mapping dictionary add int to list
            if character in self.forward_dict.keys():
                integer_list.append(self.forward_dict[character])
            elif character in string.ascii_uppercase:
                # If uppercase
                integer_list.append(self.forward_dict["<CAPITAL>"])
                integer_list.append(self.forward_dict[character.lower()])
            else:
                replacement_chars = decompose_character(character)
                if replacement_chars:
                    integer_list += self.text2int("".join(replacement_chars))
                else:
                    integer_list.append(self.forward_dict["<OOD>"])
        return integer_list

    def intlist2text(self, int_list):
        """ Convert a list of integers back into text. """
        text = str()
        capitalise = False
        for i in int_list:
            char = self.reverse_dict[i]
            if char == "<CAPITAL>":
                capitalise = True
            else:
                if capitalise:
                    char = char.upper()
                text += char
                capitalise = False
        return text

    # We need to add a method that returns a one-hot encoding
