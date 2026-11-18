---
title: Fast marching returns the unique solution of the discrete upwind eikonal equation of continuum crowds
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
The grid has square cells of size $\Delta x$.
For a cell $M$ and a neighbor $i$ in direction $\theta$, $h_{M \to i} = \Delta x\, C_{M \to i}$ with $0 < C_{M \to i} \le \infty$; an infinite cost marks an obstacle face, and a neighbor outside the grid does not exist.
The goal cells $\Gamma$ have $\phi = 0$.

## The local update

For a cell $M$ and values $\phi$ of its neighbors, define for $x \in \mathbb{R}$
$$G_M(x) = \sum_{\text{axis } a \in \{x, y\}} \Big( \max_{i \in a} \big[\, x - \phi_i \,\big]^+ / h_{M \to i} \Big)^2,$$
where $[z]^+ = \max(z, 0)$ and the maximum runs over the neighbors of the axis with finite $\phi_i$ and finite $h_{M \to i}$ (an empty maximum is 0).
The discrete equation at $M \notin \Gamma$ is $G_M(\phi_M) = 1$.
It is the upwind (Godunov) form of $|\nabla\phi| = C$.

**Lemma 1.** If $M$ has at least one usable neighbor, $G_M(x) = 1$ has exactly one solution $U_M(\phi)$.
It satisfies $U_M(\phi) > \phi_i$ for every neighbor whose term is positive at $U_M(\phi)$, and $U_M(\phi) \ge \min_i (\phi_i + h_{M \to i}/\sqrt 2)$ over the usable neighbors.

*Proof.*
$G_M$ is continuous and nondecreasing, it is 0 for $x \le \min_i \phi_i$, it is strictly increasing where it is positive, and it tends to infinity.
So it takes the value 1 exactly once.
A term is positive only if $x > \phi_i$.
At the solution at most two terms are positive and each is at most 1, so some neighbor has $(U_M - \phi_i)/h_{M \to i} \ge 1/\sqrt 2$. $\square$

**Lemma 2.** The function `_candidates` of line L6 returns $U_M(\phi)$.

*Proof.*
The code forms a candidate for every choice of at most one neighbor per axis: $\phi_i + h_i$ for one neighbor, and for two neighbors the larger root $r$ of $\sum ((r - \phi_i)/h_i)^2 = 1$, kept only if $r \ge \max(\phi_1, \phi_2)$.
Every kept candidate $r$ satisfies $G_M(r) \ge 1$, because the maximum over an axis is at least the chosen term; so $r \ge U_M$.
Conversely, at $x = U_M$ choose on each axis a neighbor that attains the maximum, if that maximum is positive.
If one axis is chosen, $U_M = \phi_i + h_i$ is a candidate.
If two are chosen, $U_M \ge \max(\phi_1, \phi_2)$ solves the quadratic; the quadratic is convex with its smaller root at most the weighted mean of $\phi_1$ and $\phi_2$, which is at most $\max(\phi_1, \phi_2)$, so $U_M$ is the larger root and a kept candidate.
So the minimum over the candidates is $U_M$. $\square$

**Lemma 3 (monotone and causal).** If $\phi_i \le \psi_i$ for every neighbor, then $U_M(\phi) \le U_M(\psi)$.
Changing the value of a neighbor $i$ with $\phi_i \ge U_M(\phi)$, or adding or removing such a neighbor, does not change $U_M(\phi)$.

*Proof.*
Smaller neighbor values make every term larger, so $G_\phi \ge G_\psi$ and the solution is smaller.
A neighbor with $\phi_i \ge U_M$ contributes $[U_M - \phi_i]^+ = 0$ at $U_M$, and also 0 for all $x \le \phi_i$, so $G_M$ is unchanged near $U_M$ and on $(-\infty, U_M]$; the solution is the same. $\square$

## Fast marching

**Lemma 4.** The cells are accepted (line L4) in nondecreasing order of their values.

*Proof.*
The heap pops the smallest tentative value (line L3).
Suppose cell $A$ is accepted with value $v$, and a neighbor $B$ then gets the new tentative value $u = U_B$ over its known neighbors (line L7).
If $u < v$, then by Lemma 3 the term of $A$ is zero at $u$, so $u$ equals the value of $U_B$ over the known neighbors without $A$.
That set has not changed since the last update of $B$, so $B$ already had the tentative value $u < v$ in the heap when $A$ was popped, which contradicts the choice of $A$.
So $u \ge v$, and every value pushed after the acceptance of $A$ is at least $v$. $\square$

**Theorem 1.** When the heap is empty, every accepted cell $M \notin \Gamma$ satisfies $\phi_M = U_M(\phi)$ over all its neighbors, the goal cells have $\phi = 0$, and every cell that is never accepted has $\phi = \infty$ and no finite path of usable faces to the goal.

*Proof.*
When $M$ is accepted, $\phi_M$ is $U_M$ over the neighbors known at that time.
Every neighbor accepted later has a value at least $\phi_M$ by Lemma 4, so by Lemma 3 it does not change $U_M$.
A neighbor that is never accepted has $\phi = \infty$ and is left out of $G_M$.
If a cell is next to an accepted cell through a usable face, it gets a finite tentative value and is accepted later; so the accepted cells contain every cell that a chain of usable faces joins to the goal. $\blacksquare$

**Theorem 2 (uniqueness).** The system $\phi = 0$ on $\Gamma$, $\phi_M = U_M(\phi)$ elsewhere, has at most one solution with values in $[0, \infty]$.
So fast marching and the brute force iteration of the test, which stops at a fixed point, return the same field.

*Proof.*
Let $\phi$ and $\psi$ be two solutions, and suppose $\phi_M > \psi_M$ for some cell.
Among such cells take one with the smallest $\psi_M$; it is finite and $M \notin \Gamma$.
By Lemma 3, $\psi_M$ depends only on the neighbors with $\psi_i < \psi_M$, and for them $\phi_i \le \psi_i$ by the choice of $M$.
So at $x = \psi_M$ every term of $G_\phi$ is at least the matching term of $G_\psi$, and $G_\phi(\psi_M) \ge G_\psi(\psi_M) = 1$.
Since $G_\phi$ is nondecreasing, $\phi_M = U_M(\phi) \le \psi_M$, a contradiction.
By symmetry $\phi = \psi$. $\blacksquare$

## Cost

Each cell is accepted once, and each acceptance updates at most four neighbors.
Each update tries at most nine candidates, and each push costs $O(\log g)$ for $g$ cells.
So fast marching costs $O(g \log g)$ time and $O(g)$ space, in the worst case.

## The paper's rule

The paper picks, on each axis, the neighbor with the smaller $\phi_i + C_{M \to i}$ and then solves its Eq. 11 with $\Delta x = 1$.
When the two faces of an axis have the same cost, that neighbor is the one with the smaller $\phi_i$, which is also the one that attains the maximum in $G_M$, so the two rules agree.
With different costs on the two faces they can differ; the code uses the rule of $G_M$, for which Theorems 1 and 2 hold.
