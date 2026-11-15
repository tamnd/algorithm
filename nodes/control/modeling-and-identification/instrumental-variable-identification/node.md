---
tag: YQN1Q7
kind: algorithm
slug: instrumental-variable-identification
name: Instrumental variable identification
aliases:
- IV identification
- instrument variable method for system identification
area: control/modeling-and-identification
level: core
summary: Replaces the regressors by instruments that are correlated with them but not with the noise, so the estimate stays consistent for colored noise.
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, d: the number of parameters}
  time: {worst: O(N d^2 + d^3)}
  space: {extra: O(N + d^2)}
properties: {deterministic: true, online: false, recursive: false, exact: true}
history:
  year: 1967
  people: [Kwan Y. Wong, Elijah Polak]
  note: "Wong and Polak, and Young in a series of papers from the middle of the 1960s, brought the instrumental variable idea of econometrics to the identification of discrete-time dynamic systems; Söderström and Stoica later gave the full analysis of consistency, accuracy and optimal instruments."
prereqs: [least-squares-arx-identification, instrumental-variables-estimation]
see_also: [prediction-error-method, armax-model, arx-model, closed-loop-identification, persistent-excitation, two-stage-least-squares, impulse-response, system-identification]
sources:
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "the chapter on instrumental variable methods (the basic and extended IV estimates, consistency conditions, asymptotic covariance and optimal instruments)"
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 7 (the instrumental variable method among the correlation approaches) and Chapter 8 (consistency)"
  - paper: "Kwan Y. Wong and Elijah Polak, Identification of linear discrete time systems using the instrumental variable method, IEEE Transactions on Automatic Control 12(6), 707-718, 1967"
    locator: the instrumental variable estimate for linear discrete-time systems and its consistency
  - paper: doi:10.1007/BF01211647
    title: "Torsten Söderström and Petre Stoica, Instrumental variable methods for system identification, Circuits, Systems and Signal Processing 21(1), 1-9, 2002"
    locator: tutorial overview, comparison with least squares, consistency and asymptotic distribution
---

Instrumental variable identification estimates the coefficients of the difference equation $A(q)\, y(k) = B(q)\, u(k) + v(k)$ when the disturbance $v$ is colored, the case where [least-squares ARX identification](/least-squares-arx-identification/) is biased. The bias comes from the past outputs in the regressor $\varphi(k)$, which are correlated with $v(k)$. The method keeps $\varphi(k)$ but multiplies the equations by an instrument vector $\zeta(k)$ that is correlated with $\varphi(k)$ and uncorrelated with $v(k)$, and solves $\sum \zeta(k) \big(y(k) - \varphi(k)^T \theta\big) = 0$, a square linear system of size $d = n_a + n_b$. It is the general [instrumental variables estimator](/instrumental-variables-estimation/) of statistics applied to a dynamic system, with one difference: the instruments are not extra measured variables but are built from the input itself, as delayed inputs or as the noise-free output of a simulated model. They are valid because in open loop the input is independent of the disturbance. The cost is $O(N d^2 + d^3)$, the same as least squares, and the estimate is consistent for any stationary disturbance that is independent of the input.

## In plain words

Least squares explains each output by the past outputs and inputs. When the noise has a memory, the past outputs carry some of the same noise as the present output, and least squares mistakes that shared noise for system behavior. The fix is to weigh the equations with signals that move with the past outputs but know nothing about the noise. The input is such a signal: you chose it, so it does not depend on the noise. Delayed copies of the input, or the output of a rough model driven by the input, serve as these helper signals. The arithmetic is the same as for least squares, one pass over the data and one small system of equations, but one factor in each product is a helper signal instead of the data.

## The problem

**Input.** Samples $y(0), \ldots, y(N-1)$ and $u(0), \ldots, u(N-1)$ taken in open loop, orders $n_a \ge 0$, $n_b \ge 1$, $n_k \ge 0$, and a choice of instruments: *delayed* or *model*.

