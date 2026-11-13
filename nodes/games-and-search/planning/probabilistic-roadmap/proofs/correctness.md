---
title: The probabilistic roadmap returns free paths and is probabilistically complete
proves: [correctness]
status: full
---

We assume that the checker is exact: it calls a point free only if it is in $\mathcal{C}_{free}$, and a segment free only if every point of it is in $\mathcal{C}_{free}$. The space $\mathcal{C}$ is a box in $\mathbb{R}^d$ and $\mu$ is volume. Write $\zeta_d$ for the volume of the unit ball in $\mathbb{R}^d$ and $B(y, s)$ for the closed ball of radius $s$ around $y$.

**Lemma 1 (soundness).** Every path that PRM-QUERY returns lies in $\mathcal{C}_{free}$ and goes from $q_I$ to $q_G$.

*Proof.* Line L8 adds an edge only after the checker calls its segment free. Line L9 links $q_I$ to $a$ and $q_G$ to $b$ only by segments that the checker calls free. Line L11 joins these two segments to a path of edges from $a$ to $b$. So every segment of the result is free, and consecutive segments share their end points. $\square$

**Lemma 2 (the forest rule keeps the components).** After each sample, the components of the roadmap with line L7 are the same as the components of sPRM, the roadmap without line L7, on the same samples.

*Proof.* By induction on the number of samples. Both roadmaps add the same node $q$. Without line L7, $q$ gets an edge to each node $q'$ within $r$ with a free segment. With line L7, the same edge is tried unless $q$ and $q'$ are already in the same component, and in that case the edge would not join two components. So after the loop of line L6, $q$ is joined to the components of all such $q'$ in both roadmaps. $\square$

**Theorem (probabilistic completeness).** Let $\tau$ be a path from $q_I$ to $q_G$ of length $L$ with clearance $\rho > 0$, that is, $B(\tau(t), \rho) \subseteq \mathcal{C}_{free}$ for every $t$. Let $r \ge 3\rho/2$, and let the $n$ samples of PRM-LEARN be independent and uniform on $\mathcal{C}_{free}$. Then PRM-QUERY$(q_I, q_G)$ fails with probability at most

$$\left\lceil \frac{2L}{\rho} \right\rceil \left( 1 - \frac{\zeta_d (\rho/2)^d}{\mu(\mathcal{C}_{free})} \right)^n \le \left\lceil \frac{2L}{\rho} \right\rceil e^{-\sigma \rho^d n}, \qquad \sigma = \frac{\zeta_d}{2^d \mu(\mathcal{C}_{free})}.$$

*Proof.* Lines L3 and L4 keep a uniform sample of $\mathcal{C}$ only when it is free, so each kept sample is uniform on $\mathcal{C}_{free}$, and the samples are independent.

Let $m = \lceil 2L/\rho \rceil$, and pick points $y_0 = q_I, y_1, \dots, y_m = q_G$ on $\tau$ such that the arc of $\tau$ between $y_{j-1}$ and $y_j$ has length at most $\rho/2$. Then $\lVert y_j - y_{j-1} \rVert \le \rho/2$. Let $A_j$ be the event that the ball $B_j = B(y_j, \rho/2)$ holds at least one sample, for $1 \le j \le m - 1$.

Assume that every $A_j$ holds, and let $x_j$ be a sample in $B_j$. Put $x_0 = q_I$ and $x_m = q_G$. For $1 \le j \le m$,

$$\lVert x_j - x_{j-1} \rVert \le \lVert x_j - y_j \rVert + \lVert y_j - y_{j-1} \rVert + \lVert y_{j-1} - x_{j-1} \rVert \le \frac{\rho}{2} + \frac{\rho}{2} + \frac{\rho}{2} = \frac{3\rho}{2} \le r.$$

Both $x_{j-1}$ and $x_j$ lie in $B(y_j, \rho)$, because $\lVert x_{j-1} - y_j \rVert \le \rho/2 + \rho/2$ and $\lVert x_j - y_j \rVert \le \rho/2$. A ball is convex, so the segment from $x_{j-1}$ to $x_j$ lies in $B(y_j, \rho) \subseteq \mathcal{C}_{free}$, and the checker calls it free. For $2 \le j \le m - 1$ both ends are roadmap nodes within $r$, so sPRM has the edge, and by Lemma 2 the two nodes are in the same component of the PRM too. So $x_1$ and $x_{m-1}$ are in one component. The case $j = 1$ shows that $x_1$ is within $r$ of $q_I$ with a free segment, so $x_1 \in A$ in line L9, and the case $j = m$ shows that $x_{m-1} \in B$. So line L10 finds a pair in one component, and Dijkstra in line L11 finds a path between them, so the query does not fail. When $m = 1$ there is no ball to fill, $\lVert q_I - q_G \rVert \le \rho/2 \le r$, and the segment from $q_I$ to $q_G$ lies in $B(q_I, \rho)$, so the direct test that the implementation makes first accepts it.

So the query can fail only if some $A_j$ fails. A sample misses $B_j$ with probability $1 - \mu(B_j)/\mu(\mathcal{C}_{free})$, since $B_j \subseteq \mathcal{C}_{free}$, and $\mu(B_j) = \zeta_d (\rho/2)^d$. The $n$ samples are independent, so $\Pr[\text{not } A_j] = (1 - \zeta_d (\rho/2)^d / \mu(\mathcal{C}_{free}))^n$. The [union bound](/union-bound/) over at most $m$ events, and $1 - x \le e^{-x}$, give the claim. $\blacksquare$

**Consequences.** For a fixed problem with a path of positive clearance, the failure probability tends to 0 as $n \to \infty$, exponentially fast, so the PRM is probabilistically complete. The bound gives no help when $\rho$ is tiny, since it needs $n$ of order $\rho^{-d} \log(L/\rho)$, and it says nothing when no path exists: then the query fails for every $n$, which is correct, but the planner cannot tell this case from bad luck.
