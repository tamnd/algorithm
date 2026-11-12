---
tag: HZZDZJ
kind: theorem
slug: shortest-common-superstring-np-hard
name: NP-hardness of shortest common superstring
aliases:
- SCS is NP-hard
area: biology/genome-assembly
level: core
summary: The decision version of shortest common superstring is NP-complete, even over a binary alphabet, by a reduction from directed Hamiltonian path.
prereqs: [shortest-common-superstring, hamiltonian-path-problem, polynomial-time-reduction, np-complete]
see_also: [greedy-shortest-common-superstring, overlap-graph, held-karp-algorithm, asymmetric-tsp, de-bruijn-assembly, sequencing-by-hybridization, gadget-reduction, apx-class]
sources:
  - paper: doi:10.1016/0022-0000(80)90004-5
    title: John Gallant, David Maier and James A. Storer, On finding minimal length superstrings, Journal of Computer and System Sciences 20(1), 1980
    locator: pp. 50 to 58, the NP-completeness of the superstring decision problem by a reduction from a restricted directed Hamiltonian path problem
  - paper: doi:10.1145/179812.179818
    title: Avrim Blum, Tao Jiang, Ming Li, John Tromp and Mihalis Yannakakis, Linear approximation of shortest superstrings, Journal of the ACM 41(4), 1994
    locator: pp. 630 to 647, the MAX SNP-hardness of the problem and the factor 4 of the greedy algorithm
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Appendix A1.3, problem GT39 (Hamiltonian path, also for directed graphs), and Appendix A4, the shortest common superstring problem
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 16, the shortest superstring problem and its relation to fragment assembly
---

The NP-hardness theorem for the [shortest common superstring](/shortest-common-superstring/) says that it is [NP-complete](/np-complete/) to decide whether a set of strings has a common superstring of length at most a given bound, and that this stays true over a two-letter [alphabet](/alphabet/). Gallant, Maier and Storer proved it in 1980 by a [reduction](/polynomial-time-reduction/) from the directed [Hamiltonian path problem](/hamiltonian-path-problem/). The theorem is the reason why no assembler computes a shortest superstring of its reads exactly, and why the first assembly models led to heuristics such as the [greedy merge](/greedy-shortest-common-superstring/).

## Statement

**Problem SCS.** The input is a finite alphabet $\Sigma$, a finite set $S$ of nonempty strings over $\Sigma$, and an integer $K$. The question is whether there is a string $w$ with $|w| \le K$ that contains each string of $S$ as a contiguous substring. The size of the input is $\|S\| = \sum_{s \in S} |s|$ plus the length of $K$ in binary.

**Theorem.** SCS is NP-complete. It stays NP-complete when $\Sigma = \{0, 1\}$ is fixed.

**Notation.** For strings $a \ne b$, $\mathrm{ov}(a, b)$ is the length of the longest proper suffix of $a$ that is also a proper prefix of $b$. A set is *substring-free* if no string of it occurs inside another. For a substring-free set $S = \{s_1, \ldots, s_N\}$, the [problem page](/shortest-common-superstring/) proves the merge formula
$$ \mathrm{SCS}(S) = \|S\| - \max_{\pi} \sum_{j=1}^{N-1} \mathrm{ov}(s_{\pi(j)}, s_{\pi(j+1)}), $$
where $\pi$ ranges over all orders of $S$. The maximum is the *maximum total overlap* $\mathrm{MO}(S)$. The proof below uses this formula and no other fact about superstrings.

The construction below is a variant of the one by Gallant, Maier and Storer. It uses strings of length 4; their construction uses strings of length 3.

## In plain words

A puzzle about strings can hide a puzzle about maps. Take a road map with one-way roads, and ask for a route that visits every town exactly one time. Most experts believe that no fast method exists for this map puzzle.

The proof turns any such map into a set of short strings. Each town gets a few strings that chain together well only in a fixed circular order, plus one short string that marks the entrance to the town. A town can hand over to the entrance string of a next town only when a road leads there. The strings fit into a short enough common string exactly when the towns can be visited in one route along the roads. A fast method for the string puzzle would thus also solve the map puzzle. A last step rewrites every letter as a block of zeros and ones.

## Proof

**Membership in NP.** Let $S'$ be $S$ with each string removed that occurs inside another string of $S$; the two sets have the same superstrings, and $S'$ can be computed in polynomial time. A [certificate](/certificate/) is an order $\pi$ of $S'$. The verifier computes the overlaps of consecutive strings and accepts when $\|S'\| - \sum_j \mathrm{ov}(s_{\pi(j)}, s_{\pi(j+1)}) \le K$. By the merge formula, an accepting order exists exactly when $\mathrm{SCS}(S) \le K$. The certificate has polynomial size and the check takes polynomial time.

