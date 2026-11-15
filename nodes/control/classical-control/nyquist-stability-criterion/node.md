---
tag: BQ1540
kind: theorem
slug: nyquist-stability-criterion
name: Nyquist stability criterion
aliases:
- Nyquist criterion
area: control/classical-control
level: core
summary: "With P open-loop poles in the right half plane and N clockwise encirclements of -1 by L(s) as s goes clockwise around that half plane, the closed loop has Z = N + P unstable poles."
prereqs: [nyquist-plot, feedback-control-loop]
see_also: [gain-margin, phase-margin, routh-hurwitz-criterion, root-locus, poles-and-zeros, bode-sensitivity-integral, small-gain-theorem, time-delay-system]
sources:
  - paper: doi:10.1002/j.1538-7305.1932.tb02344.x
    title: Harry Nyquist, Regeneration Theory, Bell System Technical Journal 11(1), 1932
    locator: pp. 126 to 147 (the stability rule for a feedback amplifier from the locus of its loop gain)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Section 10.2, The Nyquist Criterion (the statement for loops with unstable poles, conditional stability, and the proof by the argument principle)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.3, The Nyquist Stability Criterion, with Section 6.3.1, The Argument Principle
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Section 7-5, Nyquist Stability Criterion
---

The Nyquist stability criterion says that a negative feedback loop with loop transfer function $L(s)$ has $Z = N + P$ closed-loop poles in the right half plane. Here $P$ is the number of poles of $L$ in the open right half plane, and $N$ is the number of clockwise encirclements of the point $-1$ by $L(s)$ while $s$ goes once clockwise around the Nyquist contour, which encloses the right half plane. So the closed loop is asymptotically stable exactly when the [Nyquist plot](/nyquist-plot/) misses $-1$ and goes around it counterclockwise $P$ times; for a loop with no unstable poles, it must not go around $-1$ at all. Harry Nyquist gave the rule in 1932 for feedback amplifiers, and it is the base of the [gain margin](/gain-margin/), the [phase margin](/phase-margin/) and loop shaping.

## Statement

**Notation.** The loop is the negative feedback loop of the [feedback control loop](/feedback-control-loop/) page: $e = r - y$, plant $P_0(s)$, controller $C(s)$ and loop transfer function $L = P_0 C$. (The plant is written $P_0$ here because $P$ is the pole count.) Write $L = n/d$ with coprime real polynomials $n$ and $d$. A pole or zero is counted with its multiplicity. The open right half plane is $\operatorname{Re} s > 0$.

**Hypotheses.**

1. $L$ is real rational and proper.
2. No unstable cancellation: in the product $P_0 C$, no pole of $P_0$ or $C$ with $\operatorname{Re} s \ge 0$ is cancelled by a zero of the other.
3. The loop is well posed: $1 + L(\infty) \ne 0$.

**The contour and the count.** The Nyquist contour goes up the imaginary axis from $-jR$ to $jR$ and back along the half circle of radius $R$ in the right half plane, which is once clockwise around the half disk. At each pole of $L$ on the imaginary axis it goes around on a small half circle of radius $\varepsilon$ into the right half plane, so these poles are outside the contour. $R$ is large enough and $\varepsilon$ is small enough that the contour encloses all roots of $d$ and of $d + n$ in the open right half plane. Assume that the image of the contour under $L$ does not pass through $-1$. Let $N$ be the number of clockwise turns of this image around $-1$, with counterclockwise turns counted as negative.

**Theorem.** Let $P$ be the number of poles of $L$ in the open right half plane and $Z$ the number of closed-loop poles in the closed right half plane. Then

$$Z = N + P.$$

The closed loop is asymptotically stable (all its poles in the open left half plane) if and only if the Nyquist plot does not pass through $-1$ and $N = -P$.

## In plain words

Draw the curve of the loop gain while the frequency runs over all values, and close it as the Nyquist plot page says. Count how many times this curve winds around the point minus one, clockwise. Add the number of unstable poles that the loop has by itself. The sum is the number of unstable poles of the closed loop. So a loop that is stable by itself is safe exactly when the curve does not go around minus one. A loop that is unstable by itself is safe only when the curve goes around minus one the other way, once for each unstable pole. The test needs only the frequency response of the loop, which you can measure, and not the equations of the closed loop.

## Proof

