---
tag: 4AE9P1
kind: algorithm
slug: optimized-local-hashing
name: Optimized local hashing
aliases:
- OLH
area: security-and-privacy/differential-privacy
level: research
summary: A local frequency oracle in which each user hashes the value into a small range and applies generalized randomized response to the hash.
model: word-ram
complexity:
  vars: {n: the number of reports, d: the size of the domain}
  time: {worst: O(n d)}
  space: {extra: O(d)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Tianhao Wang, Jeremiah Blocki, Ninghui Li, Somesh Jha]
  note: "Wang, Blocki, Li and Jha put the local frequency oracles in one framework at USENIX Security 2017 and chose the hash range that minimizes the variance."
prereqs: [local-differential-privacy, universal-hashing]
see_also: [randomized-response, rappor, frequency-estimation, hash-function, privacy-amplification-by-shuffling, sequential-composition-theorem, count-min-sketch]
sources:
  - paper: "Tianhao Wang, Jeremiah Blocki, Ninghui Li and Somesh Jha, Locally differentially private protocols for frequency estimation, USENIX Security 2017, pages 729 to 745"
    locator: "Definition 3 (pure LDP protocols and their support sets), Theorem 2 (the variance of a pure protocol), and Section 4.5 (optimized local hashing with g = e^epsilon + 1)"
  - paper: "Raef Bassily and Adam Smith, Local, private, efficient protocols for succinct histograms, STOC 2015"
    locator: the earlier local protocol that hashes the value before randomizing it
  - paper: "Ilya Mironov, On significance of the least significant bits for differential privacy, ACM CCS 2012, pages 650 to 661"
    locator: why the samplers of a deployment must be exact
---

Optimized local hashing (OLH) is a local frequency oracle: it lets a collector estimate how many clients hold each value of a domain of size $d$, while each client's report is $\varepsilon$-[locally differentially private](/local-differential-privacy/). Each client picks a random hash function $H$ from a family into $\{0, \ldots, g - 1\}$, and applies generalized [randomized response](/randomized-response/) to $H(v)$, not to $v$. It sends $H$ (as a seed) and the noisy hash value. Wang, Blocki, Li and Jha (2017) showed that $g = e^{\varepsilon} + 1$ minimizes the variance, which is then $n \cdot 4e^{\varepsilon}/(e^{\varepsilon} - 1)^2$ for $n$ clients. This does not depend on $d$, while plain randomized response over $d$ values has a variance that grows with $d$.

## In plain words

Each client wants to report one item from a long list, such as a web page, without saying which one. Randomized response over the whole list works badly: when the list is long, the true item is only rarely sent.

So each client first picks a random way to sort all items into a few buckets, say four. It finds the bucket of its item, and then sends that bucket truthfully with some probability, or one of the other buckets. It also says which way of sorting it used.

The collector checks, for each item, how many reports point to that item's bucket. Items that many clients hold get extra hits. The collector subtracts the expected number of chance hits.

## The problem

Each of $n$ clients holds a value $v_u \in \{0, \ldots, d - 1\}$. The collector wants, for every value $v$, an estimate of $n_v$, the number of clients that hold $v$. Each client sends one report, and the report must be $\varepsilon$-LDP: for all values $u, u'$ and every report $r$, $\Pr[R(u) = r] \le e^{\varepsilon}\Pr[R(u') = r]$. The neighbor relation is replace: one client changes its value. The goal is a small variance of each estimate, and a short report.

## The algorithm

The parameter is the exact rational $e^{\varepsilon} > 1$. Let $g$ be the hash range and $p = e^{\varepsilon}/(e^{\varepsilon} + g - 1)$. The family $\{H_s\}$ must satisfy $\Pr_s[H_s(u) = H_s(v)] = 1/g$ for all $u \ne v$ (a [universal hashing](/universal-hashing/) property).

```pseudo id=main
OLH-REPORT(v, e^epsilon)                  ▷ run by the client
L1  s <- a uniform seed of the hash family
L2  x <- H_s(v)                            ▷ a value in {0, ..., g - 1}
L3  if a coin with Pr[1] = p gives 1 then
L4      return (s, x)                      ▷ send the true hash value
L5  y <- a uniform value of {0, ..., g - 1} other than x; return (s, y)

OLH-ESTIMATE(reports, e^epsilon)          ▷ run by the collector; n reports
L6  for each value v: C(v) <- the number of reports (s, y) with H_s(v) = y
L7  c(v) <- (C(v) - n/g) / (p - 1/g)
L8  return c
```

