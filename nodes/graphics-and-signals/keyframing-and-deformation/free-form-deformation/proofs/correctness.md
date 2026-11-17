---
title: Free-form deformation is the identity at rest, reproduces affine maps, and is continuous across a face whose control points are at rest
proves: [correctness]
status: full
---

We use the notation of the page.
The lattice has the corner $X_0$, the edge vectors $S$, $T$, $U$ with $(S \times T)\cdot U \ne 0$, and the degrees $l, m, n \ge 1$.
The map is $F(s, t, u) = \sum_{i,j,k} B_i^l(s)B_j^m(t)B_k^n(u)P_{ijk}$ and $X' = F(s(X), t(X), u(X))$ for a point $X$ inside the lattice.

## The local coordinates

**Lemma 1.** For every point $X$, lines L1 to L3 return the unique $(s, t, u)$ with $X = X_0 + sS + tT + uU$.

*Proof.*
$S$, $T$, $U$ are linearly independent, so the coefficients exist and are unique.
Write $X - X_0 = sS + tT + uU$ and take the dot product with $T \times U$.
The terms in $T$ and $U$ vanish, because $T \times U$ is orthogonal to both, so $(T \times U)\cdot(X - X_0) = s\,(T \times U)\cdot S$.
The divisor is the triple product $\pm(S \times T)\cdot U \ne 0$, and this is line L1.
Lines L2 and L3 follow in the same way with $S \times U$ and $S \times T$. $\square$

## The Bernstein identities

**Lemma 2.** For every $l \ge 1$ and every real $s$: $\sum_{i=0}^{l} B_i^l(s) = 1$ and $\sum_{i=0}^{l} \frac{i}{l}B_i^l(s) = s$.

*Proof.*
The first sum is $((1 - s) + s)^l = 1$ by the binomial theorem.
For the second, $\frac{i}{l}\binom{l}{i} = \binom{l-1}{i-1}$ for $i \ge 1$, so the sum is $s\sum_{i=1}^{l}\binom{l-1}{i-1}(1 - s)^{l-i}s^{i-1} = s((1 - s) + s)^{l-1} = s$. $\square$

## Identity and affine invariance

**Theorem 1.** If every control point is at rest, $P_{ijk} = X_0 + \frac{i}{l}S + \frac{j}{m}T + \frac{k}{n}U$, then $X' = X$ for every point $X$ inside the lattice.

*Proof.*
Write $b_{ijk} = B_i^l(s)B_j^m(t)B_k^n(u)$.
By the first identity of Lemma 2 applied three times, $\sum b_{ijk} = 1$, so the $X_0$ terms give $X_0$.
The $S$ terms give $S\sum_i \frac{i}{l}B_i^l(s)\sum_j B_j^m(t)\sum_k B_k^n(u) = sS$, and in the same way the $T$ and $U$ terms give $tT$ and $uU$.
So $X' = X_0 + sS + tT + uU = X$ by Lemma 1. $\square$

The proof uses only ring operations on the inputs, so it holds exactly in rational arithmetic, and the implementation checks it with `fractions.Fraction`.

**Theorem 2.** Let $A(Y) = MY + c$ be an affine map. If every control point is moved to $A(P_{ijk})$, then $X' = A(X)$ for every point $X$ inside the lattice.

*Proof.*
$\sum b_{ijk}A(P_{ijk}) = M\sum b_{ijk}P_{ijk} + c\sum b_{ijk} = M X + c$, by Theorem 1 for the rest points and by $\sum b_{ijk} = 1$. $\square$

## The Jacobian and the volume

**Lemma 3.** Inside the lattice, $\frac{\partial X'}{\partial X} = D\,C$, where the columns of $D$ are $\partial F/\partial s$, $\partial F/\partial t$, $\partial F/\partial u$ and the rows of $C$ are the vectors $(T \times U)/((T \times U)\cdot S)$, $(S \times U)/((S \times U)\cdot T)$ and $(S \times T)/((S \times T)\cdot U)$.
The derivative of a Bernstein polynomial is $\frac{d}{ds}B_i^l(s) = l(B_{i-1}^{l-1}(s) - B_i^{l-1}(s))$, with $B_{-1}^{l-1} = B_l^{l-1} = 0$.

*Proof.*
$(s, t, u)$ is a linear function of $X$ with the matrix $C$ by Lemma 1, so the chain rule gives $DC$.
The derivative formula follows from the product rule and $l\binom{l-1}{i-1} = i\binom{l}{i}$, $l\binom{l-1}{i} = (l - i)\binom{l}{i}$. $\square$

By the change of variables formula, the deformed image of a region $V$ inside the lattice, if the map is one to one on $V$, has the volume $\int_V |\det(DC)|\,dX$.
If $\det(DC) < 0$ somewhere, the map turns the orientation there, and the object is folded.

## Continuity across the lattice boundary

**Theorem 3.** Take the face $s = 0$ of the lattice. If the control points $P_{0jk}$ are at rest, then $X'$ is continuous across this face: the points just inside and just outside map to nearby points. If all the control points $P_{ijk}$ with $i \le r$ are at rest, all derivatives of $X'$ of order at most $r$ agree on both sides of the face.

*Proof.*
At $s = 0$, $B_i^l(0) = 0$ for $i \ge 1$ and $B_0^l(0) = 1$, so $F(0, t, u) = \sum_{j,k} B_j^m(t)B_k^n(u)P_{0jk}$.
If these points are at rest, this is $X_0 + tT + uU$ by Lemma 2, which is the identity, the map outside.
For the derivatives, the $q$-th derivative in $s$ of $B_i^l$ at $s = 0$ is 0 for $i > q$, so $\partial_s^q F(0, t, u)$ and all its derivatives in $t$ and $u$ depend only on the control points with $i \le q$.
If those with $i \le r$ are at rest, every mixed derivative of order at most $r$ at the face equals that of the rest map, which is the identity by Theorem 1.
Outside the lattice the map is the identity, so all derivatives of order at most $r$ match. $\square$

If a control point on the face moves, the map jumps at the face, and the object tears there; the implementation leaves points outside the lattice in place, so it shows this jump.