The proof is the argument principle of Cauchy, here only for rational functions, where it is elementary.

**Step 1. One factor.** Let $D$ be the contour, traced once clockwise, and let $a$ be a point not on $D$. Follow the continuous argument of $s - a$ while $s$ goes once around $D$. If $\varepsilon = 0$, the region inside $D$ is the half disk, which is convex. If $a$ is inside, the vector $s - a$ turns once clockwise, and its argument changes by $-2\pi$. If $a$ is outside, a line separates $a$ from the half disk, so $s - a$ stays in one open half plane, and the change is 0. For $\varepsilon > 0$ and $a$ off the imaginary axis, the change depends continuously on $\varepsilon$ and is a multiple of $2\pi$, so it does not change. For $a = j\omega_0$ a pole that the contour goes around, the argument of $s - a$ is constant on the straight parts of the axis, goes up by $\pi$ on the small half circle, and goes down by $\pi$ along the big arc, so the change is 0: the pole is outside.

**Step 2. The rational function $F = 1 + L$.** $F = (d + n)/d$. A common root of $d + n$ and $d$ would be a root of $n$, so $d + n$ and $d$ are coprime. Since $L$ is proper, $\deg n \le \deg d$, and the leading coefficient of $d + n$ is that of $d$ times $1 + L(\infty)$, which is not 0 by hypothesis 3. So $F = k\prod_i (s - a_i)/\prod_i (s - b_i)$, where the $a_i$ are the roots of $d + n$ and the $b_i$ are the roots of $d$. The argument of a product is the sum of the arguments. By step 1, the argument of $F$ changes by $-2\pi$ for each $a_i$ inside $D$ and by $+2\pi$ for each $b_i$ inside $D$. Inside $D$ there are $P$ roots of $d$. The roots of $d + n$ inside $D$ are those in the open right half plane, and there are none on the imaginary axis: at a pole of $L$ we have $d = 0$ and $n \ne 0$, and elsewhere $L(j\omega) \ne -1$ by assumption. So the total change of $\arg F$ is $-2\pi(Z - P)$, where $Z$ counts the roots of $d + n$ with $\operatorname{Re} s \ge 0$.

**Step 3. From $F$ around 0 to $L$ around $-1$.** $F(s) - 0 = L(s) - (-1)$, so the turning of $F$ around 0 is the turning of $L$ around $-1$. A change of $-2\pi$ in the argument is one clockwise turn. Hence $N = Z - P$. On the big arc, $F(s) \to 1 + L(\infty) \ne 0$, so for a large $R$ this arc maps into a small disk around one point that does not contain 0, and it adds nothing to the count. So $N$ may be counted on the limit curve.

**Step 4. The roots of $d + n$ are the closed-loop poles.** Write $P_0 = n_P/d_P$ and $C = n_C/d_C$ in coprime form. Each closed-loop transfer function from an input to a signal of the loop, such as $S = 1/(1 + L)$, $P_0 S$, $C S$ and $T = L/(1 + L)$, has a denominator that divides $d_P d_C + n_P n_C$, and the closed-loop poles are the roots of this polynomial. If $P_0 C$ has a common factor $c$, then $d_P d_C + n_P n_C = c\,(d + n)$, and the roots of $c$ are the cancelled modes. By hypothesis 2 they are in the open left half plane. So the closed-loop poles in the closed right half plane are exactly the roots of $d + n$ there, and their number is $Z = N + P$. The loop is asymptotically stable if and only if $Z = 0$, that is, $N = -P$. $\square$

**A check by hand.** Take $L = 4/((s - 1)(s + 2))$, so $P = 1$. On the axis, $(j\omega - 1)(j\omega + 2) = -(\omega^2 + 2) + j\omega$, so $L(j0) = -2$ and $\operatorname{Im} L(j\omega) < 0$ for $\omega > 0$. As $\omega$ goes from $-\infty$ to 0 the curve runs from 0 through the upper half plane to $-2$, and as $\omega$ goes from 0 to $\infty$ it comes back through the lower half plane to 0. That is one counterclockwise turn around $-1$: $N = -1$ and $Z = N + P = 0$. Indeed the closed-loop polynomial $(s - 1)(s + 2) + 4 = s^2 + s + 2$ has the roots $(-1 \pm j\sqrt 7)/2$. With the gain 1 in place of 4, the curve crosses the real axis at $-1/2$, $N = 0$ and $Z = 1$: the polynomial $s^2 + s - 1$ has the root $(\sqrt 5 - 1)/2 = 0.618$.

