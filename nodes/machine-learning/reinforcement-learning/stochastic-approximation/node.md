---
tag: TVB7PM
kind: technique
slug: stochastic-approximation
name: Stochastic approximation
aliases:
- stochastic approximation algorithms
- ODE method for stochastic approximation
area: machine-learning/reinforcement-learning
level: advanced
summary: "Find a zero of a mean field h from noisy samples by x_(n+1) = x_n + a_n (h(x_n) + noise). The ODE method: the iterates track dx/dt = h(x) and settle at its stable points."
prereqs: [robbins-monro-algorithm, martingale, conditional-expectation]
see_also: [robbins-monro-conditions, stochastic-gradient-descent, temporal-difference-learning, q-learning, tabular-q-learning-convergence, gradient-temporal-difference, actor-critic, value-function-approximation]
sources:
  - paper: doi:10.1214/aoms/1177729586
    title: Herbert Robbins and Sutton Monro, A stochastic approximation method, Annals of Mathematical Statistics 22(3), 1951, pages 400 to 407
    locator: the first stochastic approximation iteration and its step conditions
  - paper: doi:10.1214/aoms/1177729392
    title: Jack Kiefer and Jacob Wolfowitz, Stochastic estimation of the maximum of a regression function, Annals of Mathematical Statistics 23(3), 1952, pages 462 to 466
    locator: the finite difference version that locates a maximum
  - book: isbn:9780387008943
    title: Harold J. Kushner and G. George Yin, Stochastic Approximation and Recursive Algorithms and Applications, second edition, Springer, 2003
    locator: Chapter 5 (convergence with probability one by the ODE method), Chapter 6 (correlated and Markov noise), Chapter 8 (weak convergence with constant steps)
  - book: isbn:9780521515924
    title: Vivek S. Borkar, Stochastic Approximation, A Dynamical Systems Viewpoint, Cambridge University Press, 2008
    locator: Chapter 2 (the basic convergence theorem by the ODE method), Chapter 3 (stability of the iterates), Chapter 6 (two time scales), Chapter 7 (asynchronous schemes)
  - paper: doi:10.1137/S0363012997331639
    title: Vivek S. Borkar and Sean P. Meyn, The O.D.E. method for convergence of stochastic approximation and reinforcement learning, SIAM Journal on Control and Optimization 38(2), 2000, pages 447 to 469
    locator: the scaled limit ODE test that proves the iterates stay bounded
  - paper: doi:10.1007/BF00993306
    title: John N. Tsitsiklis, Asynchronous stochastic approximation and Q-learning, Machine Learning 16(3), 1994, pages 185 to 202
    locator: asynchronous stochastic approximation for a sup-norm pseudo-contraction, applied to Q-learning
---

Stochastic approximation is the family of iterative methods that find a zero of a function $h : \mathbb{R}^d \to \mathbb{R}^d$ when only noisy values of $h$ can be observed. The basic iteration is $x_{n+1} = x_n + a_n\bigl(h(x_n) + M_{n+1}\bigr)$, with small steps $a_n$ and zero-mean noise $M_{n+1}$. The ODE method shows that, under the [Robbins-Monro conditions](/robbins-monro-conditions/) on the steps, the iterates follow the solutions of the ordinary differential equation $\dot{x} = h(x)$ and converge to its stable equilibria. The [Robbins-Monro algorithm](/robbins-monro-algorithm/) is the first and simplest case; [stochastic gradient descent](/stochastic-gradient-descent/), [temporal difference learning](/temporal-difference-learning/) and [Q-learning](/q-learning/) are later ones.

## In plain words

You want the point where some average quantity is zero, but you can only measure that quantity with noise. At each step you take one measurement at your current point and move a small distance in the direction it gives. One measurement is unreliable, but many small moves average the noise out.

If the moves are very small, the path of your point looks like a smooth curve: the curve you would follow if you could see the true average with no noise. So you can study the noisy method by studying that smooth curve. Where the smooth curve settles, the noisy method also settles, provided the moves shrink at the right speed and the point does not run off to infinity.

## When it applies

Look for these signals in a problem.

- The target is a root or an equilibrium: a point where an expectation is zero, such as $\mathbb{E}[\nabla \ell(x, \xi)] = 0$ for a minimum or $\mathbb{E}[\text{TD error} \cdot \text{features}] = 0$ for a TD fixed point.
- One sample of the quantity is cheap, but its exact mean is not available, because the distribution is unknown or the sum is too large.
- The samples arrive one at a time, and you want to update the estimate after each one with $O(d)$ memory.

The setting on this page is: $x_n \in \mathbb{R}^d$; $\mathcal{F}_n$ is the history up to $x_n$; $h$ is the mean field; $M_{n+1}$ is a martingale difference noise, $\mathbb{E}[M_{n+1} \mid \mathcal{F}_n] = 0$; the steps $a_n > 0$ are fixed in advance. The [Robbins-Monro algorithm](/robbins-monro-algorithm/) page writes the same update with a minus sign, $x_{n+1} = x_n - a_n H(x_n, \xi_n)$, so its field is $-h$. Here the sign is chosen so that the limit ODE is $\dot{x} = h(x)$.

