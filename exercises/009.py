from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="009",
    color="orange",
    alpha=0.0,
)

r = (
    cq.Workplane()
    .circle(70)
    .extrude(15)
    .faces(">Z")
    .rect(65, 65, forConstruction=True)
    .rotate((0, 0, 0), (0, 0, 1), 45)
    .vertices()
    .hole(20)
    .faces(">Z")
    .rect(45, 45)
    .extrude(15)
    .faces(">Z")
    .rect(35, 35)
    .cutThruAll()
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/009.svg")
