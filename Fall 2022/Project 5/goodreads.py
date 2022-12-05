import os
from pathlib import Path
import json
import shutil
from io import BytesIO
import uuid
import requests
import hashlib
import pytest


def split_json_to_n_parts(path_to_json: str, number_files: int, output_dir: str) -> None:
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
        >>> shutil.rmtree(output_dir)
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

        This is the second test
        >>> test_json = '/anvil/projects/tdm/data/goodreads/test.json'
        >>> output_dir = f'{os.getenv("SCRATCH")}/p5testoutput'
        >>> os.mkdir(output_dir)
        >>> number_files = 2
        >>> split_json_to_n_parts(test_json, number_files, output_dir)
        >>> output_dir = Path(output_dir)
        >>> number_output_files = sum(1 for _ in output_dir.glob("*.json"))
        >>> shutil.rmtree(output_dir)
        >>> number_output_files
        2
        
        This is the third test which I added
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
        >>> print(type(result)) # doctest: +NORMALIZE_WHITESPACE
        <class 'str'>
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
                    
                writer = open(str(Path(output_dir) / f'{path_to_json.stem}_{part_number}.json'), 'w')
                part_number += 1
                
            writer.write(line)
            
            
            
def get_book_with_isbn(path_to_json: str, isbn: str) -> dict:
    """
    Given a str representing the absolute path to a `.json` file, 
    `get_book_with_isbn` will return a `dict` containing the rest of
    the data on the book with the given isbn.
    
    Args:
        path_to_json: The absolute path to the `.json` file.
        isbn: The isbn of the book of interest.

    Returns:
        A `dict` containing the rest of the data, or `None` if no
        book with the given isbn was found.
        
    Examples:
    
        >>> get_book_with_isbn('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '0312853122').get('isbn')
        '0312853122'
        
        >>> get_book_with_isbn('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '0312853122').get('title')
        'W.C. Fields: A Life on Film'
        
        >>> get_book_with_isbn('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '0312853122').get('average_rating')
        '4.00'
        
        These tests are the ones I added
        
        >>> get_book_with_isbn('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '1408882280').get('kindle_asin')
        'B0192CTMWI'
        
        >>> get_book_with_isbn('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '1408882280').get('description')
        "New, repackaged audio editions of the classic and internationally bestselling, multi-award-winning series, read by Stephen Fry containing 17 CDs with a total running time of 20 hours and 45 minutes. With irresistible new jackets by Jonny Duddle to bring Harry Potter to the next generation of readers. When Dumbledore arrives at Privet Drive one summer night to collect Harry Potter, his wand hand is blackened and shrivelled, but he does not reveal why. Secrets and suspicion are spreading through the wizarding world, and Hogwarts itself is not safe. Harry is convinced that Malfoy bears the Dark Mark: there is a Death Eater amongst them. Harry will need powerful magic and true friends as he explores Voldemort's darkest secrets, and Dumbledore prepares him to face his destiny."
        
        >>> get_book_with_isbn('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '1408882280').get('title')
        'Harry Potter and the Half-Blood Prince (Harry Potter 6)'
        
   
    """
    path_to_json = Path(path_to_json)
    with open(path_to_json, 'r') as f:
        for line in f:
            d = json.loads(line)
            if isbn == d.get('isbn'):
                return d
        
        
def get_books_by_author_name(path_to_book_data: str, path_to_author_data: str, name: str, ) -> dict:
    """
    Given a str representing the absolute path to the `goodreads_books.json` file, the 
    absolute path to the `goodreads_book_authors.json` file, and a name,
    `get_books_by_author_name` will return a list of `dict` containing the works for the
    given author.
    
    Args:
        path_to_book_data: The absolute path to the `goodreads_books.json` file.
        path_to_author_data: The absolute path to the `goodreads_book_authors.json` file.
        name: The name of the author of interest.
        fuzzy: Whether or not we get a rough match to the author name (True) or an 
            exact match (False). Default false.

    Returns:
        A tuple of `dict` containing the works for the given author or matches for
            the given author name.
        
    Examples:
    
        >>> get_books_by_author_name('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '/anvil/projects/tdm/data/goodreads/goodreads_book_authors.json', 'Brandon Sanderson')[0].get('title')
        'Edgedancer (The Stormlight Archive #2.5)'
        
        >>> get_books_by_author_name('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '/anvil/projects/tdm/data/goodreads/goodreads_book_authors.json', 'Brandon Sanderson')[2].get('title')
        'The Way of Kings (The Stormlight Archive, #1)'
        
        
        These are the tests I entered
        
        >>> get_books_by_author_name('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '/anvil/projects/tdm/data/goodreads/goodreads_book_authors.json', 'J.K. Rowling')[0].get('title')
        "Harry Potter and the Sorcerer's Stone (Harry Potter, #1)"
        
        >>> get_books_by_author_name('/anvil/projects/tdm/data/goodreads/goodreads_books.json', '/anvil/projects/tdm/data/goodreads/goodreads_book_authors.json', 'J.K. Rowling')[1].get('title')
        'Harry Potter és a Félvér Herceg (Harry Potter, #6)'
    """
    path_to_book_data = Path(path_to_book_data)
    path_to_author_data = Path(path_to_author_data)
    
    author_ids = set()
    works = []
    
    # get the author id's for the given name
    with open(path_to_author_data, 'r') as f:
        for line in f:
            d = json.loads(line)
            if name == d.get('name'):
                author_ids.add(d.get('author_id'))
                with open(path_to_book_data, 'r') as g:
                    for line in g:
                        d = json.loads(line)
                        # get the authors of the work
                        for author in d.get('authors'):
                            if author.get('author_id') in author_ids:
                                works.append(d)
                                break
                                      
            else:
                continue
             
    return works


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
