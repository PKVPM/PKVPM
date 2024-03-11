# PKVPM (Polymorphic Key-Value Path Mapping) 🚀

Self-documentation languages: [English](./README-EN.md) | [简体中文](./README.md)

## Overview

Polymorphic Key-Value Path Mapping (PKVPM) is a flexible data structure designed to enhance the handling of complex nested configurations by leveraging the principles of YAML and JSON. Its aim is to break down strict nested structures into easily manageable multi-line text formats while retaining the original data types and index information. PKVPM is particularly useful in applications requiring complex data storage, retrieval, and manipulation capabilities, providing an innovative solution for managing heterogeneous type data within hierarchical frameworks.

## Key Features

* **Polymorphism**: Supports multiple data types within the same structure, including strings, integers, floating-point numbers, boolean values, and their lists.
* **Path-based Keys**: Uses dot-separated paths as keys to achieve precise mapping of deeply nested values.
* **Multi-line Text Format**: Enhances readability and maintainability by presenting nested structures in a clear multi-line format.
* **Type and Index Preservation**: Preserves the original data types and indices, ensuring the integrity and accuracy of data representation.

## Structure Showcase

```yaml
[str]: key1: value1
[list]: key2: value2|[str], value3|[str], value4|[str]
[str]: key3: 123
[str]: key4: 123.456
[str]: key5: true
[list]: key6: 1|[int], 2|[int], 3|[int]
[list]: key7: 1.1|[float], 2.2|[float], 3.3|[float]
[list]: key8.sub_key1: True|[bool], False|[bool], True|[bool]
[list]: key9.sub_key2.sub_key3: 1|[int], 2.2|[float], True|[bool]
[str]: path1.path2.path3: value1
```

## Use Cases

The PKVPM format demonstrates its unique advantages in handling large YAML or JSON files requiring fine-grained editing and translation. Here are some specific use cases:

* **Translation of Long YAML/JSON Files**: When faced with a lengthy YAML or JSON file requiring translation, directly manipulating the original file may increase the risk of structural damage. For example, auto-completing missing symbols or modifying indentation may result in difficulties in correctly concatenating the file. The PKVPM format simplifies this process by converting complex nested structures into easily manageable multi-line text formats.
* **Minecraft Server Plugin Configuration**: Configuration files for Minecraft server plugins are often lengthy and contain complex nested structures. Processing these files in one go may exceed the capabilities of some tools. The PKVPM format allows developers and server administrators to convert these files into a more manageable and editable format, enabling batch translation or modification without concerns about disrupting the file structure.
* **Batch Processing and Editing**: A key advantage of the PKVPM format is its ability to easily process files in batches. Users can simply split the file by lines (`\n`), process a fixed number of lines, and then assemble these lines back into a PKVPM file. This method is particularly suitable for scenarios requiring batch translation or editing of large configuration files or data files.
* **Ensuring File Structure Integrity**: Using the PKVPM format, it's possible to perform significant edits and translations on files without compromising the original file structure. By reinterpreting PKVPM files as JSON or YAML files, the integrity and accuracy of the final output file structure can be ensured.

Through these use cases, the PKVPM format demonstrates its practicality and flexibility in modern software development and data processing, particularly in scenarios requiring precise control over the editing and translation processes of complex data structures.

## Defining Data

When defining data using the PKVPM format, certain rules and structures need to be followed to ensure accuracy and usability. Here are detailed steps and recommendations:

### Basic Rules

1. **Data Type Declaration**: Each data entry needs to declare the data type at the beginning (before the first colon). Supported data types include`str` (string),`int` (integer),`float` (floating-point number),`bool` (boolean value), and`list` (list). The type declaration is followed by a colon.
2. **Key-Value Pairs**: Data is represented in key-value pairs, where keys and values are separated by a colon (before the second colon). Keys are typically strings representing the name or identifier of the data.
3. **Path Representation**: For nested data structures, use dots (`.`) to separate each level, forming a path. This notation allows direct access to deep data within nested structures.

