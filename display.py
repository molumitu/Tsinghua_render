# coding=utf-8
from time import sleep
import numpy as np
import cv2
from math import pi, cos, sin, ceil, copysign
from background import BackGround
from utils import get_rotate_point, VehicleModelsReader
# update in real-time manner
class Display:
    def __init__(self, canvas=None, map_type=None):
        self.map_type = map_type
        self.reset_canvas(canvas)
        self._load_vehicle_patterns()

        self.X_MIN = 3500.0
        self.X_MAX = 6100.0
        self.Y_MIN = 7600.0
        self.Y_MAX = 8900.0

    def reset_canvas(self, canvas):
        self.k_p2g = 650/15000
        self.canvas=canvas
        h,w,d=canvas.shape
        self.sz_pix=(w,h)
        self.sz_geo = (float(self.sz_pix[0])*self.k_p2g,float(self.sz_pix[1])*self.k_p2g)
        self.background=BackGround(self.canvas,self.k_p2g,self.map_type)

    def _load_vehicle_patterns(self):
        self.vehicle_images = dict()   # vehicle images for all types
        self.vehicle_sizes = dict()    # vehicle sizes for all types
        vehicle_patterns = VehicleModelsReader('Library/vehicle_model_library.csv')
        types = vehicle_patterns.get_types()
        for t in types:
            h, w, x, y, img_path = vehicle_patterns.get_vehicle(t)
            k = self.k_p2g
            sz=[int(w/k),int(h/k)]
            sz[0]=sz[0]-sz[0]%2+1
            center=(sz[0]/2,int(y/k))
            self.vehicle_images[t]=self.__load_obj_image(img_path,sz,center)
            self.vehicle_sizes[t] = (sz[0]/2, int(y/k), sz)

    def set_pos(self, center, angle):
        """根据自车当前位置移动渲染画面，保持自车中心始终位于画面正中央"""
        self.center = center
        self.angle = angle  # roate the canvas
        cx, cy = center[0] - self.X_MIN, center[1] - self.Y_MIN # m
        sx, sy = self.sz_geo # m 
        matrix = cv2.getRotationMatrix2D(center, self.angle, 1)

        corners_raw = np.array(
            [[[cx - sx / 2, cy - sy / 2], [cx - sx / 2, cy + sy / 2],
              [cx + sx / 2, cy + sy / 2],
              [cx + sx / 2, cy - sy / 2]]],
            dtype='float32')  # m
        p1, p2, p3, p4 = cv2.transform(corners_raw, matrix)[0]

        pix_p1 = (0, self.sz_pix[1]-1)
        pix_p2 = (0, 0)
        pix_p3 = (self.sz_pix[0]-1, 0)
        pix_p4 = (self.sz_pix[0]-1, self.sz_pix[1]-1)
        self.m_g2p = cv2.getAffineTransform(np.array([p1, p2, p3], 'float32'),
                                            np.array([pix_p1, pix_p2, pix_p3],'float32'))
        # map real geo array to pix array
        self.background.set_pos(self.m_g2p, [p1, p2, p3, p4])

    def geo2pix(self,pt):
        pt_px=cv2.transform(np.array([[pt]],'float32'),self.m_g2p)
        return [int(round(x)) for x in pt_px[0][0]]

    def set_data(self, veh_info):
        self.veh_info = veh_info

    def draw(self):
        self.canvas[:]=200 # gray
        self.background.draw()
        self.draw_vehicles() #画车辆
        # self.draw_sensor_range()
        # cv2.putText(self.canvas,'speed:%0.1f km/h'%v,(0,695),cv2.FONT_HERSHEY_DUPLEX,0.5,(0,0,200))
        # cv2.putText(self.canvas,'time:%0.1f s'%self.display_info['t'],(0,695-15),cv2.FONT_HERSHEY_DUPLEX,0.5,(0,0,200))

    def draw_vehicles(self):
        """渲染交通流"""
        for i in range(len(self.veh_info)):
            self.__draw_vehicle(self.veh_info[i])

    def draw_line(self, p1, p2, color=(0,180,0)):
        x1, y1 = [int(f) for f in self.geo2pix(p1)]
        x2, y2 = [int(f) for f in self.geo2pix(p2)]
        cv2.line(self.canvas, (x1, y1), (x2, y2), color, 1,)

    def draw_polygon(self, polygon, color):
        for i in range(len(polygon)):
            p1=polygon[i]
            p2=polygon[(i+1)%len(polygon)]
            self.draw_line(p1,p2,color)

    def draw_detected_pos(self):
        """Draw detected vehicle's detection result outline.
        """
        for i, x, y, v, a, w, l in self.detected_vehicles:
            rect = [get_rotate_point((x, y), a-90, p) for
                    p in [(x-w/2, y-l/2), (x-w/2, y+l/2),
                          (x+w/2, y+l/2), (x+w/2, y-l/2)]]
            self.draw_polygon(rect, (0, 0, 255))

    def __load_obj_image(self,img_path,size,center):
        img_raw=cv2.resize(cv2.imread(img_path),tuple(size))
        mask_raw=cv2.resize(cv2.imread(img_path,-1)[:,:,3],tuple(size))
        px,py=center
        px = int(px)
        py = int(py)
        r=int(np.sqrt(px*px+py*py))+1
        img=cv2.copyMakeBorder(img_raw,r-py,r-(size[1]-py-1),r-px,r-px,borderType=cv2.BORDER_CONSTANT,value=(0,0,0))
        mask=np.zeros(img_raw.shape,'uint8')
        mask[:,:,0]=mask_raw
        mask[:,:,1]=mask_raw
        mask[:,:,2]=mask_raw
        mask=cv2.copyMakeBorder(mask,r-py,r-(size[1]-py-1),r-px,r-px,borderType=cv2.BORDER_CONSTANT,value=(0,0,0))
        return (img,mask)

    def __draw_obj_image(self, img, mask, px_pt, px_ang):
        """Draw all vehicle's graph, turn light and ego vehicle's outline.

        This function doesn't draw detected vehicle's outline.
        """
        h, w, d = img.shape
        r = int(h/2)
        m = cv2.getRotationMatrix2D((r, r), px_ang, 1)
        img_rot = cv2.warpAffine(img, m, (w, h))
        mask = cv2.warpAffine(mask, m, (w, h)) > 0
        x1, y1, x2, y2 = 0, 0, w, h
        if px_pt[0]-r < 0:
            x1 = r-px_pt[0]
        if px_pt[0]-r+x2 > self.sz_pix[0]:
            x2 = self.sz_pix[0]-px_pt[0]+r
        if px_pt[1]-r < 0:
            y1 = r-px_pt[1]
        if px_pt[1]-r+y2 > self.sz_pix[1]:
            y2 = self.sz_pix[1]-px_pt[1]+r
        if x1 >= x2 or y1 >= y2 or x1 < 0 or y1 < 0 or x2 > w or y2 > h:
            return
        np.copyto(self.canvas[px_pt[1]-r+y1:px_pt[1]-r+y2,
                  px_pt[0]-r+x1:px_pt[0]-r+x2, :],
                  img_rot[y1:y2, x1:x2, :], where=mask[y1:y2, x1:x2, :])

    def __draw_vehicle(self, veh):
        veh_x = veh['x']
        veh_y = veh['y']
        veh_heading = veh['angle']
        veh_type = veh['type']
        veh_length = veh['length']
        veh_width = veh['width']

        self.dis = 1.9
        self.geo_pt = (veh_x - cos(veh_heading / 180.0 * pi) * self.dis - self.X_MIN,
                       veh_y - sin(veh_heading / 180.0 * pi) * self.dis - self.Y_MIN)
        self.geo_angle = veh_heading - 90.0  # 神仙坐标系
        self.px, self.py = self.geo2pix(self.geo_pt)
        self.px_pt = (int(round(self.px)), int(round(self.py)))
        self.ang = self.geo_angle+self.angle
        self.img, self.mask = self.vehicle_images[veh_type]
        self.img = np.array(self.img)
        self.mask = np.array(self.mask)
        self.__draw_obj_image(self.img, self.mask, self.px_pt, self.ang)
        if veh_type in [1000, 2000]:  # 画自车的外形轮廓
            veh_length = 6.2  #回放模式下自车默认为小车，待修改
            veh_width = 2.1  #回放模式下自车默认为小车，待修改
            rect = [get_rotate_point((veh_x, veh_y), veh_heading-90,
                                     p) for
                    p in [(veh_x-veh_width/2, veh_y-veh_length/2),
                          (veh_x-veh_width/2, veh_y+veh_length/2),
                          (veh_x+veh_width/2, veh_y+veh_length/2),
                          (veh_x+veh_width/2, veh_y-veh_length/2)]]
            self.draw_polygon(rect, (0, 180, 0))

    def draw_sensor_range(self):
        x,y,v,a=self.own_car_pos
        a=a-90
        for s in self.sensors:
            dx=s.installation_lateral_bias
            dy=s.installation_longitudinal_bias
            theta=a/180.0*pi
            x1=x+dx*cos(theta)-dy*sin(theta)
            y1=y+dx*sin(theta)+dy*cos(theta)
            self.draw_sector((x1, y1), s.detection_range,
                             a+s.installation_orientation_angle,
                             s.detection_angle)

    def draw_sector(self, center, radius, a_dir, a_range):
        x,y = self.geo2pix(center)
        r=int(radius/self.k_p2g)
        self_ang=270.0-(a_dir+self.angle+a_range/2)
        self.draw_pix_sector((x,y),r,self_ang,0.0,a_range)

    def draw_pix_sector(self, center, radius, self_ang, a1, a2):
        img=np.zeros(self.canvas.shape,'uint8')
        cv2.ellipse(img,center,(radius,radius),self_ang,a1,a2,(255,255,255),-1)
        self.canvas[:]=cv2.addWeighted(self.canvas,1,img,0.08,0)

    def uishow(self):
        cv2.imshow('Autonomous Car Simulation',self.canvas)
        key=cv2.waitKey(10)
        return key








