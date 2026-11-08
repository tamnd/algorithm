---
title: For points in general position, the randomized beneath-beyond method takes O(n log n) expected time
proves: [time.expected, space.expected]
status: full
---

**Claim.** Let $P \subset \mathbb{R}^3$ be a set of $n \ge 4$ points in general position (no three on a line, no four on a plane). Over the random order of line L1, the expected running time of BENEATH-BEYOND is $O(n \log n)$ on the real RAM, and after each step the expected total size of the conflict lists is $O(n)$.

**Setup.** By general position, the first four points of the order are not on one plane, so the algorithm inserts the points in the uniformly random order $p_1, \ldots, p_n$ of line L1. Let $P_r = \{p_1, \ldots, p_r\}$. For each $r$, the set $P_r$ is a uniformly random $r$-subset of $P$, and given $P_r$, the point $p_r$ is uniform in $P_r$. The facts (F1) and (F2) and Lemmas 1 and 2 are those of the correctness proof.

**Configurations.** A *configuration* $\sigma$ has a defining set $D(\sigma) \subseteq P$ and a killing set $K(\sigma) \subseteq P \setminus D(\sigma)$. It is *active* over $R \subseteq P$ if $D(\sigma) \subseteq R$ and $K(\sigma) \cap R = \emptyset$. We use two kinds.

