---
tag: XCJC4F
kind: technique
slug: monte-carlo-tolerance-analysis
name: Monte Carlo tolerance analysis
aliases:
- statistical tolerance simulation
area: cad/reverse-engineering-and-inspection
level: core
summary: Samples each part dimension from its distribution, solves the assembly for each sample and reads off the distribution of the assembly gap, nonlinear effects included.
prereqs: [tolerance-stack-up, monte-carlo-integration, binomial-distribution]
see_also: [direct-linearization-method, jacobian-torsor-model, tolerance-allocation, latin-hypercube-sampling, importance-sampling, wilson-score-interval, clopper-pearson-interval, central-limit-theorem]
sources:
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 3, Monte Carlo integration (the empirical average, its variance and its convergence)
  - paper: doi:10.1080/01621459.1927.10502953
    title: Edwin B. Wilson, Probable inference, the law of succession, and statistical inference, Journal of the American Statistical Association 22(158), 1927
    locator: pp. 209 to 212 (the score interval for a proportion)
  - paper: doi:10.1093/biomet/26.4.404
    title: C. J. Clopper and E. S. Pearson, The use of confidence or fiducial limits illustrated in the case of the binomial, Biometrika 26(4), 1934
    locator: pp. 404 to 413 (exact confidence limits for a binomial proportion)
  - paper: doi:10.2307/2685469
    title: Alan Agresti and Brent A. Coull, Approximate is better than "exact" for interval estimation of binomial proportions, The American Statistician 52(2), 1998
    locator: pp. 119 to 126 (the poor coverage of the Wald interval and the score interval)
  - paper: doi:10.1001/jama.1983.03330370053031
    title: "James A. Hanley and Abby Lippman-Hand, If nothing goes wrong, is everything all right? Interpreting zero numerators, JAMA 249(13), 1983"
    locator: the rule of three for zero events
  - paper: doi:10.1080/00401706.1979.10489755
    title: Michael D. McKay, Richard J. Beckman and William J. Conover, A comparison of three methods for selecting values of input variables in the analysis of output from a computer code, Technometrics 21(2), 239 to 245, 1979
    locator: the whole paper (Latin hypercube sampling against simple random sampling)
  - book: isbn:9780070181311
    title: Paul J. Drake, Jr. (editor), Dimensioning and Tolerancing Handbook, McGraw-Hill, 1999
    locator: the chapters on statistical tolerance analysis of assemblies (general locator)
  - paper: doi:10.1016/j.cad.2014.02.014
    title: Hua Chen, Sun Jin, Zhimin Li and Xinmin Lai, A comprehensive study of three dimensional tolerance analysis methods, Computer-Aided Design 53, 1 to 13, 2014
    locator: the comparison of the 3D tolerance analysis methods (general locator)
---

Monte Carlo tolerance analysis estimates the variation of an assembly output by simulation. It draws a random value for every toleranced dimension from an assumed distribution, solves the assembly exactly for that sample, and repeats this $N$ times. The sample of outputs gives the mean, the spread and the fraction of assemblies outside the specification limits, the reject rate. It is [Monte Carlo integration](/monte-carlo-integration/) applied to the assembly function. Unlike the [direct linearization method](/direct-linearization-method/) it uses no first-order expansion, so it sees the curvature of the assembly function, a skewed output and samples whose parts do not fit together. Its cost is $N$ assembly solves, and its result has a sampling error of order $1/\sqrt{N}$, which this page states and bounds.

## In plain words

Build many virtual assemblies. For each one, pick every part size at random, the way a real machine would make it, and put the parts together on the computer. Write down the gap or angle that you get, and whether the assembly is good. After many assemblies, the list tells you the average result, how much it spreads, and what fraction is bad. You do not need a formula for the output, only a way to compute it for one set of parts. The method also shows effects that a straight-line estimate misses, such as an average that moves away from the nominal value, or parts that sometimes do not fit at all. The price is many solves, and an answer that is itself random. So you must also say how far the answer can be from the truth.

## When it applies

The technique needs two things. The first is an assembly function $f$ that computes the output for one set of dimensions, or reports that the parts do not assemble. It can be a closed formula, a solve of [vector loops](/vector-loop-closure/), a chain of torsors or a full contact simulation. The second is a probability model of the dimensions.

