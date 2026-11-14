---
tag: FD84ZX
kind: definition
slug: generalized-bezier-patch
name: Generalized Bezier patch
aliases:
- multi-sided Bezier patch
area: cad/surface-interrogation-and-design
level: research
summary: Varady, Salvi and Kariko's n-sided patch with a Bezier-like control net, built by blending ribbons over a regular polygon domain, that matches neighbours with G1 continuity.
prereqs: [bezier-patch, n-sided-patch, tangent-plane-continuity]
see_also: [n-sided-patch, gregory-patch, bezier-patch, tangent-plane-continuity, coons-patch, floater-mean-value-coordinates, vertex-blend, bezier-triangle]
sources:
  - paper: doi:10.1111/cgf.12833
    title: "Tamás Várady, Péter Salvi and György Karikó, A multi-sided Bézier patch with a simple control structure, Computer Graphics Forum 35(2), 307 to 317, 2016"
    locator: the original definition of the GB patch, its control structure and its G1 connection to adjacent Bézier surfaces
  - url: "http://salvi.chaosnet.org/texts/gb-fit-wait.pdf"
    title: "Péter Salvi, Tamás Várady and Kenjiro T. Miura, Approximating point clouds by Generalized Bézier surfaces, Workshop on the Advances in Information Technology (WAIT), Budapest, 2018"
    locator: Section 3, equations (1) to (4), a summary of the definition with the local parameters, the surface equation, the corner weights and the weight deficiency
  - paper: doi:10.1016/j.cagd.2024.102286
    title: "Tamás Várady, Péter Salvi and Márton Vaitkus, Genuine multi-sided parametric surface patches, a survey, Computer Aided Geometric Design 110, 102286, 2024"
    locator: the place of GB patches among control point based multi-sided schemes (general locator)
  - paper: doi:10.1145/77055.77059
    title: "Charles T. Loop and Tony D. DeRose, A multisided generalization of Bézier surfaces, ACM Transactions on Graphics 8(3), 204 to 234, 1989"
    locator: the S-patch, the earlier multi-sided generalization of Bézier surfaces
---

A Generalized Bézier patch, or GB patch, is a single surface patch with $n$ sides whose shape is set by a control net, like a tensor product [Bézier patch](/bezier-patch/). Várady, Salvi and Karikó introduced it in 2016 as a solution of the [n-sided patch](/n-sided-patch/) problem. Each side owns a few rows of control points, as a side of a Bézier patch does, and the rows of each side are blended in local parameters of that side over a regular polygon. Rational weights near the corners and one central control point complete the blend. The boundary of each side and the first cross derivative there come from the first two rows of that side, so the patch joins a Bézier neighbour with [tangent plane continuity](/tangent-plane-continuity/) in the same way as two Bézier patches do.

## Definition

Let $n \ge 3$ and let $D$ be the regular $n$-gon with corners $q_1, \dots, q_n$, indices modulo $n$. Let $\lambda_1, \dots, \lambda_n$ be the Wachspress coordinates of a point $p = (u, v)$ of $D$: with $A(a, b, c)$ the signed area of a triangle,

$$w_i(p) = \frac{A(q_{i-1}, q_i, q_{i+1})}{A(p, q_{i-1}, q_i) \, A(p, q_i, q_{i+1})}, \qquad \lambda_i = \frac{w_i}{\sum_j w_j},$$

continued to the boundary of $D$ by continuity. Side $i$ of $D$ joins $q_{i-1}$ to $q_i$. Its *local parameters* are

$$s_i = \frac{\lambda_i}{\lambda_{i-1} + \lambda_i}, \qquad h_i = 1 - \lambda_{i-1} - \lambda_i,$$

the side parameter and the distance parameter.

Fix a degree $d \ge 3$ and let $l = \lceil d/2 \rceil$, the number of control rows of each side. The control points are $C^i_{j,k}$ for $1 \le i \le n$, $0 \le j \le d$, $0 \le k < l$, and a central point $C_0$. Here $j$ runs along side $i$ and $k$ counts the rows inward from it. A point near a corner belongs to two sides and has two names: $C^i_{j,k} = C^{i+1}_{k,\, d-j}$ whenever both indices are in range. The *Generalized Bézier patch* is