### Lists and Complex Structures

* **List Representation**: When the data type is`list`, each element in the list needs to specify its type. The type of each element is declared by adding`|[Type]` after the value, with elements separated by commas followed by a space`, `.

### Practical Example

Suppose we have a data structure containing personal information and a list of their favorite books:

> test.pkvpm

```yaml
[str]: name: John Doe
[str]: gender: Male
[bool]: public: True
[int]: age: 30
[list]: favorite_books: The Great Gatsby|[str], To Kill a Mockingbird|[str], Brave New World|[str]
```

In this example:

* `name` is a string (`str`) with the value`John Doe`.
* `gender` is a string (`str`) with the value`Male`.
* `public` is a boolean value (`bool`) with the value`true`.
* `age` is an integer (`int`) with the value`30`.
* `favorite_books` is a list (`list`) containing three books, each with a string type.

0. Install the PKVPM library:

`pip install pkvpm`

1. Initialization

```python
import os
from pkvpm.parser import Parser

parser = Parser()

# Example usage, reading the required 3 files for testing (test.yml, test.json, test.pkv)
test_yml_path = os.path.join(os.path.dirname(__file__), 'test.yml')
test_json_path = os.path.join(os.path.dirname(__file__), 'test.json')
test_pkv_path = os.path.join(os.path.dirname(__file__), 'test.pkvpm')
```

2. Convert this PKVPM file to YAML:

```python
# Read PKV file
with open(r"./test.pkv", 'r', encoding='utf-8') as file:
    test_pkvpm_content = file.read()
# Convert PKVPM format data to YAML format
pkvpm_to_yaml_content = parser.to_yaml(test_pkvpm_content, test_yml_path)
print(f"PKVPM to YAML:\n{pkvpm_to_yaml_content}")
```

> Output

```yaml
name: John Doe
gender: Male
public: true
age: 30
favorite_books:
- The Great Gatsby
- To Kill a Mockingbird
- Brave New World
```

3. Convert YAML data to PKVPM format:

```python
# Read YAML file
with open(r"./test.yml", 'r', encoding='utf-8') as file:
    test_yml_content = file.read()
# Convert YAML data to PKVPM format
yaml_to_pkvpm_content = parser.parse(test_yml_content)
print(f"YAML to PKVPM:\n{yaml_to_pkvpm_content}")
```

> Output

```yaml
[str]: name: John Doe
[str]: gender: Male
[bool]: public: True
[int]: age: 30
[list]: favorite_books: The Great Gatsby|[str], To Kill a Mockingbird|[str], Brave New World|[str]
```

4. Convert PKVPM format data to JSON format

```python
pkvpm_to_json_content = parser.to_json(yaml_to_pkvpm_content, test_json_path)
print(f"PKVPM to JSON:\n{pkvpm_to_json_content}")
```

5. Convert JSON data to PKVPM format

```python
json_to_pkvpm_content = parser.parse(pkvpm_to_json_content)
print(f"JSON to PKVPM:\n{json_to_pkvpm_content}")
```

> Output

```json
{
    "name": "John Doe",
    "gender": "Male",
    "public": true,
    "age": 30,
    "favorite_books": [
        "The Great Gatsby",
        "To Kill a Mockingbird",
        "Brave New World"
    ]
}
```

### Accessing and Modifying Data

* Use the`Parser.to_json(pkvpm_str)` method to convert PKVPM files into JSON objects for CRUD operations, then escape them back into YAML or PKVPM files.

## Conclusion

PKVPM provides a powerful framework for easily and efficiently managing complex polymorphic data structures. By adopting a path-based key system and supporting a wide range of data types, PKVPM offers a flexible solution for developers and data architects facing challenges in managing complex data. Inspired by YAML and JSON, prioritizing readability, maintainability, and precise handling of nested configurations, PKVPM becomes an indispensable tool in modern software development and data processing.
