---
tag: 2GGXNP
kind: algorithm
slug: weak-constraint-4d-var
name: Weak-constraint 4D-Var
area: scientific-computing/data-assimilation
level: advanced
summary: Allows model error terms at each time in the window, penalized by their covariance, so the analysis need not follow the model exactly.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, K: the number of model steps in the window, p: the total number of observations, k: the number of outer loops, m: the number of conjugate gradient steps per outer loop, c: the cost of one full model step, s: the cost of one tangent linear or adjoint step}
  time: {worst: "Θ(K n^3 + k (K c + m (K s + K n^2 + n p)))"}
  space: {extra: "Θ(K n^2)"}
properties: {deterministic: true, control_variable: the initial state and the model error at every step, exact_for_linear_model: "one outer loop gives the Kalman smoother mean with model error covariance Q", strong_constraint_limit: Q tends to zero, outer_loop: Gauss-Newton}
history:
  year: 2006
  people: [Yannick Trémolet]
  note: Sasaki named strong and weak constraints in variational analysis in 1970, Bennett developed the weak-constraint problem for the ocean, and Trémolet studied its forms for the ECMWF 4D-Var system in 2006 and 2007.
prereqs: [four-dimensional-variational-assimilation, gauss-newton-algorithm]
see_also: [incremental-4d-var, representer-method, rauch-tung-striebel-smoother, kalman-filter, ensemble-kalman-smoother, adjoint-model, conjugate-gradient-method, lorenz-96-model]
sources:
  - paper: doi:10.1175/1520-0493(1970)098<0875:SBFINV>2.3.CO;2
    title: Y. Sasaki, Some basic formalisms in numerical variational analysis, Monthly Weather Review 98(12) (1970) 875-883
    locator: the formalisms with strong and with weak constraint
  - paper: doi:10.1256/qj.05.224
    title: Y. Trémolet, Accounting for an imperfect model in 4D-Var, Quarterly Journal of the Royal Meteorological Society 132(621) (2006) 2483-2504
    locator: the model error forcing, state and bias formulations of weak-constraint 4D-Var
  - paper: doi:10.1002/qj.94
    title: Y. Trémolet, Model-error estimation in 4D-Var, Quarterly Journal of the Royal Meteorological Society 133 (2007) 1267-1280
    locator: the estimation of model error in the ECMWF system and the specification of Q
  - book: isbn:9780521813730
    title: Andrew F. Bennett, Inverse Modeling of the Ocean and Atmosphere, Cambridge University Press, 2002
    locator: the weak-constraint least squares problem and its solution by representers
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Weak-constraint 4D-Var removes the assumption of [4D-Var](/four-dimensional-variational-assimilation/) that the model is perfect. It adds a model error term $\eta_k$ to every step of the window, $x_k = M_k(x_{k-1}) + \eta_k$, and minimizes a cost over the initial state and all the model errors together, with a penalty $\tfrac12 \eta_k^\top Q_k^{-1} \eta_k$ for each step. The analysis can then leave the model trajectory where the observations ask for it, by an amount that the model error covariance $Q_k$ controls. For a linear model and Gaussian errors the minimizer is the mean of the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) with process noise $Q_k$, so weak-constraint 4D-Var is the variational form of the full Kalman smoother. As all $Q_k$ tend to zero it becomes strong-constraint 4D-Var.

## In plain words

Ordinary 4D-Var trusts the weather model completely: the answer must be an exact run of the model, and only the start state can change. But every model has errors. Weak-constraint 4D-Var lets the answer move away from the model at each time step by a small push. Each push costs something, and pushes that the model is known to need are cheap, while others are expensive. The method finds the start state and all the pushes that together give the best balance between the background, the model and the measurements. The price is a much larger search, because there is now one unknown state for every time step instead of one in total.

## The problem

**Input.** A background $x^b$ with error covariance $B$, model steps $M_k$ with their tangent linear and adjoint models, model error covariances $Q_k$ for $k = 1, \ldots, K$, and observations $y_k$ with operators $H_k$ and error covariances $R_k$ at the times $k \in T$ of the window $0, \ldots, K$. Notation of Ide, Courtier, Ghil and Lorenc (1997).

**Output.** The control $z = (x_0, \eta_1, \ldots, \eta_K)$ that minimizes

$$J(z) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k=1}^K \tfrac12 \eta_k^\top Q_k^{-1}\eta_k + \sum_{k \in T} \tfrac12 d_k^\top R_k^{-1} d_k, \qquad d_k = y_k - H_k x_k,$$

