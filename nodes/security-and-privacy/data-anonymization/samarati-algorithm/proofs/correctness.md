---
title: Samarati's algorithm returns a k-minimal generalization of minimal height
proves: [correctness]
status: full
---

We use the notation of the page. The table $T$ has $n$ rows and $d$ quasi-identifier attributes. Attribute $a$ has a hierarchy with levels $0, 1, \ldots, h_a$, and each level coarsens the level below it: the value at level $l + 1$ is a function of the value at level $l$. A vector $v$ has $0 \le v_a \le h_a$ for each $a$, its height is $|v| = \sum_a v_a$, and $v \le w$ means $v_a \le w_a$ for each $a$. The top vector is $\top = (h_1, \ldots, h_d)$ and $h = |\top|$. We write $T_v$ for $T$ generalized by $v$, and $\mathrm{sup}(v)$ for the number of rows of $T_v$ whose combination of values occurs fewer than $k$ times. Lines L12 and L13 compute $\mathrm{sup}(v)$, so SATISFIES$(T, v, k, MaxSup)$ is true if and only if $\mathrm{sup}(v) \le MaxSup$. We say that $v$ *satisfies* when this is true.

**Lemma 1 (monotonicity).** If $v \le w$, then $\mathrm{sup}(w) \le \mathrm{sup}(v)$.

*Proof.* Because each level is a function of the level below it, the value of a row at level $w_a$ is a function of its value at level $v_a$. So two rows that are equal in $T_v$ are equal in $T_w$, and each group of equal rows of $T_w$ is a union of groups of $T_v$. A row that is in a group of at least $k$ rows in $T_v$ is therefore in a group of at least $k$ rows in $T_w$. So the rows counted by $\mathrm{sup}(w)$ are a subset of the rows counted by $\mathrm{sup}(v)$. $\square$

Let $P(t)$ be the statement "some vector of height $t$ satisfies".

**Lemma 2.** If $P(t)$ is true and $t < h$, then $P(t + 1)$ is true.

*Proof.* Let $v$ satisfy with $|v| = t < h$. Then $v_a < h_a$ for some $a$. The vector $w$ that is $v$ with $w_a = v_a + 1$ has height $t + 1$ and $v \le w$, so $\mathrm{sup}(w) \le \mathrm{sup}(v) \le MaxSup$ by Lemma 1. $\square$

**Theorem.** If no vector satisfies, SAMARATI returns NIL. Otherwise it returns the first vector in lexicographic order among the satisfying vectors of the least height $t^*$, and no satisfying vector $u$ has $u \le$ sol and $u \ne$ sol.

*Proof.* Each vector $v$ has $v \le \top$, so $\mathrm{sup}(\top) \le \mathrm{sup}(v)$ by Lemma 1. If $\top$ does not satisfy, then no vector satisfies, and line L1 returns NIL. This is correct.

Now assume that $\top$ satisfies, so $P(h)$ is true and $t^*$ exists. By Lemma 2, $P(t)$ is false for $t < t^*$ and true for $t^* \le t \le h$. We use this invariant for the loop of line L4:

> **(B)** $low \le t^* \le high$, and sol is the first satisfying vector in lexicographic order at height $high$.

Lines L2 and L3 make (B) true: $low = 0$, $high = h$, and $\top$ is the only vector of height $h$.

In one step of the loop, $low < high$, so line L5 gives $low \le try < high$. Line L7 visits all the vectors of height $try$ in lexicographic order, and line L8 stops at the first one that satisfies. If one is found, $P(try)$ is true, so $t^* \le try$, and line L9 sets $high = try$ and sol to that vector. Then (B) holds. If none is found, $P(try)$ is false, so $t^* > try$, and line L10 sets $low = try + 1 \le t^*$. Then (B) holds, and sol has not changed. In both cases $high - low$ goes down by at least 1, so the loop stops.

When the loop stops, $low = high$, so (B) gives $high = t^*$. Line L11 returns the first satisfying vector of height $t^*$ in lexicographic order. If a satisfying $u$ had $u \le$ sol and $u \ne$ sol, then $|u| < t^*$, and this contradicts the choice of $t^*$. $\blacksquare$

**Remark.** The loop of line L4 runs at most $\lceil \lg(h + 1) \rceil$ times, because the range $[low, high]$ has $h + 1$ heights at the start and loses at least half of them in each step.
