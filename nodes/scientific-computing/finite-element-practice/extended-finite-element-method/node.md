---
tag: R1XMNZ
kind: algorithm
slug: extended-finite-element-method
name: Extended finite element method
aliases:
- XFEM
- X-FEM
area: scientific-computing/finite-element-practice
level: advanced
summary: Enriches the approximation through a partition of unity with discontinuous and singular functions, so cracks can grow without remeshing.
model: real-ram
complexity:
  vars: {n: the number of nodes of the one dimensional mesh}
  time: {worst: "Θ(n)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, iterative: false, mesh_independent_of_discontinuity: true, partition_of_unity_enrichment: true, symmetric_stiffness: true, keeps_nodal_values_with_shifted_enrichment: true}
history:
  year: 1999
  people: [T. Belytschko, T. Black, N. Moës, J. Dolbow, J. M. Melenk, I. Babuška]
  note: Melenk and Babuška in 1996 gave the partition of unity method. Belytschko and Black in 1999 enriched elements near a crack with the crack tip fields, and Moës, Dolbow and Belytschko in 1999 added the jump function and named the method.
prereqs: [finite-element-method, partition-of-unity, lagrange-finite-element]
see_also: [level-set-method, cut-finite-element-method, element-free-galerkin-method, nitsche-method, patch-test, virtual-element-method, boundary-element-method]
sources:
  - paper: "doi:10.1002/(SICI)1097-0207(19990620)45:5<601::AID-NME598>3.0.CO;2-S"
    title: T. Belytschko and T. Black, Elastic crack growth in finite elements with minimal remeshing, International Journal for Numerical Methods in Engineering 45(5) (1999) 601-620
    locator: the enrichment of the nodes near a crack tip with the asymptotic crack tip fields through the partition of unity of the element shape functions
  - paper: "doi:10.1002/(SICI)1097-0207(19990910)46:1<131::AID-NME726>3.0.CO;2-J"
    title: N. Moës, J. Dolbow and T. Belytschko, A finite element method for crack growth without remeshing, International Journal for Numerical Methods in Engineering 46(1) (1999) 131-150
    locator: the jump enrichment of the nodes whose support the crack cuts, the four branch functions at the tip, and crack growth on a fixed mesh
  - paper: doi:10.1016/S0045-7825(96)01087-0
    title: J. M. Melenk and I. Babuška, The partition of unity finite element method, basic theory and applications, Computer Methods in Applied Mechanics and Engineering 139(1-4) (1996) 289-314
    locator: the approximation theorem, local approximation spaces glued by a partition of unity give a global space with the same accuracy
  - paper: doi:10.1016/S0045-7825(03)00346-3
    title: N. Moës, M. Cloirec, P. Cartraud and J.-F. Remacle, A computational approach to handle complex microstructure geometries, Computer Methods in Applied Mechanics and Engineering 192(28-30) (2003) 3163-3177
    locator: the ridge enrichment for material interfaces defined by a level set, and its optimal convergence
  - paper: doi:10.1002/nme.2914
    title: T. P. Fries and T. Belytschko, The extended/generalized finite element method, an overview of the method and its applications, International Journal for Numerical Methods in Engineering 84(3) (2010) 253-304
    locator: the shifted enrichment, blending elements, the integration of enriched functions, conditioning, and the list of applications
---

The extended finite element method (XFEM) puts a crack, a material interface or another known feature of the solution into a finite element space without making the mesh follow it. The standard shape functions $N_I$ form a partition of unity, $\sum_I N_I = 1$. XFEM multiplies some of them by an enrichment function $\psi$ that has the known feature, for example a jump across the crack or a kink at the interface, and adds the products to the space with new unknowns $a_I$. Only the nodes whose support the feature touches get the extra unknowns. The Galerkin method then works in this larger space with the normal weak form, and the quadrature splits the cut elements along the feature. When the crack grows, only the set of enriched nodes and the enrichment change. The mesh stays the same, which is the main gain over remeshing.

## In plain words

A finite element mesh is a set of small pieces, and inside each piece the solution is a simple smooth shape. A crack makes the solution jump, and a smooth shape cannot jump inside a piece. The usual remedy is to cut the mesh along the crack, which is hard when the crack grows. XFEM keeps the mesh. In each piece that the crack cuts, it adds a second shape that has the jump in it, so the piece can now show a jump at the right place. A piece that the crack does not touch stays as it was. When the crack grows into the next piece, that piece also gets the extra shape, and nothing else changes.

## The problem

**Input.** A domain with a mesh of standard finite elements, a known curve (a point in one dimension) where the solution has a jump, a kink or a singularity, and a linear elliptic problem, here the bar equation $-(E u')' = f$ on $(0, L)$ with $u(0) = u_0$ and $u(L) = u_L$. The stiffness is $E = E_1$ for $x < c$ and $E = E_2$ for $x > c$.

**Output.** A Galerkin approximation $u_h$ that has the feature at $x = c$ for any position of $c$ in the mesh.

**The two features of the reference code.**

- **Cohesive crack.** The bar is cut at $c$, $u$ can jump there, the force $\sigma = E u'$ is continuous, and a spring of stiffness $k$ transmits it: $\sigma(c) = k\,[u]$ with $[u] = u(c^+) - u(c^-)$. The weak form is $\int_0^L E u' v'\,dx + k\,[u][v] = \int_0^L f v\,dx$ for all $v$ with $v(0) = v(L) = 0$, where $v$ may jump at $c$.
- **Material interface.** $u$ is continuous at $c$ and $u'$ jumps, because $E$ jumps and $E u'$ is continuous. The weak form is the standard one in $H^1$.

**The enriched space.** With the level set $\varphi(x) = x - c$, let $e$ be the cut element $[x_e, x_{e+1}]$ that contains $c$, and let $\mathcal J = \{e, e+1\}$ be its nodes. Then

$$u_h(x) = \sum_I N_I(x)\,u_I + \sum_{I \in \mathcal J} N_I(x)\,\psi_I(x)\,a_I,$$

with the shifted Heaviside function $\psi_I(x) = H(\varphi(x)) - H(\varphi(x_I))$ for the crack and the ridge function $\psi(x) = \sum_{J \in \mathcal J} N_J(x)\,|\varphi(x_J)| - |\varphi(x)|$ of Moës, Cloirec, Cartraud and Remacle for the interface. Both enrichments are zero at every node, so $u_h(x_I) = u_I$ and the Dirichlet values are set on $u_I$ as usual. In two and three dimensions, the nodes of the elements that contain a crack tip also get the four branch functions $\sqrt r\,\{\sin\frac\theta2, \cos\frac\theta2, \sin\frac\theta2\sin\theta, \cos\frac\theta2\sin\theta\}$ of the asymptotic crack tip field.

## The algorithm

```pseudo id=main
XFEM-1D(nodes, c, kind, E, f, u_0, u_L, k)
L1  find the element e with x_e < c < x_{e+1}; enrich its two nodes with one new unknown each
L2  for each element, split it at c if c is inside, else keep it whole
L3      at each Gauss point of each piece, evaluate N_I, N_I psi_I and their derivatives
L4      add w E (phi_i)' (phi_j)' to K and w f phi_i to F for all pairs of nonzero functions
L5  for a cohesive crack, add k [phi_i] [phi_j] to K, where [N_I psi_I] = N_I(c)
L6  set u_1 = u_0 and u_n = u_L, and solve K z = F for the other unknowns
L7  u_h(x) <- sum of N_I(x) u_I + sum over enriched I of N_I(x) psi_I(x) a_I
L8  return u_h
```

Line L2 is what makes the quadrature correct. The enriched functions have a jump or a kink at $c$, so a Gauss rule on the whole element would integrate them with an error that does not go away. On each piece the integrands of $K$ are polynomials of degree at most 2, and the two point Gauss rule is exact up to degree 3. Line L5 uses that the jump of $N_I\,\psi_I$ at $c$ is $N_I(c)\,(1 - 0) = N_I(c)$ for both nodes of the cut element.

## Example

**One element with a cohesive crack.** Take the mesh $\{0, 1\}$, $c = \tfrac12$, $E = 1$, $k = 2$, $f = 0$, $u(0) = 0$ and $u(1) = 1$. The enriched functions are $N_0 H$ and $N_1 (H - 1)$, with derivatives $-H$ and $H - 1$. Their stiffness entries are $\int_{1/2}^1 1\,dx = \tfrac12$, $\int_0^{1/2} 1\,dx = \tfrac12$ and $0$ for the pair. The jumps at $c$ are $N_0(\tfrac12) = N_1(\tfrac12) = \tfrac12$, so line L5 adds $2 \cdot \tfrac14 = \tfrac12$ to all four entries. The coupling with $u_1 = 1$ is $\int (-H)\cdot 1\,dx = -\tfrac12$ and $\int (H - 1)\cdot 1\,dx = -\tfrac12$. The system is

$$\begin{pmatrix} 1 & \tfrac12 \\ \tfrac12 & 1 \end{pmatrix}\begin{pmatrix} a_0 \\ a_1 \end{pmatrix} = \begin{pmatrix} \tfrac12 \\ \tfrac12 \end{pmatrix}, \qquad a_0 = a_1 = \tfrac13.$$

Then $u_h = (1 - a_1)\,x = \tfrac23 x$ to the left of the crack and $u_h = x + a_0 (1 - x) = \tfrac23 x + \tfrac13$ to the right. This is the exact solution: the force is $\sigma = 1/(1 + 1/k) = \tfrac23$ and the jump is $\sigma/k = \tfrac13$. One element without remeshing holds the crack.

**Two elements with an interface.** Take the mesh $\{0, \tfrac12, 1\}$, $c = 0.3$, $E_1 = 1$, $E_2 = 4$, $f = 0$, $u(0) = 0$ and $u(1) = 1$. The exact force is $\sigma = 1/(0.3 + 0.7/4) = \tfrac{40}{19}$ and $u(\tfrac12) = \sigma\,(0.3 + 0.2/4) = \tfrac{14}{19} \approx 0.7368$. Standard linear elements on the same mesh, with the stiffness integrated exactly, give $u_{1} = 8/12.4 = \tfrac{20}{31} \approx 0.6452$. XFEM with the ridge enrichment gives $\tfrac{14}{19}$ and is exact everywhere.

**Convergence.** The reference tests take $c = \tfrac13$, $E_1 = 1$, $E_2 = 10$ and uniform meshes with $n$ elements. The table shows the energy norm error $\big(\int E\,(u_h' - u')^2\big)^{1/2}$ and the observed order per halving of $h$.

| $n$ | XFEM, $f = 0$ | standard, $f = 0$ | XFEM, $f = 1$ | standard, $f = 1$ |
|---|---|---|---|---|
| 4 | $1.1 \times 10^{-15}$ | $0.692$ | $0.0404$ | $0.0413$ |
| 16 | $1.6 \times 10^{-14}$ | $0.323$ (order $0.55$) | $0.0111$ (order $0.93$) | $0.0143$ (order $0.77$) |
| 64 | $3.0 \times 10^{-14}$ | $0.159$ (order $0.51$) | $0.00283$ (order $0.99$) | $0.00582$ (order $0.65$) |
| 256 | $2.9 \times 10^{-13}$ | $0.0793$ (order $0.50$) | $0.000712$ (order $1.00$) | $0.00271$ (order $0.55$) |

XFEM keeps the optimal order 1 of linear elements. Standard elements drop to order $\tfrac12$, because one element must fit a kinked function with a straight line.

## Correctness

The [proof](proofs/correctness.md) has four steps. First, on the cut element the four functions $N_e, N_{e+1}, N_e\psi_e, N_{e+1}\psi_{e+1}$ of the crack span exactly the functions that are linear on each side of $c$, with any jump. The ridge space contains every continuous function that is linear on each side. Both sets of functions are linearly independent, so the stiffness matrix is nonsingular. Second, the bilinear form is symmetric and coercive, so the Galerkin solution is the best approximation in the energy norm ([Céa's lemma](/cea-lemma/) with constant 1). Third, for $f = 0$ the exact solution is linear on each side of $c$, so it lies in the space and XFEM returns it to rounding error for any position of $c$. Fourth, for a load $f$, the function that interpolates $u$ at the nodes and at $c^\pm$ lies in the space, and the interpolation error on each piece gives the bound $\|u - u_h\|_E \le \sqrt{E_{\max}}\,(h/\pi)\,\|u''\|$, which is order 1 in $h$.

## Complexity

In one dimension each element has at most four nonzero functions and only one element is enriched, so assembly takes $\Theta(n)$ time. The matrix is banded except for the two enriched rows, which couple only to the two nodes of the cut element, so a banded or sparse solver takes $\Theta(n)$ time and memory. The reference code uses dense Gaussian elimination that skips zero multipliers, which takes $\Theta(n^2)$ time and $\Theta(n^2)$ memory. In two dimensions a crack through a mesh with $n$ nodes enriches about $\sqrt n$ nodes with the jump and a fixed number of nodes with the 4 branch functions. The cost is that of a standard finite element solve with a few more unknowns, plus the subdivision of the cut elements for quadrature.

## Properties

- **The mesh does not follow the discontinuity.** The position of $c$ enters only through the choice of enriched nodes, the enrichment and the quadrature split. Crack growth changes these and nothing else.
- **Conforming for the interface.** The ridge enrichment is continuous and zero outside the cut element, so the space is a subspace of $H^1$ and the method is a standard conforming Galerkin method.
- **Nodal values keep their meaning.** With shifted enrichments, $u_h(x_I) = u_I$. The Dirichlet values are set as in standard finite elements, and post processing at the nodes needs no correction.
- **Symmetric positive definite.** The stiffness matrix is symmetric, and positive definite on the free unknowns when the enrichment is linearly independent of the standard functions.
- **No blending problem in one dimension.** Here the enrichment is zero outside the cut element. In two dimensions, elements where only some nodes are enriched (blending elements) do not reproduce the enrichment and can reduce the order.

## Variants and improvements

- **Crack tip enrichment.** In 2D and 3D linear fracture, the nodes near the tip also get the four branch functions. With enrichment in a fixed radius around the tip (geometric enrichment), not only in the tip element, the order of convergence is optimal.
- **Generalized finite element method (GFEM).** The same partition of unity idea with enrichments taken from local numerical solutions or from analytic solutions of local problems, as in Melenk and Babuška.
- **Level set description.** Two level sets describe a crack in 2D or 3D, one for the crack surface and one for its front. The [level set method](/level-set-method/) or the [fast marching method](/fast-marching-method/) moves them as the crack grows.
- **Stable GFEM.** Babuška and Banerjee subtract the interpolant of the enrichment from the enrichment. This keeps the condition number close to that of standard elements when the feature is near a node.
- **Cut finite element method.** The [cut finite element method](/cut-finite-element-method/) also leaves the mesh fixed but doubles the unknowns of the cut elements and imposes the interface conditions weakly with [Nitsche's method](/nitsche-method/) and a ghost penalty for stability.

## When to use it

Use XFEM when a crack, a material interface, a void or a contact surface moves through a fixed mesh, or when the mesh of a complex microstructure would be hard to make conforming. It is common for crack growth in 2D and 3D linear fracture mechanics, for inclusions and voids in composite materials, and for two phase flow with a level set interface. If the feature does not move and a conforming mesh is easy to make, standard finite elements with the mesh on the interface are simpler and have no quadrature or conditioning issues.

## Pitfalls

- **Quadrature over cut elements.** Gauss points on the whole cut element integrate the jump and the kink with an error that does not converge. Split the element along the feature (line L2), or use a quadrature that adapts to it.
- **Conditioning when the feature is near a node.** If $c$ is close to a node, the enriched functions are almost zero, and the matrix is nearly singular. In the reference test with 4 elements, $E_2 = 10$ and $c = \tfrac12 + \varepsilon$, the small diagonal entry of the ridge unknowns is $4.8 \times 10^{-3}$ at $\varepsilon = 10^{-2}$, $5.3 \times 10^{-11}$ at $\varepsilon = 10^{-6}$ and $5.3 \times 10^{-19}$ at $\varepsilon = 10^{-10}$, and the error goes from $2 \times 10^{-16}$ to $1.2 \times 10^{-9}$. Remove the enrichment of nodes whose cut part is very small, or scale the unknowns.
- **Blending elements.** In 2D and 3D, elements with some enriched and some standard nodes do not form a partition of unity for the enrichment. The error there can reduce the order. Corrected or shifted enrichments and the ridge function reduce this effect.
- **Unshifted enrichment.** Without the shift, $u_h(x_I) \ne u_I$, so the Dirichlet values and the nodal output need a correction. The space is the same, so the answer does not change if this is done right.
- **Crack tip singularity in a plain Heaviside model.** A jump enrichment alone puts the tip at an element edge and misses the $\sqrt r$ field. Stress intensity factors from such a model are wrong unless the tip is enriched or the mesh is very fine.

## Implementations

## History

Melenk and Babuška in 1996 proved that local approximation spaces glued by a partition of unity give a global space with the same local accuracy, and called it the partition of unity method. Belytschko and Black in 1999 used this idea to enrich the elements near a crack with the asymptotic crack tip fields, so a crack needed only a small amount of remeshing. Moës, Dolbow and Belytschko in the same year added the Heaviside enrichment for the crack faces, removed the remeshing completely and named the method the extended finite element method. The level set descriptions of cracks and interfaces, the ridge enrichment of Moës and coauthors in 2003, and the work on blending and conditioning followed. The overview of Fries and Belytschko from 2010 lists the main variants and applications.

## References
