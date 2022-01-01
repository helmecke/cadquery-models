from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="010",
    color="orange",
    alpha=0.0,
)

r = (
    cq.Workplane()
    .rect(21, 50)
    .extrude(5)
    .edges(">Z and <X")
    .rect(5, 50, centered=(False, True))
    .extrude(50)
    .faces(">Z")
    .edges("<Y or >Y")
    .fillet(8)
    .faces(">X")
    .edges("<Y or >Y")
    .fillet(7)
    .faces("<Z[1]")
    .edges("<X")
    .workplane(centerOption="CenterOfMass")
    .transformed((90, 0, 90))
    .move(0, -16)
    .vLine(16)
    .hLine(14)
    .close()
    .extrude(3, both=True)
    .faces("<Z[1]")
    .edges("<X")
    .fillet(3)
    .faces(">X[1]")
    .workplane(centerOption="CenterOfBoundBox")
    .move(0, 2.5)
    .rect(35, 30, forConstruction=True)
    .vertices()
    .hole(8)
    .faces(">X[1]")
    .workplane(centerOption="CenterOfBoundBox")
    .move(0, 5)
    .hole(30)
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/010.svg")
