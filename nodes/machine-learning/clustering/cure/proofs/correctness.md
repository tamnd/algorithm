---
title: CURE merges the closest pair under the representative distance, and its limits are single and centroid linkage
proves: [correctness]
status: full
---

CURE is a heuristic for the clustering problem: it optimizes no stated objective. This proof shows that the pseudocode of the page does what it says, gives its two limit cases, and derives the sample size rule of the paper.

Let $S$ be the points to cluster (the whole data or a sample), with $|S| = n$. For a cluster $u$ let $\mu(u)$ be its mean and $R(u)$ its set of representatives, built by lines L8 to L11, and let

$$D(u, v) = \min_{a \in R(u),\, b \in R(v)} \lVert a - b \rVert.$$

**Lemma 1 (the representatives).** Line L10 picks $\min(c, |w|)$ different points of $w$: first a point farthest from $\mu(w)$, then each time a point whose smallest distance to the points already picked is largest. Line L11 moves each picked point $p$ to $p + \alpha(\mu(w) - p)$, on the segment from $p$ to the mean, at the fraction $\alpha$ of the way.

*Proof.* This is the loop of line L10. A picked point gets the key $-1$, below every distance, so it is not picked again, and there are $\min(c, |w|)$ rounds. $\square$

**Lemma 2 (the heap holds every live pair).** At the start of each pass of line L3, for each two clusters $x \ne y$ that are alive, the heap holds an entry $(D(x, y), x, y)$. Every other entry names a cluster that is no longer alive.

*Proof.* At the start, line L2 puts all pairs of the first clusters in the heap. A cluster never changes after it is made, so a key, once computed, stays correct. When line L5 makes $w$, line L6 pushes $(D(x, w), x, w)$ for each live $x$, which covers all new pairs. The clusters $u$ and $v$ leave the live set, so their entries become stale. The outlier step removes clusters from the live set only, which also makes entries stale. Popping removes one entry: a stale one, which is skipped, or the one live pair that is merged. $\square$

**Theorem (the merge rule).** Each pass of lines L3 to L6 that merges merges a pair of live clusters $\{u, v\}$ with the smallest $D(u, v)$; among equal distances it takes the smallest pair of identifiers. The loop stops with exactly $k$ live clusters, or fewer if the outlier step removed clusters at that moment.

*Proof.* By Lemma 2 each live pair is in the heap with its exact key, so the first live pair that line L4 pops has the smallest key among the live pairs, and the heap order breaks ties by the identifiers. Stale entries are skipped, so the loop does not stop early: while two clusters are alive their pair is in the heap. Each merge lowers the number of live clusters by one. $\square$

**Corollary 1 (no shrinking and many representatives is single linkage).** If $\alpha = 0$ and $c \ge n$, then $R(u) = u$ for each cluster, so $D(u, v) = \min_{a \in u, b \in v} \lVert a - b \rVert$, which is the [single linkage](/single-linkage-clustering/) distance. CURE then performs single linkage agglomeration, and when all pairwise distances are distinct, the clusters at $k$ are the single linkage clusters at $k$.

**Corollary 2 (full shrinking is centroid linkage).** If $\alpha = 1$, every representative of $u$ is $\mu(u)$, so $D(u, v) = \lVert \mu(u) - \mu(v) \rVert$ for any $c \ge 1$. CURE then performs centroid linkage agglomeration.

**Theorem (labeling).** Line L17 gives each point $x$ of the data the index of a cluster that holds a representative nearest to $x$. This follows from the scan over all representatives, which keeps the first strict minimum.

**Sample size.** Guha et al. pick the sample size so that each cluster $u$ is likely to have at least a fraction $f$ of its points in the sample. Let the sample have $s$ points drawn uniformly with replacement, and let $X$ be the number of them in $u$. Then $\mu_X = \mathbb{E}[X] = s |u| / n$, and the Chernoff bound gives $\Pr[X < (1 - \varepsilon)\mu_X] \le e^{-\mu_X \varepsilon^2 / 2}$. Set $L = \ln(1/\delta)$ and $t = f |u|$, and require $(1 - \varepsilon)\mu_X = t$ and $\mu_X \varepsilon^2 / 2 = L$. Then $(\mu_X - t)^2 = 2 \mu_X L$, whose larger root is $\mu_X = t + L + \sqrt{L^2 + 2 t L}$. So with

$$s \ge f n + \frac{n}{|u|} \ln\frac1\delta + \frac{n}{|u|} \sqrt{\Big(\ln\frac1\delta\Big)^2 + 2 f |u| \ln\frac1\delta},$$

the sample holds at least $f |u|$ points of $u$ with probability at least $1 - \delta$. The second and third terms grow like $n / |u|$, so small clusters need large samples.

**Cost.** Lines L1 and L2 compute $n(n-1)/2$ distances and build a heap of them, $O(n^2 d)$ time and $\Theta(n^2)$ space. There are $n - k$ merges. A merge builds the representatives of $w$ in $O(|w| c d)$ time and computes $D(x, w)$ for each of the live clusters $x$ in $O(c^2 d)$ time each, with $O(\log n)$ for each push. Each pop costs $O(\log n)$, and there are at most as many pops as pushes, $O(n^2)$. The total is $O(n^2 (\log n + c^2 d))$ time, because $\sum |w| \le n^2$ over the merges and $c d \le c^2 d$.
