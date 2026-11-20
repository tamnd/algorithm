---
tag: YFJDYK
kind: technique
slug: desroziers-diagnostics
name: Desroziers diagnostics
area: scientific-computing/data-assimilation
level: advanced
summary: Estimates observation and background error covariances from statistics of innovations and analysis residuals in observation space.
prereqs: [three-dimensional-variational-assimilation, background-error-covariance]
see_also: [optimal-interpolation, kalman-filter, covariance-inflation, ensemble-kalman-filter, representer-method, weak-constraint-4d-var, observation-operator, data-assimilation-problem]
sources:
  - paper: doi:10.1256/qj.05.108
    title: G. Desroziers, L. Berre, B. Chapnik and P. Poli, Diagnosis of observation, background and analysis-error statistics in observation space, Quarterly Journal of the Royal Meteorological Society 131(613) (2005) 3385-3396
    locator: the four relations between residual statistics and error covariances, and their iterative use for tuning
  - paper: doi:10.1002/qj.2650
    title: R. Ménard, Error covariance estimation methods based on analysis residuals, theoretical foundation and convergence properties derived from simplified observation networks, Quarterly Journal of the Royal Meteorological Society 142(694) (2016) 257-273
    locator: the convergence of the iteration, which needs a correct background error covariance, and the unchanged gain when both covariances are estimated
  - paper: doi:10.1111/j.1600-0870.1986.tb00460.x
    title: A. Hollingsworth and P. Lönnberg, The statistical structure of short-range forecast errors as determined from radiosonde data. Part I, The wind field, Tellus A 38(2) (1986) 111-136
    locator: the split of innovation covariances into a spatially correlated background part and an uncorrelated observation part
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Desroziers diagnostics estimate the error covariances of an assimilation system from the output of the system itself. From many analyses, collect three vectors in observation space: the innovation $d^o_b = y - Hx^b$, the analysis increment $d^a_b = Hx^a - Hx^b$, and the analysis residual $d^o_a = y - Hx^a$. If the analysis uses the right error covariances, the sample means of their products estimate the observation error covariance $R$, the background error covariance in observation space $HBH^\top$, and the analysis error covariance $HAH^\top$ (Desroziers, Berre, Chapnik and Poli 2005). If the assumed covariances are wrong, the estimates differ from the assumed ones, which is a test of consistency, and they can be fed back into the analysis to tune it. The tuning converges to the truth only under conditions that must be checked: a wrong background error covariance gives a wrong $R$ (Ménard 2016).

## In plain words

An assimilation system needs to know how large the errors of the measurements and of the forecast are, but nobody can measure these errors directly, because the true state is not known. This method finds them from numbers that the system already produces. For each measurement it compares three things: the measurement, the forecast and the final analysis. It then averages products of their differences over many cases. If the error sizes that the system assumes are right, these averages give back the measurement errors and the forecast errors. If they are wrong, the averages show it, and the system can correct its assumptions and try again.

## When it applies

- A linear or nearly linear analysis $x^a = x^b + K(y - Hx^b)$ with the gain $\tilde K = \tilde B H^\top (H\tilde BH^\top + \tilde R)^{-1}$ of assumed covariances $\tilde B$ and $\tilde R$, as in [optimal interpolation](/optimal-interpolation/), [3D-Var](/three-dimensional-variational-assimilation/), 4D-Var or an [ensemble Kalman filter](/ensemble-kalman-filter/).
- Many analyses are available, over time or over a set of similar observations, so that sample means converge. The errors must be statistically the same over the sample.
- Background and observation errors are not correlated with each other, and both have mean zero.
- The quantities of interest are in observation space: variances of a channel of a satellite instrument, inter-channel correlations, or correlations between nearby observations.

## The template

