---
title: SPMAIN returns the shortest-path distances from s or reports a negative cycle reachable from s
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ have integer weights $w$ and source $s$. For a potential $\phi$, $w_\phi(u, v) = w(u, v) + \phi(u) - \phi(v)$. We use two facts about potentials.

**Fact 1.** For every walk $P$ from $a$ to $b$, $w_\phi(P) = w(P) + \phi(a) - \phi(b)$; in particular every cycle has the same weight under $w$ and $w_\phi$. (The terms $\phi$ telescope.)

**Fact 2.** If $c > 0$, then $c \cdot w$ has a negative cycle if and only if $w$ has one. If $w' \ge w$ on every arc, a negative cycle under $w'$ is a negative cycle under $w$.

## ELIMNEG

Let $H$ be a graph with $N$ vertices and weights $w$. Add a virtual source $\sigma$ with an arc of weight 0 to every vertex; $\mathrm{dist}(v)$ is the distance from $\sigma$, and $\eta(v)$ is the least number of negative arcs on a shortest path from $\sigma$ to $v$, when $\mathrm{dist}(v)$ is finite.

**Lemma 3 (labels are walk weights).** At all times, each $d(v)$ is the weight of some walk from $\sigma$ to $v$. Hence $d(v) \ge \mathrm{dist}(v)$ when $\mathrm{dist}(v) > -\infty$.

*Proof.* Initially $d(v) = 0$, the weight of the arc $\sigma \to v$. A relaxation sets $d(x) = d(v) + w(v, x)$, the weight of the walk to $v$ followed by the arc $(v, x)$. $\square$

**Lemma 4 (pending vertices).** Call an arc $(v, x)$ *violated* if $d(v) + w(v, x) < d(x)$. At the start of each round, and when the loop ends, every violated arc $(v, x)$ has $v \in Q$. During the Bellman-Ford phase of a round, every violated nonnegative arc $(v, x)$ has $v \in Q$, and every violated negative arc $(v, x)$ has $v \in Q$ or $v$ marked.

*Proof.* Initially every vertex is in $Q$. An arc can become violated only when $d(v)$ decreases, and every decrease puts $v$ into $Q$. In the Dijkstra phase, a vertex leaves $Q$ only when it is extracted with its current label (stale heap entries carry larger keys and are skipped), and it is then marked and its nonnegative arcs are relaxed, so they are not violated after that; later decreases of $d(v)$ put $v$ back into $Q$. So at the end of the Dijkstra phase $Q$ is empty, no nonnegative arc is violated, and every violated negative arc starts at a marked vertex. The Bellman-Ford phase relaxes every negative arc out of a marked vertex, after which it is not violated unless $d(v)$ drops again, which puts $v$ into $Q$. Unmarking then leaves only violated arcs with $v \in Q$. $\square$

**Lemma 5 (rounds).** Assume $H$ has no negative cycle. At the end of the Dijkstra phase of round $i$, $d(v) = \mathrm{dist}(v)$ for every $v$ with $\eta(v) \le i - 1$.

*Proof.* By induction on $i$. Let $v$ have $\eta(v) \le i - 1$ and let $P = \sigma, v_0, v_1, \ldots, v_r = v$ be a shortest path with $\eta(v)$ negative arcs. Every prefix of $P$ is a shortest path.

If $P$ has no negative arc ($\eta(v) = 0$), then $\mathrm{dist}(v_0) = 0 = d(v_0)$ from the start, as $d(v_0) \le 0$ always and $d(v_0) \ge \mathrm{dist}(v_0)$ by Lemma 3. At the end of the Dijkstra phase of round $i \ge 1$, no nonnegative arc is violated (proof of Lemma 4), so along $P$, $d(v_j) \le d(v_{j-1}) + w(v_{j-1}, v_j)$, and summing gives $d(v) \le w(P) = \mathrm{dist}(v)$. With Lemma 3, $d(v) = \mathrm{dist}(v)$.

Otherwise let $(a, b)$ be the last negative arc of $P$. The prefix to $a$ is a shortest path with at most $i - 2$ negative arcs, so $\eta(a) \le i - 2$, and by induction $d(a) = \mathrm{dist}(a)$ at the end of the Dijkstra phase of round $i - 1$. Labels never increase and never go below $\mathrm{dist}$, so $d(a)$ reached its final value at its last decrease, which happened no later than that Dijkstra phase. A decrease puts $a$ into $Q$, and every Dijkstra phase empties $Q$, so $a$ was extracted with the label $\mathrm{dist}(a)$ and marked in some round $j \le i - 1$. The Bellman-Ford phase of round $j$ relaxed $(a, b)$ with $d(a) = \mathrm{dist}(a)$, so afterward $d(b) \le \mathrm{dist}(a) + w(a, b) = \mathrm{dist}(b)$, hence $d(b) = \mathrm{dist}(b)$. The rest of $P$ from $b$ to $v$ uses only nonnegative arcs; at the end of the Dijkstra phase of round $i$ none of them is violated, so summing gives $d(v) \le \mathrm{dist}(b) + w(b \ldots v) = \mathrm{dist}(v)$. $\square$

**Lemma 6 (ELIMNEG).** If $H$ has no negative cycle, ELIMNEG returns, after at most $N$ rounds, labels $d$ with $w_d(v, x) \ge 0$ on every arc. If $H$ has a negative cycle, it returns "negative cycle".

*Proof.* With no negative cycle, every $v$ has a shortest path from $\sigma$ that is simple, with at most $N$ arcs, the first of which is the nonnegative arc from $\sigma$; so $\eta(v) \le N - 1$. By Lemma 5, at the end of the Dijkstra phase of round $N$ (if the loop gets that far) every label is exact, so the Bellman-Ford phase lowers no label (Lemma 3) and $Q$ stays empty. So the loop ends after at most $N$ rounds and line L17 never fires. When the loop ends, $Q$ is empty, so by Lemma 4 no arc is violated: $d(x) \le d(v) + w(v, x)$, that is $w_d(v, x) \ge 0$.

