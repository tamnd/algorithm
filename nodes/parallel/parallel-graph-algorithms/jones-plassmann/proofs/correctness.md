---
title: Jones-Plassmann computes the greedy coloring of the priority order, and its rounds are the longest decreasing path
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is undirected with $n \ge 1$ vertices, $m$ edges and largest degree $\Delta$. The priorities $\rho$ are distinct. For a vertex $v$, $H(v)$ is the set of its neighbours $u$ with $\rho(u) > \rho(v)$ (the higher neighbours) and $L(v)$ the set of its neighbours with $\rho(u) < \rho(v)$. Define $\ell(v) = 1$ if $H(v) = \emptyset$ and $\ell(v) = 1 + \max_{u \in H(v)} \ell(u)$ otherwise; this is well defined because $\rho$ strictly increases along the recursion. By induction, $\ell(v)$ is the largest number of vertices on a path $v_1, \ldots, v_k = v$ with $\rho(v_1) > \cdots > \rho(v_k)$.

The sequential greedy algorithm takes the vertices in decreasing $\rho$ and gives each the least color not used by its neighbours colored before it. Call its result $g$.

**Lemma 1 (rounds of each vertex).** Every vertex enters the ready set exactly once, in round $\ell(v)$, and is colored in that round.

*Proof.* By strong induction along decreasing $\rho$. Line L2 sets $wait(v) = |H(v)|$, and $wait(v)$ is decremented only in line L8, once for each $u \in H(v)$ in the round in which $u$ is colored, because $v \in L(u)$. If $H(v) = \emptyset$, $wait(v) = 0$, so $v$ is in the ready set of round 1 by line L3, and no decrement reaches it later. Otherwise, by the induction hypothesis each $u \in H(v)$ is colored once, in round $\ell(u)$. So $wait(v)$ reaches 0 exactly once, in round $r = \max_{u \in H(v)} \ell(u)$, when the last of them is colored; line L8 then puts $v$ in the next ready set, and line L9 makes it ready in round $r + 1 = \ell(v)$. It was not ready earlier, since $wait(v) > 0$ before round $r$ ends and $v$ is not in the set of line L3. $\square$

**Theorem 1 (correctness).** The algorithm stops after $R = \max_v \ell(v)$ rounds, and $c = g$. In particular $c$ is a proper coloring with at most $\Delta + 1$ colors.

*Proof.* By Lemma 1, every vertex is ready in exactly one round, so the ready set is empty after round $\max_v \ell(v)$ and the loop of line L4 stops; it is not empty before, because a vertex $v$ with $\ell(v) = r$ is ready in round $r$ and, for $r > 1$, has a higher neighbour $u$ with $\ell(u) = r - 1$.

Two vertices ready in the same round are not adjacent: for an edge with $\rho(u) > \rho(v)$, $\ell(v) \ge \ell(u) + 1$. So the colors chosen in one round in line L6 read only colors set in earlier rounds.

Now show $c(v) = g(v)$ by strong induction along decreasing $\rho$. When $v$ is colored in round $\ell(v)$, every $u \in H(v)$ has been colored in round $\ell(u) < \ell(v)$, and by induction $c(u) = g(u)$. Line L6 gives $v$ the least color not in $\{c(u) : u \in H(v)\} = \{g(u) : u \in H(v)\}$. In the greedy algorithm, the neighbours of $v$ colored before $v$ are exactly those of higher $\rho$, that is $H(v)$, so $g(v)$ is the least color not in the same set. Hence $c(v) = g(v)$.

For an edge $\{u, v\}$ with $\rho(u) > \rho(v)$, $u \in H(v)$, so $c(v) \ne c(u)$; the coloring is proper. The set $\{c(u) : u \in H(v)\}$ has at most $|H(v)| \le \Delta$ elements, so the least color outside it is at most $\Delta$, and at most $\Delta + 1$ colors $0, \ldots, \Delta$ are used. $\blacksquare$

**Theorem 2 (work).** With an $O(1)$ fetch-and-add, the total work is $O(n + m)$.

*Proof.* Line L2 looks at every adjacency entry once: $O(n + m)$. By Lemma 1, each vertex is in a ready set once; then line L6 scans $H(v)$ and line L7 scans $L(v)$, which is $O(1 + \deg v)$ work, with $O(\deg v)$ for the least free color by marking the at most $\deg v$ used colors in a bit array of length $\deg v + 1$. Summed over $v$ this is $O(n + m)$. $\blacksquare$

**Theorem 3 (rounds for a random order).** Let $\rho$ be a uniformly random permutation and $\Delta \ge 1$. For every integer $k \ge 1$,

$$\Pr[R \ge k] \le \frac{n \Delta^{k-1}}{k!}.$$

For every $c > 0$, $\Pr[R > \max(e^2 \Delta, (c + 1) \ln n)] \le n^{-c}$, and $E[R] \le e^2 \Delta + \ln n + 3$.

*Proof.* By Theorem 1, $R \ge k$ holds exactly when there is a path $v_1, \ldots, v_k$ in $G$ with $\rho(v_1) > \cdots > \rho(v_k)$; strictly decreasing priorities make the $k$ vertices distinct. There are at most $n \Delta^{k-1}$ sequences $v_1, \ldots, v_k$ of distinct vertices with $v_{i+1}$ a neighbour of $v_i$: $n$ choices for $v_1$ and at most $\Delta$ for each next one. For a fixed sequence of $k$ distinct vertices, the order of their priorities is uniform over the $k!$ orders, so it is decreasing with probability $1 / k!$. The [union bound](/union-bound/) gives the first claim.

Since $k! \ge (k / e)^k$,

$$\frac{n \Delta^{k-1}}{k!} \le \frac{n}{\Delta} \left( \frac{e \Delta}{k} \right)^k \le n \left( \frac{e \Delta}{k} \right)^k.$$

If $k \ge e^2 \Delta$, then $e \Delta / k \le e^{-1}$, so $\Pr[R \ge k] \le n e^{-k}$.

Let $K = \max(e^2 \Delta, (c + 1) \ln n)$ and $k = \lfloor K \rfloor + 1 > K$. Then $k \ge e^2 \Delta$ and $k > (c + 1) \ln n$, so $\Pr[R > K] = \Pr[R \ge k] \le n e^{-k} < n \cdot n^{-(c + 1)} = n^{-c}$.

For the expectation, let $k_0 = \max(\lceil e^2 \Delta \rceil, \lceil \ln n \rceil)$. Then $\Pr[R \ge k] \le n e^{-k}$ for $k > k_0$, and

$$E[R] = \sum_{k \ge 1} \Pr[R \ge k] \le k_0 + \sum_{k > k_0} n e^{-k} = k_0 + \frac{n e^{-k_0}}{e - 1} \le k_0 + \frac{1}{e - 1} < k_0 + 1,$$

using $n e^{-k_0} \le 1$. Since $k_0 \le e^2 \Delta + \ln n + 2$, $E[R] \le e^2 \Delta + \ln n + 3$. If $\Delta = 0$, every vertex is ready in round 1 and $R = 1$. $\blacksquare$

**Corollary (span).** Each round has $O(\log n)$ span: line L6 is a minimum over at most $\Delta + 1$ marks, line L8 a set of fetch-and-add operations, and line L9 a pack of the vertices whose count reached 0. So $S = O(R \log n)$, which is $O((\Delta + \log n) \log n)$ with high probability and in expectation, by Theorem 3. $\blacksquare$
