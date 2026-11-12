---
tag: G2WSD1
kind: problem
slug: sequencing-by-hybridization
name: Sequencing by hybridization
aliases:
- SBH
- spectrum problem
area: biology/genome-assembly
level: advanced
summary: "Reconstruct a DNA string from the set of its l-mers read on a hybridization chip, as an Eulerian path in a de Bruijn graph or a Hamiltonian path on the l-mers."
prereqs: [kmer, de-bruijn-graph, eulerian-path]
see_also: [hamiltonian-path-problem, line-graph, hierholzer-algorithm, matrix-tree-theorem, de-bruijn-assembly, shortest-common-superstring-np-hard, kmer-spectrum, eulerian-superpath-problem]
sources:
  - paper: "Yu. P. Lysov, V. L. Florentiev, A. A. Khorlin, K. R. Khrapko, V. V. Shik and A. D. Mirzabekov, Determination of the nucleotide sequence of DNA using hybridization with oligonucleotides, a new method, Doklady Akademii Nauk SSSR, 1988"
    title: "Lysov et al., Determination of the nucleotide sequence of DNA using hybridization with oligonucleotides, 1988"
    locator: "the proposal of SBH, with reconstruction as a path through all l-mers of the spectrum"
  - paper: doi:10.1016/0888-7543(89)90290-5
    title: "Radoje Drmanac, Ivan Labat, Ivan Brukner and Radomir Crkvenjakov, Sequencing of megabase plus DNA by hybridization, theory of the method, Genomics 4(2), 1989"
    locator: "pp. 114 to 128, hybridization with short oligonucleotide probes and the reconstruction of the sequence from the probes that bind"
  - paper: doi:10.1080/07391102.1989.10507752
    title: "Pavel A. Pevzner, l-Tuple DNA sequencing, computer analysis, Journal of Biomolecular Structure and Dynamics 7(1), 1989"
    locator: "pp. 63 to 73, the l-mers as arcs between (l-1)-mers and reconstruction as an Eulerian path"
  - book: isbn:9780990374602
    title: "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Vol. 1, Active Learning Publishers, 2014"
    locator: "Chapter 3, string reconstruction from the k-mer composition with Hamiltonian and Eulerian paths in the de Bruijn graph"
---

Sequencing by hybridization (SBH) is the problem of reconstructing a DNA string from its $l$-mer spectrum, the set of all substrings of length $l$ that occur in it. A DNA chip that carries all $4^l$ probes of length $l$ measures this set, because the target binds to a probe only where the probe occurs in it. Lysov et al. (1988) and Drmanac et al. (1989) proposed the method, and Pevzner (1989) showed that the reconstruction is an Eulerian path problem, which has a linear-time algorithm.

## In plain words

You want to read a long word, but you cannot see it directly. You can only ask, for every short piece of a fixed length, "does this piece occur somewhere in the word?" The answer is a list of pieces, without their positions and without how many times each one occurs.

To rebuild the word, chain the pieces so that each piece continues the previous one by all of its letters except the first. One way is to visit every piece once, which is a hard search in general. A better way is to treat each piece as a step from its first part to its last part, and then to use every step once. This is the classic puzzle of drawing a figure without lifting the pen, and it has a fast solution. When the word repeats some parts, more than one word can fit the same list.

## Definition

**Model.** The target is an unknown string $s$ of length $n$ over $\{A, C, G, T\}$. In the terms of [genome assembly](/genome-assembly-problem/), the genome length is $G = n$, the probes that bind act as $N = n - l + 1$ reads of length $L = l$, and the coverage is $c = NL/G = (n - l + 1) l / n$, close to $l$. The error model of the basic problem is ideal hybridization: every $l$-mer of $s$ binds and no other probe binds. The spectrum is a set, so the chip gives no multiplicities and no positions. The graph is either the overlap graph on the $l$-mers or the [de Bruijn graph](/de-bruijn-graph/) on the $(l-1)$-mers.

**Spectrum.** For $l \le n$, the spectrum of $s$ is
$$\mathrm{Spec}(s, l) = \{\, s[i \,..\, i + l - 1] : 0 \le i \le n - l \,\}.$$

**Problem.** Input: a set $S$ of $l$-mers. Output: a string $s$ with $\mathrm{Spec}(s, l) = S$ in which each $l$-mer of $S$ occurs exactly once, so that $n = |S| + l - 1$. Also report whether this $s$ is unique, or the number of such strings.

**Hamiltonian form.** Let $H$ be the directed graph with one vertex for each $l$-mer of $S$ and an arc $u \to v$ when the last $l - 1$ letters of $u$ equal the first $l - 1$ letters of $v$. A solution is a Hamiltonian path in $H$, read off as the first $l$-mer followed by the last letter of each next $l$-mer. Lysov et al. (1988) gave the reconstruction in this form.

