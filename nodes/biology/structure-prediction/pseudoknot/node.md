---
tag: CH4145
kind: definition
slug: pseudoknot
name: Pseudoknot
aliases:
- Crossing base pairs
- RNA pseudoknot
- H-type pseudoknot
area: biology/structure-prediction
level: intro
summary: Two base pairs (i, j) and (k, l) of an RNA with i < k < j < l, which cross and so fall outside the nested secondary structure class.
prereqs: [rna-secondary-structure]
see_also: [rna-pseudoknot-prediction, pseudoknot-np-hardness, rna-secondary-structure-prediction, nearest-neighbor-model, maximum-matching, independent-set, sankoff-rna-algorithm]
sources:
  - paper: doi:10.1093/nar/13.5.1717
    title: Cornelis W. A. Pleij, Kees Rietveld and Leendert Bosch, A new principle of RNA folding based on pseudoknotting, Nucleic Acids Research 13(5), 1985, pages 1717 to 1731
    locator: the H-type pseudoknot, in which bases of a hairpin loop pair with bases outside the hairpin
  - paper: doi:10.1006/jmbi.1998.2436
    title: Elena Rivas and Sean R. Eddy, A dynamic programming algorithm for RNA structure prediction including pseudoknots, Journal of Molecular Biology 285(5), 1999, pages 2053 to 2068
    locator: the class of pseudoknots of the gap matrix algorithm, including H-type pseudoknots and kissing hairpins
  - paper: doi:10.1186/1471-2105-5-104
    title: Jens Reeder and Robert Giegerich, Design, implementation and evaluation of a practical pseudoknot folding algorithm based on thermodynamics, BMC Bioinformatics 5, 2004, article 104
    locator: the canonical simple recursive pseudoknots, the H-type and the kissing hairpin classes
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, Section 10.2, pseudoknots and why the nested folding algorithms cannot represent them
---

A pseudoknot is a pair of base pairs in an RNA that cross: one pair has exactly one of its ends between the two ends of the other. The [secondary structure](/rna-secondary-structure/) model forbids such pairs, because nested pairs are what make the interval dynamic programs of RNA folding work. Real RNAs have pseudoknots, often in functional sites, and the simplest kinds are the H-type pseudoknot and the kissing hairpins. Folding with pseudoknots is harder: polynomial algorithms exist only for restricted classes, and the general problem is NP-hard in simple energy models.

## Definition

Let $s = s_1 \cdots s_n$ be an RNA sequence. Two base pairs $(i, j)$ and $(k, l)$, with $i < j$ and $k < l$, **cross** if

$$i < k < j < l \quad \text{or} \quad k < i < l < j.$$

A **structure with pseudoknots** is a set $P$ of pairs that satisfies the other rules of a secondary structure (allowed pair types, the hairpin minimum, no shared bases) and has at least one crossing. The word pseudoknot names both the crossing and the motif that two crossing helices form.

**The crossing graph.** For a set $P$ of pairs, the crossing graph has a vertex for each pair and an edge between two crossing pairs. Then $P$ is a secondary structure if and only if its crossing graph has no edges. The graph is a circle graph: put the positions on a circle and draw each pair as a chord; two chords meet if and only if their pairs cross.

**Notation.** The dot-bracket notation uses one more kind of bracket for each level of crossing: pairs written with $[\,]$ may cross pairs written with $(\,)$, but no two pairs of the same kind cross. A structure can be written with $k$ kinds of brackets if and only if its crossing graph can be colored with $k$ colors.

**H-type pseudoknot.** Two helices $S_1$ and $S_2$ whose strands appear in the order $S_1$, $S_2$, $S_1$, $S_2$ from $5'$ to $3'$:

$$\texttt{[[[ ... ((( ... ]]] ... )))}$$

The bases of the loop of the hairpin of $S_1$ pair with bases after the hairpin. Pleij, Rietveld and Bosch (1985) described this fold.

**Kissing hairpins.** Two hairpins side by side whose loops pair with each other:

$$\texttt{(((( .. [[[ .. )))) .. (((( .. ]]] .. ))))}$$

The pairs of the middle helix cross the pairs of both hairpins.

## Examples and non-examples

- **An H-type pseudoknot.** In $s = $ GGGAUUUAACCCAAAAA ($n = 17$), take the helix $S_1 = \{(1, 12), (2, 11), (3, 10)\}$ of GC pairs and the helix $S_2 = \{(5, 17), (6, 16), (7, 15)\}$ of UA pairs. Each pair has at least 3 bases inside. The pairs $(3, 10)$ and $(7, 15)$ cross, because $3 < 7 < 10 < 15$. In the extended notation the structure is (((.[[[..)))..]]].
- **Not a pseudoknot: nested helices.** In the same sequence, the set $S_1$ alone, or $S_2$ alone, is a secondary structure. So is $\{(1, 12), (5, 9)\}$: the UA pair $(5, 9)$ lies inside $(1, 12)$, and nested pairs do not cross.
- **Not a pseudoknot: side by side.** The pairs $(1, 5)$ and $(6, 10)$ do not cross, since $5 < 6$.
- **A shared base is not a pseudoknot.** The pairs $(1, 8)$ and $(1, 12)$ share base 1. They do not cross by the definition, but they are not a structure at all.
- **A chain of crossings.** For the pairs $(1, 8)$, $(4, 12)$ and $(10, 15)$, the first crosses the second and the second crosses the third, while the first and third are side by side. Two kinds of brackets are enough, with the third pair written with $(\,)$ again: (..[...).(.]..).

## Related definitions

- **Secondary structure.** A set of pairs with no crossing. See [RNA secondary structure](/rna-secondary-structure/).
- **The largest nested subset.** Given a set of pairs, the largest subset with no crossing is a largest [independent set](/independent-set/) of its crossing graph. For circle graphs this problem is solvable in polynomial time, by an interval dynamic program over the positions.
- **Pairs with any crossing.** If crossings are allowed without any restriction, a structure is any matching in the graph of allowed pairs, and the largest number of pairs is a [maximum matching](/maximum-matching/), in polynomial time. With energies that reward stacks of neighbor pairs, the problem becomes NP-hard; see [pseudoknot NP-hardness](/pseudoknot-np-hardness/).
- **Classes of pseudoknots.** Algorithms work with restricted classes, such as the gap matrix class of Rivas and Eddy (1999), the class of Dirks and Pierce (2003), and the canonical simple recursive pseudoknots of Reeder and Giegerich (2004). See [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).
- **Tertiary structure.** Pseudoknots are sometimes counted as tertiary structure, together with base triples and other contacts that a set of pairs does not describe.

## References
