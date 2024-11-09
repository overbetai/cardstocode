import numpy as np
from scipy import optimize

# Givens
A = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,1,0,0,2,1,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,0,0,2,0,0,0,2,0],
    [0,0,0,0,0,0,0,-1,0,0,0,-1,0],
    [0,-2,1,0,0,0,0,0,0,2,1,0,0],
    [0,0,0,0,-1,0,0,0,0,0,0,0,1],
    [0,0,0,-2,0,0,0,0,0,0,0,2,0],
    [0,0,0,-1,0,0,0,0,0,0,0,-1,0],
    [0,-2,1,0,0,-2,1,0,0,0,0,0,0],
    [0,0,0,0,-1,0,0,0,-1,0,0,0,0],
    [0,0,0,-2,0,0,0,-2,0,0,0,0,0],
    [0,0,0,-1,0,0,0,-1,0,0,0,0,0]
]) / 6.0

F = np.array([
    [1,0,0,0,0,0,0,0,0,0,0,0,0],
    [-1,1,1,0,0,0,0,0,0,0,0,0,0],
    [-1,0,0,1,1,0,0,0,0,0,0,0,0],
    [-1,0,0,0,0,1,1,0,0,0,0,0,0],
    [-1,0,0,0,0,0,0,1,1,0,0,0,0],
    [-1,0,0,0,0,0,0,0,0,1,1,0,0],
    [-1,0,0,0,0,0,0,0,0,0,0,1,1]
])

f = np.array([1,0,0,0,0,0,0])

E = np.array([
    [1,0,0,0,0,0,0,0,0,0,0,0,0],
    [-1,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,-1,1,1,0,0,0,0,0,0,0,0],
    [-1,0,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,-1,1,1,0,0,0,0],
    [-1,0,0,0,0,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,-1,1,1]
])

e = np.array([1,0,0,0,0,0,0])

# Get dimensions
dim_E = E.shape
dim_F = F.shape

# Extend to cover both y and p
e_new = np.concatenate([np.zeros(dim_F[1]), e])

# Constraint changes for 2 variables
H1 = np.hstack([-F, np.zeros((dim_F[0], dim_E[0]))])
H2 = np.hstack([A, -E.T])
H3 = np.zeros(dim_E[1])

# Bounds for both
lb = np.concatenate([np.zeros(dim_F[1]), -np.inf * np.ones(dim_E[0])])
ub = np.concatenate([np.ones(dim_F[1]), np.inf * np.ones(dim_E[0])])

# Solve LP problem
result = optimize.linprog(e_new, A_ub=H2, b_ub=H3, A_eq=H1, b_eq=-f, bounds=list(zip(lb, ub)))

# Get solutions {x, y, p, q}
x = result.slack
y = result.x[:dim_F[1]]
p = result.x[dim_F[1]:dim_F[1]+dim_E[0]]
q = result.eqlin

# Print results
print("x =", x)
print("y =", y)
print("p =", p)
print("q =", q)