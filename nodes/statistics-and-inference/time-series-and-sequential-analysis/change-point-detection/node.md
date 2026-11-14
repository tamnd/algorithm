---
tag: DCHG0X
kind: problem
slug: change-point-detection
name: Change-point detection
aliases:
- change-point problem
- structural break detection
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Find the times at which the distribution of a sequence changes, offline from a whole series or online with a small delay and few false alarms.
prereqs: [likelihood-function, statistical-hypothesis-test]
see_also: [cusum, binary-segmentation, pelt-algorithm, bayesian-online-changepoint-detection, segmented-least-squares, hidden-markov-model, sequential-probability-ratio-test, bayesian-information-criterion]
sources:
  - paper: doi:10.1093/biomet/41.1-2.100
    title: E. S. Page, Continuous inspection schemes, Biometrika 41(1/2) (1954)
    locator: the cumulative sum scheme for detecting a change in a production process, and its average run length
  - paper: doi:10.1214/aoms/1177693055
    title: G. Lorden, Procedures for reacting to a change in distribution, Annals of Mathematical Statistics 42(6) (1971)
    locator: the worst-case detection delay criterion, the asymptotic lower bound log(gamma) / KL, and the asymptotic optimality of the CUSUM
  - paper: doi:10.1214/aos/1176350164
    title: George V. Moustakides, Optimal stopping times for detecting changes in distributions, Annals of Statistics 14(4) (1986)
    locator: the exact optimality of the CUSUM under Lorden's criterion
  - paper: doi:10.1214/aos/1176346587
    title: Moshe Pollak, Optimal detection of a change in distribution, Annals of Statistics 13(1) (1985)
    locator: the conditional average delay criterion and the near optimality of the randomized Shiryaev-Roberts procedure
  - paper: doi:10.1093/biomet/57.1.1
    title: David V. Hinkley, Inference about the change-point in a sequence of random variables, Biometrika 57(1) (1970)
    locator: the maximum likelihood estimate of a single change point and its asymptotic distribution
  - paper: doi:10.1080/01621459.2012.737745
    title: R. Killick, P. Fearnhead and I. A. Eckley, Optimal detection of changepoints with a linear computational cost, Journal of the American Statistical Association 107(500) (2012)
    locator: the penalized cost formulation of offline detection and the PELT algorithm
  - paper: doi:10.1016/s0092-8240(89)80047-3
    title: Ivan E. Auger and Charles E. Lawrence, Algorithms for the optimal identification of segment neighborhoods, Bulletin of Mathematical Biology 51(1) (1989)
    locator: the segment neighbourhood dynamic program for the best segmentation with a given number of changes
  - paper: doi:10.1007/s11222-016-9636-3
    title: Robert Maidstone, Toby Hocking, Guillem Rigaill and Paul Fearnhead, On optimal multiple changepoint algorithms for large data, Statistics and Computing 27(2) (2017)
    locator: functional pruning (FPOP and SNIP) and its comparison with PELT
  - paper: doi:10.1214/14-AOS1245
    title: Piotr Fryzlewicz, Wild binary segmentation for multiple change-point detection, Annals of Statistics 42(6) (2014)
    locator: binary segmentation on random intervals and its consistency
  - paper: doi:10.1093/biostatistics/kxh008
    title: Adam B. Olshen, E. S. Venkatraman, Robert Lucito and Michael Wigler, Circular binary segmentation for the analysis of array-based DNA copy number data, Biostatistics 5(4) (2004)
    locator: circular binary segmentation and its use for DNA copy number
  - paper: doi:10.1016/j.sigpro.2019.107299
    title: Charles Truong, Laurent Oudre and Nicolas Vayatis, Selective review of offline change point detection methods, Signal Processing 167 (2020)
    locator: a survey of cost functions, search methods and penalties for offline detection
  - book: isbn:9781439838204
    title: Alexander Tartakovsky, Igor Nikiforov and Michèle Basseville, Sequential Analysis, Hypothesis Testing and Changepoint Detection, CRC Press, 2014
    locator: the chapters on quickest change detection (Bayesian and minimax formulations, CUSUM and Shiryaev-Roberts procedures)
---

Change-point detection asks at which times the distribution of a sequence of observations changes. In the offline version the whole series is available, and the task is to split it into segments that each look homogeneous: the number and the places of the changes are both unknown. In the online version, also called quickest detection, the data arrive one at a time, and the task is to raise an alarm soon after a change while raising few false alarms before it. Both versions are built on the [likelihood](/likelihood-function/) of a segmented model. The offline problem with a penalty per change has an exact $O(n^2)$ dynamic program, and the [PELT](/pelt-algorithm/) algorithm often makes it linear; the online problem has the [CUSUM](/cusum/) procedure, which is optimal in a precise sense, and the Bayesian [online changepoint detector](/bayesian-online-changepoint-detection/).

## In plain words