Lines L1 and L2 hash the value with a fresh random function. Lines L3 to L5 are generalized randomized response over the $g$ hash values: the true value with probability $p$, and each of the other $g - 1$ values with probability $(1 - p)/(g - 1)$. The report is the pair of the seed and the value.

Line L6 counts the reports that "support" $v$: those whose hash function maps $v$ to the reported value. A client that holds $v$ supports it with probability $p$. A client that holds another value supports $v$ with probability exactly $1/g$, by the collision property. Line L7 removes the expected $n/g$ chance supports and scales the rest, which gives an unbiased estimate.

The choice of $g$ trades two effects. A large $g$ makes chance supports rare, but then the true hash value is sent with a small probability. The variance is smallest at $g = e^{\varepsilon} + 1$. The code takes the best integer: $\lfloor e^{\varepsilon} \rfloor + 1$ or $\lfloor e^{\varepsilon} \rfloor + 2$, whichever gives the smaller variance. Plain rounding of $e^{\varepsilon} + 1$ is not always best: at $e^{\varepsilon} = 2.45$, $g = 4$ beats $g = 3$.

The code uses the family of all functions from the domain to $\{0, \ldots, g - 1\}$, where the seed $s$ is a number below $g^d$ and $H_s(v)$ is digit $v$ of $s$ in base $g$. This family has the collision property exactly, so the tests can check every claim with fractions. Its seeds have $d \log_2 g$ bits, so a deployment uses a family with short seeds instead. The coins use exact fractions, and a deployment needs a cryptographic source of randomness and exact sampling (Mironov 2012).

## Example

Take $e^{\varepsilon} = 3$ and $d = 4$. Then $g = 4$ and $p = 3/6 = 1/2$. Four clients report. The seed $s$ is a number below $4^4 = 256$, and the table lists $H_s(0), \ldots, H_s(3)$, the base-4 digits of $s$ from the lowest.

| client | $v$ | seed $s$ (line L1) | $H_s(0..3)$ | $x$ (line L2) | coin (line L3) | report |
|---|---|---|---|---|---|---|
| 1 | 2 | 201 | 1, 2, 0, 3 | 0 | keep | (201, 0) |
| 2 | 2 | 54 | 2, 1, 3, 0 | 3 | change, $y = 1$ | (54, 1) |
| 3 | 0 | 147 | 3, 0, 1, 2 | 3 | keep | (147, 3) |
| 4 | 2 | 30 | 2, 3, 1, 0 | 1 | keep | (30, 1) |

Line L6 checks each value against each report. Value 2 is supported by reports 1 and 4, so $C(2) = 2$. Value 0 is supported by report 3 only, value 1 by report 2 only (a chance support), and value 3 by none. Line L7 gives $c(v) = (C(v) - 1)/(1/4) = 4(C(v) - 1)$, which is $0, 0, 4, -4$. The true counts are $1, 0, 3, 0$.

With four clients the estimate is very noisy: by Theorem 2 below, the standard deviation is about $\sqrt{4 \cdot 3} = 3.5$. For $n = 10000$ clients and $d = 1024$, the standard deviation is $\sqrt{3n} = 173.2$ for OLH, against 1600.8 for randomized response over all 1024 values, whose variance per client is $(d - 2 + e^{\varepsilon})/(e^{\varepsilon} - 1)^2$.

## Correctness

**Theorem 1 (privacy).** Each report is $\varepsilon$-LDP, and the bound is tight.

A report $(s, y)$ has probability $p/|\mathcal S|$ if $y = H_s(v)$ and $(1 - p)/((g - 1)|\mathcal S|)$ otherwise. The ratio of the two is $p(g - 1)/(1 - p) = e^{\varepsilon}$, for every $g$.

**Theorem 2 (unbiased estimate; Wang, Blocki, Li and Jha, Theorem 2 for pure protocols).** If the family has the collision property, then $\mathbb E[c(v)] = n_v$ and

$$\mathrm{Var}[c(v)] = \frac{n_v\,p(1 - p) + (n - n_v)\,q(1 - q)}{(p - q)^2}, \qquad q = \frac1g.$$

**Theorem 3 (the best range).** The approximate variance $\mathrm{Var}^* = n q(1 - q)/(p - q)^2$ is smallest at $g = e^{\varepsilon} + 1$, with the value $n \cdot 4e^{\varepsilon}/(e^{\varepsilon} - 1)^2$.

The key step of Theorem 2 is that a client with another value supports $v$ with probability $p/g + (1 - 1/g)(1 - p)/(g - 1) = 1/g$. The full proofs are in the correctness proof of this page. The tests check the privacy with exact fractions, and the mean and variance against an exact sum over the pmf of each report, on 500 random datasets.

