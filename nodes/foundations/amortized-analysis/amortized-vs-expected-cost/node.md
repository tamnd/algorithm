---
tag: 57RJ85
kind: concept
slug: amortized-vs-expected-cost
name: Amortized versus expected cost
aliases:
- expected amortized cost
area: foundations/amortized-analysis
level: core
summary: Amortized analysis averages over operations deterministically, while expected cost averages over random choices.
prereqs: [amortized-cost, expected-value, randomized-algorithm]
see_also: [amortized-vs-worst-case, average-case-analysis, expected-running-time, linearity-of-expectation, oblivious-adversary, cuckoo-hashing, dynamic-perfect-hashing, treap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Probabilistic Analysis and Randomized Algorithms; Chapter 16, Amortized Analysis (introduction, which separates the two notions)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press (1995)
    locator: Chapter 1, Introduction (expected running time, Las Vegas and Monte Carlo algorithms); Chapter 8, Data Structures (treaps, skip lists, hash tables)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
  - paper: doi:10.1137/S0097539791194094
    title: Martin Dietzfelbinger, Anna Karlin, Kurt Mehlhorn, Friedhelm Meyer auf der Heide, Hans Rohnert and Robert E. Tarjan, Dynamic perfect hashing, upper and lower bounds, SIAM Journal on Computing 23(4), 1994
    locator: pp. 738 to 761
  - paper: doi:10.1016/j.jalgor.2003.12.002
    title: Rasmus Pagh and Flemming Friche Rodler, Cuckoo hashing, Journal of Algorithms 51(2), 2004
    locator: pp. 122 to 144
  - paper: doi:10.1145/2786.2793
    title: Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2), 1985
    locator: pp. 202 to 208
---

Amortized cost and expected cost are two different kinds of average. An [amortized](/amortized-cost/) bound averages over the operations of one sequence: it is a certain bound on the total cost of each sequence, with no randomness. An [expected](/expected-value/) bound averages over the random choices of a [randomized algorithm](/randomized-algorithm/) (or, in [average-case analysis](/average-case-analysis/), over a random input): it says nothing certain about one run. The two combine into *expected amortized* bounds, such as the $O(1)$ insertion time of [cuckoo hashing](/cuckoo-hashing/) and of [dynamic perfect hashing](/dynamic-perfect-hashing/).

## In plain words

Both words mean "on average", but over different things. An amortized promise looks at a long run of calls to a data structure and says that the total time is at most a fixed amount per call. It holds for every run, every time, with no luck involved. Some calls may be slow, but the run as a whole is always fast. An expected promise is about chance. The algorithm flips coins, and the promise says that the time, averaged over all possible coin flips, is small. On a given day the coins can fall badly, and the run can be slow, even if that is rare. A third kind of average is over the inputs: it says the time is small for a typical input, but a bad input can still be slow.

## The idea

Let $\sigma = (o_1, \ldots, o_m)$ be a legal sequence of operations and $c_i$ the cost of $o_i$.

- **Amortized bound $a$.** For each sequence $\sigma$ and each $m$: $\sum_{i \le m} c_i \le a\,m$. Deterministic and certain.
- **Expected bound $e$ (randomized algorithm, worst-case input).** The algorithm uses random bits $r$. For each sequence $\sigma$ fixed in advance and each $i$: $\mathbb{E}_r[c_i] \le e$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}_r\big[\sum_{i \le m} c_i\big] \le e\,m$.
- **Average-case bound (deterministic algorithm, random input).** For a distribution on the inputs, $\mathbb{E}_\sigma[c_i] \le e$. This depends on the distribution, and a bad input exists.
- **Expected amortized bound.** For each sequence $\sigma$ fixed in advance and each $m$: $\mathbb{E}_r\big[\sum_{i \le m} c_i\big] \le a\,m$. Single operations may be slow even with good coins, and the total may be slow with bad coins.

**What each one gives, and what it does not.**

1. An amortized bound gives a certain bound on each total. It gives no bound on one operation.
2. An expected bound gives no certain bound on any total. By the [Markov inequality](/markov-inequality/), the total exceeds $t$ times its expectation with probability at most $1/t$; stronger tail bounds need more structure, such as independence.
3. An expected bound for each operation does not give an amortized bound, and an amortized bound does not give an expected bound for one operation (the expensive operation of a doubling array happens with certainty at a fixed position of the sequence).
4. Expected bounds for data structures assume that the sequence does not depend on the random choices, that is, an [oblivious adversary](/oblivious-adversary/). If the user can see the effect of the coins (for example, by timing) and choose the next operation from it, an [adaptive adversary](/adaptive-adversary/) can force bad cases. Amortized bounds need no such assumption: they hold for each sequence, however it is chosen.

