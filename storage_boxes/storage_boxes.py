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


def createBottom(self):
    s1 = (
        cq.Sketch()
        .rect(45.8, 45.8)
        .vertices()
        .fillet(3)
    )

    s2 = (
        cq.Sketch()
        .rect(53.8, 53.8)
        .vertices()
        .fillet(3)
    )

    R = (
        cq.Workplane()
        .placeSketch(
            s1.moved(cq.Location(cq.Vector(54.8 / 2, 54.8 / 2, 0))),
            s2.moved(cq.Location(cq.Vector(54.8 / 2, 54.8 / 2, 4)))
        )
        .loft()
        # .faces(">Z")
        # .shell(-4 * 0.28)
    )

    return self.eachpoint(lambda loc: R.val().located(loc), True)


cq.Workplane.createBottom = createBottom


def createMiddle(self, size=(1, 1)):
    s1 = (
        cq.Sketch()
        .rect(53.8 * box_size[1], 53.8 * box_size[0] + (-1 + 1 * box_size[0]))
        .vertices()
        .fillet(3)
    )

    s2 = (
        cq.Sketch()
        .rect(54.8 * box_size[1], 54.8 * box_size[0] + (-1 + 1 * box_size[0]))
        .vertices()
        .fillet(3)
    )

    R = (
        cq.Workplane()
        .placeSketch(
            s1.moved(cq.Location(cq.Vector(
                54.8 / 2 * box_size[0], 54.8 / 2 * box_size[1], 4))
            ),
            s2.moved(cq.Location(cq.Vector(
                54.8 / 2 * box_size[0], 54.8 / 2 * box_size[1], box_height - 4))
            )
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
    .union(cq.Workplane().createMiddle(size=box_size))
    .faces(">Z")
    .shell(-4 * 0.28)
    .faces("<Z[2]")
    .fillet(1.2)
)

show_object(res)
