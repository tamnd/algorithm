---
title: "The nucleus is a smallest set of mass at least p, and the draw follows the renormalized distribution"
proves: [correctness]
status: full
---

We use the notation of the page. The input is a distribution $P$ over the vocabulary $V = \{0, \ldots, |V| - 1\}$, a threshold $0 < p \le 1$, and a number $u$ drawn uniformly from $[0, 1)$. We assume exact arithmetic, as with the Fractions of the tests; the last remark treats rounding.

Let $i_1, i_2, \ldots, i_{|V|}$ be the order of line L1: the tokens sorted by the key $(-P_i, i)$. This order is unique. For $m = 0, \ldots, |V|$ let $S_m = \{i_1, \ldots, i_m\}$ and $M(m) = P(S_m)$, the mass of the first $m$ tokens. $M$ does not decrease in $m$, and $M(|V|) = 1 \ge p$.

**Lemma 1 (prefixes have maximum mass).** For every $m$ and every set $S \subseteq V$ with $|S| = m$, $P(S) \le M(m)$.

*Proof.* This is the exchange argument of [top-k sampling](/top-k-sampling/): every token of $S_m$ is at least as probable as every token outside it, so replacing a token of $S \setminus S_m$ by a token of $S_m \setminus S$ never lowers the mass, and after at most $m$ such steps the set is $S_m$. $\square$

**Theorem 2 (the nucleus is a smallest set).** Let $m^*$ be the smallest $m$ with $M(m) \ge p$. Lines L2 to L5 return $S_{m^*}$. No set of fewer than $m^*$ tokens has mass at least $p$. Among the sets of $m^*$ tokens, $S_{m^*}$ has the largest mass.

*Proof.* After the pass of line L4 for the token $i_t$, the running sum is $c = M(t)$, by induction on $t$ from $c = 0$ (line L2). Line L5 returns $S_t$ at the first $t$ with $M(t) \ge p$, which is $m^*$. Such a $t$ exists since $M(|V|) = 1 \ge p$. If a set $S$ with $|S| = m < m^*$ had $P(S) \ge p$, then $M(m) \ge P(S) \ge p$ by Lemma 1, against the choice of $m^*$. The last claim is Lemma 1 with $m = m^*$. $\square$

**Corollary 3 (no zero tokens).** The nucleus has no token of probability 0.

*Proof.* The zero tokens come last in the order. If $i_{m^*}$ had probability 0, then $M(m^* - 1) = M(m^*) \ge p$, against the choice of $m^*$. $\square$

**Theorem 4 (the draw).** Let $Z = M(m^*)$. NUCLEUS-SAMPLE returns each token $i$ of the nucleus with probability $P_i / Z$, and never returns a token outside the nucleus.

*Proof.* Line L7 sets $r = uZ$, uniform on $[0, Z)$. Lines L8 to L10 walk the nucleus in the order of line L1 with the running sum $c_t = M(t)$ and return $i_t$ for the unique $t$ with $M(t - 1) \le r < M(t)$. That interval has length $P_{i_t}$, so $i_t$ is returned with probability $P_{i_t} / Z$. Since $r < Z = M(m^*)$, the walk always returns inside the loop, and line L11 is not reached. $\square$

**Corollary 5 (limits).** For $p \le \max_i P_i$, the nucleus is the first most probable token and the step is [greedy decoding](/greedy-decoding/). For $p = 1$, the nucleus is the set of all tokens of positive probability, and the step samples from $P$.

*Proof.* For the first claim, $M(1) = \max_i P_i \ge p$, so $m^* = 1$. For the second, $M(m) = 1$ exactly when $S_m$ holds every token of positive probability, and by Corollary 3 the nucleus holds no other. $\square$

**Remark (rounding).** With floats, the running sum can stay below $p$ where the exact sum reaches it. For $P = (0.7, 0.2, 0.1)$ and $p = 0.9$, the float sum $0.7 + 0.2$ is $0.8999999999999999$, so the code keeps 3 tokens where exact arithmetic keeps 2. In the extreme case the sum stays below $p$ up to the end, and the code then keeps every token of positive probability, which is the result for $p = 1$. In the draw, $Z$ and the running sum can differ in the last bits and $uZ$ can round up, and line L11 then returns the last kept token of positive probability. These events change the result only at the boundary of the threshold, by an amount of the order of the rounding error.
