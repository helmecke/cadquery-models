import math
from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="006",
    color="orange",
    alpha=0.0,
)

r1 = (
    cq.Workplane("XZ")
    .moveTo(6, 8 + 17)
    .vLine(-17)
    .hLine(math.sqrt(-(17 ** 2) + (17 / math.sin(math.radians(-60 + 90))) ** 2))
    .close()
    .extrude(1.5, both=True)
)

r = (
    cq.Workplane()
    .move(0, 5)
    .lineTo(0, 25 / 2)
    .hLine(8)
    .vLine(-25)
    .hLine(-8)
    .vLine((25 - 10) / 2)
    .lineTo(4, -15 / 2)
    .vLine(15)
    .close()
    .extrude(-42)
    .rotate((0, 0, 0), (0, 1, 0), -90)
    .faces(">Z")
    .edges("<X")
    .workplane()
    .center(3, 0)
    .rect(6, 25)
    .extrude(22)
    .faces(">Z")
    .edges("<Y or >Y")
    .chamfer((25 - 12) / 2)
    .union(r1)
)

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/006.svg")
