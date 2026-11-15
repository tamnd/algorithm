---
tag: 2CAHAK
kind: definition
slug: h-infinity-norm
name: H-infinity norm
aliases:
- peak gain of a system
area: control/robust-and-adaptive-control
level: core
summary: The supremum over frequency of the largest singular value of a transfer matrix with no poles in the closed right half plane. It is the L2 gain, the worst ratio of output to input L2 norm.
prereqs: [transfer-function, singular-value-decomposition, frequency-response]
see_also: [h-infinity-norm-computation, h2-norm, bounded-real-lemma, small-gain-theorem, model-uncertainty, h-infinity-control-problem, structured-singular-value, hankel-singular-values]
sources:
  - paper: "George Zames, Feedback and optimal sensitivity: model reference transformations, multiplicative seminorms, and approximate inverses, IEEE Transactions on Automatic Control 26(2), 301-320, 1981"
    locator: the use of the H-infinity norm of the weighted sensitivity as the design criterion
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 4, Performance Specifications (the H-infinity norm, the L2 gain and the bounds on the norm)
  - paper: doi:10.1007/BF02551385
    title: Stephen Boyd, Venkataramanan Balakrishnan and Pierre Kabamba, A bisection method for computing the H-infinity norm of a transfer matrix and related problems, Mathematics of Control, Signals, and Systems 2(3) (1989) 207-219
    locator: the Hamiltonian test that decides whether the norm is at least gamma
---

The H-infinity norm of a linear system is its largest gain over all frequencies and all input directions: the supremum over $\omega$ of the largest singular value of the frequency response $G(j\omega)$. It is finite for a proper transfer matrix with no poles in the closed right half plane, and its square equals the largest ratio of output energy to input energy, so it is the $L_2$ gain of the system. Because it is an induced norm, it is submultiplicative, and the [small-gain theorem](/small-gain-theorem/) turns it into a robustness test. The [H2 norm](/h2-norm/) averages the gain over frequency; the H-infinity norm takes the worst case.

## Definition

**Notation.** The system is $x' = A x + B u$, $y = C x + D u$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$ and $y \in \mathbb{R}^p$, and $G(s) = C (sI - A)^{-1} B + D$ is its [transfer function](/transfer-function/). $\sigma_{\max}(M)$ is the largest [singular value](/singular-value-decomposition/) of a complex matrix $M$, which is its induced 2-norm (see [matrix norms](/matrix-norms/)).

**The space H-infinity.** $H_\infty$ is the set of $p \times m$ matrix functions $G(s)$ that are analytic in the open right half plane and bounded there. Its norm is

$$\|G\|_\infty = \sup_{\operatorname{Re} s > 0} \sigma_{\max}(G(s)).$$

For a rational $G$ with no poles in the closed right half plane, the maximum modulus principle moves the supremum to the imaginary axis:

$$\|G\|_\infty = \sup_{\omega \in \mathbb{R}} \sigma_{\max}(G(j\omega)).$$

$RH_\infty$ is the set of real rational members. A real rational $G$ is in $RH_\infty$ if and only if it is proper and has all its poles in the open left half plane. For a state-space model, $A$ [Hurwitz](/hurwitz-matrix/) is enough, and $D$ may be nonzero. Uncontrollable or unobservable modes do not change $G$ or its norm.

**The L2 gain.** For $G \in RH_\infty$, zero initial state, and every input $u$ of finite energy $\|u\|_{L_2}^2 = \int_0^\infty |u(t)|^2 dt$,

$$\|y\|_{L_2} \le \|G\|_\infty \|u\|_{L_2},$$

and no smaller constant works:

$$\|G\|_\infty = \sup_{u \in L_2,\ u \ne 0} \frac{\|y\|_{L_2}}{\|u\|_{L_2}}.$$

Proof of the bound: by Parseval, $\|y\|_{L_2}^2 = \frac{1}{2\pi} \int |G(j\omega) \hat u(j\omega)|^2 d\omega \le \|G\|_\infty^2 \frac{1}{2\pi} \int |\hat u(j\omega)|^2 d\omega = \|G\|_\infty^2 \|u\|_{L_2}^2$. Proof that the bound is tight: take $\omega_0$ where $\sigma_{\max}(G(j\omega_0))$ is near the supremum and $v$ its top right singular vector, and let $u$ be a long, slowly windowed sinusoid of frequency $\omega_0$ in the direction $v$. Its spectrum is concentrated near $\pm\omega_0$, so the ratio approaches $\sigma_{\max}(G(j\omega_0))$. The supremum need not be reached, for example when the peak is at $\omega = \infty$.

**Properties.**

