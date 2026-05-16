import re

text_string = "nb_drones: 5"
test_string2 = "hub: roof1 3 4"
pattern = re.compile(r"^nb_drones:\s\d+$")
pattern2 = re.compile(r"hub:\s\w+\s\d+\s\d+")
res = re.findall(pattern2, test_string2)
if bool(res):
    print("THis is res", res[0])
