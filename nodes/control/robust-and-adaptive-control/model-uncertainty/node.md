---
tag: ASK7MX
kind: concept
slug: model-uncertainty
name: Model uncertainty
aliases:
- unstructured uncertainty
- multiplicative uncertainty
area: control/robust-and-adaptive-control
level: core
summary: The gap between a plant and its model, described as a set of plants, by a perturbation in RH-infinity bounded in the H-infinity norm or by parameter ranges, that a controller must handle.
history:
  year: 1981
  people: [John C. Doyle, Gunter Stein]
  note: "Doyle and Stein (1981) described the error of a multivariable model by a frequency dependent bound on a multiplicative perturbation and tested robustness with singular values."
prereqs: [h-infinity-norm, transfer-function]
see_also: [small-gain-theorem, linear-fractional-transformation, structured-singular-value, coprime-factorization, kharitonov-theorem, quadratic-stability, mixed-sensitivity-design, nu-gap-metric]
sources:
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 7, Uncertainty and Robustness for SISO Systems, and Chapter 8, Robust Stability and Performance Analysis for MIMO Systems (the forms of perturbation and the robust stability tests)
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 9, Model Uncertainty and Robustness
  - paper: "John C. Doyle and Gunter Stein, Multivariable feedback design: concepts for a classical/modern synthesis, IEEE Transactions on Automatic Control 26(1), 4-16, 1981"
    locator: the multiplicative error bound and the singular value test for robust stability
---

Model uncertainty is the difference between the real plant and the model that a controller is designed for. Robust control does not try to know this difference exactly. It describes it as a set of plants that surely contains the real one, and it asks that one controller works for every plant in the set. The set is usually built from the nominal model $G$, a weight $W$ that says how large the error can be at each frequency, and an unknown perturbation $\Delta$ with all its poles in the open left half plane and $\|\Delta\|_\infty \le 1$ in the [H-infinity norm](/h-infinity-norm/). The [small-gain theorem](/small-gain-theorem/) then turns "internally stable for every plant in the set" into one norm condition on a closed-loop transfer function.

## In plain words

Every model is wrong in some way. A motor heats up and loses torque, a fast resonance was left out, a delay was rounded down. You cannot list all these errors, but you can often say how large they can be: maybe ten percent at low speeds and more than one hundred percent at high speeds. Robust control turns such a statement into a family of possible plants, and then checks one controller against the whole family. If the controller is safe for every member, it is safe for the real plant too. The price is caution: the family usually holds many plants that cannot really occur, so the check can reject a controller that would work.

## The idea

**Notation.** $G$ is the nominal model, a $p \times m$ [transfer function](/transfer-function/). $K$ is the controller in the negative feedback loop $u = -K y$ (plus references). The closed-loop maps are $S = (I + G K)^{-1}$ and $T = G K (I + G K)^{-1}$ at the plant output, and $T_I = K G (I + K G)^{-1}$ at the plant input (see the [sensitivity function](/sensitivity-function/)). $\Delta$ is any transfer matrix in $RH_\infty$, so with all poles in the open left half plane, with $\|\Delta\|_\infty \le 1$. Weights $w$ are scalar transfer functions in $RH_\infty$.

**The set of plants.** A form of perturbation fixes how $\Delta$ enters. The common forms, with the robust stability test for each, are below. Each test assumes that $K$ makes the nominal loop internally stable, that is, every closed-loop transfer function between two points of the loop is in $RH_\infty$.

| form | perturbed plant $G_p$ | the loop is internally stable for every allowed $\Delta$ if and only if |
|---|---|---|
| additive | $G + w_A \Delta$ | $\|w_A K S\|_\infty < 1$ |
| input multiplicative | $G (I + w_I \Delta)$ | $\|w_I T_I\|_\infty < 1$ |
| output multiplicative | $(I + w_O \Delta) G$ | $\|w_O T\|_\infty < 1$ |
| inverse output multiplicative | $(I + w_{iO} \Delta)^{-1} G$ | $\|w_{iO} S\|_\infty < 1$ |
| left coprime factor | $(M + \Delta_M)^{-1}(N + \Delta_N)$, $\|[\Delta_N\ \Delta_M]\|_\infty < \varepsilon$ | $\left\|\begin{bmatrix} K \\ I \end{bmatrix} (I + G K)^{-1} M^{-1}\right\|_\infty \le 1/\varepsilon$ |

**Why these tests hold.** In each case, cut the loop at $\Delta$. What $\Delta$ sees is one closed-loop transfer function $M_\Delta$ of the nominal loop: $-w_A K S$, $-w_I T_I$, $-w_O T$, $w_{iO} S$, or the coprime factor map. The perturbed loop is the feedback of $M_\Delta$ and $\Delta$, the $M$-$\Delta$ form of a [linear fractional transformation](/linear-fractional-transformation/). If $\|M_\Delta\|_\infty < 1$, the small-gain theorem gives internal stability for every $\Delta$ with $\|\Delta\|_\infty \le 1$. Conversely, if $\|M_\Delta\|_\infty \ge 1$, there is a frequency $\omega_0$ (or a sequence of them) where $\sigma_{\max}(M_\Delta(j\omega_0)) \ge 1$, and a $\Delta \in RH_\infty$ with $\|\Delta\|_\infty \le 1$ that matches the inverse of $M_\Delta$ in one direction at $\omega_0$ puts a closed-loop pole at $j\omega_0$. The converse needs $\Delta$ to be free: any complex, dynamic, full matrix. Both directions are proved in Zhou, Doyle and Glover (Chapter 9) and in Skogestad and Postlethwaite (Chapter 8). The coprime factor test, with $G = M^{-1} N$ a normalized [coprime factorization](/coprime-factorization/), is the base of [H-infinity loop shaping](/h-infinity-loop-shaping/).

