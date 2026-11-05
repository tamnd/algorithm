---
tag: EQVGFT
kind: problem
slug: de-bruijn-sequence
name: De Bruijn sequence
aliases:
- de Bruijn cycle
- universal cyclic string
area: strings/string-combinatorics
level: core
summary: A cyclic word of length k^n containing every word of length n exactly once as a window.
prereqs: [de-bruijn-graph]
see_also: [de-bruijn-existence-theorem, fkm-algorithm, de-bruijn-graph, hierholzer-algorithm, linear-feedback-shift-register, de-bruijn-bit-scan, shortest-common-superstring, necklace-enumeration]
sources:
  - paper: "Nicolaas G. de Bruijn, A combinatorial problem, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 49, 1946, 758-764"
    title: Nicolaas G. de Bruijn, A combinatorial problem
    locator: the binary cyclic sequences of length 2^n containing every word of length n, and their number 2^(2^(n-1) - n)
  - paper: doi:10.1112/jlms/s1-21.3.167
    title: Irving J. Good, Normal recurring decimals, Journal of the London Mathematical Society 21(3), 1946, 167-169
    locator: existence of such cyclic sequences through Eulerian circuits
  - paper: doi:10.1090/s0002-9904-1934-05988-3
    title: Monroe H. Martin, A problem in arrangements, Bulletin of the American Mathematical Society 40(12), 1934, 859-864
    locator: the greedy construction that always appends the largest letter that gives a new window
  - paper: doi:10.1016/0012-365X(78)90002-X
    title: Harold Fredricksen and James Maiorana, Necklaces of beads in k colors and k-ary de Bruijn sequences, Discrete Mathematics 23(3), 1978, 207-210
    locator: the concatenation of the Lyndon words whose length divides n, in lexicographic order
  - paper: doi:10.1137/1024041
    title: Harold Fredricksen, A survey of full length nonlinear shift register cycle algorithms, SIAM Review 24(2), 1982, 195-221
    locator: the survey of constructions (Eulerian circuits, the greedy and necklace methods, shift registers) and the history going back to Flye Sainte-Marie
  - paper: doi:10.1137/15m1043248
    title: Tomasz Kociumaka, Jakub Radoszewski and Wojciech Rytter, Efficient ranking of Lyndon words and decoding lexicographically minimal de Bruijn sequence, SIAM Journal on Discrete Mathematics 30(4), 2016, 2027-2046
    locator: finding the position of a given window in the lexicographically least de Bruijn sequence in polynomial time
  - paper: doi:10.1016/j.disc.2018.07.010
    title: Daniel Gabric, Joe Sawada, Aaron Williams and Dennis Wong, A framework for constructing de Bruijn sequences via simple successor rules, Discrete Mathematics 341(11), 2018, 2977-2987
    locator: successor rules that compute the next letter from the current window in O(n) time
---

A de Bruijn sequence of order $n$ over an alphabet of $k$ letters is a cyclic word of length $k^n$ in which every word of length $n$ appears exactly once as a window of $n$ consecutive letters. For $k = 2$ and $n = 3$, the cyclic word `00010111` has the 8 windows `000`, `001`, `010`, `101`, `011`, `111`, `110`, `100`. Such sequences exist for all $k$ and $n$, by the [de Bruijn existence theorem](/de-bruijn-existence-theorem/), and there are $(k!)^{k^{n-1}}/k^n$ of them. They are built in time linear in their length by an Eulerian circuit of the [de Bruijn graph](/de-bruijn-graph/), by the [FKM algorithm](/fkm-algorithm/), or by shift-register rules.

## In plain words

