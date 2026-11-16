---
title: Color coding finds a k-path with one-sided error, and one random coloring makes a fixed k-path colorful with probability k!/k^k
proves: [correctness]
status: full
---

Let $G = (V, E)$ be a graph with $n$ vertices and $m$ edges, undirected or directed, and let $k \ge 1$. For a directed graph, "a neighbor $v$ of $u$" means an arc from $u$ to $v$, and paths follow the arcs. A *walk* is a sequence of vertices in which each consecutive pair is adjacent; a *path* is a walk with pairwise distinct vertices. For a coloring $c: V \to \{1, \ldots, k\}$ and a walk $W = (w_1, \ldots, w_j)$, write $c(W) = \{c(w_1), \ldots, c(w_j)\}$. The walk is *colorful* if $|c(W)| = j$, that is, if its vertices have pairwise different colors.

**Lemma 1 (colorful walks are paths).** A colorful walk is a path.

*Proof.* If $w_a = w_b$ for some $a < b$, then $c(w_a) = c(w_b)$, and the walk is not colorful. $\square$

**Lemma 2 (the table is exact).** After COLORFUL-PATH$(G, c, k)$ has run lines L1 to L4, for every vertex $v$ and every set $S \subseteq \{1, \ldots, k\}$ with $1 \le |S| \le k$, the entry $D[v, S]$ is set if and only if $G$ has a colorful walk $W$ that ends at $v$ with $c(W) = S$. Moreover, if $D[v, S] = u$ is not the start mark, then $D[u, S \setminus \{c(v)\}]$ is set, $c(v) \in S$, $c(v) \notin S \setminus \{c(v)\}$, and $u v$ is an edge.

*Proof.* By induction on $|S|$. Note that a colorful walk $W$ with $c(W) = S$ has exactly $|S|$ vertices.

*Size 1.* Line L1 sets $D[v, \{c(v)\}]$ for every $v$, and no other line sets an entry with $|S| = 1$, since L4 sets only entries with $|S \cup \{c(v)\}| = |S| + 1 \ge 2$. A colorful walk of one vertex ending at $v$ is $(v)$, with color set $\{c(v)\}$. So the claim holds.

*Size i + 1, for 1 ≤ i ≤ k - 1.* Entries with $|S| = i + 1$ are set only at L4 in round $i$ of the loop at L2, from an entry $D[u, S']$ with $|S'| = i$. By the time round $i$ starts, all entries of size $i$ are set: those of size 1 by L1, and those of size $i \ge 2$ in round $i - 1$. So round $i$ sees all of them.

($\Rightarrow$) Suppose L4 sets $D[v, S]$ to $u$ in round $i$. Then $D[u, S']$ is set with $|S'| = i$, $v$ is a neighbor of $u$, $c(v) \notin S'$ and $S = S' \cup \{c(v)\}$. By induction, there is a colorful walk $W'$ ending at $u$ with $c(W') = S'$. Append $v$. The new walk ends at $v$, its color set is $S$, and it has $i + 1 = |S|$ vertices, so it is colorful. This also proves the second part of the lemma, since $S \setminus \{c(v)\} = S'$.

($\Leftarrow$) Let $W = (w_1, \ldots, w_{i+1})$ be a colorful walk with $w_{i+1} = v$ and $c(W) = S$. Its prefix $W' = (w_1, \ldots, w_i)$ is colorful, ends at $u = w_i$, and has the color set $S' = S \setminus \{c(v)\}$ of size $i$, with $c(v) \notin S'$. By induction $D[u, S']$ is set, so round $i$ processes it at L3 and looks at the neighbor $v$ of $u$. At that moment $c(v) \notin S'$, so L4 sets $D[v, S]$ if it is not set yet. Either way it is set after round $i$. $\square$

**Lemma 3 (the trace back).** If $D[v, \{1, \ldots, k\}]$ is set, the trace back of line L5 returns a colorful path with $k$ vertices that ends at $v$.

