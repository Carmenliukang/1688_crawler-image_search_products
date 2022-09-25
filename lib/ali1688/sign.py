#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ctypes
import struct


def struct_format(num):
    if num > 0:
        res = struct.unpack("i", struct.pack("I", num))
        return res[0] if res else 0
    else:
        return num


def left_shift(x, y):
    x, y = ctypes.c_int32(x).value, y % 32
    return ctypes.c_int32(x << y).value


def right_shift(x, y):
    x, y = ctypes.c_int32(x).value, y % 32
    return ctypes.c_int32(x >> y).value


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shitf(n, i):
    # unsigned right shift
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


class Sign(object):
    # 1688 upload image sign upload
    def __init__(self):
        pass

    def b(self, a, b):
        return struct_format(left_shift(a, b) | unsigned_right_shitf(a, 32 - b))

    def c(self, a, b):
        e = struct_format(2147483648 & a)
        f = struct_format(2147483648 & b)
        c = struct_format(1073741824 & a)
        d = struct_format(1073741824 & b)
        g = struct_format(1073741823 & a) + struct_format(1073741823 & b)
        if struct_format(c & d):
            h = struct_format(struct_format(struct_format(2147483648 ^ g) ^ e) ^ f)
        else:
            if struct_format(c | d):
                if 1073741824 & g & (2**32 - 1):
                    h = struct_format(
                        struct_format(struct_format(3221225472 ^ g) ^ e) ^ f
                    )
                else:
                    h = struct_format(
                        struct_format(struct_format(1073741824 ^ g) ^ e) ^ f
                    )
            else:
                h = struct_format(struct_format(g ^ e) ^ f)
        return h

    def d(self, a, b, c):
        return a & b | ~a & c

    def e(self, a, b, c):
        return a & c | b & ~c

    def f(self, a, b, c):
        return a ^ b ^ c

    def g(self, a, b, c):
        return b ^ (a | ~c)

    def h(self, a, e, f, g, h, i, j):
        a = self.c(a, self.c(self.c(self.d(e, f, g), h), j))
        res = self.c(self.b(a, i), e)
        return res

    def i(self, a, d, f, g, h, i, j):
        a = self.c(a, self.c(self.c(self.e(d, f, g), h), j))
        res = self.c(self.b(a, i), d)
        return res

    def j(self, a, d, e, g, h, i, j):
        a = self.c(a, self.c(self.c(self.f(d, e, g), h), j))
        res = self.c(self.b(a, i), d)
        return res

    def k(self, a, d, e, f, h, i, j):
        a = self.c(a, self.c(self.c(self.g(d, e, f), h), j))
        res = self.c(self.b(a, i), d)
        return res

    def l(self, a):
        c = len(a)
        d = c + 8
        e = int(round((d - d % 64) / 64))
        f = 16 * (e + 1)
        g = [0 for i in range(f)]
        i = 0
        while i < c:
            b = int(round((i - i % 4) / 4))
            h = i % 4 * 8
            g[b] = g[b] | left_shift(ord(a[i]), h)
            i += 1

        b = int(round((i - i % 4) / 4))
        h = i % 4 * 8
        g[b] = g[b] | left_shift(128, h)
        g[f - 2] = left_shift(c, 3)
        g[f - 1] = unsigned_right_shitf(c, 29)
        return g

    def m(self, a):
        d = ""
        for c in range(4):
            b = unsigned_right_shitf(a, 8 * c) & 255
            e = "0" + hex(b)
            d += e[-2:]
        # return d
        return d.replace("x", "0")

    def n(self, a):
        a = a.replace(r"/\r\n/g", "\n")
        b = ""
        for c in a:
            d = ord(c)
            if 128 > d:
                b += chr(d)
            else:
                if d > 127 and 2048 > d:
                    b += chr(right_shift(d, 6) | 192)
                    b += chr(63 & d | 128)
                else:
                    b += chr(right_shift(d, 12) | 224)
                    b += chr(right_shift(d, 6) & 63 | 128)
                    b += chr(63 & d | 128)
        return b

    def sign(self, a):
        o = p = q = r = s = t = u = v = w = ""
        x = []
        y = 7
        z = 12
        A = 17
        B = 22
        C = 5
        D = 9
        E = 14
        F = 20
        G = 4
        H = 11
        I = 16
        J = 23
        K = 6
        L = 10
        M = 15
        N = 21
        a = self.n(a)
        x = self.l(a)
        t = 1732584193
        u = 4023233417
        v = 2562383102
        w = 271733878
        o = 0

        while o < len(x):
            p = t
            q = u
            r = v
            s = w
            t = self.h(t, u, v, w, x[o + 0], y, 3614090360)
            w = self.h(w, t, u, v, x[o + 1], z, 3905402710)
            v = self.h(v, w, t, u, x[o + 2], A, 606105819)
            u = self.h(u, v, w, t, x[o + 3], B, 3250441966)
            t = self.h(t, u, v, w, x[o + 4], y, 4118548399)
            w = self.h(w, t, u, v, x[o + 5], z, 1200080426)
            v = self.h(v, w, t, u, x[o + 6], A, 2821735955)
            u = self.h(u, v, w, t, x[o + 7], B, 4249261313)
            t = self.h(t, u, v, w, x[o + 8], y, 1770035416)
            w = self.h(w, t, u, v, x[o + 9], z, 2336552879)
            v = self.h(v, w, t, u, x[o + 10], A, 4294925233)
            u = self.h(u, v, w, t, x[o + 11], B, 2304563134)
            t = self.h(t, u, v, w, x[o + 12], y, 1804603682)
            w = self.h(w, t, u, v, x[o + 13], z, 4254626195)
            v = self.h(v, w, t, u, x[o + 14], A, 2792965006)
            u = self.h(u, v, w, t, x[o + 15], B, 1236535329)
            t = self.i(t, u, v, w, x[o + 1], C, 4129170786)
            w = self.i(w, t, u, v, x[o + 6], D, 3225465664)
            v = self.i(v, w, t, u, x[o + 11], E, 643717713)
            u = self.i(u, v, w, t, x[o + 0], F, 3921069994)
            t = self.i(t, u, v, w, x[o + 5], C, 3593408605)
            w = self.i(w, t, u, v, x[o + 10], D, 38016083)
            v = self.i(v, w, t, u, x[o + 15], E, 3634488961)
            u = self.i(u, v, w, t, x[o + 4], F, 3889429448)
            t = self.i(t, u, v, w, x[o + 9], C, 568446438)
            w = self.i(w, t, u, v, x[o + 14], D, 3275163606)
            v = self.i(v, w, t, u, x[o + 3], E, 4107603335)
            u = self.i(u, v, w, t, x[o + 8], F, 1163531501)
            t = self.i(t, u, v, w, x[o + 13], C, 2850285829)
            w = self.i(w, t, u, v, x[o + 2], D, 4243563512)
            v = self.i(v, w, t, u, x[o + 7], E, 1735328473)
            u = self.i(u, v, w, t, x[o + 12], F, 2368359562)
            t = self.j(t, u, v, w, x[o + 5], G, 4294588738)
            w = self.j(w, t, u, v, x[o + 8], H, 2272392833)
            v = self.j(v, w, t, u, x[o + 11], I, 1839030562)
            u = self.j(u, v, w, t, x[o + 14], J, 4259657740)
            t = self.j(t, u, v, w, x[o + 1], G, 2763975236)
            w = self.j(w, t, u, v, x[o + 4], H, 1272893353)
            v = self.j(v, w, t, u, x[o + 7], I, 4139469664)
            u = self.j(u, v, w, t, x[o + 10], J, 3200236656)
            t = self.j(t, u, v, w, x[o + 13], G, 681279174)
            w = self.j(w, t, u, v, x[o + 0], H, 3936430074)
            v = self.j(v, w, t, u, x[o + 3], I, 3572445317)
            u = self.j(u, v, w, t, x[o + 6], J, 76029189)
            t = self.j(t, u, v, w, x[o + 9], G, 3654602809)
            w = self.j(w, t, u, v, x[o + 12], H, 3873151461)
            v = self.j(v, w, t, u, x[o + 15], I, 530742520)
            u = self.j(u, v, w, t, x[o + 2], J, 3299628645)
            t = self.k(t, u, v, w, x[o + 0], K, 4096336452)
            w = self.k(w, t, u, v, x[o + 7], L, 1126891415)
            v = self.k(v, w, t, u, x[o + 14], M, 2878612391)
            u = self.k(u, v, w, t, x[o + 5], N, 4237533241)
            t = self.k(t, u, v, w, x[o + 12], K, 1700485571)
            w = self.k(w, t, u, v, x[o + 3], L, 2399980690)
            v = self.k(v, w, t, u, x[o + 10], M, 4293915773)
            u = self.k(u, v, w, t, x[o + 1], N, 2240044497)
            t = self.k(t, u, v, w, x[o + 8], K, 1873313359)
            w = self.k(w, t, u, v, x[o + 15], L, 4264355552)
            v = self.k(v, w, t, u, x[o + 6], M, 2734768916)
            u = self.k(u, v, w, t, x[o + 13], N, 1309151649)
            t = self.k(t, u, v, w, x[o + 4], K, 4149444226)
            w = self.k(w, t, u, v, x[o + 11], L, 3174756917)
            v = self.k(v, w, t, u, x[o + 2], M, 718787259)
            u = self.k(u, v, w, t, x[o + 9], N, 3951481745)
            t = self.c(t, p)
            u = self.c(u, q)
            v = self.c(v, r)
            w = self.c(w, s)
            o += 16
        O = self.m(t) + self.m(u) + self.m(v) + self.m(w)
        return O.lower()
