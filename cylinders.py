#!/usr/bin/env python
"""
each thing is a tuple of materials, geometry, where:
    materials is a dict of:
        name: (r, g, b, glossiness)
        where name is a string,
        r, g, b are between 0 and 1,
        glossiness is between 0 and 1 (0 is matte)
    geometry is a list of:
        (start radius, end radius, height, material)
        in millimetres
"""
THINGS = {
    'Hockey Puck': ({
        'rubber': (0.15, 0.15, 0.15, 0)
    }, [(38.1, 38.1, 25.4, 'rubber')]),
    'Ouster OS1': ({
        'body': (0.88, 0.88, 0.88, 0.3),
        'window': (0.1, 0.1, 0.1, 0.9)
    }, [
        (38, 38, 18, 'body'),
        (38, 35, 3, 'body'),
        (35, 35, 31, 'window'),
        (35, 40, 14, 'body'),
        (40, 40, 6, 'body'),
    ]),
    'Velodyne VLP-16': ({
        'body': (0.8, 0.8, 0.83, 0.1),
        'window': (0.1, 0.5, 0, 0.9)
    }, [
        (49.5, 50, 14.8, 'body'),
        (49.5, 51, 38.1, 'window'),
        (51.5, 51.65, 18.8, 'body'),
    ]),
    'Velodyne VLP-32C': ({
        'body': (0.8, 0.8, 0.83, 0.1),
        'window': (0.1, 0.5, 0, 0.9)
    }, [
        (50, 50, 27.4, 'body'),
        (49.5, 51, 44.5, 'window'),
        (51.5, 51.65, 15.0, 'body'),
    ]),
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
    ]),
    'Surestar RFans-32': ({
        'body': (0.7, 0.7, 0.75, 0.0),
        'window': (0.85, 0.87, 0.8, 0.95)
    }, [
        (56.5, 56.5, 10, 'body'),
        (56.5, 56.5, 44, 'window'),
        (56.5, 56.5, 16, 'body'),
    ]),
    'Ouster OS2': ({
        'body': (0.88, 0.88, 0.88, 0.3),
        'window': (0.1, 0.1, 0.1, 0.9)
    }, [
        (46, 46, 6, 'body'),
        (46, 49, 66, 'window'),
        (50, 55, 20, 'body'),
        (55, 55, 8, 'body'),
    ]),
    'Robosense RS-LiDAR-32B': ({
        'body': (0.4, 0.4, 0.4, 0.0),
        'window': (0, 0.2, 0.6, 0.95)
    }, [
        (57, 57, 33, 'body'),
        (56, 55, 65, 'window'),
        (56, 56, 20, 'body'),
    ]),
    'Hesai Pandar64': ({
        'body': (0.8, 0.83, 0.8, 0.7),
        'window': (0, 0.2, 0.6, 0.95)
    }, [
        (54, 58, 4, 'body'),
        (58, 58, 30, 'body'),
        (57.5, 57, 62, 'window'),
        (57.5, 57.5, 20, 'body'),
    ]),
    'Velodyne VLS-128': ({
        'body': (0.9, 0.9, 0.9, 0.1),
        'window': (0.0, 0.0, 0.4, 0.95)
    }, [
        (30, 60, 3.3, 'body'),
        (60, 71, 2.3, 'body'),
        (71, 74, 2, 'body'),
        (74, 76, 2, 'body'),
        (76, 78, 4, 'body'),
        (78, 80.5, 7, 'body'),
        (80.5, 81, 21, 'body'),
        (79, 81, 67.0, 'window'),
        (82, 82.5, 33.0, 'body'),
    ]),
}

