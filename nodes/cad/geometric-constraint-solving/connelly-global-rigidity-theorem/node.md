---
tag: 52GW6C
kind: theorem
slug: connelly-global-rigidity-theorem
name: Connelly's sufficient condition for global rigidity
aliases:
- Connelly stress condition
area: cad/geometric-constraint-solving
level: research
summary: A generic framework with n vertices in d dimensions is globally rigid if it has an equilibrium stress whose stress matrix has rank n - d - 1.
prereqs: [equilibrium-stress-matrix, global-rigidity]
see_also: [gortler-healy-thurston-theorem, hendrickson-global-rigidity-conditions, jackson-jordan-theorem, henneberg-construction, asimow-roth-theorem, semidefinite-programming, schwartz-zippel-lemma]
sources:
  - paper: doi:10.1007/s00454-004-1124-4
    title: R. Connelly, Generic global rigidity, Discrete and Computational Geometry 33(4), 549 to 563, 2005
    locator: the main theorem, the shared stresses of equivalent generic frameworks, and Section 4 on affine images and conics at infinity
  - paper: doi:10.1007/BF01404753
    title: R. Connelly, Rigidity and energy, Inventiones Mathematicae 66(1), 11 to 33, 1982
    locator: the stress energy and the use of the stress matrix to prove that a framework is unique
  - paper: doi:10.1353/ajm.0.0132
    title: Steven J. Gortler, Alexander D. Healy and Dylan P. Thurston, Characterizing generic global rigidity, American Journal of Mathematics 132(4), 897 to 939, 2010
    locator: the restatement of Connelly's proof, the smoothness of the measurement variety at a generic point, and the randomized algorithm
  - paper: doi:10.1016/j.jctb.2004.11.002
    title: Bill Jackson and Tibor Jordán, Connected rigidity matroids and unique realizations of graphs, Journal of Combinatorial Theory, Series B 94(1), 1 to 29, 2005
    locator: the use of Connelly's condition and Henneberg 1-extensions to prove sufficiency in the plane
---

## Statement

Let $G = (V, E)$ be a graph with $n$ vertices and let $p$ be a placement in $\mathbb{R}^d$. An *equilibrium stress* of $(G, p)$ is a vector $\omega \in \mathbb{R}^E$ with $\sum_{j} \omega_{ij} (p_j - p_i) = 0$ at every vertex $i$, and its [stress matrix](/equilibrium-stress-matrix/) $\Omega$ is the $n \times n$ Laplacian with the signed weights $\omega$. The placement is *generic* if its coordinates are algebraically independent over $\mathbb{Q}$. A framework is *globally rigid* if every framework in $\mathbb{R}^d$ with the same bar lengths is congruent to it.

**Theorem (Connelly 2005).** Let $p$ be a generic placement of $G$ in $\mathbb{R}^d$ with $n \ge d + 2$. If $(G, p)$ has an equilibrium stress whose stress matrix has rank $n - d - 1$, then $(G, p)$ is globally rigid. Moreover, then every generic framework of $G$ in $\mathbb{R}^d$ is globally rigid, so $G$ is generically globally rigid.

The rank $n - d - 1$ is the largest possible: for a stress of a framework that affinely spans $\mathbb{R}^d$, the coordinate vectors and the all-ones vector lie in the kernel of $\Omega$. No sign condition on $\Omega$ is needed. For $n \le d + 1$ a generic framework is globally rigid exactly when $G$ is complete.

## In plain words

Put a framework of bars and pins in general position. Suppose the bars can carry a set of tensions and compressions that balance at every pin, and that this balanced load is as rich as it can be, in a precise sense that a matrix built from it has the largest rank allowed. Then the bar lengths fix the whole shape: no other shape, near or far, has the same bar lengths. The proof shows that any other shape with these lengths must carry the same balanced load. That forces the other shape to be a linear stretch of the first, and a stretch that keeps all bar lengths in general position must be a rigid motion.

## Proof

Fix $p$ generic with $n \ge d + 2$, a stress $\omega$ of $(G, p)$ with $\operatorname{rank} \Omega = n - d - 1$, and a framework $(G, q)$ in $\mathbb{R}^d$ with the same bar lengths. Let $f = f_G$ be the edge function $q \mapsto (\lVert q_i - q_j \rVert^2)_{ij \in E}$, so that $df(q) = 2 R(G, q)$, where $R$ is the [rigidity matrix](/rigidity-matrix/). Let $r$ be the generic rank of $R(G, \cdot)$, and let $X \subseteq \mathbb{R}^E$ be the Zariski closure of the image of $f$, the *measurement variety*. It is irreducible, it is defined over $\mathbb{Q}$, and it has dimension $r$.

