---
tag: D36VQ5
kind: technique
slug: adjoint-model
name: Adjoint model
aliases:
- tangent linear and adjoint models
area: scientific-computing/data-assimilation
level: core
summary: "The transpose of the tangent linear model, run backward in time, gives the gradient of a cost with respect to the initial state for a small multiple of one model run."
prereqs: [data-assimilation-problem, automatic-differentiation]
see_also: [four-dimensional-variational-assimilation, backpropagation, adjoint-sensitivity-analysis, adjoint-state-method, automatic-differentiation, three-dimensional-variational-assimilation, lorenz-96-model, incremental-4d-var]
sources:
  - paper: doi:10.1111/j.1600-0870.1986.tb00459.x
    title: F.-X. Le Dimet and O. Talagrand, Variational algorithms for analysis and assimilation of meteorological observations, theoretical aspects, Tellus A 38(2) (1986) 97-110
    locator: the adjoint equations for the gradient of a cost over a time window
  - paper: doi:10.1002/qj.49711347812
    title: O. Talagrand and P. Courtier, Variational assimilation of meteorological observations with the adjoint vorticity equation. I, Theory, Quarterly Journal of the Royal Meteorological Society 113(478) (1987) 1311-1328
    locator: the adjoint of a discrete model and its use in variational assimilation
  - paper: doi:10.1175/1520-0477(1997)078<2577:WIAAM>2.0.CO;2
    title: R. M. Errico, What is an adjoint model?, Bulletin of the American Meteorological Society 78(11) (1997) 2577-2591
    locator: the tangent linear model, the adjoint model, and their tests
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Section 6.3 (tangent linear model, adjoint model, singular vectors) and Appendix B (coding and checking the tangent linear and the adjoint models)
  - book: isbn:9780898716597
    title: A. Griewank and A. Walther, Evaluating Derivatives, Principles and Techniques of Algorithmic Differentiation, second edition, SIAM, 2008
    locator: the reverse mode, its cost bound, and checkpointing
---

The adjoint model of a forecast model is the transpose of its tangent linear model. The tangent linear model $M'(x)$ tells how a small change of the initial state changes the forecast. Its transpose $M'(x)^\top$, run backward in time along a stored forward trajectory, turns the sensitivity of a cost to the forecast into the sensitivity of the cost to the initial state. So one forward run and one backward adjoint run give the full gradient of a scalar cost with respect to all $n$ initial values, at a cost that is a small multiple of one forward run and does not grow with $n$. Finite differences would need $n + 1$ runs. This is what makes [4D-Var](/four-dimensional-variational-assimilation/) possible for weather models, and it is the same idea as reverse mode [automatic differentiation](/automatic-differentiation/) and [backpropagation](/backpropagation/).

## In plain words

Suppose we want to know how a forecast error at the end of a day depends on each of a million numbers at the start. Changing each start value in turn and running the model again would take a million runs. The adjoint model does it with about the work of a few runs. It first runs the model forward and keeps the states. Then it starts from the end, where it is easy to say how the error depends on the final state, and steps backward. At each step it asks: if this quantity changes, how does that change what comes later? It passes this sensitivity one step back at a time, and adds the effect of the observations it meets on the way. When it reaches the start, it has the sensitivity to every start value at once.

## When it applies

- The output is a single number, such as a cost or a forecast measure, and the inputs are many: the gradient of a scalar function of $n$ variables.
- The function is a composition of steps, $x_k = M_k(x_{k-1})$, each of which is differentiable, and the code of each step is available, so its tangent linear and adjoint can be written by hand or by a tool.
- The forward states can be stored, or recomputed from checkpoints, during the backward sweep.
- The cost is a sum of terms along the trajectory, as in the observation term of a 4D-Var cost.

## The template

For $x_k = M_k(x_{k-1})$, $k = 1, \ldots, K$, and the cost $J(x_0) = \sum_k \tfrac12 (H x_k - y_k)^\top R^{-1}(H x_k - y_k)$ over the times $k$ with observations, the gradient is

$$\nabla J(x_0) = \sum_k M_1'^\top \cdots M_k'^\top H^\top R^{-1}(H x_k - y_k), \qquad M_k' = M_k'(x_{k-1}),$$

which a backward recursion evaluates with one product by each $M_k'^\top$:

```pseudo id=main
GRADIENT(x_0, obs)
L1  run the model forward and store x_0, x_1, ..., x_K
L2  lambda <- 0
L3  for k <- K down to 0 do
L4      if time k has observations then lambda <- lambda + H^T R^-1 (H x_k - y_k)
L5      if k > 0 then lambda <- M_k'(x_{k-1})^T lambda          ▷ one adjoint step
L6  return lambda                                               ▷ = grad J(x_0)
```

The holes are the model step $M_k$, its adjoint step $M_k'^\top$ (line L5), and the forcing of the adjoint by the observations (line L4). After line L4 at time $k$, $\lambda$ is the gradient of the cost terms at times $\ge k$ with respect to $x_k$. Line L5 moves it to $x_{k-1}$ by the chain rule. A background term $\tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b)$ adds $B^{-1}(x_0 - x^b)$ at the end.

**Writing the adjoint step.** The tangent linear code is the derivative of the model code, statement by statement. The adjoint code runs the statements of the tangent linear code in the reverse order and replaces each one by its transpose. For a statement $\delta z = a\,\delta u + b\,\delta v$ the adjoint is $\bar u \mathrel{+}= a\,\bar z$, $\bar v \mathrel{+}= b\,\bar z$, $\bar z = 0$. The reference code does this for one Runge-Kutta step of the [Lorenz-96 model](/lorenz-96-model/).

**Checks.** Two tests catch almost every error (Errico 1997; Kalnay 2003, Appendix B).

