---
tag: FHH31V
kind: problem
slug: contextual-bandit
name: Contextual bandit problem
aliases:
- contextual bandits
- contextual multi-armed bandit
- associative bandit
area: machine-learning/reinforcement-learning
level: advanced
summary: "In each round, see a context, pull one of K arms, and see only that arm's reward. Compete with the best policy that maps contexts to arms."
prereqs: [multi-armed-bandit, linear-regression]
see_also: [ucb1, exp3, thompson-sampling, ridge-regression, sherman-morrison-formula, expert-problem, exploration-exploitation-tradeoff, policy]
sources:
  - paper: "John Langford and Tong Zhang, The epoch-greedy algorithm for contextual multi-armed bandits, Advances in Neural Information Processing Systems 20 (NIPS 2007)"
    locator: pp. 817 to 824; the problem setting, the epoch-greedy algorithm and its regret bound
  - paper: doi:10.1145/1772690.1772758
    title: Lihong Li, Wei Chu, John Langford and Robert E. Schapire, A contextual-bandit approach to personalized news article recommendation, WWW 2010
    locator: pp. 661 to 670; Section 3.1 (Algorithm 1, LinUCB with disjoint linear models), Section 3.2 (hybrid linear models), Sections 5 and 6 (offline evaluation on Yahoo! news data); arXiv 1003.0146
  - paper: "Wei Chu, Lihong Li, Lev Reyzin and Robert E. Schapire, Contextual bandits with linear payoff functions, AISTATS 2011, PMLR 15"
    locator: pp. 208 to 214; BaseLinUCB and SupLinUCB, the upper bound O(sqrt(T d ln^3(K T ln(T) / delta))) and the lower bound Omega(sqrt(T d))
  - paper: doi:10.1137/S0097539701398375
    title: Peter Auer, Nicolo Cesa-Bianchi, Yoav Freund and Robert E. Schapire, The nonstochastic multiarmed bandit problem, SIAM Journal on Computing 32(1), 2002
    locator: pp. 48 to 77; Section 7 (Exp4, bandits with expert advice)
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 18 (contextual bandits and Exp4), Chapter 19 (stochastic linear bandits, LinUCB, Theorem 19.2), Chapter 20 (confidence bounds for least squares)
---

The contextual bandit problem is the [multi-armed bandit](/multi-armed-bandit/) with side information. In each round the learner first sees a context, such as the features of a user, then chooses one of $K$ arms, and then sees the reward of that arm only. The best arm can change from round to round with the context, so the learner competes with the best [policy](/policy/) from contexts to arms, not with the best single arm. It sits between the plain bandit, which has no context, and full [reinforcement learning](/markov-decision-process/), where the action also changes the next context. Langford and Zhang (2007) named the problem; LinUCB (Li, Chu, Langford and Schapire 2010) is its best known algorithm for linear rewards.

## In plain words

A news site must pick one story to show at the top of the page each time someone visits. It knows a little about each visitor: the time of day, the area, what they read before. It shows one story and sees only whether the visitor clicked on it. It never learns whether the visitor would have clicked on the other stories.

The best story is not the same for every visitor. So the site must learn a rule: for this kind of visitor, show this kind of story. And it must keep trying stories that it is unsure about, or it can never learn that they are good for some visitors.

## Definition

**The protocol.** For rounds $t = 1, \ldots, T$:

1. The environment reveals a context $x_t$ from a set $\mathcal{X}$. In the linear setting, the context is a feature vector $x_{t,a} \in \mathbb{R}^d$ for each arm $a$.
2. The learner chooses an arm $a_t \in \{1, \ldots, K\}$, using the past contexts, arms and rewards and the current context.
3. The learner receives the reward $r_t(a_t) \in [0,1]$, and sees no other reward.

In the stochastic setting, the pairs $(x_t, r_t)$ are i.i.d. draws from an unknown joint law, where $r_t = (r_t(1), \ldots, r_t(K))$. In the adversarial setting they are an arbitrary fixed sequence.

**Regret against a policy class.** A policy is a map $\pi : \mathcal{X} \to \{1, \ldots, K\}$. For a class $\Pi$ of policies, the regret is

$$R_T = \max_{\pi\in\Pi}\mathbb{E}\Big[\sum_{t=1}^{T} r_t(\pi(x_t))\Big] - \mathbb{E}\Big[\sum_{t=1}^{T} r_t(a_t)\Big].$$

With one context, or with $\Pi$ the constant policies, this is the [regret](/regret/) of the plain bandit.

