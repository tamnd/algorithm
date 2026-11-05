---
tag: KXY88Q
kind: concept
slug: permutation-inverse
name: Inverse permutation
aliases:
- inverse of a permutation
area: sequences/inversions-and-permutations
level: intro
summary: The permutation that undoes a given one; computable in O(n) time.
prereqs: [permutation]
see_also: [permutation-cycles, inversion-table, lehmer-code, symmetric-group, kendall-tau-distance, cycle-leader-permutation, succinct-permutation]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3 (the inverse of a permutation, and Algorithms I and J for inverting a permutation in place)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inverses, inversion tables and the inversions of the inverse)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Sections 1.3 and 1.4 (cycles, inversions and descents of a permutation and of its inverse)
---

The inverse of a [permutation](/permutation/) $\pi$ is the permutation $\pi^{-1}$ that undoes it: $\pi^{-1}(j) = i$ exactly when $\pi(i) = j$. In an array, $\pi$ maps positions to values and $\pi^{-1}$ maps each value back to its position, so one pass with $\pi^{-1}[\pi[i]] \leftarrow i$ computes it in $\Theta(n)$ time. The inverse turns a list of ranks into the sorting order of the items and back, which is the step behind [Kendall tau distance](/kendall-tau-distance/), [inversion tables](/inversion-table/) and many index tricks. It can also be computed in place, by reversing each [cycle](/permutation-cycles/).

## In plain words

A permutation is a rule that says, for each seat, which person sits there. Its inverse answers the opposite question: for each person, which seat they are in. Both carry the same information, read in the other direction.

To build the inverse, walk over the seats. Seat one holds some person, so write "seat one" next to that person's name. Do this for every seat. One walk is enough. If you apply a permutation and then its inverse, every item is back where it started.

## The idea

**Definition.** For a permutation $\pi$ of $[n]$, the inverse $\pi^{-1}$ is the unique permutation with

$$\pi^{-1}(\pi(i)) = i \quad \text{and} \quad \pi(\pi^{-1}(j)) = j \qquad \text{for all } i, j \in [n].$$

It exists because $\pi$ is a bijection, and it is unique because a function has at most one two-sided inverse. In two-line notation, $\pi^{-1}$ is $\pi$ with the two rows exchanged and the columns sorted by the new top row.

**Computing it.** For an array $P[1 \ldots n]$ that holds $\pi$:

```pseudo
INVERSE(P[1 .. n])
1  Q[1 .. n] ← new array
2  for i ← 1 to n do Q[P[i]] ← i
3  return Q
```

Line 2 runs $n$ times, and each $j \in [n]$ is written exactly once, at the unique $i$ with $P[i] = j$. So $Q = \pi^{-1}$, in $\Theta(n)$ time and $n$ extra words.

**In place.** The inverse has the same cycles as $\pi$, each traversed backwards. So $\pi^{-1}$ can overwrite $P$ by reversing the links of each cycle, with the sign of an entry as the mark "done":

```pseudo
INVERT-IN-PLACE(P[1 .. n])                 ▷ the values are 1 .. n
1  for i ← 1 to n do
2      if P[i] > 0 then                    ▷ the cycle of i is not done yet
3          prev ← i, j ← P[i]
4          while j ≠ i do
5              next ← P[j], P[j] ← −prev, prev ← j, j ← next
6          P[i] ← −prev
7  for i ← 1 to n do P[i] ← −P[i]
```

On the cycle $i \to j_1 \to j_2 \to \cdots \to j_{k-1} \to i$, line 5 sets $P[j_1] = -i$, $P[j_2] = -j_1$, and so on, and line 6 sets $P[i] = -j_{k-1}$. These are the links of the reversed cycle. Each entry is negated once in the first loop and once in the second, so the time is $\Theta(n)$ and the extra space is $O(1)$ words plus the sign bit of each entry. Knuth gives this kind of method as Algorithm I in Section 1.3.3, and a second one due to B. C. Huang as Algorithm J.

**Laws.**

