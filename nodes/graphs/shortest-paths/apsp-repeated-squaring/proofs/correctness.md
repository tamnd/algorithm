---
title: Repeated squaring computes all distances or detects a negative cycle
proves: [correctness, termination]
status: full
---

**Claim.** Let $G$ be a directed graph on the vertices $1, \ldots, n$ with real weights, parallel edges and self-loops allowed. APSP-REPEATED-SQUARING returns NEGATIVE-CYCLE if and only if $G$ has a cycle of negative weight. Otherwise it returns the matrix $D$ with $D[i][j] = \delta(i, j)$ for all $i, j$, where $\delta(i, j) = +\infty$ when no path exists.

**Termination.** The variable $k$ starts at 1 and doubles in each pass of line L4, so the loop runs $\lceil \log_2 n \rceil$ times (zero times when $n \le 1$). Each pass has loops with fixed bounds. So the algorithm ends.

**Notation.** A walk may repeat vertices and edges; the empty walk from $i$ to $i$ has weight 0. Let $L^{(k)}[i][j]$ be the least weight of a walk from $i$ to $j$ with at most $k$ edges, or $+\infty$ if there is none. This is a minimum over finitely many walks (finitely many sequences of at most $k$ edges), so it is well defined. Write $(A \star B)[i][j] = \min_t (A[i][t] + B[t][j])$, with $\infty + x = \infty$.

**Step 1: the start.** After line L2, $L[i][j]$ for $i \ne j$ is the least weight of an edge from $i$ to $j$, and $L[i][i] = \min(0, \text{the least self-loop weight at } i)$. A walk with at most one edge from $i$ to $j$ is a single edge, or, when $i = j$, also the empty walk. So $L = L^{(1)}$. Also $L^{(k)}[i][i] \le 0$ for every $k \ge 0$, because of the empty walk.

**Step 2: the product.** For $a, b \ge 1$, $L^{(a)} \star L^{(b)} = L^{(a + b)}$.

($\ge$) Take $t$ with $L^{(a)}[i][t]$ and $L^{(b)}[t][j]$ finite, and walks $p$ from $i$ to $t$ and $q$ from $t$ to $j$ that attain them. The joined walk $pq$ has at most $a + b$ edges and weight $L^{(a)}[i][t] + L^{(b)}[t][j]$, so this sum is at least $L^{(a + b)}[i][j]$. Terms with an infinite factor are $\infty$ and do not matter.

($\le$) If $L^{(a + b)}[i][j] = \infty$ there is nothing to show. Otherwise take a walk $r$ from $i$ to $j$ with $\ell \le a + b$ edges and weight $L^{(a + b)}[i][j]$. Let $t$ be the vertex of $r$ after $\min(a, \ell)$ edges. The part of $r$ before $t$ has at most $a$ edges and the part after has $\ell - \min(a, \ell) \le b$ edges, so $L^{(a)}[i][t] + L^{(b)}[t][j] \le w(r)$.

**Step 3: the copy in line L5.** In a pass, with $L = L^{(k)}$, let $P = L \star L$ be the true product and $M$ the computed matrix, $M[i][j] = \min(L[i][j], P[i][j])$. Since $L[i][i] \le 0$, the term $t = i$ gives $P[i][j] \le L[i][i] + L[i][j] \le L[i][j]$, so $M = P$. By Step 2 and induction on the passes, $L = L^{(k)}$ after each pass, with $k$ the current value. At the end, $L = L^{(K)}$ for some $K \ge n$ (for $n \le 1$, $K = 1 \ge n$).

**Step 4: no negative cycle.** Suppose $G$ has no cycle of negative weight. Any walk from $i$ to $j$ that repeats a vertex contains a closed sub-walk, which consists of cycles, each of weight at least 0; removing it gives a walk with fewer edges and no larger weight. Repeating this gives a simple path, with at most $n - 1$ edges. So the least walk weight over walks of any length is attained by a simple path, it equals $\delta(i, j)$, and $L^{(K)}[i][j] = \delta(i, j)$ since $K \ge n - 1$. In particular $L^{(K)}[i][i] = \delta(i, i) = 0$, line L9 does not fire, and line L10 returns the distances. A pair with no path has no walk at all, so its entry is $\infty$.

**Step 5: a negative cycle.** Suppose $G$ has a cycle of negative weight. Write it as a closed walk; splitting at repeated vertices writes it as a union of simple cycles, and since their weights add up to a negative number, one simple cycle $C$ has $w(C) < 0$. It has at most $n$ edges. For a vertex $i$ on $C$, $C$ is a walk from $i$ to $i$ with at most $n \le K$ edges, so $L^{(K)}[i][i] \le w(C) < 0$, and line L9 returns NEGATIVE-CYCLE.

**Step 6: no false report.** If line L9 fires, $L^{(K)}[i][i] < 0$ is the weight of a closed walk from $i$, and by the splitting in Step 5 one of its simple cycles is negative. So a report happens only when $G$ has a negative cycle.

Steps 4 to 6 give the claim. $\blacksquare$
