---
title: MBR decoding returns a candidate of least risk, reduces to MAP under the 0-1 loss, and is consistent with samples
proves: [correctness]
status: full
---

We use the notation of the page: candidates $\mathcal{H} = (h_1, \ldots, h_H)$ in a fixed order, evidence $(y_j, w_j)$ for $j = 1, \ldots, N$ with $w_j \ge 0$, a loss $\ell \ge 0$, and the risk $R(h) = \sum_j w_j \ell(h, y_j)$. We assume exact arithmetic for the sums.

**Theorem 1 (the decision).** MBR-DECODE returns $(h_i, R(h_i))$, where $i$ is the smallest index with $R(h_i) = \min_{h \in \mathcal{H}} R(h)$.

*Proof.* The invariant after the pass for $h_i$ of the loop of line L2 is: $r^* = \min_{i' \le i} R(h_{i'})$, and best is the first candidate among $h_1, \ldots, h_i$ that attains it. It holds before the loop with $r^* = +\infty$ (line L1), since every risk is finite. Line L3 computes $R(h_i)$ exactly. Line L4 replaces the pair only on a strict decrease, so a later candidate with the same risk does not replace an earlier one. After the last pass the invariant gives the claim, and line L5 returns it. $\square$

**Lemma 2 (scaling).** For any $c > 0$, the evidence $(y_j, c w_j)$ gives the same candidate.

*Proof.* Every risk is multiplied by $c$, which keeps the order of the risks and their ties. $\square$

So weights that are proportional to the probabilities, for example $\exp$ of unnormalized log scores, give the same decision as the normalized probabilities. The code still normalizes in log space, because the unnormalized exponentials can all underflow to 0, which would make every risk 0.

**Theorem 3 (MAP as a special case).** Let the evidence be the full distribution, $w_y = p(y \mid x)$ for every output $y$, let $\mathcal{H}$ be the set of all outputs, and let $\ell(h, y) = 0$ if $h = y$ and 1 otherwise. Then $R(h) = 1 - p(h \mid x)$, and MBR returns a most probable output.

*Proof.* $R(h) = \sum_{y \ne h} p(y \mid x) = 1 - p(h \mid x)$, because the probabilities sum to 1. Minimizing $1 - p(h \mid x)$ maximizes $p(h \mid x)$. $\square$

With $N$ samples as evidence and the distinct samples as candidates, the 0-1 risk of a candidate is $1 - (\text{its count}) / N$, so sampling based MBR under the 0-1 loss returns the most frequent sample, the first one to appear on ties. The test checks this.

**Theorem 4 (unbiased and consistent risk estimates).** Let $y_1, y_2, \ldots$ be independent samples from $p(\cdot \mid x)$, and let $\hat R_N(h) = \frac{1}{N} \sum_{j=1}^{N} \ell(h, y_j)$. If $\ell$ is bounded by $B$, then for each fixed $h$, $E[\hat R_N(h)] = R(h)$, the true risk under $p$, and $P(|\hat R_N(h) - R(h)| \ge \varepsilon) \le 2 \exp(-2 N \varepsilon^2 / B^2)$.

*Proof.* Each term $\ell(h, y_j)$ has mean $\sum_y p(y \mid x) \ell(h, y) = R(h)$, so the average has the same mean. The terms are independent and lie in $[0, B]$, so Hoeffding's inequality gives the bound. $\square$

**Corollary 5 (the sampled decision).** Let $\mathcal{H}$ be a fixed finite candidate set with a unique minimizer $h^*$ of the true risk, and let $\Delta > 0$ be the gap between $R(h^*)$ and the second smallest risk. Then MBR-DECODE with the evidence $(y_j, 1/N)$ returns $h^*$ with probability at least $1 - 2 H \exp(-N \Delta^2 / (2 B^2))$.

*Proof.* If every $\hat R_N(h)$ is within $\Delta / 2$ of $R(h)$, then $\hat R_N(h^*) < R(h^*) + \Delta/2 \le R(h) - \Delta/2 < \hat R_N(h)$ for every $h \ne h^*$, and Theorem 1 returns $h^*$. Apply Theorem 4 with $\varepsilon = \Delta / 2$ to each of the $H$ candidates and take a union bound. $\square$

When the candidates are the distinct samples themselves, the candidate set is random; the corollary then applies to the decision conditioned on the candidate set, as long as the evidence samples are drawn independently of it. With the same samples as candidates and evidence, each candidate also appears in its own evidence, which adds a bias of order $1/N$ to its estimated risk for a loss with $\ell(h, h) = 0$.

**What is not claimed.** The theorems say that the decoder computes the decision it defines. They do not say that the decision is a better output under any human judgment; that is a measurement.
