---
tag: 55YGMJ
kind: theorem
slug: hypercube-hamiltonian-cycle
name: Hamiltonian cycle in the hypercube
aliases:
- hypercube Gray cycle
- Gray codes and hypercube Hamiltonian cycles
- Hamiltonicity of the n-cube
area: combinatorics/gray-codes
level: core
summary: The n-dimensional hypercube has a Hamiltonian cycle for n >= 2, equivalent to a cyclic Gray code.
prereqs: [hamiltonian-cycle, gray-code, induction]
see_also: [binary-reflected-gray-code, cyclic-gray-code, bipartite-graph, hamiltonian-path, hamiltonian-cycle-problem, gray-code-generation, balanced-gray-code, perfect-matching]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (the reflected Gray binary code as a Hamiltonian cycle of the n-cube, its history, and the counts of Gray cycles)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 2.2 (necessary conditions, bipartite balance), Section 2.3 (Hamilton-laceability of the hypercube), Section 3.1 (the binary reflected Gray code) and Section 3.11 (the number of Gray codes)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Sections 1 and 2 (Gray codes as Hamiltonian cycles of the n-cube and the reflected code)
  - url: https://patents.google.com/patent/US2632058A
    title: Frank Gray, Pulse code communication, U.S. Patent 2,632,058, 1953
    locator: the reflected binary code and its construction by reflection
  - url: https://oeis.org/A066037
    title: OEIS A066037, Number of (undirected) Hamiltonian cycles in the binary n-cube, or the number of cyclic n-bit Gray codes
    locator: the terms 1, 1, 6, 1344, 906545760, 35838213722570883870720
---

## Statement

For $n \ge 0$ the $n$-cube $Q_n$ is the graph with vertex set $\{0,1\}^n$, $N = 2^n$ vertices, in which two strings are adjacent when they differ in exactly one bit, that is, at [Hamming distance](/hamming-distance/) 1. A Hamiltonian cycle is a cycle through all $N$ vertices, which needs $N \ge 3$.

**Theorem.** For every $n \ge 2$ the graph $Q_n$ has a Hamiltonian cycle. One such cycle is the [binary reflected Gray code](/binary-reflected-gray-code/) $\Gamma_n$, defined by $\Gamma_1 = 0, 1$ and $\Gamma_{m+1} = 0\Gamma_m,\ 1\Gamma_m^R$, read as a ring. For $n \in \{0, 1\}$ the graph has no Hamiltonian cycle.

**Equivalence.** For $n \ge 2$, the Hamiltonian cycles of $Q_n$ are exactly the [cyclic Gray codes](/cyclic-gray-code/) of length $n$, read as rings: a list $v_0, \ldots, v_{N-1}$ of all strings in which $v_{i-1}$ and $v_i$ differ in one bit for each $i$, and $v_{N-1}$ and $v_0$ differ in one bit too.

**Parity lemma.** $Q_n$ is a [bipartite graph](/bipartite-graph/) whose two sides, the strings of even weight and the strings of odd weight, both have $2^{n-1}$ vertices for $n \ge 1$. Hence every Hamiltonian path of $Q_n$, for $n \ge 1$, joins two strings that differ in an odd number of bits.

## In plain words

Think of the corners of a cube in $n$ dimensions. Each corner has a label made of $n$ bits, and an edge joins two corners whose labels differ in one bit. The theorem says that for two or more dimensions, you can walk along the edges, visit each corner once, and come back to the start.

The walk is easy to build. Take the walk for one dimension less, do it once on the near face of the cube, then do it backward on the far face, and use two edges to join the faces. Since the corners split into two equal colors and each edge joins two colors, any walk that visits all corners must start and end on different colors.

## Proof

*Equivalence.* A cycle in $Q_n$ through all $N \ge 4$ vertices, listed from any vertex in either direction, is a list of all strings in which each neighbor pair, the last and first included, differ in one bit. Conversely such a list with $N \ge 4$ distinct entries gives a closed walk of $N$ distinct vertices, which is a cycle. For $n \ge 2$ we have $N \ge 4$.

*Claim.* For every $m \ge 1$, $\Gamma_m$ is a list of all $2^m$ strings of $\{0,1\}^m$, each once, in which each two consecutive strings differ in one bit, that starts at $0^m$ and ends at $10^{m-1}$.

We prove the claim by [induction](/induction/) on $m$. For $m = 1$, $\Gamma_1 = 0, 1$ meets all four parts. Assume the claim for $m$ and look at $\Gamma_{m+1} = 0\Gamma_m,\ 1\Gamma_m^R$.

1. *All strings, each once.* The first half lists each string $0x$ with $x \in \{0,1\}^m$ once, since $\Gamma_m$ lists each $x$ once. The second half lists each $1x$ once for the same reason, and reversal does not change which strings appear. No string starts with both 0 and 1, so the halves share no string.
2. *Steps inside a half.* Two consecutive strings in the first half are $0x$ and $0y$ with $x, y$ consecutive in $\Gamma_m$, so they differ in one bit. Reversal keeps the set of consecutive pairs of a list, so the same holds in the second half.
3. *The step between the halves.* The first half ends at $0z$ where $z$ is the last entry of $\Gamma_m$. The second half starts with the first entry of $\Gamma_m^R$, which is also $z$, so it starts at $1z$. The strings $0z$ and $1z$ differ in one bit.
4. *The ends.* The first entry is $0$ followed by the first entry of $\Gamma_m$, so it is $0 \cdot 0^m = 0^{m+1}$. The last entry is $1$ followed by the last entry of $\Gamma_m^R$, which is the first entry of $\Gamma_m$, so it is $1 0^m$.

