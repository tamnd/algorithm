---
tag: 52AQN8
kind: theorem
slug: edge-theorem
name: Edge theorem
aliases:
- Bartlett-Hollot-Huang edge theorem
area: control/robust-and-adaptive-control
level: advanced
summary: "For a polytope of polynomials of the same degree, the boundary of the root set lies in the roots of the exposed edges. So all roots are in a simply connected open region if all edge roots are."
prereqs: [kharitonov-theorem, convex-polytope]
see_also: [kharitonov-theorem, convex-polytope, model-uncertainty, routh-hurwitz-criterion, polynomial-root-finding, durand-kerner-method, nyquist-stability-criterion, structured-singular-value]
sources:
  - paper: doi:10.1007/BF02551236
    title: Andrew C. Bartlett, Christopher V. Hollot and Huang Lin, Root locations of an entire polytope of polynomials, it suffices to check the edges, Mathematics of Control, Signals, and Systems 1(1) (1988)
    locator: the main theorem on the boundary of the root space and its corollary for root regions
  - book: isbn:013781576X
    title: S. P. Bhattacharyya, H. Chapellat and L. H. Keel, Robust Control, The Parametric Approach, Prentice Hall, 1995
    locator: Chapter 6, The Edge Theorem (Assumption 6.1 on the degree and Theorem 6.1)
---

The edge theorem tells where the roots of a whole family of polynomials can be, when the coefficients depend affinely on uncertain parameters in a box or, more generally, fill a convex polytope. A family like this has infinitely many members, and testing only its corner polynomials is not enough: the roots of a member in the middle can cross into the right half plane while every corner is Hurwitz. Bartlett, Hollot and Lin (1988) showed that the one-dimensional edges of the polytope are enough. The boundary of the set of all roots is made of roots of edge polynomials, so a region that contains the roots of every edge contains the roots of every member, provided the region has no holes. Each edge is a one-parameter family, and checking it is a finite computation.

## Statement

**Setting.** Let $p_1, \dots, p_m$ be polynomials of degree at most $n$ with real (or complex) coefficients, and let

$$\mathcal{P} = \operatorname{conv}\{p_1, \dots, p_m\} = \Bigl\{ \textstyle\sum_i \lambda_i p_i : \lambda_i \ge 0,\ \sum_i \lambda_i = 1 \Bigr\}$$

be their polytope in the vector space of coefficients. Assume that every member of $\mathcal{P}$ has degree exactly $n$ (the leading coefficient never vanishes on $\mathcal{P}$). An exposed edge of $\mathcal{P}$ is a one-dimensional face $\{(1 - \lambda) p_i + \lambda p_j : \lambda \in [0, 1]\}$ of the [convex polytope](/convex-polytope/); let $\mathcal{E}$ be the union of the exposed edges. The root set of a family $\mathcal{F}$ is $R(\mathcal{F}) = \{ z \in \mathbb{C} : p(z) = 0 \text{ for some } p \in \mathcal{F} \}$.

**Theorem (edge theorem, Bartlett, Hollot and Lin 1988).** The boundary of $R(\mathcal{P})$ is contained in $R(\mathcal{E})$.

**Corollary.** Let $D \subset \mathbb{C}$ be open, and let every connected component of $\mathbb{C} \setminus D$ be unbounded (this holds for every simply connected open set, such as the open left half plane or the open unit disc). Then every member of $\mathcal{P}$ has all its roots in $D$ if and only if every member of every exposed edge has all its roots in $D$.

## In plain words

Plot every root of every polynomial in the family. You get a region of the complex plane. The theorem says that the outline of this region is drawn only by the edges of the family: the straight-line blends of two corner polynomials. So, to see whether the region stays inside a safe area such as the left half plane, you can follow the roots along each edge, which is a one-parameter question. The corners alone are not enough, because a blend of two good polynomials can be bad. The safe area must have no holes, or the region could cover a hole while its outline stays outside the hole.

## Proof

**Value sets.** For $z \in \mathbb{C}$, the map $L_z(p) = p(z)$ is linear in the coefficients of $p$. So the value set $V(z) = \{ p(z) : p \in \mathcal{P} \}$ is the image of a polytope under a linear map into $\mathbb{C} = \mathbb{R}^2$: a convex polygon, a segment or a point. And $z \in R(\mathcal{P})$ exactly when $0 \in V(z)$.

**Boundary points of a value set come from edges.** Let $w$ be a point on the boundary of $V(z)$. A supporting line of $V(z)$ through $w$ meets $V(z)$ in a segment or a point, and its preimage in $\mathcal{P}$ is a face $F$ of $\mathcal{P}$ with $L_z(F)$ equal to that segment or point. The vertices and edges of $F$ form a connected graph, and they are vertices and edges of $\mathcal{P}$. The image of this graph under $L_z$ is a connected set that contains the ends of the segment, so it covers the segment, and $w = L_z(e)$ for a point $e$ on an exposed edge of $\mathcal{P}$. (If $V(z)$ is a segment or a point, the same argument applies with $F = \mathcal{P}$.)

