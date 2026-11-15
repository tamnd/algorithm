---
tag: CA7DM9
kind: technique
slug: mu-analysis
name: Mu analysis
aliases:
- robust stability analysis with the structured singular value
area: control/robust-and-adaptive-control
level: advanced
summary: Tests robust stability and performance of an LFT by upper and lower bounds on the structured singular value over frequency.
prereqs: [structured-singular-value, linear-fractional-transformation, model-uncertainty]
see_also: [dk-iteration, small-gain-theorem, h-infinity-norm, linear-matrix-inequality, power-iteration, mixed-sensitivity-design, kharitonov-theorem, h-infinity-control-problem]
sources:
  - paper: doi:10.1049/ip-d.1982.0053
    title: John C. Doyle, Analysis of feedback systems with structured uncertainties, IEE Proceedings D 129(6), 242, 1982
    locator: the robust stability test by mu at each frequency and the D scaling upper bound
  - paper: doi:10.1109/CDC.1982.268218
    title: John C. Doyle, Joseph E. Wall and Gunter Stein, Performance and robustness analysis for structured uncertainty, Proceedings of the 21st IEEE Conference on Decision and Control, 629-636, 1982
    locator: robust performance as robust stability with one more full block
  - paper: doi:10.1016/0005-1098(93)90175-S
    title: Andrew Packard and John C. Doyle, The complex structured singular value, Automatica 29(1), 71-109, 1993
    locator: the main loop theorem, the bounds, and their computation
  - paper: doi:10.1109/9.62265
    title: Michael K. H. Fan, Andre L. Tits and John C. Doyle, Robustness in the presence of mixed parametric uncertainty and unmodeled dynamics, IEEE Transactions on Automatic Control 36(1), 25-38, 1991
    locator: the upper bound for mixed real and complex uncertainty
  - paper: doi:10.1109/CDC.1988.194710
    title: Andrew Packard, Michael K. H. Fan and John C. Doyle, A power method for the structured singular value, Proceedings of the 27th IEEE Conference on Decision and Control, 2132-2137, 1988
    locator: the power iteration for the lower bound
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 11, Structured Singular Value, with the robust stability and robust performance theorems
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 7, robust performance of scalar loops, and Chapter 8, robust stability and performance analysis with mu
---

Mu analysis checks whether a feedback loop stays internally stable, and keeps its performance, for every uncertainty in a given structured set. The loop and its uncertainty are written as a [linear fractional transformation](/linear-fractional-transformation/) of a known system $N$ and a block diagonal $\Delta$. At each frequency the analysis computes an upper and a lower bound on the [structured singular value](/structured-singular-value/) $\mu(N(j\omega))$. If the upper bound stays below 1 at every frequency, the loop is robust; if the lower bound goes above 1 at some frequency, it is not, and the computation gives a perturbation that breaks it. The method is due to Doyle (1982), and robust performance was added by Doyle, Wall and Stein (1982). It is much less conservative than a test with the [small gain theorem](/small-gain-theorem/), which treats all the uncertain blocks as one full block.

## In plain words

Your model has several uncertain parts: a gain known to 20 percent, unmodeled dynamics at high frequency, a sensor with an uncertain lag. Each part sits in its own place in the loop. You pull all of them out into one diagonal box and normalize each so that its size is at most 1. What is left is a known system $N$. At each frequency, $\mu$ tells you how large the diagonal box must be, in the worst arrangement, before the loop goes unstable. If $\mu < 1$ at every frequency, no allowed uncertainty can do it. Performance is checked the same way, by adding a fictitious uncertain block from the errors back to the disturbances. Because $\mu$ is hard to compute exactly, you compute bounds and hope they are close.

## When it applies

- The plant and controller are linear and time invariant, and the uncertainty can be pulled out into a block diagonal $\Delta$ with a known norm bound on each block.
- Unmodeled dynamics are complex blocks. Uncertain physical parameters are real scalars, possibly repeated. With real parameters, use the mixed bounds, or treat them as complex and accept some conservatism.
- The uncertainty is fixed in time or may vary slowly. The test with frequency-dependent D scalings is exact only for blocks that are linear and time invariant. For arbitrarily fast time variation, use constant scalings, which give the scaled small gain test.

## The template

