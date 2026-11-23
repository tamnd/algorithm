---
tag: CG87A2
kind: definition
slug: differential-privacy-definition
name: Differential privacy
aliases:
- pure differential privacy
- epsilon-differential privacy
area: security-and-privacy/differential-privacy
level: intro
summary: A randomized algorithm is epsilon-DP if changing one record changes the probability of each output set by at most a factor e^epsilon.
prereqs: [randomized-algorithm, conditional-probability]
see_also: [approximate-differential-privacy, global-sensitivity, randomized-response, laplace-mechanism, post-processing-theorem, group-privacy-theorem, sequential-composition-theorem, local-differential-privacy]
sources:
  - paper: doi:10.1007/11681878_14
    title: "Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith, Calibrating noise to sensitivity in private data analysis, TCC 2006, LNCS 3876, pages 265 to 284"
    locator: the first form of the definition, with a bound on the ratio of output probabilities for datasets that differ in one row
  - paper: doi:10.1007/11787006_1
    title: "Cynthia Dwork, Differential privacy, ICALP 2006, LNCS 4052, pages 1 to 12"
    locator: the name differential privacy and the argument that a guarantee of this kind is needed
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 2.3, Definition 2.3 (distance between databases), Definition 2.4 (differential privacy, with delta = 0 for the pure form), Proposition 2.1 and Theorem 2.2; Section 2.3.1 (what differential privacy promises)"
---

Differential privacy is a property of a randomized algorithm that reads a dataset. The algorithm is $\varepsilon$-differentially private ($\varepsilon$-DP) if adding, removing or changing one record changes the probability of every set of outputs by at most a factor $e^{\varepsilon}$. So the output looks almost the same whether or not any one person's data is in the input, and an observer learns almost nothing about that person that the observer could not learn without the data. Dwork, McSherry, Nissim and Smith (2006) gave the definition, and Dwork (2006) gave it its name. This page defines the pure form; the [approximate form](/approximate-differential-privacy/) adds a small additive term $\delta$.

## Definition

A **dataset** is a list $x = (x_1, \ldots, x_n)$ of records from a universe $\mathcal X$, or its histogram in $\mathbb N^{|\mathcal X|}$. Two datasets are **neighbors**, written $x \sim x'$, if they differ in one record. There are two neighbor relations, and every claim of privacy must say which one it uses:

- **add/remove** (unbounded): $x'$ is $x$ with one record added or removed, so the sizes differ by 1. Dwork and Roth use histograms with $\lVert x - x' \rVert_1 \le 1$, which is this relation.
- **replace** (bounded): $x$ and $x'$ have the same size $n$, and one record is changed.

A **mechanism** $M$ is a [randomized algorithm](/randomized-algorithm/) that takes a dataset and returns an output in a set $\mathcal Y$. Its randomness comes only from its own coins.

**Definition.** Let $\varepsilon \ge 0$. A mechanism $M$ is **$\varepsilon$-differentially private** under a neighbor relation $\sim$ if, for all $x \sim x'$ and all sets $S \subseteq \mathcal Y$ of outputs,

