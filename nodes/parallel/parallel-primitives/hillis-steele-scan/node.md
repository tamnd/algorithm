---
tag: H3KT7W
kind: algorithm
slug: hillis-steele-scan
name: Hillis-Steele scan
aliases:
- simple parallel scan
- naive parallel scan
- recursive doubling scan
area: parallel/parallel-primitives
level: core
summary: Logarithmic-depth scan that does n log n work.
solves: [all-prefix-sums]
model: work-span-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, in_place: false}
prereqs: [all-prefix-sums, work-span-model]
see_also: [blelloch-scan, parallel-prefix, kogge-stone-adder, pointer-jumping, work-efficiency, erew-pram, warp-level-primitives, parallel-reduce]
sources:
  - paper: doi:10.1145/7902.7903
    title: W. Daniel Hillis and Guy L. Steele Jr., Data parallel algorithms, Communications of the ACM 29(12), 1170 to 1183, 1986
    locator: the section on computing all partial sums of an array in log n steps by doubling the distance in each step
  - paper: doi:10.1109/TC.1973.5009159
    title: Peter M. Kogge and Harold S. Stone, A parallel algorithm for the efficient solution of a general class of recurrence equations, IEEE Transactions on Computers C-22(8), 786 to 793, 1973
    locator: the recursive doubling method
  - book: isbn:9780321515261
    title: Mark Harris, Shubhabrata Sengupta and John D. Owens, Parallel Prefix Sum (Scan) with CUDA, Chapter 39 of Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007
    locator: Section 39.2.1, A Naive Parallel Scan (the algorithm, its O(n log n) additions, and the double buffer)
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990
    locator: Section 1.1 (the definition of scan) and Section 1.2 (the work-efficient tree method that this scan is compared with)
---

The Hillis-Steele scan computes all prefix sums of an array in $\lceil \lg n \rceil$ rounds. In round $k$, every position $i \ge 2^k$ replaces its value $x[i]$ with $x[i - 2^k] \oplus x[i]$, all at the same time. After the last round, $x[i] = a_0 \oplus a_1 \oplus \cdots \oplus a_i$. The span is optimal, but the work is $\Theta(n \log n)$, against $n - 1$ for a sequential loop, so the scan is not [work-efficient](/work-efficiency/). It is the right choice when processors are many and idle, as in one GPU warp.

## In plain words

A row of people each hold a number, and each wants the total of their own number and all numbers to their left. In the first step, each person adds the number of the neighbour one place to the left. In the second step, each person adds the number now held by the person two places to the left. Then four places, then eight, and so on. Each step doubles the length of the stretch that each person has added up, so after about twenty steps a row of a million people is done.

Everybody works in every step, even though many of the additions repeat work that someone else has done. So the method is fast but does much more work than one person going down the row.

## The problem

The input is an array $A[0 \ldots n-1]$ over a set $S$ and an [associative operator](/associative-operator/) $\oplus$ on $S$. The output is the inclusive scan $x$ with $x[i] = A[0] \oplus \cdots \oplus A[i]$, as defined in [all-prefix-sums](/all-prefix-sums/). The operator need not be commutative, and no identity is needed. Each application of $\oplus$ costs one unit.

## The algorithm

The rounds are synchronous: in each round, all positions read the old array, and only then is the new array written.

```pseudo id=main
HILLIS-STEELE-SCAN(A, n, ⊕)
L1  x ← a copy of A
L2  d ← 1
L3  while d < n do
L4    for i ← 0 to n − 1 in parallel do
L5      if i ≥ d then y[i] ← x[i − d] ⊕ x[i] else y[i] ← x[i]
L6    x ← y                                 ▷ swap the two buffers
L7    d ← 2d
L8  return x
```

The value $x[i - d]$ is on the left of $\oplus$ on line L5 because it covers the items before those of $x[i]$. The second array $y$ is needed: an in-place update in a sequential loop would let a position read a value that was already changed in the same round.

## Example

Scan $A = [3, 1, 7, 0, 4, 1, 6, 3]$ with $+$. Each row shows $x$ after one round.

| round | $d$ | $x$ | combines |
|---|---|---|---|
| input | | 3, 1, 7, 0, 4, 1, 6, 3 | |
| 1 | 1 | 3, 4, 8, 7, 4, 5, 7, 9 | 7 |
| 2 | 2 | 3, 4, 11, 11, 12, 12, 11, 14 | 6 |
| 3 | 4 | 3, 4, 11, 11, 15, 16, 22, 25 | 4 |

The result is the inclusive scan after $3 = \lg 8$ rounds and $17 = 8 \cdot 3 - 8 + 1$ combines. After round 2, each $x[i]$ is the sum of the last four items up to $i$, or of all items up to $i$ if there are fewer than four. For example, $x[5] = 7 + 0 + 4 + 1 = 12$ and $x[2] = 3 + 1 + 7 = 11$. A sequential loop would use only 7 combines.

## Correctness

The invariant is: after $k$ rounds, $x[i] = A[\max(0, i - 2^k + 1)] \oplus \cdots \oplus A[i]$, so each position holds the sum of a window of $2^k$ items that ends at $i$, cut at the left end. In the next round, for $i \ge 2^k$, the window of $x[i - 2^k]$ ends just before the window of $x[i]$ begins, and combining them in this order gives the window of length $2^{k+1}$. For $i < 2^k$, the window already starts at 0. When $2^k \ge n$, every window starts at 0, so $x[i]$ is the full prefix. The full proof, with the exact count of combines, is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the work $W$, and the field `depth` is the span $S$, both counted in applications of $\oplus$. Let $K = \lceil \lg n \rceil$.

