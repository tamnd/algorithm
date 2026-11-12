---
tag: 0BFJGH
kind: technique
slug: value-function-approximation
name: Value function approximation
aliases:
- function approximation in RL
- linear value function approximation
area: machine-learning/reinforcement-learning
level: core
summary: "Represent a value function as Phi theta, a function of features. On-policy linear TD finds the fixed point of the projected Bellman equation, A theta = b, near the best fit."
prereqs: [state-value-function, temporal-difference-learning, least-squares-problem, stationary-distribution]
see_also: [least-squares-td, gradient-temporal-difference, deadly-triad, fitted-q-iteration, stochastic-approximation, dqn, policy-evaluation, successor-representation]
sources:
  - paper: doi:10.1109/9.580874
    title: John N. Tsitsiklis and Benjamin Van Roy, An analysis of temporal-difference learning with function approximation, IEEE Transactions on Automatic Control 42(5), 1997, pages 674 to 690
    locator: Theorem 1 (convergence of on-policy linear TD(lambda) and the error bound), Section IX (divergence examples)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapter 9, Sections 9.3 and 9.4 (semi-gradient methods and the TD fixed point)
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: Chapter 6 (approximate DP with linear architectures)
---

Value function approximation replaces the table of a [state value function](/state-value-function/) $V^\pi(s)$ by a function $\hat{v}(s; \theta)$ with far fewer parameters than states. The main case is linear: $\hat{v}(s; \theta) = \phi(s)^\top\theta$, with a feature vector $\phi(s) \in \mathbb{R}^d$. Stack the features as the rows of a matrix $\Phi$, so the approximate values are $\Phi\theta$. [Temporal difference learning](/temporal-difference-learning/) with these features does not find the best fit to $V^\pi$. It finds the solution of the projected Bellman equation $\Phi\theta = \Pi T^\pi \Phi\theta$, which is the linear system $A\theta = b$. When the data come from the policy itself, this solution exists, is unique, and is close to the best fit (Tsitsiklis and Van Roy 1997).

## In plain words

A game or a robot can have more states than you could ever list in a table. So you describe each state by a few numbers, its features, and say that its value is a weighted sum of those numbers. Learning the value then means learning a small set of weights.

States that share features now share what is learned, so experience in one state also improves the estimates for similar states. The price is that no set of weights may fit every state exactly.

TD learning adjusts the weights so that each estimate agrees with the reward plus the next estimate, on average over the states that the policy actually visits. That average gives a single answer, and that answer is never much worse than the best weighted sum. If the states are visited in the wrong proportions, this guarantee is lost.

## When it applies

- The state space is large or continuous, so a table of values cannot be stored or filled from the available experience.
- There are features $\phi(s)$ such that similar states have similar features: tile codings, radial basis functions, polynomials, or the last layer of a neural network.
- You evaluate a fixed policy $\pi$ from its own trajectories (on-policy), or you accept the extra risks of the off-policy case.

The setting on this page is: a finite [Markov decision process](/markov-decision-process/) with a fixed policy, which gives a Markov chain with transition matrix $P$ on $n$ states and expected rewards $r(s)$; a discount $\gamma < 1$; a [stationary distribution](/stationary-distribution/) $\mu$ with $\mu P = \mu$ and $\mu(s) > 0$ for all $s$; $D = \operatorname{diag}(\mu)$ and the weighted norm $\lVert v\rVert_D^2 = \sum_s \mu(s)v(s)^2$; and $\Phi \in \mathbb{R}^{n \times d}$ with linearly independent columns. The Bellman operator is $T v = r + \gamma P v$, with fixed point $V = (I - \gamma P)^{-1} r$.

## The template

```pseudo id=main
SEMI-GRADIENT-TD(0)(P, r, γ, φ, N, α)
L1  θ ← 0
L2  s ← s₀
L3  for t ← 0 to N − 1 do
L4      s′ ← sample from P(s, ·)            ▷ one step of the policy
L5      δ ← r(s) + γ φ(s′)ᵀθ − φ(s)ᵀθ        ▷ the TD error
L6      θ ← θ + αₜ δ φ(s)                    ▷ gradient of φ(s)ᵀθ only, not of the target
L7      s ← s′
L8  return θ
```

