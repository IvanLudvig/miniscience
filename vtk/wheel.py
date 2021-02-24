import vtk
import numpy as np
import gmsh


class CalcMesh:

    def __init__(self, nodes_coords, tetrs_points):
        self.nodes = np.array([nodes_coords[0::3], nodes_coords[1::3], nodes_coords[2::3]])

        self.time = 0
        self.angular_velocity = [0, 1, 0]
        self.velocity = np.transpose(np.cross(np.transpose(self.nodes), self.angular_velocity))

        self.omega = np.ones(self.nodes.shape[1]) * 10
        self.k = 0.1
        self.wave = np.sin((self.omega * self.time) + self.nodes[0, :] * self.k)

        self.tetrs = np.array([tetrs_points[0::4], tetrs_points[1::4], tetrs_points[2::4], tetrs_points[3::4]])
        self.tetrs -= 1


    def move(self, tau):
        self.time += tau
        self.nodes += self.velocity * tau
        self.velocity = np.transpose(np.cross(np.transpose(self.nodes), self.angular_velocity))
        self.wave = np.sin((self.omega * self.time) + self.nodes[0, :] * self.k)

    def snapshot(self, snap_number):
        unstructuredGrid = vtk.vtkUnstructuredGrid()
        points = vtk.vtkPoints()

        wave = vtk.vtkDoubleArray()
        wave.SetName("wave")

        velocity = vtk.vtkDoubleArray()
        velocity.SetNumberOfComponents(3)
        velocity.SetName("velocity")

        for i in range(0, len(self.nodes[0])):
            points.InsertNextPoint(self.nodes[0, i], self.nodes[1, i], self.nodes[2, i])
            wave.InsertNextValue(self.wave[i])
            velocity.InsertNextTuple((self.velocity[0, i], self.velocity[1, i], self.velocity[2, i]))

        unstructuredGrid.SetPoints(points)

        unstructuredGrid.GetPointData().AddArray(wave)
        unstructuredGrid.GetPointData().AddArray(velocity)

        for i in range(0, len(self.tetrs[0])):
            tetr = vtk.vtkTetra()
            for j in range(0, 4):
                tetr.GetPointIds().SetId(j, self.tetrs[j, i])
            unstructuredGrid.InsertNextCell(tetr.GetCellType(), tetr.GetPointIds())

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetInputDataObject(unstructuredGrid)
        writer.SetFileName("vtu/wheel-step-" + str(snap_number) + ".vtu")
        writer.Write()


gmsh.initialize()
gmsh.open('wheel.msh')
nodeTags, nodesCoord, parametricCoord = gmsh.model.mesh.getNodes()

GMSH_TETR_CODE = 4
tetrsNodesTags = None
elementTypes, elementTags, elementNodeTags = gmsh.model.mesh.getElements()
for i in range(0, len(elementTypes)):
    if elementTypes[i] != GMSH_TETR_CODE:
        continue
    tetrsNodesTags = elementNodeTags[i]

if tetrsNodesTags is None:
    print("Can not find tetra data. Exiting.")
    gmsh.finalize()
    exit(-2)

print("The model has %d nodes and %d tetrs" % (len(nodeTags), len(tetrsNodesTags) / 4))

for i in range(0, len(nodeTags)):
    assert (i == nodeTags[i] - 1)
assert (len(tetrsNodesTags) % 4 == 0)

mesh = CalcMesh(nodesCoord, tetrsNodesTags)
mesh.snapshot(0)

tau = 0.01

for i in range(1, 100):
    mesh.move(tau)
    mesh.snapshot(i)

gmsh.finalize()
