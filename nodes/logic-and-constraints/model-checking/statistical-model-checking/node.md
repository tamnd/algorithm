---
tag: HY0E25
kind: technique
slug: statistical-model-checking
name: Statistical model checking
aliases:
- SMC
- Statistical probabilistic model checking
- Approximate probabilistic model checking
area: logic-and-constraints/model-checking
level: research
summary: Decide or estimate the probability of a temporal property from simulated runs, with a Hoeffding sample size or Wald's sequential test and stated error bounds.
prereqs: [probabilistic-ctl, markov-chain, hoeffding-inequality]
see_also: [pctl-model-checking, chernoff-bound, binomial-tail-bounds, walds-equation, monte-carlo-algorithm, importance-sampling, bounded-model-checking, state-explosion-problem]
sources:
  - paper: "Håkan L. S. Younes and Reid G. Simmons, Probabilistic verification of discrete event systems using acceptance sampling, Computer Aided Verification (CAV 2002), Lecture Notes in Computer Science 2404, Springer, pages 223 to 235"
    title: Probabilistic verification of discrete event systems using acceptance sampling
    locator: the use of Wald's sequential probability ratio test with an indifference region to decide probabilistic properties from sampled runs, including nested formulas
  - paper: "Abraham Wald, Sequential tests of statistical hypotheses, The Annals of Mathematical Statistics 16(2), 1945, pages 117 to 186"
    title: Sequential tests of statistical hypotheses
    locator: the sequential probability ratio test, its thresholds A and B, and the inequalities that bound its two error probabilities
  - paper: "Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963, pages 13 to 30"
    title: Probability inequalities for sums of bounded random variables
    locator: the tail bound exp(-2 N eps^2) for the mean of N independent variables with values in [0, 1]
  - paper: "Thomas Hérault, Richard Lassaigne, Frédéric Magniette and Sylvain Peyronnet, Approximate probabilistic model checking, Verification, Model Checking, and Abstract Interpretation (VMCAI 2004), Lecture Notes in Computer Science 2937, Springer"
    title: Approximate probabilistic model checking
    locator: the estimation of path probabilities with a sample size from the Chernoff-Hoeffding bound
  - paper: "Axel Legay, Benoît Delahaye and Saddek Bensalem, Statistical model checking: an overview, Runtime Verification (RV 2010), Lecture Notes in Computer Science 6418, Springer"
    title: "Statistical model checking: an overview"
    locator: the survey of the hypothesis testing and estimation approaches, Bayesian variants, rare events and tools
---

