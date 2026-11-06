---
tag: 2ABXMX
kind: algorithm
slug: sos-dp
name: Sum over subsets dynamic programming
aliases:
- SOS DP
- subset zeta transform
- sum over subsets DP
area: techniques/bit-tricks
level: advanced
summary: Computes all subset sums in O(k 2^k) time by adding one bit at a time to the mask.
solves: [sum-over-subsets]
model: word-ram
complexity:
  vars: {n: "the number of bits of a mask, so the input has 2^n values"}
  time: {worst: Θ(n 2^n), average: Θ(n 2^n), best: Θ(n 2^n)}
  space: {extra: Θ(1)}
prereqs: [bitmask, sum-over-subsets, submask-enumeration, loop-invariant]
see_also: [sum-over-subsets-dp, sum-over-subsets, submask-enumeration, fast-walsh-hadamard-transform, mobius-inversion, bjorklund-chromatic-number, bitmask-dp]
sources:
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 7, Subset Convolution, Section 7.1, Fast zeta Transform
  - paper: doi:10.1145/1250790.1250801
    title: Andreas Björklund, Thore Husfeldt, Petteri Kaski and Mikko Koivisto, Fourier meets Möbius, fast subset convolution, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC), 2007
    locator: pp. 67 to 74 (the fast zeta and Möbius transforms and their use for subset convolution)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

SOS DP computes, for every mask $m$ of $n$ bits, the sum $F[m] = \sum_{s \subseteq m} f[s]$, by $n$ passes over the array, one for each bit. Pass $i$ adds $F[m \oplus 2^i]$ into $F[m]$ for every $m$ with bit $i$ set. It solves the [sum over subsets](/sum-over-subsets/) problem with exactly $n 2^{n-1}$ additions, in place, against $3^n - 2^n$ for the direct method with [submask enumeration](/submask-enumeration/). In the literature on exact algorithms it is the fast zeta transform, and run with subtraction it is the fast Möbius transform. This page is the algorithm; the page [sum over subsets DP](/sum-over-subsets-dp/) treats it as a design technique for dynamic programs.

## In plain words

Think of each mask as a corner of a cube with one direction for each bit. The sum for a corner must collect the values of all corners below it, in every direction at once.

Collect one direction at a time. In the first pass, each corner that has bit 0 on takes the value of its neighbor with bit 0 off. Now each corner holds the total along the first direction. In the second pass, each corner with bit 1 on takes the value of its neighbor with bit 1 off, which already holds a total along the first direction. After one pass for each bit, every corner holds the total over all corners below it.

Each pass touches each corner once, so the work is the number of bits times the number of masks.

## The problem

The input is $n \ge 0$ and an array $f[0 \ldots 2^n - 1]$ of values in a commutative monoid, usually integers with $+$. The output is the array $F$ with $F[m] = \sum_{s \subseteq m} f[s]$, where $s \subseteq m$ means that each bit of $s$ is also a bit of $m$. This is the [sum over subsets](/sum-over-subsets/) problem, the zeta transform of the lattice of subsets.

## The algorithm

```pseudo id=main
SOS-DP(f, n)
L1  F ← a copy of f
L2  for i ← 0 to n − 1 do
L3      for m ← 0 to 2^n − 1 do
L4          if bit i of m is 1 then
L5              F[m] ← F[m] + F[m XOR 2^i]
L6  return F
```

Line L5 reads $F[m \oplus 2^i]$, an entry with bit $i$ clear. Pass $i$ writes only to entries with bit $i$ set, so this entry still holds its value from the end of pass $i - 1$, whatever the order of $m$ in line L3. So the array can be updated in place and the inner loop can run in any order, or in parallel.

The supersets version changes line L4 to "bit $i$ of $m$ is 0" and line L5 to $F[m] \leftarrow F[m] + F[m \mathbin{|} 2^i]$. The Möbius transform, the inverse, keeps lines L1 to L4 and subtracts in line L5.

## Example

Let $n = 3$ and $f = [3, 1, 4, 1, 5, 9, 2, 6]$, indexed by $m = 000_2$ to $111_2$.

| after | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | 3 | 1 | 4 | 1 | 5 | 9 | 2 | 6 |
| pass $i = 0$ | 3 | 4 | 4 | 5 | 5 | 14 | 2 | 8 |
| pass $i = 1$ | 3 | 4 | 7 | 9 | 5 | 14 | 7 | 22 |
| pass $i = 2$ | 3 | 4 | 7 | 9 | 8 | 18 | 14 | 31 |

In pass 0, $F[001] = 1 + 3 = 4$ and $F[111] = 6 + 2 = 8$. In pass 1, $F[011] = 5 + 4 = 9$, which is $f[000] + f[001] + f[010] + f[011]$. In pass 2, $F[111] = 22 + 9 = 31$, the sum of all eight values. Each pass does $2^{3-1} = 4$ additions, so 12 in all; the direct method does $3^3 - 2^3 = 19$.

## Correctness

For $0 \le i \le n$ and a mask $m$, let $S_i(m)$ be the set of submasks $s \subseteq m$ that agree with $m$ on bits $i$ to $n - 1$. So $S_0(m) = \{m\}$ and $S_n(m)$ is the set of all submasks of $m$. The loop of line L2 keeps this [loop invariant](/loop-invariant/):

> Before pass $i$, $F[m] = \sum_{s \in S_i(m)} f[s]$ for every $m$.

