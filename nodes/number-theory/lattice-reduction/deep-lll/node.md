---
tag: NEWYCT
kind: algorithm
slug: deep-lll
name: Deep LLL
aliases:
- deep insertion LLL
- deep-insertion reduction
- LLL with deep insertions
- Schnorr-Euchner deep insertion
area: number-theory/lattice-reduction
level: advanced
summary: LLL variant that inserts a vector at any earlier position for stronger reduction.
solves: [lattice-basis-reduction]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors, P: "the number of passes of the main loop, finite but with no known polynomial bound"}
  time: {worst: O(n^2 m P), best: O(n^2 m), per_pass: O(n^2 m)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, exact: true, polynomial_time: false}
history:
  year: 1994
  people: [Claus-Peter Schnorr, Martin Euchner]
  note: Schnorr and Euchner introduced deep insertions in their 1994 paper on practical lattice reduction, together with floating-point LLL and BKZ.
prereqs: [lll-algorithm, gram-schmidt-orthogonalization, size-reduction]
see_also: [bkz-algorithm, lovasz-condition, lll-reduction, hkz-reduction, root-hermite-factor, approximate-svp, lattice-basis-reduction, schnorr-euchner-enumeration]
sources:
  - paper: "C. P. Schnorr and M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Mathematical Programming 66 (1994)"
    locator: pages 181 to 199 (LLL with deep insertions and its use on subset sum lattices)
  - paper: "N. Gama and P. Q. Nguyen, Predicting lattice reduction, EUROCRYPT 2008, LNCS 4965"
    locator: the experimental root Hermite factors of LLL, deep insertion and BKZ on random lattices
  - paper: "F. Fontein, M. Schneider and U. Wagner, PotLLL: a polynomial time version of LLL with deep insertions, Designs, Codes and Cryptography 73(2) (2014)"
    locator: pages 355 to 368 (the potential-based insertion rule and its polynomial running time)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 17, Lattice basis reduction (variants of LLL, including deep insertions)
---

Deep LLL is the [LLL algorithm](/lll-algorithm/) with a stronger exchange step: instead of only swapping $b_k$ with its neighbour $b_{k-1}$, it may move $b_k$ to any earlier position $i$ where it would make the $i$-th [Gram-Schmidt](/gram-schmidt-orthogonalization/) vector shorter by more than the factor $\delta$. Schnorr and Euchner introduced it in 1994. The output is LLL-reduced and in practice noticeably better, close to [BKZ](/bkz-algorithm/) with small blocks, but no polynomial bound on its running time is known.

## In plain words

LLL tidies a set of arrows that build a grid. It walks along the list, and when an arrow fits better one place earlier, it swaps the two and steps back.

Deep LLL lets the arrow jump further. It looks at how short the arrow would be if it were placed at the front, then second, then third, and so on. As soon as some earlier place would be a clear improvement, the arrow is pulled out and put there, and the walk resumes from that place.

Jumping far fixes in one move what LLL might never fix, because LLL stops as soon as no neighbour swap helps. The price is that nobody has proved that the walk ends quickly; it ends, but possibly after a very long time.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ and a parameter $\delta$ with $1/4 < \delta \le 1$.

**Output.** A basis of the same lattice that is **deep-reduced**: size-reduced, $|\mu_{kj}| \le 1/2$ for $j < k$, and

$$\|\pi_i(b_k)\|^2 = N_k + \sum_{j=i}^{k-1} \mu_{kj}^2 N_j \ \ge\ \delta N_i \qquad \text{for all } i < k,$$

where $\pi_i$ projects orthogonally to $b_1, \ldots, b_{i-1}$ and $N_j = \|b_j^*\|^2$. For $i = k - 1$ this is the [Lovász condition](/lovasz-condition/), so a deep-reduced basis is LLL-reduced.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the Gram-Schmidt data, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the reduction parameter. All arithmetic in the reference implementation is exact, on rationals. Time counts arithmetic operations per pass of the main loop. The bound per pass is proved; the number of passes is proved finite only; the quality figures in practice are observed.

## The algorithm

```pseudo id=main
DEEP-LLL(B, δ)                      ▷ independent rows b_1..b_n, 1/4 < δ ≤ 1
L1  k ← 2
L2  while k ≤ n
L3      size-reduce b_k against b_{k−1}, ..., b_1
L4      C ← ‖b_k‖²; i ← 1                 ▷ C = ‖π_i(b_k)‖²
L5      while i < k
L6          if C < δ N_i then move b_k to position i; k ← max(i, 2); go to L2
L7          C ← C − μ_ki² N_i; i ← i + 1
L8      k ← k + 1
L9  return B
```

