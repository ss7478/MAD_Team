import random
with open('/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'r') as f:
        old = f.readlines()
        old.clear()
        old = ['<?xml version="1.0" ?>\n', '<sdf version="1.5">\n', '  <world name="default">\n', '    <!-- A global light source -->\n', '    <include>\n', '      <uri>model://sun</uri>\n', '    </include>\n', '    <include>\n', '      <uri>model://parquet_plane</uri>\n', '      <pose>0 0 -0.01 0 0 0</pose>\n', '    </include>\n', '    <include>\n', '      <uri>model://dronepoint_blue</uri>\n', '      <name>one</name>\n', '      <pose>5 7 -0.01 0 0 0</pose>\n', '    </include>\n', '\n', '    <include>\n', '      <uri>model://dronepoint_green</uri>\n', '      <name>two</name>\n', '      <pose>4 5 -0.01 0 0 0</pose>\n', '    </include>\n', '    <include>\n', '      <uri>model://dronepoint_green</uri>\n', '      <name>three</name>\n', '      <pose>7 3 -0.01 0 0 0</pose>\n', '    </include>\n', '    <include>\n', '      <uri>model://dronepoint_green</uri>\n', '      <name>four</name>\n', '      <pose>8 4 -0.01 0 0 0</pose>\n', '    </include>\n', '    <include>\n', '      <uri>model://dronepoint_red</uri>\n', '      <name>five</name>\n', '      <pose>6 8 -0.01 0 0 0</pose>\n', '    </include>\n', '\n', '\n', '\n', '    <include>\n', '      <uri>model://aruco_cmit_txt</uri>\n', '    </include>\n', '\n', '    <scene>\n', '      <ambient>0.8 0.8 0.8 1</ambient>\n', '      <background>0.8 0.9 1 1</background>\n', '      <shadows>false</shadows>\n', '      <grid>false</grid>\n', '      <origin_visual>false</origin_visual>\n', '    </scene>\n', '  \n', "    <physics name='default_physics' default='0' type='ode'>\n", '      <gravity>0 0 -9.8066</gravity>\n', '      <ode>\n', '        <solver>\n', '          <type>quick</type>\n', '          <iters>10</iters>\n', '          <sor>1.3</sor>\n', '          <use_dynamic_moi_rescaling>0</use_dynamic_moi_rescaling>\n', '        </solver>\n', '        <constraints>\n', '          <cfm>0</cfm>\n', '          <erp>0.2</erp>\n', '          <contact_max_correcting_vel>100</contact_max_correcting_vel>\n', '          <contact_surface_layer>0.001</contact_surface_layer>\n', '        </constraints>\n', '      </ode>\n', '      <max_step_size>0.004</max_step_size>\n', '      <real_time_factor>1</real_time_factor>\n', '      <real_time_update_rate>250</real_time_update_rate>\n', '      <magnetic_field>6.0e-6 2.3e-5 -4.2e-5</magnetic_field>\n', '    </physics>\n', '  </world>\n', '</sdf>\n']
with open('/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w') as f:
        f.writelines(old)

p1, p2, p3, p4, p5 = random.randint(0,3), random.randint(0,3), random.randint(0,3), random.randint(0,3), random.randint(0,3)

arr_of_p = [p1, p2, p3, p4, p5]
arr_for_cords = [14, 20, 25, 30, 35]
xa = random.sample(range(10), 5)
arr_of_n = [12, 18, 23, 28, 33]
arr_for_xy = [0, 1, 2, 3, 4]
ya = random.sample(range(10), 5)
print(arr_of_n)
print(arr_of_p)
print(xa)
print(ya)

for w, l, z, x, y in zip(arr_of_p, arr_of_n, arr_for_cords, xa, ya):
    if w == 0:
        w = 'red'
    elif w == 1:
        w = 'blue'
    elif w == 2:
        w = 'yellow'
    elif w == 3:
        w = 'green'
    with open('/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'r') as f:
        old = f.readlines()

    old[l] = '      <uri>model://dronepoint_' + str(w) + '</uri>\n'
    old[z] = '      <pose>' + str(x) + ' ' +str(y) + ' '+ '-0.01 0 0 0</pose>\n'
    print(w)

    with open('/home/clover/catkin_ws/src/clover/clover_simulation/resources/worlds/clover_aruco.world', 'w') as f:
        f.writelines(old)

