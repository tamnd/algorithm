---
tag: 29VNS6
kind: theorem
slug: rank-nullity-theorem
name: Rank-nullity theorem
aliases: [rank-nullity, fundamental theorem of linear maps, dimension theorem for linear maps]
area: algebra/exact-linear-algebra
level: intro
summary: For a linear map, rank plus nullity equals the dimension of the domain.
prereqs: [rank, nullspace, linear-independence]
see_also: [reduced-row-echelon-form, nullspace-computation, rank-computation, linear-system-modulo-2, smith-normal-form, wiedemann-algorithm]
sources:
  - book: isbn:9783319110790
    title: Sheldon Axler, Linear Algebra Done Right, third edition, Springer, 2015
    locator: Section 3.B, Null Spaces and Ranges (the Fundamental Theorem of Linear Maps, with the proof by extension of a basis of the null space, and its consequences for maps to smaller and larger spaces)
  - book: isbn:9780135367971
    title: Kenneth Hoffman and Ray Kunze, Linear Algebra, second edition, Prentice Hall, 1971
    locator: Section 3.1, Linear Transformations (rank plus nullity equals the dimension of the domain)
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 0.4, Rank (the rank-nullity relation for matrices and Sylvester's rank inequality)
---

The rank-nullity theorem says that for a linear map $f : V \to W$ on a finite-dimensional vector space $V$, the dimension of the kernel plus the dimension of the image equals $\dim V$. For an $m \times n$ matrix $A$ over a field $K$ it reads $\operatorname{rank}(A) + \dim \operatorname{null}(A) = n$: each column of $A$ either adds one to the [rank](/rank/) or adds one free direction to the [nullspace](/nullspace/). It is the reason that elimination can count solutions, and that a square matrix is injective exactly when it is surjective.

## Statement

**Theorem.** Let $K$ be a field, let $V$ and $W$ be vector spaces over $K$ with $\dim V$ finite, and let $f : V \to W$ be linear. Then $\ker f = \{ v \in V : f(v) = 0 \}$ and $\operatorname{im} f = \{ f(v) : v \in V \}$ are finite-dimensional, and

$$\dim V = \dim \ker f + \dim \operatorname{im} f.$$

**Matrix form.** For an $m \times n$ matrix $A$ over $K$, apply the theorem to $f(x) = A x$ from $K^n$ to $K^m$. The kernel is $\operatorname{null}(A)$ and the image is the column space, so

$$\operatorname{rank}(A) + \operatorname{nullity}(A) = n, \qquad \operatorname{nullity}(A) = \dim \operatorname{null}(A).$$

**Over an integral domain.** Let $R$ be an integral domain with field of fractions $K$ and let $A$ be an $m \times n$ matrix over $R$. The module $\operatorname{null}_R(A) = R^n \cap \operatorname{null}_K(A)$ contains a basis of $\operatorname{null}_K(A)$ (clear the denominators of a $K$-basis), so its rank as an $R$-module is $\dim \operatorname{null}_K(A) = n - \operatorname{rank}(A)$.

## In plain words

Take a machine that turns input vectors into output vectors in a linear way. Some inputs are sent to zero; they form the kernel. The outputs that the machine can reach form the image. The theorem says that the number of independent directions of the input splits exactly in two: those that the machine kills, and those that survive and give independent outputs. No direction is lost and none is counted twice.

For a system of equations, this means: the number of unknowns equals the number of useful equations plus the number of free unknowns. Elimination finds both numbers at once.

## Proof

Let $n = \dim V$. The kernel is a subspace of $V$: it contains $0$, and $f(\lambda u + \mu v) = \lambda f(u) + \mu f(v) = 0$ for $u, v \in \ker f$. A subspace of a space of dimension $n$ has a basis with at most $n$ vectors, so let $u_1, \ldots, u_k$ be a basis of $\ker f$, with $k = \dim \ker f \le n$.

**Step 1 (extend the basis).** An independent list in $V$ can be extended to a basis of $V$: while the list does not span $V$, add a vector outside its span; the list stays independent, and this stops after at most $n$ additions, because $V$ has no independent list of more than $n$ vectors. So there are $w_1, \ldots, w_{n-k}$ such that $u_1, \ldots, u_k, w_1, \ldots, w_{n-k}$ is a basis of $V$.

**Step 2 (the images span).** Let $y = f(v) \in \operatorname{im} f$. Write $v = \sum_i a_i u_i + \sum_j b_j w_j$. Since $f(u_i) = 0$, linearity gives $y = \sum_j b_j f(w_j)$. So $f(w_1), \ldots, f(w_{n-k})$ span $\operatorname{im} f$, and in particular $\operatorname{im} f$ is finite-dimensional.

**Step 3 (the images are independent).** Suppose $\sum_j c_j f(w_j) = 0$. Then $f(\sum_j c_j w_j) = 0$, so $\sum_j c_j w_j \in \ker f$, and $\sum_j c_j w_j = \sum_i d_i u_i$ for some $d_i \in K$. This gives $\sum_j c_j w_j - \sum_i d_i u_i = 0$, a relation among the vectors of a basis of $V$. So every $c_j$ and every $d_i$ is $0$.

**Step 4 (count).** By Steps 2 and 3, $f(w_1), \ldots, f(w_{n-k})$ is a basis of $\operatorname{im} f$, so $\dim \operatorname{im} f = n - k$, which is the claim $n = k + \dim \operatorname{im} f$. $\blacksquare$

The matrix form is this theorem for $f(x) = A x$. A second proof of the matrix form, through the [reduced row echelon form](/reduced-row-echelon-form/), is on the [nullspace](/nullspace/) page: the pivot columns count the rank, and each free column gives one basis vector of the nullspace.

## Consequences

**Counting solutions.** For the matrix with rows $(1, 2, 3)$, $(4, 5, 6)$, $(7, 8, 9)$, the rank is $2$, so the nullspace has dimension $3 - 2 = 1$; it is spanned by $(1, -2, 1)^T$. For the $2 \times 4$ matrix with rows $(1, 0, 2, 1)$ and $(0, 1, 1, 3)$, the rank is $2$ and the nullspace has dimension $2$. Over a finite field $\mathbb{F}_q$ the system $A x = 0$ then has exactly $q^{\,n - \operatorname{rank}(A)}$ solutions, and each solvable system $A x = b$ has the same number.

**More unknowns than equations.** If $n > m$, then $\operatorname{rank}(A) \le m < n$, so the nullspace is not $\{0\}$. This is the step that the [quadratic sieve](/quadratic-sieve/) relies on: with $k$ exponent vectors in $\mathbb{F}_2^m$ and $k > m$, there are at least $k - m$ independent dependencies, and so at least $2^{k-m} - 1$ nonempty subsets whose product is a square. Finding them is a [system of linear equations modulo 2](/linear-system-modulo-2/).

**Square matrices.** For $m = n$ the map $x \mapsto A x$ is injective if and only if it is surjective: both mean $\operatorname{rank}(A) = n$. So a one-sided inverse of a square matrix is a two-sided inverse, and $A x = b$ has a solution for every $b$ exactly when $A x = 0$ has only $x = 0$. [Matrix inversion](/matrix-inversion/) and the [determinant](/determinant/) test use this.

**Sylvester's rank inequality.** For $A$ of size $m \times n$ and $B$ of size $n \times p$,

$$\operatorname{rank}(A) + \operatorname{rank}(B) - n \le \operatorname{rank}(A B).$$

Proof: restrict $x \mapsto A x$ to the column space $U = \operatorname{col}(B)$. Its image is $\operatorname{col}(AB)$ and its kernel is $U \cap \operatorname{null}(A)$, so the theorem gives $\operatorname{rank}(AB) = \operatorname{rank}(B) - \dim (U \cap \operatorname{null}(A)) \ge \operatorname{rank}(B) - (n - \operatorname{rank}(A))$. $\square$ It gives, for example, $\operatorname{rank}(A^2) \ge 2 \operatorname{rank}(A) - n$ for square $A$.

**Algorithms.** [Rank computation](/rank-computation/) and [nullspace computation](/nullspace-computation/) are the same computation: an algorithm that finds the rank $r$ and $n - r$ independent nullspace vectors has, by the theorem, found a full basis. The [Wiedemann algorithm](/wiedemann-algorithm/) uses the theorem to know how many random nullspace vectors are needed to span the nullspace of a singular sparse matrix.

## Tightness

The theorem is an identity, so there is no bound to improve, but each hypothesis is needed.

**Finite dimension.** On the space of infinite sequences over $K$, the left shift $(x_1, x_2, \ldots) \mapsto (x_2, x_3, \ldots)$ is surjective with a kernel of dimension $1$, and the right shift $(x_1, x_2, \ldots) \mapsto (0, x_1, x_2, \ldots)$ is injective but not surjective. So the equivalence of injective and surjective fails without finite dimension.

**Fields versus rings.** Over $\mathbb{Z}$ the rank count still holds, but the image of an integer matrix can be a proper sublattice of the integer vectors that it spans over $\mathbb{Q}$. The $1 \times 1$ matrix $(2)$ has kernel $\{0\}$ and image $2\mathbb{Z}$: rank $1$ plus nullity $0$ is $1$, but the map $\mathbb{Z} \to \mathbb{Z}$ is not surjective. The theorem does not see this torsion; the [Smith normal form](/smith-normal-form/) does.

## History

The statement for linear maps between abstract vector spaces is the form that the cited textbooks give; Axler calls it the Fundamental Theorem of Linear Maps, and Hoffman and Kunze prove it in the first section of their chapter on linear transformations. The name comes from the two terms of the sum, the rank and the nullity.

## References
