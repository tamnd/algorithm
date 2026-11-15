---
tag: 2VECK3
kind: definition
slug: linear-fractional-transformation
name: Linear fractional transformation
aliases:
- LFT
- M-Delta configuration
area: control/robust-and-adaptive-control
level: advanced
summary: "The map that closes part of a two-block system with a feedback block: F_l(P, K) = P11 + P12 K (I - P22 K)^(-1) P21. Controllers, uncertainty and 1/s all enter models this way."
prereqs: [transfer-function, feedback-control-loop]
see_also: [model-uncertainty, structured-singular-value, h-infinity-control-problem, small-gain-theorem, youla-parametrization, lpv-system, state-space-representation, mu-analysis]
sources:
  - paper: doi:10.1002/sapm1960391269
    title: Raymond Redheffer, On a certain linear fractional transformation, Journal of Mathematics and Physics 39 (1960) 269-286
    locator: the whole paper (the transformation and the composition rule now called the Redheffer star product)
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 10, Linear Fractional Transformation (the lower and upper LFT, well-posedness, the star product, and pulling uncertainty out of a system)
---

A linear fractional transformation (LFT) is the matrix function you get when you take a system with two inputs and two outputs and close one of the input-output pairs with a feedback block. If $P = \begin{bmatrix} P_{11} & P_{12} \\ P_{21} & P_{22} \end{bmatrix}$ and the block $K$ connects the second output back to the second input, the map from the first input to the first output is $P_{11} + P_{12} K (I - P_{22} K)^{-1} P_{21}$. In robust control nearly everything is written this way: a controller closes the lower loop of a generalized plant, an uncertainty block $\Delta$ closes the upper loop, and a transfer function is an LFT of its state-space matrices in $1/s$. For scalars the map is a Möbius transformation $(a\delta + b)/(c\delta + d)$, which gives the name.

## Definition

**Partition.** Let $P$ be a complex matrix (or a transfer matrix) of size $(p_1 + p_2) \times (q_1 + q_2)$, split as

$$P = \begin{bmatrix} P_{11} & P_{12} \\ P_{21} & P_{22} \end{bmatrix}, \qquad P_{11} \in \mathbb{C}^{p_1 \times q_1},\ P_{22} \in \mathbb{C}^{p_2 \times q_2}.$$

**Lower LFT.** For $K \in \mathbb{C}^{q_2 \times p_2}$ with $I - P_{22} K$ invertible,

$$F_l(P, K) = P_{11} + P_{12} K (I - P_{22} K)^{-1} P_{21}.$$

It is the map $w \mapsto z$ of the loop

$$\begin{bmatrix} z \\ y \end{bmatrix} = P \begin{bmatrix} w \\ u \end{bmatrix}, \qquad u = K y .$$

Proof: from $y = P_{21} w + P_{22} K y$, $y = (I - P_{22} K)^{-1} P_{21} w$, and $z = P_{11} w + P_{12} K y$.

**Upper LFT.** For $\Delta \in \mathbb{C}^{q_1 \times p_1}$ with $I - P_{11} \Delta$ invertible,

$$F_u(P, \Delta) = P_{22} + P_{21} \Delta (I - P_{11} \Delta)^{-1} P_{12},$$

the map from the second input to the second output when $\Delta$ closes the first pair. The convention puts the controller below and the uncertainty above.

**Well-posedness.** The LFT is well posed if the inverse exists. For transfer matrices, $F_l(P, K)$ is well posed if $I - P_{22}(\infty) K(\infty)$ is invertible; then the loop equations have a unique proper solution. For a constant matrix $\Delta$ that ranges over a set, the upper LFT is well posed for all members only if $I - P_{11} \Delta$ is invertible for all of them. That condition is exactly what the [structured singular value](/structured-singular-value/) measures.

**Algebra.** LFTs are closed under the usual operations, so a large interconnection is again one LFT:

- **Composition (Redheffer star product).** $F_l(P, F_l(Q, K)) = F_l(P \star Q, K)$ when $I - P_{22} Q_{11}$ is invertible, with
  $$P \star Q = \begin{bmatrix} P_{11} + P_{12} Q_{11} E P_{21} & P_{12} E' Q_{12} \\ Q_{21} E P_{21} & Q_{22} + Q_{21} P_{22} E' Q_{12} \end{bmatrix}, \qquad E = (I - P_{22} Q_{11})^{-1},\ E' = (I - Q_{11} P_{22})^{-1}.$$
- **Sums, products and inverses.** The sum and the product of two LFTs in the same block, and the inverse of an LFT (when it exists), are LFTs in a block that is the diagonal of the blocks involved.
- **Rational functions.** Every rational matrix function of parameters $\delta_1, \dots, \delta_k$ with no pole at $\delta = 0$ is an upper LFT in $\Delta = \operatorname{diag}(\delta_1 I_{r_1}, \dots, \delta_k I_{r_k})$ with repeated scalar blocks. The sizes $r_i$ depend on how the function is built, and smaller blocks make the later analysis cheaper.