**Linear payoffs.** In the model of Chu et al. (2011), $\mathbb{E}[r_t(a) \mid x_{t,a}] = x_{t,a}^\top\theta^*$ for an unknown $\theta^* \in \mathbb{R}^d$, with $\|x_{t,a}\| \le 1$ and $\|\theta^*\| \le 1$. The benchmark is the best arm in each round, $a_t^* = \arg\max_a x_{t,a}^\top\theta^*$, so $R_T = \mathbb{E}\big[\sum_t (x_{t,a_t^*} - x_{t,a_t})^\top\theta^*\big]$. In the disjoint model of Li et al. (2010), each arm has its own $\theta_a$, which is the shared model with $Kd$ coordinates and one block per arm.

## Variants

- **Finite policy class.** $\Pi$ is finite, or has finite VC dimension, and the learner may call a supervised learning oracle for $\Pi$. This is the setting of epoch-greedy and of the later oracle based methods.
- **Bandits with expert advice.** In each round $N$ experts each give a distribution over the arms, and the learner competes with the best expert. This is the adversarial version, solved by Exp4.
- **Linear and generalized linear bandits.** The reward is linear in the features, or a known link function of a linear score, such as a logistic model for clicks.
- **Offline (logged) contextual bandits.** Learn or evaluate a policy from logged triples $(x_t, a_t, r_t(a_t))$ with the probabilities of the logged choices; see [off-policy evaluation](/off-policy-evaluation/).

## Examples

**LinUCB, step by step.** Take $K = 2$, $d = 2$, the disjoint model with $\theta_1 = (1, 0)$ and $\theta_2 = (0.4, 0.6)$, no noise, $\alpha = 1$, and the same context $x_t$ for both arms. The scores are those of line L5 of the pseudocode below.

| $t$ | $x_t$ | score of arm 1 | score of arm 2 | arm | reward |
|---|---|---|---|---|---|
| 1 | (1, 0) | 1.000 | 1.000 | 1 | 1.0 |
| 2 | (0, 1) | 1.000 | 1.000 | 1 | 0.0 |
| 3 | (0, 1) | 0.707 | 1.000 | 2 | 0.6 |
| 4 | (1, 0) | 1.207 | 1.000 | 1 | 1.0 |
| 5 | (0.6, 0.8) | 1.063 | 1.065 | 2 | 0.72 |
| 6 | (0, 1) | 0.707 | 1.050 | 2 | 0.6 |

In round 1 both arms have $\hat\theta = 0$ and width 1, and the tie goes to arm 1. In round 3 arm 1 has seen $x = (0,1)$ once with reward 0, so its estimate is 0 and its width in that direction is $\sqrt{1/2} \approx 0.707$; arm 2 has seen nothing and scores 1. In round 5, arm 1 has $\hat\theta_1 = (2/3, 0)$ and arm 2 has $\hat\theta_2 = (0, 0.3)$. The means $0.4$ and $0.24$ favor arm 1, but arm 2 is less known in the new direction: its width is $\sqrt{0.68} \approx 0.825$ against $\sqrt{0.44} \approx 0.663$, and it wins by a little. Its true mean, 0.72, is the larger one. After round 6, $A_2^{-1} \approx \begin{pmatrix}0.771 & -0.102\\ -0.102 & 0.288\end{pmatrix}$ and $\hat\theta_2 \approx (0.153, 0.468)$, moving toward $(0.4, 0.6)$.

**Regret on a random linear instance.** Take $K = 5$ arms, $d = 6$, the disjoint model with unit vectors $\theta_a$ and contexts drawn from `random.Random(s)`, and Gaussian noise with standard deviation 0.1. Averaged over the seeds 0 to 4, LinUCB with $\alpha = 1$ has regret 13.3, 14.1, 15.1 and 16.3 after 1000, 2000, 4000 and 8000 rounds. A uniform random policy has 450.8, 924.3, 1869.6 and 3741.7, which is linear.

## Known algorithms

| Algorithm | Setting | Regret | Source |
|---|---|---|---|
| Epoch-greedy | stochastic, finite class $\Pi$, oracle | $O(T^{2/3}(K\ln\lvert\Pi\rvert)^{1/3})$ | Langford and Zhang 2007 |
| Exp4 | adversarial, $N$ experts | $O(\sqrt{TK\ln N})$ | Auer et al. 2002, Section 7 |
| LinUCB | stochastic, linear | no published bound for the 2010 form | Li et al. 2010 |
| SupLinUCB | stochastic, linear | $O\big(\sqrt{Td\ln^3(KT\ln(T)/\delta)}\big)$ with probability $1-\delta$ | Chu et al. 2011 |
| OFUL / LinUCB with a growing radius | stochastic, linear | $O(d\sqrt{T}\log T)$ | Abbasi-Yadkori, Pal and Szepesvari 2011; Lattimore and Szepesvari, Chapter 19 |
| Linear Thompson sampling | stochastic, linear | $\tilde O(d^{3/2}\sqrt{T})$ | Agrawal and Goyal 2013 |

