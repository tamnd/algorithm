---
tag: 3GDP61
kind: definition
slug: lagrange-finite-element
name: Lagrange finite element
aliases:
- Pk Lagrange element
area: scientific-computing/finite-element-practice
level: intro
summary: The element whose degrees of freedom are values at nodes, giving continuous piecewise polynomials of degree k.
prereqs: [lagrange-interpolation, weak-formulation]
see_also: [ciarlet-finite-element, finite-element-assembly, isoparametric-mapping, bramble-hilbert-lemma, finite-element-method, spectral-element-method, hp-finite-element-method, gauss-lobatto-quadrature]
sources:
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 3 (Lagrange elements on simplices and rectangles, continuity of the global space)
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 2 (simplicial and rectangular Lagrange finite elements, the principal lattice)
  - book: isbn:9780387205748
    title: Alexandre Ern and Jean-Luc Guermond, Theory and Practice of Finite Elements, Applied Mathematical Sciences 159, Springer, 2004
    locator: Chapter 1 (Lagrange finite elements and their interpolation)
  - paper: doi:10.1090/S0002-9904-1943-07818-4
    title: R. Courant, Variational methods for the solution of problems of equilibrium and vibrations, Bulletin of the American Mathematical Society 49(1) (1943) 1-23
    locator: the appendix with piecewise linear functions on triangles
---

The Lagrange finite element of degree $k$ is the element whose shape functions are the polynomials of degree at most $k$ on a cell and whose degrees of freedom are the values of the function at a fixed set of nodes. Its nodal basis functions are $1$ at one node and $0$ at all the others, so the coefficient of a finite element function is its value at that node. On a mesh, neighboring cells share the nodes on their common face, and this makes the global function continuous, so the space lies in $H^1$ and suits second-order problems such as the Poisson equation. The case $k = 1$ on triangles is Courant's piecewise linear element.

## Definition

**On a simplex.** Let $K \subset \mathbb{R}^d$ be a simplex with vertices $a_0, \ldots, a_d$ and let $k \ge 1$. The Lagrange element of degree $k$ is the [Ciarlet finite element](/ciarlet-finite-element/) $(K, \mathcal{P}_k, \mathcal{N})$ with

$$\mathcal{N} = \{v \mapsto v(x_\beta)\}, \qquad x_\beta = \sum_{i=0}^d \frac{\beta_i}{k}\,a_i, \qquad \beta = (\beta_0, \ldots, \beta_d), \ \beta_i \ge 0 \text{ integers}, \ \sum_i \beta_i = k .$$

The nodes $x_\beta$ form the *principal lattice* of order $k$. Their number equals $\dim\mathcal{P}_k = \binom{k+d}{d}$: in 2D it is $(k+1)(k+2)/2$, which is $3, 6, 10$ for $k = 1, 2, 3$, and in 3D it is $(k+1)(k+2)(k+3)/6$, which is $4, 10, 20$.

**Unisolvence and continuity.** A polynomial of degree $k$ that vanishes at the principal lattice is zero. The proof goes face by face: the nodes on a face are the principal lattice of that face, so by induction on $d$ the polynomial vanishes on the face and contains the barycentric coordinate of the face as a factor. The same face property gives continuity. Two cells that share a face have the same nodes on it, the restriction of each polynomial to the face is a polynomial of degree $k$ fixed by those nodes, so the two restrictions agree. The global space

$$V_h = \{v \in C(\overline\Omega) : v|_K \in \mathcal{P}_k \text{ for all } K \in \mathcal{T}_h\}$$

is therefore a subspace of $H^1(\Omega)$. Its nodal basis function $\phi_i$ is $1$ at the global node $x_i$, $0$ at all other nodes, and nonzero only on the cells that contain $x_i$.

**On boxes.** On a rectangle or a brick the space $\mathcal{Q}_k$ of polynomials of degree at most $k$ in each variable separately, with the tensor product of $k+1$ nodes per direction, is the tensor-product Lagrange element. Q1 on a square has the four vertex values and the basis $(1-x)(1-y)$, $x(1-y)$, $xy$, $(1-x)y$.

**Basis in barycentric coordinates.** With barycentric coordinates $\lambda_i$ of the simplex, the P1 basis is $\lambda_i$. The P2 basis is $\lambda_i(2\lambda_i - 1)$ for each vertex and $4\lambda_i\lambda_j$ for the edge between vertices $i$ and $j$. At an edge midpoint, $\lambda_i = \lambda_j = \tfrac12$, the edge function is $1$ and the vertex functions are $0$. The six functions add up to $2(\sum_i\lambda_i)^2 - \sum_i\lambda_i = 1$.

## Examples and non-examples

**P1 on an interval.** On $[x_{i-1}, x_i]$ of length $h$ the two shape functions are linear and the element matrices for $a(u, v) = \int u'v'$ and the mass form $(u, v)$ are