Line L1 makes it true for $i = 0$. In pass $i$, if bit $i$ of $m$ is 0, then $S_{i+1}(m) = S_i(m)$ and $F[m]$ does not change. If bit $i$ of $m$ is 1, then $S_{i+1}(m)$ is the disjoint union of $S_i(m)$, the submasks with bit $i$ set, and $S_i(m \oplus 2^i)$, those with bit $i$ clear; line L5 adds the two sums, and the second one is still the value from before the pass, as shown above. After pass $n - 1$ the invariant for $i = n$ is the claim. The full proof is below.

## Complexity

- **Additions.** Pass $i$ does one addition for each of the $2^{n-1}$ masks with bit $i$ set, so there are exactly $n 2^{n-1}$ additions, in each case.
- **Time.** Lines L3 and L4 run $n 2^n$ times, so the time is $\Theta(n 2^n)$ on the [word RAM](/word-ram/) when an addition of two values costs $O(1)$. A loop that visits only the masks with bit $i$ set halves the tests but not the bound.
- **Space.** In place, $\Theta(1)$ extra words besides the output array, or the input array if it may be overwritten.

| $n$ | 10 | 16 | 20 | 24 |
| --- | --- | --- | --- | --- |
| SOS DP, $n 2^{n-1}$ | 5120 | 524288 | 10485760 | 201326592 |
| direct, $3^n - 2^n$ | 58025 | 42981185 | 3485735825 | 282412759265 |

## Properties

- **In place.** Line L5 reads only entries that the current pass does not write.
- **Order-free inner loop.** The masks of one pass can be done in any order, and in parallel; only the passes must run in sequence.
- **Oblivious.** The sequence of additions does not depend on the values, so the same code works for any commutative monoid: sums, $\max$, $\min$, OR, $\gcd$.
- **Exact on integers.** With integer values there is no rounding; the only risk is overflow, below.

## Variants and improvements

- **Sum over supersets.** Test for bit $i$ clear and read $F[m \mathbin{|} 2^i]$. Gives $G[m] = \sum_{s \supseteq m} f[s]$.
- **Möbius transform.** Subtract in line L5. Gives back $f$ from $F$ in $n 2^{n-1}$ subtractions; with supersets it inverts the superset transform.
- **OR and AND convolution.** Transform both inputs, multiply pointwise, and apply the Möbius transform: three runs and $2^n$ products. See [sum over subsets](/sum-over-subsets/).
- **Ranked transform and subset convolution.** Split $f$ by the number of ones of the mask into $n + 1$ arrays, transform each, and combine the ranks; this gives subset convolution in $O(n^2 2^n)$ operations (Björklund, Husfeldt, Kaski and Koivisto).
- **Other operators per bit.** Replacing the pair update $(F[m \oplus 2^i], F[m]) \mapsto (F[m \oplus 2^i], F[m] + F[m \oplus 2^i])$ with $(a, b) \mapsto (a + b, a - b)$ gives the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), with the same loop structure.
- **Several dimensions of larger size.** For indices with digits in base $b$, the same pass per digit with prefix sums along that digit gives sums over the dominated indices.

## When to use it

Use SOS DP when every mask of $n$ bits needs an aggregate over all its submasks or supersets, and $n$ is up to about 25, so that $2^n$ values fit in memory. If only a few masks need the sum, [submask enumeration](/submask-enumeration/) for those masks alone costs $2^{\operatorname{pop}(m)}$ each and needs no table. If the aggregate is over masks $s$ with $s \oplus m$ in some set, rather than $s \subseteq m$, the Walsh-Hadamard transform is the right tool. For the design of a whole dynamic program around this pass structure, see [sum over subsets DP](/sum-over-subsets-dp/).

## Pitfalls

- **Loops in the wrong nesting.** With the loop over masks outside and the loop over bits inside, line L5 reads entries that are already final for other bits, and some subsets are counted more than once. For $f$ all ones and $n = 2$, the wrong order gives $F[11] = 5$ instead of 4. The loop over bits must be outside, as in line L2.
- **Reading the updated neighbor.** In place, the supersets version must read $F[m \mathbin{|} 2^i]$ and test bit $i$ clear; mixing the subset test with the superset read adds an entry that the same pass has already changed.
- **Overflow.** $F[2^n - 1]$ is the sum of all $2^n$ inputs. With values up to $10^9$ and $n = 20$, it is about $10^{15}$, beyond 32 bits. Use 64-bit sums or reduce modulo a prime.
- **Möbius in the wrong order of signs.** The inverse subtracts, $F[m] \leftarrow F[m] - F[m \oplus 2^i]$, in the same loop order; adding the sign $(-1)^{\operatorname{pop}(m)}$ by hand to each term is a common source of errors.
- **Memory for large n.** For $n = 30$ the array has about $10^9$ entries. Check that $2^n$ values fit before you choose this method.

## Implementations

## History

The fast zeta and Möbius transforms on the lattice of subsets are used by Björklund, Husfeldt, Kaski and Koivisto in their 2007 paper on fast subset convolution, which builds subset convolution in $O(n^2 2^n)$ operations from ranked zeta transforms. Fomin and Kratsch present the fast zeta transform in Section 7.1 of their book on exact exponential algorithms. In programming contests the same loop is known as SOS DP and is used to answer queries over submasks.

## References