**The source problem.** The input of directed Hamiltonian path is a directed graph $G = (V, A)$ with $n = |V| \ge 1$, and the question is whether some order $y_1, \ldots, y_n$ of all vertices has $(y_j, y_{j+1}) \in A$ for $1 \le j < n$. It is NP-complete (Garey and Johnson, GT39). Self-loops never occur in such a path, so we delete them. Let $m = |A|$ after the deletion.

**Construction.** Fix an order of the out-neighbours of each vertex $v$, say $w_0, \ldots, w_{d_v - 1}$, where $d_v$ is the out-degree of $v$. Let the list $L_v = (w_0, \ldots, w_{d_v - 1}, \$)$ have $D_v = d_v + 1$ entries, where $\$$ is one fresh symbol shared by all lists. The alphabet is $\Sigma = \{ v, \bar v : v \in V \} \cup \{\$\}$, with $2n + 1$ symbols. All indices of $L_v$ are taken modulo $D_v$. The set $S$ has two kinds of strings:

- the *gadget* strings $x_{v,i} = \bar v \; L_v[i] \; \bar v \; L_v[i+1]$ for $v \in V$ and $0 \le i < D_v$, each of length 4;
- the *connector* strings $c_v = v \, \bar v$ for $v \in V$, each of length 2.

So $S$ has $N = \sum_v D_v + n = m + 2n$ strings and $\|S\| = 4(m + n) + 2n$. Set the bound to
$$ K = \|S\| - (2m + 2n - 1) = 2m + 4n + 1. $$
The construction takes time polynomial in $n + m$.

**Lemma 1 (overlaps).** For distinct $a, b \in S$:

1. $\mathrm{ov}(x_{v,i}, x_{v,i+1}) = 2$ when $D_v \ge 2$;
2. $\mathrm{ov}(x_{v,i}, c_w) = 1$ when $L_v[i+1] = w$;
3. $\mathrm{ov}(c_u, x_{u,i}) = 1$ for each $i$;
4. $\mathrm{ov}(a, b) = 0$ for all other pairs.

Also, $S$ is substring-free.

*Proof.* In a gadget string, positions 0 and 2 hold a barred symbol and positions 1 and 3 hold an unbarred vertex or $\$$. A connector has an unbarred symbol at position 0 and a barred one at position 1.

- Gadget to gadget, $a = x_{v,i}$, $b = x_{u,j}$. A length-1 overlap compares the last symbol of $a$ (not barred) with the first of $b$ (barred), so it fails. A length-3 overlap compares position 1 of $a$ (not barred) with position 0 of $b$ (barred), so it fails. A length-2 overlap needs $\bar v \, L_v[i+1] = \bar u \, L_u[j]$, so $u = v$ and $L_v[j] = L_v[i+1]$. The entries of $L_v$ are distinct, so $j = i + 1 \bmod D_v$, and $a \ne b$ forces $D_v \ge 2$. This gives item 1.
- Gadget to connector. Only length 1 is possible, and it needs the last symbol $L_v[i+1]$ of $a$ to equal the first symbol $w$ of $c_w$. This gives item 2.
- Connector to gadget. Only length 1 is possible, and it needs $\bar u = \bar v$. This gives item 3.
- Connector to connector. The barred last symbol of $c_u$ differs from the unbarred first symbol of $c_w$.

For substring-freeness: the gadget strings are distinct and of equal length, so none is inside another. A connector $u \bar u$ inside $x_{v,i}$ needs an unbarred symbol followed by a barred one, which occurs only at positions 1 and 2, so $u = L_v[i]$ and $\bar u = \bar v$. Then $v$ is its own out-neighbour, which is a deleted self-loop. A gadget is longer than a connector. $\square$

**Lemma 2 (upper bound).** Every order $\pi$ of $S$ has total overlap at most $2m + 2n - 1$. If equality holds, then every consecutive pair of $\pi$ has a positive overlap, and the $D_v$ gadget strings of each vertex $v$ occupy consecutive positions of $\pi$.

*Proof.* Let $p$ be the number of consecutive pairs of $\pi$ with overlap 2 and $q$ the number with overlap 1. By Lemma 1 no overlap exceeds 2, so the total is $2p + q$ and $p + q \le N - 1$. A pair with overlap 2 is a pair $(x_{v,i}, x_{v,i+1})$, an arc of the directed cycle $x_{v,0} \to x_{v,1} \to \cdots \to x_{v,D_v - 1} \to x_{v,0}$. The consecutive pairs of $\pi$ form a path, and a path contains no cycle, so at most $D_v - 1$ of these arcs are consecutive pairs of $\pi$. Hence $p \le \sum_v (D_v - 1) = m$, and
$$ 2p + q \le p + (N - 1) \le m + (m + 2n - 1) = 2m + 2n - 1. $$
Equality forces $p + q = N - 1$, so every consecutive pair has a positive overlap, and it forces exactly $D_v - 1$ consecutive pairs inside the $D_v$ gadget strings of $v$. A set of $k$ positions of a sequence that contains $k - 1$ adjacent pairs is one interval, since the number of adjacent pairs inside it is $k$ minus its number of maximal runs. $\square$

