---
title: DIANA returns n - 1 proper splits with heights that never increase
proves: [correctness]
status: full
---

Let $D$ be an $n \times n$ symmetric matrix with a zero diagonal and nonnegative values, and $\text{diam}(C) = \max_{i, j \in C} D(i, j)$, with $\text{diam}(\{i\}) = 0$.

**Lemma 1 (SPLINTER).** For a cluster $C$ with $m \ge 2$ points, SPLINTER$(D, C)$ ends after at most $m - 2$ moves and returns $S$, $R$ with $S \cup R = C$, $S \cap R = \emptyset$, $S \ne \emptyset$ and $R \ne \emptyset$. Each point $y$ that moves has $g(y) > 0$ at its move: its mean dissimilarity to the other points of $R$ exceeds its mean dissimilarity to $S$.

*Proof.* Line L9 makes $S = \{x\}$ and $R = C - \{x\}$, a partition of $C$ with $|S| = 1$ and $|R| = m - 1 \ge 1$. Line L14 moves one point from $R$ to $S$, which keeps a partition of $C$ and keeps $S$ nonempty. The loop of line L10 runs only while $|R| \ge 2$, so after a move $|R| \ge 1$. Each move lowers $|R|$ by one, so there are at most $m - 2$ moves, and the loop ends. In line L11, the mean over $R - \{i\}$ is defined because $|R| \ge 2$, and the mean over $S$ because $S \ne \emptyset$. Line L13 stops before any move with $g(y) \le 0$. $\square$

**Running sums.** Keep $\sigma_R(i) = \sum_{j \in R} D(i, j)$ and $\sigma_S(i) = \sum_{j \in S} D(i, j)$ for each $i \in C$. Since $D(i, i) = 0$, for $i \in R$ the mean over $R - \{i\}$ is $\sigma_R(i)/(|R| - 1)$, so $g(i) = \sigma_R(i)/(|R| - 1) - \sigma_S(i)/|S|$. A move of $y$ subtracts $D(i, y)$ from $\sigma_R(i)$ and adds it to $\sigma_S(i)$ for each $i$, which keeps both sums right. So line L11 costs $O(|R|)$ and each move costs $O(m)$.

**Lemma 2 (monotone diameters).** If $A \subseteq B$, then $\text{diam}(A) \le \text{diam}(B)$.

*Proof.* The maximum for $A$ is over a subset of the pairs for $B$. $\square$

**Theorem.** DIANA$(D)$ makes exactly $n - 1$ splits. The current clusters always form a partition of the points, and at the end each cluster is one point. The split heights $h_1, h_2, \ldots, h_{n-1}$, in the order made, satisfy $h_1 \ge h_2 \ge \cdots \ge h_{n-1}$. Each split cluster has height at most that of the split that made it. So the splits, read in reverse, are the merges of a monotone dendrogram.

*Proof.* At line L1 the single cluster is a partition. In each round, line L2 finds a cluster with two or more points, and line L3 chooses, among the clusters with two or more points, one with the largest diameter. A single point has diameter 0, so this is also a largest diameter over all clusters. By Lemma 1, line L5 replaces $C$ by two nonempty disjoint parts whose union is $C$, so the clusters stay a partition, and their number grows by one. The loop stops when each cluster has one point, which is when there are $n$ clusters, so after exactly $n - 1$ rounds.

*Heights.* Let $\Delta_t$ be the largest diameter among the clusters at the start of round $t$, so $h_t = \Delta_t$. The new parts $S$ and $R$ of round $t$ are subsets of $C$, so by Lemma 2 their diameters are at most $\text{diam}(C) = h_t$. The other clusters have diameters at most $\Delta_t = h_t$. So $\Delta_{t+1} \le h_t$, and $h_{t+1} \le h_t$. In particular, a part of $C$ is split later at a height at most $h_t$.

*The dendrogram.* Read the splits from the last to the first. The last split joins two single points, and each earlier split $(S, R)$ joins two clusters that are, at that time in the reverse order, both current: they were made by the split and are split only later. So the reverse list is a valid list of $n - 1$ merges, with heights $h_{n-1} \le \cdots \le h_1$ that never decrease. $\square$

**Running time.** Line L3 computes the diameters of the current clusters, $O(n^2)$ time in total per round, since the clusters are disjoint. By the running sums, SPLINTER on $m$ points takes $O(m^2)$ for the start and $O(m)$ per move, so $O(m^2)$ in all. With $n - 1$ rounds and $m \le n$, the total is $O(n^3)$. The memory beyond the matrix is $O(n)$ for the sums and the clusters.

**The exact best split.** A cluster of $m$ points has $2^{m-1} - 1$ splits into two nonempty parts: each of the $2^m$ subsets $S$ gives the split $\{S, C - S\}$, each split arises from two subsets, and the two subsets $\emptyset$ and $C$ give no split. So a method that tries all splits takes time exponential in $m$, and SPLINTER, which takes $O(m^2)$ time, is a heuristic for any such criterion.
