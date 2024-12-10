import xml.etree.ElementTree as ET
import requests
import zipfile
import shutil

url = 'https://github.com/bart02/dronepoint/archive/refs/heads/main.zip'
r = requests.get(url)

arr_names = ['dronepoint_green','dronepoint_red', 'dronepoint_blue', 'dronepoint_yellow']

# clover launch
file_path = '/home/clover/catkin_ws/src/clover/clover/launch/clover.launch'
tree = ET.parse(file_path)
root = tree.getroot()

for arg in root.findall('arg'):
    if arg.get('name') == 'aruco':
        arg.set('default', 'true')
        break

tree.write(file_path, encoding='utf-8', xml_declaration=True)

# aruco launch
file_path = '/home/clover/catkin_ws/src/clover/clover/launch/aruco.launch'
tree = ET.parse(file_path)
root = tree.getroot()

for arg in root.findall('arg'):
    if arg.get('name') == 'aruco_map':
        arg.set('default', 'true')
    if arg.get('name') == 'aruco_vpe':
        arg.set('default', 'true')
    if arg.get('name') == 'map':
        arg.set('default', 'cmit.txt')

tree.write(file_path, encoding='utf-8', xml_declaration=True)

with open('/home/clover/catkin_ws/src/clover/clover_simulation/models/main.zip', 'wb') as f: 
    f.write(r.content)

with zipfile.ZipFile('/home/clover/catkin_ws/src/clover/clover_simulation/models/main.zip', 'r') as f:
    f.extractall('/home/clover/catkin_ws/src/clover/clover_simulation/models')

for i, j in zip(range(4), arr_names):
    shutil.move('/home/clover/catkin_ws/src/clover/clover_simulation/models/dronepoint-main/' + j, '/home/clover/catkin_ws/src/clover/clover_simulation/models/' + j)


