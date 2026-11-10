---
tag: VVN821
kind: theorem
slug: online-restricted-assignment-lower-bound
name: Omega(log m) lower bound for restricted assignment
aliases:
- Azar-Naor-Rom lower bound
- lower bound for online restricted assignment
area: online-and-streaming/online-scheduling
level: advanced
summary: "Every deterministic online algorithm for restricted assignment has ratio at least ceil(log2(m + 1)), and every randomized one at least ln m against an oblivious adversary, already for unit jobs."
prereqs: [online-restricted-assignment-load-balancing, adversary-argument, yao-minimax-principle]
see_also: [online-restricted-assignment-load-balancing, greedy-restricted-assignment, restricted-assignment, unrelated-machines, yao-minimax-principle, oblivious-adversary, harmonic-series, online-makespan-lower-bound]
sources:
  - paper: "Y. Azar, J. Naor and R. Rom, The competitiveness of on-line assignments, Journal of Algorithms 18(2), 1995"
    title: Azar, Naor and Rom 1995
    locator: the deterministic lower bound of about log2 m and the randomized lower bound ln m for online assignment with restricted sets (SODA 1992 version)
  - paper: "Yossi Azar, On-line load balancing, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Azar 1998, survey chapter
    locator: the section on the restricted assignment model, the lower bounds
  - paper: "Fu-Hong Liu, Hsiang-Hsuan Liu and Prudence W. H. Wong, Greedy is optimal for online restricted assignment and smart grid scheduling for unit size jobs, WAOA 2019"
    title: Liu, Liu and Wong 2019
    locator: the result that greedy is an optimal deterministic online algorithm for restricted assignment with unit jobs
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 12 (load balancing), the lower bound for restricted assignment
---

