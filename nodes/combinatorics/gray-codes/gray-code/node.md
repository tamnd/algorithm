---
tag: DYWN8S
kind: concept
slug: gray-code
name: Gray code
aliases:
- reflected Gray code
- binary Gray code
- reflected binary code
- Gray's code
area: combinatorics/gray-codes
level: intro
summary: Ordering of bit strings in which consecutive strings differ in exactly one bit.
prereqs: [hamming-distance, bitwise-operations]
see_also: [binary-reflected-gray-code, cyclic-gray-code, hypercube-hamiltonian-cycle, ruler-sequence, gray-code-generation, balanced-gray-code, k-ary-gray-code, minimal-change-ordering]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (Gray binary code, its history, Algorithms G and L, and the counts of Gray cycles)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Sections 1 and 2 (the binary reflected Gray code and the general idea of a combinatorial Gray code)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 3.1 (the binary reflected Gray code) and Section 3.11 (the number of Gray codes)
  - url: https://patents.google.com/patent/US2632058A
    title: Frank Gray, Pulse code communication, US Patent 2,632,058, issued 17 March 1953
    locator: the reflected binary code and its use in a pulse code tube
---

A Gray code is a list of all $2^n$ binary strings of length $n$ in which each two neighbors differ in exactly one bit, so that their [Hamming distance](/hamming-distance/) is 1. The standard example is the [binary reflected Gray code](/binary-reflected-gray-code/), which Frank Gray patented for pulse code communication in 1953, and whose $k$-th string is $k \oplus \lfloor k/2 \rfloor$. In graph terms, a Gray code is a Hamiltonian path in the $n$-dimensional hypercube, and a [cyclic Gray code](/cyclic-gray-code/) is a Hamiltonian cycle. The name also covers any listing of combinatorial objects in which each step makes a small change, such as one transposition of a permutation.

## In plain words

Count from zero to fifteen in binary with four switches. The step from seven to eight turns three switches off and one switch on. If a machine reads the switches while they move, it can see a value that is far from both seven and eight.

A Gray code puts the same sixteen patterns in a different order. From each pattern to the next, exactly one switch moves. So a reading in the middle of a step is always one of the two neighbors, never a far value.

The most common Gray code is made by a mirror trick. Take the list for one switch less. Write it once with the new switch off, then write it backwards with the new switch on. The join in the middle and the wrap from the end to the start both move only the new switch.

## The idea

**Notation.** On this page $n \ge 0$ is the length of the strings, $N = 2^n$ is the number of strings, and $\oplus$ is bitwise exclusive or. A string $a_{n-1} \ldots a_1 a_0$ has its bit $a_0$ on the right.

**Definition.** An $n$-bit Gray code is a sequence $(v_0, v_1, \ldots, v_{N-1})$ that contains each string of $\{0,1\}^n$ exactly once, such that $v_{i-1}$ and $v_i$ differ in exactly one bit for $1 \le i \le N-1$. It is a *Gray cycle* (a cyclic Gray code) if $v_{N-1}$ and $v_0$ also differ in exactly one bit. The *delta sequence* $(\delta_1, \ldots, \delta_{N-1})$ lists the index of the bit that changes at each step: $v_i = v_{i-1} \oplus 2^{\delta_i}$.

**The graph view.** The $n$-cube $Q_n$ is the [graph](/graph/) with vertex set $\{0,1\}^n$, in which two strings are adjacent when they differ in one bit. A Gray code is exactly a [Hamiltonian path](/hamiltonian-path/) of $Q_n$, and a Gray cycle is exactly a [Hamiltonian cycle](/hamiltonian-cycle/). For each $n \ge 2$, $Q_n$ has a Hamiltonian cycle; this is the [hypercube Hamiltonian cycle theorem](/hypercube-hamiltonian-cycle/).

**The reflected code.** The binary reflected Gray code $\Gamma_n$ is defined by $\Gamma_0 = \varepsilon$ (the list with one empty string) and

$$\Gamma_{n+1} = 0\Gamma_n,\ 1\Gamma_n^R,$$

