---
tag: J62NE6
kind: problem
slug: multi-armed-bandit
name: Multi-armed bandit problem
aliases:
- bandit problem
- K-armed bandit
- stochastic multi-armed bandit
area: machine-learning/reinforcement-learning
level: intro
summary: "Pull one of K arms in each of n rounds, see only that arm's reward, and keep the regret against the best arm small."
prereqs: [regret, expected-value]
see_also: [exploration-exploitation-tradeoff, epsilon-greedy, ucb1, thompson-sampling, exp3, lai-robbins-lower-bound, gittins-index, contextual-bandit]
sources:
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 4 (stochastic bandits, Section 4.4 the regret, Section 4.5 Lemma 4.5 the regret decomposition, Section 4.6 the canonical model), Chapter 11 (adversarial bandits), Chapter 15 (Theorem 15.2 the minimax lower bound), Chapter 16 (instance dependent lower bounds)
  - paper: doi:10.1090/S0002-9904-1952-09620-8
    title: Herbert Robbins, Some aspects of the sequential design of experiments, Bulletin of the American Mathematical Society 58(5), 1952
    locator: pp. 527 to 535 (the two-population sampling problem and a rule whose average reward tends to the larger mean)
  - paper: doi:10.1561/2200000024
    title: Sebastien Bubeck and Nicolo Cesa-Bianchi, Regret analysis of stochastic and nonstochastic multi-armed bandit problems, Foundations and Trends in Machine Learning 5(1), 2012
    locator: Chapter 1 (the expected regret and the pseudo-regret), Chapter 2 (stochastic bandits), Chapter 3 (adversarial bandits)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapter 2 (multi-armed bandits, the k-armed testbed and the action-value methods)
---

The multi-armed bandit problem is the simplest model of learning by trial: in each of $n$ rounds a learner pulls one of $K$ arms, receives a reward from that arm only, and wants a total reward close to that of the best arm. The quality of a strategy is its [regret](/regret/), the reward lost against the best arm. It is the setting where the [exploration-exploitation tradeoff](/exploration-exploitation-tradeoff/) appears in its pure form, and it is a [Markov decision process](/markov-decision-process/) with a single state. Robbins posed it in 1952. Good algorithms have regret that grows like $\log n$ when the rewards are random and like $\sqrt{Kn}$ when an adversary picks them.

## In plain words

You stand in front of a row of slot machines. Each machine pays out at random, and each has its own average payout, which you do not know. You have a fixed number of coins. With each coin you pick one machine and see what it pays. You see nothing about the machines you did not pick.

If you always play the machine that looks best so far, a bad first result can hide the best machine from you for ever. If you keep trying every machine, you waste coins on bad ones. A good strategy tries machines often at the start and less and less later, and plays the machine that is truly best for almost all of the coins. The loss against a player who knew the best machine from the start is the regret.

## Definition

**Notation.** $K \ge 2$ is the number of arms and $n$ is the horizon, the number of rounds. On the bandit pages, $n$ is the horizon and not the number of training examples. The round is $t \in \{1, \ldots, n\}$, the arm pulled is $A_t$ and the reward is $X_t$. The number of pulls of arm $i$ in the first $t$ rounds is $T_i(t) = \sum_{s=1}^{t} \mathbb{1}\{A_s = i\}$.

**Stochastic bandit.** The environment is a list $\nu = (P_1, \ldots, P_K)$ of reward distributions on $\mathbb{R}$ with finite means $\mu_1, \ldots, \mu_K$. Let $\mu^* = \max_i \mu_i$, and let $\Delta_i = \mu^* - \mu_i \ge 0$ be the gap of arm $i$. A policy chooses $A_t$ as a function of $A_1, X_1, \ldots, A_{t-1}, X_{t-1}$ and its own random bits. Given the past and $A_t$, the reward $X_t$ has the law $P_{A_t}$. The regret is

$$R_n = n\mu^* - \mathbb{E}\Big[\sum_{t=1}^{n} X_t\Big].$$

**Regret decomposition** (Lattimore and Szepesvari, Lemma 4.5). For each policy and each stochastic bandit with finite means,

$$R_n = \sum_{i=1}^{K} \Delta_i \, \mathbb{E}[T_i(n)].$$

*Proof.* Given the past and $A_t$, the mean of $X_t$ is $\mu_{A_t}$. By the tower rule, $\mathbb{E}[X_t] = \mathbb{E}[\mu_{A_t}] = \sum_i \mu_i \Pr[A_t = i]$. Sum over $t$: $\mathbb{E}[\sum_t X_t] = \sum_i \mu_i \mathbb{E}[T_i(n)]$. Since $\sum_i T_i(n) = n$, also $n\mu^* = \sum_i \mu^* \mathbb{E}[T_i(n)]$. Subtract the two lines. $\square$

