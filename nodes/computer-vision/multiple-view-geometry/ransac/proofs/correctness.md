---
title: RANSAC keeps the largest consensus set it sees and finds a largest one with probability p under the sampling assumptions
proves: [correctness]
status: full
---

We use the notation of the page. $D$ has $n$ items, a minimal sample has $s \le n$ distinct items, and $I(\theta) = \{x \in D : r(\theta, x) \le \varepsilon\}$ is the consensus set of a model $\theta$. Let $m^*$ be the largest $|I(\theta)|$ over the models that the minimal solver can return from some sample, and let $I$ be a consensus set of size $m^*$. Let $q$ be the probability that one sample of line L4 is a subset of $I$, and let $k(w) = \lceil \log(1 - p) / \log(1 - w^s) \rceil$ for $0 < w < 1$, with $k(1) = 1$. The minimal solver, the residual and the refit are correct subroutines, and the model of computation is the real RAM.

**Claim.** (a) At each test of line L2, $I^*$ is a consensus set of largest size among the models of the samples drawn so far, and $\theta^*$ is its model. (b) The loop ends after at most $k_{\max}$ rounds. (c) Assume that the samples are independent, that every sample inside $I$ gives a model whose consensus set has size $m^*$, that $q \ge (m^*/n)^s$ and that $k_{\max} \ge \lceil \log(1 - p) / \log(1 - q) \rceil$. Then the set $I^*$ returned in line L14 has size $m^*$ with probability at least $p$.

**Lemma 1 (invariant).** Part (a) holds.

*Proof.* Before the first round no sample is drawn and $I^* = \emptyset$. In a round, either line L6 skips the sample, so the set of models does not change, or line L7 computes $I(\theta)$ for the new model $\theta$. Line L8 replaces $I^*$ exactly when $|I(\theta)| > |I^*|$, so after line L9, $I^*$ has the largest size among the old models and the new one. $\square$

**Lemma 2 (termination).** Part (b) holds.

*Proof.* $k$ starts at $k_{\max}$, and line L11 sets it only to values at most $k_{\max}$. Each round increases $t$ by 1, so after $k_{\max}$ rounds $t \ge k_{\max} \ge k$ and the test of line L2 fails. $\square$

**Lemma 3 (the adaptive count does not stop too early).** At each test of line L2, $k \ge \min(k_{\max}, k(m^*/n))$.

*Proof.* For $0 < w < 1$, $\log(1 - w^s)$ is negative and decreases as $w$ grows, so $\log(1 - p) / \log(1 - w^s)$ is positive and does not increase; hence $k(w)$ does not increase in $w$. By Lemma 1, $|I^*| \le m^*$ at all times, so the value $w = |I^*|/n$ of line L10 is at most $m^*/n$, and line L11 sets $k = \min(k_{\max}, k(w)) \ge \min(k_{\max}, k(m^*/n))$. Before the first update, $k = k_{\max}$. $\square$

**Proof of (c).** Let $K = \lceil \log(1 - p) / \log(1 - q) \rceil$. From $q \ge (m^*/n)^s$ we get $K \le k(m^*/n)$, and $K \le k_{\max}$ by assumption. By Lemma 3, the loop does not stop before round $K$ unless $|I^*| = m^*$ already. The samples are independent, so the probability that none of the first $K$ samples is a subset of $I$ is $(1 - q)^K \le 1 - p$, by the choice of $K$. If one of them is a subset of $I$, its model has a consensus set of size $m^*$ by assumption, and by Lemma 1 $I^*$ has size $m^*$ from that round on. Line L13 changes the model but not $I^*$, and line L14 returns $I^*$. $\square$

**Remark (sampling without replacement).** If the $s$ items of a sample were drawn with replacement, $q = (m^*/n)^s$ and the condition $q \ge (m^*/n)^s$ holds with equality. Line L4 draws $s$ distinct items, so $q = \binom{m^*}{s} / \binom{n}{s} = \prod_{j=0}^{s-1} \frac{m^* - j}{n - j}$, and each factor is at most $m^*/n$. Then $q \le (m^*/n)^s$, part (c) does not apply as stated, and the success probability after $k(m^*/n)$ rounds is $1 - (1 - q)^{k(m^*/n)}$, a little less than $p$. For the example of the page, $q = \binom{5}{2} / \binom{8}{2} = 10/28 \approx 0.357$ against $(5/8)^2 = 0.390625$. The gap shrinks as $n$ grows with $m^*/n$ fixed.

**Remark (noise).** Without noise, any sample of $s$ distinct points on one line gives that line, and the assumption of (c) holds. With noise, two close inliers can give a line far from the truth, so the assumption fails and the count of line L11 is optimistic. This is a statement about the model of the data, not a theorem about noisy data.