A keypad lock opens when the last $n$ digits typed are the code. Typing every code one after another takes $n$ times as many key presses as there are codes. A de Bruijn sequence does it with about one key press per code: each new key press, together with the $n - 1$ before it, forms a code not seen before, and every code shows up once. Written around a circle, it is the shortest circle of letters that shows every word of length $n$ in some window.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/) of $k \ge 1$ letters; only equality is needed, and for the constructions $\Sigma = \{0, \ldots, k-1\}$ with its usual order. Indices are 0-based and taken modulo the length for cyclic words. For a word $s$ of length $L$ and $0 \le i < L$, the cyclic window of length $n$ at $i$ is $s[i]\,s[(i+1) \bmod L] \cdots s[(i+n-1) \bmod L]$.

**De Bruijn sequence.** A word $s$ of length $L$ is a de Bruijn sequence of order $n \ge 1$ if its $L$ cyclic windows of length $n$ are pairwise distinct and are all of $\Sigma^n$. Then $L = k^n$. Two de Bruijn sequences that are rotations of each other define the same de Bruijn cycle; each cycle has exactly one rotation that starts with $0^n$.

**The problem.** Given $k$ and $n$, output a de Bruijn sequence of order $n$. Related tasks are to count them, to output the next letter from the last $n$ letters (a successor rule), and to decode: given a word $w \in \Sigma^n$, find the index of its window.

**Linear form.** The word $s\,s[0..n-2]$ of length $k^n + n - 1$ contains every word of length $n$ exactly once as an ordinary factor. No shorter word contains all $k^n$ words of length $n$ as factors, since a word of length $L$ has only $L - n + 1$ factors of length $n$.

## Variants

- **Universal cycles.** Chung, Diaconis and Graham asked for cyclic sequences in which each object of another family, such as permutations or $k$-subsets, appears once as a window in some encoding.
- **De Bruijn tori.** Two-dimensional arrays in which each $r \times c$ array over $\Sigma$ appears once as a window, used for absolute positioning on a plane.
- **Order $n$ windows without one word.** A binary maximal-length [linear feedback shift register](/linear-feedback-shift-register/) sequence has length $2^n - 1$ and contains every nonzero window once; it is a de Bruijn sequence with one 0 removed.
- **Shortest superstring of all words.** Without the cyclic condition, the problem is the [shortest common superstring](/shortest-common-superstring/) of $\Sigma^n$, and the linear form above is optimal.
- **Decoding.** Finding the index of a given window without generating the sequence; for the lexicographically least sequence it takes polynomial time in $n$ by ranking Lyndon words (Kociumaka, Radoszewski and Rytter).

## Examples

| $k$ | $n$ | a de Bruijn sequence | number of de Bruijn cycles |
|---|---|---|---|
| 2 | 1 | `01` | 1 |
| 2 | 2 | `0011` | 1 |
| 2 | 3 | `00010111` | 2 |
| 2 | 4 | `0000100110101111` | 16 |
| 2 | 5 | `00000100011001010011101011011111` | 2048 |
| 3 | 2 | `001021122` | 24 |
| 3 | 3 | `000100201101202102211121222` | 373248 |
| 4 | 2 | `0010203112132233` | 20736 |

The sequences in the table are the ones built by the [FKM algorithm](/fkm-algorithm/), the lexicographically least in each case. For $k = 2$ and $n = 3$, the only other cycle is `00011101`. The counts agree with $(k!)^{k^{n-1}}/k^n$: for example, $(3!)^{3}/3^2 = 24$ and $(2!)^{8}/2^4 = 16$.

**Not de Bruijn.** The cyclic word `00110` has length 5, not 4. The word `0101` has the right length for $k = 2$, $n = 2$, but its windows are `01`, `10`, `01`, `10`, so `00` and `11` are missing.

## Known algorithms