*Statistical model checking* (SMC) answers questions about the probability of a temporal property by running a stochastic model many times and counting. Each run is drawn from the model, for example a [Markov chain](/markov-chain/), and is checked against a path formula such as "a reply comes within 5 steps". This gives independent [Bernoulli trials](/bernoulli-trials/) with the unknown success probability $p$. There are two ways to use them. *Estimation* draws a fixed number $N = \lceil \ln(2/\delta) / (2\varepsilon^2) \rceil$ of runs, and by [Hoeffding's inequality](/hoeffding-inequality/) the fraction of successes is within $\varepsilon$ of $p$ with probability at least $1 - \delta$ (Hérault, Lassaigne, Magniette and Peyronnet 2004). *Hypothesis testing* decides "is $p \ge \theta$?" with Wald's sequential probability ratio test (SPRT), which stops as soon as the evidence is strong enough (Younes and Simmons 2002). The test is allowed to give either answer when $p$ is within $\varepsilon$ of $\theta$. Otherwise its error probabilities are bounded by explicit values such as $\alpha / (1 - \beta)$. The cost does not depend on the number of states, so SMC works where exact methods suffer from the [state explosion problem](/state-explosion-problem/). The price is that the answer is only correct with high probability. The logic is [probabilistic CTL](/probabilistic-ctl/). The exact algorithm for it, by graph search and linear equations, is [PCTL model checking](/pctl-model-checking/). This page is the simulation alternative to that algorithm.

## In plain words

Some systems flip coins, and we want to know how likely a good or bad outcome is. Computing this exactly means solving equations over every state of the system, and there can be far too many states. Statistical model checking runs the system many times, checks each run, and counts the good runs.

The count gives an estimate. Probability theory says how many runs are enough to be close to the true value, with a chosen level of confidence. If we only need a yes or no answer to "is the chance at least this much?", we can stop early. We keep a running score that adds evidence for one side or the other. We stop when the score crosses a line that we set from the error we accept. When the true chance is far from the line, the test is fast and almost always right.

## When it applies

Use statistical model checking when:

- the model can be *simulated*: each run can be generated step by step with the right probabilities, as for Markov chains, continuous-time chains, stochastic hybrid systems and discrete event simulators;
- the property can be decided on a *finite prefix* of each run, as for bounded until $\Phi \,\mathcal{U}^{\le k}\, \Psi$ and time-bounded properties;
- the model is too large or too complex for exact methods, or it has no finite state space at all;
- an answer that is correct with probability $1 - \delta$, or a decision with error probabilities $\alpha$ and $\beta$, is acceptable.

It is a poor fit when:

- the property has an unbounded horizon, such as $\mathcal{F}\, \Psi$ with no bound, because a finite run cannot always decide it;
- the probability is very small, such as $10^{-9}$, because the absolute error $\varepsilon$ of the plain method is then larger than the value (see the pitfalls);
- the model has nondeterministic choices, as in a [Markov decision process](/markov-decision-process/), because a run needs a scheduler and the result then holds for that scheduler only;
- a proof is needed: SMC never gives certainty.

## The template

```pseudo id=main
SPRT(sample, θ, ε, α, β)       ▷ decide P≥θ with indifference region (θ − ε, θ + ε)
L1  p0 ← θ + ε;  p1 ← θ − ε            ▷ H0: p ≥ p0 against H1: p ≤ p1
L2  a ← ln((1 − β)/α);  b ← ln(β/(1 − α))
L3  m ← 0;  d ← 0                       ▷ samples drawn, successes seen
L4  loop
L5      x ← sample()                    ▷ 1 if a fresh simulated run satisfies the path formula
L6      m ← m + 1;  d ← d + x
L7      λ ← d · ln(p1/p0) + (m − d) · ln((1 − p1)/(1 − p0))
L8      if λ ≥ a: return false          ▷ accept H1: the property P≥θ fails
L9      if λ ≤ b: return true           ▷ accept H0: the property P≥θ holds

ESTIMATE(sample, ε, δ)
L10 N ← ⌈ln(2/δ) / (2ε²)⌉
L11 k ← the number of calls among N calls of sample() that return 1
L12 return k / N
```

The value $\lambda$ is the logarithm of the *likelihood ratio*: the probability of the observed sequence when $p = p_1$, divided by its probability when $p = p_0$. A success multiplies the ratio by $p_1/p_0 < 1$, and a failure multiplies it by $(1 - p_1)/(1 - p_0) > 1$. Write $A = e^a = (1 - \beta)/\alpha$ and $B = e^b = \beta/(1 - \alpha)$.

The holes of the template:

- **The sampler.** For $\mathcal{P}_{\bowtie \theta}(\Phi \,\mathcal{U}^{\le k}\, \Psi)$ in a Markov chain, simulate at most $k$ steps from the start state. Return 1 when a $\Psi$-state comes before any state outside $\Phi$, and 0 otherwise. The runs must be independent, so the generator state must not be reset between them.
- **The comparison.** $\mathcal{P}_{\le \theta}(\varphi)$ is $\mathcal{P}_{\ge 1 - \theta}(\neg\varphi)$ on the same runs, with the bit $x$ flipped. Strict and non-strict comparisons give the same test, since the answer is free inside the indifference region.
- **Nested formulas.** When $\Phi$ or $\Psi$ contains a probability operator, the sampler must call SMC again in each state it visits. The inner tests also err, so their error budgets must be part of the outer analysis, as Younes and Simmons do.

### Example

**The symmetric case by hand.** Take $\theta = 0.5$ and $\varepsilon = 0.05$, so $p_0 = 0.55$ and $p_1 = 0.45$, and $\alpha = \beta = 0.05$. Then a success adds $\ln(9/11) \approx -0.2007$ to $\lambda$ and a failure adds $\ln(11/9) \approx 0.2007$. The thresholds are $a = \ln 19 \approx 2.944$ and $b = -2.944$, and $2.944 / 0.2007 \approx 14.67$. So the test stops at the first moment when the number of failures and the number of successes differ by 15. It answers "fails" if the failures are ahead and "holds" if the successes are ahead.

This is the gambler's ruin. At $p = p_0 = 0.55$ the difference moves up with probability $0.45$ and down with probability $0.55$, and the chance of reaching $+15$ before $-15$ is $1/(1 + (11/9)^{15}) \approx 0.0470$. That is the true error $\alpha'$, below both $\alpha = 0.05$ and the guaranteed bound $\alpha/(1 - \beta) \approx 0.0526$. The exact distribution of the test, computed by dynamic programming in the tests, gives:

| true $p$ | 0.45 | 0.5 | 0.55 | 0.6 | 0.7 | 0.9 |
|---|---|---|---|---|---|---|
| Pr(answer "holds") | 0.0470 | 0.5 | 0.9530 | 0.9977 | 0.999997 | $1 - 5 \cdot 10^{-15}$ |
| expected samples | 135.9 | 225 | 135.9 | 74.7 | 37.5 | 18.75 |

A test with a fixed number of samples that answers "holds" when $k/N \ge \theta$ needs $N = \lceil \ln(1/0.05) / (2 \cdot 0.05^2) \rceil = 600$ samples for the same error bound at $p_0$ and $p_1$ by Hoeffding's inequality. To estimate $p$ within $0.05$ with $\delta = 0.05$, line L10 gives $N = 738$.

**The Knuth-Yao die.** The chain on the page [PCTL model checking](/pctl-model-checking/) simulates a fair die with a fair coin. The exact probability that the die is done within 3 flips is $3/4$. With $\varepsilon = \delta = 0.01$, line L10 gives $N = 26492$ runs, and one seeded run of the implementation estimates $0.7503$. The SPRT with $\varepsilon = 0.02$ and $\alpha = \beta = 0.01$ answers "holds" for $\mathcal{P}_{\ge 0.7}(\mathcal{F}^{\le 3}\, \mathit{done})$ after $487$ samples on average, and "fails" for $\mathcal{P}_{\ge 0.8}$ after $369$ on average. The exact error probabilities at $p = 0.75$ are about $6 \cdot 10^{-6}$ and $1.6 \cdot 10^{-5}$.

### Why it is correct

Assume that the calls of sample() return independent bits, each equal to 1 with the same probability $p$. Write $\Pr_p$ for probabilities when the true value is $p$.

**Theorem 1 (estimation).** The value $\hat p = k/N$ returned by ESTIMATE satisfies $\Pr_p(|\hat p - p| \ge \varepsilon) \le \delta$ for every $p \in [0, 1]$.

*Proof.* The bits lie in $[0, 1]$ and have mean $p$. [Hoeffding's inequality](/hoeffding-inequality/) gives $\Pr(\hat p - p \ge \varepsilon) \le e^{-2N\varepsilon^2}$ and $\Pr(p - \hat p \ge \varepsilon) \le e^{-2N\varepsilon^2}$. By the [union bound](/union-bound/), $\Pr(|\hat p - p| \ge \varepsilon) \le 2e^{-2N\varepsilon^2}$. Line L10 makes $N \ge \ln(2/\delta)/(2\varepsilon^2)$, so $2e^{-2N\varepsilon^2} \le \delta$. $\square$

For the SPRT, write $u = \ln(p_1/p_0) < 0$ and $v = \ln((1 - p_1)/(1 - p_0)) > 0$, so each sample adds $u$ or $v$ to $\lambda$. Let $\alpha' = \Pr_{p_0}(\text{accept } H_1)$ and $\beta' = \Pr_{p_1}(\text{accept } H_0)$ be the true errors at the edges of the indifference region.

**Lemma 2 (termination).** For every $p \in [0, 1]$ the test stops with probability 1, and the number of samples has finite expectation.

*Proof.* While the test runs, $b < \lambda < a$. Let $K$ be an integer with $K v > a - b$. If $p < 1$, then $K$ failures in a row end the test, since $\lambda$ would leave the interval upward. Each block of $K$ samples is all failures with probability $(1 - p)^K > 0$, and the blocks are independent. So the test runs past $jK$ samples with probability at most $(1 - (1 - p)^K)^j$. This tail is geometric, so the test stops with probability 1 and the expected number of samples is finite. If $p = 1$, use runs of successes and $u$ instead. $\square$

**Lemma 3 (Wald's inequalities).** $A\,\alpha' \le 1 - \beta'$ and $\beta' \le B\,(1 - \alpha')$.

*Proof.* Let $W_1$ be the set of finite bit sequences after which the test stops with $H_1$. A sequence $w$ with $m$ bits and $d$ ones has $\Pr_{p}(w) = p^d (1 - p)^{m - d}$. So $\Pr_{p_1}(w) = e^{\lambda(w)} \Pr_{p_0}(w)$, where $\lambda(w)$ is the value of line L7 on $w$. Line L8 accepts $H_1$ only when $\lambda(w) \ge a$, so $\Pr_{p_1}(w) \ge A \Pr_{p_0}(w)$ for each $w \in W_1$. The sequences in $W_1$ are disjoint events, so summing gives $\Pr_{p_1}(W_1) \ge A \Pr_{p_0}(W_1) = A \alpha'$. By Lemma 2 the test stops with probability 1 at $p_1$, so $\Pr_{p_1}(W_1) = 1 - \beta'$. The second inequality is the same argument on the set $W_0$ where $H_0$ is accepted, with $\lambda(w) \le b$ and $\Pr_{p_0}(W_0) = 1 - \alpha'$. $\square$

**Theorem 4 (error bounds).** With $A = (1 - \beta)/\alpha$ and $B = \beta/(1 - \alpha)$,

$$\alpha' \le \frac{\alpha}{1 - \beta}, \qquad \beta' \le \frac{\beta}{1 - \alpha}, \qquad \alpha' + \beta' \le \alpha + \beta.$$

*Proof.* Lemma 3 gives $\alpha' \le (1 - \beta')\,\alpha/(1 - \beta) \le \alpha/(1 - \beta)$ and $\beta' \le (1 - \alpha')\,\beta/(1 - \alpha) \le \beta/(1 - \alpha)$. Multiply the first form by $1 - \beta$ and the second by $1 - \alpha$: $\alpha' - \alpha'\beta \le \alpha - \alpha\beta'$ and $\beta' - \alpha\beta' \le \beta - \alpha'\beta$. Adding them, the terms $\alpha'\beta$ and $\alpha\beta'$ cancel, and $\alpha' + \beta' \le \alpha + \beta$. $\square$

**Corollary 5 (strict thresholds).** With $A = 1/\alpha$ and $B = \beta$ instead, $\alpha' \le \alpha$ and $\beta' \le \beta$.

*Proof.* Lemma 3 gives $\alpha' \le (1 - \beta')\,\alpha \le \alpha$ and $\beta' \le \beta\,(1 - \alpha') \le \beta$. $\square$

