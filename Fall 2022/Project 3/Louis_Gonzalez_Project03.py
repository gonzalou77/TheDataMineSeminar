"""This module is for project 3 for TDM 30100.

**Serialization:** Serialization is the process of taking a set or subset of data and transforming it into a specific file format that is designed for transmission over a network, storage, or some other specific use-case.
**Deserialization:** Deserialization is the opposite process from serialization where the serialized data is reverted back into its original form.

The following are some common serialization formats:

- JSON
- Bincode
- MessagePack
- YAML
- TOML
- Pickle
- BSON
- CBOR
- Parquet
- XML
- Protobuf

**JSON:** One of the more wide-spread serialization formats, JSON has the advantages that it is human readable, and has a excellent set of optimized tools written to serialize and deserialize. In addition, it has first-rate support in browsers. A disadvantage is that it is not a fantastic format storage-wise (it takes up lots of space), and parsing large JSON files can use a lot of memory.

**MessagePack:** MessagePack is a non-human-readable file format (binary) that is extremely fast to serialize and deserialize, and is extremely efficient space-wise. It has excellent tooling in many different languages. It is still not the *most* space efficient, or *fastest* to serialize/deserialize, and remains impossible to work with in its serialized form.

Generally, each format is either *human-readable* or *not*. Human readable formats are able to be read by a human when opened up in a text editor, for example. Non human-readable formats are typically in some binary format and will look like random nonsense when opened in a text editor.
"""


import lxml
import lxml.etree
from datetime import datetime, date


def get_records_for_date(tree: lxml.etree._ElementTree, for_date: date) -> list:
    """
    Given an `lxml.etree` object and a `datetime.date` object, return a list of records
    with the startDate equal to `for_date`.
    Args:
        tree (lxml.etree): The watch_dump.xml file as an `lxml.etree` object.
        for_date (datetime.date): The date for which returned records should have a startDate equal to.
    Raises:
        TypeError: If `tree` is not an `lxml.etree` object.
        TypeError: If `for_date` is not a `datetime.date` object.
    Returns:
        list: A list of records with the startDate equal to `for_date`.
    """

    if not isinstance(tree, lxml.etree._ElementTree):
        raise TypeError('tree must be an lxml.etree')

    if not isinstance(for_date, date):
        raise TypeError('for_date must be a datetime.date')

    results = []
    for record in tree.xpath('/HealthData/Record'):
        if for_date == datetime.strptime(record.attrib.get('startDate'), '%Y-%m-%d %X %z').date():
            results.append(record)

    return results