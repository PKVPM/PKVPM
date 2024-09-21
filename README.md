# PKVPM (多态键值路径映射) 🚀

自述文档语言: [English](./README-EN.md) | [简体中文](./README.md)

## 概览

多态键值路径映射（PKVPM-**Polymorphic Key-Value Path Mapping**）是一种灵活的数据结构，旨在通过利用YAML和JSON的原理，增强复杂嵌套配置的处理能力。它的目标是将严格的嵌套结构分解成易于管理的多行文本格式，同时保留原始数据类型和索引信息。PKVPM在需要复杂数据存储、检索和操作能力的应用中特别有用，为在层次框架内管理异构类型数据提供了创新解决方案。

## 关键特性

* **多态性**：支持同一结构内包含字符串、整数、浮点数、布尔值及其列表等多种数据类型。
* **基于路径的键**：使用点分隔的路径作为键，以实现对深层嵌套值的精确映射。
* **多行文本格式**：通过清晰的多行格式展示嵌套结构，增强了可读性和可维护性。
* **类型和索引保留**：保留数据的原始类型和索引，确保数据表示的完整性和准确性。

## 结构展示

```yaml
[str]: name: "John Doe"
[str]: gender: "Male"
[bool]: public: true
[int]: age: 30
[str]: favorite_books[0]: "The Great Gatsby"
[str]: favorite_books[1]: "To Kill a Mockingbird"
[str]: favorite_books[2]: "Brave New World"
```

## 应用场景

PKVPM格式在处理需要细粒度编辑和翻译的大型YAML或JSON文件时显示出其独特的优势。以下是一些具体的应用场景：

* **翻译长YAML/JSON文件**：当面对一个很长的YAML或JSON文件需要翻译时，直接操作原始文件可能会增加文件结构损坏的风险。例如，自动补全缺失的符号或修改缩进可能导致文件最终难以正确拼接。PKVPM格式通过将复杂的嵌套结构转换为易于管理的多行文本格式，简化了这一过程。
* **Minecraft服务器插件配置**：Minecraft服务器的插件配置文件往往非常长，且包含复杂的嵌套结构。一次性处理这些文件可能超出某些工具的处理能力。PKVPM格式允许开发者和服务器管理员将这些文件转换为更易于管理和编辑的格式，从而分批次进行翻译或修改，而不用担心破坏文件结构。
* **分批处理和编辑**：PKVPM格式的一个关键优势是能够轻松地对文件进行分批处理。用户可以简单地按行（`\n`）切割文件，选择固定长度的行数进行处理，然后再将这些行组装回PKVPM文件。这种方法特别适合需要将大型配置文件或数据文件分批翻译或编辑的场景。
* **保证文件结构完整性**：使用PKVPM格式，可以在不破坏原始文件结构的前提下，对文件进行重要的编辑和翻译工作。通过将PKVPM文件重新解释为JSON或YAML文件，可以确保最终输出文件的结构完整性和准确性。

通过这些应用场景，PKVPM格式展现了其在现代软件开发和数据处理中的实用性和灵活性，特别是在需要精确控制复杂数据结构编辑和翻译过程的情况下。

## 定义数据

使用PKVPM格式定义数据时，需要遵循一定的规则和结构，以确保数据的准确性和易用性。以下是详细的步骤和建议：

### 基本规则

1. **数据类型声明**：每条数据的开始（第一个冒号前）使用格式`[Type(类型)]`来声明需要声明数据的类型。支持的数据类型包括`str`（字符串）、`int`（整数）、`float`（浮点数）、`bool`（布尔值）和`list`（列表）。类型声明后跟一个冒号。
2. **键值对**：数据以键值对的形式表示，键和值之间使用冒号分隔（第二个冒号前）。键通常是一个字符串，表示数据的名称或标识符。
3. **路径表示法**：对于嵌套的数据结构，使用点（`.`）来分隔每一级，形成一个路径。这种表示法允许直接访问嵌套结构中的深层数据。

