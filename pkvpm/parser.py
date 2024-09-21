#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description: PKVPM Parser library for converting between YAML, JSON, and PKVPM formats.
@Date: 2024/09/21
@version: 1.0.2
@License: MIT License
@Github: https://github.com/PKVPM/PKVPM

@Contributors:
https://github.com/Evil0ctal
https://github.com/Johnserf-Seed
"""

import json
import yaml
import re
import os
from datetime import date, datetime
from typing import Dict, Union


class Parser:

    def __init__(self):
        # 初始化数据
        self.data = {}
        # 类型转换器
        self.type_converters = {
            "list": json.loads,
            "bool": json.loads,
            "int": json.loads,
            "float": json.loads,
            "str": json.loads,
            "date": self.parse_date,
            "NoneType": lambda x: None,
        }

    def flatten(self, data, parent_key='', sep='.'):
        """
        将嵌套的字典和列表展平成键值对列表
        """
        items = []
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
                items.extend(self.flatten(v, new_key, sep=sep))
        elif isinstance(data, list):
            for i, v in enumerate(data):
                new_key = f"{parent_key}[{i}]" if parent_key else f"[{i}]"
                items.extend(self.flatten(v, new_key, sep=sep))
        else:
            # 获取数据类型的名称
            value_type = type(data).__name__
            items.append((parent_key, data, value_type))
        return items

    def parse(self, content: Union[str, Dict]) -> str:
        """
        将输入数据转换为多态键值路径映射格式
        :param content: 输入数据(字符串或字典)
        :return: PKVPM 数据字符串
        """
        # 如果是字符串，假设输入为 YAML 文本并转换为字典对象
        content = yaml.safe_load(content) if isinstance(content, str) else content

        # 展平数据
        linear_format = self.flatten(content)

        # 构建输出行
        line_list = []
        for path, value, value_type in linear_format:
            # 处理特殊类型
            if isinstance(value, (date, datetime)):
                value_serialized = json.dumps(value.isoformat())
                value_type = 'date'
            elif value is None:
                value_serialized = 'null'
                value_type = 'NoneType'
            else:
                value_serialized = json.dumps(value, ensure_ascii=False)
            line = f"[{value_type}]: {path}: {value_serialized}"
            line_list.append(line)

        result = "\n".join(line_list)
        return result

    def process_translation_line(self, line):
        """处理翻译行
        :param line: 翻译行
        :return: 路径、值、值类型
        """
        line = line.strip()
        # 先匹配类型
        if not line.startswith('['):
            raise ValueError(f"Invalid line format: {line}")
        type_end = line.find(']: ')
        if type_end == -1:
            raise ValueError(f"Invalid line format: {line}")
        value_type = line[1:type_end]
        rest = line[type_end + 3:]
        # 找到最后一个 ': '，以此分隔路径和值
        split_index = rest.rfind(': ')
        if split_index == -1:
            raise ValueError(f"Invalid line format: {line}")
        path = rest[:split_index]
        value = rest[split_index + 2:]
        return path, value, value_type

    def set_value(self, data_dict, path, value):
        """根据路径在嵌套字典中设置值
        :param data_dict: 数据字典
        :param path: 路径字符串
        :param value: 要设置的值
        """
        keys = re.findall(r'[^.\[\]]+|\[\d+\]', path)
        current = data_dict
        for i, key in enumerate(keys):
            if key.startswith('[') and key.endswith(']'):
                # 处理列表索引
                index = int(key[1:-1])
                if not isinstance(current, list):
                    current = []
                while len(current) <= index:
                    current.append({})
                if i == len(keys) - 1:
                    # 最后一个键，设置值
                    current[index] = value
                else:
                    current = current[index]
            else:
                if i == len(keys) - 1:
                    # 最后一个键，设置值
                    current[key] = value
                else:
                    next_key = keys[i + 1] if i + 1 < len(keys) else None
                    if next_key and next_key.startswith('['):
                        # 下一个键是列表索引，current[key] 应该是列表
                        if key not in current or not isinstance(current[key], list):
                            current[key] = []
                    else:
                        # 下一个键不是列表索引，current[key] 应该是字典
                        if key not in current or not isinstance(current[key], dict):
                            current[key] = {}
                    current = current[key]

    def translate_list(self, value):
        """
        将字符串解析为列表，支持嵌套列表和字典
        :param value: 列表字符串，应该是 JSON 格式的字符串
        :return: 解析后的列表对象
        """
        # 使用 json.loads 解析列表字符串
        return json.loads(value)

    def parse_date(self, value):
        """
        将日期字符串解析为 datetime.date 对象
        :param value: 日期字符串
        :return: datetime.date 对象
        """
        date_str = json.loads(value)
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # 如果解析失败，返回原始字符串
            return date_str

    def add_translation(self, path, value, value_type, data=None):
        """添加翻译
        :param path: 路径
        :param value: 值（已序列化）
        :param value_type: 值类型
        :param data: 数据字典
        """
        if data is None:
            data = self.data
        # 获取对应的类型转换器
        converter = self.type_converters.get(value_type, lambda x: x)
        # 反序列化值
        value_deserialized = converter(value)
        # 设置值
        self.set_value(data, path, value_deserialized)

    def to_json(self, pkvpm_str, file_path=None):
        """
        将 PKVPM 数据字符串转换为 JSON 格式
        :param pkvpm_str: PKVPM 数据字符串
        :param file_path: 输出的 JSON 文件路径
        :return: JSON 格式的数据
        """
        yaml_data = self.to_yaml(pkvpm_str)
        data = yaml.safe_load(yaml_data)
        json_data = json.dumps(data, ensure_ascii=False, indent=4, default=str)

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(json_data)

        return json_data

    def to_yaml(self, data=None, file_path=None):
        """
        将数据转换为 YAML 格式
        :param data: PKVPM 格式数据，如果为 None 则使用初始化的数据
        :param file_path: 输出的 YAML 文件路径
        :return: YAML 格式数据
        """
        if data:
            # 创建一个新的空字典来存储解析后的数据
            new_data = {}
            for line in data.split('\n'):
                if line.strip():
                    path, value, value_type = self.process_translation_line(line)
                    self.add_translation(path, value, value_type, new_data)
            data = new_data
        else:
            data = self.data

        yaml_data = yaml.dump(data, sort_keys=False, indent=4, allow_unicode=True, default_flow_style=False)

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(yaml_data)

        return yaml_data


if __name__ == "__main__":

    parser = Parser()

    # 示例使用，读取测试需要的 3 个文件（test.yml, test.json, test.pkv）
    test_yml_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.yml')
    test_json_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.json')
    test_pkv_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.pkv')

    # 读取 YAML 文件
    with open(test_yml_path, 'r', encoding='utf-8') as file:
        test_yml_content = file.read()

    # 读取 JSON 文件
    with open(test_json_path, 'r', encoding='utf-8') as file:
        test_json_content = file.read()

    # 读取 PKV 文件
    with open(test_pkv_path, 'r', encoding='utf-8') as file:
        test_pkvpm_content = file.read()

    # 将 YAML 数据转换为 PKVPM 格式
    yaml_to_pkvpm_content = parser.parse(test_yml_content)
    print(f"YAML to PKVPM:\n{yaml_to_pkvpm_content}")

    # 保存 PKVPM 格式数据
    with open(test_pkv_path, 'w', encoding='utf-8') as file:
        file.write(yaml_to_pkvpm_content)

    # 将 PKVPM 格式数据转换为 YAML 格式
    pkvpm_to_yaml_content = parser.to_yaml(yaml_to_pkvpm_content, test_yml_path)
    print(f"PKVPM to YAML:\n{pkvpm_to_yaml_content}")

    # 将 PKVPM 格式数据转换为 JSON 格式
    pkvpm_to_json_content = parser.to_json(yaml_to_pkvpm_content, test_json_path)
    print(f"PKVPM to JSON:\n{pkvpm_to_json_content}")

    # 将 JSON 数据转换为 PKVPM 格式
    json_to_pkvpm_content = parser.parse(pkvpm_to_json_content)
    print(f"JSON to PKVPM:\n{json_to_pkvpm_content}")
