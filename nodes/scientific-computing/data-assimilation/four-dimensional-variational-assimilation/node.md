---
tag: XB7N6C
kind: algorithm
slug: four-dimensional-variational-assimilation
name: Four-dimensional variational assimilation
aliases:
- 4D-Var
- strong-constraint 4D-Var
area: scientific-computing/data-assimilation
level: core
summary: Finds the initial state whose model trajectory best fits the background and the observations over a time window, with gradients from the adjoint model.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, K: the number of model steps in the window, p: the total number of observations, I: the number of minimizer iterations, c: the cost of one model step}
  time: {worst: "Θ(n^3 + I (K c + n^2 + n p))"}
  space: {extra: "Θ(K n + n^2)"}
properties: {deterministic: true, gradient: one forward run and one adjoint run, equals_kalman_smoother: "for a linear model, a linear H and Q = 0", model_constraint: perfect model, minimizer: BFGS with a line search}
history:
  year: 1986
  people: [François-Xavier Le Dimet, Olivier Talagrand, Philippe Courtier]
  note: Le Dimet and Talagrand gave the adjoint method for variational assimilation over a time window in 1986, and ECMWF made 4D-Var its operational analysis on 25 November 1997.
prereqs: [three-dimensional-variational-assimilation, adjoint-model]
see_also: [incremental-4d-var, weak-constraint-4d-var, representer-method, four-dimensional-ensemble-variational, kalman-filter, rauch-tung-striebel-smoother, bfgs, lorenz-96-model]
sources:
  - paper: doi:10.1111/j.1600-0870.1986.tb00459.x
    title: F.-X. Le Dimet and O. Talagrand, Variational algorithms for analysis and assimilation of meteorological observations, theoretical aspects, Tellus A 38(2) (1986) 97-110
    locator: the variational problem over a time window and the adjoint equations for its gradient
  - paper: doi:10.1002/qj.49711347812
    title: O. Talagrand and P. Courtier, Variational assimilation of meteorological observations with the adjoint vorticity equation. I, Theory, Quarterly Journal of the Royal Meteorological Society 113(478) (1987) 1311-1328
    locator: the adjoint of the discrete model and the gradient of the cost
  - paper: doi:10.1002/qj.49711347813
    title: P. Courtier and O. Talagrand, Variational assimilation of meteorological observations with the adjoint vorticity equation. II, Numerical results, Quarterly Journal of the Royal Meteorological Society 113(478) (1987) 1329-1347
    locator: numerical experiments with a barotropic vorticity model
  - paper: doi:10.1002/qj.49712656415
    title: F. Rabier, H. Järvinen, E. Klinker, J.-F. Mahfouf and A. Simmons, The ECMWF operational implementation of four-dimensional variational assimilation. I, Experimental results with simplified physics, Quarterly Journal of the Royal Meteorological Society 126(564) (2000) 1143-1170
    locator: the operational ECMWF 4D-Var and its comparison with 3D-Var
  - paper: doi:10.1002/qj.49712051912
    title: P. Courtier, J.-N. Thépaut and A. Hollingsworth, A strategy for operational implementation of 4D-Var, using an incremental approach, Quarterly Journal of the Royal Meteorological Society 120(519) (1994) 1367-1387
    locator: the incremental form with outer and inner loops
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Section 5.6 (methods with an evolving forecast error covariance, 4D-Var and the Kalman filter)
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Four-dimensional variational assimilation (4D-Var) finds the initial state $x_0$ of an assimilation window whose model trajectory $x_k = M_{0 \to k}(x_0)$ best fits a background $x^b$ at the start and all the observations $y_k$ made at their own times $k$ during the window. The fit is measured by a cost function with the same two terms as in [3D-Var](/three-dimensional-variational-assimilation/), the departure from the background weighted by $B^{-1}$ and the departures from the observations weighted by $R_k^{-1}$, but the observation term is a sum over the window and the model links the times. The model is a strong constraint: the analysis is an exact model trajectory. The gradient of the cost with respect to all $n$ components of $x_0$ comes from one forward run of the model and one backward run of its [adjoint](/adjoint-model/), and a quasi-Newton or conjugate gradient method minimizes the cost. For a linear model and Gaussian errors the result is the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) estimate, and at the end of the window it is the [Kalman filter](/kalman-filter/) estimate, without ever forming a covariance matrix of the size of the state.

## In plain words

A weather center has a forecast for the start of a six or twelve hour period and many measurements taken at different moments during that period. It wants the start state from which the model, run forward, passes as close as possible to all the measurements at their own times, while it stays near the old forecast at the start. Each start state gets a score: how far it is from the old forecast, plus how far its model run is from each measurement. The method runs the model forward to compute the score, then runs a special backward model that tells, for every start value, which way to change it to lower the score. It takes a step in that direction and repeats until the score stops falling.

## The problem

**Input.** A background $x^b \in \mathbb R^n$ for time $0$ with error covariance $B$; model steps $x_k = M_k(x_{k-1})$ for $k = 1, \ldots, K$, with their adjoint steps $M_k'(x)^\top$; and for each time $k$ of a set $T \subseteq \{0, \ldots, K\}$, observations $y_k$ with an operator $H_k$ and an error covariance $R_k$. The total number of observations is $p$. The notation is that of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $M$ is its $A$, $H_k$ is its $C$, and $x^b$ and $B$ are its predicted mean and covariance at time $0$.

