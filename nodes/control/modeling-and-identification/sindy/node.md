---
tag: 5WMZP5
kind: algorithm
slug: sindy
name: Sparse identification of nonlinear dynamics
aliases:
- SINDy
area: control/modeling-and-identification
level: research
summary: Finds the few terms of a library of candidate functions that explain the measured derivatives, by sparse regression.
solves: [system-identification]
model: real-ram
complexity:
  vars: {n: the number of states, M: the number of samples, p: the number of library functions}
  time: {worst: O(n M p^3)}
  space: {extra: O(M p)}
properties: {deterministic: true, online: false, exact: true, iterative: true}
history:
  year: 2016
  people: [Steven L. Brunton, Joshua L. Proctor, J. Nathan Kutz]
  note: "Brunton, Proctor and Kutz introduced SINDy with sequentially thresholded least squares in the Proceedings of the National Academy of Sciences in 2016."
prereqs: [least-squares-problem, qr-decomposition, ode-initial-value-problem]
see_also: [dynamic-mode-decomposition, lasso-regression, orthogonal-matching-pursuit, compressed-sensing, system-identification, runge-kutta-methods, akaike-information-criterion, hammerstein-wiener-model]
sources:
  - paper: doi:10.1073/pnas.1517384113
    title: "Steven L. Brunton, Joshua L. Proctor and J. Nathan Kutz, Discovering governing equations from data by sparse identification of nonlinear dynamical systems, Proceedings of the National Academy of Sciences 113(15), 3932-3937, 2016"
    locator: the library of candidate functions, the sequentially thresholded least squares algorithm, and the Lorenz system example
  - paper: doi:10.1137/18m1189828
    title: "Linan Zhang and Hayden Schaeffer, On the convergence of the SINDy algorithm, Multiscale Modeling and Simulation 17(3), 948-972, 2019"
    locator: the proof that the algorithm approximates local minimizers of a least squares problem with an l0 penalty, and the conditions for convergence and one-step recovery
---

SINDy (sparse identification of nonlinear dynamics) finds the equations $\dot x = f(x)$ of a nonlinear system from samples of the state and its derivative. It assumes that each component of $f$ is a sum of a few terms from a library of candidate functions, for example all monomials of degree at most 2. It writes the derivatives as a linear combination of the library, $\dot x \approx \Xi^T \theta(x)$, and finds a sparse coefficient matrix $\Xi$ by sequentially thresholded least squares: fit, set the small coefficients to zero, fit again on the rest, and repeat. The result is a short equation that a person can read. SINDy differs from [dynamic mode decomposition](/dynamic-mode-decomposition/), which fits a linear map between snapshots and returns eigenvalues and modes, and from black-box nonlinear models such as neural networks, which fit $f$ well but do not give a short formula.

## In plain words

Measure the state of a system and how fast each component changes. Make a long list of guesses for the terms that could appear in the equations: a constant, each variable, each product of two variables, and so on. Fit the measured rates of change with all guesses at once by least squares. Most guesses get a small coefficient that only fits the noise. Remove every term whose coefficient is smaller than a threshold, and fit again with the terms that are left. Repeat until no term is removed. What is left is a short equation with only the important terms.

## The problem

**Input.** Samples $x(t_0), \ldots, x(t_{M-1}) \in \mathbb{R}^n$ of the state, the derivatives $\dot x(t_i)$ (measured, or estimated from the samples), a library $\theta(x) = (\theta_1(x), \ldots, \theta_p(x))$ of candidate functions, and a threshold $\lambda > 0$.

**Output.** A $p \times n$ coefficient matrix $\Xi$ with few nonzero entries, such that $\dot x \approx \Xi^T \theta(x)$ at the samples. Column $j$ gives the equation for $\dot x_j$.

**Notation.** $\Theta$ is the $M \times p$ matrix with $\Theta_{ik} = \theta_k(x(t_i))$. For a set $S$ of library indices, $\Theta_S$ is the matrix of the columns in $S$.

## The algorithm

