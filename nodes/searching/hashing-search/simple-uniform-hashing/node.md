---
tag: XR1VA1
kind: definition
slug: simple-uniform-hashing
name: Simple uniform hashing assumption
aliases:
- SUHA
- simple uniform hashing
- uniform hashing assumption
- independent uniform hashing
area: searching/hashing-search
level: core
summary: Each key is equally likely to hash to any slot, independently of other keys.
prereqs: [hash-function, probability-space, independent-random-variables]
see_also: [uniform-hashing-assumption, chaining-expected-search-time, chaining-analysis, universal-hash-family, k-wise-independent-hashing, balls-into-bins, random-oracle-model, open-addressing-expected-probes]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 11 (Hash tables), Section 11.2 (the independent uniform hash function and the analysis of chaining) and Section 11.3 (random hashing and universal hashing)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of chaining under the assumption that the hash values are independent and uniform
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2) (1979)
    locator: pages 143 to 154 (the critique of averaging over the keys, and the move to a random choice of the function)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5 (Balls, bins and random graphs), the hashing applications of the balls and bins model
---

The simple uniform hashing assumption says that the hash values of distinct keys behave like independent random variables, each uniform on the $m$ slots of the table. It is the probabilistic model under which the classic expected costs of [separate chaining](/separate-chaining/) are derived, such as the [expected search time](/chaining-expected-search-time/) $\Theta(1 + \alpha)$. No single fixed [hash function](/hash-function/) satisfies it for all inputs, so it is either an assumption on the distribution of the keys or a property of a random choice of the function. This page gives the exact statement in both readings and separates it from the weaker and stronger conditions that are often confused with it.

## Definition

Let $U$ be the universe of keys, let $m \ge 1$, and write $[m] = \{0, 1, \ldots, m - 1\}$ for the slots of the table.

**Random-function reading.** Let $h$ be a random function from $U$ to $[m]$, drawn from some distribution on such functions, independently of the keys. The distribution satisfies **simple uniform hashing** if, for every $n \ge 1$, every list of distinct keys $x_1, \ldots, x_n \in U$ and every list of slots $s_1, \ldots, s_n \in [m]$,
$$\Pr[h(x_1) = s_1, \ h(x_2) = s_2, \ \ldots, \ h(x_n) = s_n] = m^{-n}.$$
Equivalently, the values $h(x_1), \ldots, h(x_n)$ are [independent random variables](/independent-random-variables/), each uniform on $[m]$. When $U$ is finite this holds if and only if $h$ is uniform over all $m^{|U|}$ functions from $U$ to $[m]$, a *truly random function*. CLRS (fourth edition) calls such an $h$ an *independent uniform hash function*.

**Random-keys reading.** Let $h$ be a fixed function, and let the keys $K_1, \ldots, K_n$ be random. The input satisfies simple uniform hashing if $h(K_1), \ldots, h(K_n)$ are independent and uniform on $[m]$. This is the form of earlier textbooks, which state that each element is equally likely to hash into any of the $m$ slots, independently of where the others hashed. It is a statement about the input distribution, not about $h$.

**What is required for a given analysis.** Most proofs use only the keys that one execution touches. An analysis of $n$ stored keys and one searched key needs the condition only for lists of at most $n + 1$ distinct keys. With the condition for lists of length at most $k$ only, the family is uniform and *$k$-wise independent*; see [k-wise independent hashing](/k-wise-independent-hashing/).

**The open-addressing form.** For [open addressing](/open-addressing/), each key needs a whole probe sequence, not one slot. The stronger *uniform hashing* assumption says that the probe sequences of distinct keys are independent, each a uniformly random permutation of $[m]$. Simple uniform hashing says nothing about the second and later probes. The stronger model is the subject of the [uniform hashing assumption](/uniform-hashing-assumption/) page and of the [expected probes](/open-addressing-expected-probes/) theorem.

**Immediate facts.** Under simple uniform hashing, for $n$ distinct stored keys:

- the slot of each key is uniform, and two distinct keys collide with probability exactly $1/m$;
- the number of keys in a fixed slot is [binomial](/binomial-distribution/) with parameters $n$ and $1/m$, with mean $\alpha = n/m$;
- the vector of slot counts is multinomial: the table is the [balls into bins](/balls-into-bins/) model with $n$ balls and $m$ bins;
- the expected number of colliding pairs is $\binom{n}{2}/m$, by [linearity of expectation](/linearity-of-expectation/) over the pairs.

