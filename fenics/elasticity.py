from fenics import *
from ufl import nabla_grad
from ufl import nabla_div

# Scaled variables
L = 4; W = 0.2
mu = 1.5
rho = 2
delta = W/L
gamma = 0.4*delta**2
beta = 1.25
lambda_ = beta
g = gamma

# Create mesh and define function space
mesh = BoxMesh(Point(0, 0, 0), Point(L, W, W), 10, 3, 3)
V = VectorFunctionSpace(mesh, 'P', 1)

# Define boundary condition
left = 1E-14
right = L - (1E-14)

def clamped_boundary_left(x, on_boundary):
    return on_boundary and x[0] < left

def clamped_boundary_right(x, on_boundary):
    return on_boundary and x[0] > right

bc_left = DirichletBC(V, Constant((0, 0, 0)), clamped_boundary_left)
bc_right = DirichletBC(V, Constant((0, 0, 0)), clamped_boundary_right)
bc = [bc_left, bc_right]

# Define strain and stress

def epsilon(u):
    return 0.5*(nabla_grad(u) + nabla_grad(u).T)
    #return sym(nabla_grad(u))

def sigma(u):
    return lambda_*nabla_div(u)*Identity(d) + 2*mu*epsilon(u)

# Define variational problem
u = TrialFunction(V)
d = u.geometric_dimension()  # space dimension
v = TestFunction(V)
f = Constant((0, 0, -rho*g))
T = Constant((0, 0, 0))
a = inner(sigma(u), epsilon(v))*dx
L = dot(f, v)*dx + dot(T, v)*ds

# Compute solution
u = Function(V)
solve(a == L, u, bc)

# Plot stress
s = sigma(u) - (1./3)*tr(sigma(u))*Identity(d)  # deviatoric stress
von_Mises = sqrt(3./2*inner(s, s))
V = FunctionSpace(mesh, 'P', 1)
von_Mises = project(von_Mises, V)

# Compute magnitude of displacement
u_magnitude = sqrt(dot(u, u))
u_magnitude = project(u_magnitude, V)

# Save solution to file in VTK format
File('res/displacement.pvd') << u
File('res/von_mises.pvd') << von_Mises
File('res/magnitude.pvd') << u_magnitude

 
