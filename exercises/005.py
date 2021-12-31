from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="005",
    color="orange",
    alpha=0.0,
)

s1 = (
    cq.Sketch()
    .rect(20, 10)
    .edges(">Y")
    .tag("top")
    .circle(10)
    .select("top")
    .circle(5, mode="s")
)

r = (
    cq.Workplane()
    .box(52, 26, 13, centered=(False, True, False))
    .faces("<Y")
    .workplane()
    .center(10, 18)
    .placeSketch(s1)
    .extrude(-7)
    .faces(">Y")
    .workplane()
    .placeSketch(s1)
    .extrude(-7)
    .faces("<Z[1]")
    .edges(">X")
    .workplane(centerOption="CenterOfMass")
    .center(-15, 0)
    .slot2D(23, 10)
    .cutThruAll()
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/005.svg")
