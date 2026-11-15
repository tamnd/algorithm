---
tag: 2CRD0P
kind: theorem
slug: final-value-theorem
name: Final value theorem
aliases:
- final value theorem of the Laplace transform
area: control/classical-control
level: intro
summary: "If f(t) has a limit, it equals the limit of sF(s) as s goes to 0. For rational F the limit of f exists exactly when all poles of sF(s) are in the open left half plane. Else sF(0) can mislead."
history:
  year: 1826
  people: [Niels Henrik Abel, Alfred Tauber]
  note: The theorem is a Laplace transform form of an Abelian theorem. Abel proved the power series form in 1826, and Tauber gave a first converse for power series in 1897.
prereqs: [laplace-transform, poles-and-zeros]
see_also: [steady-state-error, step-response-specifications, laplace-transform, z-transform, partial-fraction-decomposition, bibo-stability, feedback-control-loop, internal-model-principle]
sources:
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 3, Dynamic Response (the final value theorem and its use on rational transforms)
  - book: "David V. Widder, The Laplace Transform, Princeton University Press, 1941"
    locator: the chapters on Abelian and Tauberian theorems for the Laplace transform
---

The final value theorem gives the limit of a signal $f(t)$ as $t \to \infty$ from its [Laplace transform](/laplace-transform/) $F(s)$, as the limit of $s F(s)$ as $s \to 0$. Control engineers use it to find the steady-state value of a step response and the [steady-state error](/steady-state-error/) of a loop without solving for $f(t)$. The theorem has two parts that are often mixed up. If $f(t)$ has a limit, the formula gives it, for any locally integrable $f$. But $s F(s)$ can have a limit at 0 when $f(t)$ has none. For a rational $F$ there is an exact test: $f(t)$ has a limit if and only if all poles of $s F(s)$ are in the open left half plane. Without this test the formula can give a finite number for $\sin t$ or $e^t$.

## Statement

Let $f : [0, \infty) \to \mathbb{R}$ be locally integrable, with the one-sided Laplace transform $F(s) = \int_0^\infty e^{-s t} f(t)\, dt$.

**Theorem 1 (Abelian part).** If $f(t) \to c$ as $t \to \infty$, with $c$ finite, then $F(s)$ converges for every real $s > 0$, and

$$\lim_{s \to 0^+} s\,F(s) = c.$$

**Theorem 2 (rational case).** Let $F$ be a strictly proper rational function, and let $f$ be its inverse transform, so that $f$ is a finite sum of terms $q(t)\,e^{p t}$ with $p$ a pole of $F$ and $q$ a polynomial. Then $\lim_{t \to \infty} f(t)$ exists and is finite if and only if every pole of $s F(s)$ is in the open left half plane. In that case

$$\lim_{t \to \infty} f(t) = \lim_{s \to 0} s\,F(s).$$

Equivalently: every pole of $F$ is in the open left half plane, except possibly a simple pole at $s = 0$.

**Theorem 3 (discrete time).** Let $x[k]$, $k = 0, 1, 2, \ldots$, have a rational [z-transform](/z-transform/) $X(z) = \sum_{k \ge 0} x[k]\,z^{-k}$. Then $\lim_{k \to \infty} x[k]$ exists and is finite if and only if every pole of $(z - 1) X(z)$ is in the open unit disc $|z| < 1$. In that case

$$\lim_{k \to \infty} x[k] = \lim_{z \to 1} (z - 1)\,X(z).$$

Some texts write $(1 - z^{-1}) X(z)$, which has the same limit at $z = 1$.

## In plain words

If a signal settles to a final value, that value can be read off its transform with a short formula, and you never need to compute the signal itself. The formula always gives a number, and that is the trap. A signal that swings for ever or grows without limit can still give a clean number. So before you trust the number, check that the signal really settles. For the usual signals of linear systems this check is simple. Look at the points where the transform blows up, after the formula has removed the one at the origin. If all of them lie strictly on the stable side, the signal settles and the number is right. If any of them is on the boundary or past it, the number means nothing.

## Proof

**Theorem 1.** Since $f$ is locally integrable and $f(t) \to c$, $f$ is bounded for large $t$, so the integral defining $F(s)$ converges absolutely for every $s > 0$. Because $s \int_0^\infty e^{-s t}\, dt = 1$,

$$s F(s) - c = s \int_0^\infty e^{-s t}\,(f(t) - c)\, dt.$$