where $0\Gamma_n$ puts a 0 in front of each string and $\Gamma_n^R$ is the list in reverse order. Its string of rank $k$ is $g(k) = k \oplus \lfloor k/2 \rfloor$, read as an $n$-bit number. Step $k$ changes bit $\rho(k)$, where $\rho(k)$ is the exponent of the largest power of 2 that divides $k$; this is the [ruler sequence](/ruler-sequence/). Each of these facts is proved on the page of the [binary reflected Gray code](/binary-reflected-gray-code/).

**Many Gray codes.** The reflected code is one Gray code among very many. Counted as Hamiltonian cycles of $Q_n$ without a start or a direction, there are 1, 6 and 1344 Gray cycles for $n = 2, 3, 4$, and 906,545,760 for $n = 5$ (Knuth, Section 7.2.1.1; OEIS A066037). Other Gray codes trade the simple formula for other properties: a [balanced Gray code](/balanced-gray-code/) changes each bit about equally often, and a monotone Gray code passes through the strings roughly in order of their weight.

**Cost of listing.** A program that lists all $N$ strings must spend $\Omega(N)$ time, one step for each string. The reflected code meets this bound with a constant amount of work in the worst case between two strings: see [loopless Gray code generation](/loopless-gray-code-generation/). A copy of each string costs $\Theta(n)$ more, so a fast program changes one bit of a single array and lets the caller read it.

**Combinatorial Gray codes.** The same goal applies to other objects. A [minimal change ordering](/minimal-change-ordering/) lists objects so that each step makes one small change, for example a [revolving door order](/revolving-door-ordering/) for $k$-subsets, the [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) order for permutations, and the [k-ary Gray codes](/k-ary-gray-code/) for strings over a larger alphabet.

## Examples

The binary reflected Gray code for $n = 3$. The column $\delta$ gives the bit that changes from the row above.

| rank $k$ | $k$ in binary | $g(k)$ | $\delta$ |
|---|---|---|---|
| 0 | 000 | 000 | |
| 1 | 001 | 001 | 0 |
| 2 | 010 | 011 | 1 |
| 3 | 011 | 010 | 0 |
| 4 | 100 | 110 | 2 |
| 5 | 101 | 111 | 0 |
| 6 | 110 | 101 | 1 |
| 7 | 111 | 100 | 0 |

The last string 100 differs from the first string 000 in bit 2 only, so $\Gamma_3$ is a Gray cycle.

- **Non-example.** The binary counting order 000, 001, 010, 011, 100, ... is not a Gray code. The step from 011 to 100 changes three bits.
- **A Gray path that is not a cycle.** The list 000, 001, 011, 010, 110, 100, 101, 111 contains each 3-bit string once, and each step changes one bit. The last string 111 differs from the first in three bits, so the list is a Gray code but not a Gray cycle.

## Where it is used

- **Position encoders.** A rotary or linear encoder prints a Gray code on a disc or strip. When the reading head sits on a border, only one track is in doubt, so the read value is off by at most one position. This was the use in Gray's patent, for the output of a pulse code tube.
- **Karnaugh maps.** The rows and columns of a Karnaugh map follow the 2-bit Gray code 00, 01, 11, 10, so that cells next to each other differ in one input variable.
- **Listing subsets.** Read bit $j$ as "element $j$ is in the set". Then a Gray code lists all subsets, and each step adds or removes one element. A sum or a product over each subset can then be updated in $O(1)$ time per subset, instead of $O(n)$. See [power set enumeration](/power-set-enumeration/).
- **Puzzles.** In the [Tower of Hanoi](/tower-of-hanoi/) with $n$ discs, the disc moved at step $k$ of the optimal solution is disc $\rho(k) + 1$, counted from the smallest, the same index that the reflected code changes at step $k$. The Chinese rings puzzle follows the reflected code itself.
- **Digital modulation.** Signal points that are close to each other get labels that differ in one bit, so the most likely error of a receiver costs one bit.

## References
