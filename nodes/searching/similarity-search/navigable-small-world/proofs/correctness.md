---
title: The NSW graph stays connected, its search returns the best points it evaluates, and a full beam is exact
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. The distance $d$ is any function with $d(x, y) \ge 0$; only comparisons of its values are used. Ties between equal distances are broken by a fixed order of the points, so "nearest" and "largest distance" are well defined; the implementation compares pairs (distance, index).

**Lemma 1 (the graph).** After any sequence of insertions of $p_0, p_1, \ldots, p_{n-1}$, (I1) the graph is undirected, (I2) $p_i$ was linked at its insertion to $\min(f, i)$ distinct earlier points, and (I3) the graph is connected.

*Proof.* Induction on the number of insertions. Line L11 inserts $p_0$ with no links, and the three statements hold. Let $i \ge 1$ and assume them before $p_i$ is inserted. Line L12 calls SEARCH on the graph of $p_0, \ldots, p_{i-1}$ with $k = f$ and $ef = \max(ef_c, f) \ge f$. By Theorem 1 below, it returns the $\min(f, |V|)$ nearest of the set $V$ of the points it evaluates, all distinct and all earlier than $p_i$. The graph of the earlier points is connected by the induction hypothesis, so by Lemma 2 below $|V| \ge \min(ef, i) \ge \min(f, i)$, and the search returns $\min(f, i)$ points. Lemma 2 and Theorem 1 concern a single search on a fixed graph and do not use this lemma, so there is no circularity. Line L13 adds an undirected edge from $p_i$ to each of them, so (I1) and (I2) hold. Since $\min(f, i) \ge 1$, $p_i$ is adjacent to an earlier point, which is connected to all other earlier points by the induction hypothesis, so (I3) holds. $\square$

**Lemma 2 (the search fills its beam).** Let the graph be connected with $m \ge 1$ points, and let SEARCH run with $ef \ge 1$ and at least one entry point. Then it evaluates at least $\min(ef, m)$ points.

*Proof.* Suppose it stops having evaluated fewer than $\min(ef, m)$ points. Since every evaluated point that is not inserted into $W$ fails the test of line L9, which passes whenever $|W| < ef$, and points leave $W$ only when $|W| > ef$, the size of $W$ is the number of evaluated points as long as that number is at most $ef$. So at the end $|W| < ef$, and line L6 never stopped the loop: the loop ended with $C = \emptyset$. Every evaluated point was inserted into $C$ (in line L3, or in line L9 since $|W| < ef$ at that time) and later removed by line L5 and expanded by line L7. So every neighbor of an evaluated point is evaluated. The evaluated set contains an entry point and is closed under taking neighbors, so by connectivity it is the whole graph, and it has $m$ points, a contradiction. $\square$

**Lemma 3 (the beam holds the best seen).** At every moment of SEARCH, $W$ is the set of the $\min(ef, |V|)$ points nearest to $q$ in the set $V$ of the points evaluated so far.

*Proof.* Initially $V = W = \emptyset$. Each evaluation, in line L2 or L8, adds one point $e$ to $V$. Assume the claim before it. If $|W| < ef$, then $|W| = |V| < ef$, $W = V$, and $e$ is inserted (the test of line L9 passes, and line L3 always inserts), so $W = V \cup \{e\}$, as claimed. If $|W| = ef$, then $W$ holds the $ef$ nearest points of $V$. If $e$ is nearer than the farthest point of $W$, line L9 inserts it and removes that farthest point, which leaves the $ef$ nearest points of $V \cup \{e\}$. Otherwise $e$ is not among the $ef$ nearest of $V \cup \{e\}$, and $W$ is unchanged, as needed. Line L2 of the implementation applies the same rule, insertion followed by removal of the farthest point when $|W| > ef$, which is the same update. $\square$

**Theorem 1 (the answer).** SEARCH returns the $\min(k, |V|)$ points nearest to $q$ among the set $V$ of the points it evaluates, in order of distance, and it terminates.

*Proof.* Each point is evaluated at most once, since it is marked when evaluated and line L7 skips marked points, and each point enters $C$ at most once, when it is evaluated. So the loop of line L4 runs at most $n$ times, and each iteration scans one adjacency set. At the end, Lemma 3 gives that $W$ is the set of the $\min(ef, |V|)$ nearest points of $V$. Since $k \le ef$, the $k$ nearest points of $W$ are the $\min(k, |V|)$ nearest points of $V$, and line L10 returns them in order. $\square$

**Theorem 2 (a full beam is exact).** If the graph is connected, $ef \ge n$ and there is at least one entry point, then SEARCH evaluates all $n$ points and returns the $\min(k, n)$ nearest neighbors of $q$.

*Proof.* By Lemma 2 with $m = n$ it evaluates at least $\min(ef, n) = n$ points, so $V$ is the whole set, and Theorem 1 gives the claim. By Lemma 1, the graph built by INSERT is connected. $\blacksquare$
