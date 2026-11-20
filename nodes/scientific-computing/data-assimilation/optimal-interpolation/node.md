---
tag: BG2VYK
kind: algorithm
slug: optimal-interpolation
name: Optimal interpolation
aliases:
- statistical interpolation
area: scientific-computing/data-assimilation
level: intro
summary: "Sets each grid value to background plus weights times innovations of nearby observations, with weights from fixed B and R that minimize the error variance."
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the number of grid values, p: the number of observations, s: "the largest number of observations selected for one grid value, with covariance entries from a formula"}
  time: {worst: "Θ(n s^3)"}
  space: {extra: "Θ(s^2)"}
properties: {deterministic: true, linear_in_data: true, best_linear_unbiased: "for the selected observations, if B and R are correct", equals_kalman_update: "when every point uses all observations", covariances: fixed in time}
history:
  year: 1963
  people: [Lev S. Gandin]
  note: Gandin gave the method of optimal interpolation of meteorological fields in 1963, and Lorenc made a global multivariate version the operational analysis at ECMWF.
prereqs: [background-error-covariance, observation-operator]
see_also: [three-dimensional-variational-assimilation, kalman-filter, kriging, gaussian-process, gauss-markov-theorem, covariance-localization, ensemble-kalman-filter, nudging]
sources:
  - book: "L. S. Gandin, Objective Analysis of Meteorological Fields, Gidrometeoizdat, Leningrad, 1963; English translation, Israel Program for Scientific Translations, Jerusalem, 1965"
    title: L. S. Gandin, Objective Analysis of Meteorological Fields, 1963 (English translation 1965)
    locator: optimal interpolation of meteorological fields with statistical structure functions
  - paper: doi:10.1175/1520-0493(1981)109<0701:AGTDMS>2.0.CO;2
    title: A. C. Lorenc, A global three-dimensional multivariate statistical interpolation scheme, Monthly Weather Review 109(4) (1981) 701-721
    locator: the operational global multivariate scheme, with data selection in boxes
  - book: isbn:9780521796293
    title: Eugenia Kalnay, Atmospheric Modeling, Data Assimilation and Predictability, Cambridge University Press, 2003
    locator: Section 5.4 (multivariate statistical data assimilation methods) and Section 5.5 (relation of 3D-Var and PSAS to OI)
  - book: isbn:9780521382151
    title: Roger Daley, Atmospheric Data Analysis, Cambridge University Press, 1991
    locator: the chapters on statistical interpolation
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Optimal interpolation (OI) computes an analysis $x^a$ of a gridded field from a background $x^b$ (usually a short forecast) and a set of observations $y^o$. For each grid value it adds to the background a weighted sum of the innovations $y^o - H(x^b)$ of nearby observations. The weights come from the [background error covariance](/background-error-covariance/) $B$ and the observation error covariance $R$, which are fixed in advance, and they minimize the error variance of the analysis. If every grid value uses all observations, OI gives exactly the analysis step of the [Kalman filter](/kalman-filter/) and the minimizer of [3D-Var](/three-dimensional-variational-assimilation/). The local selection of observations is what made OI cheap enough for operational weather prediction in the 1970s and 1980s, and it is also its main weakness.

## In plain words

A weather center has a forecast for every point of a grid and a few hundred measurements scattered between the points. At each measurement it looks at how far the measurement is from the forecast. Then, for each grid point, it takes the forecast and adds a part of the differences at the measurements nearby. A close measurement gets a large part and a far one gets a small part. A measurement that is known to be poor also gets a small part. The parts are not guessed: they come from a statistical model of how forecast errors at two places are related, and they are the ones that make the expected error at that point as small as possible. To save work, each grid point only looks at the measurements that are close to it.

## The problem

**Input.** A background $x^b \in \mathbb R^n$ with error covariance $B$ ($n \times n$, symmetric positive semidefinite), observations $y^o \in \mathbb R^p$ with error covariance $R$ ($p \times p$, symmetric positive definite), a linear [observation operator](/observation-operator/) $H$ ($p \times n$), and for each grid index $i$ a selection $S_i \subseteq \{1, \ldots, p\}$ of observations. Here $n$ is the number of grid values and $p$ the number of observations. The errors are assumed to have zero mean and to be uncorrelated with each other. This is the notation of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, and $x^b$ and $B$ are its predicted values $\hat x$ and $P$.

**Output.** For each $i$, the value $x^a_i = x^b_i + w_i^\top d_{S_i}$, where $d = y^o - H x^b$ is the innovation and $w_i$ minimizes the error variance of $x^a_i$ among all such linear updates, and that smallest variance $\sigma^2_{a,i}$.

