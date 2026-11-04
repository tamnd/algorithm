---
title: A spectral Bloom filter never underestimates
proves: [correctness, invariant, termination]
status: full
---

Fix the hash functions and a sequence of operations. Write $f$ for the multiset after the first $t$ operations, $C$ for the counters of minimum selection and $D$ for the counters of minimal increase on the same sequence of inserts. Each operation loops over at most $k$ positions, so it ends.

**Lemma 1 (invariant (M)).** Under minimum selection, after each operation $C[p] = \sum_{y : p \in H(y)} f_y$ for each $p$, provided every DELETE$(x, w)$ has $f_x \ge w$ before it.

*Proof.* At the start both sides are 0. INSERT$(x, w)$ adds $w$ to $f_x$, which adds $w$ to the right side exactly for the $p \in H(x)$, and line L3 adds $w$ to exactly these counters, once each, since $H(x)$ is a set. DELETE$(x, w)$ is the same with $-w$. $\square$

**Theorem 1 (minimum selection).** For each $x$, $\hat f_x = f_x + \min_{p \in H(x)} \sum_{y \ne x,\, p \in H(y)} f_y$. So $\hat f_x \ge f_x$, with equality exactly when some $p \in H(x)$ lies in $H(y)$ for no $y \ne x$ with $f_y > 0$.

*Proof.* By Lemma 1, for $p \in H(x)$ the counter is $C[p] = f_x + \sum_{y \ne x,\, p \in H(y)} f_y$, and line L7 takes the minimum over $p \in H(x)$. The sums have nonnegative terms, so the minimum is 0 exactly when one of them has no positive term. $\square$

**Theorem 2 (minimal increase).** If all operations are inserts and minimal increase is used, then after each insert, for each key $y$ and each $p \in H(y)$,
$$ f_y \le D[p] \le C[p]. $$
Hence $f_x \le \hat f_x^{\mathrm{MI}} \le \hat f_x^{\mathrm{MS}}$ for each $x$.

*Proof.* By induction over the inserts. At the start all values are 0. Consider INSERT$(x, w)$, and let $f'$, $C'$ and $D'$ be the values after it.

*Lower bound.* Let $v = \min_{p \in H(x)} D[p]$, the value of line L4. By the induction hypothesis $v \ge f_x$. Line L5 sets $D'[p] = \max(D[p], v + w) \ge f_x + w = f'_x$ for each $p \in H(x)$. For $y \ne x$, $f'_y = f_y$ and no counter decreases, so $D'[p] \ge D[p] \ge f_y$ for $p \in H(y)$.

*Upper bound.* For $p \notin H(x)$ nothing changes. For $p \in H(x)$, line L3 gives $C'[p] = C[p] + w$. If $D'[p] = D[p]$, then $D'[p] \le C[p] \le C'[p]$. Otherwise $D'[p] = v + w \le D[p] + w \le C[p] + w = C'[p]$, since $v \le D[p]$ for each $p \in H(x)$.

The estimates are minima over the same set $H(x)$ of values that satisfy the bounds pointwise, which gives the last claim. $\blacksquare$
