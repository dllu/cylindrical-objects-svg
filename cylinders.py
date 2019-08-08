#!/usr/bin/env python
import math
"""
each thing is a tuple of materials, geometry, weight where:
    materials is a dict of:
        name: (r, g, b, glossiness)
        where name is a string,
        r, g, b are between 0 and 1,
        glossiness is between 0 and 1 (0 is matte)
    geometry is a list of:
        (start radius, end radius, height, material)
        in millimetres
    weight is in grams
"""
THINGS = {
    'Hockey Puck': ({
        'rubber': (0.15, 0.15, 0.15, 0)
    }, [(38.1, 38.1, 25.4, 'rubber')], 170),
    'Coca-Cola': ({
        'aluminium': (0.88, 0.88, 0.88, 0.5),
        'body': (1, 0, 0, 0.8),
    }, [
        (30.5, 31.0, 0.5, 'aluminium'),
        (31.0, 31.0, 1, 'body'),
        (31.0, 33.2, 10, 'body'),
        (33.2, 33.2, 95, 'body'),
        (33.2, 32, 4, 'body'),
        (32, 31, 3, 'aluminium'),
        (31, 30, 2, 'aluminium'),
    ], 330),
    'Ouster OS1': ({
        'body': (0.88, 0.88, 0.88, 0.3),
        'window': (0.1, 0.1, 0.1, 0.9)
    }, [
        (38, 38, 18, 'body'),
        (38, 35, 3, 'body'),
        (35, 35, 31, 'window'),
        (35, 40, 14, 'body'),
        (40, 40, 6, 'body'),
    ], 396),
    'Velodyne VLP-16': ({
        'body': (0.8, 0.8, 0.83, 0.1),
        'window': (0.1, 0.5, 0, 0.9)
    }, [
        (49.5, 50, 14.8, 'body'),
        (49.5, 51, 38.1, 'window'),
        (51.5, 51.65, 18.8, 'body'),
    ], 830),
    'Velodyne VLP-32C': ({
        'body': (0.8, 0.8, 0.83, 0.1),
        'window': (0.1, 0.5, 0, 0.9)
    }, [
        (50, 50, 27.4, 'body'),
        (49.5, 51, 44.5, 'window'),
        (51.5, 51.65, 15.0, 'body'),
    ], 925),
    'Quanergy M8': ({
        'body': (0.1, 0.1, 0.1, 0.7),
        'window': (0.1, 0.1, 0.1, 0.95),
        'base': (0.2, 0.2, 0.2, 0.3),
    }, [
        (43, 45, 2, 'window'),
        (45, 47, 67, 'window'),
        (48, 50, 1, 'body'),
        (50, 51, 1, 'body'),
        (51, 51, 10, 'body'),
        (51.5, 51.5, 8, 'base'),
    ], 900),
    'SureStar RFans-32': ({
        'body': (0.7, 0.7, 0.75, 0.0),
        'window': (0.85, 0.87, 0.8, 0.95)
    }, [
        (56.5, 56.5, 10, 'body'),
        (56.5, 56.5, 44, 'window'),
        (56.5, 56.5, 16, 'body'),
    ], 738),
    'Ouster OS2': ({
        'body': (0.88, 0.88, 0.88, 0.3),
        'window': (0.1, 0.1, 0.1, 0.9)
    }, [
        (46, 46, 6, 'body'),
        (46, 49, 66, 'window'),
        (50, 55, 20, 'body'),
        (55, 55, 8, 'body'),
    ], 600),
    'Robosense RS-LiDAR-16': ({
        'body': (0.4, 0.4, 0.4, 0.0),
        'window': (0, 0.2, 0.6, 0.95)
    }, [
        (54.5, 54.5, 16, 'body'),
        (54, 54, 4, 'body'),
        (53.5, 54, 45, 'window'),
        (54, 54, 3, 'body'),
        (54.5, 54.5, 12, 'body'),
    ], 840),
    'Robosense RS-LiDAR-32B': ({
        'body': (0.4, 0.4, 0.4, 0.0),
        'window': (0, 0.2, 0.6, 0.95)
    }, [
        (57, 57, 33, 'body'),
        (56, 55, 65, 'window'),
        (56, 56, 20, 'body'),
    ], 1130),
    'Hesai Pandar64': ({
        'body': (0.8, 0.83, 0.8, 0.7),
        'window': (0, 0.2, 0.6, 0.95)
    }, [
        (54, 58, 4, 'body'),
        (58, 58, 30, 'body'),
        (57.5, 57, 62, 'window'),
        (57.5, 57.5, 20, 'body'),
    ], 1520),
    'Velodyne VLS-128': ({
        'body': (0.9, 0.9, 0.9, 0.1),
        'window': (0.0, 0.0, 0.4, 0.95)
    }, [
        (0, 30, 0.01, 'body'),
        (30, 60, 3.3, 'body'),
        (60, 71, 2.3, 'body'),
        (71, 74, 2, 'body'),
        (74, 76, 2, 'body'),
        (76, 78, 4, 'body'),
        (78, 80.5, 7, 'body'),
        (80.5, 81, 21, 'body'),
        (79, 81, 67.0, 'window'),
        (82, 82.5, 33.0, 'body'),
    ], 3530),
}

