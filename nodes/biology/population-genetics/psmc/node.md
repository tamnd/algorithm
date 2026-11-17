---
tag: H1EZ3X
kind: algorithm
slug: psmc
name: Pairwise sequentially Markovian coalescent
aliases:
- PSMC
area: biology/population-genetics
level: research
summary: Infer past effective population size from one diploid genome with an HMM whose hidden states are binned coalescence times along the sequence.
model: real-ram
complexity:
  vars: {n: the number of bins, k: the number of time intervals, r: the number of EM iterations, m: the number of integration steps per interval, g: the number of line-search steps per size}
  time: {worst: Θ(r (n k^2 + g k^3 m)), average: Θ(r (n k^2 + g k^3 m)), best: Θ(r (n k^2 + g k^3 m))}
  space: {extra: Θ(n k + k^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2011
  people: [Heng Li, Richard Durbin]
  note: Li and Durbin published PSMC in 2011 and used it to infer the size histories of human populations from single diploid genomes.
prereqs: [sequentially-markov-coalescent, hidden-markov-model, forward-backward-algorithm, expectation-maximization, effective-population-size]
see_also: [baum-welch-algorithm, kingman-coalescent, coalescent-simulation, ancestral-recombination-graph-inference, simpsons-rule, golden-section-search, nucleotide-diversity, watterson-estimator]
sources:
  - paper: doi:10.1038/nature10231
    title: Heng Li and Richard Durbin, Inference of human population history from individual whole-genome sequences, Nature 475(7357), 2011
    locator: pp. 493-496 and the Supplementary Information (the hidden Markov model of the coalescence time, its transition and emission probabilities, the time intervals and the scaling to years)
  - paper: doi:10.1098/rstb.2005.1673
    title: Gilean A. T. McVean and Niall J. Cardin, Approximating the coalescent with recombination, Philosophical Transactions of the Royal Society B 360(1459), 2005
    locator: pp. 1387-1393 (the sequentially Markov coalescent, on which the transition of PSMC is based)
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989
    locator: pp. 257-286 (the scaled forward-backward procedure and the re-estimation of HMM parameters)
---

PSMC reads the history of a population from the genome of one diploid individual. The two copies of each chromosome have a common ancestor at some time in the past, and that time changes along the chromosome, because recombination gives different parts different ancestors. Where the time is long, the two copies differ at many sites; where it is short, they differ at few. PSMC is a [hidden Markov model](/hidden-markov-model/) along the genome whose hidden state is the coalescence time, put into $k$ intervals, and whose observations are the heterozygous and homozygous parts of the genome. The rate of coalescence at time $t$ is the inverse of the [effective population size](/effective-population-size/) at $t$, so the sizes that best explain the observations, found by [expectation maximization](/expectation-maximization/), give a history of $N(t)$. Li and Durbin introduced it in 2011.

## In plain words

Look at two copies of a chromosome and mark where they differ. The marks are not spread evenly. Some long stretches have many marks, and other long stretches have almost none. A stretch with many marks goes back a long time to its common ancestor, so mutations had a long time to build up. A stretch with few marks has a recent common ancestor.

So the genome gives many samples of coalescence times, one per stretch, from one person. If the population was small at some time in the past, many stretches found their common ancestor then, because two lineages meet fast in a small population. If it was large, few did. PSMC counts how many stretches, in effect, have each coalescence time, and turns those counts into population sizes. It does this without seeing the stretch boundaries: the HMM averages over all ways to cut the genome into stretches.

## The problem

**Input.** A sequence $o_1, \ldots, o_n$ of bins of $s$ bases along the genome of one diploid individual. A bin is 1 if it has at least one heterozygous site, 0 if it has none, and missing if too few of its bases were called. Time breaks $0 = t_0 < t_1 < \cdots < t_{k-1} < t_k = \infty$ in units of $2N_0$ generations, where $N_0$ is a reference size. The scaled mutation rate $\theta = 4N_0 \mu s$ and recombination rate $\rho = 4N_0 r s$ per bin.

**Output.** Relative sizes $\lambda_1, \ldots, \lambda_k$, with $N(t) = N_0 \lambda_j$ for $t$ in $[t_{j-1}, t_j)$, that locally maximize the likelihood of the bins.

**The model.** Let $\Lambda(t) = \int_0^t du / \lambda(u)$, the cumulative rate of coalescence of two lineages.

- **Hidden states.** State $j$ means that the coalescence time $T$ at the bin is in $[t_{j-1}, t_j)$. At the first bin, $T$ has the density $p(t) = e^{-\Lambda(t)} / \lambda(t)$, so $\pi_j = e^{-\Lambda(t_{j-1})} - e^{-\Lambda(t_j)}$.
- **Emission.** Given $T = t$, a bin is heterozygous with probability $1 - e^{-\theta t}$: on the path of length $2t$ between the two copies, mutations come at rate $\theta/2$ per unit of length. So $e_j = 1 - \frac{1}{\pi_j}\int_{t_{j-1}}^{t_j} p(t) e^{-\theta t}\, dt$.
- **Transition.** Between two neighbouring bins, with $T = t$, a recombination happens with probability $1 - e^{-\rho t}$. Then, as in the [sequentially Markov coalescent](/sequentially-markov-coalescent/), one lineage is cut at an age $u$ uniform on $(0, t)$ and coalesces again with the other lineage, going back from $u$ at rate $1/\lambda$. Otherwise $T$ stays the same. Integrating over the interval of $T$ gives the $k \times k$ matrix $A$.

## The algorithm

```pseudo id=main
PSMC(o_1..o_n, t_0..t_k, θ, ρ, λ)
L1  for each of R iterations do
L2      build π, A and e from λ, θ and ρ
L3      forward pass: α_1 ← π ∘ e(o_1), then α_i ← (α_{i−1} A) ∘ e(o_i), scaled to sum 1
L4      backward pass: β_n ← 1, then β_{i−1} ← A (e(o_i) ∘ β_i), with the same scales
L5      add up the expected counts: first state, transitions j → l, het and hom bins per state
L6      for j = 1, ..., k do change λ_j to raise Q(λ), the expected log-likelihood of the counts
L7  return λ
```

Here $e(o)$ is the vector of $e_j$ for a heterozygous bin, of $1 - e_j$ for a homozygous bin, and all ones for a missing bin. Lines L3 to L5 are the [forward-backward algorithm](/forward-backward-algorithm/): the posterior of state $j$ at bin $i$ is $\alpha_i(j)\beta_i(j)$, and the expected number of transitions $j \to l$ between bins $i - 1$ and $i$ is $\alpha_{i-1}(j) A_{jl}\, e_l(o_i) \beta_i(l) / c_i$, where $c_i$ is the scale of bin $i$. The log-likelihood is $\sum_i \ln c_i$.

$Q(\lambda)$ is the expected complete-data log-likelihood

$$Q(\lambda) = \sum_j F_j \ln \pi_j + \sum_{j,l} X_{jl} \ln A_{jl} + \sum_j \left(H_j \ln e_j + M_j \ln(1 - e_j)\right),$$

where $F$, $X$, $H$ and $M$ are the expected counts of line L5 and $\pi$, $A$, $e$ are computed from the new $\lambda$. Line L6 changes one $\ln \lambda_j$ at a time by a [golden-section search](/golden-section-search/) and keeps a change only if $Q$ goes up.

**The transition in closed form, up to one integral.** Write $G(x) = \int_0^x e^{\Lambda(u)} du$. With the cut at $u$, the new time $T'$ satisfies $P(T' \ge x) = e^{-(\Lambda(x) - \Lambda(u))}$ for $x \ge u$ and $1$ for $x < u$. Averaging over $u$ uniform on $(0, t)$,

$$\int_0^t P(T' \ge x \mid u)\, du = \begin{cases} e^{-\Lambda(x)} G(t), & x \ge t, \\ e^{-\Lambda(x)} G(x) + (t - x), & x < t. \end{cases}$$

Call this $H(t, x)$. Then the joint probability that $T$ is in interval $j$ and $T'$ is in interval $l$ is

$$J_{jl} = [j = l] \int_{t_{j-1}}^{t_j} p(t) e^{-\rho t}\, dt + \int_{t_{j-1}}^{t_j} p(t)\, \frac{1 - e^{-\rho t}}{t}\, \big(H(t, t_{l-1}) - H(t, t_l)\big)\, dt,$$

and $A_{jl} = J_{jl} / \pi_j$. The first integral has a closed form because $\lambda$ is constant on the interval. The implementation computes the second by the composite [Simpson rule](/simpsons-rule/), and $G$ in closed form, piece by piece. Li and Durbin give closed forms for the whole matrix.

**Time intervals.** The implementation spaces the breaks as $t_j = 0.1\left(e^{j \ln(1 + 10 t_{\max})/(k-1)} - 1\right)$ for $j < k$, dense near the present and sparse in the past, so that each interval holds a useful number of coalescences.

## Example

Take $k = 3$ intervals with breaks $0, 0.5, 1.5, \infty$, a constant size $\lambda = (1, 1, 1)$, $\theta = 0.05$ and $\rho = 0.01$ per bin.

- **Initial law.** $\pi = (1 - e^{-0.5},\ e^{-0.5} - e^{-1.5},\ e^{-1.5}) = (0.39347, 0.38340, 0.22313)$.
- **Emission.** For interval 1, $\int_0^{0.5} e^{-t} e^{-0.05t} dt = (1 - e^{-0.525})/1.05 = 0.38899$, so $e_1 = 1 - 0.38899/0.39347 = 0.01137$. In the same way $e = (0.01137, 0.04477, 0.11643)$: older states give more heterozygous bins.
- **Transition.** The rows of $A$ are $(0.998361, 0.001036, 0.000603)$, $(0.001060, 0.995370, 0.003570)$ and $(0.001052, 0.006090, 0.992858)$. A bin with an old common ancestor is more likely to have a recombination before the next bin, so the diagonal falls with the state.

For the five bins $0, 0, 1, 1, 0$, the log-likelihood is $-5.8766$, and the posterior of the third bin is $(0.0177, 0.2396, 0.7427)$. The two heterozygous bins pull the posterior of every bin toward the oldest state, because the states change rarely from one bin to the next.

For a fit, simulate $20\,000$ bins with $\theta = 0.1$, $\rho = 0.02$, breaks $0, 0.214, 0.887, 3, \infty$ and true sizes $(0.3, 1, 1, 1)$, and start EM at $(1, 1, 1, 1)$. Eight iterations raise the log-likelihood from $-2663.5$ to $-2645.3$ and give $\lambda = (0.17, 1.10, 0.87, 0.65)$. The fit finds the small recent size, but with only 738 heterozygous bins the estimates are noisy. A human genome has about $3 \times 10^7$ bins of 100 bases.

## Correctness

Lines L3 to L5 compute, for the HMM $(\pi, A, e)$, the exact likelihood of the bins and the exact posterior expectations of the counts of first states, transitions and emissions; this is the forward-backward algorithm, and a missing bin has emission 1 in every state. The transition formula follows from the model: with probability $e^{-\rho t}$ the time stays, and otherwise the new time has the law of $T'$ averaged over the cut age, whose tail is $H(t, x)/t$. Its row sums are $\pi_j$, so $A$ is a stochastic matrix.

For the sizes, $\ell(\lambda') - \ell(\lambda) \ge Q(\lambda') - Q(\lambda)$ when $Q$ is built from the posterior under $\lambda$, which is the basic inequality of EM. Line L6 accepts a new $\lambda'$ only when $Q(\lambda') > Q(\lambda)$, so the log-likelihood never goes down from one iteration to the next. Like all EM methods, it can stop at a local maximum. The full proof is below.

## Complexity

- **Forward-backward.** Each bin costs a vector-matrix product, $\Theta(k^2)$, so a pass costs $\Theta(n k^2)$ and stores $\Theta(n k)$ forward values.
- **Building the model.** The Simpson rule with $m$ points per interval, and $H$ at $k + 1$ breaks for each point, costs $\Theta(k^2 m)$ per matrix.
- **The M step.** Line L6 evaluates $Q$ about $g$ times for each of the $k$ sizes, each time with a new matrix, so it costs $\Theta(g k^3 m)$. It does not depend on $n$.
- **Total.** $\Theta(r(n k^2 + g k^3 m))$ time for $r$ iterations. For a genome, $n$ is in the tens of millions and $k$ is about 64, so the forward-backward passes dominate.

## Properties

- **One genome is enough.** The many local trees along the genome act as many partly independent samples of the coalescence time.
- **Inverse coalescence rate.** What PSMC estimates is the inverse of the coalescence rate of two lineages at each time. It equals the size only for a single population with random mating.
- **Approximate stationarity.** With recombination probability $1 - e^{-\rho t}$ per bin, the chain keeps the law $\pi$ only up to an error of order $\rho^2$. The rows of the joint matrix sum to $\pi$ exactly, and its columns only nearly.
- **Resolution.** Few pairs of copies coalesce in the very recent past or in the deep past, so the sizes there have large errors. With human data, the method has little power for the last 20 000 years or so.
- **Scale.** The fit gives $\theta$ and $\lambda$ in coalescent units. With a mutation rate $\mu$ per base per generation and a generation time $g$, $N_0 = \theta/(4\mu s)$, a break $t_j$ is $2 N_0 t_j g$ years, and $N(t) = N_0 \lambda_j$. Errors in $\mu$ and $g$ move the curve along both axes.

## Variants and improvements

- **The PSMC program.** It also estimates $\theta$ and $\rho$, uses closed-form transitions, and groups the 64 atomic intervals into fewer free parameters, for example a pattern of the form `4+25*2+4+6`, to keep the estimates stable. It adds a bootstrap over parts of the genome for confidence bands.
- **Faster transitions.** The transition matrices of SMC models have structure that lets the forward step run in $O(k)$ time per bin instead of $O(k^2)$ (Harris and coauthors).
- **More genomes.** MSMC uses several haplotypes and estimates the time of the first coalescence among them, which gives better resolution for the recent past, and the cross-coalescence rate between two populations. SMC++ combines one genome with the frequency spectrum of many.
- **Other methods.** ARG-based methods, see [ARG inference](/ancestral-recombination-graph-inference/), infer whole genealogies and then sizes from them.

## When to use it

Use it to get the broad size history of a population, or of a species with only a few sequenced genomes, away from the very recent and the very deep past. It needs a high-coverage genome of one diploid individual, a mutation rate and a generation time. For the recent past, or to estimate split times between populations, use methods with more genomes.

## Pitfalls

- **Structure looks like size change.** In a structured population, the inverse coalescence rate changes over time even when no deme changes size. A peak in the curve can be the trace of old structure, not of a large population.
- **Coverage and filtering.** Missed heterozygous sites at low coverage lower $\theta$ and shift the curve. Bins with repeats or bad mapping must be marked missing, not homozygous.
- **Fixed bins.** A bin of 100 bases is heterozygous at most once. If $\theta$ per bin is not small, many differences are lost; for very diverse species, use smaller bins.
- **Too many free parameters.** With one size per atomic interval, the estimates in the sparse intervals swing wildly. Group intervals.
- **Recent sizes.** Sizes in the first interval are often overestimated or noisy. Do not read sharp changes there.
- **Mutation rate and generation time.** The years and sizes are only as good as $\mu$ and $g$.

## Implementations

## History

Li and Durbin published PSMC in Nature in 2011 with genomes of individuals from several human populations, and it became the standard method to infer size history from single genomes. They based the transition on the sequentially Markov coalescent of McVean and Cardin (2005) and fitted it with the EM algorithm for HMMs. Schiffels and Durbin extended it to several haplotypes as MSMC in 2014.

## References
