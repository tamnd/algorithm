---
tag: HQ75X7
kind: theorem
slug: bloom-filter-optimal-hash-count
name: Optimal number of Bloom filter hash functions
aliases:
- optimal k for Bloom filters
area: data-structures/probabilistic-structures
level: core
summary: The false positive rate is minimized at k = (m/n) ln 2 hash functions for m bits and n items.
prereqs: [bloom-filter, false-positive-rate, logarithms]
see_also: [bloom-filter-lower-bound, counting-bloom-filter, scalable-bloom-filter, approximate-membership, xor-filter]
sources:
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2.1 (the optimal number of hash functions and the symmetry argument in p)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.5 (Bloom filters, minimizing the false positive probability over k)
  - paper: doi:10.1145/362686.362692
    title: Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970
    locator: pages 422 to 426 (the analysis of Method 2)
  - paper: doi:10.1109/TNET.2002.803864
    title: Michael Mitzenmacher, Compressed Bloom filters, IEEE/ACM Transactions on Networking 10(5), 2002
    locator: pages 604 to 612 (a different optimal k when the filter is compressed for transmission)
---

For a [Bloom filter](/bloom-filter/) with $m$ bits and $n$ keys, the standard estimate $(1 - e^{-kn/m})^k$ of the [false positive rate](/false-positive-rate/) is smallest when the number of hash functions is $k = (m/n)\ln 2$. At this point each bit is 1 with probability one half, and the rate is $2^{-k} \approx 0.6185^{m/n}$. Read the other way, a rate $\varepsilon$ needs $m/n = \log_2(1/\varepsilon)/\ln 2 \approx 1.44 \log_2(1/\varepsilon)$ bits per key, which is the figure that compares Bloom filters with every other filter.

## Statement

Fix integers $m \ge 1$ and $n \ge 1$, and let $c = n/m$. For real $k > 0$ let
$$ f(k) = \left(1 - e^{-ck}\right)^k. $$
Then $f$ has a unique minimum on $(0, \infty)$, at
$$ k^* = \frac{\ln 2}{c} = \frac{m}{n}\ln 2, \qquad f(k^*) = 2^{-k^*} = \left(2^{-\ln 2}\right)^{m/n} \approx 0.6185^{m/n}. $$
The function $f$ decreases on $(0, k^*]$ and increases on $[k^*, \infty)$. So the best integer number of hash functions is $\lfloor k^* \rfloor$ or $\lceil k^* \rceil$.

The same holds for the finite form $(1 - (1 - 1/m)^{kn})^k$, with $k^* = \ln 2 / (-n \ln(1 - 1/m))$, which is slightly smaller than $(m/n)\ln 2$. In both forms the minimum is where the expected fraction of 0 bits is exactly one half.

## In plain words

More hash functions help a query: an absent key must find more 1 bits to fool the filter. But more hash functions also hurt: each insert sets more bits, so the array fills up faster. With very few hash functions the test is too weak, and with very many the array is almost all ones.

The best choice sits in between, at the point where about half of the bits are 1 and half are 0. For a filter with ten bits for each key, this is about seven hash functions, and then about one absent key in 120 is a false positive.

## Proof

Let $g(k) = \ln f(k) = k \ln(1 - e^{-ck})$. Since $\ln$ is increasing, $f$ and $g$ have the same minimizers and the same intervals of increase and decrease.

**Change of variable.** Let $p = e^{-ck}$, the expected fraction of 0 bits. The map $k \mapsto p$ is a strictly decreasing bijection from $(0, \infty)$ onto $(0, 1)$, with inverse $k = -\ln(p)/c$. In terms of $p$,
$$ g = -\frac{1}{c}\,\ln(p)\,\ln(1 - p) = -\frac{1}{c}\,h(p), \qquad h(p) = \ln(p)\ln(1-p). $$
Both logarithms are negative on $(0, 1)$, so $h(p) > 0$. Minimizing $g$ over $k$ is the same as maximizing $h$ over $p \in (0, 1)$.

**$h$ has a unique maximum at $p = 1/2$.** The derivative is
$$ h'(p) = \frac{\ln(1-p)}{p} - \frac{\ln p}{1 - p} = \frac{\psi(p)}{p(1-p)}, \qquad \psi(p) = (1 - p)\ln(1 - p) - p \ln p. $$
So $h'$ has the sign of $\psi$. We show that $\psi > 0$ on $(0, 1/2)$ and $\psi < 0$ on $(1/2, 1)$.

1. *Symmetry.* $\psi(1 - p) = p \ln p - (1-p)\ln(1-p) = -\psi(p)$. So $\psi(1/2) = 0$, and the claim on $(1/2, 1)$ follows from the claim on $(0, 1/2)$.
2. *The limit at 0.* As $p \to 0^+$, $(1-p)\ln(1-p) \to 0$ and $p \ln p \to 0$, so $\psi(p) \to 0$.
3. *The shape of $\psi$.* $\psi'(p) = -\ln(1-p) - 1 - \ln p - 1 = -\ln(p(1-p)) - 2$. This is positive exactly when $p(1-p) < e^{-2}$. Since $p(1-p)$ increases on $(0, 1/2]$ from $0$ to $1/4$, and $e^{-2} \approx 0.135 < 1/4$, there is one point $p_0 \in (0, 1/2)$ with $p_0(1 - p_0) = e^{-2}$. So $\psi$ is strictly increasing on $(0, p_0]$ and strictly decreasing on $[p_0, 1/2]$.
4. *Sign on $(0, 1/2)$.* On $(0, p_0]$, $\psi$ is strictly increasing with limit 0 at $0^+$, so $\psi > 0$ there. On $[p_0, 1/2)$, $\psi$ is strictly decreasing and $\psi(1/2) = 0$, so $\psi > 0$ there too.

