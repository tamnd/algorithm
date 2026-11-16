---
tag: Y83ZRN
kind: algorithm
slug: extremum-seeking-control
name: Extremum seeking control
aliases:
- extremum seeking
area: control/robust-and-adaptive-control
level: advanced
summary: Drives a system to the optimum of an unknown performance map by a small periodic dither and demodulation that estimates the gradient.
model: real-ram
complexity:
  vars: {N: the number of integration steps, n: the number of tuned parameters, c: the cost of one measurement of the map}
  time: {worst: O(N (n + c))}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 2000
  people: [Miroslav Krstić, Hsin-Hsiung Wang]
  note: "The method is much older, with roots in the 1920s and wide use in the 1950s and 1960s; Krstić and Wang gave in 2000 the first general proof of local convergence for a plant with dynamics, by averaging and singular perturbation."
prereqs: [adaptive-control, gradient-descent, averaging-method]
see_also: [derivative-free-optimization, stochastic-approximation, robbins-monro-algorithm, hill-climbing, mit-rule, iterative-learning-control, adaptive-filtering]
sources:
  - book: isbn:9780471468592
    title: "Kartik B. Ariyur and Miroslav Krstić, Real-Time Optimization by Extremum-Seeking Control, Wiley 2003"
    locator: "Chapter 1, Introduction to extremum seeking (the basic scheme with a dither, a washout filter and a demodulator, and the averaging analysis)"
  - paper: doi:10.1016/S0005-1098(99)00183-1
    title: "Miroslav Krstić and Hsin-Hsiung Wang, Stability of extremum seeking feedback for general nonlinear dynamic systems, Automatica 36(4), 2000"
    locator: "pages 595 to 601 (the local convergence theorem for a plant with dynamics)"
  - paper: doi:10.1016/j.automatica.2006.01.014
    title: "Ying Tan, Dragan Nešić and Iven Mareels, On non-local stability properties of extremum seeking control, Automatica 42(6), 2006"
    locator: "pages 889 to 903 (semi-global practical convergence with a tuning of the dither amplitude, the frequency and the gain)"
  - book: isbn:9780130673893
    title: "Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall 2002"
    locator: "Chapter 10, Section 10.4, Averaging (the averaging theorem for periodic systems used in the proof)"
---

Extremum seeking control is a feedback method that moves the input $\theta$ of a system to the minimum or maximum of a performance map $J(\theta)$ that is not known, using only measurements of $J$. It adds a small sine dither $a\sin\omega t$ to $\theta$, multiplies the measured output by the same sine, and integrates the product; on average this is [gradient descent](/gradient-descent/) with the gradient estimated from the response to the dither. It is close to [derivative-free optimization](/derivative-free-optimization/), but the difference is the setting: derivative-free optimization calls a static function at points that it chooses, one call after the other, while extremum seeking runs continuously in closed loop with a plant that has dynamics and noise, and its gradient estimate comes from the dither and not from separate function calls.

## In plain words

You want to find the setting of a knob that gives the best output, but you have no formula for the output. You move the knob a little back and forth in a regular rhythm around its current value. If the output goes up when the knob goes up, the best point is lower; if the output goes down, the best point is higher. A simple filter finds this relation by multiplying the output by the same rhythm and averaging. The result pushes the center of the knob slowly in the good direction. The rhythm must be fast compared with the slow movement of the center, and slow compared with the response of the system, so that each measurement belongs to the right knob position.

## The problem

A plant with input $\theta \in \mathbb{R}^n$ and a scalar output $y$ is given. After the transients, a constant $\theta$ gives the output $y = J(\theta)$. The map $J$ is smooth but unknown, and it has a minimum at an unknown $\theta^*$ with $\nabla J(\theta^*) = 0$ and a positive definite Hessian. The aim is to drive $\theta$ to a neighborhood of $\theta^*$ and keep it there, using only measurements of $y$. For a maximum, replace $J$ by $-J$. On this page the plant has no dynamics, so $y = J(\theta)$ at each instant; the section Variants and improvements treats a plant with dynamics.

## The algorithm

Let $\hat\theta$ be the current estimate. The scheme has four parts.

- **Dither.** Apply $\theta = \hat\theta + d(t)$ with $d_i(t) = a_i\sin\omega_i t$, a small amplitude $a_i > 0$, and distinct frequencies $\omega_i$ for the components.
- **Washout.** The high-pass filter $\eta' = h(y - \eta)$ with $h > 0$ follows the slow part of $y$, so $y - \eta$ is mainly the response to the dither.
- **Demodulation.** Multiply: $\xi_i = (y - \eta)\sin\omega_i t$. The mean of $\xi_i$ over one period is about $(a_i/2)\,\partial J/\partial\theta_i$.
- **Integration.** Set $\hat\theta_i' = -k_i\xi_i$ with $k_i > 0$ for a minimum. For a maximum use $k_i < 0$.