- It is a norm, and it is submultiplicative: $\|G H\|_\infty \le \|G\|_\infty \|H\|_\infty$, because it is an induced norm.
- It is at least $\sigma_{\max}(D)$, the limit at $\omega \to \infty$, and at least the largest [Hankel singular value](/hankel-singular-values/) $\sigma_1$. It is at most $\sigma_{\max}(D) + 2(\sigma_1 + \dots + \sigma_n)$, from the [balanced truncation error bound](/balanced-truncation-error-bound/).
- For $\gamma > \sigma_{\max}(D)$ and $A$ Hurwitz, $\|G\|_\infty \ge \gamma$ if and only if a Hamiltonian matrix built from $(A, B, C, D, \gamma)$ has an eigenvalue on the imaginary axis. This is the basis of [H-infinity norm computation](/h-infinity-norm-computation/).
- $\|G\|_\infty < \gamma$ holds if and only if a linear matrix inequality in a symmetric matrix $P > 0$ is feasible, by the [bounded real lemma](/bounded-real-lemma/).
- In the [small-gain theorem](/small-gain-theorem/), a feedback loop of $M \in RH_\infty$ and $\Delta \in RH_\infty$ is internally stable in the sense of finite $L_2$ gain if $\|M\|_\infty \|\Delta\|_\infty < 1$. This is how [model uncertainty](/model-uncertainty/) bounded in the H-infinity norm enters robust control.

**The L-infinity norm.** For a rational $G$ with no poles on the imaginary axis, $\|G\|_{L_\infty} = \sup_\omega \sigma_{\max}(G(j\omega))$ is finite even when $G$ has poles in the right half plane. It is then not the $L_2$ gain of a causal system, and it is not called the H-infinity norm.

**Discrete time.** For $G(z) = C (zI - A)^{-1} B + D$ with $A$ Schur, $\|G\|_\infty = \sup_{\theta \in [-\pi, \pi]} \sigma_{\max}(G(e^{j\theta}))$, the $\ell_2$ gain of the system.

## Examples and non-examples

- **First order, the check value.** $G(s) = 1/(s + 1)$: $|G(j\omega)| = 1/\sqrt{1 + \omega^2}$, largest at $\omega = 0$, so $\|G\|_\infty = 1$. The H2 norm is $1/\sqrt 2$.
- **Lightly damped mode, the check value.** $G(s) = 1/(s^2 + 0.2 s + 1)$, with $\zeta = 0.1$ and $\omega_n = 1$. Here $|G(j\omega)|^2 = 1/((1 - \omega^2)^2 + 0.04\,\omega^2)$. The denominator is smallest at $\omega^2 = 1 - 2\zeta^2 = 0.98$, so the peak is at $\omega = 0.98995$ rad/s and $\|G\|_\infty = 1/(2\zeta\sqrt{1 - \zeta^2}) = 5.02519$. The H2 norm is only $\sqrt{2.5} = 1.58114$, because the peak is narrow.
- **Peak at zero frequency.** $G(s) = (s + 2)/(s + 1)$: $|G(j\omega)|^2 = (4 + \omega^2)/(1 + \omega^2)$ falls from 4 to 1, so $\|G\|_\infty = 2$ at $\omega = 0$. The H2 norm is infinite, because $D = 1$.
- **Peak not reached.** $G(s) = (s + 1)/(s + 2)$: $|G(j\omega)|$ rises from $0.5$ toward 1 and never reaches it. $\|G\|_\infty = \sigma_{\max}(D) = 1$, a supremum and not a maximum.
- **All-pass.** $G(s) = (s - 1)/(s + 1)$: $|G(j\omega)| = 1$ for every $\omega$, so $\|G\|_\infty = 1$, and every input of finite energy keeps its energy.
- **Several inputs and outputs.** $G(s) = \frac{1}{s + 1} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$. The largest singular value of the constant matrix is the golden ratio $(1 + \sqrt 5)/2 = 1.61803$, so $\|G\|_\infty = 1.61803$ at $\omega = 0$. The largest H-infinity norm of a single entry is 1. The norm of a transfer matrix is not the largest norm of its entries.
- **Non-example: a pole on the axis.** $G(s) = 1/s$: $|G(j\omega)| = 1/|\omega|$ is unbounded near $\omega = 0$, so $G \notin H_\infty$. A constant input gives an output that grows like $t$.
- **Non-example: an unstable pole.** $G(s) = 1/(s - 1)$: $\sup_\omega |G(j\omega)| = 1$, so $\|G\|_{L_\infty} = 1$, but $G$ is not bounded in the right half plane (it has a pole at $s = 1$), so $G \notin H_\infty$. The causal system has infinite $L_2$ gain.
- **Non-example: improper.** $G(s) = s$, a pure differentiator: $|G(j\omega)| = |\omega|$ is unbounded, so the norm is infinite.

## Related definitions

- [H2 norm](/h2-norm/): the root of the integral of the squared Frobenius norm over frequency. It needs $D = 0$, it is not an induced norm, and it can be larger or smaller than the H-infinity norm.
- [H-infinity norm computation](/h-infinity-norm-computation/): the bisection and level set algorithms that compute this norm to a set accuracy.
- [Bounded real lemma](/bounded-real-lemma/): the LMI and Riccati tests for $\|G\|_\infty < \gamma$.
- [Small-gain theorem](/small-gain-theorem/) and [model uncertainty](/model-uncertainty/): the use of the norm to bound the effect of unknown dynamics.
- [Structured singular value](/structured-singular-value/): the refinement of the norm test for uncertainty with a block structure.
- [H-infinity control problem](/h-infinity-control-problem/): the design of a controller that makes the H-infinity norm of a closed-loop transfer matrix less than $\gamma$.
- [Frequency response](/frequency-response/): $G(j\omega)$, whose largest singular value the norm bounds.

## References
