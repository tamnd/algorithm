---
tag: SDH9BZ
kind: algorithm
slug: estrin-scheme
name: Estrin's scheme
aliases:
- Estrin's method
- Estrin's algorithm
area: algebra/polynomial-arithmetic
level: advanced
summary: Evaluates a polynomial by a balanced tree of pairwise combinations, shortening the critical path on parallel hardware.
solves: [polynomial-evaluation]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the polynomial}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
  depth: {worst: Θ(log n)}
  ring_operations: {worst: 2n + log2(n + 1), best: 2n + log2(n + 1)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1960
  people: [Gerald Estrin]
  note: Estrin described the scheme in 1960 in his paper on the fixed plus variable structure computer at UCLA, as a way to evaluate polynomials with several arithmetic units at once.
prereqs: [horner-rule, polynomial, dense-polynomial-representation]
see_also: [polynomial-evaluation, paterson-stockmeyer-algorithm, horners-rule-optimality, fused-multiply-add, multipoint-evaluation, fast-multipoint-evaluation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials (Estrin's method for parallel evaluation, and the rule of Horner)
  - paper: doi:10.1145/1460361.1460365
    title: Gerald Estrin, Organization of computer systems, the fixed plus variable structure computer, Papers presented at the Western Joint IRE-AIEE-ACM Computer Conference, 1960, 33-40
    locator: the evaluation of polynomials with several arithmetic units
---

Estrin's scheme evaluates a polynomial by grouping its coefficients in pairs, then pairs of pairs, and so on, like a balanced binary tree. It uses about as many operations as [Horner's rule](/horner-rule/), $n$ additions and $n + \lceil \log_2 (n + 1) \rceil - 1$ multiplications for degree $n$, but the operations of one round do not depend on each other. So with enough parallel units, or with a processor that can run several independent multiply-adds at a time, the critical path has $2 \lceil \log_2(n + 1) \rceil$ operations instead of the $2n$ of Horner's rule.

Notation: $R$ is a commutative ring, $f = \sum_{k=0}^{n} a_k x^k \in R[x]$ is a list of coefficients with the constant term first, and the point $x$ is an element of $R$. Costs count ring operations of $R$ in the algebraic complexity model. The depth is the length of the longest chain of operations in which each needs the result of the one before; it is the time with unlimited parallel units.

## In plain words

Horner's rule works from the top coefficient down, and each step needs the answer of the step before. So it cannot go faster with more hands. Estrin's scheme first joins the coefficients in pairs, each pair into a small linear piece. All these joins can happen at the same time. It then joins the pieces in pairs, using the square of the point, and again all these joins can happen at the same time. After each round the number of pieces is halved, so a polynomial of degree one thousand needs only ten rounds. The total work is about the same as for Horner's rule.

## The problem

**Input:** a list $a = [a_0, \ldots, a_n]$ of elements of $R$ and a point $x \in R$.

**Output:** $f(x) = \sum_{k=0}^{n} a_k x^k$.

This is [polynomial evaluation](/polynomial-evaluation/) at one point. Estrin's scheme answers it with a different order of the same operations, chosen for parallel hardware.

## The algorithm

The identity behind the scheme splits the coefficient list into the even and odd positions after pairing: with $c_i = a_{2i} + a_{2i+1} x$,

$$f(x) = \sum_{i} c_i\, (x^2)^i,$$

which is a polynomial of half the length at the point $x^2$. Repeating with $x^4, x^8, \ldots$ gives one value after $\lceil \log_2(n + 1) \rceil$ rounds.

```pseudo id=main
ESTRIN(a_0, ..., a_n; x)
L1  c ← [a_0, ..., a_n]
L2  p ← x                                     ▷ p = x^(2^k) in round k
L3  while c has more than one entry do
L4      c' ← [c_{2i} + c_{2i+1} · p  for 0 ≤ i < ⌊len(c)/2⌋]   ▷ independent
L5      if len(c) is odd then append the last entry of c to c'
L6      c ← c'
L7      if c has more than one entry then p ← p · p
L8  return c_0
```

The products and additions of line L4 can all run at the same time, and the squaring of line L7 can run in parallel with them, since it only needs the old $p$. On a processor with a fused multiply-add instruction, each entry of line L4 is one instruction.

## Example

Evaluate $f = 1 + 2x + 3x^2 + 4x^3 + 5x^4 + 6x^5 + 7x^6 + 8x^7$ at $x = 2$ over $\mathbb{Z}$.

| round | $p$ | list $c$ after the round |
|---|---|---|
| start | | $[1, 2, 3, 4, 5, 6, 7, 8]$ |
| 1 | $2$ | $[1 + 2 \cdot 2, 3 + 4 \cdot 2, 5 + 6 \cdot 2, 7 + 8 \cdot 2] = [5, 11, 17, 23]$ |
| 2 | $4$ | $[5 + 11 \cdot 4, 17 + 23 \cdot 4] = [49, 109]$ |
| 3 | $16$ | $[49 + 109 \cdot 16] = [1793]$ |

So $f(2) = 1793$, which agrees with $\sum_{k=0}^{7} (k + 1) 2^k = 7 \cdot 2^8 + 1$. The scheme used 7 additions and 9 multiplications (7 in the rounds and 2 squarings), and the longest chain has 6 operations. Horner's rule uses 7 additions and 7 multiplications, in a chain of 14. A script checked the table and the counts.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The invariant is that at the start of round $k$, with $p = x^{2^k}$, the value $\sum_i c_i p^i$ equals $f(x)$. It holds at the start with $p = x$ and $c = a$. One round maps it to itself, because $c_{2i} p^{2i} + c_{2i+1} p^{2i+1} = (c_{2i} + c_{2i+1} p)(p^2)^i$, and an unpaired last entry $c_{2i}$ has the same weight $(p^2)^i$. Each round with more than one entry shortens the list, so the loop ends with one entry, which is then $f(x)$.

## Complexity

All bounds are proved and count ring operations of $R$. Let $L = \lceil \log_2(n + 1) \rceil$ be the number of rounds.

- **Additions.** Each addition of line L4 joins two entries into one, and the list goes from $n + 1$ entries to $1$, so there are exactly $n$ additions.
- **Multiplications.** One per addition in line L4, so $n$, plus $L - 1$ squarings in line L7 for $n \ge 1$: $n + L - 1$ in total. With the additions, at most $2n + \log_2(n + 1)$ ring operations.
- **Depth.** Each round adds one multiplication and one addition to the longest chain, and the squarings run alongside, so the depth is at most $2L$. Horner's rule has depth $2n$.
- **Space.** $\Theta(n)$ ring elements for the list $c$, against $\Theta(1)$ for Horner's rule. A version that works in place on the coefficient array uses $\Theta(1)$ extra space.

**Lower bound on depth.** Every straight-line program that computes $f(x)$ for a polynomial of degree $n$ in an indeterminate $x$ has multiplicative depth at least $\lceil \log_2 n \rceil$, since a product of two expressions of degree at most $d$ has degree at most $2d$, and additions do not raise the degree. So Estrin's depth is optimal up to a constant factor.

**In practice (observed).** On processors that can start a new fused multiply-add every cycle but take several cycles to finish one, Horner's rule waits on each result, while Estrin's scheme keeps the pipeline full. For the moderate degrees of the polynomial approximations in mathematical libraries, Estrin's scheme or a mix of Estrin and Horner is often faster. For very high degrees the gain is limited by the number of units and by the memory for the list. These effects depend on the processor.

## Properties

- **Same result in exact arithmetic.** Over $\mathbb{Z}$, $\mathbb{Z}/m\mathbb{Z}$ or $\mathbb{Q}$, the value is the same as Horner's rule.
- **Floating point.** The rounding errors depend on the order of the operations, so they differ from those of Horner's rule; neither method is more accurate for every input.
- **Parallel.** All operations in one round are independent.
- **Not online.** Horner's rule can consume coefficients from the top one at a time; Estrin's scheme needs all of them before the first round ends.
- **Power of two lengths are the best case.** When $n + 1$ is a power of two, no entry is carried up and every round is full.

## Variants and improvements

- **Fixed blocks.** Split the coefficients into blocks of $b$, evaluate each block by Horner's rule, and combine the blocks with $x^b$ by Estrin's scheme or by Horner's rule. This balances work and depth for a fixed number of units.
- **Second order Horner.** Evaluate the even and odd parts separately by Horner's rule in $x^2$ and combine: $f(x) = E(x^2) + x\, O(x^2)$. This halves the depth with only one extra multiplication, and is the first step of Estrin's scheme.
- **Many points.** For one polynomial at many points, the [subproduct tree](/subproduct-tree/) method of [fast multipoint evaluation](/fast-multipoint-evaluation/) uses fewer operations in total; Estrin's scheme is for one point.
- **Few nonscalar products.** When multiplications by coefficients are cheap and products of two expressions in $x$ are expensive, as for matrices, use the [Paterson-Stockmeyer algorithm](/paterson-stockmeyer-algorithm/), which uses about $2\sqrt{n}$ such products.
- **Preconditioning.** If the polynomial is fixed and is evaluated many times, its coefficients can be transformed once so that each evaluation uses about $n/2$ multiplications (Knuth, Section 4.6.4).

## When to use it

Use Estrin's scheme for one polynomial of moderate degree at one point, on hardware that can run several independent multiplications at once: SIMD units, deep floating point pipelines, GPUs, or circuits. Use Horner's rule when the hardware runs one operation at a time, when space is tight, or when the coefficients arrive one at a time. For many points use fast multipoint evaluation, and for matrix arguments use Paterson-Stockmeyer.

## Pitfalls

- **Forgetting the unpaired entry.** When the list has odd length, its last entry must be carried to the next round unchanged. Treating it as paired with a zero is correct but wastes a multiplication; dropping it is wrong.
- **One squaring too many.** The square $p^2$ is not needed after the last round. Computing it anyway costs one multiplication and can overflow with fixed-size numbers.
- **Expecting a speedup on a sequential machine.** With one unit and no pipeline, Estrin's scheme does a few more multiplications than Horner's rule and is slower.
- **Large powers of $x$.** In floating point, $x^{2^k}$ can overflow or underflow for large $|x|$ or small $|x|$ even when $f(x)$ is moderate. Horner's rule never forms these powers.

## Implementations

## History

Gerald Estrin described the scheme in 1960, in his paper on the fixed plus variable structure computer at UCLA, as an example of how several arithmetic units can work on one problem. Knuth presents it in Section 4.6.4 next to Horner's rule as a method for parallel evaluation. The scheme and its mixes with Horner's rule are used in the polynomial kernels of mathematical libraries for processors with wide SIMD units and fused multiply-add.

## References
