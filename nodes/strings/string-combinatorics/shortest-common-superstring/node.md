---
tag: DF9CKT
kind: problem
slug: shortest-common-superstring
name: Shortest common superstring
aliases:
- SCS
- Shortest common superstring problem
- shortest common superstring problem
area: strings/string-combinatorics
level: core
summary: Find the shortest string that contains every string in a given set as a substring.
model: word-ram
complexity:
  vars: {m: the number of strings, n: the total length of the strings}
  time: {exact: O(n + m^2 2^m)}
  space: {extra: O(n + m 2^m)}
prereqs: [overlap-graph]
see_also: [greedy-superstring-merge, greedy-shortest-common-superstring, shortest-common-superstring-np-hard, held-karp-algorithm, asymmetric-tsp, shortest-common-supersequence, overlap-layout-consensus, de-bruijn-assembly]
sources:
  - paper: doi:10.1016/0022-0000(80)90004-5
    title: John Gallant, David Maier and James A. Storer, On finding minimal length superstrings, Journal of Computer and System Sciences 20(1), 1980, 50-58
    locator: the NP-completeness of the superstring decision problem
  - paper: doi:10.1145/179812.179818
    title: Avrim Blum, Tao Jiang, Ming Li, John Tromp and Mihalis Yannakakis, Linear approximation of shortest superstrings, Journal of the ACM 41(4), 1994, 630-647
    locator: the reduction to overlap and distance graphs, the bound 4 for the greedy algorithm, the 3-approximation through cycle covers, and the MAX SNP-hardness
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 16, the shortest superstring problem (overlaps, the greedy algorithm and the cycle-cover approximation), and Section 7.10, the all-pairs suffix-prefix problem
  - paper: "Dan Gusfield, Gad M. Landau and Baruch Schieber, An efficient algorithm for the all pairs suffix-prefix problem, Information Processing Letters 41(4), 1992, 181-185"
    locator: the O(n + m^2) computation of all pairwise suffix-prefix overlaps
  - paper: "Marcin Mucha, Lyndon words and short superstrings, Proceedings of the 24th ACM-SIAM Symposium on Discrete Algorithms (SODA 2013), 958-972"
    locator: the approximation ratio 2 11/23
---

The shortest common superstring problem asks, for a set of strings, for a shortest string that contains each of them as a contiguous substring. After removing strings that occur inside others, an optimal superstring is obtained by laying the strings out in some order and overlapping each with the next as much as possible, so the problem is a maximum-weight Hamiltonian path in the [overlap graph](/overlap-graph/). It is NP-hard and even hard to approximate within some constant, but the greedy merge algorithm and cycle-cover methods give small constant factors. It models genome assembly from reads and data compression.

## In plain words

You have a pile of short strips of text, cut from one long text that you lost. Every strip is a copy of some stretch of the original, and strips may share pieces at their ends. You want the shortest text that could have produced all of them: every strip must appear somewhere inside it as one unbroken stretch.

To save room you put the strips in a row and slide each one as far as you can over the end of the one before it, as long as the shared letters agree. A strip that already sits inside another strip can be thrown away. The only real choice is the order of the strips, and with many strips there are far too many orders to try.

## Definition

Let $\Sigma$ be a finite [alphabet](/alphabet/); only equality of letters is used. Strings are indexed from 0.

**Input.** A finite set $S = \{s_1, \ldots, s_m\}$ of nonempty strings over $\Sigma$, of total length $n = \sum_i |s_i|$.

**Output.** A string $w$ of minimum length such that each $s_i$ is a substring (factor) of $w$. The decision version asks, for a given $K$, whether such a $w$ with $|w| \le K$ exists.

**Overlaps.** For strings $a \ne b$ let $\mathrm{ov}(a, b)$ be the length of the longest string that is a proper suffix of $a$ and a proper prefix of $b$. The *merge* of an order $s_{\pi(1)}, \ldots, s_{\pi(m)}$ is the string obtained by writing $s_{\pi(1)}$ and then, for each next string $s_{\pi(j+1)}$, appending it without its first $\mathrm{ov}(s_{\pi(j)}, s_{\pi(j+1)})$ letters.

**Reduction to a substring-free set.** If $s_i$ is a substring of $s_j$ with $i \ne j$, then every superstring of $S \setminus \{s_i\}$ is a superstring of $S$, so $s_i$ can be dropped. After dropping such strings, $S$ is *substring-free*.

**Theorem.** Let $S$ be substring-free with $m \ge 1$. Then
$$ \mathrm{SCS}(S) = \sum_i |s_i| - \max_{\pi} \sum_{j=1}^{m-1} \mathrm{ov}(s_{\pi(j)}, s_{\pi(j+1)}), $$
where the maximum is over all orders $\pi$, and the merge of a maximizing order is a shortest common superstring.