**Eulerian form.** Let $D$ be the directed multigraph whose vertices are the $(l-1)$-mers that occur as a prefix or a suffix of a member of $S$, with one arc $x[0..l-2] \to x[1..l-1]$ for each $x \in S$. A solution is an [Eulerian path](/eulerian-path/) in $D$: a walk that uses each arc once. This is the form of Pevzner (1989). The graph $H$ is the [line graph](/line-graph/) of $D$, so the Hamiltonian paths of $H$ are in one-to-one correspondence with the Eulerian paths of $D$.

## Variants

- **Spectrum with multiplicities.** If the chip also measures how many times each $l$-mer occurs, $D$ gets one arc for each occurrence, and the problem is still an Eulerian path in a multigraph.
- **Errors.** With false negatives, some $l$-mers of $s$ are missing from $S$; with false positives, $S$ contains $l$-mers that do not occur in $s$. The path must then use most of the arcs and may add or skip some, and the exact Eulerian reduction no longer applies. Methods for these versions are search or heuristics.
- **Positional SBH.** Each $l$-mer comes with an interval of possible positions in $s$. The intervals remove many of the alternative paths.
- **Gapped probes.** Probes with fixed letters and wildcard positions read pairs of letters at a distance larger than $l$, so they separate repeats that ordinary probes of the same number of fixed letters cannot.
- **Unknown target length.** If $s$ can repeat $l$-mers, $n$ is not given by $|S|$, and the problem asks for any string, or the shortest string, with spectrum $S$.

## Examples

**Two reconstructions.** Take $s = \texttt{ATGGCGTGCA}$ and $l = 3$. The spectrum has 8 distinct 3-mers:

$$S = \{\texttt{ATG}, \texttt{TGG}, \texttt{GGC}, \texttt{GCG}, \texttt{CGT}, \texttt{GTG}, \texttt{TGC}, \texttt{GCA}\}.$$

In the Eulerian form, the vertices are the 7 2-mers AT, TG, GG, GC, CG, GT and CA, and each 3-mer is one arc, for example ATG is the arc AT → TG. The vertices TG and GC each have in-degree 2 and out-degree 2. AT has one more outgoing arc than incoming arcs, and CA has one more incoming arc, so every Eulerian path goes from AT to CA. There are exactly two:

| Eulerian path | string |
|---|---|
| AT, TG, GG, GC, CG, GT, TG, GC, CA | ATGGCGTGCA |
| AT, TG, GC, CG, GT, TG, GG, GC, CA | ATGCGTGGCA |

Both strings have the spectrum $S$, so SBH with $l = 3$ cannot tell them apart. In the Hamiltonian form, $H$ has 8 vertices and 11 arcs, and the same two strings are its two Hamiltonian paths.

**Counting with the BEST theorem.** For a connected balanced directed multigraph, the BEST theorem gives the number of Eulerian circuits as
$$\mathrm{ec}(D) = t_w(D) \prod_{v} \bigl(\deg^+(v) - 1\bigr)!,$$
where $t_w(D)$ is the number of spanning arborescences directed towards any fixed vertex $w$, which the [matrix-tree theorem](/matrix-tree-theorem/) gives as a determinant. Since the arcs are distinct $l$-mers, the Eulerian paths from the start to the end correspond one to one to the Eulerian circuits of $D$ plus one arc from the end to the start. In the example, add the arc CA → AT. Take $w = \texttt{TG}$. Every vertex other than GC has one outgoing arc, and GC can use either GC → CG or GC → CA, and both lead to TG, so $t_w = 2$. The degrees give $1! \cdot 1! = 1$, so there are $2 \cdot 1 = 2$ reconstructions, as in the table. If $s$ starts and ends with the same $(l-1)$-mer, $D$ is balanced, and the number of strings is $|S| \cdot \mathrm{ec}(D)$, one for each arc at which the circuit can be cut.

**How often the answer is unique.** For uniform random strings with $l = 8$, which is a chip of $4^8 = 65536$ probes, 400 strings for each length with a fixed seed give these fractions, counted with the BEST theorem. The values are observed, not proved.

| $n$ | all 8-mers distinct | exactly one reconstruction |
|---|---|---|
| 50 | 0.9875 | 0.9875 |
| 100 | 0.9625 | 0.96 |
| 150 | 0.875 | 0.86 |
| 200 | 0.8375 | 0.7975 |
| 300 | 0.6325 | 0.4775 |
| 400 | 0.4475 | 0.21 |

## Known algorithms

