---
tag: GXQF52
kind: algorithm
slug: blelloch-scan
name: Blelloch scan
aliases:
- work-efficient scan
- up-sweep down-sweep scan
- tree scan
area: parallel/parallel-primitives
level: core
summary: Work-efficient parallel scan using an up-sweep and a down-sweep over a balanced tree.
solves: [all-prefix-sums]
model: work-span-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: O(n)}
properties: {deterministic: true}
prereqs: [all-prefix-sums, parallel-reduce, work-span-model]
see_also: [hillis-steele-scan, parallel-prefix, brent-kung-adder, segmented-scan, parallel-pack, decoupled-look-back-scan, work-efficiency, brent-theorem]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.2, Implementation (the up-sweep in Figure 1.2, the down-sweep in Figure 1.4, Theorem 1.1, and the time on p processors)
  - paper: doi:10.1109/12.42122
    title: Guy E. Blelloch, Scans as primitive parallel operations, IEEE Transactions on Computers 38(11), 1526 to 1538, 1989
    locator: Section III-A, Tree Scan
  - book: isbn:9780321515261
    title: Mark Harris, Shubhabrata Sengupta and John D. Owens, Parallel Prefix Sum (Scan) with CUDA, Chapter 39 of Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007
    locator: Section 39.2.2, A Work-Efficient Parallel Scan, and Section 39.2.3, Avoiding Bank Conflicts
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Section 2.1, Balanced trees (the prefix-sums algorithm on a balanced binary tree)
---

The Blelloch scan computes the exclusive [all-prefix-sums](/all-prefix-sums/) of an array with $\Theta(n)$ work and $\Theta(\log n)$ span. It lays a balanced binary tree over the array. An up-sweep, which is a [parallel reduce](/parallel-reduce/), stores the sum of each left subtree. A down-sweep then sends to each node the sum of everything to its left. For $n$ a power of two it does exactly $2(n - 1)$ combines in $2 \lg n$ rounds, so unlike the [Hillis-Steele scan](/hillis-steele-scan/) it is [work-efficient](/work-efficiency/).

## In plain words

Think of a company with a manager tree. Each worker has a number, and each worker wants the total of all workers to their left. First, the totals go up: each manager adds the totals of the two teams below, and remembers the total of the left team. Then the answers come down. The top manager tells the left team "nothing comes before you" and tells the right team "the left team comes before you, so start from its total". Every manager does the same with what it was told: the left team gets the same starting value, and the right team gets that value plus the left team's total.

Each manager adds once on the way up and once on the way down, so the total work is about twice that of one person going down the row.

## The problem

The input is an array $A[0 \ldots n-1]$ over a set $S$, an [associative operator](/associative-operator/) $\oplus$ on $S$, and its identity $e$. The output is the exclusive scan $x$ with $x[0] = e$ and $x[j] = A[0] \oplus \cdots \oplus A[j-1]$, together with the total $A[0] \oplus \cdots \oplus A[n-1]$. The operator need not be commutative. Each application of $\oplus$ costs one unit.

## The algorithm

The array is padded with copies of $e$ to a length $m$ that is a power of two. In round $h$, the cells $i + h - 1$ and $i + 2h - 1$, for $i$ a multiple of $2h$, are the right ends of the left and the right child of a tree node. Each round updates all of its nodes at the same time.

```pseudo id=main
BLELLOCH-SCAN(A, n, ⊕, e)
L1   if n = 0 then return (empty array, e)
L2   m ← 2^⌈lg n⌉; x ← A followed by m − n copies of e
L3   for h ← 1, 2, 4, …, m/2 do                     ▷ up-sweep
L4     for each i ∈ {0, 2h, 4h, …, m − 2h} in parallel do
L5       x[i + 2h − 1] ← x[i + h − 1] ⊕ x[i + 2h − 1]
L6   total ← x[m − 1]; x[m − 1] ← e
L7   for h ← m/2, m/4, …, 1 do                      ▷ down-sweep
L8     for each i ∈ {0, 2h, 4h, …, m − 2h} in parallel do
L9       t ← x[i + h − 1]                           ▷ sum of the left child
L10      x[i + h − 1] ← x[i + 2h − 1]               ▷ left child: same as parent
L11      x[i + 2h − 1] ← x[i + 2h − 1] ⊕ t          ▷ right child: parent ⊕ left
L12  return (x[0 .. n − 1], total)
```