**Output.** A minimizer, or for a nonlinear model a stationary point, of

$$J(x_0) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k \in T} \tfrac12 \big(y_k - H_k x_k\big)^\top R_k^{-1}\big(y_k - H_k x_k\big), \qquad x_k = M_{0 \to k}(x_0).$$

The reference code uses linear operators $H_k$. A nonlinear $h_k$ replaces $H_k x_k$ by $h_k(x_k)$ and $H_k^\top$ by the adjoint of its Jacobian. The analysis trajectory is $x_k^a = M_{0 \to k}(x_0^a)$, and its last state is the start of the next forecast.

## The algorithm

```pseudo id=main
4DVAR(x^b, B, {y_k, H_k, R_k}, M, M'^T)
L1  x_0 <- x^b
L2  for iter <- 1 to max_iter do
L3      run the model from x_0 and store x_1, ..., x_K
L4      J <- 1/2 |x_0 - x^b|^2_(B^-1) + sum_k 1/2 |d_k|^2_(R_k^-1),  d_k = y_k - H_k x_k
L5      lambda <- 0
L6      for k <- K down to 0 do
L7          if k in T then lambda <- lambda - H_k^T R_k^-1 d_k           ▷ observation forcing
L8          if k > 0 then lambda <- M_k'(x_(k-1))^T lambda              ▷ one adjoint step
L9      g <- B^-1 (x_0 - x^b) + lambda                                 ▷ = grad J(x_0)
L10     if |g| <= tol then break
L11     x_0 <- x_0 + alpha p, p from BFGS, alpha from a line search on J
L12 return x_0
```

Lines L3 to L9 are one evaluation of the cost and its gradient. The backward loop is the template of the [adjoint model](/adjoint-model/) page, with the sign of the observation forcing written for departures $d_k = y_k - H_k x_k$. Line L11 is a quasi-Newton step. The reference code uses BFGS, started with $B$ as the inverse Hessian, which is the inverse Hessian of the background term, and an Armijo backtracking line search; each trial point of the line search costs one more evaluation of lines L3 to L9. Operational systems use limited memory quasi-Newton or conjugate gradient methods inside the incremental form (see [incremental 4D-Var](/incremental-4d-var/)), and they minimize over a [control variable](/control-variable-transform/) $v$ with $x_0 - x^b = Uv$ instead of applying $B^{-1}$.

## Example

**A scalar window.** Take $x_1 = 2x_0$ ($K = 1$), $x^b = 0$, $B = 1$, and one observation $y_1 = 2$ with $H_1 = R_1 = 1$. Then

$$J(x_0) = \tfrac12 x_0^2 + \tfrac12 (2 - 2x_0)^2, \qquad J'(x_0) = 5x_0 - 4 .$$

At $x_0 = 0$ the code gives $x_1 = 0$, $d_1 = 2$, $J = 2$. Line L7 at $k = 1$ gives $\lambda = -2$, line L8 gives $\lambda = 2 \cdot (-2) = -4$, and line L9 gives $g = 0 + (-4) = J'(0)$. The minimizer is $x_0^a = 0.8$, so $x_1^a = 1.6$.

Check with the Kalman filter: the forecast at time 1 has mean $0$ and variance $2 \cdot 1 \cdot 2 = 4$, the gain is $4/(4 + 1) = 0.8$, and the filter mean is $0.8 \cdot 2 = 1.6 = x_1^a$. The smoother gain is $1 \cdot 2 / 4 = 0.5$, and the smoothed mean at time 0 is $0.5 \cdot 1.6 = 0.8 = x_0^a$.

**Lorenz-63 twin experiments.** With forward Euler steps of $\Delta t = 0.01$ on the Lorenz-63 system, a window of $K = 40$ steps, all three variables observed every 8 steps with error standard deviation $0.5$, $B = I$, and a background error drawn from $N(0, I)$, the reference code converges in 9 to 11 BFGS iterations. Over 8 seeds the mean error of $x_0$ falls from 1.55 for the background to 0.41 for the analysis, and the mean error at the end of the window from 1.60 to 0.31 (a measurement).

## Correctness

The [proof](proofs/correctness.md) shows by induction over the backward loop that line L9 returns the exact gradient of $J$, so every BFGS direction is a descent direction. For a linear model, linear $H_k$ and Gaussian errors, $J(x_0)$ is, up to a constant, the negative logarithm of the posterior density of $x_0$ given all the observations of the window, so the minimizer is the posterior mean (a theorem). Run forward, it is the smoother mean at every time of the window, and at the last time the Kalman filter mean with the same $B$ at the start. The tests check this to $10^{-8}$ against a separate Kalman filter and smoother, check the gradient against finite differences, and check the adjoint with the dot product test to $10^{-10}$. For a nonlinear model, 4D-Var finds a stationary point, which need not be the global minimum.

## Complexity