```pseudo id=main
SINDY(x, ẋ, θ, λ)
L1  Θ ← the M × p matrix of the library functions at the samples
L2  for each state component j = 1, ..., n:
L3      ξ ← the least squares solution of Θ ξ = ẋ_j;  S ← {1, ..., p}
L4      repeat
L5          S_new ← {k ∈ S : |ξ_k| ≥ λ}
L6          if S_new ≠ S: S ← S_new;  ξ ← 0;  ξ_S ← the least squares solution of Θ_S ξ_S = ẋ_j
L7      until S did not change
L8  return Ξ, with column j equal to the final ξ of component j
```

The set $S$ can only shrink, and the loop goes on only while it shrinks, so there are at most $p + 1$ fits for each component. On exit, every kept coefficient is at least $\lambda$ in size and the kept coefficients are the least squares fit on their own columns. The code builds the library of all monomials of total degree at most $d$ and solves each least squares problem by a Householder [QR decomposition](/qr-decomposition/), which is more accurate than the normal equations. When only the states are measured, the code estimates the derivatives by central differences $(x_{k+1} - x_{k-1}) / (2h)$.

## Example

Take the Lorenz system

$$\dot x_0 = 10 (x_1 - x_0), \qquad \dot x_1 = x_0 (28 - x_2) - x_1, \qquad \dot x_2 = x_0 x_1 - \tfrac{8}{3} x_2,$$

from $x(0) = (-8, 7, 27)$. Simulate it with the classical [Runge-Kutta method](/runge-kutta-methods/) with step $0.002$ up to $t = 5$, and keep every fifth point, so $h = 0.01$ and $M = 501$. The library is the $p = 10$ monomials of degree at most 2 in $x_0$, $x_1$, $x_2$, and $\lambda = 0.5$. The true $\Xi$ has 7 nonzero entries.

**Exact derivatives.** With $\dot x$ from the right side of the equations, SINDy returns the 7 true coefficients to 10 digits and sets the other 23 entries to zero.

**Central differences.** With derivatives from central differences ($M = 499$), it finds the right 7 terms:

| term | $\dot x_0$ | $\dot x_1$ | $\dot x_2$ |
|---|---|---|---|
| $x_0$ | $-9.9825$ | $27.8137$ | |
| $x_1$ | $9.9820$ | $-0.9659$ | |
| $x_2$ | | | $-2.6596$ |
| $x_0 x_1$ | | | $0.9973$ |
| $x_0 x_2$ | | $-0.9947$ | |

**Noisy derivatives (measurement).** Add Gaussian noise with standard deviation 1 to the exact derivatives (seed 1). With $\lambda = 0.5$ SINDy again finds the right 7 terms, for example $28.0126\, x_0 - 1.0086\, x_1 - 1.0002\, x_0 x_2$ for $\dot x_1$. With $\lambda = 0.05$ it keeps two wrong constant terms, $-0.0630$ in $\dot x_0$ and $0.1035$ in $\dot x_2$. With $\lambda = 2$ it removes the true terms of size 1: the equation for $\dot x_1$ becomes $-2.7256\, x_0$ and the equation for $\dot x_2$ loses all its terms.

## Correctness

**Claim.** For each component, the loop stops after at most $p + 1$ fits, and the result $\xi$ is the least squares fit on its support with every nonzero entry at least $\lambda$ in size. If $\Theta$ has full column rank, the derivatives are exact, $\dot x = \Xi^{*T} \theta(x)$, and $\lambda$ is at most the smallest nonzero entry of $\Xi^*$ in size, SINDy returns $\Xi^*$.

**Key invariant.** $S_0 \supsetneq S_1 \supsetneq \cdots$ until the stop, and $\xi = \operatorname{LS}(S)$, the least squares fit on the current set.

For exact derivatives, the first fit already gives $\xi^*$, the threshold keeps exactly its support, and the second fit gives $\xi^*$ again. If the error in the derivatives, mapped through $\Theta^{+}$ and $\Theta_{S^*}^{+}$, is smaller than both $\lambda$ and the gap between $\lambda$ and the smallest true coefficient, the same steps give the least squares fit on the true support. The full proof is below.

## Complexity

In the [real RAM](/real-ram/). L1 evaluates $p$ functions at $M$ samples; for monomials this costs $O(M p n)$. Each least squares fit with $k \le p$ columns costs $O(M k^2)$ with Householder QR. There are at most $p + 1$ fits per component and $n$ components, so the total is $O(n M p^3)$ in the worst case. In practice the loop stops after a few fits, and the cost is close to $O(n M p^2)$. The extra space is $O(M p)$ for $\Theta$.

