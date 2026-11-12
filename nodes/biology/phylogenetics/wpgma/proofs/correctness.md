---
title: WPGMA returns the tree of an ultrametric, and its output is always an ultrametric tree
proves: [correctness]
status: full
---

Let $D$ be a symmetric matrix on the taxa $X$ with zero diagonal and entries at least 0, and write $c(x, y) = 2\, h(\mathrm{lca}(x, y))$ for the distance that the output tree gives to two leaves. We prove: (1) the merge heights never decrease, so the edge lengths are at least 0 and $c$ is an ultrametric; (2) if $D$ is an [ultrametric](/ultrametric/), then $c = D$.

**Statement 1.** Let $A, B$ be merged at $\delta = D_{AB}$, the smallest current entry. Line L5 sets $D_{uK} = (D_{AK} + D_{BK}) / 2$, and both terms are at least $\delta$, so $D_{uK} \ge \delta$. The other entries do not change and were at least $\delta$. So the next merge height is at least $\delta / 2$, and by induction the heights never decrease. Each child of $u$ is a leaf at height 0 or an earlier node, so each edge has length at least 0. For three leaves, two of the three lowest common ancestors coincide and the third is below them, so the largest of the three values of $c$ is attained twice; this is the ultrametric inequality. $\square$

**Statement 2.** In an ultrametric, the largest of $D_{xy}, D_{yz}, D_{xz}$ is attained at least twice: if $D_{xz}$ is a largest value, the condition $D_{xz} \le \max(D_{xy}, D_{yz})$ makes one of the other two equal to it.

We show that the following holds at the start of every pass, for the current partition $\mathcal{C}$ of $X$ into clusters.

- (I1) For distinct $A, B \in \mathcal{C}$, $D_{ab}$ is the same for all $a \in A$, $b \in B$, and the stored entry $D_{AB}$ equals it.
- (I2) For each $A \in \mathcal{C}$, $c(a, a') = D_{aa'}$ for all distinct $a, a' \in A$.
- (I3) For each $A \in \mathcal{C}$, all $a, a' \in A$ and $b \notin A$: $D_{aa'} \le 2\, h(A) \le D_{ab}$.

At the start all clusters are single leaves at height 0, and the three statements hold, the last as $0 \le 0 \le D_{ab}$.

In a pass, line L3 picks $A, B$ with the smallest stored entry $\delta$, and $h(u) = \delta / 2$. By (I3), $2 h(A) \le \delta$ and $2 h(B) \le \delta$, so the two new edges have length at least 0. For $a \in A$ and $b \in B$, $c(a, b) = 2 h(u) = \delta = D_{ab}$ by (I1), and the other pairs inside $A \cup B$ keep their lowest common ancestor, so (I2) holds for $u$. Let $K$ be another cluster, with common values $\alpha = D_{AK}$ and $\beta = D_{BK}$. For $a \in A$, $b \in B$, $k \in K$ the triple has values $\delta \le \alpha$ and $\delta \le \beta$, by the choice of the pair. If $\alpha < \beta$, then $\beta$ is a largest value attained once, which is impossible; the case $\beta < \alpha$ is the same. So $\alpha = \beta$, all distances from $A \cup B$ to $K$ equal $\alpha$, and line L5 stores $(\alpha + \alpha)/2 = \alpha$. This is (I1) for $u$. For (I3), two leaves of $A \cup B$ are at distance at most $\delta$ (by (I3) for $A$ and for $B$, and by (I1) across), and a leaf of $A \cup B$ is at distance $D_{uK} \ge \delta$ from each leaf of another cluster $K$. Statements that do not involve $u$ do not change.

Each pass removes one cluster, so after $n - 1$ passes one cluster is left, and (I2) for it says $c = D$. $\blacksquare$
