import cadquery as cq

bearing_inner = 5
bearing_outer = 16 / 2
bearing_thickness = 5
wall = 2
bottle = (25 + 0.1) / 2
loft = 4

adapter = (
    cq.Workplane('front')
    .circle(bearing_outer + wall)
    .extrude(bearing_thickness - loft)
    .faces('>Z')
    .circle(bearing_outer + wall)
    .workplane(4)
    .circle(bottle + wall)
    .loft(combine=True)
    .faces('<Z')
    .circle(bearing_outer)
    .cutBlind(bearing_thickness)
    .edges('<Z').last()
    .chamfer(0.5)
    .faces('>Z')
    .circle(bottle + wall)
    .extrude(0.1)
    .faces('>Z')
    .circle(bearing_inner)
    .circle(bottle + wall)
    .extrude(1)
    .faces('>Z')
    .circle(bottle)
    .circle(bottle + wall)
    .extrude(40)
    .faces('>Z')
    .fillet(wall / 2 - 0.01)
)

crank = (
    cq.Workplane('front')
    .circle(2.525)
    .extrude(5)
    .faces('>Z')
    .chamfer(0.5)
    .faces('<Z')
    .center(-2.5, 0)
    .circle(5)
    .extrude(-20)
)
