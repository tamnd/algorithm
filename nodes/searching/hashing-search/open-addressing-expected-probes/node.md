---
tag: HQ4QCG
kind: theorem
slug: open-addressing-expected-probes
name: Expected probes in open addressing
aliases:
- Knuth's probe analysis
area: searching/hashing-search
level: core
summary: Expected unsuccessful probes are at most 1/(1-alpha) and successful ones about (1/alpha)ln(1/(1-alpha)).
model: word-ram
prereqs: [open-addressing, probe-sequence, uniform-hashing-assumption, load-factor, linearity-of-expectation]
see_also: [linear-probing-analysis, yao-open-addressing-lower-bound, double-hashing, primary-clustering, secondary-clustering, chaining-expected-search-time, lazy-deletion, uniform-hashing-assumption]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4 (Open addressing), the theorems on the expected number of probes in an unsuccessful search, in an insertion and in a successful search
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of uniform probing and its comparison with linear probing and double hashing
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables), the proposition on the cost of search in linear probing, for comparison
---

The expected number of probes in [open addressing](/open-addressing/) is the classic cost formula for a hash table that stores its keys in the array itself. Under uniform hashing, where each key has an independent and uniformly random [probe sequence](/probe-sequence/), an unsuccessful search or an insertion in a table with [load factor](/load-factor/) $\alpha = n/m < 1$ makes at most $1/(1 - \alpha)$ probes on average, and a successful search makes at most $(1/\alpha) \ln (1/(1 - \alpha))$. These are the bounds of CLRS Section 11.4 and the limits of the exact formulas of Knuth. This page gives the exact law of the number of probes, its variance, the exact successful-search cost, and how far real probing schemes are from the model.

## Statement

Let a table have $m$ slots and hold $n$ keys, with $0 \le n < m$, inserted by open addressing with no deletions. Assume the [uniform hashing](/uniform-hashing-assumption/) model for probe sequences: the probe sequences of the stored keys and of the searched key are independent, and each is a uniformly random permutation of the $m$ slots. Let $\alpha = n/m$, and let $X$ be the number of probes of an unsuccessful search for a key that is not stored, which equals the number of probes of its insertion. For $k \ge 0$ write $H_k = \sum_{j=1}^{k} 1/j$.

**Theorem.**

1. **(Law.)** For $0 \le i \le n$, $\Pr[X > i] = \dfrac{n (n-1) \cdots (n-i+1)}{m (m-1) \cdots (m-i+1)}$, and $\Pr[X > n] = 0$.
2. **(Mean.)** $\mathrm{E}[X] = \dfrac{m + 1}{m - n + 1} \le \dfrac{1}{1 - \alpha}$.
3. **(Variance.)** $\mathrm{Var}[X] = \dfrac{n (m + 1)(m - n)}{(m - n + 1)^2 (m - n + 2)} \le \dfrac{\alpha}{(1 - \alpha)^2}$.
4. **(Successful search.)** For $n \ge 1$, a search for a stored key chosen uniformly at random makes on average
$$C_n = \frac{m + 1}{n} \left( H_{m+1} - H_{m-n+1} \right) \le \frac{1}{\alpha} \ln \frac{1}{1 - \alpha}$$
probes.
5. **(Limits.)** As $m \to \infty$ with $n/m \to \alpha$ for a fixed $\alpha < 1$, $\mathrm{E}[X] \to 1/(1 - \alpha)$, $\mathrm{Var}[X] \to \alpha/(1 - \alpha)^2$ and $C_n \to (1/\alpha)\ln(1/(1 - \alpha))$.

## In plain words

In open addressing, a search knocks on doors in a random order until it finds an empty room. If three quarters of the rooms are full, each knock finds a full room with chance three in four, so the search needs about four knocks on average. In general the cost is one divided by the share of empty rooms.

A search for a key that is stored retraces the knocks of its own insertion. Keys inserted early met an almost empty table and are cheap to find; keys inserted late met a full one. On average, finding a stored key costs much less than a failed search. Both costs explode as the table fills, which is why open-addressing tables grow well before they are full.

## Proof

Keys never move after they are inserted, so the set $F$ of the $n$ full slots is a function of the probe sequences of the stored keys. The probe sequence $\pi$ of the searched key is independent of them, so given $F$ it is still a uniform permutation of the slots. Condition on $F$ for the rest of the proof of Parts 1 to 3; the results do not depend on $F$.

**Part 1.** $X > i$ holds exactly when the first $i$ slots of $\pi$ are all full. The first $i$ entries of a uniform permutation form a uniform ordered list of $i$ distinct slots, so the probability that all lie in $F$ is $\binom{n}{i} i! / (\binom{m}{i} i!) = n(n-1)\cdots(n-i+1)/(m(m-1)\cdots(m-i+1))$. For $i > n$ there are not enough full slots.

