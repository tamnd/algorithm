---
tag: N76ANH
kind: concept
slug: false-positive-rate
name: False positive rate
aliases:
- false positive probability
area: data-structures/probabilistic-structures
level: intro
summary: Probability that a query for an absent key is wrongly reported as present.
prereqs: [approximate-membership, probability-space, expected-value]
see_also: [bloom-filter, bloom-filter-optimal-hash-count, bloom-filter-lower-bound, one-sided-error, cuckoo-filter, xor-filter, union-bound]
sources:
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the false positive probability, its approximations, and the fraction of false positives of a fixed filter)
  - paper: doi:10.1016/j.ipl.2008.05.018
    title: Prosenjit Bose, Hua Guo, Evangelos Kranakis, Anil Maheshwari, Pat Morin, Jason Morrison, Michiel Smid and Yihui Tang, On the false-positive rate of Bloom filters, Information Processing Letters 108(4), 2008
    locator: pages 210 to 213 (the classical formula is not exact, and is a lower bound)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.5 (hashing, fingerprints and Bloom filters, the false positive probability)
  - paper: doi:10.1145/3376122
    title: Thomas Mueller Graf and Daniel Lemire, Xor filters, faster and smaller than Bloom and cuckoo filters, ACM Journal of Experimental Algorithmics 25, 2020
    locator: Section 2 (false positive rates and bits per key of the common filters)
---

The false positive rate $\varepsilon$ of a filter is the probability that a query for a key that is not in the stored set returns "present". It is the only error of a solution to the [approximate membership problem](/approximate-membership/), since such a filter has no false negatives. The rate is a probability over the random hash functions of the filter, for one fixed absent key. It is not a probability over the queries, and the difference matters when the same key is queried many times.

## In plain words

A filter answers "maybe present" or "surely absent". A false positive is a "maybe present" for a key that was never stored. The false positive rate says how often this happens.

Think of it like a smoke alarm that never misses a fire but sometimes rings for burnt toast. The rate is the chance that it rings for one given piece of toast. It does not say how many of the rings are real fires. That depends on how often you burn toast and how often there is a fire.

A filter with a smaller rate needs more memory. Each time you halve the rate, each stored key needs at least one more bit. The rate also changes as the filter fills up, so it is fixed by design only up to a planned number of keys.

## The idea

**The per-key rate.** Let BUILD make a filter $F$ from a set $S$ with random bits $\rho$, as in the [approximate membership problem](/approximate-membership/). For a fixed key $x \notin S$, the false positive rate is

$$ \varepsilon(S, x) = \Pr_\rho[\text{QUERY}(F, x) = \text{yes}]. $$

A filter *has false positive rate at most $\varepsilon$* if $\varepsilon(S, x) \le \varepsilon$ for each $S$ of the allowed size and each $x \notin S$. For most filters the rate does not depend on $S$ or $x$, only on $n = |S|$ and the parameters, when the hash functions are ideal.

**The rate of one built filter.** Once $F$ is built, it is a fixed object. Let $A(F)$ be its set of accepted keys. Its *realized* rate is the fraction
$$ \rho(F) = \frac{|A(F) \setminus S|}{u - n} $$
of the absent keys that it accepts, where $u$ is the size of the universe. This is a [random variable](/random-variable/) over the choice of $\rho$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\rho(F)]$ is the average of $\varepsilon(S, x)$ over the $x \notin S$, so it equals the per-key rate when that rate is the same for each $x$. A filter can be unlucky: its realized rate can be much larger than its expectation.

**Repeated queries.** A filter is a fixed function of the key. If $x$ is a false positive once, it is a false positive each time. So a workload that queries the same absent key a thousand times sees an empirical rate of 0 or 1, not $\varepsilon$. Independence holds only across different keys, and even there only under the assumption of ideal hash functions.

**The rate is not the error of a "yes".** Let a fraction $q$ of the queries be keys of $S$. Then a "yes" is wrong with probability
$$ \frac{(1-q)\varepsilon}{q + (1-q)\varepsilon}, $$
by Bayes' rule. This can be much larger than $\varepsilon$ when $q$ is small.