**Work.** Round $k$ does $n - 2^k$ combines, so
$$
W(n) = \sum_{k=0}^{K-1} (n - 2^k) = nK - 2^K + 1,
$$
which is $n \lg n - n + 1$ when $n$ is a power of two. This is $\Theta(n \log n)$.

**Span.** There are exactly $K$ rounds, and each adds one combine to every chain, so $S(n) = \lceil \lg n \rceil$. No scan can have a smaller span, because $x[n-1]$ depends on all $n$ items.

**On a PRAM.** With $n$ processors, each round takes $O(1)$ steps on an [EREW PRAM](/erew-pram/): processor $i$ reads $x[i]$, then $x[i - d]$, then writes $y[i]$, and in each substep the addresses are distinct. The time is $O(\log n)$ and the processor-time product is $\Theta(n \log n)$. With $p < n$ processors, [Brent's theorem](/brent-theorem/) gives $O((n \log n)/p + \log n)$, which is worse by a factor of $\log n$ than a work-efficient scan when $p$ is small.

**In fork-join code.** If each round is a [parallel for loop](/parallel-for/), each loop adds $\Theta(\log n)$ span for its spawn tree, so the span becomes $\Theta(\log^2 n)$. The $\Theta(\log n)$ bound is for synchronous rounds, as on a PRAM or a GPU.

**Space.** The second buffer takes $\Theta(n)$ extra space.

| measure | Hillis-Steele | [Blelloch scan](/blelloch-scan/) | sequential |
|---|---|---|---|
| combines | $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ | $2(n - 1)$ for $n = 2^K$ | $n - 1$ |
| rounds | $\lceil \lg n \rceil$ | $2 \lceil \lg n \rceil$ | $n - 1$ |
| output | inclusive | exclusive | either |

## Properties

- **Inclusive.** The output at $i$ includes $A[i]$. For the exclusive scan, shift the result one place to the right and put the identity at position 0.
- **No identity needed.** Positions $i < d$ copy their value, so the operator needs no identity. The [Blelloch scan](/blelloch-scan/) needs one.
- **Order-keeping.** The left operand always covers earlier items, so the operator need not be commutative.
- **Deterministic.** The bracketing is fixed by $n$, so floating-point results are the same on every run.
- **Regular.** Every round does the same simple step at every position, with no tree layout and no padding to a power of two.

## Variants and improvements

- **As a circuit.** The dependence graph of the scan is the prefix circuit of [Kogge and Stone](/kogge-stone-adder/), with depth $\lceil \lg n \rceil$ and fan-out 2 at each gate. The [parallel prefix](/parallel-prefix/) page compares it with the circuits of Sklansky, Brent and Kung, and Ladner and Fischer.
- **Warp scan.** On a GPU, the 32 lanes of a warp run in lockstep and are busy anyway, so the extra work costs nothing. A warp scan is a Hillis-Steele scan with shuffle instructions in 5 rounds. See [warp-level primitives](/warp-level-primitives/).
- **Blocked scan.** With $p$ processors and $n \gg p$, scan each block of $n/p$ items sequentially, run a Hillis-Steele scan on the $p$ block totals, and add each block's offset to its items. The work is $O(n + p \log p)$ and the time is $O(n/p + \log p)$.
- **On a linked list.** The same doubling idea with pointers in place of indices is [pointer jumping](/pointer-jumping/), which ranks a linked list in $O(\log n)$ rounds with $O(n \log n)$ work.

## When to use it

Use the Hillis-Steele scan when the number of processors is at least the number of items, so the extra work uses processors that would otherwise be idle, and when a short, regular loop matters more than the operation count. This is the case for one warp or one small block on a GPU, and for the top level of a blocked scan. For a large array on few processors, use a work-efficient scan such as the [Blelloch scan](/blelloch-scan/).

## Pitfalls

- **Updating in place.** A sequential simulation that writes $x[i]$ in increasing order of $i$ makes later positions read new values. On $[1, 1, 1, 1]$ it gives $[1, 2, 4, 6]$ instead of $[1, 2, 3, 4]$. On a GPU, the same race happens without a barrier between the reads and the writes of a round.
- **Swapped operands.** Writing $x[i] \oplus x[i - d]$ is correct for $+$ and $\max$, but wrong for string concatenation and matrix products.
- **Forgetting the extra work.** For $n = 10^8$, the scan does about 26 times as many combines as a sequential loop. On a machine with 8 cores, it is then about 3 times slower than one core.
- **Off-by-one rounds.** The loop runs while $d < n$. With the test $d \le n$, a power of two $n$ gets one extra round that does nothing but still costs a barrier.

## Implementations

## History

Kogge and Stone (1973) gave the recursive doubling method for first-order recurrences, which computes all prefixes of an associative operator in $\lceil \lg n \rceil$ steps; its circuit form is the Kogge-Stone adder. Hillis and Steele (1986) presented the same algorithm as a basic data-parallel operation for the Connection Machine, with one processor for each item. The GPU literature took the name from them: Harris, Sengupta and Owens (2007) call it the naive parallel scan and contrast it with the work-efficient tree scan of Blelloch.

## References