$$S(u, v) = \sum_{i=1}^{n} \sum_{j=0}^{d} \sum_{k=0}^{l-1} \mu^i_{j,k} \, B^d_j(s_i) \, B^d_k(h_i) \, C^i_{j,k} + B_0(u, v) \, C_0,$$

where $B^d_j$ are the Bernstein polynomials of degree $d$ and the weights $\mu^i_{j,k}$ are as follows. For the $2 \times 2$ points at the corners of side $i$, the weight is the rational function

$$\alpha_i = \frac{h_{i-1}}{h_{i-1} + h_i} \quad (j \le 1,\ k \le 1), \qquad \beta_i = \frac{h_{i+1}}{h_{i+1} + h_i} \quad (j \ge d - 1,\ k \le 1),$$

and for the other points it is a constant $0$, $\tfrac12$ or $1$, chosen in the original paper so that each point is counted the right number of times. The central blend is the *weight deficiency*

$$B_0 = 1 - \sum_{i=1}^{n} \sum_{j=0}^{d} \sum_{k=0}^{l-1} \mu^i_{j,k} \, B^d_j(s_i) \, B^d_k(h_i).$$

The patch is defined so that, along side $i$, $S$ is the Bézier curve of degree $d$ of the row $C^i_{0,0}, \dots, C^i_{d,0}$, and the cross derivative is that of the tensor product Bézier patch whose first two rows are rows $0$ and $1$ of side $i$. These are the properties that the rational weights are there to give.

**Lemma 1 (local parameters on the boundary).** On side $i$, $h_i = 0$ and $s_i$ runs linearly from $0$ at $q_{i-1}$ to $1$ at $q_i$. On side $i$ also $h_{i-1} = s_i$, $h_{i+1} = 1 - s_i$, and $h_m = 1$ for every side $m$ that does not touch side $i$. On side $i - 1$, $s_i = 0$, and on side $i + 1$, $s_i = 1$.

*Proof.* Wachspress coordinates are generalized barycentric coordinates: on a side of a convex polygon only the two coordinates of its ends are nonzero, and they are the linear coordinates of the segment. (In the formula, when $p$ tends to side $i$, the area $A(p, q_{i-1}, q_i)$ tends to $0$, so $w_{i-1}$ and $w_i$ grow without bound and the other $w_j$ stay bounded.) So on side $i$, $\lambda_{i-1} = 1 - t$ and $\lambda_i = t$ for the linear parameter $t$ from $q_{i-1}$ to $q_i$, and $\lambda_m = 0$ otherwise. Then $s_i = t$ and $h_i = 1 - (1 - t) - t = 0$. Also $h_{i-1} = 1 - \lambda_{i-2} - \lambda_{i-1} = 1 - (1 - t) = t$, $h_{i+1} = 1 - \lambda_i - \lambda_{i+1} = 1 - t$, and $h_m = 1$ when neither $\lambda_{m-1}$ nor $\lambda_m$ is one of $\lambda_{i-1}, \lambda_i$. On side $i - 1$, $\lambda_i = 0$ and $\lambda_{i-1} > 0$ away from $q_{i-2}$, so $s_i = 0$; on side $i + 1$, $\lambda_{i-1} = 0$ and $\lambda_i > 0$ away from $q_{i+1}$, so $s_i = 1$. $\square$

**Corollary (the corner weights on the boundary).** On side $i$, away from its ends, $\alpha_i = \beta_i = 1$. On side $i - 1$, away from its ends, $\alpha_i = 0$, and on side $i + 1$, $\beta_i = 0$.

*Proof.* On side $i$, $h_i = 0$ and $h_{i-1}, h_{i+1} > 0$ inside the side, so both quotients are $1$. On side $i - 1$, $h_{i-1} = 0$ by Lemma 1 for side $i - 1$, and $h_i = 1 - \lambda_{i-1} > 0$ away from $q_{i-1}$, so $\alpha_i = 0$. The case of $\beta_i$ on side $i + 1$ is the same. $\square$

So a corner point of side $i$ has full weight on side $i$ and no weight, under its name of side $i$, on the neighbouring side, where it is blended under its other name. This is how the double names at the corners do not count a point twice on the boundary.

