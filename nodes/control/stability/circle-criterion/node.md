---
tag: 8N8WP5
kind: theorem
slug: circle-criterion
name: Circle criterion
aliases:
- circle stability criterion
area: control/stability
level: advanced
summary: A Lur'e system is absolutely stable for a sector if the Nyquist plot of its linear part avoids a disk set by the sector bounds.
prereqs: [lure-problem, kalman-yakubovich-popov-lemma, nyquist-stability-criterion]
see_also: [popov-criterion, lure-problem, small-gain-theorem, passivity-theorem, kalman-yakubovich-popov-lemma, nyquist-plot, describing-function, linear-matrix-inequality]
sources:
  - paper: doi:10.1002/j.1538-7305.1964.tb04100.x
    title: Irwin W. Sandberg, A frequency-domain condition for the stability of feedback systems containing a single time-varying nonlinear element, Bell System Technical Journal 43(4), 1601-1608, 1964
    locator: a frequency condition for a loop with one time-varying sector nonlinearity, by a functional analysis argument
  - paper: doi:10.1109/TCT.1964.1082320
    title: K. S. Narendra and R. M. Goldwyn, A geometrical criterion for the stability of certain nonlinear nonautonomous systems, IEEE Transactions on Circuit Theory 11(3), 406-408, 1964
    locator: the disk condition on the Nyquist plot, proved with a quadratic Lyapunov function
  - paper: doi:10.1109/TAC.1966.1098356
    title: "George Zames, On the input-output stability of time-varying nonlinear feedback systems, Part II: Conditions involving circles in the frequency plane and sector nonlinearities, IEEE Transactions on Automatic Control 11(3), 465-476, 1966"
    locator: the circle condition for sector nonlinearities in the input-output setting
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 7.1 (absolute stability and the circle criterion, with the three cases of the sector and the disk D(k1, k2))
---

The circle criterion is a test for the [Lur'e problem](/lure-problem/): a linear system in negative feedback with a nonlinearity that is known only through a sector $[k_1, k_2]$. It draws a disk on the real axis between the points $-1/k_1$ and $-1/k_2$, and asks that the [Nyquist plot](/nyquist-plot/) of the linear part avoids the disk and goes around it the right number of times. Then the loop is globally exponentially stable for every nonlinearity in the sector, also a time-varying one. When the sector shrinks to one gain $k$, the disk shrinks to the critical point $-1/k$ and the test becomes the [Nyquist stability criterion](/nyquist-stability-criterion/). The proof is a quadratic Lyapunov function from the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/), so the test is also a [linear matrix inequality](/linear-matrix-inequality/). Sandberg, Narendra and Goldwyn, and Zames found it in 1964 to 1966.

## Statement

**Setting.** $\dot x = Ax + Bu$, $y = Cx$, $u = -\psi(t, y)$, with scalar $u$ and $y$. The realization $(A, B, C)$ is minimal, and $G(s) = C(sI - A)^{-1}B$. The nonlinearity $\psi$ is piecewise continuous in $t$, locally Lipschitz in $y$, and in the sector $[k_1, k_2]$ with $k_1 < k_2$:

$$k_1 y^2 \ \le\ y\, \psi(t, y) \ \le\ k_2 y^2 \qquad \text{for all } t \ge 0 \text{ and all } y.$$

The nonlinearity can depend on time. For $k_1 \ne 0$, let $D(k_1, k_2)$ be the closed disk in the complex plane whose diameter is the segment from $-1/k_1$ to $-1/k_2$. Let $p$ be the number of eigenvalues of $A$ in the open right half plane.

**Theorem (circle criterion).** The origin is globally exponentially stable, with constants that do not depend on $\psi$, for every $\psi$ in the sector $[k_1, k_2]$, if one of these conditions holds:
1. $0 < k_1 < k_2$, the Nyquist plot of $G(j\omega)$ does not meet $D(k_1, k_2)$, and it goes around the disk $p$ times counterclockwise. If $G$ has poles on the imaginary axis, the Nyquist path goes around them on small half circles in the right half plane.
2. $0 = k_1 < k_2$, $A$ is [Hurwitz](/hurwitz-matrix/), and $\operatorname{Re} G(j\omega) > -1/k_2$ for all $\omega \in \mathbb{R}$.
3. $k_1 < 0 < k_2$, $A$ is Hurwitz, and $G(j\omega)$ lies in the interior of $D(k_1, k_2)$ for all $\omega \in \mathbb{R}$.

For $k_1 < k_2 \le 0$, apply the theorem to $-G$ and the sector $[-k_2, -k_1]$. Each condition is the same as this one: $A - k_1 BC$ is Hurwitz and

$$Z(s) = \frac{1 + k_2 G(s)}{1 + k_1 G(s)}$$

is strictly positive real.

## In plain words

A linear system is in a loop with a device whose gain is unknown and can change with time, but always stays between a lower and an upper value. For one known gain, the classic test looks at the frequency response curve of the linear system and asks how it goes around one critical point. When the gain is only known to lie in a range, the critical point grows into a disk, and each end of the range sets one end of the disk. If the curve stays clear of the whole disk and goes around it the right number of times, the loop settles to rest from every start, for every device in the range. The test is easy to draw, and a computer can check it as a small matrix problem.

## Proof

**Step 1, loop transformation.** Let $k = k_2 - k_1$ and $\psi_T(t, y) = \psi(t, y) - k_1 y$. Then $\psi_T$ is in the sector $[0, k]$, and the loop is

$$\dot x = A_T x - B \psi_T(t, y), \qquad A_T = A - k_1 BC, \qquad y = Cx,$$

with the transfer function $G_T = G/(1 + k_1 G)$. Output feedback keeps $(A_T, B)$ controllable and $(A_T, C)$ observable. Also $1 + k G_T = (1 + k_2 G)/(1 + k_1 G) = Z$.

**Step 2, the sector $[0, k]$.** Suppose $A_T$ is Hurwitz and $Z(s) = 1 + kC(sI - A_T)^{-1}B$ is strictly positive real. The realization $(A_T, B, kC, 1)$ is minimal, so the strict form of the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) (Khalil 2002, Section 6.3) gives $P = P^T > 0$, a matrix $L$, a column $W$ and $\varepsilon > 0$ with

