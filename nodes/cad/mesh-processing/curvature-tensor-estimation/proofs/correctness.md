---
title: Taubin's edge samples are exact on circles and consistent on smooth surfaces, his eigenvalue step is exact for balanced directions and biased otherwise, and the edge tensor has a closed form on a cylinder
proves: [correctness, termination]
status: full
---

**Setup.** Fix an inner vertex $i$ with position $x_i$, unit normal $N$, and neighbours $j$. For a neighbour $j$, let $d_j = x_i - x_j$, let $T_j$ be the unit vector along the projection of $d_j$ to the plane normal to $N$, and let $\kappa_j = 2\,N \cdot d_j / |d_j|^2$. The weights $w_j > 0$ sum to 1. In a basis $E_1, E_2$ of the tangent plane, write $T_j = (\cos\theta_j, \sin\theta_j)$. The algorithm forms $M = \sum_j w_j\kappa_j T_jT_j^\top$, takes its eigenvalues $m_1 \ge m_2$, and returns $k_1 = 3m_1 - m_2$ and $k_2 = 3m_2 - m_1$. The sign convention is: the curvature is positive where the surface bends away from $N$. Each loop of the pseudocode runs over a finite set, and the eigenvalues of a $2 \times 2$ symmetric matrix have a closed form, so the algorithm stops.

**Lemma 1 (exact on a circle).** If $x_j$ lies on a circle of radius $\rho$ through $x_i$ whose center is $x_i - \rho N$, then $\kappa_j = 1/\rho$. So on a sphere of radius $r$ with the true normals, every $\kappa_j = 1/r$.

*Proof.* The center is $c = x_i - \rho N$, and $|x_j - c|^2 = \rho^2$. Write $x_j - c = -d_j + \rho N$. Then $|d_j|^2 - 2\rho\,N \cdot d_j + \rho^2 = \rho^2$, so $N \cdot d_j = |d_j|^2 / (2\rho)$ and $\kappa_j = 1/\rho$. On a sphere with the outward normal, every point of the sphere is on the great circle through $x_i$ and that point, whose center is $x_i - rN$. $\square$

**Lemma 2 (consistent on a smooth surface).** Let the vertices lie on a smooth surface with principal curvatures $k_1, k_2$ at $x_i$, and let $N$ be the true normal. Then $\kappa_j = \kappa_n(T_j) + O(|d_j|)$, where $\kappa_n(T) = k_1\cos^2\theta + k_2\sin^2\theta$ is the normal curvature in the direction $T$ at the angle $\theta$ from the first principal direction.

*Proof.* Put $x_i$ at the origin, $N$ on the $z$ axis, and the principal directions on the $x$ and $y$ axes. Near $x_i$ the surface is the graph $z = -\frac{1}{2}(k_1x^2 + k_2y^2) + O(\rho^3)$ with $\rho^2 = x^2 + y^2$, and the minus sign is the sign convention. For $x_j = (x, y, z)$, $N \cdot d_j = -z = \frac{1}{2}(k_1x^2 + k_2y^2) + O(\rho^3)$ and $|d_j|^2 = \rho^2 + O(\rho^4)$. So $\kappa_j = (k_1x^2 + k_2y^2)/\rho^2 + O(\rho)$. The direction of $(x, y)$ is $\pm T_j$, and the sign does not change $\cos^2$ and $\sin^2$. $\square$

**Lemma 3 (the continuous average).** For $\kappa(\theta) = k_1\cos^2\theta + k_2\sin^2\theta$ and $t(\theta) = (\cos\theta, \sin\theta)$,

$$\frac{1}{2\pi}\int_0^{2\pi}\kappa(\theta)\,t(\theta)\,t(\theta)^\top d\theta = \begin{pmatrix} \frac{3k_1 + k_2}{8} & 0 \\ 0 & \frac{k_1 + 3k_2}{8} \end{pmatrix}.$$

So if $M$ equals this average, then $3m_1 - m_2 = k_1$ and $3m_2 - m_1 = k_2$ (with $m_1$ the entry for $k_1 \ge k_2$), and the eigenvectors are the principal directions.

*Proof.* The averages of $\cos^4$, $\cos^2\sin^2$ and $\sin^4$ over a period are $\frac{3}{8}$, $\frac{1}{8}$ and $\frac{3}{8}$, and the averages of $\cos^3\sin$ and $\cos\sin^3$ are 0. The diagonal entries are $\frac{3}{8}k_1 + \frac{1}{8}k_2$ and $\frac{1}{8}k_1 + \frac{3}{8}k_2$. Then $3(\frac{3}{8}k_1 + \frac{1}{8}k_2) - (\frac{1}{8}k_1 + \frac{3}{8}k_2) = k_1$, and the other formula follows the same way. $\square$

