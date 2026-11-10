---
tag: H59CZB
kind: problem
slug: all-prefix-sums
name: All-prefix-sums (scan)
aliases:
- scan
- prefix sums
- prefix reduction
- prescan
area: parallel/parallel-primitives
level: intro
summary: Compute every prefix of a sequence under an associative operator.
prereqs: [associative-operator, prefix-sums]
see_also: [parallel-reduce, hillis-steele-scan, blelloch-scan, parallel-prefix, segmented-scan, parallel-pack, parallel-radix-sort, list-ranking]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.1 (the definitions of scan and prescan, and the list of uses), Section 1.3 (line of sight and radix sort), Section 1.4 (recurrences) and Section 1.5 (segmented scans)
  - paper: doi:10.1109/12.42122
    title: Guy E. Blelloch, Scans as primitive parallel operations, IEEE Transactions on Computers 38(11), 1526 to 1538, 1989
    locator: Section II (scans as primitives in the scan vector model and simple operations built from them)
  - paper: doi:10.1145/322217.322232
    title: Richard E. Ladner and Michael J. Fischer, Parallel Prefix Computation, Journal of the ACM 27(4), 831 to 838, 1980
    locator: the definition of the prefix problem for an associative operator and the circuits P_k(n)
  - paper: doi:10.1016/0196-6774(86)90003-9
    title: Marc Snir, Depth-size trade-offs for parallel prefix computation, Journal of Algorithms 7(2), 185 to 201, 1986
    locator: the lower bound depth + size ≥ 2n − 2
  - paper: doi:10.1145/65950.65958
    title: Paul Beame and Johan Håstad, Optimal bounds for decision problems on the CRCW PRAM, Journal of the ACM 36(3), 643 to 670, 1989
    locator: the Ω(log n / log log n) time lower bound for parity with a polynomial number of processors
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Section 2.1, Balanced trees (the prefix-sums algorithm with O(n) work and O(log n) time on the EREW PRAM)
---

The all-prefix-sums problem, also called scan, takes a sequence $a_0, \ldots, a_{n-1}$ and an [associative operator](/associative-operator/) $\oplus$ and asks for every prefix $a_0 \oplus a_1 \oplus \cdots \oplus a_i$. It is the parallel form of the running total that a [prefix sums](/prefix-sums/) loop computes in one pass. Blelloch (1990) argued that scan should be a basic operation of parallel machines, like a memory read, because it has $O(n)$ work and $O(\log n)$ span and so many algorithms reduce to it. This page is about the problem; the [Hillis-Steele scan](/hillis-steele-scan/), the [Blelloch scan](/blelloch-scan/) and the [parallel prefix](/parallel-prefix/) circuits are ways to solve it.

## In plain words

A shop records the money it takes in each hour. The owner wants, for each hour, the total taken since opening. One clerk can go down the list and keep a running total. The question here is how a team of clerks can do the same job faster, when each running total seems to need the one before it.

The answer is that the running totals can be built in pieces, because the way the hours are grouped does not change a total. The same trick works for running maximums, for joining text, and for many other operations where the grouping does not matter but the order does.

## Definition

Let $\oplus$ be an associative operator on a set $S$ with identity $e$, and let $a = [a_0, a_1, \ldots, a_{n-1}]$ with $a_i \in S$.