with $x_k = M_k(x_{k-1}) + \eta_k$, and the trajectory $x_0, \ldots, x_K$ of that control. This is the model error forcing form. Trémolet (2006) also describes the state form, with the states $x_0, \ldots, x_K$ as the control, and a form in which a constant bias is the control.

## The algorithm

```pseudo id=main
WEAK-4DVAR(x^b, B, {Q_k}, {y_k, H_k, R_k}, M, M', M'^T)
L1  x_0 <- x^b ; eta_k <- 0 for k = 1..K
L2  for outer <- 1 to max_outer do
L3      x_k <- M_k(x_(k-1)) + eta_k for k = 1..K
L4      d_k <- y_k - H_k x_k for k in T
L5      mu_k <- sensitivity to x_k from one adjoint run forced by -H_k^T R_k^-1 d_k
        g <- (B^-1 (x_0 - x^b) + mu_0, Q_1^-1 eta_1 + mu_1, ..., Q_K^-1 eta_K + mu_K)
L6      A v = D v + G^T H^T R^-1 H G v   ▷ one tangent linear run and one adjoint run
L7      dz <- solve A dz = -g by conjugate gradients
L8      (x_0, eta) <- (x_0, eta) + dz
L9      if |dz| <= tol (1 + |z|) then break
L10 return x_0, ..., x_K
```

Line L5 is the same backward sweep as in 4D-Var, but the gradient now has a part for every step: the sensitivity $\mu_k$ to the state at time $k$ is also the sensitivity to the model error $\eta_k$, because $\eta_k$ adds to $x_k$ directly. In line L6, $G$ maps an increment $(\delta x_0, \delta\eta_1, \ldots, \delta\eta_K)$ to the trajectory increments $\delta x_k = M_k' \delta x_{k-1} + \delta\eta_k$, and $D$ is the block diagonal matrix of $B^{-1}$ and the $Q_k^{-1}$. Each outer loop is a Gauss-Newton step, as in [incremental 4D-Var](/incremental-4d-var/), with a control $K + 1$ times larger.

## Example

**One step.** Take $x_1 = x_0 + \eta_1$ ($K = 1$), $x^b = 0$, $B = Q_1 = 1$, and one observation $y_1 = 3$ with $H = R = 1$. The cost is

$$J(x_0, \eta_1) = \tfrac12 x_0^2 + \tfrac12 \eta_1^2 + \tfrac12 (3 - x_0 - \eta_1)^2 .$$

Both partial derivatives are zero when $x_0 = \eta_1 = 3 - x_0 - \eta_1$, so $x_0 = \eta_1 = 1$ and $x_1 = 2$. The misfit of 2 between background and observation is shared equally between the initial state and the model error, because $B = Q_1$. As a check, the prior variance of $x_1$ is $B + Q_1 = 2$, so the Kalman filter gives $x_1 = 2 \cdot 3 / (2 + 1) = 2$. With strong constraint ($\eta_1 = 0$) the cost is $\tfrac12 x_0^2 + \tfrac12 (3 - x_0)^2$, with the minimizer $x_0 = x_1 = 1.5$: the analysis at time 1 is pulled less towards the observation, because the prior variance of $x_1$ is only $B = 1$.

**A model with a missing forcing.** In a twin test with the Lorenz-63 model, 40 forward Euler steps with $\Delta t = 0.01$, the truth has a forcing of $0.05$ per step on the third component that the model does not have. All three components are observed every 4 steps with error standard deviation 0.2, and $B = I$. Over six seeds the mean error of the analysis at the end of the window is 0.20 for weak-constraint 4D-Var with $Q_k = 0.01 I$ and 0.73 for strong constraint, with 6 to 8 and 8 to 9 outer loops (a measurement). The strong-constraint analysis must fit the drift of the truth with the initial state alone, and the error grows towards the end of the window.

## Correctness

The [proof](proofs/correctness.md) shows that the backward sweep gives the exact gradient over $x_0$ and every $\eta_k$, that the inner matrix $A$ is symmetric positive definite, and that each outer loop is a Gauss-Newton step (a theorem). For a linear model one outer loop gives the minimizer, and the prior times the likelihood of the control is proportional to $e^{-J}$, so the trajectory of the minimizer is $E[x_k \mid y]$ at every time, the Rauch-Tung-Striebel smoother mean with model error $Q_k$ (a theorem). The tests check this to $10^{-8}$ against a separate Kalman filter and smoother on random problems, the gradient against finite differences on Lorenz-63, the approach to strong constraint as $Q \to 0$, and the stationarity of the nonlinear result.