- $(\pi^{-1})^{-1} = \pi$, and $\iota^{-1} = \iota$.
- $(\sigma\tau)^{-1} = \tau^{-1}\sigma^{-1}$: to undo "do $\tau$, then $\sigma$", undo $\sigma$ first. In general $(\sigma\tau)^{-1} \ne \sigma^{-1}\tau^{-1}$.
- $(a_1\ a_2\ \cdots\ a_k)^{-1} = (a_k\ \cdots\ a_2\ a_1)$, so $\pi$ and $\pi^{-1}$ have the same cycle type, the same [order](/permutation-power/) and the same [parity](/permutation-parity/).
- $\operatorname{inv}(\pi^{-1}) = \operatorname{inv}(\pi)$: the map $(i, j) \mapsto (\pi(j), \pi(i))$ is a bijection between their [inversions](/inversion/).
- The [permutation matrix](/permutation/) of $\pi^{-1}$ is the transpose of that of $\pi$. The plot of the points $(i, \pi(i))$ of $\pi^{-1}$ is the plot of $\pi$ reflected in the main diagonal.
- Knuth's [inversion table](/inversion-table/) of $\pi$, which counts for each value the larger values to its left, equals the [Lehmer code](/lehmer-code/) of $\pi^{-1}$, which counts for each position the smaller entries to its right.
- $\pi$ has a descent at $i$, $\pi(i) > \pi(i+1)$, while $\pi^{-1}$ has a descent at $k$ exactly when the value $k + 1$ appears before the value $k$ in $\pi$. These *inverse descents* differ from the [descents](/descents/) of $\pi$ in general.
- An *involution* is a permutation with $\pi = \pi^{-1}$, which means that all its cycles have length 1 or 2. For $n = 1, \ldots, 7$ there are $1, 2, 4, 10, 26, 76, 232$ of them.

## Examples

**A 5-cycle.** For $\pi = 3\,1\,4\,5\,2 = (1\ 3\ 4\ 5\ 2)$, line 2 of INVERSE writes $Q[3] = 1$, $Q[1] = 2$, $Q[4] = 3$, $Q[5] = 4$ and $Q[2] = 5$, so

$$\pi^{-1} = 2\,5\,1\,3\,4 = (2\ 5\ 4\ 3\ 1) = (1\ 2\ 5\ 4\ 3),$$

the same cycle backwards. Both have 4 inversions.

**Inverse as a power.** $\sigma = 2\,4\,1\,3\,6\,5 = (1\ 2\ 4\ 3)(5\ 6)$ has order 4, so $\sigma^{-1} = \sigma^3 = 3\,1\,4\,2\,6\,5$.

**Ranks and sorting order.** The array $A = (40, 10, 70, 90, 20)$ has the rank permutation $3\,1\,4\,5\,2$: $A[1] = 40$ is the third smallest, and so on. Its inverse $2\,5\,1\,3\,4$ lists the positions of $A$ in sorted order: $A[2] = 10 < A[5] = 20 < A[1] < A[3] < A[4]$. This is what `argsort` returns. So "rank of each item" and "item of each rank" are inverse permutations, and each one is computed from the other in $\Theta(n)$ time.

**Non-example.** Reversing the one-line notation does not invert: the reverse of $3\,1\,4\,5\,2$ is $2\,5\,4\,1\,3$, which is $\pi$ composed with the reversal $i \mapsto n + 1 - i$, not $\pi^{-1}$.

## Where it is used

- **[Kendall tau distance](/kendall-tau-distance/).** To compare rankings $\sigma$ and $\tau$, relabel by $\tau^{-1}$ and count the inversions of $\tau^{-1}\sigma$.
- **[Inversion tables](/inversion-table/) and [Lehmer codes](/lehmer-code/).** The two codes of $\pi$ are exchanged by taking the inverse.
- **Sorting by keys.** An index sort produces the inverse of the rank permutation, and applying it with a [cycle-leader permutation](/cycle-leader-permutation/) moves the records into place.
- **Positions of items.** Keeping both $\pi$ and $\pi^{-1}$ lets a program answer "what is at position $i$" and "where is item $j$" in $O(1)$ time. A [succinct permutation](/succinct-permutation/) stores $\pi$ in about $n \lg n$ bits and computes $\pi^{-1}$ with a few extra bits.
- **Group computations.** In the [symmetric group](/symmetric-group/), conjugation $\rho\pi\rho^{-1}$ relabels the items of $\pi$ by $\rho$.

## References
