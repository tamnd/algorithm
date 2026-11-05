---
tag: JDY5CY
kind: definition
slug: descents
name: Descents of a permutation
aliases:
- descent set
area: sequences/inversions-and-permutations
level: core
summary: Positions i where a[i] > a[i+1].
prereqs: [permutation, inversion]
see_also: [eulerian-numbers, mahonian-numbers, lehmer-code, natural-merge-sort, presortedness, permutation-inverse, inversion, adaptive-sorting]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.4 (descents, the descent set, the major index and the Eulerian numbers)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.3 (runs, ascents and descents, and the Eulerian numbers)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 6.2 (Eulerian numbers, their recurrence and Worpitzky's identity)
---

A descent of a sequence $a_1 a_2 \cdots a_n$ is a position $i$ with $a_i > a_{i+1}$, an adjacent pair that is out of order. The descent set $D(a)$ collects these positions, the number of descents $\operatorname{des}(a)$ is one less than the number of maximal ascending runs, and the sum of the descents is the major index $\operatorname{maj}(a)$. Every descent is an [inversion](/inversion/) between neighbors, so descents are the local view of disorder that [natural merge sort](/natural-merge-sort/) uses. The number of permutations of $[n]$ with $k$ descents is the [Eulerian number](/eulerian-numbers/) $A(n, k)$, and the major index has the same distribution as the number of inversions.

## Definition

**Descents.** For a sequence $a = (a_1, \ldots, a_n)$ from a [total order](/total-order/), a *descent* is an index $i \in [n-1]$ with $a_i > a_{i+1}$, and an *ascent* is an index with $a_i < a_{i+1}$. The *descent set* is
$$D(a) = \{\, i \in [n-1] : a_i > a_{i+1} \,\},$$
and $\operatorname{des}(a) = |D(a)|$.

**Runs.** Cutting $a$ after every descent splits it into maximal ascending runs, each increasing. There are $\operatorname{des}(a) + 1$ of them for $n \ge 1$.

**Major index.** $\operatorname{maj}(a) = \sum_{i \in D(a)} i$, named after Major Percy MacMahon.

**Inverse descents.** For a [permutation](/permutation/) $\pi$, $i$ is a descent of $\pi^{-1}$ exactly when the value $i + 1$ appears before the value $i$ in $\pi$. These are the descents of the [inverse](/permutation-inverse/), and they differ from the descents of $\pi$ in general.

**Facts.**

- **Counting by descent set.** For $S = \{s_1 < \cdots < s_k\} \subseteq [n-1]$, the permutations of $[n]$ with $D(\pi) \subseteq S$ are those that increase on each of the blocks $[1, s_1], [s_1 + 1, s_2], \ldots, [s_k + 1, n]$. Choosing which values go into each block determines them, so there are $\binom{n}{s_1,\ s_2 - s_1,\ \ldots,\ n - s_k}$ of them. The number with $D(\pi) = S$ exactly follows by inclusion and exclusion over the subsets of $S$.
- **Eulerian numbers.** $A(n, k) = |\{\pi \in S_n : \operatorname{des}(\pi) = k\}|$ satisfies $A(n, k) = (k + 1)A(n-1, k) + (n - k)A(n-1, k-1)$, by inserting the value $n$ into a permutation of $[n-1]$: placed at the end or inside a descent it keeps the number of descents, and placed at the front or inside an ascent it adds one. It is symmetric, $A(n, k) = A(n, n - 1 - k)$, through the reversal of the sequence. See [Eulerian numbers](/eulerian-numbers/).
- **Mean and variance.** Each adjacent pair is a descent with probability $1/2$ in a uniform random permutation, so $\mathbb{E}[\operatorname{des}] = (n - 1)/2$. The variance is $(n + 1)/12$ for $n \ge 2$.
- **Major index and inversions.** MacMahon proved that $\operatorname{maj}$ and $\operatorname{inv}$ have the same distribution on $S_n$: both have the generating function $\prod_{k=1}^{n}(1 + z + \cdots + z^{k-1})$, whose coefficients are the [Mahonian numbers](/mahonian-numbers/). Foata gave a bijection $\phi$ of $S_n$ with $\operatorname{maj}(\pi) = \operatorname{inv}(\phi(\pi))$, and the joint distribution of the pair $(\operatorname{inv}, \operatorname{maj})$ is symmetric.
- **In the Lehmer code.** $i$ is a descent of $\pi$ exactly when $c_i > c_{i+1}$ in the [Lehmer code](/lehmer-code/) $c$.
- **Worpitzky's identity.** $x^n = \sum_{k} A(n, k) \binom{x + k}{n}$ for every integer $x \ge 0$. For $n = 3$ and $x = 2$: $8 = 1 \cdot \binom 23 + 4 \cdot \binom 33 + 1 \cdot \binom 43$.
- **Computing.** One pass over the sequence finds $D(a)$, $\operatorname{des}(a)$ and $\operatorname{maj}(a)$ in $\Theta(n)$ time, compared with $O(n \log n)$ for the inversion count.

## Examples and non-examples

**One permutation.** $\pi = 3\,1\,4\,5\,2$ has $D(\pi) = \{1, 4\}$, since $3 > 1$ and $5 > 2$. So $\operatorname{des}(\pi) = 2$, its runs are $3 \mid 1\,4\,5 \mid 2$, and $\operatorname{maj}(\pi) = 1 + 4 = 5$. It has 4 inversions, two of which are descents.

**More.** $3\,1\,6\,2\,5\,4$ has $D = \{1, 3, 5\}$ and $\operatorname{maj} = 9$, and $2\,4\,1\,3\,6\,5$ has $D = \{2, 5\}$ and $\operatorname{maj} = 7$.

**Inverse descents.** In $\pi = 3\,1\,4\,5\,2$ the values $1, 2, 3, 4, 5$ stand at the positions $2, 5, 1, 3, 4$. The value $i + 1$ stands before the value $i$ only for $i = 2$, since 3 is at position 1 and 2 at position 5. So the only inverse descent is 2, and indeed $\pi^{-1} = 2\,5\,1\,3\,4$ has $D(\pi^{-1}) = \{2\}$.

**Eulerian numbers.** For $n = 4$ the 24 permutations have $0, 1, 2, 3$ descents in $1, 11, 11, 1$ cases, and for $n = 5$ in $1, 26, 66, 26, 1$ cases. The mean for $n = 5$ is $2$ and the variance $1/2 = 6/12$.

**Counting by descent set.** Among the permutations of $[5]$, $\binom52 = 10$ have $D(\pi) \subseteq \{2\}$ and 9 have $D(\pi) = \{2\}$, all but the identity. $\binom{5}{1,\,2,\,2} = 30$ have $D(\pi) \subseteq \{1, 3\}$, and $30 - 5 - 10 + 1 = 16$ have $D(\pi) = \{1, 3\}$.

**Non-example: descents are not inversions.** $2\,3\,4\,5\,1$ has a single descent but 4 inversions, and $2\,1\,4\,3\,6\,5$ has 3 descents and 3 inversions. The number of descents is at most the number of inversions, and the two can be far apart.

## Related definitions

- **[Inversions](/inversion/).** Pairs $i < j$ with $a_i > a_j$ at any distance. Descents are the inversions with $j = i + 1$.
- **[Eulerian numbers](/eulerian-numbers/).** The distribution of $\operatorname{des}$ over $S_n$.
- **[Mahonian numbers](/mahonian-numbers/).** The common distribution of $\operatorname{inv}$ and $\operatorname{maj}$.
- **[Presortedness](/presortedness/).** The number of runs, $\operatorname{des} + 1$, is the measure $\mathrm{Runs}$ used in [adaptive sorting](/adaptive-sorting/), and [natural merge sort](/natural-merge-sort/) takes $O(n \log(\operatorname{des} + 2))$ time.
- **Peaks and alternating permutations.** A peak is an $i$ with $a_{i-1} < a_i > a_{i+1}$. Permutations whose descents are exactly the even positions are alternating, counted by the Euler zigzag numbers.

## References
