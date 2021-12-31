from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="003",
    color="steelblue",
    alpha=0.0,
)

r = (
    cq.Workplane()
    .circle(25)
    .extrude(8)
    .faces(">Z")
    .circle(21)
    .cutBlind(-5)
    .rect(20, 20)
    .extrude(24)
    .faces(">Z")
    .rect(12, 12)
    .cutBlind(-24)
    .faces(">Z")
    .rect(8, 20)
    .cutBlind(-12)
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/003.svg")
