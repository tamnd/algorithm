---
tag: CZ4F59
kind: definition
slug: cyclic-gray-code
name: Cyclic Gray code
aliases:
- closed Gray code
- cyclic Gray sequence
- Gray cycle
area: combinatorics/gray-codes
level: intro
summary: A Gray code in which the last and first codewords also differ in exactly one bit.
prereqs: [gray-code, hamming-distance]
see_also: [hypercube-hamiltonian-cycle, binary-reflected-gray-code, hamiltonian-cycle, bipartite-graph, balanced-gray-code, ruler-sequence, k-ary-gray-code, steinhaus-johnson-trotter]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (Gray cycles of the n-cube, the reflected and modular mixed-radix Gray codes, and the counts of Gray cycles)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Sections 1 and 2 (Gray codes as Hamiltonian paths and cycles, and the binary reflected Gray code)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 3.1 (the binary reflected Gray code) and Section 3.11 (the number of Gray codes)
  - url: https://oeis.org/A066037
    title: OEIS A066037, Number of (undirected) Hamiltonian cycles in the binary n-cube, or the number of cyclic n-bit Gray codes
    locator: the terms 1, 1, 6, 1344, 906545760, 35838213722570883870720
---

A cyclic Gray code is a Gray code whose last word and first word are also neighbors, so that the list closes into a ring. For $n$-bit strings with $n \ge 2$, a cyclic Gray code is the same thing as a [Hamiltonian cycle](/hypercube-hamiltonian-cycle/) of the $n$-cube, and the [binary reflected Gray code](/binary-reflected-gray-code/) is one. Because the ring has no special start, any rotation of a cyclic code is again a Gray code, so a program can begin the walk at any word it likes. In a bipartite closeness graph an odd number of words can never form a cyclic code, which is the main obstruction.

## Definition

Let $S$ be a finite set of $N \ge 2$ objects and let $\sim$ be a symmetric closeness relation on $S$, for example "differ in exactly one bit". A *Gray code* for $(S, \sim)$ is a list $v_0, v_1, \ldots, v_{N-1}$ that contains each object of $S$ exactly once, with $v_{i-1} \sim v_i$ for $1 \le i < N$. It is *cyclic* when also

$$v_{N-1} \sim v_0.$$

Otherwise it is *open*. In the closeness graph, whose vertices are $S$ and whose edges join close objects, an open Gray code is a Hamiltonian path and a cyclic Gray code with $N \ge 3$ is a [Hamiltonian cycle](/hamiltonian-cycle/).

For binary strings, $S = \{0,1\}^n$, $N = 2^n$, and $u \sim v$ when $u$ and $v$ are at [Hamming distance](/hamming-distance/) 1. The closeness graph is the $n$-cube $Q_n$. For $n = 1$ the list $0, 1$ meets the condition $v_1 \sim v_0$, but the ring uses the single edge of $Q_1$ twice, so it is not a Hamiltonian cycle. Authors differ on whether to call it cyclic; the statements on this page are for $n \ge 2$ unless they say otherwise.

**Rotations and symmetries.** If $v_0, \ldots, v_{N-1}$ is cyclic, then so is the rotation $v_s, v_{s+1}, \ldots, v_{N-1}, v_0, \ldots, v_{s-1}$ for each $s$, and so is the reversed list. For binary strings, the map $v \mapsto v \oplus m$ for a fixed mask $m$ and any fixed permutation of the bit positions also keep the Hamming distance, so they map a cyclic code to a cyclic code.

**Parity rule for binary codes.** Each step of a binary Gray code changes the number of ones by 1, so it changes the parity of the weight. A list of $N = 2^n$ words has $N - 1$ steps, an odd number for $n \ge 1$. So the first and last words of any binary Gray code have weights of different parity, and they differ in an odd number of bits. An open code is one whose ends differ in 3, 5, 7, ... bits.

**Odd sets have no cyclic code.** More generally, if the closeness graph is a [bipartite graph](/bipartite-graph/), each step of a closed walk goes from one side to the other, so every closed walk has even length. A cyclic Gray code is a closed walk of length $N$. Hence $N$ must be even.

