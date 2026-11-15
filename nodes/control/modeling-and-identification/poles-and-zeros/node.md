---
tag: T5CT23
kind: definition
slug: poles-and-zeros
name: Poles and zeros
aliases:
- pole-zero map
- poles and zeros of a transfer function
area: control/modeling-and-identification
level: intro
summary: The roots of the denominator and the numerator of a rational transfer function in lowest terms. Poles set the modes of the response; zeros are the exponents an input can have and give no output.
prereqs: [laplace-transform]
see_also: [transmission-zero, minimum-phase, bibo-stability, second-order-system, root-locus, partial-fraction-decomposition, zero-dynamics, hurwitz-matrix]
sources:
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 3.1.8, Poles and Zeros; Section 3.3, Effect of Pole Locations; Section 3.5, Effects of Zeros and Additional Poles
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Sections 4.4 (Poles), 4.5 (Zeros), 4.6 (Some important remarks on poles and zeros) and 4.7 (Internal stability of feedback systems)
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 3, Linear Dynamical Systems (hidden modes and pole-zero cancellation, and Section 3.11, Multivariable System Poles and Zeros)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 9, Transfer Functions (poles and zeros, and pole-zero cancellations)
---

The poles of a rational [transfer function](/transfer-function/) $G(s) = N(s)/D(s)$ in lowest terms are the roots of the denominator $D$, and its zeros are the roots of the numerator $N$. Each pole $p$ is a mode of the system: it puts a term $e^{pt}$ (times a power of $t$ if the pole is repeated) into the impulse response, so the poles decide [BIBO stability](/bibo-stability/) and the speed and damping of the response. Each zero $z$ is an exponent that the system blocks: the input $e^{zt}$, started from the right initial state, gives the output zero. A plot of the poles (as crosses) and the zeros (as circles) in the complex plane is the pole-zero map.

## Definition

**Notation.** $G(s) = N(s)/D(s)$, where $N$ and $D$ are polynomials with real coefficients, written highest power first, $D \ne 0$, and $N$ and $D$ have no common root. Such a fraction is in *lowest terms*. If a model gives $N$ and $D$ with a common root, cancel it first; the [polynomial gcd](/polynomial-gcd/) finds it in exact arithmetic.

**Definition.** A complex number $p$ is a *pole* of $G$ of order $k$ if $p$ is a root of $D$ of multiplicity $k$. A complex number $z$ is a *zero* of $G$ of order $k$ if $z$ is a root of $N$ of multiplicity $k$. Then

$$G(s) = K\, \frac{(s - z_1)(s - z_2) \cdots (s - z_q)}{(s - p_1)(s - p_2) \cdots (s - p_n)},$$

with $K \ne 0$ real, $q = \deg N$ and $n = \deg D$. Because the coefficients are real, complex poles and zeros come in conjugate pairs. If the relative degree $r = n - q$ is positive, $G(s) \to 0$ as $s \to \infty$, and one says that $G$ has $r$ zeros at infinity.

**Poles as modes.** If $G$ is strictly proper, a [partial fraction decomposition](/partial-fraction-decomposition/) gives the impulse response

$$g(t) = \sum_{\text{poles } p} \sum_{j=0}^{k_p - 1} c_{p,j}\, t^j e^{p t}, \qquad t > 0,$$

where $k_p$ is the order of $p$, and the coefficient $c_{p, k_p - 1}$ of the highest power is not zero. So $g$ decays exactly when every pole has a negative real part, and a proper $G$ is BIBO stable exactly when all its poles are in the open left half plane. A pole $p = -\sigma \pm i\omega_d$ gives a term $e^{-\sigma t}\cos(\omega_d t + \phi)$: $\sigma$ sets the decay rate in 1/s and $\omega_d$ the frequency of the oscillation in rad/s.

**Zeros as blocked exponents.** Let $x' = A x + B u$, $y = C x + D u$ be a realization of $G$ with a single input and output, and let $z$ be a zero of $G$ that is not an eigenvalue of $A$. Take $x(0) = (zI - A)^{-1} B$ and $u(t) = e^{zt}$. Then $x(t) = x(0) e^{zt}$ solves the state equation, because $z\, x(0) = A x(0) + B$, and

$$y(t) = \bigl(C (zI - A)^{-1} B + D\bigr)\, e^{zt} = G(z)\, e^{zt} = 0.$$