**Rate and space.** A filter that keeps $\varepsilon$ fixed needs about $\log_2(1/\varepsilon)$ bits per key at the least (the [space lower bound](/bloom-filter-lower-bound/)). Many filters reach a rate of exactly $2^{-r}$ by storing an $r$-bit fingerprint for each key: the [xor filter](/xor-filter/), the [ribbon filter](/ribbon-filter/) and, up to a factor for the number of slots compared, the [cuckoo filter](/cuckoo-filter/) and the [quotient filter](/quotient-filter/). The [Bloom filter](/bloom-filter/) has a rate that depends on how full its bit array is.

**The rate depends on the load.** For each incremental filter the rate grows with the number of inserted keys. A Bloom filter of $m$ bits with $k$ hash functions has rate close to $(1 - e^{-kn/m})^k$ after $n$ inserts. The design value $\varepsilon$ holds only up to the planned capacity. The [scalable Bloom filter](/scalable-bloom-filter/) adds new filters to keep a bound as the set grows.

## Examples

**An exact small case.** Take a Bloom filter with $m = 8$ bits and $k = 2$ ideal hash functions, and insert $n = 2$ keys. The four hash values are independent and uniform on the 8 positions. Let $X$ be the number of distinct positions among them, which is the number of bits set to 1. A fixed absent key is a false positive when both of its positions are set, which has probability $(X/8)^2$ given $X$. Counting the $8^4 = 4096$ outcomes gives this table.

| $X$ | $\Pr[X]$ | realized rate $(X/8)^2$ |
|---|---|---|
| 1 | $1/512$ | $1/64 \approx 0.016$ |
| 2 | $49/512$ | $4/64 \approx 0.063$ |
| 3 | $252/512$ | $9/64 \approx 0.141$ |
| 4 | $210/512$ | $16/64 = 0.25$ |

So the per-key rate is $\mathbb{E}[(X/8)^2] = 5825/32768 \approx 0.1778$. The classical formula $(1 - (1 - 1/m)^{kn})^k$ gives $0.1712$, and the approximation $(1 - e^{-kn/m})^k$ gives $0.1548$. Both are too small. The classical formula squares the expected fraction of set bits, and by Jensen's inequality the expected square is at least the square of the expectation. Bose et al. (2008) pointed out this gap. It shrinks as $m$ grows.

**A large filter.** With $m = 10^7$ bits, $n = 10^6$ keys and $k = 7$, both formulas give $0.00819$ to three significant digits. For large filters the gap of the small case does not matter in practice.

**The rate of a "yes".** With $\varepsilon = 0.01$ and $q = 0.1$, so that 90 percent of the queries are for absent keys, a "yes" is wrong with probability $0.009/0.109 \approx 0.083$. One "yes" in twelve is false, although the filter has a rate of one percent.

**Fingerprints.** A filter that stores an 8-bit fingerprint for each key and accepts $x$ when its fingerprint matches the one stored at a single place has rate $2^{-8} \approx 0.0039$. If the query compares with $2b$ stored fingerprints, as a [cuckoo filter](/cuckoo-filter/) does with two buckets of $b$ entries, the [union bound](/union-bound/) gives a rate of at most $2b \cdot 2^{-8}$, which is $1/32$ for $b = 4$.

## Where it is used

- The [Bloom filter](/bloom-filter/) and its [optimal number of hash functions](/bloom-filter-optimal-hash-count/), which minimizes the rate for a given space.
- The [approximate membership space lower bound](/bloom-filter-lower-bound/), which says how small the rate can be for a given space.
- Fingerprint filters: [cuckoo](/cuckoo-filter/), [quotient](/quotient-filter/), [xor](/xor-filter/), [binary fuse](/binary-fuse-filter/) and [ribbon](/ribbon-filter/) filters.
- The [learned Bloom filter](/learned-bloom-filter/), whose rate is defined only with respect to a distribution of queries.
- The [scalable](/scalable-bloom-filter/) and [stable](/stable-bloom-filter/) Bloom filters, which bound the rate as the input grows without limit.
- The analysis of [Monte Carlo algorithms](/monte-carlo-algorithm/) with [one-sided error](/one-sided-error/), where the same distinction between per-input and average error appears.

## References