This proves the claim. Now let $n \ge 2$. By the claim, $\Gamma_n$ is a Hamiltonian path of $Q_n$ from $0^n$ to $10^{n-1}$. These two ends differ only in bit $n - 1$, so they are adjacent, and the edge between them is not an edge of the path: the path has $N - 1 \ge 3$ edges and uses the edge $\{0^n, 10^{n-1}\}$ only if the two ends are consecutive in it, which would make $N = 2$. Adding this edge closes the path into a cycle through all $N$ vertices.

*No cycle for $n \le 1$.* $Q_0$ has one vertex and $Q_1$ has two, and a cycle in a simple graph has at least three distinct vertices.

*Parity lemma.* Color each string by the parity of its number of ones. Flipping one bit changes the number of ones by $\pm 1$, so each edge joins strings of different color, and $Q_n$ is bipartite. For $n \ge 1$, the map that flips bit 0 is a bijection from the even strings to the odd strings, so each side has $2^{n-1}$ strings. A Hamiltonian path $v_0, \ldots, v_{N-1}$ alternates colors and has $N - 1$ edges, an odd number for $n \ge 1$. So $v_0$ and $v_{N-1}$ have different colors, that is, weights of different parity, and two strings whose weights have different parity differ in an odd number of bits. $\blacksquare$

## Consequences

- **Gray code generation is always possible.** For every $n \ge 1$ a list of all $n$-bit strings with one-bit steps exists, and for $n \ge 2$ it can be closed into a ring. This is the basis of [Gray code generation](/gray-code-generation/), and $\Gamma_n$ is computable in $O(1)$ time per step.
- **Products.** The proof uses only one fact about $Q_n$: $Q_{m+1}$ is two copies of $Q_m$ joined by a [perfect matching](/perfect-matching/) between copies of the same vertex. The same argument shows that if a graph $G$ with at least two vertices has a Hamiltonian path, then $G \times K_2$ has a Hamiltonian cycle.
- **Every even cycle length.** For $n \ge 2$ and each even $L$ with $4 \le L \le 2^n$, $Q_n$ contains a cycle of length exactly $L$. Write $L = 2m$ with $2 \le m \le 2^{n-1}$ and take the first $m$ entries $x_1, \ldots, x_m$ of $\Gamma_{n-1}$. Then $0x_1, \ldots, 0x_m, 1x_m, \ldots, 1x_1$ is a cycle of length $2m$, by the same four steps as in the proof. $Q_n$ has no odd cycle at all, because it is bipartite.
- **Paths between given ends.** By the parity lemma, a Hamiltonian path from $u$ to $v$ needs $u$ and $v$ to differ in an odd number of bits. Simmons (1978) proved that this condition is also sufficient for $n \ge 1$: the hypercube is Hamilton-laceable (Mütze, Section 2.3).
- **Ring embedding.** A parallel machine whose processors are the vertices of $Q_n$ can run a ring of $2^n$ processes with each ring link on one machine link: process $i$ goes to vertex $\Gamma_n[i] = i \oplus \lfloor i/2 \rfloor$.
- **Hamiltonian cycle problem.** Deciding whether a graph has a Hamiltonian cycle is NP-complete in general: see [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). The hypercube is one of the many families for which an explicit construction settles it.

## Tightness

- **The bound $n \ge 2$.** It is tight: $Q_1$ is a single edge, so it has a Hamiltonian path but no Hamiltonian cycle.
- **The parity condition.** It cannot be dropped. For $n = 2$, the strings 00 and 11 differ in two bits, and no Hamiltonian path joins them: both neighbors of 00 are also neighbors of 11, and a path from 00 to 11 through 01 and 10 would need an edge between 01 and 10, which differ in two bits.
- **Removing one vertex.** $Q_n$ minus any one vertex, $n \ge 1$, has $2^n - 1$ vertices, an odd number, and is still bipartite. So it has no Hamiltonian cycle, because a cycle in a bipartite graph has even length. The same holds for any set of strings of odd size with one-bit steps.
- **Number of cycles.** The theorem gives one cycle, but there are many. Counted with no start and no direction, $Q_n$ has 1, 6, 1344 and 906,545,760 Hamiltonian cycles for $n = 2, 3, 4, 5$, and $35{,}838{,}213{,}722{,}570{,}883{,}870{,}720$ for $n = 6$ (OEIS A066037). A brute force search over $Q_2$, $Q_3$ and $Q_4$ confirmed the first three numbers. No closed formula is known.

## History

The reflected code itself is old. Knuth (Section 7.2.1.1) points to a telegraph machine that Émile Baudot showed in 1878, to a U.S. patent of George Stibitz from 1943, and to a booklet of 1872 by Louis Gros on the Chinese ring puzzle, whose states follow the reflected code. The name comes from Frank Gray, whose 1953 patent on pulse code communication defined the code by reflection. The view of a Gray code as a Hamiltonian cycle of the $n$-cube is standard in the surveys of Savage (1997) and Mütze (2023), which use it as the model case of a combinatorial Gray code. The count for $n = 6$ is from Haanpää and Östergård (2014).

## References
