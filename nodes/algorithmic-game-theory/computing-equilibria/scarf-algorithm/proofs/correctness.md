---
title: Scarf's ordinal algorithm ends at a completely labeled primitive set, and its points give approximate fixed points and equilibria
proves: [correctness]
status: full
---

**Setting.** Fix $d \ge 1$ and $N \ge 1$. The vectors are the slacks $s_0, \dots, s_d$ and the grid points $p = v/N$ of the simplex $\Delta_d = \{x \in \mathbb{R}^{d+1} : x \ge 0, \sum_i x_i = 1\}$, where $v$ has nonnegative integer entries with sum $N$. For each $i \in \{0, \dots, d\}$ there is a strict total order $\prec_i$ on all vectors:

- $s_i$ is the lowest vector in order $i$;
- next come all grid points, by the value of $p_i$, with ties broken by a fixed index of the points;
- the slacks $s_j$ with $j \ne i$ are above all grid points, in the order of $j$.

So for grid points, $p \preceq_i q$ implies $p_i \le q_i$. A set $S$ of $d + 1$ distinct vectors is **primitive** if there is no vector $u$ with $u \succ_i \min_i S$ for every $i$, where $\min_i S$ is the lowest member of $S$ in order $i$. We say that a member $u$ of $S$ **holds** order $i$ if $u = \min_i S$. Each slack $s_j$ has label $j$, and each grid point has a label in $\{0, \dots, d\}$ given by a labeling function. A set is **completely labeled** if its labels are exactly $\{0, \dots, d\}$.

The algorithm starts from $P_0 = \{s_1, \dots, s_d, e_0\}$, where $e_0$ is the grid point with $p_0 = 1$, and it calls the newest member $z$. While $z$ does not have label 0, it removes the other member $y$ with the label of $z$, lets $Q = P \setminus \{y\}$, lets $a$ be the order that $y$ holds and $w = \min_a Q$, lets $b$ be the order that $w$ holds in $P$, and adds the vector
$$z = \text{the highest vector in order } b \text{ of } C = \{u \notin Q : u \succ_i \min_i Q \text{ for all } i \ne b\}.$$

**Lemma 1.** In a primitive set, each member holds exactly one order.

*Proof.* If a member $u$ holds no order, then $u \succ_i \min_i S$ for every $i$, so $u$ itself breaks primitivity. So each of the $d + 1$ members holds at least one of the $d + 1$ orders, and then each holds exactly one. $\square$

**Lemma 2.** $P_0$ is primitive. The set of all $d + 1$ slacks is not primitive.

*Proof.* In $P_0$, $s_i$ holds order $i$ for $i \ge 1$, and $e_0$ holds order 0, because the slacks $s_j$ with $j \ne 0$ are above all points in order 0. A vector $u$ above all these minima must satisfy $u \succ_0 e_0$. Since $e_0$ is the highest grid point in order 0, $u$ is a slack $s_i$ with $i \ge 1$. But $u$ must also satisfy $u \succ_i s_i$, which fails for $u = s_i$. So no vector is above all the minima. For the slacks, $\min_i = s_i$, and every grid point is above $s_i$ in order $i$, so any grid point breaks primitivity. $\square$

**Lemma 3 (the pivot).** Let $S$ be primitive, $y \in S$ and $Q = S \setminus \{y\}$.

1. If $Q = \{s_j : j \ne a\}$ for some $a$, then $S$ is the only primitive set that contains $Q$.
2. Otherwise there is exactly one vector $z \ne y$ such that $Q \cup \{z\}$ is primitive, and it is the vector of the rule above.

*Proof.* Let $a$ be the order that $y$ holds in $S$, and write $m_i = \min_i Q$. For $i \ne a$, $m_i = \min_i S$, since $y$ held only order $a$. Let $w = m_a$. Then $w \succ_a y$, and $w$ holds some order $b \ne a$ in $S$, so in $Q$ the member $w$ is the minimum of both orders $a$ and $b$, and every other member of $Q$ holds the same single order as in $S$.

Let $Q \cup \{z'\}$ be primitive with $z' \ne y$, $z' \notin Q$. By Lemma 1, $z'$ holds exactly one order, and every member of $Q$ keeps at least one order. A member of $Q$ other than $w$ holds only one order in $Q$, so $z'$ cannot take it. So $z'$ holds order $a$ or order $b$.

*$z'$ holds order $a$.* Then $z' \prec_a w$ and $z' \succ_i m_i$ for $i \ne a$. The vector $y$ has the same two properties. Let $D$ be the set of vectors outside $Q$ with both properties. Primitivity of $S$ says that no vector of $D$ is above $y$ in order $a$, and primitivity of $Q \cup \{z'\}$ says that no vector of $D$ is above $z'$ in order $a$. So both are the highest vector of $D$ in order $a$, and $z' = y$, which is excluded.