Let $\varepsilon > 0$ and take $T$ with $|f(t) - c| < \varepsilon$ for $t > T$. Split the integral at $T$:

$$|s F(s) - c| \le s \int_0^T |f(t) - c|\, dt + s \int_T^\infty e^{-s t}\,\varepsilon\, dt \le s\,M_T + \varepsilon,$$

with $M_T = \int_0^T |f(t) - c|\,dt$ finite. As $s \to 0^+$ the first term goes to 0, so $\limsup_{s \to 0^+} |s F(s) - c| \le \varepsilon$ for every $\varepsilon > 0$. $\square$

**Two lemmas for Theorem 2.**

*Lemma B (trigonometric sums).* Let $h(t) = \sum_{i=1}^r a_i\,e^{j \omega_i t}$ with distinct real $\omega_i$ and complex $a_i$. If $h(t) \to 0$ as $t \to \infty$, then all $a_i = 0$.

*Proof.* Expand $|h|^2 = \sum_{i,l} a_i \bar a_l\, e^{j(\omega_i - \omega_l) t}$. For $i \ne l$, $\frac{1}{T}\int_0^T e^{j(\omega_i - \omega_l)t}\,dt$ has modulus at most $2/(T |\omega_i - \omega_l|)$, which goes to 0. So $\frac{1}{T}\int_0^T |h(t)|^2\,dt \to \sum_i |a_i|^2$. If $h(t) \to 0$, the mean of $|h|^2$ goes to 0 too, so $\sum_i |a_i|^2 = 0$. $\square$

*Lemma A (exponential polynomials).* Let $g(t) = \sum_{p} q_p(t)\,e^{p t}$ be a finite sum over distinct complex $p$ with $\operatorname{Re} p \ge 0$ and polynomials $q_p$. If $g(t) \to 0$, then every $q_p$ is zero.

*Proof.* Suppose not. Among the $p$ with $q_p \ne 0$, let $\sigma$ be the largest real part, and among those with $\operatorname{Re} p = \sigma$ let $d$ be the largest degree of $q_p$. Let $a_p$ be the coefficient of $t^d$ in $q_p$ for the $p$ with $\operatorname{Re} p = \sigma$ (zero when the degree is lower), and write $p = \sigma + j\omega_p$. Then

$$\frac{g(t)}{t^d e^{\sigma t}} = \sum_{\operatorname{Re} p = \sigma} a_p\,e^{j\omega_p t} + o(1),$$

because each other term has a smaller real part of the exponent or a smaller power of $t$. Since $\sigma \ge 0$ and $d \ge 0$, $t^d e^{\sigma t} \ge 1$ for $t \ge 1$, so the left side goes to 0. By Lemma B all $a_p$ are zero, against the choice of $d$. $\square$

**Theorem 2.** By [partial fraction decomposition](/partial-fraction-decomposition/), $f(t) = \sum_p q_p(t)\,e^{p t}$, summed over the poles $p$ of $F$, where $q_p$ is a nonzero polynomial of degree one less than the order of the pole.

*If.* Suppose all poles of $s F(s)$ are in the open left half plane. Then $F$ has no pole with $\operatorname{Re} p \ge 0$ other than a simple pole at 0, with some residue $c$ (possibly $c = 0$). So $f(t) = c + \sum_{\operatorname{Re} p < 0} q_p(t)\,e^{p t}$, and each term of the sum goes to 0, so $f(t) \to c$. Also $s F(s) = c + s\,F_-(s)$ with $F_-$ analytic at 0, so $\lim_{s \to 0} s F(s) = c$.

*Only if.* Suppose $f(t) \to c$. Split $f = f_- + f_+$, where $f_-$ collects the poles with $\operatorname{Re} p < 0$ and $f_+$ the poles with $\operatorname{Re} p \ge 0$. Then $f_-(t) \to 0$, so $g = f_+ - c \to 0$. The function $g$ is an exponential polynomial over exponents with $\operatorname{Re} p \ge 0$, where the constant $-c$ is added to the polynomial of $p = 0$. By Lemma A, all its polynomials are zero: $q_p = 0$ for every pole with $\operatorname{Re} p \ge 0$ and $p \ne 0$, and $q_0 = c$ is a constant. A pole at 0 with a constant $q_0 \ne 0$ is simple, so $F$ has, in the closed right half plane, at most a simple pole at 0, and all poles of $s F(s)$ are in the open left half plane. The value of the limit then follows from the *if* part, or from Theorem 1. $\square$

