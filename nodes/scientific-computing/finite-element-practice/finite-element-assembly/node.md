---
tag: AW3E0H
kind: algorithm
slug: finite-element-assembly
name: Finite element assembly
aliases:
- stiffness matrix assembly
- direct stiffness method
area: scientific-computing/finite-element-practice
level: intro
summary: Computes small element matrices by quadrature and adds them into the global sparse matrix through the local-to-global map of degrees of freedom.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {E: the number of cells, n: the number of local degrees of freedom per cell, q: the number of quadrature points per cell, N: the number of global degrees of freedom}
  time: {average: "Θ(E q n^2)"}
  space: {extra: "Θ(N + E n^2)"}
properties: {deterministic: true, keeps_symmetry: true, exact_with_exact_quadrature: true}
history:
  year: 1956
  people: [M. J. Turner, Ray W. Clough, H. C. Martin, L. J. Topp]
  note: Turner, Clough, Martin and Topp described the direct stiffness method for aircraft structures in 1956, adding element stiffness matrices into the global matrix node by node.
prereqs: [weak-formulation, lagrange-finite-element, sparse-matrix]
see_also: [finite-element-method, ciarlet-finite-element, isoparametric-mapping, mass-lumping, static-condensation, sparse-linear-systems, conjugate-gradient-method, corotational-fem]
sources:
  - paper: doi:10.2514/8.3664
    title: M. J. Turner, R. W. Clough, H. C. Martin and L. J. Topp, Stiffness and deflection analysis of complex structures, Journal of the Aeronautical Sciences 23(9) (1956) 805-823
    locator: element stiffness matrices and the direct stiffness assembly
  - paper: doi:10.1023/A:1019155918070
    title: J. Alberty, C. Carstensen and S. A. Funken, Remarks around 50 lines of Matlab, short finite element implementation, Numerical Algorithms 20 (1999) 117-137
    locator: element stiffness of P1 triangles and assembly with Dirichlet and Neumann data
  - book: isbn:9780486411811
    title: Thomas J. R. Hughes, The Finite Element Method, Linear Static and Dynamic Finite Element Analysis, Dover, 2000
    locator: Chapters 1 and 2 (element point of view, location matrix and the assembly operator)
---

Finite element assembly builds the global stiffness matrix $A$ and load vector $b$ of a finite element method cell by cell: it computes a small element matrix $A_K$ and vector $b_K$ on each cell $K$ and adds their entries into $A$ and $b$ at the rows and columns that the local-to-global map of degrees of freedom gives. This works because every entry $A_{ij} = a(\phi_j, \phi_i)$ is an integral over the domain, so it is the sum of the integrals over the cells, and only the few cells where both basis functions are nonzero contribute. Graphics simulators use the same loop with linear triangles or tetrahedra, one integration point and lumped masses, and the accurate method adds quadrature that integrates the element integrals exactly, elements of higher degree, consistent mass and load vectors, and boundary conditions imposed so that the matrix stays symmetric, which together give a proved error bound of order $h^k$ in the energy norm. The output is a sparse symmetric matrix that a [sparse solver](/sparse-linear-systems/) or [conjugate gradients](/conjugate-gradient-method/) can handle.

## In plain words

A large structure is hard to analyze as a whole, but each small piece of it is easy. Assembly first works out how each piece responds when its corner points move, which gives a small table of numbers for that piece. Then it adds every small table into one big table for the whole structure. Each corner point has one place in the big table, and a short list for each piece says where its corners go. Where two pieces share a corner, both add their numbers into the same place. At the end, the points where the structure is held fixed get special treatment. Their known values move to the other side of the equations, so that the big table keeps its balanced, mirror-image form.

## The problem

**Input.** A mesh $\mathcal{T}_h$ with cells $K$, and for each cell a [finite element](/ciarlet-finite-element/) with local basis $\phi^K_1, \ldots, \phi^K_n$ and a one-to-one local-to-global map $g_K : \{1, \ldots, n\} \to \{1, \ldots, N\}$, so that $\phi_{g_K(r)}|_K = \phi^K_r$. A bilinear form and a linear form that split into cell integrals, $a = \sum_K a_K$ and $l = \sum_K l_K$, for the model problem $a(u, v) = \int_\Omega \kappa\nabla u\cdot\nabla v$ and $l(v) = \int_\Omega fv$. A set $D$ of Dirichlet degrees of freedom with values $g_j$.

