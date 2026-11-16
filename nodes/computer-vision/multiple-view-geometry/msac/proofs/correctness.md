---
title: MSAC keeps the sampled model of least truncated quadratic cost and finds a least-cost model with high probability under the sampling assumptions
proves: [correctness]
status: full
---

We use the notation of the page. $D$ has $n$ items, a minimal sample has $s \le n$ distinct items, $\rho(r) = \min(r^2, T^2)$ and $C(\theta) = \sum_i \rho(r(\theta, x_i))$. The minimal solver, the residual and the refit are correct subroutines, and the model of computation is the real RAM.

**Claim.** (a) At each test of line L2, $\theta^*$ has the least cost among the models of the samples drawn so far, $C^* = C(\theta^*)$, and $I^*$ is the set of items with $r(\theta^*, x)^2 \le T^2$; if no sample gave a model, $C^* = \infty$. (b) The loop ends after at most $k_{\max}$ rounds. (c) Let $\theta_{\min}$ be a model of least cost among all models the solver can return, let $I = \{x : r(\theta_{\min}, x) \le T\}$, assume that every sample inside $I$ gives the model $\theta_{\min}$, and that the samples are independent, and let $q$ be the probability that one sample is a subset of $I$. If the loop runs at least $K$ rounds, then $C^* = C(\theta_{\min})$ at the end with probability at least $1 - (1 - q)^K$.

**Lemma 1 (invariant).** Part (a) holds.

*Proof.* Before the first round, no model is drawn and $C^* = \infty$. In a round, either line L6 skips the sample and nothing changes, or lines L7 and L8 compute $C = C(\theta)$ for the new model, since $\min(e_i, T^2) = \rho(r(\theta, x_i))$ when $e_i = r(\theta, x_i)^2$. Line L9 replaces $\theta^*$ exactly when $C < C^*$, so after line L10 $C^*$ is the least cost among the old models and the new one. Line L11 recomputes $I^*$ from the residuals of the new $\theta^*$, so $I^*$ belongs to $\theta^*$. $\square$

**Lemma 2 (termination).** Part (b) holds.

*Proof.* $k$ starts at $k_{\max}$, and line L12 sets it only to values at most $k_{\max}$. The value of $k$ can go up or down, but each round increases $t$ by 1, so after $k_{\max}$ rounds $t \ge k_{\max} \ge k$ and the test of line L2 fails. $\square$

**Proof of (c).** The samples are independent, so the probability that none of the first $K$ samples is a subset of $I$ is $(1 - q)^K$. If one of them is a subset of $I$, it gives $\theta_{\min}$ by assumption, and by Lemma 1 $C^* \le C(\theta_{\min})$ from that round on. No sampled model has a smaller cost than $\theta_{\min}$, so $C^* = C(\theta_{\min})$. The refit of line L14 changes the returned model but not $C^*$. $\square$

**Remark (why the stopping rule is a heuristic for MSAC).** In RANSAC, the inlier ratio of line L12 never exceeds the ratio of the best model, so the rule never stops early under its assumptions. In MSAC, the model of least cost so far can have more inliers than $\theta_{\min}$. Example: with $T = 1$, a model with 6 inliers at residual 0.9 each and 4 outliers costs $6(0.81) + 4 = 8.86$, and a model with 5 inliers at residual 0 and 5 outliers costs $5$. The first has more inliers and a higher cost. If the first is the best so far, the rule uses $w = 0.6$ instead of $0.5$ and can stop before the count that $\theta_{\min}$ needs. So for MSAC, the count of line L12 is a heuristic, not a bound.

**Remark (ties).** The test of line L9 is strict, so among models of equal cost the first one found is kept. In the example of the page, the lines $y = 0.1$ and $y = 0$ have the same inliers but costs 0.155 and 0.145, so MSAC keeps $y = 0$ even though it is found second, while RANSAC keeps $y = 0.1$.
