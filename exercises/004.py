from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="004",
    color="steelblue",
    alpha=0.0,
)

r = (
    cq.Workplane()
    .box(52, 52, 5, centered=(True, True, False))
    .faces(">Z")
    .rect(37, 37)
    .workplane(offset=18)
    .rect(18, 18)
    .loft()
    .wires(">Z")
    .toPending()
    .extrude(8)
    .faces(">Z")
    .rect(11, 11)
    .cutBlind(-8)
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/004.svg")
