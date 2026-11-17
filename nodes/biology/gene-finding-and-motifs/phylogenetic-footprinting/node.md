---
tag: ST9XHW
kind: technique
slug: phylogenetic-footprinting
name: Phylogenetic footprinting
aliases:
- substring parsimony
area: biology/gene-finding-and-motifs
level: advanced
summary: Find regulatory sites as short substrings conserved across orthologous regions, scored by parsimony on the species tree.
prereqs: [small-parsimony, motif-finding-problem, phylogenetic-tree]
see_also: [fitch-algorithm, sankoff-algorithm, median-string-problem, comparative-gene-finding, position-specific-scoring-matrix, maximum-parsimony, steiner-tree-problem, multiple-sequence-alignment]
sources:
  - paper: doi:10.1016/0022-2836(88)90011-3
    title: Danilo A. Tagle, Ben F. Koop, Morris Goodman, Jerry L. Slightom, David L. Hess and Richard T. Jones, Embryonic epsilon and gamma globin genes of a prosimian primate (Galago crassicaudatus), nucleotide and amino acid sequences, developmental regulation and phylogenetic footprints, Journal of Molecular Biology 203(2), 1988
    locator: pp. 439 to 455; the term phylogenetic footprint for non-coding sequence conserved across primate globin genes
  - paper: doi:10.1089/10665270252935421
    title: Mathieu Blanchette, Benno Schwikowski and Martin Tompa, Algorithms for phylogenetic footprinting, Journal of Computational Biology 9(2), 2002
    locator: pp. 211 to 223; the parsimony formulation of footprinting on a given tree, its exact dynamic programming algorithm, and the speed-ups of the program
  - paper: doi:10.1101/gr.6902
    title: Mathieu Blanchette and Martin Tompa, Discovery of regulatory elements by a computational method for phylogenetic footprinting, Genome Research 12(5), 2002
    locator: pp. 739 to 748; the program FootPrinter, which reports all motifs with the lowest parsimony scores, and its results on known regulatory regions
---

Phylogenetic footprinting finds regulatory sites, such as transcription factor binding sites, by looking for short stretches that stay conserved in the non-coding DNA next to the same gene in several species. Sites that the cell uses are kept by selection, while the DNA around them changes, so the sites stand out as conserved "footprints" when the regions are compared. Tagle and colleagues named the idea in 1988 in a study of primate globin genes. Blanchette, Schwikowski and Tompa (2002) made it an exact optimization problem: choose one substring of length $k$ in each species so that the total number of changes along the branches of the known species tree is as small as possible, and solve it by dynamic programming over the tree. Their program FootPrinter reports all motifs with the lowest scores.

## In plain words

Genes are switched on and off by proteins that stick to short words in the DNA near the gene, often six to twelve letters long. These words are hard to find in one genome, because the DNA around them is a long random-looking text, and a word of eight letters appears by chance many times. But if we look at the same gene in a human, a mouse, a cow and a chicken, the switching words are often still there, almost unchanged, while the text around them has changed a lot. So take the region before the gene in each species, and look for a word that appears, in nearly the same form, in all of them. Use the family tree of the species to count the changes in the fairest way: two close cousins that share a word count for less than two distant species that share it.

## When it applies

- **Orthologous regions are known.** The input is the regulatory region (for example 1000 to 2000 bases upstream of the start) of the same gene in several species, and the species tree. If some regions come from paralogs, the tree of the regions is not the species tree, and conservation means less.
- **The species are at a useful distance.** Very close species share almost every base, so every word looks conserved. Very distant species may not share the site at all, or may have moved it. A good set has several species at moderate distances, so that the background has had time to change.
- **Sites are short and ungapped.** The method looks for words of a fixed length $k$, compared by Hamming distance. It does not handle sites with insertions inside them.
- **The regions cannot be aligned well.** For regions that align reliably, a column-based conservation score on an alignment is simpler. The parsimony formulation does not need an alignment: each species may put the site anywhere in its region. This is its main advantage over alignment-based methods.

