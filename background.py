import cv2
import numpy as np

class BackGround:
    """
    Static map layer to display
    """
    def __init__(self,canvas,k_p2g,map_type='Tsinghua_Map_Intersection'):
        # load map images to self.grid_img
        self.X_MIN = 3500.0 # x, y range of the map
        self.X_MAX = 6100.0
        self.Y_MIN = 7600.0
        self.Y_MAX = 8900.0
        self.CENTER = ((self.X_MAX + self.X_MIN) / 2, (self.Y_MAX + self.Y_MIN) / 2)
        self.__load_map_split(map_type, 4, 2)
        
        self.canvas=canvas
        h,w,d=canvas.shape
        self.sz_pix=(w,h)
        self.k_p2g=k_p2g

        self.GX_MIN, self.GY_MIN = self.__geo2grid_tsinghua(self.X_MIN, self.Y_MIN)
        self.GX_MAX, self.GY_MAX = self.__geo2grid_tsinghua(self.X_MAX, self.Y_MAX)

    def __load_map_split(self, res_name, horizontal_num, vertical_num):
        im_list = []
        for i in range(horizontal_num):
            im_list.append([])
            for j in range(vertical_num):
                fig_name = res_name + '_' + str(i) + str(j) + '.jpg'
                fig_path = 'Resources/Rendering/' + res_name + '/' + fig_name
                im_list[i].append(cv2.imread(fig_path))
        self.grid_cycle = 1
        self.len_grid = (self.X_MAX - self.X_MIN)/horizontal_num
        self.grid_img = im_list

    def __geo2grid_tsinghua(self,x, y):
        return int((float(x) - self.X_MIN)//self.len_grid), int((float(y)-self.Y_MIN)//self.len_grid)

    def __geo2grid_1d(self,x):
        grid = int(float(x) // self.len_grid)
        return grid if float(grid) >= 0 else 0

    def set_pos(self, m_g2p, disp_quad):
        self.m_g2p = m_g2p
        self.disp_quad = disp_quad

    def draw(self):
        p1, p2, p3, p4 = self.disp_quad
        # self.rect = geometry.Polygon([p1, p2, p3, p4, p1])
        x1 = min(p1[0], p2[0], p3[0], p4[0])
        x2 = max(p1[0], p2[0], p3[0], p4[0])
        y1 = min(p1[1], p2[1], p3[1], p4[1])
        y2 = max(p1[1], p2[1], p3[1], p4[1])
        gx1 = max(self.__geo2grid_1d(x1), self.GX_MIN)
        gx2 = min(self.__geo2grid_1d(x2), self.GX_MAX)
        gy1 = max(self.__geo2grid_1d(y1), self.GY_MIN)
        gy2 = min(self.__geo2grid_1d(y2), self.GY_MAX)
        for gx in range(gx1, gx2+1):
            for gy in range(gy1, gy2+1):
                img = self.get_grid_image_tsinghua(gx, gy)
                r = self.__grid_geo_rect_tsinghua(gx, gy)
                self.draw_rect_image(img, r)

    def draw_rect_image(self, img, r):
        if img is not None:
            h, w, d = img.shape
            rect_tr = cv2.transform(np.array([[(r[0], r[1]), (r[0]+r[2], r[1]),
                                               (r[0]+r[2], r[1]+r[3])]],
                                             'float32'), self.m_g2p)
            mat = cv2.getAffineTransform(np.array([(0, h-1), (w-1, h-1),
                                                   (w-1, 0)], 'float32'), rect_tr)
            cv2.warpAffine(img, mat, self.sz_pix, self.canvas,
                           borderMode=cv2.BORDER_TRANSPARENT)

    def get_grid_image_tsinghua(self, gx, gy):
        gx_index = gx - self.GX_MIN
        gy_index = gy - self.GY_MIN
        return self.grid_img[gx_index][gy_index]

    def __grid_geo_rect_tsinghua(self,gx,gy):
        return ((gx)*self.len_grid, (gy)*self.len_grid, self.len_grid, self.len_grid)

    def uishow(self):
        cv2.imshow('Autonomous Car Simulation',self.canvas)
        print(self.canvas.shape)
        key=cv2.waitKey(0)
        return key