## The algorithm

Write $A = H B H^\top + R$, the covariance of the innovation. The entry $(HB)_{k,i}$ is the covariance between the background error at observation $k$ and the background error at grid value $i$.

```pseudo id=main
OI(x^b, B, y^o, H, R, select)
L1  d <- y^o - H x^b                                   ▷ innovations
L2  for i <- 1 to n do
L3      S <- select(i)                                 ▷ nearby observations
L4      A_S <- (H B H^T + R)[S, S]
L5      c <- (H B)[S, i]
L6      w <- solve A_S w = c
L7      x^a_i <- x^b_i + w^T d[S]
L8      var_i <- B_ii - w^T c
L9  return x^a, var
```

Line L1 computes the observation minus background differences once. Lines L3 to L6 set up and solve a small symmetric positive definite system for each grid value. Line L7 applies the weights, and line L8 gives the expected error variance of the result. If `select` returns no observation, the analysis keeps the background value and its variance $B_{ii}$. Operational schemes often share one selection between all the grid values of a box, so that one factorization of $A_S$ serves many values of $i$ (Lorenc 1981).

## Example

Take $n = 6$ grid points at positions $0, \ldots, 5$, $B_{ij} = (1/2)^{|i - j|}$ (unit variance, correlation halving with each grid step), two observations at points 1 and 4 with $R = \tfrac14 I$, $x^b = (2, 3, 4, 4, 3, 2)$ and $y^o = (4, 2)$. The innovations are $d = (1, -1)$. The global analysis uses both observations everywhere. The local analysis uses only the observations within distance $1.5$ of the grid point. All numbers are exact fractions in the test file, and they are rounded here.

| $i$ | $x^b_i$ | global $x^a_i$ | global $\sigma^2_{a,i}$ | local $S_i$ | local $x^a_i$ | local $\sigma^2_{a,i}$ |
|---|---|---|---|---|---|---|
| 0 | 2 | 2.389 | 0.800 | {1} | 2.4 | 0.8 |
| 1 | 3 | 3.778 | 0.199 | {1} | 3.8 | 0.2 |
| 2 | 4 | 4.222 | 0.768 | {1} | 4.4 | 0.8 |
| 3 | 4 | 3.778 | 0.768 | {4} | 3.6 | 0.8 |
| 4 | 3 | 2.222 | 0.199 | {4} | 2.2 | 0.2 |
| 5 | 2 | 1.611 | 0.800 | {4} | 1.6 | 0.8 |

At point 1 the global gain gives the observation the weight $79/99 \approx 0.80$ and the far observation the weight $2/99$. The local analysis at points 2 and 3 uses different observations, so the field jumps from $4.4$ to $3.6$ between two points that had the same background, while the global field goes from $4.222$ to $3.778$. The local variances are never smaller than the global ones, as Corollary 4 of the proof states.

For a smaller check: two points with $B = \begin{pmatrix} 1 & 1/2 \\ 1/2 & 1 \end{pmatrix}$, $x^b = (10, 12)$ and one observation $y^o = 11$ of the first point with $R = 1$. Then $d = 1$, $A = 2$, the weights are $1/2$ and $1/4$, $x^a = (10.5, 12.25)$, and the variances are $1/2$ and $7/8$. The second point is not observed, but it moves because its background error is correlated with the error at the first point.

## Correctness

The [proof](proofs/correctness.md) shows four facts. $A_S$ is positive definite, so line L6 always has a unique solution. The error of $x^b_i + w^\top d_S$ has the variance $B_{ii} - 2w^\top c + w^\top A_S w$, which line L6 minimizes, and line L8 is the minimum (a theorem when the errors are unbiased, uncorrelated with each other, and $B$ and $R$ are their true covariances). Adding observations to $S_i$ never increases the variance. With all observations selected, the output is $x^b + K d$ with $K = B H^\top (H B H^\top + R)^{-1}$, the variances are the diagonal of $(I - KH)B$, and this equals $(B^{-1} + H^\top R^{-1} H)^{-1}(B^{-1}x^b + H^\top R^{-1} y^o)$, the 3D-Var minimizer.

## Complexity

