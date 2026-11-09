---
tag: ZCRDJ3
kind: problem
slug: counting-set-partitions
name: Counting set partitions
aliases:
- Bell number computation
- computing Bell numbers
- counting equivalence relations
area: combinatorics/counting-algorithms
level: core
summary: Computing the number of partitions of a finite set.
prereqs: [bell-numbers, stirling-numbers-second-kind]
see_also: [bell-numbers, set-partitions, set-partition-generation, restricted-growth-string, equivalence-relation, linear-recurrence-nth-term, exponential-generating-functions, clustering-problem]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.5, Generating all set partitions (Bell numbers, Peirce's triangle, and the exercises on congruences)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.9, The twelvefold way
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Section II.3, Surjections, set partitions, and words
---

Counting set partitions asks for the number $B_n$ of ways to split an $n$-element set into nonempty unordered blocks, or for the number $S(n, k)$ with exactly $k$ blocks. The answer grows like $(n / \ln n)^n$, so listing the partitions is hopeless beyond $n \approx 15$, but the count itself has an exact $O(n^2)$-step recurrence. Modulo a small prime $p$, Touchard's congruence makes $B_n \bmod p$ computable for $n$ as large as $10^{18}$.

## In plain words

You have a group of different people and want to know in how many ways they can split into teams. The number of teams is free, every team has at least one member, and teams have no names or order. For 3 people there are 5 ways, for 10 people there are 115975. The task is to compute this number fast and exactly for large groups, or to compute its remainder after division by a fixed prime when the exact number is too long to store.

## Definition

**Notation.** $n \ge 0$, $[n] = \{1, \ldots, n\}$, $k$ is the number of blocks, $C(n, k)$ is a binomial coefficient, $S(n, k)$ is a [Stirling number of the second kind](/stirling-numbers-second-kind/) and $B_n = \sum_k S(n, k)$ is the [Bell number](/bell-numbers/).

**Input:** an integer $n \ge 0$, and in some variants also $k$ or a prime $p$.

**Output:** the number $B_n$ of set partitions of $[n]$, as an exact integer, or $B_n \bmod p$.

A set partition of $[n]$ is the same thing as an [equivalence relation](/equivalence-relation/) on $[n]$, and the same thing as a [restricted growth string](/restricted-growth-string/) $a_1 \cdots a_n$ with $a_1 = 0$ and $a_{i+1} \le 1 + \max(a_1, \ldots, a_i)$. So the problem also counts equivalence relations and restricted growth strings.

## Variants

- **Fixed number of blocks.** Compute $S(n, k)$, or the whole row $S(n, 0), \ldots, S(n, n)$.
- **Prefix of the sequence.** Compute $B_0, \ldots, B_n$ together.
- **Modular.** Compute $B_n \bmod p$ or $S(n, k) \bmod p$ for a prime $p$, where $n$ may be far larger than $p$.
- **Restricted block sizes.** Count the partitions whose block sizes lie in a set $A$. The [exponential generating function](/exponential-generating-functions/) is $\exp\bigl(\sum_{s \in A} z^s / s!\bigr)$. With $A = \{2, 3, \ldots\}$ (no singletons) the counts are $1, 0, 1, 1, 4, 11, 41, 162, 715, 3425$ for $n = 0$ to $9$ (OEIS A000296), and by inclusion-exclusion over the set of singletons they equal $\sum_j (-1)^j C(n, j)\, B_{n-j}$.
- **Ordered blocks.** Count the ordered set partitions, $\sum_k k!\, S(n, k)$: the Fubini numbers.
- **Noncrossing partitions.** If the elements sit on a circle and blocks may not cross, the count is the [Catalan number](/catalan-numbers/) $C_n$.

## Examples

**Example 1.** For $n = 3$ the five partitions are $1|2|3$, $12|3$, $13|2$, $1|23$ and $123$, so $B_3 = 5$. Their restricted growth strings are $012$, $001$, $010$, $011$ and $000$.

**Example 2.** The number of ways to group 10 data points into clusters, with any number of clusters, is $B_{10} = 115975$. This is why exhaustive search over all clusterings of a [clustering problem](/clustering-problem/) fails beyond a handful of points.

**Example 3.** $B_{50} = 185724268771078270438257767181908917499221852770$, a number with 48 digits, and $B_{100}$ has 116 digits (385 bits).

**Example 4: parity.** Touchard's congruence for $p = 2$ is $B_{n+2} \equiv B_n + B_{n+1} \pmod 2$. With $B_0 = B_1 = 1$ the residues run $1, 1, 0, 1, 1, 0, \ldots$, so $B_n$ is even exactly when $n \equiv 2 \pmod 3$.

## Known algorithms

**Brute force.** List all partitions as restricted growth strings by [set partition generation](/set-partition-generation/) and count them. This takes $\Theta(B_n)$ steps at least, which is useless for counting but serves as a test oracle for small $n$.

**The Bell triangle.** Start with the row $(1)$. Each new row starts with the last entry of the old row, and each next entry is the sum of its left neighbour and the entry above that neighbour. The first entry of row $n$ is $B_n$ (the proof is on the [Bell numbers](/bell-numbers/) page). This uses $n(n+1)/2$ additions and no multiplications, and it keeps only one row of $O(n)$ numbers. In exact arithmetic the numbers have $O(n \log n)$ bits, so the bit cost is $O(n^3 \log n)$ and the memory is $O(n^2 \log n)$ bits. It yields the whole prefix $B_0, \ldots, B_n$.

**The binomial recurrence.** $B_{m+1} = \sum_{j=0}^{m} C(m, j)\, B_j$ also gives the prefix with $O(n^2)$ multiplications. It has the same order of cost as the triangle but multiplies large numbers, so the triangle is usually faster.

**The Stirling table.** The recurrence $S(m, j) = j\, S(m-1, j) + S(m-1, j-1)$ fills the triangle in $O(n^2)$ operations and gives every $S(n, k)$ and, by row sums, every $B_m$. Use it when the variant asks for the number of blocks.

**Power series.** Modulo a prime $p > n$ that suits the [number-theoretic transform](/number-theoretic-transform/), each $B_m$ with $m \le n$ is $m!$ times the coefficient of $z^m$ in $\exp(e^z - 1)$. The exponential of a power series can be computed by Newton iteration in $O(n \log n)$ operations, in the same way as [power series inversion](/power-series-inversion/). Of the methods on this page, it is the fastest for a long prefix modulo a prime.

**Touchard's congruence for a small prime.** For a prime $p$ and every $n \ge 0$,

$$B_{n+p} \equiv B_n + B_{n+1} \pmod p.$$

*Proof.* Let the cyclic group of order $p$ act on the partitions of $[n] \cup \mathbb{Z}_p$ by rotating the elements of $\mathbb{Z}_p$ and fixing the elements of $[n]$. Each orbit has size 1 or $p$, so $B_{n+p}$ is congruent mod $p$ to the number of fixed partitions. In a fixed partition, a block that contains an element of $[n]$ is mapped to itself, so it contains none or all of $\mathbb{Z}_p$. The blocks inside $\mathbb{Z}_p$ form a rotation-invariant partition of $\mathbb{Z}_p$, and since $p$ is prime this is either one block or $p$ singletons. If all of $\mathbb{Z}_p$ is in one block, contract it to one new element: this gives the $B_{n+1}$ partitions of an $(n+1)$-set. Otherwise every element of $\mathbb{Z}_p$ is a singleton, and the rest is any of the $B_n$ partitions of $[n]$. $\square$

So modulo $p$ the sequence satisfies a linear recurrence with characteristic polynomial $x^p - x - 1$. Compute $B_0, \ldots, B_{p-1} \bmod p$ with the triangle in $O(p^2)$ operations, then compute $x^n \bmod (x^p - x - 1)$ over $\mathbb{F}_p$ by repeated squaring and combine its coefficients with $B_0, \ldots, B_{p-1}$, as for any [linear recurrence](/linear-recurrence-nth-term/). With schoolbook polynomial multiplication this costs $O(p^2 \log n)$ operations, which handles $p = 7$ and $n = 10^{18}$ instantly.

**Dobinski's formula.** $B_n = e^{-1} \sum_{m \ge 0} m^n / m!$ gives floating-point approximations, and the sum can be cut after about $2n$ terms for a good relative error. It is not a practical way to get exact values, because the precision must grow with the length of $B_n$.

## Bounds

- **Output size.** $\log_2 B_n = n \log_2 n - n \log_2 \ln n + O(n)$, so any exact algorithm must write $\Theta(n \log n)$ bits. No algorithm for the exact value can run in less time than that.
- **Elementary bounds.** $2^{n-1} \le B_n \le n!$ for $n \ge 1$, which shows $B_n$ is above any polynomial and below $n!$.
- **Prefix output.** The prefix $B_0, \ldots, B_n$ has $\Theta(n^2 \log n)$ bits in total, while the triangle uses $O(n^3 \log n)$ bit operations, a factor $n$ above the output size.

## Reductions

- $B_n = \sum_k S(n, k)$, so any algorithm for a row of [Stirling numbers of the second kind](/stirling-numbers-second-kind/) gives $B_n$ with $n$ more additions.
- $B_n$ equals the number of equivalence relations on $[n]$, the number of restricted growth strings of length $n$, and the number of words of length $n$ up to renaming of the letters.
- $B_n$ is the number of ways to write a product of $n$ distinct primes as an unordered product of factors greater than 1, since such a factorization is a partition of the set of primes.
- $B_n$ is the $n$th moment $\mathbb{E}[X^n]$ of a Poisson random variable $X$ with mean 1, by Dobinski's formula.

## Applications

- **Clustering and grouping.** $B_n$ is the size of the search space of a clustering of $n$ items when the number of clusters is free, as in [correlation clustering](/correlation-clustering/).
- **Testing string algorithms.** A string algorithm that depends only on which positions hold equal letters needs to be tested on one string per restricted growth string, that is, on $B_n$ strings of length $n$ instead of $\sigma^n$.
- **Rhyme schemes and equality patterns.** The rhyme schemes of an $n$-line poem and the equality patterns of $n$ variables are counted by $B_n$.
- **Moments.** Moments of Poisson variables and of the number of occupied boxes in balls-into-boxes models reduce to Bell and Stirling numbers.

## References