The same algebra without the expectation gives a pathwise identity: $n\mu^* - \sum_t \mu_{A_t} = \sum_i \Delta_i T_i(n)$ on every run. The left side is the *random pseudo-regret*. So to keep the regret small, a policy must pull each arm with a gap $\Delta_i > 0$ only a few times, and the number of pulls that each bad arm needs depends on its gap.

**Pseudo-regret and expected regret.** Bubeck and Cesa-Bianchi (Chapter 1) separate two quantities. Let $X_{i,t}$ be the reward that arm $i$ would pay in round $t$. The expected regret is $\mathbb{E}[\max_i \sum_t X_{i,t} - \sum_t X_{A_t,t}]$, the loss against the best arm in hindsight. The pseudo-regret is $\max_i \mathbb{E}[\sum_t X_{i,t} - \sum_t X_{A_t,t}]$, which for a stochastic bandit is $R_n$ above. Since $\mathbb{E}[\max] \ge \max \mathbb{E}$, the expected regret is at least the pseudo-regret. For stochastic rewards the gap between them can be of order $\sqrt{n}$, so the $\log n$ bounds of the stochastic pages are bounds on the pseudo-regret.

**Adversarial bandit.** The rewards are a table $x \in [0,1]^{n \times K}$, fixed in advance by an *oblivious* adversary. The learner gets $x_{t,A_t}$ and sees nothing else. The regret is $\max_i \sum_t x_{t,i} - \mathbb{E}[\sum_t x_{t,A_t}]$, with the expectation over the random choices of the learner. A deterministic policy can have regret linear in $n$ here, since the adversary can predict each choice and put a reward of 0 on it. So good adversarial policies are randomized.

## Variants

- **Bernoulli, Gaussian or bounded rewards.** The class of distributions matters for the constants: the [Lai-Robbins lower bound](/lai-robbins-lower-bound/) uses the Kullback-Leibler divergence inside the class, and [UCB1](/ucb1/) only needs rewards in $[0,1]$.
- **Adaptive adversary.** The table may depend on the past choices of the learner. See [oblivious adversary](/oblivious-adversary/) and [adaptive adversary](/adaptive-adversary/).
- **Bayesian bandit.** The arm parameters have a known prior. With a discount factor $\gamma < 1$ and independent arms, the [Gittins index](/gittins-index/) gives the optimal policy. With a finite horizon the criterion is the Bayesian regret.
- **Contextual bandit.** A context is shown before each pull, and the best arm depends on it. See [contextual bandit](/contextual-bandit/).
- **Pure exploration.** The goal is to name the best arm at the end, not to collect reward on the way. The cost is the probability of a wrong answer or the number of pulls needed.
- **Full information.** If the learner sees the rewards of all arms in each round, the problem is the [expert problem](/expert-problem/).

## Examples

**Exact regret of explore-then-commit.** Take two Bernoulli arms with $\mu = (3/5, 2/5)$, so $\Delta_2 = 1/5$, and $n = 4$. The policy pulls arm 1, then arm 2, and then commits for rounds 3 and 4 to the arm with the larger reward, with a tie going to arm 1. It commits to arm 2 only if arm 1 paid 0 and arm 2 paid 1, which has probability $\frac25 \cdot \frac25 = \frac{4}{25}$. So $\mathbb{E}[T_2(4)] = 1 + 2 \cdot \frac{4}{25} = \frac{33}{25}$ and $R_4 = \frac15 \cdot \frac{33}{25} = \frac{33}{125} = 0.264$. An exact enumeration of the $2^8$ reward tables gives the same value for $n\mu^* - \mathbb{E}[\sum_t X_t]$, and gives the expected regret against the best arm in hindsight as $\frac{38801}{78125} \approx 0.497$, almost twice the pseudo-regret.

**One run.** Take the same arms with $n = 10$ and two pulls of each arm before the commit, with the generator `random.Random(7)` of the implementation. Arm 1 pays 1 and 0, and arm 2 pays 1 and 1, so the policy commits to arm 2, the worse arm. The pulls are $T_1 = 2$ and $T_2 = 8$, and the random pseudo-regret is $\frac15 \cdot 8 = \frac85$. The total reward is 6, equal to $n\mu^* = 6$: on this run luck hides the loss, which is why the regret is defined with an expectation.

**Adversarial table.** Let $K = 2$ and fix a deterministic policy. An oblivious adversary that knows the policy can simulate it before the game: in round $t$ it gives reward 0 to the arm that the policy will pull and reward 1 to the other arm. The policy gets 0. The two arms pay $n$ in total, so the better arm pays at least $n/2$, and the regret is at least $n/2$. On the same table, a policy that pulls each arm with probability $1/2$ in each round gets $n/2$ in expectation, so its regret is at most $n/2$ and is 0 when the two arms pay $n/2$ each.

