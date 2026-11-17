---
tag: 9NY424
kind: algorithm
slug: minimum-path-cover-transcript-assembly
name: Minimum path cover transcript assembly
aliases:
- Cufflinks assembly
area: biology/transcriptomics
level: advanced
summary: 'Assemble the fewest transcripts that explain all fragments: order the compatible fragments, find a maximum bipartite matching, and merge each chain into one transcript, by Dilworth''s theorem.'
solves: [transcript-assembly]
model: word-ram
complexity:
  vars: {F: the number of fragments after line L1, λ: the largest number of nodes in a fragment, n: the number of nodes of the graph, E: the number of edges}
  time: {worst: O(F^3 + F^2·λ + (F+n)·(n+E))}
  space: {extra: O(F^2 + n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2010
  people: [Cole Trapnell, Brian A. Williams, Geo Pertea, Ali Mortazavi, Gordon Kwan, Marijke J. van Baren, Steven L. Salzberg, Barbara J. Wold, Lior Pachter]
  note: Cufflinks assembled the fragments of each locus into the fewest transcripts by a constructive proof of Dilworth's theorem, a maximum matching in a bipartite graph built from the transitive closure of the overlap graph.
prereqs: [transcript-assembly, splice-graph, minimum-path-cover-problem, dilworth-theorem, bipartite-matching]
see_also: [path-cover-by-bipartite-matching, flow-based-transcript-assembly, hopcroft-karp, transitive-closure, em-isoform-quantification, paired-end-reads, np-hard, flow-decomposition]
sources:
  - paper: doi:10.1038/nbt.1621
    title: Cole Trapnell, Brian A. Williams, Geo Pertea, Ali Mortazavi, Gordon Kwan, Marijke J. van Baren, Steven L. Salzberg, Barbara J. Wold and Lior Pachter, Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation, Nature Biotechnology 28(5) (2010)
    locator: pp. 511 to 515, Online Methods (the overlap graph of fragments, the minimum path cover by Dilworth's theorem and bipartite matching)
  - paper: doi:10.2307/1969503
    title: R. P. Dilworth, A decomposition theorem for partially ordered sets, Annals of Mathematics 51(1) (1950)
    locator: pp. 161 to 166
  - paper: doi:10.1186/1471-2105-15-S9-S5
    title: Romeo Rizzi, Alexandru I. Tomescu and Veli Mäkinen, On the complexity of minimum path cover with subpath constraints for multi-assembly, BMC Bioinformatics 15(Suppl 9) (2014)
    locator: Article S5 (subpath constraints in polynomial time by a reduction to the classical problem; pairs of subpaths are NP-hard)
  - paper: doi:10.1093/comjnl/bxu116
    title: Niko Beerenwinkel, Stefano Beretta, Paola Bonizzoni, Riccardo Dondi and Yuri Pirola, Covering pairs in directed acyclic graphs, The Computer Journal 58(7) (2015)
    locator: pp. 1673 to 1686 (deciding whether three paths cover all pairs is NP-hard)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Part V, the chapter on transcriptomics (path covers for transcript assembly)
---

Minimum path cover transcript assembly finds the smallest set of transcripts that explains every read of a gene locus. Each read, or each read pair with a known gap, is a fragment: a path through the [splice graph](/splice-graph/) of the locus. Two fragments are compatible when one transcript can hold both. The method orders the compatible fragments, finds a maximum matching in a bipartite graph of that order, and merges each chain of matched fragments into one transcript. By [Dilworth's theorem](/dilworth-theorem/) the number of transcripts is the least possible and equals the largest set of fragments of which no two fit on one transcript. This is the assembly step of Cufflinks. The optimum is exact for the stated problem, but the choice of the fewest transcripts is a parsimony heuristic: nothing forces the cell to use the fewest isoforms.

## In plain words

Each read is a short piece of some message. Two pieces can belong to the same message when they agree where they overlap, or when one can be followed by the other along the gene.

Line up the pieces so that every piece points to a piece that can come after it on the same message. Each line of pieces becomes one message. We want as few lines as possible, so that we invent no more messages than the reads need.

A matching finds the best way to link pieces in pairs, and the number of messages is the number of pieces minus the number of links. Two pieces that can never be on one message must be in different lines, so the answer can never be smaller than the largest group of such pieces.

## The problem

The input is a DAG $G$ on the nodes $1, \ldots, n$, numbered so that each edge $(u, v)$ has $u < v$; the nodes of a splice graph in coordinate order have this property. A *fragment* is a path of $G$: the node path of a read, or of a read pair whose two mates and the part between them are known. A path $P$ *holds* a fragment $x$ if $x$ is a contiguous part of $P$. The task is to find the fewest paths of $G$ that together hold every fragment.

This is the [minimum path cover problem](/minimum-path-cover-problem/) with subpath constraints, where each fragment is one constraint. Rizzi, Tomescu and Mäkinen (2014) show that this version is solvable in polynomial time. The pseudocode numbers nodes from 1; the code numbers them from 0.

## The algorithm

For a fragment $x$, $f(x)$ is its first node and $l(x)$ its last node.

```pseudo id=main
MIN-PATH-COVER-ASSEMBLY(G, fragments)
L1  F ← the distinct fragments that are not a contiguous part of another fragment
L2  for each pair x, y in F with f(x) < f(y) do
L3      if f(y) is in x at index i then x ≺ y iff x[i..] = y[..|x| - i]
L4      else x ≺ y iff l(x) < f(y) and f(y) can be reached from l(x)
L5  H ← the bipartite graph with a left copy and a right copy of F and an edge (x, y) for each x ≺ y
L6  M ← a maximum matching of H
L7  for each fragment that is not matched on the right, follow its matched successors to get a chain
L8  merge each chain into one path: append the rest of y, or a connecting path and then y
L9  return the paths; there are |F| - |M| of them
```

Line L1 is safe, because a path that holds a fragment holds every part of it. Lines L3 and L4 test whether one path can hold $x$ and then $y$: either $y$ starts inside $x$ and they agree on the overlap, or $y$ starts after $x$ ends and the graph has a way from one to the other. Reachability comes from a [transitive closure](/transitive-closure/) of $G$, computed once. Line L6 is any maximum [bipartite matching](/bipartite-matching/) algorithm; the code uses augmenting paths, and [Hopcroft-Karp](/hopcroft-karp/) is faster. Line L7 starts a chain at each fragment that is no one's successor, and line L8 walks the chain and appends each fragment to the path. The connecting path in line L8 is any path from $l(x)$ to $f(y)$, found by breadth-first search.

This is the [path cover by bipartite matching](/path-cover-by-bipartite-matching/) construction applied to the order $\prec$ on fragments. Cufflinks calls the graph of fragments and their compatibility the overlap graph.

## Example

Use the splice graph of the [splice graph page](/splice-graph/): nodes $v_1 = 1..100$, $v_2 = 201..250$, $v_3 = 251..300$, $v_4 = 401..500$, and edges $v_1 v_2$, $v_2 v_3$, $v_3 v_4$, $v_1 v_3$, $v_1 v_4$. The reads give seven fragments: $A = v_1 v_2$ twice, $B = v_2 v_3$, $C = v_3 v_4$, $D = v_1 v_3$, $E = v_1 v_4$, and $v_3$ alone.

Line L1 drops the second copy of $A$ and the fragment $v_3$, which is part of $B$. Lines L2 to L4 give this order:

| pair | test | result |
|---|---|---|
| $A, B$ | $f(B) = v_2$ is in $A$ at index 1; $A[1..] = v_2 = B[..0]$ | $A \prec B$ |
| $A, C$ | $v_3$ is not in $A$; $l(A) = v_2 < v_3$ and $v_3$ is reachable | $A \prec C$ |
| $B, C$ | $v_3$ is in $B$ at index 1, and they agree | $B \prec C$ |
| $D, C$ | $v_3$ is in $D$ at index 1, and they agree | $D \prec C$ |
| $D, B$ | $v_2$ is not in $D$, and $l(D) = v_3$ is not before $v_2$ | no |
| $A, D, E$ | the same first node $v_1$ | no |
| $B, E$ and $D, E$ | $E$ jumps from $v_1$ to $v_4$ | no |

$H$ has the four edges $A B$, $A C$, $B C$, $D C$. The code matches $A \to B$ first, then $D \to C$; then $B$ tries $C$, which is taken by $D$, and $D$ has no other edge, so $B$ stays unmatched. $|M| = 2$ and line L9 returns $5 - 2 = 3$ paths: $A B$ merged into $v_1 v_2 v_3$, $D C$ merged into $v_1 v_3 v_4$, and $E = v_1 v_4$.

Three is the least possible: $B$, $D$ and $E$ are pairwise incompatible, so no two of them share a path. The output is still not the true set of transcripts. The gene has $v_1 v_2 v_3 v_4$, $v_1 v_3 v_4$ and $v_1 v_4$, and the cover gave $C$ to the second path, so the first path ends at $v_3$. The other maximum matching, $A \to B$ and $B \to C$, gives $v_1 v_2 v_3 v_4$, $v_1 v_3$ and $v_1 v_4$. Both are minimum covers. Cufflinks breaks such ties with the read abundances.

## Correctness

[The proof](proofs/correctness.md) has four steps. Line L1 does not change the set of covers. For fragments that are not parts of each other, $x \prec y$ holds exactly when some path holds $x$ and then $y$, and $\prec$ is a strict partial order. The fragments on one path form a chain, and line L8 turns any chain into one path that holds all its fragments, with the invariant that the merged path ends with the last fragment added. So the fewest paths equals the fewest chains, which is $|F| - |M|$ by the matching argument, and by Dilworth's theorem also the size of the largest antichain. Every statement is a theorem about the model; that the model picks the right transcripts is not claimed.

## Complexity

The word RAM, with $F$ fragments after line L1, at most $\lambda$ nodes in each, and a graph with $n$ nodes and $E$ edges.

- Line L1: each pair of fragments is compared in $O(\lambda)$, because a path visits a node once, so one lookup finds where $x$ could start in $y$. Total $O(F^2 \lambda)$.
- Lines L2 to L4: the reachability bit sets cost $O(nE / w)$ word operations once, and each of the $F^2$ pairs costs $O(\lambda)$.
- Line L6: augmenting paths cost $O(F \cdot |H|) = O(F^3)$. Hopcroft-Karp costs $O(|H| \sqrt{F}) = O(F^{2.5})$.
- Line L8: at most $F$ connecting searches of $O(n + E)$ each.

The total is $O(F^3 + F^2 \lambda + (F + n)(n + E))$ time, and $O(F^2 + n^2)$ space for $H$ and the bit sets. In practice $F$ is the number of distinct fragments of one locus, often a few hundred after duplicates and contained fragments are removed.

## Properties

- **Exact for its model.** The number of paths is the least possible, a theorem (Theorem 2 of the proof).
- **Parsimony is a heuristic.** The true transcript set may have more transcripts than the minimum, and the minimum cover need not be unique.
- **Abundance-blind.** The cover uses only which fragments exist, not how many reads each has. Cufflinks estimates abundances in a separate maximum likelihood step.
- **Paths may be truncated.** A path starts and ends where its first and last fragments do, and a fragment that two transcripts share goes to only one of them.
- **Deterministic.** The order of the fragments and of the edges fixes the matching.

## Variants and improvements

- **Cufflinks.** It also marks pairs of fragments as incompatible when they disagree on splicing, which is the same as $\prec$ failing in both directions. Among the maximum matchings it takes one of least cost, with a cost on each edge that is small when the two fragments have similar estimated splicing ratios, so that fragments of the same abundance end up on the same transcript.
- **Paired fragments.** When a read pair is two separate subpaths with an unknown part between them, each constraint is a pair of subpaths. Rizzi, Tomescu and Mäkinen (2014) show that the minimum path cover with pairs of subpaths is NP-hard, and Beerenwinkel, Beretta, Bonizzoni, Dondi and Pirola (2015) show that already deciding whether three paths are enough is NP-hard. The simple method then needs a heuristic, such as filling the gap when it is unique.
- **Faster matching.** Hopcroft-Karp or a flow algorithm in place of augmenting paths one at a time.
- **Weighted covers.** Methods that also use the read counts replace the path cover by a [flow decomposition](/flow-decomposition/) of the coverage, as in [flow-based assembly](/flow-based-transcript-assembly/).

## When to use it

Use it when you want the smallest transcript set that is consistent with every read, for example to avoid reporting false isoforms from noise, and when the reads or the read pairs are single subpaths of the splice graph. It is not a good choice when the expression levels of the isoforms are very different, because it ignores the counts, or when many pairs leave a gap with several possible fillings. Then a flow-based method such as StringTie, which uses the coverage, is usually more accurate (a measurement on benchmarks, not a theorem).

## Pitfalls

- **Skipping line L1.** If a contained fragment stays, it can match into a chain on its own and add a path. Remove duplicates and contained fragments first.
- **Testing only adjacent fragments in line L4.** The order must use reachability, not only a direct edge from $l(x)$ to $f(y)$; otherwise $\prec$ is not transitive and the matching can return more paths than needed.
- **Taking the paths as full transcripts.** Line L8 builds paths that start and end at fragment ends. A shared fragment goes to one chain only, as in the example; report the cover as a set of partial transcripts, or extend the ends with the splice graph.
- **One bad fragment costs one path.** A misaligned read that is incompatible with all others forces its own transcript, because the method must explain every fragment. Filter fragments with few reads or short anchors before line L1.
- **Merging mates as one path.** Joining the two mates of a pair by an arbitrary connecting path in line L8 invents the part between them. Only do this when the gap has one possible path.

## Implementations

## History

Dilworth (1950) proved that the least number of chains that cover a finite partial order equals the size of its largest antichain, and Fulkerson (1956) gave a proof by bipartite matching that is also an algorithm. Trapnell, Williams, Pertea, Mortazavi, Kwan, van Baren, Salzberg, Wold and Pachter (2010) used this construction in Cufflinks to assemble the fewest transcripts that explain the fragments of each locus, and then estimated their abundances in FPKM. Rizzi, Tomescu and Mäkinen (2014) showed that the path cover with subpath constraints stays polynomial and that pairs of subpaths make it NP-hard, and Beerenwinkel, Beretta, Bonizzoni, Dondi and Pirola (2015) studied covers of pairs in DAGs.

## References