**Output.** The sparse matrix $A$ with $A_{ij} = a(\phi_j, \phi_i)$ and the vector $b$ with $b_i = l(\phi_i)$, where row $i$ belongs to the test function $\phi_i$, modified so that the solution of $AU = b$ has $U_j = g_j$ for $j \in D$ and satisfies the Galerkin equations $a(u_h, \phi_i) = l(\phi_i)$ for all other $i$.

## The algorithm

The element routine computes $A_K[r, s] = a_K(\phi^K_s, \phi^K_r)$ and $b_K[r] = l_K(\phi^K_r)$ by quadrature on the cell, usually through a map from a reference cell. The assembly itself does not depend on the element.

```pseudo id=main
ASSEMBLE(N, cells, ELEMENT)                ▷ each cell is (g, data); g maps local to global dofs
L1  A <- empty sparse N by N matrix; b <- zero vector of length N
L2  for each cell in cells do
L3      (g, data) <- cell
L4      (A_K, b_K) <- ELEMENT(data)          ▷ quadrature on the cell
L5      for i <- 1 to |g| do
L6          b[g[i]] <- b[g[i]] + b_K[i]
L7          for j <- 1 to |g| do
L8              A[g[i], g[j]] <- A[g[i], g[j]] + A_K[i, j]   ▷ add, never overwrite
L9  return A, b

APPLY-DIRICHLET(A, b, D)                   ▷ D maps each Dirichlet dof j to its value g_j
L10 for each j in D do
L11     for each row i not in D with A[i, j] != 0 do b[i] <- b[i] - A[i, j] g_j
L12 for each i in D do clear row i and column i of A, set A[i, i] <- 1 and b[i] <- g_i
L13 return A, b
```

**The P1 triangle element.** For a triangle with vertices $p_0, p_1, p_2$ let $B = [\,p_1 - p_0,\ p_2 - p_0\,]$, so that $F_K(\hat x) = p_0 + B\hat x$ maps the reference triangle onto $K$ and $|K| = |\det B|/2$. The reference gradients of the basis $1 - \hat x - \hat y$, $\hat x$, $\hat y$ are the columns of $\hat G = \begin{pmatrix} -1 & 1 & 0 \\ -1 & 0 & 1\end{pmatrix}$. The physical gradients are $G = B^{-\top}\hat G$, and for constant $\kappa$

$$A_K = \kappa\,|K|\,G^\top G, \qquad M_K = \frac{|K|}{12}\begin{pmatrix} 2 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2\end{pmatrix}.$$

On the reference triangle itself $A_K = \tfrac12\begin{pmatrix} 2 & -1 & -1 \\ -1 & 1 & 0 \\ -1 & 0 & 1\end{pmatrix}$. Its rows add up to zero, because the three basis functions add up to $1$ and a constant has no gradient. The off-diagonal entries equal $-\tfrac12\cot\theta$ for the angle $\theta$ opposite the edge, which is the cotangent formula of mesh processing. For curved or quadrilateral cells the [isoparametric mapping](/isoparametric-mapping/) replaces $B$ by a Jacobian that changes from point to point.

## Example

**Two triangles on the unit square.** Number the corners $v_0 = (0,0)$, $v_1 = (1,0)$, $v_2 = (1,1)$, $v_3 = (0,1)$ and split the square along the diagonal $v_0v_2$ into $T_1 = (v_0, v_1, v_2)$ and $T_2 = (v_0, v_2, v_3)$, with $\kappa = 1$. On $T_1$ the basis is $1 - x$, $x - y$, $y$ with gradients $(-1, 0)$, $(1, -1)$, $(0, 1)$, and on $T_2$ it is $1 - y$, $x$, $y - x$ with gradients $(0, -1)$, $(1, 0)$, $(-1, 1)$. Both areas are $\tfrac12$, so

$$A_{T_1} = \frac12\begin{pmatrix} 1 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 1\end{pmatrix} \text{ on } (0, 1, 2), \qquad A_{T_2} = \frac12\begin{pmatrix} 1 & 0 & -1 \\ 0 & 1 & -1 \\ -1 & -1 & 2\end{pmatrix} \text{ on } (0, 2, 3).$$