PATH = '<path d="{d}" style="fill:url(#{material})" transform="{transform}"/>'
ELLIPSE = '<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" style="fill:url(#{material})" transform="{transform}"/>'
GROUP = '<g transform="{transform}">{group}</g>'
SOLIDCOLOR = """\
<linearGradient id="{id}-solid" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" style="stop-color:rgb{c0}"/>
</linearGradient>\
"""

GRADIENT = """\
<linearGradient id="{id}" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" style="stop-color:rgb{c0}"/>
<stop offset="{s1:.1f}%" style="stop-color:rgb{c1}"/>
<stop offset="{s2:.1f}%" style="stop-color:rgb{c2}"/>
<stop offset="{s3:.1f}%" style="stop-color:rgb{c3}"/>
<stop offset="{s4:.1f}%" style="stop-color:rgb{c4}"/>
<stop offset="{s5:.1f}%" style="stop-color:rgb{c5}"/>
<stop offset="100%" style="stop-color:rgb{c6}"/>
</linearGradient>\
"""
SVG = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{width}px" height="{height}px">{svg}</svg>'
TEXT = '<text x="{x:.1f}" y="{y:.1f}" style="font: {size}px monospace;">{text}</text>'


def rgb(colour, mult, add=0):
    return tuple(min(255, round(255 * (c * mult + add))) for c in colour[0:3])


def render_materials(materials, key, ss=70):
    material_svg = '<defs>{}</defs>'.format(''.join('{}{}'.format(
        GRADIENT.format(id=k + key,
                        c0=rgb(v, 0.3 - 0.2 * v[3]),
                        c1=rgb(v, 0.7),
                        c2=rgb(v, 1.0, 0.2 * v[3]),
                        c3=rgb(v, 1.2, 0.25 * v[3]),
                        c4=rgb(v, 1.1, 0.2 * v[3]),
                        c5=rgb(v, 0.8),
                        c6=rgb(v, 0.6 - 0.2 * v[3]),
                        s1=ss - 18 - 10 * (1 - v[3]),
                        s2=ss - 18 + 10 * (1 - v[3]),
                        s3=ss,
                        s4=ss + 18 - 10 * (1 - v[3]),
                        s5=ss + 18 + 10 * (1 - v[3])),
        SOLIDCOLOR.format(id=k +
                          key, c0=rgb(v, 1))) for k, v in materials.items()))
    return material_svg


