from display import Display
import numpy as np

vehicles = []
# vehicles.append({'type': 500, 'x': 4150.154067852198, 'y': 8385.915221484507, 'angle': -89.745263830916, 'v': 2.2075325753400104, 'rotation': 0, 'winker': 0, 'winker_time': 0, 'render_flag': True, 'length': 1.0, 'width': 0.48, 'lane_index': 1, 'max_decel': 7.0})
# vehicles.append({'type': 500, 'x': 4150.154067852198, 'y': 8395.915221484507, 'angle': -89.745263830916, 'v': 2.2075325753400104, 'rotation': 0, 'winker': 0, 'winker_time': 0, 'render_flag': True, 'length': 1.0, 'width': 0.48, 'lane_index': 1, 'max_decel': 7.0})
# vehicles.append({'type': 2000, 'x': 4150.154067852198, 'y': 8395.915221484507, 'angle': -89.745263830916, 'v': 2.2075325753400104, 'rotation': 0, 'winker': 0, 'winker_time': 0, 'render_flag': True, 'length': 6.2, 'width': 2.1, 'lane_index': 1, 'max_decel': 7.0})
vehicles.append({'type': 0, 'x': 4150.154067852198, 'y': 8536.915221484507, 'angle': 2, 'v': 2.2075325753400104, 'rotation': 0, 'winker': 0, 'winker_time': 0, 'render_flag': True, 'length': 4.5, 'width': 1.8, 'lane_index': 1, 'max_decel': 7.0})
vehicles.append({'type': 1, 'x': 4160.154067852198, 'y': 8536.915221484507, 'angle': 2, 'v': 2.2075325753400104, 'rotation': 0, 'winker': 0, 'winker_time': 0, 'render_flag': True, 'length': 4.5, 'width': 1.8, 'lane_index': 1, 'max_decel': 7.0})

# the unit of angle is degree
# hight and width of the canvas
h = 800
w = 800
canvas=np.zeros((h, w, 3), dtype='uint8')
disp = Display(canvas, map_type='Tsinghua_Map_Intersection')

for i in range(1000):
    for veh in vehicles:
        veh['x'] += 0.1 * np.cos(veh['angle']/180*np.pi)
        veh['y'] += 0.1 * np.sin(veh['angle']/180*np.pi)
    disp.set_data(vehicles)
    disp.set_pos((vehicles[0]['x'], vehicles[0]['y']), 0.0)
    disp.draw()
    disp.uishow()