Moving $b_k$ to position $i$ shifts $b_i, \ldots, b_{k-1}$ one place up. The new $i$-th Gram-Schmidt vector is $\pi_i(b_k)$, which is shorter than $\sqrt\delta \, \|b_i^*\|$. LLL is the special case where line L6 is tried only for $i = k - 1$.

## Example

The basis $b_1 = (4, 0, 0)$, $b_2 = (-2, 3, 0)$, $b_3 = (1, 1, 3)$ with $\delta = 3/4$. It is LLL-reduced: $\mu_{21} = -\tfrac12$, $N = (16, 9, 9)$, $\mu_{31} = \tfrac14$, $\mu_{32} = \tfrac13$, and $9 \ge (\tfrac34 - \tfrac14) \cdot 16$, $9 \ge (\tfrac34 - \tfrac19) \cdot 9$. So LLL leaves it unchanged. But $\|b_3\|^2 = 11 < \tfrac34 \cdot 16 = 12$, so deep LLL moves $b_3$ to the front.

| Pass | $k$ | After L3 | Checks at L6 | Action |
|------|-----|------|------|------|
| 1 | 2 | $b_2 = (-2, 3, 0)$ | $i = 1$: $13 \ge 12$ | $k \leftarrow 3$ |
| 2 | 3 | $b_3 = (1, 1, 3)$ | $i = 1$: $11 < 12$ | move $b_3$ to position 1, $k \leftarrow 2$ |
| 3 | 2 | basis $(1, 1, 3), (4, 0, 0), (-2, 3, 0)$ | $i = 1$: $16 \ge \tfrac{33}{4}$ | $k \leftarrow 3$ |
| 4 | 3 | $b_3 = (2, 3, 0)$ | $i = 1$: $13 \ge \tfrac{33}{4}$; $i = 2$: $\tfrac{118}{11} < \tfrac34 \cdot \tfrac{160}{11} = \tfrac{120}{11}$ | move $b_3$ to position 2, $k \leftarrow 2$ |
| 5 | 2 | basis $(1, 1, 3), (2, 3, 0), (4, 0, 0)$ | $i = 1$: $13 \ge \tfrac{33}{4}$ | $k \leftarrow 3$ |
| 6 | 3 | $b_3 = (2, -3, 0)$ | $i = 1$: $13 \ge \tfrac{33}{4}$; $i = 2$: $\tfrac{142}{11} \ge \tfrac{177}{22}$ | $k \leftarrow 4$, stop |

The output $(1, 1, 3), (2, 3, 0), (2, -3, 0)$ has squared lengths $11, 13, 13$, and $11 = \lambda_1^2$, which enumeration confirms. Pass 4 is an ordinary LLL swap of positions 2 and 3; pass 2 is a deep insertion that LLL would not make.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Size reduction and moving a row are unimodular, so the lattice never changes. After a pass that ends without an insertion, $b_k$ is size-reduced and satisfies the deep condition against every earlier position, because $C$ runs through $\|\pi_1(b_k)\|^2, \|\pi_2(b_k)\|^2, \ldots$; so the first $k$ vectors are deep-reduced, and an insertion at position $i$ keeps the first $i - 1$ untouched. When $k$ passes $n$, the whole basis is deep-reduced.

For termination, let $D_j = N_1 \cdots N_j$. An insertion at position $i$ keeps $D_1, \ldots, D_{i-1}$ and multiplies $D_i$ by less than $\delta$. For a lattice with entries in $\frac1s \mathbb{Z}$, the scaled values $s^{2j} D_j$ are positive integers, so the tuple $(s^2 D_1, \ldots, s^{2n} D_n)$ decreases lexicographically at every insertion, and a strictly decreasing sequence of tuples of positive integers in that order is finite. This works even for $\delta = 1$, but it gives no polynomial bound.

## Complexity

