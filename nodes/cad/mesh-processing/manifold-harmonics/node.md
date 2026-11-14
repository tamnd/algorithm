---
tag: Q55GWK
kind: technique
slug: manifold-harmonics
name: Manifold harmonics
aliases:
- spectral mesh processing
- Laplace-Beltrami eigenfunctions
area: cad/mesh-processing
level: advanced
summary: Uses the eigenfunctions of the cotangent Laplacian as a Fourier basis on a mesh, as Vallet and Levy did, for filtering, compression and shape descriptors.
prereqs: [cotangent-laplacian, generalized-eigenvalue-problem, discrete-fourier-transform]
see_also: [laplacian-smoothing, taubin-smoothing, implicit-fairing, spectral-clustering, lanczos-algorithm, heat-method, finite-element-method, laplacian-surface-editing]
sources:
  - paper: doi:10.1111/j.1467-8659.2008.01122.x
    title: Bruno Vallet and Bruno Lévy, Spectral geometry processing with manifold harmonics, Computer Graphics Forum 27(2) (Eurographics 2008), 251 to 260
    locator: the manifold harmonic basis as the eigenvectors of the discrete Laplace-Beltrami operator, its orthonormality for the mass matrix, the manifold harmonic transform and its inverse, the filtering of the geometry with transfer functions, and the computation of the eigenvectors band by band
  - paper: doi:10.1145/218380.218473
    title: Gabriel Taubin, A signal processing approach to fair surface design, SIGGRAPH 1995, 351 to 358
    locator: the eigenvectors of the mesh Laplacian as the natural frequencies of a mesh, smoothing as a low-pass filter, and the two-step filter that does not shrink the mesh
  - paper: doi:10.1145/344779.344924
    title: Zachi Karni and Craig Gotsman, Spectral compression of mesh geometry, SIGGRAPH 2000, 279 to 286
    locator: the projection of the vertex coordinates on the eigenvectors of the combinatorial mesh Laplacian, the truncation of the coefficients for compression, and the partition of large meshes into patches
  - paper: doi:10.1016/j.cad.2005.10.011
    title: Martin Reuter, Franz-Erich Wolter and Niklas Peinecke, Laplace-Beltrami spectra as Shape-DNA of surfaces and solids, Computer-Aided Design 38(4), 2006, 342 to 366
    locator: the beginning of the Laplace-Beltrami spectrum, computed with finite elements, as a signature of a shape that does not change under isometries
---

