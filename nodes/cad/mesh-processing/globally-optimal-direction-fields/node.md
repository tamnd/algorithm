---
tag: 8TE408
kind: algorithm
slug: globally-optimal-direction-fields
name: Globally optimal direction fields
aliases:
- Knoppel direction fields
- n-direction field design
area: cad/mesh-processing
level: research
summary: Knöppel, Crane, Pinkall and Schröder's smoothest n-direction fields on a surface, found as the eigenvector of the smallest eigenvalue of one sparse Hermitian matrix.
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of inverse iteration steps}
  time: {dense: O(n^3 + k n^2), nested_dissection: O(n^(3/2) + k n log n)}
  space: {dense: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2013
  people: [Felix Knöppel, Keenan Crane, Ulrich Pinkall, Peter Schröder]
  note: Knöppel, Crane, Pinkall and Schröder showed in ACM Transactions on Graphics in 2013 that the smoothest n-direction field, in a relaxed form, is the eigenvector of the smallest eigenvalue of a Hermitian matrix.
prereqs: [cross-field, rayleigh-quotient, inverse-iteration, cotangent-laplacian, discrete-gaussian-curvature]
see_also: [mixed-integer-quadrangulation, curvature-tensor-estimation, generalized-eigenvalue-problem, spectral-theorem, power-iteration, cholesky-decomposition, discrete-gauss-bonnet-theorem, cut-graph]
sources:
  - paper: doi:10.1145/2461912.2462005
    title: Felix Knöppel, Keenan Crane, Ulrich Pinkall and Peter Schröder, Globally optimal direction fields, ACM Transactions on Graphics 32(4), Article 59, 2013
    locator: the n-th power representation, the quadratic smoothness energy with the discrete connection, the relaxation of the unit length condition to one global norm, and the smallest eigenvector computed by inverse iteration
  - paper: doi:10.1145/1356682.1356683
    title: Nicolas Ray, Bruno Vallet, Wan Chiu Li and Bruno Lévy, N-symmetry direction field design, ACM Transactions on Graphics 27(2), Article 10, 2008
    locator: the representation of N-symmetry fields by angles and period jumps, and the index of a singularity
  - paper: doi:10.1111/cgf.12864
    title: Amir Vaxman, Marcel Campen, Olga Diamanti, Daniele Panozzo, David Bommes, Klaus Hildebrandt and Mirela Ben-Chen, Directional field synthesis, design, and processing, Computer Graphics Forum 35(2), 545-572, 2016
    locator: the survey of power vector representations, connection Laplacians and the eigenvector method among the field design methods
---

A smooth field of $n$ directions on a surface, such as a [cross field](/cross-field/) with $n = 4$, usually cannot exist without singular points, and searching over where to put them is a hard combinatorial problem. Knöppel, Crane, Pinkall and Schröder removed the combinatorial part. They store the field at each vertex as one complex number, the $n$-th power of a direction, so that the smoothness energy becomes a Hermitian quadratic form, and they replace the unit length condition at each vertex by one condition on the whole field. The smoothest field is then the eigenvector of the smallest eigenvalue, the minimizer of a [Rayleigh quotient](/rayleigh-quotient/), and [inverse iteration](/inverse-iteration/) finds it with one matrix factorization. The singularities appear where the field passes through zero, with no search.

## In plain words

Picture a field of small crosses drawn on a curved surface, for example to guide where the lines of a grid go. Neighbouring crosses should line up as well as the curvature allows.

Each cross is stored as one turning number that does not care which of its four arms comes first. Then the mismatch between neighbours is a simple sum of squares.

Asking every cross to have full size at once makes the problem hard. So the method only asks that the crosses be large on average, and it may shrink some of them. The best answer to this easier question is the first natural mode of one big table of numbers, and a few rounds of repeated solving find it. The places where the crosses shrink to nothing are the unavoidable defects, and the method puts them there by itself.

## The problem

The input is a connected, oriented [manifold mesh](/manifold-mesh/) of triangles with $V$ vertices, with faces oriented by the right-hand rule, and an integer $n \ge 1$. The output is an $n$-direction field at the vertices that is as smooth as possible, with its singularities.

**Frames and transport.** At a vertex $i$ with corner angles $\alpha$ around it, scale the angles by $s_i = 2\pi / \sum\alpha$ at an inner vertex and $s_i = 1$ at a boundary vertex. Measure the direction of each edge $ij$ at $i$ by the angle $\varphi_i(j)$ from one chosen edge at $i$, adding the scaled corner angles counterclockwise. The scaled angles at an inner vertex add up to $2\pi$, so this is a full turn of directions in the tangent plane of $i$. Moving from $i$ to $j$ along the edge, the direction of the edge turns from $\varphi_i(j)$ to $\varphi_j(i) + \pi$, so a direction at angle $\theta$ at $i$ is carried to $\theta + \varphi_j(i) + \pi - \varphi_i(j)$ at $j$. This is the discrete transport along the edge.

**Representation.** The $n$ directions at angles $\theta, \theta + 2\pi/n, \dots$ at a vertex are stored as one complex number $u_i = e^{in\theta}$, which does not depend on which of the $n$ directions is called $\theta$. Transport along $ij$ multiplies it by

$$r_{ij} = e^{in(\varphi_j(i) + \pi - \varphi_i(j))}.$$

**Energy.** With the cotangent weights $w_{ij} = \frac12(\cot\alpha_{ij} + \cot\beta_{ij})$ of the [cotangent Laplacian](/cotangent-laplacian/), the energy of a field $u \in \mathbb{C}^V$ is

$$E(u) = \sum_{\text{edges } ij} w_{ij} \lvert u_j - r_{ij} u_i \rvert^2 = u^* A u,$$

where $A$ is Hermitian, with $A_{ii} = \sum_j w_{ij}$ and $A_{ji} = -w_{ij} r_{ij}$, $A_{ij} = -w_{ij}\bar r_{ij}$. It is zero exactly when every value is the transport of its neighbour, a parallel field.

**Relaxation.** The real problem asks for $\lvert u_i\rvert = 1$ at every vertex, which is not convex. The relaxed problem asks only for $u^* M u = 1$, where $M$ is the diagonal matrix of vertex areas (one third of the areas of the triangles at the vertex):

$$\min_{u \ne 0} \frac{u^* A u}{u^* M u}.$$

The answer of the relaxed problem is normalized afterwards to unit length at the vertices where it is not zero, and its zeros are the singularities.

## The algorithm

```pseudo id=main
SmoothestField(M, n, ε, δ)
L1  for each vertex i: the frame angles φ_i(j) of its edges, with corner angles scaled by s_i
L2  for each edge ij: r_ij ← e^{in(φ_j(i) + π − φ_i(j))},  w_ij ← (cot α_ij + cot β_ij)/2
L3  A ← Σ over edges of w_ij |u_j − r_ij u_i|^2 written as a Hermitian matrix
L4  M ← diag(vertex areas)
L5  factor A + σM = L L^*, with σ = ε · max A_ii / max M_ii    ▷ Cholesky, once
L6  u ← a random complex vector
L7  repeat:  solve L L^* y = M u
L8           u ← y / sqrt(y^* M y)
L9           λ ← u^* A u
L10 until |A u − λ M u| in the M^{-1} norm ≤ δ · max(1, λ)
L11 return u, λ
```

Lines L1 to L4 build the problem in $O(V)$ time. Line L5 adds a tiny multiple of $M$ so that the matrix is positive definite even when $\lambda_1 = 0$, which happens when a parallel field exists. Lines L7 and L8 are one step of inverse iteration on the pencil $A - \lambda M$: a solve with the fixed factor and a normalization. Line L10 stops when the pair $(u, \lambda)$ is an eigenpair up to $\delta$. The directions at a vertex are the $n$-th roots of $u_i / \lvert u_i\rvert$.

**Singularities.** The code of this page reads the index of the field in each face $f$ with vertices $p_0, p_1, p_2$ counterclockwise:

$$I(f) = \frac{n K_f + \sum_{c} \tau_c}{2\pi n}, \qquad K_f = \sum_c s_{p_c} \alpha_c - \pi, \qquad \tau_c = \arg\frac{u_{p_{c+1}}}{r_{p_c p_{c+1}} u_{p_c}} \in (-\pi, \pi].$$

$K_f$ is the curvature of the scaled frames in $f$, and $\tau_c$ is the turn from the transported value to the next value. $I(f)$ is a multiple of $1/n$, and on a closed mesh the indices add up to $\chi = V - E + F = 2 - 2g$. The faces with $I(f) \ne 0$ are the singularities.

## Example

**The regular octahedron with $n = 4$.** Each vertex has four angles of $60°$, so $s = 2\pi / (4\pi/3) = 3/2$, and each face has $K_f = 3 \cdot \tfrac32 \cdot \tfrac{\pi}{3} - \pi = \pi/2$. Transport once around a face multiplies $u$ by $e^{-4iK_f} = e^{-2\pi i} = 1$, so a parallel cross field exists, $\lambda_1 = 0$, and the code finds it in 2 steps. Every face has the index $(4 \cdot \pi/2 + 0)/(8\pi) = 1/4$, and the 8 faces give $2 = \chi$. With $n = 1$ or $n = 2$ the transport around a face is not trivial, there is no parallel field, and the code returns $\lambda_1 = 1.0$ in both cases.

**The regular icosahedron.** Five angles of $60°$ meet at each vertex, so $s = 6/5$ and $K_f = \pi/5$, and the transport around a face is trivial only for $n$ a multiple of 10. The code returned:

| $n$ | $\lambda_1$ | steps | singular faces | indices |
|---|---|---|---|---|
| 1 | $0.2763932$ | 17 | 2 | $1, 1$ |
| 2 | $0.4763932$ | 24 | 4 | $\tfrac12$ four times |
| 4 | $0.5527864$ | 43 | 8 | $\tfrac14$ eight times |

The indices add up to 2 in every row. A vector field gets two singularities of index 1, like the poles of a sphere, and a cross field gets eight of index $1/4$, like the corners of a cube. The eigenvalues agree to $10^{-9}$ with the smallest eigenvalue from a dense Jacobi eigenvalue computation, in the tests.

**Measured on finer meshes.** Icosahedra subdivided once (42 vertices, 80 faces) and twice (162 vertices, 320 faces), projected to the unit sphere, or to an ellipsoid with half axes $1, 1, 0.5$, with seed 0, $\varepsilon = 10^{-8}$, $\delta = 10^{-10}$, dense factorization in pure Python:

| mesh | $n$ | $\lambda_1$ | steps | singular faces | quotient of the unit field |
|---|---|---|---|---|---|
| sphere, 42 | 1 | 0.99968 | 16 | 2 of index 1 | 1.98 |
| sphere, 42 | 4 | 3.41685 | 417 | 8 of index 1/4 | 4.39 |
| sphere, 162 | 1 | 1.00003 | 16 | 2 of index 1 | 2.41 |
| sphere, 162 | 2 | 1.97753 | 18 | 4 of index 1/2 | 4.03 |
| sphere, 162 | 4 | 3.84255 | 1679 | 8 of index 1/4 | 6.68 |
| ellipsoid, 42 | 1 | 1.40211 | 3925 | 2 of index 1 | 3.07 |
| ellipsoid, 162 | 2 | 2.28189 | 6847 | 4 of index 1/2 | 6.18 |

On the 162 vertex ellipsoid with $n = 4$ the residual did not reach $\delta$ in 10000 steps. The large step counts come from the second smallest eigenvalue being very close to the first on these symmetric shapes. The last column is the Rayleigh quotient after each $u_i$ is set to unit length. It is always at least $\lambda_1$, and here it is 1.3 to 2.7 times $\lambda_1$. These numbers are measurements on these meshes, not bounds.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows the following.

1. $E(u) = u^* A u$ with $A$ Hermitian, and $A$ is positive semidefinite when all weights $w_{ij}$ are positive.
2. **Key invariant.** The minimum of $u^* A u / u^* M u$ over $u \ne 0$ is the smallest eigenvalue $\lambda_1$ of $Au = \lambda M u$, and it is reached exactly by the eigenvectors of $\lambda_1$. The proof writes $v = M^{1/2} u$ and uses the [spectral theorem](/spectral-theorem/) for the Hermitian matrix $M^{-1/2} A M^{-1/2}$. This is a [generalized eigenvalue problem](/generalized-eigenvalue-problem/).
3. If the random start has a nonzero part in the eigenspace of $\lambda_1$, which happens with probability 1, inverse iteration converges to that eigenspace. If $\lambda_2$ is the next distinct eigenvalue, the rest shrinks by the factor $(\lambda_1 + \sigma) / (\lambda_2 + \sigma)$ per step.
4. A returned pair has $u^* M u = 1$, $\lambda = u^* A u \ge \lambda_1$, and an eigenvalue within $\delta \max(1, \lambda)$ of $\lambda$.
5. The face indices are multiples of $1/n$, and on a closed mesh they add up to $\chi$.

So the code solves the relaxed problem exactly, up to the stopping test. It does not solve the problem with $\lvert u_i\rvert = 1$: the unit field made from the eigenvector is not proved to be the smoothest unit field, and in the measurements its Rayleigh quotient is 1.3 to 2.7 times $\lambda_1$.

## Complexity

Lines L1 to L4 take $O(V)$ time. With a dense factorization, as in the code, line L5 takes $O(V^3)$ time and $O(V^2)$ space once, and each step of lines L7 to L10 takes $O(V^2)$. For $k$ steps the total is $O(V^3 + k V^2)$. $A$ has one nonzero entry per vertex and two per edge, so a sparse [Cholesky factorization](/cholesky-decomposition/) with [nested dissection](/nested-dissection/) on the planar mesh graph takes $O(V^{3/2})$ time and $O(V \log V)$ space, and each solve then takes $O(V \log V)$. The factor is computed once, which is why one eigenvector is about as cheap as one linear solve when $k$ is small. The number $k$ depends on the gap between the two smallest eigenvalues and is not bounded in advance.

## Properties

- **Proved.** The eigenvector of the smallest eigenvalue minimizes the energy among all fields with $u^* M u = 1$, the relaxed problem. This optimum is global: every local minimum of the quotient is an eigenvector of $\lambda_1$.
- **Proved.** The returned $\lambda$ is at least $\lambda_1$, and the residual test certifies an eigenvalue within $\delta \max(1, \lambda)$.
- **Proved.** The face indices are multiples of $1/n$ and add up to $\chi$ on a closed mesh.
- **Not proved.** The unit field made from the eigenvector is not proved to be the smoothest unit field. It is optimal for the relaxed problem only.
- **Measured.** On flat disks of 19 vertices (seeds 0 to 2) the code returns $\lambda_1 < 10^{-10}$ and $\lvert u_j - r_{ij} u_i\rvert < 10^{-5}$ on all edges, a parallel field.
- **No integer unknowns.** The singularities, their number and their positions all follow from the eigenvector, with no rounding step.
- **No starting field.** The output does not depend on a starting field or a choice of singularities. Only the random start of inverse iteration enters, and it changes $u$ only by a phase when $\lambda_1$ is simple.

## Variants and improvements

- **Alignment to given directions.** Knöppel et al. also fit the field to a given field $q$, such as the principal curvature directions from [curvature tensor estimation](/curvature-tensor-estimation/), by solving one linear system of the form $(A - \lambda M) u = M q$ with a parameter $\lambda$ below $\lambda_1$ (check the exact form in the paper).
- **Smoothness measures.** The paper describes a family of energies that weigh the Dirichlet energy against a holomorphic or antiholomorphic part, which changes the kind of singularity the field prefers (check).
- **Face based fields.** The same idea works with one value per face and transport across edges, with dual weights. The [cross field](/cross-field/) page gives the index in that form.
- **Other eigensolvers.** The [Lanczos algorithm](/lanczos-algorithm/) or a shift closer to $\lambda_1$ converges faster than plain inverse iteration when the two smallest eigenvalues are close. [Power iteration](/power-iteration/) on $A$ itself would find the largest eigenvalue instead, the roughest field.
- **Quad meshing.** The cross field with $n = 4$ is the input of [mixed-integer quadrangulation](/mixed-integer-quadrangulation/), which cuts the surface along a [cut graph](/cut-graph/) through the singularities.

## When to use it

Use it to design cross fields for quad meshing, line fields for hatching, or vector fields on meshes, when the singularities should be placed automatically and the result should not depend on a starting guess. It needs one sparse factorization, so it scales to large meshes. If the user must control the singularities exactly, or a unit field is required everywhere with no shrinking, a mixed-integer method or a method with fixed singularities is more suitable.

## Pitfalls

- **Negative cotangent weights.** On meshes with obtuse angles, $\cot\alpha + \cot\beta$ can be negative. Then $E$ can take negative values and $A$ is not positive semidefinite, so the Cholesky factorization of line L5 can fail and the minimum loses its meaning. The code raises an error in that case. Use a mesh with the Delaunay property or intrinsic weights.
- **Eigenvalues that are almost equal.** On symmetric shapes the two smallest eigenvalues are almost equal, and inverse iteration then needs thousands of steps, as the ellipsoid rows show. The eigenvalue converges much faster than the eigenvector. A stopping test on the change of $u$ is the slowest. A test on the residual, as in line L10, stops earlier, but any field in the nearly repeated eigenspace is then a valid answer, and the singularities can move between runs with different seeds.
- **No shift.** If $\lambda_1 = 0$, as on the octahedron with $n = 4$ or on a flat disk, $A$ is singular and its Cholesky factorization fails. Add $\sigma M$ with a small $\sigma > 0$, as in line L5.
- **Unscaled angles.** Without the scaling $s_i$, the frame at an inner vertex with angle sum other than $2\pi$ does not close up, and the transport around the vertex is wrong. The scaled angles put the curvature of each vertex into the transport.
- **Reading off the singularities.** The singularities are where $u$ winds around zero, not where $\lvert u\rvert$ is small. Compute the index from the turns and the curvature; the size of $u$ only hints at where they are.

## Implementations

## History

Fields of crosses and other symmetric directions were designed on meshes before 2013 by smoothing angles with integer period jumps, as in the work of Ray, Vallet, Li and Lévy in 2008, and by mixed-integer methods that round the jumps one at a time. These methods need a starting field or a choice of singularities. Felix Knöppel, Keenan Crane, Ulrich Pinkall and Peter Schröder showed in ACM Transactions on Graphics in 2013 that with the $n$-th power representation and one global norm the problem becomes a smallest eigenvalue problem, whose answer is globally optimal and places the singularities by itself. The survey of Vaxman and others in 2016 places the method among the other representations of directional fields.

## References