1. **Build the LFT.** Write each uncertainty as a normalized block, $\Delta_i$ with $\|\Delta_i\|_\infty \le 1$, by moving its size into a weight. Close the loop with the controller to get $N = \mathcal{F}_l(P, K)$, partitioned as $\begin{bmatrix} N_{11} & N_{12} \\ N_{21} & N_{22} \end{bmatrix}$, where $N_{11}$ maps the outputs of $\Delta$ back to its inputs and $N_{22}$ is the performance map from the disturbances $w$ to the weighted errors $z$.
2. **Nominal stability.** Check that $N$ is internally stable. Every later test assumes this.
3. **Robust stability.** With $\boldsymbol\Delta$ the structure of the uncertainty, the loop $\mathcal{F}_u(N, \Delta)$ is well posed and internally stable for every $\Delta \in RH_\infty$ in the structure with $\|\Delta\|_\infty < 1/\beta$ if and only if $\sup_\omega \mu_{\boldsymbol\Delta}(N_{11}(j\omega)) \le \beta$ (theorem; Zhou, Doyle and Glover 1996, chapter 11). For blocks normalized as in step 1, with $\|\Delta_i\|_\infty \le 1$, the test is $\sup_\omega \mu_{\boldsymbol\Delta}(N_{11}(j\omega)) < 1$.
4. **Robust performance.** Add a full block $\Delta_P$ of size $\dim w \times \dim z$ and let $\hat{\boldsymbol\Delta} = \{\mathrm{diag}(\Delta, \Delta_P)\}$. By the main loop theorem (Doyle, Wall and Stein 1982; Packard and Doyle 1993), the loop is internally stable and $\|\mathcal{F}_u(N, \Delta)\|_\infty \le \beta$ for every structured $\Delta$ with $\|\Delta\|_\infty < 1/\beta$ if and only if $\sup_\omega \mu_{\hat{\boldsymbol\Delta}}(N(j\omega)) \le \beta$.
5. **Compute the bounds on a frequency grid.** At each $\omega$:
   - the upper bound $\inf_D \bar\sigma(D N D^{-1})$ over the scalings $D$ that commute with the structure, a convex problem (an LMI in $D^* D$, or Osborne balancing as a fast start); for real blocks add the $G$ scalings of Fan, Tits and Doyle (1991);
   - the lower bound $\max_U \rho(N U)$ over the unitary matrices of the structure, by the [power iteration](/power-iteration/) of Packard, Fan and Doyle (1988), which gives a $\Delta$ that reaches it.
6. **Read the result.** Upper bound below 1 everywhere: robust. Lower bound above 1 at $\omega_0$: not robust, and the $\Delta_0 = U/\mu_{\rm lower}$ found there makes $I - N(j\omega_0)\Delta_0$ singular. A real-rational $\Delta(s)$ with $\Delta(j\omega_0) = \Delta_0$ and the same norm can be built from first order all pass factors. If the bounds straddle 1, refine the grid or the bounds. The peak frequency of $\mu$ shows where the loop is weakest.

For $S$ repeated scalar blocks of sizes $r_i$, $F$ full blocks and a matrix of size $n$, the upper bound test $N^* X N - \beta^2 X < 0$ at one frequency and a fixed $\beta$ is an LMI with $\sum_i r_i^2 + F$ real variables (each $X_i$ is complex Hermitian) and one complex Hermitian block of size $n$. The least $\beta$ is a generalized eigenvalue problem, solved by interior point methods ([semidefinite programming](/semidefinite-programming/)). Its solution to a fixed accuracy takes time polynomial in these sizes and in the log of the accuracy, under strict feasibility. Exact $\mu$ is NP-hard (Braatz, Young, Doyle and Morari 1994), so the gap between the bounds cannot be closed fast in general.

## Classic examples

**Robust performance of a scalar loop.** Let the plant be $P(s) = 1/s$ with a multiplicative input uncertainty, $P_p = P(1 + W_I \Delta_I)$ with $|\Delta_I| \le 1$, and the uncertainty weight $W_I(s) = (s + 0.2)/(0.5 s + 1)$: 20 percent at low frequency, rising to 200 percent at high frequency. The performance requirement is $|W_P S_p| < 1$ for the perturbed sensitivity, with $W_P(s) = (s/2 + 0.25)/(s + 0.0025)$. With negative feedback and the error $e = r - y$, the matrix $N$ for the structure $\mathrm{diag}(\Delta_I, \Delta_P)$ is

$$N = \begin{bmatrix} -W_I T & -W_I K S \\ W_P S P & W_P S \end{bmatrix},$$

