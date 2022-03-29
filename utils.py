import numpy as np

def get_rotate_point(center, angle, pt):
    """
    get rotated position of point pt with the center and angle
    """
    x0, y0 = center
    x, y = pt
    dx, dy = x - x0, y - y0
    theta = float(angle) / 180.0 * np.pi
    x1 = dx * np.cos(theta) - dy * np.sin(theta) + x0
    y1 = dx * np.sin(theta) + dy * np.cos(theta) + y0
    return x1, y1

class VehicleModelsReader(object):
    """用于读取不同车辆模型信息文件的类

        LasVSim所用到的所有车辆的模型信息保存在
        Library/vehicle_model_library.csv里,该模块
        用于从该文件中获取每种车辆的模型信息。

        Attributes:
            __type_array(tuple(int)): 车辆类型编号元组. #元组不可变
            __lasvsim_version(string): 代码版本类型. 'gui' or 'package'
            __info(dict(int: tuple)): 保存各类型车辆模型信息的字典

    """

    def __init__(self, model_path):
        """
        VehicleModelsReader类构造函数

        Args:
            model_path(string): 文件路径
        """
        self.__type_array = (0, 1, 2, 3, 7, 100, 1000, 200, 2000, 300, 301, 302, 500)
        self.__lasvsim_version = 'gui'
        self.__info = dict()
        self.__read_file(model_path)

    def __read_file(self, file_path):
        """读取车辆模型信息保存文件

        Args:
            file_path(string): 文件路径

        Returns:

        """
        with open(file_path) as f:
            line = f.readline()
            line = f.readline()
            while len(line)>0:
                data = line.split(',')
                type = int(data[1])
                if type not in self.__type_array:
                    line=f.readline()
                    continue
                length=float(data[7])
                width=float(data[8])
                x=float(data[4])  # 车一侧到原点的距离
                y=float(data[2])  # 车头到原点的距离
                if self.__lasvsim_version == 'package':
                    img_path = []
                else:
                    img_path = 'Resources/Rendering/%d.png' % type
                self.__info[type] = (length, width, x, y, img_path)
                line = f.readline()

    def get_types(self):
        """
        返回保存车辆类型编号的元组

        Returns:
            保存车辆类型编号的元组
        """
        return self.__type_array

    def get_vehicle(self, type):
        """
        返回输入车辆类型的长、宽、车一侧到原点的距离、车头到原点的距离和渲染图片
        的保存路径。

        Args:
            type(int): 车辆类型编号

        Returns:
            车辆参数元组。
            例：
            (length(m), width(m), center_to_side(m), center_to_head(m),
            render_image_path(string))

        """
        if type not in self.__info:
            type = 0
        return self.__info[type]