$$A_K = \frac1h\begin{pmatrix} 1 & -1 \\ -1 & 1\end{pmatrix}, \qquad M_K = \frac h6\begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}.$$

**P2 on an interval.** On $[0, 1]$ with nodes $0, \tfrac12, 1$ the basis is $\phi_0 = (1 - x)(1 - 2x)$, $\phi_{1/2} = 4x(1 - x)$ and $\phi_1 = x(2x - 1)$. For example $\phi_{1/2}(\tfrac12) = 4\cdot\tfrac12\cdot\tfrac12 = 1$. On a cell of length $h$, with the local order left, middle, right, the exact element matrices are

$$A_K = \frac1{3h}\begin{pmatrix} 7 & -8 & 1 \\ -8 & 16 & -8 \\ 1 & -8 & 7\end{pmatrix}, \qquad M_K = \frac h{30}\begin{pmatrix} 4 & 2 & -1 \\ 2 & 16 & 2 \\ -1 & 2 & 4\end{pmatrix}.$$

The rows of $A_K$ add up to zero because constants have zero derivative. The entries of $M_K$ add up to $h$, the length of the cell, because the basis functions add up to $1$.

**An interpolation error by hand.** Interpolate $u = x^3$ on $[0, 1]$ by one P2 element. The nodal values are $0, \tfrac18, 1$, so $I u = \tfrac18\phi_{1/2} + \phi_1 = \tfrac32x^2 - \tfrac12x$ and $u - Iu = x(x - \tfrac12)(x - 1)$, the node polynomial. Its maximum size is $\sqrt3/36 \approx 0.0481$, at $x = \tfrac12 \pm \tfrac1{2\sqrt3}$.

**Convergence rates.** For $-u'' = \pi^2\sin(\pi x)$ on $(0, 1)$ with $u(0) = 0$ and $u(1) = 1$, so $u = \sin(\pi x) + x$, the Galerkin solutions on $n$ equal cells give these errors. The code is the 1D solver of [finite element assembly](/finite-element-assembly/).

| $n$ | P1, $\Vert u - u_h\Vert_0$ | P1, $\vert u - u_h\vert_1$ | P2, $\Vert u - u_h\Vert_0$ | P2, $\vert u - u_h\vert_1$ |
|---|---|---|---|---|
| 4 | 3.928e-02 | 4.985e-01 | 1.952e-03 | 5.062e-02 |
| 8 | 9.921e-03 | 2.512e-01 | 2.457e-04 | 1.274e-02 |
| 16 | 2.487e-03 | 1.258e-01 | 3.076e-05 | 3.190e-03 |
| 32 | 6.220e-04 | 6.295e-02 | 3.847e-06 | 7.978e-04 |

The observed orders from the last two rows are $2.00$ and $1.00$ for P1 and $3.00$ and $2.00$ for P2, as the estimates $\|u - u_h\|_0 \le Ch^{k+1}|u|_{k+1}$ and $|u - u_h|_1 \le Ch^k|u|_{k+1}$ predict. For the same number of unknowns, P2 on 16 cells (33 nodes) is about 20 times more accurate in $L^2$ than P1 on 32 cells (33 nodes).

**Non-example: discontinuous elements.** The same $\mathcal{P}_k$ with nodes strictly inside each cell gives a space of discontinuous functions. It is not a subspace of $H^1$, and it needs the [discontinuous Galerkin](/discontinuous-galerkin-method/) weak form.

**Non-example: a hanging node.** Split one of two neighboring triangles so that a new vertex sits at the midpoint of the shared edge, but not the other. Gluing P1 elements by nodes gives a function that is not continuous along that edge, unless the value at the hanging node is constrained to the mean of the values at the two ends of the edge.

**Non-example: wrong nodes.** Six nodes on a triangle that lie on one conic do not determine a quadratic. The [Ciarlet finite element](/ciarlet-finite-element/) page gives an example.

## Related definitions

- **[Ciarlet finite element](/ciarlet-finite-element/).** The general triple of which the Lagrange element is the case with point values as degrees of freedom.
- **Hermite elements.** Add derivative values to the degrees of freedom, for $C^1$ continuity in one dimension or for plates.
- **Spectral elements.** Use $\mathcal{Q}_k$ with Gauss-Lobatto-Legendre nodes in place of equispaced ones, which keeps the basis well conditioned for large $k$ and makes nodal quadrature accurate. See [spectral element method](/spectral-element-method/) and [Gauss-Lobatto quadrature](/gauss-lobatto-quadrature/).
- **Hierarchical bases.** Span the same $\mathcal{P}_k$ with a basis in which raising $k$ adds functions and keeps the old ones, as the [hp finite element method](/hp-finite-element-method/) needs.
- **[Isoparametric elements](/isoparametric-mapping/).** Use the Lagrange basis of degree $k$ also to map the reference cell, which gives curved cells.

## References
