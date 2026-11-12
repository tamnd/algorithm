---
title: UPGMA returns the tree of an ultrametric, and its output is always an ultrametric tree
proves: [correctness]
status: full
---

Let $X$ be a finite set of taxa and $D$ a symmetric matrix on $X$ with $D_{xx} = 0$ and $D_{xy} \ge 0$. For a rooted tree with heights, write $\mathrm{lca}(x, y)$ for the lowest common ancestor of the leaves $x$ and $y$, and $c(x, y) = 2\, h(\mathrm{lca}(x, y))$ for the *cophenetic distance* of the output. We prove two statements.

1. If $D$ is an [ultrametric](/ultrametric/), that is $D_{xz} \le \max(D_{xy}, D_{yz})$ for all $x, y, z$, then UPGMA returns a tree with $c(x, y) = D_{xy}$ for all leaves $x \ne y$ and with all edge lengths at least 0.
2. For every $D$, the heights of the merges never decrease, so all edge lengths are at least 0 and $c$ is an ultrametric.

**Fact (isosceles).** In an ultrametric, for any $x, y, z$ the largest of $D_{xy}, D_{yz}, D_{xz}$ is attained at least twice. *Proof.* Say $D_{xz}$ is a largest value. The condition for the triple in the other two orders gives $D_{xz} \le \max(D_{xy}, D_{yz})$, so one of $D_{xy}, D_{yz}$ is at least $D_{xz}$, hence equal to it. $\square$

**Proof of statement 2.** Let $A, B$ be the pair merged in some pass, at $\delta = D_{AB}$, the smallest value among the current clusters. For another cluster $K$, line L6 sets $D_{uK}$ to a weighted average of $D_{AK} \ge \delta$ and $D_{BK} \ge \delta$, so $D_{uK} \ge \delta$. The other entries do not change and were at least $\delta$. So every entry after the pass is at least $\delta$, and the next merge is at height at least $\delta / 2$. By induction the merge heights never decrease. A child of $u$ is a leaf (height 0) or a node made in an earlier pass, so $h(u)$ is at least the height of each child, and edge lengths are at least 0.

Now let $x, y, z$ be leaves and look at the two lowest common ancestors among them. In a rooted tree two of the three nodes $\mathrm{lca}(x,y), \mathrm{lca}(y,z), \mathrm{lca}(x,z)$ are equal, and the third is a descendant of them (or equal). Heights do not decrease towards the root, so the largest of the three cophenetic values is attained twice, which implies the ultrametric inequality for the triple. $\square$

**Proof of statement 1.** Let $D$ be an ultrametric. At the start of each pass, the current clusters form a partition $\mathcal{C}$ of $X$. We show that the following invariant holds at the start of every pass.

- (I1) For distinct $A, B \in \mathcal{C}$, all values $D_{ab}$ with $a \in A$, $b \in B$ are equal, and the stored entry $D_{AB}$ equals this common value.
- (I2) For each $A \in \mathcal{C}$, the subtree built for $A$ gives $c(a, a') = D_{aa'}$ for all distinct $a, a' \in A$.
- (I3) For each $A \in \mathcal{C}$, all $a, a' \in A$ and all $b \notin A$: $D_{aa'} \le 2\, h(A) \le D_{ab}$.

*Start.* All clusters are single leaves at height 0. (I1) holds because the stored entries are the input entries, (I2) has no pairs to check, and (I3) reads $0 \le 0 \le D_{ab}$.

*One pass.* Line L3 picks $A, B$ with the smallest stored entry $\delta = D_{AB}$, and line L4 makes $u$ with $h(u) = \delta / 2$.

- Edge lengths. By (I3) for $A$ with any $b \in B$, $2 h(A) \le D_{ab} = \delta$, so $h(u) - h(A) \ge 0$. The same holds for $B$.
- (I2) for $u$. Pairs inside $A$ or inside $B$ keep their lowest common ancestor. For $a \in A$ and $b \in B$ the lowest common ancestor is $u$, and $c(a, b) = \delta = D_{ab}$ by (I1).
- (I1) for $u$. Let $K$ be another cluster, and let $\alpha = D_{AK}$ and $\beta = D_{BK}$, the common values given by (I1). Take $a \in A$, $b \in B$, $k \in K$. The triple has the values $D_{ab} = \delta$, $D_{ak} = \alpha$ and $D_{bk} = \beta$, and $\delta \le \alpha$, $\delta \le \beta$ by the choice of $A, B$. If $\alpha \ne \beta$, say $\alpha < \beta$, then $\beta$ is the largest value and $\delta \le \alpha < \beta$, so it is attained once, which contradicts the Fact. So $\alpha = \beta$, and $D_{xk} = \alpha$ for all $x \in A \cup B$ and $k \in K$. Line L6 stores $(|A| \alpha + |B| \alpha) / (|A| + |B|) = \alpha$.
- (I3) for $u$. For $x, x' \in A \cup B$: if both are in $A$, $D_{xx'} \le 2h(A) \le \delta$ by (I3); the same for $B$; and if one is in each, $D_{xx'} = \delta$. So $D_{xx'} \le 2 h(u)$. For $k \notin A \cup B$, $D_{xk} = D_{uK} \ge \delta$ by the choice of the pair.
- The other clusters keep their subtrees, and the statements (I1) to (I3) that do not involve $u$ do not change.

*End.* Each pass replaces two clusters by one, so after $n - 1$ passes one cluster is left, and (I2) for it is the claim. $\blacksquare$

**Remark.** The proof of (I1) shows that, on an ultrametric, the two entries that line L6 averages are always equal. So any rule that returns a value between them, such as the equal weights of [WPGMA](/wpgma/), the minimum of [single linkage](/single-linkage-clustering/) or the maximum of [complete linkage](/complete-linkage-clustering/), gives the same tree on an ultrametric.
