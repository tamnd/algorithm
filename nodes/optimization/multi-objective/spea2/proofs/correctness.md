---
title: SPEA2 fitness is below 1 exactly for non-dominated points, is strictly monotone under dominance, and the archive has exactly M members
proves: [correctness]
status: full
---

All objectives are minimized, $N$ is the population size, $M$ is the archive size, and line numbers refer to the `pseudo id=main` block of the SPEA2 page. $U$ is the multiset $P + A$ of line L3. SPEA2 is a heuristic; the statements below are about its fitness and its archive, not about reaching the Pareto front of a problem.

## Fitness

**Lemma 1.** For $i \in U$, $R(i) = 0$ if no member of $U$ dominates $i$, and $R(i) \ge 1$ otherwise. $0 < D(i) \le 1/2$. So $F(i) < 1$ exactly when $i$ is non-dominated in $U$.

*Proof.* If $j$ dominates $i$, then $S(j) \ge 1$, since $j$ dominates at least $i$. So $R(i)$, the sum of $S(j)$ over the dominators $j$ of $i$, is $0$ when there is no dominator and at least $1$ when there is one. $\sigma_i^k \ge 0$ gives $D(i) = 1/(\sigma_i^k + 2) \in (0, 1/2]$. Then $F = R + D$ is in $(0, 1/2]$ in the first case and at least $1$ in the second. $\square$

**Lemma 2.** If $i$ dominates $j$ in $U$, then $F(i) < F(j)$.

*Proof.* Dominance is transitive, so every dominator of $i$ also dominates $j$, and $i$ dominates $j$ too. So $R(j) \ge R(i) + S(i) \ge R(i) + 1$. With Lemma 1, $F(j) \ge R(i) + 1 + D(j) > R(i) + 1/2 \ge R(i) + D(i) = F(i)$. $\square$

This is the change from [SPEA](/spea/), where a dominated pair can get equal fitness.

## The archive

**Theorem 3.** If $\lvert U \rvert \ge M$, then after lines L7 to L9 the archive has exactly $M$ members. If $U$ has at least $M$ non-dominated members, all archive members are non-dominated in $U$. If it has fewer, all non-dominated members are in the archive, and each other member of the archive has $F$ no larger than any member of $U$ left out.

*Proof.* Let $D_U$ be the set of non-dominated members, which line L7 takes by Lemma 1. If $\lvert D_U \rvert < M$, line L8 adds the $M - \lvert D_U \rvert$ members with $F \ge 1$ and the smallest $F$; there are enough of them because $\lvert U \rvert \ge M$. Line L9 does nothing. If $\lvert D_U \rvert \ge M$, line L8 does nothing, and line L9 removes members of $D_U$ one at a time until $M$ are left. $\square$

**Corollary 4.** Let $S_t$ be the set of images of all members of $U$ up to generation $t$. If in each generation $U$ has at most $M$ non-dominated members, then every non-dominated image of $S_t$ is the image of a member of the archive after generation $t$.

*Proof.* Let $y$ be a non-dominated image of $S_t$, first seen in generation $s \le t$. In each generation $r$ from $s$ to $t$, a member with image $y$ is in $U_r$ (in $P_s$ for $r = s$, in the archive after that), and no member of $U_r \subseteq S_t$ dominates it. By Theorem 3 with $\lvert D_U \rvert \le M$, it stays in the archive. $\square$

When more than $M$ points are non-dominated, truncation removes some, and a later archive can hold a point that a removed point dominates.

## Truncation

**Lemma 5.** Each step of line L9 removes a member of a closest pair of the current archive. The loop stops after $\lvert D_U \rvert - M$ steps.

*Proof.* The sorted list of member $i$ starts with the distance from $i$ to its nearest neighbour. The lexicographically smallest list has the smallest first entry, which is the smallest distance between two members. Each step removes one member. $\square$

Zitzler, Laumanns and Thiele argue that this rule keeps boundary points. It is not a theorem. With $M = 4$ and the five mutually non-dominated points $(0, 2, 3)$, $(1, 0, 5)$, $(1, 3, 2)$, $(4, 0, 4)$, $(6, 1, 3)$, the closest pair is $(0, 2, 3)$ and $(1, 3, 2)$, at squared distance $3$. The next squared distances are $9$ for $(0, 2, 3)$ and $18$ for $(1, 3, 2)$, so line L9 removes $(0, 2, 3)$, the only point with first objective $0$. The point $(6, 1, 3)$, which is extreme in no objective, stays.

## The output

**Lemma 6.** Line L10 returns a nonempty set of mutually non-dominated members of the archive.

*Proof.* The archive is nonempty for $M \ge 1$, and the non-dominated members of a nonempty finite set form a nonempty set with no dominated pair. $\square$
