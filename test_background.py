import numpy as np
import cv2
from background import BackGround

k_p2g = 650/15000

h = 500
w = 500
canvas=np.zeros((h, w, 3), dtype='uint8')
X_MIN = 3500.0 # x, y range of the map
X_MAX = 6100.0
Y_MIN = 7600.0
Y_MAX = 8900.0
sz_pix = (w,h)
sz_geo = (float(sz_pix[0]) * k_p2g, float(sz_pix[1]) * k_p2g)

center = (4150.154067852198, 8536.915221484507)  #ego position
angle = 0.0  
cx, cy = center[0] - X_MIN, center[1] - Y_MIN
sx, sy = sz_geo
matrix = cv2.getRotationMatrix2D(center, angle, 1)

corners_raw = np.array(
    [[[cx - sx / 2, cy - sy / 2], [cx - sx / 2, cy + sy / 2],
        [cx + sx / 2, cy + sy / 2],
        [cx + sx / 2, cy - sy / 2]]],
    dtype='float32')
p1, p2, p3, p4 = cv2.transform(corners_raw, matrix)[0]
pix_p1 = (0, sz_pix[1]-1)
pix_p2 = (0, 0)
pix_p3 = (sz_pix[0]-1, 0)
pix_p4 = (sz_pix[0]-1, sz_pix[1]-1)
m_g2p = cv2.getAffineTransform(np.array([p1, p2, p3], 'float32'),
                                    np.array([pix_p1, pix_p2, pix_p3],
                                                'float32'))
back = BackGround(canvas, k_p2g)
back.set_pos(m_g2p, [p1, p2, p3, p4])
back.draw()
back.uishow()