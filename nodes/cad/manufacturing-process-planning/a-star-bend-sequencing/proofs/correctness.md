---
title: A*-BENDS returns a cheapest bend plan, or none if there is no plan
proves: [correctness]
status: full
---

We use the definitions of the page. $B = \{1, \dots, n\}$ is the set of bends, $s_b \in \{+1, -1\}$ is the sign of bend $b$, and $T$ is the list of $k$ tools. A tool $t$ *fits* bend $b$ when $\min(l_{b-1}, l_b) \ge m_t$. For a set $S \subseteq B$ and $b \notin S$, write $\mathrm{coll}(S, b, t)$ for the result of the collision rule of the page: the profile with the bends of $S \cup \{b\}$ done, in the frame of bend $b$, meets the open punch region or the open die region of $t$. A *plan* is a sequence $(b_1, t_1), \dots, (b_n, t_n)$ in which $b_1, \dots, b_n$ is an order of $B$, each $t_i$ fits $b_i$, and $\mathrm{coll}(\{b_1, \dots, b_{i-1}\}, b_i, t_i)$ is false for each $i$. Its cost is

$$\mathrm{cost} = \sum_{i=2}^{n} \bigl(\textit{flip} \cdot [s_{b_{i-1}} \ne s_{b_i}] + \textit{change} \cdot [t_{i-1} \ne t_i]\bigr).$$

**The graph $G$.** The nodes are the start $u_0 = (\emptyset, 0, \bot)$ and the triples $(S, \sigma, \tau)$ with $S \subseteq B$ not empty, $\sigma \in \{+1, -1\}$ and $\tau$ a tool. From $u = (S, \sigma, \tau)$ there is an arc to $v = (S \cup \{b\}, s_b, t)$ for each $b \notin S$ and each tool $t$ that fits $b$ with $\mathrm{coll}(S, b, t)$ false, with the cost

$$c(u, v) = \textit{flip} \cdot [\sigma \notin \{0, s_b\}] + \textit{change} \cdot [\tau \notin \{\bot, t\}] \ge 0.$$

These are the arcs that lines L5 to L7 make. The goals are the nodes with $S = B$.

**Lemma 1 (the state model).** The plans are in one to one correspondence with the paths in $G$ from $u_0$ to a goal, and a plan and its path have the same cost.

*Proof.* The function `profile_after` builds the profile from the set of done bends and the bend $b$ only: it walks from flange $b$ to flange $n$, and from flange $b - 1$ to flange $0$, and turns at bend $j$ if and only if $j$ is in the set. So $\mathrm{coll}(S, b, t)$ depends only on $S$, $b$ and $t$. This is the claim of the page that the shape does not depend on the order of the bends.

Given a plan, let $S_i = \{b_1, \dots, b_i\}$ and $u_i = (S_i, s_{b_i}, t_i)$ for $i \ge 1$. Each step $u_{i-1} \to u_i$ is an arc of $G$, because $t_i$ fits $b_i$ and $\mathrm{coll}(S_{i-1}, b_i, t_i)$ is false, and $u_n$ is a goal. The arc $u_0 \to u_1$ costs 0, since $\sigma = 0$ and $\tau = \bot$. For $i \ge 2$ the arc costs $\textit{flip} \cdot [s_{b_{i-1}} \ne s_{b_i}] + \textit{change} \cdot [t_{i-1} \ne t_i]$, the $i$-th term of the plan cost. Conversely, each arc adds one new bend to $S$, so a path from $u_0$ to a goal has exactly $n$ arcs, each adds one bend with a tool that fits it and does not collide, and reading off the pairs $(b, t)$ gives a plan. The two maps are inverse to each other, and the costs agree term by term. $\square$

**Lemma 2 (the heuristic is consistent).** For each arc $u \to v$ of $G$, $h(u) \le c(u, v) + h(v)$. Also $h = 0$ at each goal. Hence $h(u) \le h^*(u)$, the least cost of a path from $u$ to a goal, for each node $u$ from which a goal is reachable.

*Proof.* Let $u = (S, \sigma, \tau)$, let the arc add bend $b$ with tool $t$, so $v = (S \cup \{b\}, s_b, t)$, and let $R = B \setminus S$ and $R' = R \setminus \{b\}$. Write $c = c_\varphi + c_\psi$ with $c_\varphi = \textit{flip} \cdot [\sigma \notin \{0, s_b\}]$ and $c_\psi = \textit{change} \cdot [\tau \notin \{\bot, t\}]$. Since $h = \textit{flip} \cdot \varphi + \textit{change} \cdot \psi$ when $R \ne \emptyset$, it is enough to show

$$\textit{flip} \cdot \varphi(u) \le c_\varphi + \textit{flip} \cdot \varphi(v), \qquad \textit{change} \cdot \psi(u) \le c_\psi + \textit{change} \cdot \psi(v),$$

with $\varphi(v) = \psi(v) = 0$ when $R' = \emptyset$. The weights are not negative, so each inequality holds when its left side is 0. Assume the left side is not 0.

*The term $\varphi$.* Case $\sigma \ne 0$. Some $b' \in R$ has $s_{b'} \ne \sigma$. If $s_b \ne \sigma$, then $c_\varphi = \textit{flip}$, and we are done. If $s_b = \sigma$, then $b' \ne b$, so $b' \in R'$, and the last sign of $v$ is $s_b = \sigma \ne s_{b'}$. So $\varphi(v) = 1$. Case $\sigma = 0$. Then $u = u_0$ and $R$ holds bends of both signs. The bend $b$ has one sign, so some $b' \in R$ has $s_{b'} = -s_b$, and $b' \ne b$, so $b' \in R'$ and $\varphi(v) = 1$.

