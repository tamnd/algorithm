---
tag: MZPX76
kind: theorem
slug: tabular-q-learning-convergence
name: Convergence of tabular Q-learning
aliases:
- Watkins-Dayan theorem
- convergence of Q-learning
- Q-learning convergence theorem
area: machine-learning/reinforcement-learning
level: advanced
summary: "In a finite discounted MDP, if every state action pair is updated infinitely often with Robbins-Monro step sizes, tabular Q-learning converges to Q* with probability 1."
prereqs: [q-learning, bellman-contraction, robbins-monro-conditions, stochastic-approximation]
see_also: [sarsa, double-q-learning, temporal-difference-learning, value-iteration, deadly-triad, minimax-q, banach-fixed-point-theorem, martingale]
sources:
  - paper: doi:10.1007/BF00992698
    title: "Christopher J. C. H. Watkins and Peter Dayan, Q-learning, Machine Learning 8(3-4), 1992, pages 279 to 292"
    locator: the convergence theorem for tabular Q-learning and its proof by the action-replay process
  - paper: "Tommi Jaakkola, Michael I. Jordan and Satinder P. Singh, On the convergence of stochastic iterative dynamic programming algorithms, Neural Computation 6(6), 1994, pages 1185 to 1201"
    locator: the stochastic approximation theorem for max-norm pseudo-contractions and its application to Q-learning and TD(lambda)
  - paper: "John N. Tsitsiklis, Asynchronous stochastic approximation and Q-learning, Machine Learning 16(3), 1994, pages 185 to 202"
    locator: the asynchronous stochastic approximation theorem, the boundedness of the iterates, and the convergence of Q-learning
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: the chapter on stochastic iterative algorithms (convergence of iterations based on contractions) and the section on Q-learning
  - paper: "Eyal Even-Dar and Yishay Mansour, Learning rates for Q-learning, Journal of Machine Learning Research 5, 2003, pages 1 to 25"
    locator: the lower bound for linear step sizes and the polynomial bounds for polynomial step sizes
---

The convergence theorem for tabular [Q-learning](/q-learning/) says that the algorithm finds the optimal action values $q_*$ of a finite discounted MDP with probability 1, whatever policy produces the data, if every state action pair keeps being updated and the step sizes of each pair satisfy the [Robbins-Monro conditions](/robbins-monro-conditions/). Watkins and Dayan (1992) gave the first full proof. Jaakkola, Jordan and Singh (1994) and Tsitsiklis (1994) then proved it as a case of [stochastic approximation](/stochastic-approximation/) for a max-norm contraction, the [Bellman optimality operator](/bellman-contraction/). This second proof is the one given here; the same scheme proves the convergence of [SARSA](/sarsa/), [TD(λ)](/td-lambda/) and [Double Q-learning](/double-q-learning/).

## Statement

Let the MDP have finite sets of states and actions, discount $0 \le \gamma < 1$, and rewards with bounded mean and variance. Q-learning makes, at each time $t$, the update

$$Q_{t+1}(s, a) = \big(1 - \alpha_t(s, a)\big) Q_t(s, a) + \alpha_t(s, a)\Big(R_{t+1} + \gamma\max_{a'} Q_t(S_{t+1}, a')\Big)$$

for the pair $(s, a) = (S_t, A_t)$, and leaves the other pairs unchanged, which is the same as $\alpha_t(s, a) = 0$ for them. Each step $\alpha_t(s, a) \in [0, 1]$ is known before $R_{t+1}$ and $S_{t+1}$ are drawn.

**Theorem.** If, with probability 1, for every pair $(s, a)$,

$$\sum_{t} \alpha_t(s, a) = \infty \qquad \text{and} \qquad \sum_{t} \alpha_t(s, a)^2 < \infty ,$$

then $Q_t(s, a) \to q_*(s, a)$ for all pairs, with probability 1.

The first condition implies that every pair is updated infinitely often. For example, $\alpha_t(s, a) = 1/n_t(s, a)$, where $n_t(s, a)$ counts the updates of the pair, satisfies both conditions whenever every pair is updated infinitely often. The behavior policy can be anything that achieves this: ε-greedy, uniform, or a log of past data.

As a check, take a continuing MDP with 3 states, 2 actions and $\gamma = 1/2$, with transition probabilities $p(\cdot \mid 0, 0) = (1/2, 1/2, 0)$, $p(\cdot \mid 0, 1) = (0, 0, 1)$, $p(\cdot \mid 1, 0) = (1, 0, 0)$, $p(\cdot \mid 1, 1) = (0, 1/4, 3/4)$, $p(\cdot \mid 2, 0) = (1/3, 0, 2/3)$, $p(\cdot \mid 2, 1) = (0, 1, 0)$, and rewards $r(0, \cdot) = (1, 0)$, $r(1, \cdot) = (2, -1)$, $r(2, \cdot) = (0, 3)$. The exact solution is $q_*(0, \cdot) = (12/5, 23/10)$, $q_*(1, \cdot) = (16/5, 9/8)$ and $q_*(2, \cdot) = (29/15, 23/5)$. Q-learning with a uniform random behavior and $\alpha = 1/n(s, a)$ had a largest error of 0.08 to 0.18 after $10^3$ steps, 0.012 to 0.055 after $10^4$ steps and 0.003 to 0.019 after $10^5$ steps, over 5 seeds.