which has rank one, since $\det N = W_I W_P S\,(K S P - T) = 0$. For a rank one matrix $u v^*$ and $1 \times 1$ complex blocks, $\mu = \sum_i |u_i v_i|$. Proof: $\bar\sigma(D u v^* D^{-1}) = \|D u\|\,\|D^{-1} v\| \ge \sum_i |u_i v_i|$ by the Cauchy-Schwarz inequality, with equality for $d_i^2 = |v_i|/|u_i|$, and $\delta_i = e^{-j \arg(u_i \bar v_i)}/\sum_k |u_k v_k|$ makes $\det(I - u v^* \Delta) = 1 - \sum_i \delta_i u_i \bar v_i = 0$. So

$$\mu_{\rm RP}(\omega) = |W_I T| + |W_P S|,$$

a sum where the separate tests use a maximum. For the controller $K = k$, a frequency sweep (measurement, 1601 points from $10^{-4}$ to $10^4$ rad/s) gives:

| $k$ | peak $\lvert W_P S\rvert$ (nominal performance) | peak $\lvert W_I T\rvert$ (robust stability) | peak $\mu_{\rm RP}$ | at $\omega$ |
|---|---|---|---|---|
| 0.4 | 0.623 | 0.342 | 0.879 | 0.51 |
| 0.5 | 0.500 | 0.409 | 0.909 | 0.93 |
| 0.75 | 0.500 | 0.553 | 1.015 | 1.35 |
| 1 | 0.500 | 0.674 | 1.112 | 1.60 |
| 1.5 | 0.500 | 0.863 | 1.265 | 2.00 |

Every gain gives nominal performance and robust stability, since both peaks are below 1. Robust performance holds only for $k \le 0.5$ among these. For $k = 0.75$ some uncertainty of size at most 1 keeps the loop internally stable but drives $|W_P S_p|$ above 1 near 1.35 rad/s.

**Diagonal versus full uncertainty.** For $N_{11} = \begin{bmatrix} 1 & 4 \\ 1 & 1 \end{bmatrix}$ at some frequency and two scalar uncertainties, $\mu = 3$ while $\bar\sigma = 4.30$ (see the [structured singular value](/structured-singular-value/) page). The small gain test would allow uncertainties of size up to $0.232$, and the mu test allows up to $0.333$.

## Variations

- **Mixed mu.** Real parameters with complex dynamics, with the $D$ and $G$ upper bound and a lower bound by a power iteration for mixed structures.
- **Skewed mu.** Fix the size of some blocks and find the largest size of the others that keeps $\mu < 1$, for example the largest uncertainty with a fixed performance level.
- **State-space tests.** The frequency sweep can be replaced by one LMI with a frequency-independent scaling, which is a sufficient condition and avoids the grid, at the cost of conservatism.
- **Synthesis.** Searching for a controller that lowers the peak of $\mu$ is mu synthesis; [D-K iteration](/dk-iteration/) is the usual method.
- **Parametric methods.** For a single uncertain polynomial with interval coefficients, the [Kharitonov theorem](/kharitonov-theorem/) gives an exact test with four polynomials.

## Pitfalls

- **The grid can miss the peak.** A lightly damped mode gives a narrow peak of $\mu$ between grid points. Add points near the poles of $N$, or bound the derivative of $\mu$ in frequency.
- **Real parameters treated as complex.** This is safe but can be very conservative, since a complex $\delta$ can take phases that a real one cannot.
- **Time variation.** Frequency-dependent $D$ scales are justified only for time-invariant uncertainty. If the parameters vary fast, the test can call a loop robust when it is not.
- **Robust performance is not the sum of the parts in general.** In the scalar case it is the sum of the two peaks at the same frequency. In ill-conditioned multivariable plants, $\mu_{\rm RP}$ can be far larger than both the nominal performance and the robust stability measures (Skogestad and Postlethwaite 2005, chapter 8).
- **Normalization.** The test $\mu < 1$ is meaningful only if each block is scaled to size 1 by its weight. A wrong weight changes the answer.

## Exercises

1. Show that for $\boldsymbol\Delta = \{\delta I\}$ the robust stability test of step 3 is $\sup_\omega \rho(N_{11}(j\omega)) < 1$, and for $\boldsymbol\Delta$ a full block it is $\|N_{11}\|_\infty < 1$.
2. In the scalar example, show that robust performance holds if and only if $|W_I T| + |W_P S| < 1$ at every frequency, by direct use of $S_p = S/(1 + W_I \Delta_I T)$.
3. For $k = 0.5$ in the table, find the largest $c$ such that the loop has robust performance with $W_I$ replaced by $c W_I$. (A frequency sweep is enough.)
4. For $N_{11} = \begin{bmatrix} 0 & a \\ 0 & 0 \end{bmatrix}$ with two scalar blocks, show that every size of diagonal uncertainty is tolerated, and explain this from the block diagram.

## References
