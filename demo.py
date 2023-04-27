from yaml_function import orange_yaml

# yaml_file = "D:\Capstone1_KDTF\locators_config.yaml"
data_file='D:\\Capstone1_KDTF\\data_config.yaml'

orange_data = orange_yaml(data_file).yaml_reader()

locator_file='D:\\Capstone1_KDTF\\locators_config.yaml'

orange_locator = orange_yaml(locator_file).yaml_reader()
#
data=orange_locator['tab_xpath']
print(data)
for i in data.values():
	print(i)
#
# a= input('enter the value:')
# # a=int(a)
# print(type(a),a)