The holes are the features $\phi$ and the steps $\alpha_t$. Each step costs $O(d)$ time and the method keeps $\Theta(d)$ memory. The update is called semi-gradient because it differentiates the estimate $\phi(s)^\top\theta$ but treats the target $r + \gamma\phi(s')^\top\theta$ as a constant. It is not the gradient of any fixed loss.

**The mean update.** When $s$ is drawn from $\mu$ and $s'$ from $P(s, \cdot)$, the expected change of $\theta$ in line L6 is $\alpha_t(b - A\theta)$ with

$$A = \Phi^\top D (I - \gamma P)\Phi, \qquad b = \Phi^\top D r.$$

So semi-gradient TD(0) is [stochastic approximation](/stochastic-approximation/) with the mean field $h(\theta) = b - A\theta$, and its limit ODE is $\dot{\theta} = b - A\theta$. The candidate limit is the TD fixed point $\theta^* = A^{-1}b$.

**The projected Bellman equation.** Let $\Pi = \Phi(\Phi^\top D\Phi)^{-1}\Phi^\top D$ be the projection onto the span of the features in the $D$ norm, so $\Pi v$ is the best fit $\Phi\theta$ to $v$ by weighted [least squares](/least-squares-problem/). A vector $\Phi\theta$ satisfies $\Phi\theta = \Pi T\Phi\theta$ exactly when the residual $T\Phi\theta - \Phi\theta$ is $D$-orthogonal to every column of $\Phi$, that is $\Phi^\top D(r + \gamma P\Phi\theta - \Phi\theta) = 0$, which is $A\theta = b$.

**Why it works on-policy.** Four facts give the result.

1. $P$ does not expand the $D$ norm. By Jensen's inequality and $\mu P = \mu$, $\lVert Pv\rVert_D^2 = \sum_s \mu(s)\bigl(\sum_{s'} P(s, s')v(s')\bigr)^2 \le \sum_s \mu(s)\sum_{s'} P(s, s')v(s')^2 = \sum_{s'}\mu(s')v(s')^2 = \lVert v\rVert_D^2$.
2. $\Pi T$ is a $\gamma$-contraction in the $D$ norm. $\Pi$ is an orthogonal projection in the $D$ inner product, so $\lVert \Pi u\rVert_D \le \lVert u\rVert_D$, and $\lVert Tu - Tv\rVert_D = \gamma\lVert P(u - v)\rVert_D \le \gamma\lVert u - v\rVert_D$. So $\Pi T$ has exactly one fixed point, and it is $\Phi\theta^*$.
3. $A$ is positive definite (not symmetric in general). For $x \in \mathbb{R}^d$ and $u = \Phi x$, Cauchy-Schwarz and fact 1 give $x^\top A x = \lVert u\rVert_D^2 - \gamma\langle u, Pu\rangle_D \ge (1 - \gamma)\lVert u\rVert_D^2$, which is positive for $x \ne 0$. So every eigenvalue of $A$ has a positive real part, and $\dot{\theta} = b - A\theta$ converges to $\theta^*$ from every start.
4. The error bound. $V - \Phi\theta^* = (V - \Pi V) + (\Pi V - \Phi\theta^*)$, and the two parts are $D$-orthogonal. The second part is $\Pi T V - \Pi T\Phi\theta^*$, of norm at most $\gamma\lVert V - \Phi\theta^*\rVert_D$. So $\lVert V - \Phi\theta^*\rVert_D^2 \le \lVert V - \Pi V\rVert_D^2 + \gamma^2\lVert V - \Phi\theta^*\rVert_D^2$, which gives

$$\lVert \Phi\theta^* - V\rVert_D \le \frac{1}{\sqrt{1 - \gamma^2}}\,\lVert \Pi V - V\rVert_D \le \frac{1}{1 - \gamma}\,\lVert \Pi V - V\rVert_D.$$

Tsitsiklis and Van Roy (1997, Theorem 1) prove that TD($\lambda$) with linear features converges with probability one along a single trajectory of an ergodic chain, when the steps meet the [Robbins-Monro conditions](/robbins-monro-conditions/). The limit $\theta^*$ is the fixed point of $\Pi T^{(\lambda)}$, where $T^{(\lambda)}$ is the $\lambda$-weighted Bellman operator, and it satisfies $\lVert\Phi\theta^* - V\rVert_D \le \frac{1 - \lambda\gamma}{1 - \gamma}\lVert\Pi V - V\rVert_D$. At $\lambda = 0$ this is the right-hand bound above; at $\lambda = 1$ the limit is $\Pi V$ itself. The noise in the trajectory version is Markov, not a martingale difference, and their proof handles that.

**A worked example.** Take three states with

