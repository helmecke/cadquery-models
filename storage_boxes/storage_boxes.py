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
label_length = 15
label_width = 40
label_height = 20
extrusion_width = 0.45


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
            box_width * box_size[1],
            box_length * box_size[0],
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
                        box_height,
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

box = (
    cq.Workplane()
    .pushPoints(pts)
    .createBottom()
    .union(cq.Workplane().createMiddle())
    .faces(">Z")
    .shell(-3 * extrusion_width)
    .faces("<Z[2]")
    .fillet(1.2)
    # .faces("<X")
    # .workplane()
    # .center(-box_length / 2, box_height - base_height - label_height - 2)
    # .rect(label_width - 4, label_height - 5, centered=(True, False))
    # .cutBlind('next')
)

label = (
    cq.Workplane()
    .box(label_length, label_width, label_height, centered=(False, True, False))
    .edges("<Z and >X")
    .chamfer(label_height - 3 * extrusion_width, label_length - extrusion_width)
    .faces(">Z")
    .wires()
    .toPending()
    .offset2D(-3 * extrusion_width)
    .cutBlind(-1)
    .edges("|Z and >X")
    .fillet(3 * extrusion_width)
    .translate(
        (extrusion_width, box_length * box_size[1] / 2, box_height - label_height - 4)
    )
)

res = box.union(label)

show_object(res)