$$P A_T + A_T^T P = -L^T L - \varepsilon P, \qquad P B = k C^T - L^T W, \qquad W^T W = 2.$$

Take $V(x) = x^T P x$ and write $\psi$ for $\psi_T(t, y)$. Since $B^T P x = k y - W^T L x$,

$$\dot V = x^T (P A_T + A_T^T P) x - 2\psi B^T P x = -\varepsilon V - |Lx|^2 - 2k y \psi + 2\psi W^T L x.$$

The sector $[0, k]$ gives $\psi(\psi - k y) \le 0$, so $-2ky\psi \le -2\psi^2 = -\psi^2 W^T W$. Then

$$\dot V \ \le\ -\varepsilon V - |Lx|^2 + 2\psi W^T L x - \psi^2 W^T W = -\varepsilon V - |Lx - W\psi|^2 \ \le\ -\varepsilon V.$$

So $V(x(t)) \le e^{-\varepsilon t} V(x(0))$ and $|x(t)| \le \sqrt{\lambda_{\max}(P)/\lambda_{\min}(P)}\, e^{-\varepsilon t/2} |x(0)|$. The constants depend on $P$ and $\varepsilon$ only, not on $\psi$.

**Step 3, the frequency conditions.** $Z(\infty) = 1 > 0$, and the poles of $Z$ are eigenvalues of $A_T$. So $Z$ is strictly positive real if $A_T$ is Hurwitz and $\operatorname{Re} Z(j\omega) > 0$ for all $\omega$. It remains to show that each of the three conditions gives these two facts.

*Case 2.* Here $k_1 = 0$, so $A_T = A$ and $Z = 1 + k_2 G$. The condition $\operatorname{Re} Z(j\omega) > 0$ is $\operatorname{Re} G(j\omega) > -1/k_2$.

*Cases 1 and 3.* With $a = -1/k_1$ and $b = -1/k_2$,