*Proof.* The merge of an order $\pi$ contains every $s_i$ and has length $\sum_i |s_i| - \sum_j \mathrm{ov}(s_{\pi(j)}, s_{\pi(j+1)})$, so the minimum is at most the right-hand side. Conversely, let $w$ be any common superstring and fix one occurrence of each $s_i$ in $w$, starting at $p_i$ and ending at $e_i = p_i + |s_i| - 1$. Two occurrences cannot start at the same position, since then the shorter string would be a prefix of the longer one; likewise they cannot end at the same position. If $p_i < p_j$ then $e_i < e_j$, since otherwise $s_j$ would lie inside $s_i$. So sorting the occurrences by start gives an order $\pi$ in which the ends also increase. For consecutive strings $a = s_{\pi(j)}$ and $b = s_{\pi(j+1)}$ with starts $p < q$, either $q > e_a$ and then $q - p \ge |a| \ge |a| - \mathrm{ov}(a, b)$, or the two occurrences share $o = e_a - q + 1$ positions with $0 < o < |a|$ and $o < |b|$, and then the last $o$ letters of $a$ equal the first $o$ letters of $b$, so $o \le \mathrm{ov}(a, b)$ and $q - p = |a| - o \ge |a| - \mathrm{ov}(a, b)$. Summing over $j$,
$$ |w| \ge e_{\pi(m)} - p_{\pi(1)} + 1 = \sum_{j=1}^{m-1} (p_{\pi(j+1)} - p_{\pi(j)}) + |s_{\pi(m)}| \ge \sum_i |s_i| - \sum_{j=1}^{m-1} \mathrm{ov}(s_{\pi(j)}, s_{\pi(j+1)}). \qquad \square $$

So on a substring-free set the problem is to find a Hamiltonian path of maximum weight in the complete directed graph on $S$ with arc weights $\mathrm{ov}(a, b)$, the [overlap graph](/overlap-graph/).

## Variants

- **Maximum compression.** Maximize the total overlap $\sum_i |s_i| - |w|$ instead of minimizing $|w|$. The two have the same optimal solutions but different approximation behaviour: the greedy algorithm achieves at least half the optimal overlap (Tarhio and Ukkonen; Turner).
- **Cyclic superstring.** Find a shortest cyclic string that contains every $s_i$ as a factor of the cycle. On a substring-free set this is a maximum-weight Hamiltonian cycle problem, and the minimum-weight cycle cover of the distance graph is its relaxation used by the approximation algorithms.
- **Superstrings with reversals.** In DNA assembly each read may come from either strand, so the superstring must contain each $s_i$ or its reverse complement.
- **Short strings.** When every $s_i$ has length at most 2 the problem is solvable in polynomial time, while Gallant, Maier and Storer showed that it stays NP-complete when the string lengths are bounded by a small constant.
- **Shortest common supersequence.** The letters of each $s_i$ need only appear in order, not contiguously; this is a different problem, the [shortest common supersequence](/shortest-common-supersequence/).

## Examples

- $S = \{$`cde`, `abc`, `eab`$\}$. The overlaps $\mathrm{ov}(a, b)$, row $a$ and column $b$, are as follows.

| $\mathrm{ov}$ | `cde` | `abc` | `eab` |
| --- | --- | --- | --- |
| `cde` | - | 0 | 1 |
| `abc` | 1 | - | 0 |
| `eab` | 0 | 2 | - |

The six orders have total overlaps 0, 3, 2, 0, 0, 3. The best total is 3, reached by `cde`, `eab`, `abc` and by `eab`, `abc`, `cde`, so the minimum length is $9 - 3 = 6$, with superstrings `cdeabc` and `eabcde`.

- $S = \{$`ab`, `bc`, `ca`$\}$: every order along the cycle has overlap $1 + 1$, and the answer has length 4, for instance `abca`.
- $S = \{$`ACGT`, `CGTA`, `GTAC`, `TACG`$\}$: consecutive rotations overlap in 3 letters, and the answer `ACGTACG` has length $16 - 9 = 7$.
- **Removing contained strings.** For $\{$`abcd`, `bc`, `cdx`$\}$ the string `bc` lies inside `abcd` and is dropped; the answer is `abcdx`.
- **Greedy is not optimal.** For $S_k = \{c(ab)^k, (ba)^k, (ab)^k c\}$ the largest overlap is $2k$, between $c(ab)^k$ and $(ab)^k c$. Merging these first gives $c(ab)^k c$, which shares nothing with $(ba)^k$, so the greedy result has length $4k + 2$. The order $c(ab)^k, (ba)^k, (ab)^k c$ has overlaps $2k - 1$ twice and gives length $2k + 4$, for instance `cabababc` when $k = 2$. The ratio tends to 2.