*The term $\psi$.* Case $\tau \ne \bot$. Some $b' \in R$ is not fit by $\tau$. If $t \ne \tau$, then $c_\psi = \textit{change}$, and we are done. If $t = \tau$, then $t$ fits $b$, because the arc exists, so $b' \ne b$, $b' \in R'$, and the last tool $t$ of $v$ does not fit $b'$. So $\psi(v) = 1$. Case $\tau = \bot$. No one tool fits all bends of $R$. If $t$ fit all bends of $R'$, then $t$ would fit all bends of $R = R' \cup \{b\}$, since it fits $b$. So some $b' \in R'$ is not fit by $t$, and $\psi(v) = 1$.

So $h(u) \le c(u, v) + h(v)$ when $R' \ne \emptyset$. When $R' = \emptyset$, that is $R = \{b\}$, the left sides are 0: for $\varphi$, $\sigma = 0$ would need two bends in $R$, and $\sigma \ne 0$ with $s_b \ne \sigma$ gives $c_\varphi = \textit{flip}$; for $\psi$, $\tau = \bot$ is not possible because $t$ fits all of $R$, and $\tau \ne \bot$ not fitting $b$ forces $t \ne \tau$, so $c_\psi = \textit{change}$. So the inequality holds in this case too.

A goal has $R = \emptyset$, so $h = 0$. For admissibility, take a cheapest path $u = w_0, w_1, \dots, w_r$ from $u$ to a goal. Adding the inequalities $h(w_{j}) \le c(w_j, w_{j+1}) + h(w_{j+1})$ for $j = 0, \dots, r - 1$ gives $h(u) \le \sum_j c(w_j, w_{j+1}) + h(w_r) = h^*(u)$. $\square$

**Lemma 3 (exact clipping).** For a segment $[p, q]$ with integer end points and a finite set of strict inequalities $a x + c y < k$ with integer coefficients, `_meets_open` returns true if and only if some point of the segment satisfies all of them.

*Proof.* The points of the segment are $p + \lambda (q - p)$ with $\lambda \in [0, 1]$. For one inequality, let $\alpha = a p_x + c p_y - k$ and $\beta = a (q_x - p_x) + c (q_y - p_y)$, so the point satisfies it if and only if $\alpha + \beta \lambda < 0$. If $\beta = 0$, this holds for all $\lambda$ when $\alpha < 0$ and for none when $\alpha \ge 0$; the code returns false in the second case and ignores the inequality in the first. If $\beta > 0$, it holds if and only if $\lambda < r$ with $r = -\alpha / \beta$, an open upper bound. If $\beta < 0$, it holds if and only if $\lambda > r$, an open lower bound. The set of good $\lambda$ is therefore an interval with the lower end $\mathrm{lo}$, the largest of 0 and the lower bounds, and the upper end $\mathrm{hi}$, the smallest of 1 and the upper bounds. An end is open when it comes from an inequality, and closed when it is the 0 or the 1 of the segment. When an inequality gives the same value as the current end, the code marks the end open, which is the tighter of the two. The interval is not empty if and only if $\mathrm{lo} < \mathrm{hi}$, or $\mathrm{lo} = \mathrm{hi}$ with both ends closed. This is the last test of the code. All values are rationals in `Fraction`, so each comparison is exact. $\square$

The punch region $\{x > 0, y > 0, \lvert x - y \rvert < w\}$ is the set of four strict inequalities $-x < 0$, $-y < 0$, $x - y < w$ and $-x + y < w$, and the die region is $x + y < 0$, $x - y < D$ and $-x + y < D$. So by Lemma 3, `collides` computes $\mathrm{coll}(S, b, t)$ exactly, and line L6 removes exactly the arcs that $G$ does not have. The cache of line L6 is keyed by $(S, b, t)$, and by Lemma 1 the result depends on nothing else, so the cache returns the same value as a new test.

**Theorem.** A*-BENDS returns a plan of least cost if a plan exists, and none otherwise. It ends after at most $1 + 2k \cdot 2^n$ states are closed.

*Proof.* By Lemma 3 and the remark after it, lines L5 to L8 generate exactly the arcs of $G$ with their costs. Lines L1 to L9 are A* on $G$ from $u_0$ with the goal test when a state leaves the queue (line L4), lazy deletion of old queue entries (line L3), and no reopening of closed states. By Lemma 2, $h$ is consistent with $h = 0$ at the goals. For such a heuristic, A* without reopening takes each state from the queue at most once, with $g$ equal to the least cost of a path from the start, and the first goal it takes has the least cost of all goals reachable from the start. If no goal is reachable, the queue becomes empty and A* reports none. This is the result stated on the [A* search](/a-star-search/) page (Hart, Nilsson and Raphael 1968).

For completeness of this note, here is the core step. With a consistent $h$, the reduced costs $c'(u, v) = c(u, v) - h(u) + h(v)$ are not negative, and the cost of a path in $c'$ is its cost in $c$ minus $h(u_0)$ plus $h$ at its end. A* with key $g + h$ is Dijkstra's algorithm on $c'$, whose keys are $g + h - h(u_0)$. Dijkstra's algorithm with nonnegative costs takes each node from the queue with its least distance, in order of that distance. Each goal has $h = 0$, so the first goal taken has the least $g$ among all goals.

By Lemma 1, the path that line L4 follows back through the parent links is a plan of the same cost, and a cheaper plan would give a cheaper path to a goal. So the plan has least cost. If no plan exists, no goal is reachable, by Lemma 1 again, and line L9 returns none.

$G$ has at most $1 + 2^n \cdot 2k$ nodes, so at most that many states are closed. Each closed state puts at most $nk$ entries in the queue, so the queue empties after finitely many steps, and the search ends. $\square$