**Step 1: $q$ is a regular point.** Let $Z$ be the set of placements where the rank of $R(G, \cdot)$ is below $r$. As on the [Hendrickson page](/hendrickson-global-rigidity-conditions/), Sard's theorem in its semialgebraic form shows that $f(Z)$ lies in a proper subvariety of $X$ defined over $\mathbb{Q}$, so some polynomial $g$ with rational coefficients vanishes on $f(Z)$ and not on $X$. Then $g \circ f$ is a nonzero polynomial with rational coefficients, so $g(f(p)) \ne 0$ at the generic $p$. Since $f(q) = f(p)$, $q \notin Z$: the rank of $R(G, q)$ is $r$.

**Step 2: $f(p)$ is a smooth point of $X$.** The singular points of $X$ form a proper subvariety defined over $\mathbb{Q}$. The same argument with a polynomial that vanishes on it and not on $X$ shows that $f(p)$ is not singular. So the tangent space $T$ of $X$ at $f(p)$ has dimension $r$.

**Step 3: $\omega$ is a stress of $(G, q)$.** Let $h$ be any polynomial that vanishes on $X$. Then $h \circ f = 0$ identically, and its derivative at $q$ is $\nabla h(f(q))^\top df(q) = 0$. So every column of $df(q)$ is orthogonal to all such gradients at the point $f(q) = f(p)$, which means the image of $df(q)$ lies in $T$. By Step 1 that image has dimension $r = \dim T$, so it equals $T$. The same holds at $p$. Hence $df(q)$ and $df(p)$ have the same image, so they have the same left kernel. The stress $\omega$ is in the left kernel of $R(G, p)$, so it is in the left kernel of $R(G, q)$, and by Fact 3 of the rigidity matrix page it is an equilibrium stress of $(G, q)$.

**Step 4: $q$ is an affine image of $p$.** The points of $p$ affinely span $\mathbb{R}^d$ because $p$ is generic and $n \ge d + 1$. The stress matrix has rank $n - d - 1$ and $\omega$ is a stress of both frameworks, so by Fact 4 of the [stress matrix page](/equilibrium-stress-matrix/) there are a $d \times d$ matrix $A$ and a vector $b$ with $q_i = A p_i + b$ for every $i$. In matrix form: $\ker \Omega$ is spanned by the $d$ coordinate columns of $p$ and the all-ones vector, and the coordinate columns of $q$ lie in $\ker \Omega$.

**Step 5: the affine map is an isometry.** For every edge $ij$, with $v = p_i - p_j$,
$$ \lVert A v \rVert^2 = \lVert q_i - q_j \rVert^2 = \lVert p_i - p_j \rVert^2 = \lVert v \rVert^2, \qquad \text{so} \qquad v^\top (A^\top A - I) \, v = 0 . $$
A nonzero symmetric matrix $Q$ with $v^\top Q v = 0$ for every edge vector $v$ is called a *conic at infinity* that holds the edge directions. Connelly proved that at a generic placement with a stress of rank $n - d - 1$, the edge directions do not lie on any conic at infinity (Connelly 2005, Section 4; see the lemma below). So $A^\top A = I$, $A$ is orthogonal, $x \mapsto A x + b$ is an isometry, and $(G, q)$ is congruent to $(G, p)$. $\square$

**Lemma (no conic at infinity).** Let $p$ be generic with $n \ge d + 2$, and let $(G, p)$ have a stress whose stress matrix has rank $n - d - 1$. Then no nonzero symmetric $Q$ satisfies $(p_i - p_j)^\top Q (p_i - p_j) = 0$ for all edges $ij$. This is the lemma that Connelly proves in Section 4 of his paper. One ingredient is easy: every vertex has degree at least $d + 1$. Indeed, if a vertex $i$ had at most $d$ neighbors, the equilibrium at $i$ would be a linear relation among at most $d$ generic vectors $p_j - p_i$, so $\omega$ would vanish on all edges at $i$, row $i$ of $\Omega$ would be zero, and the unit vector $e_i$ would lie in $\ker \Omega$. But every vector of $\ker \Omega$ has the form $x_j = a \cdot p_j + c$, and $e_i$ vanishes at $n - 1 \ge d + 1$ generic points, which forces $a = 0$ and $c = 0$, a contradiction.

*Why the lemma reduces to one example.* The symmetric $Q$ with $v_e^\top Q v_e = 0$ for all edges form the kernel of a linear map from the $D$-dimensional space of symmetric matrices, $D = d(d + 1)/2$, whose matrix has polynomial entries in $p$. If this kernel is nonzero at a generic $p$, all $D \times D$ minors vanish identically, so the kernel is nonzero at every placement. So it is enough to exhibit one placement of $G$, generic or not, where only $Q = 0$ works. *The plane.* For $d = 2$ the proof is short. A nonzero binary quadratic form vanishes on at most two lines through the origin. At a generic placement no two distinct edges are parallel, because parallelism of two given edges is a polynomial condition that fails at some placement. Every vertex has degree at least 3 and $n \ge 4$, so there are at least 6 edges, the edge directions are at least 3 distinct lines, and $Q = 0$. *The line.* For $d = 1$, $Q$ is a number and $v^2 Q = 0$ for one edge with $v \ne 0$ gives $Q = 0$.