## The template

```pseudo id=main
STOCHASTIC-APPROXIMATION(sample, x₀, a, N, P)
L1  x ← x₀
L2  for n ← 0 to N − 1 do
L3      y ← sample(x)                ▷ y = h(x) + M_{n+1}, one noisy look at the field
L4      x ← P(x + aₙ y)              ▷ P projects onto a bounded set, or is the identity
L5  return x
```

The holes are the noisy oracle `sample`, the step sequence $a_n$ and the optional projection $P$. The cost is one call to `sample` and $O(d)$ arithmetic per step, with $\Theta(d)$ memory.

**The ODE method.** Put the iterates on a time axis with the clock $t_0 = 0$ and $t_{n+1} = t_n + a_n$, and join them by straight lines into a path $\bar{x}(t)$. Over a window of length $T$ of this clock, the update is

$$x_{m+k} = x_m + \sum_{j=m}^{m+k-1} a_j h(x_j) + \sum_{j=m}^{m+k-1} a_j M_{j+1}.$$

The first sum is an Euler scheme with steps $a_j$ for $\dot{x} = h(x)$. The second sum is a [martingale](/martingale/) whose variance is bounded by a constant times $\sum_{j \ge m} a_j^2$. When $\sum a_n^2 < \infty$ this tail tends to $0$, so the noise term vanishes on every window. When $a_n \to 0$ the Euler error also vanishes, and when $\sum a_n = \infty$ the clock $t_n$ runs to infinity, so the path sees the whole future of the ODE. The precise result (Borkar 2008, Chapter 2) assumes: $h$ is Lipschitz; $\sum a_n = \infty$ and $\sum a_n^2 < \infty$; $\mathbb{E}[\lVert M_{n+1}\rVert^2 \mid \mathcal{F}_n] \le K(1 + \lVert x_n\rVert^2)$; and $\sup_n \lVert x_n\rVert < \infty$ almost surely. Then, almost surely, for every $T > 0$,

$$\lim_{s \to \infty} \sup_{t \in [s, s + T]} \lVert \bar{x}(t) - x^s(t)\rVert = 0,$$

where $x^s$ is the solution of $\dot{x} = h(x)$ that starts at $\bar{x}(s)$ at time $s$. So $x_n$ converges to an invariant set of the ODE (a compact, connected, internally chain transitive one). If the ODE has a globally asymptotically stable equilibrium $x^*$, then $x_n \to x^*$ almost surely.

The boundedness assumption is not free. Borkar and Meyn (2000) give a test for it: if $h_\infty(x) = \lim_{c \to \infty} h(cx)/c$ exists and the origin is a globally asymptotically stable equilibrium of $\dot{x} = h_\infty(x)$, the iterates stay bounded. The step conditions themselves, why each one is needed and which step sequences meet them, are on the page [Robbins-Monro conditions](/robbins-monro-conditions/).

**A worked run.** Take $d = 2$ and the linear field $h(x) = b - Ax$ with

$$A = \begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}, \qquad b = \begin{pmatrix} 2 \\ 0 \end{pmatrix}, \qquad x^* = A^{-1}b = \begin{pmatrix} 1 \\ 1 \end{pmatrix}.$$

The eigenvalues of $A$ are $1 \pm i$, so the ODE $\dot{x} = b - Ax$ spirals into $x^*$. Its solution is $x(t) - x^* = e^{-t}R(t)(x_0 - x^*)$, where $R(t)$ is the rotation matrix with rows $(\cos t, -\sin t)$ and $(\sin t, \cos t)$. Start at $x_0 = (3, -1)$, use $a_n = 1/(n + 2)$, and add independent standard normal noise to each coordinate of each observation. The clock is $t_n = \sum_{k<n} 1/(k + 2)$.

| $n$ | $t_n$ | noisy run, seed 0 | noiseless iteration | ODE at time $t_n$ | mean $\lVert x_n - x^*\rVert$ over 100 seeds |
|---|---|---|---|---|---|
| 0 | 0 | (3, −1) | (3, −1) | (3, −1) | 2.828 |
| 1 | 0.5 | (3.471, 0.302) | (3, 1) | (2.646, 0.517) | 2.010 |
| 2 | 0.833 | (2.653, 1.482) | (2.333, 1.667) | (2.228, 1.059) | 1.569 |
| 10 | 2.020 | (1.151, 1.112) | (0.862, 1.449) | (1.124, 1.354) | 0.573 |
| 100 | 4.197 | (1.049, 0.991) | (0.970, 0.955) | (0.959, 0.989) | 0.128 |
| 1000 | 6.486 | (0.988, 1.033) | (1.005, 1.001) | (1.004, 0.998) | 0.041 |
| 10000 | 8.788 | (1.020, 0.996) | (1.000, 1.000) | (1.000, 1.000) | 0.013 |

The noiseless iteration is the Euler method for the ODE with steps $a_n$. Its first steps are large and it overshoots, but it joins the ODE path as the steps shrink. The noisy run follows the same spiral. The mean distance falls by about $\sqrt{10}$ for each factor of 10 in $n$, which is the $O(n^{-1/2})$ rate that steps $c/n$ give when $c$ times the smallest real part of an eigenvalue of $A$ exceeds $1/2$ (here $c = 1$ and the real part is $1$).

