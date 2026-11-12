---
tag: YVJ262
kind: algorithm
slug: dali
name: DALI
aliases:
- Distance matrix alignment
- Dali
area: biology/structure-prediction
level: advanced
summary: Aligns two protein structures by matching their C-alpha distance matrices under an elastic score, with no superposition, using fragment pairs and a Monte Carlo search.
solves: [structure-alignment]
model: real-ram
complexity:
  vars: {n: residues of the first structure, m: residues of the second structure, L: the smaller of n and m, w: the fragment length, K: Monte Carlo steps for each seed, T: the number of seeds, R: refinement passes}
  time: {worst: O(n m w² + T K L² + T R n m L²), average: O(n m w² + T K L² + T R n m L²)}
  space: {extra: O(n² + m² + n m)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1993
  people: [Liisa Holm, Chris Sander]
  note: Holm and Sander published DALI in 1993 and used it to build a database of structural neighbors of all known protein structures.
prereqs: [structure-alignment, contact-map, metropolis-criterion]
see_also: [combinatorial-extension, tm-score, simulated-annealing, metropolis-hastings, rmsd, local-search]
sources:
  - paper: doi:10.1006/jmbi.1993.1489
    title: Liisa Holm and Chris Sander, Protein structure comparison by alignment of distance matrices, Journal of Molecular Biology 233(1), 1993, 123-138
    locator: the rigid and elastic similarity scores, the envelope function, the comparison of hexapeptide contact patterns, and the Monte Carlo optimization
  - paper: doi:10.1109/TCBB.2012.143
    title: Inken Wohlers, Rumen Andonov and Gunnar W. Klau, DALIX, optimal DALI protein structure alignment, IEEE/ACM Transactions on Computational Biology and Bioinformatics 10(1), 2013, 26-36
    locator: the integer programming formulation of the DALI score and its exact solution by Lagrangian relaxation
  - paper: doi:10.1109/SFFCS.1999.814624
    title: Deborah Goldman, Sorin Istrail and Christos H. Papadimitriou, Algorithmic aspects of protein structure similarity, 40th Annual Symposium on Foundations of Computer Science (FOCS), 1999, 512-521
    locator: the contact map overlap problem, a close relative of the DALI objective, and its NP-hardness
---

DALI (distance matrix alignment) aligns two protein structures by comparing their intramolecular distances instead of their coordinates. Each structure is described by its [contact map](/contact-map/) in the wider sense, the matrix of all $C_\alpha$ to $C_\alpha$ distances, which is the same for each rotation and translation, so DALI needs no superposition. A residue matching scores well when matched pairs of residues have similar distances in both structures. Holm and Sander (1993) defined an elastic score that tolerates small relative changes and down-weights long distances, and they searched for good matchings with fragment pairs and a Monte Carlo method. DALI is a heuristic for the [structure alignment](/structure-alignment/) problem.

## In plain words

A protein is a chain of links. Write the distance between each two links into a table. Turning or moving the protein does not change the table, so you can compare two proteins by their tables alone, without placing one on the other.

A good matching pairs links of the two chains so that the distances between paired links agree. Each agreeing distance earns a point, and each clear disagreement costs a point. Small differences are forgiven, more so for long distances, and very long ones count little.

To find a good matching, the method first looks for short pieces of the two chains whose small tables agree. It then builds a matching from such pieces by trial: add or remove a piece, keep the change if the total improves, and sometimes keep a worse change to escape a dead end.

## The problem

**Input.** Two $C_\alpha$ traces $A = (a_1, \ldots, a_n)$ and $B = (b_1, \ldots, b_m)$ in $\mathbb{R}^3$, in Å.

**Output.** A sequential alignment $M = \{(i_1, j_1), \ldots, (i_k, j_k)\}$, with $i_1 < \cdots < i_k$ and $j_1 < \cdots < j_k$, of large elastic score

$$S(M) = \sum_{(i, j) \in M}\ \sum_{(i', j') \in M} \phi(i, i', j, j').$$

Let $d^A = |a_i - a_{i'}|$, $d^B = |b_j - b_{j'}|$ and $d^* = (d^A + d^B)/2$. The elastic score has $\phi = \theta^E$ on the diagonal, $(i, j) = (i', j')$, and

$$\phi = \left(\theta^E - \frac{|d^A - d^B|}{d^*}\right) w(d^*), \qquad w(r) = e^{-r^2/\alpha^2},$$

otherwise, with $\theta^E = 0.2$ and $\alpha = 20$ Å. A pair of distances adds to the score when the two differ by less than 20% of their mean, and it costs when they differ by more. The envelope $w$ shrinks the terms of distances well beyond $\alpha$, which would otherwise dominate the score of a large protein.

## The algorithm

DALI works in two steps. First it compares all pairs of fragments of $w$ consecutive residues ($w = 6$, hexapeptides, in the paper) and keeps the pairs whose small distance matrices agree. Then a Metropolis Monte Carlo search, started from the best fragment pairs, builds alignments out of these pieces.

```pseudo id=main
DALI(A, B, w, T, K, β₀, g)
L1  D^A ← distance matrix of A ;  D^B ← distance matrix of B
L2  C ← all fragment pairs F = {(i + k, j + k) : 0 ≤ k < w} with S(F) > 0, best first
L3  (s*, M*) ← (0, ∅)
L4  for each of the T best fragment pairs F in C
L5      M ← F ;  β ← β₀ ;  (s_F, M_F) ← (S(F), F)
L6      repeat K times
L7          M′ ← with probability ½ M minus one random segment, else M plus a random F′ ∈ C, minus the pairs of M that conflict with F′
L8          if S(M′) ≥ S(M) or random() < exp(β (S(M′) − S(M))) then M ← M′
L9          if S(M) > s_F then (s_F, M_F) ← (S(M), M)
L10         β ← g β
L11     (s_F, M_F) ← REFINE(M_F): add any F′ ∈ C or delete any segment while this raises S
L12     if s_F > s* then (s*, M*) ← (s_F, M_F)
L13 return (s*, M*)
```

A pair of $M$ conflicts with $F'$ in line L7 if it uses a residue of $F'$ or would break the order of the residues. A segment is a maximal run of $M$ without gaps. Line L8 is the [Metropolis criterion](/metropolis-criterion/): an improvement is always kept, and a loss of $\Delta$ is kept with probability $e^{-\beta\Delta}$. Raising $\beta$ in line L10 makes the search greedier with time, as in [simulated annealing](/simulated-annealing/). Line L11 is a greedy [local search](/local-search/) over the same moves; it plays the role of the expansion and trimming cycles of the paper, which test the candidates of the pair list and remove parts that do not pay.

## Example

**The score of single distances.** With $\theta^E = 0.2$ and $\alpha = 20$ Å:

| $d^A$ (Å) | $d^B$ (Å) | $\phi$ |
|---|---|---|
| 5 | 5 | 0.1879 |
| 5 | 6 | 0.0169 |
| 5 | 7 | −0.1219 |
| 10 | 11 | 0.0795 |
| 20 | 20 | 0.0736 |
| 20 | 22 | 0.0348 |

A difference of 1 Å at 5 Å scores almost nothing, while at 10 Å it still scores, because the tolerance is relative. Equal distances score less at 20 Å than at 5 Å, because of the envelope.

**An insertion.** Let $A$ be an ideal $\alpha$-helix of 12 residues ($C_\alpha$ radius 2.3 Å, $100°$ and 1.5 Å per residue). Let $B$ be the same 12 points with two extra residues placed after the sixth, at $(6, 6, 8)$ and $(6.5, 4, 9)$, so $B$ has 14 residues. With $w = 4$:

| step | result |
|---|---|
| L1 | two distance matrices, $12 \times 12$ and $14 \times 14$ |
| L2 | 72 fragment pairs of positive score; the best have $S(F) = 3.0751$, for example $(1..4, 1..4)$ and $(7..10, 9..12)$ |
| L4 to L11 | the search joins fragments into one alignment and refines it |
| L13 | $M$ = residues 1 to 6 of $A$ with 1 to 6 of $B$, and 7 to 12 of $A$ with 9 to 14 of $B$ |
| L13 | $S(M) = 24.8241$ |

The alignment has one gap, against the two inserted residues, which is the planted answer. The first six pairs alone score only 6.7982. Because the score is quadratic in $|M|$, two halves that fit together score much more than the sum of their own scores.

## Correctness

DALI is a heuristic, so it need not return the maximum of $S$. What holds is the following. Each state of the search is a sequential alignment: the add move keeps only the pairs that are compatible with the new fragment, and the delete move takes a subset. The returned value is the true score of the returned alignment. The result is at least the score of each seed fragment, and it is a local optimum of the refinement moves: no single addition of a candidate fragment and no single deletion of a segment raises the score. The search stops, because the Monte Carlo loop has a fixed length and each refinement move raises the score among finitely many alignments. The full proof is below.

## Complexity

Let $L = \min(n, m)$, so each alignment has at most $L$ pairs and its score costs $O(L^2)$ to compute from scratch. Line L1 costs $O(n^2 + m^2)$. Line L2 scores $(n - w + 1)(m - w + 1)$ fragments at $O(w^2)$ each, $O(n m w^2)$, and sorts them. Lines L4 to L10 cost $O(T K L^2)$. Each pass of the refinement of line L11 tries $|C| \le n m$ candidates at $O(L^2)$ each. The number of passes has no useful bound in theory, but it is small in practice, so the time is heuristic. The space is $O(n^2 + m^2)$ for the matrices and $O(n m)$ for the candidates. An implementation that updates the score incrementally, at $O(L w)$ for each move, saves a factor of $L / w$.

## Properties

- **No superposition.** The method uses only internal distances, so it never needs a rotation. It also cannot tell a structure from its mirror image.
- **Elastic.** The relative tolerance allows the small changes of shape of related proteins, such as a shift of a helix, without losing the whole match.
- **Heuristic and random.** Different random seeds can give different alignments. The search keeps the best of each trajectory.
- **Repeats.** Internally repetitive structures, such as a long helix, have many shifted alignments of almost the same score. A search that starts in the wrong register may stay there.
- **Size dependent.** The raw score $S$ grows with the size of the match, so DALI reports a Z-score that compares $S$ with the scores expected for unrelated structures of the same size.

## Variants and improvements

- **Rigid score.** Holm and Sander also defined a rigid score, $\phi = \theta^R - |d^A - d^B|$ with a fixed threshold $\theta^R$ in Å, for very similar structures.
- **Exact optimization.** The DALI problem is closely related to contact map overlap, which is NP-hard. Wohlers, Andonov and Klau (2013) wrote it as an integer program, DALIX, and used Lagrangian relaxation to solve many instances to optimality and to give upper bounds for the others.
- **Database search.** The DALI server compares one query with all known structures and ranks the hits by Z-score.
- **Other aligners.** [Combinatorial extension](/combinatorial-extension/) also builds alignments from fragment pairs, but grows one path greedily and then refits with a superposition. TM-align maximizes the [TM-score](/tm-score/) with superpositions.

## When to use it

Use DALI to find remote structural relatives of a protein, where the sequence gives no signal, and to compare structures whose parts have moved a little relative to each other. For two very similar structures with a known correspondence, an [optimal superposition](/optimal-superposition/) and the [RMSD](/rmsd/) are simpler and exact. For a score with a fixed meaning across sizes, report the Z-score or a [TM-score](/tm-score/) of the alignment.

## Pitfalls

- **Overflow in line L8.** Evaluating $\exp(\beta (S(M') - S(M)))$ for a large gain overflows. Test $S(M') \ge S(M)$ first, as line L8 does, so the exponential is only computed for a loss.
- **Conflicts in line L7.** Adding a fragment without removing the pairs of $M$ that share a residue or break the order produces a matching that is not one-to-one, and its score counts some residues twice.
- **A zero mean distance.** In the score of line L2 and later, $|d^A - d^B| / d^*$ divides by zero when two residues sit at the same point. Use $\phi = \theta^E$ there, or keep the diagonal apart as the definition does.
- **No envelope.** Leaving out $w(d^*)$ in the score lets the many long distances of a large protein dominate, and the alignment then fits the overall size instead of the local structure.
- **Raw scores across sizes.** The score of line L13 grows with the length, so comparing raw scores of hits of different sizes ranks large hits too high. Use the Z-score.

## Implementations

## History

Holm and Sander published DALI in 1993. They used it to compare all known protein structures with each other and to build the FSSP database of structural families, and the method became a standard tool for the classification of folds. The DALI server has run since the 1990s and has been updated many times. In 2013 Wohlers, Andonov and Klau gave DALIX, an exact method for the DALI score based on integer programming.

## References
