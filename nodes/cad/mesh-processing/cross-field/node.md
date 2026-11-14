---
tag: E95VWG
kind: definition
slug: cross-field
name: Cross field
aliases:
- 4-symmetry direction field
- 4-RoSy field
area: cad/mesh-processing
level: advanced
summary: A field of four directions related by 90 degree turns on a surface, whose singularities set the irregular vertices of a field-aligned quad mesh.
prereqs: [manifold-mesh, discrete-gaussian-curvature, discrete-gauss-bonnet-theorem]
see_also: [globally-optimal-direction-fields, mixed-integer-quadrangulation, curvature-tensor-estimation, cut-graph, euler-poincare-formula, mesh-parameterization, rayleigh-quotient, cotangent-laplacian]
sources:
  - paper: doi:10.1145/1356682.1356683
    title: Nicolas Ray, Bruno Vallet, Wan Chiu Li and Bruno Lévy, N-symmetry direction field design, ACM Transactions on Graphics 27(2), Article 10, 2008
    locator: the definition of N-symmetry direction fields on a triangle mesh, the period jumps across edges, and the index of a singularity with its relation to the Euler characteristic
  - paper: doi:10.1111/cgf.12864
    title: Amir Vaxman, Marcel Campen, Olga Diamanti, Daniele Panozzo, David Bommes, Klaus Hildebrandt and Mirela Ben-Chen, Directional field synthesis, design, and processing, Computer Graphics Forum 35(2), 545-572, 2016
    locator: the survey of representations (angles with period jumps, the power vector), discretizations, singularities and the Poincaré-Hopf theorem for directional fields
  - paper: doi:10.1145/2461912.2462005
    title: Felix Knöppel, Keenan Crane, Ulrich Pinkall and Peter Schröder, Globally optimal direction fields, ACM Transactions on Graphics 32(4), Article 59, 2013
    locator: the representation of an n-direction field by the n-th power of a complex number, and the quadratic smoothness energy
---

A cross field on a surface gives, at each point, a cross: four tangent directions at right angles, with no first direction among them. It is the kind of field that a quad mesh follows, since the edges at a regular quad vertex form a cross. A smooth cross field cannot exist everywhere on most surfaces. It has isolated singular points, whose indices are multiples of $1/4$ and add up to the Euler characteristic of the surface, by a form of the Poincaré-Hopf theorem. In a quad mesh built from the field, a singularity of index $+1/4$ becomes a vertex of valence 3 and one of index $-1/4$ a vertex of valence 5, so choosing the field chooses the irregular vertices of the mesh.

## Definition

Let $M$ be a connected, oriented [manifold mesh](/manifold-mesh/) of triangles, with faces oriented by the right-hand rule, so that each triangle has a well-defined counterclockwise rotation $J$ by $90°$ in its plane. A **cross** in a triangle $f$ is a set

$$\{v, Jv, -v, -Jv\}$$

of four unit vectors in the plane of $f$. In a fixed reference direction of $f$, for example along one of its edges, the cross is given by the angle $\theta_f$ of any of its four vectors, and $\theta_f$ is defined modulo $\pi/2$. A **cross field** on $M$ gives one cross in each triangle, or one in the tangent plane of each vertex in other discretizations. More generally, an *$N$-direction field* or *$N$-RoSy field* has $N$ directions at angles $2\pi/N$; $N = 1$ gives vector fields, $N = 2$ line fields, such as the principal curvature directions, and $N = 4$ cross fields.

**Two representations.**

- **Angle and period jump.** Unfold two triangles $f$ and $g$ that share an edge into one plane. Let $\rho_{fg}$ be the angle from the reference direction of $f$ to that of $g$ in this plane; it is the discrete parallel transport from $f$ to $g$. The crosses of $f$ and $g$ are compared by $\theta_g - \theta_f - \rho_{fg}$, which is defined modulo $\pi/2$. Fixing a representative $\theta$ in each face, an integer $p_{fg}$, the *period jump* or *matching*, says which of the four vectors of $g$ the vector $\theta_f$ goes to. Smoothness energies in this form, $\sum_{fg} w_{fg}(\theta_g - \theta_f - \rho_{fg} - p_{fg}\pi/2)^2$, mix real and integer unknowns.
- **Fourth power.** The complex number $z_f = e^{4i\theta_f}$ does not depend on which of the four vectors is chosen, because $4 \cdot \pi/2 = 2\pi$. Transport across an edge multiplies by $e^{4i\rho_{fg}}$. So a cross field is the same as a field of unit complex numbers in the face frames, with no integer unknowns, and the smoothness energy $\sum_{fg} w_{fg}\lvert z_g - e^{4i\rho_{fg}} z_f\rvert^2$ is a Hermitian quadratic form. This is the starting point of [globally optimal direction fields](/globally-optimal-direction-fields/).

**Index of a vertex.** Let $v$ be an inner vertex with the triangles $f_1, \dots, f_m$ around it in counterclockwise order, and let $d(v) = 2\pi - \sum\alpha$ be its angle defect, the [discrete Gaussian curvature](/discrete-gaussian-curvature/). For each step from $f_k$ to $f_{k+1}$ (with $f_{m+1} = f_1$), let $\delta_k$ be the smallest rotation that turns the transported cross of $f_k$ onto the cross of $f_{k+1}$:

$$\delta_k \equiv \theta_{f_{k+1}} - \theta_{f_k} - \rho_{f_k f_{k+1}} \pmod{\pi/2}, \qquad -\frac{\pi}{4} < \delta_k \le \frac{\pi}{4}.$$

