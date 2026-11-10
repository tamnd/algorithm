---
tag: 68DH25
kind: theorem
slug: universal-hashing-expected-chain-length
name: Expected chain length under universal hashing
aliases:
- universal hashing analysis
- expected chain length bound
- Carter-Wegman chain length bound
area: randomized/random-hashing
level: core
summary: With a universal family, expected search cost in a chained table with load factor alpha is O(1 + alpha) for any key set.
prereqs: [universal-hash-family, separate-chaining, indicator-random-variable, linearity-of-expectation]
see_also: [universal-hashing-lemma, universal-hashing, pairwise-independence, k-independent-hashing, dot-product-hashing, multiply-shift-hashing, perfect-hashing, load-factor]
sources:
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 143 to 154, 1979
    locator: the definition of a universal class and the bound on the expected cost of operations with chaining for any fixed sequence of requests
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 11.3 (Hash functions), the theorem on the expected length of the list of a key under universal hashing and its corollary for a sequence of operations
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 15.3 (Universal Families of Hash Functions), the expected number of items in the bin of a key and the use for perfect hashing
---

## Statement

Let $\mathcal{H}$ be a universal family of functions from a universe $U$ to the slots $\{0, \ldots, m-1\}$: $\Pr_h[h(x) = h(y)] \le 1/m$ for all distinct $x, y \in U$, for $h$ drawn uniformly from $\mathcal{H}$. Fix a set $S \subseteq U$ of $n$ keys before $h$ is drawn, store $S$ in a table with [separate chaining](/separate-chaining/) under $h$, and let $\alpha = n/m$ be the [load factor](/load-factor/). For a key $x \in U$ let $L(x)$ be the number of keys of $S$ in the chain of slot $h(x)$, and let $L_j$ be the length of the chain of slot $j$.

**Theorem (Carter and Wegman 1979).**

1. If $x \notin S$, then $E[L(x)] \le \alpha$.
2. If $x \in S$, then $E[L(x)] \le 1 + (n-1)/m < 1 + \alpha$.
3. $E\big[\sum_j L_j^2\big] \le n + n(n-1)/m$. So the expected number of colliding pairs $C = \sum_j \binom{L_j}{2}$ is at most $\binom{n}{2}/m$, and the average of $L(x)$ over the stored keys $x \in S$ has expectation at most $1 + (n-1)/m$.
4. Any fixed sequence of $s$ operations (insert, delete, search) on a table that never holds more than $n$ keys takes $O(s(1 + \alpha))$ expected time, if each operation costs $O(1)$ plus the length of the chain it scans and $h$ takes $O(1)$ time.

If the family is only $c/m$-almost universal, the same bounds hold with $\alpha$ replaced by $c\alpha$ and $(n-1)/m$ by $c(n-1)/m$.

## In plain words

A hash table with chains is fast when the chain you search is short. For one fixed hash function, someone can always pick keys that all land in one slot. Universal hashing picks the function at random after the keys are fixed, from a family where any two keys share a slot at most one time in $m$.

Then the chain you search holds, on average, at most the keys per slot, plus the key itself if it is stored. No key set is bad on average. The random choice is the algorithm's, so the guarantee holds for every input, not only for random inputs.

## Proof

For $y \in S$, let $I_{xy}$ be the [indicator](/indicator-random-variable/) of the event $h(x) = h(y)$. The chain of slot $h(x)$ holds exactly the keys $y \in S$ with $h(y) = h(x)$, so
$$L(x) = \sum_{y \in S} I_{xy}.$$

*Part 1.* If $x \notin S$, each $y \in S$ differs from $x$, so $E[I_{xy}] = \Pr[h(x) = h(y)] \le 1/m$. By [linearity of expectation](/linearity-of-expectation/), $E[L(x)] \le n/m = \alpha$.

*Part 2.* If $x \in S$, the term $y = x$ is always 1, and the other $n - 1$ terms have expectation at most $1/m$. So $E[L(x)] \le 1 + (n-1)/m$, and $(n-1)/m < n/m = \alpha$.

*Part 3.* Count ordered pairs: $\sum_j L_j^2$ is the number of ordered pairs $(x, y) \in S \times S$ with $h(x) = h(y)$. The $n$ pairs with $x = y$ always count. Each of the $n(n-1)$ pairs with $x \ne y$ counts with probability at most $1/m$. So $E[\sum_j L_j^2] \le n + n(n-1)/m$. Since $\sum_j L_j = n$, $C = \frac{1}{2}\big(\sum_j L_j^2 - n\big)$, so $E[C] \le n(n-1)/(2m) = \binom{n}{2}/m$. Finally $\sum_{x \in S} L(x) = \sum_j L_j \cdot L_j$, because each of the $L_j$ keys in slot $j$ sees a chain of length $L_j$. Dividing by $n$ gives the average over stored keys.