## Examples and non-examples

- **The reflected code, $n = 3$.** 000, 001, 011, 010, 110, 111, 101, 100. The last word 100 differs from 000 only in bit 2, so the code is cyclic. Its cyclic delta sequence is 0, 1, 0, 2, 0, 1, 0, 2: the [ruler sequence](/ruler-sequence/) $R_3$ followed by $n - 1 = 2$. The reflected code is cyclic for every $n \ge 1$, since its last word is $10 \ldots 0$.
- **An open code, $n = 3$.** 000, 001, 011, 010, 110, 100, 101, 111. Each step flips one bit, but 111 and 000 differ in three bits.
- **$n = 2$.** 00, 01, 11, 10 is cyclic. Every Gray code of length 2 that starts at 00 is one of the two directions of this one cycle, so $Q_2$ has exactly one Gray cycle.
- **Counts.** Counted as undirected cycles, with no start fixed, $Q_n$ has 1, 6, 1344 and 906,545,760 Gray cycles for $n = 2, 3, 4, 5$ (OEIS A066037). From a fixed start and with a direction, there are $2$, $12$ and $2688$ for $n = 2, 3, 4$, twice the undirected count. A script that searched all Hamiltonian cycles of $Q_2$, $Q_3$ and $Q_4$ found these numbers.
- **Base 3, reflected.** The reflected ternary code for $n = 2$ is 00, 01, 02, 12, 11, 10, 20, 21, 22, with one digit changed by $\pm 1$ per step. It is not cyclic: 22 and 00 differ in both digits. With $\pm 1$ steps and no wrap, the closeness graph is a $3 \times 3$ grid, which is bipartite with 9 vertices, so no cyclic code exists at all.
- **Base 3, modular.** If a digit may also step from 2 to 0 or from 0 to 2, a cyclic code exists: 00, 01, 02, 12, 10, 11, 21, 22, 20, then back to 00 by a change of the first digit from 2 to 0. This is the modular Gray code, in which the code of $b$ has digit $j$ equal to $b_j - b_{j+1} \bmod k$. See [k-ary Gray code](/k-ary-gray-code/).
- **Base 4, reflected.** For even $k$ the reflected code over $\{0, \ldots, k-1\}^n$ ends at $(k-1)0 \ldots 0$, so it closes into a ring if a digit may wrap from $k - 1$ to 0. For $k = 4$, $n = 2$ the last word is 30.
- **Permutations.** The [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) list of the permutations of $\{1, \ldots, n\}$, with adjacent transpositions as the closeness relation, is cyclic for $n \ge 2$: it starts at $12 \ldots n$ and ends at $213 \ldots n$. A script checked this for $n \le 5$.
- **Combinations.** The [revolving door order](/revolving-door-ordering/) of the $k$-subsets of an $n$-set, with one element out and one element in per step, is cyclic. The homogeneous [Eades-McKay order](/eades-mckay-algorithm/) starts at $1^k 0^{n-k}$ and ends at $0^{n-k} 1^k$. For $n = 4$ and $k = 2$ these are 1100 and 0011, which differ in four positions, so that list is not cyclic.

## Related definitions

- **[Hamiltonian cycle in the hypercube](/hypercube-hamiltonian-cycle/).** The theorem that $Q_n$ has a cyclic Gray code for every $n \ge 2$, with a proof by the reflected construction.
- **[Gray code](/gray-code/).** The general notion, open or cyclic.
- **[Balanced Gray code](/balanced-gray-code/).** A cyclic binary code in which each bit changes about $2^n / n$ times. The definition counts the wrap step, so it needs the code to be cyclic.
- **Delta sequence.** The cyclic delta sequence of a cyclic binary code has $2^n$ entries, one for each edge of the ring. Each bit position appears an even number of times in it, because the walk returns to its start.
- **Hamiltonian path.** An open Gray code. In $Q_n$ there is a Gray path between $u$ and $v$ exactly when they differ in an odd number of bits; the parity rule above proves the "only if" part.

## References