## Known algorithms

| algorithm | guarantee | time |
| --- | --- | --- |
| brute force over orders | exact | $O(n + m^2 + m! \cdot m)$ |
| dynamic programming over subsets ([Held-Karp](/held-karp-algorithm/)) | exact | $O(n + m^2 2^m)$ |
| [greedy merging](/greedy-superstring-merge/) | ratio at most 3.5 (conjectured 2) | $O(n + m^2 \log m)$ |
| cycle cover then merge (Blum et al.) | ratio at most 3 | polynomial |
| refined cycle-cover methods (Mucha 2013 and later) | ratio below 2.5 | polynomial |

- **Overlaps.** All $m^2$ values $\mathrm{ov}(a, b)$ can be computed naively with the [prefix function](/prefix-function/) of $b \# a$ in $O(|a| + |b|)$ time per pair, or all together in $O(n + m^2)$ time with a suffix tree or an [Aho-Corasick](/aho-corasick/) automaton (Gusfield, Landau and Schieber, 1992).
- **Exact dynamic programming.** Let $f(X, j)$ be the largest total overlap of an order of the set $X \subseteq S$ that ends with $s_j \in X$. Then $f(\{s_j\}, j) = 0$ and $f(X, j) = \max_{i \in X \setminus \{j\}} f(X \setminus \{s_j\}, i) + \mathrm{ov}(s_i, s_j)$. This is the [bitmask DP](/bitmask-dp/) of the traveling salesman problem and is practical up to about 20 strings.
- **Greedy.** Repeatedly merge the two strings with the largest overlap, removing strings that become substrings. Blum et al. (1994) proved the ratio 4, Kaplan and Shafrir (2005) improved the analysis to 3.5, and the *greedy conjecture* that the ratio is 2 is open; the example above shows that 2 cannot be improved.
- **Cycle cover.** A minimum-weight cycle cover of the distance graph, with weights $|a| - \mathrm{ov}(a, b)$, is an assignment problem, solvable in polynomial time. Opening each cycle and concatenating the results gives a superstring of length at most 3 times the optimum.

## Bounds

- **NP-hardness.** The decision version is NP-complete (Gallant, Maier and Storer, 1980), and it remains NP-complete over a binary alphabet; see [the NP-hardness of the shortest common superstring](/shortest-common-superstring-np-hard/).
- **Hardness of approximation.** Blum et al. (1994) showed that the problem is MAX SNP-hard, so there is no polynomial-time approximation scheme unless P = NP; explicit constants just above 1 are known.
- **Exact time.** The subset DP takes $2^m$ times a polynomial; since the problem is NP-hard, no polynomial-time exact algorithm is expected.
- **Trivial bounds.** $\max_i |s_i| \le \mathrm{SCS}(S) \le \sum_i |s_i|$, and after the reduction to a substring-free set, at least one letter per string is new, so $\mathrm{SCS}(S) \ge m$.

## Reductions

- **To the asymmetric traveling salesman problem.** By the theorem above, add a vertex joined to every string by arcs of overlap 0; a maximum-weight Hamiltonian cycle in this graph is a maximum-weight Hamiltonian path in the overlap graph. With distances $|a| - \mathrm{ov}(a, b)$ it becomes a minimum [asymmetric TSP](/asymmetric-tsp/) tour.
- **From Hamiltonian path.** The NP-hardness proof of Gallant, Maier and Storer encodes a directed [Hamiltonian path](/hamiltonian-path/) instance in strings whose overlaps mirror the arcs of the graph.
- **Spectrum strings.** If $S$ is the set of all factors of length $k$ of an unknown string, superstrings correspond to Eulerian walks in the de Bruijn graph; this is the idea behind [de Bruijn graph assembly](/de-bruijn-assembly/), which avoids the hard Hamiltonian formulation.

## Applications

- **Genome assembly.** Sequencing machines read short fragments of a long DNA molecule; the superstring model, with the [overlap-layout-consensus](/overlap-layout-consensus/) method and the [greedy assembler](/greedy-shortest-common-superstring/), was the first formal model of assembly. Repeats make the shortest superstring differ from the true genome, which is why practical assemblers use more information.
- **Data compression.** Storing a set of strings as one superstring with pointers saves space; the compression variant measures the saving.
- **Scheduling and test design.** Short sequences that contain given fragments, such as test inputs that must exercise given patterns, are superstring instances.

## References
