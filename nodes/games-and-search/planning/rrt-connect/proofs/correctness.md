---
title: RRT-Connect returns free paths and is probabilistically complete
proves: [correctness]
status: full
---

We assume that the checker is exact: it calls a segment free only if every point of it is in $\mathcal{C}_{free}$. The space $\mathcal{C}$ is a box in $\mathbb{R}^d$ and $\mu$ is volume. Write $\zeta_d$ for the volume of the unit ball in $\mathbb{R}^d$ and $B(y, s)$ for the closed ball of radius $s$ around $y$. The step size $\eta > 0$ is fixed. Call $T_s$ the tree rooted at $x_{init}$ and $T_g$ the tree rooted at $x_{goal}$, whichever of them is $T_a$ at a given time.

**Lemma 1 (soundness).** At all times $T_s$ and $T_g$ are trees whose edges are free segments. Every path that RRT-CONNECT returns lies in $\mathcal{C}_{free}$ and goes from $x_{init}$ to $x_{goal}$.

*Proof.* Each vertex is added by line L4, with one edge to an old vertex of the same tree, after line L3 has checked that the edge is free. So both sets stay trees with free edges. Line L13 runs only when CONNECT returned REACHED, and then line L5 has added a vertex equal to $x_{new}$ to $T_b$, while $x_{new}$ is already a vertex of $T_a$. So the path of $T_s$ from $x_{init}$ to $x_{new}$ and the path of $T_g$ from $x_{new}$ to $x_{goal}$ meet at $x_{new}$, and their union is a chain of free segments from $x_{init}$ to $x_{goal}$. $\square$

**Lemma 2 (one step along a tube).** Let $\nu \le \eta/3$, and let $y, y'$ be points with $\lVert y - y' \rVert \le \nu$ and $B(y', 4\nu) \subseteq \mathcal{C}_{free}$. If a tree $T$ has a vertex in $B(y, \nu)$ and $x \in B(y', \nu)$, then EXTEND$(T, x, \eta)$ returns REACHED and adds the vertex $x$.

*Proof.* Let $v$ be a vertex in $B(y, \nu)$. Then $\lVert x - v \rVert \le 3\nu$, so the nearest vertex $x_{near}$ of line L1 has $\lVert x - x_{near} \rVert \le 3\nu \le \eta$, and line L2 returns $x_{new} = x$. Both $x_{near}$ and $x$ lie in $B(y', 4\nu)$, because $\lVert x_{near} - y' \rVert \le 3\nu + \nu$. The ball is convex and free, so line L3 passes, line L4 adds $x$, and line L5 returns REACHED. $\square$

**Theorem (probabilistic completeness).** Let $\tau$ be a path from $x_{init}$ to $x_{goal}$ of length $L$ with clearance $\delta > 0$, that is, $B(\tau(t), \delta) \subseteq \mathcal{C}_{free}$ for every $t$. Let $\nu = \min(\delta/4, \eta/3)$, $m = \lceil L/\nu \rceil$ and $p = \zeta_d \nu^d / \mu(\mathcal{C})$. If $N \ge 4(m + 1)/p$, then RRT-CONNECT fails with probability at most $e^{-pN/16}$.

*Proof.* Pick points $y_0 = x_{init}, y_1, \dots, y_m = x_{goal}$ on $\tau$ with arcs of length at most $\nu$ between consecutive points. Then $\lVert y_j - y_{j-1} \rVert \le \nu$ and $B(y_j, 4\nu) \subseteq \mathcal{C}_{free}$. Let $B_j = B(y_j, \nu)$, and let $S$ be the largest $j$ such that $T_s$ has a vertex in $B_j$. At the start $S \ge 0$, since $x_{init} \in B_0$, and $S$ never decreases, because vertices are never removed.

Look only at the *start iterations*, those in which $T_a = T_s$. Line L14 swaps the trees after every iteration, so these are the iterations $1, 3, 5, \dots$, and there are $\lceil N/2 \rceil$ of them. Call a start iteration a *hit* if $x_{rand}$ lies in $B_{S+1}$ when $S < m$, or in $B_m$ when $S = m$. Each ball is free and lies in $\mathcal{C}$, so, whatever happened before, a start iteration is a hit with probability $\mu(B_j)/\mu(\mathcal{C}) = p$.

If $S < m$ and a hit occurs, Lemma 2 with $y = y_S$ and $y' = y_{S+1}$ shows that EXTEND adds a vertex in $B_{S+1}$, so $S$ grows by at least 1. Vertices that CONNECT adds to $T_s$ in other iterations can only make $S$ larger.

If $S = m$ and a hit occurs, Lemma 2 with $y = y' = x_{goal}$ shows that EXTEND$(T_s, x_{rand}, \eta)$ adds $x_{new} = x_{rand} \in B_m$. Then line L12 runs CONNECT$(T_g, x_{new}, \eta)$. The tree $T_g$ contains $x_{goal}$, and $\lVert x_{new} - x_{goal} \rVert \le \nu$, so Lemma 2 with $y = y' = x_{goal}$ again shows that the first EXTEND of CONNECT returns REACHED. Line L13 returns a path.

So after $m$ hits $S = m$, and the next hit ends the run with a path, unless the run has already returned one, which is also a success. The run fails only if the start iterations have at most $m$ hits. The number $X$ of hits dominates a binomial variable with $\lceil N/2 \rceil$ trials and success probability $p$, whose mean $\mu_X \ge pN/2 \ge 2(m + 1)$. The lower tail of the [Chernoff bound](/chernoff-bound/), $\Pr[X \le (1 - \epsilon)\mu_X] \le e^{-\epsilon^2 \mu_X / 2}$, with $\epsilon = 1/2$ gives

$$\Pr[\text{failure}] \le \Pr[X \le m] \le \Pr[X \le \mu_X / 2] \le e^{-\mu_X/8} \le e^{-pN/16}. \qquad \blacksquare$$

**Consequences.** For a fixed problem with a path of positive clearance, the failure probability of RRT-Connect tends to 0 exponentially fast in $N$. The bound is weaker than the bound for the RRT by a factor of 2 in the exponent, because it uses only half of the iterations and ignores the help of CONNECT. In practice CONNECT is what makes the method fast. The argument follows the one for the geometric RRT, as in Kleinbort et al. (2019), and it gives no bound on the length of the path.