**From one generic placement to all.** Let $\omega_1, \ldots, \omega_s$ be a basis of the stress space at $p$, found by elimination on $R(G, p)^\top$. Near a regular point this basis can be chosen with entries that are rational functions of the placement with rational coefficients, so the statement "some combination $\sum_k c_k \omega_k$ has stress matrix of rank at least $n - d - 1$" is the nonvanishing of a polynomial with rational coefficients in the placement and the $c_k$. At one generic placement it holds, so the polynomial is not zero, so it holds at every generic placement. By the theorem, every generic framework of $G$ is globally rigid. $\square$

## Consequences

- **A certificate that can be checked.** For a given graph, choose a random integer placement, compute a basis of the stresses with exact arithmetic, take a random combination, and compute the rank of its stress matrix. If the rank is $n - d - 1$ and the placement is regular, $G$ is generically globally rigid. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), a random placement in a large box gives the generic stress rank with high probability. Gortler, Healy and Thurston turned this into a randomized polynomial-time algorithm.
- **With the converse, a characterization.** [Gortler, Healy and Thurston](/gortler-healy-thurston-theorem/) proved that a generically globally rigid graph with $n \ge d + 2$ always has such a stress. So generic global rigidity is decided by the generic stress rank in every dimension, although no purely combinatorial test is known for $d \ge 3$.
- **Constructions that keep the condition.** Connelly proved that a Henneberg 1-extension (split an edge and join the new vertex to one more vertex) keeps the stress condition when the graph minus the split edge is rigid. Jackson and Jordán combined this with a construction of all 3-connected redundantly rigid graphs in the plane from $K_4$ by edge additions and 1-extensions. This proves the [Jackson and Jordán theorem](/jackson-jordan-theorem/): in the plane, [Hendrickson's conditions](/hendrickson-global-rigidity-conditions/) are sufficient.
- **Coning.** Connelly and Whiteley showed that coning, adding a new vertex joined to all others, takes generically globally rigid graphs in $\mathbb{R}^d$ to generically globally rigid graphs in $\mathbb{R}^{d + 1}$, again through stresses.
- **Universal rigidity.** If the stress matrix is in addition positive semidefinite, the energy argument of Connelly (1982) shows that the framework is unique in every dimension, not only in $\mathbb{R}^d$, whenever the edge directions do not lie on a conic at infinity. Such a stress can be searched for by [semidefinite programming](/semidefinite-programming/).

## Tightness

The examples use exact rational arithmetic at random integer placements.

- **The rank cannot be lower.** For $K_{5,5}$ in $\mathbb{R}^3$, the stress space has dimension 1 and the stress matrix has rank 2, below $10 - 3 - 1 = 6$. The graph is 5-connected and redundantly rigid, and still not generically globally rigid. So a stress of lower rank is not enough, even together with Hendrickson's conditions.
- **Small cases.** $K_4$ in the plane has a one-dimensional stress space with stress matrix of rank $1 = 4 - 2 - 1$. $K_5$ in $\mathbb{R}^3$ has rank $9 = 3 \cdot 5 - 6$, one stress, and stress matrix rank $1 = 5 - 3 - 1$. The wheel with a hub and a 5-cycle in the plane has 10 edges, rank 9, one stress that is nonzero on every edge, and stress matrix rank $3 = 6 - 2 - 1$. All three are globally rigid by the theorem.
- **More than one stress.** $K_{4,4}$ in the plane has rank $13 = 2 \cdot 8 - 3$ and three independent stresses. The three basis stresses that elimination returns have stress matrices of ranks 4, 4 and 5, and a random combination has rank $5 = 8 - 2 - 1$. So the condition asks for one stress of full rank somewhere in the stress space, and a single basis vector can miss it.
- **Genericity is needed.** At special placements the condition can fail for globally rigid frameworks. The 4-cycle at $0, 1, 2, 3$ on a line inside the plane, with lengths $1, 1, 1, 3$, is globally rigid, but its points do not span the plane, so the rank count $n - d - 1$ does not apply, and its graph is not even generically rigid. In the other direction, at a special placement whose edge directions lie on a conic at infinity, a stress of rank $n - d - 1$ does not prevent an affine flex, which is why Step 5 needs the genericity of $p$.

## History

Connelly introduced the stress matrix and the stress energy in his 1982 study of tensegrity frameworks, where a positive semidefinite stress matrix proves that a framework of cables and struts is rigid. In a 1991 note he used stresses to show that $K_{5,5}$ is a counterexample to Hendrickson's conjecture in three dimensions. The general sufficient condition for generic frameworks, without a sign condition, appeared in his 2005 paper, after a long circulation as a preprint. Jackson and Jordán used it in the same year to settle the plane. Gortler, Healy and Thurston proved the converse in 2010, which turned Connelly's condition into an exact test.

## References
