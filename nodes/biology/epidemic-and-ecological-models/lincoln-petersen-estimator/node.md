---
tag: XD1A1J
kind: algorithm
slug: lincoln-petersen-estimator
name: "Lincoln-Petersen estimator"
aliases:
- capture-recapture estimator
- Lincoln index
area: biology/epidemic-and-ecological-models
level: intro
summary: Estimate a closed population size as M C / R, from M marked animals, C caught later and R of those that were marked.
model: real-ram
complexity:
  vars: {M: the number of animals in the first sample, C: the number of animals in the second sample}
  time: {worst: Θ((M + C) log M), average: Θ(M + C), best: Θ(M + C)}
  space: {extra: Θ(M)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1896
  people: [C. G. Johannes Petersen, Frederick C. Lincoln, Douglas G. Chapman]
  note: Petersen used marked plaice to estimate a fish stock in 1896, Lincoln used bird bands to estimate waterfowl numbers in 1930, and Chapman gave the modified form with R + 1 in 1951.
prereqs: [linearity-of-expectation]
see_also: [chao1-estimator, maximum-likelihood-estimation, method-of-moments, horvitz-thompson-estimator, delta-method, confidence-interval, bootstrap-method, distinct-elements-problem]
sources:
  - book: isbn:9780852642627
    title: George A. F. Seber, The Estimation of Animal Abundance and Related Parameters, second edition, Griffin, 1982
    locator: the chapter on closed populations with a single release of marked animals (the Petersen estimate, Chapman's form, its variance and the assumptions)
  - paper: "C. G. Johannes Petersen, The yearly immigration of young plaice into the Limfjord from the German Sea, Report of the Danish Biological Station 6, 1896"
    title: Petersen 1896
    locator: the use of marked plaice to estimate the size of the stock
  - paper: "Frederick C. Lincoln, Calculating waterfowl abundance on the basis of banding returns, United States Department of Agriculture Circular 118, 1930, pages 1 to 4"
    title: Lincoln 1930
    locator: the ratio of banded birds among the birds shot as an estimate of the total number
  - paper: "Douglas G. Chapman, Some properties of the hypergeometric distribution with applications to zoological sample censuses, University of California Publications in Statistics, 1951"
    title: Chapman 1951
    locator: the hypergeometric model of the second sample and the modified estimate (M + 1)(C + 1)/(R + 1) - 1
---

The Lincoln-Petersen estimator gives the size $N$ of a closed animal population from two samples. Catch $M$ animals, mark them and release them. Later, catch $C$ animals and count the $R$ among them that carry a mark. If the marked fraction of the second sample is the same as the marked fraction of the population, then $R / C \approx M / N$, so $\hat N = M C / R$. The estimate has no value when $R = 0$, and its expected value is too high when $R$ is small. Chapman's form $(M + 1)(C + 1)/(R + 1) - 1$ is always defined, and it is exactly unbiased when $N \le M + C$. This page computes both forms and a variance estimate from the two lists of animal identifiers.

## In plain words

You want to know how many fish live in a pond, but you cannot count them all. Catch some fish, put a tag on each, and let them go. Wait until the tagged fish mix with the others. Then catch fish again and look at how many of them have a tag.

If one fish in five of the second catch has a tag, then you guess that one fish in five of the whole pond has a tag. You know how many fish you tagged, so the whole pond holds about five times that number.

This works only if the pond is the same between the two catches, the tags stay on, and a tagged fish is as easy to catch as any other fish. When very few tagged fish come back, the guess is unstable, so a small correction is used.

## The problem

**Input.** Two lists of animal identifiers. The first list holds the $M$ distinct animals of the first sample, which were marked and released. The second list holds the $C$ distinct animals of the second sample.

**Model.** The population is closed: the same $N$ animals are present at both samples, with no births, deaths or movement in or out. Marks are not lost and are read correctly. The second sample is a simple random sample: every set of $C$ animals has the same probability, whatever the marks are. Then the number $R$ of marked animals in the second sample has the hypergeometric distribution

$$\Pr(R = r) = \frac{\binom{M}{r}\binom{N - M}{C - r}}{\binom{N}{C}}, \qquad \mathbb{E}[R] = \frac{M C}{N}.$$

**Output.** The counts $M$, $C$ and $R$, the Lincoln-Petersen estimate $\hat N_{LP} = M C / R$ (no value when $R = 0$), Chapman's estimate $\hat N_C$ and the variance estimate $\hat V_C$ of $\hat N_C$.

## The algorithm

```pseudo id=main
LINCOLN-PETERSEN(first, second)
L1  marked ← the set of identifiers in first; M ← |marked|
L2  C ← the number of identifiers in second
L3  R ← the number of identifiers in second that are in marked
L4  N_C ← (M + 1)(C + 1) / (R + 1) - 1
L5  V_C ← (M + 1)(C + 1)(M - R)(C - R) / ((R + 1)^2 (R + 2))
L6  if R = 0 then N_LP ← no value else N_LP ← M C / R
L7  return (M, C, R, N_LP, N_C, V_C)
```

Lines L1 to L3 reduce the two lists to the three counts. Line L1 builds a set, so that line L3 tests each animal of the second sample in expected constant time. Line L4 is Chapman's estimate. It equals the Lincoln-Petersen estimate of a population with one extra animal that is in both samples, minus that animal. Line L5 is the variance estimate of $\hat N_C$ that Seber gives. Line L6 is the classic estimate, the value of $N$ that makes $\mathbb{E}[R]$ equal to the observed $R$.

## Example

The first sample holds the animals 3, 7, 12, 18, 25 and 31. The second sample holds the animals 2, 7, 9, 18, 22, 25, 30 and 33.

| line | what it computes | value |
|---|---|---|
| L1 | marked = {3, 7, 12, 18, 25, 31} | $M = 6$ |
| L2 | the size of the second sample | $C = 8$ |
| L3 | 7, 18 and 25 are marked | $R = 3$ |
| L4 | $7 \cdot 9 / 4 - 1$ | $\hat N_C = 59/4 = 14.75$ |
| L5 | $7 \cdot 9 \cdot 3 \cdot 5 / (16 \cdot 5)$ | $\hat V_C = 189/16 = 11.8125$ |
| L6 | $6 \cdot 8 / 3$ | $\hat N_{LP} = 16$ |

The two samples hold $6 + 8 - 3 = 11$ distinct animals, so $N \ge 11$ in any case. The standard error of $\hat N_C$ is about $\sqrt{11.8125} = 3.44$.

With larger samples, $M = 50$, $C = 40$ and $R = 10$ give $\hat N_{LP} = 2000 / 10 = 200$, $\hat N_C = 51 \cdot 41 / 11 - 1 = 2080/11 = 189.091$ and $\hat V_C = 209100/121 = 1728.10$, so the standard error is about $41.6$. A normal interval $189.1 \pm 1.96 \cdot 41.6$ is about $(107.6, 270.6)$. It is only a rough guide, because $\hat N_C$ has a skewed distribution.

## Correctness

Lines L1 to L3 count $M$, $C$ and $R$ exactly, because both samples are lists of distinct identifiers. The statistical claims hold in the model of "The problem". Line L6 is the moment estimate: $\mathbb{E}[R] = M C / N$, and $\hat N_{LP}$ solves $R = M C / N$ for $N$. For $R \ge 1$, the maximum likelihood estimate of the integer $N$ is $\lfloor M C / R \rfloor$, the classic estimate rounded down. Chapman's estimate of line L4 has the exact mean

$$\mathbb{E}[\hat N_C] = N - (N - M - C)\Pr(R = 0) \quad \text{when } N \ge M + C,$$

and $\mathbb{E}[\hat N_C] = N$ exactly when $N \le M + C$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Time.** Line L1 inserts $M$ identifiers into a set, and line L3 makes $C$ membership tests. With a hash table this is $\Theta(M + C)$ expected time. With a balanced search tree, or with a sorted array and binary search, it is $\Theta((M + C) \log M)$ in the worst case. Lines L4 to L6 do a fixed number of arithmetic operations on the counts. When the three counts are given directly, the whole estimate costs $\Theta(1)$.

**Space.** The set of line L1 holds $M$ identifiers, so the extra space is $\Theta(M)$.

## Properties

- **Moment estimate (theorem).** $\mathbb{E}[R] = M C / N$ by [linearity of expectation](/linearity-of-expectation/): each of the $C$ animals of the second sample is marked with probability $M / N$. Line L6 sets $R$ equal to this mean.
- **Likelihood (theorem).** For $R \ge 1$, the hypergeometric likelihood of $N$ increases while $N \le M C / R$ and decreases after that. So $\lfloor M C / R \rfloor$ is the largest maximizer. When $M C / R$ is an integer, $M C / R - 1$ has the same likelihood.
- **Bias of the classic estimate (theorem).** If $N > M + C$, then $\Pr(R = 0) > 0$, and $\hat N_{LP}$ has no finite mean. Given $R \ge 1$ its mean is finite, but it can be much larger than $N$: for $N = 200$, $M = 50$ and $C = 40$ it is $214.5$ (an exact sum over the hypergeometric law). This is the reason for Chapman's form.
- **Bias of Chapman's form (theorem).** The bias is $-(N - M - C)\Pr(R = 0)$, which is very small when $M C / N$ is not small. For $N = 200$, $M = 50$ and $C = 40$, $\Pr(R = 0) = 2.15 \times 10^{-6}$ and $\mathbb{E}[\hat N_C] = 199.99976$.
- **Variance (known result).** $\hat V_C$ of line L5 is the variance estimate in Seber's book, and it is approximately unbiased in the hypergeometric model. For $N = 200$, $M = 50$ and $C = 40$, the exact standard deviation of $\hat N_C$ is $52.5$.
- **Not exact.** The arithmetic is exact in rational numbers, but the output is an estimate. Its error comes from the sampling and from any failure of the model.

## Variants and improvements

- **Chapman's form.** Line L4. It is the standard choice for one release and one recapture.
- **Sampling with replacement.** If the second sample can see the same animal more than once (camera traps, or a sample that is returned at once), $R$ is binomial. Bailey's form $M (C + 1)/(R + 1)$ is the corresponding bias-corrected estimate.
- **Horvitz-Thompson view.** $R / M$ estimates the probability that an animal is in the second sample, and $C$ divided by that probability is $\hat N_{LP}$. This is a [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) with an estimated inclusion probability.
- **Many samples.** The Schnabel census combines a sequence of samples into one estimate. Models for open populations, such as Jolly-Seber, also estimate survival and recruitment.
- **Unequal catchability.** If some animals are easier to catch, $\hat N_{LP}$ is too low. Chao (1987) gives a lower bound for $N$ from the numbers of animals caught once and twice in many samples, the same idea as the [Chao1 estimator](/chao1-estimator/) of species richness.
- **Interval estimates.** The [delta method](/delta-method/) on $\log \hat N$, the profile likelihood, or a parametric [bootstrap](/bootstrap-method/) from the hypergeometric model give better [confidence intervals](/confidence-interval/) than the normal interval when $R$ is small.

## When to use it

Use it for a closed population with two samples close in time, and with marks that stay on. It needs only three counts and no model fit. Design the study so that the expected $R$ is at least about 10. With fewer recaptures the estimate is very unstable, and the normal interval is not useful. When there are three or more samples, or when catchability varies between animals or over time, use a model that estimates this variation, for example the Chao (1987) bound or the models in Seber's book. For counts of species instead of animals, use the [Chao1 estimator](/chao1-estimator/).

## Pitfalls

- **No recaptures.** When $R = 0$, the division at line L6 is not defined. Return no value at line L6 and report Chapman's estimate of line L4, which is $(M + 1)(C + 1) - 1$ in this case and is a rough guess, not a reliable value.
- **Counting the same animal twice.** Line L3 must count distinct marked animals. If an animal can appear twice in the second list (it was photographed twice), $C$ and $R$ are both too large. Remove the repeats before line L2, or use a model for sampling with replacement.
- **Trap response.** Animals that learn to avoid the trap make $R$ too small, and $\hat N$ too large at line L6. Animals that come back for the bait do the opposite. No line of the algorithm can find this from one pair of samples.
- **Mark loss and an open population.** Lost marks make $R$ too small and $\hat N$ too large. Deaths of marked animals between the samples have the same effect. Births and immigration between the samples add unmarked animals, and the estimate then refers to the second sample time.
- **Normal intervals.** $\hat N \pm 1.96 \sqrt{\hat V_C}$ from line L5 can go below $M + C - R$, the number of animals seen. Use an interval on the log scale or a profile likelihood interval when $R$ is small.

## Implementations

## History

Petersen marked young plaice in the Limfjord in Denmark in the 1890s, and in 1896 he used the fraction of marked fish in later catches to estimate the stock. Lincoln used the returns of bands from ducks shot by hunters to estimate the number of waterfowl in North America in 1930, and the ratio became known as the Lincoln index. Laplace used the same ratio to estimate the population of France at the end of the eighteenth century, with registered births in place of marks. Chapman worked out the hypergeometric model of the second sample in 1951 and proposed the form with $R + 1$. Seber's book of 1973, with a second edition in 1982, collected the theory of capture-recapture for closed and open populations.

## References
