---
tag: 3MZHPY
kind: problem
slug: gray-code-generation
name: Gray code generation
aliases:
- listing all Gray codes
- enumerating Gray codes
- Gray order listing of bit strings
area: combinatorics/gray-codes
level: intro
summary: Output all 2^n n-bit strings so that consecutive strings differ in one bit.
prereqs: [gray-code, combinatorial-generation]
see_also: [binary-reflected-gray-code, loopless-gray-code-generation, ruler-sequence, cyclic-gray-code, hypercube-hamiltonian-cycle, balanced-gray-code, power-set-enumeration, k-ary-gray-code-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (Algorithm G, Gray binary generation, and Algorithm L, loopless Gray binary generation; the counts of Gray cycles)
  - paper: doi:10.1145/360336.360343
    title: James R. Bitner, Gideon Ehrlich and Edward M. Reingold, Efficient generation of the binary reflected Gray code and its applications, Communications of the ACM 19(9), 517 to 521, 1976
    locator: the loopless generator of the reflected Gray code
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 2.3 (the hypercube is Hamilton-laceable), Section 3.1 (the binary reflected Gray code) and Section 3.11 (the number of Gray codes)
---

Gray code generation asks for a list of all $2^n$ binary strings of length $n$ in which each two neighbors differ in exactly one bit. The [binary reflected Gray code](/binary-reflected-gray-code/) solves it, and a [loopless generator](/loopless-gray-code-generation/) outputs it with $O(1)$ worst-case time between two strings, which is optimal because any listing takes $\Omega(2^n)$ time. The problem is the same as finding a Hamiltonian path in the $n$-cube, and the cyclic form is a [Hamiltonian cycle](/hypercube-hamiltonian-cycle/). A second meaning, listing or counting all the different Gray codes of length $n$, is much harder.

## In plain words

You have a row of switches and want to try every on and off pattern exactly once. Each move may flip only one switch. Gray code generation asks for such a plan of moves.

One plan always works, and it is easy to run: at move number one, three, five and so on, flip the first switch; at the other moves, flip the switch just after the first switch that is on. A program can find the next switch to flip in a fixed, small number of steps, so the cost is about one step per pattern. No method can be faster, because each pattern must appear once.

Another question is how many different plans exist. For four switches there are already well over a thousand, and the count grows very fast.

## Definition

Let $n \ge 0$ be the length of the strings and $N = 2^n$.

- **Input:** $n$.
- **Output:** a sequence $v_0, v_1, \ldots, v_{N-1}$ that contains each string of $\{0,1\}^n$ exactly once, with $v_{i-1}$ and $v_i$ at [Hamming distance](/hamming-distance/) 1 for $1 \le i < N$.

The output model matters for the cost. In the usual model the generator keeps one array $a_{n-1} \ldots a_0$, changes one bit, and then *visits* the array: the caller reads it in place. An equivalent output is the delta sequence $\delta_1, \ldots, \delta_{N-1}$, where step $i$ flips bit $\delta_i$. A copy of each string costs $\Theta(n)$ more per string.

## Variants

- **Cyclic.** Require also that $v_{N-1}$ and $v_0$ differ in one bit: a [cyclic Gray code](/cyclic-gray-code/). The reflected code is cyclic.
- **A fixed start or a fixed end.** In the $n$-cube there is a Gray path from $u$ to $v$ exactly when $u$ and $v$ differ in an odd number of bits, for $n \ge 1$ (Simmons, 1978; see Mütze, Section 2.3). The parity part of this is proved on the page of the [hypercube Hamiltonian cycle](/hypercube-hamiltonian-cycle/).
- **Balanced.** Each bit must change about $N/n$ times: see [balanced Gray code](/balanced-gray-code/).
- **Larger alphabets.** List all strings over $\{0, \ldots, k-1\}$ with one digit changed by $\pm 1$ per step: see [k-ary Gray code generation](/k-ary-gray-code-generation/).
- **Restricted sets.** List only the strings with exactly $k$ ones, with one swap of a 0 and a 1 per step: see [combination Gray code generation](/combination-gray-code-generation/).
- **All Gray codes.** List or count every Gray cycle of $Q_n$. Up to the start and the direction there are 1, 6, 1344 and 906,545,760 cycles for $n = 2$ to 5, and $35{,}838{,}213{,}722{,}570{,}883{,}870{,}720$ for $n = 6$ (Haanpää and Östergård, 2014; OEIS A066037). No formula is known.

## Examples

- $n = 1$: 0, 1.
- $n = 2$: 00, 01, 11, 10. The only other Gray code from 00 is 00, 10, 11, 01, which is the same cycle in the other direction.
- $n = 3$, the reflected code: 000, 001, 011, 010, 110, 111, 101, 100, with delta sequence 0, 1, 0, 2, 0, 1, 0, the [ruler sequence](/ruler-sequence/).
- $n = 3$, a Gray code that is not cyclic: 000, 001, 011, 010, 110, 100, 101, 111. The ends 000 and 111 differ in three bits.
- Not a solution: 000, 001, 011, 111, 110, 100. Each step changes one bit, but 010 and 101 are missing.

## Known algorithms

| algorithm | time per string | total time | extra space | notes |
|---|---|---|---|---|
| [reflected construction](/binary-reflected-gray-code/) of the whole list | $O(1)$ amortized | $\Theta(N)$ | $\Theta(N)$ | random access to the list |
| unrank each $k$ with [binary to Gray conversion](/binary-to-gray-conversion/) | $O(1)$ | $\Theta(N)$ | $O(1)$ | writes each string, $n \le w$ |
| Knuth's Algorithm G (parity rule) | $O(1)$ amortized, $O(n)$ worst | $\Theta(N)$ | $O(n)$ | CAT, one array |
| increment a counter $k$, flip bit $\rho(k)$ with a [trailing zero count](/trailing-zero-count/) | $O(1)$ with the instruction | $\Theta(N)$ | $O(1)$ | $n \le w$ |
| [loopless generation](/loopless-gray-code-generation/) with focus pointers (Bitner, Ehrlich and Reingold, 1976) | $O(1)$ worst case | $\Theta(N)$ | $O(n)$ | loopless |

All bounds are on the [word RAM](/word-ram/), with the string visited in place. Algorithm G and the focus pointer method give the same list $\Gamma_n$.

## Bounds

- **Lower bound.** Any generator must visit $N = 2^n$ strings, so it takes $\Omega(N)$ time. A generator that writes each string as a new array takes $\Omega(nN)$ time.
- **Upper bound.** The loopless generator meets $O(1)$ worst-case time per string and $O(n)$ extra space, so the bound $\Theta(N)$ is tight.
- **Output size.** The delta sequence has $N - 1$ entries of $\lceil \lg n \rceil$ bits each, so writing it costs $\Theta(N)$ word operations.

## Reductions

- **Hamiltonian path.** A Gray code is a [Hamiltonian path](/hamiltonian-path/) of the $n$-cube $Q_n$, and a cyclic one is a [Hamiltonian cycle](/hamiltonian-cycle/). The general [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) is NP-complete, but $Q_n$ has the explicit solution $\Gamma_n$.
- **From unranking.** Generation reduces to [Gray code conversion](/gray-code-conversion/): unrank $0, 1, \ldots, N - 1$.
- **To a binary counter.** The bit that the reflected code flips at step $k$ is the lowest bit that a [binary counter increment](/binary-counter-increment/) changes from 0 to 1 at step $k$, so a counter drives a Gray code generator.

## Applications

- **Subset search with cheap updates.** Read bit $j$ as "item $j$ is chosen". Then the list visits all subsets of $n$ items, and each step adds or removes one item. A total, a product or a count over the chosen items changes by one term per step. See [power set enumeration](/power-set-enumeration/).
- **Puzzles.** The [Tower of Hanoi](/tower-of-hanoi/) moves disc $\rho(k) + 1$ at step $k$, and the Chinese rings puzzle follows the reflected code.
- **Testing hardware.** Input vectors in Gray order change one input line per test, which limits the switching activity of the circuit under test.
- **Exhaustive search over Boolean functions.** Karnaugh maps and truth table methods order the rows in Gray order so that neighbor rows differ in one variable.

## References