The library size grows fast: all monomials of degree at most $d$ in $n$ variables give $p = \binom{n + d}{d}$ functions.

## Properties

- **At most p + 1 fits (theorem).** The kept set shrinks at every step that does not stop.
- **Exact recovery (theorem).** With exact derivatives, a full rank library matrix and $\lambda$ at most the smallest true coefficient in size, the result is the true model.
- **Robust recovery (theorem).** If the derivative error is small enough compared with $\lambda$ and with the gap to the smallest true coefficient, the support is right and the result is the least squares fit on the true support.
- **Link to an l0 penalty (theorem).** Zhang and Schaeffer (2019) prove that the iteration approximates local minimizers of $\lVert \Theta \xi - b \rVert^2 + \lambda^2 \lVert \xi \rVert_0$, and give conditions for convergence and one-step recovery.
- **Sensitive to the threshold (measurement).** In the example, $\lambda = 0.05$ kept wrong terms and $\lambda = 2$ removed true terms. The right range depends on the size of the true coefficients and on the noise.
- **Interpretable.** The result is a short formula in the library functions, which can be checked against physical laws.

## Variants and improvements

- **Lasso and other sparse regressions.** [Lasso regression](/lasso-regression/) or [orthogonal matching pursuit](/orthogonal-matching-pursuit/) in place of thresholded least squares. Ridge regularization inside each fit helps when the library columns are nearly dependent.
- **SINDy with control.** Adds the inputs to the library, $\dot x \approx \Xi^T \theta(x, u)$.
- **Implicit SINDy.** For rational right sides, such as in enzyme kinetics, the equations are written in implicit form.
- **Weak or integral forms.** Multiply by test functions and integrate by parts, so no derivative of noisy data is needed.
- **Ensemble SINDy.** Fit on many subsamples of the data and keep the terms that appear often, which also gives a measure of uncertainty.
- **Model selection.** Run SINDy for several $\lambda$ and choose with [cross-validation](/cross-validation/) or the [Akaike information criterion](/akaike-information-criterion/).
- **Discrete time.** Fit $x_{k+1} \approx \Xi^T \theta(x_k)$ directly, with no derivatives.

## When to use it

Use SINDy when the state is measured, the dynamics are nonlinear, and you expect the equations to be a short combination of known kinds of terms, as for many mechanical, chemical and fluid systems. It needs good derivatives, so the sampling must be fast and the noise small, or a variant that avoids derivatives. It does not work well when the true right side is not sparse in the library, when only some states are measured, or when the library columns are nearly dependent on the data. For a linear model of many measurements, use [dynamic mode decomposition](/dynamic-mode-decomposition/) or a subspace method.

## Pitfalls

- **Noisy derivatives.** Finite differences make noise larger by a factor of about $1/h$. Smooth the data first, use total variation differentiation, or use a weak form.
- **Collinear library columns.** If the trajectory stays near an attractor, some library functions are nearly linear combinations of others on the data. Then $\Theta$ is badly conditioned and the selected terms are not reliable. Use several initial states or richer inputs.
- **Scaling.** Coefficients of different library functions have different units. One threshold for all of them favors large-scale terms. Normalize the columns of $\Theta$, or use a threshold for each term.
- **The library must contain the true terms.** If a needed term is missing, SINDy returns the best sparse fit in the wrong library, often with many terms.
- **Too few samples.** The least squares problems need $M \ge p$ and a library matrix of full column rank. The code raises an error when it meets an exactly zero pivot.
- **Validation.** Simulate the identified model and compare with data that were not used for the fit. A small fit error on the derivatives does not guarantee a correct long-time simulation.

## Implementations

## History

Fitting equations to data by searching over terms has a long history, from regression on candidate terms to symbolic regression by genetic programming, for example by Schmidt and Lipson in 2009. Brunton, Proctor and Kutz (2016) made the search a sparse linear regression over a fixed library and solved it by sequentially thresholded least squares, which is fast and simple. They showed it on the Lorenz system, on vortex shedding behind a cylinder and on other examples. Many extensions followed, for control, implicit equations, weak forms and model selection. Zhang and Schaeffer (2019) gave a convergence analysis of the thresholded least squares iteration.

## References