**Uses.** With the controller closed, $M = F_l(P, K)$, and the uncertainty is put in the upper loop: the closed loop is $F_u(M, \Delta)$. Robust stability of this $M$-$\Delta$ loop is a property of $M_{11}$ and the set of $\Delta$: the [small-gain theorem](/small-gain-theorem/) for full blocks, and $\mu$ for block diagonal ones (see [model uncertainty](/model-uncertainty/)). The [Youla parametrization](/youla-parametrization/) writes every stabilizing controller as an LFT of one free stable parameter, and the [H-infinity control problem](/h-infinity-control-problem/) is to make $\|F_l(P, K)\|_\infty < \gamma$.

## Examples and non-examples

- **A transfer function is an LFT in 1/s.** With $M = \begin{bmatrix} A & B \\ C & D \end{bmatrix}$ and $\Delta = s^{-1} I_n$,
  $$F_u(M, s^{-1} I) = D + C s^{-1} (I - A s^{-1})^{-1} B = D + C (sI - A)^{-1} B = G(s).$$
  The state-space matrices are the coefficient matrix, and the integrators are the feedback block. Discrete time uses $z^{-1} I$ in the same way.
- **The sensitivity function.** In a loop with plant $G$, controller $K$ and $e = r - G u$, take $w = r$, $z = e$, the controller input $y = e$ and $u = K y$. Then $P_{11} = I$, $P_{12} = -G$, $P_{21} = I$, $P_{22} = -G$, and
  $$F_l(P, K) = I - G K (I + G K)^{-1} = (I + G K)^{-1} = S,$$
  the [sensitivity function](/sensitivity-function/). Other choices of $w$, $z$ give $T$, $K S$ and $S G$.
- **An uncertain gain.** A gain $k = \bar k (1 + r\delta)$ with $\delta \in [-1, 1]$ is $F_u\left(\begin{bmatrix} 0 & 1 \\ \bar k r & \bar k \end{bmatrix}, \delta\right) = \bar k + \bar k r \delta$. Here the LFT is affine in $\delta$ because $M_{11} = 0$.
- **An uncertain mass.** For $m = \bar m (1 + r\delta)$, the inverse $1/m$ is not affine in $\delta$, but it is an LFT:
  $$\frac{1}{\bar m (1 + r\delta)} = F_u\left(\begin{bmatrix} -r & 1 \\ -r/\bar m & 1/\bar m \end{bmatrix}, \delta\right) = \frac{1}{\bar m} - \frac{r}{\bar m} \frac{\delta}{1 + r\delta}.$$
  For $\bar m = 2$, $r = 0.5$ and $\delta = 1$ both sides are $1/3$. This is why a mass-spring model with an uncertain mass fits the $M$-$\Delta$ loop with one scalar block.
- **Composition.** For the scalar $P = \begin{bmatrix} 1 & 2 \\ 3 & 1/2 \end{bmatrix}$, $Q = \begin{bmatrix} 1/3 & 1 \\ -1 & 1/4 \end{bmatrix}$ and $K = 2/7$, both $F_l(P, F_l(Q, K))$ and $F_l(P \star Q, K)$ equal $89/77$ (computed in exact rational arithmetic).
- **Non-example: an ill-posed loop.** $P_{22} = 1$ and $K = 1$ give $1 - P_{22} K = 0$: the loop equation $y = P_{21} w + y$ has no solution when $P_{21} w \ne 0$, and $F_l(P, K)$ is not defined. For transfer functions the same happens when $P_{22}(\infty) K(\infty) = 1$, for example a plant and a controller that are both constant 1 at infinity: the loop is an algebraic loop with no proper solution.
- **Non-example: a quadratic in the parameter with a single block.** $f(\delta) = \delta^2$ is not an LFT in one scalar block $\delta I_1$, because such an LFT is a Möbius function $(a\delta + b)/(c\delta + d)$ of degree at most 1. It is an LFT in $\delta I_2$: $f = F_u\left(\begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}, \delta I_2\right)$, with the upper left $2 \times 2$ block as $M_{11}$. The repeated block is the price of polynomial dependence.

## Related definitions

- [Model uncertainty](/model-uncertainty/): the perturbed plants that are pulled into the upper block $\Delta$.
- [Structured singular value](/structured-singular-value/) and [mu-analysis](/mu-analysis/): the robustness test for an upper LFT with a block diagonal $\Delta$.
- [H-infinity control problem](/h-infinity-control-problem/): the design of $K$ for a lower LFT $F_l(P, K)$ with a small H-infinity norm.
- [Youla parametrization](/youla-parametrization/): the set of all stabilizing controllers, an LFT in a free parameter $Q \in RH_\infty$.
- [LPV system](/lpv-system/) and [gain scheduling](/gain-scheduling/): a system whose state-space matrices depend on a scheduling parameter is often written as an LFT in that parameter.
- [State-space representation](/state-space-representation/): the LFT in $s^{-1} I$ above.

## References