**Theorem 1 (balanced directions are exact).** Let $\kappa_j = \kappa_n(T_j)$ for every $j$. If the weighted directions satisfy

$$\sum_j w_j e^{2\mathrm{i}\theta_j} = 0 \quad\text{and}\quad \sum_j w_j e^{4\mathrm{i}\theta_j} = 0,$$

then $M$ is the continuous average of Lemma 3, so $k_1, k_2$ and the principal directions are exact. In general, without the two conditions, $m_1 + m_2 = \sum_j w_j\kappa_j$, so $\frac{1}{2}(k_1 + k_2) = \sum_j w_j\kappa_j$ is the weighted mean of the samples.

*Proof.* Let $\phi$ be the angle of the first principal direction, $H = \frac{1}{2}(k_1 + k_2)$ and $D = \frac{1}{2}(k_1 - k_2)$. Then $\kappa(\theta) = H + D\cos(2\theta - 2\phi)$ and $t\,t^\top = \frac{1}{2}I + \frac{1}{2}R(2\theta)$ with $R(\psi) = \begin{pmatrix}\cos\psi & \sin\psi \\ \sin\psi & -\cos\psi\end{pmatrix}$. The product is

$$\kappa\,t\,t^\top = \tfrac{1}{2}H\,I + \tfrac{1}{2}H\,R(2\theta) + \tfrac{1}{2}D\cos(2\theta - 2\phi)\,I + \tfrac{1}{4}D\,\big(R(4\theta - 2\phi) + R(2\phi)\big),$$

where the last term uses $\cos(\alpha)R(\beta) = \frac{1}{2}(R(\beta + \alpha) + R(\beta - \alpha))$, which holds entry by entry by the product formulas for $\cos$ and $\sin$. Each entry of $R(2\theta)$, $R(4\theta - 2\phi)$ and $\cos(2\theta - 2\phi)$ is a real part or an imaginary part of a constant times $e^{2\mathrm{i}\theta}$ or $e^{4\mathrm{i}\theta}$. Under the two conditions, the weighted sums of these terms vanish, and $M = \frac{1}{2}H\,I + \frac{1}{4}D\,R(2\phi)$. The continuous average has the same form, because the averages of $e^{2\mathrm{i}\theta}$ and $e^{4\mathrm{i}\theta}$ over a period are 0. So $M$ equals the matrix of Lemma 3. For the trace: $\operatorname{tr}(T_jT_j^\top) = 1$, so $m_1 + m_2 = \operatorname{tr} M = \sum_j w_j\kappa_j$, and $k_1 + k_2 = 2(m_1 + m_2)$. $\square$

**Corollary 1.** For $p \ge 5$ equally spaced directions with equal weights, the two sums are sums of $p$-th roots of unity raised to the power 2 or 4, which are 0 because $p$ does not divide 2 or 4. So the estimate is exact for exact samples. For $p = 4$, $\sum e^{4\mathrm{i}\theta_j} = 4e^{4\mathrm{i}\theta_0} \ne 0$, and the estimate is not exact: with $k_1 = 1$, $k_2 = 0$ and directions along the principal axes, the samples are $1, 0, 1, 0$, $M = \operatorname{diag}(\frac{1}{2}, 0)$, and the output is $k_1 = \frac{3}{2}$, $k_2 = -\frac{1}{2}$.

**Corollary 2 (the sphere).** On a sphere of radius $r$ with the true normals, every $\kappa_j = 1/r$ by Lemma 1, so $k_1 + k_2 = 2/r$ exactly at every vertex, for every mesh. At a vertex with 5 equally spaced neighbour directions and equal weights, such as the 12 vertices of valence 5 of an icosphere, $k_1 = k_2 = 1/r$ exactly.

**Theorem 2 (a bias that refinement does not remove).** On the grid where each square is cut by the diagonal of direction $(1, 1)$, every inner vertex has six neighbours, in the directions $0°, 45°, 90°, 180°, 225°, 270°$. Up to sign, these are the three directions $0°, 45°, 90°$, each one two times. All faces have the same area and each inner edge is in two faces, so all weights are equal. When the grid is refined on a smooth surface with this pattern in the tangent plane, the output tends to the value for exact samples (Lemma 2), which is not $(k_1, k_2)$ in general:

