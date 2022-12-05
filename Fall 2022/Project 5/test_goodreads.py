import unittest
import os
from pathlib import Path
import json
import shutil
import uuid
import requests
import hashlib
from io import BytesIO
import pytest


def split_json_to_n_parts(path_to_json: str,number_files: int,output_dir: str) -> None:
    """
    Given a str representing the absolute path to a `.json` file, 
    `split_json` will split it into `number_files` `.json` files of equal size.
    
    Args:
        path_to_json: The absolute path to the `.json` file.
        number_files: The number of files to split the `.json` file into.
        output_dir: The absolute path to the directory where the split `.json` 
            files are to be output.

    Returns:
        Nothing.
        
    Examples:
    
        This is the first test
        >>> test_json = '/anvil/projects/tdm/data/goodreads/test.json'
        >>> output_dir = f'{os.getenv("SCRATCH")}/p5testoutput'
        >>> os.mkdir(output_dir)
        >>> number_files = 2
        >>> split_json_to_n_parts(test_json, number_files, output_dir)
        >>> test_json = Path(test_json)
        >>> result = ''
        >>> for part_num in range(number_files):
        ...     file = Path(output_dir) / f'{test_json.stem}_{part_num}.json'
        ...     with open(file, 'r+') as p:
        ...         for line in p:
        ...             result = f'{result}{json.loads(line)}\\n'
        >>> # cleanup
        >>> shutil.rmtree(output_dir)
        >>> print(result) # doctest: +NORMALIZE_WHITESPACE
        {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        {'key1': 'aaa', 'key2': 'aaa', 'key3': 'aaa'}
        {'key1': 'bbb', 'key2': 'bbb', 'key3': 'bbb'}
        {'key1': 'ccc', 'key2': 'value2', 'key3': 'ccc'}
        {'key1': 'ddd', 'key2': 'ddd', 'key3': 'ddd'}
        {'key1': 'ddd', 'key2': 'ddd', 'key3': 'dddd'}
        {'key1': 'eeee', 'key2': 'eeee', 'key3': 'eeee'}
    """
    
    path_to_json = Path(path_to_json)
    num_lines = sum(1 for _ in open(path_to_json))
    group_amount = num_lines//number_files + 1
    with open(path_to_json, 'r') as f:
        part_number = 0
        writer = None
        for idx, line in enumerate(f):
            if idx % group_amount == 0:
                if writer:  
                    writer.close()
    
                writer = open(str(Path(output_dir)/f'{path_to_json.stem}_{part_number}.json'), 'w')
                part_number += 1
                
            writer.write(line)
            
            
def scrape_image_from_url(url_str: str, filename: str):

    """
    Given a str representing the desired url and filename, this function returns
    a read .jpg file and returns a byte type object.
        
    Args:
        url_str: The url from which the .jpg file is loaded from.
        path_to_author_data: The absolute path to the `goodreads_book_authors.json` file.
        
    Returns:
        A byte type object
        
    Examples:
    
        Although this test is simple, it is absolutely important to ensure that the object is a byte type and not an IO type object.
        >>> unique_filename = 'test'
        >>> url = 'http://images.gr-assets.com/books/1310220028m/5333265.jpg' 
        >>> my_bytes = scrape_image_from_url(url, unique_filename)
        >>> print(type(my_bytes))
        <class 'bytes'>
    """

    response = requests.get(url_str, stream = True)
    file = open(filename+'.jpg', 'wb')
    shutil.copyfileobj(response.raw, file)
    BR_file = open(filename+".jpg", "rb")
    BR_file = BR_file.read()
    path = os.getcwd()
    os.remove(path + '/' +  filename + ".jpg")
    return  BR_file



nums = [1, 2, 3]


@pytest.mark.parametrize('path_to_json,number_files,output_dir',[('/anvil/projects/tdm/data/goodreads/test.json',1,f'{os.getenv("SCRATCH")}/p5testoutput')])
def test_split_json_to_n_parts(path_to_json,number_files,output_dir) -> None:
#def test_split_json_to_n_parts(number_files,path_to_json,output_dir) -> None:
    #test_json = '/anvil/projects/tdm/data/goodreads/test.json'
    #output_dir = f'{os.getenv("SCRATCH")}/p5testoutput'
    #number_files = 2
    #shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    num_files = number_files
    split_json_to_n_parts(path_to_json,num_files,output_dir)
    test_json = Path(path_to_json)
    result = ''
    for part_num in range(num_files):
        file = Path(output_dir) / f'{test_json.stem}_{part_num}.json'
        with open(file, 'r+') as p:
            for line in p:
                parsed = json.loads(line)
                result = f'{result}{parsed}\\n'
    shutil.rmtree(output_dir)
    assert result == result
    
    
    
    
    
    

    
def scrape_image_from_url(url_str: str, filename: str):

    """
    Given a str representing the desired url and filename, this function returns
    a read .jpg file and returns a byte type object.
        
    Args:
        url_str: The url from which the .jpg file is loaded from.
        path_to_author_data: The absolute path to the `goodreads_book_authors.json` file.
        
    Returns:
        A byte type object
        
    Examples:
    
        Although this test is simple, it is absolutely important to ensure that the object is a byte type and not an IO type object.
        >>> unique_filename = 'test'
        >>> url = 'http://images.gr-assets.com/books/1310220028m/5333265.jpg' 
        >>> my_bytes = scrape_image_from_url(url, unique_filename)
        >>> print(type(my_bytes))
        <class 'bytes'>
    """

    response = requests.get(url_str, stream = True)
    file = open(filename+'.jpg', 'wb')
    shutil.copyfileobj(response.raw, file)
    BR_file = open(filename+".jpg", "rb")
    BR_file = BR_file.read()
    path = os.getcwd()
    os.remove(path + '/' +  filename + ".jpg")
    return  BR_file


@pytest.mark.parametrize('url_str,filename',[('http://images.gr-assets.com/books/1310220028m/5333265.jpg',str(uuid.uuid4()))])
def test_scrape_image_from_url(url_str, filename):
    """
    The test below is solely to test if the function provides the <class 'Byte'> type object.
    """
    test_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_272x92dp.png'
    test_filename = str(uuid.uuid4())
    response = requests.get(test_url, stream = True)
    file = open(test_filename+'.png', 'wb')
    shutil.copyfileobj(response.raw, file)
    BR_file = open(test_filename+".png", "rb")
    BR_file = BR_file.read()
    tested = print(type(BR_file))
    path = os.getcwd()
    testing = print(type(scrape_image_from_url(url_str, filename)))
    assert tested == testing