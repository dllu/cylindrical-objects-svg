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
hockey_puck = ({
    'rubber': (0.15, 0.15, 0.15, 0)
}, [(38.1, 38.1, 25.4, 'rubber')])

vlp16 = ({
    'body': (0.8, 0.8, 0.8, 0.1),
    'window': (0.1, 0.5, 0, 0.9)
}, [
    (49.5, 50, 14.8, 'body'),
    (49.5, 51, 38.1, 'window'),
    (51.5, 51.65, 18.8, 'body'),
])

vlp32 = ({
    'body': (0.8, 0.8, 0.8, 0.1),
    'window': (0.1, 0.5, 0, 0.9)
}, [
    (50, 50, 27.4, 'body'),
    (49.5, 51, 44.5, 'window'),
    (51.5, 51.65, 15.0, 'body'),
])

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


def render_materials(materials):
    def rgb(colour, mult):
        return tuple(min(255, 255 * c * mult) for c in colour[0:3])

    material_svg = '<defs>{}</defs>'.format(''.join(
        GRADIENT.format(id=k,
                        c0=rgb(v, 0.3),
                        c1=rgb(v, 0.7),
                        c2=rgb(v, 1.0),
                        c3=rgb(v, 1.2),
                        c4=rgb(v, 1.1),
                        c5=rgb(v, 0.8),
                        c6=rgb(v, 0.6),
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


def render_flat(materials, geometry):
    v_offset = 0
    h_offset = max(max(r1, r2) for r1, r2, _, _ in geometry)
    svg = render_materials(materials)
    for x1, x2, h, mat in geometry:
        svg += PATH.format(
            d='M{x1},{y1} L-{x1},{y1} L-{x2},{y2} L{x2},{y2} L{x1},{y1}'.
            format(x1=x1, x2=x2, y1=v_offset, y2=v_offset + h),
            transform='translate({}, 0)'.format(h_offset),
            material=mat)
        v_offset += h
    return svg, v_offset, 2 * h_offset


def render_all(things, renderer, padding=10):
    renders = [renderer(*thing) for thing in things]

    total_height = 2 * padding + max(height for _, height, _ in renders)
    h_offset = padding

    svg = ''
    for render, height, width in renders:
        svg += GROUP.format(transform='translate({x},{y})'.format(
            x=h_offset, y=total_height - height - padding),
                            group=render)
        h_offset += width + padding

    print(SVG.format(svg=svg, height=total_height, width=h_offset))


def main():
    render_all([hockey_puck, vlp16, vlp32], render_flat)


main()