## Examples

**The same mean, two kinds of guarantee.** Take a structure that does a cleanup of cost 100 at some operations and costs 1 otherwise, for $m = 1000$ operations.

- *Deterministic rule:* clean up at each 100th operation. There are exactly 10 cleanups, and the total is exactly $990 + 1000 = 1990$ for each sequence. The amortized cost is below 2.
- *Random rule:* clean up with probability $\tfrac{1}{100}$ at each operation, independently. The expected total is also 1990, so the expected cost is below 2 per operation. But the number $X$ of cleanups is binomial with mean 10. $\Pr[X \ge 20] \approx 0.0033$, and then the total is at least $980 + 2000 = 2980$; $\Pr[X \ge 30] \approx 2.1 \times 10^{-7}$, with a total of at least 3970. No total below $100{,}000$ is certain.

**Binary counter: amortized and average-case.** For a [binary counter](/binary-counter-increment/) that starts at 0, $n$ increments flip exactly $2n - s_2(n)$ bits, so the amortized cost is less than 2 for each $n$, with certainty. Separately, if a $k$-bit counter holds a uniformly random value, one increment flips $2 - 2^{1-k}$ bits in expectation: $\tfrac74$ for $k = 3$ and $\tfrac{15}{8}$ for $k = 4$. The numbers are close, but the statements differ. The amortized one is about every sequence from 0; the average-case one is about one increment from a random state, and says nothing about a counter that a user sets to $2^k - 1$ before each increment.

**Hash tables.** With chaining and a hash function from a [universal family](/universal-hashing/), a search takes $O(1 + n/m)$ expected time on a table with $m$ slots, for each fixed set of keys. If the table doubles when $n/m$ exceeds a constant, the resize costs are amortized, and an insertion takes $O(1)$ expected amortized time. Both averages are needed: the expectation for the chains and the amortization for the resizes.

**Cuckoo hashing.** Pagh and Rodler (2004) give a dictionary with lookups in $O(1)$ worst-case time (two probes) and insertions in $O(1)$ expected amortized time. An insertion can fail and force a rehash with new hash functions, which is both rare (expected) and paid by earlier insertions (amortized).

**Dynamic perfect hashing.** Dietzfelbinger and others (1994) give $O(1)$ worst-case lookups and $O(1)$ expected amortized updates. The expectation covers the random choice of hash functions; the amortization covers the periodic global rebuild.

**Balanced search trees.** A [treap](/treap/) or a [skip list](/skip-list/) has $O(\log n)$ expected time for each operation, for each sequence fixed in advance. A [splay tree](/splay-tree/) has $O(\log n)$ amortized time for each operation, deterministically. A single treap operation is slow only with small probability; a single splay operation can be slow with certainty on some sequences, but the total of each sequence is $O(m \log n)$.

**Randomized quicksort.** [Randomized quicksort](/randomized-quicksort/) runs in $O(n \log n)$ expected time on each input. This is an expected bound on one run of an algorithm, not an amortized bound: there is no sequence of operations to average over.

## Where it is used

- **Choosing a data structure.** If each operation must be fast with certainty, neither kind is enough; use worst-case structures (see [amortized versus worst-case cost](/amortized-vs-worst-case/)). If only the total matters and inputs may be hostile, amortized deterministic bounds are the safest. If inputs are not hostile, randomized structures are often simpler and faster.
- **Security.** A hash table whose expected bound depends on a secret random hash function, such as [SipHash](/siphash/) with a random key, keeps its bound against users who cannot learn the key. With a fixed public hash function, an attacker can choose colliding keys and make $n$ operations cost $\Theta(n^2)$. Amortization alone does not protect against this.
- **Online algorithms.** Sleator and Tarjan (1985) used amortized analysis with a potential to compare [move-to-front](/move-to-front/) with each other list rule on the same sequence; this gave a deterministic bound that started the study of the [competitive ratio](/competitive-ratio/). Randomized online algorithms instead bound the expected cost against an oblivious adversary.
- **Analysis of algorithms that use both.** Proofs of expected amortized bounds usually take the expectation of a potential argument: show that $\mathbb{E}[\hat c_i] \le a$ for each operation, with a potential that is never negative, and add the expectations.

## References