## Examples and non-examples

**A truly random function.** Let $U = \{a, b, c\}$ and $m = 2$, and let $h$ be uniform over the $2^3 = 8$ functions. Each of the 8 lists $(h(a), h(b), h(c))$ has probability $1/8$, so the definition holds for all key lists. Storing such an $h$ needs a table of $|U| \lceil \lg m \rceil$ bits, here 3 bits; for 64-bit keys it needs $2^{64}$ entries, which is why the model is not a recipe for building $h$.

**Uniform keys and the division method.** Let $U = \{0, \ldots, 11\}$, $m = 4$ and the fixed function $h(k) = k \bmod 4$. If the keys are drawn independently and uniformly from $U$, each slot receives exactly 3 of the 12 keys of $U$, so each $h(K_i)$ is uniform on $[4]$, and the $h(K_i)$ are independent because the $K_i$ are. So the random-keys reading holds. If the keys are the even numbers of $U$, only slots 0 and 2 are used, and it fails: the assumption is about the input.

**Non-example: one random slot for all keys.** Let $r$ be uniform on $[m]$ and $h(x) = r$ for every key. Each single key is uniform, but any two keys collide with probability 1. Uniformity of each value alone is not enough; the independence is the part that keeps the chains short.

**Non-example: a universal family.** Let $U = \{0, 1\}^2$, $m = 2$, and $h_a(x) = a_1 x_1 + a_2 x_2 \bmod 2$ with $a$ uniform on $\{0,1\}^2$. For $x \ne y$, $h_a(x) = h_a(y)$ exactly when $a \cdot (x - y) = 0 \pmod 2$, which holds for 2 of the 4 choices of $a$, so collisions have probability $1/2 = 1/m$ and the family is a [universal family](/universal-hash-family/). For the keys $x = (1, 0)$ and $y = (0, 1)$, the pair $(h_a(x), h_a(y)) = (a_1, a_2)$ is even uniform on all 4 values. But $z = (1, 1)$ has $h_a(z) = h_a(x) + h_a(y) \bmod 2$, so $\Pr[h_a(x) = 0, h_a(y) = 0, h_a(z) = 1] = 0 \ne 1/8$. The family is pairwise independent and fails simple uniform hashing on three keys. Also the key $(0, 0)$ always goes to slot 0. Universality bounds the expected chain length, as the [universal hashing lemma](/universal-hashing-lemma/) shows, but not every quantity that the model gives.

**Non-example: a fixed function and arbitrary keys.** For a fixed $h$ and $|U| \ge (n - 1) m + 1$, the [pigeonhole principle](/pigeonhole-principle/) gives a slot that receives at least $n$ keys of $U$. An input made of these $n$ keys puts all of them in one chain. So no fixed function satisfies the assumption in the worst case, and the random-function reading needs randomness in $h$, as in [universal hashing](/universal-hashing/), while the random-keys reading needs keys that do not depend on $h$. Inputs built to break a known $h$ are an [algorithmic complexity attack](/algorithmic-complexity-attack/).

**Practical functions.** Fast functions such as [MurmurHash](/murmurhash/) or [xxHash](/xxhash/) are fixed functions, so they satisfy neither reading in the worst case; analyses that use the model for them are heuristic. A keyed [pseudorandom function](/pseudorandom-function/) such as [SipHash](/siphash/), with a secret random key, is designed so that no efficient adversary can tell it from a truly random function, which makes the random-function reading a sound working model against such adversaries. [Tabulation hashing](/tabulation-hashing/) is 3-wise independent and provably matches several bounds of the model, though not all.

## Related definitions

- [Uniform hashing assumption](/uniform-hashing-assumption/): the concept page for the model, including its stronger form with random probe permutations.
- [Universal hash family](/universal-hash-family/): the weaker condition $\Pr[h(x) = h(y)] \le 1/m$ for each pair, which a small family can meet.
- [k-wise independent hashing](/k-wise-independent-hashing/): the condition of this page restricted to lists of at most $k$ keys.
- [Random oracle model](/random-oracle-model/): the same idealization in cryptography, where all parties query one truly random function.
- [Balls into bins](/balls-into-bins/): the probability model that the slot counts follow under the assumption.
- [Expected search time with chaining](/chaining-expected-search-time/) and [analysis of separate chaining](/chaining-analysis/): the main results proved under the assumption.

## References
