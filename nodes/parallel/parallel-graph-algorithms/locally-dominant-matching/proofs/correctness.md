---
title: The locally dominant matching is the greedy matching, has at least half the maximum weight, and takes at most as many rounds as the longest decreasing chain of edges
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E, w)$ is an undirected graph without self-loops, with $n$ vertices, $m$ edges and largest degree $\Delta$. Every edge has a distinct key $(w(e), \text{index})$; "heavier" means "larger key". Two different edges are *adjacent* if they share an end. $G^*$ is the greedy matching: take the edges in decreasing key and add an edge when neither end is covered yet. In round $t$, $G_t$ is the graph of the edges whose two ends are unmatched at the start of the round; its edges are the *live* edges.

**Lemma 1 (local description of the greedy matching).** An edge $e$ is in $G^*$ exactly when no heavier edge adjacent to $e$ is in $G^*$.

*Proof.* When the greedy algorithm reaches $e$, the edges taken so far are exactly the edges of $G^*$ heavier than $e$. It takes $e$ exactly when no end of $e$ is covered by them, that is, when no heavier edge of $G^*$ is adjacent to $e$. $\square$

**Lemma 2 (candidates).** At line L6 of every round, every unmatched vertex $v$ has $cand(v)$ equal to its heaviest live edge, or none if it has no live edge. Moreover, the set $D$ of line L6 is the set of locally dominant edges of $G_t$, and $D$ is a matching.

*Proof.* Only line L5 sets $cand(v)$, and only for $v$ in $check$. Line L4 moves $ptr(v)$ past the edges to matched vertices; the list is sorted by decreasing key, so the edge at $ptr(v)$ is then the heaviest live edge of $v$. Now let $v$ be unmatched and not in $check$ in round $t$, and let $t' < t$ be the last round in which $v$ was in $check$ (round 0 if $v$ has an edge at all). If $cand(v)$ was none at $t'$, all neighbours of $v$ were matched, and they stay matched. Otherwise the other end $u$ of $cand(v)$ is still unmatched: if $u$ had been matched in a round between $t'$ and $t - 1$, line L8 of that round would have marked $v$, and $v$ would be in $check$ in the next round. Since vertices only become matched, the live edges of $v$ at round $t$ are a subset of those at round $t'$, and $cand(v)$ is still among them, so it is still the heaviest.

An edge $e = \{u, v\}$ of $G_t$ is locally dominant exactly when it is the heaviest live edge at both ends, that is, when $cand(u) = cand(v) = e$. Line L6 only looks at the ends in $check$. Suppose $cand(u) = cand(v) = e$ and neither $u$ nor $v$ is in $check$ in round $t$. Let $t_u, t_v < t$ be the last rounds in which $u$ and $v$ were in $check$, and $t' = \max(t_u, t_v)$. From round $t'$ on, both candidates are $e$, and the end set in round $t'$ was in $check$ then, so $e \in D$ in round $t'$ and both ends were matched, a contradiction. So $D$ is exactly the set of locally dominant edges of $G_t$. Each vertex has one candidate, so the edges of $D$ share no end. $\square$

**Theorem 1 (correctness and termination).** The algorithm stops after at most $\lfloor n/2 \rfloor$ rounds that add edges, and returns $M = G^*$. So $M$ is a maximal matching.

*Proof.* Invariant at the start of each round: (a) $M \subseteq G^*$, and (b) every edge that is neither live nor in $M$ is not in $G^*$. Both hold at the start.

Let $e \in D$ in round $t$. Every heavier edge $f$ adjacent to $e$ is not live, since $e$ is locally dominant in $G_t$ (Lemma 2). And $f \notin M$, since an edge of $M$ adjacent to $e$ would have matched an end of $e$, while both ends of the live edge $e$ are unmatched. So by (b), $f \notin G^*$. By Lemma 1, $e \in G^*$, and (a) holds after the round. The edges that stop being live in the round, other than the edges of $D$, share an end with an edge of $D \subseteq G^*$; since $G^*$ is a matching, they are not in $G^*$, and (b) holds.