## The template

**The objective.** Let $T$ be a rooted tree whose leaves are the species, and let $S_v$ be the region of the leaf $v$. Choose a $k$-mer $x_v$ for every node $v$ of $T$, so that at each leaf $x_v$ is a substring of $S_v$; the internal $k$-mers can be any strings. The cost is

$$\sum_{(u, v) \in E(T)} d_H(x_u, x_v),$$

the total Hamming distance over the edges. The task is to find the choices of lowest cost, or all choices with cost at most a bound $d$. This is a [small parsimony](/small-parsimony/) problem with one extra freedom: each leaf chooses its own label from the substrings of its region.

**The dynamic program.** For each node $v$ and each $k$-mer $s$, let $W_v(s)$ be the lowest cost of the subtree of $v$ when $x_v = s$.

```pseudo id=main
FOOTPRINT(T, S, k)
L1  for each leaf v do
L2      W_v(s) ← 0 if s is a substring of S_v, and ∞ otherwise, for every k-mer s
L3  for each internal node u, from the leaves up do
L4      W_u(s) ← 0 for every k-mer s
L5      for each child v of u do
L6          D_v ← W_v
L7          for p ← 1 to k do
L8              for every k-mer s do D'(s) ← min over letters a of D_v(s with letter a at position p) + [a ≠ s_p]
L9              D_v ← D'
L10         W_u(s) ← W_u(s) + D_v(s) for every k-mer s
L11 return the k-mers s with the lowest W_root(s), and trace back the choices at the children
```

Lines L6 to L9 compute $D_v(s) = \min_t (W_v(t) + d_H(s, t))$ for all $s$ at once. The Hamming distance is a sum over positions, so the minimum can be taken one position at a time: after round $p$, $D_v(s)$ is the best value over the strings $t$ that may differ from $s$ in the first $p$ positions. After $k$ rounds this is the full minimum. This is a theorem, and the proof is the same induction as for any distance that is a sum over coordinates.

**Cost.** Line L2 costs $O(k L)$ in total for regions of total length $L$, or $O(L)$ with a rolling code of the $k$-mers. Lines L7 to L9 cost $O(k \cdot 4^k)$ per edge, with 4 letters. The whole program costs $O(N k 4^k + k L)$ time and $O(N 4^k)$ space for a tree with $N$ nodes, in the word RAM. This bound is derived on this page from the recurrence. It is exponential in $k$ and linear in everything else, which is fine for $k$ up to about 10 to 12 and impossible for long motifs. The program of Blanchette, Schwikowski and Tompa adds pruning and other speed-ups that make it fast on most real data sets.

**Reporting.** To find all motifs with cost at most $d$, keep at each node only the $k$-mers with $W_v(s) \le d$, which is usually a small set, and trace back all choices from every $s$ with $W_{\mathrm{root}}(s) \le d$. FootPrinter reports all motifs with the lowest parsimony scores; it is exact for its objective.

## Classic examples

**A toy footprint.** Take $k = 5$, the tree ((human, chimp), (mouse, chicken)), and these upstream regions of 12 bases:

| species | region |
|---|---|
| human | CTTGACGTCAGA |
| chimp | CTTGACGTCAGG |
| mouse | AGTGACGTAACT |
| chicken | GCTGACTTAAGC |

The program gives a lowest cost of 1, reached by two choices: GACGT in human, chimp and mouse with GACTT in chicken, and TGACG in the first three with TGACT in chicken. Both are windows of the same conserved site TGACGT, which chicken carries as TGACTT. One change on the branch to chicken explains it, with GACGT (or TGACG) at every internal node. A search over all $8^4 = 4096$ ways to choose one 5-mer in each region, each scored by small parsimony per position, gives the same two optima; 8 choices have cost at most 2 and 18 have cost at most 3. Human and chimp share 7 of their 8 5-mers, so a word that only they share costs 0 on their side of the tree. This is why close species add little.

