#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:PKVPM Parser library for converting between YAML, JSON, and PKVPM formats.
@Date: 2024/03/10
@version: 1.0.0
@License: MIT License
@Github: https://github.com/PKVPM/PKVPM

@Contributors:
https://github.com/Evil0ctal
https://github.com/Johnserf-Seed
"""

import json
import yaml

from typing import Dict, Union


class Parser:

    def __init__(self):
        # 初始化数据/Initialize data
        self.data = {}
        # 类型转换器/Type converter
        self.type_converters = {
            "list": self.translate_list,
            "bool": lambda x: x.lower() == "true",
            "int": int,
            "float": float,
            "str": str,
        }

    def linear_format_generator(self, kv_data, prefix=""):
        """
        将键值数据转换为线性格式的键值对列表/Convert key-value data to a linear format list of key-value pairs
        :param kv_data: 键值对数据/Key-value pair data
        :param prefix: 键的前缀/Prefix of the key
        :return: 线性格式的键值对列表/Linear format list of key-value pairs
        """
        if isinstance(kv_data, dict):
            for key, value in kv_data.items():
                if isinstance(value, list):
                    # 如果值是列表，则将其转换为逗号分隔的字符串，并记录每个值的类型
                    # If the value is a list, convert it to a comma-separated string and record the type of each value
                    value_with_types = ", ".join(
                        f"{item}|[{type(item).__name__}]" for item in value
                    )
                    yield f"{prefix}.{key}" if prefix else key, value_with_types, list
                else:
                    yield from self.linear_format_generator(
                        value, prefix=f"{prefix}.{key}" if prefix else key
                    )
        elif isinstance(kv_data, list):
            for index, value in enumerate(kv_data):
                yield from self.linear_format_generator(
                    value, prefix=f"{prefix}[{index}]"
                )
        else:
            yield prefix, kv_data, type(kv_data).__name__

    def parse(self, content: Union[str, Dict]) -> str:
        """
        将输入数据转换为多态键值路径映射格式/Convert input data to polymorphic key-value path mapping format
        :param content: 输入数据(字符串或字典)/Input data (string or dictionary)
        :return: 多态键值路径映射格式(PKVPM)数据字符串/Polytypic key-value path mapping (PKVPM) data string
        """

        # 如果是字符串就假设输入为YAML文本并转换为字典对象，如果是字典就直接使用无需转换。
        # If it is a string, it is assumed that the input is YAML text and converted to a dictionary object, and if it is a dictionary, it is used directly without conversion.
        content = yaml.safe_load(content) if isinstance(content, str) else content

        # 转换为线性格式/Convert to linear format
        linear_format = list(self.linear_format_generator(content))

        # 保存线性格式数据/Save linear format data
        line_list = []
        for path, value, value_type in linear_format:
            # 如果值的类型是列表，不进行转换，直接保存
            # If the value type is a list, do not convert, save directly
            if value_type == list:
                line = f"[{value_type.__name__}]: {path}: {value}"
            else:
                line = f"[{value_type}]: {path}: {value}"
            line_list.append(line)

        result = "\n".join(line_list)

        # 返回线性格式数据/Return linear format data
        return result

    def translate_list(self, value):
        """
        将列表字符串转换为列表，并保留每个元素的类型/Convert list string to list and retain the type of each element
        :param value: 列表字符串/List string
        例如/Example：1|[int], 2.2|[float], true|[bool]
        """
        items = [
            item.split("|[") for item in value.split(", ") if item.strip()
        ]  # 跳过空字符串的元素
        result = []
        for item in items:
            if isinstance(item, list) and len(item) == 2:
                item_value, item_type = item
                if item_type == "int]":
                    result.append(int(item_value))
                elif item_type == "float]":
                    result.append(float(item_value))
                elif item_type == "bool]":
                    result.append(item_value.lower() == "true")
                else:
                    result.append(item_value)
            else:
                result.append(item)  # 不是列表类型或者不带类型信息的项目，直接添加值
        return result

    def add_translation(self, path, value, value_type, data=None):
        """添加翻译
        :param path: 路径
        :param value: 值
        :param value_type: 值类型
        :param data: 数据字典
        """
        keys = path.split(".")
        current_dict = self.data if data is None else data
        for key in keys[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]

        # 使用类型转换器转换值
        converter = self.type_converters.get(value_type, lambda x: x)
        current_dict[keys[-1]] = converter(value)

    def process_translation_line(self, line):
        """处理翻译行
        :param line: 翻译行
        :return: 路径、值、值类型
        """
        line = line.strip()
        parts = line.split(": ")  # 保留空格
        value_type = parts[0][1:-1]
        path = parts[1].rstrip(
            ":"
        )  # 去除末尾的冒号 因为parts保留空格导致获取的路径包含:
        value = ": ".join(parts[2:])

        return (
            path,
            value,
            value_type,
        )

    def to_json(self, pkvpm_str, file_path=None):
        """
        将数据转换为 JSON 格式
        """
        yaml_data = self.to_yaml(pkvpm_str, file_path=file_path)
        json_data = json.dumps(yaml.safe_load(yaml_data), ensure_ascii=False, indent=4)

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(json_data)

        return json_data

    def to_yaml(self, data=None, file_path=None):
        """
        将数据转换为 YAML 格式
        :param data: PKVPM格式数据，如果为None则使用初始化的数据
        :param file_path: 输出的YAML文件路径
        :return: YAML格式数据
        """
        if data:
            # 创建一个新的空字典来存储解析后的数据
            new_data = {}
            for line in data.split('\n'):
                if line:
                    path, value, value_type = self.process_translation_line(line)
                    self.add_translation(path, value, value_type, new_data)
            data = new_data
        else:
            data = self.data

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                yaml.dump(data, file, sort_keys=False, indent=4, allow_unicode=True)

        return yaml.dump(data, sort_keys=False, indent=4, allow_unicode=True)


if __name__ == "__main__":

    # 一个pkvpm文件的例子:
    # [str]: key1: value1
    # [list]: key2: value2 | [str], value3 | [str], value4 | [str]
    # [int]: key3: 123
    # [float]: key4: 123.456
    # [bool]: key5: true
    # [list]: key6: 1 | [int], 2 | [int], 3 | [int]
    # [list]: key7: 1.1 | [float], 2.2 | [float], 3.3 | [float]
    # [list]: key8: true | [bool], false | [bool], true | [bool]
    # [list]: key9: 1 | [int], 2.2 | [float], true | [bool]
    # [str]: path1.path2.path3: value1

    import os

    parser = Parser()

    # 示例使用，读取测试需要的一共3个文件（test.yml, test.json, test.pkv）
    test_yml_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.yml')
    test_json_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.json')
    test_pkv_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.pkv')

    # 读取YAML文件/Read YAML file
    with open(test_yml_path, 'r', encoding='utf-8') as file:
        test_yml_content = file.read()

    # 读取JSON文件/Read JSON file
    with open(test_json_path, 'r', encoding='utf-8') as file:
        test_json_content = file.read()

    # 读取PKV文件/Read PKV file
    with open(test_pkv_path, 'r', encoding='utf-8') as file:
        test_pkvpm_content = file.read()

    # 将YAML数据转换为PKVPM格式
    yaml_to_pkvpm_content = parser.parse(test_yml_content)
    print(f"YAML to PKVPM:\n{yaml_to_pkvpm_content}")

    # 保存PKVPM格式数据/Save PKVPM format data
    with open(test_pkv_path, 'w', encoding='utf-8') as file:
        file.write(yaml_to_pkvpm_content)

    # 将PKVPM格式数据转换为YAML格式/Convert PKVPM format data to YAML format
    pkvpm_to_yaml_content = parser.to_yaml(yaml_to_pkvpm_content, test_yml_path)
    print(f"PKVPM to YAML:\n{pkvpm_to_yaml_content}")

    # 将PKVPM格式数据转换为JSON格式
    pkvpm_to_json_content = parser.to_json(yaml_to_pkvpm_content, test_json_path)
    print(f"PKVPM to JSON:\n{pkvpm_to_json_content}")

    # 将JSON数据转换为PKVPM格式
    json_to_pkvpm_content = parser.parse(pkvpm_to_json_content)
    print(f"JSON to PKVPM:\n{json_to_pkvpm_content}")
