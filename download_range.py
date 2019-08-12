import argparse
import os
from urllib.parse import urlparse

import requests


def integer_to_roman(number: int):
    value = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1,
    ]
    symbol = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I",
    ]
    roman_numeral = ''
    i = 0
    while number > 0:
        for _ in range(number // value[i]):
            roman_numeral += symbol[i]
            number -= value[i]
        i += 1
    return roman_numeral


if __name__ == "__main__":

    # parse the command line arguments
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--prefix",
                             required=True,
                             type=str,
                             help="URL path prefix before the range digits")
    args_parser.add_argument("--postfix",
                             required=True,
                             type=str,
                             help="URL path postfix after the range digits")
    args_parser.add_argument("--first",
                             required=True,
                             type=int,
                             help="first number in the range of digits")
    args_parser.add_argument("--last",
                             required=True,
                             type=int,
                             help="last number in the range of digits (inclusive)")
    args_parser.add_argument("--dest",
                             required=True,
                             type=str,
                             help="destination directory path")
    args = vars(args_parser.parse_args())

    # range check
    if args["first"] > args["last"]:
        raise ValueError("Invalid range arguments, first must be less than or equal to last")

    # find the width we should use for the digits portion, for left zero padding
    digits_width = len(str(args["last"]))

    # loop over the specified range
    for i in range(args["first"], args["last"] + 1):

        # compose the URL
        url = args["prefix"] + str(i).zfill(digits_width) + args["postfix"]

        # if we've included "<roman>" somewhere in the URL then also replace this with a Roman numeral
        url = url.replace("<roman>", integer_to_roman(i))

        # if a URL has dashes in it and these are at the start of
        # the postfix then we'll need to escape them at the command line,
        # and here we'll get rid of the extraneous backslashes
        url = url.replace("\\", "")

        response = requests.get(url)

        # get the file name from the URL
        file_name = os.path.basename(urlparse(url).path)

        # write the downloaded response content into the file
        with open(os.sep.join([args["dest"], file_name]), "wb") as file:
            file.write(response.content)