- **Eulerian path, Pevzner (1989).** Build $D$ with a hash table of the $(l-1)$-mers in $O(l \cdot |S|)$ expected time, check the degree conditions and connectivity, and find the path with [Hierholzer's algorithm](/hierholzer-algorithm/) in $O(|S|)$ time. With a trie in place of the hash table the whole method is $O(l \cdot |S|)$ in the worst case, which is linear in the size of the input.
- **Hamiltonian path search, Lysov et al. (1988).** Search for a Hamiltonian path in $H$. The [Hamiltonian path problem](/hamiltonian-path-problem/) is NP-complete on general directed graphs, and a generic search takes exponential time in the worst case. It is not needed here, because $H$ is a line graph and the Eulerian algorithm solves the same instance.
- **Counting and uniqueness.** Contract every vertex of $D$ with in-degree 1 and out-degree 1 into the arcs through it. This keeps the number of arborescences. Then evaluate the BEST formula with one determinant of size $b - 1$, where $b$ is the number of remaining vertices, in $O(b^3)$ arithmetic operations in the worst case. Uniqueness is the test $\mathrm{ec} = 1$.
- **Enumeration.** List all Eulerian paths by backtracking over the choice of the next arc, with a time that grows with the number of reconstructions.

## Bounds

- **Time.** The Eulerian algorithm reads the input once and does constant work per arc after the hashing, so $O(l \cdot |S|)$ is optimal up to the cost of reading $S$. This bound is worst case.
- **Two causes of ambiguity.** Write an Eulerian path as a sequence of vertex visits. If the path visits $(l-1)$-mers $X \ne Y$ in the order $X, Y, X, Y$, it has the form $X \, W_1 \, Y \, M \, X \, W_2 \, Y$, where $W_1$ and $W_2$ are walks from $X$ to $Y$ and $M$ is a walk from $Y$ to $X$. Then $X \, W_2 \, Y \, M \, X \, W_1 \, Y$ uses the same arcs, so it gives a second string with the same spectrum; it is a different string, because $W_1$ and $W_2$ start with different arcs. In the example, $X = \texttt{TG}$, $Y = \texttt{GC}$, $W_1$ goes through GG and $W_2$ is the arc TGC. In the same way, a vertex $X$ visited three times splits the path into two closed walks at $X$, and exchanging them gives a second string.
- **Worst case length.** A string of length $n$ has $n - l + 2$ positions of $(l-1)$-mers. If $n - l + 2 > 2 \cdot 4^{l-1}$, some $(l-1)$-mer occurs three times, so by the last bound every such string with distinct $l$-mers has at least two reconstructions. For $l = 8$ this is $n > 32774$.
- **Expected length.** For a uniform random string, the expected number of pairs of positions with equal $(l-1)$-mers is about $\binom{n}{2} 4^{-(l-1)}$, a heuristic that ignores overlapping positions. A single repeated pair does not make the answer ambiguous, but two pairs can interleave, so a unique answer is typical while $n$ is below about $(2 \cdot 4^{l-1})^{1/2}$. For $l = 8$ this is about 181, and the observed table shows the drop between $n = 150$ and $n = 400$. A chip of $4^l$ probes thus reads strings of length of the order of $2^l$, far less than the number of probes.

## Reductions

- **To Eulerian path.** SBH with distinct $l$-mers is the Eulerian path problem on $D$, a subgraph of the de Bruijn graph of order $l - 1$.
- **From Hamiltonian path on a line graph.** The Hamiltonian form is the Hamiltonian path problem restricted to $H$, which is the line graph of $D$; on line graphs this restriction reduces back to Eulerian path, so the NP-hardness of the general problem does not transfer.
- **To shortest common superstring.** Two distinct $l$-mers overlap in at most $l - 1$ letters, so every superstring of $S$ has length at least $|S| + l - 1$. A solution of SBH is a superstring of exactly this length, so SBH with distinct $l$-mers is the question whether the [shortest common superstring](/shortest-common-superstring-np-hard/) of $S$ has length $|S| + l - 1$. The general superstring problem is NP-hard, and this special case is not.
- **To de Bruijn assembly.** [De Bruijn assembly](/de-bruijn-assembly/) cuts reads into $k$-mers and reconstructs the genome from the [k-mer spectrum](/kmer-spectrum/) with the same graph. The [Eulerian superpath problem](/eulerian-superpath-problem/) adds the constraint that each read must be a subpath.

## Applications

- DNA chips for resequencing and for the detection of known variants, where a reference sequence is known and the chip tests whether each expected $l$-mer is present.
- The model for the de Bruijn graph method of short-read assembly: there the reads give the $k$-mers with multiplicities and errors, and repeats longer than $k$ cause the same ambiguity as in SBH.
- A standard example in teaching of how a choice of graph turns an NP-complete formulation into a linear-time one.

## References
