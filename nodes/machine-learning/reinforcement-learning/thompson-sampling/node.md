---
tag: JKGDPY
kind: algorithm
slug: thompson-sampling
name: Thompson sampling
aliases:
- posterior sampling
- probability matching
- Beta-Bernoulli Thompson sampling
area: machine-learning/reinforcement-learning
level: core
summary: "Keep a posterior over the mean of each arm, draw one sample from each posterior, and pull the arm with the largest sample. Its regret on Bernoulli arms is logarithmic."
solves: [multi-armed-bandit]
model: real-ram
complexity:
  vars: {n: the number of rounds, K: the number of arms, d: the smallest positive gap}
  time: {worst: "Θ(n·K)"}
  space: {extra: "Θ(K)"}
  regret: {expected: "O(K log(n) / d)"}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1933
  people: [William R. Thompson]
  note: Thompson proposed the rule for clinical trials. Agrawal and Goyal (2012) and Kaufmann, Korda and Munos (2012) proved its first logarithmic regret bounds.
prereqs: [multi-armed-bandit, bayes-theorem, conjugate-prior]
see_also: [exploration-exploitation-tradeoff, ucb1, epsilon-greedy, lai-robbins-lower-bound, gittins-index, bayesian-inference, contextual-bandit]
sources:
  - paper: doi:10.1093/biomet/25.3-4.285
    title: William R. Thompson, On the likelihood that one unknown probability exceeds another in view of the evidence of two samples, Biometrika 25(3/4), 1933
    locator: pp. 285 to 294
  - paper: arxiv:1111.1797
    title: Shipra Agrawal and Navin Goyal, Analysis of Thompson sampling for the multi-armed bandit problem, COLT 2012, JMLR Workshop and Conference Proceedings 23
    locator: pp. 39.1 to 39.26; Algorithm 1 (Bernoulli bandits), Algorithm 2 (rewards in [0,1]), Theorems 1 and 2
  - paper: arxiv:1205.4217
    title: Emilie Kaufmann, Nathaniel Korda and Remi Munos, Thompson sampling, an asymptotically optimal finite-time analysis, ALT 2012, LNCS 7568
    locator: Theorem 1 (the Lai-Robbins constant for Bernoulli arms)
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 36, Theorem 36.1 (Bayesian regret) and Theorem 36.2 (frequentist analysis)
  - paper: doi:10.1561/2200000070
    title: Daniel J. Russo, Benjamin Van Roy, Abbas Kazerouni, Ian Osband and Zheng Wen, A tutorial on Thompson sampling, Foundations and Trends in Machine Learning 11(1), 2018
    locator: Chapters 3 and 4 (Beta-Bernoulli bandit and general Thompson sampling)
---

Thompson sampling is a randomized policy for the [multi-armed bandit](/multi-armed-bandit/). It keeps a Bayesian posterior over the unknown mean of each arm. In each round it draws one sample from each posterior and pulls the arm whose sample is largest. So each arm is pulled with the posterior probability that it is the best arm. For Bernoulli arms with Beta priors the posterior stays a Beta distribution, and the update is two counters per arm. Thompson proposed the rule in 1933. Its first logarithmic [regret](/regret/) bounds came only in 2012, and Kaufmann, Korda and Munos showed that it reaches the constant of the [Lai-Robbins lower bound](/lai-robbins-lower-bound/) for Bernoulli arms.

## In plain words

For each machine, keep a range of beliefs about how often it pays, wide when you know little and narrow when you know a lot. Before each play, pick one value at random from each machine's range of beliefs, as a guess. Play the machine with the best guess, and then update its range with the result.

A machine that you know little about has a wide range, so its guess is sometimes very high, and it gets played now and then. A machine that is surely bad has a narrow, low range, so its guess is almost never the best. The rule plays each machine about as often as it believes that machine is the best one.

## The problem

The input is a stochastic bandit with $K$ arms whose rewards are 0 or 1, with unknown means $\mu_1, \ldots, \mu_K$, and a horizon $n$. Rewards in $[0,1]$ reduce to this case (see line L6). The output is a sequence of pulls $A_1, \ldots, A_n$, each chosen from the rewards seen so far. The goal is small regret $R_n = \sum_i \Delta_i\,\mathbb{E}[T_i(n)]$, where $\Delta_i = \mu^* - \mu_i$ and $T_i(n)$ is the number of pulls of arm $i$ in $n$ rounds.

## The algorithm

```pseudo id=main
THOMPSON-SAMPLING(K, n, a, b)
L1  for i ← 1 to K do α[i] ← a, β[i] ← b        ▷ the prior Beta(a, b) on each mean
L2  for t ← 1 to n do
L3      for i ← 1 to K do draw θ[i] from Beta(α[i], β[i])
L4      A ← argmax_i θ[i]
L5      pull arm A and observe the reward X
L6      if X is not 0 or 1 then X ← 1 with probability X, else 0
        if X = 1 then α[A] ← α[A] + 1 else β[A] ← β[A] + 1
```

