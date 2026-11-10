---
tag: FB12GR
kind: algorithm
slug: scatter-and-gather
name: Scatter and gather
aliases:
- permute
- indexed write
- indexed read
- gather and scatter
area: parallel/parallel-primitives
level: intro
summary: Basic data-movement primitives that write or read elements at computed indices.
model: crew-pram
complexity:
  vars: {n: "the number of indices, with one processor for each"}
  time: {worst: Θ(n)}
  depth: {worst: Θ(1)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
prereqs: [pram-model, work-span-model]
see_also: [parallel-pack, compaction, permutation, crcw-pram, erew-pram, parallel-histogram, parallel-radix-sort, gpu-memory-hierarchy]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.3, Line-of-Sight and Radix-Sort (the split operation, which computes new indices with two scans and moves the items with permute, an exclusive write; Figure 1.9)
  - book: isbn:9780262023139
    title: Guy E. Blelloch, Vector Models for Data-Parallel Computing, MIT Press, 1990
    locator: the scan vector model and its primitive instructions, which include the permute and the indexed operations on vectors
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 1 (the PRAM model, the EREW, CREW and CRCW variants, and the common, arbitrary and priority rules for concurrent writes)
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 6, Data Reorganization (gather, scatter, the collisions of a scatter and their rules, and the conversion of a scatter into a gather)
  - paper: doi:10.1145/800133.804339
    title: Steven Fortune and James Wyllie, Parallelism in random access machines, Proceedings of the 10th ACM Symposium on Theory of Computing, 114 to 118, 1978
    locator: the definition of the PRAM, with processors that share one memory and run in synchronous steps
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1116 to 1127, 1988
    locator: the bound for permuting in external memory, which is the minimum of n and the sorting bound
---

Gather and scatter are the two basic ways to move data by computed indices. A **gather** reads $B[i] = A[I[i]]$ for every $i$; a **scatter** writes $C[I[i]] = A[i]$ for every $i$; and a **permute** is a scatter whose index array is a permutation. On a [PRAM](/pram-model/) with one processor for each index, each is one step: $\Theta(1)$ time and $\Theta(n)$ work. The cost model matters when indices repeat. A gather with repeated indices needs concurrent reads ([CREW](/crew-pram/)), and a scatter with repeated indices needs concurrent writes ([CRCW](/crcw-pram/)) together with a rule that says which value a cell gets. With distinct indices both run on the [EREW PRAM](/erew-pram/). Most data-parallel algorithms, such as [pack](/parallel-pack/), split and radix sort, end with a scatter to positions computed by a scan.

## In plain words

A gather is a list of requests: "give me the item in box 7, the item in box 2, and again box 7". Each request is answered on its own, so all requests can be served at once. Several requests for the same box are easy if the box can be read by many people at once.

A scatter is a list of deliveries: "put this item in box 4, that one in box 0". If every delivery goes to a different box, all deliveries can be made at once. If two deliveries go to the same box, the rules must say what happens: only equal items may arrive, one item wins, the first in line wins, or the items are added together.

A permute is a scatter in which every box gets exactly one item, so it only changes the order of the items.

## The problem

The input is an array $A[0 \ldots n-1]$ and an index array $I[0 \ldots n-1]$. A gather returns $B$ with $B[i] = A[I[i]]$. A scatter takes an output array $C[0 \ldots m-1]$ with $0 \le I[i] < m$ and returns $C$ with $C[I[i]] = A[i]$ for every $i$; cells that no index names keep their old values. If $I$ is a [permutation](/permutation/) of $0, \ldots, n-1$, the scatter is a permute. Costs are given on a synchronous PRAM, in which every processor reads before any processor writes in a step, and on the [work-span model](/work-span-model/).

## The algorithm

```pseudo id=main
GATHER(A, I, n)
L1  for i ← 0 to n − 1 in parallel do
L2    B[i] ← A[I[i]]
L3  return B

SCATTER(A, I, C, n)
L4  for i ← 0 to n − 1 in parallel do
L5    C[I[i]] ← A[i]          ▷ repeated indices need a CRCW rule
L6  return C
```

Each loop is one PRAM step with processor $i$ doing iteration $i$. The direction of the index is the only difference: a gather uses $I$ to say where to read, and a scatter uses $I$ to say where to write.

**Rules for concurrent writes.** When indices repeat, line L5 has several writers for one cell. The CRCW PRAM has the following common rules:

| Rule | Value that a cell with writers $W_j$ gets |
|---|---|
| common | the shared value; all writers must write the same value |
| arbitrary | the value of one writer, chosen by the machine; the program must be correct for every choice |
| priority | the value of the writer with the smallest processor number |
| combining | the combination of all values under an associative and commutative operator, such as $+$ or $\max$ |

The implementation also has an exclusive rule, which reports an error at the first conflict, as a check that a step is valid on an EREW or CREW PRAM.

## Example

Let $A = [a, b, c, d]$.

- **Gather** with $I = [2, 0, 0, 3]$ gives $[c, a, a, d]$. Cell 0 is read twice in one step, so this needs CREW.
- **Permute** with $P = [2, 0, 3, 1]$ writes $a$ to cell 2, $b$ to cell 0, $c$ to cell 3 and $d$ to cell 1, so the result is $[b, d, a, c]$. Gathering that result with $P$ gives $[a, b, c, d]$ back.
- **Scatter** of $[5, 6, 7]$ with $I = [1, 1, 3]$ into $[0, 0, 0, 0]$: cells 1 and 3 are written, and cell 1 has two writers. Priority gives $[0, 5, 0, 7]$; arbitrary gives 5 or 6 in cell 1; common is not allowed, because $5 \ne 6$; combining with $+$ gives $[0, 11, 0, 7]$.

A scatter reads only old values. With $I = [1, 2, 3, 0]$ and the output equal to the input $[1, 2, 3, 4]$, one scatter step gives the rotation $[4, 1, 2, 3]$, because every processor reads its item before any item is written.

## Correctness

A gather writes each cell $B[i]$ once, with $A[I[i]]$. In a scatter with distinct indices, each output cell has at most one writer, so the step has no conflict, no CRCW rule is applied, and the result equals that of a serial loop in any order. With a permutation every cell is written exactly once, and gathering with the same permutation undoes it. With repeated indices, the priority rule equals the serial loop from the last index down to the first, and the combining rule with an associative and commutative operator equals the serial loop in any order. The tests check each of these against list comprehensions and loops. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the work, and the field `depth` is the time with $n$ processors on a CREW PRAM.

**PRAM.** Each operation is one step with $n$ processors: $\Theta(1)$ time and $\Theta(n)$ work, which matches the $\Theta(n)$ of the serial loop. The variant of the PRAM depends on the indices:

- distinct indices, so a gather of a permutation, a scatter of distinct indices, and a permute: EREW;
- a gather with repeated indices: CREW;
- a scatter with repeated indices: CRCW, with a write rule.

On an EREW PRAM, a gather with repeats takes $\Omega(\log n)$ time in the worst case, because when all processors read one cell, the number of processors that know its value can at most double in each step. A gather or a priority scatter with repeats can be done on the EREW PRAM in $O(\log n)$ time by sorting the requests by index and copying within each group of equal indices with a [segmented scan](/segmented-scan/).

**Work-span.** In the fork-join model, the parallel loop is a balanced tree of spawns, so each operation has work $\Theta(n)$ and span $\Theta(\log n)$, as for a [parallel map](/parallel-map/).

**Memory.** Real machines charge for where the indices point. A gather or scatter with random indices touches a different cache line or memory segment for each item, while a copy with $I[i] = i$ touches $n / B$ lines of $B$ items. In the external-memory model, permuting $n$ items takes $\Theta(\min(n, \frac{n}{B} \log_{M/B} \frac{n}{B}))$ block transfers (Aggarwal and Vitter 1988), which is the sorting bound for most sizes. So a permute is a cheap step on a PRAM but can cost as much as a sort in practice.

## Properties

- **Gather and scatter are inverse for permutations.** A scatter by $P$ equals a gather by $P^{-1}$, and the inverse $P^{-1}$ is one scatter of the values $0, \ldots, n-1$ by $P$.
- **A gather is always well defined.** Its writes go to distinct cells, so it never has a write conflict. This makes it the safer of the two, and libraries often turn a scatter into a gather when the inverse indices are known.
- **One step.** All reads are of old values, so a scatter can move items inside one array, as in the rotation example, only with a second buffer or the synchronous semantics.
- **Deterministic** with distinct indices, or with the common, priority or combining rule. The arbitrary rule makes the result depend on the machine.

## Variants and improvements

- **Permute.** A scatter with a permutation, which is a primitive of Blelloch's scan vector model and of NESL. With distinct indices it needs only exclusive writes.
- **Combining scatter.** A scatter with $+$ is a [histogram](/parallel-histogram/) of the values by index. On GPUs and multicores it is done with atomic adds, which are a hardware form of the combining rule; see [fetch-and-add](/fetch-and-add/).
- **Masked forms.** A scatter or gather with a flag for each item does only the flagged moves. The [pack](/parallel-pack/) is a masked scatter to positions computed by an exclusive scan of the flags.
- **Split.** Blelloch's split moves the items with flag 0 to the front and those with flag 1 to the back, both in order, with two scans and one permute. It is the step of the split radix sort.
- **Hardware instructions.** Vector processors and SIMD instruction sets have indexed loads and stores. For example, the x86 AVX2 extension has gather instructions, and AVX-512 adds scatter instructions.

## When to use it

Use a gather to read data through an index: a table lookup, the vector entries $x_j$ in a [sparse matrix-vector product](/sparse-matrix-vector-multiplication/), or the values of a permutation known in its inverse form. Use a scatter or permute to put items in places computed earlier, which is the last step of [pack](/parallel-pack/), split, [radix sort](/parallel-radix-sort/) and [counting sort](/counting-sort/). Prefer a gather when both are possible, because it needs no write rule. If the indices are not known to be distinct, choose the write rule on purpose, or sort the items by index first.

## Pitfalls

- **Write conflicts.** A scatter with repeated indices on a machine with no rule is a [race condition](/race-condition/): the result depends on timing. Check that the indices are distinct, or use atomic operations.
- **Gather and scatter confused.** PERMUTE$(A, P)$ puts $A[i]$ at position $P[i]$, while GATHER$(A, P)$ puts $A[P[i]]$ at position $i$. These are inverse to each other, and using one for the other gives the inverse permutation. The example above shows both.
- **In-place scatter.** Writing into the input array with a loop that is not synchronous can read a value that another iteration has already overwritten. Use a separate output array.
- **Unwritten cells.** A scatter with fewer indices than cells leaves the other cells unchanged, so the output must be set to a known value first.
- **Indices out of range.** Computed indices that leave the array are a common bug in scatters, and they write over other data without an error in languages without bounds checks.
- **Cost of random access.** On a GPU, the threads of a warp that gather from scattered addresses cannot share memory transactions, so the step can be many times slower than a copy; see the [GPU memory hierarchy](/gpu-memory-hierarchy/).

## Implementations

## History

Fortune and Wyllie (1978) defined the PRAM. The variants by read and write access, and the rules for concurrent writes, came in the work of the late 1970s and the 1980s, which JaJa (1992) summarizes. Vector computers had indexed load and store instructions for sparse data. Blelloch (1989, 1990) made permute, together with scan, a primitive of the scan vector model, and expressed split, pack and radix sort with scans followed by a permute. Aggarwal and Vitter (1988) showed that permuting is as hard as sorting in external memory for most parameters. McCool, Robison and Reinders (2012) present gather, scatter and pack as the data reorganization patterns of structured parallel programming.

## References