**Model.** $A(q) = 1 + a_1 q^{-1} + \cdots + a_{n_a} q^{-n_a}$ and $B(q) = b_1 q^{-n_k} + \cdots + b_{n_b} q^{-n_k-n_b+1}$, with regressor $\varphi(k) = \big(-y(k-1), \ldots, -y(k-n_a),\ u(k-n_k), \ldots, u(k-n_k-n_b+1)\big)^T$ and $\theta = (a_1, \ldots, a_{n_a}, b_1, \ldots, b_{n_b})$. The disturbance $v$ may be any stationary process independent of $u$; it need not be white.

**Instruments.** The *delayed* instruments are $\zeta(k) = \big(u(k-n_k), u(k-n_k-1), \ldots, u(k-n_k-d+1)\big)^T$. The *model* instruments are $\zeta(k) = \big(-x(k-1), \ldots, -x(k-n_a),\ u(k-n_k), \ldots, u(k-n_k-n_b+1)\big)^T$, where $x = (B_{\text{aux}}/A_{\text{aux}})\, u$ is the output of an auxiliary model simulated from rest, by default the least squares ARX fit.

**Output.** The solution $\hat\theta$ of the IV equations

$$\sum_{k=k_0}^{N-1} \zeta(k) \big(y(k) - \varphi(k)^T \theta\big) = 0,$$

or a report that their matrix is singular.

## The algorithm

```pseudo id=main
IV-ARX(y, u, na, nb, nk, ⟨instruments⟩)
L1  d ← na + nb;  k0 ← max(na, nk + d - 1) for delayed instruments, max(na, nk + nb - 1) for model instruments;  for model instruments: θaux ← ARX-LS(y, u, na, nb, nk) and x ← (Baux / Aaux) u from rest
L2  R ← the d × d zero matrix;  f ← the zero vector of length d
L3  for k ← k0 to N - 1 do
L4      φ ← (-y(k-1), ..., -y(k-na), u(k-nk), ..., u(k-nk-nb+1));  ζ ← the instrument vector at time k
L5      R ← R + ζ φᵀ
L6      f ← f + ζ · y(k)
L7  if R is singular then fail: the instruments are not correlated enough with φ
L8  θ ← the solution of R θ = f
L9  return θ
```

Line L1 chooses the first time $k_0$ at which both $\varphi(k)$ and $\zeta(k)$ stay inside the record; the delayed instruments reach back to $u(k - n_k - d + 1)$, further than the regressor. For model instruments, L1 also runs least squares once and simulates the auxiliary model, using only $u$, so $x$ contains no noise. Lines L3 to L6 add up the IV equations in one pass. Unlike the least squares matrix, $R$ is not symmetric and not positive semidefinite, so L8 needs a general solver such as Gaussian elimination with pivoting. With $\zeta = \varphi$ the loop is exactly the loop of least squares.

## Example

Take $n_a = n_b = n_k = 1$ and delayed instruments, so $\varphi(k) = (-y(k-1), u(k-1))$, $\zeta(k) = (u(k-1), u(k-2))$ and $k_0 = 2$. The data are those of the least squares example,

$$u = (1, 1, -1, 1, -1, -1), \qquad y = (0, 1, 1.4, -0.2, 0.9, -0.6).$$

| $k$ | $\zeta(k)$ | $\varphi(k)$ | $y(k)$ | $\varphi(k)^T \hat\theta$ | residual |
|---|---|---|---|---|---|
| 2 | $(1, 1)$ | $(-1, 1)$ | $1.4$ | $1.4$ | $0$ |
| 3 | $(-1, 1)$ | $(-1.4, -1)$ | $-0.2$ | $-0.3091$ | $0.1091$ |
| 4 | $(1, -1)$ | $(0.2, 1)$ | $0.9$ | $0.8545$ | $0.0455$ |
| 5 | $(-1, 1)$ | $(-0.9, -1)$ | $-0.6$ | $-0.5364$ | $-0.0636$ |

The loop of L3 to L6 gives

$$R = \begin{pmatrix} 1.5 & 4 \\ -3.5 & -2 \end{pmatrix}, \qquad f = \begin{pmatrix} 3.1 \\ -0.3 \end{pmatrix}.$$

For example $R_{21} = \sum u(k-2) \cdot (-y(k-1)) = -1 - 1.4 - 0.2 - 0.9 = -3.5$. The determinant is $1.5 \cdot (-2) - 4 \cdot (-3.5) = 11$, so L7 passes, and L8 gives