$$P = \begin{pmatrix} 1/2 & 1/2 & 0 \\ 1/4 & 1/2 & 1/4 \\ 0 & 1/2 & 1/2 \end{pmatrix}, \quad r = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}, \quad \gamma = \frac{9}{10}, \quad \Phi = \begin{pmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 3 \end{pmatrix}.$$

The stationary distribution is $\mu = (1/4, 1/2, 1/4)$, and the true values are $V = (81/44, 9/4, 161/44) \approx (1.841, 2.250, 3.659)$. These three numbers do not lie on a line in the feature values $0, 1, 3$, so no $\theta$ fits them exactly. The exact quantities are

$$A = \begin{pmatrix} 1/10 & 1/8 \\ 1/8 & 67/80 \end{pmatrix}, \qquad b = \begin{pmatrix} 1/4 \\ 3/4 \end{pmatrix}, \qquad \theta^* = A^{-1}b = \left(\frac{185}{109}, \frac{70}{109}\right) \approx (1.6972, 0.6422).$$

| quantity | weights | values at the 3 states | $\lVert \cdot - V\rVert_D^2$ |
|---|---|---|---|
| true values $V$ | none | (1.841, 2.250, 3.659) | 0 |
| TD fixed point $\Phi\theta^*$ | (1.6972, 0.6422) | (1.697, 2.339, 3.624) | 217841/23001616 ≈ 0.009471 |
| best fit $\Pi V$ | (1435/836, 131/209) ≈ (1.7165, 0.6268) | (1.717, 2.343, 3.597) | 169/18392 ≈ 0.009189 |

The TD fixed point is a different vector from the best fit, and its error is larger, as fact 4 allows. The ratio of the two errors in norm is $1.015$, far below the worst case $1/\sqrt{1 - \gamma^2} \approx 2.294$. Semi-gradient TD(0) on one trajectory from state 0, with $\alpha_t = 0.05/(1 + t/1000)$, gives these weights, averaged over seeds 0 to 3:

| steps $N$ | mean $\theta$ over 4 seeds |
|---|---|
| 1000 | (1.387, 0.623) |
| 10000 | (1.620, 0.650) |
| 120000 | (1.692, 0.637) |

The runs approach $\theta^* \approx (1.697, 0.642)$, not the best fit $(1.717, 0.627)$.

## Classic examples

- **Tabular TD as a special case.** With one-hot features, $\Phi = I$, the projection is the identity and the TD fixed point is $V$ itself. Linear approximation contains the table as its most expressive case.
- **Linear TD($\lambda$).** The same analysis with the operator $T^{(\lambda)}$ and [eligibility traces](/eligibility-traces/) gives the family of fixed points of Tsitsiklis and Van Roy, which moves from the TD(0) fixed point at $\lambda = 0$ to $\Pi V$ at $\lambda = 1$; see [TD(lambda)](/td-lambda/).
- **Least-squares TD.** [Least-squares TD](/least-squares-td/) estimates $A$ and $b$ from the data and solves $A\theta = b$ directly, with no step size.
- **Neural network values.** [DQN](/dqn/) uses a neural network for $\hat{q}(s, a; \theta)$ with a semi-gradient Q-learning update. The linear theory above does not cover it, and extra devices such as a target network and [experience replay](/experience-replay/) are used to keep it stable.
- **Batch fitting.** [Fitted Q iteration](/fitted-q-iteration/) applies a supervised regressor to Bellman targets in rounds, one regression per round.

## Variations

- **Monte Carlo targets.** Replace the TD target by the full return. This is true stochastic gradient descent on $\lVert\hat{v} - V\rVert_D^2$ and converges to $\Pi V$, at the cost of higher variance.
- **Gradient TD.** [Gradient temporal difference](/gradient-temporal-difference/) methods do true gradient descent on the mean squared projected Bellman error $\lVert\Pi T\Phi\theta - \Phi\theta\rVert_D^2$, which stays stable off-policy.
- **Action values.** For control, use features $\phi(s, a)$ and approximate $Q(s, a)$; the semi-gradient update becomes SARSA or Q-learning with features.
- **Nonlinear approximators.** With $\hat{v}(s; \theta)$ nonlinear in $\theta$, replace $\phi(s)$ in line L6 by the gradient $\nabla_\theta\hat{v}(s; \theta)$. Tsitsiklis and Van Roy (1997) show that convergence can fail in this case.

## Pitfalls

- **Off-policy data.** If the states are weighted by a distribution other than the on-policy $\mu$, fact 1 fails, $A$ need not be positive definite, and semi-gradient TD can diverge. Bootstrapping, function approximation and off-policy data together form the [deadly triad](/deadly-triad/).
- **TD does not minimize the value error.** The limit is the TD fixed point, not $\Pi V$. Do not judge a TD solution by the claim that it is the best fit in the feature space.
- **Dependent features.** If the columns of $\Phi$ are linearly dependent, $A$ is singular and $\theta^*$ is not unique, although $\Phi\theta^*$ still is.
- **The norm matters.** The guarantees hold in the $D$ norm. States that the policy rarely visits can have large errors that the bound does not show.

## Exercises

1. For the worked example, verify $A\theta^* = b$ with $\theta^* = (185/109, 70/109)$, and check that $\Pi T\Phi\theta^* = \Phi\theta^*$.
2. Show that with one-hot features the matrix $A$ equals $D(I - \gamma P)$ and that $A^{-1}b = V$.
3. Give a two-state chain and a weighting $\mu$ that is not stationary for which $\lVert Pv\rVert_D > \lVert v\rVert_D$ for some $v$.
4. Show that the Monte Carlo update $\theta \leftarrow \theta + \alpha(G - \phi(s)^\top\theta)\phi(s)$, with $G$ the return from $s$, has the mean field $\Phi^\top D(V - \Phi\theta)$, whose zero is the weights of $\Pi V$.

## References
