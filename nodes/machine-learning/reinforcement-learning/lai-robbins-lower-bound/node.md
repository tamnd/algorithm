---
tag: TH9RN9
kind: theorem
slug: lai-robbins-lower-bound
name: Lai-Robbins lower bound
aliases:
- asymptotic regret lower bound for bandits
- Lai-Robbins bound
area: machine-learning/reinforcement-learning
level: advanced
summary: "Each consistent bandit policy pulls each suboptimal arm at least about ln n / KL(P_i, P*) times, so its regret is at least a KL constant times ln n."
prereqs: [multi-armed-bandit, regret]
see_also: [ucb1, thompson-sampling, epsilon-greedy, exploration-exploitation-tradeoff, exp3, shannon-entropy, bayes-theorem]
sources:
  - paper: doi:10.1016/0196-8858(85)90002-8
    title: Tze Leung Lai and Herbert Robbins, Asymptotically efficient adaptive allocation rules, Advances in Applied Mathematics 6(1), 1985
    locator: pp. 4 to 22; the lower bound for uniformly good rules in a one-parameter family, and the upper confidence rules that attain it
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Theorem 14.2 (Bretagnolle-Huber inequality); Lemma 15.1 (divergence decomposition); Chapter 16, Section 16.1 and Theorem 16.2 (asymptotic lower bound); Chapter 10 (KL-UCB)
  - paper: doi:10.1023/A:1013689704352
    title: Peter Auer, Nicolo Cesa-Bianchi and Paul Fischer, Finite-time analysis of the multiarmed bandit problem, Machine Learning 47(2-3), 2002
    locator: Section 1 (the Lai-Robbins bound as the target) and Theorem 1 (the UCB1 constant 8 over the gap)
  - paper: arxiv:1205.4217
    title: Emilie Kaufmann, Nathaniel Korda and Remi Munos, Thompson sampling, an asymptotically optimal finite-time analysis, ALT 2012, LNCS 7568
    locator: Theorem 1 (Thompson sampling attains the bound for Bernoulli arms)
---

The Lai-Robbins lower bound says how much exploration a good bandit policy cannot avoid. In a stochastic [multi-armed bandit](/multi-armed-bandit/), a policy is consistent if its [regret](/regret/) is $o(n^a)$ for each $a > 0$ on every instance of the model. Lai and Robbins (1985) proved that each consistent policy pulls each suboptimal arm $i$ at least $(1 - o(1))\ln n/\mathrm{KL}(P_i, P^*)$ times in expectation, where $\mathrm{KL}$ is the relative entropy between the reward law of arm $i$ and that of the best arm. So the regret is at least $\sum_i \Delta_i/\mathrm{KL}(P_i, P^*)$ times $\ln n$, in the limit. Policies that reach this constant are called asymptotically optimal.

## Statement

The model is a family of reward laws, here the Bernoulli laws with means in $(0,1)$, and the class of instances is all $K$-tuples of them. For an instance $\nu$ with means $\mu_1, \ldots, \mu_K$, let $\mu^* = \max_j\mu_j$, $\Delta_i = \mu^* - \mu_i$, and let $T_i(n)$ be the number of pulls of arm $i$ in $n$ rounds. The relative entropy of two Bernoulli laws is

$$\mathrm{kl}(p, q) = p\ln\frac{p}{q} + (1-p)\ln\frac{1-p}{1-q}.$$

A policy is **consistent** if for each instance $\nu$ in the class and each $a > 0$, $R_n(\nu) = o(n^a)$ as $n \to \infty$.

**Theorem** (Lai and Robbins 1985; in this form Lattimore and Szepesvari, Theorem 16.2). For each consistent policy, each instance $\nu$ with means in $(0,1)$, and each arm $i$ with $\Delta_i > 0$,

