---
title: The BFR summaries are exact and each point is counted exactly once
proves: [correctness]
status: full
---

We use the pseudocode of the page. The points are vectors in $\mathbb{R}^d$. For a finite set $P$ of points, its summary is $\Sigma(P) = (N, \mathrm{SUM}, \mathrm{SUMSQ})$ with $N = |P|$, $\mathrm{SUM}_i = \sum_{x \in P} x_i$ and $\mathrm{SUMSQ}_i = \sum_{x \in P} x_i^2$ for $i = 1, \ldots, d$. BFR does not promise a good clustering: its decisions rest on the assumption that each cluster is close to a Gaussian with axis-aligned axes. What we prove is that the bookkeeping is exact, so the statistics that BFR uses are the true statistics of the points it has assigned.

**Lemma 1 (additivity).** If $P$ and $Q$ are disjoint, then $\Sigma(P \cup Q) = \Sigma(P) + \Sigma(Q)$, added in each component.

*Proof.* Each component is a sum over the points, and a sum over a disjoint union is the sum of the two sums. $\square$

Adding one point $x$ to a summary is the case $Q = \{x\}$, so lines L4 and L5 and the merges of lines L7 and L8 all keep the summaries exact.

**Lemma 2 (statistics from a summary).** The centroid of $P$ is $\mu_i = \mathrm{SUM}_i / N$, and the variance of $P$ in dimension $i$ is $\sigma_i^2 = \mathrm{SUMSQ}_i / N - (\mathrm{SUM}_i / N)^2$.

*Proof.* The first formula is the definition of the mean. For the second,
$$\frac{1}{N} \sum_{x \in P} (x_i - \mu_i)^2 = \frac{1}{N} \sum_{x \in P} x_i^2 - 2\mu_i \frac{1}{N}\sum_{x \in P} x_i + \mu_i^2 = \frac{\mathrm{SUMSQ}_i}{N} - \mu_i^2. \qquad \square$$

So the squared Mahalanobis distance $\sum_i (x_i - \mu_i)^2 / \sigma_i^2$ of line L3 is computed from the summary alone. It is the distance for a Gaussian with mean $\mu$ and the diagonal covariance $\mathrm{diag}(\sigma_1^2, \ldots, \sigma_d^2)$. The implementation replaces a variance below a small floor $\varphi > 0$ by $\varphi$, so that a cluster with zero spread in some dimension does not cause a division by zero.

**Invariant.** After the first chunk and after each later chunk, the points read so far are partitioned among the summaries of DS, CS and RS, and each summary is $\Sigma$ of its own part. Each CS summary has $N \ge 2$ and each RS summary has $N = 1$.

*Proof.* Line L1 partitions the first chunk into the $k$ clusters of k-means and builds one summary for each; empty clusters give no summary. In a later chunk, each point $x$ goes to exactly one place: to one DS summary at line L4, or to one CS summary at line L5, or into a new RS summary at line L6. By Lemma 1 the summary that receives $x$ stays exact. Line L7 only merges summaries of disjoint parts, which by Lemma 1 gives the summary of the union, and then sorts the results by $N$ into CS and RS. So no point is lost or counted twice. $\square$

**Theorem.** At the end, the DS summaries are the summaries of a partition of all $n$ points into at most $k$ clusters, so their counts add up to $n$, and their centroids and variances are the true centroids and variances of these clusters.

*Proof.* By the invariant, before line L8 the summaries of DS, CS and RS are exact and partition the points. Line L8 merges each CS and RS summary into one DS summary, which by Lemma 1 is the summary of the union. Lemma 2 gives the centroids and variances. $\blacksquare$

**Termination.** Each chunk is read once. In line L7 each merge lowers the number of summaries by one, so there are fewer merges than summaries.

**What is not proved.** A point that BFR puts into a DS cluster is never moved again, even if later data shows that another cluster fits it better. So the final clusters can differ from a k-means local optimum on all the data, and they can be poor if the clusters are not close to axis-aligned Gaussians or if the first chunk is not typical of the data.
