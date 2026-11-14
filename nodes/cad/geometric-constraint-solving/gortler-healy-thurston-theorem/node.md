---
tag: SPQDQE
kind: theorem
slug: gortler-healy-thurston-theorem
name: Gortler-Healy-Thurston theorem
aliases:
- generic global rigidity theorem
area: cad/geometric-constraint-solving
level: research
summary: The converse of Connelly's condition. A generic framework with n >= d + 2 vertices is globally rigid exactly when some stress matrix has rank n - d - 1, so global rigidity is generic.
prereqs: [connelly-global-rigidity-theorem, equilibrium-stress-matrix]
see_also: [hendrickson-global-rigidity-conditions, jackson-jordan-theorem, global-rigidity, asimow-roth-theorem, witness-configuration-method, schwartz-zippel-lemma, monte-carlo-algorithm]
sources:
  - paper: doi:10.1353/ajm.0.0132
    title: Steven J. Gortler, Alexander D. Healy and Dylan P. Thurston, Characterizing generic global rigidity, American Journal of Mathematics 132(4), 897 to 939, 2010
    locator: Section 1.1 (main results), Section 2 (the domain of stress satisfiers, the range, properness and the mod-two degree), Section 5 (the randomized algorithm) and Section 6 (flexes one dimension higher); arXiv 0710.0926
  - paper: doi:10.1007/s00454-004-1124-4
    title: R. Connelly, Generic global rigidity, Discrete and Computational Geometry 33(4), 549 to 563, 2005
    locator: the sufficient direction and the conjecture that the stress condition is also necessary
  - paper: doi:10.1137/0221008
    title: Bruce Hendrickson, Conditions for unique graph realizations, SIAM Journal on Computing 21(1), 65 to 84, 1992
    locator: the earlier necessary conditions, proved by reflection and by a degree argument on a circle of flexes
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, CRC Press, 2018
    locator: the chapter on global rigidity and stress matrices
---

## Statement

Let $G = (V, E)$ be a graph with $n \ge d + 2$ vertices. For a placement $p$ in $\mathbb{R}^d$, an *equilibrium stress* is a vector $\omega \in \mathbb{R}^E$ with $\sum_j \omega_{ij} (p_j - p_i) = 0$ at every vertex $i$, and its [stress matrix](/equilibrium-stress-matrix/) $\Omega$ is the $n \times n$ Laplacian with the signed weights $\omega$. A placement is *generic* if its coordinates are algebraically independent over $\mathbb{Q}$, and a framework is *globally rigid* if every framework in $\mathbb{R}^d$ with the same bar lengths is congruent to it.

**Theorem (Gortler, Healy and Thurston 2010).** Let $p$ be a generic placement of $G$ in $\mathbb{R}^d$, with $n \ge d + 2$. If $(G, p)$ is globally rigid, then $(G, p)$ has an equilibrium stress whose stress matrix has rank $n - d - 1$.