- *Facet configurations*: an oriented triangle $(x, y, z)$ of points of $P$, with $D = \{x, y, z\}$ and $K$ the points beyond it. By (F1), for $|R| \ge 4$ the active ones over $R$ are the facets of $\mathrm{conv}(R)$ with their outward orientations, and their number is at most $2|R| - 4$ by [Euler's formula](/euler-formula/).
- *Edge configurations*: a tuple $(u, v, w, z)$ such that $f = (u, v, w)$ and $g = (v, u, z)$ have $z$ beneath $f$ and $w$ beneath $g$, with $D = \{u, v, w, z\}$ and $K$ the points beyond $f$ or beyond $g$. If one is active over $R$, then $f$ and $g$ are facets of $\mathrm{conv}(R)$ by (F1) and share the directed edges $(u, v)$ and $(v, u)$. Each directed edge of $\mathrm{conv}(R)$ gives at most one active edge configuration, so their number is at most $2(3|R| - 6) < 6|R|$.

In both kinds $|D(\sigma)| = d$ with $d = 3$ or $d = 4$, and for every $R$ the number of active configurations is at most $c|R|$, with $c = 2$ or $c = 6$. For $|R| < d$ there are none.

**Lemma 3 (created configurations).** For a kind with these constants, let $\Gamma$ be the set of configurations that are active over $P_r$ for some $r \ge 4$. Then

$$\mathbb{E}\Big[\sum_{\sigma \in \Gamma} 1\Big] \le c\, d\, n \quad\text{and}\quad \mathbb{E}\Big[\sum_{\sigma \in \Gamma} |K(\sigma)|\Big] \le 2^{d+1} c\, d \, n H_n,$$

where $H_n = 1 + 1/2 + \cdots + 1/n$ is the [harmonic number](/harmonic-series/).

*Proof.* For $\sigma \in \Gamma$, let $j(\sigma)$ be the step at which the last point of $D(\sigma)$ arrives, or $4$ if this is smaller than $4$. If $\sigma$ is active over $P_r$, then $r \ge j(\sigma)$ and $\sigma$ is active over the smaller set $P_{j(\sigma)}$ too. So each $\sigma \in \Gamma$ is counted exactly once in the sums below, at $r = j(\sigma)$: it is active over $P_r$ and, for $r \ge 5$, $p_r \in D(\sigma)$. For $r = 4$ all points of $D$ are in $P_4$.

*Backwards step.* Fix $r \ge 5$ and condition on $P_r = R$. Then $p_r$ is uniform in $R$, so each active $\sigma$ over $R$ has $p_r \in D(\sigma)$ with probability $d / r$. Write $A(R)$ for the number of active configurations over $R$ and $W(R) = \sum |K(\sigma)|$ over the active ones. Then

$$\mathbb{E}\Big[\sum_{\sigma \in \Gamma} 1\Big] \le A(P_4) + \sum_{r=5}^{n} \frac{d}{r} \mathbb{E}[A(P_r)] \le 4c + \sum_{r=5}^{n} d c \le c\, d\, n,$$

and in the same way $\mathbb{E}[\sum_\Gamma |K|] \le \mathbb{E}[W(P_4)] + \sum_{r=5}^{n} \frac{d}{r} \mathbb{E}[W(P_r)]$.

*The size of the killing sets.* Fix $r < n$. Let $R' = P_{r+1}$ and $q = p_{r+1}$, so that $P_r = R' \setminus \{q\}$, the set $R'$ is a uniform $(r+1)$-subset and $q$ is uniform in $R'$ given $R'$. For a fixed set $R$, $W(R) = \sum_{x \notin R} |\{\sigma \text{ active over } R : x \in K(\sigma)\}|$, and $(P_r, p_{r+1})$ is a uniform pair of an $r$-subset and an outside point. So

$$\mathbb{E}[W(P_r)] = (n - r)\, \mathbb{E}\big[\,|\{\sigma : D(\sigma) \subseteq R',\ K(\sigma) \cap R' = \{q\}\}|\,\big] = (n - r)\, \frac{\mathbb{E}[A_1(R')]}{r + 1},$$

where $A_1(R')$ is the number of configurations with $D(\sigma) \subseteq R'$ and $|K(\sigma) \cap R'| = 1$. The second step averages over $q \in R'$: each configuration counted by $A_1(R')$ is counted for exactly one $q$.

*Sampling.* Fix a set $R'$ of size $s$ and let $Q \subseteq R'$ contain each point independently with probability $1/2$. A configuration counted by $A_1(R')$, with killing point $x \in R'$, is active over $Q$ when $D(\sigma) \subseteq Q$ and $x \notin Q$, which has probability $2^{-(d+1)}$. So $2^{-(d+1)} A_1(R') \le \mathbb{E}[A(Q)] \le c\, \mathbb{E}|Q| = c s / 2$, and $A_1(R') \le 2^d c\, s$.

So $\mathbb{E}[W(P_r)] \le 2^d c (n - r)$ for $r < n$, and $W(P_n) = 0$. Then

$$\mathbb{E}\Big[\sum_{\sigma \in \Gamma} |K(\sigma)|\Big] \le 2^d c\, n + \sum_{r=5}^{n} \frac{d}{r}\, 2^d c\, n \le 2^{d+1} c\, d\, n H_n. \qquad \square$$

**The cost of the algorithm.** Charge the work of each step as follows.

1. *Lines L2 to L4.* Line L2 is $O(n)$ under general position (four points), line L3 is $O(1)$ and line L4 is $O(n)$.
2. *Lines L6 to L8 and the deletion of facets in line L12.* $O(1 + |V|)$ per step. Each facet in $V$ is deleted then and was created once, so the total is $O(n)$ plus the number of created facets. Each created facet is a facet configuration in $\Gamma$, so by Lemma 3 its expected number is at most $6n$.
3. *Line L11.* At step $r$, a horizon edge $(u, v)$ with facets $f = (u, v, w) \in V$ and $g = (v, u, z) \notin V$ is an edge configuration $\sigma = (u, v, w, z)$ that is active over $P_{r-1}$. The work for it is $O(1 + |C(f)| + |C(g)|) = O(1 + |K(\sigma)|)$, since both lists hold points beyond $f$ or $g$. After the step, $p_r \in K(\sigma)$, so $\sigma$ is not active over any later $P_j$, and each $\sigma$ is charged at most once. Each charged $\sigma$ is in $\Gamma$, so by Lemma 3 with $d = 4$ and $c = 6$ the expected total is $O(n) + 2^5 \cdot 24\, n H_n = O(n \log n)$.
4. *Line L10 and the conflict pairs.* Line L10 is $O(1)$ per created facet. Each conflict pair is added once, in line L4 or line L11, and removed at most once, in line L12. The pairs added in line L11 are at most the work of line L11.

Summing, the expected time is $O(n \log n)$, since $H_n \le 1 + \ln n$.

**Space.** After step $r$, the conflict lists hold exactly the pairs $(x, t)$ with $t$ a facet of $\mathrm{conv}(P_r)$ and $x \notin P_r$ beyond $t$. Their number is $W(P_r)$ for facet configurations, and its expectation is at most $2^3 \cdot 2\, (n - r) = 16 (n - r)$ by the computation above. The hull has at most $2r - 4$ facets and the edge map at most $6r$ entries. So the expected size of the data structure after each step is $O(n)$. $\blacksquare$