**Choosing the weight.** For a family of possible plants $\Pi$, a multiplicative weight must cover the relative error of each member at each frequency:

$$|w_I(j\omega)| \ge \max_{G_p \in \Pi} \sigma_{\max}\bigl(G^{-1}(G_p - G)\bigr)(j\omega) \quad \text{for every } \omega$$

(for $m = p = 1$ this is $|G_p/G - 1|$). Typical weights are small at low frequency, where the model is good, and above 1 at high frequency, where even the sign of the plant is unknown. The test $\|w_O T\|_\infty < 1$ then forces $|T(j\omega)|$ below $1/|w_O(j\omega)|$, which limits the bandwidth.

**Structured and parametric uncertainty.** The forms above use one full block $\Delta$ and so allow every complex perturbation. Real uncertainty often has more structure:

- Several independent blocks, for example errors at the input and at the output at the same time. Pull all of them into a block diagonal $\Delta$ by a linear fractional transformation. The exact test is then the [structured singular value](/structured-singular-value/) $\mu$, and [mu-analysis](/mu-analysis/) computes bounds on it.
- Real parameters in known ranges. If the coefficients of the characteristic polynomial vary independently in intervals, the [Kharitonov theorem](/kharitonov-theorem/) decides robust stability with four polynomials. If they depend affinely on the parameters, the [edge theorem](/edge-theorem/) checks the edges of a polytope.
- A state matrix in a polytope. A common quadratic Lyapunov function, found by an LMI at the vertices, proves [quadratic stability](/quadratic-stability/).

**Robust performance.** Robust stability is not enough. Robust performance asks that a performance bound, such as $\|w_P S_p\|_\infty < 1$ on the perturbed sensitivity, holds for every plant in the set. With one full block of uncertainty and one performance channel, this is a $\mu$ test with two blocks.

## Examples

- **A neglected fast pole.** The model is $G = 1/(s + 1)$, and the real plant may be $G_p = 1/((s + 1)(0.1 s + 1))$. The relative error is $G_p/G - 1 = -0.1 s/(0.1 s + 1)$, with magnitude $0.0995$ at 1 rad/s, $0.707$ at 10 rad/s and $0.995$ at 100 rad/s. Take $w_I = 0.1 s/(0.1 s + 1)$. With the controller $K = k > 0$, $T = k/(s + 1 + k)$ and $w_I T = k s/((s + 10)(s + 1 + k))$. The peak of $|s/((s + a)(s + b))|$ is $1/(a + b)$, at $\omega = \sqrt{ab}$, so $\|w_I T\|_\infty = k/(k + 11)$: $0.0833$ for $k = 1$, $0.476$ for $k = 10$ and $0.901$ for $k = 100$. The test passes for every gain. This agrees with the real plant: its loop polynomial $0.1 s^2 + 1.1 s + 1 + k$ is Hurwitz for every $k > -1$.
- **A gain range covered by a disc.** The model is $k\,G_0$ with $G_0 = 1/(s + 1)^3$ and a gain $k \in [1, k_{\max}]$, in a loop with $K = 1$. The real loop is Hurwitz exactly for $k < 8$ (the ultimate gain of $1/(s + 1)^3$ is 8). Write $k = \bar k (1 + r \delta)$ with $\bar k = (1 + k_{\max})/2$, $r = (k_{\max} - 1)/(k_{\max} + 1)$ and $\delta \in [-1, 1]$. If $\delta$ is replaced by a complex $\Delta$ with $\|\Delta\|_\infty \le 1$, the test $\|r\,T\|_\infty < 1$ with $T = \bar k G_0/(1 + \bar k G_0)$ passes only for $k_{\max}$ below about $4.83$ (computed on a dense frequency grid; $k_{\max} = 4$ gives $0.761$). The complex disc contains phase errors that a real gain cannot make, so it loses the range from 4.83 to 8. This is the conservatism of a full complex block for real parameters.
- **A time delay.** If the real plant is $G e^{-\theta s}$ with $0 \le \theta \le \theta_{\max}$, the relative error is $|e^{-j\omega\theta} - 1| = 2|\sin(\omega\theta/2)|$. At low frequency it is about $\omega\theta_{\max}$, and it reaches 2 at $\omega = \pi/\theta_{\max}$. Any weight $w_O$ must be at least this large, so near $\omega = \pi/\theta_{\max}$ the test needs $|T(j\omega)| < 1/2$. An unknown delay limits the closed-loop bandwidth to roughly $1/\theta_{\max}$.

## Where it is used

- **Robust controller design.** [Mixed sensitivity design](/mixed-sensitivity-design/) and the [H-infinity control problem](/h-infinity-control-problem/) put the weight of the uncertainty on $T$ or $K S$ and minimize the H-infinity norm. [H-infinity loop shaping](/h-infinity-loop-shaping/) uses the coprime factor form.
- **Analysis.** [Mu-analysis](/mu-analysis/) tests robust stability and robust performance against structured uncertainty; [quadratic stability](/quadratic-stability/), the Kharitonov theorem and the edge theorem handle parameters.
- **Distance between models.** The [nu-gap metric](/nu-gap-metric/) measures how far apart two plants are in the sense that matters for feedback, through coprime factor perturbations.
- **Identification for control.** An identified model comes with an error bound, and the bound becomes the weight.
- **Adaptive control.** Where the uncertainty is too large for one fixed controller, [adaptive control](/adaptive-control/) estimates the parameters online. Unmodeled dynamics remain, and the [Rohrs counterexample](/rohrs-counterexample/) shows what happens when an adaptive law ignores them.

## References
