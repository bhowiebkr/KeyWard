import cadquery as cq


def switch():

    # Base
    switch_hole = 14
    thickness = 2
    depth = 5

    side_len = switch_hole + (thickness * 2)

    result = (
        cq.Workplane("XY")
        .rect(side_len, side_len)
        .rect(switch_hole, switch_hole)
        .extrude(depth)
    )

    # Corner circles
    half = switch_hole / 2
    c = 1.6 / 2
    circles = cq.Workplane("XY").pushPoints(
        [(half, half), (-half, half), (half, -half), (-half, -half)]
    )
    circles = circles.circle(c).extrude(depth)

    # locking things
    locks = (
        cq.Workplane("XY").rect(6, switch_hole + 2).rect(switch_hole + 2, 6).extrude(4)
    )

    # Boolean
    return result - circles - locks


result = switch()