## In plain words

Q-learning makes small corrections from single random samples. Each correction moves one score toward a target, and the targets are noisy. The theorem says that if every score keeps being corrected forever, and the corrections get smaller in the right way, the noise averages out and the scores end at the true optimal values.

The corrections must shrink slowly enough that their total is still unlimited, so the scores can travel as far as they need. They must also shrink fast enough that the noise cannot keep pushing the scores around. The step sizes one over the number of visits do both.

## Proof

We give the proof of Jaakkola, Jordan and Singh (1994) and Tsitsiklis (1994), with two simplifications: we assume that rewards are bounded, $|R_{t+1}| \le R_{\max}$, which makes the iterates bounded at once, and we cite the one lemma about averages of noise. Write $\|Q\| = \max_{s,a}|Q(s, a)|$, let $\mathcal{F}_t$ be the past up to the choice of $\alpha_t$, and let $T^*$ be the Bellman optimality operator, $(T^* Q)(s, a) = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a)\max_{a'} Q(s', a')$.

**Step 1 (the form of stochastic approximation).** For the pair updated at time $t$, write the target as $(T^* Q_t)(s, a) + w_t$. Then

$$Q_{t+1}(s, a) = (1 - \alpha_t(s, a))\, Q_t(s, a) + \alpha_t(s, a)\big((T^* Q_t)(s, a) + w_t(s, a)\big)$$

for every pair (with $\alpha_t = 0$ for the pairs not updated), where $\mathbb{E}[w_t \mid \mathcal{F}_t] = 0$ because, given the past and the pair, $(R_{t+1}, S_{t+1})$ follows the law of the MDP. This is proved on the [Q-learning](/q-learning/) page.

**Step 2 (the contraction).** $\|T^* Q - T^* Q'\| \le \gamma\|Q - Q'\|$, and $q_*$ is the unique fixed point of $T^*$ ([Bellman contraction](/bellman-contraction/)).

**Step 3 (the iterates are bounded).** Let $M = \max(\|Q_0\|, R_{\max}/(1 - \gamma))$. If $\|Q_t\| \le M$, every target satisfies $|R_{t+1} + \gamma\max_{a'} Q_t(S_{t+1}, a')| \le R_{\max} + \gamma M \le M$, and the new value is a convex combination of two numbers in $[-M, M]$. By induction $\|Q_t\| \le M$ for all $t$. Also $\|q_*\| \le R_{\max}/(1-\gamma) \le M$. So $\|\Delta_t\| \le 2M$, with $\Delta_t = Q_t - q_*$, and the noise has $\mathbb{E}[w_t^2 \mid \mathcal{F}_t] \le C$ for a constant $C$.

**Step 4 (the noise averages out).** For a time $\tau$ and a pair $(s, a)$, define $W^\tau_\tau = 0$ and $W^\tau_{t+1} = (1 - \alpha_t)W^\tau_t + \alpha_t w_t$ for $t \ge \tau$. Under the Robbins-Monro conditions, with noise of mean 0 and bounded conditional variance, $W^\tau_t \to 0$ with probability 1 as $t \to \infty$. This is the basic lemma of stochastic approximation (Jaakkola, Jordan and Singh 1994; Bertsekas and Tsitsiklis 1996); the [Robbins-Monro conditions](/robbins-monro-conditions/) page explains why the two sums are needed.

**Step 5 (the envelope).** Subtract $q_* = T^* q_*$ from the update:

$$\Delta_{t+1}(s, a) = (1 - \alpha_t)\Delta_t(s, a) + \alpha_t F_t(s, a) + \alpha_t w_t(s, a), \qquad F_t = T^* Q_t - T^* q_*,$$

and by Step 2, $\|F_t\| \le \gamma\|\Delta_t\|$. Suppose that $\|\Delta_t\| \le D$ for all $t \ge \tau$. For each pair define $Y_\tau = D$ and $Y_{t+1} = (1 - \alpha_t)Y_t + \alpha_t\gamma D$. We claim $|\Delta_t - W^\tau_t| \le Y_t$ for all $t \ge \tau$. It holds at $t = \tau$. If it holds at $t$, then

$$\Delta_{t+1} - W^\tau_{t+1} = (1 - \alpha_t)(\Delta_t - W^\tau_t) + \alpha_t F_t ,$$

so $|\Delta_{t+1} - W^\tau_{t+1}| \le (1 - \alpha_t)Y_t + \alpha_t\gamma D = Y_{t+1}$, using $0 \le \alpha_t \le 1$ and $|F_t| \le \gamma D$. Now $Y_t - \gamma D = (1-\gamma)D\prod_{u=\tau}^{t-1}(1 - \alpha_u)$, which tends to 0 because $\sum_u \alpha_u = \infty$. With Step 4, $\limsup_t \|\Delta_t\| \le \gamma D$ with probability 1.

**Step 6 (the induction).** Fix $\beta$ with $\gamma < \beta < 1$. By Step 3, $\|\Delta_t\| \le D_0 = 2M$ for all $t \ge 0$. If $\|\Delta_t\| \le D_k$ for all $t \ge \tau_k$, Step 5 gives a random time $\tau_{k+1}$ after which $\|\Delta_t\| \le \beta D_k = D_{k+1}$, since $\gamma D_k < \beta D_k$. So $\|\Delta_t\| \le \beta^k D_0$ for all large $t$, for every $k$, which means $\Delta_t \to 0$, that is, $Q_t \to q_*$, with probability 1. $\blacksquare$

The original proof of Watkins and Dayan (1992) is different: it builds an artificial MDP, the action-replay process, from the stored samples, shows that $Q_t$ is exactly the optimal value of this process, and shows that the process tends to the real MDP.

## Consequences

- **The greedy policy becomes optimal.** In a finite MDP, let $g > 0$ be the smallest gap between $q_*(s, a^*)$ and a non-optimal $q_*(s, a)$. Once $\|Q_t - q_*\| < g/2$, every greedy action for $Q_t$ is optimal. So the greedy policy is optimal after a finite random time.
- **Off-policy learning works.** The theorem does not depend on the behavior policy, only on the visits and the steps. Learning from a log, from another agent or from replayed data converges in the tabular case, if the data cover all pairs.
- **SARSA.** The same scheme, with an extra term that vanishes under GLIE exploration, proves the convergence of [SARSA](/sarsa/) (Singh, Jaakkola, Littman and Szepesvari 2000) and of [Expected SARSA](/expected-sarsa/).
- **Double Q-learning.** van Hasselt (2010) proves the convergence of [Double Q-learning](/double-q-learning/) with a lemma of the same kind.
- **Other operators.** Replacing $T^*$ by any max-norm contraction gives convergence of the matching sampled algorithm, for example [minimax-Q](/minimax-q/) for zero-sum Markov games and TD(λ) for policy evaluation.

## Tightness

- **Every pair must be updated infinitely often.** A pair that is never tried keeps its initial value, and the max target of its state can then be wrong forever.
- **$\sum_t \alpha_t = \infty$ is needed.** Take one pair with reward 1 and a terminal next state, so $q_* = 1$ and $Q_{n+1} = Q_n + \alpha_n(1 - Q_n)$. Then $1 - Q_n = (1 - Q_0)\prod_{k<n}(1 - \alpha_k)$, and for steps in $(0, 1)$ this product tends to a positive limit when $\sum_k \alpha_k < \infty$. So $Q_n$ stops short of 1.
- **$\sum_t \alpha_t^2 < \infty$ is needed for convergence with probability 1.** With a constant step $\alpha$ and a reward of variance $\sigma^2$ in the example above, $Q_n$ keeps a variance near $\alpha\sigma^2/(2 - \alpha)$, so it does not converge. It only stays near $q_*$ on average.
- **Rates.** The theorem gives no rate. Even-Dar and Mansour (2003) show that with $\alpha = 1/n(s, a)$ the time to reach a given accuracy can grow exponentially in $1/(1 - \gamma)$, and that steps $1/n^\omega$ with $1/2 < \omega < 1$ give bounds polynomial in $1/(1-\gamma)$.
- **Function approximation.** The proof uses the max norm on a table. With function approximation, off-policy data and bootstrapping, Q-learning can diverge ([deadly triad](/deadly-triad/)), and no general convergence result holds.
- **$\gamma = 1$.** For undiscounted tasks the operator is not a contraction in general. Convergence still holds in stochastic shortest path problems where every policy reaches the terminal state with probability 1 (Tsitsiklis 1994), but not without such a condition.

## History

Watkins (1989) introduced Q-learning with a sketch of the convergence argument. Watkins and Dayan (1992) gave the full proof by the action-replay process. In 1994, Jaakkola, Jordan and Singh, and independently Tsitsiklis, proved convergence as a case of asynchronous stochastic approximation for contractions, with Robbins-Monro steps per pair; this form of the proof extended at once to TD(λ) and later to SARSA. Even-Dar and Mansour (2003) studied the rates.

## References