**Globin footprints (Tagle et al. 1988).** The term comes from the comparison of the embryonic globin genes of a prosimian primate with those of other primates. Non-coding stretches near the genes that stayed conserved over the primate tree were proposed as regulatory sites. The name recalls DNase footprinting, the laboratory method that shows where a bound protein protects DNA.

**FootPrinter (Blanchette and Tompa 2002).** The program implements the parsimony formulation, with options for real data, and is tested on regulatory regions of genes with known binding sites. Its abstract states that it is guaranteed to report all sets of motifs with the lowest parsimony scores.

## Variations

- **Star tree and median string.** With a tree of one internal node and the leaves as its children, the objective is $\min_s \sum_v \min_{t \in S_v} d_H(s, t)$, which is the [median string problem](/median-string-problem/) of [motif finding](/motif-finding-problem/). The same lines L6 to L9 then solve it in $O(n k 4^k + k L)$ for $n$ sequences, instead of $O(4^k n L)$ for the plain enumeration. Phylogenetic footprinting is motif finding with the tree as extra information.
- **Weighted changes.** Hamming distance counts every change as 1. A [Sankoff](/sankoff-algorithm/) style cost per pair of letters, or a cost that depends on the branch length, keeps the same dynamic program with a different line L8.
- **Motif loss.** A site can be lost in some lineage. A variant lets a subtree have no motif at a fixed cost, so one species without the site does not hide a motif that the others share.
- **Likelihood instead of parsimony.** Score a motif by the probability of its copies under a substitution model on the tree with branch lengths, as in [Felsenstein's pruning](/felsenstein-pruning/), or by a [position-specific scoring matrix](/position-specific-scoring-matrix/) that evolves on the tree. This uses the branch lengths that parsimony ignores.
- **Alignment-based conservation.** If the regions align, compute a conservation score per column of a [multiple alignment](/multiple-sequence-alignment/), and report conserved windows. This is fast and works for long elements, but it misses sites that moved.
- **Many close species.** With many primates instead of a few distant species, single changes are rare and conservation is measured by the lack of changes over the summed branch length. This is useful for regions that are specific to one lineage.

## Pitfalls

- **Conserved does not mean regulatory.** Conserved non-coding DNA includes non-coding RNA genes, unannotated exons and sequence kept for other reasons. A footprint is a candidate site, and experiments decide.
- **Not every site is conserved.** Many binding sites turn over between species, and some are specific to one lineage. Footprinting misses them by design.
- **Chance motifs.** With long regions and few species, low-cost motifs appear by chance. The expected number of chance motifs grows with the region lengths and falls with the number of species and the tree length. Judge a motif against shuffled regions or random sequence on the same tree.
- **Close species dominate.** Two very close species share most of their words, so their part of the tree costs almost nothing for any word. The score then rests on the distant species. Choose species that spread over the tree.
- **The wrong tree or paralogs.** If one region comes from a paralog or the tree is wrong, the parsimony cost is computed on the wrong branches, and true sites can look poor.
- **Large $k$.** The tables have $4^k$ entries per node. At $k = 12$ that is about 16.8 million per node. Use pruning, or a smaller $k$ and a search for longer sites by joining windows.

## Exercises

1. In the toy example, change the chicken region so that it carries TGACGT exactly. What is the new lowest cost, and how many choices reach it?
2. Prove that lines L6 to L9 compute $\min_t (W_v(t) + d_H(s, t))$ for all $s$, by induction on the number of rounds.
3. Show that for a tree with two leaves the objective is the smallest Hamming distance between a $k$-mer of $S_1$ and a $k$-mer of $S_2$, and give a direct algorithm for it.
4. Derive the cost of lines L6 to L9 for an alphabet of size $\sigma$, and compare it with computing $\min_t (W_v(t) + d_H(s, t))$ directly over all pairs $(s, t)$.
5. For $n$ random regions of length $L$ on a star tree, estimate the expected number of $k$-mers $s$ with $W_{\mathrm{root}}(s) = 0$, and use it to explain why footprinting with short regions and few species gives false motifs.

## References