A machine fills bottles. One day a part wears and the bottles start to come out a little too light. Each bottle varies anyway, so one light bottle proves nothing. The question is when the pattern changed. If you have the whole record, you can look back and split it into calm stretches, each with its own average, and ask where the splits best explain the data. Each extra split must earn its place, or you would split the record at every bottle. If you watch the line as it runs, you want an alarm soon after the change. But every alarm stops the line, so false alarms cost money. Both problems trade one error against another: too many splits against too few, or a late alarm against a false one.

## Definition

**Offline, penalized form.** Given observations $y_1, \ldots, y_n$, a segment cost $\mathcal C(y_{s+1..t})$, usually twice the negative maximized log-likelihood of the segment, and a penalty $\beta > 0$, find a number of changes $m \ge 0$ and change points $0 = \tau_0 < \tau_1 < \cdots < \tau_m < \tau_{m+1} = n$ that minimize
$$\sum_{j=0}^{m} \mathcal C\bigl(y_{\tau_j+1..\tau_{j+1}}\bigr) + \beta m.$$
The change point $\tau_j$ is the last index of a segment. For a change in the mean of normal data with known variance $\sigma^2 = 1$, $\mathcal C$ is the residual sum of squares of the segment about its own mean, and a common default is $\beta = 2\log n$, a [BIC](/bayesian-information-criterion/)-type penalty.

**Offline, constrained form.** Given $m$, minimize the total cost over the placements of exactly $m$ change points. Solving it for every $m$ up to $m_{\max}$ and choosing $m$ by a criterion is the segment neighbourhood approach.

**Online, quickest detection.** Observations $X_1, X_2, \ldots$ have density $f_0$ before an unknown change time $\nu$ and density $f_1$ from time $\nu$ on. A detection rule is a stopping time $T$. Write $P_\nu$ for the law with change at $\nu$ and $P_\infty$ for no change. The usual minimax criteria are:

- the false alarm constraint $E_\infty[T] \ge \gamma$, the average run length to a false alarm;
- Lorden's worst-case delay $\bar d(T) = \sup_{\nu \ge 1}\operatorname{ess\,sup} E_\nu\bigl[(T - \nu + 1)^+ \mid X_1, \ldots, X_{\nu-1}\bigr]$;
- Pollak's delay $\sup_{\nu \ge 1} E_\nu[T - \nu \mid T \ge \nu]$.

The task is to minimize the delay subject to the false alarm constraint. In the Bayesian form, $\nu$ has a prior, often geometric, and the task is to minimize $P(T < \nu) + c\,E[(T - \nu)^+]$.

## Variants

- **What changes.** The mean, the variance, both, the slope of a trend, the parameters of an autoregressive model, the whole distribution (nonparametric costs based on ranks or empirical distribution functions), or the covariance of a multivariate series.
- **Known or unknown parameters.** In quality control the in-control law $f_0$ is often known, and the post-change law is a planned shift. In segmentation both are usually unknown and estimated per segment.
- **One change or many.** The at-most-one-change problem is a test of "no change" against "one change at an unknown time", with a maximum over the change time; many changes need a search over segmentations.
- **Offline, online, or online with a window.** Online methods may also look back over a finite window, which bounds their memory.
- **Bayesian.** A product partition model puts a prior on the segmentation and computes posterior probabilities of change points, online or offline.
- **Epidemic changes.** The parameter changes and later changes back, as in a burst; this is two changes with a constraint.

## Examples

**Offline, a mean shift with a penalty.** For $y = (1, 0, 1, 5, 6, 5, 6, 1, 0)$, the RSS cost and $\beta = 4$, the best segmentation with each number of changes $m$ is:

| $m$ | best change points | best total RSS | RSS $+ 4m$ |
|---|---|---|---|
| 0 | none | 55.56 | 55.56 |
| 1 | 3 | 35.50 | 39.50 |
| 2 | 3, 7 | 2.17 | 10.17 |
| 3 | 3, 7, 8 | 1.67 | 13.67 |
| 4 | 3, 4, 7, 8 | 1.33 | 17.33 |

The penalized optimum has the two changes at 3 and 7, the segments $(1, 0, 1)$, $(5, 6, 5, 6)$ and $(1, 0)$. A third change lowers the RSS by only 0.5, less than the penalty. The [PELT](/pelt-algorithm/) page computes this answer step by step.

**Offline, a short burst.** Fifty zeros, then four values of 3, then fifty zeros. A single split anywhere explains little, because a burst in the middle needs two changes at once, so [binary segmentation](/binary-segmentation/) with a standard threshold finds nothing, while PELT and wild binary segmentation find the changes at 50 and 54.

**Online, a mean shift.** In-control data are $N(0, 1)$ and the shift is to $N(1, 1)$. The CUSUM with threshold $h$ has, in simulation, an average run length to a false alarm of 121.7 for $h = 3$ and 913.7 for $h = 5$, with average delays after a change at the start of 6.28 and 10.29 observations. The [CUSUM](/cusum/) page shows how the delay grows like $\log(\text{false alarm run length})$.

**Online, Bayesian.** For the data $0.2, -0.5, 0.4, 3.9, 4.3, 3.6$ with known noise, the [Bayesian online changepoint detector](/bayesian-online-changepoint-detection/) gives posterior probability 0.80 that a change happened just before the fourth value, as soon as that value arrives.

