---
title: The fast non-dominated sort and the two-objective sweep return the Pareto fronts
proves: [correctness]
status: full
---

All objectives are minimized. The input is a list $Y = (y^1, \ldots, y^N)$ of points of $\mathbb{R}^p$. We write $a \prec b$ when $a$ dominates $b$: $a_t \le b_t$ for each $t$ and $a \ne b$. This relation is irreflexive and transitive, so it is a strict partial order on the indices.

**Fronts.** Let $R_0 = \{1, \ldots, N\}$. For $k \ge 1$ let $F_k$ be the set of $j \in R_{k-1}$ such that no $i \in R_{k-1}$ has $y^i \prec y^j$, and let $R_k = R_{k-1} \setminus F_k$. The rank of $j$ is the $k$ with $j \in F_k$.

**Lemma 1.** (a) A nonempty $R_{k-1}$ gives a nonempty $F_k$. So each index gets a rank, and there are at most $N$ fronts. (b) If $y^i \prec y^j$, then $\mathrm{rank}(i) < \mathrm{rank}(j)$. (c) If $\mathrm{rank}(j) = k \ge 2$, then some $i$ with $\mathrm{rank}(i) = k - 1$ has $y^i \prec y^j$.

*Proof.* (a) A finite nonempty set with a strict partial order has a minimal element, and a minimal element of $R_{k-1}$ is in $F_k$. Each step removes at least one index, so after at most $N$ steps all indices have a rank.
(b) Let $j \in F_k$. Then no index of $R_{k-1}$ dominates $j$, so $i \notin R_{k-1}$, and $i$ was removed in an earlier step: $\mathrm{rank}(i) < k$.
(c) The index $j$ is in $R_{k-2}$ but not in $F_{k-1}$, so the set $D$ of the indices of $R_{k-2}$ that dominate $j$ is not empty. Let $m$ be a minimal element of $D$. If some $z \in R_{k-2}$ had $y^z \prec y^m$, then $y^z \prec y^j$ by transitivity, so $z \in D$, and $m$ would not be minimal. So $m \in F_{k-1}$. $\square$

## The fast non-dominated sort

**Lemma 2.** After lines L1 to L5, $S[i] = \{j : y^i \prec y^j\}$ and $n[j] = |\{i : y^i \prec y^j\}|$.

*Proof.* Lines L2 and L3 visit each unordered pair $\{i, j\}$ with $i < j$ one time. At most one of $y^i \prec y^j$ and $y^j \prec y^i$ is true, because the relation is a strict order. Line L4 records the first case and line L5 the second. $\square$

**Theorem.** The loop of lines L7 to L13 outputs $F_1, F_2, \ldots$ in this order, and stops after the last front.

*Proof.* We show this invariant at the test of line L7 in round $k$:

> **(I)** The current set equals $F_k$, and for each $j \in R_{k-1}$, $n[j] = |\{i \in R_{k-1} : y^i \prec y^j\}|$.

*Start.* In round 1, $R_0$ is the full set. By Lemma 2, $n[j]$ counts all dominators of $j$, and line L6 takes the $j$ with $n[j] = 0$, which is $F_1$.

*Step.* In round $k$, lines L9 to L12 decrease $n[j]$ by one for each pair $(i, j)$ with $i \in F_k$ and $y^i \prec y^j$. By Lemma 1(b), such a $j$ has a rank larger than $k$, so $j \in R_k$. After the round, for each $j \in R_k$,
$$n[j] = |\{i \in R_{k-1} : y^i \prec y^j\}| - |\{i \in F_k : y^i \prec y^j\}| = |\{i \in R_k : y^i \prec y^j\}|.$$
So $n[j] = 0$ at the end of the round exactly when $j \in F_{k+1}$. Each $j \in R_k$ had $n[j] \ge 1$ at the start of the round, because $j \notin F_k$. So line L12 adds $j$ to $Q$ exactly when its count goes from 1 to 0 in this round, which happens one time for each $j \in F_{k+1}$ and never for the other indices. So $Q = F_{k+1}$ with no repeats, and line L13 makes it the current set. This is (I) for round $k + 1$.

*End.* By Lemma 1(a), $F_k$ is empty exactly when $R_{k-1}$ is empty, that is, after the last front. Each round removes at least one index from $R$, so there are at most $N + 1$ tests of line L7. $\blacksquare$

## The two-objective sweep

The sweep NDS-2D visits the indices in the lexicographic order of $(y_1, y_2)$, and keeps for each front the last index added to it.

**Lemma 3.** Inside one front, in the order of the sweep, $y_1$ does not decrease and $y_2$ does not increase.

*Proof.* The first part holds by the order. Let $a$ come before $b$ in the same front. Then $a_1 \le b_1$. If $a_2 \le b_2$, then $a \preceq b$, and since $a$ does not dominate $b$, $a = b$. So $a_2 \ge b_2$ in each case. $\square$

**Lemma 4.** A point $q$ is dominated only by points that come before it in the sweep. When $q$ is visited, let $\ell_k$ be the last point of front $k$. Then (a) some point of front $k$ dominates $q$ if and only if $\ell_k \prec q$. (b) Assume that each earlier point $u$ went to a front $k + 1 \ge 2$ only when the last point of front $k$ at that time dominated $u$. Then $\ell_{k+1} \prec q$ implies $\ell_k \prec q$.

*Proof.* A point $t$ after $q$ has $t_1 > q_1$, or $t_1 = q_1$ and $t_2 \ge q_2$. In both cases $t$ does not dominate $q$.
(a) Let $r$ be a point of front $k$ with $r \prec q$. By Lemma 3, $\ell_{k,1} \le q_1$ (by the order) and $\ell_{k,2} \le r_2 \le q_2$. So $\ell_k \preceq q$. If $\ell_k = q$, then $r \prec \ell_k$ inside one front, which is false. So $\ell_k \prec q$.
(b) By the assumption, when $\ell_{k+1}$ entered front $k+1$, the last point $s$ of front $k$ at that time dominated it. So $s \prec \ell_{k+1} \prec q$, and $s$ is still in front $k$. By (a), $\ell_k \prec q$. $\square$

**Theorem.** NDS-2D puts each index in its front.

*Proof.* By induction over the sweep, with this hypothesis: each earlier point $u$ is in its right front, and it went to the first front whose last point did not dominate it, so it went to a front $k + 1 \ge 2$ only when the last point of front $k$ dominated it. By Lemma 4(b), the set of fronts whose last point dominates $q$ is a prefix $1, \ldots, h$, so the binary search finds $h$, and $q$ goes to front $h + 1$, which keeps the hypothesis. By Lemma 4(a), some point of front $h$ dominates $q$ (if $h \ge 1$), and no point of a front after $h$ does. By Lemma 1(b) and (c), the rank of $q$ is one more than the largest rank of a point that dominates $q$, and all these points come before $q$. So the rank of $q$ is $h + 1$, which is the front that the sweep gives it. $\blacksquare$