The averaged system is $\bar\theta_i' = -k_i(a_i/2)\,\partial J/\partial\theta_i(\bar\theta)$ plus a term of order $a^3$: a gradient flow with the gain $k_i a_i/2$. The implementation integrates $\hat\theta$ and $\eta$ with the classical fourth order Runge-Kutta method and a fixed step $dt$.

```pseudo id=main
EXTREMUM-SEEKING(J, a, ω, k, h, θ₀, dt, N)        ▷ N steps of length dt
L1  θ̂ ← θ₀; η ← J(θ₀)
L2  for i ← 0 to N - 1 do
L3      d ← a sin(ω t)                            ▷ one sine per component, t = i dt
L4      y ← J(θ̂ + d)                              ▷ measure the map
L5      η' ← h (y - η)                            ▷ washout filter
L6      ξ ← (y - η) sin(ω t)                      ▷ demodulation
L7      θ̂' ← -k ξ                                 ▷ integrate the gradient estimate
L8      advance θ̂ and η by one RK4 step of length dt
L9  return θ̂
```

Lines L3 to L7 are the right-hand side of the differential equation; RK4 evaluates them four times per step in line L8.

## Example

Take $J(\theta) = (\theta - 2)^2 + 1$, the start $\hat\theta(0) = 0$, the dither $a = 0.2$ and $\omega = 50$ rad/s, the gain $k = 1$ and the washout $h = 5$. The averaged system is $\bar\theta' = -k(a/2)\cdot 2(\bar\theta - 2) = -0.2(\bar\theta - 2)$, so $\bar\theta(t) = 2 - 2e^{-0.2t}$. With RK4 and $dt = 0.005$ s (6000 steps for 30 s), the simulation gives:

| $t$ | $\hat\theta(t)$ | $\bar\theta(t)$ | $y(t)$ |
|---|---|---|---|
| 0 | 0 | 0 | 5 |
| 2 | 0.6535 | 0.6594 | 3.0959 |
| 5 | 1.2578 | 1.2642 | 1.8766 |
| 10 | 1.7235 | 1.7293 | 1.1369 |
| 15 | 1.8975 | 1.9004 | 1.0022 |
| 30 | 1.9947 | 1.9950 | 1.0416 |

This is a measurement: the largest gap between $\hat\theta$ and $\bar\theta$ over the run is 0.011. The output $y$ exceeds the minimum 1 by $(a\sin\omega t + \hat\theta - 2)^2$, which does not die out because the dither never stops; this is the price of the method. The excess is at most $(a + |\hat\theta - 2|)^2$, which tends to $a^2 = 0.04$ as $\hat\theta \to 2$; at $t = 30$ it is at most $0.2053^2 = 0.0421$, and $y = 1.0416$.

The same loop with $a = 0.1$, $\omega = 10$, $k = 5$ and $h = 1$ has the averaged rate $ka = 0.5$ in place of 0.2, but the time scales are not well separated. Then $\hat\theta(1) = 2.04$ while $\bar\theta(1) = 0.79$: the washout lags, $y - \eta$ is large, and the oscillation of $\hat\theta$ is no longer small. The loop still reaches $|\hat\theta - 2| < 0.002$ at $t = 30$, but the averaged model fails to describe the transient (a measurement).

For two parameters with $J = (\theta_1 - 1)^2 + 2(\theta_2 + 1)^2 + 3$, the frequencies 50 and 70 rad/s, $a = 0.2$ and $k = 1$, the averaged rates are 0.2 and 0.4, and the simulation stays within 0.03 of $(1 - e^{-0.2t}, -1 + e^{-0.4t})$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has three parts. First, the demodulation identity: the mean of $(J(\theta + a\sin\tau) - c)\sin\tau$ over one period is $(a/2)J'(\theta) + (a^3/16)J'''(\theta) + O(a^5)$ for any constant $c$, and exactly $(a/2)J'(\theta)$ for a quadratic $J$. Second, the averaged system: in the time $\tau = \omega t$ the loop is $\epsilon$ times a periodic vector field with $\epsilon = 1/\omega$, and its average decouples, with $\bar\theta' = -k M(\bar\theta)$ where $M$ is the mean above. For a quadratic $J$ the averaged equilibrium is exponentially stable with the rate $k a c$, where $c$ is the curvature. Third, by the averaging theorem (Khalil, Theorem 10.4), for $\omega$ large enough the real loop has an exponentially attractive periodic solution within $O(1/\omega)$ of that equilibrium, so $\hat\theta$ converges to an $O(1/\omega + a^2)$ neighborhood of $\theta^*$. This is a local theorem; Tan, Nešić and Mareels (2006) give a semi-global version.