### 列表和复杂结构

* **列表表示**：当数据类型为`list`时，列表中的每个元素都需要指定类型。元素类型通过在值后面添加`|[Type(类型)]`来声明，各元素之间用逗号加空格`, `进行分隔。

### 实践示例

假设我们有一个包含个人信息和他们喜欢的书籍列表的数据结构：

> test.pkv

```yaml
[str]: name: "John Doe"
[str]: gender: "Male"
[bool]: public: true
[int]: age: 30
[str]: favorite_books[0]: "The Great Gatsby"
[str]: favorite_books[1]: "To Kill a Mockingbird"
[str]: favorite_books[2]: "Brave New World"
```

在这个例子中：

* `name`是一个字符串（`str`），值为`John Doe`。
* `gender`是一个字符串（`str`），值为`Male`。
* `public`是一个布尔值（`bool`），值为`true`。
* `age`是一个整数（`int`），值为`30`。
* `favorite_books`是一个列表（`list`），包含三本书，每本书的名称都是字符串类型。

0.安装PKVPM库：

`pip install pkvpm`

1.初始化

```python
import os
from pkvpm.parser import Parser

parser = Parser()

# 示例使用，读取测试需要的一共3个文件（test.yml, test.json, test.pkv）
# An example of using the test requires a total of 3 files (test.yml, test.json, test.pkv)
test_yml_path = os.path.join(os.path.dirname(__file__), 'test.yml')
test_json_path = os.path.join(os.path.dirname(__file__), 'test.json')
test_pkv_path = os.path.join(os.path.dirname(__file__), 'test.pkv')
```

2.将这个PKVPM文件转换成YAML：

```python
# 读取PKV文件/Read PKV file
with open(r"./test.pkv", 'r', encoding='utf-8') as file:
    test_pkvpm_content = file.read()
# 将PKVPM格式数据转换为YAML格式/Convert PKVPM format data to YAML format
pkvpm_to_yaml_content = parser.to_yaml(test_pkvpm_content, test_yml_path)
print(f"PKVPM to YAML:\n{pkvpm_to_yaml_content}")
```

> 输出

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

3.将YAML数据转换为PKVPM格式：

```python
# 读取YAML文件/Read YAML file
with open(r"./test.yml", 'r', encoding='utf-8') as file:
    test_yml_content = file.read()
# 将YAML数据转换为PKVPM格式
yaml_to_pkvpm_content = parser.parse(test_yml_content)
print(f"YAML to PKVPM:\n{yaml_to_pkvpm_content}")
```

> 输出

```yaml
[str]: name: "John Doe"
[str]: gender: "Male"
[bool]: public: true
[int]: age: 30
[str]: favorite_books[0]: "The Great Gatsby"
[str]: favorite_books[1]: "To Kill a Mockingbird"
[str]: favorite_books[2]: "Brave New World"
```

4. 将PKVPM格式数据转换为JSON格式

```python
pkvpm_to_json_content = parser.to_json(yaml_to_pkvpm_content, test_json_path)
print(f"PKVPM to JSON:\n{pkvpm_to_json_content}")
```

5.将JSON数据转换为PKVPM格式

```python
json_to_pkvpm_content = parser.parse(pkvpm_to_json_content)
print(f"JSON to PKVPM:\n{json_to_pkvpm_content}")
```

> 输出

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

### 访问及修改数据

* 直接使用`Parser.to_json(pkvpm_str)`方法将PKVPM文件转换成JSON对象实现增删改查操作，然后再转义成YAML或PKVPM文件。

## 结论

PKVPM为轻松高效地管理复杂的多态数据结构提供了强大的框架。通过采用基于路径的键系统并支持广泛的数据类型，PKVPM为面临复杂数据管理挑战的开发人员和数据架构师提供了灵活的解决方案。其设计灵感来源于YAML和JSON，优先考虑可读性、可维护性和精确处理嵌套配置，使其成为现代软件开发和数据处理中不可或缺的工具。
