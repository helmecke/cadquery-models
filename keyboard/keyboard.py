import cadquery as cq  # type: ignore
from math import sin, pi

if "show_object" not in globals():

    def show_object(*args, **kwargs):
        pass


debug = {"alpha": 0.5}

wall_thickness = 3
keyswitch_length = 14.4
keyswitch_width = 14.4
mount_length = keyswitch_length + wall_thickness
mount_width = keyswitch_width + wall_thickness
plate_thickness = 4
key_cap_profile_height = 12.7
key_cap_profile_height = 7.4
key_cap_double_length = 37.5
columns = range(7)
rows = range(5)
center_column = 3
center_row = 2
alpha = pi / 12
beta = pi / 36
cap_top_height = plate_thickness + key_cap_profile_height
row_radius = (mount_length + 0.5) / sin(alpha) + cap_top_height
column_radius = (mount_width + 2) / sin(beta) + cap_top_height
web_thickness = 3.5

thumb_columns = range(4)
thumb_rows = range(3)
thumb_center_column = 2
thumb_center_row = 1


def plate(size=1, align="horizontal"):
    if size == 2:
        width = key_cap_double_length - wall_thickness
    elif size == 1.5:
        width = 27 - wall_thickness
    else:
        width = mount_width

    plate = (
        cq.Workplane()
        .box(mount_length, width, plate_thickness)
        .faces(">Z")
        .rect(keyswitch_length, keyswitch_width)
        .cutThruAll()
    )

    nibble = (
        cq.Workplane("YZ")
        .center(keyswitch_length / 2, -plate_thickness / 2)
        .line(0, plate_thickness)
        .spline([(-0.5, 0.05), (0, 0)], includeCurrent=True)
        .close()
        .extrude(2.75 / 2, both=True)
        .mirror("XZ", union=True)
    )

    if align == "horizontal":
        plate = plate.rotate([0, 0, 1], [0, 0, 0], 90)

    return plate.union(nibble)


def key_place(column, row, shape, size=1, align="horizontal"):
    if align == "vertical":
        if size == 2:
            row += 1 / 2
        elif size == 1.5:
            row += 1 / 4
    else:
        if size == 2:
            column += 1 / 2
        elif size == 1.5:
            column += 1 / 4

    row_placed_shape = (
        shape(size, align)
        .translate([0, 0, -row_radius])
        .rotate((1, 0, 0), (0, 0, 0), -15 * (center_row - row))
        .translate([0, 0, row_radius])
    )

    if column == center_column - 3:
        column_row_offset = [0, 0, 1]
    elif column == center_column:
        column_row_offset = [0, 2.82, -3.0]
    elif column == center_column + 2:
        column_row_offset = [0, -5.8, 5.64]
    elif column >= center_column + 3:
        column_row_offset = [0.2, -5.8, 6.14]
    else:
        column_row_offset = [0, 0, 0]

    column_angle = 5 * (center_column - column)

    placed_shape = (
        row_placed_shape.translate([0, 0, -column_radius])
        .rotate((0, 1, 0), (0, 0, 0), column_angle)
        .translate([0, 0, column_radius])
        .translate(column_row_offset)
    )

    return placed_shape.rotate((0, 1, 0), (0, 0, 0), 15).translate([0, 0, 14.5])


def thumb_place(column, row, shape, size=1, align="horizontal"):
    row_radius = (mount_length + 1) / sin(alpha) + cap_top_height
    column_radius = (mount_width + 2) / sin(beta) + cap_top_height

    if align == "vertical":
        if size == 2:
            row -= 1 / 2
        elif size == 1.5:
            row -= 1 / 4
    else:
        if size == 2:
            column -= 1 / 2
        elif size == 1.5:
            column -= 1 / 4

    row_placed_shape = (
        shape(size, align)
        .translate([0, 0, -row_radius])
        .rotate((1, 0, 0), (0, 0, 0), -15 * (thumb_center_row - row))
        .translate([0, 0, row_radius])
    )

    if column == thumb_center_column + 1:
        column_row_offset = [mount_width, 0, -1.1]
    else:
        column_row_offset = [mount_width, 0, 0]

    column_angle = 5 * (thumb_center_column - column)

    placed_shape = (
        row_placed_shape.translate([0, 0, -column_radius])
        .rotate((0, 1, 0), (0, 0, 0), column_angle)
        .translate([0, 0, column_radius])
        .translate(column_row_offset)
        .rotate((0, 0, 1), (0, 0, 0), 11.25)
    )

    return placed_shape.rotate((1, 1, 0), (0, 0, 0), 20).translate([20, -40, 37])


def key_layout(shape):
    placed_shape = cq.Workplane()

    for row in rows:
        for column in columns:
            if column == center_column + 3 and not row >= center_row + 2:
                placed_shape.add(key_place(column, row, shape, 1.5))
            elif column == center_column - 3 and row >= center_row + 1:
                pass
            elif column >= center_column or not row >= center_row + 2:
                placed_shape.add(key_place(column, row, shape))

    return placed_shape


def thumb_layout(shape):
    placed_shape = cq.Workplane()

    for row in thumb_rows:
        for column in thumb_columns:
            if column >= thumb_center_column and row <= thumb_center_row:
                pass
            elif column == thumb_center_column - 1 and row == thumb_center_row:
                pass
            elif column == thumb_center_column + 1:
                placed_shape.add(thumb_place(column, row, shape, 1.5, "vertical"))
            elif (
                column == thumb_center_column or column == thumb_center_column - 1
            ) and row == thumb_center_row + 1:
                placed_shape.add(thumb_place(column, row, shape, 2, "vertical"))
            else:
                placed_shape.add(thumb_place(column, row, shape))

    return placed_shape


res = key_layout(plate).add(thumb_layout(plate))

show_object(res)