*Part 4.* Before each operation the table holds a set of at most $n$ keys that depends only on the fixed sequence, not on $h$. By parts 1 and 2 the expected length of the chain the operation scans is at most $1 + \alpha$, so its expected cost is $O(1 + \alpha)$. Linearity of expectation over the $s$ operations gives $O(s(1 + \alpha))$.

*Almost universal families.* Replace $1/m$ by $c/m$ in each step. $\blacksquare$

## Consequences

- **Constant expected time.** With $m = \Theta(n)$ slots, for example by doubling the table when $\alpha$ exceeds a constant, each dictionary operation takes $O(1)$ expected time for every input. This is the standard guarantee for chained tables with [dot-product](/dot-product-hashing/), Carter-Wegman or [multiply-shift](/multiply-shift-hashing/) hashing; for multiply-shift the stored-key bound reads $1 + 2(n-1)/m$.
- **No collisions with quadratic space.** With $m = n^2$, part 3 gives $E[C] \le \binom{n}{2}/n^2 < 1/2$, so by Markov's inequality $h$ is injective on $S$ with probability more than $1/2$. With $m = n$, $E[C] < n/2$. Both facts are the two levels of FKS [perfect hashing](/perfect-hashing/).
- **A bound on the longest chain.** For $m = n$, part 3 gives $E[\binom{L_{\max}}{2}] \le E[C] \le (n-1)/2$, so $E[L_{\max}] = O(\sqrt{n})$. Better bounds need more independence; see [k-independent hashing](/k-independent-hashing/).
- **Rehash when unlucky.** By Markov's inequality, $\Pr[L(x) \ge 2(1 + \alpha)] \le 1/2$. A table that draws a new $h$ when a chain is far too long has expected $O(1)$ rehashes.

**Example with exact numbers.** Take the Carter-Wegman family $h_{a,b}(x) = ((ax + b) \bmod 17) \bmod 6$ with $a \in \{1, \ldots, 16\}$ and $b \in \{0, \ldots, 16\}$, 272 functions, and the six keys $S = \{0, 1, 6, 7, 12, 13\}$, so $\alpha = 1$. The fixed function $x \bmod 6$ puts $0, 6, 12$ in one chain. Averaged over the 272 functions, the absent key 3 has $E[L(3)] = 12/17 \approx 0.71 \le 1$, the stored key 0 has $E[L(0)] = 27/17 \approx 1.59 \le 1 + 5/6$, and $E[\sum_j L_j^2] = 162/17 \approx 9.53 \le 6 + 30/6 = 11$. Here every pair collides with probability at most $2/17 < 1/6$, which is why the values are below the bounds.

## Tightness

- **The bounds are reached.** For a [pairwise independent](/pairwise-independence/) family, or for the family of all functions, $\Pr[h(x) = h(y)] = 1/m$ exactly, so parts 1, 2 and 3 hold with equality: $E[L(x)] = n/m$ for an absent key, and $1 + (n-1)/m$ for a stored key.
- **The collision bound is nearly optimal.** No family can have collision probability much below $1/m$ for all pairs when $|U|$ is much larger than $m$: every function splits the $|U|$ keys into $m$ slots and so has at least $|U|(|U| - m)/(2m)$ colliding pairs, by convexity, and averaging over all pairs gives a lower bound of $(|U| - m)/(m(|U| - 1))$. The page [universal hashing lemma](/universal-hashing-lemma/) gives this bound, due to Stinson, and the statement for $\varepsilon$-universal families.
- **Only expectations.** The theorem does not bound $L(x)$ with high probability. For the 40 keys $13, 26, \ldots, 520$ and the dot-product family modulo 13, the mean number of colliding pairs is 60, but 13 of the 2197 functions put all keys in one chain. See [dot-product hashing](/dot-product-hashing/).
- **Keys chosen after h.** If an adversary sees $h$, or sees enough timings to learn it, and then chooses the keys, the bound fails: the keys may all share a slot. The theorem needs $S$ and the sequence of operations to be fixed independently of $h$.

## History

Carter and Wegman introduced universal classes of hash functions in a paper at STOC 1977, with the journal version in 1979. Their point was that the expected cost of hashing with chaining can be proved for every input, with the probability taken over the choice of the hash function, instead of assuming that the keys are random. They proved the bound for any fixed sequence of requests. Wegman and Carter defined strongly universal classes in 1981. Fredman, Komlós and Szemerédi used the collision count of part 3 for their static perfect hashing scheme in 1984, and the theorem is now the standard analysis of chained hashing in textbooks such as Cormen, Leiserson, Rivest and Stein.

## References