**Lemma 6 (the edges are the worst case).** If $p \ge p_0$, then $\Pr_p(\text{accept } H_1) \le \alpha'$. If $p \le p_1$, then $\Pr_p(\text{accept } H_0) \le \beta'$.

*Proof.* Couple the two tests. Draw uniform numbers $U_1, U_2, \ldots$ in $[0, 1)$, and let the $i$-th bit be $[U_i < p]$ in one test and $[U_i < p_0]$ in the other. Since $p \ge p_0$, every bit of the first test is at least the bit of the second. A one adds $u < 0$ and a zero adds $v > 0$, so after every number of samples the first $\lambda$ is at most the second. Suppose the first test accepts $H_1$ at step $m$. Then the second $\lambda$ is at least $a$ at step $m$. Before step $m$, the second $\lambda$ is at least the first, which is above $b$, so the second test has not accepted $H_0$. So the second test also accepts $H_1$, at step $m$ or earlier. Hence $\Pr_p(H_1) \le \Pr_{p_0}(H_1) = \alpha'$. The case $p \le p_1$ is symmetric. $\square$

**Theorem 7 (the guarantee of SPRT).** If the property holds with margin, that is $p \ge \theta + \varepsilon$, then SPRT answers "fails" with probability at most $\alpha/(1 - \beta)$. If it fails with margin, that is $p \le \theta - \varepsilon$, then SPRT answers "holds" with probability at most $\beta/(1 - \alpha)$. Inside the indifference region, either answer may come.

