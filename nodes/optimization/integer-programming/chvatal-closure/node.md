---
tag: BEHN16
kind: concept
slug: chvatal-closure
name: Chvátal closure
aliases:
- Chvátal-Gomory closure
- elementary closure
- first Chvátal closure
- Chvátal rank
area: optimization/integer-programming
level: advanced
summary: The polyhedron obtained by adding all Chvátal-Gomory cuts once.
prereqs: [chvatal-gomory-cut, integer-hull, totally-dual-integrality]
see_also: [chvatal-gomory-cut, chvatal-gomory-finite-convergence, integer-hull, totally-dual-integrality, lift-and-project, zero-half-cut, gomory-cutting-plane-algorithm, integrality-gap]
sources:
  - paper: "Vašek Chvátal, Edmonds polytopes and a hierarchy of combinatorial problems, Discrete Mathematics 4 (1973), 305 to 337"
    locator: the closure operation for polytopes and the notion of rank
  - paper: "Alexander Schrijver, On cutting planes, Annals of Discrete Mathematics 9 (1980), 291 to 296"
    locator: the closure of a rational polyhedron is a rational polyhedron
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 23 (cutting planes, the closure and its rank)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (the Chvátal closure and the Chvátal rank)
  - paper: "Friedrich Eisenbrand, On the membership problem for the elementary closure of a polyhedron, Combinatorica 19 (1999), 297 to 300"
    locator: NP-hardness of membership in the closure
  - paper: "Friedrich Eisenbrand and Andreas S. Schulz, Bounds on the Chvátal rank of polytopes in the 0/1-cube, Combinatorica 23 (2003), 245 to 261"
    locator: the upper bound on the rank of 0/1 polytopes
  - paper: "Thomas Rothvoss and Laura Sanità, 0/1 polytopes with quadratic Chvátal rank, Integer Programming and Combinatorial Optimization (IPCO 2013), Lecture Notes in Computer Science 7801, Springer, 2013"
    locator: the quadratic lower bound
  - paper: "Matteo Fischetti and Andrea Lodi, Optimizing over the first Chvátal closure, Mathematical Programming 110 (2007), 3 to 20"
    locator: separation of rank-one cuts by a mixed-integer program
  - paper: "Daniel Dadush, Santanu S. Dey and Juan Pablo Vielma, On the Chvátal-Gomory closure of a compact convex set, Mathematical Programming 145 (2014)"
    locator: the closure of a compact convex set is a rational polytope
---

The Chvátal closure $P'$ of a polyhedron $P$ is the set of points that satisfy every [Chvátal-Gomory cut](/chvatal-gomory-cut/) of $P$. It lies between $P$ and the [integer hull](/integer-hull/) $P_I$. For rational $P$ it is again a rational polyhedron, so the operation can be repeated: $P \supseteq P' \supseteq P'' \supseteq \cdots \supseteq P_I$. The [finite convergence theorem](/chvatal-gomory-finite-convergence/) says that some $P^{(k)}$ equals $P_I$, and the least such $k$ is the *Chvátal rank* of $P$. The rank measures how far a formulation is from ideal, and it can be large even in the plane.

## In plain words

Take all the rules of a problem and look for every way to combine them and round, as on the Chvátal-Gomory cut page. Add all the new rules at once. The region that is left is the closure. It still contains every whole-number answer, and it is smaller than the region we started with.

Now do it again with the new region, and again. Each round shaves off more of the fractional part. After a finite number of rounds, nothing fractional is left at the corners, and the region is exactly the hull of the whole-number points. The number of rounds needed is the rank. A small rank means the starting rules were already close to the best possible.

## The idea

**Definition.** For a rational polyhedron $P = \{x : Ax \le b\}$,

$$P' = \bigcap_{u \ge 0,\ u^T A \in \mathbb{Z}^n} \{x : (u^T A)\, x \le \lfloor u^T b \rfloor\}.$$

The definition depends only on $P$, not on the system: every inequality $c^T x \le \delta$ valid for $P$, with $c$ integral, gives the cut $c^T x \le \lfloor \delta \rfloor$, and these are exactly the CG cuts. Let $P^{(0)} = P$ and $P^{(k+1)} = (P^{(k)})'$. The *rank* of $P$ is the least $k$ with $P^{(k)} = P_I$, and the rank of a valid inequality for $P_I$ is the least $k$ for which it is valid for $P^{(k)}$.

**Basic properties.**

- $P_I \subseteq P' \subseteq P$, since each cut is valid for the integer points and each original row is a cut with $u$ a unit vector.
- If $P \subseteq Q$, then $P' \subseteq Q'$.
- For a face $F$ of $P$, $F' = P' \cap F$. This is the key lemma in the proof of finite convergence.
- If $P$ is integral, then $P' = P$, so the rank of an [ideal formulation](/ideal-formulation/) is 0.

**The closure is a polyhedron.** Chvátal (1973) proved this for polytopes, and Schrijver (1980) for rational polyhedra. A short proof uses [total dual integrality](/totally-dual-integrality/). By the theorem of Giles and Pulleyblank, $P = \{x : Ax \le b\}$ for some TDI system with $A$ integral. We show

$$P' = \{x : Ax \le \lfloor b \rfloor\}.$$

The inclusion $\subseteq$ holds since each row $a_i^T x \le b_i$ gives the cut $a_i^T x \le \lfloor b_i \rfloor$. For $\supseteq$, assume $P \ne \emptyset$ and take a cut $c^T x \le \lfloor \delta \rfloor$ with $c = u^T A$ integral and $\delta = u^T b$. By weak duality, $\max_P c^T x \le \delta$ is finite, and by TDI there is an integral $y \ge 0$ with $y^T A = c^T$ and $y^T b = \max_P c^T x$. For $x$ with $Ax \le \lfloor b \rfloor$,

