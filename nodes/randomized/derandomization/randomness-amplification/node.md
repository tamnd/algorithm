---
tag: Q78DHE
kind: problem
slug: randomness-amplification
name: Randomness amplification
aliases:
- error reduction with few random bits
- deterministic amplification
- randomness-efficient error reduction
area: randomized/derandomization
level: advanced
summary: Reduce the error probability of a randomized algorithm while using as few random bits as possible.
prereqs: [error-amplification, rp, bpp, pairwise-independence]
see_also: [expander-walk-sampler, limited-independence, hitting-set-generator, disperser, randomness-extractor, median-trick, chebyshev-inequality, chernoff-bound]
sources:
  - paper: doi:10.1016/0885-064x(89)90015-0
    title: Benny Chor and Oded Goldreich, On the power of two-point based sampling, Journal of Complexity 5(1), 1989
    locator: pages 96 to 106 (error reduction with pairwise independent samples)
  - paper: doi:10.1145/28395.28410
    title: Miklós Ajtai, János Komlós and Endre Szemerédi, Deterministic simulation in LOGSPACE, STOC 1987
    locator: pages 132 to 140 (walks on expanders to save random bits)
  - paper: doi:10.1109/sfcs.1989.63449
    title: Aviad Cohen and Avi Wigderson, Dispersers, deterministic amplification, and weak random sources, FOCS 1989
    locator: pages 14 to 19 (deterministic amplification of RP and BPP with expander walks and dispersers)
  - paper: doi:10.1109/sfcs.1989.63486
    title: Russell Impagliazzo and David Zuckerman, How to recycle random bits, FOCS 1989
    locator: pages 248 to 253 (error reduction by reusing random bits along expander walks)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 3, Section 3.5 (pairwise independent repetitions), Chapter 4, Section 4.2 (random walks on expanders) and Chapter 6, Section 6.2 (extractors as samplers)
---

Randomness amplification is the problem of reducing the error probability of a randomized algorithm from a constant to $2^{-k}$ while spending few random bits. Running the algorithm $k$ times with fresh random strings of $m$ bits each costs $km$ bits. Pairwise independent runs use only $2m$ bits but reduce the error only to about $1/t$ for $t$ runs, and walks on expanders reach error $2^{-k}$ with $m + O(k)$ bits and $O(k)$ runs. The question links error reduction with [hitting set generators](/hitting-set-generator/), [dispersers](/disperser/) and [extractors](/randomness-extractor/). This page is about saving random bits; the plain version with independent runs is [error amplification](/error-amplification/).

## In plain words

A randomized algorithm can be wrong, say with chance one half. Running it many times, each time with new random choices, makes a wrong answer much less likely. But each run needs its own random bits, and random bits can be expensive: they may come from slow hardware, or they may have to be stored.

The question is how few random bits are enough to make the chance of error tiny. The trick is to let the runs share their randomness in a careful way: the random strings of the runs depend on each other, but in a way that makes it unlikely that all of them are unlucky. Good ways to do this use only a little more randomness than one run.

## Definition

Notation. $\mathcal{A}(w, r)$ is a randomized algorithm on input $w$ with a random string $r \in \{0,1\}^m$. $k \ge 1$ is the target: the new error must be at most $\delta = 2^{-k}$. $\Pr_r$ is over a uniform $r$.

**One-sided error ([RP](/rp/)).** If $w$ is in the language, $\Pr_r[\mathcal{A}(w, r) \text{ accepts}] \ge 1/2$; otherwise $\mathcal{A}$ never accepts. A *black-box amplifier* uses $R$ random bits to choose $q$ strings $r_1, \ldots, r_q \in \{0,1\}^m$ (which may depend on each other), runs $\mathcal{A}(w, r_i)$, and accepts if and only if some run accepts. It *reduces the error to $\delta$* if, for every set $B \subseteq \{0,1\}^m$ of density at most $1/2$,

$$\Pr[r_1, \ldots, r_q \in B] \le \delta.$$

Here $B$ is the set of strings on which $\mathcal{A}$ wrongly rejects $w$. The error stays one-sided: inputs outside the language are never accepted.

