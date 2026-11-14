---
tag: VR19M7
kind: definition
slug: log-sum-exp-wirelength
name: Log-sum-exp wirelength
aliases:
- LSE wirelength model
area: eda/partitioning-floorplanning-and-placement
level: advanced
summary: The smooth bound gamma times the log of the sum of exp(x_i/gamma), and its counterpart for the minimum, that approximates the half-perimeter wire length.
prereqs: [half-perimeter-wirelength, log-sum-exp-trick, convex-function]
see_also: [analytical-placement, electrostatics-based-placement, quadratic-placement, clique-net-model, smoothness, nesterov-accelerated-gradient, gradient-descent]
sources:
  - paper: "William C. Naylor, Ross Donelly and Lu Sha, Non-linear optimization system and method for wire length and delay optimization for an automatic electric circuit placer, United States Patent 6,301,693, 2001"
    locator: the smooth log-sum-exp form of the bounding box length of a net (general locator)
  - paper: doi:10.1109/TCAD.2008.923063
    title: Tung-Chieh Chen, Zhe-Wei Jiang, Tien-Chang Hsu, Hsin-Chen Chen and Yao-Wen Chang, NTUplace3, an analytical placer for large-scale mixed-size designs with preplaced blocks and density constraints, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(7), 1228 to 1240, 2008
    locator: the log-sum-exp wirelength model and its smoothing parameter in the objective of the analytical placer
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 3, the log-sum-exp function as an example of a convex function, with its Hessian
  - paper: doi:10.1145/2699873
    title: Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis Jen-Hsin Huang, Chin-Chi Teng and Chung-Kuan Cheng, ePlace, electrostatics-based placement using fast Fourier transform and Nesterov's method, ACM Transactions on Design Automation of Electronic Systems 20(2), article 17, 2015
    locator: the weighted average wirelength model used in place of log-sum-exp
---

The log-sum-exp (LSE) wirelength is a smooth function of the pin positions of a net that approximates its [half-perimeter wirelength](/half-perimeter-wirelength/) (HPWL) from above. It replaces the maximum of the pin coordinates by $\gamma \ln \sum_i e^{x_i / \gamma}$ and the minimum by $-\gamma \ln \sum_i e^{-x_i / \gamma}$, where $\gamma > 0$ is a smoothing length. For a net of $p$ pins it is never below the HPWL and at most $4 \gamma \ln p$ above it. It is convex, has a gradient everywhere, and its gradient is Lipschitz with a constant of order $1 / \gamma$, so gradient methods can minimize it. Nonlinear [analytical placers](/analytical-placement/) such as NTUplace3 use it as their wirelength term; they start with a large $\gamma$ and make it smaller as the cells spread.

## Definition

Let a net $e$ have $p \ge 1$ pins at $(x_1, y_1), \ldots, (x_p, y_p)$, and let $\gamma > 0$. Write

$$ \mathrm{smax}_\gamma(x) = \gamma \ln \sum_{i=1}^{p} e^{x_i / \gamma}, \qquad \mathrm{smin}_\gamma(x) = -\gamma \ln \sum_{i=1}^{p} e^{-x_i / \gamma}. $$

The LSE wirelength of $e$ is

$$ \mathrm{LSE}_\gamma(e) = \bigl( \mathrm{smax}_\gamma(x) - \mathrm{smin}_\gamma(x) \bigr) + \bigl( \mathrm{smax}_\gamma(y) - \mathrm{smin}_\gamma(y) \bigr), $$

and the total for a netlist is $\sum_e w_e \, \mathrm{LSE}_\gamma(e)$, with the pins at the cell centers unless pin offsets are given. Pads give fixed terms. The $x$ part and the $y$ part are independent; below, only the $x$ part is shown.

**Bounds.** Let $M = \max_i x_i$ and $m = \min_i x_i$. The sum $\sum_i e^{x_i / \gamma}$ has one term $e^{M / \gamma}$ and $p$ terms of at most $e^{M / \gamma}$, so

$$ M \le \mathrm{smax}_\gamma(x) \le M + \gamma \ln p, \qquad m - \gamma \ln p \le \mathrm{smin}_\gamma(x) \le m. $$

So $M - m \le \mathrm{smax}_\gamma(x) - \mathrm{smin}_\gamma(x) \le M - m + 2 \gamma \ln p$, and with the $y$ part, $\mathrm{HPWL}(e) \le \mathrm{LSE}_\gamma(e) \le \mathrm{HPWL}(e) + 4 \gamma \ln p$. The upper bound holds with equality when all $x_i$ are equal and all $y_i$ are equal. As $\gamma \to 0$, $\mathrm{LSE}_\gamma(e) \to \mathrm{HPWL}(e)$.

**Gradient.** With $a_i = e^{x_i / \gamma} / \sum_j e^{x_j / \gamma}$ and $b_i = e^{-x_i / \gamma} / \sum_j e^{-x_j / \gamma}$,

$$ \frac{\partial}{\partial x_i} \bigl( \mathrm{smax}_\gamma - \mathrm{smin}_\gamma \bigr) = a_i - b_i. $$

The weights $a$ are the softmax of $x / \gamma$, and $b$ the softmax of $-x / \gamma$. Each sums to 1, so the gradient sums to 0 over the pins: moving all pins of a net by the same amount does not change the value. Each partial derivative lies in $(-1, 1)$, so the function is 1-Lipschitz in each coordinate. For a cell, add $w_e (a_i - b_i)$ over the pins $i$ of the cell.

