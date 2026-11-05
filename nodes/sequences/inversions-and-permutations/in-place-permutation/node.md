---
tag: EHMTE3
kind: problem
slug: in-place-permutation
name: In-place permutation problem
aliases:
- applying a permutation in place
area: sequences/inversions-and-permutations
level: core
summary: Rearrange an array by a given permutation without extra storage proportional to n.
prereqs: [permutation, permutation-cycles]
see_also: [cycle-leader-permutation, permutation-inverse, bit-reversal-permutation, faro-shuffle, index-sort, permuting-problem, in-place-algorithm, scatter-and-gather]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2 (rearranging the records in place after an address table sort, by following the cycles of the permutation)
  - paper: "Faith E. Fich, J. Ian Munro and Patricio V. Poblete, Permuting in place, SIAM Journal on Computing 24(2) (1995) 266-278"
    locator: permuting with a read-only permutation and few extra bits of memory
  - paper: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988) 1116-1127"
    locator: the bound on the number of block transfers needed to permute in external memory
---

The in-place permutation problem asks to rearrange an array $A$ of $n$ items by a given [permutation](/permutation/) $P$, moving the item at position $i$ to position $P(i)$, while using only $O(1)$ extra words or a few extra bits instead of a second array. The array splits into the [cycles](/permutation-cycles/) of $P$, and each cycle can be rotated with one spare cell, so the whole problem is about finding each cycle exactly once. With one free mark bit per entry, the [cycle-leader method](/cycle-leader-permutation/) does it in $\Theta(n)$ time. With a read-only $P$ and $O(\log n)$ bits, the simple leader test costs $\Theta(n^2)$ in the worst case, and the best methods take $O(n \log n)$.

## In plain words

You have a row of boxes and a list that says, for each box, which slot it should end up in. The easy way is to build a second row and put each box straight into its slot. The problem asks you to do it with no second row, only a hand that can hold one box at a time.

The boxes form loops: box 1 goes where box 3 is, box 3 goes where box 4 is, box 4 goes back to slot 1. You can fix a loop by carrying one box around it. The hard part is not moving the boxes but remembering which loops are already done, because that bookkeeping is exactly the kind of extra memory the problem forbids.

## Definition

**Input.** An array $A[1..n]$ of items and a permutation $P$ of $[n]$, given as an array or as a function that can be evaluated.

**Output, scatter form.** The array $A'$ with $A'[P(i)] = A[i]$ for every $i$, stored in $A$ itself.

**Output, gather form.** The array $A'$ with $A'[i] = A[P(i)]$. This is the scatter form for the [inverse](/permutation-inverse/) $P^{-1}$.

**Resources.** Besides $A$ and $P$, the algorithm may use $O(1)$ words of $O(\log n)$ bits, or more generally a budget of $s$ extra bits. The question is the best running time for a given budget, and whether $P$ may be written.

## Variants

- **Writable $P$.** If $P$ may be changed temporarily, its entries carry one free bit each, since the values $1$ to $n$ leave the sign unused, and the problem is solved in linear time.
- **Read-only $P$.** $P$ is in read-only memory or is shared with other code. The algorithm must recognize the cycles it has already moved from $P$ alone.
- **Implicit $P$.** $P(i)$ is given by a formula, as in a rotation, a [perfect shuffle](/faro-shuffle/), a [bit-reversal permutation](/bit-reversal-permutation/) or the transposition of a matrix stored in row-major order. Then the structure of the cycles is often known in advance.
- **$P$ and $P^{-1}$ both available.** A cycle can then be walked in both directions, which makes the leader test cheaper.
- **Inverting a permutation in place.** Replacing the array $P$ by $P^{-1}$ is the special case in which the items are the indices themselves, written by scatter into $P$.
- **External memory.** When $A$ is on disk, the [permuting problem](/permuting-problem/) asks for the fewest block transfers instead of the least extra space.

## Examples

**Three cycles.** For $A = (\mathrm{A}, \mathrm{B}, \mathrm{C}, \mathrm{D}, \mathrm{E}, \mathrm{F})$ and $P = 3\,6\,4\,1\,5\,2$ with cycles $(1\,3\,4)(2\,6)(5)$, the scatter form gives $(\mathrm{D}, \mathrm{F}, \mathrm{A}, \mathrm{C}, \mathrm{E}, \mathrm{B})$ and the gather form gives $A'[i] = A[P(i)]$, which is $(\mathrm{C}, \mathrm{F}, \mathrm{D}, \mathrm{A}, \mathrm{E}, \mathrm{B})$. The two differ because $P$ has a cycle of length 3. The page on the [cycle-leader method](/cycle-leader-permutation/) traces the scatter step by step.

