import json
import yaml
from typing import Dict, Union


class Parser:
    def __init__(self):
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
        """
        if isinstance(kv_data, dict):
            for key, value in kv_data.items():
                if isinstance(value, list):
                    value_with_types = ", ".join(f"{item}|[{type(item).__name__}]" for item in value)
                    yield f"{prefix}.{key}" if prefix else key, value_with_types, 'list'
                else:
                    yield from self.linear_format_generator(value, prefix=f"{prefix}.{key}" if prefix else key)
        elif isinstance(kv_data, list):
            for index, value in enumerate(kv_data):
                yield from self.linear_format_generator(value, prefix=f"{prefix}[{index}]")
        else:
            yield prefix, kv_data, type(kv_data).__name__

    def parse(self, content: Union[str, Dict]) -> str:
        """
        将输入数据转换为多态键值路径映射格式
        """
        content = yaml.safe_load(content) if isinstance(content, str) else content
        linear_format = list(self.linear_format_generator(content))
        line_list = [f"[{value_type}]: {path}: {value}" for path, value, value_type in linear_format]
        return "\n".join(line_list)

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

    def add_translation(self, path, value, value_type, data):
        """
        添加翻译
        """
        keys = path.split(".")
        current_dict = data
        for key in keys[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        converter = self.type_converters.get(value_type, lambda x: x)
        current_dict[keys[-1]] = converter(value)

    def process_translation_line(self, line):
        """
        处理翻译行
        """
        line = line.strip()
        value_type, path_value = line.split("]: ", 1)
        value_type = value_type[1:]
        path, value = path_value.split(": ", 1)
        return path, value, value_type

    def to_yaml(self, pkvpm_str, file_path=None):
        """
        将PKVPM格式数据转换为YAML格式
        """
        data = {}
        for line in pkvpm_str.split('\n'):
            if line:
                path, value, value_type = self.process_translation_line(line)
                self.add_translation(path, value, value_type, data)
        yaml_str = yaml.dump(data, sort_keys=False, indent=4, allow_unicode=True, default_flow_style=False)
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(yaml_str)

        return yaml_str

    def to_json(self, pkvpm_str, file_path=None):
        """
        将数据转换为 JSON 格式
        """
        yaml_data = self.to_yaml(pkvpm_str, file_path=file_path)
        json_data = json.dumps(yaml.safe_load(yaml_data), indent=4)

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(json_data)

        return json_data


if __name__ == "__main__":
    import os

    parser = Parser()

    # 示例使用，读取测试需要的一共3个文件（test.yml, test.json, test.pkvpm）
    test_yml_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.yml')
    test_json_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.json')
    test_pkv_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'test.pkvpm')

    # 读取YAML文件
    with open(test_yml_path, 'r', encoding='utf-8') as file:
        test_yml_content = file.read()

    # 读取JSON文件
    with open(test_json_path, 'r', encoding='utf-8') as file:
        test_json_content = file.read()

    # 读取PKV文件
    with open(test_pkv_path, 'r', encoding='utf-8') as file:
        test_pkvpm_content = file.read()

    # 将YAML数据转换为PKVPM格式
    yaml_to_pkvpm_content = parser.parse(test_yml_content)
    # print(f"YAML to PKVPM:\n{yaml_to_pkvpm_content}")

    # 将PKVPM格式数据转换为YAML格式
    pkvpm_to_yaml_content = parser.to_yaml(yaml_to_pkvpm_content, test_yml_path)
    print(f"PKVPM to YAML:\n{pkvpm_to_yaml_content}")

    # 将PKVPM格式数据转换为JSON格式
    pkvpm_to_json_content = parser.to_json(test_pkvpm_content, test_json_path)
    print(f"PKVPM to JSON:\n{pkvpm_to_json_content}")

    # 将JSON数据转换为PKVPM格式
    json_to_pkvpm_content = parser.parse(test_json_content)
    print(f"JSON to PKVPM:\n{json_to_pkvpm_content}")




