---
tag: 6YYQY7
kind: algorithm
slug: representer-method
name: Representer method
area: scientific-computing/data-assimilation
level: advanced
summary: Solves weak-constraint variational assimilation exactly in the span of representer functions, one per observation, from adjoint and forward runs.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, K: the number of model steps in the window, p: the number of scalar observations, c: the cost of one model or adjoint step}
  time: {worst: "Θ(p K (c + n^2) + p^2 n + p^3)"}
  space: {extra: "Θ(K n + p n + p^2)"}
properties: {deterministic: true, exact_for_linear_model: true, unknowns: one coefficient per observation, representer_matrix: the prior covariance of the observed quantities, runs: "p + 1 adjoint runs and p + 2 forward runs"}
history:
  year: 1982
  people: [Andrew F. Bennett, Peter C. McIntosh]
  note: Bennett and McIntosh solved an open ocean tidal inverse problem with representers in 1982, and Bennett made the method the standard tool for weak-constraint ocean inverse problems in his books of 1992 and 2002.
prereqs: [weak-constraint-4d-var, adjoint-model]
see_also: [four-dimensional-variational-assimilation, rauch-tung-striebel-smoother, kalman-filter, linear-gaussian-inverse-problem, conjugate-gradient-method, optimal-interpolation, schur-complement, generalized-least-squares]
sources:
  - book: isbn:9780521813730
    title: Andrew F. Bennett, Inverse Modeling of the Ocean and Atmosphere, Cambridge University Press, 2002
    locator: the representer solution of the weak-constraint problem and its indirect solution by iterations
  - book: isbn:9780521385688
    title: Andrew F. Bennett, Inverse Methods in Physical Oceanography, Cambridge University Press, 1992
    locator: the generalized inverse of a linear model and its representer expansion
  - paper: doi:10.1175/1520-0485(1982)012<1004:OOMAAI>2.0.CO;2
    title: A. F. Bennett and P. C. McIntosh, Open ocean modeling as an inverse problem, tidal theory, Journal of Physical Oceanography 12(10) (1982) 1004-1018
    locator: the variational tidal inverse problem
  - paper: doi:10.1029/94JC01894
    title: G. D. Egbert, A. F. Bennett and M. G. G. Foreman, TOPEX/POSEIDON tides estimated using a global inverse model, Journal of Geophysical Research 99(C12) (1994) 24821-24852
    locator: a global tidal inverse solution with representers and altimeter data
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

The representer method solves the linear [weak-constraint 4D-Var](/weak-constraint-4d-var/) problem in observation space. For every scalar observation it computes a representer: the change of the whole trajectory over the window that one unit of influence from that observation causes, found by one run of the [adjoint model](/adjoint-model/) backward and one forward run of the model forced by the background and model error covariances. The answer is the first guess plus a combination of the representers, and the $p$ coefficients solve one symmetric positive definite system $(P + R)\beta = d$, where $P$ holds the representers at the observation points and $d$ is the innovation. The method replaces a minimization over $n(K + 1)$ unknowns by a linear system of size $p$, and for a linear model the result is exact: it is the mean of the [Kalman smoother](/rauch-tung-striebel-smoother/) with model error.

## In plain words

Each measurement can only change the estimate in one fixed pattern over space and time. The pattern spreads out from the place and time of the measurement, forward along the model and also backward, and its shape comes from what is known about the errors of the start state and of the model. This pattern is the representer. The method computes the pattern of each measurement once. Then the best estimate is the first guess plus a weighted sum of these patterns, and the weights come from a small system of equations with one unknown per measurement. Few measurements and a large model make the method cheap.

## The problem

**Input.** A linear model $x_k = M_k x_{k-1} + \eta_k$ on the time levels $0, \ldots, K$ with its adjoint, a background $x^b$ with error covariance $B$, model error covariances $Q_k$, and $p$ scalar observations $y_i = h_i^\top x_{k_i} + \epsilon_i$ with error covariance $R$. Notation of Ide, Courtier, Ghil and Lorenc (1997).

**Output.** The trajectory $\hat x_0, \ldots, \hat x_K$ of the minimizer of the weak-constraint cost