$$Z = \frac{k_2}{k_1} \cdot \frac{G - b}{G - a}.$$

The argument of $(w - b)/(w - a)$ is the angle at the point $w$ between the directions to $b$ and to $a$. By Thales' theorem, this angle is less than $90$ degrees exactly when $w$ is outside the closed disk with diameter $[a, b]$, equal to $90$ degrees on the circle, and more than $90$ degrees inside. So $\operatorname{Re}[(w - b)/(w - a)] > 0$ outside the closed disk and $< 0$ in its interior. In case 1, $k_2/k_1 > 0$, and the plot outside $D(k_1, k_2)$ gives $\operatorname{Re} Z(j\omega) > 0$. In case 3, $k_2/k_1 < 0$, and the plot in the interior of the disk gives $\operatorname{Re} Z(j\omega) > 0$.

For $A_T$: the matrix $A - k_1 BC$ is the closed loop matrix for the constant gain $k_1$. By the Nyquist criterion, it is Hurwitz exactly when the plot of $G$ goes around $-1/k_1$ $p$ times counterclockwise. In case 1, the plot does not meet the disk, so it goes around every point of the disk the same number of times, and in particular around $-1/k_1$, which is on the disk. In case 3, $p = 0$, and the plot lies in the open disk, while $-1/k_1$ is on the boundary circle; a closed curve in a convex set does not go around a point outside the set, so the count is $0 = p$. Steps 1 and 2 finish the proof.

## Consequences

**Nyquist criterion as a limit.** As $k_1$ and $k_2$ tend to one gain $k > 0$, the disk shrinks to the point $-1/k$, and case 1 becomes the Nyquist criterion for the gain $k$. Rule of thumb: the circle criterion is the Nyquist criterion with the critical point blown up to a disk, whose size measures how little is known about the gain.

**Small gain as a special case.** For the sector $[-c, c]$, the disk $D(-c, c)$ has center $0$ and radius $1/c$, and case 3 is $|G(j\omega)| < 1/c$ for all $\omega$, that is, $\|G\|_\infty < 1/c$. This is the [small-gain theorem](/small-gain-theorem/) for a nonlinearity of gain $c$.

**Passivity.** Case 2 can be read as the [passivity theorem](/passivity-theorem/) after a loop shift. The static map from $y$ to $\psi$ in the sector $[0, k_2]$ satisfies $y\psi \ge \psi^2/k_2$, so it is passive with a margin. Moved to the linear part, this margin is the constant $1/k_2$, and case 2 asks that $1/k_2 + G$ is strictly positive real.

**Multivariable form.** For vector $u$ and $y$ with the sector condition $(\psi - K_1 y)^T(\psi - K_2 y) \le 0$, the same proof works with $Z(s) = [I + K_2 G(s)][I + K_1 G(s)]^{-1}$ strictly positive real and $A - B K_1 C$ Hurwitz (Khalil 2002, Section 7.1).

**LMI form.** By the KYP lemma, the condition is feasibility of an LMI of size $(n + 1) \times (n + 1)$ in $P$, with $n(n + 1)/2$ unknowns. It is solved by [semidefinite programming](/semidefinite-programming/), and the solution $P$ gives the Lyapunov function $x^T P x$ directly. The KYP lemma also says that the frequency test is the same as the existence of a common quadratic Lyapunov function for all linear gains in the sector, up to boundary cases.