**The model of variation.** Each toleranced dimension $X_j$ is a random variable with a known distribution, and the dimensions are independent unless a joint distribution is given. The code of this page uses two common choices for a tolerance $\pm T_j$: a normal distribution with mean at the nominal value and standard deviation $T_j / 3$, and a uniform distribution on $[m_j - T_j, m_j + T_j]$. The output is $Y = f(X)$, evaluated exactly. There is no linearization and no small-angle approximation in the technique itself. If $f$ is a first-order model, such as a [small displacement torsor](/small-displacement-torsor/) or [Jacobian-torsor](/jacobian-torsor-model/) chain, the simulation inherits that first-order approximation, and then only the propagation through $f$ is exact.

Use it when the assembly function is far from linear over the tolerance range, when a sample can fail to assemble, when the input distributions are far from normal, when the reject rate itself is wanted, or to check a linear method. A linear method such as [tolerance stack-up](/tolerance-stack-up/) or DLM is cheaper and exact on linear stacks, so simulation adds nothing there except a check.

## The template

Let $D$ give the distribution of each dimension, let $f$ return the output or NO-FIT, and let $[lo, hi]$ be the specification limits of the output.

```pseudo id=main
MC-TOLERANCE(f, D, N, seed, lo, hi)
L1  rejects ← 0;  start an empty running mean and variance Y;  rng ← generator from seed
L2  for i ← 1 to N do
L3      x ← one independent draw of every dimension from D, using rng
L4      y ← f(x)                                  ▷ solve the assembly exactly
L5      if y = NO-FIT then rejects ← rejects + 1; continue
L6      if y < lo or y > hi then rejects ← rejects + 1
L7      add y to Y                                ▷ Welford's update
L8  p ← rejects / N;  se ← sqrt(p (1 − p) / N)
L9  return mean(Y), var(Y), p, se, a confidence interval for p
```