**Rotation.** Rotating $A[0..n-1]$ left by $k$ places is the gather $A'[i] = A[(i + k) \bmod n]$. Its cycles are the $\gcd(n, k)$ classes of indices modulo $\gcd(n, k)$, each of length $n/\gcd(n, k)$, and their leaders are $0, 1, \ldots, \gcd(n, k) - 1$. So no marks are needed. For $n = 6$ and $k = 2$ there are two cycles, $0 \to 2 \to 4$ and $1 \to 3 \to 5$, read as "position $i$ takes the item at position $i + 2$".

**Bit reversal.** For $n = 8$, the permutation that maps $i$ to the number with the reversed 3-bit binary digits has the cycles $(1\,4)$, $(3\,6)$ and four fixed points. It is its own inverse, so swapping $A[i]$ and $A[\operatorname{rev}(i)]$ for each $i < \operatorname{rev}(i)$ solves the problem with no marks. This is the reordering step of the iterative [fast Fourier transform](/fast-fourier-transform/).

## Known algorithms

- **Copy.** $B[P(i)] \leftarrow A[i]$ for all $i$, then copy $B$ back. $\Theta(n)$ time and $n$ extra words.
- **Cycle leader with marks.** Walk each cycle once and mark its entries in $P$ or in a bit vector, then clear the marks. $\Theta(n)$ time with $n$ extra bits, or with $O(1)$ extra words if $P$ has a free bit per entry. See the [cycle-leader method](/cycle-leader-permutation/).
- **Cycle leader with a read-only $P$.** Move a cycle only from its smallest index, recognized by walking the cycle until it meets a smaller index. $O(1)$ extra words, $\Theta(n^2)$ time in the worst case, and $(n+1)H_n - n$ reads of $P$ on average over random permutations.
- **Better leader tests.** Fich, Munro and Poblete gave methods for a read-only $P$ with $O(n \log n)$ worst-case time and a polylogarithmic number of extra bits, and studied the case in which $P^{-1}$ can also be evaluated.
- **Rotations.** The three-reversal method ($A \leftarrow (A_1^R A_2^R)^R$) and the gcd-cycle method each take $\Theta(n)$ time and $O(1)$ extra words.
- **Sorting by target.** If items can be compared by their target position, any in-place sort, such as [heapsort](/heapsort/), applied to the pairs $(P(i), A[i])$ does the job in $O(n \log n)$ time, but it needs the targets stored next to the items.

## Bounds

- **Moves.** Every position $m$ with $P^{-1}(m) \ne m$ must be written at least once, so at least $n - f$ writes into $A$ are needed, where $f$ is the number of fixed points. With one spare cell and copies only, the fewest copies is $\sum (L + 1)$ over the cycles of length $L \ge 2$: each such cycle needs one copy into the spare cell, because its first write overwrites an item that is still needed. The cycle method meets this bound.
- **Time.** $\Omega(n)$ for any non-identity permutation, met by the marking method.
- **Space and time with a read-only $P$.** A cycle must be recognized as already done from $P$ and a few bits of memory. The methods of Fich, Munro and Poblete take $O(n \log n)$ time in the worst case with a polylogarithmic number of extra bits, against $\Theta(n)$ time with $n$ extra bits.
- **External memory.** Aggarwal and Vitter showed that permuting $N$ items with a memory of $M$ items and blocks of $B$ items takes $\Theta\big(\min\big(N, \tfrac{N}{B} \log_{M/B} \tfrac{N}{B}\big)\big)$ block transfers in the worst case, which is the cost of sorting unless the blocks are tiny. See the [external-memory model](/external-memory-model/).

## Reductions

- **Gather to scatter.** The gather by $P$ is the scatter by $P^{-1}$. Inverting $P$ in place first, by the same cycle method, and then scattering reduces one form to the other.
- **Inverting $P$.** Scattering the items $A[i] = i$ by $P$ gives $A' = P^{-1}$, so inverting a permutation in place is an instance of the problem.
- **Matrix transposition.** Transposing an $r \times c$ matrix stored row by row in place is the in-place permutation $i \mapsto i \cdot r \bmod (rc - 1)$ on the indices $0$ to $rc - 2$, with the last index fixed.
- **From sorting.** After an [index sort](/index-sort/) computes the sorted order of the keys as a permutation, moving the records into that order is an in-place permutation.

## Applications

- **Reordering records** after their keys have been sorted through an index or an address table, writing each large record once.
- **Fast Fourier transform.** The bit-reversal reordering of the input or output.
- **Matrix transposition in place** for large non-square matrices, and the perfect shuffle in merging and interleaving.
- **Applying a relabeling** to the nodes of a graph or the cells of a mesh, for example to improve memory locality.
- **Random permutations.** Applying a uniform [random permutation](/random-permutation/) to an array in place, although the [Fisher-Yates shuffle](/fisher-yates-shuffle/) does this directly without building $P$.

## References
