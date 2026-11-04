---
tag: 7DQ08F
kind: concept
slug: uniform-hashing-assumption
name: Uniform hashing assumption
aliases:
- simple uniform hashing
area: data-structures/hashing
level: intro
summary: Modelling assumption that each key is equally likely to hash to any slot, independently of others.
prereqs: [hash-function, load-factor, linearity-of-expectation]
see_also: [simple-uniform-hashing, separate-chaining, open-addressing, universal-hashing, k-wise-independent-hashing, double-hashing, yao-open-addressing-lower-bound, linear-probing-analysis]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (the random hashing model for chaining) and Section 11.4 (the model of random probe sequences for open addressing, and its analysis)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing (the analysis of uniform probing, and of double hashing as compared with it)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2) (1979)
    locator: pages 143 to 154
  - paper: "Leo J. Guibas and Endre Szemeredi, The analysis of double hashing, Journal of Computer and System Sciences 16(2) (1978)"
    locator: pages 226 to 274
  - paper: "George S. Lueker and Mariko Molodowitch, More analysis of double hashing, Combinatorica 13(1) (1993)"
    locator: pages 83 to 96
---

The uniform hashing assumption is the model in which the [hash function](/hash-function/) of a table behaves like a truly random function: each key goes to each of the $m$ slots with probability $1/m$, independently of all other keys. For [open addressing](/open-addressing/) the stronger form says that the whole probe sequence of each key is a uniformly random order of the $m$ slots, again independently for each key. Under these assumptions the expected costs of a table depend only on the [load factor](/load-factor/) $\alpha$, and they have short exact formulas. No single fixed hash function satisfies the assumption for every input, so it is a model, and the results that hold under it are checked separately for the hash functions that tables use.

## In plain words

To analyze a hash table, we need to know where its keys land. Real hash functions are fixed rules, and for some bad inputs a fixed rule puts many keys in the same place. The analysis therefore uses an ideal model instead: we pretend that each key picks its slot by a fair roll of a die with one face per slot, and that the rolls for different keys do not affect each other.

With this model, the questions "how long is a chain" and "how many places does a search look at" become simple counting questions with clean answers. The answers describe well what good hash functions do on typical data. They do not protect against an attacker who knows the hash rule and picks the keys.

## The idea

Let $U$ be the set of possible keys and let the table have slots $\{0, \ldots, m-1\}$.

**Simple uniform hashing.** The values $h(k)$ for distinct keys $k$ are independent random variables, and each is uniform on $\{0, \ldots, m-1\}$. In other words, $h$ is a function chosen uniformly at random among all $m^{|U|}$ functions from $U$ to the slots. This is the model for [separate chaining](/separate-chaining/). The name follows CLRS, third edition. Other names are *totally random hashing* and, in cryptography, the *random oracle*.

**Uniform hashing for probe sequences.** An open-addressing table probes the slots $h(k, 0), h(k, 1), \ldots, h(k, m-1)$, a [probe sequence](/probe-sequence/) that is a permutation of the slots. The assumption is that the probe sequences of distinct keys are independent, and each is uniform among the $m!$ permutations. Knuth calls a scheme with this property *uniform probing*.

**Two readings.** The probability can come from the input or from the hash function. In the first reading, the keys are random and $h$ is fixed, so the results are average-case bounds over inputs. In the second reading, the input is fixed in advance, before $h$ is drawn, and $h$ is random, so the results are expected bounds of a [randomized algorithm](/randomized-algorithm/) for every input. The second reading is the one that a [universal](/universal-hashing/) or [$k$-wise independent](/k-wise-independent-hashing/) family makes true in part.

**No fixed function satisfies it.** Let $h$ be any fixed function and let $|U| > (n-1)m$. By the pigeonhole principle, some slot $j$ has at least $n$ keys $k$ with $h(k) = j$. An input of $n$ of these keys puts all of them in slot $j$, so a search costs $\Theta(n)$. So a statement such as "each operation costs $O(1)$ expected time" is true for a fixed $h$ only on average over some input distribution, never for every input.

### The cost of open addressing under uniform hashing

**Claim.** Assume uniform hashing for probe sequences, with $n < m$ keys in the table and no deletions. Let $X$ be the number of probes of an unsuccessful search, which is also the number of probes of the next insertion. Then

$$\mathrm{E}[X] = \frac{m+1}{m-n+1} \le \frac{1}{1-\alpha}, \qquad \alpha = \frac{n}{m}.$$

*Proof.* Keys never move after insertion, so the set $S$ of the $n$ full slots depends only on the probe sequences of the stored keys. The probe sequence $\pi$ of the new key is independent of these, so it is a uniform permutation of the slots, independent of $S$. The search probes the slots in the order $\pi$ and stops at the first slot that is not in $S$. So $X = 1 + G$, where $G$ is the number of full slots that come before every empty slot in $\pi$. For a full slot $s$, consider the $m - n + 1$ slots formed by $s$ and the $m - n$ empty slots. Their relative order in $\pi$ is uniform, so $s$ is first among them with probability $1/(m - n + 1)$. By [linearity of expectation](/linearity-of-expectation/) over the $n$ full slots, $\mathrm{E}[G] = n/(m - n + 1)$, and $\mathrm{E}[X] = 1 + n/(m-n+1) = (m+1)/(m-n+1)$.