Line L8 adds them at the global positions. The diagonal entries for $v_0$ and $v_2$ get a contribution from both triangles, and the result is

$$A = \begin{pmatrix} 1 & -\tfrac12 & 0 & -\tfrac12 \\ -\tfrac12 & 1 & -\tfrac12 & 0 \\ 0 & -\tfrac12 & 1 & -\tfrac12 \\ -\tfrac12 & 0 & -\tfrac12 & 1\end{pmatrix}.$$

The entry $A_{02}$ is $0$ although $v_0$ and $v_2$ share an edge: both angles opposite the diagonal are right angles, and $\cot(\pi/2) = 0$. Every row adds up to $0$, so $A$ is singular until boundary conditions are imposed.

**A Dirichlet step in one dimension.** Take $-u'' = 1$ on $(0, 1)$ with $u(0) = 0$ and $u(1) = 1$, and three P1 cells with $h = \tfrac13$. Each cell gives $A_K = 3\begin{pmatrix} 1 & -1 \\ -1 & 1\end{pmatrix}$ and $b_K = (\tfrac16, \tfrac16)$, so ASSEMBLE returns

$$A = 3\begin{pmatrix} 1 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 1\end{pmatrix}, \qquad b = \bigl(\tfrac16, \tfrac13, \tfrac13, \tfrac16\bigr).$$

Line L11 for $j = 3$ with $g_3 = 1$ changes $b_2$ to $\tfrac13 - (-3)(1) = \tfrac{10}3$. Line L12 replaces rows and columns $0$ and $3$ by those of the identity. The free equations are $3(2U_1 - U_2) = \tfrac13$ and $3(-U_1 + 2U_2) = \tfrac{10}3$, with the solution $U_1 = \tfrac49$ and $U_2 = \tfrac79$. These are the exact values of $u = x(1-x)/2 + x$ at $x = \tfrac13$ and $\tfrac23$, because P1 elements are exact at the nodes for this one-dimensional problem. The final matrix is still symmetric.

**Sparsity.** On the uniform $m \times m$ square mesh with two triangles per square, the assembled P1 matrix has $(m+1)^2 + 2(3m^2 + 2m)$ stored entries: one per node and two per edge. For $m = 32$ that is $7361$ entries for $1089$ unknowns, about 6.8 per row. Only $5313$ of them are nonzero in value, because the diagonal edges give zeros as in the example, and the remaining entries form the 5-point stencil of the [finite difference method](/finite-difference-method/).

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). A loop invariant for lines L2 to L8 shows that after line L9 each $A[i, j]$ is the sum over the cells of $a_K(\phi_j|_K, \phi_i|_K)$, which is $a(\phi_j, \phi_i)$ because the map $g_K$ is one to one and the basis functions vanish on cells outside their support. Lines L10 to L12 turn the system into the block form $\begin{pmatrix} A_{FF} & 0 \\ 0 & I\end{pmatrix}$ with right side $(b_F - A_{FD}g,\ g)$ for the free indices $F$ and the Dirichlet indices $D$. So the solution takes the prescribed values and satisfies the Galerkin equations of the free rows, and the matrix stays symmetric and positive definite when $a$ is symmetric and coercive.

## Complexity

The element routine does $\Theta(q)$ work per entry, so it costs $\Theta(q n^2)$ per cell for a fixed dimension, and the scatter of lines L5 to L8 costs $\Theta(n^2)$ updates per cell. With a hash map per row, as in the reference code, an update takes expected constant time, and the total is $\Theta(E q n^2)$ on average. With a sparsity pattern computed in advance (compressed sparse row storage), each update is a search in a short row, and the bound holds in the worst case. The matrix has at most $E n^2$ stored entries before duplicates merge, and $\Theta(N)$ after, for a mesh whose node degrees stay bounded. The Dirichlet step touches each stored entry of the Dirichlet rows and columns once. Assembly is linear in the size of the mesh. The solve that follows usually costs more.

## Properties

