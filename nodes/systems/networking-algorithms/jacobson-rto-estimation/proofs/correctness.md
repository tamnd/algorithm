---
title: The RFC 6298 estimator averages the samples, adapts to their spread and catches a longer path by doubling
proves: [correctness]
status: full
---

**Setting.** The estimator gets the samples $R_1, R_2, \ldots \ge 0$. Line L3 and line L4 set $\mathrm{SRTT}_1 = R_1$ and $\mathrm{RTTVAR}_1 = R_1/2$. For $n \ge 2$, with $d_n = |\mathrm{SRTT}_{n-1} - R_n|$, line L5 and line L6 set

$$\mathrm{RTTVAR}_n = \tfrac34 \mathrm{RTTVAR}_{n-1} + \tfrac14 d_n, \qquad \mathrm{SRTT}_n = \tfrac78 \mathrm{SRTT}_{n-1} + \tfrac18 R_n.$$

Line L7 sets $\mathrm{RTO}_n = \mathrm{SRTT}_n + \max(G, 4\,\mathrm{RTTVAR}_n)$ with $G \ge 0$, and line L8 clamps it to $[L, U]$, where $L$ is the lower bound (1 s) and $U$ the upper bound (at least 60 s). A sample is *late* if it is larger than the RTO that was in force when its segment was sent; then the timer would have expired before the ACK came.

**Claim 1 (SRTT is a weighted mean).** For $n \ge 1$,

$$\mathrm{SRTT}_n = \left(\tfrac78\right)^{n-1} R_1 + \sum_{i=2}^{n} \tfrac18 \left(\tfrac78\right)^{n-i} R_i,$$

and the weights are positive with sum 1. So $\min_i R_i \le \mathrm{SRTT}_n \le \max_i R_i$.

*Proof.* Induction on $n$. For $n = 1$ the formula is $R_1$. Line L6 multiplies each old weight by $7/8$ and gives $R_n$ the weight $1/8$, which is the formula for $n$. The weights sum to $(7/8)^{n-1} + \frac18 \sum_{j=0}^{n-2} (7/8)^j = (7/8)^{n-1} + 1 - (7/8)^{n-1} = 1$. A convex combination lies between the smallest and the largest value. $\square$

**Claim 2 (RTTVAR is a weighted mean of the deviations).** $\mathrm{RTTVAR}_n = (3/4)^{n-1} R_1/2 + \sum_{i=2}^{n} \frac14 (3/4)^{n-i} d_i \ge 0$. The proof is the same as for Claim 1, with $R_1/2$ as the first term. In particular, if $R_i = R$ for all $i$, then $\mathrm{SRTT}_n = R$, each $d_i = 0$, and $\mathrm{RTTVAR}_n = (3/4)^{n-1} R/2$. So the unclamped RTO is $R + \max(G, 2R(3/4)^{n-1})$, which falls to $R + G$ geometrically. On a steady path the timeout approaches the round-trip time plus one clock tick. $\square$

**Claim 3 (one jump raises the RTO above the jump).** Let $R_n > \mathrm{SRTT}_{n-1}$ and $d = R_n - \mathrm{SRTT}_{n-1}$. Then the unclamped $\mathrm{RTO}_n$ is larger than $R_n$ when $d > 0$, so if the next sample is again $R_n$, and the clamp does not cut the RTO, it is not late.

*Proof.* Line L5 uses the old SRTT, so $\mathrm{RTTVAR}_n \ge d/4$ and $4\,\mathrm{RTTVAR}_n \ge d$. Line L6 gives $\mathrm{SRTT}_n = \mathrm{SRTT}_{n-1} + d/8$. So $\mathrm{RTO}_n \ge \mathrm{SRTT}_{n-1} + d/8 + d = R_n + d/8 > R_n$. $\square$

If line L6 ran before line L5, the deviation would be $|\mathrm{SRTT}_n - R_n| = 7d/8$, and the bound would become $\mathrm{SRTT}_{n-1} + d/8 + 7d/8 = R_n$, with no margin. This is the reason for the order in RFC 6298, rule 2.3.

**Claim 4 (backoff catches a longer path).** Assume that the round-trip time grows to $D$ with $D < U$, and that every segment that is sent now times out while $\mathrm{RTO} \le D$. Line L9 doubles the RTO at each timeout, so after $j$ timeouts in a row $\mathrm{RTO} = \min(U, 2^j \mathrm{RTO})$. Since $\mathrm{RTO} \ge L > 0$, after at most $\lceil \log_2 (D/L) \rceil + 1$ timeouts the RTO is larger than $D$, and the next transmission is acknowledged before the timer expires. With [Karn's algorithm](/karn-algorithm/), the sample of that segment is not used, but the next segment that is sent once gives a sample near $D$, and Claims 1 and 3 then move the estimate toward $D$. $\square$

**Claim 5 (fewer late samples than RFC 793).** On the periodic trace of four samples of $0.1$ s and one of $0.4$ s, repeated 20 times, the RFC 793 rule with $\alpha = 0.9$ and $\beta = 2$ keeps $\mathrm{SRTT}$ between $0.1$ and about $0.174$, so $\beta\,\mathrm{SRTT} < 0.35 < 0.4$ and each of the 20 spikes is late. In the RFC 6298 rule without the 1 s lower bound, each spike adds at least a quarter of its deviation to RTTVAR (Claim 3), and RTTVAR decays only by the factor $(3/4)^4 \approx 0.32$ over the four short samples. The exact computation in the tests with fractions shows that only the spikes at the indices 4, 9 and 14 are late; after these three, the RTO stays above $0.4$. $\blacksquare$
