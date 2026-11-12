---
tag: 4D15PJ
kind: concept
slug: deadly-triad
name: Deadly triad
area: machine-learning/reinforcement-learning
level: advanced
summary: "Function approximation, bootstrapping and off-policy training together can make TD value estimates diverge. Any two of the three are safe in the linear case."
prereqs: [value-function-approximation, importance-sampling-off-policy]
see_also: [gradient-temporal-difference, dqn, q-learning, retrace, experience-replay, offline-reinforcement-learning, fitted-q-iteration, least-squares-td]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 11.2 (examples of off-policy divergence, Baird's counterexample, Example 11.1), Section 11.3 (the deadly triad)
  - paper: doi:10.1016/B978-1-55860-377-6.50013-X
    title: Leemon Baird, Residual algorithms, Reinforcement learning with function approximation, Machine Learning Proceedings 1995, pages 30 to 37
    locator: the star counterexample
  - paper: doi:10.1007/BF00114724
    title: John N. Tsitsiklis and Benjamin Van Roy, Feature-based methods for large scale dynamic programming, Machine Learning 22, 1996, pages 59 to 94
    locator: the two-state example on which value iteration with least-squares fitting diverges
  - paper: doi:10.1109/9.580874
    title: John N. Tsitsiklis and Benjamin Van Roy, An analysis of temporal-difference learning with function approximation, IEEE Transactions on Automatic Control 42(5), 1997, pages 674 to 690
    locator: Theorem 1 (on-policy convergence), Section IX (divergence off-policy and with nonlinear approximators)
  - paper: arxiv:1812.02648
    title: Hado van Hasselt, Yotam Doron, Florian Strub, Matteo Hessel, Nicolas Sonnerat and Joseph Modayil, Deep reinforcement learning and the deadly triad, 2018
    locator: the empirical study of divergence in deep Q-learning variants
---

The deadly triad is the name Sutton and Barto give to three ingredients whose combination can make temporal difference methods unstable: function approximation, bootstrapping, and off-policy training. With all three, the value estimates can grow without limit, even for a fixed target policy, exact expected updates and linear features that can represent the true values. With any two of the three, linear methods are stable. The name is from Sutton and Barto (2018, Section 11.3); the examples behind it are from Baird (1995) and Tsitsiklis and Van Roy (1996, 1997).

## In plain words

Three habits make learning values efficient. You share what you learn between similar states instead of keeping a separate number for each. You update a guess using another guess, instead of waiting for the final outcome. And you learn about one way of acting while you behave in another way.

Each habit alone is fine, and so is each pair. But all three together can feed on each other. A guess is pulled up toward a neighbor's guess; because the guesses share parameters, the neighbor rises too; and because the data come from a different behavior, the corrections that would pull the neighbor back down are too rare. The loop can repeat until the numbers become huge.

## The idea

The three ingredients are:

- **Function approximation.** The values are $\hat{v}(s) = \phi(s)^\top w$ with fewer weights than states, so one update changes the estimates of many states. See [value function approximation](/value-function-approximation/).
- **Bootstrapping.** The update target contains current estimates, as in $r + \gamma\hat{v}(s')$ for [temporal difference learning](/temporal-difference-learning/) or dynamic programming, instead of only observed rewards.
- **Off-policy training.** The states and actions are weighted by a distribution $d$ that is not the on-policy distribution of the target policy, as in [Q-learning](/q-learning/) or any use of [importance sampling](/importance-sampling-off-policy/) to learn about $\pi$ from data of $\mu$.

**Where the instability comes from.** For linear features and the target policy's transition matrix $P$, the expected semi-gradient TD update with update weights $d$ is

$$w \leftarrow w + \alpha(b - Aw), \qquad A = \Phi^\top D(I - \gamma P)\Phi, \qquad b = \Phi^\top D r, \qquad D = \operatorname{diag}(d).$$

This iteration is stable for small $\alpha$ exactly when every eigenvalue of $A$ has a positive real part. Remove any one ingredient and that holds:

- **Without function approximation** ($\Phi = I$), the update of $w(s)$ is $\alpha d(s)\bigl((Tw)(s) - w(s)\bigr)$ with the Bellman operator $T$, a $\gamma$-contraction in the max norm. It is asynchronous value iteration with steps $\alpha d(s) \le 1$, and it converges for every positive $d$.
- **Without bootstrapping**, the target is a fixed number, such as the true value or a Monte Carlo return, and the update is gradient descent on the convex function $\sum_s d(s)(\text{target}(s) - \phi(s)^\top w)^2$. It converges for small $\alpha$ and every $d$.
- **On-policy**, $d$ is the stationary distribution of $P$. Then $\lVert Pv\rVert_D \le \lVert v\rVert_D$, which gives $x^\top Ax \ge (1 - \gamma)\lVert\Phi x\rVert_D^2 > 0$, so $A$ is positive definite (Tsitsiklis and Van Roy 1997).

With all three, $D$ is not matched to $P$, the inequality $\lVert Pv\rVert_D \le \lVert v\rVert_D$ can fail, and $A$ can have an eigenvalue with negative real part. Then $w$ diverges from almost every start, for every step size.

**The smallest case.** Take two states whose features are the numbers $1$ and $2$, so their values are $w$ and $2w$. The first state moves to the second with reward $0$. If the data contain only this transition (off-policy, because the second state is never updated), the TD error is $\delta = 2\gamma w - w$, and the update is

$$w \leftarrow \bigl(1 + \alpha(2\gamma - 1)\bigr)w.$$

For $\gamma > 1/2$ the factor exceeds $1$, so $w$ grows geometrically from any $w \ne 0$, although the true value is $0$ (Sutton and Barto 2018, Section 11.2).

**Not caused by sampling.** Tsitsiklis and Van Roy (1996) extend this example: the second state stays where it is with probability $1 - \epsilon$ and ends the episode otherwise. Run exact value iteration and fit each new value function by least squares with equal weight on the two states:

$$w_{k+1} = \arg\min_w\bigl[(w - 2\gamma w_k)^2 + (2w - 2\gamma(1 - \epsilon)w_k)^2\bigr] = \frac{\gamma(6 - 4\epsilon)}{5}\,w_k.$$

With $\epsilon = 1/10$ and $\gamma = 99/100$, the factor is $693/625 \approx 1.109$, so $w_k$ grows without limit. There is no noise and no step size here: exact expectations and exact regressions still diverge. If the two states are weighted by how often the policy visits them, $\epsilon$ and $1$ in proportion, the expected TD update becomes $w \leftarrow w - \alpha\frac{4(1 - \gamma) + \epsilon(1 + 2\gamma)}{1 + \epsilon}w$, which shrinks $w$ for every $\gamma < 1$.

## Examples

**Baird's counterexample.** Seven states and eight weights (Baird 1995). The six upper states have values $2w_i + w_8$ and the lower state has value $w_7 + 2w_8$. The target policy always moves to the lower state, all rewards are $0$, $\gamma = 0.99$, and the states are weighted uniformly, which is the distribution under a behavior policy that moves to a uniform upper state with probability $6/7$. The features span every value function on the seven states, so $w$ can represent the true values $0$ exactly. Start from $w = (1, 1, 1, 1, 1, 1, 10, 1)$ and apply the expected update above with $\alpha = 0.01$:

| setting | ingredients | result |
|---|---|---|
| linear features, bootstrapping, uniform weights | all three | $\lVert w\rVert$ = 10.61 after 10 updates, 16.83 after 100, 436.9 after 1000, 5279 after 2000 |
| one weight per state, uniform weights, $\alpha = 1$ | no function approximation | every value below $10^{-3}$ after 8000 updates |
| linear features, target $0$ (the true value), uniform weights, $\alpha = 0.1$ | no bootstrapping | every value below $10^{-9}$ after 3000 updates |
| linear features, bootstrapping, all weight on the lower state, $\alpha = 0.1$ | on-policy | the value of the lower state goes to $0$ and $w$ stays bounded |

The on-policy distribution of this target policy puts all its weight on the lower state, because every transition leads there. Sampled semi-gradient TD diverges in the same way; see [gradient temporal difference](/gradient-temporal-difference/) for a sampled run, and for TDC, which stays bounded on the same problem.

**Q-learning with features.** [Q-learning](/q-learning/) bootstraps, learns about the greedy policy from exploratory data, and in large problems uses function approximation. So it has all three ingredients, and linear Q-learning has known divergent examples.

**Deep Q-networks.** [DQN](/dqn/) has all three ingredients and uses a target network and [experience replay](/experience-replay/) to make divergence less likely. Van Hasselt et al. (2018) found in experiments that unbounded growth of the values is uncommon in practice but does occur. In their runs it was less common with multi-step returns, which bootstrap less, and more common with stronger prioritization of the replayed data, which moves the data further from on-policy.

## Where it is used

- **Choosing a prediction method.** For off-policy prediction with linear features, use a method that is stable by design: [gradient temporal difference](/gradient-temporal-difference/) methods (GTD2, TDC), emphatic TD, or [least-squares TD](/least-squares-td/) with a check on the solution.
- **Multi-step returns.** Less bootstrapping means more stability. Methods such as [Retrace](/retrace/) and [V-trace](/v-trace/) use multi-step, truncated importance-weighted returns to trade bias, variance and stability.
- **Offline reinforcement learning.** [Offline reinforcement learning](/offline-reinforcement-learning/) works only with a fixed dataset, so it is off-policy by nature. Value overestimation there is often explained by the triad together with actions that the data never contain; [conservative Q-learning](/conservative-q-learning/) is one response.
- **Batch methods.** [Fitted Q iteration](/fitted-q-iteration/) with averaging regressors, such as trees or nearest neighbors, is a contraction and avoids the divergence; with linear regression it can diverge as in the example of Tsitsiklis and Van Roy.

## References