## Complexity

The cost is that of a fixed step simulation in the real-RAM model. Each RK4 step evaluates the right-hand side four times, and each evaluation costs one measurement of the map ($c$ operations) and $O(n)$ for the dither, the demodulation and the update. So $N$ steps cost $O(N(n + c))$ and the memory is $O(n)$ besides the output samples. In a real loop, the measurement is the plant itself, and the controller costs $O(n)$ per sample.

## Properties

- **Gradient flow on average.** Theorem for a quadratic map: the averaged update is exactly $-k_i(a_i/2)\,\partial J/\partial\theta_i$, with no bias.
- **Bias for other maps.** The averaged equilibrium solves $M(\theta) = 0$, which differs from $\theta^*$ by $O(a^2)$. For $J = \theta^4$ at $\theta = 1$ and $a = 0.1$, the mean is $0.2015$ in place of $(a/2)J' = 0.2$ (an exact computation, checked in the tests).
- **Persistent oscillation.** The dither stays on, so $y$ oscillates around $J(\hat\theta)$ with a mean excess of about $a^2 J''/4$. The loss is the price for a gradient estimate.
- **Time scales.** The analysis needs the plant to be fast, the dither to be slower than the plant, and the adaptation $k a$ to be slower than the dither. These conditions are qualitative; the constants in the theorems are not explicit.
- **Local result.** The averaging theorem gives convergence from a neighborhood of $\theta^*$ or, for a quadratic map, from a compact set that grows as $\omega$ grows.

## Variants and improvements

- **Plant with dynamics.** If $\theta$ drives a plant with an exponentially attractive equilibrium $x = \ell(\theta)$ and $J(\theta) = h(\ell(\theta))$, the dither must be slow compared with the plant. Krstić and Wang (2000) proved local convergence for this case with averaging and singular perturbation.
- **Phase compensation.** When the plant shifts the phase of the dither, demodulate with $\sin(\omega t - \phi)$ for a phase estimate $\phi$; otherwise the gain of the averaged loop shrinks by $\cos\phi$.
- **Newton based extremum seeking.** Estimate the Hessian with a second demodulation signal and invert it, so the rate does not depend on the curvature.
- **Stochastic dither.** Replace the sines by random signals; this is close to [stochastic approximation](/stochastic-approximation/) and to the simultaneous perturbation method SPSA.
- **Sliding mode and relay versions.** Replace the sine by a switching signal; they are faster but give a larger oscillation.

## When to use it

Use extremum seeking when a plant has an optimum that moves slowly, the map is unknown, and the output can be measured continuously, for example the power of a wind turbine or a solar panel, the efficiency of a combustion process, or the formation flight of aircraft. It needs no model, but it is slow, because the dither must be slower than the plant and the adaptation slower than the dither. If the map can be evaluated cheaply and on demand, use [derivative-free optimization](/derivative-free-optimization/) or [hill climbing](/hill-climbing/). If a model is available, a model based optimizer is faster.

## Pitfalls

- **Poor time scale separation.** With a large gain or a slow dither, the averaged model fails; the second example shows a large overshoot.
- **Equal frequencies.** Two components with the same frequency cannot be separated by the demodulation; use distinct frequencies, and for a map with cubic or higher terms avoid frequencies that are sums or differences of others.
- **Wrong sign of the gain.** With $k > 0$ the loop seeks a minimum and with $k < 0$ a maximum. A wrong sign sends $\hat\theta$ away from the optimum.
- **Plant phase lag.** A dither faster than the plant arrives with a phase shift; above $90$ degrees the update has the wrong sign.
- **Noise and drift.** Measurement noise at the dither frequency enters the gradient estimate; a slow drift of the map without a washout filter adds a bias.

## Implementations

## History

Extremum seeking is one of the oldest adaptive methods. Leblanc (1922) is often cited as the first use, for the power transfer to an electric tram. Draper and Li (1951) studied the optimization of the spark timing of an engine with a similar loop, and the method was common in the 1950s and 1960s under names such as optimalizing control. A general proof of local convergence for a plant with dynamics came only with Krstić and Wang (2000). Tan, Nešić and Mareels (2006) proved semi-global practical convergence. Ariyur and Krstić (2003) give a full account of the design.

## References