- On the saddle $z = \frac{1}{2}(x^2 - y^2)$ at the origin, the principal axes are the grid axes, and the samples tend to $1, -1, 1, -1$ on the axes (with the sign convention, $k_1 = 1$ along $y$) and $0, 0$ on the diagonals. Then $M = \frac{1}{6}\operatorname{diag}(2, -2)$ in the frame of $y$ and $x$, so $m_{1,2} = \pm\frac{1}{3}$ and $k_{1,2} = \pm\frac{4}{3}$, not $\pm 1$.
- On a cylinder of radius 1 with square cells, the samples tend to $1$ around, $0$ along the axis and $\frac{1}{2}$ on the diagonals. Then $6M = 2\operatorname{diag}(1, 0) + 2 \cdot \frac{1}{2} \cdot \frac{1}{2}\begin{pmatrix}1 & 1\\ 1 & 1\end{pmatrix}$, with eigenvalues of $M$ equal to $\frac{1}{4} \pm \frac{\sqrt 5}{12}$. So $k_{1,2} \to \frac{1}{2} \pm \frac{\sqrt 5}{3} \approx 1.245, -0.245$, not $1$ and $0$. The mean $\frac{1}{2}(k_1 + k_2) = \frac{1}{2}$ is right, as Theorem 1 says.

*Proof.* The directions are fixed by the grid, the weights are equal because every edge lies in two faces of the same area, and by Lemma 2 the samples converge to the normal curvatures in these directions. $M$ is continuous in the samples, and the eigenvalues of a symmetric matrix are continuous in its entries. The two computations are direct. $\square$

The tests check Corollary 1, Corollary 2, the two limits of Theorem 2 within $0.01$, and the twisted cylinder, where every vertex has six near-equal directions, so that the error tends to 0.

**Theorem 3 (the edge tensor on a cylinder).** Take the cylinder of radius $r$ with $m$ columns and rows of height $h$, each rectangle cut by the same diagonal, and let $B$ be the mixed cell of an inner vertex, or the union of the cells of the vertices at most $r'$ edges away that does not meet the border. Then the edge tensor, restricted to the tangent plane, has the eigenvalue $\frac{\pi/m}{r\sin(\pi/m)}$ along the axis and $0$ around the axis. So the method returns $k_1 = \frac{\pi/m}{r\sin(\pi/m)}$ in the direction around the axis and $k_2 = 0$ along the axis.

*Proof.* The rectangles are planar, so the diagonals and the ring edges lie between two faces in one plane, with $\beta = 0$. A vertical edge lies between two columns, whose planes meet at the angle $2\pi/m$, and the edge is convex, so $\beta = 2\pi/m$. Each cell holds half of each vertical edge at its vertex, and each vertex has two of them, so a cell adds $2 \cdot \frac{2\pi}{m}\cdot\frac{h}{2}\,\hat z\hat z^\top = \frac{2\pi h}{m}\hat z\hat z^\top$. Every face is a right triangle with legs $c = 2r\sin(\pi/m)$ and $h$, and each vertex is the right-angle corner of 2 of its 6 faces, No triangle is obtuse, so the mixed cell is the Voronoi cell. The circumcenter of a right triangle is the midpoint of its hypotenuse, so the right-angle corner gets half of the area $\frac{1}{2}ch$ and each other corner gets a quarter. A vertex gets $2 \cdot \frac{1}{4}ch + 4 \cdot \frac{1}{8}ch = ch$. A region of $b$ cells gives $\frac{b\,2\pi h/m}{b\,ch}\hat z\hat z^\top = \frac{\pi/m}{r\sin(\pi/m)}\hat z\hat z^\top$. Its eigenvector $\hat z$ has the eigenvalue above, and the tangent direction around the axis has the eigenvalue 0. The curvature across $\hat z$ is in the direction $N \times \hat z$, around the axis. $\square$

As $m \to \infty$, $k_1 \to 1/r$, with the relative error $\frac{x}{\sin x} - 1 \approx x^2/6$ for $x = \pi/m$. For general meshes, Cohen-Steiner and Morvan bound the error of the edge tensor over $B$ for restricted Delaunay triangulations of a smooth surface when $B$ is large compared with the triangles. The code does not prove that bound. The tests measure it on icospheres: with $B$ the cells of a vertex and its neighbours, the largest error of $k_1, k_2$ on the sphere of radius 2 falls from $0.031$ at 162 vertices to $0.012$ at 642 vertices.

**Lemma 4 (exact signs).** The sign of $\beta$ comes from the sign of $\det(b - a, c - a, p - a)$, where $a, b, c$ are the corners of one face and $p$ the far corner of the other. The code converts the float coordinates to fractions, which is exact, and evaluates the determinant exactly. So a convex edge never gets a negative $\beta$ from a rounding error, and an edge between two coplanar faces gets $\beta = 0$.

**Lemma 5 (rigid motions).** If every position is mapped by $x \mapsto Rx + t$ with $R$ a rotation, then both methods return the same $k_1, k_2$, and the directions are mapped by $R$.

*Proof.* The normals, the face areas, the samples $\kappa_j$ and the dihedral angles depend only on differences of positions, dot products and cross products, and a rotation keeps dot products and maps cross products to cross products. The determinant of Lemma 4 is unchanged by a rotation. The tangent basis is a different basis of the rotated plane, but the eigenvalues do not depend on the basis, and the eigenvectors are mapped by $R$. $\square$