$$\liminf_{n\to\infty}\frac{\mathbb{E}_\nu[T_i(n)]}{\ln n} \ge \frac{1}{\mathrm{kl}(\mu_i, \mu^*)}, \qquad\text{so}\qquad \liminf_{n\to\infty}\frac{R_n(\nu)}{\ln n} \ge \sum_{i:\Delta_i>0}\frac{\Delta_i}{\mathrm{kl}(\mu_i, \mu^*)}.$$

For a general family, $\mathrm{kl}(\mu_i, \mu^*)$ is replaced by $d_{\inf}(P_i, \mu^*)$, the smallest $\mathrm{KL}(P_i, P')$ over laws $P'$ in the family with mean above $\mu^*$. Lai and Robbins proved the bound for one-parameter families, where $d_{\inf}$ is $\mathrm{KL}(P_i, P^*)$ under regularity conditions, and Burnetas and Katehakis (1996) extended it to the general form.

## In plain words

To be sure that a machine is worse than the best one, you have to play it enough times to tell the two apart. Two machines that pay in very similar ways are hard to tell apart, so you need many plays.

The theorem says that a policy that does well on every set of machines must keep testing each worse machine, and the number of tests must grow with the number of rounds, at the rate of the log of the rounds. If a policy tests less, there is a set of machines on which it fails badly: one where the machine it gave up on is really the best. The constant in front of the log is set by how hard the two machines are to tell apart.

## Proof

Fix a consistent policy, an instance $\nu$, and an arm $i$ with $\Delta_i > 0$. Write $\mathrm{KL}(P, Q) = \sum_\omega P(\omega)\ln\frac{P(\omega)}{Q(\omega)}$ for laws on the same space.

**Step 1 (a hard alternative).** Fix $\varepsilon > 0$. The map $\lambda \mapsto \mathrm{kl}(\mu_i, \lambda)$ is continuous on $(0,1)$, so there is $\lambda \in (\mu^*, 1)$ with $\mathrm{kl}(\mu_i, \lambda) \le \mathrm{kl}(\mu_i, \mu^*) + \varepsilon$. Let $\nu'$ be $\nu$ with the mean of arm $i$ changed to $\lambda$. In $\nu'$ arm $i$ is the unique best arm, and each other arm has gap at least $\lambda - \mu^* > 0$.

**Step 2 (divergence decomposition).** Let $P$ and $P'$ be the laws of the history $H_n = (A_1, X_1, \ldots, A_n, X_n)$ under $\nu$ and $\nu'$, with the same policy. Then $\mathrm{KL}(P, P') = \mathbb{E}_\nu[T_i(n)]\,\mathrm{kl}(\mu_i, \lambda)$ (Lattimore and Szepesvari, Lemma 15.1). *Proof.* The probability of a history is $\prod_t \pi_t(A_t \mid H_{t-1})\,p_{A_t}(X_t)$, where $\pi_t$ is the policy and $p_j$ is the reward law of arm $j$. The policy terms are the same under $\nu$ and $\nu'$, and so are the reward terms of arms other than $i$. So

$$\ln\frac{P(H_n)}{P'(H_n)} = \sum_{t=1}^{n}\mathbb{1}\{A_t = i\}\ln\frac{p_i(X_t)}{p'_i(X_t)}.$$

Given $H_{t-1}$ and $A_t = i$, $X_t$ has law $p_i$, so the conditional expectation of the $t$-th term is $\Pr_\nu[A_t = i \mid H_{t-1}]\,\mathrm{kl}(\mu_i, \lambda)$. Sum over $t$ and take expectations. If the policy uses extra random bits, add them to the history; they have the same law under both instances and add nothing.

**Step 3 (Bretagnolle-Huber).** For laws $P, Q$ on the same space and each event $E$,

$$P(E) + Q(E^c) \ge \tfrac12\exp(-\mathrm{KL}(P, Q))$$

(Lattimore and Szepesvari, Theorem 14.2). *Proof.* $P(E) + Q(E^c) \ge \sum_\omega \min(P(\omega), Q(\omega))$. By the Cauchy-Schwarz inequality, $\big(\sum_\omega\sqrt{PQ}\big)^2 = \big(\sum_\omega\sqrt{\min(P,Q)\max(P,Q)}\big)^2 \le \sum\min(P,Q)\cdot\sum\max(P,Q) \le 2\sum\min(P,Q)$, since $\sum\max(P,Q) \le 2$. By Jensen's inequality for the concave $\ln$, $\ln\sum_{\omega:P>0} P\sqrt{Q/P} \ge \sum P\cdot\frac12\ln(Q/P) = -\frac12\mathrm{KL}(P,Q)$, so $\big(\sum\sqrt{PQ}\big)^2 \ge \exp(-\mathrm{KL}(P,Q))$.

**Step 4 (the two regrets).** Let $E = \{T_i(n) > n/2\}$. On $E$, arm $i$ is pulled more than $n/2$ times, each at cost $\Delta_i$ in $\nu$. On $E^c$, the other arms are pulled at least $n/2$ times, each at cost at least $\lambda - \mu^*$ in $\nu'$. With the regret decomposition $R_n = \sum_j \Delta_j\mathbb{E}[T_j(n)]$, and $\delta = \min(\Delta_i, \lambda - \mu^*)$,

$$R_n(\nu) + R_n(\nu') \ge \frac{n\delta}{2}\big(P(E) + P'(E^c)\big) \ge \frac{n\delta}{4}\exp\big(-\mathbb{E}_\nu[T_i(n)]\,\mathrm{kl}(\mu_i, \lambda)\big).$$

**Step 5 (use consistency).** Rearranged,

$$\mathbb{E}_\nu[T_i(n)] \ge \frac{1}{\mathrm{kl}(\mu_i, \lambda)}\ln\frac{n\delta}{4(R_n(\nu) + R_n(\nu'))}.$$

Both $\nu$ and $\nu'$ are in the class, so for each $a > 0$ there is $C_a$ with $R_n(\nu) + R_n(\nu') \le C_a n^a$ for all large $n$. Then the logarithm is at least $(1-a)\ln n + \ln\frac{\delta}{4C_a}$, and

$$\liminf_{n\to\infty}\frac{\mathbb{E}_\nu[T_i(n)]}{\ln n} \ge \frac{1-a}{\mathrm{kl}(\mu_i, \lambda)} \ge \frac{1-a}{\mathrm{kl}(\mu_i, \mu^*) + \varepsilon}.$$

Let $a \to 0$ and $\varepsilon \to 0$. The bound on the regret follows from the regret decomposition, since $R_n/\ln n = \sum_i\Delta_i\,\mathbb{E}[T_i(n)]/\ln n$ and the liminf of a sum is at least the sum of the liminfs. $\blacksquare$

**Where consistency is used.** Without it the theorem is false: the policy that always pulls arm 1 has zero regret on each instance where arm 1 is best. It fails on the other instances, and consistency rules this out. Step 5 is the only step that uses it.

## Consequences

**The constants, worked out.** For Bernoulli arms, Pinsker's inequality gives $\mathrm{kl}(\mu_i, \mu^*) \ge 2\Delta_i^2$. So the Lai-Robbins coefficient of arm $i$ in the regret, $\Delta_i/\mathrm{kl}(\mu_i,\mu^*)$, is at most $1/(2\Delta_i)$, while the bound of [UCB1](/ucb1/) has $8/\Delta_i$, at least 16 times more.

| means | arm | $\mathrm{kl}(\mu_i, \mu^*)$ | $2\Delta_i^2$ | $\Delta_i/\mathrm{kl}$ | $1/(2\Delta_i)$ | UCB1: $8/\Delta_i$ |
|---|---|---|---|---|---|---|
| 0.9, 0.6, 0.3 | 0.6 | 0.3112 | 0.18 | 0.964 | 1.667 | 26.67 |
| 0.9, 0.6, 0.3 | 0.3 | 1.0326 | 0.72 | 0.581 | 0.833 | 13.33 |
| 0.9, 0.8, 0.7 | 0.8 | 0.0444 | 0.02 | 2.252 | 5.000 | 80.00 |
| 0.9, 0.8, 0.7 | 0.7 | 0.1537 | 0.08 | 1.302 | 2.500 | 40.00 |
| 0.5, 0.4 | 0.4 | 0.0201 | 0.02 | 4.966 | 5.000 | 80.00 |
| 0.99, 0.9 | 0.9 | 0.1445 | 0.0162 | 0.623 | 5.556 | 88.89 |

For the means $(0.9, 0.6, 0.3)$ the regret of each consistent policy is at least about $1.545\ln n$ in the limit; the UCB1 bound is $40\ln n$ plus a constant. Near $\frac12$ Pinsker is almost tight, as in the row $(0.5, 0.4)$. Near 0 or 1 the variance is small and the arms are much easier to tell apart: in the row $(0.99, 0.9)$ the true constant is 9 times smaller than the Pinsker estimate.

**Observed regret.** On the means $(0.9, 0.6, 0.3)$, with the implementations of the [UCB1](/ucb1/) and [Thompson sampling](/thompson-sampling/) pages, averaged over the seeds 0 to 19, the regret grows from $n = 1000$ to $n = 16000$ by 40.7 for UCB1 and by 4.2 for Thompson sampling. Divided by $\ln 16 \approx 2.77$, the slopes are 14.7 and 1.5 per unit of $\ln n$, against 1.545 for the bound. The theorem is about the limit, so a slope over a finite range can be smaller than the constant; on the means $(0.9, 0.8, 0.7)$ Thompson sampling has slope 2.1 over the same range, below the constant 3.55.

**Optimal policies.** KL-UCB (Lattimore and Szepesvari, Chapter 10) and Thompson sampling with a uniform prior (Kaufmann, Korda and Munos 2012) attain the constant for Bernoulli arms, and Lai and Robbins built rules that attain it for their one-parameter families. UCB1 and the decaying [epsilon-greedy](/epsilon-greedy/) rule have the right order $\ln n$ but not the right constant.

**Gap and worst case.** The bound depends on the instance. It does not contradict the minimax lower bound of order $\sqrt{nK}$ for the worst instance at a fixed $n$ (see [EXP3](/exp3/)): the hard instances of the minimax bound have gaps of order $\sqrt{K/n}$, which change with $n$.

## Tightness

The constant is exact: for Bernoulli arms, KL-UCB and Thompson sampling have $\limsup_n \mathbb{E}[T_i(n)]/\ln n \le 1/\mathrm{kl}(\mu_i, \mu^*)$, so the liminf in the theorem is a limit for them. The order $\ln n$ is needed only for consistent policies. The bound holds for each instance, not uniformly: for a fixed $n$ and gaps near 0 the right side grows without limit, while the regret is at most $n\max_i\Delta_i$. Finite-time forms of the bound, such as Theorem 16.4 in Lattimore and Szepesvari for Gaussian bandits, have extra terms that matter when $n$ is small.

## History

Robbins (1952) posed the bandit problem in its modern form and gave a rule with regret $o(n)$. Lai and Robbins (1985) proved the lower bound for one-parameter families and built upper confidence rules that attain it; these were the first upper confidence bound policies. Agrawal (1995) gave simpler index rules based on sample means. Burnetas and Katehakis (1996) extended the bound and the optimal rules to families with several parameters. Auer, Cesa-Bianchi and Fischer (2002) gave [UCB1](/ucb1/), with a bound for each finite $n$ and a constant that is not optimal. Garivier and Cappe (2011) with KL-UCB, and Kaufmann, Korda and Munos (2012) with Thompson sampling, gave finite-time bounds that match the Lai-Robbins constant for Bernoulli arms.

## References
