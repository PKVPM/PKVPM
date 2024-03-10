import json
import yaml

from typing import Dict, Union


class Parser:

    def __init__(self):
        # 初始化数据
        self.data = {}
        # 类型转换器
        self.type_converters = {
            "list": self.translate_list,
            "bool": lambda x: x.lower() == "true",
            "int": int,
            "float": float,
            "str": str,
        }

    def linear_format_generator(self, kv_data, prefix=""):
        """
        将键值数据转换为线性格式的键值对列表
        :param kv_data: 键值对数据
        :param prefix: 键的前缀
        :return: 线性格式的键值对列表
        """
        if isinstance(kv_data, dict):
            for key, value in kv_data.items():
                if isinstance(value, list):
                    # 如果值是列表，则将其转换为逗号分隔的字符串，并记录每个值的类型
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
        将输入数据转换为多态键值路径映射格式
        :param content: 输入数据(字符串或字典)
        :return: 多态键值路径映射格式(PKVPM)数据字符串
        """

        # 如果是字符串就假设输入为YAML文本并转换为字典对象，如果是字典就直接使用无需转换。
        content = yaml.safe_load(content) if isinstance(content, str) else content

        # 转换为线性格式
        linear_format = list(self.linear_format_generator(content))

        # 保存线性格式数据
        line_list = []
        for path, value, value_type in linear_format:
            # 如果值的类型是列表，不进行转换，直接保存
            if value_type == list:
                line = f"[{value_type.__name__}]: {path}: {value}"
            else:
                line = f"[{value_type}]: {path}: {value}"
            line_list.append(line)

        result = "\n".join(line_list)

        # 返回线性格式数据
        return result

    def translate_list(self, value):
        """
        将列表字符串转换为列表，并保留每个元素的类型
        value: 列表字符串，例如：1|[int], 2.2|[float], true|[bool]
        """
        items = [
            item.split("|") for item in value.split(", ") if item.strip()
        ]  # 跳过空字符串的元素
        result = []
        for item in items:
            if isinstance(item, list) and len(item) == 2:
                item_value, item_type = item
                if item_type == "[int]":
                    result.append(int(item_value))
                elif item_type == "[float]":
                    result.append(float(item_value))
                elif item_type == "[bool]":
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

    def to_json(self):
        """
        将数据转换为 JSON 格式
        """
        return json.dumps(self.data, indent=4)

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
        else:
            print(yaml.dump(data, sort_keys=False, indent=4, allow_unicode=True, default_flow_style=False))


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

    # 创建解析器
    parser = Parser()

    # 构建到tests目录下文件的路径
    tests_file_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.yml')

    # 读取 YAML 文件
    with open(tests_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 解析 YAML 数据
    pkvpm_content = parser.parse(content)
    print(pkvpm_content)

    # 保存 PKVPM 数据
    pkvpm_file_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.pkvpm')
    with open(pkvpm_file_path, 'w', encoding='utf-8') as file:
        file.write(pkvpm_content)

    # 读取 PKVPM 文件
    with open(pkvpm_file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # 添加翻译
    for line in data.split('\n'):
        if line:
            path, value, value_type = parser.process_translation_line(line)
            parser.add_translation(path, value, value_type)

    # 输出 JSON 格式数据
    # print(parser.to_json())

    # 输出 YAML 格式数据
    yaml_file = parser.to_yaml(data, os.path.join(os.path.dirname(__file__), '..', 'tests', 'test_output.yml'))
    print(yaml_file)