$$\Pr[M(x) \in S] \le e^{\varepsilon}\Pr[M(x') \in S].$$

The probability is over the coins of $M$ only; the datasets are fixed. Both relations are symmetric, so the bound also holds with $x$ and $x'$ swapped. A smaller $\varepsilon$ is a stronger guarantee. Values from 0.1 to a few units are common; $e^{0.1} = 1.105$ and $e^{1} = 2.718$.

For a finite or countable $\mathcal Y$, the definition is the same as the pointwise bound $\Pr[M(x) = y] \le e^{\varepsilon}\Pr[M(x') = y]$ for every output $y$: the pointwise bound is the case $S = \{y\}$, and the sum over $y \in S$ gives the set bound. For outputs with densities $p_x$ and $p_{x'}$, a bound $p_x(y) \le e^{\varepsilon} p_{x'}(y)$ for every $y$ is enough. In terms of the **privacy loss** $L(y) = \ln(\Pr[M(x) = y] / \Pr[M(x') = y])$, the mechanism is $\varepsilon$-DP if and only if $|L(y)| \le \varepsilon$ for every output $y$ that has positive probability, for every pair of neighbors.

Three equivalent readings help to use the definition.

1. **Odds.** Let an observer have a prior on whether the input is $x$ or $x'$. After seeing any output $y$, by [Bayes' theorem](/bayes-theorem/) the posterior odds are the prior odds times $\Pr[M(x) = y]/\Pr[M(x') = y]$, which lies in $[e^{-\varepsilon}, e^{\varepsilon}]$. With prior probability 0.01 for $x$ and $\varepsilon = 1$, the posterior probability of $x$ is at most $0.01e/(0.01e + 0.99) = 0.026724$.
2. **Tests.** Any test that decides between $x$ and $x'$ from the output, with false positive rate $\alpha$ and false negative rate $\beta$ (see [type I and type II errors](/type-i-and-type-ii-errors/)), has $\alpha + e^{\varepsilon}\beta \ge 1$ and $e^{\varepsilon}\alpha + \beta \ge 1$. Proof: if the test says "$x'$" on the output set $S$, then $\alpha = \Pr[M(x) \in S]$ and $1 - \beta = \Pr[M(x') \in S] \le e^{\varepsilon}\alpha$; the other bound is the same with the roles swapped. For $\varepsilon = 1$ and $\alpha = 0.05$, $\beta \ge 1 - 0.05e = 0.864$.
3. **Harm.** For any future event that depends only on the output, the probability that a person faces it changes by at most the factor $e^{\varepsilon}$ when the person's record is added or removed (Dwork-Roth Section 2.3.1).

The definition does not promise that nothing can be learned about a person. If the data show that smokers often get cancer, a smoker is affected by that result whether or not the smoker is in the data. The definition only bounds the effect of the presence of one record.

## Examples and non-examples

**Randomized response.** Each person reports a true bit with probability $3/4$ and the flipped bit with probability $1/4$. The ratio of the probabilities of any answer for two values of the bit is at most $(3/4)/(1/4) = 3$, so the release of all answers is $\ln 3$-DP under replace, where one person changes the bit. See [randomized response](/randomized-response/).

**Laplace mechanism.** Release a count plus noise with density $\frac{\varepsilon}{2}e^{-\varepsilon|z|}$. A count changes by at most 1 between neighbors, and the density ratio at each output is at most $e^{\varepsilon}$. So the output is $\varepsilon$-DP under both relations. See [Laplace mechanism](/laplace-mechanism/) and [global sensitivity](/global-sensitivity/).

**The relation matters.** Release a histogram with $\mathrm{Lap}(1/\varepsilon)$ noise on each bin. Under add/remove one bin changes by 1, and the release is $\varepsilon$-DP. Under replace two bins change by 1, and the same release is only $2\varepsilon$-DP. In general $\varepsilon$-DP under add/remove gives $2\varepsilon$-DP under replace, because a replace step is a removal followed by an addition (the [group privacy theorem](/group-privacy-theorem/) with $k = 2$). The converse fails: a mechanism that publishes $n$ exactly is $0$-DP under replace and is not DP for any $\varepsilon$ under add/remove.

**Constant output.** A mechanism that ignores the data and returns a fixed value or a fixed random value is $0$-DP. It is private and useless; the definition measures privacy, not utility.

**Non-example: an exact count.** A deterministic count $f(x)$ is not $\varepsilon$-DP for any $\varepsilon$: for neighbors with $f(x) \ne f(x')$, the set $S = \{f(x)\}$ has probability 1 under $x$ and 0 under $x'$. Every nonconstant deterministic function of the data fails the same way, so every DP mechanism with useful output is randomized.

**Non-example: a sample of the records.** Publish each record independently with probability $0.01$. A record that is in $x$ and not in $x'$ appears in the output with probability $0.01$ under $x$ and 0 under $x'$, so the release is not $\varepsilon$-DP for any $\varepsilon$. It is $(0, 0.01)$-DP in the [approximate](/approximate-differential-privacy/) sense, which shows why $\delta$ must be very small.

**Non-example: k-anonymity.** A table that is [k-anonymous](/k-anonymity/) is the output of a deterministic map of the data, and it is not DP. It can also leak a sensitive value when all the records of a group share it.

## Related definitions

- **Approximate DP.** [$(\varepsilon, \delta)$-DP](/approximate-differential-privacy/) adds $\delta$ to the right side of the bound. Pure DP is the case $\delta = 0$.
- **Sensitivity.** The [global sensitivity](/global-sensitivity/) of a query is the largest change between neighbors. It sets the noise of the Laplace and the Gaussian mechanisms.
- **Basic properties.** DP survives any processing of the output that does not read the data ([post-processing theorem](/post-processing-theorem/)). Two releases with $\varepsilon_1$ and $\varepsilon_2$ are $(\varepsilon_1 + \varepsilon_2)$-DP together ([sequential composition theorem](/sequential-composition-theorem/)). A group of $k$ records gets $k\varepsilon$ ([group privacy theorem](/group-privacy-theorem/)).
- **Local DP.** In [local differential privacy](/local-differential-privacy/) each person randomizes the record before it leaves the device, and the bound holds for any two values of one record. The curator is not trusted.
- **Divergence forms.** [Renyi DP](/renyi-differential-privacy/), [zero-concentrated DP](/zero-concentrated-differential-privacy/) and [Gaussian DP](/gaussian-differential-privacy/) bound other measures of the distance between $M(x)$ and $M(x')$. Pure $\varepsilon$-DP is the bound on the largest privacy loss, the Renyi divergence of order $\infty$.
- **Metric forms.** [Geo-indistinguishability](/geo-indistinguishability/) replaces the neighbor relation by a distance between locations, with the bound $e^{\varepsilon d(x, x')}$.
- **Noninterference.** [Noninterference](/noninterference/) asks that public outputs do not depend on secret inputs at all. DP allows a bounded dependence, which is what makes useful statistics possible.

## References