The up-sweep is the level-by-level form of the [parallel reduce](/parallel-reduce/), written in place so that each left subtree sum stays in the array. Line L11 puts the parent value on the left because it covers the items before those of the left child.

## Example

Scan $A = [3, 1, 7, 0, 4, 1, 6, 3]$ with $+$, so $m = n = 8$ and $e = 0$.

| step | $x$ |
|---|---|
| input | 3, 1, 7, 0, 4, 1, 6, 3 |
| up, $h = 1$ | 3, **4**, 7, **7**, 4, **5**, 6, **9** |
| up, $h = 2$ | 3, 4, 7, **11**, 4, 5, 6, **14** |
| up, $h = 4$ | 3, 4, 7, 11, 4, 5, 6, **25** |
| clear the root (total 25) | 3, 4, 7, 11, 4, 5, 6, **0** |
| down, $h = 4$ | 3, 4, 7, **0**, 4, 5, 6, **11** |
| down, $h = 2$ | 3, **0**, 7, **4**, 4, **11**, 6, **16** |
| down, $h = 1$ | **0**, **3**, **4**, **11**, **11**, **15**, **16**, **22** |

The output is $[0, 3, 4, 11, 11, 15, 16, 22]$ with total 25, after $7 + 7 = 14$ combines in 6 rounds. In the last round, the pair at cells 4 and 5 had the parent value 11 (the sum of the first four items) and the left sum 4: cell 4 gets 11 and cell 5 gets $11 + 4 = 15$.

## Correctness

The up-sweep leaves in each cell the sum of the highest tree node that ends at that cell, as in a reduce. The down-sweep keeps this invariant, which is Theorem 1.1 of Blelloch: before the round for height $h$, the right end of each node of that height holds the sum of all items before the node. Line L10 gives the left child the same value, which is right because the left child starts where the parent starts. Line L11 gives the right child the parent value followed by the sum of the left child, which is the sum of everything before the right child. At the leaves, this is the exclusive scan. The full proof, with the exact counts, is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the work $W$, and the field `depth` is the span $S$, both counted in applications of $\oplus$. Let $K = \lceil \lg n \rceil$ and $m = 2^K < 2n$.

**Work.** Each sweep does one combine for each of the $m - 1$ inner nodes of the tree, so $W = 2(m - 1)$. For $n$ a power of two this is $2n - 2$, and in all cases it is less than $4n$. A sequential exclusive scan needs $n - 1$ combines, so the factor is at most 4.

**Span.** There are $K$ rounds in each sweep, so $2K = 2 \lceil \lg n \rceil$ rounds. The longest chain of dependent combines has $2K - 1$ combines, because the total computed by the last up-sweep round is not used by the down-sweep. The [Hillis-Steele scan](/hillis-steele-scan/) has half as many rounds.

**Time on $p$ processors.** Each round updates distinct cells, so it runs on an EREW PRAM. With $p$ processors, Blelloch's blocked version scans each block of $n/p$ items, runs the tree on the $p$ block sums, and adds the results back, in $2(\lceil n/p \rceil + \lceil \lg p \rceil)$ steps. [Brent's theorem](/brent-theorem/) gives the same $O(n/p + \log n)$ for the tree version.

**In fork-join code.** If each round is a [parallel for loop](/parallel-for/), the span is $\Theta(\log^2 n)$. A recursive version, with one spawn for each subtree in both sweeps, has span $\Theta(\log n)$.

**Space.** The algorithm works in place on the padded array. When $n$ is a power of two and the input may be overwritten, the extra space is $O(1)$; otherwise the padded copy takes $O(n)$.

| measure | Blelloch | [Hillis-Steele](/hillis-steele-scan/) | sequential |
|---|---|---|---|
| combines, $n = 2^K$ | $2n - 2$ | $n \lg n - n + 1$ | $n - 1$ |
| rounds | $2 \lceil \lg n \rceil$ | $\lceil \lg n \rceil$ | $n - 1$ |
| output | exclusive and total | inclusive | either |
| identity needed | yes | no | no |