**Lemma 2 (affine invariance).** The blending functions of $S$ sum to $1$ at every point of $D$. So for every affine map $T$, applying $T$ to all control points gives the patch $T \circ S$.

*Proof.* The first claim is the definition of $B_0$. If blending functions $\phi_m$ sum to $1$ and $T(x) = M x + b$, then $\sum_m \phi_m T(C_m) = M \sum_m \phi_m C_m + b \sum_m \phi_m = T\bigl(\sum_m \phi_m C_m\bigr)$. $\square$

Lemma 2 does not give the convex hull property, which would also need blends that are never negative. Later work by the same group reports that for larger $n$ or $d$ the central blend $B_0$ becomes too large, and changes the treatment of the central point.

## Examples and non-examples

**The centre of the domain.** At the centre of the regular $n$-gon, symmetry gives $\lambda_i = 1/n$ for all $i$. So $s_i = \tfrac12$ and $h_i = 1 - \tfrac2n$ for every side. For $n = 5$ this is $h_i = \tfrac35$, and for $n = 4$ it is $h_i = \tfrac12$, the centre of a square in the usual parameters.

**Counting control points.** The rows of side $i$ have $(d + 1) l$ names. The $l \times l$ block at each end of the rows is shared with a neighbour, by the rule $C^i_{j,k} = C^{i+1}_{k, d-j}$, which applies when $j > d - l$. Assign each shared point to the side in whose left block it lies. Then each side owns $(d + 1) l - l^2 = l (d + 1 - l)$ points, and the patch has $n \, l (d + 1 - l) + 1$ control points with the central one.

- For $d = 3$, $l = 2$: $4 n + 1$ points, so $21$ for a five sided patch.
- For $n = 4$ and even $d$, $l = d/2$ gives $4 \cdot \frac d2 \bigl(\frac d2 + 1\bigr) + 1 = (d + 1)^2$, the number of control points of a tensor product patch of degree $d$.
- For $n = 4$ and odd $d$ it gives $(d + 1)^2 + 1$: the extra point is the central point, which a tensor product patch of odd degree does not have.

**A five sided cubic patch.** With $n = 5$ and $d = 3$, each side has two rows of four points. The first row of side $i$ is the cubic Bézier boundary curve, and the second row sets the cross derivative, as on the boundary of a bicubic patch. To join the patch to a bicubic neighbour with $G^1$ continuity, one chooses the second row of side $i$ to meet the $G^1$ conditions of the [tangent plane continuity](/tangent-plane-continuity/) page with the neighbour's last two rows. The $21$st point, the centre, is free for the designer.

**Non-example: the S-patch.** The S-patch of Loop and DeRose is also a multi-sided generalization of Bézier surfaces over a polygon, but its control points are labeled by $n$-tuples of nonnegative integers that sum to the degree $d$. There are $\binom{d + n - 1}{n - 1}$ such labels, by counting the ways to place $d$ units into $n$ slots: for $n = 5$ and $d = 3$, $\binom{7}{4} = 35$, against $21$ for the GB patch. The GB control net keeps the layout of rows along the sides, which is the reason for its simpler structure.

**Non-example: a split of the polygon.** Cutting a five sided region into five four sided Bézier or [Gregory patches](/gregory-patch/) solves the same problem with several patches and inner joins. A GB patch is one patch with one formula over the whole polygon.

**Non-example: a polygon that is not convex.** The definition uses a regular polygon, and Wachspress coordinates are made for convex polygons. Variants over curved or concave domains replace them by other coordinates, such as harmonic coordinates.

## Related definitions

- **[Bézier patch](/bezier-patch/).** The tensor product patch whose boundary rows the GB patch copies along each side.
- **[N-sided patch](/n-sided-patch/).** The problem the GB patch solves with a single patch.
- **[Gregory patch](/gregory-patch/).** A four sided patch that uses rational weights so that each side sees only its own cross derivative data.
- **[Coons patch](/coons-patch/).** Transfinite multi-sided patches blend ribbons in a similar way, but without a control net in the interior.
- **[Mean value coordinates](/floater-mean-value-coordinates/).** Another family of generalized barycentric coordinates, used for local parameters in some multi-sided schemes.
- **[Bézier triangle](/bezier-triangle/).** The three sided Bézier patch, whose control points are labeled like those of the S-patch with $n = 3$.

## References