*Proof.* Lemma 6 and Theorem 4. $\square$

The bounds of Theorem 4 are exact inequalities and not approximations: they hold for every overshoot of the thresholds. Wald also gave approximations of $\alpha'$ and $\beta'$ and of the expected sample size that ignore the overshoot. Those are estimates and not guarantees.

### Size and time

The cost is the number of runs times the cost of one run. A run of a bounded until with bound $k$ costs at most $k$ simulation steps. Neither method depends on the number of states.

| method | number of runs | guarantee |
|---|---|---|
| ESTIMATE | $N = \lceil \ln(2/\delta) / (2\varepsilon^2) \rceil$, fixed | $\lvert\hat p - p\rvert < \varepsilon$ with probability at least $1 - \delta$ |
| Fixed-size test of $p \ge \theta$ | $\lceil \ln(1/\alpha) / (2\varepsilon^2) \rceil$ for $\alpha = \beta$ | errors at most $\alpha$ outside the indifference region |
| SPRT | random, with finite expectation; largest inside the indifference region | Theorems 4 and 7 |

The dependence on $\varepsilon$ is $1/\varepsilon^2$ and the dependence on the confidence is $\ln(1/\delta)$. So ten times more precision costs a hundred times more runs, and ten times more confidence costs only an additive term. For example, $\varepsilon = 0.01$ and $\delta = 0.01$ give $N = 26492$, and $\varepsilon = 0.001$ and $\delta = 10^{-6}$ give $N = 7254329$. The SPRT uses far fewer samples when $p$ is far from $\theta$, as the table in the example shows. Wald and Wolfowitz proved that among all tests with error probabilities at most $\alpha'$ and $\beta'$ at $p_0$ and $p_1$, the SPRT has the smallest expected number of samples at both $p_0$ and $p_1$.

