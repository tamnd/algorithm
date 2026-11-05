---
tag: ZRBVWF
kind: theorem
slug: chaining-expected-search-time
name: Expected search time with chaining
area: searching/hashing-search
level: core
summary: Under simple uniform hashing, expected search time is Theta(1+alpha).
model: word-ram
prereqs: [separate-chaining, simple-uniform-hashing, load-factor, binomial-distribution, linearity-of-expectation]
see_also: [chaining-analysis, universal-hashing-lemma, open-addressing-expected-probes, balls-into-bins-max-load, hash-table, chernoff-bound, variance, uniform-hashing-assumption]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (the theorems on unsuccessful and successful search in hashing with chaining, and the corollary that searching takes constant time on average when n = O(m))
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of separate chaining under random hash values
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5 (Balls, bins and random graphs), the maximum load and its use for chain hashing
---

The expected search time with chaining is the statement that, in a [hash table](/hash-table/) with [separate chaining](/separate-chaining/), $m$ slots and $n$ keys, a search takes $\Theta(1 + \alpha)$ expected time under [simple uniform hashing](/simple-uniform-hashing/), where $\alpha = n/m$ is the [load factor](/load-factor/). It holds for searches that fail and for searches that succeed, so a table that keeps $n = O(m)$ searches in $O(1)$ expected time. The exact means are derived on the [analysis of separate chaining](/chaining-analysis/) page; this page proves the two-sided time bound from the [binomial](/binomial-distribution/) law of a chain, and adds its variance, its tail and the effect of the order in which chains are kept.

## Statement

Let a chained hash table have $m \ge 1$ slots and hold $n \ge 1$ distinct keys $x_1, \ldots, x_n$, inserted in this order. Assume simple uniform hashing: the slots $h(x_1), \ldots, h(x_n)$ and the slot $h(k)$ of a searched key $k$ that is not stored are independent and uniform on $\{0, \ldots, m - 1\}$. A search computes $h(k)$ in time $\Theta(1)$ and then compares $k$ with the keys of its chain, one at a time, in time $\Theta(1)$ each. Let $L$ be the number of keys that an unsuccessful search for $k$ examines, and $S$ the number that a successful search for a key chosen uniformly from $x_1, \ldots, x_n$, independently of $h$, examines.

**Theorem.**

1. **(Distribution.)** $L$ is binomial with parameters $n$ and $1/m$. So $\mathrm{E}[L] = \alpha$ and $\mathrm{Var}[L] = \alpha (1 - 1/m)$.
2. **(Tail.)** For each integer $t \ge 1$, $\Pr[L \ge t] \le \binom{n}{t} m^{-t} \le (e \alpha / t)^t$.
3. **(Successful search.)** Whether each insert puts the new key at the head or at the tail of its chain, $\mathrm{E}[S] = 1 + (n - 1)/(2m)$.
4. **(Time.)** The expected time of an unsuccessful search and of a successful search are both $\Theta(1 + \alpha)$: there are constants $0 < c_1 \le c_2$, independent of $n$ and $m$, with $c_1 (1 + \alpha) \le \mathrm{E}[\text{time}] \le c_2 (1 + \alpha)$.
5. **(Sorted chains.)** If each chain is kept in increasing order and an unsuccessful search stops at the first key larger than $k$, and the rank of $k$ among the keys of its chain is uniform, then the expected number of keys examined is
$$\frac{\alpha}{2} + 1 - \frac{m}{n + 1} \left( 1 - \left( 1 - \frac{1}{m} \right)^{n + 1} \right).$$

## In plain words

Picture the slots as boxes and the keys as balls thrown at random into them. A search for a missing key goes to one box and looks at every ball in it. On average a box holds the number of balls divided by the number of boxes, and that is the cost. A search for a key that is there stops when it finds it, so on average it looks at about half of the other balls in the box plus the one it wants.

The cost is also unlikely to be much more than the average. For a box to hold ten balls when the average is one, ten particular throws must all land in the same box, which almost never happens. Keeping each box sorted lets a failed search stop early, which saves about half of the work.

## Proof

**Part 1.** For $i = 1, \ldots, n$, let $X_i$ be 1 if $h(x_i) = h(k)$ and 0 otherwise. Fix the slot $s = h(k)$. Given $s$, the $X_i$ are independent, since the $h(x_i)$ are, and $\Pr[X_i = 1 \mid h(k) = s] = 1/m$. So given $s$, $L = \sum_i X_i$ is binomial with parameters $n$ and $1/m$. This law does not depend on $s$, so it is also the law of $L$. A binomial variable with parameters $n$ and $p$ has mean $np$ and [variance](/variance/) $np(1 - p)$, which gives $\mathrm{E}[L] = n/m = \alpha$ and $\mathrm{Var}[L] = \alpha(1 - 1/m)$.