**Part 2.** Let $k = m - n \ge 1$ be the number of empty slots. Then $X = 1 + G$, where $G$ is the number of full slots that come before every empty slot in $\pi$. For a full slot $s$, let $Z_s$ be the indicator that $s$ precedes all $k$ empty slots. The relative order of $s$ and the empty slots in $\pi$ is uniform over the $(k + 1)!$ orders, so $\Pr[Z_s = 1] = 1/(k + 1)$. By [linearity of expectation](/linearity-of-expectation/), $\mathrm{E}[G] = n/(k + 1)$ and
$$\mathrm{E}[X] = 1 + \frac{n}{m - n + 1} = \frac{m + 1}{m - n + 1}.$$
For the bound, each factor $(n - j)/(m - j)$ of Part 1 is at most $n/m = \alpha$, so $\Pr[X > i] \le \alpha^i$, and $\mathrm{E}[X] = \sum_{i \ge 0} \Pr[X > i] \le \sum_{i \ge 0} \alpha^i = 1/(1-\alpha)$.

**Part 3.** For two distinct full slots $s$ and $t$, $Z_s Z_t = 1$ when both precede all empty slots. Among the $k + 2$ slots $s$, $t$ and the empty ones, all orders are equally likely, and the event holds when the first two places go to $s$ and $t$, in either order, which has probability $2/((k+2)(k+1))$. So
$$\mathrm{E}[G(G-1)] = \sum_{s \ne t} \mathrm{E}[Z_s Z_t] = \frac{2 n (n-1)}{(k+1)(k+2)}.$$
Then $\mathrm{Var}[X] = \mathrm{Var}[G] = \mathrm{E}[G(G-1)] + \mathrm{E}[G] - \mathrm{E}[G]^2$. With $\mathrm{E}[G] = n/(k+1)$, putting the three terms over the denominator $(k+1)^2(k+2)$ gives the numerator
$$2n(n-1)(k+1) + n(k+1)(k+2) - n^2(k+2) = n\,(k+1+n)\,k = n(m+1)(m-n),$$
using $k + 1 + n = m + 1$; expanding both sides as polynomials in $n$ and $k$ checks the middle equality. This is the formula of Part 3. For the bound, $\alpha/(1-\alpha)^2 = nm/k^2$, and $n(m+1)k/((k+1)^2(k+2)) \le nm/k^2$ is equivalent to $(m + 1) k^3 \le m (k+1)^2 (k+2)$. The right side is at least $m k^3 + m k^2$, and the left side is $m k^3 + k^3 \le m k^3 + m k^2$ since $k \le m$.

**Part 4.** A search for a stored key follows the same probe sequence as the insertion of that key and stops at the same slot, so it makes the same number of probes. The key inserted $(i+1)$-th met a table with $i$ keys, and its probe sequence was independent of the earlier ones, so by Part 2 its insertion made $(m+1)/(m-i+1)$ probes on average. Averaging over $i = 0, \ldots, n-1$,
$$C_n = \frac{1}{n} \sum_{i=0}^{n-1} \frac{m+1}{m - i + 1} = \frac{m+1}{n} \sum_{j = m - n + 2}^{m + 1} \frac{1}{j} = \frac{m + 1}{n} \left( H_{m+1} - H_{m-n+1} \right).$$
For the bound, $(m+1)/(m-i+1) \le m/(m-i)$ for $0 \le i < m$, and $\frac{1}{j} \le \int_{j-1}^{j} dx/x$, so
$$C_n \le \frac{1}{n} \sum_{i=0}^{n-1} \frac{m}{m-i} = \frac{1}{\alpha} \sum_{j=m-n+1}^{m} \frac{1}{j} \le \frac{1}{\alpha} \int_{m-n}^{m} \frac{dx}{x} = \frac{1}{\alpha} \ln \frac{m}{m - n} = \frac{1}{\alpha} \ln \frac{1}{1 - \alpha}.$$

**Part 5.** With $n = \alpha_m m$ and $\alpha_m \to \alpha$, $(m+1)/(m - n + 1) = (1 + 1/m)/(1 - \alpha_m + 1/m) \to 1/(1-\alpha)$, and the variance formula is $\alpha_m (1 + 1/m)(1 - \alpha_m)$ over $(1 - \alpha_m + 1/m)^2(1 - \alpha_m + 2/m)$, which tends to $\alpha/(1-\alpha)^2$. For $C_n$, $H_{m+1} - H_{m-n+1} = \ln \frac{m+1}{m-n+1} + O(1/(m - n))$, by $H_k = \ln k + \gamma + O(1/k)$, so $C_n = \frac{1 + 1/m}{\alpha_m}\bigl(\ln \frac{1}{1 - \alpha_m} + o(1)\bigr) \to \frac{1}{\alpha}\ln\frac{1}{1-\alpha}$. $\blacksquare$

## Consequences