The holes are $f$, the distributions $D$ and the generator. Line L3 draws the dimensions in a fixed order from one seeded generator (the code uses Python's `random.Random`, a [Mersenne twister](/mersenne-twister/)), so a run can be repeated exactly. Line L7 keeps the running mean and the sum of squared deviations by Welford's update, which avoids the cancellation of the formula $E[Y^2] - (E Y)^2$. A sample that does not assemble counts as a reject and does not enter the mean and variance, so these describe the assemblies that are built.

**The reject-rate estimate is unbiased.** Let $p$ be the probability that one sample is a reject, a sample that does not fit or has its output outside $[lo, hi]$. Let $I_i$ be the [indicator](/indicator-random-variable/) of the event that sample $i$ is a reject. Then $E[I_i] = p$, and line L8 computes $\hat p = \frac{1}{N} \sum_i I_i$. By linearity of expectation, $E[\hat p] = \frac1N \sum_i p = p$. $\blacksquare$

**Its standard error is $\sqrt{p(1-p)/N}$.** Each $I_i$ is a Bernoulli variable with variance $E[I_i^2] - p^2 = p - p^2 = p(1-p)$, because $I_i^2 = I_i$. The samples are independent, so the [variances](/variance/) add: $\operatorname{Var}(\sum_i I_i) = N p (1 - p)$, and $\operatorname{Var}(\hat p) = N p(1-p)/N^2 = p(1-p)/N$. The standard error is its square root. The sum $\sum_i I_i$ has the [binomial distribution](/binomial-distribution/) with parameters $N$ and $p$. Line L8 replaces the unknown $p$ by $\hat p$ in the formula. $\blacksquare$

The relative error is $\sqrt{(1-p)/(pN)}$. So a reject rate of $p = 0.001$ known to within 10 percent at one standard error needs $N \approx (1 - p)/(p \cdot 0.01) \approx 10^5$ samples. The error falls as $1/\sqrt{N}$ for any number of dimensions, the property of [Monte Carlo integration](/monte-carlo-integration/), and the [law of large numbers](/law-of-large-numbers/) gives $\hat p \to p$ with probability $1$.

**Confidence intervals.** By the [central limit theorem](/central-limit-theorem/), $(\hat p - p)/\sqrt{p(1-p)/N}$ is close to standard normal for large $N p (1 - p)$. Let $z = 1.95996$ be the 0.975 quantile of the standard normal. The Wald interval $\hat p \pm z \sqrt{\hat p (1 - \hat p)/N}$ puts $\hat p$ in the standard error. The [Wilson score interval](/wilson-score-interval/) instead keeps $p$ in it and solves $(\hat p - p)^2 \le z^2 p (1 - p)/N$ for $p$. This is the quadratic $p^2 (1 + z^2/N) - p (2 \hat p + z^2/N) + \hat p^2 \le 0$, whose roots are

$$ \frac{\hat p + z^2/(2N)}{1 + z^2/N} \pm \frac{z}{1 + z^2/N} \sqrt{\frac{\hat p (1 - \hat p)}{N} + \frac{z^2}{4 N^2}}. $$

Both intervals have coverage close to 95 percent only in the limit. For small $N \hat p$ the Wald interval covers badly, and with no rejects it is the single point $0$. The Wilson interval keeps close to its nominal coverage (Agresti and Coull 1998). The exact [Clopper-Pearson interval](/clopper-pearson-interval/) has coverage at least 95 percent for every $p$.

**No rejects in $N$ samples.** If no sample is a reject, the exact one-sided 95 percent upper bound on $p$ is $p_u = 1 - 0.05^{1/N}$. *Proof.* The probability of no reject is $(1 - p)^N$, which decreases in $p$. A value $p > p_u$ gives $(1-p)^N < 0.05$, so the test that rejects $p$ when no reject is seen has level $0.05$, and the set of values of $p$ that it does not reject is $[0, p_u]$. Since $1 - e^{-x} \le x$, $p_u = 1 - e^{-\ln(20)/N} \le \ln(20)/N \approx 3.00/N$. This is the rule of three (Hanley and Lippman-Hand 1983). $\blacksquare$

**The output moments.** The sample mean of the assembled outputs is an unbiased estimate of $E[Y \mid \text{assembled}]$, with standard error $\sigma_Y/\sqrt{N_a}$ for $N_a$ assembled samples. The sample variance with divisor $N_a - 1$ is an unbiased estimate of $\sigma_Y^2$. For a normal output its standard error is $\sigma_Y^2 \sqrt{2/(N_a - 1)}$, which is about $0.3$ percent of $\sigma_Y^2$ for $N_a = 200\,000$.

**Cost.** Each sample costs one draw per dimension and one evaluation of $f$, so the run costs $O(N (n + C_f))$ time for $n$ dimensions and an assembly solve of cost $C_f$. For vector loops $C_f$ is a few Newton steps. The extra space is $O(n)$, since the running moments replace the list of outputs; keep the list only for a histogram or quantiles.

**Results.** The proofs above are mathematical results. The numbers in the next section are measured with the code of this page and the stated seeds. There are no standard benchmarks for tolerance analysis, so no other numbers are given.

## Classic examples

**A linear stack against DLM.** The housing gap $G = A - B - C - D$ of the [stack-up page](/tolerance-stack-up/), with $A = 50 \pm 0.10$ and $B, C, D = 20, 15, 14.8 \pm 0.05$, is linear, so DLM is exact for it. With normal dimensions ($\sigma_j = T_j/3$) the predicted variance is $0.0175/9 = 0.0019444$. A run with $N = 200\,000$ and seed 2026 gives the mean $0.19974$ and the variance $0.0019484$, within one standard error of the variance ($0.0000062$). With uniform dimensions the predicted variance is $0.0175/3 = 0.0058333$, and the same run gives $0.0058339$. With the lower limit $lo = 0.1$ and normal dimensions, the exact reject rate is $\Phi(-0.1/0.044096) = 0.011671$. The run gives $2398$ rejects, $\hat p = 0.01199$, a standard error of $0.00024$ and the Wilson interval $(0.01152, 0.01248)$, which contains the exact value. The tests check these agreements within four standard errors.

**The one-way clutch.** The pressure angle of Chase's clutch is $\phi = \arccos((a + c)/(e - c))$, with nominal $a = 27.645$, $c = 11.43$, $e = 50.8$ mm and $\phi_0 = 7.0184^\circ$ (see the [DLM page](/direct-linearization-method/)). If $a + c > e - c$, the roller does not fit. With normal dimensions, the same tolerance $T$ on each, $N = 100\,000$ and seed 31:

| $T$ (mm) | DLM standard deviation | MC standard deviation | MC mean minus $\phi_0$ | second-order shift $\tfrac12 \sum_j H_{jj} \sigma_j^2$ | samples that do not fit |
|---|---|---|---|---|---|
| $0.0127$ | $0.1230^\circ$ | $0.1233^\circ$ | $-0.0011^\circ$ | $-0.0011^\circ$ | $0$ |
| $0.05$ | $0.4844^\circ$ | $0.4896^\circ$ | $-0.0172^\circ$ | $-0.0169^\circ$ | $0$ |
| $0.1$ | $0.9688^\circ$ | $1.0115^\circ$ | $-0.0733^\circ$ | $-0.0675^\circ$ | $14$ |

At the smallest tolerance the linear result is good. As $T$ grows, the simulated spread exceeds the linear one and the mean moves below the nominal angle by about the second-order term of the [DLM correctness proof](/direct-linearization-method/), which DLM does not report. At $T = 0.1$ some samples do not assemble. With uniform dimensions on $\pm 0.1$, $1229$ of the $100\,000$ samples do not fit, $\hat p = 0.01229$ with the Wilson interval $(0.01163, 0.01299)$; DLM gives a finite angle for every one of them.

**Zero rejects.** At $T = 0.0127$ every sample assembles. If a failure to fit is the only reject, the run has no reject and $\hat p = 0$. The Wald interval is then $[0, 0]$, which claims too much. The Wilson upper limit for $N = 100\,000$ is $3.84 \times 10^{-5}$, and the exact one-sided bound is $1 - 0.05^{1/N} = 2.996 \times 10^{-5}$, about $3/N$.

## Variations

- **Variance reduction.** [Latin hypercube sampling](/latin-hypercube-sampling/) (McKay, Beckman and Conover 1979) stratifies each input. When $f$ is monotone in each input, the variance of its mean is no larger than that of plain sampling, and it is much smaller when $f$ is close to a sum of functions of single inputs, as many assemblies are. [Stratified sampling](/stratified-sampling/) and [quasi-Monte Carlo](/quasi-monte-carlo-integration/) points do the same with other designs. The interval of this page assumes independent samples, so these designs need their own error estimate, such as independent replicates.
- **Rare rejects.** For a reject rate in parts per million, plain sampling needs $N$ of the order of $10^7$. [Importance sampling](/importance-sampling/) draws more samples near the limits and weights them back.
- **Other distributions.** Any distribution with a sampler fits line L3: a truncated normal for a process with inspection, a shifted mean for tool wear, or an empirical distribution from measured parts. Correlated dimensions need a joint sampler.
- **Geometric tolerances.** For form, orientation and position tolerances, line L3 draws a small displacement of each feature inside its tolerance zone, a point of a [tolerance map](/tolerance-map/) or a torsor box, and $f$ is the torsor chain. The approximation is then the first-order one of the torsor model.
- **Sensitivities from the sample.** A regression of the outputs on the inputs estimates the sensitivities, which the [DLM](/direct-linearization-method/) gives exactly at the nominal point.
- **Allocation.** Simulation can check the result of [tolerance allocation](/tolerance-allocation/), which uses a linear stack model.

## Pitfalls

- **Too few samples for a small reject rate.** With $N$ samples, rates far below $1/N$ are invisible. Report the interval, not only $\hat p$.
- **The Wald interval at zero or few rejects.** It gives a zero width interval at zero rejects and poor coverage near it. Use the Wilson or Clopper-Pearson interval, or the bound $1 - 0.05^{1/N}$.
- **The distribution is an assumption.** The rule $\sigma = T/3$ is a convention, and real processes have shifted means and other shapes. The result is only as good as the model of variation; it is not a property of the drawing.
- **Silent no-fit samples.** If $f$ returns a value for parts that do not assemble, for example a clipped $\arccos$, the simulation hides the failures. Make $f$ detect them, and count them as rejects.
- **Correlated dimensions.** Two dimensions made in one setup are not independent. Independent sampling then gives the wrong spread.
- **Seeds and generators.** Without a fixed seed a run cannot be repeated, and two methods compared with different random numbers differ by sampling noise as well. Use the same seed, or common random numbers, for comparisons.
- **Inherited linearization.** A simulation through a first-order torsor or Jacobian model is only as accurate as that model; it does not remove the small-angle approximation.

## Exercises

1. Show that the Wilson interval with $\hat p = 1/2$ is symmetric about $1/2$, and that with $\hat p = 0$ its lower limit is $0$ and its upper limit is $(z^2/N)/(1 + z^2/N)$.
2. How many samples are needed to show, with 95 percent confidence and no rejects seen, that the reject rate is below 100 parts per million?
3. For the clutch at $T = 0.05$, compute $\tfrac12 \sum_j H_{jj} \sigma_j^2$ from the closed form of $\phi$ and compare it with the table.
4. A sample is a reject when it breaks the lower or the upper limit. Show that the indicators of the two events are not independent, and that the estimate $\hat p$ of the total reject rate is still unbiased.
5. Show that for a linear $f$ and normal inputs, the simulated output is exactly normal with the RSS variance, so that the only error of the simulation is the sampling error.

## References