The **index** of $v$ is

$$I(v) = \frac{d(v) + \sum_{k=1}^{m} \delta_k}{2\pi}.$$

Transport once around $v$ rotates every tangent vector by the defect $d(v)$, and the crosses then turn by the $\delta_k$ and come back to the cross they started from. So $d(v) + \sum_k \delta_k$ is a multiple of $\pi/2$, and $I(v)$ is a multiple of $1/4$. The vertex is **singular** if $I(v) \ne 0$. The index of the fourth power field $z$ is $4 I(v)$, an integer, the winding number of $z$ around $v$ measured against the transport.

**Theorem (Poincaré-Hopf for cross fields).** On a closed mesh with Euler characteristic $\chi = V - E + F = 2 - 2g$, where $g$ is the genus, and with $\delta$ chosen so that the step from $g$ to $f$ has $\delta = -\delta_{fg}$ for every edge,

$$\sum_v I(v) = \chi.$$

*Proof.* By the [discrete Gauss-Bonnet theorem](/discrete-gauss-bonnet-theorem/), $\sum_v d(v) = 2\pi\chi$. Each edge $vw$ has two triangles $f$ and $g$. The walk counterclockwise around $v$ crosses this edge in one direction, say from $f$ to $g$, and the walk counterclockwise around $w$ crosses it from $g$ to $f$, since the two walks run on opposite sides of the edge. The two terms are $\delta_{fg}$ and $\delta_{gf} = -\delta_{fg}$, so the $\delta$ terms of all vertices add up to 0. Hence $2\pi \sum_v I(v) = 2\pi\chi$. $\blacksquare$

The choice $\delta_{gf} = -\delta_{fg}$ only matters when $\delta_{fg} = \pi/4$ exactly, where both $\pi/4$ and $-\pi/4$ are smallest rotations.

## Examples and non-examples

- **The cube.** Put on each face of a cube the cross along its edges, and split the faces into triangles. Across every edge the crosses match exactly after unfolding, so all $\delta_k = 0$. A corner has three right angles, so $d = 2\pi - 3\pi/2 = \pi/2$ and $I = 1/4$. The 8 corners give $8 \cdot 1/4 = 2 = \chi$ of the sphere. The quad mesh of the cube surface has 8 vertices of valence 3, one per singularity.
- **A flat singularity.** Take six equilateral triangles around a vertex in the plane, so $d = 0$, and in the triangle $f_k$ the cross at the angle $k\pi/12$, $k = 0, \dots, 5$, in one global frame. The steps give $\delta_k = \pi/12$ for $k = 0, \dots, 4$, and from $f_5$ back to $f_0$ the angle goes from $5\pi/12$ to $0 \equiv \pi/2$, again $\delta = \pi/12$. So $I = 6 \cdot (\pi/12) / (2\pi) = 1/4$. The fourth powers $e^{ik\pi/3}$ go once around the unit circle, winding number $1 = 4 \cdot 1/4$. A vector field cannot do this: going once around, it must turn by a multiple of $2\pi$.
- **The torus.** $\chi = 0$, so a cross field on a torus can have no singularities, like the field along the two grid directions of a flat torus. A field with singularities on a torus has as much positive index as negative index.
- **A surface of genus $g \ge 2$.** The indices add up to $2 - 2g < 0$. With indices of $-1/4$ only, a field needs at least $4(2g - 2) = 8g - 8$ singularities; a quad mesh of a genus 2 surface needs at least 8 vertices of valence 5, or some of higher valence.
- **Quad meshes.** In a closed quad mesh, the edges at a vertex of valence $k$ form a cross field with index $(4 - k)/4$ at that vertex. The sum is $\sum_v (4 - k_v)/4 = V - 2E/4 = V - E/2 = V - E + F$, because $4F = 2E$, which checks the theorem.
- **Non-example: a vector field read as a cross field.** A field of single vectors gives a cross field, but not the other way round. The cross field of the flat example has no consistent choice of one of its four vectors around the vertex, so it is not a vector field with a $90°$ symmetry chosen at each point.
- **Non-example: four arbitrary directions.** Four unit vectors at angles $0°$, $80°$, $180°$ and $260°$ are not a cross. A field of such frames is a non-orthogonal frame field, a wider class with its own representations.

## Related definitions

- **Line fields and principal directions.** The two principal curvature directions, from [curvature tensor estimation](/curvature-tensor-estimation/), are a line field with $N = 2$, the same idea with period $\pi$. Taking both principal directions together gives a cross field away from the umbilic points, and quad meshing often aligns the cross field with them where the curvature is clearly anisotropic.
- **Smoothest cross field.** With the fourth power representation, the smoothest unit cross field is approached by the eigenvector of the smallest eigenvalue of a Hermitian matrix like the [cotangent Laplacian](/cotangent-laplacian/), the minimizer of its [Rayleigh quotient](/rayleigh-quotient/). This is the algorithm of [globally optimal direction fields](/globally-optimal-direction-fields/), which places the singularities by itself.
- **Field-aligned parameterization.** [Mixed-integer quadrangulation](/mixed-integer-quadrangulation/) computes a map whose gradients follow a given cross field, on the surface cut open along a [cut graph](/cut-graph/) through the singularities, with integer conditions across the cut so that the integer grid lines close up into quads.
- **Euler characteristic.** The [Euler-Poincaré formula](/euler-poincare-formula/) gives the total index $\chi$ that every cross field on the surface must have.

## References