**Two-sided error ([BPP](/bpp/)).** $\mathcal{A}$ answers correctly for at least $2/3$ of the strings $r$. The amplifier runs $\mathcal{A}$ on $r_1, \ldots, r_q$ and outputs the majority answer. It reduces the error to $\delta$ if, for every set $B$ of density at most $1/3$, $\Pr[\text{at least } q/2 \text{ of the } r_i \text{ are in } B] \le \delta$.

The two resources are the number $R$ of random bits and the number $q$ of runs. The best methods have $R = m + O(k)$ and $q = O(k)$.

## Variants

- **Fixed error, fewer runs.** Reach a constant error, or error $1/\mathrm{poly}$, with few random bits and few runs; pairwise independence is the simple tool.
- **Samplers.** Estimate the mean of an arbitrary function $f : \{0,1\}^m \to [0, 1]$ within $\varepsilon$ with probability $1 - \delta$. Amplification for BPP is the case of a $\{0,1\}$-valued $f$ with mean far from $1/2$. An *oblivious* sampler chooses its sample points without looking at $f$.
- **Amplification with weak sources.** The random bits come from a source with only some [min-entropy](/min-entropy/), or from a [Santha-Vazirani source](/santha-vazirani-source/). Dispersers and extractors solve this version. In quantum information, "randomness amplification" also names the task of turning a Santha-Vazirani source into nearly uniform bits, which classical deterministic procedures cannot do.
- **Space-bounded amplification.** In logspace computation, the random bits are read once and cannot be stored, so the amplifier must also run in small space; walks on explicit expanders do.

## Examples

**Pairwise independent runs.** Pick two independent uniform elements $a, b$ of the field $\mathrm{GF}(2^m)$, and for $t$ distinct nonzero field elements $\alpha_1, \ldots, \alpha_t$ (so $t \le 2^m - 1$) let $r_i = a + b\alpha_i$. The strings are uniform and [pairwise independent](/pairwise-independence/), and use $2m$ random bits. Let $X$ be the number of accepting runs on an input in the language, with acceptance probability $p \ge 1/2$ for one run. Then $\mathrm{E}[X] = pt$ and $\mathrm{Var}[X] = tp(1 - p)$, and the [Chebyshev inequality](/chebyshev-inequality/) gives

$$\Pr[X = 0] \le \Pr\big[|X - pt| \ge pt\big] \le \frac{tp(1-p)}{(pt)^2} = \frac{1 - p}{pt} \le \frac{1}{t}.$$

So $t$ runs give error at most $1/t$ with $2m$ random bits. For error $2^{-k}$ this needs $2^k$ runs, which is too many when $k$ is large.

**A comparison.** Let $m = 100$ and $k = 20$. For the expander walk, assume a 16-regular graph on $2^{100}$ vertices with spectral expansion $\lambda \le 1/2$; then the error after $t$ vertices is at most $\frac{1}{2}(3/4)^{t-1}$, which is below $2^{-20}$ for $t = 47$.

| method | random bits | runs | error | bits for $m = 100$, $k = 20$ | runs |
|---|---|---|---|---|---|
| independent repetition | $km$ | $k$ | $2^{-k}$ | 2000 | 20 |
| pairwise independent runs | $2m$ | $t$ | $1/t$ | 200 | $2^{20} \approx 10^6$ |
| expander walk | $m + (t - 1)\log_2 d$ | $t = O(k)$ | $\frac{1}{2}\big(\frac{1 + \lambda}{2}\big)^{t-1}$ | 284 | 47 |

The expander walk is close to the 200 bits of pairwise runs and to the 20 runs of independent repetition at the same time.

**Two-sided error with independent runs and a majority vote.** By the [Chernoff bound](/chernoff-bound/), $O(k)$ independent runs give error $2^{-k}$ with $O(km)$ random bits. With pairwise independent runs and a majority vote, Chebyshev gives error $O(1/t)$. The [median trick](/median-trick/) combines the two: independent groups of pairwise independent runs.

## Known algorithms

