---
tag: 8K2YAC
kind: definition
slug: gaussian-q-function
name: Gaussian Q-function
aliases:
- Gaussian tail function
area: communications/modulation-and-detection
level: intro
summary: The probability that a standard normal variable exceeds x, the function in which error rates in Gaussian noise are written.
model: floating-point-model
see_also: [symbol-error-rate, bit-error-rate, chernoff-bound, union-bound, additive-white-gaussian-noise-channel, floating-point-model, importance-sampling, central-limit-theorem]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 2.3, Some Useful Random Variables (the Gaussian random variable and the Q-function), and Section 2.4, Bounds on Tail Probabilities
  - paper: doi:10.1109/MILCOM.1991.258319
    title: John W. Craig, A new, simple and exact result for calculating the probability of error for two-dimensional signal constellations, MILCOM 91 Conference Record, 1991
    locator: pp. 571-575 (the integral of Q over a finite range of angles)
  - book: isbn:9780471649533
    title: Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, second edition, Wiley, 2005
    locator: Chapter 4, Alternative Representations of Classical Functions, Section 4.1, Gaussian Q-Function
---

The Gaussian Q-function gives the probability that a standard normal random variable is larger than $x$. In additive Gaussian noise, the probability that the noise pushes a received sample past a decision boundary is a value of $Q$, so the error rates of almost all modulation schemes are written with it. This page defines $Q$, gives its standard forms and bounds, and shows how to compute it without loss of accuracy in floating point.

## Definition

Let $Z \sim \mathcal{N}(0, 1)$. The **Q-function** is

$$Q(x) = \Pr[Z > x] = \frac{1}{\sqrt{2\pi}} \int_x^\infty e^{-t^2/2}\, dt.$$

It is $1 - \Phi(x)$, where $\Phi$ is the standard normal distribution function. It is strictly decreasing, $Q(0) = 1/2$, and $Q(-x) = 1 - Q(x)$. In terms of the complementary error function,

$$Q(x) = \tfrac{1}{2} \operatorname{erfc}\!\big(x/\sqrt{2}\big), \qquad \operatorname{erfc}(u) = 2\,Q\big(\sqrt{2}\,u\big).$$

Some textbooks, Haykin's among them, write error rates with erfc. The two forms are the same function: for example $\tfrac{1}{2}\operatorname{erfc}(\sqrt{E_b/N_0}) = Q(\sqrt{2E_b/N_0})$.

**The tail of a general Gaussian.** If $X \sim \mathcal{N}(\mu, \sigma^2)$, then $\Pr[X > a] = Q((a - \mu)/\sigma)$. In the complex AWGN model with $w \sim \mathcal{CN}(0, N_0)$, the noise along any fixed real direction has the variance $N_0/2$. So the probability that it moves a point past the bisector to a point at the distance $d$ is

$$Q\!\left(\frac{d/2}{\sqrt{N_0/2}}\right) = Q\!\left(\frac{d}{\sqrt{2N_0}}\right).$$

**Craig's form.** *Theorem (Craig 1991).* For $x \ge 0$,

$$Q(x) = \frac{1}{\pi} \int_0^{\pi/2} \exp\!\left(-\frac{x^2}{2\sin^2\theta}\right) d\theta.$$

*Proof.* Let $(X, Y)$ be independent standard normals, so $Q(x) = \Pr[X > x]$. In polar coordinates $X = r\cos\phi$, $Y = r\sin\phi$ with $x \ge 0$, the event is $\phi \in (-\pi/2, \pi/2)$ and $r > x/\cos\phi$. The joint density is $e^{-r^2/2}/(2\pi)$ times $r\,dr\,d\phi$, and $\int_{c}^\infty e^{-r^2/2}\, r\, dr = e^{-c^2/2}$. So $Q(x) = \frac{1}{2\pi}\int_{-\pi/2}^{\pi/2} \exp(-x^2/(2\cos^2\phi))\, d\phi$. The integrand is even in $\phi$; substitute $\theta = \pi/2 - \phi$ on $[0, \pi/2)$. $\square$

The limits of the integral are finite and the argument $x$ is not a limit, which makes the form useful for averaging over fading, where $x$ is random. The same method gives $Q(x)^2 = \frac{1}{\pi}\int_0^{\pi/4} \exp(-x^2/(2\sin^2\theta))\, d\theta$ for $x \ge 0$, and the exact symbol error rate of $M$-PSK (see [phase-shift keying](/phase-shift-keying/)).

**Bounds.** For $x > 0$:

1. *Chernoff bound:* $Q(x) \le \tfrac{1}{2} e^{-x^2/2}$. It follows from Craig's form, since $\sin^2\theta \le 1$ makes each value of the integrand at most $e^{-x^2/2}$. The general [Chernoff bound](/chernoff-bound/) gives $e^{-x^2/2}$ without the factor $1/2$.
2. *Upper bound:* $Q(x) < \varphi(x)/x$, where $\varphi(x) = e^{-x^2/2}/\sqrt{2\pi}$. *Proof:* on $t > x$, $1 < t/x$, so $Q(x) < \int_x^\infty (t/x)\varphi(t)\, dt = \varphi(x)/x$. $\square$
3. *Lower bound:* $Q(x) > \frac{x}{1 + x^2}\varphi(x)$.

