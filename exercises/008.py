import math
from types import SimpleNamespace as Measures

import cadquery as cq
import cadquery.selectors as cqs

s = Measures(
    name="008",
    color="orange",
    alpha=0.0,
)

r = (
    cq.Workplane()
    .sketch()
    .circle(2)
    .rarray(1, 6.3, 1, 2)
    .circle(1.1, "s")
    .circle(1)
    .wires()
    .hull()
    .finalize()
    .extrude(1)
    .faces(">Z")
    .circle(1.5)
    .extrude(3)
    .faces(">Z")
    .circle(1)
    .cutThruAll()
    .faces(">Z[1]")
    .workplane()
    .rarray(1, 6.3, 1, 2)
    .hole(1)
    .faces(">Z")
    .edges(cqs.RadiusNthSelector(0))
    .chamfer(
        math.sqrt(-(0.5 ** 2) + (0.5 / math.sin(math.radians(60))) ** 2), 0.5 - 0.0001
    )
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/008.svg")
