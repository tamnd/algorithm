---
tag: Z7JZYG
kind: algorithm
slug: rauch-tung-striebel-smoother
name: Rauch-Tung-Striebel smoother
aliases:
- RTS smoother
- Kalman smoother
- RTS fixed-interval smoother
area: machine-learning/probabilistic-inference
level: advanced
summary: "Exact fixed-interval smoother for linear Gaussian state space models: a Kalman filter forward pass, then a backward pass with gain C_t = P_t|t A^T P_(t+1|t)^(-1)."
solves: [smoothing]
model: real-ram
complexity:
  vars: {n: the state dimension, m: the observation dimension, T: the number of time steps}
  time: {worst: "O(T (n^3 + n^2 m + n m^2 + m^3))"}
  space: {extra: "O(T n^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1965
  people: [Herbert E. Rauch, F. Tung, Charlotte T. Striebel]
  note: Rauch, Tung and Striebel derived the smoother as the maximum likelihood estimate of the state trajectory and split it into a forward Kalman filter and a backward recursion.
prereqs: [kalman-filter, smoothing]
see_also: [filtering, state-space-model, forward-backward-algorithm, extended-kalman-filter, unscented-kalman-filter, gaussian-belief-propagation, expectation-maximization, particle-filter]
sources:
  - paper: doi:10.2514/3.3166
    title: "H. E. Rauch, F. Tung and C. T. Striebel, Maximum likelihood estimates of linear dynamic systems, AIAA Journal 3(8), 1965, pages 1445 to 1450"
    locator: the fixed-interval smoother as a forward filter followed by a backward recursion
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 8 (Bayesian smoothing equations and the Rauch-Tung-Striebel smoother), Chapter 4 (the Kalman filter), Chapter 9 (extended and unscented smoothers)"
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: "Section 13.3 (linear dynamical systems: inference by the Kalman filter and the backward smoothing pass, and learning by EM)"
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, pages 35 to 45"
    locator: the forward recursion that the smoother uses as its first pass
---

The Rauch-Tung-Striebel (RTS) smoother computes the exact [smoothing](/smoothing/) distributions $p(x_t \mid y_{1:T})$ of a linear Gaussian [state space model](/state-space-model/) for every $t$ in a fixed interval $0 \le t \le T$. It runs the [Kalman filter](/kalman-filter/) forward over the data and stores the filtered and predicted moments. Then it runs one backward pass that corrects each filtered estimate with the information that came later, through the gain $C_t = P_{t|t} A^\top P_{t+1|t}^{-1}$. Each smoothed distribution is Gaussian, so the output is a mean $m_{t|T}$ and a covariance $P_{t|T}$ for each step. The method is the linear Gaussian counterpart of the [forward-backward algorithm](/forward-backward-algorithm/) for hidden Markov models.

## In plain words

A filter tracks a hidden quantity, such as the position of a car, and updates its guess each time a new noisy measurement comes in. At each moment it uses only the measurements up to that moment. When the whole record is available, you can do better for past moments: a measurement taken later also tells you where the car was earlier.

The smoother first runs the filter from start to end and keeps all its guesses. Then it walks back from the end. At each step it asks how much the next guess changed when the later data came in, and it moves the current guess by a part of that change. The part is large when the current guess was uncertain and the motion from now to the next step is predictable, and small in the other case.

## The problem

The model is the linear Gaussian state space model, also called a linear dynamical system:

$$x_0 \sim \mathcal N(m_0, P_0), \qquad x_t = A x_{t-1} + q_t, \quad q_t \sim \mathcal N(0, Q), \qquad y_t = H x_t + r_t, \quad r_t \sim \mathcal N(0, R),$$

for $t = 1, \ldots, T$, with all noise terms independent. The state $x_t$ has dimension $n$ and the observation $y_t$ has dimension $m$. The matrices $A$, $Q$, $H$, $R$ and the prior $(m_0, P_0)$ are known, and $Q$ and $R$ are positive definite.

The query is the fixed-interval smoothing marginal $p(x_t \mid y_{1:T})$ for each $t = 0, \ldots, T$. In this model it is the Gaussian $\mathcal N(m_{t|T}, P_{t|T})$. The notation $m_{t|s}$ and $P_{t|s}$ means the mean and covariance of $x_t$ given $y_{1:s}$.

## The algorithm

The forward pass is the Kalman filter. Its two steps are the predict step $m_{t|t-1} = A m_{t-1|t-1}$, $P_{t|t-1} = A P_{t-1|t-1} A^\top + Q$, and the update step with the innovation covariance $S_t = H P_{t|t-1} H^\top + R$, the gain $K_t = P_{t|t-1} H^\top S_t^{-1}$, $m_{t|t} = m_{t|t-1} + K_t (y_t - H m_{t|t-1})$ and $P_{t|t} = P_{t|t-1} - K_t S_t K_t^\top$. The backward pass uses only the stored moments, not the observations.

```pseudo id=main
RTS-SMOOTHER(A, Q, H, R, m_0, P_0, y_1..y_T)
L1  m_{0|0} ← m_0, P_{0|0} ← P_0
L2  for t ← 1 to T do                                   ▷ forward pass: Kalman filter
L3      m_{t|t−1} ← A m_{t−1|t−1};  P_{t|t−1} ← A P_{t−1|t−1} Aᵀ + Q
L4      S_t ← H P_{t|t−1} Hᵀ + R;  K_t ← P_{t|t−1} Hᵀ S_t⁻¹
L5      m_{t|t} ← m_{t|t−1} + K_t (y_t − H m_{t|t−1});  P_{t|t} ← P_{t|t−1} − K_t S_t K_tᵀ
L6  m_{T|T} and P_{T|T} are the smoothed moments at T
L7  for t ← T − 1 down to 0 do                          ▷ backward pass
L8      C_t ← P_{t|t} Aᵀ P_{t+1|t}⁻¹
L9      m_{t|T} ← m_{t|t} + C_t (m_{t+1|T} − m_{t+1|t})
L10     P_{t|T} ← P_{t|t} + C_t (P_{t+1|T} − P_{t+1|t}) C_tᵀ
L11 return m_{0|T}, …, m_{T|T} and P_{0|T}, …, P_{T|T}
```

Line L9 corrects the filtered mean by the gain times the change that the future data made to the next step: $m_{t+1|T} - m_{t+1|t}$. Line L10 does the same for the covariance; since $P_{t+1|T} \preceq P_{t+1|t}$, the correction makes the covariance smaller. The pass also gives the lag-one cross-covariance $\mathrm{Cov}(x_{t+1}, x_t \mid y_{1:T}) = P_{t+1|T} C_t^\top$, which the M-step of [expectation maximization](/expectation-maximization/) for this model needs.

## Example

Take a scalar random walk with $A = H = Q = R = 1$, the prior $m_0 = 0$, $P_0 = 1$, and three observations $y = (1, 2, 0)$. All numbers are exact fractions.

| $t$ | $y_t$ | $P_{t\mid t-1}$ | $m_{t\mid t}$ | $P_{t\mid t}$ | $C_t$ | $m_{t\mid 3}$ | $P_{t\mid 3}$ |
|---|---|---|---|---|---|---|---|
| 0 | | | 0 | 1 | 1/2 | 3/7 | 13/21 |
| 1 | 1 | 2 | 2/3 | 2/3 | 2/5 | 6/7 | 10/21 |
| 2 | 2 | 5/3 | 3/2 | 5/8 | 5/13 | 8/7 | 10/21 |
| 3 | 0 | 13/8 | 4/7 | 13/21 | | 4/7 | 13/21 |

The forward pass at $t = 1$: $P_{1|0} = 1 + 1 = 2$, $S_1 = 3$, $K_1 = 2/3$, so $m_{1|1} = 2/3$ and $P_{1|1} = 2 - 4/3 = 2/3$. The backward pass starts at $t = 3$ with the filtered values. At $t = 2$: $C_2 = (5/8)/(13/8) = 5/13$, and $m_{3|2} = m_{2|2} = 3/2$ because $A = 1$, so

$$m_{2|3} = \tfrac32 + \tfrac{5}{13}\bigl(\tfrac47 - \tfrac32\bigr) = \tfrac32 - \tfrac{5}{14} = \tfrac87, \qquad P_{2|3} = \tfrac58 + \tfrac{25}{169}\bigl(\tfrac{13}{21} - \tfrac{13}{8}\bigr) = \tfrac58 - \tfrac{25}{168} = \tfrac{10}{21}.$$

The last observation $y_3 = 0$ pulls the estimate of $x_2$ down from $3/2$ to $8/7$. The smoothed variances are smaller than the filtered ones at every $t < T$, and equal at $t = T$. The smoothed mean at $t = 0$ moves from the prior mean $0$ to $3/7$, because the prior alone saw no data.

The same numbers come out of a direct solve of the joint Gaussian posterior of $(x_0, \ldots, x_3)$: build its tridiagonal precision matrix and invert it.

## Correctness

The forward pass is the Kalman filter, so after it $x_t \mid y_{1:t} \sim \mathcal N(m_{t|t}, P_{t|t})$ and $x_{t+1} \mid y_{1:t} \sim \mathcal N(m_{t+1|t}, P_{t+1|t})$. The backward pass rests on one [conditional independence](/conditional-independence/): given $x_{t+1}$, the state $x_t$ does not depend on $y_{t+1:T}$, so $p(x_t \mid x_{t+1}, y_{1:T}) = p(x_t \mid x_{t+1}, y_{1:t})$. Given $y_{1:t}$, the pair $(x_t, x_{t+1})$ is jointly Gaussian with cross-covariance $P_{t|t} A^\top$, so conditioning gives $x_t \mid x_{t+1}, y_{1:t} \sim \mathcal N(m_{t|t} + C_t (x_{t+1} - m_{t+1|t}),\ P_{t|t} - C_t P_{t+1|t} C_t^\top)$. Averaging this over $x_{t+1} \sim \mathcal N(m_{t+1|T}, P_{t+1|T})$, which holds by backward induction, gives lines L9 and L10. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each forward step multiplies $n \times n$, $n \times m$ and $m \times m$ matrices and solves with the $m \times m$ matrix $S_t$: $O(n^3 + n^2 m + n m^2 + m^3)$ operations. Each backward step inverts or factors the $n \times n$ matrix $P_{t+1|t}$ and does a few $n \times n$ products: $O(n^3)$. Over $T$ steps the time is

$$O\bigl(T (n^3 + n^2 m + n m^2 + m^3)\bigr),$$

which is linear in $T$. A direct solve of the joint Gaussian of all $T + 1$ states uses a matrix of size $n(T+1)$, which costs $O(n^3 T^3)$ with dense elimination; the RTS smoother is block tridiagonal elimination on that matrix, done in time order. The memory is $O(T n^2)$ for the stored $m_{t|t}$, $P_{t|t}$, $m_{t+1|t}$ and $P_{t+1|t}$. The smoother must have all data before the backward pass starts, so it is an offline method.

## Properties

- **Exact.** In exact arithmetic it gives the true posterior marginals of the linear Gaussian model. They are also the minimum mean squared error estimates of each $x_t$ from $y_{1:T}$.
- **Same at the end.** $m_{T|T}$ and $P_{T|T}$ equal the last filtered moments.
- **Smaller covariance.** $P_{t|T} \preceq P_{t|t}$ for every $t$: more data never makes the posterior wider in this model.
- **Covariances do not depend on the data.** $P_{t|t}$, $P_{t+1|t}$, $C_t$ and $P_{t|T}$ depend only on the model, so they can be computed ahead of time. Only the means use the observations.
- **Joint posterior.** Together with the lag-one cross-covariances, the smoothed moments describe the whole joint posterior of $x_{0:T}$, which is a Gauss-Markov chain backward in time with transition $x_t \mid x_{t+1}$ as above.

## Variants and improvements

- **Time-varying models.** Replace $A, Q, H, R$ by $A_t, Q_t, H_t, R_t$. Nothing else changes. A known input $B u_t$ adds to the predicted mean.
- **Two-filter smoother.** Run a forward filter and a separate backward information filter, then combine the two estimates at each $t$. It is useful when the backward pass must not depend on the stored forward moments.
- **Modified Bryson-Frazier smoother.** A backward recursion on information quantities that does not invert $P_{t+1|t}$. It is preferred when $P_{t+1|t}$ is close to singular.
- **Square-root forms.** Propagate Cholesky factors of the covariances instead of the covariances, for numerical stability.
- **Extended and unscented RTS smoothers.** For nonlinear models, run an [extended Kalman filter](/extended-kalman-filter/) or an [unscented Kalman filter](/unscented-kalman-filter/) forward and use the matching linearization in the backward gain. These are approximations.
- **Fixed-lag smoothing.** Run the backward pass over only the last $L$ steps to get $p(x_{t-L} \mid y_{1:t})$ online, with a delay of $L$.
- **Parameter learning.** The smoothed moments and the lag-one cross-covariances are the E-step of EM for $A, Q, H, R$ (Shumway and Stoffer, 1982).

## When to use it

Use the RTS smoother when the model is linear with Gaussian noise, all the data are available, and you want the best estimate of each past state: offline tracking, trajectory reconstruction, filling gaps in a time series, or the E-step of EM. For online estimation use the [filter](/filtering/) alone. For nonlinear or non-Gaussian models, use the extended or unscented variants as approximations, or particle smoothers built on a [particle filter](/particle-filter/). For discrete hidden states, use the forward-backward algorithm.

## Pitfalls

- **Off-by-one indices.** The gain at time $t$ uses $P_{t|t}$ and the predicted covariance of the next step, $P_{t+1|t}$, not $P_{t|t-1}$. Store both the predicted and the filtered moments in the forward pass.
- **Explicit inverses.** Inverting $P_{t+1|t}$ is fine for small $n$ but loses accuracy when it is ill-conditioned. Solve the linear system with a [Cholesky decomposition](/cholesky-decomposition/) instead.
- **Lost symmetry.** Rounding makes computed covariances slightly asymmetric or even indefinite over long runs. Symmetrize them, or use a square-root form.
- **Singular $Q$.** With a singular process noise, $P_{t+1|t}$ can be singular and $C_t$ is not defined by this formula. Use a pseudo-inverse with care, or the modified Bryson-Frazier form.
- **Wrong noise model.** The output is exact only for the model you give it. If $Q$ or $R$ is wrong, the smoothed covariances are wrong too, and they will look confident.

## Implementations

## History

Rauch, Tung and Striebel published the smoother in 1965 in the AIAA Journal. They derived it as the maximum likelihood estimate of the whole state trajectory of a linear dynamic system, and they showed that it splits into the forward Kalman filter of 1960 and a backward recursion. Earlier smoothing work by Bryson and Frazier (1963) gave a different backward form. The RTS form became the standard because it reuses the filter output directly. In machine learning the same recursion appears as the E-step of EM for linear dynamical systems.

## References
