---
title: NSGA-II keeps N members, keeps whole fronts first, and keeps every OneMinMax value when N is at least 4(n+1)
proves: [correctness]
status: full
---

All objectives are minimized, $N$ is the population size, and line numbers refer to the `pseudo id=main` block of the NSGA-II page. NSGA-II is a heuristic. The statements below are the invariants of its survival step and one runtime lemma of Zheng, Liu and Doerr (2022) for a test function; nothing here says that NSGA-II reaches the Pareto front of a general problem.

We use two facts from other pages. The [non-dominated sorting](/non-dominated-sorting/) proof shows that line L6 returns the fronts $F_1, F_2, \ldots$ of $R$, which partition $R$, with $F_1$ the set of members of $R$ that no member of $R$ dominates. The [crowding distance](/crowding-distance/) page shows that the two extremes of each objective in a front get distance $\infty$.

## Survival

**Theorem 1.** Assume $\lvert R \rvert \ge N$. After lines L7 to L11, $\lvert P \rvert = N$. There is an index $k$ such that $P = F_1 \cup \cdots \cup F_{k-1} \cup S$, where $S \subseteq F_k$ is empty when $\lvert F_1 \cup \cdots \cup F_{k-1} \rvert = N$, and otherwise $S$ holds the $N - \lvert F_1 \cup \cdots \cup F_{k-1} \rvert$ members of $F_k$ with the largest crowding distance in $F_k$.

*Proof.* The loop of lines L8 and L9 adds whole fronts while they fit. It stops at the first $k$ with $\lvert P \rvert + \lvert F_k \rvert > N$, or when no front is left. In the second case $P = R$, so $\lvert R \rvert \le N$, and with $\lvert R \rvert \ge N$ this gives $\lvert P \rvert = N$. In the first case $\lvert P \rvert \le N < \lvert P \rvert + \lvert F_k \rvert$, so $0 \le N - \lvert P \rvert < \lvert F_k \rvert$, and line L11 can take exactly $N - \lvert P \rvert$ members of $F_k$. After it, $\lvert P \rvert = N$. The fronts are disjoint, so no member is counted twice. $\square$

**Corollary 2.** (a) If $\lvert F_1(R) \rvert \le N$, then every member of $F_1(R)$ survives. (b) If $\lvert F_1(R) \rvert \ge N$, then every survivor is in $F_1(R)$, and if at most $N$ members of $F_1(R)$ have crowding distance $\infty$, all of them survive.

*Proof.* (a) is the case $k \ge 2$ of Theorem 1, or $k = 1$ with $S = F_1$. (b) If $\lvert F_1 \rvert \ge N$, the loop adds nothing, or adds $F_1$ exactly when $\lvert F_1 \rvert = N$, and line L11 takes the members of $F_1$ with the largest distances. Members with distance $\infty$ come first in that order. $\square$

**Corollary 3 (elitism).** Let $P_t$ and $Q_t$ be the parents and offspring of generation $t$. If $\lvert F_1(P_t \cup Q_t) \rvert \le N$, then each image that is non-dominated in $P_t \cup Q_t$ is the image of a member of $P_{t+1}$.

*Proof.* Corollary 2(a). $\square$

When $\lvert F_1 \rvert > N$, a non-dominated member can be removed by line L11, and a later population can then hold a point that the removed member dominates. The page of the [MOEA template](/multi-objective-evolutionary-algorithm/) gives a three-point example of this effect for a truncation by crowding distance.

## A runtime lemma for OneMinMax

OneMinMax on bit strings of length $n$ has the objectives $f_1(x) = \lvert x \rvert_1$ and $f_2(x) = n - \lvert x \rvert_1$ in the minimization form used here. Every string is Pareto-optimal, and there are $n + 1$ images, one for each value $v = f_1(x) \in \{0, \ldots, n\}$.

**Theorem 4 (Zheng, Liu and Doerr, 2022).** If $N \ge 4(n + 1)$, then each value of $f_1$ that occurs in $P_t$ occurs in $P_{t+1}$.

*Proof.* No string dominates another, so $R = P_t \cup Q_t$ is one front, of size $2N > N$, and line L11 keeps the $N$ members of $R$ with the largest crowding distance. In the sort by $f_1$, the members with one value $v$ form a block of consecutive positions. Since $f_2 = n - f_1$, the same members also form a block in the sort by $f_2$. A member that is neither first nor last of its block in the sort for objective $m$ has two neighbors with the same image, so its gap in objective $m$ is $0$. So a member has a positive distance only if it is first or last of its block in at least one of the two sorts. That gives at most $4$ members per value, and at most $4(n+1) \le N$ members with a positive distance in all of $R$. The first member of each block in the sort by $f_1$ has a positive distance: either it is the first of all, with distance $\infty$, or its left neighbor has a smaller value and its right neighbor a value at least $v$, so its gap is positive. Line L11 keeps the $N$ members with the largest distances, and at most $N$ members have a positive distance, so all of them are kept, among them one member of each value present in $R$. The values of $P_t$ are present in $R$. $\square$

With this lemma, Zheng, Liu and Doerr bound the expected number of evaluations by $O(N n \log n)$ on OneMinMax and $O(N n^2)$ on LOTZ for $N \ge 4(n+1)$, with bit-wise mutation and the selection of their paper. Those bounds are their theorems; the test of this page checks only the invariant of Theorem 4.

## The output

**Lemma 5.** Line L12 returns a nonempty set of mutually non-dominated members of the last population.

*Proof.* The first front of a nonempty finite set is nonempty and has no dominated pair, by its definition. $\square$
