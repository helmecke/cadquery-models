import cadquery as cq  # type: ignore
import numpy as np

if "show_object" not in globals():

    def show_object(*args, **kwargs):
        pass


debug = {"alpha": 0.5}

box_size = (3, 2)
half_height = True
label = True
separator = True

box_length = 54.8
box_width = 54.8
box_height = 75.0
base_height = 4
label_length = 12
label_width = 35
extrusion_width = 0.45
tab_length = label_length + 3 * extrusion_width
tab_width = label_width + 3 * extrusion_width
tab_height = tab_length

if half_height:
    box_height = box_height / 2 - 1


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

    return self.union(self.eachpoint(lambda loc: R.val().located(loc), True))


cq.Workplane.createBottom = createBottom


def createSep(self):
    s1 = cq.Sketch().rect(
        (box_width - 1 - 3 * extrusion_width) * box_size[1] + (-1 + 1 * box_size[1]),
        3 * extrusion_width,
    )

    s2 = cq.Sketch().rect(
        (box_width - 3 * extrusion_width) * box_size[1],
        3 * extrusion_width,
    )

    R = (
        cq.Workplane()
        .placeSketch(
            s1.moved(
                cq.Location(
                    cq.Vector(
                        0,
                        box_width / 2 * box_size[1],
                        base_height,
                    )
                )
            ),
            s2.moved(
                cq.Location(
                    cq.Vector(
                        0,
                        box_width / 2 * box_size[1],
                        box_height - 1,
                    )
                )
            ),
        )
        .loft()
    )

    return self.eachpoint(lambda loc: R.val().located(loc), True)


cq.Workplane.createSep = createSep

x_af = np.linspace(0, (box_length) * (box_size[0] - 1), box_size[0])
y_af = np.linspace(0, (box_width) * (box_size[1] - 1), box_size[1])
x_af, y_af = np.meshgrid(x_af, y_af)
pts = [(x, y) for x, y in zip(x_af.flatten(), y_af.flatten())]

res = (
    cq.Workplane()
    .placeSketch(
        cq.Sketch()
        .rect(
            (box_width - 1) * box_size[1] + (-1 + 1 * box_size[1]),
            (box_length - 1) * box_size[0] + (-1 + 1 * box_size[0]),
        )
        .vertices()
        .fillet(3)
        .moved(
            cq.Location(
                cq.Vector(
                    box_length / 2 * box_size[0],
                    box_width / 2 * box_size[1],
                    base_height,
                )
            )
        ),
        cq.Sketch()
        .rect(
            box_width * box_size[1],
            box_length * box_size[0],
        )
        .vertices()
        .fillet(3)
        .moved(
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
    .pushPoints(pts)
    .createBottom()
    .faces(">Z")
    .shell(-3 * extrusion_width)
    .faces("<Z[2]")
    .fillet(1.2)
)

if label:
    res = res.union(
        cq.Workplane()
        .box(tab_length, tab_width, tab_height, centered=(False, True, False))
        .edges("<Z and >X")
        .chamfer(tab_height - 3 * extrusion_width, tab_length - extrusion_width)
        .faces(">Z")
        .wires()
        .toPending()
        .offset2D(-3 * extrusion_width)
        .cutBlind(-1)
        .edges("|Z and >X")
        .fillet(3 * extrusion_width)
        .translate(
            (
                extrusion_width,
                box_length * box_size[1] / 2,
                box_height - tab_height - base_height + 1,
            )
        )
    )

if separator:
    res = (
        res.union(
            cq.Workplane().pushPoints(pts[1:box_size[0]]).createSep()
        )
        .faces(
            cq.selectors.BoxSelector(
                (box_length - 10, box_width - 10, base_height + 2),
                (
                    box_length * box_size[0] - 10,
                    box_width * box_size[1] - 10,
                    box_height - 1,
                ),
            )
        )
        .edges(">Y or <Y")
        .fillet(1)
    )

show_object(res)
