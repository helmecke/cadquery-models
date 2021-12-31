from types import SimpleNamespace as Measures

import cadquery as cq

s = Measures(
    name="002",
    color="steelblue",
    alpha=0.0,
)

r = cq.Workplane("XZ").cylinder(19, 12, centered=(True, True, False))

show_object(r, s.name, options={"color": s.color, "alpha": s.alpha})  # noqa: F821

cq.exporters.export(r, "docs/002.svg")