1. *Tangent linear test.* $(M(x + \epsilon\,\delta x) - M(x - \epsilon\,\delta x))/(2\epsilon) - M'(x)\delta x$ must fall like $\epsilon^2$.
2. *Dot product test.* $\langle M'(x)\delta x, \lambda \rangle = \langle \delta x, M'(x)^\top \lambda \rangle$ must hold to rounding error for random $\delta x$ and $\lambda$. In the reference code it holds to $10^{-10}$ relative for 20 steps of Lorenz-96 with 40 variables.

**Worked example.** Take the scalar model $x_k = x_{k-1}^2$, $K = 2$, $x_0 = 2$ and one observation $y_2 = 15$ at the last time with $H = R = 1$. Then $J(x_0) = \tfrac12 (x_0^4 - 15)^2$ and $J'(2) = (16 - 15)\cdot 4 \cdot 2^3 = 32$. The adjoint step is multiplication by $M'(x_{k-1}) = 2x_{k-1}$.

| $k$ | $x_k$ (forward) | after line L4 | after line L5 |
|---|---|---|---|
| 2 | 16 | $\lambda = 16 - 15 = 1$ | $\lambda = 2 x_1 \cdot 1 = 8$ |
| 1 | 4 | $\lambda = 8$ (no observation) | $\lambda = 2 x_0 \cdot 8 = 32$ |
| 0 | 2 | $\lambda = 32$ (no observation) | returned |

The result $32$ is $J'(2)$.

**Cost.** One adjoint step costs a small multiple of one forward step, independent of $n$ (the cheap gradient principle of reverse mode differentiation, Griewank and Walther 2008). For the Lorenz-96 code here, with $n = 40$ and $K = 200$ steps, the gradient took about 4 times as long as one forward run, including the forward sweep (a measurement). The memory is the stored trajectory, $\Theta(nK)$, unless checkpointing trades it for recomputation.

## Classic examples

- **[4D-Var](/four-dimensional-variational-assimilation/).** The gradient of the 4D-Var cost with respect to the initial state is exactly the template, and the minimizer calls it once per iteration. [Incremental 4D-Var](/incremental-4d-var/) uses the tangent linear model in the inner loop and its adjoint for the gradient.
- **[3D-Var](/three-dimensional-variational-assimilation/).** The gradient needs $H^\top$, the adjoint of the observation operator, for example of a radiative transfer model. This is the case $K = 0$ of the template.
- **[Backpropagation](/backpropagation/).** The layers of a neural network are the steps $M_k$, the loss is the cost, and the backward pass is the adjoint sweep.
- **[Adjoint sensitivity analysis](/adjoint-sensitivity-analysis/) and the [adjoint state method](/adjoint-state-method/).** The gradient of a scalar output of an ODE or PDE model with respect to many parameters or initial values, used in optimal control, shape optimization and seismic imaging.
- **[Automatic differentiation](/automatic-differentiation/).** Reverse mode applied to any program gives the adjoint automatically. Tools of this kind now produce many of the adjoint models in use.

## Variations

- **Discrete or continuous adjoint.** The discrete adjoint is the exact transpose of the code, so its gradient is exact for the discrete cost and passes the dot product test. The continuous adjoint discretizes the adjoint differential equation separately, and its gradient is only an approximation of the gradient of the discrete cost.
- **Checkpointing.** Store the state only at some steps and recompute the others during the backward sweep. With logarithmic checkpointing the memory is $\Theta(n \log K)$ for $\Theta(K \log K)$ forward steps (Griewank and Walther 2008).
- **Singular vectors.** The leading eigenvectors of $M'^\top M'$, found with alternate runs of the tangent linear and adjoint models, are the perturbations that grow fastest over a time window, used to start ensemble forecasts (Kalnay 2003, Section 6.3).
- **Sensitivity to observations.** The adjoint of the whole assimilation system gives the effect of each observation on a forecast measure.
- **Simplified tangent linear models.** Operational systems often use a tangent linear model of a simplified or lower resolution model. Its adjoint must then be the transpose of that simplified model, not of the full one.

## Pitfalls

- **Wrong order in the backward sweep.** In the template the observation term at time $k$ is added (line L4) before $\lambda$ is moved to time $k - 1$ (line L5). Swapping the two lines attaches each observation to the wrong time.
- **Not the exact transpose.** A small slip, such as a wrong index in one statement, gives a gradient that is wrong but plausible, and the minimizer then stalls or converges to a wrong point. Always run the dot product test, step by step and for the full window.
- **Linearizing about the wrong state.** The adjoint step at time $k$ must use the forward state $x_{k-1}$ that the forward run produced, including the intermediate stages of the time step. Using the state at the end of the step, or a state from another run, gives the wrong Jacobian.
- **Switches and thresholds.** Physical parameterizations with `if` statements, such as the onset of convection, are not differentiable at the threshold. The tangent linear model can then be a poor approximation of finite differences, even if the adjoint is the exact transpose of the code.
- **Long windows in a chaotic model.** The tangent linear model describes small perturbations only for a limited time: in Lorenz-96 small errors double in about 0.42 time units. Over long windows the cost has many local minima, and the gradient from the adjoint, although exact, is of little use for a global search.

## Exercises

1. For the scalar model $x_k = a x_{k-1}$ and observations $y_1, \ldots, y_K$ of every $x_k$ with $R = 1$, write the adjoint recursion and check that it gives $\nabla J = \sum_k a^k(a^k x_0 - y_k)$.
2. Write the tangent linear and adjoint statements of $z = u\,v$, and check the dot product test by hand at $u = 2$, $v = 3$ for $(\delta u, \delta v) = (1, 1)$ and $\bar z = 1$.
3. Show that the dot product test with random vectors detects an error in a single entry of $M'^\top$ with probability 1.

## References