*Proof.* Start with $(v_k, S_k) = (v, \{1, \ldots, k\})$. While $D[v_j, S_j]$ is a vertex $u$, set $v_{j-1} = u$ and $S_{j-1} = S_j \setminus \{c(v_j)\}$. By the second part of Lemma 2, $D[v_{j-1}, S_{j-1}]$ is set, $v_{j-1} v_j$ is an edge, and $|S_{j-1}| = |S_j| - 1$. The size of the set falls by one at each step, and an entry of size 1 is always the start mark, so the trace stops after exactly $k - 1$ steps at $(v_1, S_1)$ with $|S_1| = 1$, and $S_1 = \{c(v_1)\}$. By construction $S_j = \{c(v_1), \ldots, c(v_j)\}$ with $|S_j| = j$ for every $j$, so the colors $c(v_1), \ldots, c(v_k)$ are pairwise different. The sequence $v_1, \ldots, v_k$ is a colorful walk, and by Lemma 1 it is a path with $k$ vertices. $\square$

**Theorem 1 (COLORFUL-PATH is correct).** COLORFUL-PATH$(G, c, k)$ returns a $k$-path if $G$ has a colorful $k$-path under $c$, and NONE otherwise.

*Proof.* A colorful walk with $k$ vertices and colors in $\{1, \ldots, k\}$ has the color set $\{1, \ldots, k\}$. By Lemma 2, some entry $D[v, \{1, \ldots, k\}]$ is set if and only if a colorful walk with $k$ vertices exists, and by Lemma 1 such a walk is a colorful $k$-path. If an entry is set, line L5 returns a $k$-path by Lemma 3. If no entry is set, line L6 returns NONE, and no colorful $k$-path exists. $\square$

**Lemma 4 (one coloring).** Let $P$ be a fixed $k$-path, and let $c$ give each vertex a color from $\{1, \ldots, k\}$ uniformly and independently. Then $P$ is colorful with probability exactly $k!/k^k$, and $k!/k^k > e^{-k}$.

*Proof.* The colors of the $k$ distinct vertices of $P$ form a uniform random element of $\{1, \ldots, k\}^k$, because the colors are independent and uniform. $P$ is colorful exactly when this tuple has pairwise different entries, that is, when it is a permutation of $\{1, \ldots, k\}$. There are $k!$ permutations among the $k^k$ tuples, so the probability is $k!/k^k$. For the bound, $e^k = \sum_{i \ge 0} k^i / i!$, and every term is positive, so $e^k > k^k / k!$ (the sum has the term $i = k$ and the term $i = 0$). Hence $k!/k^k > e^{-k}$. $\square$

The colors of vertices outside $P$ do not matter for this event, so the bound holds for every graph that contains $P$.

**Theorem 2 (K-PATH has one-sided error).** Let $t \ge 1$.

1. If $G$ has no $k$-path, K-PATH$(G, k, t)$ returns NONE with probability 1.
2. If $G$ has a $k$-path, K-PATH$(G, k, t)$ returns a $k$-path with probability at least $1 - (1 - k!/k^k)^t \ge 1 - \exp(-t \, k!/k^k)$.
3. With $t = \lceil \ln(1/\delta) \, k^k / k! \rceil$ for some $0 < \delta < 1$, the probability in part 2 is at least $1 - \delta$.

*Proof.* Part 1. By Theorem 1, every value that line L9 returns is a $k$-path. If $G$ has none, every call returns NONE, and line L10 returns NONE.

Part 2. Fix a $k$-path $P$ of $G$. Trial $j$ draws a coloring $c_j$ independently of the other trials. By Lemma 4, $P$ is colorful under $c_j$ with probability $p = k!/k^k$. If $P$ is colorful under $c_j$, then by Theorem 1 the call at L9 returns a $k$-path (perhaps another one), and K-PATH stops with it. So K-PATH returns NONE only if $P$ is colorful under none of $c_1, \ldots, c_t$, an event of probability $(1 - p)^t$ by independence. Since $1 - p \le e^{-p}$, this is at most $e^{-pt}$.