| method | time | extra space | output |
|---|---|---|---|
| Eulerian circuit of the de Bruijn graph on $\Sigma^{n-1}$ ([Hierholzer](/hierholzer-algorithm/)) | $\Theta(k^n)$ | $\Theta(k^n)$ | any cycle, depending on the edge order |
| greedy, prefer the largest letter (Martin, 1934) | $\Theta(k^n)$ expected with a hash set | $\Theta(k^n)$ | the cycle from $0^n$ that appends the largest letter giving a new window |
| [FKM algorithm](/fkm-algorithm/), Lyndon words in order | $\Theta(k^n)$ | $\Theta(n)$ | the lexicographically least sequence |
| maximal-length LFSR plus one 0 ($k$ prime) | $O(n)$ per letter, $O(1)$ with word operations | $\Theta(n)$ | a sequence from a [primitive polynomial](/primitive-polynomial/) over $\mathbb{F}_k$ |
| successor rules (Gabric, Sawada, Williams and Wong) | $O(n)$ per letter | $\Theta(n)$ | the next letter from the current window alone |

**Eulerian circuit.** In the de Bruijn graph with vertex set $\Sigma^{n-1}$ and an edge $x[0..n-2] \to x[1..n-1]$ for each $x \in \Sigma^n$, each vertex has in-degree and out-degree $k$, and the graph is strongly connected, so an Eulerian circuit exists. Its edge labels, read in order with the last letter of each, give a de Bruijn sequence.

**Greedy.** Start with $0^n$ and repeatedly append the largest letter whose new window has not been seen; stop when no letter works. For $k = 2$, $n = 3$ this gives `0001110100`, whose first 8 letters `00011101` form a de Bruijn sequence. The method always produces a full sequence, of linear length $k^n + n - 1$.

**Shift register.** For $k = 2$, $n = 3$, the recurrence $a_{t+3} = a_t + a_{t+1} \bmod 2$, from the polynomial $x^3 + x + 1$, gives the period `0010111`, which has the 7 nonzero windows. Inserting one 0 into the run of two 0s gives `00010111`.

## Bounds

- **Length.** Every cyclic word containing all of $\Sigma^n$ as windows has length at least $k^n$, and de Bruijn sequences reach it. As a linear word the optimum is $k^n + n - 1$.
- **Time.** Writing the sequence takes $\Omega(k^n)$ time, so the Eulerian, greedy and FKM methods are optimal; FKM also uses only $O(n)$ space besides the output.
- **Number.** There are $(k!)^{k^{n-1}}/k^n$ de Bruijn cycles of order $n$ over $k$ letters, so $2^{2^{n-1} - n}$ for $k = 2$. This comes from the BEST theorem, which counts the Eulerian circuits of a balanced directed graph through the [matrix-tree theorem](/matrix-tree-theorem/).

## Reductions

- **To Eulerian circuits.** A de Bruijn sequence of order $n$ is an [Eulerian circuit](/eulerian-circuit/) of the de Bruijn graph on $\Sigma^{n-1}$, and conversely: the windows are the edges.
- **To Hamiltonian cycles.** It is also a [Hamiltonian cycle](/hamiltonian-cycle/) of the de Bruijn graph on $\Sigma^n$, where the windows are the vertices. That graph is the [line graph](/line-graph/) of the one on $\Sigma^{n-1}$, which turns the Hamiltonian problem into an Eulerian one, solvable in linear time.
- **From necklaces.** The FKM construction reduces the problem to [necklace enumeration](/necklace-enumeration/): the Lyndon words whose length divides $n$, concatenated in lexicographic order.

## Applications

- **Lowest set bit.** Multiplying a power of two $2^i$ by a 64-bit constant whose binary digits form a de Bruijn sequence of order 6 starting with `000000`, and keeping the top 6 binary digits, gives a different value for each $i$; a table of 64 entries turns it into $i$. This is the [de Bruijn bit scan](/de-bruijn-bit-scan/).
- **Position sensing.** A ring or strip marked with a de Bruijn sequence lets a reader that sees $n$ consecutive marks know its absolute position, as in rotary encoders and structured-light scanners.
- **Brute-force testing.** Entering a de Bruijn sequence tries every code of length $n$ on a lock that checks only the last $n$ symbols, with $k^n + n - 1$ presses instead of $n k^n$.
- **Experimental design and probes.** Sequences in which each short context occurs once are used to balance stimuli in experiments and to design DNA probes that cover all $k$-mers.

## References