$$\hat a = \frac{-2 \cdot 3.1 - 4 \cdot (-0.3)}{11} = -\frac{5}{11} \approx -0.4545, \qquad \hat b = \frac{1.5 \cdot (-0.3) + 3.5 \cdot 3.1}{11} = \frac{52}{55} \approx 0.9455.$$

The residuals are orthogonal to both instrument columns, $0 - 0.1091 + 0.0455 + 0.0636 = 0$ and $0 + 0.1091 - 0.0455 - 0.0636 = 0$, but not to the column $-y(k-1)$ of $\varphi$; least squares on one more equation of the same data gave $(-0.4851, 0.9655)$.

## Correctness

**Claim.** If $R = \sum_{k \ge k_0} \zeta(k) \varphi(k)^T$ is nonsingular, IV-ARX returns the unique solution of the IV equations. If moreover the data satisfy $y(k) = \varphi(k)^T \theta_0 + v(k)$ for $k \ge k_0$, then $\hat\theta - \theta_0 = R^{-1} \sum \zeta(k)\, v(k)$; in particular $\hat\theta = \theta_0$ exactly for noise-free data, and $\hat\theta \to \theta_0$ whenever $\frac1N R$ tends to a nonsingular matrix and $\frac1N \sum \zeta(k) v(k) \to 0$.

**Key invariant.** After the pass of the loop for time $k$, $R = \sum_{j=k_0}^{k} \zeta(j) \varphi(j)^T$ and $f = \sum_{j=k_0}^{k} \zeta(j)\, y(j)$.

With the invariant at $k = N - 1$, the IV equations read $R \theta = f$, and L8 solves them. Substituting $y = \varphi^T \theta_0 + v$ into $f$ gives $f = R \theta_0 + \sum \zeta v$, which yields the error formula. The full proof is below.

## Complexity

Line L4 costs $O(d)$ and lines L5 and L6 cost $d^2 + d$ multiplications, so the loop costs $O(N d^2)$. Line L8 costs $O(d^3)$ by Gaussian elimination, which also detects the singular case of L7. For model instruments, L1 adds one least squares fit, $O(N d^2 + d^3)$, and one simulation, $O(N d)$. The total is $O(N d^2 + d^3)$ in the [real RAM](/real-ram/). The extra space is $O(d^2)$ for $R$ and $f$, plus $O(N)$ for the simulated output $x$ with model instruments.

## Properties

- **Exact.** In exact arithmetic the result is the exact solution of the IV equations; with rational data it is rational, and noise-free ARX data of the right orders give $\theta_0$ exactly.
- **Consistent for colored noise (theorem).** If the data come from $A_0 y = B_0 u + v$ in open loop with $v$ stationary and independent of $u$, the instruments are built from $u$ only, and $\mathbb{E}\, \zeta(k) \varphi(k)^T$ is nonsingular, then $\hat\theta \to \theta_0$ with probability 1 (Söderström and Stoica 1989; Ljung 1999, Chapter 8). No model of $v$ is needed.
- **The nonsingularity condition (computation).** For the delayed instruments with $n_a = n_b = 2$, $n_k = 1$ and white unit-variance $u$, the entries of $\mathbb{E}\, \zeta \varphi^T$ are $0$, $1$ or $-g_i$, where $g_i$ is the [impulse response](/impulse-response/) of $B_0/A_0$, and the matrix is nonsingular exactly when $g_2^2 - g_1 g_3 \ne 0$. For $A_0 = 1 - 1.5 q^{-1} + 0.7 q^{-2}$ and $B_0 = q^{-1} + 0.5 q^{-2}$, $g = (1, 2, 2.3, \ldots)$ and $g_2^2 - g_1 g_3 = 1.7$.
- **Bias removed (measurement).** For that system with ARMAX noise $C = 1 - q^{-1} + 0.2 q^{-2}$, a white $\pm 1$ input and $N = 50000$, least squares gave $(-1.2286, 0.4547, 0.9965, 0.7650)$, delayed IV gave $(-1.5250, 0.7356, 0.9956, 0.4698)$ and model IV gave $(-1.5067, 0.7071, 0.9954, 0.4877)$, against the true $(-1.5, 0.7, 1, 0.5)$.
- **Variance depends on the instruments (measurement).** Over 20 runs with $N = 2000$, the estimate of $a_1$ had mean $-1.2248$ and standard deviation $0.0136$ for least squares, $-1.5162$ and $0.038$ for delayed IV, and $-1.5023$ and $0.0142$ for model IV. Here the model instruments, which are closer to the noise-free regressor, gave the smaller variance.
- **Not efficient (theorem).** The basic IV estimate is in general less accurate than the [prediction error method](/prediction-error-method/) with a correct noise model; the best accuracy over all instruments and prefilters needs the true noise model (Söderström and Stoica 1989).

