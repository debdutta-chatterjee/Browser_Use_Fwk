from src.util.file_util import FileUtil





file_content = FileUtil.read_file_to_string("./test_cases/tc_0001_ui_flow.feature")
print(file_content)

steps_only = FileUtil.extract_steps(file_content)
print(steps_only)