**The cost at common loads.** The limits of Part 5, against [linear probing](/linear-probing/) (Knuth's formulas, proved on the [linear probing analysis](/linear-probing-analysis/) page) and [separate chaining](/separate-chaining/) (keys examined, from [expected search time with chaining](/chaining-expected-search-time/)):

| $\alpha$ | uniform, unsuccessful | uniform, successful | standard deviation, unsuccessful | linear probing, unsuccessful | linear probing, successful | chaining, unsuccessful | chaining, successful |
|---|---|---|---|---|---|---|---|
| 0.25 | 1.333 | 1.151 | 0.667 | 1.389 | 1.167 | 0.25 | 1.125 |
| 0.5 | 2 | 1.386 | 1.414 | 2.5 | 1.5 | 0.5 | 1.25 |
| 0.75 | 4 | 1.848 | 3.464 | 8.5 | 2.5 | 0.75 | 1.375 |
| 0.9 | 10 | 2.558 | 9.487 | 50.5 | 5.5 | 0.9 | 1.45 |
| 0.95 | 20 | 3.153 | 19.494 | 200.5 | 10.5 | 0.95 | 1.475 |

At $\alpha = 1/2$, a failed search costs 2 probes and a successful one about 1.39. The standard deviation $\sqrt{\alpha}/(1-\alpha)$ is about as large as the mean, so single failed searches vary a lot.

**Small tables.** For $m = 8$ and $n = 6$, Part 2 gives $\mathrm{E}[X] = 9/3 = 3$, Part 3 gives $\mathrm{Var}[X] = 6 \cdot 9 \cdot 2/(9 \cdot 4) = 3$, and the limit $\alpha/(1-\alpha)^2 = 12$ overstates it, since in a small table the search cannot probe more than $n + 1$ slots. For $m = 1000$, the exact means are $\mathrm{E}[X] \approx 1.998$ and $C_n \approx 1.385$ at $n = 500$, and $\mathrm{E}[X] \approx 9.911$ and $C_n \approx 2.546$ at $n = 900$, a little below the limits.

**The full table.** With $n = m - 1$, the last insertion costs $(m+1)/2$ probes on average. With $n = m$, Part 4 still holds and gives $C_m = \frac{m+1}{m}(H_{m+1} - 1)$, about $\ln m$; for $m = 1000$ it is about 6.49. So searching a full table for stored keys is cheap on average, but each failed search scans the whole table.

**Design rule.** Since the unsuccessful cost $1/(1-\alpha)$ grows without bound as $\alpha \to 1$, open-addressing tables grow before they are full, typically at a load between $1/2$ and $7/8$, and the bounds then give $O(1)$ expected time per operation.

**Deletions.** The proof needs that keys never move and that slots never become free again. With [lazy deletion](/lazy-deletion/), deleted slots stay marked, a search treats them as full, and the formulas hold with $n$ counting the marked slots too. Removing keys outright breaks the searches for keys that were inserted past them.

## Tightness

**The bounds are reached in the limit.** Part 5 shows that $1/(1-\alpha)$ and $(1/\alpha)\ln(1/(1-\alpha))$ are the exact limits, so no better bound in terms of $\alpha$ alone holds for large tables. For finite $m$ the exact values are smaller, as the table for $m = 1000$ shows: $(m+1)/(m-n+1) < m/(m-n)$ whenever $n \ge 1$.

**No open-addressing scheme does much better.** Yao proved that, for open-addressing schemes in which keys do not move after insertion, the expected cost of a successful search is at least $(1/\alpha)\ln(1/(1-\alpha)) - o(1)$, so uniform probing is asymptotically optimal among them; see [Yao's lower bound](/yao-open-addressing-lower-bound/). Schemes that move keys, such as [Robin Hood hashing](/robin-hood-hashing/) and [cuckoo hashing](/cuckoo-hashing/), escape this bound.

**Real schemes are not uniform.** [Linear probing](/linear-probing/) has only $m$ distinct probe sequences, and [primary clustering](/primary-clustering/) makes its costs grow like $1/(1-\alpha)^2$, as the table shows. [Quadratic probing](/quadratic-probing/) avoids primary clustering but keeps [secondary clustering](/secondary-clustering/). [Double hashing](/double-hashing/) has $m(m-1)$ sequences for prime $m$ and matches the formulas of uniform hashing asymptotically, by the results of Guibas and Szemeredi and of Lueker and Molodowitch quoted on the [uniform hashing assumption](/uniform-hashing-assumption/) page.

## History

The analysis of uniform probing goes back to the first papers on hashing in the 1950s, and Knuth gives the exact formulas in Section 6.4 together with the analysis of linear probing, which he derived in 1962. CLRS proves the bounds $1/(1-\alpha)$ and $(1/\alpha)\ln(1/(1-\alpha))$ in Section 11.4 by the tail sum and the integral bound used above. Yao, in 1985, showed that uniform probing is optimal among open-addressing schemes that do not move keys.

## References