So $h$ is strictly increasing on $(0, 1/2]$ and strictly decreasing on $[1/2, 1)$, and $p = 1/2$ is its unique maximizer.

**Back to $k$.** Since $k \mapsto p$ is strictly decreasing, $p \in (1/2, 1)$ corresponds to $k \in (0, k^*)$ and $p \in (0, 1/2)$ to $k \in (k^*, \infty)$, where $e^{-ck^*} = 1/2$, that is $k^* = (\ln 2)/c$. As $k$ grows from 0 to $k^*$, $p$ falls from 1 to $1/2$, so $h$ grows and $g$ falls. As $k$ grows beyond $k^*$, $p$ falls below $1/2$, so $h$ falls and $g$ grows. Hence $f$ decreases on $(0, k^*]$, increases on $[k^*, \infty)$, and has its unique minimum at $k^*$, with
$$ f(k^*) = \left(1 - \tfrac12\right)^{k^*} = 2^{-k^*} = 2^{-(m/n)\ln 2}. $$
Since $2^{-\ln 2} = e^{-(\ln 2)^2} = 0.61850\ldots$, this is $0.6185^{m/n}$ to four digits.

**Integer $k$.** A function that decreases up to $k^*$ and increases after it takes its least value over the integers $k \ge 1$ at $\lfloor k^* \rfloor$ or at $\lceil k^* \rceil$ (only $\lceil k^* \rceil = 1$ if $k^* < 1$).

**The finite form.** The proof used only that $p = a^k$ for a constant $a \in (0, 1)$: here $a = e^{-c}$. For $(1 - (1 - 1/m)^{kn})^k$, take $a = (1 - 1/m)^n$ and the same steps give the minimum where $(1 - 1/m)^{kn} = 1/2$. $\blacksquare$

## Consequences

**Bits per key.** At $k = k^*$ the rate is $\varepsilon = 2^{-k^*}$, so $k^* = \log_2(1/\varepsilon)$ and
$$ \frac{m}{n} = \frac{k^*}{\ln 2} = \log_2 e \cdot \log_2(1/\varepsilon) \approx 1.4427 \log_2(1/\varepsilon). $$
A rate of 1 percent needs 9.59 bits per key and 6.64 hash functions, so 7 in practice. The [space lower bound](/bloom-filter-lower-bound/) for every filter is $\log_2(1/\varepsilon)$ bits per key, so a Bloom filter uses about 44 percent more than the bound. [Xor filters](/xor-filter/), [binary fuse filters](/binary-fuse-filter/) and [ribbon filters](/ribbon-filter/) close most of this gap for static sets.

**Rates near the optimum.** For $m/n = 10$ the function is flat near $k^* = 6.93$.

| $k$ | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|
| $(1 - e^{-k/10})^k$ | 0.00943 | 0.00844 | 0.00819 | 0.00846 | 0.00913 |

So an error of one in $k$ costs only a few percent in the rate. Rounding $k$ down saves hash work and memory probes.

**Half of the bits are 1.** At the optimum each bit is 1 with probability $1/2$. An array of this kind has close to the most entropy that an array of $m$ bits can have, so it cannot be compressed much. This is why Mitzenmacher (2002) found a different optimum for a filter that is compressed before it is sent: there, a larger and sparser array with fewer hash functions can give a smaller compressed message for the same rate.

**Design rules.** For the [counting Bloom filter](/counting-bloom-filter/), the overflow bound of its counters uses this $k$. The [scalable Bloom filter](/scalable-bloom-filter/) fills each of its filters to half ones, which is this optimum.

## Tightness

The value $k^*$ is the minimizer of the estimate, not of the exact rate. The exact rate is $\mathbb{E}[(X/m)^k]$, where $X$ is the random number of 1 bits, and it is slightly larger than the estimate for small $m$, see the [false positive rate](/false-positive-rate/). For large $m$ the two agree to many digits: for $m = 100$ and $n = 10$ the finite form gives $k^* = 6.897$ against $(m/n)\ln 2 = 6.931$, and both round to 7.

The factor $\log_2 e$ in the bits per key cannot be removed by any choice of $k$, because the theorem says that $2^{-(m/n)\ln 2}$ is the smallest value of the estimate. It is a limit of the Bloom filter design, not of the problem.

## History

Bloom (1970) analyzed the rate of his bit-array method as a function of the number of bits set by each key. The closed form $k = (m/n)\ln 2$, and the argument by the symmetry of $\ln(p)\ln(1-p)$ in $p$ and $1 - p$, are standard in the later literature; the survey of Broder and Mitzenmacher (2004) presents both. This page does not say who first wrote the closed form.

## References