With $s$ observations selected for a grid value, line L6 costs $\Theta(s^3)$, so the loop costs $\Theta(n s^3)$ when the covariance entries of lines L4 and L5 come from a formula in $\Theta(1)$ time each and $H$ touches a bounded number of grid values per observation. Sharing one selection over a box of $b$ grid values divides the factorization cost by about $b$. The extra space is $\Theta(s^2)$ for $A_S$. For comparison, the global solve with all $p$ observations costs $\Theta(p^3)$ with a direct method. The reference code forms $HB$ and $HBH^\top$ as dense matrices for clarity, which costs $\Theta(p n^2 + p^2 n)$ in addition.

## Properties

- **Linear in the data.** $x^a$ is an affine function of $x^b$ and $y^o$, and the weights do not depend on the values of the data, only on $B$, $R$, $H$ and the selection.
- **Optimal only for the model of the errors.** The variance of line L8 is the true error variance only if $B$ and $R$ are the true covariances. With wrong covariances the analysis is still unbiased, but it is no longer the best one, and line L8 is no longer its error variance.
- **Exact for observed values in the limit.** As $R \to 0$ with observations at grid points and global selection, the analysis matches the observations and interpolates between them with the shape of $B$.
- **Fixed covariances.** $B$ does not evolve with the flow. Methods that propagate it, such as the [Kalman filter](/kalman-filter/) and the [ensemble Kalman filter](/ensemble-kalman-filter/), give gains that change from day to day.
- **Same equations as kriging.** For one variable with $H$ selecting point values, the weights of line L6 are those of simple [kriging](/kriging/) and of the posterior mean of a [Gaussian process](/gaussian-process/) with a known mean.

## Variants and improvements

- **Multivariate OI.** The state holds several variables, such as height and wind, and $B$ couples them, for example with geostrophic balance. One height observation then also changes the wind (Lorenc 1981).
- **Box selection.** All grid values of a box use the same observations from the box and its neighbours. This shares the work and reduces the jumps between neighbouring values.
- **Physical space analysis (PSAS).** Solve the global system $A z = d$ once, for example with the [conjugate gradient method](/conjugate-gradient-method/), and set $x^a = x^b + B H^\top z$. This removes the selection and gives the global analysis (Kalnay 2003, Section 5.5).
- **3D-Var.** Minimize the cost function in state space. For a linear $H$ this gives the same analysis, and it also accepts a nonlinear $H$ (see [3D-Var](/three-dimensional-variational-assimilation/)).
- **Flow dependent weights.** Replace the fixed $B$ by a sample covariance from an ensemble, with [localization](/covariance-localization/), which gives the [ensemble Kalman filter](/ensemble-kalman-filter/).

## When to use it

Use OI when the covariances can be modeled by simple formulas, when the observations are direct or nearly direct measurements of the state (so that $H$ is an interpolation), and when a cheap analysis with a known error estimate is needed. It is still a good choice for surface fields such as sea surface temperature, snow and soil moisture. For satellite radiances and other observations with a nonlinear $H$, or when a smooth global analysis is needed, use [3D-Var](/three-dimensional-variational-assimilation/) or an ensemble method.

## Pitfalls

- **Jumps from the selection (line L3).** Neighbouring grid values that select different observations get different weights, and the analysis can jump between them, as in the example. Large overlapping selections or boxes reduce the jumps. The size of the selection is a tuned rule of thumb.
- **Sign of the innovation (line L1).** Writing $d = H x^b - y^o$ moves the analysis away from the observations. A test with one observation and $B = R$ shows the error at once: the analysis must be halfway between background and observation.
- **Covariance with the wrong grid value (line L5).** For an observation between grid points, $c$ must be $(HB)_{k,i}$, the covariance between the background interpolated to the observation and the value at $i$. Using $B$ at the nearest grid point gives the wrong weights.
- **Correlated observation errors (line L4).** Taking $R$ diagonal when the errors of nearby observations are correlated, as for dense satellite data, gives too much weight to clusters of observations. Thinning the data or modeling the correlation in $R$ fixes this.
- **Trusting the variance (line L8).** The variance only reflects the model of $B$ and $R$. Check it against the statistics of the innovations, for example with [Desroziers diagnostics](/desroziers-diagnostics/).

## Implementations

## History

Lev Gandin published the method in 1963 in Leningrad as the optimal interpolation of meteorological fields, using statistical structure functions estimated from data, and the book was translated into English in 1965. Andrew Lorenc's global three-dimensional multivariate scheme of 1981 was the operational analysis at ECMWF. OI was the main analysis method of the large weather centers until variational methods replaced it in the 1990s, starting with the spectral statistical interpolation of Parrish and Derber (1992) at the US National Meteorological Center, which solves the same statistical problem without local selection.

## References