The bounds 2 and 3 have the ratio $1 + 1/x^2$, so both are close for large $x$, and $Q(x) \sim \varphi(x)/x$ as $x \to \infty$.

**Inverse.** $Q^{-1}(p)$ is the $x$ with $Q(x) = p$. It gives the SNR that a target error rate needs. Since $Q$ is strictly decreasing and continuous, bisection finds it.

**Floating-point computation.** The values of $Q$ that matter in communications are small: a bit error rate of $10^{-9}$ is $Q(6.0)$. Computing $Q(x)$ as $1 - \Phi(x)$ subtracts two nearly equal numbers. In the [floating-point model](/floating-point-model/) with unit roundoff $u = 2^{-53}$, $\Phi(x)$ is stored with an absolute error of about $u$, so the relative error of the difference is about $u/Q(x)$, which grows without bound as $x$ grows. Computing $\tfrac{1}{2}\operatorname{erfc}(x/\sqrt{2})$ instead keeps a small relative error over the whole range, because the library erfc is computed directly for large arguments. The table is a measurement in IEEE double precision, with $\Phi(x) = \tfrac{1}{2}(1 + \operatorname{erf}(x/\sqrt{2}))$ and Python's `math.erf` and `math.erfc`.

| $x$ | $Q(x)$ by erfc | relative error of $1 - \Phi(x)$ |
|---|---|---|
| 3 | $1.3499 \times 10^{-3}$ | $5.8 \times 10^{-15}$ |
| 5 | $2.8665 \times 10^{-7}$ | $-2.3 \times 10^{-10}$ |
| 6 | $9.8659 \times 10^{-10}$ | $5.6 \times 10^{-8}$ |
| 7 | $1.2798 \times 10^{-12}$ | $4.1 \times 10^{-5}$ |
| 8 | $6.2210 \times 10^{-16}$ | $7.1 \times 10^{-2}$ |
| 9 | $1.1286 \times 10^{-19}$ | the result is 0 |

## Examples and non-examples

**Values.** $Q(1) = 0.158655$, $Q(2) = 0.022750$, $Q(3) = 0.0013499$, $Q(4) = 3.1671 \times 10^{-5}$, $Q(5) = 2.8665 \times 10^{-7}$. For the inverse, $Q^{-1}(10^{-3}) = 3.0902$, $Q^{-1}(10^{-5}) = 4.2649$ and $Q^{-1}(10^{-6}) = 4.7534$.

**The bounds at $x = 3$.** The Chernoff bound gives $0.0055545$, four times too large. The upper bound $\varphi(3)/3$ gives $0.0014773$ and the lower bound $\tfrac{3}{10}\varphi(3)$ gives $0.0013296$; the true value $0.0013499$ lies between them.

**BPSK.** With the points $\pm\sqrt{E_b}$, $d = 2\sqrt{E_b}$, and the bit error rate is $Q(\sqrt{2E_b/N_0})$. At $E_b/N_0 = 0$ dB this is $Q(\sqrt 2) = 0.078650$, at 4 dB it is $0.012501$, and at 8 dB it is $1.9091 \times 10^{-4}$. The bit error rate $10^{-5}$ needs $\sqrt{2E_b/N_0} = Q^{-1}(10^{-5}) = 4.2649$, so $E_b/N_0 = 9.0946$, which is 9.588 dB.

**Craig's integral in practice.** At $x = 3$, the midpoint rule with $N$ equal steps on $[0, \pi/2]$ has a relative error of $-1.1 \times 10^{-3}$ for $N = 4$, $3.1 \times 10^{-6}$ for $N = 8$, $-1.9 \times 10^{-10}$ for $N = 16$, and about $10^{-15}$ for $N = 32$. The integrand is smooth and all its derivatives vanish at $\theta = 0$, so the rule converges very fast.

**Non-example: the tail of a Rayleigh or chi-square variable.** The probability that the envelope of complex Gaussian noise exceeds a threshold is $e^{-r^2/N_0}$, not a value of $Q$. Error rates of noncoherent detectors are written with such exponentials, and error rates on a fading channel are averages of $Q$ over the fading, not values of $Q$.

## Related definitions

- **Normal distribution function.** $\Phi(x) = 1 - Q(x)$, and $Q$ is the upper tail of the standard normal distribution. The [central limit theorem](/central-limit-theorem/) is one reason Gaussian tails appear so often.
- **Error function.** $\operatorname{erf}(u) = 1 - \operatorname{erfc}(u)$ and $\operatorname{erfc}(u) = 2Q(\sqrt{2}u)$.
- **Pairwise error probability.** $Q(d/\sqrt{2N_0})$ for two points at the distance $d$; the [union bound](/union-bound/) adds such terms to bound the [symbol error rate](/symbol-error-rate/).
- **Error rates.** The [symbol error rate](/symbol-error-rate/) and the [bit error rate](/bit-error-rate/) of PAM, PSK and QAM in AWGN are sums and products of values of $Q$.
- **Simulation of small tails.** Plain Monte Carlo needs about $100/Q(x)$ samples to see 100 errors; [importance sampling](/importance-sampling/) estimates small tail probabilities with far fewer samples.

## References