**Lemma 3 (path gives order).** If $G$ has a Hamiltonian path, then $\mathrm{MO}(S) = 2m + 2n - 1$.

*Proof.* Let $y_1, \ldots, y_n$ be the path. For $j < n$ the vertex $y_{j+1}$ is an out-neighbour of $y_j$, so $y_{j+1} = L_{y_j}[r_j]$ for some $r_j$; set $r_n = d_{y_n}$, the index of $\$$. Let $B_j$ be the gadget strings of $y_j$ in cyclic order from $x_{y_j, r_j}$ to $x_{y_j, r_j - 1}$. The last string $x_{y_j, r_j - 1}$ ends with $L_{y_j}[r_j]$, which is $y_{j+1}$ when $j < n$. Take the order
$$ c_{y_1}, B_1, c_{y_2}, B_2, \ldots, c_{y_n}, B_n. $$
By Lemma 1 each step from $c_{y_j}$ into $B_j$ has overlap 1, each of the $D_{y_j} - 1$ steps inside $B_j$ has overlap 2, and each step from the end of $B_j$ to $c_{y_{j+1}}$ has overlap 1. The total is $n + 2\sum_v (D_v - 1) + (n - 1) = 2m + 2n - 1$, and Lemma 2 shows that no order does better. $\square$

**Lemma 4 (order gives path).** If $\mathrm{MO}(S) = 2m + 2n - 1$, then $G$ has a Hamiltonian path.

*Proof.* Take an order $\pi$ with this total. By Lemma 2 the gadget strings of each vertex $v$ form one block $B_v$ of consecutive positions, and every consecutive pair has a positive overlap. By Lemma 1 the step from the last string of a block $B_v$ to the first string of a block $B_u$ with $u \ne v$ has overlap 0, and so does a step from a connector to a connector. So blocks and connectors alternate. There are $n$ of each, so $\pi$ has one of two forms.

- $c_{u_1}, B_{y_1}, c_{u_2}, B_{y_2}, \ldots, c_{u_n}, B_{y_n}$. A step from $c_{u_j}$ into $B_{y_j}$ has positive overlap only if $y_j = u_j$ (item 3). A step from $B_{y_j}$ to $c_{u_{j+1}}$ has positive overlap only if the last string of $B_{y_j}$ ends with $u_{j+1}$ (item 2), that is, only if $u_{j+1}$ is an out-neighbour of $y_j$. So $(y_j, y_{j+1}) \in A$ for all $j < n$.
- $B_{y_1}, c_{u_1}, B_{y_2}, c_{u_2}, \ldots, B_{y_n}, c_{u_n}$. The same two rules give $u_j = y_{j+1}$ and $(y_j, u_j) \in A$ for $j < n$, so again $(y_j, y_{j+1}) \in A$.

In both cases the blocks belong to distinct vertices, so $y_1, \ldots, y_n$ lists every vertex once and is a Hamiltonian path. $\square$

**NP-hardness over $2n + 1$ letters.** $S$ is substring-free by Lemma 1, so the merge formula gives $\mathrm{SCS}(S) \le K$ if and only if $\mathrm{MO}(S) \ge 2m + 2n - 1$. By Lemmas 2, 3 and 4 this holds if and only if $G$ has a Hamiltonian path.

**Binary alphabet.** Number the $2n + 1$ symbols with $r = \lceil \log_2(2n + 1) \rceil$ binary digits. Map the symbol with digits $e_1 \cdots e_r$ to the codeword
$$ h(\sigma) = 1\,1\,0\,e_1\,0\,e_2 \cdots 0\,e_r\,0, $$
of length $\ell = 2r + 3$, and extend $h$ to strings letter by letter. In a concatenation of codewords, the factor $11$ occurs only at the start of a codeword: inside a codeword every pair of adjacent positions after the first one contains a 0, and a codeword ends with 0. Codewords have fixed length and are distinct, so $h$ is injective on strings.

- If $h(a)$ occurs in $h(b)$, then the occurrence starts with $11$, so it starts at a codeword boundary and covers whole codewords, and $a$ occurs in $b$. So $h(S)$ is substring-free.
- Let $k = \mathrm{ov}(h(a), h(b)) > 0$. The overlap cannot be 1, since $h(a)$ ends with 0 and $h(b)$ starts with 1. So $k \ge 2$, the shared part starts with $11$, and it starts at a codeword boundary of $h(a)$. Thus $k = j\ell$, and the last $j$ symbols of $a$ equal the first $j$ symbols of $b$, with $j < \min(|a|, |b|)$. Conversely, a symbol overlap of $j$ gives a binary overlap of $j\ell$. So $\mathrm{ov}(h(a), h(b)) = \ell \cdot \mathrm{ov}(a, b)$.

