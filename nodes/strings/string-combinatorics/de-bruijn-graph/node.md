---
tag: ZCP03V
kind: data-structure
slug: de-bruijn-graph
name: de Bruijn graph
aliases:
- De Bruijn graph
- de Bruijn graph of k-mers
- de Bruijn graph of order k
area: strings/string-combinatorics
level: core
summary: Graph whose vertices are (k-1)-mers and whose edges are k-mers of the reads.
model: word-ram
complexity:
  vars: {N: the total length of the reads, K: the k-mer length, m: the number of distinct K-mers, σ: the alphabet size, w: the number of edges of a walk}
  time: {build: O(N·K) expected, add: O(K) expected, successors: O(σ·K) expected, spell: O(K + w)}
  space: {extra: O(m·K)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [kmer, directed-graph, hash-table]
see_also: [de-bruijn-sequence, de-bruijn-existence-theorem, de-bruijn-assembly, eulerian-path, hierholzer-algorithm, overlap-graph, unitig, line-graph]
sources:
  - paper: "Nicolaas G. de Bruijn, A combinatorial problem, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 49, 1946, 758-764"
    title: Nicolaas G. de Bruijn, A combinatorial problem
    locator: the graph on binary words of length n - 1 with an edge for each word of length n, and the count of its Eulerian circuits
  - paper: doi:10.1112/jlms/s1-21.3.167
    title: Irving J. Good, Normal recurring decimals, Journal of the London Mathematical Society 21(3), 1946, 167-169
    locator: the same graph, used to show that cyclic sequences containing every word of length n once exist
  - paper: doi:10.1089/cmb.1995.2.291
    title: Ramana M. Idury and Michael S. Waterman, A new algorithm for DNA sequence assembly, Journal of Computational Biology 2(2), 1995, 291-306
    locator: the graph of the k-tuples of the reads and assembly as a walk through it
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, Proceedings of the National Academy of Sciences 98(17), 2001, 9748-9753
    locator: the de Bruijn graph of the reads, Eulerian paths and superpaths, and the handling of repeats and errors
  - paper: doi:10.1038/nbt.2023
    title: Phillip E. C. Compeau, Pavel A. Pevzner and Glenn Tesler, How to apply de Bruijn graphs to genome assembly, Nature Biotechnology 29(11), 2011, 987-991
    locator: the comparison of the Hamiltonian overlap-graph view with the Eulerian de Bruijn view of assembly
  - paper: doi:10.1007/978-3-642-33122-0_18
    title: Alexander Bowe, Taku Onodera, Kunihiko Sadakane and Tetsuo Shibuya, Succinct de Bruijn graphs, Algorithms in Bioinformatics (WABI 2012), Lecture Notes in Computer Science 7534, 2012, 225-235
    locator: the succinct representation of the edges by a sorted list of last letters with rank and select
---

A de Bruijn graph of order $K$ has the words of length $K - 1$ as vertices and one directed edge for each word $x$ of length $K$, from its prefix $x[0..K-2]$ to its suffix $x[1..K-1]$. Built from all $\sigma^K$ words, it is the complete de Bruijn graph, whose Eulerian circuits are exactly the [de Bruijn sequences](/de-bruijn-sequence/) of order $K$. Built from the [$K$-mers](/kmer/) of a set of sequencing reads, it is the main data structure of [de Bruijn assembly](/de-bruijn-assembly/): each walk spells a string whose $K$-mers are the edges it uses, so a genome appears as a walk that uses the edges. A [hash table](/hash-table/) from each vertex to its out-edges stores it in space proportional to the number of distinct $K$-mers.

## In plain words

Cut every read into all its pieces of length $K$. Each piece becomes an arrow, going from its first $K - 1$ letters to its last $K - 1$ letters. Arrows that share an end are joined there, so two pieces that overlap by $K - 1$ letters become consecutive arrows. Walking along arrows and writing down the last letter of each new stop spells a longer string, and every piece of length $K$ of that string is an arrow on the walk. So rebuilding a genome from its reads becomes finding a walk that uses the arrows. If every possible piece is an arrow, a walk that uses each arrow once spells a circular string that contains every possible piece exactly once.

## The abstract type

The alphabet $\Sigma$ is finite with $\sigma$ letters, used only as keys; no order is needed. Indices are 0-based. Fix $K \ge 2$. A $K$-mer is a word of length $K$. For a multiset $X$ of $K$-mers, the de Bruijn graph $G_K(X)$ is the directed multigraph with

- vertex set: the words $x[0..K-2]$ and $x[1..K-1]$ for $x \in X$;
- one edge $x[0..K-2] \to x[1..K-1]$ for each distinct $x \in X$, labeled by $x$ and with multiplicity the number of copies of $x$ in $X$.

For a set of reads $R$, $X$ is the multiset of all $K$-mers $r[i..i+K-1]$ of all reads $r \in R$. The complete de Bruijn graph $B(\sigma, K - 1)$ is $G_K(\Sigma^K)$: it has $\sigma^{K-1}$ vertices, $\sigma^K$ edges, and in-degree and out-degree $\sigma$ at each vertex. An edge leaving $u$ is determined by its last letter $c$, and it goes to $u[1..K-2]\,c$.

The operations are:

- **ADD-KMER$(x)$.** Add one copy of the $K$-mer $x$.
- **ADD-READ$(r)$.** Add all $K$-mers of the read $r$; a read shorter than $K$ adds nothing.
- **SUCCESSORS$(u)$** and **PREDECESSORS$(v)$.** The vertices joined to $u$ by an out-edge, and to $v$ by an in-edge.
- **SPELL$(v_0, \ldots, v_w)$.** For a walk, the string $v_0$ followed by the last letter of each later vertex.

A walk $v_0 \to v_1 \to \cdots \to v_w$ is a sequence of vertices with an edge from each $v_{t-1}$ to $v_t$.

## Representation

- **Out-table.** A hash table that maps each vertex $u$ to a small table $\mathrm{out}[u]$ from letters $c$ to the multiplicity of the edge $u \to u[1..K-2]\,c$.
- **In-table.** The same for in-edges: $\mathrm{in}[v]$ maps a letter $a$ to the multiplicity of the $K$-mer $a\,v$, the edge from $a\,v[0..K-3]$ to $v$.
- **Vertices.** The keys of both tables; a vertex with no out-edge still has an empty out-table.

Only the vertices are stored as strings. An edge is the pair of a vertex and a letter, so the space is $O(mK)$ letters for $m$ distinct $K$-mers, plus $O(m)$ counters. Packing each vertex into $\lceil (K-1) \log_2 \sigma \rceil$ binary digits of a machine word makes the hash keys integers when they fit.

## Operations

```pseudo id=main
ADD-KMER(x)                              ▷ |x| = K
L1  u ← x[0 .. K − 2], v ← x[1 .. K − 1]
L2  create empty out[u], in[u], out[v], in[v] if missing
L3  out[u][x[K − 1]] ← out[u][x[K − 1]] + 1
L4  in[v][x[0]] ← in[v][x[0]] + 1
ADD-READ(r)
L5  for i ← 0 to |r| − K do ADD-KMER(r[i .. i + K − 1])
SUCCESSORS(u)
L6  return the list of u[1 .. K − 2] c for each key c of out[u]
PREDECESSORS(v)
L7  return the list of a v[0 .. K − 3] for each key a of in[v]
SPELL(v_0, ..., v_w)                     ▷ a walk in the graph
L8  s ← v_0
L9  for t ← 1 to w do append the last letter of v_t to s
L10 return s
```

Line L5 slides a window of length $K$ over the read. Lines L6 and L7 rebuild the neighbors from the stored letters. Line L9 adds one letter per edge: consecutive vertices of a walk overlap in $K - 2$ letters, so only the last letter of $v_t$ is new.

## Example

Let $K = 3$ and let the reads be `ACGTCG` and `GTCGAT`, two overlapping pieces of `ACGTCGAT`. Their 3-mers are `ACG`, `CGT`, `GTC`, `TCG` and `GTC`, `TCG`, `CGA`, `GAT`. So `GTC` and `TCG` have multiplicity 2, and the other four have multiplicity 1.

| vertex | in-edges | out-edges |
|---|---|---|
| `AC` | none | `ACG` to `CG` |
| `CG` | `ACG` from `AC`, `TCG` from `TC` | `CGT` to `GT`, `CGA` to `GA` |
| `GT` | `CGT` from `CG` | `GTC` to `TC` |
| `TC` | `GTC` from `GT` | `TCG` to `CG` |
| `GA` | `CGA` from `CG` | `GAT` to `AT` |
| `AT` | `GAT` from `GA` | none |

The vertex `CG` is a branch: it is reached twice, once from `AC` and once around the cycle `CG` $\to$ `GT` $\to$ `TC` $\to$ `CG`, which is the repeat `CG` of the genome. The walk `AC` $\to$ `CG` $\to$ `GT` $\to$ `TC` $\to$ `CG` $\to$ `GA` $\to$ `AT` uses each distinct edge once, and SPELL gives `AC` followed by `G`, `T`, `C`, `G`, `A`, `T`, that is, `ACGTCGAT`. The other way out of `CG` first, `AC` $\to$ `CG` $\to$ `GA` $\to$ `AT`, spells `ACGAT` and leaves the cycle unused.

In the complete graph $B(2, 2)$ over $\{0, 1\}$, the vertices are `00`, `01`, `10`, `11` and the 8 edges are the binary 3-mers. The circuit `00` $\to$ `00` $\to$ `01` $\to$ `10` $\to$ `01` $\to$ `11` $\to$ `11` $\to$ `10` $\to$ `00` uses each edge once and spells `0001011100`; its first 8 letters, `00010111`, read cyclically, contain each binary word of length 3 once.

## Correctness

The invariant is that, after any sequence of ADD-KMER calls with the multiset $X$, $\mathrm{out}[u][c]$ is the number of copies of $u\,c$ in $X$, $\mathrm{in}[v][a]$ is the number of copies of $a\,v$ in $X$, and the keys are the vertices of $G_K(X)$. Each call changes exactly the two counters of its $K$-mer and adds its two end vertices, so the invariant holds by induction, and SUCCESSORS and PREDECESSORS read the edges off the tables. The spelling lemma says that a string $s$ of length at least $K$ is spelled by a walk if and only if every $K$-mer of $s$ is an edge, and then the walk is $s[0..K-2], s[1..K-1], \ldots$, and its $t$-th edge is the $K$-mer $s[t-1..t+K-2]$. So an Eulerian walk of $G_K(X)$ spells a string whose $K$-mers are exactly the distinct $K$-mers of $X$, each once. The full proof is in the proof file.

## Complexity

- **ADD-KMER.** Two slices of length $K - 1$ and four hash operations on keys of length $K - 1$: $O(K)$ expected time. With vertices packed in machine words and updated by shifts, it is $O(1)$ expected.
- **BUILD.** ADD-READ over reads of total length $N$ calls ADD-KMER at most $N$ times: $O(NK)$ expected, or $O(N)$ expected with packed or rolling keys.
- **SUCCESSORS and PREDECESSORS.** At most $\sigma$ neighbors, each built in $O(K)$: $O(\sigma K)$. The degree alone costs $O(K)$ for the lookup.
- **SPELL.** $O(K + w)$ for a walk of $w$ edges, plus the check that it is a walk if that is wanted.
- **Space.** At most $2m$ vertices for $m$ distinct $K$-mers, each stored once as a key: $O(mK)$ letters and $O(m)$ counters. The complete graph has $\sigma^{K-1}$ vertices and does not need to be stored, since its edges are known.

## Variants

- **Node-centric graph.** Some assemblers use the $K$-mers as vertices and join two $K$-mers when they overlap in $K - 1$ letters. This is the [line graph](/line-graph/) of the graph above; it loses the multiplicities but makes each $K$-mer a vertex.
- **Bidirected graph.** For DNA, a $K$-mer and its reverse complement are stored as one canonical vertex, and edges record which strand they use.
- **Compacted graph.** Each maximal non-branching path is merged into one vertex, a [unitig](/unitig/). The compacted graph has far fewer vertices and the same set of spelled strings.
- **Succinct graph.** Bowe, Onodera, Sadakane and Shibuya store the edges as a sorted array of last letters with rank and select support, in the style of the [Burrows-Wheeler transform](/burrows-wheeler-transform/), using a few binary digits per edge for DNA instead of a hash table entry.
- **Complete graph $B(\sigma, n)$.** The graph on all words of length $n$ is a classical interconnection network, of diameter $n$ and degree $\sigma$, and its Eulerian circuits are the de Bruijn sequences of order $n + 1$.

## When to use it

Use a de Bruijn graph to assemble many short reads with high coverage, where the overlaps of length $K - 1$ between $K$-mers are exact and the read boundaries do not matter; its size depends on the number of distinct $K$-mers, not on the number of reads. Use it on the complete alphabet to build or count [de Bruijn sequences](/de-bruijn-sequence/), through the [existence theorem](/de-bruijn-existence-theorem/). For long reads with many errors, the [overlap graph](/overlap-graph/) or [string graph](/string-graph/), which keep whole reads, are the usual choice.

## Pitfalls

- **Off by one in the order.** A de Bruijn sequence of order $n$ comes from the graph on words of length $n - 1$, with the words of length $n$ as edges. The graph whose vertices are the words of length $n$ is the next order.
- **Reading the multiplicity.** A count mixes coverage with copy number. In the example, `GTC` and `TCG` have count 2 only because both reads cover them, while each occurs once in `ACGTCGAT`. Counts must be compared with the coverage before they are used to decide how often a cycle is traversed.
- **Reads shorter than $K$.** They give no edge at all; ADD-READ must handle $|r| < K$ without a negative loop bound.
- **Choosing $K$.** A small $K$ merges distinct places of the genome whose $(K-1)$-mers agree, as `CG` above; a large $K$ breaks the graph where coverage is low or reads have errors. A read error creates up to $K$ wrong edges.
- **Eulerian is not unique.** A graph with a repeat can have several Eulerian walks that spell different strings; the graph alone cannot tell which one is the genome.

## Implementations

## History

De Bruijn (1946) and Good (1946) introduced the complete graph to count and construct the cyclic sequences now called [de Bruijn sequences](/de-bruijn-sequence/); the problem for two letters had been posed and solved by Flye Sainte-Marie in 1894. Van Aardenne-Ehrenfest and de Bruijn (1951) extended the count of Eulerian circuits to all alphabet sizes and to general directed graphs. In sequencing, Idury and Waterman (1995) proposed assembling reads from the graph of their $k$-tuples, and Pevzner, Tang and Waterman (2001) turned assembly into an Eulerian path problem, the approach of most short-read assemblers since. Bowe, Onodera, Sadakane and Shibuya (2012) gave a succinct representation.

## References
