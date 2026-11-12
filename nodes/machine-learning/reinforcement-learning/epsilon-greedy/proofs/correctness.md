---
title: Epsilon-greedy computes the empirical means, has linear regret with a constant rate, and logarithmic regret with the decaying rate
proves: [correctness]
status: sketch
---

We use the pseudocode of the page and the notation of the [multi-armed bandit](/multi-armed-bandit/): $K$ arms, horizon $n$, means $\mu_i$, gaps $\Delta_i = \mu^* - \mu_i$, and $T_i(n)$ the number of pulls of arm $i$. The rewards are in $[0,1]$.

**Claim 1 (the estimates).** Before round $t$, for each arm $i$, $N[i] = T_i(t-1)$ and $S[i]$ is the sum of the rewards of arm $i$ in rounds $1, \ldots, t-1$. So $Q[i] = S[i]/N[i]$ is the empirical mean of arm $i$ when $N[i] > 0$.

*Proof.* Induction on $t$. Line L1 sets all counts and sums to 0, which is right for $t = 1$. In round $t$ exactly one arm $A$ is pulled (line L4 or line L5 picks it), and line L7 adds 1 to $N[A]$ and the reward to $S[A]$. The other arms are not pulled and do not change. $\square$

**Claim 2 (a constant rate gives linear regret).** If $\varepsilon_t = \varepsilon$ for all $t$, then for each $n$,

$$R_n \ge \frac{\varepsilon\, n}{K} \sum_{i=1}^{K} \Delta_i .$$

*Proof.* In each round the test of line L3 succeeds with probability $\varepsilon$, independent of the past, and then line L4 picks arm $i$ with probability $1/K$. So $\Pr[A_t = i] \ge \varepsilon / K$ for each $i$ and $t$, and $\mathbb{E}[T_i(n)] \ge \varepsilon n / K$. The regret decomposition $R_n = \sum_i \Delta_i \mathbb{E}[T_i(n)]$ gives the claim. $\square$

The bound is linear in $n$ as soon as one gap is positive. The same argument gives an upper bound: an arm with a positive gap is pulled at most $\varepsilon n / K$ times in expectation by line L4, plus the times that line L5 picks it.

**Claim 3 (the greedy rule can have linear regret).** Let $\varepsilon_t = 0$ for all $t$, $K = 2$ and Bernoulli arms with $\mu_1 > \mu_2 > 0$ and $\mu_1 < 1$. Then $R_n \ge (1 - \mu_1)\,\mu_2\,(\mu_1 - \mu_2)(n - 2)$ for $n \ge 2$.

*Proof.* With $\varepsilon = 0$, line L5 runs in each round. An arm never pulled has $Q = +\infty$, so round 1 pulls arm 1 and round 2 pulls arm 2. Let $E$ be the event that arm 1 pays 0 in round 1 and arm 2 pays 1 in round 2. $\Pr[E] = (1 - \mu_1)\mu_2 > 0$. On $E$, after round 2 we have $Q[1] = 0$ and $Q[2] = 1$. Arm 1 is pulled again only if $Q[2] \le Q[1] = 0$, but $S[2] \ge 1$ from then on, so $Q[2] > 0$. So on $E$ arm 2 is pulled in all rounds $3, \ldots, n$, and $T_2(n) = n - 1 \ge n - 2$. Hence $\mathbb{E}[T_2(n)] \ge \Pr[E](n-2)$, and the regret decomposition gives the claim. $\square$

**Claim 4 (the decaying rate gives logarithmic regret).** Let $\varepsilon_t = \min(1, cK/(d^2 t))$ with $c > 0$ and $0 < d \le \min_{i:\Delta_i>0} \Delta_i$. The rounds split into the exploration rounds (line L4) and the greedy rounds (line L5).

*Exploration part, full proof.* Let $t_0 = \lceil cK/d^2 \rceil$. The expected number of exploration rounds that pull arm $i$ is

$$\sum_{t=1}^{n} \frac{\varepsilon_t}{K} \le \frac{t_0}{K} + \sum_{t=t_0+1}^{n} \frac{c}{d^2 t} \le \frac{t_0}{K} + \frac{c}{d^2}\ln n ,$$

since $\sum_{t=t_0+1}^{n} 1/t \le \int_{t_0}^{n} dx/x \le \ln n$. With $t_0 \le cK/d^2 + 1$, this part of the regret is at most $\sum_i \Delta_i \big(\frac{c}{d^2}(1 + \ln n) + \frac1K\big)$, which is $O(\log n)$.

*Greedy part, proof sketch.* Line L5 picks a suboptimal arm $j$ only if the empirical mean of $j$ is at least $\mu_j + \Delta_j/2$ or the empirical mean of an optimal arm is at most $\mu^* - \Delta_j/2$. Up to round $t$, each arm has received about $\frac{1}{K}\sum_{s \le t} \varepsilon_s \ge \frac{c}{d^2}\ln\frac{t d^2}{cK}$ exploration pulls. A Bernstein bound shows that the number of these pulls is at least half its mean, except with a probability that is $O(t^{-1-\epsilon})$ when $c$ is large enough. On that event each arm has $s \ge \frac{c}{2d^2}\ln\frac{t d^2}{cK}$ samples, and the [Hoeffding inequality](/hoeffding-inequality/) bounds each of the two deviation events by $\exp(-2s(\Delta_j/2)^2) \le \exp(-s d^2/2) \le (\frac{t d^2}{cK})^{-c/4}$, which is $O(t^{-1-\epsilon})$ for $c > 4$. Auer, Cesa-Bianchi and Fischer carry out these steps in the proof of their Theorem 3 (Machine Learning 47, 2002, Section 3). The result is that the probability that round $t$ pulls a suboptimal arm $j$ is at most $\frac{c}{d^2 t} + o(1/t)$ for $c > 5$. Summed over $t$, the greedy part adds $O(\log n)$ to $\mathbb{E}[T_j(n)]$, and with the exploration part, $\mathbb{E}[T_j(n)] = O(\frac{c}{d^2}\ln n)$. $\square$

The first term of their bound, $\frac{c}{d^2 t}$, is the exploration term above, so with $c > 5$ the regret is dominated by the forced exploration: about $\frac{c}{d^2}\ln n$ pulls of each suboptimal arm. If $d$ is larger than the true smallest gap, the hypothesis fails and the guarantee is lost.