Manifold harmonics is a technique that does Fourier analysis on a curved surface. On a line or a circle, the sines and cosines are the eigenfunctions of the second derivative, and their frequencies are the eigenvalues. On a surface, the operator that takes the place of the second derivative is the Laplace-Beltrami operator, and its eigenfunctions are the harmonics of the surface. On a triangle mesh, the [cotangent Laplacian](/cotangent-laplacian/) is the discrete form of this operator. It gives a stiffness matrix $C$ and a mass matrix $M$, and the harmonics are the solutions of the [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $C\phi = \lambda M\phi$. A function on the vertices, such as one coordinate of the vertex positions, then has coefficients $\tilde x_k = \phi_k^{\mathsf T} M x$, and it can be rebuilt as $x = \sum_k \tilde x_k \phi_k$. Small $\lambda$ are the low frequencies, the coarse shape; large $\lambda$ are the fine detail. Vallet and Lévy (2008) built the basis with the mass matrix and called it the manifold harmonic basis. Because the basis is orthonormal in the inner product of $M$, the transform is exactly invertible and has the same properties as the [discrete Fourier transform](/discrete-fourier-transform/), on any mesh and with any sampling.

## In plain words

A guitar string has a set of natural tones: the low base tone and higher tones above it. Any sound of the string is a mix of these tones, and a sound filter changes the mix.

A curved surface also has natural tones. The lowest tone is the same value on the whole surface. The next tones go up on one side and down on the other side. Higher tones make more and smaller waves, like ripples on a drum.

Manifold harmonics finds these tones for a triangle mesh. A value at each vertex, for example the height of each point, is then written as a mix of tones. Keep only the low tones and the mesh becomes smooth. Make the high tones stronger and the details stand out. Keep few tones and the mesh needs little storage. The list of tones also describes the shape.

## When it applies

- The data are values at the vertices of a triangle mesh: the vertex positions, a color, a curvature, a temperature. The positions are treated as three separate signals.
- The task is about frequencies: to smooth, to sharpen, to compress, to compare shapes, or to find a function that changes slowly on the surface.
- The result must not depend on how the mesh is sampled. This needs the cotangent weights and the mass matrix, not the uniform graph [Laplacian](/laplacian-matrix/).
- The number of harmonics needed is small compared with the number of vertices, or the mesh is small enough for a dense eigensolver.

## The template

```pseudo id=main
MANIFOLD-HARMONICS(mesh with vertices p_1..p_n, signal x on the vertices, count m, transfer function h)
L1  C ← the stiffness matrix: C_ij = −(cot α_ij + cot β_ij) / 2 for an edge ij, C_ii = −Σ_{j≠i} C_ij
L2  M ← the mass matrix: the diagonal of the vertex areas, or the finite element mass matrix
L3  (λ_k, φ_k) for k = 1..m ← the m smallest solutions of C φ = λ M φ, with φ_kᵀ M φ_l = 1 if k = l and 0 if not
L4  x̃_k ← φ_kᵀ M x for k = 1..m
L5  y ← Σ_{k=1..m} h(λ_k) x̃_k φ_k
L6  return y
```

**Why it works.** $C$ is symmetric and positive semidefinite: $u^{\mathsf T} C u$ is the Dirichlet energy $\int |\nabla u|^2$ of the piecewise linear function with values $u$, and the cotangent formula of line L1 is exactly this integral. $M$ is symmetric positive definite. So the eigenvalues are real and not negative, and the eigenvectors can be chosen with $\Phi^{\mathsf T} M \Phi = I$, where $\Phi$ has the columns $\phi_k$. Then $\Phi^{-1} = \Phi^{\mathsf T} M$, which is why line L4 multiplies by $M$. The transform is exactly invertible, the M-norm of a signal is the sum of its squared coefficients, and the energy is $x^{\mathsf T} C x = \sum_k \lambda_k \tilde x_k^2$. The partial sum of the first $m$ terms is the closest signal to $x$ that uses only the first $m$ harmonics. On a connected mesh, $\lambda_1 = 0$ and $\phi_1$ is constant. The [proof](proofs/correctness.md) gives the details.

**Line L2.** The mass matrix is the area that each vertex stands for. A diagonal ("lumped") mass gives each vertex one third of the area of its triangles, or its mixed Voronoi area; the finite element mass has $M_{ij} = \int \varphi_i \varphi_j$ for the hat functions $\varphi_i$. Both are symmetric positive definite when all triangles have positive area. Without $M$, the eigenvectors of $C$ alone depend on the density of the vertices: a part of the mesh with many small triangles gets a different basis from the same part with few large ones.

**Line L3.** With a diagonal $M$, set $\psi = M^{1/2}\phi$; then $M^{-1/2} C M^{-1/2} \psi = \lambda \psi$ is a standard [symmetric eigenproblem](/symmetric-eigenproblem/), and its orthonormal eigenvectors give $\phi = M^{-1/2}\psi$. With a full $M$, the [Cholesky factor](/cholesky-decomposition/) $M = LL^{\mathsf T}$ does the same. For a large mesh, only the first $m$ eigenpairs are computed, with the [Lanczos algorithm](/lanczos-algorithm/) and a shift-invert transform, which needs a sparse factorization of $C - \sigma M$. When an eigenvalue is repeated, any M-orthonormal basis of its eigenspace is correct; the [Gram-Schmidt process](/gram-schmidt-process/) in the inner product $u^{\mathsf T} M v$ gives one.

**Line L5.** The transfer function $h$ chooses the filter. $h = 1$ for $\lambda \le \lambda_c$ and $0$ above is an ideal low-pass filter; $h(\lambda) = e^{-t\lambda}$ is heat diffusion for the time $t$; a bump above $1$ in a band of $\lambda$ makes the details of that size stronger. With $h = 1$ and $m = n$, $y = x$.

**Example.** Take the octahedron with the six vertices $\pm e_1, \pm e_2, \pm e_3$. All eight faces are equilateral with side $\sqrt 2$ and area $\sqrt3/2$, and all angles are $60°$ with $\cot 60° = 1/\sqrt3$. So $C_{ij} = -1/\sqrt3$ on the twelve edges and $C_{ii} = 4/\sqrt3$. The lumped mass gives each vertex a third of its four faces, $M_{ii} = 2/\sqrt3$, and the total area is $T = 4\sqrt3$. Then $M^{-1}C = \tfrac12(4I - A)$, where $A$ is the adjacency matrix of the octahedron. The eigenvalues of $A$ are $4$, $0$ (three times) and $-2$ (twice), so the manifold harmonic eigenvalues are

$$\lambda = 0,\ 2,\ 2,\ 2,\ 3,\ 3.$$

The eigenvectors are the constant, the three coordinate functions $x$, $y$, $z$ at the vertices, and the functions $x^2 - y^2$ and $y^2 - z^2$. On the unit sphere, the eigenvalues are $l(l + 1) = 0, 2, 6, \ldots$ with the same eigenfunctions, so the octahedron gets the first two levels right, and the third one too low.

Now let the signal $x$ be $1$ at the top vertex $e_3$ and $0$ at the other five. Its parts in the three eigenspaces are $\tfrac16$ at every vertex (for $\lambda = 0$), $\tfrac12 z$ (for $\lambda = 2$), and $\tfrac16(2z^2 - x^2 - y^2)$ (for $\lambda = 3$). At the top vertex they add up to $\tfrac16 + \tfrac12 + \tfrac13 = 1$, and at the equator to $\tfrac16 + 0 - \tfrac16 = 0$. Their squared M-norms are $T/36$, $T/12$ and $T/18$, and they add up to $T/6 = x^{\mathsf T} M x$, as Parseval's identity says. A low-pass filter that keeps $\lambda \le 2$ gives $\tfrac16 + \tfrac12 z$: the value $\tfrac23$ at the top, $\tfrac16$ on the equator and $-\tfrac13$ at the bottom. The sharp spike is spread over the whole shape.

On larger meshes the eigenvalues approach those of the sphere. On the icosphere with 162 vertices on the unit sphere, with the mixed Voronoi mass, a dense solve gives $0$, $2.000$ (three times), $5.865$ (five times), $11.234$ (three times), $11.415$ (four times) and $18.004$, against $0$, $2$, $6$, $12$ and $20$ on the sphere. The seven harmonics of degree $3$ split into a group of three and a group of four, because the symmetry group of the icosahedron has no irreducible representation of dimension $7$. The function $xyz$ is a spherical harmonic of degree $3$; its M-norm is $0.341$, and after it is projected on the first $16$ harmonics, the M-norm of the rest is $0.0018$.

**Cost.** The matrices of lines L1 and L2 take $\Theta(n)$ time on a mesh with $n$ vertices. A dense solve of line L3 takes $\Theta(n^3)$ time and $\Theta(n^2)$ space, which is practical only for a few thousand vertices. For the first $m$ harmonics of a large mesh, Lanczos needs one sparse factorization for each shift, and the orthogonalization against $m$ vectors costs $\Theta(n m^2)$; storing the basis takes $\Theta(n m)$. Lines L4 and L5 take $\Theta(n m)$ time for each signal.

## Classic examples

- **Filtering the geometry.** Vallet and Lévy apply lines L4 and L5 to the three coordinates of the vertices. A low-pass $h$ smooths the mesh, and a band that is made stronger exaggerates the features of one size. The low harmonics keep the coarse shape, so a few hundred of them already give a smooth version of a detailed model.
- **Smoothing as a filter.** [Laplacian smoothing](/laplacian-smoothing/) with a step $t$ multiplies each coefficient by $1 - t\lambda$, [implicit fairing](/implicit-fairing/) by $1/(1 + t\lambda)$, and [Taubin smoothing](/taubin-smoothing/) by a product of two such factors that stays near $1$ at low frequencies. Taubin used this view to design his filter without computing any eigenvector.
- **Compression.** Karni and Gotsman project the vertex coordinates on the first eigenvectors of the combinatorial Laplacian and keep only the first coefficients. For a smooth mesh, these coefficients carry most of the energy. They split large meshes into patches, because the eigenvectors of the whole mesh cost too much.
- **Shape signatures.** The eigenvalues depend only on the intrinsic metric, so they do not change when the shape bends without stretching. Reuter, Wolter and Peinecke use the first eigenvalues, after a normalization of the scale, as a signature to search for similar shapes. The heat kernel signature of Sun, Ovsjanikov and Guibas uses $\sum_k e^{-t\lambda_k}\phi_k(i)^2$ at each vertex $i$ as a descriptor of points.
- **Partitioning.** The sign of the second harmonic $\phi_2$ cuts the surface into two parts along a narrow neck, as in [spectral clustering](/spectral-clustering/) of a graph.

## Variations

- **Lumped or consistent mass.** The diagonal mass makes line L3 a standard symmetric problem and is cheaper; the finite element mass gives eigenvalues that are more accurate on a coarse mesh. Reuter and his coauthors use higher order finite elements for more accuracy still.
- **Graph Laplacian.** Taubin and Karni-Gotsman use the uniform or combinatorial Laplacian with $M = I$. It needs no geometry, but its basis follows the connectivity, so the same surface with a different triangulation gets a different basis.
- **Boundary conditions.** On a mesh with a boundary, the template as written gives the Neumann harmonics, which are free on the boundary. For Dirichlet harmonics, which are $0$ on the boundary, remove the rows and columns of the boundary vertices from $C$ and $M$.
- **Heat and diffusion.** With $h(\lambda) = e^{-t\lambda}$, line L5 solves the heat equation for the time $t$. The [heat method](/heat-method/) uses one implicit step of the same equation, with a sparse solve instead of a basis.
- **Matching shapes.** The coefficients of functions in the bases of two shapes can be related by a small matrix. This is the idea of the functional maps of Ovsjanikov and his coauthors, which use the first harmonics of each shape.

## Pitfalls

- **Sign and order of the eigenvectors.** $-\phi$ is also a solution, and the vectors of a repeated eigenvalue are only defined up to a rotation of their space. Two meshes of the same shape can return different signs, different bases, or two close eigenvalues in a different order. Compare eigenspaces, or use quantities like $\phi_k(i)^2$ summed over an eigenspace, not single vectors.
- **The mass matrix in the transform.** The coefficient is $\phi_k^{\mathsf T} M x$, not $\phi_k^{\mathsf T} x$. With the plain dot product, the reconstruction $\sum_k \tilde x_k \phi_k$ is wrong, because the basis is not orthonormal in that product.
- **Ringing.** An ideal low-pass filter on a signal with a sharp edge makes ripples next to the edge, as in the Gibbs phenomenon of Fourier series. A smooth transfer function, like $e^{-t\lambda}$, avoids them.
- **Bad triangles.** A triangle with an angle near $0$ or $180°$ gives a very large cotangent, and a triangle with zero area makes $M$ singular. Then the eigenvalues and eigenvectors are poor. Clean up or remesh the mesh first.
- **Cost of many harmonics.** Each harmonic is a dense vector of length $n$, and the solve gets slower as $m$ grows. For a filter of the low frequencies only, a sparse solve such as implicit fairing is often cheaper than a basis.
- **Rounding.** A floating point eigensolver gives vectors that are M-orthonormal only up to rounding, and the vectors of close eigenvalues are sensitive to small changes of the mesh. Check $\Phi^{\mathsf T} M \Phi$ against $I$ before trusting the transform.

## Exercises

1. Show that one step of implicit fairing, $(M + tC)\,y = Mx$, gives $y = \sum_k \tilde x_k \phi_k / (1 + t\lambda_k)$.
2. On the octahedron of the example, check that the vector with the values of $x^2 - y^2$ at the vertices satisfies $C\phi = 3M\phi$.
3. Show that if all vertex areas are equal, $M = aI$, the manifold harmonics are the eigenvectors of $C$, and the coefficient is $a\,\phi_k^{\mathsf T} x$.
4. Show that the Rayleigh quotient $u^{\mathsf T} C u / u^{\mathsf T} M u$ is at least $\lambda_2$ for every $u \ne 0$ with $\mathbf 1^{\mathsf T} M u = 0$ on a connected mesh. What does this say about $\phi_2$?
5. Scale a mesh by a factor $s$. How do $C$, $M$ and the eigenvalues change? Why must a shape signature normalize the scale?

## References