If $H$ has a negative cycle $C$, the loop cannot end normally: then no arc would be violated, and summing $w_d \ge 0$ around $C$ would give $w(C) = w_d(C) \ge 0$ by Fact 1. Each round is finite: in the Dijkstra phase the extracted keys never decrease, because a relaxation of a nonnegative arc gives a key at least the key just extracted, so each vertex is extracted at most once per phase; the Bellman-Ford phase relaxes each arc at most once. So the counter $r$ grows until line L17 returns "negative cycle". $\square$

## SCALEDOWN

**Lemma 7.** Let $w \ge -2B$ on $H$, with integer $B \ge 1$. SCALEDOWN terminates. If it returns "negative cycle", then $H$ has a negative cycle under $w$. If $H$ has no negative cycle under $w$, it returns $\phi$ with $w_\phi(e) \ge -B$ for every arc $e$.

*Proof.* Termination: the recursive calls in line L11 have $\Delta$ halved, so the depth is at most $\log_2 \Delta$; the LDD, the SCC computation and FIXDAGEDGES are finite; and ELIMNEG ends by Lemma 6.

A recursive call runs on an induced subgraph $H[V_j]$ with the same weights $w \ge -2B$, so by induction on the depth it returns "negative cycle" only if $H[V_j]$, and so $H$, has a negative cycle. Line L13 runs ELIMNEG on $(w_B)_{\phi_2}$. If it reports a negative cycle, then $w_B$ has one by Fact 1, and so $w$ has one by Fact 2, since $w_B \ge w$.

Now assume $H$ has no negative cycle under $w$. Then $w_B \ge w$ has none (Fact 2), and $(w_B)_{\phi_2}$ has none (Fact 1), so the recursive calls do not report a cycle, and by Lemma 6 line L13 returns $\psi$ with $(w_B)_{\phi_2 + \psi}(e) \ge 0$. Let $\phi = \phi_2 + \psi$. For every arc, $w_B(e) \le w(e) + B$, so

$$w_\phi(e) = (w_B)_\phi(e) - (w_B(e) - w(e)) \ge 0 - B = -B. \qquad \square$$

The lemma does not use any property of $E_{\mathrm{rem}}$, of the components, or of $\phi_2$; these affect only the running time.

## SPMAIN

Let $R$ be the set of vertices reachable from $s$, and $k = |R|$. Line L1 keeps $G[R]$. Every walk from $s$ stays in $R$, so $\delta(s, v)$ is the same in $G$ and in $G[R]$ for $v \in R$, it is $+\infty$ for $v \notin R$, and a negative cycle is reachable from $s$ in $G$ exactly when $G[R]$ has a negative cycle.

**Invariant.** If $G[R]$ has no negative cycle, then before the call in line L4 with the value $b = B / 2^i$, every arc has $\bar{w}_\phi(e) \ge -2b$.

*Proof.* For $i = 1$, $\phi = 0$ and $\bar{w}(e) = 2k\, w(e) \ge -2kW \ge -B = -2b$. The call returns $\psi$ with $(\bar{w}_\phi)_\psi \ge -b = -2 \cdot (b / 2)$ by Lemma 7, since $\bar{w}_\phi$ has no negative cycle (Facts 1 and 2). $\square$

**Theorem.** SPMAIN returns "negative cycle" exactly when a negative cycle is reachable from $s$, and otherwise returns $\delta(s, v)$ for every $v$.

*Proof.* Suppose $G[R]$ has no negative cycle. No call in line L4 reports a cycle (Lemma 7). After the last call, with $b = 1$, every $\bar{w}_\phi(e) \ge -1$, so $w^*(e) = \bar{w}_\phi(e) + 1 \ge 0$ and line L5 passes. Dijkstra in line L6 is correct for nonnegative weights and gives a tree $T$ whose path $P$ from $s$ to each $v \in R$ is simple and shortest under $w^*$. Let $Q$ be a simple shortest path from $s$ to $v$ under $w$, which exists as there is no negative cycle. By Fact 1, for every path $X$ from $s$ to $v$, $w^*(X) = 2k\, w(X) + \phi(s) - \phi(v) + |X|$, where $|X|$ is its number of arcs. From $w^*(P) \le w^*(Q)$,

$$2k \bigl( w(P) - w(Q) \bigr) \le |Q| - |P| \le k - 1 < 2k,$$

so $w(P) - w(Q) < 1$, and since both are integers, $w(P) \le w(Q) = \delta(s, v)$. Hence $w(P) = \delta(s, v)$, which is the value returned.

Suppose $G[R]$ has a negative cycle $C$, so $w(C) \le -1$. If some call in line L4 reports a cycle, the answer is right. Otherwise, after the loop, by Facts 1 and 2, $w^*(C) = 2k\, w(C) + |C| \le -2k + k < 0$, so some arc of $C$ has $w^*(e) < 0$ and line L5 returns "negative cycle". In both cases the answer is correct, and line L6 is not reached.

Conversely, "negative cycle" is returned only by line L4, which needs a negative cycle by Lemma 7 and Facts 1 and 2, or by line L5, which by the invariant cannot fire when there is no negative cycle. $\square$

**Termination.** Line L3 runs $\log_2 B$ iterations, each a call of SCALEDOWN that terminates by Lemma 7; lines L1, L2, L5 and L6 are finite. So SPMAIN terminates on every input, with or without negative cycles. $\blacksquare$
