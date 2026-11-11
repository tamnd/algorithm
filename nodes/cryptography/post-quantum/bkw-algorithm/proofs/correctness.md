---
title: The BKW reduction keeps the parity relation and squares the bias at each level
proves: [correctness]
status: full
---

We use the notation of the page. A sample is $(x, y)$ with $x \in \mathbb{F}_2^n$, $n = ab$, and $y = \langle x, s \rangle + e$, where $e \in \mathbb{F}_2$ is 1 with probability $\tau < 1/2$. The bias of a bit $e$ is $\delta(e) = \Pr[e = 0] - \Pr[e = 1]$, so one original error has bias $\delta = 1 - 2\tau$. Block $i$ of $x$ is the $b$ coordinates $(i - 1)b + 1, \ldots, ib$.

**Lemma 1 (one reduction step).** Let $(x, y)$ and $(x', y')$ satisfy $y = \langle x, s \rangle + e$ and $y' = \langle x', s \rangle + e'$, and let them agree on block $i$. Then $(x + x', y + y')$ is zero on block $i$, agrees with both inputs on every block that was already zero in both, and satisfies $y + y' = \langle x + x', s \rangle + (e + e')$.

*Proof.* Over $\mathbb{F}_2$, equal coordinates add to 0, and two zero coordinates add to 0. The inner product is linear, so $y + y' = \langle x, s \rangle + \langle x', s \rangle + e + e' = \langle x + x', s \rangle + (e + e')$. $\square$

**Lemma 2 (the invariant).** Fix a round $t$ of line L2, and assume that the bits of blocks $t + 1, \ldots, a$ of $s$ are correct when the round starts. After line L3, every sample in $R$ is zero outside blocks $1, \ldots, t$ and satisfies $y = \langle x, s \rangle + e$ with its original error $e$. After $k$ passes of the loop in line L4, every sample in $R$ is zero on blocks $1, \ldots, k$ and outside blocks $1, \ldots, t$, and is the sum of the samples of line L3 over a set $T$ of at most $2^k$ original samples, so its error is $\sum_{i \in T} e_i$.

*Proof.* Line L3 removes the part $x_{\text{high}}$ of $x$ on blocks $t + 1, \ldots, a$ and adds $\langle x_{\text{high}}, s_{\text{high}} \rangle$ to $y$. Since $s_{\text{high}}$ is correct, $y + \langle x_{\text{high}}, s_{\text{high}} \rangle = \langle x_{\text{low}}, s \rangle + e$. For the loop, use induction on $k$. Lines L5 and L6 replace each sample except the first in its group by its sum with the first sample of the group, which agrees with it on block $k$. By Lemma 1 the sum is zero on block $k$, stays zero where both were zero, and keeps the relation. If the two summands are the sums over sets $T_1$ and $T_2$, each of size at most $2^{k-1}$, then over $\mathbb{F}_2$ their sum is the sum over the symmetric difference of $T_1$ and $T_2$, because a sample that occurs twice cancels. This set has at most $2^k$ elements. If it is empty, then $x = 0$ and $y = 0$, and the sample never votes in line L8. $\square$

If no original sample occurs in both $T_1$ and $T_2$ at any step, then $|T| = 2^k$ exactly. A shared original sample can only make $T$ smaller.

**Theorem 1 (noiseless case).** If $\tau = 0$ and, in every round $t$, every unit vector of block $t$ appears in $R$ at line L8, then BKW returns $s$.

*Proof.* Use induction on the rounds, from $t = a$ down to $t = 1$. Assume blocks $t + 1, \ldots, a$ are correct. After line L4, Lemma 2 shows that every sample is zero on blocks $1, \ldots, t - 1$ and outside block $t$, and has $y = \langle x, s \rangle$ with no error, since a sum of zero errors is zero. A sample with $x = e_j$ for a position $j$ in block $t$ has $y = s_j$. So every vote in line L8 is $s_j$, and the majority is $s_j$. Block $t$ is then correct, which is the induction step. In the round $t = 1$ there is no reduction, and the same argument applies. $\square$

**Lemma 3 (the bias squares).** If $e_1, \ldots, e_m$ are independent bits with biases $\delta_1, \ldots, \delta_m$, then $\delta(e_1 + \cdots + e_m) = \delta_1 \cdots \delta_m$. In particular, the error of a sample of Lemma 2 at level $k$ has bias $\delta^{|T|} \ge \delta^{2^k}$, with equality when $|T| = 2^k$. So the bias at level $k$ is the square of the bias at level $k - 1$.

*Proof.* Write $\delta(e) = \mathbb{E}[(-1)^e]$. Then $(-1)^{e_1 + \cdots + e_m} = \prod_i (-1)^{e_i}$, and the expectation of a product of independent variables is the product of the expectations. The errors of distinct original samples are independent, and $0 < \delta \le 1$, so $\delta^{|T|} \ge \delta^{2^k}$. Also $\delta^{2^k} = (\delta^{2^{k-1}})^2$. $\square$

**Theorem 2 (noisy case, fresh samples).** Assume that, in round $t$, the votes for each position $j$ come from $V$ reduced samples whose errors are independent. This holds when the $2^{t-1}$ original samples behind each vote are distinct from those behind every other vote, as in the version of Blum, Kalai and Wasserman that draws new samples for each vote. Then the majority in line L8 is wrong with probability at most $\exp(-V \delta^{2^{t}} / 2)$. If $V \ge 2 \delta^{-2^{a}} \ln(n / \varepsilon)$ for every position, BKW returns $s$ with probability at least $1 - \varepsilon$.

*Proof.* By Lemma 2, a vote for $s_j$ equals $s_j + E$, where $E$ is a sum of at most $2^{t-1}$ original errors, and by Lemma 3, $E$ has bias at least $\beta = \delta^{2^{t-1}}$. So each vote is wrong with probability at most $(1 - \beta)/2$. The majority is wrong only if at least half of the $V$ independent votes are wrong. The mean number of wrong votes is at most $V(1 - \beta)/2$, which is at least $V\beta/2$ below $V/2$. By the Hoeffding inequality, the chance of a deviation of $V\beta/2$ above the mean is at most $\exp(-2 (V\beta/2)^2 / V) = \exp(-V\beta^2/2) = \exp(-V \delta^{2^{t}} / 2)$. Since $t \le a$, $\delta^{2^t} \ge \delta^{2^a}$, so the bound on $V$ makes each error probability at most $\varepsilon / n$. Round $t$ uses only the bits found in earlier rounds, so if all $n$ votes are right, Theorem 1's induction goes through. A union bound over the $n$ positions gives the claim. $\square$

**The shared batch.** The code with this page uses one batch of samples for all rounds and all votes. Many reduced samples then share a representative, so their errors are not independent, and Theorem 2 does not apply as stated. Lemma 2, Lemma 3 for each single vote, and Theorem 1 still hold. The shared batch is a heuristic; it works well on the toy sizes of the tests, but its failure rate is not covered by this proof.

$\blacksquare$