One evaluation of $J$ and $\nabla J$ costs one forward run, $K$ model steps, plus one adjoint run, whose steps cost a small multiple of a model step each (the cheap gradient principle of reverse mode differentiation). The observation terms cost $\Theta(np)$ with dense $H_k$. The reference code factors $B$ and the $R_k$ once and keeps a dense $n \times n$ BFGS matrix, so $I$ iterations cost $\Theta(n^3 + I(Kc + n^2 + np))$, with a few extra cost evaluations when the line search backtracks. The memory is the stored trajectory, $\Theta(Kn)$, which checkpointing can reduce. For a weather model with $n$ near $10^8$ or more, the dense matrix is replaced by limited memory updates in $\Theta(n)$ memory, and the work is dominated by the forward and adjoint runs: the cost of 4D-Var is roughly the number of iterations times two or three model runs over the window (a rule of thumb).

## Properties

- **Flow-dependent increments.** The effective covariance of the analysis at time $k$ is propagated by the model through the window, so a single observation spreads along the flow of the day even with a static $B$.
- **Same result as the smoother for linear models.** With a linear model, linear $H_k$ and no model error, 4D-Var and the Kalman smoother give the same estimates (a theorem), but 4D-Var never forms or stores an $n \times n$ covariance matrix.
- **Strong constraint.** The analysis is an exact model trajectory. Model error is ignored, which limits the useful length of the window. [Weak-constraint 4D-Var](/weak-constraint-4d-var/) adds model error terms.
- **Observations at their own times.** Each observation is compared with the model at the time it was taken, which suits satellite and aircraft data spread through the window.
- **No analysis covariance.** The method returns the estimate only. The analysis error covariance is the inverse Hessian, which is not computed; the next window starts from the static $B$ again.

## Variants and improvements

- **Incremental 4D-Var.** Minimize a sequence of quadratic costs for an increment with the tangent linear model, at a lower resolution, inside outer loops with the full model. This is the form of all operational systems (Courtier, Thépaut and Hollingsworth 1994; see [incremental 4D-Var](/incremental-4d-var/)).
- **Weak-constraint 4D-Var.** Add model error terms with covariance $Q$ to the cost (see [weak-constraint 4D-Var](/weak-constraint-4d-var/)). Its dual, observation space form is the [representer method](/representer-method/).
- **4DEnVar.** Replace the tangent linear and adjoint models by an ensemble of trajectories over the window (see [four-dimensional ensemble-variational assimilation](/four-dimensional-ensemble-variational/)).
- **Hybrid 4D-Var.** Replace $B$ by a weighted sum of the static covariance and a localized ensemble covariance (see [hybrid ensemble-variational assimilation](/hybrid-ensemble-variational/)).
- **Long windows and quasi-static minimization.** For a chaotic model, lengthen the window step by step and start each minimization from the previous solution, which avoids some of the local minima of a long window.

## When to use it

Use 4D-Var when the observations are spread in time, when the model is good enough to be a strong constraint over the window, and when a tangent linear and adjoint model can be written and maintained. It gives a dynamically consistent analysis and uses the model to spread information from the observations, which an analysis at one time cannot do. If an adjoint is not available, use an ensemble method or [4DEnVar](/four-dimensional-ensemble-variational/). If the model error over the window is comparable to the observation error, use the weak-constraint form.

## Pitfalls

- **A wrong adjoint (line L8).** A gradient that is wrong but close makes the minimizer stall or stop at a wrong point. Run the dot product test for each step and for the whole window, and compare the gradient with finite differences.
- **The order of forcing and adjoint step (lines L7 and L8).** The observation at time $k$ must enter $\lambda$ before the adjoint step to time $k - 1$. The other order attaches each observation to the wrong time.
- **Departures at the wrong state (line L4).** The departures must use the trajectory of the current $x_0$, not of the background.
- **A long window in a chaotic model.** The cost becomes very rough as the window grows, with many local minima, and the tangent linear approximation behind the incremental form breaks down. Windows of 6 to 12 hours are usual for global weather models.
- **Ignoring model error.** With a strong constraint, systematic model errors are pushed into $x_0$, and the analysis can fit the observations by an unrealistic initial state.
- **Badly conditioned minimization (line L11).** Without a good preconditioner, such as $B$ in the BFGS start or the control variable transform, the number of iterations grows with the condition number of the Hessian.

## Implementations

## History

Variational methods with a dynamical constraint go back to Sasaki in the late 1950s and 1970. Le Dimet and Talagrand in 1986 posed assimilation over a time window as an optimal control problem and computed the gradient with the adjoint equations, and Talagrand and Courtier in 1987 applied the adjoint of a discrete vorticity model, with numerical results in the companion paper of Courtier and Talagrand. Lewis and Derber had used an adjoint method for the same kind of problem in 1985. The cost of the full method for a weather model was too high until Courtier, Thépaut and Hollingsworth proposed the incremental form in 1994. ECMWF began operational 4D-Var on 25 November 1997 (Rabier et al. 2000), and Météo-France, the UK Met Office, the Japan Meteorological Agency and Environment Canada followed in the next decade.

## References
