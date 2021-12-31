from types import SimpleNamespace as Measures

import cadquery as cq
import cadquery.selectors as cqs

s = Measures(
    name="001",
    color="steelblue",
    alpha=0.0,
)

r = (
    cq.Workplane()
    .box(10, 10, 3, centered=(True, True, False))
    .edges("|Z")
    .fillet(2)
    .faces(">Z")
    .rect(10 - 2 * 2, 10 - 2 * 2, forConstruction=True)
    .vertices()
    .hole(2)
    .faces(">Z")
    .cylinder(6, 2, centered=(True, True, False))
    .edges(cqs.NearestToPointSelector((0, 0, 3)))
    .fillet(1)
    .faces(">Z")
    .hole(2)
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/001.svg")
