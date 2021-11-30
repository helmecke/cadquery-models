import cadquery as cq  # type: ignore
import numpy as np

if "show_object" not in globals():

    def show_object(*args, **kwargs):
        pass


debug = {"alpha": 0.5}

box_size = (3, 1)
box_length = 54.8
box_width = 54.8
box_height = 75
base_height = 4


def createBottom(self):
    s1 = cq.Sketch().rect(box_width - 9, box_length - 9).vertices().fillet(3)

    s2 = cq.Sketch().rect(box_width - 1, box_length - 1).vertices().fillet(3)

    R = (
        cq.Workplane()
        .placeSketch(
            s1.moved(cq.Location(cq.Vector(box_length / 2, box_width / 2, 0))),
            s2.moved(
                cq.Location(cq.Vector(box_length / 2, box_width / 2, base_height))
            ),
        )
        .loft()
    )

    return self.eachpoint(lambda loc: R.val().located(loc), True)


cq.Workplane.createBottom = createBottom


def createMiddle(self):
    s1 = (
        cq.Sketch()
        .rect(
            (box_width - 1) * box_size[1] + (-1 + 1 * box_size[1]),
            (box_length - 1) * box_size[0] + (-1 + 1 * box_size[0]),
        )
        .vertices()
        .fillet(3)
    )

    s2 = (
        cq.Sketch()
        .rect(
            box_width * box_size[1] + (-1 + 1 * box_size[1]),
            box_length * box_size[0] + (-1 + 1 * box_size[0]),
        )
        .vertices()
        .fillet(3)
    )

    R = (
        cq.Workplane()
        .placeSketch(
            s1.moved(
                cq.Location(
                    cq.Vector(
                        box_length / 2 * box_size[0],
                        box_width / 2 * box_size[1],
                        base_height,
                    )
                )
            ),
            s2.moved(
                cq.Location(
                    cq.Vector(
                        box_length / 2 * box_size[0],
                        box_width / 2 * box_size[1],
                        box_height - base_height,
                    )
                )
            ),
        )
        .loft()
    )

    return self.eachpoint(lambda loc: R.val().located(loc), True)


cq.Workplane.createMiddle = createMiddle

x_af = np.linspace(0, (box_length) * (box_size[0] - 1), box_size[0])
y_af = np.linspace(0, (box_width) * (box_size[1] - 1), box_size[1])
x_af, y_af = np.meshgrid(x_af, y_af)
pts = [(x, y) for x, y in zip(x_af.flatten(), y_af.flatten())]

res = (
    cq.Workplane()
    .pushPoints(pts)
    .createBottom()
    .union(cq.Workplane().createMiddle())
    .faces(">Z")
    .shell(-4 * 0.28)
    .faces("<Z[2]")
    .fillet(1.2)
)

show_object(res)