**Part 2.** If $L \ge t$, then some set $T$ of $t$ stored keys has $h(x) = h(k)$ for all $x \in T$. For a fixed $T$, this event has probability $m^{-t}$ by independence. A union bound over the $\binom{n}{t}$ sets gives $\Pr[L \ge t] \le \binom{n}{t} m^{-t}$. With $\binom{n}{t} \le n^t / t! \le (en/t)^t$, which uses $t! \ge (t/e)^t$, the bound is at most $(en/(tm))^t = (e\alpha/t)^t$.

**Part 3.** *Head insertion.* The chain of $x_i$ holds, before $x_i$, the keys of its slot that were inserted after it. So a search for $x_i$ examines $1 + \sum_{j > i} Y_{ij}$ keys, where $Y_{ij} = 1$ if $h(x_j) = h(x_i)$. For $i \ne j$, $\Pr[Y_{ij} = 1] = 1/m$ by independence and uniformity. By [linearity of expectation](/linearity-of-expectation/), the expected cost for $x_i$ is $1 + (n - i)/m$, and the average over $i$ is
$$1 + \frac{1}{nm} \sum_{i=1}^{n} (n - i) = 1 + \frac{1}{nm} \cdot \frac{n(n-1)}{2} = 1 + \frac{n - 1}{2m}.$$
*Tail insertion.* Now the keys before $x_i$ in its chain are those of its slot inserted before it, the cost for $x_i$ is $1 + \sum_{j < i} Y_{ij}$ with mean $1 + (i - 1)/m$, and the average over $i$ is again $1 + (n-1)/(2m)$.

**Part 4.** The time of an unsuccessful search is $\Theta(1)$ for the hash plus $\Theta(1)$ per examined key, so it lies between $a(1 + L)$ and $b(1 + L)$ for constants $0 < a \le b$. Taking expectations and using Part 1, it lies between $a(1 + \alpha)$ and $b(1 + \alpha)$. For a successful search, by Part 3, $\mathrm{E}[S] = 1 + (n-1)/(2m)$. Since $n \ge 1$, $(n - 1)/(2m) \le \alpha/2$, so $\mathrm{E}[S] \le 1 + \alpha$. For the lower bound, if $n = 1$ then $\alpha \le 1$ and $\mathrm{E}[S] = 1 \ge (1 + \alpha)/2$; if $n \ge 2$ then $n - 1 \ge n/2$, so $\mathrm{E}[S] \ge 1 + \alpha/4 \ge (1 + \alpha)/4$. With the same constants $a$ and $b$ for the time per step, the expected time of a successful search lies between $a(1 + \alpha)/4$ and $2b(1 + \alpha)$. So $c_1 = a/4$ and $c_2 = 2b$ work for both kinds of search.

**Part 5.** Condition on $L = \ell$. The chain holds $\ell$ keys in increasing order, and by assumption the number $r$ of them that are smaller than $k$ is uniform on $\{0, 1, \ldots, \ell\}$. The search examines the $r$ smaller keys and then, if $r < \ell$, one larger key where it stops. So it examines $r + [r < \ell]$ keys, with conditional mean
$$\frac{\ell}{2} + \frac{\ell}{\ell + 1} = \frac{\ell}{2} + 1 - \frac{1}{\ell + 1}.$$
By Part 1, $\mathrm{E}[L/2] = \alpha/2$. For a binomial variable $L$ with parameters $n$ and $p = 1/m$,
$$\mathrm{E}\left[\frac{1}{L + 1}\right] = \sum_{\ell=0}^{n} \frac{1}{\ell + 1} \binom{n}{\ell} p^\ell (1-p)^{n-\ell} = \frac{1}{(n+1)p} \sum_{\ell=0}^{n} \binom{n + 1}{\ell + 1} p^{\ell + 1} (1 - p)^{n - \ell} = \frac{1 - (1 - p)^{n + 1}}{(n + 1) p},$$
using $\frac{1}{\ell + 1}\binom{n}{\ell} = \frac{1}{n+1}\binom{n+1}{\ell+1}$ and the binomial theorem without its $\ell + 1 = 0$ term. With $p = 1/m$ this gives the formula of the statement. $\blacksquare$

## Consequences

