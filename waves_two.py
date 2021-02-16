import numpy as np
import pygame as pg
from Experiments.vectors import Vec3


class Projector:
    pi = np.pi
    l = 2000

    def __init__(self):
        pass

    @classmethod
    def matrix_rotate_x(cls, alpha):
        rad = alpha * 3.1415 / 180
        c = np.cos(rad)
        s = np.sin(rad)
        return np.array([[1, 0, 0, 0],
                         [0, c, -s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]])

    @classmethod
    def matrix_rotate_y(cls, betha):
        rad = betha * 3.1415 / 180
        c = np.cos(rad)
        s = np.sin(rad)
        return np.array([[c, 0, s, 0],
                         [0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [0, 0, 0, 1]])

    @classmethod
    def matrix_rotate_z(cls, gamma):
        rad = gamma * 3.1415 / 180
        c = np.cos(rad)
        s = np.sin(rad)
        return np.array([[c, -s, 0, 0],
                         [s, c, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    @classmethod
    def matrix_trans(cls, dx, dy, dz=0):
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [dx, dy, dz, 1]])

    @classmethod
    def matrix_scale(cls, sc):
        return np.array([[sc, 0, 0, 0],
                         [0, sc, 0, 0],
                         [0, 0, sc, 0],
                         [0, 0, 0, 1]])

    @classmethod
    def project(cls, r: Vec3, l):
        x0, y0, z0 = r.get_xyz()
        x = l * x0 / (z0 + l)
        y = l * y0 / (z0 + l)
        return x, y


class Wave:
    def __init__(self, x, y, z, a, w, k, f, t0):
        self.r = Vec3(x, y, z)
        self.a = a
        self.a2 = a ** 2
        self.w = w
        self.k = k
        self.f = f
        self.t0 = t0

    def __str__(self):
        return "wave (" + str(self.r) + ") " + str(self.a) + " " + str(self.w)

    def get_a(self, t, k_betha):
        t1 = t - self.t0
        return (self.a2 / self.a) * np.exp(-k_betha * t1)

    def z(self, r: Vec3, t, k_betha):
        t1 = t - self.t0
        a1 = (self.a2 / (self.a + (r - self.r).len())) * np.exp(-k_betha * t1)  # koef_betha - koef zatuhanya
        rad = (r - self.r).len()
        z = a1 * np.sin(self.w * t1 - self.k * rad + self.f)
        return z


def draw():
    draw_dots = []
    for vector in data_dots:
        new_z = 0
        for wave in waves:
            new_z += wave.z(vector, time, koef_betha)
            if wave.get_a(time, koef_betha) < eps:
                waves.remove(wave)
        vector.set_xyz(vector.get_xyz()[0], vector.get_xyz()[1], new_z)
        draw_dots.append([vector.get_xyz()[0], vector.get_xyz()[1], vector.get_xyz()[2], 1])

    draw_dots = np.dot(draw_dots, Projector.matrix_trans(-0.5, 0.5, 0))
    draw_dots = np.dot(np.dot(np.dot(draw_dots, Projector.matrix_rotate_z(gamma)), Projector.matrix_rotate_y(betha)),
                       Projector.matrix_rotate_x(alpha))
    draw_dots = np.dot(np.dot(draw_dots, Projector.matrix_scale(sc)), Projector.matrix_trans(x0, y0, z0))
    ord_dots = order(draw_dots)

    z_min = min(ord_dots[:][2])
    z_max = max(ord_dots[:][2])
    for dot in ord_dots:
        dot_color = color(dot[2], z_min, z_max)
        if dot_color > 10:
            l = Projector.l
            x = int(round(l * dot[0] / (l + dot[2])))
            y = int(round(l * dot[1] / (l + dot[2])))
            pg.draw.circle(screen, [dot_color, dot_color, dot_color], [x, y], dot_radius)


def color(dot_z, z_min, z_max):
    color_max = 255  # white
    color_min = 0  # dark gray
    k = (color_max - color_min) / (z_min - z_max)
    new_color = k * dot_z + color_max
    if new_color > 255:
        new_color = 255
    return int(round(new_color))


def order(draw_dots):
    draw_ord = []
    for vector in draw_dots:
        draw_ord.append(vector[2] * -1)
    draw_ord = np.array(draw_ord)
    draw_ord = draw_ord.argsort()
    return np.take(draw_dots, draw_ord, 0)


def new_wave(t0):
    a = np.random.randint(10, 100) / 1000
    ld = 0.15
    k = 2 * 3.1415 / ld
    w = 2 * 3.1415 *5
    x, y = np.random.randint(0, 1000) / 1000, np.random.randint(0, 1000) / 1000
    wave1 = Wave(x, -y, 0, a, w, k, 0, t0)
    waves.append(wave1)


g = 1
n = 30
m = n
data_dots = []
for x in range(n):
    for y in range(m):
        for z in range(g):
            xr, yr, zr = 1 / n * x, 1 / m * y, 1 / g * z
            data_dots.append(Vec3(xr, -yr, zr))

data_dots = np.array(data_dots)
dot_radius = 3
alpha, betha, gamma = 80, 0, 0
sc = 500
color_max = 255  # white
color_min = 20  # dark gray
color_bkg = [color_min, color_min, color_min]

ww = 1200
wh = ww // 16 * 9
fps = 60
time = 0
x0, y0, z0 = ww // 2, wh // 2, 0
screen = pg.display.set_mode((ww, wh))
pg.display.set_caption("waves")
key_press = []
used_keys = [
    pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT,
    pg.K_EQUALS, pg.K_MINUS]

waves = []
koef_betha = 1.2
eps = 0.001

pg.init()

clock = pg.time.Clock()
NEW_WAVE = pg.USEREVENT + 1
pg.time.set_timer(NEW_WAVE, 5000)

run = True
while run:
    dt = clock.tick(fps) / 1000
    time += dt
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            key_press.append(event.key)
        if event.type == pg.KEYUP:
            if event.key in key_press:
                key_press.remove(event.key)
            else:
                pass
        if NEW_WAVE:
            new_wave(time)
    for key in key_press:
        if key == pg.K_UP:
            alpha += 1
            if alpha == 360: alpha = 0
        if key == pg.K_DOWN:
            alpha -= 1
            if alpha == 0: alpha = 360
        if key == pg.K_RIGHT:
            betha += 1
            if betha == 360: betha = 0
        if key == pg.K_LEFT:
            betha -= 1
            if betha == 0: betha = 360
        if key == pg.K_0:
            gamma += 1
            if gamma == 360: gamma = 0
        if key == pg.K_9:
            gamma -= 1
            if gamma == 0: gamma = 360
        if key == pg.K_EQUALS:
            sc += 10
        if key == pg.K_MINUS:
            sc -= 10
        if key == pg.K_SPACE:
            new_wave(time)
            key_press.remove(pg.K_SPACE)
    screen.fill(color_bkg)
    draw()
    pg.display.flip()
pg.quit()