The pseudocode is LinUCB with disjoint models, as in Algorithm 1 of Li et al. (2010).

```pseudo id=main
LINUCB(K, d, α)
L1  for a ← 1 to K do A⁻¹[a] ← I_d, b[a] ← 0
L2  for t ← 1, 2, … do
L3      observe x_{t,a} for each arm a
L4      for each a: θ̂[a] ← A⁻¹[a] · b[a]
L5          p[a] ← θ̂[a]ᵀ x_{t,a} + α · sqrt(x_{t,a}ᵀ A⁻¹[a] x_{t,a})
L6      a_t ← argmax_a p[a], ties to the smallest a
L7      pull a_t and observe r_t
L8      u ← A⁻¹[a_t] x;  A⁻¹[a_t] ← A⁻¹[a_t] − u uᵀ / (1 + xᵀ u)      ▷ x = x_{t,a_t}
L9      b[a_t] ← b[a_t] + r_t · x
```

$A[a] = I + \sum x x^\top$ over the rounds where arm $a$ was pulled, so $\hat\theta[a]$ is the [ridge regression](/ridge-regression/) estimate with penalty 1, and $\sqrt{x^\top A^{-1}x}$ is the width of its confidence interval in the direction $x$. Line L8 is the [Sherman-Morrison formula](/sherman-morrison-formula/) for $(A + xx^\top)^{-1}$, which costs $O(d^2)$ in place of the $O(d^3)$ of a new [matrix inversion](/matrix-inversion/). Li et al. set $\alpha = 1 + \sqrt{\ln(2/\delta)/2}$.

**Why LinUCB has no clean analysis.** In LinUCB the arms chosen depend on the past rewards, and the same rewards then form $\hat\theta$. So the rewards used by the estimate are not independent given the contexts used, and the fixed design confidence interval that motivates $\alpha$ does not apply. Chu et al. (2011) state this and analyse SupLinUCB in its place: it splits the rounds into stages so that, within a stage, the chosen contexts do not depend on the rewards used, and then the fixed design bound holds. Abbasi-Yadkori, Pal and Szepesvari (2011) take another route: a self-normalized martingale bound gives a confidence ellipsoid valid under this dependence, at the price of a radius that grows like $\sqrt{d\log t}$, which gives the $O(d\sqrt{T}\log T)$ bound.

## Bounds

- **Linear payoffs, lower bound.** Chu et al. (2011) prove that each algorithm has regret $\Omega(\sqrt{Td})$ on some linear instance. SupLinUCB matches this up to log factors.
- **Finite policy class.** Exp4 gets regret $O(\sqrt{TK\ln\lvert\Pi\rvert})$, which is the best possible up to log factors, but it keeps one weight for each policy. Oracle based methods get the same rate with a small number of calls to a supervised learning oracle.
- **No context.** With $\lvert\mathcal{X}\rvert = 1$ the problem is the plain bandit, with the minimax lower bound of order $\sqrt{TK}$.

## Reductions

- **From the plain bandit.** Ignoring the context gives a $K$-armed bandit, but then the benchmark is the best single arm, which can be far worse than the best policy.
- **Finite contexts.** With $C$ contexts, run a separate bandit for each context. The regret is $O(\sqrt{TCK})$ in the worst case, which is poor when $C$ is large. Features let the contexts share what is learned.
- **To supervised learning.** Importance weighting turns each round into a cost-sensitive example with the estimate $r_t(a)\mathbb{1}\{a = a_t\}/p_t(a_t)$ for each arm, as in [EXP3](/exp3/). Epoch-greedy and the oracle based methods use this to call a classifier.
- **To reinforcement learning.** A contextual bandit is an MDP whose next state does not depend on the action, with horizon 1. Methods for [Markov decision processes](/markov-decision-process/) apply, but they do not use this structure.

## Applications

- **News and content recommendation.** Li et al. (2010) ran LinUCB on the Yahoo! front page news module, with evaluation on logged random traffic; they report a click lift of 12.5% over a bandit that ignores the context.
- **Online advertising.** Choose an ad for a user and a page, and learn from the clicks.
- **Personalized medicine and mobile health.** Choose a treatment or a prompt from the state of a patient.
- **Systems tuning.** Choose a configuration for each request or job from its features.

## References