**Convexity and smoothness.** The Hessian of $\mathrm{smax}_\gamma$ is $\frac{1}{\gamma} \bigl( \mathrm{diag}(a) - a a^\top \bigr)$. For a vector $v$, $v^\top (\mathrm{diag}(a) - a a^\top) v = \sum_i a_i v_i^2 - (\sum_i a_i v_i)^2 \ge 0$, the variance of $v$ under the weights $a$, so $\mathrm{smax}_\gamma$ is convex. In row $i$ the diagonal entry is $a_i (1 - a_i)$ and the other entries have absolute values summing to $a_i (1 - a_i)$, so by Gershgorin's theorem every eigenvalue is at most $\max_i 2 a_i (1 - a_i) \le \frac12$. The same holds for $-\mathrm{smin}_\gamma$ with $b$. So the $x$ part of $\mathrm{LSE}_\gamma(e)$ is convex, and its gradient is Lipschitz with constant at most $1 / \gamma$ in the Euclidean norm.

**Computation.** For a small $\gamma$, $e^{x_i / \gamma}$ overflows. Compute $\mathrm{smax}_\gamma(x) = M + \gamma \ln \sum_i e^{(x_i - M) / \gamma}$, where every exponent is at most 0, and likewise for $\mathrm{smin}_\gamma$ with $m$; this is the [log-sum-exp trick](/log-sum-exp-trick/). One net costs $O(p)$ time for the value and the gradient together, and a netlist costs $O(P)$ for $P$ pins.

## Examples and non-examples

- **Three pins, several $\gamma$.** Pins at $x = 0, 1, 4$, so $M - m = 4$. The $x$ part of LSE, its excess over 4, the bound $2 \gamma \ln 3$, and the gradient $(a_i - b_i)$, rounded to 4 places:

| $\gamma$ | $x$ part of LSE | excess | bound $2 \gamma \ln 3$ | gradient at $x = 0, 1, 4$ |
| --- | --- | --- | --- | --- |
| 2 | 5.7226 | 1.7226 | 4.3944 | $-0.4745, -0.1840, 0.6584$ |
| 1 | 4.3924 | 0.3924 | 2.1972 | $-0.7043, -0.2188, 0.9230$ |
| 0.5 | 4.0650 | 0.0650 | 1.0986 | $-0.8802, -0.1167, 0.9969$ |
| 0.25 | 4.0045 | 0.0045 | 0.5493 | $-0.9820, -0.0180, 1.0000$ |

As $\gamma$ falls, the value tends to 4 and the gradient tends to the subgradient $(-1, 0, 1)$ of $M - m$, which pulls only the outer pins. With a large $\gamma$ the middle pin also feels a pull.

- **All pins at one point.** Three pins at $x = 2$ with $\gamma = 1$: the HPWL is 0, but the $x$ part of LSE is $2 \ln 3 \approx 2.1972$, the full bound. LSE never reaches 0 for $p \ge 2$, so it does not measure the length of a net whose pins coincide.
- **Two pins.** Pins at $x = 0$ and $x = 4$ with $\gamma = 1$: the value is $4 + 2 \ln(1 + e^{-4}) \approx 4.0363$. The excess shrinks fast as the pins move apart, since only the far terms are small.
- **Not the length of a route.** LSE is a smooth stand-in for HPWL, and HPWL is a lower bound on the routed length; LSE is not an upper bound on the routed length.

## Related definitions

- **[Half-perimeter wirelength](/half-perimeter-wirelength/).** The limit of LSE as $\gamma \to 0$; convex and piecewise linear, but not differentiable where two pins tie for the extreme.
- **Weighted average (WA) model.** Replace the maximum by $\sum_i x_i e^{x_i / \gamma} / \sum_i e^{x_i / \gamma}$ and the minimum by $\sum_i x_i e^{-x_i / \gamma} / \sum_i e^{-x_i / \gamma}$ (Hsu, Chang and Balabanov 2011). Each is a weighted mean of the $x_i$, so the WA value is at most $M - m$; the first mean puts more weight on large $x_i$ than the plain mean and the second less, so the value is at least 0. With $x = 0, 1, 4$ and $\gamma = 1$ it is 3.4733, against 4.3924 for LSE. [ePlace](/electrostatics-based-placement/) and later placers use WA. WA is not convex in general.
- **Lp-norm model.** Replace the maximum by $(\sum_i x_i^q)^{1/q}$ for a large $q$ and positive coordinates. It is another smooth bound used in some placers.
- **Quadratic net models.** The [clique net model](/clique-net-model/) and the star model use squared distances. They are smooth and lead to linear systems, as in [quadratic placement](/quadratic-placement/), but they are not close to HPWL for nets of many pins.
- **Softmax and the log-sum-exp trick.** The gradient of $\mathrm{smax}_\gamma$ is the softmax of $x / \gamma$, and its stable evaluation is the [log-sum-exp trick](/log-sum-exp-trick/).
- **Smoothing of a nonsmooth convex function.** $\mathrm{smax}_\gamma$ is the standard smooth approximation of the maximum, with the trade-off of error $\gamma \ln p$ against [smoothness](/smoothness/) $1 / \gamma$ that governs how fast [gradient methods](/gradient-descent/) converge.

## References