**Theorem 3.** The proof is the same with sequences. Partial fractions of $X(z)/z$ write $x[k]$, for $k$ large, as a finite sum $\sum_p q_p(k)\,p^k$ over the poles $p \ne 0$ of $X$. Terms with $|p| < 1$ go to 0. For the terms with $|p| \ge 1$, divide by $k^d |p|^k$ and use the discrete form of Lemma B: for distinct angles $\theta_i \in (-\pi, \pi]$, $\frac{1}{K}\sum_{k < K} e^{j(\theta_i - \theta_l)k} \to 0$ for $i \ne l$. So $x[k]$ has a limit if and only if $X$ has, outside the open unit disc, at most a simple pole at $z = 1$. That is the condition that $(z - 1)X(z)$ has all its poles in $|z| < 1$. $\square$

## Consequences

- **Steady-state value of a step response.** If $G$ is rational with all poles in the open left half plane, the unit step response $y$ has $Y(s) = G(s)/s$, so $y(t) \to G(0)$, the static gain. This is the steady-state value in the [step response specifications](/step-response-specifications/).
- **Steady-state error.** For an internally stable loop, $e_\infty = \lim_{s \to 0} s\,S(s)\,R(s)$ whenever $s\,S(s)\,R(s)$ has all poles in the open left half plane. This gives the table of the [steady-state error](/steady-state-error/) page.
- **Internal model principle.** Zero error to a sinusoid of frequency $\omega_0$ needs the poles $\pm j\omega_0$ of the reference transform to be cancelled by zeros of $S$; the theorem with the test explains why an uncancelled pole on the imaginary axis leaves a persistent error; see [internal model principle](/internal-model-principle/).
- **Initial value theorem.** For a strictly proper rational $F$, $f(0^+) = \lim_{s \to \infty} s\,F(s)$, with no condition on the poles. The proof: $s F(s) = \sum_p \sum_i c_{p,i}\, s/(s - p)^i$, and as $s \to \infty$ only the terms with $i = 1$ survive, each giving $c_{p,1}$, whose sum is $f(0^+)$.
- **Non-rational transforms.** Theorem 1 holds for any locally integrable $f$, so it applies to loops with a time delay $e^{-s\tau}$. Only the test of Theorem 2 needs a rational $F$.

## Tightness

Each hypothesis of Theorem 2 is needed, and the converse of Theorem 1 fails without one.

| $F(s)$ | $f(t)$ | $\lim_{s \to 0} s F(s)$ | $\lim_{t \to \infty} f(t)$ | pole of $s F(s)$ that fails |
|---|---|---|---|---|
| $\dfrac{3}{s(s + 2)}$ | $1.5\,(1 - e^{-2t})$ | 1.5 | 1.5 | none, the theorem applies |
| $\dfrac{1}{s^2 + 1}$ | $\sin t$ | 0 | none | $\pm j$ on the imaginary axis |
| $\dfrac{1}{s - 1}$ | $e^{t}$ | 0 | $+\infty$ | $1$ in the right half plane |
| $\dfrac{1}{s^2}$ | $t$ | $\infty$ | $+\infty$ | a pole at 0 |

In the second and third rows the formula returns a finite number for a signal with no finite limit. In the discrete case, $x[k] = (-1)^k$ has $X(z) = z/(z + 1)$ and $(z - 1)X(z) \to 0$ as $z \to 1$, but $x[k]$ has no limit; the pole $z = -1$ is on the unit circle.

**The converse of Theorem 1 needs a Tauberian condition.** The example $\sin t$ shows that $\lim_{s \to 0^+} s F(s) = c$ alone does not imply $f(t) \to c$. Theorems that add a side condition on $f$ (for example, a one-sided bound on its growth) and then conclude $f(t) \to c$ are called Tauberian theorems; Widder (1941) treats them for the Laplace transform. For rational $F$, Theorem 2 is an exact Tauberian test.

## History

The theorem is the Laplace transform form of an Abelian theorem, named after Abel's 1826 theorem on power series: if $\sum a_k$ converges to $c$, then $\sum a_k x^k \to c$ as $x \to 1^-$. Tauber's 1897 theorem was the first partial converse for power series, and later Tauberian theorems of Hardy, Littlewood and Wiener extended this line of work. Engineers came to the theorem through the operational calculus and the Laplace transform methods for circuits and control, where it became the standard tool for steady-state values.

## References