The input $e^{zt}$ enters the system and leaves no trace at the output. For a zero on the imaginary axis, $z = i\omega_0$, the sinusoid of frequency $\omega_0$ is blocked in steady state.

**State-space view.** For a realization $(A, B, C, D)$, $G(s) = C(sI - A)^{-1}B + D$, and every pole of $G$ is an eigenvalue of $A$. If the realization is [minimal](/minimal-realization/) (controllable and observable), the poles of $G$ are exactly the eigenvalues of $A$, with the same multiplicities in the characteristic polynomial. An eigenvalue of a non-minimal $A$ can be missing from $G$: it is an uncontrollable or an unobservable mode.

## Examples and non-examples

- **Two real poles and a zero.** $G(s) = (s + 3)/(s^2 + 3s + 2) = (s + 3)/((s + 1)(s + 2))$ has the poles $-1$ and $-2$, the zero $-3$ and relative degree 1. Partial fractions give $G = 2/(s + 1) - 1/(s + 2)$, so $g(t) = 2e^{-t} - e^{-2t}$. The input $e^{-3t}$ with the right initial state gives $y \equiv 0$.
- **Complex poles.** $G(s) = 1/(s^2 + 0.2s + 1)$ has the poles $-0.1 \pm 0.99499\, i$: the damping ratio is $\zeta = 0.1$ and the natural frequency is $\omega_n = 1$ rad/s. The impulse response oscillates at $0.99499$ rad/s and decays like $e^{-0.1t}$. See [second-order system](/second-order-system/).
- **A zero in the right half plane.** $G(s) = (1 - s)/(s + 1)^2$ has the zero $+1$. Its unit step response is $y(t) = 1 - e^{-t} - 2t\, e^{-t}$. It starts with the slope $y'(0^+) = -1$, reaches its minimum $-0.21306$ at $t = 0.5$ s, and then rises to 1. This initial undershoot is typical of a real zero in the right half plane, and such a $G$ is not [minimum phase](/minimum-phase/).
- **A hidden unstable mode.** Let the plant be $P(s) = 1/(s - 1)$ and the controller $C(s) = (s - 1)/(s + 1)$. The loop gain is $L = PC = 1/(s + 1)$, and the closed loop from the reference to the output is $T = L/(1 + L) = 1/(s + 2)$, which looks fine. But the transfer function from a disturbance $d$ at the plant input to the output is
$$\frac{P}{1 + PC} = \frac{s + 1}{(s - 1)(s + 2)},$$
with the pole $+1$. A unit step in $d$ gives $y(t) = \tfrac23 e^{t} - \tfrac16 e^{-2t} - \tfrac12$, which grows without bound. The cancellation of the pole $+1$ by the zero of $C$ hides an unstable mode: the system is not internally stable, although one transfer function is stable. So check every transfer function of a loop, not one of them. A cancellation in the open left half plane is safe in this sense; one in the closed right half plane is not.
- **Non-example: common factor not cancelled.** $(s - 1)/((s - 1)(s + 2))$ is not in lowest terms. Its transfer function is $1/(s + 2)$, with no pole at $+1$ and no zero at $+1$. A realization of the unreduced fraction of order 2 has the eigenvalue $+1$ as a hidden mode, as in the example above.
- **Non-example: a delay.** $e^{-s\tau}$ is not rational. It has no finite poles or zeros, and it is not a ratio of polynomials. See [time-delay system](/time-delay-system/).

## Related definitions

- [Laplace transform](/laplace-transform/): the transform that turns a pole $p$ of order $k$ into the terms $t^j e^{pt}$, $j < k$.
- [Transmission zero](/transmission-zero/): the zeros of a transfer matrix with several inputs and outputs, which need not be zeros of any entry.
- [Smith-McMillan form](/smith-mcmillan-form/): the form that defines the poles and zeros of a transfer matrix, with multiplicities.
- [Minimum phase](/minimum-phase/): a stable system with no zeros in the right half plane.
- [BIBO stability](/bibo-stability/): for a proper rational $G$ in lowest terms, all poles in the open left half plane.
- [Hurwitz matrix](/hurwitz-matrix/): a matrix whose eigenvalues all have negative real parts; for a minimal realization, the poles are those eigenvalues.
- [Zero dynamics](/zero-dynamics/): the nonlinear analogue of the zeros, the dynamics left when the output is held at zero.
- [Root locus](/root-locus/): the paths of the closed-loop poles as a gain varies; they start at the open-loop poles and end at the open-loop zeros.

## References