## Known algorithms

| policy | setting | regret bound | kind of bound |
|---|---|---|---|
| [epsilon-greedy](/epsilon-greedy/), constant $\varepsilon$ | stochastic | $\Theta(n)$ | expected, linear |
| [epsilon-greedy](/epsilon-greedy/) with $\varepsilon_t = \min(1, cK/(d^2 t))$ | stochastic, rewards in $[0,1]$, $d \le \min_{i:\Delta_i>0} \Delta_i$ | $O(\log n)$ | expected |
| [UCB1](/ucb1/) | stochastic, rewards in $[0,1]$ | $\sum_{i:\Delta_i>0} \frac{8\ln n}{\Delta_i} + (1 + \frac{\pi^2}{3})\sum_i \Delta_i$ | expected, for each $n$ |
| [Thompson sampling](/thompson-sampling/) | stochastic, Bernoulli | $(1+\epsilon)\sum_{i:\Delta_i>0} \frac{\Delta_i \ln n}{\mathrm{kl}(\mu_i, \mu^*)} + O(1)$ | expected, asymptotically optimal |
| [EXP3](/exp3/) | adversarial, oblivious, rewards in $[0,1]$ | $2\sqrt{e-1}\sqrt{nK\ln K}$ | expected |
| [Gittins index](/gittins-index/) | Bayesian, discounted, independent arms | optimal for the discounted Bayesian reward | exact |

## Bounds

**Instance dependent.** For each policy that is consistent (regret $o(n^a)$ for each $a > 0$ on each instance of the class), the [Lai-Robbins lower bound](/lai-robbins-lower-bound/) gives $\liminf_{n} R_n / \ln n \ge \sum_{i:\Delta_i > 0} \Delta_i / \mathrm{KL}(P_i, P^*)$ in a one-parameter family. UCB1 meets the order $\log n$, and Thompson sampling meets the constant for Bernoulli arms.

**Minimax, stochastic.** For $n \ge K - 1$ and each policy there is a Gaussian bandit with unit variance and means in $[0,1]$ on which $R_n \ge \frac{1}{27}\sqrt{(K-1)n}$ (Lattimore and Szepesvari, Theorem 15.2). The UCB1 bound gives $O(\sqrt{Kn\log n})$ against the worst instance, and the MOSS policy removes the $\log n$ factor (Lattimore and Szepesvari, Chapter 9).

**Minimax, adversarial.** For each $K \ge 2$ and $n$ there is a random reward table on which each policy has expected regret at least $\frac{1}{20}\min(\sqrt{Kn}, n)$ (Auer, Cesa-Bianchi, Freund and Schapire 2002, Theorem 5.1). EXP3 matches this up to the factor $\sqrt{\ln K}$.

**Full information is easier only by a factor.** With full feedback, Hedge (the [multiplicative weights update](/multiplicative-weights-update/)) has regret $O(\sqrt{n \ln K})$. Bandit feedback costs a factor of about $\sqrt{K}$, because one round gives one sample instead of $K$.

## Reductions

- **To the expert problem.** EXP3 is the exponential weights method of the expert problem run on importance weighted estimates of the rewards. The estimate of the reward of each arm is unbiased, so the expert analysis goes through with a variance term that costs the factor $\sqrt{K}$.
- **From MDPs.** A [Markov decision process](/markov-decision-process/) with one state and the average or total reward criterion is a bandit. A contextual bandit is an MDP whose actions do not change the next state. Many exploration rules for MDPs, such as [UCT](/uct/) inside [Monte Carlo tree search](/monte-carlo-tree-search/), apply a bandit policy at each state.
- **Doubling.** A policy tuned for a known horizon $n$ becomes an anytime policy by restarts on horizons $1, 2, 4, \ldots$, with the [doubling trick](/doubling-trick/). This keeps a $\sqrt{n}$ bound up to a constant factor, but it can spoil a $\log n$ bound.

## Applications

- **Clinical trials.** Thompson (1933) asked how to assign patients to two treatments when the evidence comes in during the trial. This is the two-armed Bernoulli bandit.
- **Web experiments and recommendation.** Online tests of page variants, ad selection and news recommendation use bandit policies so that fewer users see the worse variant. The news recommendation study of Li, Chu, Langford and Schapire (2010) used the contextual version.
- **Game tree search.** UCT applies [UCB1](/ucb1/) at each node of a game tree to decide which move to simulate next.
- **Reinforcement learning.** The bandit is the testbed for exploration rules that are later used in full RL agents, such as [epsilon-greedy](/epsilon-greedy/) action selection in [Q-learning](/q-learning/).

## References