## Variants and improvements

- **Extended IV.** Use more instruments than parameters and solve the overdetermined system $\sum \zeta \varphi^T \theta = \sum \zeta y$ in a weighted least squares sense, which can lower the variance.
- **Prefiltered and refined IV.** Filter $y$, $u$ and the instruments by a filter $L(q)$ before L3. With $L$ close to the inverse of the noise model, and the instruments from the current model, iterating gives the refined IV method of Young, which approaches the optimal accuracy.
- **Multistep IV.** Least squares, then model IV, then a noise model fitted to the residuals, then IV again with prefiltering, a fixed sequence of linear solves.
- **Recursive IV.** Update $\hat\theta$ after every sample in $O(d^2)$ as in the [RLS algorithm](/rls-algorithm/), with $\zeta$ in place of one of the two $\varphi$ factors.
- **Closed loop.** In [closed-loop identification](/closed-loop-identification/), build the instruments from the external reference signal $r$, which is independent of the noise, instead of from $u$.
- **Two-stage least squares.** Regressing $\varphi$ on the instruments and then $y$ on the fitted regressor is [two-stage least squares](/two-stage-least-squares/). It gives the same estimate when there are as many instruments as parameters, and an extended IV estimate with one particular weighting when there are more.

## When to use it

Use it when least squares is biased because the disturbance is colored, and a full noise model is not needed or not wanted. It costs one or two linear solves, needs no starting value and has no local minima, so it is also a good starting value for the [prediction error method](/prediction-error-method/) on [ARMAX](/armax-model/) or Box-Jenkins structures. Do not use input-based instruments when the data come from a closed loop, and prefer a prediction error method when the most accurate estimate is needed.

## Pitfalls

- **Past outputs as instruments.** Taking $\zeta(k) = \varphi(k)$, or any vector with measured $y(k-i)$, in L4 brings back the correlation with $v(k)$ and the bias of least squares. In L4 the instrument must be built from $u$ only, or from the simulated $x$.
- **A one-step predictor instead of a simulation.** Computing $x(k)$ in L1 from measured past outputs, $x(k) = -\sum a_i y(k-i) + \cdots$, puts the noise into the instruments. L1 must simulate $x = (B_{\text{aux}}/A_{\text{aux}})\, u$ from rest, using its own past values.
- **The start index of least squares.** Starting the loop of L3 at $\max(n_a, n_k + n_b - 1)$ with delayed instruments makes $\zeta$ read $u$ before time 0; in Python a negative index silently reads the end of the record. For delayed instruments, L1 must use $k_0 = \max(n_a, n_k + d - 1)$.
- **Feedback in the data.** In closed loop $u$ depends on past noise, so instruments from $u$ are correlated with $v$ and the estimate is biased. Build $\zeta$ in L4 from the reference signal instead.
- **A nearly singular $R$.** If the input is not [persistently exciting](/persistent-excitation/) of order $d$ or more, or if a computation like $g_2^2 - g_1 g_3$ is close to 0, $R$ in L7 is close to singular and the estimate has a large variance. Choose a rich input, or model instruments, before L3.

## Implementations

## History

The instrumental variable idea came from econometrics, where it was used to estimate equations whose regressors are correlated with the error. In the middle of the 1960s Young, and Wong and Polak in 1967, applied it to discrete-time dynamic systems, with instruments generated from the input by an auxiliary model. Söderström and Stoica analyzed the method in detail from about 1980 on, in a monograph of 1983 and in their 1989 textbook: they gave the conditions for consistency, the asymptotic covariance and the optimal choice of instruments and prefilters. Young's refined IV method is the iterative form that approaches that optimal accuracy.

## References
