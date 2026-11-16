---
tag: WY53ER
kind: algorithm
slug: lqg-control
name: Linear quadratic Gaussian control
aliases:
- LQG
- LQG regulator
area: control/optimal-and-predictive-control
level: core
summary: Combines a Kalman filter with LQR on the state estimate, which is optimal for linear systems with Gaussian noise by the separation theorem.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, p: the number of outputs, i: "the number of sign function iterations, usually 10 to 30"}
  time: {worst: "O(i n^3 + n^2 (m + p))"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1961
  people: [Rudolf E. Kalman, Richard S. Bucy, Peter D. Joseph, Julius T. Tou, Michael Athans]
  note: "Kalman and Bucy (1961) gave the continuous-time filter, Joseph and Tou (1961) the separation of estimation and control, and Athans (1971) collected the LQG design method."
prereqs: [infinite-horizon-lqr, kalman-bucy-filter, separation-principle, continuous-algebraic-riccati-equation]
see_also: [h2-optimal-control, loop-transfer-recovery, lqg-guaranteed-margins-counterexample, kalman-filter, lqr-stability-margins, state-observer, h-infinity-control-problem, sensitivity-function]
sources:
  - paper: doi:10.1109/TAC.1971.1099818
    title: Michael Athans, The role and use of the stochastic linear-quadratic-Gaussian problem in control system design, IEEE Transactions on Automatic Control 16(6), 529-552, 1971
    locator: the LQG problem, the separation of the filter and the regulator, and its use as a design method
  - paper: "R. E. Kalman and R. S. Bucy, New results in linear filtering and prediction theory, Journal of Basic Engineering 83(1), 95-108, 1961"
    locator: the continuous-time filter and the duality between filtering and the regulator problem
  - paper: doi:10.1109/TAC.1978.1101812
    title: John C. Doyle, Guaranteed margins for LQG regulators, IEEE Transactions on Automatic Control 23(4), 756-757, 1978
    locator: the example that shows that LQG regulators have no guaranteed margins
  - paper: doi:10.1080/00207178008922881
    title: J. D. Roberts, Linear model reduction and solution of the algebraic Riccati equation by use of the sign function, International Journal of Control 32(4), 677-687, 1980
    locator: the matrix sign function and its use to find the stable invariant subspace of the Hamiltonian matrix
  - paper: doi:10.1016/0024-3795(87)90222-9
    title: Ralph Byers, Solving the algebraic Riccati equation with the matrix sign function, Linear Algebra and its Applications 85, 267-279, 1987
    locator: the determinant scaling of the Newton iteration for the sign function
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: the chapters on state estimator design and on the linear quadratic Gaussian controller
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: the chapter on H2 optimal control, where the LQG controller is the H2 optimal controller
---

Linear quadratic Gaussian (LQG) control is the optimal output feedback for a linear plant with Gaussian white process and measurement noise and an average quadratic cost. The controller is a [Kalman-Bucy filter](/kalman-bucy-filter/) that estimates the state, followed by the [LQR](/infinite-horizon-lqr/) gain applied to the estimate. The two gains come from two independent [algebraic Riccati equations](/continuous-algebraic-riccati-equation/), one for the regulator and one for the filter. That the two designs can be done apart and still give the optimal controller is the separation theorem. The optimality is with respect to the noise model only: an LQG loop can have arbitrarily small gain and phase margins, as [Doyle's example](/lqg-guaranteed-margins-counterexample/) shows.

## In plain words

We want to steer a machine whose state we cannot see directly. We only get noisy sensor readings, and random pushes act on the machine. LQG splits the job in two. The first part is an estimator: it runs a copy of the machine's model, compares the predicted reading with the real one, and corrects its guess by a fixed amount of the difference. The second part is the best controller for the case where the state is known, and it acts on the guess as if the guess were the truth. Each part is designed on its own by solving one matrix equation. With the noise model and the cost of the problem, no other controller does better on average. But "best on average" does not mean "robust": a small change in the machine can still break the loop.

## The problem

Input: matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ of the plant

$$\dot x = A x + B u + w, \qquad y = C x + v,$$

where $w$ and $v$ are independent zero mean Gaussian white noises with intensities $W = W^T \ge 0$ and $V = V^T > 0$, and the weights $Q = Q^T \ge 0$ and $R = R^T > 0$ of the cost

$$J = \lim_{T \to \infty} \frac1T\, \mathbb{E} \int_0^T \left(x^T Q x + u^T R u\right) dt.$$

Assumptions: $(A, B)$ [stabilizable](/stabilizability/), $(Q^{1/2}, A)$ [detectable](/detectability/), $(C, A)$ detectable and $(A, W^{1/2})$ stabilizable.

Output: a dynamic controller $\dot{\hat x} = A_c \hat x + B_c y$, $u = -C_c \hat x$, that uses only past outputs and minimizes $J$ over all such causal output feedbacks.

The answer is $u = -K \hat x$, where $\hat x$ is the steady state Kalman-Bucy estimate. Here $L_o$ is the filter gain; the letter $L$ alone is kept for loop transfer functions.

## The algorithm

```pseudo id=main
LQG(A, B, C, Q, R, W, V)
L1   P ← CARE-SOLVE(A, B, Q, R)                       ▷ regulator: Aᵀ P + P A - P B R⁻¹ Bᵀ P + Q = 0
L2   K ← R⁻¹ Bᵀ P
L3   S ← CARE-SOLVE(Aᵀ, Cᵀ, W, V)                     ▷ filter: A S + S Aᵀ - S Cᵀ V⁻¹ C S + W = 0
L4   L_o ← S Cᵀ V⁻¹
L5   return controller x̂' = (A - B K - L_o C) x̂ + L_o y,  u = -K x̂
CARE-SOLVE(A, B, Q, R)                                ▷ stabilizing solution by the matrix sign function
L6   G ← B R⁻¹ Bᵀ;  H ← [[A, -G], [-Q, -Aᵀ]]          ▷ Hamiltonian matrix, 2n × 2n
L7   Z ← H; repeat c ← |det Z|^(-1/(2n)); Z ← (c Z + (c Z)⁻¹) / 2 until Z stops changing
L8   P ← least squares solution of [Z₁₂; Z₂₂ + I] P = -[Z₁₁ + I; Z₂₁]
L9   twice: P ← solution of (A - G P)ᵀ P' + P' (A - G P) + Q + P G P = 0
```

Lines L1 to L4 are the whole design: two Riccati equations, one for the regulator and one for the filter. Line L3 uses duality: the filter equation is the regulator equation for the data $(A^T, C^T, W, V)$, so the same solver serves both. Line L5 returns the controller in state-space form. Its order is $n$, the order of the plant.

Any method for the stabilizing CARE solution can be used in lines L1 and L3, for example the [Schur method](/schur-method-riccati/). This page uses the matrix sign function (Roberts 1980). Line L7 is Newton's iteration for $\mathrm{sign}(H)$, with the determinant scaling of Byers (1987), which cuts the number of steps when the eigenvalues of $H$ are far from $\pm 1$. The limit $Z$ has $Z + I$ equal to 0 on the stable invariant subspace of the [Hamiltonian matrix](/hamiltonian-matrix/), and that subspace is the range of $[I; P]$. Line L8 reads $P$ off from this fact. Line L9 runs two steps of [Kleinman's iteration](/kleinman-iteration/), which is Newton's method on the CARE and removes the rounding error of line L8. The code solves each Lyapunov equation by its Kronecker form, which is fine for the small $n$ of the tests.

## Example

Take the double integrator with the position measured: $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$, with $Q = I$, $R = 1$, $W = I$ and $V = 1$. The two Riccati equations have the same solution, because the data are symmetric under duality:

$$P = S = \begin{bmatrix} \sqrt3 & 1 \\ 1 & \sqrt3 \end{bmatrix}, \qquad K = \begin{bmatrix} 1 & \sqrt3 \end{bmatrix}, \qquad L_o = \begin{bmatrix} \sqrt3 \\ 1 \end{bmatrix}.$$

**Eigenvalues.** $A - B K$ and $A - L_o C$ both have the characteristic polynomial $s^2 + \sqrt3\, s + 1$, with roots $-\tfrac{\sqrt3}{2} \pm \tfrac{j}{2}$. The closed loop of order 4 has the polynomial $(s^2 + \sqrt3\, s + 1)^2$, as the [separation principle](/separation-principle/) says.

**Controller.** $A_c = A - B K - L_o C = \begin{bmatrix} -\sqrt3 & 1 \\ -2 & -\sqrt3 \end{bmatrix}$, and the controller from $y$ to $-u$ has the transfer function

$$C(s) = K (sI - A_c)^{-1} L_o = \frac{2\sqrt3\, s + 1}{s^2 + 2\sqrt3\, s + 5}.$$

**Cost.** The optimal cost is $J^* = \mathrm{tr}(P W) + \mathrm{tr}(S K^T R K) = 2\sqrt3 + 6\sqrt3 = 8\sqrt3 \approx 13.856$. The first term is the cost with the full state known; the second is the price of the estimate. The stationary covariance of the closed loop, from a Lyapunov equation, gives the same number. Gains near $K$ and $L_o$ give a higher cost.

**Margins.** Put a gain $k$ at the plant input. The closed-loop polynomial is $s^4 + 2\sqrt3\, s^3 + 5 s^2 + 2\sqrt3\, k\, s + k$. The Routh conditions are $k > 0$ and $2\sqrt3\, k (10\sqrt3 - 2\sqrt3\, k) - 12 k = k (48 - 12 k) > 0$, so the loop stays Hurwitz exactly for $0 < k < 4$. The LQG loop $L(s) = C(s)/s^2$ has a phase margin of about 39.0 degrees at $\omega \approx 0.726$ rad/s. The LQR loop $K (sI - A)^{-1} B = (\sqrt3\, s + 1)/s^2$ with the full state keeps every gain $k > 0$ and has a phase margin of about 72.4 degrees. The estimator costs margin. [Loop transfer recovery](/loop-transfer-recovery/) is one way to get it back.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts. The sign function iteration converges to $\mathrm{sign}(H)$, and line L8 returns the stabilizing CARE solution, because the null space of $\mathrm{sign}(H) + I$ is the stable invariant subspace of $H$; Newton steps from the exact solution do not move it. Line L3 returns the stabilizing filter solution, by duality. In the coordinates $(x, x - \hat x)$ the closed-loop matrix is block triangular with diagonal blocks $A - BK$ and $A - L_o C$. Finally, for any causal output feedback, completing the square with the CARE gives

$$J = \mathrm{tr}(P W) + \lim_{T \to \infty} \frac1T \int_0^T \mathbb{E}\,(u + K x)^T R (u + K x)\, dt,$$

and splitting $x = \hat x + e$, with the filter error $e$ orthogonal to every function of the past outputs, gives $J \ge \mathrm{tr}(P W) + \mathrm{tr}(S K^T R K)$ with equality exactly for $u = -K \hat x$.

## Complexity

Each sign function step inverts a $2n \times 2n$ matrix and costs $O(n^3)$. The iteration converges quadratically once the eigenvalues are near $\pm 1$; with determinant scaling, 10 to 30 steps are usual, and more are needed when $H$ has eigenvalues near the imaginary axis, which is the case when the problem is close to losing stabilizability or detectability. Lines L2 and L4 cost $O(n^2 (m + p))$ with $R$ and $V$ factored once. A Kleinman step with a Bartels-Stewart Lyapunov solver costs $O(n^3)$; the code uses the Kronecker form, which costs $O(n^6)$ and is only meant for small $n$. The controller itself costs $O(n^2 + n (m + p))$ per evaluation of its right-hand side.

## Properties

- **Separation.** $K$ does not depend on $C$, $W$ or $V$, and $L_o$ does not depend on $B$, $Q$ or $R$. The closed-loop eigenvalues are those of $A - B K$ together with those of $A - L_o C$.
- **Order.** The controller has the order $n$ of the plant. Lower order controllers that minimize $J$ have no such closed form.
- **Certainty equivalence.** The controller acts on $\hat x$ as LQR acts on $x$. This holds for the linear plant with Gaussian noise and quadratic cost; it fails in general for nonlinear plants or other costs.
- **Same as H2.** With the noise and the weighted outputs put into one generalized plant, $J^*$ is the squared [H2 norm](/h2-norm/) of the closed loop, and the LQG controller is the [H2 optimal controller](/h2-optimal-control/).
- **No guaranteed margins.** LQR with the full state has the gain margin $(1/2, \infty)$ and at least 60 degrees of phase margin ([LQR stability margins](/lqr-stability-margins/)). The LQG loop has no such bounds: Doyle (1978) gave a plant where the gain margin shrinks to 1 as the weights grow.

## Variants and improvements

- **Discrete time.** Use the [DARE](/discrete-algebraic-riccati-equation/) for both gains and the discrete [Kalman filter](/kalman-filter/). The predictor form uses $\hat x_{k|k-1}$; the current estimator form uses $\hat x_{k|k}$ and is the optimal one when the computation delay is short.
- **Finite horizon.** Run the regulator Riccati equation backward from the final time and the filter Riccati equation forward from the initial covariance. The gains then vary in time.
- **Correlated noise and cross terms.** A cross covariance between $w$ and $v$, or a cross term $2 x^T N u$ in the cost, changes the gains to $K = R^{-1}(B^T P + N^T)$ and $L_o = (S C^T + M) V^{-1}$, with modified Riccati equations.
- **Loop transfer recovery.** Make the filter fast with fictitious input noise so that the loop tends to the LQR loop ([LTR](/loop-transfer-recovery/)), or do the dual at the output.
- **Integral action.** Add the integral of the tracking error as a state, or estimate a constant disturbance, so that the loop has zero steady state error; see [integral state feedback](/integral-state-feedback/).
- **Robust synthesis.** When margins matter, use [H-infinity](/h-infinity-control-problem/) design, of which LQG is the limit as the bound $\gamma$ goes to infinity in the central controller.

## When to use it

Use LQG when only some states are measured, the plant is linear near the operating point, and the disturbances and sensor noise can be modeled as white noise with known intensities, possibly after shaping filters. It gives a first controller of full order with one design knob per weight, and it is the base for LTR and for estimators in MPC. Check the margins of every LQG design, at the plant input and at the output. If the plant model is uncertain in a known way, prefer an H-infinity or $\mu$ design. If the inputs or states have hard limits, use the filter with [MPC](/model-predictive-control/) instead of the static gain $K$.

## Pitfalls

- **Assuming LQR margins.** The 60 degree and $(1/2, \infty)$ margins of LQR do not survive the estimator. In the example the upper gain margin drops from infinity to 4. Compute the margins of the actual loop.
- **Breaking the loop at the wrong point.** Margins at the plant input and at the plant output are different for multivariable plants. Check both.
- **Fast filters with poor models.** A large $W$ gives a fast filter that relies on the model. Unmodeled dynamics at high frequencies then reduce robustness.
- **Noise intensities as tuning knobs.** $W$ and $V$ are rarely known. Treat them as design parameters and check the result, not as facts.
- **Ill conditioned Hamiltonians.** When $(A, B)$ is close to losing stabilizability or $(C, A)$ is close to losing detectability, $H$ has eigenvalues near the imaginary axis, the sign iteration is slow, and $P$ or $S$ is large. Scale the problem and check the Riccati residuals.
- **Plant and controller unstable together.** The LQG controller can itself have eigenvalues with positive real part even when the plant is open-loop Hurwitz. The loop is fine as long as the closed loop is Hurwitz, but startup and saturation then need care.

## Implementations

## History

Kalman (1960) solved the linear quadratic regulator, and Kalman and Bucy (1961) gave the continuous-time filter and noted its duality with the regulator. That the optimal stochastic controller is the deterministic regulator acting on the filter estimate was shown by Joseph and Tou (1961) and by Gunckel and Franklin (1963), and in more generality by Wonham (1968). Athans (1971) edited a special issue of IEEE Transactions on Automatic Control on the LQG problem and presented it as a design method. Doyle (1978) then showed with a two-state example that LQG regulators can have arbitrarily small margins, which led to loop transfer recovery (Doyle and Stein 1979, 1981) and to H-infinity control. The matrix sign function for Riccati equations goes back to a 1971 report by Roberts, published in 1980.

## References
