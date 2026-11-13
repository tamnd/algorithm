---
title: The RRT returns free paths and is probabilistically complete
proves: [correctness]
status: full
---

We assume that the checker is exact: it calls a segment free only if every point of it is in $\mathcal{C}_{free}$. The space $\mathcal{C}$ is a box in $\mathbb{R}^d$ and $\mu$ is volume. Write $\zeta_d$ for the volume of the unit ball in $\mathbb{R}^d$ and $B(y, s)$ for the closed ball of radius $s$ around $y$. The parameters $\eta > 0$, $r_{goal} > 0$ and $p_{goal} \in [0, 1)$ are fixed.

**Lemma 1 (soundness).** At all times $T$ is a tree rooted at $x_{init}$ whose edges are free segments. Every path that RRT returns lies in $\mathcal{C}_{free}$ and goes from $x_{init}$ to $x_{goal}$.

*Proof.* Line L1 makes a tree with one vertex. Line L7 adds one new vertex with one edge to an old vertex, so $T$ stays a tree, and line L6 has checked that this edge is free. Line L9 returns the tree path from $x_{init}$ to $x_{new}$, made of free edges, and then the segment from $x_{new}$ to $x_{goal}$, which line L8 has checked. Consecutive segments share their end points. $\square$

**Lemma 2 (one step along a tube).** Let $\nu \le \eta/3$, and let $y, y'$ be points with $\lVert y - y' \rVert \le \nu$ and $B(y', 4\nu) \subseteq \mathcal{C}_{free}$. If $T$ has a vertex in $B(y, \nu)$ and line L3 draws $x_{rand} \in B(y', \nu)$, then the iteration adds a vertex in $B(y', \nu)$.

*Proof.* Let $v$ be a vertex in $B(y, \nu)$. Then $\lVert x_{rand} - v \rVert \le \nu + \nu + \nu = 3\nu$. The nearest vertex $x_{near}$ is at most as far, so $\lVert x_{rand} - x_{near} \rVert \le 3\nu \le \eta$, and STEER in line L5 returns $x_{new} = x_{rand}$, which lies in $B(y', \nu)$. Both $x_{near}$ and $x_{new}$ lie in $B(y', 4\nu)$, because $\lVert x_{near} - y' \rVert \le 3\nu + \nu$. The ball is convex and free, so the segment from $x_{near}$ to $x_{new}$ is free, and line L7 adds $x_{new}$. Note that $x_{near}$ need not be $v$: the lemma holds for any nearest vertex. $\square$

**Theorem (probabilistic completeness).** Let $\tau$ be a path from $x_{init}$ to $x_{goal}$ of length $L$ with clearance $\delta > 0$, that is, $B(\tau(t), \delta) \subseteq \mathcal{C}_{free}$ for every $t$. Let $\nu = \min(\delta/4, \eta/3, r_{goal})$, $m = \lceil L/\nu \rceil$ and $p = (1 - p_{goal}) \zeta_d \nu^d / \mu(\mathcal{C})$. If $N \ge 2m/p$, then RRT fails with probability at most $e^{-pN/8}$.

*Proof.* Pick points $y_0 = x_{init}, y_1, \dots, y_m = x_{goal}$ on $\tau$ such that the arc between $y_{j-1}$ and $y_j$ has length at most $\nu$. Then $\lVert y_j - y_{j-1} \rVert \le \nu$, and $B(y_j, 4\nu) \subseteq B(y_j, \delta) \subseteq \mathcal{C}_{free}$. Let $B_j = B(y_j, \nu)$.

Define the *stage* of the run as follows. It starts at 0, since $x_{init} \in B_0$, and it moves from $j$ to $j + 1$ when an iteration adds a vertex in $B_{j+1}$. Vertices are never removed, so once in stage $j$ the tree keeps a vertex in $B_j$.

In each iteration, line L3 draws a uniform point with probability $1 - p_{goal}$, and that point lies in $B_{j+1}$ with probability $\mu(B_{j+1}) / \mu(\mathcal{C}) = \zeta_d \nu^d / \mu(\mathcal{C})$, since $B_{j+1} \subseteq \mathcal{C}_{free} \subseteq \mathcal{C}$. So with probability at least $p$, whatever happened before, $x_{rand} \in B_{j+1}$, and by Lemma 2 the stage moves to $j + 1$. The draws of different iterations are independent.

When the stage reaches $m$, the new vertex $x_{new}$ lies in $B_m = B(x_{goal}, \nu)$. Then $\lVert x_{new} - x_{goal} \rVert \le \nu \le r_{goal}$, and the segment from $x_{new}$ to $x_{goal}$ lies in the free ball $B(x_{goal}, \delta)$, so line L8 accepts it and the run returns a path. The run may also return earlier, which is a success too.

So the run fails only if fewer than $m$ of the $N$ iterations draw a point in the next ball. Couple the iterations with $N$ independent coins of bias $p$, where each coin that shows heads forces a draw in the next ball. Then the number $X$ of stage moves is at least the number of heads, a binomial variable with mean $\mu_X = pN \ge 2m$. The lower tail of the [Chernoff bound](/chernoff-bound/), $\Pr[X \le (1 - \epsilon)\mu_X] \le e^{-\epsilon^2 \mu_X / 2}$, with $\epsilon = 1/2$ gives

$$\Pr[\text{failure}] \le \Pr[X < m] \le \Pr[X \le \mu_X / 2] \le e^{-pN/8}. \qquad \blacksquare$$

**Consequences.** For a fixed problem with a path of positive clearance, the failure probability tends to 0 exponentially fast in $N$. This is the geometric case of Theorem 16 of Karaman and Frazzoli (2011), which they credit to LaValle and Kuffner (2001), and of the result of Kleinbort et al. (2019), with explicit constants from this argument. The bound needs $N$ of order $\nu^{-d} L/\nu$, which is large when the clearance is small or the dimension is high. It says nothing when no path exists, and then RRT fails for every $N$, which is correct, but a failure is never a proof.

**Why the path is not optimal.** Lemma 1 shows that a vertex keeps its parent for ever. Karaman and Frazzoli (Theorem 33) prove that, as a result, the cost of the best path in the tree converges with probability 1 to a value above the optimum when the set of optimal paths has measure zero. The argument above gives completeness only, not a bound on the length.