$$c^T x = y^T A x \le y^T \lfloor b \rfloor \le \lfloor y^T b \rfloor \le \lfloor \delta \rfloor,$$

where the middle step holds because $y^T \lfloor b \rfloor$ is an integer and at most $y^T b$. So $x$ satisfies the cut. $\square$

Dadush, Dey and Vielma (2014) extended the result: the closure of any compact convex set is a rational polytope.

**The rank.**

- In dimension 2, the rank is unbounded: the triangle in the example below has rank $2t$.
- For a polytope in $[0, 1]^n$, the rank is at most $O(n^2 \log n)$ (Eisenbrand and Schulz, 2003), and there are 0/1 polytopes of rank $\Omega(n^2)$ (Rothvoss and Sanità, 2013).
- Many classical facet families have rank 1 relative to a natural formulation: Edmonds' odd set inequalities for matching, odd cycle inequalities for stable sets, and comb inequalities relative to the subtour relaxation of the [traveling salesman problem](/traveling-salesman-problem/).

**Complexity.** Deciding whether a point lies in $P'$ is coNP-complete (Eisenbrand 1999), so optimizing over $P'$ is NP-hard in general. Fischetti and Lodi (2007) separated rank-one cuts exactly with a mixed-integer program over the multipliers $u$, and found that the first closure closes a large part of the [integrality gap](/integrality-gap/) on many benchmark instances. In practice solvers approximate $P'$ by [Gomory cuts](/gomory-cutting-plane-algorithm/) from the tableau and by [zero-half cuts](/zero-half-cut/).

## Examples

**Rank one.** For $P = \{x \ge 0 : 3x_1 + 2x_2 \le 6,\ -3x_1 + 2x_2 \le 0\}$, the CG cuts $-x_1 + x_2 \le 0$ and $x_1 + x_2 \le 2$ together with $x_2 \ge 0$ describe $P_I = \operatorname{conv}\{(0,0), (2,0), (1,1)\}$. So $P' = P_I$, and the rank is 1.

**A thin triangle of rank $2t$.** For an integer $t \ge 1$, let $T_s = \operatorname{conv}\{(0, 0),\ (0, 1),\ (s, 1/2)\}$ and $P = T_t$. The integer points are $(0,0)$ and $(0,1)$, so $P_I$ is the segment from $(0,0)$ to $(0,1)$.

*Claim.* If $s \ge 1/2$ is a multiple of $1/2$ and $Q \supseteq T_s$, then $Q' \supseteq T_{s - 1/2}$.

*Proof.* Let $c^T x \le \lfloor \delta \rfloor$ be a CG cut of $Q$, with $c \in \mathbb{Z}^2$ and $\delta \ge \max_Q c^T x \ge \max_{T_s} c^T x$. We check the three vertices of $T_{s-1/2}$. At $(0, 0)$ the value is $0 \le \lfloor \delta \rfloor$, since $\delta \ge 0$. At $(0, 1)$ it is $c_2$, an integer at most $\delta$, so at most $\lfloor \delta \rfloor$. At the apex the value is $c_1 (s - 1/2) + c_2 / 2$. If $c_1 \le 0$, this is at most $c_2 / 2 \le \max(0, c_2) \le \lfloor \delta \rfloor$. If $c_1 \ge 1$, let $y = c_1 s + c_2/2 \le \delta$, the value at the apex of $T_s$. The value at the new apex is $y - c_1/2 \le y - 1/2$. Since $y$ is a multiple of $1/2$, either $y$ is an integer and $y - 1/2 < y \le \lfloor \delta \rfloor$, or $y - 1/2 = \lfloor y \rfloor \le \lfloor \delta \rfloor$. $\square$

Applying the claim $2t - 1$ times gives $P^{(2t-1)} \supseteq T_{1/2}$, which contains the point $(1/2, 1/2) \notin P_I$. So the rank is at least $2t$. For $t = 2$ the closures are exactly the triangles with apex $x_1 = 2, 3/2, 1, 1/2$, and the fourth closure is the segment, so the rank is 4. A maximization of $x_1$ by [Gomory's algorithm](/gomory-cutting-plane-algorithm/) also needs at least $2t$ cuts on this triangle.

**Matching.** For the degree polytope $\{x \ge 0 : x(\delta(v)) \le 1\}$ of any graph, the first closure is the [matching polytope](/matching-polytope/), since the odd set inequalities are rank-one cuts and Edmonds showed that they suffice. So this formulation has rank at most 1.

**Stable sets.** For the edge formulation of the stable set polytope, odd cycle inequalities have rank 1, but clique inequalities $\sum_{v \in K} x_v \le 1$ for a large clique $K$ need higher rank, which grows with $|K|$. Chvátal (1973) used such ranks to compare the difficulty of combinatorial problems.

## Where it is used

- **Measuring formulations.** The rank and the gap closed by $P'$ compare formulations and cut families, as in the work of Fischetti and Lodi.
- **Theory of cutting planes.** The closure is the model for other closures: the split closure, the [lift-and-project](/lift-and-project/) closure and the MIR closure, all of which are compared with it.
- **Proof complexity.** The rank of the empty integer set is a measure of the depth of cutting plane proofs of infeasibility.
- **Finite convergence.** The proof that repeated closures reach $P_I$ underlies the finiteness of pure cutting plane algorithms.

## References