## Classic examples

- **Bounded until in a Markov chain.** The [Knuth-Yao die](/pctl-model-checking/) above, and in general $\mathcal{P}_{\bowtie \theta}(\Phi \,\mathcal{U}^{\le k}\, \Psi)$, where the exact answer from [PCTL model checking](/pctl-model-checking/) is available for comparison on small models.
- **Discrete event systems.** Younes and Simmons applied the SPRT to time-bounded properties of continuous-time models, such as queueing systems, in which a run is a sequence of timed events.
- **Systems biology.** Models of biochemical reaction networks are simulated with stochastic simulation algorithms, and properties such as "a protein level stays above a threshold for 100 time units" are tested or estimated.
- **Stochastic timed and hybrid models.** Tools such as UPPAAL-SMC and Plasma Lab simulate networks of stochastic timed automata, where the region and zone methods of [timed automata](/timed-automata/) give no probabilities. PRISM and Storm also have simulation engines next to their exact engines.
- **Randomized algorithms and protocols.** Estimating the success probability of a [Monte Carlo algorithm](/monte-carlo-algorithm/) on a fixed input is the same task, and [error amplification](/error-amplification/) uses the same [Chernoff bound](/chernoff-bound/).

## Variations

- **Strict thresholds.** $A = 1/\alpha$ and $B = \beta$ give $\alpha' \le \alpha$ and $\beta' \le \beta$ exactly (Corollary 5), for a slightly larger expected sample size.
- **Confidence intervals instead of Hoeffding.** The exact Clopper-Pearson interval, or other [binomial tail bounds](/binomial-tail-bounds/), give smaller sample sizes than Hoeffding's inequality when $p$ is near 0 or 1. The central limit approximation is smaller still, but it has no guarantee for a fixed $N$.
- **Sequential estimation.** Stop when a confidence interval is narrow enough, with a stopping rule that is designed for sequential use, such as the Chow-Robbins rule. A fixed-$N$ bound must not be checked again after each sample.
- **Bayesian SMC.** Put a prior on $p$, update it after each sample, and stop when the posterior probability of $p \ge \theta$ or of $p < \theta$ is high enough. This uses a Bayes factor in place of the likelihood ratio, as in work by Jha, Clarke and others from 2009.
- **Rare events.** [Importance sampling](/importance-sampling/) changes the transition probabilities so that the rare event is common, and weights each run by its likelihood ratio. Importance splitting restarts runs from intermediate levels. Both aim at a small *relative* error.
- **Nondeterminism.** For a Markov decision process, sample schedulers as well as runs, and report the best scheduler found. This gives a bound on one side only.
- **Unbounded properties.** If the chain has a known lower bound on the probability of stopping at each step, a run can be stopped at a random time with a known bias. Otherwise combine simulation with a graph analysis of the states from which $\Psi$ cannot be reached, as in [PCTL model checking](/pctl-model-checking/).
- **Runtime monitoring.** The same estimates and tests apply to logs of a real system, when the runs are independent and come from one distribution.

