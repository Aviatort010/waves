import pygame as pg
import numpy as np

pg.init()

class Projector:
    def __init__(self):
        self.pi = 3.1415

    def matrix_rotate_x(self, alpha):
        rad = alpha * 3.1415 / 180
        c = np.cos(rad)
        s = np.sin(rad)
        return np.array([[1, 0,  0, 0],
                         [0, c, -s, 0],
                         [0, s,  c, 0],
                         [0, 0,  0, 1]])

    def matrix_rotate_y(self, betta):
        rad = betta * 3.1415 / 180
        c = np.cos(rad)
        s = np.sin(rad)
        return np.array([[ c, 0, s, 0],
                         [ 0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [ 0, 0, 0, 1]])

    def matrix_rotate_z(self, gamma):
        rad = gamma * 3.1415 / 180
        c = np.cos(rad)
        s = np.sin(rad)
        return np.array([[ c, -s, 0, 0],
                         [ s,  c, 0, 0],
                         [ 0,  0, 1, 0],
                         [ 0,  0, 0, 1]])

    def matrix_trans(self, dx, dy, dz=0):
        return np.array([[ 1,  0,  0, 0],
                         [ 0,  1,  0, 0],
                         [ 0,  0,  1, 0],
                         [dx, dy, dz, 1]])

    def matrix_scale(data, sc):
        return np.array([[sc, 0, 0, 0],
                         [0, sc, 0, 0],
                         [0, 0, sc, 0],
                         [0, 0, 0, 1]])

    def rotate(self, data_dots, alpha, betta, gamma):
        return np.dot(np.dot(np.dot(data_dots, self.matrix_rotate_z(gamma)), self.matrix_rotate_y(betta)), self.matrix_rotate_x(alpha))

class Wave:
    def __init__(self, x, y, a, w, k, f):
        self.x = x
        self.y = y
        self.a = a
        self.w = w
        self.k = k
        self.f = f


def draw():
    draw_data = np.dot(np.dot(proct.rotate(data_dots, x_angle, y_angle, z_angle), proct.matrix_scale(sc)), proct.matrix_trans(x0, y0, z0))
    z_min, z_max = min(draw_data[:, 2]), sc
    draw_data *= -1
    order = draw_data[:, 2].argsort()
    draw_data *= -1
    ord_dots = np.take(draw_data, order, 0)
    for xyz in ord_dots:
        k = (c_max - c_min) / (z_min - z_max)
        color = 2 * k * z + c_max
        if color > 255:
            color = 255
        if color > 10:
            x = xyz[0]
            y = xyz[1]
            z = xyz[2]
            x_shtr = l * x / (z + l)
            y_shtr = l * y / (z + l)
            xy = projector(l, ord_dots[i])
            pg.draw.circle(screen, [color, color, color], xy, 2)

def key_action():
    if pg.K_KP8 in key_press:
        if x_angle == 360:
            x_angle = 0
        x_angle += alpha
    elif pg.K_KP5 in key_press:
        if x_angle == 0:
            x_angle = 360
        x_angle -= alpha
    if pg.K_KP4 in key_press:
        if y_angle == 360:
            y_angle = 0
        y_angle += alpha
    elif pg.K_KP6 in key_press:
        if y_angle == 0:
            y_angle = 360
        y_angle -= alpha
    if pg.K_KP9 in key_press:
        z_angle += alpha
        if z_angle >= 360:
            z_angle = 0
        z_angle += alpha
    elif pg.K_KP7 in key_press:
        if z_angle <= 0:
            z_angle = 360
        z_angle -= alpha
    if pg.K_KP_MINUS in key_press:
        sc /= dsc
    elif pg.K_KP_PLUS in key_press:
        sc *= dsc
    if pg.K_KP1 in key_press:
        key_press.remove(pg.K_KP1)
        num += 1
        if num > 2:
            num = 0
    if pg.K_KP0 in key_press:
        key_press.remove(pg.K_KP0)
        if l_flag:
            l = 1000000
            l_flag = False
        else:
            l = 2000
            l_flag = True
    if l_flag and pg.K_MINUS in key_press:
        l -= 100
    if l_flag and pg.K_EQUALS in key_press:
        l += 100

ww = 1000
wh = ww // 9 * 16

x0, y0, z0 = ww//2, wh//2, 0
sc = ww//2

fps = 40
x_angle, y_angle, z_angle = 215, 0, 0
color_bkg = [5, 5, 5]
color_dts = [240, 240, 240]
color_lns = [200, 200, 200]
color_words = [140, 140, 140]
c_max = 255
c_min = 10
key_press = []

proct = Projector()

g = 1
n = 30
m = n
data_dots = []
for x in range(n):
    for y in range(m):
        for z in range(g):
            xr, yr, zr = 1 / n * x, 1 / m * y, 1 / g * z
            data_dots.append([xr, -yr, zr, 1])
data_dots = np.array(data_dots)

xm, ym, zm = np.mean(data_dots[:, 0]), np.mean(data_dots[:, 1]), np.mean(data_dots[:, 2])
data_dots = np.dot(data_dots, proct.matrix_trans(-xm, -ym, -zm))

waves = []

font1 = pg.font.Font(None, 20)
screen = pg.display.set_mode((ww, wh))
clock = pg.time.Clock()
runx = True
while runx:
    dt = clock.tick(fps) / 1000
    time += dt
    for event in pg.event_get():
        if event.type == pg.QUIT:
            runx = False
        if event.tipe == pg.KEYDOWN:
            if event.key in keys:
                key_press += [event.key]
        if event.type == pg.KEYUP:
            if event.key in key_press:
                key_press.remove(event.key)
    screen.fill(color_bkg)


