---
tag: 5CEWMG
kind: technique
slug: sum-over-subsets-dp
name: Sum over subsets (SOS) dynamic programming
aliases:
- SOS DP
area: techniques/dynamic-programming
level: advanced
summary: Compute, for every mask, an aggregate over all its submasks in O(n 2^n) time.
prereqs: [bitmask-dp, prefix-sums, submask-enumeration]
see_also: [sos-dp, sum-over-subsets, bitmask-dp, submask-enumeration, inclusion-exclusion-principle, prefix-sums]
sources:
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 7, Subset Convolution, Section 7.1, Fast zeta Transform
  - paper: doi:10.1145/1250790.1250801
    title: Andreas Björklund, Thore Husfeldt, Petteri Kaski and Mikko Koivisto, Fourier meets Möbius, fast subset convolution, Proceedings of the 39th ACM STOC, 67-74, 2007
    locator: the fast zeta and Möbius transforms over the subset lattice
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546-563, 2009
    locator: the use of the zeta transform for counting covers and partitions
---

Sum over subsets DP is the technique of computing, for every subset $S$ of an $n$-element set, an aggregate of $f(T)$ over all $T \subseteq S$ (or over all $T \supseteq S$), by treating the subsets as the corners of an $n$-dimensional cube with side 2 and taking [prefix sums](/prefix-sums/) along one dimension at a time. It takes $O(n 2^n)$ operations instead of the $O(3^n)$ of a loop over all submasks of all masks. This page is about when and how to use the method. The exact problem is on the [sum over subsets](/sum-over-subsets/) page, and the algorithm with its proof of correctness is on the [SOS DP](/sos-dp/) page.

## In plain words

Sometimes you need, for every set of items, a total over all of its smaller sets. For example: for every set of features, how many products have only features from that set. Visiting all smaller sets of all sets is slow.

Instead, handle one item at a time. In the first round, every set that contains item 0 adds in the total of the same set without item 0. In the next round, do the same for item 1, and so on. After the last round, every set holds the total over all of its smaller sets, and each round was only one pass over the table.

## When it applies

- The answer for each mask $S$ needs an aggregate over its submasks $T \subseteq S$, or over its supermasks $T \supseteq S$.
- The aggregate is associative and commutative: sum, count, minimum, maximum, OR, or a sum modulo a prime. For subtraction-based questions (exact counts from "at most" counts), it also needs an inverse, as for sums.
- $n$ is at most about 20 to 23, so that the $2^n$ table fits in memory.
- The problem talks about bitwise AND, OR or the relation "is a subset of" between pairs of numbers below $2^n$. Questions such as "for each $x$, count the $y$ with $x \mathbin{\&} y = 0$" become submask questions, since $x \mathbin{\&} y = 0$ means $y \subseteq \overline{x}$.

## The template

The holes are the starting values, the operator $\oplus$ and the direction (submasks or supermasks).

```pseudo id=main
SOS(f, n)
L1  F ← copy of f                                     ▷ hole: the starting values f[T]
L2  for i ← 0 to n − 1 do                             ▷ one dimension per round
L3      for S ← 0 to 2^n − 1 do
L4          if bit i of S is 1 then                   ▷ hole: use bit 0 for supermasks
L5              F[S] ← F[S] ⊕ F[S without bit i]      ▷ hole: the operator ⊕; for supermasks use S with bit i
L6  return F
```

**Why it works.** After the rounds for the bits $0, \ldots, i$, the entry $F[S]$ holds the aggregate of $f(T)$ over the sets $T$ that agree with $S$ on the bits $i+1, \ldots, n-1$ and satisfy $T \subseteq S$ on the bits $0, \ldots, i$. The round for bit $i$ joins the two halves that differ only in bit $i$, exactly as one pass of a prefix sum along that dimension. Each $T \subseteq S$ is counted once, because it is reached by one path: at each bit where $S$ has 1 and $T$ has 0, one round takes the value from the side without that bit. The full proof is on the [SOS DP](/sos-dp/) page.

**Cost.** Line L5 runs $n 2^{n-1}$ times. The update is in place, which is safe because the value read in line L5 has bit $i$ equal to 0 and is not changed in round $i$.

**The inverse.** For sums, running the same loop with subtraction in line L5 recovers $f$ from $F$. This is the Möbius transform, and with the zeta transform it gives the fast subset convolution of Björklund, Husfeldt, Kaski and Koivisto in $O(n^2 2^n)$ time.

## Classic examples

Let the numbers be $a = (1, 2, 3, 4, 6)$, all below $2^3$, and let $c[x]$ count the copies of $x$, so $c = (0, 1, 1, 1, 1, 0, 1, 0)$ for $x = 0, \ldots, 7$.