For the bound, $\Pr[X > i]$ is the probability that the first $i$ probes all hit $S$. This is $\prod_{j=0}^{i-1} (n-j)/(m-j)$ for $i \le n$ and 0 for $i > n$. Each factor is at most $n/m = \alpha$, because $n \le m$. So $\mathrm{E}[X] = \sum_{i \ge 0} \Pr[X > i] \le \sum_{i \ge 0} \alpha^i = 1/(1 - \alpha)$. $\square$

**Successful search.** A search for a key follows the same probes as its insertion. If the key was the $(i+1)$-th key inserted, its insertion met $i$ keys, so its expected cost is $(m+1)/(m-i+1)$. Averaged over the $n$ keys, the expected cost of a successful search for a random stored key is

$$\frac{1}{n} \sum_{i=0}^{n-1} \frac{m+1}{m-i+1} = \frac{m+1}{n} \bigl(H_{m+1} - H_{m-n+1}\bigr) \le \frac{1}{n} \sum_{i=0}^{n-1} \frac{m}{m-i} \le \frac{1}{\alpha} \int_{m-n}^{m} \frac{dx}{x} = \frac{1}{\alpha} \ln \frac{1}{1-\alpha}.$$

Here $H_k$ is the $k$-th harmonic number. The first inequality holds because $(m+1)/(m-i+1) \le m/(m-i)$ for $0 \le i < m$. The second bounds each term $1/k$ by the integral of $1/x$ over $[k-1, k]$. These are the formulas of Knuth for uniform probing, and the bounds of CLRS Section 11.4.

### How real hash functions relate to the model

- **Chaining needs much less.** The expected length of a chain is at most $\alpha$ for a key not in the table if only each pair of distinct keys collides with probability at most $1/m$. This is the property of a [universal hash family](/universal-hash-family/) of Carter and Wegman. Bounds on the longest chain need more independence.
- **Linear probing is not uniform probing.** [Linear probing](/linear-probing/) has only $m$ different probe sequences, one for each start slot, not $m!$. Its analysis assumes only that the start slots are uniform and independent, and its costs are larger than those of uniform probing, because of primary clustering.
- **Double hashing comes close.** [Double hashing](/double-hashing/) with $m$ prime has only $m(m-1)$ probe sequences. Guibas and Szemeredi proved that its expected cost of an insertion is asymptotically that of uniform probing for $\alpha$ below about $0.319$. Lueker and Molodowitch extended this to every fixed $\alpha < 1$.
- **The model is a lower bound for open addressing.** Among open-addressing schemes in which keys do not move, no scheme beats uniform probing by much in the expected cost of a successful search. This is [Yao's lower bound](/yao-open-addressing-lower-bound/).

## Examples

**Collisions among a few keys.** Under simple uniform hashing, two given distinct keys collide with probability $1/m$. With 23 keys and $m = 365$, the expected number of colliding pairs is $\binom{23}{2}/365 = 253/365 \approx 0.69$. This is the setting of the [birthday paradox](/birthday-paradox/).

**An insertion into a table with 8 slots.** Let $m = 8$ and $n = 6$, so $\alpha = 3/4$. Under uniform probing, the expected number of probes of the next insertion is $(8+1)/(8-6+1) = 3$. The bound $1/(1-\alpha)$ gives 4. A count over all $8! = 40\,320$ probe sequences, with 6 fixed full slots, gives the same mean of 3 probes. The expected cost of a successful search in this table is $(9/6)(H_9 - H_3) = 2509/1680 \approx 1.49$ probes, and the bound $(1/\alpha)\ln(1/(1-\alpha))$ gives about $1.85$.

**A non-example: keys with a pattern.** Let $h(k) = k \bmod 8$ and let the keys be $0, 8, 16, 24, 32$. All five keys go to slot 0, while the model predicts an expected chain length of $5/8$ for each slot. A hash function that ignores some bits of the key fails the assumption on keys that differ only in those bits.

**A non-example: an adversary.** An attacker who knows a fixed hash function, such as the default string hash of a language without a random seed, can produce many keys with equal hash values. This is the [algorithmic complexity attack](/algorithmic-complexity-attack/), and it is the reason that many libraries now draw a random seed at start-up.

## Where it is used

- The expected costs of [separate chaining](/separate-chaining/) and the theorem on [chaining analysis](/chaining-analysis/).
- The analysis of [open addressing](/open-addressing/), [double hashing](/double-hashing/) and the [probe sequence](/probe-sequence/) model, and [Yao's lower bound](/yao-open-addressing-lower-bound/).
- The [analysis of linear probing](/linear-probing-analysis/), which uses uniform and independent start slots.
- The false positive rate of a [Bloom filter](/bloom-filter/), and the analysis of [cuckoo hashing](/cuckoo-hashing/).
- The [balls into bins](/balls-into-bins/) model, which is simple uniform hashing under another name.
- The design of [universal](/universal-hashing/), [$k$-wise independent](/k-wise-independent-hashing/) and [tabulation](/tabulation-hashing/) hash functions, which aim to give some of the guarantees of the model with a short random seed.

## References