$$J = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k=1}^K \tfrac12 \eta_k^\top Q_k^{-1}\eta_k + \tfrac12 (y - \mathcal H x)^\top R^{-1}(y - \mathcal H x), \qquad (\mathcal H x)_i = h_i^\top x_{k_i} .$$

## The algorithm

```pseudo id=main
REPRESENTER-METHOD(x^b, B, {Q_k}, {h_i, k_i, y_i}, R, M, M^T)
L1  x^f_0 <- x^b ; x^f_k <- M_k x^f_(k-1)            ▷ first guess, no model error
L2  for i <- 1 to p do
L3      lambda <- adjoint run backward, forced by h_i at time k_i
L4      r_i(0) <- B lambda_0 ; r_i(k) <- M_k r_i(k-1) + Q_k lambda_k
L5      P_ji <- h_j^T r_i(k_j) for j = 1..p
L6  d_i <- y_i - h_i^T x^f_(k_i) for i = 1..p           ▷ innovations
L7  beta <- solve (P + R) beta = d
L8  lambda <- adjoint run backward, forced by beta_i h_i at times k_i
L9  x_0 <- x^b + B lambda_0 ; x_k <- M_k x_(k-1) + Q_k lambda_k
L10 return x_0, ..., x_K
```

The representer $r_i$ of line L4 is the prior covariance of the trajectory with the observed quantity $h_i^\top x_{k_i}$, so $P$ is the prior covariance of the observed quantities. Lines L8 and L9 form $x^f + \sum_i \beta_i r_i$ with one more pair of sweeps, without storing the representers. The adjoint variable $\lambda$ of line L8 is the same as in the Euler-Lagrange equations of $J$: the analysis increment of the initial state is $B\lambda_0$ and the estimated model error is $\eta_k = Q_k\lambda_k$.

## Example

**One step.** Take $x_1 = x_0 + \eta_1$, $x^b = 0$, $B = Q_1 = R = 1$ and one observation $y_1 = 3$ of $x_1$. The adjoint run gives $\lambda_1 = \lambda_0 = 1$, and the forward run gives $r(0) = 1$ and $r(1) = 1 + 1 = 2$. So $P = 2$, $d = 3$ and $\beta = 3/(2 + 1) = 1$, and the estimate is $\hat x = \beta r = (1, 2)$, the same as the result of weak-constraint 4D-Var on that page.

**Two observations.** Take the scalar model $x_k = \tfrac12 x_{k-1} + \eta_k$ with $K = 2$, $x^b = 2$, $B = 1$, $Q_1 = Q_2 = \tfrac12$, and the observations $y = 3$ at time 1 and $y = 1$ at time 2, each with error variance $\tfrac12$. The first guess is $(2, 1, \tfrac12)$ and the innovations are $d = (2, \tfrac12)$. The representers are

| | $k = 0$ | $k = 1$ | $k = 2$ |
|---|---|---|---|
| $r_1$ (observation at time 1) | $1/2$ | $3/4$ | $3/8$ |
| $r_2$ (observation at time 2) | $1/4$ | $3/8$ | $11/16$ |

so

$$P + R = \begin{pmatrix} 5/4 & 3/8 \\ 3/8 & 19/16 \end{pmatrix}, \qquad \beta = \begin{pmatrix} 70/43 \\ -4/43 \end{pmatrix}.$$

The estimate is $\hat x = x^f + \beta_1 r_1 + \beta_2 r_2 = (120/43, 94/43, 45/43) = (2.791, 2.186, 1.047)$. The second coefficient is negative: the first observation alone would pull $x_2$ above 1, and the second observation pulls it back. The reference code gives these values exactly in rational arithmetic.

## Correctness

The [proof](proofs/correctness.md) shows by direct expansion of the sweeps that $r_i(k) = \mathrm{Cov}(x_k, x_{k_i})h_i$ under the prior, so $P = \mathrm{Cov}(\mathcal H x)$, and that the estimate is $E[x] + \mathrm{Cov}(x, y)\mathrm{Cov}(y)^{-1}(y - E[y])$, the Gaussian conditional mean, which is also the minimizer of $J$ (a theorem). The tests check the estimate and $P$ with exact rational arithmetic against a direct conditioning of the stacked trajectory, in floating point against a Kalman filter and smoother with model error to $10^{-9}$, and they count the model and adjoint runs.