def render_revolve(materials, geometry, angle=0.1):
    if angle == 0:
        return render_flat(materials, geometry)
    key = str(hash('{}{}'.format(geometry, angle)))
    svg = render_materials(materials, key, 70 - 30 * angle)
    angle = math.pi / 2 - angle

    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)

    h_offset = max(max(r1, r2) for r1, r2, _, _ in geometry)
    height = v_offset = sum(h * sin_angle
                            for _, _, h, _ in geometry) + h_offset * cos_angle

    last_ellipse = ''
    last_rx1 = -1

    for rx1, rx2, h, mat in geometry[::-1]:
        v_offset -= h * sin_angle
        ry1 = cos_angle * rx1
        ry2 = cos_angle * rx2
        large1 = 0
        if rx1 > rx2:
            large1 = 1
        large2 = 1 - large1

        hypot = h * sin_angle / cos_angle
        if hypot < abs(rx2 - rx1):
            last_ellipse = ELLIPSE.format(cx=0,
                                          cy=0,
                                          rx=rx1,
                                          ry=ry1,
                                          transform='translate({}, {})'.format(
                                              h_offset, v_offset),
                                          material=mat + key + '-solid')
            continue
        sin_theta = (rx2 - rx1) / hypot
        cos_theta = math.sqrt(1 - sin_theta**2)

        x1 = rx1 * cos_theta
        y1 = -rx1 * sin_theta * cos_angle

        x2 = rx2 * cos_theta
        y2 = h * sin_angle + -rx2 * sin_theta * cos_angle

        d = 'M{x1:.1f},{y1:.1f}'.format(x1=x1, y1=y1)
        d += 'A{rx1:.1f},{ry1:.1f},0,{large1},{sweep},{x1:.1f},{y1:.1f}'.format(
            rx1=rx1, ry1=ry1, large1=large1, sweep=0, x1=-x1, y1=y1)
        d += 'L{x2:.1f},{y2:.1f}'.format(x2=-x2, y2=y2)
        d += 'A{rx2:.1f},{ry2:.1f},0,{large2},{sweep},{x2:.1f},{y2:.1f}'.format(
            rx2=rx2, ry2=ry2, large2=large2, sweep=0, x2=x2, y2=y2)
        d += 'Z'

        if last_rx1 != -1 and not rx2 == last_rx1:
            svg += last_ellipse
        svg += PATH.format(d=d,
                           transform='translate({0:.1f}, {1:.1f})'.format(
                               h_offset, v_offset),
                           material=mat + key)
        last_ellipse = ELLIPSE.format(
            cx=0,
            cy=0,
            rx=rx1,
            ry=ry1,
            transform='translate({0:.1f}, {1:.1f})'.format(h_offset, v_offset),
            material=mat + key + '-solid')
        last_rx1 = rx1
    svg += last_ellipse
    return svg, height + h_offset * cos_angle, 2 * h_offset


def render_flat(materials, geometry):
    key = str(hash('{}'.format(geometry)))
    v_offset = 0
    h_offset = max(max(r1, r2) for r1, r2, _, _ in geometry)
    svg = render_materials(materials, key)
    for x1, x2, h, mat in geometry:
        svg += PATH.format(
            d='M{x1:.1f},{y1:.1f} L-{x1:.1f},{y1:.1f} L-{x2:.1f},{y2:.1f} L{x2:.1f},{y2:.1f} Z'
            .format(x1=x1, x2=x2, y1=v_offset - 0.5, y2=v_offset + h),
            transform='translate({0:.1f}, 0)'.format(h_offset),
            material=mat + key)
        v_offset += h
    return svg, v_offset, 2 * h_offset


def render_all(things, renderer, padding=30, textsize=8):
    renders = {
        k: (renderer(*thing[0:2]), thing[2])
        for k, thing in things.items()
    }

    total_height = 2 * padding + max(v[0][1] for _, v in renders.items())
    h_offset = padding

    svg = ''
    for k, v in renders.items():
        render, height, width = v[0]
        svg += GROUP.format(transform='translate({x:.1f},{y:.1f})'.format(
            x=h_offset, y=total_height - height - padding),
                            group=render)
        svg += TEXT.format(x=h_offset, y=total_height, text=k, size=textsize)
        svg += TEXT.format(x=h_offset,
                           y=total_height + textsize,
                           text='{} g'.format(v[1]),
                           size=textsize)
        h_offset += width + padding

    return svg, total_height + padding + 2 * textsize, h_offset


def main():
    all_svg = []
    all_height = []
    for a in range(0, 150, 5):
        angle = a / 100
        svg, height, width = render_all(
            THINGS, lambda x, y: render_revolve(x, y, angle))
        all_svg.append(svg)
        all_height.append(height)
    each_height = math.ceil(max(all_height))

    svg = ''
    v_offset = 0
    for s, h in zip(all_svg, all_height):
        svg += GROUP.format(
            transform='translate(0,{y})'.format(y=v_offset + each_height - h),
            group=s)
        v_offset += each_height

    print(SVG.format(svg=svg, height=each_height * len(all_svg), width=width))


main()