- **Symmetry.** If every $A_K$ is symmetric, so is $A$, and lines L10 to L12 keep it symmetric.
- **Semidefiniteness.** For a symmetric form with $a_K(v, v) \ge 0$, each $A_K$ is positive semidefinite, and a sum of such matrices is positive semidefinite.
- **Zero row sums.** For $a(u, v) = \int\kappa\nabla u\cdot\nabla v$ and Lagrange elements, $\sum_j\phi_j = 1$ gives $\sum_j A_{ij} = a(1, \phi_i) = 0$ before boundary conditions.
- **Mass.** The entries of the assembled mass matrix $M_{ij} = (\phi_j, \phi_i)$ add up to $|\Omega|$, which is the starting point of [mass lumping](/mass-lumping/).
- **Locality.** $A_{ij} \ne 0$ only if $\phi_i$ and $\phi_j$ are both nonzero on some cell, so the pattern is the graph of the mesh.
- **Exactness.** The result is the exact Galerkin matrix when the quadrature in ELEMENT is exact for the integrands. The reference code uses Boole's rule, exact for degree 5, which covers P1 and P2 stiffness and mass matrices in 1D.

## Variants and improvements

- **Triplet assembly.** Store the $(i, j, value)$ triples of all cells, then sort and add duplicates in one pass. This is the vectorized method of Alberty, Carstensen and Funken, with the sparse matrix constructor doing the sums.
- **Pattern first.** Build the compressed sparse row pattern from the mesh graph, then fill values. Codes that assemble many times, such as Newton or time stepping, reuse the pattern.
- **Parallel assembly.** Color the cells so that no two cells of one color share a degree of freedom and process each color in parallel, or use atomic additions, or give each process its own cells plus ghost entries.
- **[Static condensation](/static-condensation/).** Eliminate interior degrees of freedom of each cell from $A_K$ before the scatter, which shrinks the global system for high order.
- **Matrix-free operation.** Never form $A$. Compute $AU$ by the same loop over cells applied to vectors. For high degree on tensor-product cells, sum factorization makes this cheaper than storing $A$.
- **Other Dirichlet methods.** Penalty terms, Lagrange multipliers or [Nitsche's method](/nitsche-method/) impose the values weakly, and a lifting function moves them into the right side before assembly.
- **Graphics practice.** Deformable-body codes such as [corotational FEM](/corotational-fem/) assemble linear tetrahedra with one-point integration and diagonal masses, and they often apply constraints by projection inside the solver.

## When to use it

Use assembly when an implicit method needs the matrix: sparse direct solvers, algebraic [multigrid](/multigrid-method/) and incomplete factorizations all need the entries. For low-order elements the stored matrix is also the fastest way to apply the operator many times. For high-order elements, or on GPUs where memory bandwidth limits the speed, matrix-free application often wins, and assembly is only needed for a coarse level or a preconditioner.

## Pitfalls

- **Overwriting instead of adding.** Line L8 must add. With an assignment, the two-triangle example gives $A_{00} = \tfrac12$ in place of $1$, and the solution is wrong without any error message.
- **Nonsymmetric Dirichlet rows.** Replacing only the Dirichlet rows by unit rows, without line L11 and without clearing the columns, gives a nonsymmetric matrix, and conjugate gradients may then fail.
- **Orientation of cells.** A clockwise triangle has $\det B < 0$. Use $|\det B|$ for the area, and check the sign when an inverted cell would mean a bad mesh.
- **Orientation of shared degrees of freedom.** For P3 and higher, or for edge elements, two cells may order the nodes on a shared edge in opposite directions. The map $g_K$ must agree on both sides, or the global function is not continuous.
- **Weak quadrature for data.** A rule that is exact for the stiffness matrix can be too weak for a variable $\kappa$ or a rough $f$, and the convergence order drops.
- **Dense storage.** An $N \times N$ dense matrix is $N^2$ numbers. For $N = 10^6$ that is $8 \times 10^{12}$ bytes, while the sparse matrix needs about $10^8$.
- **Races in parallel.** Two threads that add into the same entry at the same time lose one of the updates unless the cells are colored or the additions are atomic.

## Implementations

## History

M. J. Turner, Ray Clough, H. C. Martin and L. J. Topp published the direct stiffness method in 1956 for aircraft structures at Boeing. They computed stiffness matrices of triangular plate pieces and added them into the global matrix by node numbers, which is the loop above. Clough named the method the finite element method in 1960. Bruce Irons published the frontal solver in 1970, which interleaves assembly with Gaussian elimination so that only a small front of the matrix is in memory. The short vectorized implementations of the 1990s, such as the 50 lines of Matlab of Alberty, Carstensen and Funken, made the algorithm a standard part of teaching.

## References