## Classic examples

- **The running mean.** With $h(x) = \mathbb{E}Z - x$, observations $Z_n - x_n$ and $a_n = 1/(n + 1)$, the iterate $x_{n+1}$ is exactly the mean of $Z_0, \ldots, Z_n$. The ODE is $\dot{x} = \mathbb{E}Z - x$, and the [law of large numbers](/law-of-large-numbers/) is a special case.
- **Root finding.** The [Robbins-Monro algorithm](/robbins-monro-algorithm/) finds the level at which a noisy response has a given mean. It has the field $-h$ in the sign convention of that page.
- **Stochastic gradient descent.** [Stochastic gradient descent](/stochastic-gradient-descent/) is the case $h(x) = -\nabla f(x)$, where the ODE is the gradient flow and $f$ is a Lyapunov function.
- **TD(0) with linear features.** [Temporal difference learning](/temporal-difference-learning/) with features $\phi$ updates $\theta$ by $a_n\delta_n\phi(s_n)$. Its mean field is $h(\theta) = b - A\theta$ with the matrices of [value function approximation](/value-function-approximation/), and on-policy $A$ is positive definite, so the ODE is stable. The noise is Markov, not a martingale difference, which needs the extra arguments of Tsitsiklis and Van Roy (1997).
- **Q-learning.** [Q-learning](/q-learning/) is an asynchronous scheme: one component, one state and action pair, changes per step. Its mean field is $TQ - Q$ for the Bellman optimality operator $T$, a sup-norm contraction. Tsitsiklis (1994) and the page [tabular Q-learning convergence](/tabular-q-learning-convergence/) give the proof.
- **Two time scales.** [Gradient temporal difference](/gradient-temporal-difference/) methods and [actor-critic](/actor-critic/) methods run two coupled iterations, a fast one with steps $\beta_n$ and a slow one with steps $\alpha_n$, with $\alpha_n/\beta_n \to 0$. The fast iterate sees the slow one as fixed and tracks its equilibrium $\lambda(x)$; the slow iterate then follows $\dot{x} = h(x, \lambda(x))$ (Borkar 2008, Chapter 6).

## Variations

- **Kiefer-Wolfowitz.** Estimate a gradient from two noisy function values at $x \pm c_n e_i$, to find a maximum without gradient samples (Kiefer and Wolfowitz 1952).
- **Projected stochastic approximation.** Apply a projection onto a compact convex set after each step, as in line L4. Then boundedness holds by design, and the limit ODE is the projected ODE (Kushner and Yin 2003).
- **Markov noise.** When the samples come from a Markov chain, as in reinforcement learning, the noise is correlated. The ODE is then the field averaged over the stationary distribution of the chain (Kushner and Yin 2003, Chapter 6).
- **Constant steps.** With $a_n = a$, the iterates do not converge. For small $a$, they stay in a neighborhood of the stable equilibria whose size goes to $0$ with $a$, and they can track a slowly moving target (Kushner and Yin 2003, Chapter 8).
- **Averaging.** Polyak-Ruppert averaging returns the mean of the iterates. See the [Robbins-Monro algorithm](/robbins-monro-algorithm/) page.

## Pitfalls

- **The iterates must stay bounded.** The ODE theorem assumes $\sup_n \lVert x_n\rVert < \infty$. Off-policy TD with linear features is a stochastic approximation scheme whose ODE can be unstable, and then its iterates go to infinity; see the [deadly triad](/deadly-triad/). Check the scaled ODE of Borkar and Meyn, or project.
- **A stable equilibrium is needed, not only a root.** The method converges to stable points of $\dot{x} = h(x)$. A root of $h$ where the Jacobian has an eigenvalue with positive real part is unstable, and the iterates leave it.
- **The sign convention.** With $x_{n+1} = x_n - a_n H$, the ODE is $\dot{x} = -h(x)$. Mixing the two conventions turns a stable point into an unstable one.
- **Rate depends on the step constant.** With $a_n = c/n$, the error is of order $n^{-1/2}$ only when $c$ times the smallest real part of the eigenvalues of $-\partial h(x^*)$ exceeds $1/2$. A smaller $c$ gives a slower rate.

## Exercises

1. Show that $x_{n+1} = x_n + \frac{1}{n + 1}(Z_n - x_n)$ with $x_0 = 0$ gives $x_{n+1} = \frac{1}{n + 1}\sum_{k=0}^{n} Z_k$.
2. Write tabular TD(0) for a fixed policy on a finite [Markov decision process](/markov-decision-process/) in the form $x_{n+1} = x_n + a_n(h(x_n) + M_{n+1})$ for the synchronous version that updates every state at each step. Identify $h$ and show that its only zero is $V^\pi$.
3. For the field $h(x) = x - x^3$ on $\mathbb{R}$, find the zeros and say which are stable equilibria of $\dot{x} = h(x)$. To which points can stochastic approximation with this field converge?

## References