## Complexity

The control has $n(K + 1)$ entries instead of $n$. An outer loop costs one full model run, $Kc$, and each conjugate gradient step one tangent linear and one adjoint run, $Ks$, plus solves with the factors of $B$ and the $Q_k$, $\Theta(Kn^2)$ with dense covariances, and the observation terms, $\Theta(np)$. With $k$ outer loops of $m$ inner steps the time is $\Theta(Kn^3 + k(Kc + m(Ks + Kn^2 + np)))$, where $Kn^3$ is the Cholesky factorization of $B$ and every $Q_k$. The memory is $\Theta(Kn^2)$ for the dense factors of the $Q_k$; with a single $Q$ for all steps, or with an operator for $Q$, it is the $\Theta(Kn)$ of the trajectory and the control. The inner problem is also harder to precondition than in strong constraint, so $m$ is larger in practice.

## Properties

- **Kalman smoother with model error.** For a linear model and Gaussian errors, the minimizer is the smoother mean with process noise $Q_k$ (a theorem). Strong-constraint 4D-Var is the case $Q_k = 0$.
- **Continuous in $Q$.** As $Q_k \to 0$ the minimizer tends to the strong-constraint minimizer (a theorem for the linear case; the tests check it with $Q = 10^{-9}$ times a positive definite matrix).
- **The window can be longer.** Strong-constraint 4D-Var needs a window short enough that the model is nearly perfect over it; the model error terms relax this.
- **The answer depends on $Q$.** A $Q$ that is too large lets the analysis follow the observation noise, and a $Q$ that is too small gives strong constraint back. $Q$ is harder to estimate than $B$ (a heuristic that Trémolet 2007 discusses).
- **Parallel in time.** In the state form the model runs over the subwindows are independent, so they can run in parallel.

## Variants and improvements

- **State form.** Use the states at the start of each subwindow as the control, and penalize the jumps between the model run from one and the next. This is the form that allows parallel subwindows (Trémolet 2006).
- **Bias form.** Use one constant model error $\eta$ for the whole window, with a small control. It suits systematic model errors.
- **Representer method.** Solve the linear problem exactly in observation space, with one unknown per observation, using representer functions. This is the [representer method](/representer-method/) of Bennett, the dual of this algorithm.
- **Ensemble estimates of $Q$.** Estimate the model error covariance from differences between model versions or from ensemble statistics, as [ensemble Kalman smoothers](/ensemble-kalman-smoother/) do with inflation.

## When to use it

Use weak-constraint 4D-Var when the model error over the window is not small next to the background error: long windows, models with known systematic errors, and ocean and atmospheric chemistry problems with weakly known forcing. If the model is good over a short window, strong-constraint 4D-Var is cheaper and has fewer parameters to tune. If no model error covariance can be estimated, start with the bias form.

## Pitfalls

- **A gradient that ignores the model error (line L5).** The gradient over $\eta_k$ is $Q_k^{-1}\eta_k + \mu_k$, with $\mu_k$ the adjoint variable after the forcing at time $k$. Taking it before the forcing at time $k$ drops the observation at that time.
- **A badly chosen $Q$.** The answer depends strongly on $Q$; check it with innovation statistics, as in [Desroziers diagnostics](/desroziers-diagnostics/).
- **Poor conditioning (line L7).** The inner problem has $n(K + 1)$ unknowns and couples them along the window, so the conjugate gradient method needs a preconditioner, such as a control variable transform with $B^{1/2}$ and $Q_k^{1/2}$.
- **Memory.** Storing a dense $Q_k$ for every step is not possible for a large model; use one $Q$ for all steps or an operator form.
- **An unobserved error.** Model error and initial state error can have the same effect on the observations, and then only $B$ and $Q$ decide how the misfit is split, as in the example.

## Implementations

## History

Sasaki (1970) distinguished strong and weak constraints in variational analysis, depending on whether the dynamics must hold exactly or only approximately. Bennett developed the weak-constraint problem for ocean models in the 1980s and 1990s and solved it with representers (Bennett 1992 and 2002). Trémolet (2006) compared the forcing, state and bias formulations for the ECMWF 4D-Var system and studied the estimation of model error in 2007.

## References