With [Connelly's theorem](/connelly-global-rigidity-theorem/), which is the converse, this gives:

**Corollary.** For $n \ge d + 2$ and generic $p$, the framework $(G, p)$ is globally rigid if and only if it has a stress matrix of rank $n - d - 1$, the largest possible rank. Either every generic framework of $G$ in $\mathbb{R}^d$ is globally rigid, or none is. So *generic global rigidity* is a property of the graph.

**Theorem (flex one dimension higher).** If $G$ is not generically globally rigid in $\mathbb{R}^d$, then a generic framework of $G$ in $\mathbb{R}^d$ can be joined to a framework that is not congruent to it by a continuous path of frameworks in $\mathbb{R}^{d + 1}$ that keeps all bar lengths.

## In plain words

Connelly showed that a rich enough balanced load on the bars of a framework in general position proves that the bar lengths fix the shape. This theorem says that nothing else can. If the shape is fixed by its bar lengths, such a load must exist. So there is a single linear algebra test that decides whether a graph has a unique shape, for almost all choices of bar lengths, in every dimension. The test needs random numbers but no search. The answer depends only on the graph, not on the lengths, as long as the lengths come from a shape in general position.

## Proof

This is an outline of the proof of Gortler, Healy and Thurston, Section 2, with the steps named as in their paper. Fix a generic $p$ and suppose that no stress of $(G, p)$ has a stress matrix of rank $n - d - 1$. We build a framework $(G, q)$ with the same bar lengths that is not congruent to $(G, p)$. If $G$ is not generically rigid, then $(G, p)$ is already flexible by the [Asimow and Roth theorem](/asimow-roth-theorem/), so assume that $G$ is generically rigid. Write $\ell(q) = (\lVert q_i - q_j \rVert^2)_{ij \in E}$ for the squared edge lengths.

**Step 1: choose a generic stress.** Take a stress $\omega$ of $(G, p)$ that is generic in the stress space. Its stress matrix $\Omega$ has the largest rank among the stresses of $(G, p)$, which is below $n - d - 1$ by assumption. So its kernel $K = \ker \Omega$ has dimension $k > d + 1$, and $K$ contains the coordinate vectors of $p$ and the all-ones vector.

**Step 2: the domain.** Let $A(\Omega)$ be the set of placements $q$ in $\mathbb{R}^d$ for which $\omega$ is an equilibrium stress. By Fact 2 of the stress matrix page this is the condition $\Omega Q = 0$ on the coordinate matrix $Q$, so $A(\Omega) = K^d$, a linear space of dimension $dk$ that contains $p$. Every affine image of $p$ is in it, but since $k > d + 1$ it contains much more. The isometry group $\mathrm{E}(d)$ acts on it, and the domain is the quotient $X = A(\Omega) / \mathrm{E}(d)$. The authors show that the singular part of $X$, from placements with a small affine span, has codimension at least 2.

**Step 3: the range.** Let $B(\Omega) = \ell(A(\Omega))$ and let $L(\Omega)$ be the smallest linear subspace of $\mathbb{R}^E$ that contains it. A key fact, from the generic choice of $\omega$ and a Bertini type argument on the contact locus of the dual variety, is that $B(\Omega)$ is *flat*: it has the same dimension as $L(\Omega)$. The authors identify $L(\Omega)$ as the span of the vectors $\big((x_i - x_j)(y_i - y_j)\big)_{ij \in E}$ for $x, y \in K$, and they show that $X$ and $L(\Omega)$ have the same dimension.

**Step 4: the map and its degree.** The map $\bar\ell : X \to L(\Omega)$ induced by $\ell$ is proper. Since the singular part of $X$ has codimension at least 2, $\bar\ell$ has a well defined degree modulo 2, which is the parity of the number of preimages of any regular value. Now $L(\Omega)$ is a linear space that contains $\ell(p)$, whose coordinates are all positive, so it also contains $-\ell(p)$, whose coordinates are all negative. No placement has a negative squared length, so $-\ell(p)$ has no preimage at all. A point with no preimage is a regular value, so the degree modulo 2 is 0.

**Step 5: a second framework.** Because $p$ is generic, $\ell(p)$ is a regular value of $\bar\ell$. So the number of classes $[q] \in X$ with $\ell(q) = \ell(p)$ is even. The class $[p]$ is one of them, so there is another, $[q] \ne [p]$. Then $(G, q)$ is a framework in $\mathbb{R}^d$ with the same bar lengths as $(G, p)$, and it is not congruent to it. So $(G, p)$ is not globally rigid. $\square$

The parity idea is the same as in the proof of [Hendrickson's](/hendrickson-global-rigidity-conditions/) redundant rigidity condition, where the domain is a circle of flexes and the second point comes from the intermediate value theorem. Here the domain is the set of all frameworks that share the stress $\omega$, and the second point comes from the mod 2 degree. The corollary follows: if one generic framework is globally rigid, it has a stress of rank $n - d - 1$, and by the last part of the proof of Connelly's theorem, so has every generic framework, which is then globally rigid by Connelly's theorem.

## Consequences

- **A randomized test in every dimension.** Choose a random integer placement $p$ in a box $\{1, \ldots, N\}^{dn}$. Compute the rank of the [rigidity matrix](/rigidity-matrix/) exactly. If it is $dn - D$, with $D = d(d + 1)/2$, the placement is regular and $G$ is generically rigid. Then compute a basis of the stresses, take a random combination, and compute the rank of its stress matrix. At a regular placement this rank is at most the generic value, so the answer "rank $n - d - 1$, globally rigid" is always correct, and only a "no" answer can be wrong. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) the error probability is at most a degree bound divided by $N$. This is a [Monte Carlo algorithm](/monte-carlo-algorithm/) with polynomial running time, and the authors analyze it with computation modulo random primes.
- **No search over realizations.** The test never looks for a second framework. It decides a question about all realizations of a system of distance equations by linear algebra at one random point, which is the same idea as the [witness configuration method](/witness-configuration-method/) for local rigidity.
- **A property of the graph.** In the plane, generic global rigidity has a combinatorial form, the [Jackson and Jordán theorem](/jackson-jordan-theorem/). In $\mathbb{R}^3$ no combinatorial form is known, but the theorem shows that one exists in principle, since the answer depends only on $G$.
- **Flexes in one more dimension.** A generic framework that is not globally rigid in $\mathbb{R}^d$ can be moved continuously in $\mathbb{R}^{d + 1}$ to a second shape that lies in $\mathbb{R}^d$. In the plane, a framework with a mirror image can turn the mirror image into reach through space, like a hinged figure flipped over.
- **Universal rigidity is different.** Global rigidity asks about frameworks in $\mathbb{R}^d$ only. The condition here puts no sign on $\Omega$, while uniqueness in all dimensions needs a positive semidefinite stress matrix in Connelly's energy argument.

## Tightness

The numbers are exact ranks at random integer placements.

- **$K_{5,5}$ in space.** It satisfies [Hendrickson's](/hendrickson-global-rigidity-conditions/) two conditions: it is 5-connected, its rigidity matrix has rank $24 = 3 \cdot 10 - 6$, and the rank stays 24 after the removal of any edge. Its stress space has dimension 1 and the stress matrix has rank 2, below $6 = 10 - 3 - 1$. By the theorem, its generic frameworks in $\mathbb{R}^3$ are not globally rigid. This is the example that Connelly found in 1991, and the theorem explains it.
- **The prism in the plane.** The triangular prism has 9 independent edges and no stress, so the only stress matrix is zero, of rank $0 < 3$. By the theorem it is not globally rigid, which matches the second realization built on the Hendrickson page.
- **Why $n \ge d + 2$.** For $n = d + 1$ the target rank $n - d - 1$ is 0, and the zero stress reaches it for every graph. $K_{d + 1}$ is globally rigid, but $K_{d + 1}$ minus an edge is not even rigid. So the equivalence fails for $n = d + 1$, and the statement needs $n \ge d + 2$.
- **Genericity is needed.** The 4-cycle at $0, 1, 2, 3$ on a line inside the plane, with lengths $1, 1, 1, 3$, is globally rigid, although the 4-cycle is not even generically rigid in the plane. Its points do not span the plane, so $n - d - 1 = 1$ is not the right target: its only stress is the stress of the line framework, and its stress matrix has rank 2. The theorem speaks only of generic frameworks.

## History

Hendrickson (1992) found the first necessary conditions and asked whether they suffice. Connelly found $K_{5,5}$ as a counterexample in space, proved that a full rank stress matrix suffices (circulated for years, published 2005), and conjectured that it is also necessary. Steven Gortler, Alexander Healy and Dylan Thurston proved the conjecture in a paper that appeared on arXiv in 2007 and in the American Journal of Mathematics in 2010. Their proof replaced the circle of flexes in Hendrickson's argument by the space of all frameworks that share a generic stress, and used the mod 2 degree of the squared length map on it. The same paper gave the randomized polynomial-time algorithm and the theorem on flexes in one dimension higher.

## References