If $G_t$ has an edge, its heaviest edge is locally dominant, so $D \ne \emptyset$ and at least two vertices are matched. By Lemma 2, an end of that edge is in $check$, so the loop does not stop while live edges remain. When no live edge remains, line L5 gives no candidates, line L6 finds nothing and line L8 marks nothing, so the loop stops after one more pass. At that point no edge is live, so every edge of $G$ has a matched end and $M$ is maximal; and every edge of $G^*$ is in $M$, since by (b) an edge outside $M$ that is not live is not in $G^*$. With (a), $M = G^*$. $\blacksquare$

**Theorem 2 (half of the maximum weight).** If all weights are non-negative and $M^*$ is any matching, then $w(M^*) \le 2\, w(M)$.

*Proof.* Let $f \in M^*$. If $f \in M$, charge $w(f)$ to $f$ at either end. Otherwise, by Lemma 1 and $M = G^*$, some heavier edge $e \in M$ is adjacent to $f$; charge $w(f) \le w(e)$ to $e$ at a shared end. At each end $x$ of an edge $e \in M$, at most one edge of $M^*$ has the end $x$, so $e$ gets at most two charges, each at most $w(e)$. Summing, $w(M^*) \le 2\, w(M)$. $\blacksquare$

**Theorem 3 (rounds).** For an edge $e$, let $\ell(e) = 1$ if no heavier edge is adjacent to $e$, and $\ell(e) = 1 + \max \ell(f)$ over the heavier edges $f$ adjacent to $e$ otherwise; so $L = \max_e \ell(e)$ is the number of edges on the longest sequence $f_1, \ldots, f_k$ of edges with $f_i$ adjacent to $f_{i+1}$ and decreasing keys. Then $r \le L$.

*Proof.* By strong induction along decreasing keys, every edge $e$ stops being live by the end of round $\ell(e)$. At the start of round $\ell(e)$, every heavier adjacent edge $f$ has stopped being live by the end of round $\ell(f) \le \ell(e) - 1$. So if $e$ is still live, it is locally dominant in $G_{\ell(e)}$ and joins $M$ in that round by Lemma 2. Hence no edge is live after round $L$. Every round that adds an edge starts with a live edge, and these rounds come first, so $r \le L$. $\blacksquare$

**Theorem 4 (rounds for a random order).** Let $G$ be simple with $\Delta \ge 2$ and let the key order be a uniformly random order of the edges. For every $c > 0$ and $n \ge 2$, $\Pr[r > \max(2 e^2 \Delta, (c + 2) \ln n)] \le n^{-c}$.

*Proof.* By Theorem 3, $r \ge k$ implies a sequence of $k$ distinct edges, each adjacent to the next, with decreasing keys. There are at most $m (2\Delta)^{k-1}$ such sequences: $m$ choices for the first edge and fewer than $2 \Delta$ edges adjacent to each edge. A fixed sequence of $k$ distinct edges is in decreasing order with probability $1/k!$. By the union bound and $k! \ge (k/e)^k$, with $D = 2\Delta$,

$$\Pr[r \ge k] \le \frac{m D^{k-1}}{k!} \le \frac{m}{D} \left( \frac{e D}{k} \right)^k \le m e^{-k} \quad \text{for } k \ge e^2 D.$$

Let $K = \max(2 e^2 \Delta, (c + 2) \ln n)$ and $k = \lfloor K \rfloor + 1$. Then $\Pr[r > K] = \Pr[r \ge k] \le m e^{-k} < n^2 \cdot n^{-(c + 2)} = n^{-c}$, using $m < n^2$. If $\Delta \le 1$, the edges are pairwise disjoint and $r \le 1$. $\blacksquare$

**Theorem 5 (work).** After the sort, the rounds do $O(n + m)$ work in total.

*Proof.* Each pointer only moves forward, so line L4 does $O(n + m)$ steps over the run, plus $O(1)$ per vertex in $check$. Each vertex is matched at most once, and line L8 then scans its edges once, $O(m)$ in total. A vertex enters $check$ after round 1 only when line L8 marks it, and each mark comes from one scanned edge, so the sizes of all $check$ sets add up to at most $n + 2m$. Lines L5 to L7 and L9 cost $O(1)$ per vertex in $check$. $\blacksquare$