**Count the submask elements of each mask.** Run the template on $c$ with $+$. The table after each round is:

| round | $F[0]$ | $F[1]$ | $F[2]$ | $F[3]$ | $F[4]$ | $F[5]$ | $F[6]$ | $F[7]$ |
|---|---|---|---|---|---|---|---|---|
| start | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 0 |
| bit 0 | 0 | 1 | 1 | 2 | 1 | 1 | 1 | 1 |
| bit 1 | 0 | 1 | 1 | 3 | 1 | 1 | 2 | 2 |
| bit 2 | 0 | 1 | 1 | 3 | 1 | 2 | 3 | 5 |

So $F[6] = 3$: the elements 2, 4 and 6 are submasks of $110_2$.

**Count the pairs with AND equal to 0.** For each $x$, the $y$ with $x \mathbin{\&} y = 0$ are the submasks of $7 \oplus x$. Summing $F[7 \oplus x]$ over the elements gives $F[6] + F[5] + F[4] + F[3] + F[1] = 3 + 2 + 1 + 3 + 1 = 10$ ordered pairs, which are the 5 pairs $\{1, 2\}$, $\{1, 4\}$, $\{1, 6\}$, $\{2, 4\}$ and $\{3, 4\}$, each in two orders.

**Count the subsets with AND equal to 0.** Let $G[m]$ be the number of elements that contain $m$, by the supermask form: $G = (5, 2, 3, 1, 2, 0, 1, 0)$. A nonempty set of elements has an AND that contains $m$ exactly when all its elements contain $m$, which gives $2^{G[m]} - 1$ sets. By the [inclusion-exclusion principle](/inclusion-exclusion-principle/), the number of nonempty sets with AND equal to 0 is

$$\sum_{m} (-1)^{|m|} \bigl( 2^{G[m]} - 1 \bigr) = 31 - 3 - 7 + 1 - 3 + 0 + 1 - 0 = 20.$$

A check of all 31 nonempty sets gives the same 20.

**Other uses.**

- For each $x$, find some $y$ in the input with $x \mathbin{\&} y = 0$: run the template with the operator "keep any nonzero witness".
- Counting covers and partitions, and the chromatic number in $O(2^n \operatorname{poly}(n))$ time, by Björklund, Husfeldt and Koivisto.
- The best value over all submasks, such as the largest weight of an independent set contained in $S$, with $\max$ as the operator.

## Variations

- **Supermasks.** Change the test of line L4 to bit $i$ equal to 0 and read $F[S \text{ with bit } i]$. This is the same method on the complemented masks.
- **Möbius inversion.** Subtract in place of add to undo the transform. Use it to get "exactly $S$" counts from "within $S$" counts.
- **Subset convolution.** Combine the zeta transform, ranked by the number of bits, with pointwise products and the Möbius transform, to compute $h(S) = \sum_{T \subseteq S} f(T) g(S \setminus T)$ for all $S$ in $O(n^2 2^n)$.
- **Higher bases.** The same idea works on any product of chains: for digits in base $b$, take a prefix aggregate along each digit position.

## Pitfalls

- **The order of the loops.** The loop over the bits must be the outer loop. With the loop over masks outside, some submasks are counted more than once and others are missed.
- **Using it where $O(3^n)$ is needed.** SOS gives one aggregate per mask over all submasks. A DP whose value for $S$ depends on a combination of $f(T)$ and $g(S \setminus T)$ for each split is a subset convolution or a [bitmask DP](/bitmask-dp/) in split form, not plain SOS.
- **Operators without an inverse.** With $\max$ or $\min$, the transform cannot be undone, so "exactly" counts cannot be recovered.
- **Overflow.** Counts like $2^{G[m]}$ grow fast; compute modulo a prime when the problem allows it.

## Exercises

1. Show that the template with the loops swapped (masks outside, bits inside) gives a wrong result for $n = 2$ and $f = (1, 1, 1, 1)$.
2. Given $2^n$ values $F[S] = \sum_{T \subseteq S} f(T)$, recover $f$ in $O(n 2^n)$ time.
3. For each element $x$ of an array of numbers below $2^{20}$, count the elements $y$ with $x \mathbin{|} y = x$.
   <details><summary>Hint</summary>$x \mathbin{|} y = x$ means $y \subseteq x$; this is the submask count of the first example.</details>
4. Count the pairs $(x, y)$ of elements with $x \mathbin{\&} y = z$ for a given $z$, using the supermask form and inclusion-exclusion.

## References
