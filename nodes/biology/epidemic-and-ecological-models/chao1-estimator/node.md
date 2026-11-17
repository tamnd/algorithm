---
tag: A0Z4WE
kind: algorithm
slug: chao1-estimator
name: "Chao1 estimator"
aliases:
- Chao1 species richness estimator
area: biology/epidemic-and-ecological-models
level: core
summary: Estimate the number of species including unseen ones as the observed count plus f1^2 / (2 f2), from singletons and doubletons.
model: real-ram
complexity:
  vars: {n: the number of individuals in the sample, s: the number of observed species}
  time: {worst: Θ(n log s), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(s)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1984
  people: [Anne Chao]
  note: Chao proposed f1^2 / (2 f2) for the number of unseen classes in 1984, used the same bound for capture-recapture with unequal catchability in 1987, and later gave the bias-corrected form.
prereqs: [poisson-distribution]
see_also: [lincoln-petersen-estimator, good-turing-estimation, stads-residual-risk, rarefaction, shannon-diversity-index, coupon-collector-problem, distinct-elements-problem, sequencing-coverage]
sources:
  - paper: "Anne Chao, Nonparametric estimation of the number of classes in a population, Scandinavian Journal of Statistics 11, 1984, pages 265 to 270"
    title: Chao 1984
    locator: the lower bound for the number of classes from the numbers of classes seen once and twice
  - paper: doi:10.2307/2531532
    title: Anne Chao, Estimating the population size for capture-recapture data with unequal catchability, Biometrics 43(4), 1987
    locator: pages 783 to 791 (the estimate from the animals caught once and twice, and its variance)
  - book: isbn:9780199580675
    title: Nicholas J. Gotelli and Robert K. Colwell, Estimating species richness, Chapter 4 of Anne E. Magurran and Brian J. McGill (editors), Biological Diversity, Frontiers in Measurement and Assessment, Oxford University Press, 2011
    locator: Chapter 4 (the classic and the bias-corrected forms of Chao1, and their use with rarefaction curves)
  - paper: doi:10.1111/biom.12200
    title: Chun-Huo Chiu, Yi-Ting Wang, Bruno A. Walther and Anne Chao, An improved nonparametric lower bound of species richness via a modified Good-Turing frequency formula, Biometrics 70(3), 2014
    locator: pages 671 to 682 (the factor (n - 1)/n under sampling of individuals, and the improved bound iChao1 from f3 and f4)
---

The Chao1 estimator gives a lower estimate of the number of species $S$ in a community from one sample of $n$ individuals. Rare species are the ones that a sample misses, and the sample shows how many rare species there are: $f_1$ species have one individual in the sample (singletons) and $f_2$ species have two (doubletons). Chao's estimate is $\hat S = S_{obs} + f_1^2 / (2 f_2)$. When $f_1$ is large compared with $f_2$, many species are still unseen. When $f_1 = 0$, the sample has probably found all species. The formula is not a guess at the shape of the species abundance distribution. It comes from an inequality that holds for every community, so its expected value is a lower bound of the true richness, up to the error of replacing expected counts with observed ones.

## In plain words

You walk through a forest and write down the species of every bird you see. At the end you have a list of species and how many birds of each one you saw.

Some species you saw many times. Some you saw only once, and some only twice. The species you saw only once are a warning: if there are many of them, there must be other rare species that you did not see at all. If almost every species turned up at least twice, you probably saw nearly all of them.

The method adds to the number of species you saw a correction that is large when once-seen species are common and twice-seen species are few. The answer is a careful lower guess, not the exact number.

## The problem

**Input.** A sample of $n$ individuals, given as the list of their species labels.

**Model.** The community has $S$ species with relative abundances $p_1, \ldots, p_S > 0$ that sum to 1. The $n$ individuals are drawn independently, and each one belongs to species $i$ with probability $p_i$ (multinomial sampling). Let $X_i$ be the number of individuals of species $i$ in the sample, and $f_k$ the number of species with $X_i = k$. Then $S_{obs} = S - f_0$, and $f_0$, the number of unseen species, is what the estimate must supply.

**Output.** $n$, $S_{obs}$, $f_1$, $f_2$, the classic estimate $S_{obs} + f_1^2 / (2 f_2)$ (no value when $f_2 = 0$), the bias-corrected estimate $S_{obs} + f_1 (f_1 - 1)/(2 (f_2 + 1))$, and Chao's variance estimate of the classic form.

## The algorithm

```pseudo id=main
CHAO1(sample)
L1  count ← an empty map; for each label x in sample: count[x] ← count[x] + 1
L2  n ← the length of sample; S_obs ← the number of keys of count
L3  f1 ← the number of species with count 1; f2 ← the number of species with count 2
L4  S_bc ← S_obs + f1 (f1 - 1) / (2 (f2 + 1))
L5  if f2 = 0 then S_classic ← no value; V ← no value
L6  else q ← f1 / f2; S_classic ← S_obs + q f1 / 2; V ← f2 (q^4 / 4 + q^3 + q^2 / 2)
L7  return (n, S_obs, f1, f2, S_classic, S_bc, V)
```

Line L1 counts the individuals of each species. Lines L2 and L3 reduce the counts to the frequency counts that the estimate uses: the number of species, the singletons and the doubletons. Line L4 is the bias-corrected form, which has a value for every sample. Line L6 is the classic form, since $q f_1 / 2 = f_1^2 / (2 f_2)$, and Chao's (1987) variance estimate. Line L5 skips both when there are no doubletons.

## Example

A sample of $n = 16$ birds has 5 of species A, 3 of B, 2 each of C and D, and 1 each of E, F, G and H.

| line | what it computes | value |
|---|---|---|
| L1 | counts A 5, B 3, C 2, D 2, E 1, F 1, G 1, H 1 | 8 keys |
| L2 | the sample size and the observed species | $n = 16$, $S_{obs} = 8$ |
| L3 | singletons E, F, G, H; doubletons C, D | $f_1 = 4$, $f_2 = 2$ |
| L4 | $8 + 4 \cdot 3 / (2 \cdot 3)$ | $S_{bc} = 10$ |
| L6 | $q = 2$, $8 + 2 \cdot 4 / 2$, $2 (4 + 8 + 2)$ | $S_{classic} = 12$, $V = 28$ |

The form with the factor $(n - 1)/n$ (see "Variants and improvements") gives $8 + (15/16) \cdot 4 = 11.75$. For a larger sample with $S_{obs} = 20$, $f_1 = 6$ and $f_2 = 3$, the classic form gives $20 + 36 / 6 = 26$, the bias-corrected form gives $20 + 30 / 8 = 23.75$, and the variance estimate is $3 (4 + 8 + 2) = 42$.

## Correctness

Lines L1 to L3 compute $n$, $S_{obs}$, $f_1$ and $f_2$ exactly. The statistical claim is a theorem about expected values. For multinomial sampling of $n$ individuals,

$$\mathbb{E}[f_0] \ge \frac{n - 1}{n} \cdot \frac{\mathbb{E}[f_1]^2}{2\, \mathbb{E}[f_2]},$$

with equality if and only if all $S$ species have the same abundance. Under Poisson sampling the same bound holds without the factor $(n - 1)/n$. The proof is the Cauchy-Schwarz inequality on $\sum_i p_i (1 - p_i)^{n - 1}$. Line L6 puts the observed $f_1$ and $f_2$ in place of their expected values. So the estimate targets a lower bound of $S$, and the step from expected to observed counts is a plug-in, not a theorem. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Time.** Line L1 does $n$ map updates. With a hash map this is $\Theta(n)$ expected time, and with a balanced search tree it is $\Theta(n \log s)$ in the worst case, for $s = S_{obs}$ keys. Line L3 reads the $s$ counts once, in $\Theta(s) \subseteq O(n)$ time. Lines L4 to L6 do a fixed number of arithmetic operations.

**Space.** The map holds $s$ keys and their counts, so the extra space is $\Theta(s)$. The algorithm is online: it can read the sample as a stream and keep only the map, and it can then report the estimate after any prefix.

## Properties

- **A lower bound (theorem).** The expected-value form is at most $S$ for every community, by the inequality above. It is equal to $S$ only when all abundances are equal. A community with many very rare species can have far more species than any estimate from $f_1$ and $f_2$ shows.
- **Never below the observed count (theorem).** Both forms are at least $S_{obs}$, and both are equal to $S_{obs}$ when $f_1 = 0$. The bias-corrected form is smaller than the classic form when $f_1 \ge 1$ and $f_2 \ge 1$, because $f_1 - 1 < f_1$ and $f_2 + 1 > f_2$.
- **When $f_2 = 0$.** The classic form has no value. The bias-corrected form gives $S_{obs} + f_1 (f_1 - 1)/2$, which is a large correction. A sample with no doubletons is too small for a reliable estimate.
- **Behavior in a simulation (measurement).** Take $S = 30$ species with $p_i$ proportional to $1/i$ and $n = 100$. The exact values are $\mathbb{E}[S_{obs}] = 24.12$ and a lower bound of $29.15$ from the inequality. In 2000 samples drawn with Python's `random.Random(5).choices`, the bias-corrected form had mean $29.18$, the classic form had mean $31.43$ over the 1999 samples with $f_2 > 0$, and $S_{obs}$ had mean $24.16$.
- **Variance (known result).** $V$ of line L6 is the variance estimate of Chao (1987), a large-sample approximation of the same kind as the [delta method](/delta-method/). Confidence intervals are usually built on the log of $\hat S - S_{obs}$, so that the lower end is not below $S_{obs}$.

## Variants and improvements

- **The factor $(n - 1)/n$.** Under multinomial sampling of individuals the bound is $S_{obs} + \frac{n - 1}{n} \frac{f_1^2}{2 f_2}$. The factor matters only for small $n$.
- **Bias-corrected form.** Line L4 is the form in Gotelli and Colwell (2011), and it has a value when $f_2 = 0$. With the factor it is $S_{obs} + \frac{n - 1}{n} \frac{f_1 (f_1 - 1)}{2 (f_2 + 1)}$.
- **iChao1.** Chiu, Wang, Walther and Chao (2014) add a term from $f_3$ and $f_4$ that makes the bound sharper.
- **Chao2.** For incidence data (the presence or absence of each species in each of several sampling units), replace $f_1$ and $f_2$ with the numbers of species found in one and in two units. The same argument applies.
- **ACE and the jackknife.** The abundance-based coverage estimator uses all rare species, not only singletons and doubletons, and the jackknife estimators use $f_1$ and $f_2$ with other weights. They are not lower bounds.
- **Capture-recapture.** Chao (1987) uses the same bound for the number of animals in a population with unequal catchability, with the numbers of animals caught once and twice. With equal catchability and two samples, the [Lincoln-Petersen estimator](/lincoln-petersen-estimator/) is the simpler tool.
- **Other fields.** [Good-Turing estimation](/good-turing-estimation/) uses the same $f_1$ to estimate the total probability of unseen words, and [STADS](/stads-residual-risk/) uses these ideas to estimate how much behavior a fuzzer has not yet found.

## When to use it

Use it when you need a minimum number of species, and the sample is a set of individuals (or reads, or words) drawn from one community. It needs only the frequency counts, and it makes no assumption on the shape of the abundance distribution. Report it together with $S_{obs}$, $n$, $f_1$, $f_2$ and an interval. To compare communities sampled with different effort, put the estimate next to the [rarefaction](/rarefaction/) curves of the samples. Do not use it as an estimate of the exact richness of a community with a long tail of very rare species: the true value can be much higher.

## Pitfalls

- **No doubletons.** Line L6 divides by $f_2$. When $f_2 = 0$, skip it at line L5 and report the bias-corrected form of line L4, and say that the sample is very small.
- **Counting errors make singletons.** A single misidentified individual or a sequencing error creates a false species with count 1. This raises $f_1$ at line L3, and the estimate grows by about $f_1 / f_2$ for each false singleton. In amplicon sequencing data, denoise the reads before line L1, and do not use Chao1 on data from which singletons were removed.
- **Pooled samples.** Line L1 assumes one sample from one community. Pooling samples from different habitats mixes communities, and the estimate then refers to no real community.
- **Reading it as an exact count.** The theorem gives a lower bound. Do not report $S_{classic}$ as the true number of species.

## Implementations

## History

Fisher, Corbet and Williams fitted a log-series distribution to the counts of moths and butterflies in 1943, an early parametric approach to the number of unseen species. In 1953 I. J. Good published the frequency formulas that he had worked out with Alan Turing during the war, with the estimate $f_1 / n$ for the total probability of unseen species. Anne Chao gave the nonparametric lower bound $S_{obs} + f_1^2 / (2 f_2)$ for the number of classes in 1984, and in 1987 she applied it to capture-recapture data with unequal catchability. The bias-corrected form came later from Chao's group, and Chiu, Wang, Walther and Chao gave the sharper bound iChao1 in 2014. Chao1 became a standard tool in ecology through programs such as EstimateS, and in microbiology through amplicon sequencing.

## References