## Complexity

The model is the [word RAM](/word-ram/), with a hash evaluation counted as $O(1)$ word operations.

- **Client.** Lines L1 to L5 take $O(1)$ time and three uniform draws. The report has $\log_2 |\mathcal S| + \log_2 g$ bits. With a family of short seeds this is $O(\log n)$ bits; with the family of all functions it is $d \log_2 g$ bits.
- **Collector.** Line L6 evaluates one hash for each pair of a report and a value, so the estimate of all $d$ counts takes $O(n d)$ time. The extra space is $O(d)$ for the counts. For a large domain the collector estimates only a list of candidate values.

## Properties

- **Pure.** In the terms of Wang, Blocki, Li and Jha, OLH is a pure protocol: the support probability is $p$ for the true value and a constant $q$ for every other value. This makes the estimate of line L7 unbiased.
- **The variance does not depend on $d$.** At the best $g$, $\mathrm{Var}^*/n = 4e^{\varepsilon}/(e^{\varepsilon} - 1)^2$. For $e^{\varepsilon} = 3$ it is 3. Randomized response over $d$ values has $\mathrm{Var}^*/n = (d - 2 + e^{\varepsilon})/(e^{\varepsilon} - 1)^2$, which is 256.25 for $d = 1024$.
- **Short reports.** Optimized unary encoding, from the same paper, has the same variance, but its report has $d$ bits.
- **Slow decoding.** The collector does $O(n d)$ work, more than unary encoding, which only adds the bit vectors.
- **One report per client.** A second report of the same value with a fresh seed spends $\varepsilon$ again, by [sequential composition](/sequential-composition-theorem/). OLH has no permanent step like [RAPPOR](/rappor/).

## Variants and improvements

- **Binary local hashing.** With $g = 2$, the report is one bit plus a seed. This is close to the protocol of Bassily and Smith (2015). By Theorem 3 it is the best integer range only when $e^{\varepsilon} \le \sqrt 2$.
- **Optimized unary encoding.** Encode $v$ as a one-hot vector of $d$ bits, and send each bit with randomized response with different probabilities for ones and zeros. It has the same variance as OLH, a longer report and faster decoding.
- **Large domains and heavy hitters.** A frequency oracle for a domain of $2^{64}$ values cannot test every value. Later protocols run OLH on prefixes or on hashes of the value, and keep only the frequent ones.
- **Shuffling.** If the reports are mixed before the collector reads them, the central loss is much smaller ([privacy amplification by shuffling](/privacy-amplification-by-shuffling/)).

## When to use it

Use OLH when the collector is not trusted, each client reports once, the domain is too large for plain randomized response (roughly when $d > 3e^{\varepsilon} + 2$, the point where the two variances cross), and the collector can afford $O(n d)$ work or has a candidate list. Use plain randomized response for a small domain. Use RAPPOR when one client reports the same value many times.

## Pitfalls

- **The wrong correction.** Line L7 with $C(v)/p$, or with $n/d$ in place of $n/g$, is biased. Line L7 must subtract $n/g$, the expected number of chance supports, and divide by $p - 1/g$.
- **A weak hash family.** If line L1 uses a family whose collision probability is not $1/g$, the chance supports of line L6 are not $n/g$ on average, and line L7 is biased. Use a family with a known collision probability, and use that probability in line L7.
- **A seed that the client does not choose at random.** If line L1 uses the same seed for all clients, then all clients with values in the same bucket look the same, and the collector cannot tell those values apart. Each client must draw its own seed.
- **A float coin.** Line L3 written as "random float below $p$" gives a probability that differs a little from $p$. Compare a uniform integer with the numerator of the exact fraction.
- **Ignoring the range choice.** Line L2 with a fixed $g = 2$ for a large $\varepsilon$ wastes privacy budget: at $e^{\varepsilon} = 9$, $g = 2$ gives $\mathrm{Var}^*/n = 1.5625$ against $0.5625$ at $g = 10$.

## Implementations

## History

Local hashing goes back to Bassily and Smith (STOC 2015), who hashed each value to a single bit before randomizing it, to get short reports for succinct histograms. Wang, Blocki, Li and Jha (USENIX Security 2017) put direct encoding, unary encoding and local hashing into one framework of pure protocols, gave the variance of each, and chose the parameters that minimize it. The choice $g = e^{\varepsilon} + 1$ gave optimized local hashing. Later work on local frequency estimation often compares against OLH and optimized unary encoding.

## References