*$z'$ holds order $b$.* Then $z' \succ_i m_i$ for all $i \ne b$ (for $i = a$ because $w$, not $z'$, holds order $a$), so $z' \in C$. Primitivity of $Q \cup \{z'\}$ says that no vector of $C$ is above $z'$ in order $b$, so $z'$ is the highest vector of $C$ in order $b$. So there is at most one such $z'$, and it is the $z$ of the rule.

*$z$ works when $C$ is not empty.* First, every $u \in C$ satisfies $u \prec_b w$: otherwise $u \succ_b w = \min_b S$, $u \succ_a w \succ_a y = \min_a S$ and $u \succ_i m_i = \min_i S$ for the other $i$, so $u$ would break the primitivity of $S$. So $z \prec_b w$, and in $Q \cup \{z\}$ the minima are $m_i$ for $i \ne b$ and $z$ for order $b$. A vector above all of them is not in $Q$ (members of $Q$ hold an order), so it lies in $C$ and is above $z$ in order $b$, which contradicts the choice of $z$. So $Q \cup \{z\}$ is primitive. Also $y \notin C$, because $y \prec_a w = m_a$ and $a \ne b$.

*When $C$ is empty.* For $i \ne b$, the minimum $m_i$ is either a grid point, or a slack. A slack in $Q$ holds its own order, so if $m_i$ is a slack and $i \ne a$, then $m_i = s_i$. If $s_b \notin Q$, then $s_b \in C$: it is above every grid point in each order $i \ne b$, above $s_i$ in order $i$, and if $m_a = w$ is a slack then $w$ holds order $b$, so $w = s_b$. Hence $C$ is empty only if $w = s_b$. Then $s_b = \min_a Q$, so every member of $Q$ is above $s_b$ in order $a$; grid points are below $s_b$ in order $a$, and $s_a$ would be the minimum of order $a$, so $Q$ consists of $d$ slacks other than $s_a$, that is, $Q = \{s_j : j \ne a\}$. Conversely, for this $Q$, the only candidate $z'$ is the one that holds order $a$, and the argument of the first case shows that $S$ is the only primitive set that contains $Q$. If $Q$ is not of this form, $C$ is not empty and part 2 holds. $\square$

**Theorem 1 (the path).** The algorithm ends after finitely many pivots with a completely labeled primitive set. The number of completely labeled primitive sets is odd.

*Proof.* Call a $d$-subset $Q$ of a primitive set a **door** if its labels are exactly $\{1, \dots, d\}$. Among the slack sets $\{s_j : j \ne a\}$, only $Q_0 = \{s_1, \dots, s_d\}$ is a door, since the others contain $s_0$ with label 0. By Lemma 3, every door other than $Q_0$ lies in exactly two primitive sets, and $Q_0$ lies only in $P_0$.

Build a graph whose nodes are the primitive sets that contain a door, with an edge between two of them if they share a door. A completely labeled set has exactly one door (remove its member with label 0). Any other node has labels $\{1, \dots, d\}$ with one label twice, and so exactly two doors (remove either member with the repeated label). The edges at a node are its doors other than $Q_0$. So every node has degree at most 2, the nodes of degree 1 are $P_0$ (if it is not complete) and the complete sets other than $P_0$, and $P_0$ has degree 0 if it is complete.

The algorithm walks in this graph. At $P_0$ it enters through $Q_0$ with $z = e_0$. At each node $P$ entered through the door $P \setminus \{z\}$, if $z$ has label 0 the node is complete and the walk stops. Otherwise the repeated label is the label of $z$, and the walk leaves through the other door $P \setminus \{y\}$, to the other primitive set that contains it, which Lemma 3 computes. A walk in a graph of maximum degree 2 that starts at a node of degree at most 1 never repeats a node, and the graph is finite (there are finitely many sets of $d + 1$ vectors). So the walk ends, at a node of degree 1 other than $P_0$, which is complete, or at $P_0$ itself if $P_0$ is complete.

The number of nodes of degree 1 is even, because each path component has two ends. If $P_0$ is complete, the nodes of degree 1 are the other complete sets, which is an even number, and with $P_0$ the total is odd. If $P_0$ is not complete, the nodes of degree 1 are $P_0$ and all complete sets, so the number of complete sets is odd. $\square$

**Lemma 4 (primitive sets are small).** Let $P$ be primitive, let $T$ be the set of indices $j$ with $s_j \in P$, and let $\delta = (d+1)/N$. For any two grid points $p, q$ in $P$ and every $i$, $|p_i - q_i| < \delta$, and $p_j < \delta$ for every $j \in T$.

*Proof.* Let $t = d + 1 - |T|$. For $i \notin T$, the minimum $m_i = \min_i P$ is a grid point; write $\mu_i$ for its coordinate $i$. Every grid point $p$ of $P$ has $p \succeq_i m_i$, so $p_i \ge \mu_i$. If $\sum_{i \notin T} \mu_i + t/N \le 1$, the grid point $u$ with $u_i = \mu_i + 1/N$ for $i \notin T$, with the rest of the mass put on one coordinate in $T$ (or on any coordinate if $T$ is empty), satisfies $u \succ_i m_i$ for $i \notin T$ and $u \succ_j s_j$ for $j \in T$, which breaks primitivity. So $\sum_{i \notin T} \mu_i > 1 - t/N$. Then for $i \notin T$, $p_i = 1 - \sum_{l \ne i} p_l \le 1 - \sum_{l \notin T, l \ne i} \mu_l < \mu_i + t/N$, so $p_i \in [\mu_i, \mu_i + t/N)$. For $j \in T$, $p_j \le 1 - \sum_{l \notin T} \mu_l < t/N$. Since $t \le d + 1$, the claim follows. $\square$

**Theorem 2 (approximate fixed point).** Let $f : \Delta_d \to \Delta_d$ satisfy $\|f(p) - f(q)\|_\infty \le \lambda \|p - q\|_\infty$. Label each grid point $p$ by the least $i$ with $f_i(p) \ge p_i$; such an $i$ exists because both $f(p)$ and $p$ sum to 1. Then every grid point $p^*$ of the output $P$ satisfies $\|f(p^*) - p^*\|_\infty < d(1 + \lambda)(d + 1)/N$.

*Proof.* $P$ contains a grid point by Lemma 2. Let $g = f(p^*) - p^*$, so $\sum_i g_i = 0$. Fix $i$. If the label $i$ comes from a grid point $q \in P$, then $f_i(q) \ge q_i$, and by Lemma 4, $|q_i - p^*_i| < \delta$ and $|f_i(q) - f_i(p^*)| < \lambda \delta$. So $g_i > -(1 + \lambda)\delta$. If the label $i$ comes from $s_i \in P$, then $p^*_i < \delta$ by Lemma 4, and $g_i \ge -p^*_i > -\delta$. So $g_i > -(1 + \lambda)\delta$ for every $i$, and then $g_i = -\sum_{l \ne i} g_l < d(1 + \lambda)\delta$. As $d \ge 1$, $|g_i| < d(1 + \lambda)\delta$. $\square$

**Theorem 3 (symmetric games).** Let $C$ be a $k \times k$ matrix with entries in $[0, 1]$, $k = d + 1$, and consider the symmetric game where the row player gets $C_{rc}$ and the column player gets $C_{cr}$. Label each grid point $q$ by the least pure best response to $q$, that is, the least $i$ with $(Cq)_i = \max_r (Cq)_r$. Then for every grid point $p^*$ of the output, $(p^*, p^*)$ is a $2k^2/N$-Nash equilibrium.

*Proof.* Let $M = \max_r (Cp^*)_r$. The gain of the row player from a pure deviation is at most $M - p^{*\mathsf T} C p^* = \sum_i p^*_i (M - (Cp^*)_i)$. For any grid point $q \in P$, let $t = q - p^*$; then $\sum_c t_c = 0$, and $\|t\|_1 < k\delta$ by Lemma 4, so $|(Cq)_r - (Cp^*)_r| = |\sum_c C_{rc} t_c| \le \sum_{t_c > 0} t_c = \|t\|_1 / 2 < k\delta/2$ for every row $r$. If the label $i$ comes from a grid point $q$, then $(Cq)_i = \max_r (Cq)_r$, and so $M - (Cp^*)_i < k\delta$. If it comes from $s_i$, then $p^*_i < \delta$ and $M - (Cp^*)_i \le 1$. Summing, the gain is less than $k\delta \sum_i p^*_i + k \delta = 2k\delta = 2k^2/N$. By symmetry, the column player has the same gain. $\square$

**Running time.** There are $d + 1 + \binom{N + d}{d}$ vectors. One pivot finds $a$, $w$ and $b$ in $O(d^2)$ comparisons and the new vector in $O(d)$ comparisons for each vector, so $O(d \binom{N + d}{d})$ time. The number of pivots is at most the number of primitive sets, which is finite but can be large; no polynomial bound in $\log N$ and $d$ is known, and none is expected, since the problem is PPAD-complete.
