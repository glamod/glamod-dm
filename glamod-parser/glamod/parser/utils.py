'''
Created on 28/09/2018

@author: Ag Stephens
'''

import time
import os
import zipfile
import logging
import math
import numbers

from pandas import notnull

from glamod.parser.exceptions import ParserError
from glamod.parser.settings import INPUT_ENCODING


logger = logging.getLogger(__name__)


def timeit(method):
    "Decorator to wrap functions and time them."
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        method_name = method.__qualname__
        logger.info('TIMED FUNCTION: "{}" ran in: {:.5f} seconds'.format(method_name, (te - ts)))
        return result
    return timed


def is_null(value):
    
    # Check if None
    if value is None: return True
    
    if isinstance(value, numbers.Number):
        # Check if NaN value
        if math.isnan(value): return True
    
    # Check if empty string
    if isinstance(value, str) and not value: return True
    
    return False


def robust_notnull(value):
    
    if hasattr(value, 'any'):
        return notnull(value.any())
    else:
        return notnull(value)


def to_dict_dropna(data_frame):
    
    data = data_frame.to_dict(orient='rows')
    stripped_data = []
    for row in data:
        row_dict = {}
        for key, value in row.items():
            if not isinstance(value, list) and notnull(value):
                row_dict[key] = value
        stripped_data.append(row_dict)
    
    return stripped_data


def unzip(location, target_dir):
    logger.info('Found zip file: {}'.format(location))
    target_dir = os.path.abspath(target_dir)

    safe_mkdir(target_dir)

    with zipfile.ZipFile(location, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    expected_subdir = os.path.basename(location)[:-4]
    contents = os.listdir(target_dir)

    if contents != [expected_subdir]:
        raise ParserError('[ERROR] Zip file must unzip to directory with identical name '
                          'with ".zip" extension removed. Not: \n{}'.format(str(contents))) 

    logger.info('Unzipped contents to: {}'.format(target_dir))
    return os.path.join(target_dir, expected_subdir)


def report_errors(errs, msg_tmpl):
    err_string = '\n' + ', \n'.join(errs)
    raise ParserError(msg_tmpl.format(err_string))


def count_lines(fpath):
    count = 0

    with open(fpath, 'r', encoding=INPUT_ENCODING) as reader:
        for _ in reader:
            count += 1

    logger.info('File length of "{}" is: {}'.format(fpath, count))
    return count


def map_file_type(lookup, reverse=False):
    """
    Generic mapper for file name to/from table name.

    :param lookup: key to look up (file name or table name).
    :param reverse: direction to do lookup.
    :return: value (looked up in dictionary).
    """
    # Just use the file name (if relevant)
    lookup = os.path.basename(lookup)

    # If lookup key is a class then use its name here
    if not isinstance(lookup, str):
        lookup = lookup.__class__.__name__

    _map = {
        'source_configuration': 'SourceConfiguration',
        'station_configuration_optional': 'StationConfigurationOptional',
        'station_configuration': 'StationConfiguration',
        'header_table': 'HeaderTable', 
        'observations_table': 'ObservationsTable'}

    if reverse:
        dct = dict([(_value, _key) for _key, _value in _map.items()])
    else:
        dct = _map

    for _key in dct:
        if lookup.startswith(_key):
            return dct[_key]

    raise KeyError('Cannot lookup mapping for: {}'.format(lookup))


def get_path_sub_dirs(path, depth=1):
    """
    Returns a sub-directory tree under a path to the depth specified.
    """
    dir_path = os.path.abspath(os.path.dirname(path))
    items = dir_path.strip('/').split('/')

    return '/'.join(items[-(depth):])


def safe_mkdir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)
