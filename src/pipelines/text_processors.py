
import re

import ftfy

import lxml
import lxml.html

import nltk

from dateutil.parser import parse as date_parser

# a regex that determins all the valid snetence terminations
terminator_list_re = r'(?:\!\?|\?\!|\.{3}|\!{3}|(?<![A-Z\d]{1})\.|\!|\?){1}'

STOP_CHARS = '!?.'


def _split_into_sentences(input):
    ''' splitting the input text in to sentences using NLTK library.
    It fails to recognize all the terminators except for dot.'''
    input = re.sub('\.+', '.', input)
    return [sent for sent in nltk.sent_tokenize(input)]


def _split_into_sentences_raw(input):
    ''' spliting text in to sentences using our coustom regex '''
    sentences = re.split(r'\W*(.*?%s)' % terminator_list_re, input)
    # in case last sentence has no terminator
    sentences[-1] = re.sub(r'^\W*', '', sentences[-1])
    return filter(None, sentences)


def remove_string(bad_sequence):
    """remove string that matches bad_sequence from input."""
    # '+' is an operator and needs to be escaped
    bad_sequence = bad_sequence.replace('+', '\+')

    def helper(input):
        return re.sub(bad_sequence, '', input)

    return helper


def _remove_space_before_terminator(input):
    """removing spaces before  end of sentences"""
    return re.sub(r'([ \r\t]*)(%s)' % terminator_list_re, r'\2', input)


def remove_empty_sentences(input):
    """Remove sentences that don't have any chars or have just spaces"""
    filtered = _split_into_sentences_raw(input)
    filtered = ' '.join(filtered)
    return _remove_space_before_terminator(filtered)


def strip_until_after(startswith):
    """Strips a string to string[len(startswith):] if the `startswith`
    is found """
    length = len(startswith)

    def helper(input):
        if input.startswith(startswith):
            return input[length:]
        else:
            return input

    return helper


def enforce_unicode(input):
    """Convert string to unicode."""
    if isinstance(input, str):
        return unicode(input, 'UTF-8', errors='ignore')
    else:
        return input


def fix_text(input):
    """Fix text encoding, line breaks, entities"""
    try:
        return ftfy.fix_text(input)
    except ValueError:
        return input


def string_to_date(input):
    """Convert string to date"""
    try:
        return date_parser(input)
    except Exception:
        return input


def replace_bad_chars(bad_chars):
    """Returns a function which replaces characters,
    bad_chars is a dictionary"""

    def helper(input):
        for key, value in bad_chars.items():
            input = input.replace(key, value)
        return input

    return helper


def capitalisation(input):
    """Capitalises every word in `input`"""
    return ' '.join(map(unicode.capitalize, input.split(' ')))


def append_fullstop(input):
    """Adds a fullstop at the end of `input`"""
    # if input and not input.endswith('.'):
    if input and input[-1] not in STOP_CHARS:
        return input + '.'
    else:
        return input


def strip_html(input):
    """Strips html tags out of a string."""
    return lxml.html.fromstring(input).text_content()


def strip_tags(input):
    """
    Returns the given HTML with all tags stripped.

    (from django.utils.html, can't import it here)

    """
    return re.sub(r'<[^>]*?>', '', input)


def normalise_internal_space(input):
    """Remove redundant spaces."""
    return ' '.join(input.split())


def capitalise_sentences(input):
    """Capitalises the letter after every `splitchar`"""
    input = normalise_internal_space(input.strip())
    sentences = _split_into_sentences_raw(input)
    sentences = [sentence[0].capitalize() + sentence[1:] for sentence in sentences]
    return ' '.join(sentences)
