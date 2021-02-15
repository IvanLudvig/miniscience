import gmsh
import sys

gmsh.initialize()

gmsh.model.add("t2")

lc = 1e-2
for z in [0, .1]:
    gmsh.model.geo.addPoint(0, 0, z, lc, 1 + 4 * (not not z))
    gmsh.model.geo.addPoint(.1, 0, z, lc, 2 + 4 * (not not z))
    gmsh.model.geo.addPoint(.1, .1, z, lc, 3 + 4 * (not not z))
    gmsh.model.geo.addPoint(0, .1, z, lc, 4 + 4 * (not not z))

gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(2, 3, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)

gmsh.model.geo.addLine(5, 6, 5)
gmsh.model.geo.addLine(6, 7, 6)
gmsh.model.geo.addLine(7, 8, 7)
gmsh.model.geo.addLine(8, 5, 8)

gmsh.model.geo.addLine(1, 5, 9)
gmsh.model.geo.addLine(2, 6, 10)
gmsh.model.geo.addLine(3, 7, 11)
gmsh.model.geo.addLine(4, 8, 12)

gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
gmsh.model.geo.addCurveLoop([5, 6, 7, 8], 2)

gmsh.model.geo.addCurveLoop([9, 5, -10, -1], 3)
gmsh.model.geo.addCurveLoop([10, 6, -11, -2], 4)
gmsh.model.geo.addCurveLoop([11, 7, -12, -3], 5)
gmsh.model.geo.addCurveLoop([12, 8, -9, -4], 6)

for i in range(6):
    gmsh.model.geo.addPlaneSurface([i + 1], i + 1)

l = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(6)])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

gmsh.write("t2.msh")
gmsh.write("t2.geo_unrolled")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
