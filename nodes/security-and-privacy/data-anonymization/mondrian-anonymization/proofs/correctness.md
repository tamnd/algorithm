---
title: Mondrian returns a partition into regions of at least k rows with no allowable cut
proves: [correctness]
status: full
---

The table $T$ has $n \ge k \ge 1$ rows, and each row has $d$ integer attributes. A *cut* of a set $P$ of rows on attribute $a$ at the value $x$ splits $P$ into $\{t \in P : t.a \le x\}$ and $\{t \in P : t.a > x\}$. The cut is *allowable* when both sides have at least $k$ rows. Let $m$ be the largest number of equal rows in $T$.

**Lemma 1 (the cut search).** Line L5 returns NIL if and only if $P$ has no allowable cut on $a$. Otherwise it returns an allowable cut.

*Proof.* Let $u_1 < u_2 < \cdots < u_q$ be the distinct values of $a$ in $P$. A cut at $x$ has the same two sides as the cut at the largest $u_j \le x$, or puts all of $P$ on one side when $x < u_1$ or $x \ge u_q$. A cut with an empty side is not allowable, because $k \ge 1$. So $P$ has an allowable cut on $a$ if and only if one of the cuts at $u_1, \ldots, u_{q-1}$ is allowable. The implementation tests exactly these cuts, at each place where two neighbors in the sorted list of values differ, and keeps the allowable one with the best balance. $\square$

**Lemma 2 (the size bound).** If a set $P$ of $r \ge 1$ rows has no allowable cut on any attribute, then $r \le 2d(k - 1) + m$.

*Proof.* Fix an attribute $a$. Sort the values of $a$ in $P$, and let $v$ be the value at position $\lceil r/2 \rceil$, counted from 1. Let $L$ be the number of rows with $t.a < v$ and $R$ the number with $t.a > v$. Then $L \le \lceil r/2 \rceil - 1$ and $R \le r - \lceil r/2 \rceil = \lfloor r/2 \rfloor$.

If $L \ge k$, let $u$ be the largest value below $v$. The cut at $u$ has $L \ge k$ rows on the left and $r - L \ge \lfloor r/2 \rfloor + 1 \ge \lceil r/2 \rceil > L \ge k$ rows on the right, so it is allowable. If $R \ge k$, the cut at $v$ has $R \ge k$ rows on the right and $r - R \ge \lceil r/2 \rceil \ge \lfloor r/2 \rfloor \ge R \ge k$ rows on the left, so it is allowable. $P$ has no allowable cut, so neither case is possible, and $L \le k - 1$ and $R \le k - 1$. At most $2(k - 1)$ rows of $P$ have a value of $a$ other than $v$.

Do this for each attribute, with the values $v_1, \ldots, v_d$. At most $2d(k - 1)$ rows differ from $(v_1, \ldots, v_d)$ on some attribute. The other rows are equal to $(v_1, \ldots, v_d)$, and there are at most $m$ of them. $\square$

**Theorem.** MONDRIAN$(T, k)$ stops. The sets of its result are a partition of the rows of $T$. Each set has at least $k$ rows, has no allowable cut on any attribute, and has at most $2d(k - 1) + m$ rows.

*Proof.* We use this invariant for the loop of line L2:

> **(P)** The sets in the stack and in the result are disjoint, their union is the set of all rows of $T$, and each of them has at least $k$ rows. Each set in the result has no allowable cut on any attribute.

Line L1 makes (P) true, because the stack holds all $n \ge k$ rows and the result is empty. In a step, line L3 removes a set $P$. If line L5 finds a cut on some attribute, Lemma 1 says that the cut is allowable, so line L7 pushes two disjoint sets with union $P$, each with at least $k$ rows. Otherwise Lemma 1 says that $P$ has no allowable cut on any attribute, and line L8 puts $P$ in the result. In both cases (P) holds.

Each cut replaces a set by two sets that are smaller and not empty. So the number of cuts is at most $n - 1$, and the number of steps is at most $2n - 1$. When the stack is empty, (P) says that the result is a partition into sets of at least $k$ rows with no allowable cut, and Lemma 2 gives the size bound. $\blacksquare$

**Remark.** Lemma 2 is Theorem 2 of LeFevre, DeWitt and Ramakrishnan (2006). The proof shows a point that the paper does not state: with repeated values, the cut at the median value $v$ can have an empty side even when the cut just below $v$ is allowable. That is why line L5 tests every distinct value and not only the median.