PATH = '<path d="{d}" style="fill:url(#{material})" transform="{transform}"/>'
GROUP = '<g transform="{transform}">{group}</g>'
GRADIENT = """\
<linearGradient id="{id}" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" style="stop-color:rgb{c0};stop-opacity:1" />
    <stop offset="{s1}%" style="stop-color:rgb{c1};stop-opacity:1" />
    <stop offset="{s2}%" style="stop-color:rgb{c2};stop-opacity:1" />
    <stop offset="{s3}%" style="stop-color:rgb{c3};stop-opacity:1" />
    <stop offset="{s4}%" style="stop-color:rgb{c4};stop-opacity:1" />
    <stop offset="{s5}%" style="stop-color:rgb{c5};stop-opacity:1" />
    <stop offset="100%" style="stop-color:rgb{c6};stop-opacity:1" />
</linearGradient>\
"""
SVG = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{width}px" height="{height}px">{svg}</svg>'
TEXT = '<text x="{x}" y="{y}" style="font: {size}px sans-serif;">{text}</text>'


def render_materials(materials, key):
    def rgb(colour, mult, add=0):
        return tuple(min(255, 255 * (c * mult + add)) for c in colour[0:3])

    material_svg = '<defs>{}</defs>'.format(''.join(
        GRADIENT.format(id=k + key,
                        c0=rgb(v, 0.3 - 0.2 * v[3]),
                        c1=rgb(v, 0.7),
                        c2=rgb(v, 1.0, 0.2 * v[3]),
                        c3=rgb(v, 1.2, 0.25 * v[3]),
                        c4=rgb(v, 1.1, 0.2 * v[3]),
                        c5=rgb(v, 0.8),
                        c6=rgb(v, 0.6 - 0.2 * v[3]),
                        s1=52 - 10 * (1 - v[3]),
                        s2=52 + 10 * (1 - v[3]),
                        s3=70,
                        s4=88 - 10 * (1 - v[3]),
                        s5=88 + 10 * (1 - v[3]))
        for k, v in materials.items()))
    return material_svg


def render_revolve(materials, geometry, angle):
    if angle == 0:
        return render_flat(materials, geometry)
    return

    v_offset = 0
    h_offset = max(max(r1, r2) for r1, r2, _, _ in geometry)
    svg = render_materials(materials)
    for x1, x2, h, mat in geometry[::-1]:
        svg += PATH.format(
            d='A{x1},{y1},0,0,{l1}, L-{x1},{y1} L-{x2},{y2} L{x2},{y2} L{x1},{y1}'
            .format(x1=x1, x2=x2, y1=v_offset, y2=v_offset + h),
            transform='translate({}, 0)'.format(h_offset),
            material=mat)
        v_offset += h
    return svg, v_offset, 2 * h_offset


def render_flat(materials, geometry):
    key = str(hash('{}'.format(geometry)))
    v_offset = 0
    h_offset = max(max(r1, r2) for r1, r2, _, _ in geometry)
    svg = render_materials(materials, key)
    for x1, x2, h, mat in geometry:
        svg += PATH.format(
            d='M{x1},{y1} L-{x1},{y1} L-{x2},{y2} L{x2},{y2} L{x1},{y1}'.
            format(x1=x1, x2=x2, y1=v_offset - 0.5, y2=v_offset + h),
            transform='translate({}, 0)'.format(h_offset),
            material=mat + key)
        v_offset += h
    return svg, v_offset, 2 * h_offset


def render_all(things, renderer, padding=20, textsize=10):
    renders = {k: renderer(*thing) for k, thing in things.items()}

    total_height = 2 * padding + max(v[1] for _, v in renders.items())
    h_offset = padding

    svg = ''
    for k, v in renders.items():
        render, height, width = v
        svg += GROUP.format(transform='translate({x},{y})'.format(
            x=h_offset, y=total_height - height - padding),
                            group=render)
        svg += TEXT.format(x=h_offset, y=total_height, text=k, size=textsize)
        h_offset += width + padding

    print(
        SVG.format(svg=svg,
                   height=total_height + padding + textsize,
                   width=h_offset))


def main():
    render_all(THINGS, render_flat)


main()