**The theorem.** Let $z$ be a boundary point of $R(\mathcal{P})$. Since $\mathcal{P}$ is compact, $R(\mathcal{P})$ is closed, so $z \in R(\mathcal{P})$ and $0 \in V(z)$. If $0$ were an interior point of the polygon $V(z)$, then, because its corners $p_i(z')$ move continuously with $z'$, $0$ would stay inside $V(z')$ for all $z'$ near $z$, and $z$ would be an interior point of $R(\mathcal{P})$. So $0$ is on the boundary of $V(z)$, and by the previous step $e(z) = 0$ for some polynomial $e$ on an exposed edge: $z \in R(\mathcal{E})$.

**The corollary.** The "only if" part holds because $\mathcal{E} \subset \mathcal{P}$. For the "if" part, assume $R(\mathcal{E}) \subset D$, and suppose some $w \in R(\mathcal{P})$ is not in $D$. The degree is fixed and the leading coefficient is bounded away from 0 on the compact set $\mathcal{P}$, so all roots are bounded and $R(\mathcal{P})$ is bounded. The component $C$ of $\mathbb{C} \setminus D$ that contains $w$ is connected and unbounded, so it contains $w \in R(\mathcal{P})$ and a point outside $R(\mathcal{P})$. A connected set that meets a set and its complement meets its boundary, so $C$ contains a boundary point of $R(\mathcal{P})$. By the theorem that point is in $R(\mathcal{E}) \subset D$, but it is in $C$, outside $D$: a contradiction.

## Consequences

- **Affine parameter dependence.** If $p(s, q) = a_0(s) + q_1 a_1(s) + \dots + q_k a_k(s)$ with each $q_i$ in an interval, the family is the image of a box under a linear map, a polytope with at most $2^k$ vertices. Its exposed edges are covered by the images of the $k\,2^{k-1}$ edges of the box, so it is enough to check those. This covers closed-loop characteristic polynomials of plants whose numerator and denominator coefficients depend affinely on the parameters, with a fixed controller.
- **Checking one edge for Hurwitz stability.** For $D$ the open left half plane, the edge $[p, q]$ (of constant degree) is Hurwitz if and only if $p$ and $q$ are Hurwitz and there is no $\omega \ge 0$ at which $p(j\omega)$ and $q(j\omega)$ point in opposite directions. Proof by zero exclusion, as in the [Kharitonov theorem](/kharitonov-theorem/): a member $(1 - \lambda) p + \lambda q$ with $0 < \lambda < 1$ has a root $j\omega$ exactly when $p(j\omega) = -\frac{\lambda}{1 - \lambda} q(j\omega)$. The candidate frequencies are the real roots of the polynomial $\operatorname{Im}\bigl(p(j\omega)\overline{q(j\omega)}\bigr)$, of degree at most $2n - 1$ in $\omega$; at each, check the sign of the real part.
- **Other regions.** The corollary holds for any region without holes: a sector for a minimum damping ratio, a half plane $\operatorname{Re} s < -\alpha$ for a minimum decay rate, or the unit disc for Schur stability of discrete-time systems. Kharitonov's four polynomials work only for the left half plane and independent coefficients.
- **Relation to Kharitonov.** An interval polynomial is a polytope (a box), so the edge theorem applies to it, with $(n + 1) 2^n$ edges. For Hurwitz stability, Kharitonov's theorem reduces these to four vertices. For general polytopes no such reduction holds, as the example below shows.

**Example.** Let $p(s) = s^4 + s^3 + 3 s^2 + 2 s + 1$ and $q(s) = s^4 + 2 s^3 + 6 s^2 + 11 s + 1$. For a quartic with positive coefficients, the Hurwitz conditions are $a_3 a_2 > a_4 a_1$ and $a_3 a_2 a_1 > a_4 a_1^2 + a_3^2 a_0$. For $p$: $3 > 2$ and $6 > 5$. For $q$: $12 > 11$ and $132 > 125$. Both vertices are Hurwitz. On the edge, $p(j\omega)$ and $q(j\omega)$ point in opposite directions at $\omega = 1.9122$ (ratio $-0.4494$) and at $\omega = 2.1987$ (ratio $-2.1287$), so the members with $\lambda = 0.3100$ and $\lambda = 0.6804$ have roots on the imaginary axis, and the members between them are not Hurwitz. The midpoint $s^4 + 1.5 s^3 + 4.5 s^2 + 6.5 s + 1$ fails the second condition ($43.875 < 44.5$), and its roots are $0.0079 \pm 2.0714j$, $-1.3421$ and $-0.1737$. A test of the vertices alone would wrongly accept this family.

## Tightness

- **Vertices are not enough.** The example above is a polytope with two vertices (a single edge) whose vertices are Hurwitz while the edge is not.
- **The region must have no holes.** Take the annulus $D = \{1 < |s| < 3\}$, whose complement has the bounded component $\{|s| \le 1\}$. With complex coefficients (the theorem and its proof do not use real coefficients), let $\mathcal{P} = \operatorname{conv}\{s - c_0, s - c_1, s - c_2\}$ with $c_k = 2.5\, e^{2\pi j k/3}$. The root of $s - c$ is $c$, so $R(\mathcal{P})$ is the filled triangle with corners $c_k$, and the edge roots are its sides. The sides are at distance $2.5 \cos(\pi/3) = 1.25$ from 0 and within distance $2.5$, so all edge roots lie in $D$. But the member $s$ (all $\lambda_i = 1/3$) has the root $0 \notin D$.
- **The degree must not drop.** If the leading coefficient vanishes somewhere on $\mathcal{P}$, a root goes to infinity there, $R(\mathcal{P})$ is unbounded, and the proof of the corollary fails.
- **Sampling is not a proof.** Random members of $\mathcal{P}$ can show a member that is not Hurwitz, but no finite sample of points proves that all members are Hurwitz. The edge theorem replaces the sample by a finite set of one-parameter checks.

## History

After Kharitonov's theorem of 1978 became known, it was natural to ask for families whose coefficients are not independent. Bartlett, Hollot and Lin answered this for polytopes of polynomials in 1988, in the first volume of Mathematics of Control, Signals, and Systems, with the title "Root locations of an entire polytope of polynomials: it suffices to check the edges". Later work gave finite tests for single edges and sharper results for interval plants in a loop with a fixed controller. The textbook of Bhattacharyya, Chapellat and Keel (1995) presents these results together.

## References
