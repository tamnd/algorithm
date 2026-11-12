---
title: Bisecting k-means keeps a partition, never raises the SSE, and stops
proves: [correctness]
status: full
---

For a finite non-empty set $P$ of points let $\mu(P)$ be its mean and $\mathrm{SSE}(P) = \sum_{x \in P}\|x - \mu(P)\|^2$.

**Lemma 1 (the gain of a split).** If $P$ is the disjoint union of non-empty sets $A$ and $B$, then
$$\mathrm{SSE}(P) = \mathrm{SSE}(A) + \mathrm{SSE}(B) + \frac{|A||B|}{|A| + |B|}\|\mu(A) - \mu(B)\|^2 .$$
In particular $\mathrm{SSE}(A) + \mathrm{SSE}(B) \le \mathrm{SSE}(P)$.

*Proof.* By the centroid identity, $\sum_{x \in A}\|x - \mu(P)\|^2 = \mathrm{SSE}(A) + |A|\|\mu(A) - \mu(P)\|^2$, and the same for $B$. Add the two and use $\mu(P) = \frac{|A|\mu(A) + |B|\mu(B)}{|A| + |B|}$. Then $\mu(A) - \mu(P) = \frac{|B|}{|A| + |B|}(\mu(A) - \mu(B))$ and $\mu(B) - \mu(P) = \frac{|A|}{|A| + |B|}(\mu(B) - \mu(A))$, so
$$|A|\|\mu(A) - \mu(P)\|^2 + |B|\|\mu(B) - \mu(P)\|^2 = \frac{|A||B|^2 + |B||A|^2}{(|A| + |B|)^2}\|\mu(A) - \mu(B)\|^2 = \frac{|A||B|}{|A| + |B|}\|\mu(A) - \mu(B)\|^2 . \qquad \square$$

**Lemma 2 (a 2-means run).** If $P$ has at least two distinct points, a run of line L5 stops and returns two non-empty sets $A$ and $B$ with $A \cup B = P$, $A \cap B = \emptyset$, such that each point of $A$ is at least as near to $\mu(A)$ as to $\mu(B)$, and each point of $B$ the other way round.

*Proof.* The run is Lloyd's algorithm on $P$ with $k = 2$ and two distinct initial centers, so it stops at a fixed point by the correctness of [k-means](/k-means/). The first assignment step gives each of the two initial centers, which are points of $P$, at least that point, so both sides are non-empty after it. A side never loses all its points later. Let $A$ be a side with mean $\mu(A)$ and let $c$ be the other center. By the centroid identity, $\sum_{x \in A}\|x - c\|^2 = \sum_{x \in A}\|x - \mu(A)\|^2 + |A|\|\mu(A) - c\|^2 \ge \sum_{x \in A}\|x - \mu(A)\|^2$, so at least one point of $A$ is at least as near to $\mu(A)$ as to $c$, and the tie rule keeps it in $A$. At the fixed point each point is at a nearest center and the centers are the means. $\square$

**Theorem.** The loop of lines L2 to L7 stops. Before each test of line L2, $L$ is a partition of the points into non-empty clusters, and the total SSE is at most its value before the previous pass.

*Proof.* At the start $L$ has one cluster, all the points. Suppose that $L$ is a partition into non-empty clusters. Line L7 replaces a cluster $P$ by two non-empty disjoint sets with union $P$ (Lemma 2), so $L$ stays a partition into non-empty clusters, with one more cluster. By Lemma 1 the total SSE does not rise. Each pass that splits adds a cluster, and a partition of $n$ points has at most $n$ non-empty clusters, so at most $\min(k, n) - 1$ passes split. A pass that cannot split its cluster (all its points coincide) marks it, and a marked cluster is not chosen again; when every cluster is marked, the loop stops. There are finitely many clusters to mark, so the loop stops. $\square$

**Remark (not a global fixed point).** A point is compared only with the two centers of its own split. In the final partition it can be nearer to the center of another cluster, so the result need not be a fixed point of Lloyd's algorithm on all points.