This theorem says that [online restricted assignment](/online-restricted-assignment-load-balancing/) has no algorithm with a constant competitive ratio. A deterministic algorithm can be forced to a ratio of $\lceil \log_2 (m + 1) \rceil$, and a randomized one to $\ln m$ against an [oblivious adversary](/oblivious-adversary/), with jobs of size $1$ only. The deterministic proof is an [adversary argument](/adversary-argument/) that halves a set of machines in each round. The randomized proof hides a random machine and uses [Yao's principle](/yao-minimax-principle/). Since [greedy](/greedy-restricted-assignment/) is $(\lceil \log_2 m \rceil + 1)$-competitive, both bounds are tight up to constants.

## Statement

**Notation.** There are $m$ machines. The request sequence $\sigma$ consists of jobs; job $t$ has size $p_t$ and an eligible set $M_t$. $\mathrm{ALG}(\sigma)$ is the makespan of the online algorithm and $\mathrm{OPT}(\sigma)$ the optimal makespan. An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$; for a randomized algorithm $\mathrm{ALG}(\sigma)$ is replaced by its expectation, and $\sigma$ is fixed in advance by an oblivious adversary.

**Theorem (Azar, Naor and Rom 1995).** Let $m \ge 1$.

1. For every deterministic online algorithm there is a sequence of unit jobs with $\mathrm{OPT}(\sigma) = 1$ and $\mathrm{ALG}(\sigma) \ge \lfloor \log_2 m \rfloor + 1 = \lceil \log_2 (m + 1) \rceil$. So its competitive ratio is at least $\lceil \log_2 (m + 1) \rceil$.
2. For every randomized online algorithm there is a sequence of $m$ unit jobs with $\mathrm{OPT}(\sigma) = 1$ and $\mathbb{E}[\mathrm{ALG}(\sigma)] \ge H_m = 1 + \frac12 + \cdots + \frac1m$. Since $H_m > \ln m$, its competitive ratio against an oblivious adversary is at least $\ln m$.

Both parts are proved here. Both hold for every additive constant $b$.

## In plain words

For the first part, the opponent picks a group of machines whose size is a power of two and pairs them up. Each pair gets one task that may go to either machine of the pair. The machines that the algorithm used form the next group, which is half as large, and each has one more task. After all the halving rounds, one machine is left with one task per round, and a last task may only go to it. The best plan used the other machine of each pair every time, so no machine got more than one task. For the second part, the opponent removes machines from the allowed set in a random order and hides which machine stays to the end. The algorithm cannot avoid it, and the expected work on that machine grows like the logarithm.

## Proof

**Part 1.** Let $k = \lfloor \log_2 m \rfloor$, so $2^k \le m < 2^{k+1}$, and let $A_0$ be a set of $2^k$ machines. For $r = 1, \ldots, k$ the adversary does round $r$:

- split $A_{r-1}$ into $2^{k-r}$ disjoint pairs, and for each pair $\{a, b\}$ give a unit job with eligible set $\{a, b\}$;
- let $A_r$ be the set of machines that the algorithm chose in this round, one per pair, so $|A_r| = 2^{k-r}$.

After round $k$, $A_k = \{a^*\}$. The adversary gives a last unit job with eligible set $\{a^*\}$.

*The online load.* By induction on $r$, every machine of $A_r$ has load at least $r$ after round $r$. This holds for $r = 0$. A machine of $A_r$ was in $A_{r-1}$, so it had load at least $r - 1$, and in round $r$ it got the job of its pair. So $a^*$ has load at least $k$ after round $k$, and the last job makes it $k + 1$.

*The optimum.* Assign each job of round $r$ to the machine of its pair that the algorithm did not choose. That machine is not in $A_r$, so it is in no pair of a later round, and it gets no other job in any round. Assign the last job to $a^*$, which the algorithm chose in every round. Every machine gets at most one job, so $\mathrm{OPT} = 1$.

Hence $\mathrm{ALG} \ge k + 1 = \lfloor \log_2 m \rfloor + 1$, which equals $\lceil \log_2 (m + 1) \rceil$ because $2^k \le m < 2^{k+1}$ gives $2^k < m + 1 \le 2^{k+1}$. For an additive constant $b$, give all jobs size $\lambda$: then $\mathrm{OPT} = \lambda$ and $\mathrm{ALG} \ge (k + 1)\lambda$, and for large $\lambda$ the inequality $\mathrm{ALG} \le c \cdot \mathrm{OPT} + b$ fails for every $c < k + 1$.

**Part 2.** Let $\pi = (\pi_1, \ldots, \pi_m)$ be a uniformly random order of the machines. The input $\sigma_\pi$ has $m$ unit jobs, and job $t$ has eligible set
$$M_t = \{\pi_t, \pi_{t+1}, \ldots, \pi_m\}.$$
For every $\pi$, $\mathrm{OPT}(\sigma_\pi) = 1$: assign job $t$ to $\pi_t$.

Fix a deterministic online algorithm $D$. Before job $t$, the sets $M_1, \ldots, M_{t-1}$ reveal $\pi_1, \ldots, \pi_{t-1}$, and nothing about the order of the remaining machines. So, given everything that $D$ has seen when job $t$ comes, the machine $\pi_m$ is uniform over the $m - t + 1$ machines of $M_t$, and the choice of $D$ is fixed by what it has seen. Hence $D$ puts job $t$ on $\pi_m$ with probability $\frac1{m - t + 1}$, and

$$\mathbb{E}_\pi[\mathrm{ALG}_D(\sigma_\pi)] \ge \mathbb{E}_\pi[\text{load of } \pi_m] = \sum_{t=1}^{m} \frac1{m - t + 1} = H_m .$$

A randomized online algorithm $R$ is a probability distribution over deterministic algorithms $D$. Exchanging the two expectations,
$$\mathbb{E}_\pi \mathbb{E}_{D \sim R}[\mathrm{ALG}_D(\sigma_\pi)] = \mathbb{E}_{D \sim R} \mathbb{E}_\pi[\mathrm{ALG}_D(\sigma_\pi)] \ge H_m ,$$
so some fixed $\pi$ has $\mathbb{E}_{D \sim R}[\mathrm{ALG}_D(\sigma_\pi)] \ge H_m$, while $\mathrm{OPT}(\sigma_\pi) = 1$. This is the easy direction of Yao's principle. An oblivious adversary chooses this $\sigma_\pi$ in advance. By comparing the sum with the integral of $\frac1x$, $H_m > \int_1^{m+1} \frac{dx}{x} = \ln (m + 1) > \ln m$ ([harmonic series](/harmonic-series/)). The scaling by $\lambda$ handles an additive constant as in Part 1. $\square$

**Small cases.** For $m = 3$, Part 1 uses two machines: one job eligible on both, then one job eligible only on the chosen one, so $\mathrm{ALG} = 2 = \lceil \log_2 4 \rceil$. Part 2 gives $H_3 = \frac{11}{6}$: the expected load of the hidden machine is $\frac13 + \frac12 + 1$, from the three jobs in order. The exact values of $H_m$ for $m = 1, \ldots, 6$ are $1, \frac32, \frac{11}6, \frac{25}{12}, \frac{137}{60}, \frac{49}{20}$.

## Consequences

- **Greedy is nearly optimal.** [Greedy restricted assignment](/greedy-restricted-assignment/) is $(\lceil \log_2 m \rceil + 1)$-competitive. This equals the deterministic bound when $m$ is a power of two. On unit jobs with $\mathrm{OPT} = 1$, the instances of Part 1, greedy has makespan at most $\lfloor \log_2 m \rfloor + 1$, which equals the bound for every $m$.
- **Randomization does not change the order.** The optimal randomized ratio is also $\Theta(\log m)$; the possible gain is at most a factor near $\frac1{\ln 2} \approx 1.44$ for large $m$.
- **Unrelated machines.** Restricted assignment is a special case of [unrelated machines](/unrelated-machines/), so both bounds hold there, and the $O(\log m)$ algorithm of Aspnes et al. is optimal up to a constant.
- **The sets must be adversarial.** If the eligible sets are random, as in the [power of two choices](/power-of-two-choices/), greedy does much better.

## Tightness

Part 1 is exactly tight on unit jobs with $\mathrm{OPT} = 1$, and for general sizes when $m$ is a power of two, by the greedy upper bound. Liu, Liu and Wong (2019) show that greedy is optimal for all unit-job instances (cited). For general sizes and other $m$ the deterministic bounds differ by $1$. Part 2 is tight up to a constant factor; this page does not settle the optimal randomized constant. The construction of Part 2 also gives a deterministic bound, but only $H_m$, which is weaker than Part 1 for large $m$.

## History

Azar, Naor and Rom (1995; SODA 1992) introduced online assignment with restricted sets, motivated by mobile users that can reach only some base stations. They showed that greedy is within one of $\log_2 m$, and proved the deterministic and randomized lower bounds; the randomized bound appears there as $\ln m$. The model became the basic example of online load balancing in the survey of Azar (1998) and in the book of Borodin and El-Yaniv (1998).

## References