Let $S = HBH^\top + R$ be the true covariance of the innovation, $\tilde S = H\tilde BH^\top + \tilde R$ the one the analysis assumes, and $G = H\tilde BH^\top \tilde S^{-1}$, so $d^a_b = Gd^o_b$ and $d^o_a = (I - G)d^o_b = \tilde R\tilde S^{-1}d^o_b$. Then, exactly,

$$E[d^o_a d^{o\top}_b] = \tilde R\tilde S^{-1}S, \qquad E[d^a_b d^{o\top}_b] = H\tilde BH^\top \tilde S^{-1}S, \qquad E[d^a_b d^{o\top}_a] = H\tilde BH^\top \tilde S^{-1}S\tilde S^{-1}\tilde R, \qquad E[d^o_b d^{o\top}_b] = S .$$

If $\tilde B = B$ and $\tilde R = R$, then $\tilde S = S$ and the four right sides are $R$, $HBH^\top$, $HAH^\top$ and $HBH^\top + R$, where $A = (I - KH)B$ is the analysis error covariance; the third one follows from $HAH^\top = HBH^\top - HBH^\top S^{-1}HBH^\top = HBH^\top S^{-1}R$.

```pseudo id=main
DESROZIERS({d^o_b}, H B~ H^T, R~)
L1  G <- H B~ H^T (H B~ H^T + R~)^-1
L2  for each analysis t do
L3      d^a_b <- G d^o_b                 ▷ in a real system: H x^a - H x^b
L4      d^o_a <- d^o_b - d^a_b           ▷ y - H x^a
L5      add d^o_a d^o_b^T, d^a_b d^o_b^T, d^a_b d^o_a^T, d^o_b d^o_b^T to the sums
L6  divide the sums by the number of analyses
L7  return the estimates of R, H B H^T, H A H^T and H B H^T + R
```

The holes are the analysis that gives $x^a$ (line L3), the set of analyses over which the means are taken (line L2), and the use of the estimates. In an operational system $d^a_b$ and $d^o_a$ come directly from the analysis and line L1 is not needed. The reference code forms $G$ to simulate a linear analysis, and also gives the expected values above and the iteration below in exact rational arithmetic.

**Consistency check and tuning.** Compare each estimate with the assumed covariance. A mismatch shows that $\tilde B$ or $\tilde R$ is wrong. Tuning replaces $\tilde R$ by the symmetric part of the estimate of $E[d^o_a d^{o\top}_b]$ and runs the analyses again. In expectation this is the fixed point iteration $\tilde R_{j+1} = \tilde R_j \tilde S_j^{-1}S$.

**Worked example.** Take one scalar observation with $HBH^\top = R = 1$, so $S = 2$, and an analysis that uses the right $HBH^\top$ but $\tilde R_0 = 2$. Then $E[d^o_a d^o_b] = \tilde R_0 S/\tilde S_0 = 2 \cdot 2/3 = 4/3$: smaller than the assumed 2, so the diagnostic says that $R$ is overestimated. The iteration gives $\tilde R = 2, 4/3, 8/7, 16/15, \ldots$, that is $\tilde R_j = 2^{j+1}/(2^{j+1} - 1)$, which tends to the true value 1, with the error halved at each step. In general, with the right $HBH^\top$, the scalar map $\tilde R \mapsto \tilde R S/(HBH^\top + \tilde R)$ has the derivative $HBH^\top/S$ at the fixed point $R$, so the iteration converges slowly when the background is much less accurate than the observations.

**A wrong background.** If the analysis assumes $H\tilde BH^\top = 3/2$ instead of 1, the same iteration converges to $\tilde R = S - 3/2 = 1/2$, not to 1: the iteration only makes the total $\tilde S$ match $S$. If both $\tilde R$ and $H\tilde BH^\top$ are updated, one step makes $\tilde S = S$ and keeps the ratio of the first guesses, so the gain does not change and the split between $B$ and $R$ is never learned. This agrees with the results of Ménard (2016). The tests check both cases exactly.

