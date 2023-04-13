from yaml_function import orange_yaml

yaml_file = "D:\Capstone1_KDTF\locators_config.yaml"

orange_data = orange_yaml(yaml_file).yaml_reader()

data=orange_data['tabs_xpath']
print(data)
for i in data:
	print(i)