Part 3. With $t \ge \ln(1/\delta) / p$, we get $e^{-pt} \le e^{-\ln(1/\delta)} = \delta$. $\square$

**Theorem 3 (running time and space).** One call of COLORFUL-PATH runs in $O(2^k m + n)$ time on a word RAM where a set $S \subseteq \{1, \ldots, k\}$ fits in one word, and K-PATH with $t$ trials runs in $O(t (2^k m + n))$ time. With $t = \lceil \ln(1/\delta) k^k/k! \rceil$, this is $O((2e)^k (n + m) \log(1/\delta))$. The space is $O(2^k n + m)$.

*Proof.* Keep $D[v, \cdot]$ as an array of $2^k$ cells per vertex, or as a hash table; each lookup and update is $O(1)$. By Lemma 2, an entry $D[u, S]$ is set at most once, and only when $c(u) \in S$, since a colorful walk ending at $u$ uses the color $c(u)$. So for each $u$ at most $2^{k-1}$ entries exist, and each is processed once at L3, in a later round than the one that set it. Processing $(u, S)$ scans the $\deg(u)$ neighbors of $u$ with $O(1)$ work each: a bit test, a union and a lookup. The total work at L3 and L4 is at most $\sum_u 2^{k-1} \deg(u)$, which is $2^{k-1} \cdot 2m = 2^k m$ for an undirected graph and $2^{k-1} m$ for a directed one. Line L1 takes $O(n)$, the scan for a full entry at L5 takes $O(n)$, and the trace back takes $O(k)$ steps by Lemma 3, with $k \le n$ whenever a $k$-path exists. So one call is $O(2^k m + n)$.

K-PATH draws a coloring in $O(n)$ time and calls COLORFUL-PATH at most $t$ times, so its time is $O(t (2^k m + n))$. By Lemma 4, $k^k / k! < e^k$, so $t \le \ln(1/\delta) e^k + 1$, and the time is $O(e^k 2^k (n + m) \log(1/\delta))$, which is $O((2e)^k (n + m) \log(1/\delta))$.

Only one table is alive at a time. It has at most $2^{k-1}$ entries per vertex, so the space is $O(2^k n)$ for the table and $O(n + m)$ for the graph and the coloring. $\square$

**Lemma 5 (the counting form).** Define $N[v, \{c(v)\}] = 1$ for each $v$, and let round $i$ add $N[u, S]$ to $N[v, S \cup \{c(v)\}]$ for each $(u, S)$ with $|S| = i$ and each neighbor $v$ of $u$ with $c(v) \notin S$. Then $N[v, S]$ is the number of colorful walks that end at $v$ with the color set $S$. So $\sum_v N[v, \{1, \ldots, k\}]$ is the number of colorful $k$-paths, counted as vertex sequences.

*Proof.* By induction on $|S|$, as in Lemma 2. For $|S| = 1$, the only such walk is $(v)$. For $|S| = i + 1$ with $c(v) \in S$, let $S' = S \setminus \{c(v)\}$. The map that removes the last vertex is a bijection from the colorful walks that end at $v$ with color set $S$ onto the colorful walks with color set $S'$ that end at some vertex $u$ with $v$ a neighbor of $u$. It is injective because a walk is its prefix plus $v$, and it is onto because appending $v$ to such a walk gives a colorful walk with color set $S$, as $c(v) \notin S'$. Round $i$ adds $N[u, S']$ to $N[v, S]$ once for each such $u$, so by induction $N[v, S]$ is the number of these prefixes, which is the number of walks. If $c(v) \notin S$, no walk ends at $v$ with color set $S$, and $N[v, S]$ stays 0. By Lemma 1 the colorful walks are paths. $\square$

In an undirected graph with $k \ge 2$, a $k$-path and its reverse are different sequences with the same colors, so each path is counted twice. The tests of this page compare $\sum_v N[v, \{1, \ldots, k\}]$ with a brute-force count of the colorful vertex sequences on random small graphs.
