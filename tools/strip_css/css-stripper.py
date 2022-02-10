import os
import re

# Strips CSS To Color/themable lines only

input_file_name = 'input.css'
output_file_name = 'output.css'
selector_regex = re.compile('[^\n\{\}]*\{[^\{\}]*}')


class css_handler:
    def __init__(self, css_file: str) -> None:
        self.modified_css = css_file

    def check(self, check_string: str) -> bool:
        """ Check if check_string contains certain text

            Returns a bool based on if the text was found.

            Args:
                check_string: String | text to check against.
        """
        for element in ['color:', 'background:', 'border:']:
            if element in str(check_string):
                return True
        return False

    def replace(self, css_selector: str) -> str:
        """ Replaces css_selector with only wanted properties.

            Returns a String of the CSS Selector With Only Wanted Properties or Blank String If No Properties Were Found

            Args:
                css_selector: String | contains selector to check for valid properties from
        """
        css_props = re.findall(r'(?<=\{)[^\{\}]*', css_selector)[0]
        props_list = ''.join(
            [c for c in css_props if c not in ['\t', '\n']]).split(';')
        valid_props = []
        for css_prop in props_list:
            if self.check(css_prop):
                valid_props.append(css_prop)
        valid_props = ';'.join(valid_props)
        return '' if not valid_props else css_selector.replace(css_props, valid_props) + ';'

    def grab_selectors(self) -> list:
        """ Grab Selectors From The CSS File Contents Specificied When Creating The Class.

            Returns a List of all Css Selectors.
        """
        return selector_regex.findall(self.modified_css)


class file_handler:
    """ Handles all file-related activities

        Args:
            input_file_name: String | contains file name & extention to read from (Default: input.css)

            output_file_name: String | contains file name & extention to write to (Default: output.css)
    """

    def __init__(self, input_file_name: str = 'input.css', output_file_name: str = 'output.css') -> None:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_path = os.path.join(
            file_dir, input_file_name)
        self.output_path = os.path.join(
            file_dir, output_file_name)

    def read(self) -> str:
        """ Reads the input file.

            Returns a String with File contents, or an empty string if no input file was found.
        """
        if not os.path.exists(self.input_path):
            open(self.input_path, 'w')
            print('Input File Was Not Found and Was Created. Please Input Your CSS In The File. \n' + self.input_path)
            return ''
        with open(self.input_path, 'r', encoding='utf-8-sig') as css:
            file_contents = css.read()
        return file_contents

    def write(self, text: str) -> None:
        """ Writes text to the output file.

            Args:
                text: String | text to write to the output file (self.output_path).
        """
        open(self.output_path, 'w').write(text)


def main():
    file = file_handler(input_file_name, output_file_name)
    css_file = file.read()
    if not css_file:
        return
    css = css_handler(css_file)
    selectors = css.grab_selectors()
    for selector in selectors:
        replacement = css.replace(selector)
        css_file = css_file.replace(selector, replacement)
    file.write(css_file)


main()