## Pitfalls

- **Wrong:** read $\alpha$ and $\beta$ of Wald's thresholds as exact error bounds. **Right:** they give $\alpha' \le \alpha/(1 - \beta)$ and $\beta' \le \beta/(1 - \alpha)$ by Theorem 4. Use the strict thresholds of Corollary 5 when $\alpha$ itself must be a bound.
- **Wrong:** expect a guarantee when $p$ is close to $\theta$. **Right:** inside the indifference region $(\theta - \varepsilon, \theta + \varepsilon)$ the test may answer either way, and with $p = \theta$ in the symmetric example it answers each way with probability $1/2$. With $\varepsilon = 0$, $p_0 = p_1$ and the test is not defined.
- **Wrong:** compute $N$ from Hoeffding's inequality and then stop as soon as the estimate looks clear. **Right:** the bound holds for the fixed $N$ only. Stopping on the data changes the error, and a sequential method must be designed as one, as the SPRT is.
- **Wrong:** use the absolute error $\varepsilon$ for a rare event. **Right:** with $p = 10^{-9}$, any $\varepsilon \ge 10^{-9}$ allows the answer 0, and a relative error of $\varepsilon p$ needs about $1/(\varepsilon^2 p)$ runs. Use importance sampling or splitting.
- **Wrong:** check many states or many properties, each with error $\delta$, and claim $\delta$ for all of them. **Right:** by the union bound, $k$ separate tests need error $\delta/k$ each for a joint error $\delta$.
- **Wrong:** cut unbounded runs at an arbitrary length and count them as failures. **Right:** that estimates a bounded property, which is a lower bound for the unbounded one. Report it as such, or bound the error of the cut.
- **Wrong:** reuse one random seed for each run, or use a weak generator. **Right:** the theorems assume independent runs with the correct distribution. Correlated runs can make the error much larger than the bound.

## Exercises

1. Compute $N$ for $\varepsilon = 0.001$ and $\delta = 10^{-6}$, and check the value $7254329$. How does $N$ change when $\delta$ is divided by 10?
2. For $\theta = 0.5$, $\varepsilon = 0.05$ and $\alpha = \beta = 0.05$, show that the test stops when the number of failures and the number of successes differ by 15, and derive $\alpha' = 1/(1 + (11/9)^{15})$ from the gambler's ruin.
3. In the same setting, show that the expected number of samples at $p = 0.5$ is $15^2 = 225$. Use the fact that $D_m^2 - m$ is a [martingale](/martingale/) for a fair walk $D_m$, and the [optional stopping theorem](/optional-stopping-theorem/).
4. Show that the strict thresholds of Corollary 5 give the same test as Wald's thresholds in the symmetric example, and find a choice of $\alpha$ and $\beta$ where they differ.
5. A model checker tests a nested formula $\mathcal{P}_{\ge 0.9}(\mathcal{F}^{\le 10}\, \mathcal{P}_{\ge 0.5}(\mathcal{X}\, a))$ by simulation. Explain why the error of the inner tests changes the success probability seen by the outer test, and give one way to bound the effect.

## References