- **Per pass, proved.** One pass computes the Gram-Schmidt data of $b_1, \ldots, b_k$ in $O(n^2 m)$ arithmetic operations, size-reduces $b_k$ in $O(n m + n^2)$ and runs the insertion test in $O(n)$. So the total is $O(n^2 m P)$ for $P$ passes; an implementation that updates the Gram-Schmidt data after each insertion instead of recomputing them brings a pass down to $O(n m)$ in the common case.
- **Number of passes, open.** Between two insertions there are at most $n - 1$ passes, and the number of insertions is finite. LLL's potential $\prod_j D_j$ can increase at a deep insertion, since $D_{i+1}, \ldots, D_{k-1}$ may grow, so the LLL argument fails, and no polynomial bound is known for unrestricted deep insertions. Schnorr and Euchner reported that it can be slow in high dimension, which led to restricted depth.
- **Restricted depth.** Allowing insertions only at positions $i \le \eta$ or $k - i \le \eta$ for a fixed depth $\eta$ is the form used in practice. With insertions restricted to the case where they decrease the potential by the factor $\delta$, as in PotLLL, the running time is polynomial, like LLL.
- **Observed quality.** On random lattices in moderate dimension, Gama and Nguyen measured a [root Hermite factor](/root-hermite-factor/) of about $1.011$ for deep insertion with depth 50, against about $1.0219$ for LLL and $1.0128$ for BKZ with block size 20. These are experiments, not bounds.
- **Proved quality.** The output is LLL-reduced, so with $\alpha = 1/(\delta - 1/4)$, $\|b_1\|^2 \le \alpha^{n-1} \lambda_1^2$ and $\|b_1\| \le \alpha^{(n-1)/4} \det(L)^{1/n}$. The worst-case guarantee is the same as LLL's.

## Properties

- **Stronger than LLL.** Every deep-reduced basis is LLL-reduced with the same $\delta$; the converse fails, as the example shows.
- **Weaker than HKZ.** A [HKZ-reduced](/hkz-reduction/) basis is deep-reduced for every $\delta \le 1$, since $b_i^*$ is a shortest vector of the projected lattice and $\pi_i(b_k)$ is a nonzero vector of it.
- **Exact and deterministic.** In exact arithmetic the output is a function of the input and $\delta$.
- **Insertion order matters.** The implementation inserts at the first position $i$ that qualifies; other rules, such as the position of largest gain, give different outputs.

## Variants and improvements

- **Depth-restricted deep LLL.** Insert only at the first $\eta$ positions or within $\eta$ positions of $k$; Schnorr and Euchner used this form for subset sum lattices.
- **PotLLL.** Fontein, Schneider and Wagner (2014) insert where the potential $\prod_j D_j$ decreases the most and only when it decreases by the factor $\delta$; this is polynomial time and keeps most of the practical gain.
- **Deep-BKZ.** Running deep LLL instead of LLL inside [BKZ](/bkz-algorithm/) tours, studied by Yamaguchi and Yasuda, improves the output of small block sizes.
- **Floating point.** Practical versions keep the Gram-Schmidt data in floating point, as in Schnorr and Euchner's paper and in the $L^2$ algorithm.

## When to use it

- When LLL is not strong enough but BKZ is too slow, in moderate dimension, for example as a stronger preprocessing step before enumeration.
- In knapsack and subset sum attacks, where Schnorr and Euchner first used it.
- Prefer PotLLL or restricted depth when a running time guarantee matters, and BKZ when strong reduction in high dimension is the goal.

## Pitfalls

- **Unbounded running time.** Unrestricted deep insertion can be slow in high dimension; restrict the depth or use PotLLL.
- **Stale Gram-Schmidt data.** After an insertion, the Gram-Schmidt vectors from position $i$ on change; reuse old values and the test at L6 is wrong.
- **Wrong reset of $k$.** After inserting at position $i$, continue at $\max(i, 2)$, not at $k - 1$; otherwise the new vector is never checked against its predecessors.
- **Forgetting size reduction.** The deep condition is tested on the size-reduced $b_k$; testing before size reduction compares the wrong projections.

## Implementations

## History

Claus-Peter Schnorr and Martin Euchner introduced LLL with deep insertions in 1994, in the same paper as floating-point LLL, BKZ and the zigzag enumeration that bears their names, and used it to solve subset sum problems of a size out of reach before. They observed that unrestricted deep insertion could be slow and proposed a bounded depth. Gama and Nguyen's experiments of 2008 placed it between LLL and BKZ in practice, and Fontein, Schneider and Wagner's PotLLL of 2014 gave the first polynomial-time variant with comparable quality.

## References