The usual prior is $a = b = 1$, the uniform distribution on $[0,1]$. After $s$ successes and $f$ failures of an arm, its posterior is $\mathrm{Beta}(a+s, b+f)$, by [Bayes' theorem](/bayes-theorem/): the prior density is proportional to $\theta^{a-1}(1-\theta)^{b-1}$, and each success multiplies it by $\theta$ and each failure by $1-\theta$. The Beta family is a [conjugate prior](/conjugate-prior/) for Bernoulli rewards. The step in line L6 turns a reward $x \in [0,1]$ into a Bernoulli trial with the same mean (Agrawal and Goyal, Algorithm 2).

## Example

Take three Bernoulli arms with means $(0.7, 0.5, 0.3)$ and the uniform prior. The policy draws with `random.Random(3)` and the arms with `random.Random(103)`. The table lists the samples $\theta$ of line L3, the arm pulled, the reward, and the posterior of that arm after the round.

| $t$ | $\theta[1]$ | $\theta[2]$ | $\theta[3]$ | arm | reward | new posterior |
|---|---|---|---|---|---|---|
| 1 | 0.257 | 0.333 | 0.935 | 3 | 0 | Beta(1, 2) |
| 2 | 0.007 | 0.529 | 0.744 | 3 | 0 | Beta(1, 3) |
| 3 | 0.388 | 0.139 | 0.393 | 3 | 0 | Beta(1, 4) |
| 4 | 0.944 | 0.614 | 0.248 | 1 | 0 | Beta(1, 2) |
| 5 | 0.157 | 0.330 | 0.069 | 2 | 1 | Beta(2, 1) |
| 6 | 0.800 | 0.792 | 0.133 | 1 | 1 | Beta(2, 2) |
| 7 | 0.439 | 0.834 | 0.022 | 2 | 0 | Beta(2, 2) |
| 8 | 0.403 | 0.175 | 0.014 | 1 | 1 | Beta(3, 2) |
| 9 | 0.257 | 0.497 | 0.045 | 2 | 1 | Beta(3, 2) |
| 10 | 0.706 | 0.802 | 0.308 | 2 | 0 | Beta(3, 3) |

Arm 3 wins the first three draws by chance and pays 0 three times. Its posterior $\mathrm{Beta}(1, 4)$ has mean $1/5$ and puts most of its mass below 0.4, so its samples become small: from round 5 on they are below 0.31, and arm 3 is not pulled again in these rounds. Arms 1 and 2 still have wide posteriors, so they share the pulls. After 10 rounds the posteriors are $\mathrm{Beta}(3,2)$, $\mathrm{Beta}(3,3)$ and $\mathrm{Beta}(1,4)$.

**Regret over many runs.** On means $(0.9, 0.6, 0.3)$, averaged over the seeds 0 to 19, the regret is 6.2, 7.2, 8.2, 9.1 and 10.4 at $n = 1000$, 2000, 4000, 8000 and 16000, against 38.7, 49.0, 59.1, 69.0 and 79.4 for [UCB1](/ucb1/) on the same reward draws. Each doubling of $n$ adds about 1. The Lai-Robbins rate for these arms is about $1.545 \ln n$, which is $1.07$ for each doubling. On the harder means $(0.9, 0.8, 0.7)$ Thompson sampling has 13.9 to 19.8 at the same horizons, against 49.0 to 174.8 for UCB1. These are observations on two instances, not a theorem.

## Correctness

- **The posterior is exact.** With independent $\mathrm{Beta}(a,b)$ priors on the means and Bernoulli rewards, the posterior of arm $i$ after $s$ successes and $f$ failures is $\mathrm{Beta}(a+s, b+f)$, and the arms stay independent given the data. So $\alpha[i]$ and $\beta[i]$ hold the full posterior.
- **Probability matching.** Given the data so far, $\Pr[A_t = i] = \Pr[\mu_i = \max_j \mu_j]$, the posterior probability that arm $i$ is best.
- **Bayesian regret** (Lattimore and Szepesvari, Theorem 36.1, after Russo and Van Roy). If the means are drawn from the prior that the policy uses, then the regret averaged over the prior is at most $K + 4\sqrt{2Kn\ln n} + 4K/n^2$. The proof is the UCB proof with one change: given the data, $A_t$ and the optimal arm have the same law.
- **Frequentist regret.** For fixed Bernoulli means and the uniform prior, Agrawal and Goyal (2012) proved $R_n = O\big((\sum_{i:\Delta_i>0} 1/\Delta_i^2)^2 \ln n\big)$, and $O(\ln n/\Delta + 1/\Delta^3)$ for two arms. Kaufmann, Korda and Munos (2012) proved that for each $\varepsilon > 0$, $\mathbb{E}[T_i(n)] \le (1+\varepsilon)\frac{\ln n}{\mathrm{kl}(\mu_i, \mu^*)} + o(\ln n)$, where $\mathrm{kl}$ is the relative entropy of two Bernoulli laws. This is the Lai-Robbins constant.

The [proof page](proofs/correctness.md) proves the first three claims in full. The frequentist bounds are long, and the page states them with pointers to the papers.

## Complexity

- **Time.** Line L3 draws $K$ Beta samples, each in expected $O(1)$ time, so each round costs $\Theta(K)$ and the run costs $\Theta(nK)$.
- **Space.** $\Theta(K)$ for $\alpha$ and $\beta$.
- **Regret.** $\sum_{i:\Delta_i>0}\frac{\Delta_i \ln n}{\mathrm{kl}(\mu_i,\mu^*)}(1+o(1))$ on Bernoulli arms. Since $\mathrm{kl}(\mu_i,\mu^*) \ge 2\Delta_i^2$ by Pinsker's inequality, this is at most $\sum_i \frac{\ln n}{2\Delta_i}(1+o(1))$, so $O(K\log(n)/d)$ with $d$ the smallest positive gap.

## Properties

- **Randomized.** The pulls are random even when the posteriors are fixed, and the randomness is what explores.
- **Anytime and free of tuning.** It does not use $n$ or the gaps. The prior is the only choice, and the uniform prior is the default.
- **Asymptotically optimal on Bernoulli arms.** It matches the Lai-Robbins constant, which [UCB1](/ucb1/) does not.
- **Explores by uncertainty.** The chance of a pull depends on how likely the arm is to be best, so a clearly bad arm is almost never pulled, unlike in [epsilon-greedy](/epsilon-greedy/).
- **Not the Bayes optimal policy.** It does not plan ahead. For discounted rewards with independent arms the Bayes optimal policy is the [Gittins index](/gittins-index/), and for a finite horizon it needs dynamic programming.

## Variants and improvements

- **Gaussian Thompson sampling.** For Gaussian rewards, draw $\theta_i$ from $\mathcal{N}(\bar X_i, 1/(N_i+1))$ (Agrawal and Goyal 2013).
- **Linear Thompson sampling.** For the linear [contextual bandit](/contextual-bandit/), draw $\theta$ from a Gaussian centered at the ridge estimate, with covariance proportional to the inverse design matrix.
- **Posterior sampling for RL (PSRL).** Draw a whole MDP from the posterior at the start of each episode, and follow its optimal policy for the episode.
- **Top-two and information-directed sampling.** Change the choice rule for best arm identification or for structured problems where a pure sample explores badly.
- **Approximate posteriors.** With neural networks, use ensembles, bootstrap samples or Laplace approximations in place of the exact posterior.

## When to use it

Use Thompson sampling when the rewards are Bernoulli or have a simple conjugate model, which covers clicks, conversions and the arms of a trial. It is easy to code, works well in practice, and has the optimal constant on Bernoulli arms. Use [UCB1](/ucb1/) when a deterministic policy is needed, for example to make results repeatable without storing random seeds. Use [EXP3](/exp3/) when the rewards may be set by an adversary.

## Pitfalls

- **A wrong reward model.** The Beta update assumes 0 or 1 rewards. For rewards in $[0,1]$, do the Bernoulli trial of line L6; do not add $x$ to $\alpha$ and $1-x$ to $\beta$ without care, since the guarantees are for the trial version.
- **A strong wrong prior.** A prior with large $a + b$ needs many pulls to be overcome, and the policy may ignore the best arm for a long time.
- **Delayed or batched feedback.** With many pulls between updates, the same posterior is sampled many times. This is still sound, unlike a deterministic rule, which repeats the same arm for the whole batch.
- **Bad samplers.** The Beta sampler must be correct for small parameters such as $\mathrm{Beta}(1, 1)$. Use a library sampler.

## Implementations

## History

Thompson (1933) asked how to share patients between two treatments with unknown success rates, and proposed to give each treatment with the probability that it is the better one, given the data. The idea was used in practice for decades without a proof. Chapelle and Li (2011) showed in experiments that it does better than UCB methods on display advertising and news data, which brought new interest. In 2012 Agrawal and Goyal gave the first logarithmic regret bound, and Kaufmann, Korda and Munos showed that it reaches the Lai-Robbins constant for Bernoulli arms. Russo and Van Roy (2014) proved the Bayesian regret bound that holds for general priors.

## References