## Known algorithms

| algorithm | setting | guarantee | cost |
|---|---|---|---|
| optimal partitioning ([segmented least squares](/segmented-least-squares/)) | offline, penalized | exact | $O(n^2)$ cost evaluations |
| segment neighbourhood (Auger and Lawrence 1989) | offline, $m$ changes | exact for each $m \le m_{\max}$ | $O(m_{\max} n^2)$ |
| [PELT](/pelt-algorithm/) | offline, penalized | exact | $O(n^2)$ worst case, close to $O(n)$ when changes are frequent |
| FPOP (Maidstone et al. 2017) | offline, penalized, one-parameter costs | exact | close to $O(n \log n)$ in practice |
| [binary segmentation](/binary-segmentation/) | offline | approximate, greedy | $O(n(m + 1))$; $O(n \log n)$ for balanced splits |
| wild binary segmentation (Fryzlewicz 2014) | offline | consistent under conditions | $O(nM)$ for $M$ random intervals |
| [CUSUM](/cusum/) (Page 1954) | online, known $f_0, f_1$ | optimal for Lorden's criterion | $O(1)$ per observation |
| Shiryaev-Roberts | online | near optimal for Pollak's criterion | $O(1)$ per observation |
| [Bayesian online changepoint detection](/bayesian-online-changepoint-detection/) | online, Bayesian | exact posterior of the run length | $O(t)$ at time $t$, less with pruning |
| [hidden Markov model](/hidden-markov-model/) decoding | offline or online, a finite set of regimes | exact for the model | $O(nk^2)$ for $k$ states by the [Viterbi](/viterbi-algorithm/) or [forward](/forward-algorithm/) algorithm |

For models with a continuous latent state that jumps, a [Kalman filter](/kalman-filter/) with outlier and jump tests, or a [particle filter](/particle-filter/), detects changes in a [state space model](/state-space-model/).

## Bounds

- **Offline, exact search.** Any exact method for a general segment cost must, in the worst case, consider all $O(n^2)$ segments, and optimal partitioning does so with $O(n^2)$ cost evaluations. PELT and FPOP are exact as well; their gain depends on the data. Killick, Fearnhead and Eckley (2012) prove that PELT has expected cost $O(n)$ when the number of changes grows linearly with $n$, under conditions on the model; with no change, PELT prunes little and costs $\Theta(n^2)$.
- **Offline, estimation accuracy.** For one change of size $\delta$ in the mean of normal data with variance $\sigma^2$, the error of the maximum likelihood estimate of the change time stays bounded in probability as $n$ grows, and its limit distribution depends only on $\delta/\sigma$ (Hinkley 1970).
- **Online, the delay lower bound.** Lorden (1971) proved that every rule with $E_\infty[T] \ge \gamma$ has worst-case delay at least $(1 + o(1))\log\gamma / D(f_1 \,\|\, f_0)$ as $\gamma \to \infty$, where $D$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/), and that the CUSUM attains it. Moustakides (1986) proved that the CUSUM is exactly optimal for Lorden's criterion at every $\gamma$. These results are cited, not proved, on this site.
- **Online, Pollak's criterion.** Pollak (1985) proved that a randomized Shiryaev-Roberts procedure is optimal up to an additive $o(1)$ term in the delay.

## Reductions

- **To shortest paths.** The penalized offline problem is a shortest path from node 0 to node $n$ in the acyclic graph with an edge $s \to t$ of weight $\mathcal C(y_{s+1..t}) + \beta$ for every $s < t$. Optimal partitioning is this shortest path computed in order, and [segmented least squares](/segmented-least-squares/) is the same recursion with a line fit as the cost.
- **To sequential tests.** The CUSUM is a sequence of [SPRTs](/sequential-probability-ratio-test/) with lower threshold 0, restarted each time one accepts "no change". Its statistic is the maximum over the change time of the log likelihood ratio.
- **To hidden Markov models.** A segmentation with $m$ changes and a left-to-right chain of regimes is a [hidden Markov model](/hidden-markov-model/) whose states can only advance; Viterbi decoding gives the most likely segmentation under the model.
- **To hypothesis tests.** The at-most-one-change problem is a [hypothesis test](/statistical-hypothesis-test/) with a nuisance parameter that exists only under the alternative. The maximum of the likelihood ratio over the change time does not have the usual chi-square limit, so its critical values come from extreme value theory or simulation.

## Applications

- **Quality control.** CUSUM charts monitor production lines, laboratory assays and hospital outcomes.
- **Genomics.** Segmenting DNA copy number along a chromosome finds gains and losses; circular binary segmentation (Olshen et al. 2004) was built for this.
- **Economics and finance.** Structural breaks in regression relations, volatility regimes in returns.
- **Signals and systems.** Fault detection in sensors and machines, segmentation of speech and of physiological signals, intrusion detection in networks.
- **Climate and environment.** Breaks in temperature records caused by station moves or new instruments.

## References
