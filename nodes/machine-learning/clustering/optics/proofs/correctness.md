---
title: OPTICS computes a greedy reachability ordering, and ExtractDBSCAN recovers DBSCAN up to border points
proves: [correctness]
status: full
---

We use the pseudocode of the page, with a generating distance $\varepsilon$ and an integer $\mathit{MinPts} \ge 1$. UNDEFINED is $\infty$. For points $o, p$ let

$$r(o, p) = \begin{cases} \max(\mathrm{core}(o), \mathrm{dist}(o, p)) & \text{if } \mathrm{core}(o) < \infty \text{ and } \mathrm{dist}(o, p) \le \varepsilon, \\ \infty & \text{otherwise,} \end{cases}$$

the reachability distance of $p$ with respect to $o$ (Definition 6 of the paper). Here $\mathrm{core}(o)$ is the distance from $o$ to its $\mathit{MinPts}$-th nearest point, $o$ itself counted, if $|N_\varepsilon(o)| \ge \mathit{MinPts}$, and $\infty$ otherwise (Definition 5). The output order is $o_1, \ldots, o_n$, and $\mathrm{reach}(o_i)$ is the value of reach$[o_i]$ at the end.

**Lemma 1 (the invariant).** At each moment, for each unprocessed point $u$, reach$[u] = \min_{p \text{ processed}} r(p, u)$ (the minimum of an empty set is $\infty$), and the seed list holds exactly the unprocessed points with a finite reach$[u]$, each with its current value.

*Proof.* At the start no point is processed and each reach$[u] = \infty$. A point $p$ becomes processed in line L4 or line L10, and its core distance is set from $N_\varepsilon(p)$, which is the definition. For $u \notin N_\varepsilon(p)$ or for a non-core $p$, $r(p, u) = \infty$, so the minimum over the processed points does not change, and UPDATE is not called or does not touch $u$. For an unprocessed $u \in N_\varepsilon(p)$ and a core $p$, lines L13 and L14 compute $r(p, u)$ and replace reach$[u]$ by it if it is smaller, so reach$[u]$ becomes the new minimum. A point enters the seed list when its reach becomes finite, and it leaves only when it becomes processed (with lazy deletion, the stale entries of a point do not count: the valid entry is the one with the current value). $\square$

**Lemma 2 (the greedy order).** $\mathrm{reach}(o_i) = \min_{j < i} r(o_j, o_i)$, and when $o_i$ is chosen, $\mathrm{reach}(o_i) \le \min_{j < i} r(o_j, u)$ for each point $u$ that comes after $o_i$.

*Proof.* UPDATE never changes the reach of a processed point, so $\mathrm{reach}(o_i)$ is the value of reach$[o_i]$ when $o_i$ is chosen, and Lemma 1 gives the first statement. If $o_i$ is chosen in line L9, it is the seed with the smallest reach, and by Lemma 1 the unprocessed points outside the seed list have reach $\infty$. If $o_i$ is chosen in line L1, the seed list is empty, so each unprocessed point has reach $\infty$, and so does $o_i$. $\square$

**Lemma 3.** Fix $\varepsilon' \le \varepsilon$ and call a point *$\varepsilon'$-core* if $\mathrm{core}(p) \le \varepsilon'$. This holds if and only if $|N_{\varepsilon'}(p)| \ge \mathit{MinPts}$, which is the DBSCAN core test at $\varepsilon'$. Also $r(o, p) \le \varepsilon'$ if and only if $o$ is $\varepsilon'$-core and $\mathrm{dist}(o, p) \le \varepsilon'$.

*Proof.* The $\mathit{MinPts}$-th smallest distance from $p$ is at most $\varepsilon'$ if and only if at least $\mathit{MinPts}$ points lie within $\varepsilon'$; such points lie within $\varepsilon$ too, so the core distance is finite. For the second statement, $r(o, p) = \max(\mathrm{core}(o), \mathrm{dist}(o, p))$ when finite, and a maximum is at most $\varepsilon'$ if and only if both terms are. $\square$

**Theorem (ExtractDBSCAN).** Let $\varepsilon' \le \varepsilon$, and run EXTRACT-DBSCAN on the order. Let $G'$ be the graph on the $\varepsilon'$-core points with an edge between two of them at distance at most $\varepsilon'$. Then:

