import cadquery as cq
import numpy as np

row_radius = 10
column_radius = 10
num_rows = 5
num_columns = 3

pi = 3.14159
alpha = pi / 12.0  # curvature of the columns
beta = pi / 36  # curvature of the rows
centercol = 3  # controls left_right tilt / tenting (higher number is more tenting)

centerrow = 3

column_offset = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 2.82, -4.5],
    [0, 0, 0],
    [0, -6, 5],  # REDUCED STAGGER
    [0, -6, 5],  # REDUCED STAGGER
    [0, -6, 5],  # NOT USED IN MOST FORMATS (7th column)
]


def rad2deg(rad: float) -> float:
    return rad * 180 / pi


def union(shapes):
    shape = None
    try:
        for item in shapes:
            if item is not None:
                if shape is None:
                    shape = item
                else:
                    shape = shape.union(item)
    except Exception:
        pass
    return shape


def translate(shape, vector):
    if shape is None:
        return None
    return shape.translate(tuple(vector))


def rotate(shape, angle):
    if shape is None:
        return None
    origin = (0, 0, 0)
    shape = shape.rotate(
        axisStartPoint=origin, axisEndPoint=(1, 0, 0), angleDegrees=angle[0]
    )
    shape = shape.rotate(
        axisStartPoint=origin, axisEndPoint=(0, 1, 0), angleDegrees=angle[1]
    )
    shape = shape.rotate(
        axisStartPoint=origin, axisEndPoint=(0, 0, 1), angleDegrees=angle[2]
    )
    return shape


def x_rot(shape, angle):
    # Rotates the shape around the x-axis by the given angle.
    # Convert the angle to degrees and call the rotate function.
    return rotate(shape, [rad2deg(angle), 0, 0])


def y_rot(shape, angle):
    # Rotates the shape around the y-axis by the given angle.
    # Convert the angle to degrees and call the rotate function.
    return rotate(shape, [0, rad2deg(angle), 0])


def rotate_around_x(position, angle):
    # Rotates a 3D position vector around the x-axis by a given angle.
    # The transformation matrix for x-axis rotation is created.
    t_matrix = np.array(
        [
            [1, 0, 0],  # No change in the x-coordinate
            [0, np.cos(angle), -np.sin(angle)],  # Update y-coordinate
            [0, np.sin(angle), np.cos(angle)],  # Update z-coordinate
        ]
    )
    # Multiply the transformation matrix by the position vector to get the rotated position.
    return np.matmul(t_matrix, position)


def rotate_around_y(position, angle):
    # Rotates a 3D position vector around the y-axis by a given angle.
    # The transformation matrix for y-axis rotation is created.
    t_matrix = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],  # Update x-coordinate
            [0, 1, 0],  # No change in the y-coordinate
            [-np.sin(angle), 0, np.cos(angle)],  # Update z-coordinate
        ]
    )
    # Multiply the transformation matrix by the position vector to get the rotated position.
    return np.matmul(t_matrix, position)


def make_switch():

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


def key_place(shape, column, row):
    return shape


def make_holes():

    holes = []
    for column in range(num_columns):

        column_angle = beta * (centercol - column)

        for row in range(num_rows):

            print(column, row)
            shape = make_switch()

            # shape = rotate(shape, rotate_around_x((row * 20, column * 20, 10), 10))

            shape = translate(shape, [0, 0, -row_radius])
            shape = x_rot(shape, alpha * (centerrow - row))
            shape = translate(shape, [0, 0, row_radius])
            shape = translate(shape, [0, 0, -column_radius])
            shape = y_rot(shape, column_angle)
            shape = translate(shape, [0, 0, column_radius])
            shape = translate(shape, column_offset[column])

            shape = translate(shape, (column * 20, row * 20, 0))

            holes.append(key_place(shape, column, row))

    return union(holes)


result = make_holes()
