---
tag: Z0JFEF
kind: definition
slug: nu-gap-metric
name: Nu-gap metric
aliases:
- Vinnicombe metric
area: control/robust-and-adaptive-control
level: research
summary: A distance between plants, at most 1. A controller whose stability margin with one plant exceeds the distance also stabilizes the other plant.
prereqs: [coprime-factorization, h-infinity-norm, nyquist-stability-criterion]
see_also: [h-infinity-loop-shaping, model-uncertainty, small-gain-theorem, youla-parametrization, h-infinity-control-problem, mixed-sensitivity-design]
sources:
  - paper: doi:10.1109/9.237648
    title: Glenn Vinnicombe, Frequency domain uncertainty and the graph topology, IEEE Transactions on Automatic Control 38(9), 1371-1383, 1993
    locator: the definition of the nu-gap metric, its winding number condition, and the robust stability result with the generalized stability margin
  - book: doi:10.1142/p140
    title: Glenn Vinnicombe, Uncertainty and Feedback, H-infinity Loop-Shaping and the nu-Gap Metric, Imperial College Press, 2000
    locator: Chapter 3, The nu-gap metric
  - paper: doi:10.1109/9.29424
    title: Keith Glover and Duncan McFarlane, Robust stabilization of normalized coprime factor plant descriptions with H-infinity-bounded uncertainty, IEEE Transactions on Automatic Control 34(8), 821-830, 1989
    locator: the optimal stability margin for normalized coprime factor uncertainty in terms of the Hankel norm
  - paper: doi:10.1016/S1474-6670(17)63475-X
    title: George Zames and Ali K. El-Sakkary, Uncertainty in unstable systems, the gap metric, IFAC Proceedings Volumes 14, 149-152, 1981
    locator: the gap metric as a measure of distance between possibly unstable plants
  - paper: doi:10.1016/0167-6911(88)90067-9
    title: Tryphon T. Georgiou, On the computation of the gap metric, Systems and Control Letters 11(4), 253-257, 1988
    locator: the computation of the gap from normalized coprime factors
---

The nu-gap metric, written $\delta_\nu(P_1, P_2)$, is a distance between two linear plants with the same numbers of inputs and outputs. Glenn Vinnicombe defined it in 1993. Its values lie in $[0, 1]$, and it is designed for one use: if a controller $C$ stabilizes $P_1$ with a generalized stability margin $b_{P_1, C}$ larger than $\delta_\nu(P_1, P_2)$, then $C$ also stabilizes $P_2$. Two plants can be close in this metric even when one is unstable and the other is not, and far apart even when their frequency responses differ by little in the usual norm. The metric is computed from the frequency responses at each frequency, plus one winding number test.

## Definition

**Notation.** For a transfer function matrix $P$, let $P^*(s) = P(-s)^T$, so $P^*(j\omega)$ is the complex conjugate transpose of $P(j\omega)$. Let $\eta(P)$ be the number of poles of $P$ in the open right half plane and $\eta_0(P)$ the number on the imaginary axis. For a scalar rational function $g$ with no poles or zeros on the imaginary axis, let $\mathrm{wno}\,g$ be the number of zeros of $g$ minus the number of poles of $g$ in the open right half plane. By the argument principle this is the number of turns of $g$ around 0 along the Nyquist contour, the same count as in the [Nyquist criterion](/nyquist-stability-criterion/). Poles on the axis are handled by an indentation of the contour.

**Pointwise distance.** For two complex matrices $p_1$ and $p_2$ of the same size,

$$\kappa(p_1, p_2) = \bar\sigma\big((I + p_2 p_2^*)^{-1/2}\,(p_2 - p_1)\,(I + p_1^* p_1)^{-1/2}\big).$$

For scalars this is $\kappa(p_1, p_2) = |p_1 - p_2| / \big(\sqrt{1 + |p_1|^2}\sqrt{1 + |p_2|^2}\big)$, the chordal distance between the two points after projection on the Riemann sphere of diameter 1. It is at most 1, with 1 for $p_2 = -1/\bar p_1$.

**Nu-gap metric** (Vinnicombe 1993). For finite-dimensional plants $P_1$ and $P_2$ of the same size,

$$\delta_\nu(P_1, P_2) = \begin{cases} \sup_\omega \kappa\big(P_1(j\omega), P_2(j\omega)\big) & \text{if } \det(I + P_2^* P_1)(j\omega) \ne 0 \text{ for all } \omega \text{ and } \mathrm{wno}\det(I + P_2^* P_1) + \eta(P_1) - \eta(P_2) - \eta_0(P_2) = 0, \\ 1 & \text{otherwise.} \end{cases}$$

The supremum includes $\omega = \infty$. Vinnicombe (1993) proved that $\delta_\nu$ is a metric on the set of finite-dimensional plants of a given size.

**Generalized stability margin.** For a plant $P$ and a controller $C$ in the negative feedback loop $u = C(r - y)$,

$$b_{P, C} = \left\| \begin{bmatrix} P \\ I \end{bmatrix} (I + C P)^{-1} \begin{bmatrix} C & I \end{bmatrix} \right\|_\infty^{-1}$$

if the loop is internally stable, and $b_{P, C} = 0$ if it is not. The matrix is the map from the input and output disturbances to the plant output and input. Vinnicombe uses positive feedback, $(I - C P)^{-1}[-C \ \ I]$. The change of sign of $C$ multiplies a block column by $-1$, which does not change the norm. For a scalar loop, $b_{P, C} = \inf_\omega |1 + P C| / \big(\sqrt{1 + |P|^2}\sqrt{1 + |C|^2}\big)$, which equals $\inf_\omega \kappa(P, -1/C)$.