- **Independent repetition**, see [error amplification](/error-amplification/): $R = km$, $q = k$ for RP, and $q = O(k)$ for BPP.
- **Pairwise independent repetition** (Chor and Goldreich 1989): $R = 2m$, error $O(1/q)$. With $k$-wise independent runs and a higher moment bound ([limited independence](/limited-independence/)), the error falls like $q^{-\Theta(k)}$ for a constant $k$, with $O(km)$ random bits.
- **Expander walks** (Ajtai, Komlós and Szemerédi 1987; Cohen and Wigderson 1989; Impagliazzo and Zuckerman 1989), see [expander walk sampler](/expander-walk-sampler/): $R = m + O(k)$ and $q = O(k)$, for RP by the hitting property and for BPP by the Chernoff bound for expander walks.
- **Dispersers and extractors.** An explicit [disperser](/disperser/) gives one-sided amplification, and an explicit [extractor](/randomness-extractor/) gives a sampler for two-sided amplification, with a random bit count of the form $m + O(k)$ and in some constructions a constant close to 1 in front of $k$. They also work when the random bits come from a weak source.

## Bounds

**A lower bound on the random bits.** Every one-sided black-box amplifier with $R$ random bits, $q$ runs and error $\delta < 1$, with $2q \le 2^m$, has

$$R \ge m + \log_2(1/\delta) - \log_2 q - 2.$$

*Proof.* Let $s = \lfloor 2^m/(2q) \rfloor \ge 1$. If the amplifier has fewer than $s$ seeds, put the strings of all seeds into a set $B$ of $2^{m-1}$ strings; then every seed fails and $\delta = 1$. Otherwise pick $s$ seeds. Their runs use at most $sq \le 2^{m-1}$ strings in total, so some set $B$ of exactly $2^{m-1}$ strings, of density $1/2$, contains all of them. Each chosen seed makes all $q$ runs reject, so $\delta \ge s/2^R \ge 2^{m-R}/(4q)$, using $\lfloor x \rfloor \ge x/2$ for $x \ge 1$. Take logarithms. $\square$

So with $q = O(k)$ runs and $\delta = 2^{-k}$, $R \ge m + k - O(\log k)$. Expander walks reach $m + O(k)$, so they are optimal up to the constant in front of $k$. Sharper bounds on the constant follow from the lower bounds on the parameters of dispersers and extractors of Radhakrishnan and Ta-Shma (2000).

**A lower bound on the runs.** Error $2^{-k}$ needs at least about $k$ runs. Choose $B$ as a uniformly random set of $2^{m-1}$ strings. For a fixed seed whose runs use $q' \le q$ distinct strings, the probability that all of them are in $B$ is $\prod_{i < q'} \frac{2^{m-1} - i}{2^m - i} \ge \big(\frac{1}{2} - \frac{q}{2^m}\big)^q$. Averaging over seeds, some fixed $B$ makes the amplifier fail with at least this probability, so $\delta \ge 2^{-q}(1 - 2q/2^m)^q$, and $q \ge k - O(1)$ when $q^2$ is much smaller than $2^m$.

## Reductions

- **One-sided amplification is a hitting problem.** A one-sided amplifier with error $\delta$ is a function from seeds to $q$-tuples of strings that hits every set of density at least $1/2$ from all but a $\delta$ fraction of seeds. Viewed as a bipartite graph from seeds to strings, this is a [disperser](/disperser/) (Cohen and Wigderson 1989; Sipser 1988), and with a short seed and all seeds tried it is a [hitting set generator](/hitting-set-generator/).
- **Two-sided amplification is sampling.** A two-sided amplifier is an oblivious sampler for Boolean functions. Samplers with good parameters and [extractors](/randomness-extractor/) are essentially the same objects (Zuckerman 1997).
- **From weak sources.** If the amplifier's seed is replaced by a sample of a weak source of [min-entropy](/min-entropy/) $k'$, a disperser or extractor gives the same guarantee; this is how BPP algorithms are simulated with weak random sources.

## Applications

- **Saving random bits** in algorithms where randomness is costly, and in protocols where each random bit must be sent.
- **Space-bounded computation.** Error reduction for [randomized logspace](/randomized-logspace/) with expander walks, which can be computed in small space.
- **Complexity theory.** Strong error reduction underlies the proofs that $\mathrm{BPP} \subseteq \mathrm{P/poly}$ ([P/poly](/p-poly/)) and that BPP is in the second level of the polynomial hierarchy.
- **Probabilistically checkable proofs.** Randomness-efficient repetition reduces the soundness error of PCPs while keeping the number of random bits small.

## References
