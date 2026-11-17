---
title: Wires deformation is the identity at rest, moves only points near the reference curve, interpolates the wire, and is continuous at the radius of influence
proves: [correctness]
status: full
---

We use the notation of the page.
Write $c = R(u)$ for the closest point of line L1, $d = |P - c|$, and $\Phi(P)$ for the result of the algorithm.
Let $\rho = 1 + (s - 1)F$ be the factor of line L4 and $T$ the turn rot$(a, F\theta)$ of line L6, or the identity if the tangents are parallel.
Then, for $F > 0$,

$$\Phi(P) = c + \rho\,T(P - c) + F(W(u) - c).$$

## The closest point

**Lemma 1.** On a segment from $A$ to $B$ with $A \ne B$, the point closest to $P$ is $A + t(B - A)$ with $t$ the value of $(P - A)\cdot(B - A)/|B - A|^2$ clamped to $[0, 1]$.

*Proof.*
$g(t) = |P - A - t(B - A)|^2$ is a quadratic in $t$ with the leading coefficient $|B - A|^2 > 0$ and its minimum at the unclamped value. On $[0, 1]$ a convex quadratic has its minimum at the clamped value. $\square$

Taking the nearest of the segment points gives a closest point of the polyline, so $d$ is the distance from $P$ to $R$.

## Four properties

**Theorem 1 (identity at rest).** If $W = R$ and $s = 1$, then $\Phi(P) = P$ for every $P$.

*Proof.*
If $F = 0$, line L3 returns $P$.
Otherwise $\rho = 1$, the two tangents are the same, so $a$ is not defined and $T$ is the identity, and $W(u) - c = 0$. So $\Phi(P) = c + (P - c) = P$. $\square$

**Theorem 2 (locality).** If $d \ge r$, then $\Phi(P) = P$.

*Proof.*
$d/r \ge 1$, so $F = f(d/r) = 0$, and line L3 returns $P$. $\square$

**Theorem 3 (interpolation).** If $P$ lies on $R$, then $\Phi(P) = W(u)$.

*Proof.*
$P = c$, so $d = 0$ and $F = f(0) = 1$. The offset $P - c$ is 0, so $\rho T(0) = 0$, and $\Phi(P) = c + W(u) - c = W(u)$. $\square$

**Theorem 4 (continuity at the radius).** Let $P_k \to P^*$ with $d(P_k) < r$ and $d(P^*) = r$, and let $f$ be continuous with $f(1) = 0$. Then $\Phi(P_k) \to P^* = \Phi(P^*)$.

*Proof.*
The distance to $R$ is continuous in $P$, so $F_k = f(d(P_k)/r) \to f(1) = 0$.
Then $\rho_k \to 1$ and $F_k\theta_k \to 0$, with $|\theta_k| \le \pi$, so $T_k \to I$ uniformly.
The offsets $P_k - c_k$ are bounded by $r$ and the moves $W(u_k) - c_k$ are bounded by the largest vertex move, because $W - R$ is piecewise linear in $u$.
So $\Phi(P_k) - P_k = (\rho_kT_k - I)(P_k - c_k) + F_k(W(u_k) - c_k) \to 0$, and $P_k \to P^*$. $\square$

The proof does not need $u_k$ to converge, so it holds even where the closest point is not unique.

## The size of the offset

**Theorem 5.** For $F > 0$, $|\Phi(P) - (c + F(W(u) - c))| = \rho\,d$. In particular, with $s = 1$ the moved point keeps its distance from the moved curve point $c + F(W(u) - c)$.

*Proof.*
$T$ is a rotation, so $|T(P - c)| = |P - c| = d$, and $\rho > 0$ because $s > 0$ and $0 \le F \le 1$. $\square$

## Where the map jumps

Let $P$ have two closest points $c_1 = R(u_1)$ and $c_2 = R(u_2)$ with $W(u_1) - R(u_1) \ne W(u_2) - R(u_2)$, and let $s = 1$ and the tangents be unchanged.
Points close to $P$ on either side of the set of such points bind to $u_1$ or to $u_2$, and their moves tend to $F(W(u_1) - c_1)$ and $F(W(u_2) - c_2)$, which differ when $F > 0$.
So the map is discontinuous there, which is the medial jump of the Pitfalls.
The same argument with the turn $T$ in place of the move applies to a point whose closest point is an inner vertex of a polyline, where $R'$ and $W'$ change.
Away from these sets, $u$ and the tangents depend continuously on $P$, and so does $\Phi$.