**Constant time at bounded load.** If the table keeps $n \le c\,m$ for a constant $c$, by [rehashing](/rehashing/) into a larger array when the load passes $c$, then both kinds of search take $O(1)$ expected time. This is the usual guarantee of a hash table, and it holds for insertion and deletion as well, since both start with a search of the chain.

**The numbers.** For $m = 1000$ slots:

| $n$ | $\alpha$ | $\mathrm{E}[L]$ | standard deviation of $L$ | $\mathrm{E}[S]$ | sorted chains, unsuccessful |
|---|---|---|---|---|---|
| 500 | 0.5 | 0.5 | 0.707 | 1.2495 | 0.4631 |
| 1000 | 1 | 1 | 0.999 | 1.4995 | 0.8680 |
| 2000 | 2 | 2 | 1.414 | 1.9995 | 1.5677 |
| 5000 | 5 | 5 | 2.235 | 3.4995 | 3.3014 |

The standard deviation is $\sqrt{\alpha}$ up to a factor $1 - 1/m$, so at load 1 a typical unsuccessful search examines 0, 1 or 2 keys. Sorted chains save little at low load and approach a saving of $\alpha/2$ at high load, at the price of an ordered insert.

**Concentration.** At $\alpha = 1$ and $n = m = 1000$, the union bound of Part 2 gives $\Pr[L \ge 6] \le \binom{1000}{6} 1000^{-6} \approx 1.37 \cdot 10^{-3}$, against the exact binomial value of about $5.9 \cdot 10^{-4}$, and $\Pr[L \ge 10] \le 2.6 \cdot 10^{-7}$. The simpler form $(e/t)^t$ gives $8.7 \cdot 10^{-3}$ and $2.2 \cdot 10^{-6}$. A [Chernoff bound](/chernoff-bound/) gives tails of the same shape for the sum of independent indicators.

**Choice of the table size.** The cost depends on $n$ and $m$ only through $\alpha$, and the space is $\Theta(n + m)$. So a table with $m = \Theta(n)$ gets both $O(1)$ expected search and $O(n)$ space, and a larger $m$ buys only a constant factor.

**Weaker hash families.** Parts 1 and 3 use only that two distinct keys collide with probability $1/m$. So the expected values, and hence Part 4, hold for any hash family in which distinct keys collide with probability at most $1/m$, with the inequality in place of the equality; this is the [universal hashing lemma](/universal-hashing-lemma/). The variance and the tail of Parts 1 and 2 use independence of more keys: the variance needs 3-wise independence of the slots of $k$ and two stored keys, and the bound for $t$ keys needs $(t + 1)$-wise independence; see [k-wise independent hashing](/k-wise-independent-hashing/).

## Tightness

**The bound is two-sided.** Part 4 is a $\Theta$ bound, not only an upper bound: an unsuccessful search examines $\alpha$ keys on average, so no chained table under the model searches in $o(\alpha)$ expected time, and every search pays the hash.

**Expected cost against the worst search.** The theorem bounds the cost of one search for a key chosen without knowledge of $h$. The largest chain is longer. At $n = m$, the longest chain has $\Theta(\log n / \log \log n)$ keys with high probability, by the [balls into bins](/balls-into-bins-max-load/) bound. So the worst search over all stored keys is slower than the average by this factor, and an adversary who sees the table can always search the longest chain.

**Without the model.** For a fixed hash function there is an input that puts all $n$ keys in one chain, as soon as the universe has at least $(n-1)m + 1$ keys, and then searches take $\Theta(n)$ time. So the assumption, or a random choice of the hash function, is necessary for any bound in terms of $\alpha$ alone.

**Sharpness of the tail.** The bound of Part 2 exceeds the exact tail by at most a factor that tends to $e^{\alpha}$ when $t$ is fixed and $n$ and $m$ grow at fixed $\alpha$, since then $\binom{n}{t} m^{-t} \to \alpha^t / t!$ while $\Pr[L = t] \to e^{-\alpha} \alpha^t / t!$, the [Poisson](/poisson-distribution/) limit.

## History

The analysis of chaining under random hash values goes back to the first studies of hashing in the 1950s and 1960s, and Knuth gives it with exact formulas in Section 6.4. CLRS states the two theorems for unsuccessful and successful search in Section 11.2 and draws the corollary that search takes $O(1)$ average time when $n = O(m)$. The study of the longest chain as the maximum load of balls into bins, and its $\Theta(\log n / \log \log n)$ order, is standard in the probabilistic analysis of algorithms, as in Chapter 5 of Mitzenmacher and Upfal.

## References
