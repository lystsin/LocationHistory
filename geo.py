# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:12:39 2018

@author: lystsin

参考URL:https://qiita.com/damyarou/items/9cb633e844c78307134a
"""

from math import radians, sin, cos, tan, acos, atan


def cal_phi(ra, rb, lat):
    return atan(rb/ra*tan(lat))


def cal_rho(lat_a, lon_a, lat_b, lon_b):
    try:
        ra = 6378.140  # equatorial radius (km)
        rb = 6356.755  # polar radius (km)
        F = (ra - rb) / ra  # flattening of the earth
        rad_lat_a = radians(lat_a)
        rad_lon_a = radians(lon_a)
        rad_lat_b = radians(lat_b)
        rad_lon_b = radians(lon_b)
        pa = cal_phi(ra, rb, rad_lat_a)
        pb = cal_phi(ra, rb, rad_lat_b)
        xx = acos(sin(pa) * sin(pb) + cos(pa) * cos(pb) * cos(rad_lon_a - rad_lon_b))
        c1 = (sin(xx) - xx) * (sin(pa) + sin(pb)) ** 2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(pa) - sin(pb)) ** 2 / sin(xx / 2) ** 2
        dr = F / 8 * (c1 - c2)
        rho = ra * (xx + dr)
    except ZeroDivisionError:
        rho = 0
    except ValueError:
        rho = 0
    return rho


def main():
    for iii in (0, 1):
        if iii == 0:
            lat_a = 3.117
            lon_a = 101.550
            loc_a = 'Kuala Lumpur'
            lat_b = 35.690
            lon_b = 139.760
            loc_b = 'Tokyo'
        if iii == 1:
            lat_a = 3.117
            lon_a = 101.550
            loc_a = 'Kuala Lumpur'
            lat_b = -6.183
            lon_b = 106.833
            loc_b = 'Jakarta'

        rho = cal_rho(lat_a, lon_a, lat_b, lon_b)
        print('(lat_a, lon_a)=({0:8.3f},{1:8.3f}): {2:16s}'.format(
              lat_a, lon_a, loc_a))
        print('(lat_b, lon_b)=({0:8.3f},{1:8.3f}): {2:16s}'.format(
              lat_b, lon_b, loc_b))
        print('Distance={0:10.3f} km'.format(rho))
        print()


# ==============
# Execution
# ==============
if __name__ == '__main__':
    main()
