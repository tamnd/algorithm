---
tag: TQMTWW
kind: definition
slug: eulerian-numbers
name: Eulerian numbers
aliases:
- Eulerian numbers of permutations
- Eulerian numbers of the first kind
- Euler's triangle
area: combinatorics/counting-algorithms
level: advanced
summary: Number of permutations of n elements with k descents.
prereqs: [descents, permutation]
see_also: [descents, natural-merge-sort, stirling-numbers-first-kind, stirling-numbers-second-kind, insertion-sort, exponential-generating-functions, binomial-coefficient]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.2, Eulerian Numbers (the recurrence, Worpitzky's identity and the explicit formula)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.4, Descents (the Eulerian polynomials)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 5.1.3, Runs (Eulerian numbers and the distribution of runs)
---

The Eulerian number $A(n, k)$, also written $\langle {n \atop k} \rangle$, is the number of permutations of $n$ elements that have exactly $k$ descents. A permutation with $k$ descents splits into $k + 1$ ascending runs, so the Eulerian numbers give the exact distribution of the number of runs that a [natural merge sort](/natural-merge-sort/) finds in random input. Row $n$ of the triangle is symmetric and sums to $n!$. Worpitzky's identity links the numbers to powers and [binomial coefficients](/binomial-coefficient/).

## Definition

**Notation.** $n \ge 0$ is the number of elements and $[n] = \{1, \ldots, n\}$. For a permutation $\sigma = \sigma_1 \sigma_2 \cdots \sigma_n$ of $[n]$ in one-line notation, a [descent](/descents/) is a position $i$ with $1 \le i < n$ and $\sigma_i > \sigma_{i+1}$. $\operatorname{des}(\sigma)$ is the number of descents. $C(n, k)$ is a binomial coefficient.

For integers $n, k \ge 0$,

$$A(n, k) = \bigl|\{\sigma \text{ a permutation of } [n] : \operatorname{des}(\sigma) = k\}\bigr|.$$

The empty permutation has no descents, so $A(0, 0) = 1$. For $n \ge 1$, $A(n, k) \ne 0$ exactly when $0 \le k \le n - 1$. Some books index by $k + 1$, the number of ascending runs, instead of $k$: OEIS A008292 uses that shift. The Eulerian polynomial is $A_n(t) = \sum_k A(n, k)\, t^k$.

**Recurrence.** For $n \ge 1$,

$$A(n, k) = (k + 1)\, A(n-1, k) + (n - k)\, A(n-1, k-1).$$

*Proof.* Each permutation of $[n]$ comes from exactly one permutation $\tau$ of $[n-1]$ by putting $n$ into one of the $n$ gaps of $\tau$ (before the first entry, between two entries, or after the last). Say $\tau$ has $j$ descents. If $n$ goes into a descent gap $a > b$, the descent $a > b$ becomes the descent $n > b$, and $a < n$ is an ascent, so the count stays $j$. If $n$ goes at the end, the count also stays $j$. In the other $n - 1 - j$ gaps (an ascent gap or the front), the new pair $n > b$ is a new descent, so the count becomes $j + 1$. A permutation of $[n]$ with $k$ descents therefore comes from $\tau$ with $j = k$ in $k + 1$ ways, or from $\tau$ with $j = k - 1$ in $n - 1 - (k - 1) = n - k$ ways. $\square$

**Symmetry.** $A(n, k) = A(n, n - 1 - k)$ for $n \ge 1$. *Proof.* The map $\sigma_i \mapsto n + 1 - \sigma_i$ turns each descent into an ascent and each ascent into a descent, and it is a bijection. $\square$

**Worpitzky's identity.** For $n \ge 1$ and every $x$,

$$x^n = \sum_{k=0}^{n-1} A(n, k)\, C(x + k, n).$$

*Proof.* Both sides are polynomials in $x$ of degree $n$, so it is enough to prove it for every positive integer $x$. The left side counts the words $f = f(1) \cdots f(n)$ with letters in $[x]$. For each word, sort the positions stably: let $\sigma$ be the permutation with $f(\sigma_1) \le \cdots \le f(\sigma_n)$ that puts equal letters in increasing order of position. Then $f(\sigma_i) < f(\sigma_{i+1})$ at every descent $i$ of $\sigma$. Conversely, for a fixed $\sigma$ with $d$ descents, the words that give $\sigma$ are the sequences $1 \le a_1 \le \cdots \le a_n \le x$ with a strict step at the $d$ descents. Subtract from $a_i$ the number of descents before position $i$. This is a bijection onto the weakly increasing sequences with values in $[x - d]$, and there are $C(x - d + n - 1, n)$ of them. So $x^n = \sum_d A(n, d)\, C(x + n - 1 - d, n)$, and symmetry with $k = n - 1 - d$ gives the identity. $\square$

**Generating function and explicit formula.** For $n \ge 1$,

$$\sum_{m \ge 0} (m + 1)^n t^m = \frac{A_n(t)}{(1 - t)^{n+1}}, \qquad A(n, k) = \sum_{j=0}^{k} (-1)^j\, C(n + 1, j)\, (k + 1 - j)^n.$$

*Proof.* The proof above, read before the symmetry step at $x = m + 1$, gives $(m + 1)^n = \sum_k A(n, k)\, C(m - k + n, n)$. Since $\sum_{m \ge k} C(m - k + n, n)\, t^m = t^k / (1 - t)^{n+1}$, the first identity follows. Multiply both sides by $(1 - t)^{n+1} = \sum_j (-1)^j C(n + 1, j)\, t^j$ and compare the coefficients of $t^k$ to get the second. $\square$

**Mean and variance.** For $n \ge 2$, a uniformly random permutation of $[n]$ has $(n - 1)/2$ descents on average, with variance $(n + 1)/12$. The mean is direct: each of the $n - 1$ positions is a descent with probability $1/2$. The variance comes from the fact that two neighbouring positions are both descents with probability $1/6$, and two positions with a gap between them are independent (Knuth, Section 5.1.3).

### Computing the numbers

- **The table.** The recurrence fills all $A(m, k)$ for $m \le n$ with $O(n^2)$ additions and multiplications by small integers. The entries are exact integers below $n!$, so they have $O(n \log n)$ bits, and the bit cost of the table is $O(n^3 \log n)$.
- **One entry.** The explicit formula has $k + 1$ terms. Modulo a prime $p$, each power costs $O(\log n)$ by [binary exponentiation](/binary-exponentiation/), so one entry costs $O(k \log n)$. In exact arithmetic the terms are much larger than the result and cancel, so the table is often the better choice.

## Examples and non-examples

**Example 1.** For $n = 3$ the permutations sort by descents as $123$ (no descent), $132$, $213$, $231$, $312$ (one descent each) and $321$ (two descents). So row 3 is $1, 4, 1$. The recurrence gives $A(3, 1) = 2\, A(2, 1) + 2\, A(2, 0) = 2 + 2 = 4$.

**Example 2.** The triangle for $n = 1$ to $8$ (OEIS A008292).

| n \ k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | | | | | | | |
| 2 | 1 | 1 | | | | | | |
| 3 | 1 | 4 | 1 | | | | | |
| 4 | 1 | 11 | 11 | 1 | | | | |
| 5 | 1 | 26 | 66 | 26 | 1 | | | |
| 6 | 1 | 57 | 302 | 302 | 57 | 1 | | |
| 7 | 1 | 120 | 1191 | 2416 | 1191 | 120 | 1 | |
| 8 | 1 | 247 | 4293 | 15619 | 15619 | 4293 | 247 | 1 |

**Example 3: one descent.** $A(n, 1) = 2^n - n - 1$, giving $0, 1, 4, 11, 26, 57, 120, 247, 502$ for $n = 1$ to $9$ (OEIS A000295). A permutation with at most one descent is fixed by the set $S$ of entries in its first run, since both runs are increasing. Every subset $S$ gives such a permutation, and it has no descent exactly when $S = \{1, \ldots, j\}$ for some $0 \le j \le n$. So $2^n - (n + 1)$ subsets give one descent.

**Example 4: Worpitzky at $n = 3$.** $x^3 = C(x, 3) + 4\, C(x + 1, 3) + C(x + 2, 3)$. At $x = 2$ this is $0 + 4 + 4 = 8$.

**Example 5: runs in sorting.** A natural merge sort on $n = 4$ distinct keys in random order finds $k + 1$ runs with probability $A(4, k)/24$, so it finds 1, 2, 3 or 4 runs with probabilities $1/24$, $11/24$, $11/24$, $1/24$. The mean number of runs is $(n + 1)/2$.

**Non-example 1: cycles.** The number of permutations of $[n]$ with $k$ cycles is a [Stirling number of the first kind](/stirling-numbers-first-kind/), not an Eulerian number. Both rows sum to $n!$, but for $n = 3$ the cycle row is $2, 3, 1$ and the Eulerian row is $1, 4, 1$.

**Non-example 2: Euler numbers.** The Euler (up/down) numbers $1, 1, 1, 2, 5, 16, 61, 272$ (OEIS A000111) count alternating permutations. They are a different sequence with a similar name.

**Non-example 3: the second kind.** The second-order Eulerian numbers, with rows $1$; $1, 2$; $1, 8, 6$; $1, 22, 58, 24$ (OEIS A008517), count descents of Stirling permutations of the multiset $\{1, 1, 2, 2, \ldots, n, n\}$, not of permutations of $[n]$. Their recurrence has the factor $2n - 1 - k$ in place of $n - k$.

## Related definitions

- [Descents](/descents/) are the statistic that the Eulerian numbers count.
- [Natural merge sort](/natural-merge-sort/) and [insertion sort](/insertion-sort/) are sorting methods whose cost depends on runs and descents.
- [Stirling numbers of the second kind](/stirling-numbers-second-kind/) expand $x^n$ in falling factorials, as Worpitzky's identity expands it in the binomials $C(x + k, n)$.
- [Stirling numbers of the first kind](/stirling-numbers-first-kind/) count permutations by cycles.
- [Binomial coefficients](/binomial-coefficient/) appear in Worpitzky's identity and in the explicit formula.

## References
