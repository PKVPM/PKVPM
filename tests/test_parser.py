# test_parser.py
import unittest
from pkvpm.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        """在每个测试前执行，用于设置测试环境"""
        self.parser = Parser()
        # 你可以在这里加载或定义一些测试数据

    def test_parse(self):
        """测试 parse 方法"""
        test_data = {
            'key1': 'value1',
            'key2': ['value2', 'value3', 'value4'],
            'key3': 123,
            'key4': 123.456,
            'key5': True,
            'key6': [1, 2, 3],
            'key7': [1.1, 2.2, 3.3],
            'key8': [True, False, True],
            'key9': [1, 2.2, True],
            'path1': {
                'path2': {
                    'path3': 'value1'
                }
            }
        }
        expected_output = """[str]: key1: value1
[list]: key2: value2|[str], value3|[str], value4|[str]
[int]: key3: 123
[float]: key4: 123.456
[bool]: key5: true
[list]: key6: 1|[int], 2|[int], 3|[int]
[list]: key7: 1.1|[float], 2.2|[float], 3.3|[float]
[list]: key8: true|[bool], false|[bool], true|[bool]
[list]: key9: 1|[int], 2.2|[float], true|[bool]
[str]: path1.path2.path3: value1
"""
        result = self.parser.parse(test_data)
        self.assertEqual(result.strip(), expected_output.strip())

    # 在这里可以添加更多的测试方法


if __name__ == '__main__':
    unittest.main()