**A twin measurement.** With four observations of a three-variable state, correlated $B$ and an $R$ with one correlated pair, 10000 simulated analyses with the right covariances give the estimates of $R$ to within 0.008 and of $HBH^\top$ to within 0.016 of the truth in every entry (a measurement). With $\tilde R = 2R$ the estimate of $R$ has the diagonal $(0.68, 0.68, 0.74, 0.40)$ instead of the true $(0.5, 0.5, 0.5, 0.3)$, as the formula $\tilde R\tilde S^{-1}S$ predicts, and three steps of the iteration bring it to $(0.58, 0.57, 0.58, 0.36)$.

## Classic examples

- **Satellite radiance errors.** Estimates of the error variances and the inter-channel correlations of satellite instruments, which then enter $R$ in operational systems.
- **Consistency of a 3D-Var or 4D-Var system.** The ratio of the estimated to the assumed variances, for each observation type, shows which part of $B$ or $R$ is too large or too small.
- **Ensemble systems.** In an [ensemble Kalman filter](/ensemble-kalman-filter/) the same relations give a check of the ensemble spread, and they underlie some adaptive [covariance inflation](/covariance-inflation/) schemes.
- **The innovation method.** The older method of Hollingsworth and Lönnberg (1986) splits the covariance of innovations at pairs of stations, as a function of distance, into a correlated background part and an uncorrelated observation part. Desroziers diagnostics need no such assumption on the spatial structure.

## Variations

- **Scalar tuning factors.** Estimate only one factor for the variances of each observation type, from the trace of the estimates. This needs fewer samples and is more robust than full matrices.
- **Iterated tuning.** Apply the estimates, run the analyses again and repeat. The iteration converges to the truth for $R$ when $B$ is right (a theorem in the scalar case shown above), and Ménard (2016) gives the conditions for observation networks.
- **Estimates of correlations.** The off-diagonal entries of the estimate of $R$ give observation error correlations, for example between channels or between nearby observations.
- **Chi-squared checks.** The trace relations $E[d^{o\top}_b S^{-1}d^o_b] = p$ and their variational forms, such as the expected minimum of the cost, give single number checks of the whole system.

## Pitfalls

- **The diagnostic is not an estimate when the statistics are wrong.** With a wrong $\tilde B$ or $\tilde R$, the first estimate is $\tilde R\tilde S^{-1}S$, not $R$ (line L5). Only the fixed point of the iteration, and only with the right $B$, is the truth.
- **Two unknowns from one equation.** Tuning $B$ and $R$ together keeps the gain fixed and cannot find the right split; extra assumptions, such as a known spatial structure of one of them, are needed.
- **The sample must be homogeneous.** Means over observations with different error statistics, or over weather situations with very different background errors, mix them.
- **Correlated errors.** If background and observation errors are correlated, as for observations used to make the background, the relations do not hold.
- **The estimate of $R$ is not symmetric.** The sample mean of $d^o_a d^{o\top}_b$ is not exactly symmetric; take its symmetric part before use, and check that it is positive definite.
- **Nonlinear and quality controlled analyses.** The relations assume a linear analysis with the optimal gain of the assumed statistics. Variational quality control, nonlinear observation operators and thinning change them.

## Exercises

1. Show that $d^o_a = \tilde R\tilde S^{-1}d^o_b$ for a linear analysis with the gain $\tilde K = \tilde BH^\top \tilde S^{-1}$.
2. In the scalar case with the right $HBH^\top$, show that the iteration $\tilde R_{j+1} = \tilde R_j S/(HBH^\top + \tilde R_j)$ has the closed form $1/\tilde R_j - 1/R = (HBH^\top/S)^j (1/\tilde R_0 - 1/R)$, and check it against $2, 4/3, 8/7, \ldots$.
3. Show that updating both $\tilde R$ and $H\tilde BH^\top$ in the scalar case keeps their ratio and so does not change the gain.

## References
