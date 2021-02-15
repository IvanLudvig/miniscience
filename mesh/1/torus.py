import gmsh
import sys

gmsh.initialize()
gmsh.open("t1.geo")

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

gmsh.write("torus.msh")
gmsh.write("torus.geo_unrolled")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