## Complexity

Each representer costs one adjoint run and one forward run, $\Theta(K(c + n^2))$ with dense $Q_k$, and filling column $i$ of $P$ costs $\Theta(pn)$. With the dense solve of size $p$ and the final pair of sweeps the time is $\Theta(pK(c + n^2) + p^2 n + p^3)$. The memory is one trajectory, the observation vectors and $P$, $\Theta(Kn + pn + p^2)$. So the cost grows with the number of observations, not with the number $n(K + 1)$ of unknowns of the primal problem: the method suits a large model with few observations, and is too expensive for the millions of observations of weather prediction unless the system is solved by iterations (see the variants).

## Properties

- **Exact for linear models.** The result is the minimizer of the weak-constraint cost and the Kalman smoother mean with model error (a theorem).
- **Dual form.** The unknowns are the $p$ coefficients in observation space. Strong-constraint 4D-Var has the same dual with $Q = 0$, and the [optimal interpolation](/optimal-interpolation/) formula is the case $K = 0$.
- **A covariance in each column.** The representers are prior covariances of the trajectory with the observed quantities, so they show which parts of the window and of the state each observation can correct.
- **Statistics for free.** $P + R$ is the covariance of the innovations, so $d^\top(P + R)^{-1}d$ has a $\chi^2$ distribution with $p$ degrees of freedom when the error statistics are right, a test of $B$, $Q$ and $R$ (a theorem for Gaussian errors).
- **Linear only.** For a nonlinear model the method applies to the linearized problem inside outer loops, as in incremental 4D-Var.

## Variants and improvements

- **Iterative (indirect) solution.** Do not form $P$. Solve $(P + R)\beta = d$ by the [conjugate gradient method](/conjugate-gradient-method/), where each product $P v$ costs one adjoint run forced by $v$ and one forward run. The cost is then one pair of runs per iteration instead of one per observation (Bennett 2002).
- **Outer loops for nonlinear models.** Linearize the model around the current estimate, solve the linear problem with representers, and repeat.
- **Strong constraint.** With $Q_k = 0$ the same algorithm gives the strong-constraint 4D-Var solution in its dual form, which is the physical space form used in some weather systems.
- **Representer analysis of an observing network.** The eigenvectors of $R^{-1/2} P R^{-1/2}$ show which combinations of the observations the prior can resolve, a tool for the design of observing systems.

## When to use it

Use the representer method for a linear or linearized model when the number of observations is much smaller than the number of unknowns $n(K + 1)$ of the weak-constraint problem, as in ocean tide and circulation problems with sparse data, and when the representers themselves are of interest. With many observations, use the iterative form, or solve the primal problem with [weak-constraint 4D-Var](/weak-constraint-4d-var/).

## Pitfalls

- **An adjoint that is not the transpose (lines L3 and L8).** Then $P$ is not symmetric and is not a covariance, and the estimate is wrong. Check the adjoint with the dot product test.
- **The forward run without model error (line L4).** Dropping $Q_k \lambda_k$ gives the strong-constraint representers, not the weak-constraint ones.
- **Forming $P$ when $p$ is large (line L5).** The cost of $p$ pairs of runs and the $p^3$ solve both grow fast; use the iterative form.
- **An ill-conditioned $P + R$ (line L7).** With small observation errors and nearly redundant observations the system is close to singular, and the solve loses accuracy.
- **Two separate first guesses.** The innovation of line L6 must come from the same first guess that line L9 starts from, the model run from $x^b$ without model error.

## Implementations

## History

Bennett and McIntosh used representers in 1982 to solve a variational inverse problem for open ocean tides, in which the tidal equations hold only as weak constraints. Bennett developed the method into a general tool for ocean inverse problems in his books of 1992 and 2002, with the iterative form that avoids the computation of all representers. Egbert, Bennett and Foreman (1994) applied it to estimate global ocean tides from TOPEX/POSEIDON altimeter data.

## References