1. a point has a cluster label if it is $\varepsilon'$-core, and two $\varepsilon'$-core points have the same label if and only if they lie in the same component of $G'$;
2. each DBSCAN noise point at $(\varepsilon', \mathit{MinPts})$ gets NOISE;
3. a non-core point with a cluster label lies within $\varepsilon'$ of an $\varepsilon'$-core point with the same label;
4. a non-core point within $\varepsilon'$ of an $\varepsilon'$-core point gets NOISE if and only if all such core points come after it in the order.

*Proof.* Call index $i$ a *break* if $\mathrm{reach}(o_i) > \varepsilon'$. Index 1 is a break, since $\mathrm{reach}(o_1) = \infty$.

*Claim A.* If $i$ is a break and $k > i$ has $\mathrm{reach}(o_k) \le \varepsilon'$, then some $j$ with $i \le j < k$ has $o_j$ $\varepsilon'$-core and $\mathrm{dist}(o_j, o_k) \le \varepsilon'$. Indeed, by Lemma 2, $\min_{j < i} r(o_j, o_k) \ge \mathrm{reach}(o_i) > \varepsilon'$, and $\mathrm{reach}(o_k) = \min_{j < k} r(o_j, o_k) \le \varepsilon'$, so the minimum is reached at some $j \ge i$, and Lemma 3 gives the rest.

*Runs.* By Claim A with $k = i + 1$, a break $i$ with a non-core $o_i$ is followed by another break or by the end, because $j = i$ is the only choice and $o_i$ is not core. So the order splits into *runs*: a break at an $\varepsilon'$-core point (lines L18 and L19 start a new label there), followed by the non-breaks up to the next break (line L21 gives them the same label), and single breaks at non-core points (line L20 gives NOISE). Lines L17 to L21 do exactly this.

*Part 1, one direction.* Take a run that starts at $s$. By Claim A, each later point $o_k$ of the run is within $\varepsilon'$ of an $\varepsilon'$-core point $o_j$ of the same run with $j < k$. By induction on $k$, each $\varepsilon'$-core point of the run is joined to $o_s$ in $G'$. So the core points of one label lie in one component. This also proves part 3.

*Part 1, other direction.* Let $p = o_i$ and $q = o_k$ be $\varepsilon'$-core and adjacent in $G'$, with $i < k$. Then $r(p, q) \le \varepsilon'$ by Lemma 3, so $\mathrm{reach}(q) \le \varepsilon'$. If some break $m$ had $i < m \le k$, then $m \ne k$, and Lemma 2 at the choice of $o_m$ would give $\mathrm{reach}(o_m) \le \min_{j < m} r(o_j, q) \le r(p, q) \le \varepsilon'$, a contradiction. So $p$ and $q$ are in the same run, and following a path in $G'$ puts each component into one run. Each $\varepsilon'$-core point is in a run with a label, because a core break starts a run and a core non-break follows a run start by the run structure. Different runs have different labels.

*Part 2.* A DBSCAN noise point $p$ is not $\varepsilon'$-core and has no $\varepsilon'$-core point within $\varepsilon'$. By Lemma 3, $r(o, p) > \varepsilon'$ for each $o$, so $p$ is a break at a non-core point, and line L20 gives NOISE.

*Part 4.* Let $p = o_k$ be a non-core point within $\varepsilon'$ of an $\varepsilon'$-core point. By Lemma 3 and Lemma 2, $\mathrm{reach}(p) \le \varepsilon'$ if and only if some such core point comes before $p$. If one does, $p$ is a non-break and gets a cluster label. If none does, $p$ is a non-core break and gets NOISE. $\square$

**Consequence.** The extraction and DBSCAN at $(\varepsilon', \mathit{MinPts})$ have the same core points, the same partition of the core points, and the same clusters except for border points: the noise of the extraction holds the DBSCAN noise and, in addition, the border points of part 4. The paper says this in its discussion of Figure 8. A post-processing step that gives each such point the label of a core point within $\varepsilon'$ removes the difference.

**Termination and cost.** Each point is processed once, either in line L4 or after it leaves the seed list in line L9, so OPTICS makes $n$ range queries. Each UPDATE call touches each neighbor once, so there are at most $\sum_p |N_\varepsilon(p)| \le n^2$ heap insertions. With brute force queries in $\mathbb{R}^d$ and a binary heap with lazy deletion, the time is $O(n^2 d + n^2 \log n)$. EXTRACT-DBSCAN is one pass over the order, $\Theta(n)$.