**Worked example.** Take $G(s) = 1/(s + 1)^3$, with $A$ Hurwitz, $p = 0$ and $1/G(j\omega) = (1 + j\omega)^3$. With $t = \omega^2$, $\operatorname{Re}(1 + j\omega)^3 = 1 - 3t$ and $|1 + j\omega|^6 = (1 + t)^3$. The constant gains give the Hurwitz sector $(-1, 8)$.
- *Sector $[0, \beta]$.* $\operatorname{Re} G(j\omega) = (1 - 3t)/(1 + t)^3$ has the minimum $-1/4$ at $t = 1$, with $G(j1) = -0.25 - 0.25j$. Case 2 holds exactly when $-1/\beta < -1/4$, that is, $\beta < 4$.
- *Sector $[-c, c]$.* $|G(j\omega)| = (1 + t)^{-3/2}$ has the maximum $1$ at $\omega = 0$, so case 3 holds for $c < 1$.
- *Sector $[1, \beta]$.* Multiply $Z$ by $|1 + k_1 G|^2/|G|^2 > 0$: the condition $\operatorname{Re} Z(j\omega) > 0$ becomes $f(t) = (1 + t)^3 + (k_1 + k_2)(1 - 3t) + k_1 k_2 > 0$ for all $t \ge 0$. With $k_1 = 1$ and $k_2 = 2 + 2\sqrt 2 = 4.82843$, the minimum of $f$ is at $(1 + t)^2 = 3 + 2\sqrt 2 = (1 + \sqrt 2)^2$, that is, $t = \sqrt 2$, and $f(\sqrt 2) = (7 + 5\sqrt 2) - (9 + 7\sqrt 2) + (2 + 2\sqrt 2) = 0$. So case 1 holds for every $k_2 < 2 + 2\sqrt 2$, and the disk touches the plot at $\omega = 2^{1/4} = 1.18921$ in the limit. The plot crosses the negative real axis only at $G(j\sqrt 3) = -1/8$, to the right of $-1/k_1 = -1$, so it does not go around the disk, which matches $p = 0$. The same computation gives $k_2 < 2 + 2\sqrt{1 + k_1}$ for every $k_1 \ge 0$.

The circle criterion covers time-varying nonlinearities, and it pays for that: for $[0, \beta]$ it stops at $4$, while the Hurwitz sector goes to $8$. For time-invariant nonlinearities, the [Popov criterion](/popov-criterion/) reaches every $k < 8$ for the same $G$.

## Tightness

**The disk cannot shrink.** For $G(s) = 1/(s + 1)^3$ and the sector $[-c, c]$, the theorem holds for every $c < 1$. At $c = 1$ the sector contains the linear gain $\psi = -y$, and the closed loop polynomial $(s + 1)^3 - 1 = s(s^2 + 3s + 3)$ has a root at $s = 0$, so the origin is not asymptotically stable. A smaller disk would certify $c = 1$, which is false.

**The Hurwitz sector is not enough for time-varying nonlinearities.** Take $G(s) = 1/(s^2 + 0.2s)$ and the sector $[1, 9]$. Every constant gain $k > 0$ gives the Hurwitz polynomial $s^2 + 0.2s + k$. The time-varying gain that is $1$ while $|y|$ grows and $9$ while $|y|$ shrinks multiplies the speed $|\dot y|$ at each zero of $y$ by $2.45299$, as the [Lur'e problem](/lure-problem/) page computes, so the origin is not asymptotically stable. The circle criterion detects this: with $k_1 = 1$ and $1/G(j\omega) = -t + 0.2j\omega$, the test is $t^2 - (k_2 + 0.96)t + k_2 > 0$ for all $t \ge 0$, which holds exactly when $(k_2 + 0.96)^2 < 4k_2$, that is, $k_2 < 1.44$. The test does not certify the sector $[1, 9]$, as it must not.

**The criterion is only sufficient.** For time-invariant nonlinearities in $[0, \beta]$ and $G = 1/(s + 1)^3$, the circle criterion stops at $\beta = 4$, but the loop is absolutely stable for every $\beta < 8$ by the Popov criterion. The circle criterion gives one quadratic Lyapunov function for the whole sector, and a loop can be absolutely stable without one.

## History

Popov (1961) gave the first frequency domain test for the Lur'e problem, for time-invariant nonlinearities. In 1964, Sandberg proved a frequency condition for a loop with one time-varying nonlinear element by a functional analysis argument, and Narendra and Goldwyn gave the geometric disk condition with a quadratic Lyapunov function. Zames (1966, Part II) placed the result in his input-output theory of conic sectors, with the disk condition in the frequency plane that gives the test its name. The Lyapunov proof rests on the KYP lemma of Yakubovich (1962) and Kalman (1963). Khalil (2002, Section 7.1) gives the three cases in the form used here.

## References