By the merge formula, $\mathrm{SCS}(h(S)) = \ell \cdot \mathrm{SCS}(S)$, so the instance $(\{0, 1\}, h(S), \ell K)$ is a yes-instance exactly when $G$ has a Hamiltonian path. Its size is $O((m + n) \log n)$. $\blacksquare$

**Example.** Take the path $a \to b \to c$ with $n = 3$ and $m = 2$, so $K = 17$. The strings are $\bar a b \bar a \$$, $\bar a \$ \bar a b$, $\bar b c \bar b \$$, $\bar b \$ \bar b c$, $\bar c \$ \bar c \$$, $a \bar a$, $b \bar b$ and $c \bar c$, with total length 26. The order of Lemma 3 is $a \bar a$, $\bar a b \bar a \$$, $\bar a \$ \bar a b$, $b \bar b$, $\bar b c \bar b \$$, $\bar b \$ \bar b c$, $c \bar c$, $\bar c \$ \bar c \$$, with overlaps $1, 2, 1, 1, 2, 1, 1$. Its merge has $26 - 9 = 17$ symbols:
$$ a\,\bar a\,b\,\bar a\,\$\,\bar a\,b\,\bar b\,c\,\bar b\,\$\,\bar b\,c\,\bar c\,\$\,\bar c\,\$ $$
For the graph with arcs $a \to b$ and $a \to c$ only, which has no Hamiltonian path, the same construction gives 8 strings of total length 26 and a shortest superstring of length 18. With $r = 3$ digits for the 7 symbols, the binary codewords have length $\ell = 9$, and the binary instance of the path graph has a shortest superstring of length $153 = 9 \cdot 17$.

## Consequences

- **No exact polynomial algorithm unless P = NP.** An exact assembler that returns a shortest superstring of its reads solves an [NP-hard](/np-hard/) problem. The exact methods take exponential time, such as the [Held-Karp](/held-karp-algorithm/) subset dynamic program in $O(\|S\| + N^2 2^N)$ time, which is practical only for about 20 strings.
- **Maximum overlap is hard too.** The proof decides SCS through $\mathrm{MO}(S)$, so deciding whether a set of strings has total overlap at least a given value is also NP-complete. This is the maximum-weight Hamiltonian path in the [overlap graph](/overlap-graph/).
- **Hardness of approximation.** Blum, Jiang, Li, Tromp and Yannakakis (1994) proved that the problem is MAX SNP-hard. So there is no [polynomial-time approximation scheme](/ptas/) unless P = NP. Constant-factor approximations do exist, so the problem lies in [APX](/apx-class/).
- **Assembly needs a different model.** The superstring model is hard, and it also collapses repeats of the genome into one copy. These two facts moved assembly towards graph models in which the hard step disappears or is replaced by a heuristic, such as the [de Bruijn graph](/de-bruijn-assembly/) model and the [string graph](/string-graph/).

## Tightness

- **String length.** When every string has length at most 2, SCS can be solved in polynomial time (Gallant, Maier and Storer). Their reduction shows NP-completeness when every string has length 3, so length 3 is the exact boundary. The construction on this page uses length 4 over $2n + 1$ letters, and length $4\ell$ over two letters.
- **Alphabet size.** Over one letter the answer is the longest input string, so the problem is trivial. Two letters are already enough for NP-completeness.
- **Spectrum inputs.** If $S$ is the set of all length-$k$ substrings of some string, superstrings of the right kind correspond to Eulerian paths in a de Bruijn graph, and these can be found in linear time; see [sequencing by hybridization](/sequencing-by-hybridization/). The hardness needs inputs that are not spectra.
- **Approximation.** The greedy algorithm has ratio at most 3.5 (Kaplan and Shafrir, 2005), and cycle-cover methods reach ratios below 2.5. The gap between these upper bounds and the inapproximability constants, which are only slightly above 1, is open.

## History

Gallant, Maier and Storer published the NP-completeness proof in the Journal of Computer and System Sciences in 1980; the list of NP-complete problems in the book of Garey and Johnson (1979) already contains the problem. The first constant-factor approximation, and the MAX SNP-hardness, came from Blum, Jiang, Li, Tromp and Yannakakis, first at STOC 1991 and then in the Journal of the ACM in 1994. Gusfield's textbook of 1997 presents the problem as the first formal model of shotgun fragment assembly and discusses why the shortest superstring is not always the true genome.

## References