- The **inclusive scan** (Blelloch's *scan*) is $[a_0,\ a_0 \oplus a_1,\ \ldots,\ a_0 \oplus a_1 \oplus \cdots \oplus a_{n-1}]$.
- The **exclusive scan** (Blelloch's *prescan*) is $[e,\ a_0,\ a_0 \oplus a_1,\ \ldots,\ a_0 \oplus \cdots \oplus a_{n-2}]$.

Each output $y_i$ is well defined because, by associativity, every bracketing of $a_0 \oplus \cdots \oplus a_i$ in the given order has the same value. The operator need not be commutative, so the order of the items matters. The inclusive scan needs no identity; the exclusive scan uses it for the empty prefix. The two forms differ by a shift: the exclusive scan is the inclusive scan moved one place to the right with $e$ in front, and the inclusive scan is $y_i \oplus a_i$ for the exclusive $y$.

The cost is counted in applications of $\oplus$, each of unit cost, in the [work-span model](/work-span-model/) or on a [PRAM](/pram-model/).

## Variants

- **Backward scan.** The suffixes $a_i \oplus \cdots \oplus a_{n-1}$. This is a scan of the reversed array with the operator $(x, y) \mapsto y \oplus x$.
- **Segmented scan.** The array is cut into contiguous segments by flags, and the scan restarts at each segment start. See [segmented prefix sums](/segmented-prefix-sums/) for the problem and [segmented scan](/segmented-scan/) for the algorithm.
- **Scan on a linked list.** When the order is given by next pointers and not by array indices, the problem is [list ranking](/list-ranking/), which needs other methods.
- **Blocked or distributed scan.** With $p$ processors and $n \gg p$, each processor owns a block. The cost on $p$ processors, not only the work and the span, is the measure.
- **Multidimensional scan.** Prefix sums over a grid, as in [two-dimensional prefix sums](/two-dimensional-prefix-sums/), are scans along each axis in turn when $\oplus$ is commutative.
- **Reduction.** If only the last prefix is needed, the problem is [reduction](/parallel-reduction/).

## Examples

For $a = [3, 1, 7, 0, 4, 1, 6, 3]$:

| operator | identity | inclusive scan | exclusive scan |
|---|---|---|---|
| $+$ | 0 | 3, 4, 11, 11, 15, 16, 22, 25 | 0, 3, 4, 11, 11, 15, 16, 22 |
| $\max$ | $-\infty$ | 3, 3, 7, 7, 7, 7, 7, 7 | $-\infty$, 3, 3, 7, 7, 7, 7, 7 |
| $\min$ | $+\infty$ | 3, 1, 1, 0, 0, 0, 0, 0 | $+\infty$, 3, 1, 1, 0, 0, 0, 0 |

With string concatenation on $[a, b, c]$, the inclusive scan is $[a, ab, abc]$. With $2 \times 2$ matrix products, the scan of $[M_0, M_1, M_2]$ is $[M_0, M_0 M_1, M_0 M_1 M_2]$, and the order of the factors matters. The linear recurrence $x_i = c_i x_{i-1} + d_i$ is a scan over the affine maps $x \mapsto c_i x + d_i$ under composition, which is associative but not commutative.

## Known algorithms

All counts are applications of $\oplus$; $m = 2^{\lceil \lg n \rceil}$.

| algorithm | work | span | output |
|---|---|---|---|
| sequential loop | $n - 1$ | $n - 1$ | either |
| [Hillis-Steele scan](/hillis-steele-scan/) | $n \lceil \lg n \rceil - m + 1$ | $\lceil \lg n \rceil$ | inclusive |
| [Blelloch scan](/blelloch-scan/) | $2(m - 1)$ | $2 \lceil \lg n \rceil$ rounds | exclusive and total |
| [Ladner-Fischer](/parallel-prefix/) $P_0(n)$ | $\le 4n$ | $\lceil \lg n \rceil$ | inclusive |
| blocked scan on $p$ processors | $n + O(p)$ | $O(n/p + \log p)$ | either |

- **Sequential.** One loop with a running value. It is optimal in work, and it is the base case of every blocked method.
- **Hillis-Steele.** Rounds with distances $1, 2, 4, \ldots$. Few rounds, but not [work-efficient](/work-efficiency/).
- **Blelloch.** An up-sweep and a down-sweep on a balanced tree. Work-efficient, with twice the rounds of Hillis-Steele.
- **Prefix circuits.** The Sklansky, Kogge-Stone, Brent-Kung and Ladner-Fischer circuits trade size against depth. See [parallel prefix](/parallel-prefix/).
- **Blocked scan.** Scan each block, scan the block totals, then add each block's offset. Some versions first reduce each block and scan the block sums, so that the second pass writes the output.
- **Single-pass GPU scan.** The [decoupled look-back scan](/decoupled-look-back-scan/) lets each block get its offset from earlier blocks while they are still running, so the data is read only once.

## Bounds

**Work.** For an operator such as string concatenation, the $n$ outputs are distinct and each output other than $a_0$ is the result of its own application of $\oplus$, so at least $n - 1$ applications are needed. The sequential loop meets this.

**Span.** The output $y_{n-1}$ depends on all $n$ items, and a value made by $d$ levels of a binary operator depends on at most $2^d$ items, so the span is at least $\lceil \lg n \rceil$. The Hillis-Steele scan and $P_0(n)$ meet this.

**Both at once.** Snir (1986) proved that every prefix circuit of size $s$ and depth $d$ has $s + d \ge 2n - 2$. So a circuit with the optimal depth $\lceil \lg n \rceil$ needs at least $2n - 2 - \lceil \lg n \rceil$ gates, nearly twice the $n - 1$ of the sequential loop: optimal work and optimal span cannot be reached together. Within a factor of 2 in work and 1 in depth, the Ladner-Fischer circuits come close to both.

**PRAM time.** With $n / \lg n$ processors, the blocked tree scan runs in $O(\log n)$ time on an EREW PRAM, so the time-processor product is $O(n)$, which is optimal. On a CRCW PRAM, concurrent writes do not help much: the scan of bits under $+$ gives the parity of the input in its last entry, and Beame and Håstad (1989) proved that parity needs $\Omega(\log n / \log\log n)$ time with a polynomial number of processors.

## Reductions

- **Reduce from scan.** The last entry of the inclusive scan, or the total that the Blelloch scan returns, is the [reduction](/parallel-reduction/).
- **Linear recurrences to scan.** The recurrence $x_i = c_i x_{i-1} + d_i$ becomes a scan over pairs $(c_i, d_i)$ with $(c, d) \circ (c', d') = (c c', c' d + d')$ for the composition "first $(c, d)$, then $(c', d')$". Blelloch (Section 1.4) extends this to higher-order recurrences.
- **Segmented scan to scan.** A segmented scan is one unsegmented scan with an operator on (flag, value) pairs, which Schwartz (1980) showed is associative. See [segmented scan](/segmented-scan/).
- **Pack to scan.** Keeping the items that satisfy a test is an exclusive $+$-scan of the 0-1 flags, followed by a scatter. See [compaction](/compaction/) and [parallel pack](/parallel-pack/).
- **Automata to scan.** Running a [finite automaton](/deterministic-finite-automaton/) over a string is a scan of the transition functions $\delta_c : Q \to Q$ under composition, so lexical analysis takes $O(\log n)$ span.
- **Range sums from scan.** When $\oplus$ has inverses, every range sum is a difference of two prefix sums, as on the [prefix sums](/prefix-sums/) page.

## Applications

Blelloch (1990) lists uses that include comparing strings, adding multiprecision numbers, evaluating polynomials, solving recurrences and tridiagonal systems, radix sort and quicksort, deleting marked elements, allocating processors, lexical analysis and labeling components in images. Some of the main ones:

- **Radix sort.** Each pass of a [parallel radix sort](/parallel-radix-sort/) splits the keys by one bit with two scans of the flags, which keeps the sort stable.
- **Pack and filter.** [Parallel pack](/parallel-pack/) uses an exclusive scan of the flags to give each kept item its output index.
- **Line of sight.** On a [terrain](/terrain-visibility/), a point is visible from the observer when its angle of elevation is larger than the maximum angle of all points before it, which is a $\max$-prescan.
- **Carry-lookahead addition.** The carries of a binary adder are a scan with the carry operator on (generate, propagate) pairs; this is the [carry-lookahead adder](/carry-lookahead-adder/).
- **Allocation.** When each task asks for $c_i$ slots, an exclusive $+$-scan of the $c_i$ gives each task the start of its slots in one shared array, as in [counting sort](/counting-sort/) and in building [compressed sparse row](/compressed-sparse-row/) arrays.
- **Sparse matrix-vector product.** A [segmented](/segmented-prefix-sums/) $+$-scan sums the products in each row of a sparse matrix.

## References