**Robust stability theorem** (Vinnicombe 1993). Let $C$ stabilize $P_1$. If $\delta_\nu(P_1, P_2) < b_{P_1, C}$, then $C$ stabilizes $P_2$. The test cannot be improved: $C$ stabilizes every $P_2$ with $\delta_\nu(P_1, P_2) \le \beta$ if and only if $b_{P_1, C} > \beta$, so the ball in the nu-gap is the largest set of plants that the margin alone guarantees. A quantitative form (Vinnicombe 2000, chapter 3) is

$$\arcsin b_{P_2, C} \ge \arcsin b_{P_1, C} - \arcsin \delta_\nu(P_1, P_2).$$

## Examples and non-examples

**Close plants, one of them unstable.** Let $P_1(s) = 100/(2s + 1)$ and $P_2(s) = 100/(2s - 1)$. On the axis, $P_1 - P_2 = 200/(4\omega^2 + 1)$ and $|P_1|^2 = |P_2|^2 = 10^4/(4\omega^2 + 1)$, so

$$\kappa\big(P_1(j\omega), P_2(j\omega)\big) = \frac{200}{4\omega^2 + 1 + 10^4},$$

with the largest value $200/10001 = 0.019998$ at $\omega = 0$. For the winding condition, $1 + P_2^* P_1 = 1 - 10^4/(2s + 1)^2$, which has no zero on the axis, the zeros $s = 49.5$ and $s = -50.5$, and the poles at $s = -0.5$. So $\mathrm{wno} = 1$, and $1 + \eta(P_1) - \eta(P_2) - \eta_0(P_2) = 1 + 0 - 1 - 0 = 0$. Hence $\delta_\nu(P_1, P_2) = 0.019998$. The controller $C = 1$ has $b_{P_1, C} = 1/\sqrt 2 = 0.70711$ (since $\mathrm{Re}\,P_1 > 0$, $|1 + P_1| \ge \sqrt{1 + |P_1|^2}$, and the infimum is the limit as $\omega \to \infty$). This is larger than $0.019998$, so $C = 1$ stabilizes $P_2$: indeed $1 + P_2 = (2s + 99)/(2s - 1)$, with the closed loop pole $-49.5$. The arcsin bound gives $b_{P_2, C} \ge \sin(\pi/4 - \arcsin 0.019998) = 0.69282$, and the true value is $99/\sqrt{20002} = 0.70000$. In contrast, $\sup_\omega |P_1 - P_2| = 200$, so the plain distance of the responses says nothing useful.

**The winding condition matters.** Let $Q_1(s) = 0.1/(s + 1)$ and $Q_2(s) = 0.1/(s - 1)$. The pointwise distance is $\kappa = 0.2/(\omega^2 + 1.01)$, at most $0.19802$. But $1 + Q_2^* Q_1 = 1 - 0.01/(s + 1)^2$ has its zeros at $-0.9$ and $-1.1$, so $\mathrm{wno} = 0$, the condition gives $0 + 0 - 1 - 0 \ne 0$, and $\delta_\nu(Q_1, Q_2) = 1$. This is correct: the controller $C = 0$ has $b_{Q_1, 0} = 1/\sqrt{1.01} = 0.99504$, far above $0.19802$, but it does not stabilize $Q_2$. By the Nyquist criterion, a controller that stabilizes $Q_2$ needs $|Q_2 C| > 1$, so $|C| > 10$, at some frequency.

**Static plants.** For constants $p_1 = 10$ and $p_2 = -10$, $\kappa = 20/101 = 0.198$ and the winding condition holds, so $\delta_\nu = 0.198$. For $p_1 = 1$ and $p_2 = -1$, $\kappa = 1$ and $\delta_\nu = 1$: a loop gain of $+1$ and one of $-1$ are as far apart as possible, since $1 + p_2^* p_1 = 0$.

**A non-example: the H-infinity distance.** $\|P_1 - P_2\|_\infty$ is not a good distance for feedback. It is infinite when one plant is unstable and the other is not, and it treats a change from 100 to 110 the same as a change from 0 to 10, though the first barely matters inside a loop. The nu-gap weighs each difference by $\sqrt{1 + |p_1|^2}\sqrt{1 + |p_2|^2}$, so large gains count less.

## Related definitions

- **Gap metric.** Zames and El-Sakkary introduced the gap $\delta_g(P_1, P_2)$ between the graphs of the two plants, and Georgiou (1988) showed how to compute it from normalized [coprime factors](/coprime-factorization/) with an H-infinity optimization. Vinnicombe (1993) proved $\delta_\nu \le \delta_g$, and that the two metrics give the same topology, the weakest one in which closed loop stability is an open property. The nu-gap is the less conservative of the two for the robust stability test.
- **Normalized coprime factor uncertainty.** The set $\{P_2 : \delta_\nu(P_1, P_2) < \beta\}$ contains the plants $(\tilde M + \Delta_M)^{-1}(\tilde N + \Delta_N)$ with $\|[\Delta_N \ \Delta_M]\|_\infty < \beta$, where $P_1 = \tilde M^{-1}\tilde N$ is a normalized left coprime factorization. The controller with the largest $b_{P, C}$ is the one of [H-infinity loop shaping](/h-infinity-loop-shaping/).
- **Optimal stability margin.** $b_{\rm opt}(P) = \sup_C b_{P, C} = \sqrt{1 - \|[N \ M]\|_H^2}$, where $\|\cdot\|_H$ is the Hankel norm of the normalized coprime factors (Glover and McFarlane 1989, as used on the [H-infinity loop shaping](/h-infinity-loop-shaping/) page).
- **Model validation.** For a set of models identified from data, $\max \delta_\nu$ over pairs is a measure of the model spread, to compare with the margin $b_{P, C}$ of a candidate controller ([model uncertainty](/model-uncertainty/)).

## References
