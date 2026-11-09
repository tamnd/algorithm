---
title: The SPEA archive is non-dominated, has at most M members, and without clustering equals the front of all points seen
proves: [correctness]
status: full
---

All objectives are minimized, $N$ is the population size, $M$ is the bound on the archive, and line numbers refer to the `pseudo id=main` block of the SPEA page. We write $a \preceq b$ when $a$ weakly dominates $b$, that is $a_m \le b_m$ for every objective $m$; Zitzler and Thiele say that $a$ covers $b$. SPEA is a heuristic; the statements below are about its archive and its fitness, not about reaching the Pareto front of a problem.

## The archive

**Lemma 1.** After line L4, no member of $A$ dominates another and no two members have the same image. After line L5, $\lvert A \rvert \le M$, and $A$ still has both properties.

*Proof.* Line L4 keeps a candidate only when no candidate dominates it and no kept member has its image, so no kept member dominates another and the images are distinct. Line L5 returns one member of each of $M$ clusters when $\lvert A \rvert > M$ (Lemma 4), so a subset of size $M$; a subset keeps both properties. $\square$

**Theorem 2.** Let $S_t$ be the set of images of all members of $P$ that lines L3 to L5 have seen up to generation $t$. If line L5 never cuts the archive, then after line L4 of generation $t$ the set of images of $A$ is exactly the set of non-dominated images of $S_t$.

*Proof.* By induction on $t$. Write $\mathrm{ND}(S)$ for the non-dominated images of $S$, and $C$ for the candidates of line L4: the old archive and the non-dominated members of the current $P$. Every image of $C$ is in $S_t$.

Let $y \in \mathrm{ND}(S_t)$. If $y$ is an image of the current $P$, then no member of $P$ dominates it, so $y$ is in $C$. Otherwise $y \in S_{t-1}$ and no point of $S_{t-1}$ dominates it, so $y$ is an image of the old archive by the hypothesis, and again in $C$. No member of $C$ dominates $y$, since $C \subseteq S_t$. So line L4 keeps one member with image $y$.

Let $c$ be kept, and assume a point $z \in S_t$ dominates $c$. $S_t$ is finite, so some $w \in \mathrm{ND}(S_t)$ has $w \preceq z$, and then $w$ dominates $c$. By the first part $w$ is in $C$, so line L4 would not keep $c$. So $c \in \mathrm{ND}(S_t)$. $\square$

When line L5 cuts the archive, Theorem 2 can fail: a removed point $u$ no longer blocks a later point $v$ that $u$ dominates, so $A$ can hold $v$. The bounded archive is then not a subset of the front of the points seen.

## Strength and fitness

**Lemma 3.** For each $a \in A$, $0 \le s(a) \le N/(N + 1) < 1$. For each $x \in P$, $F(x) \ge 1$. If $x, x' \in P$ and $f(x) \preceq f(x')$, then $F(x) \le F(x')$.

*Proof.* $a$ covers at most the $N$ members of $P$, which gives the bounds on $s$. $F(x) = 1 + \sum s(a)$ with all terms nonnegative. If $a \preceq f(x)$ and $f(x) \preceq f(x')$, then $a \preceq f(x')$, because $\preceq$ is transitive. So each term of the sum for $x$ is also a term of the sum for $x'$. $\square$

So in the tournament of line L8, every member of the archive beats every member of the population. The order of Lemma 3 is weak: a member can dominate another and still get the same fitness, as the example of the SPEA page shows.

## Clustering

Average linkage starts with one cluster per member and merges the two clusters with the smallest average distance $d(U, V) = \frac{1}{\lvert U \rvert \lvert V \rvert} \sum_{u \in U, v \in V} \lVert u - v \rVert$ until $M$ clusters are left. Then each cluster gives the member with the smallest sum of distances to the other members of its cluster.

**Lemma 4.** If $\lvert A \rvert = k > M$, line L5 stops after $k - M$ merges and returns exactly $M$ members, one from each cluster. The update $d(U \cup V, W) = \frac{\lvert U \rvert d(U, W) + \lvert V \rvert d(V, W)}{\lvert U \rvert + \lvert V \rvert}$ gives the average distance of the merged cluster.

*Proof.* Each merge lowers the number of clusters by one, from $k$ to $M$. The clusters are disjoint and nonempty, so one member per cluster gives $M$ distinct members. For the update, the sum of the distances over $(U \cup V) \times W$ is $\lvert U \rvert \lvert W \rvert d(U, W) + \lvert V \rvert \lvert W \rvert d(V, W)$, because $U$ and $V$ are disjoint; dividing by $(\lvert U \rvert + \lvert V \rvert) \lvert W \rvert$ gives the formula. $\square$

## The output

**Lemma 5.** Line L10 returns a nonempty set of at most $M$ mutually non-dominated solutions.

*Proof.* The non-dominated members of the nonempty $P$ form a nonempty set, so the candidates of line L4 are nonempty; a nonempty finite set has a non-dominated member, so $A$ is nonempty. The rest is Lemma 1. $\square$