## Properties

- **Exclusive.** The output at $j$ excludes $A[j]$. The inclusive scan is $x[j] \oplus A[j]$ for each $j$, one more parallel step, or the output shifted left with the total appended.
- **Work-efficient.** The work is within a factor 2 of the sequential scan for powers of two, and within 4 in general.
- **Order-keeping.** With line L11 as written, the operator need not be commutative.
- **Deterministic.** The tree is fixed by $n$, so floating-point results do not change from run to run. They differ from the results of a sequential loop, because the bracketing differs.
- **Regular access.** Each round reads and writes cells at fixed strides, which suits SIMD and GPU hardware, apart from the bank conflicts noted below.

## Variants and improvements

- **Recursive form.** Pair up adjacent items, scan the $n/2$ pair sums recursively, then fill in the odd positions. This has the same work and span, works for any $n$ without padding, and is the [Ladner-Fischer and Brent-Kung](/parallel-prefix/) construction in software.
- **Blocked scan.** For $n \gg p$, each processor scans its block sequentially, a small scan runs on the block totals, and each processor adds its offset. The work is $n + O(p)$ combines and two passes over the data. This is the form used on multicore machines.
- **GPU scan.** A GPU block runs the up-sweep and the down-sweep in shared memory, then scans the block sums in a second level. Harris, Sengupta and Owens pad the shared-memory indices to avoid bank conflicts. Single-pass GPU scans, such as the [decoupled look-back scan](/decoupled-look-back-scan/), replace the second level.
- **Segmented scan.** The same code with the segmented operator computes a scan that restarts at each segment start. See [segmented scan](/segmented-scan/).
- **The circuit view.** The dependence graph of the two sweeps is the [Brent-Kung](/brent-kung-adder/) prefix circuit. For the inclusive scan on $n = 2^K \ge 4$ items, that circuit has size $2n - 2 - K$ and depth $2K - 2$.

## When to use it

Use the Blelloch scan, or the blocked form of it, when the input is much larger than the number of processors, so the work matters more than the number of rounds. This covers multicore scans and the block level of GPU scans. Use it also when the exclusive scan and the total are both needed, as in [parallel pack](/parallel-pack/) and radix sort, where the total is the size of the output. When processors are as many as items, as in one GPU warp, the [Hillis-Steele scan](/hillis-steele-scan/) has fewer rounds.

## Pitfalls

- **The order on line L11.** Some published code writes the right child as $t \oplus x[i + 2h - 1]$, that is, the left sum before the parent value. This is correct for $+$ and $\max$, but for string concatenation on "abcd" it gives "", "a", "ab", "cab". The tests check this case.
- **A missing or wrong identity.** The root and the padding need the identity of $\oplus$: $0$ for $+$, $-\infty$ for $\max$, the empty string for concatenation, the identity matrix for matrix products.
- **Forgetting the total.** Line L6 overwrites the total. Save it first if the caller needs it.
- **Padding.** Without padding, $n$ that is not a power of two leaves cells out of range. Either pad with $e$ or use the recursive form.
- **Bank conflicts on a GPU.** The strides $h$ are powers of two, so in shared memory many threads of a warp hit the same bank. Padding the index by $\lfloor i / 32 \rfloor$, or a similar shift, removes most conflicts.

## Implementations

## History

The two-sweep tree method is the software form of prefix circuits from computer arithmetic, in particular the circuit of Brent and Kung (1982). Blelloch made the scan a primitive operation of parallel programming. In "Scans as primitive parallel operations" (1989) and in "Prefix Sums and Their Applications" (1990) he described the up-sweep and the down-sweep on a balanced tree, proved that the down-sweep leaves at each vertex the sum of the leaves before it, and gave its time on $p$ processors. Harris, Sengupta and Owens (2007) described the method for GPUs in GPU Gems 3 and credit it to Blelloch. In the GPU literature it is often called the Blelloch scan.

## References