## Consequences

- **Loops that are stable by themselves.** If $P = 0$, the closed loop is asymptotically stable if and only if the Nyquist plot does not go around $-1$. The [gain margin](/gain-margin/), the [phase margin](/phase-margin/) and the peak sensitivity $M_s$ say how far the curve stays from $-1$.
- **Unstable loops need gain.** For $L = K/((s - 1)(s + 2))$ the curve starts at $-K/2$ and must go around $-1$ once counterclockwise, so the loop is asymptotically stable only for $K > 2$. A gain margin then has a lower limit: here the gain can drop by a factor of 2 for $K = 4$.
- **Conditional stability.** For $L = 3k(s + 6)^2/(s(s + 1)^2)$ the polar plot crosses the negative real axis at $-12k$ (at $\omega = 2$) and at $-4.5k$ (at $\omega = 3$); you can check both values by hand. The closed loop $s^3 + (2 + 3k)s^2 + (1 + 36k)s + 108k$ is asymptotically stable for $k < 1/12$ and for $k > 2/9$, and unstable between. For $k = 1$, a drop of the gain by a factor of 4.5 makes the loop unstable. A single number such as "the gain margin" does not describe this loop.
- **Gain variation.** The closed loop of $kL$ has $Z = N_k + P$, where $N_k$ counts encirclements of $-1/k$ by the plot of $L$. So one plot gives the stability for all gains, as a [root locus](/root-locus/) does in the $s$ plane.
- **Delays and measured data.** The count uses only $L(j\omega)$, so it works with a measured frequency response. It extends to a loop with a [time delay](/time-delay-system/) $e^{-s\tau}$ by the general argument principle for meromorphic functions, which this page does not prove.
- **Other theorems.** The [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) gives the same answer from the coefficients of $d + n$. The [small-gain theorem](/small-gain-theorem/) is the case where $|L(j\omega)| < 1$ at all frequencies, so the curve cannot reach $-1$. The [Bode sensitivity integral](/bode-sensitivity-integral/) assumes the closed loop is asymptotically stable, which this criterion checks.

## Tightness

- **Unstable cancellation.** Take $P_0 = 1/(s - 1)$ and $C = (s - 1)/(s + 1)$. Then $L = 1/(s + 1)$, $P = 0$, $N = 0$ and the criterion gives $Z = 0$. But $P_0 S = (s + 1)/((s - 1)(s + 2))$ has a pole at 1: the cancelled mode is unstable, and hypothesis 2 fails.
- **The curve through $-1$.** For $L = 6/(s(s + 1)(s + 2))$, $L(j\sqrt 2) = -1$, and $N$ is not defined. The closed-loop polynomial $s^3 + 3s^2 + 2s + 6 = (s + 3)(s^2 + 2)$ has the poles $\pm j\sqrt 2$ on the axis: the loop is neither asymptotically stable nor unstable with a pole in the open right half plane.
- **Direction.** If the contour is traced counterclockwise, or if counterclockwise turns are counted as positive, the formula changes sign: $-N = Z - P$. Each textbook fixes one convention; this page uses clockwise for both. If the detours around imaginary-axis poles go to the left, those poles count in $P$, and the closing arcs change in the same way, so $Z = N + P$ still holds with the new $N$ and $P$.
- **Well posedness.** If $L(\infty) = -1$, then $1 + L$ is strictly proper, $d + n$ loses degree, and the closed loop is not proper. Step 2 fails.

## History

Harold Black invented the negative feedback amplifier in 1927 at Bell Telephone Laboratories, and some of these amplifiers oscillated for reasons that the designers could not predict. Harry Nyquist, also at Bell Laboratories, solved the problem in "Regeneration Theory" (1932): he plotted the loop gain in the complex plane for all frequencies and gave the rule that decides stability from the position of the critical point relative to the curve. His paper treated loops without unstable poles of their own. The form $Z = N + P$ for loops with open-loop poles in the right half plane, with the proof by the argument principle, is the form that the textbooks give today. Hendrik Bode then turned the rule into the design margins of his 1945 book.

## References
