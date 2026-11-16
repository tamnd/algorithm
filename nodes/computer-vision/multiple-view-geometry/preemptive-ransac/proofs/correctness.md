---
title: Preemptive RANSAC returns the best survivor by accumulated score after a number of scorings fixed in advance
proves: [correctness]
status: full
---

We use the notation of the page. There are $N \ge 1$ observations in the random order $o_1, \ldots, o_N$ of line L1, $M \ge 1$ hypotheses and the non-increasing preemption function $f(i) = \lfloor M 2^{-\lfloor i/B \rfloor} \rfloor$ with $B \ge 1$. The model of computation is the real RAM, and one scoring is one evaluation of $\rho(o, h)$.

**Claim.** (a) At each test of line L5, every $h \in H$ has $L(h) = \sum_{j < i} \rho(o_j, h)$, and $|H| = \min(M, f(i-1))$ for $i \ge 3$, $|H| = M$ for $i = 2$. (b) The loop ends, and the returned hypothesis has the least accumulated score in $H$. (c) The number of scorings is $M + \sum_{i=2}^{i^*} \min(M, f(i))$, where $i^*$ is the last $i \le N$ with $f(i) \ge 2$ (and the sum is empty if there is none), so it does not depend on the data or on the random order. It is at most $2BM$. (d) If $f(i) \ge M$ for all $i \le N$, the result is a hypothesis of least total score $\sum_{j=1}^N \rho(o_j, h)$ over all $M$ hypotheses.

**Lemma 1 (invariant).** Part (a) holds.

*Proof.* At $i = 2$, line L3 has set $L(h) = \rho(o_1, h)$ for all $M$ hypotheses. Suppose the claim holds at the test of line L5 for some $i$ and the loop does not return. Line L6 keeps a subset of $H$ and does not change $L$, and after it $|H| = \min(|H|, f(i))$. Since $f$ does not increase, and $|H| \le M$, this is $\min(M, f(i))$. Line L7 adds $\rho(o_i, h)$ to $L(h)$ for every kept $h$, so $L(h) = \sum_{j \le i} \rho(o_j, h)$. Line L8 raises $i$ by 1, and the claim holds at the next test. $\square$

**Lemma 2 (termination and result).** Part (b) holds.

*Proof.* Each pass of the loop that does not return raises $i$ by 1, and line L5 returns once $i > N$. So the loop runs at most $N - 1$ passes. Line L5 returns a hypothesis of least $L(h)$ in $H$, which by Lemma 1 is the least accumulated score among the survivors. $H$ is not empty: it starts with $M \ge 1$ hypotheses, and line L6 only runs when $f(i) \ge 2$, so it keeps at least 2. $\square$

**Lemma 3 (count).** Part (c) holds.

*Proof.* Line L3 makes $M$ scorings. A pass of the loop at index $i$ reaches line L7 exactly when $i \le N$ and $f(i) \ge 2$, and then makes $|H| = \min(M, f(i))$ scorings by Lemma 1. Since $f$ does not increase, the passes that reach line L7 are those with $2 \le i \le i^*$. None of these quantities depends on the scores. For the bound, $\min(M, f(i)) \le M 2^{-q}$ with $q = \lfloor i/B \rfloor$, and at most $B$ indices $i$ share a value of $q$. If $B \ge 2$, the indices $i \ge 2$ with $q = 0$ are $2, \ldots, B - 1$, so the count is at most $M + (B - 2) M + \sum_{q \ge 1} B M 2^{-q} = (2B - 1) M \le 2BM$. If $B = 1$, then $q = i \ge 2$, and the count is at most $M + \sum_{q \ge 2} M 2^{-q} = \frac{3}{2} M \le 2BM$. $\square$

**Lemma 4 (no preemption).** Part (d) holds.

*Proof.* If $f(i) \ge M$ for all $i \le N$, then line L6 never removes a hypothesis, since $|H| \le M \le f(i)$, and line L5 returns only at $i = N + 1$ (note $f(i) \ge M \ge 2$ if $M \ge 2$; if $M = 1$ the single hypothesis is the answer). By Lemma 1, $L(h)$ is then the total score over all $N$ observations for every one of the $M$ hypotheses, and line L5 returns one of least total score. $\square$

**Remark (what is not proved).** With preemption, a hypothesis of least total score can be dropped at a cut when its partial score on the first observations is worse than the partial scores of others. The example of the page with the seed 3 shows this. Nistér analyzes the probability of such losses under a simple model of inliers and outliers; the algorithm itself gives no guarantee that the best hypothesis survives.
