---
title: NSGA-III keeps N members, keeps whole fronts first, and gives each empty niche one member before any niche gets two
proves: [correctness]
status: full
---

All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, $H$ is the number of reference points, and line numbers refer to the `pseudo id=main` block of the NSGA-III page. NSGA-III is a heuristic. The statements below are about the reference points and the survival step; nothing here says that NSGA-III reaches the Pareto front of a problem.

We use one fact from another page: the [non-dominated sorting](/non-dominated-sorting/) proof shows that line L4 returns the fronts $F_1, F_2, \ldots$ of $R$, which partition $R$, with $F_1$ the set of members of $R$ that no member of $R$ dominates.

## The reference points

**Lemma 1.** For $h \ge 1$, the set $Z$ of points $w \in \mathbb{R}^p$ with $w_m \ge 0$, $\sum_m w_m = 1$ and each $h w_m$ an integer has $\binom{h + p - 1}{p - 1}$ members.

*Proof.* The map $w \mapsto (h w_1, \ldots, h w_p)$ is a bijection from $Z$ onto the tuples of $p$ nonnegative integers with sum $h$. A tuple matches one row of $h$ stars and $p - 1$ bars, and a row is fixed by the choice of the $p - 1$ bar places among $h + p - 1$ places. $\square$

## Survival

**Theorem 2.** Assume $\lvert R \rvert \ge N$. After lines L4 to L15, $\lvert P \rvert = N$, and $P = F_1 \cup \cdots \cup F_{l-1} \cup A$ with $A \subseteq F_l$, where $l$ is the first index with $\lvert F_1 \cup \cdots \cup F_l \rvert \ge N$.

*Proof.* The fronts partition $R$ and $\lvert R \rvert \ge N$, so line L5 finds $l$. If $\lvert S \rvert = N$, line L6 returns $S = F_1 \cup \cdots \cup F_l$ with $A = F_l$. Otherwise $\lvert F_1 \cup \cdots \cup F_{l-1} \rvert < N < \lvert S \rvert$, so line L7 sets $K = N - \lvert P \rvert$ with $1 \le K < \lvert F_l \rvert$. By Lemma 3 the loop of lines L11 to L15 adds exactly $K$ distinct members of $F_l$. $\square$

**Lemma 3.** The loop of lines L11 to L15 stops after at most $K + H$ rounds and adds exactly $K$ distinct members of $F_l$.

*Proof.* Each round either adds a member of $F_l$ that was not added before (line L15), or excludes a line (line L14). At most $H$ lines can be excluded. A line $j$ is excluded only when no member of $F_l$ that is still free is attached to $j$, and from then on no free member is attached to $j$, because members are only taken, never returned. Line L9 attaches every member of $S$, so every member of $F_l$, to some line. While fewer than $K < \lvert F_l \rvert$ members are added, a free member $s$ exists, its line is not excluded, and so line L12 has a line to choose. So the loop does not get stuck, and it stops after the $K$-th addition, after at most $K + H$ rounds. $\square$

**Corollary 4 (elitism).** If $\lvert F_1(R) \rvert \le N$, then every member of $F_1(R)$ survives.

*Proof.* Then $l \ge 2$, or $l = 1$ with $\lvert S \rvert = N$. In both cases Theorem 2 puts all of $F_1$ in $P$. $\square$

## Empty niches first

Let $\rho_j$ be the niche counts of line L10, before the loop, and let $E$ be the set of lines $j$ with $\rho_j = 0$ to which at least one member of $F_l$ is attached.

**Theorem 5.** The first $\min(K, \lvert E \rvert)$ members that the loop adds are attached to distinct lines of $E$. The member added for a line $j \in E$ is a member of $F_l$ attached to $j$ with the smallest perpendicular distance $d$.

*Proof.* Call a line of $E$ served once a member is added for it. Consider a round in which fewer than $\min(K, \lvert E \rvert)$ members were added and only lines of $E$ received them. Then some line $j_0 \in E$ is not served. Its count is still $0$, and its members of $F_l$ are all still free, so $j_0$ is not excluded. So the smallest count among the lines that are not excluded is $0$, and line L12 picks a line $j$ with count $0$. If no free member of $F_l$ is attached to $j$, the round only excludes $j$. Otherwise $j \in E$, because a line outside $E$ with count $0$ has no member of $F_l$ at all. Its count is $0$, so $j$ was not served before, all its members of $F_l$ are free, and line L15 adds the one with the smallest $d$. Then the count of $j$ becomes $1$, so $j$ is never picked again while a count of $0$ is left. By induction on the rounds, the first $\min(K, \lvert E \rvert)$ additions go to distinct lines of $E$. $\square$

So a reference line that the kept fronts do not reach yet, and that a candidate of $F_l$ is near, gets a member before any line gets a second one. This is the diversity rule of Deb and Jain in exact form.

## Normalization

**Lemma 6.** After the translation of line L8, every translated image of $S$ has nonnegative coordinates and each coordinate has minimum $0$ over $S$. If the extreme points $e^1, \ldots, e^p$ span a hyperplane $\sum_m s_m / a_m = 1$ with all $a_m > 0$, then each normalized extreme point has coordinate sum $1$.

*Proof.* The ideal point $z$ has $z_m = \min_{s \in S} f_m(s)$, so $f_m(s) - z_m \ge 0$, with equality for a minimizer. The normalized point of $e^k$ has coordinates $e^k_m / a_m$, and their sum is $1$ because $e^k$ lies on the hyperplane. $\square$

With the fallback, the intercepts are the largest translated values, or $1$ where the largest value is $0$, so all normalized coordinates of $S$ are in $[0, 1]$.

## The output

**Lemma 7.** Line L16 returns a nonempty set of mutually non-dominated members of the last population.

*Proof.* The first front of a nonempty finite set is nonempty and has no dominated pair. $\square$
