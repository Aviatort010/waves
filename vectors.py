import pygame as pg
import numpy as np

zero = 0.000001
def ir(x):
    return int(round(x))

class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __pos__(self):
        return Vec2(self.x, self.y)

    def __str__(self):
        return "V2 " + str(self.x) + " " + str(self.y) + " " + str(self.len())

    def __rmul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)

    def get_xy(self):
        return self.x, self.y

    def len(self):
        return np.hypot(self.x, self.y)

    def get_ang(self):
        return np.arctan2(self.y, self.x)

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def set_len(self, len):
        l = self.len()
        self.x = len * self.x / l
        self.y = len * self.y / l

    def set_ang(self, alpha):
        l = self.len()
        self.x = l * np.cos(alpha)
        self.y = l * np.sin(alpha)

    def e(self):
        l = self.len()
        if l == 0: l = zero
        return Vec2(self.x / l, self.y / l)

    def draw(self, xy0, scale=1, color=[200, 200, 200], arrow=True):
        xy1 = (xy0[0] + self.x * scale, xy0[1] + self.y * scale)
        pg.draw.line(screen, color, (ir(xy0[0]), ir(wh - xy0[1])), (ir(xy1[0]), ir(wh - xy1[1])), 2)
        if arrow:
            betta = np.pi / 4
            alpha = self.get_ang()
            r = np.sqrt(self.x ** 2 + self.y ** 2) / 5
            v1 = Vec2(-self.x, -self.y)
            v1.set_len(r)
            v1.set_ang(np.pi + alpha + betta)
            v1.draw((xy1[0], xy1[1]), 1, color, False)
            v2 = Vec2(-self.x, -self.y)
            v2.set_len(r)
            v2.set_ang(np.pi + alpha - betta)
            v2.draw((xy1[0], xy1[1]), 1, color, False)

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):     # умножение вектора на вектора
            return self.x * other.x + self.y * other.y + self.z * other.z
        elif isinstance(other, (int, float)):   # число на вектор
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __pos__(self):
        return Vec3(self.x, self.y, self.z)

    def __str__(self):
        return "V3 " + str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + str(self.len())

    def __rmul__(self, other):
        if isinstance(other, Vec3):     # vevtor * vec
            return self.x * other.x + self.y * other.y + self.z * other.z
        elif isinstance(other, (int, float)):   # vec * num
            return Vec3(self.x * other, self.y * other, self.z * other)

    def get_xy(self):
        return self.x, self.y

    def get_xyz(self):
        return self.x, self.y, self.z

    def len(self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def get_ang_xy(self):
        return np.arctan2(self.y, self.x)

    def get_ang(self):  # для "правой" тройки векторов
        etta = np.arccos(self.z / self.len())
        fi = self.get_ang_xy()
        return etta, fi

    def set_xyz(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_len(self, len):
        l = self.len()
        self.x = len * self.x / l
        self.y = len * self.y / l
        self.z = len * self.z / l

    def set_ang(self, etta, fi):
        l = self.len()
        s_etta = np.sin(etta)
        self.x = l * s_etta * np.cos(fi)
        self.y = l * s_etta * np.sin(fi)
        self.z = l * np.cos(etta)

    def e(self):
        l = self.len()
        if l == 0: l = zero
        return Vec3(self.x / l, self.y / l, self.z / l)

