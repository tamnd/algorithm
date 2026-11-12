---
tag: K6H9KW
kind: algorithm
slug: protein-threading
name: Protein threading
aliases:
- Threading
- Fold recognition by threading
area: biology/structure-prediction
level: advanced
summary: Places a sequence onto the core segments of each fold template and scores the fit with a contact potential. Dynamic programming without pair terms; NP-hard with them (Lathrop 1994).
solves: [protein-fold-recognition]
model: real-ram
complexity:
  vars: {n: the length of the sequence, m: the number of core positions of the template}
  time: {worst: "O(n m)"}
  space: {extra: "O(n m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1992
  people: [David T. Jones, William R. Taylor, Janet M. Thornton]
  note: Bowie, Luthy and Eisenberg (1991) matched sequences to 3D profiles of structures, and Jones, Taylor and Thornton (1992) threaded sequences through folds with pairwise potentials. Lathrop (1994) proved the pairwise problem NP-complete.
prereqs: [protein-fold-recognition]
see_also: [comparative-modeling, i-tasser, energy-function, depth-first-branch-and-bound, binary-integer-programming, lp-relaxation, needleman-wunsch, side-chain-packing]
sources:
  - paper: doi:10.1126/science.1853201
    title: James U. Bowie, Roland Luthy and David Eisenberg, A method to identify protein sequences that fold into a known three-dimensional structure, Science 253(5016), 1991, 164-170
    locator: the 3D profile of a structure (one environment class per position) and the alignment of sequences to it
  - paper: doi:10.1038/358086a0
    title: David T. Jones, William R. Taylor and Janet M. Thornton, A new approach to protein fold recognition, Nature 358(6381), 1992, 86-89
    locator: the threading of a sequence through a library of folds with pairwise potentials
  - paper: doi:10.1016/S0022-2836(05)80269-4
    title: Manfred J. Sippl, Calculation of conformational ensembles from potentials of mean force, Journal of Molecular Biology 213(4), 1990, 859-883
    locator: the knowledge-based pair potentials derived from known structures
  - paper: doi:10.1021/ma00145a039
    title: Sanzo Miyazawa and Robert L. Jernigan, Estimation of effective interresidue contact energies from protein crystal structures, quasi-chemical approximation, Macromolecules 18(3), 1985, 534-552
    locator: the table of contact energies between pairs of amino acid types
  - paper: doi:10.1093/protein/7.9.1059
    title: Richard H. Lathrop, The protein threading problem with sequence amino acid interaction preferences is NP-complete, Protein Engineering 7(9), 1994, 1059-1068
    locator: the NP-completeness of threading with variable-length loops and pairwise interactions
  - paper: doi:10.1006/jmbi.1996.0053
    title: Richard H. Lathrop and Temple F. Smith, Global optimum protein threading with gapped alignment and empirical pair score functions, Journal of Molecular Biology 255(4), 1996, 641-665
    locator: the core segment model with loop length limits and the branch and bound search for the global optimum
  - paper: doi:10.1142/S0219720003000186
    title: Jinbo Xu, Ming Li, Dongsup Kim and Ying Xu, RAPTOR, optimal protein threading by linear programming, Journal of Bioinformatics and Computational Biology 1(1), 2003, 95-117
    locator: the integer program for threading and its linear relaxation
---

Protein threading fits a query sequence onto the backbone of a known fold, the *template*, and scores how well the sequence suits that structure. The template is reduced to a set of core segments, usually its helices and strands, in order along the chain. A threading puts each core segment onto a stretch of the sequence, with loops of free length between them, and the score adds a term for each residue in its structural environment and a term for each pair of residues that the template puts in contact. Threading the sequence onto each fold of a library, and keeping the folds with the best scores, is a method for [fold recognition](/protein-fold-recognition/). Without the pair terms an optimal threading takes a simple dynamic program; with them the problem is NP-complete (Lathrop 1994).

## In plain words

A known protein structure is like a mold with slots. Some slots are buried in the middle of the protein, some are on the surface, and some slots touch each other. We take a new sequence and try to lay it into the mold, letter by letter, in order. The parts between the slots, the loops, can stretch or shrink as needed.

Each way of laying the sequence into the mold gets a score. A water-fearing letter in a buried slot scores well, and so does a pair of letters that like each other in two slots that touch. We look for the way of laying the sequence in with the best score. Then we do the same for many molds. The mold with the best score is our guess for the shape of the new protein.

## The problem

**The template.** A core model of a known structure has $K$ core segments of lengths $c_1, \ldots, c_K$, in order along the chain, with $m = c_1 + \cdots + c_K$ core positions in total. Let $o_k = c_1 + \cdots + c_{k-1}$, so the positions of segment $k$ are $o_k + 1, \ldots, o_k + c_k$. Between segments $k$ and $k + 1$ the loop has at least $g_k \ge 0$ residues. The template also gives a set $P$ of pairs $(u, v)$ of core positions that are in contact.

**A threading.** For a sequence $a = a_1 \ldots a_n$, a threading is a vector $t = (t_1, \ldots, t_K)$ of start positions with

$$t_1 \ge 1, \qquad t_{k+1} \ge t_k + c_k + g_k, \qquad t_K + c_K - 1 \le n.$$

Residue $a_{t_k + l - 1}$ then sits at core position $o_k + l$. Write $x_u$ for the residue at core position $u$.

**The energy.** For a singleton term $\varepsilon(u, x)$, the fit of amino acid $x$ to the environment of position $u$, and a pair term $\pi(x, y)$, for example a statistical potential (Sippl 1990, Miyazawa and Jernigan 1985),

$$E(t) = \sum_{u=1}^{m} \varepsilon(u, x_u) + \sum_{(u, v) \in P} \pi(x_u, x_v).$$

The *threading problem* asks for a threading of least energy. Residues in loops do not score here; many methods add a loop or gap cost, which fits into $\varepsilon$ and the recurrence below. The *singleton case* has $P = \emptyset$. Costs are in the [real RAM](/real-ram/) model, one step per energy lookup or addition.

## The algorithm

In the singleton case the energy of segment $k$ depends only on its own start, so the energy is a sum over the segments of $S_k(s) = \sum_{l=1}^{c_k} \varepsilon(o_k + l, a_{s+l-1})$. The segments interact only through the order constraint. Let $F_k(s)$ be the least energy of segments $1, \ldots, k$ with segment $k$ at start $s$. Then

$$F_1(s) = S_1(s), \qquad F_k(s) = S_k(s) + \min_{q \le s - c_{k-1} - g_{k-1}} F_{k-1}(q).$$

The minimum over $q$ is a prefix minimum, so a running value computes it while $s$ grows.

```pseudo id=main
THREAD(a, c, g, ε)                       ▷ K core segments, singleton energy ε(u, x)
L1  for k ← 1 to K and s ← 1 to n − c_k + 1 do S[k][s] ← Σ_{l=1..c_k} ε(o_k + l, a[s+l−1])
L2  for s ← 1 to n − c_1 + 1 do
L3      F[1][s] ← S[1][s]
L4  for k ← 2 to K do
L5      best ← ∞; for s ← 1 to n − c_k + 1 do
L6          q ← s − c_{k−1} − g_{k−1}; if q ≥ 1 and F[k−1][q] < best then best ← F[k−1][q], arg ← q
L7          F[k][s] ← S[k][s] + best, B[k][s] ← arg
L8  t_K ← an s with least F[K][s]
L9  for k ← K down to 2 do t_{k−1} ← B[k][t_k]   ▷ follow the back pointers
L10 return F[K][t_K], (t_1, ..., t_K)
```

With pair terms the recurrence fails, because the score of segment $k$ then depends on where all the earlier segments in contact with it were placed, not only on the start of segment $k - 1$. The implementation of this page solves that case by brute force over all threadings, which is the reference; the methods of the section on variants solve it in practice.

## Example

Let the template have $K = 2$ segments of length 2, so the core positions are 1, 2 (segment 1) and 3, 4 (segment 2), and a minimum loop $g_1 = 1$. Positions 1 and 4 are buried, positions 2 and 3 are exposed, and positions 2 and 3 are in contact. With the alphabet H (hydrophobic) and P (polar), let

$$\varepsilon(u, \mathrm{H}) = -1, \quad \varepsilon(u, \mathrm{P}) = +1 \text{ for } u \in \{1, 4\}, \qquad \varepsilon(u, x) = 0 \text{ otherwise}, \qquad \pi(\mathrm{H}, \mathrm{H}) = -3,$$

and $\pi = 0$ for the other pairs. The sequence is $a = $ H H P P H P P, with $n = 7$.

**The singleton case.** Only position 1 of segment 1 and position 4 of segment 2 score, so $S_1(s)$ is $-1$ when $a_s = \mathrm{H}$ and $+1$ otherwise, and $S_2(s)$ is $-1$ when $a_{s+1} = \mathrm{H}$ and $+1$ otherwise:

| $s$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $S_1(s)$ | $-1$ | $-1$ | $+1$ | $+1$ | $-1$ | $+1$ |
| $S_2(s)$ | $-1$ | $+1$ | $+1$ | $-1$ | $+1$ | $+1$ |

Segment 2 must start at $s \ge q + 3$, so $F_2(4) = S_2(4) + S_1(1) = -2$, $F_2(5) = S_2(5) + \min(S_1(1), S_1(2)) = 0$ and $F_2(6) = S_2(6) + \min(S_1(1), S_1(2), S_1(3)) = 0$. Line L8 picks $t_2 = 4$, and the back pointer gives $t_1 = 1$. The optimum is $t = (1, 4)$ with energy $-2$: H at both buried positions.

**With the pair term.** There are six threadings. The table gives the singleton energy and the full energy $E(t)$:

| $t$ | (1, 4) | (1, 5) | (1, 6) | (2, 5) | (2, 6) | (3, 6) |
|---|---|---|---|---|---|---|
| singleton part | $-2$ | 0 | 0 | 0 | 0 | 2 |
| $E(t)$ | $-2$ | $-3$ | 0 | 0 | 0 | 2 |

At $t = (1, 5)$, position 2 holds $a_2 = \mathrm{H}$ and position 3 holds $a_5 = \mathrm{H}$, so the contact gives $-3$, which pays for the polar residue $a_6$ at the buried position 4. The optimum moves from $(1, 4)$ to $(1, 5)$. The dynamic program cannot see this, because the pair term links segment 1 to segment 2 through the residues, not through the starts alone.

## Correctness

For the singleton case, by induction on $k$, $F_k(s)$ is the least energy of the first $k$ segments with segment $k$ at $s$. The case $k = 1$ is line L3. For $k > 1$, a partial threading with $t_k = s$ is a partial threading of the first $k - 1$ segments with $t_{k-1} = q$ for some $q \le s - c_{k-1} - g_{k-1}$, followed by segment $k$. Its energy is the energy of the first part plus $S_k(s)$, because no term links the two parts. So the least energy is $S_k(s)$ plus the least $F_{k-1}(q)$ over the allowed $q$, and lines L5 to L7 compute exactly that minimum as a running minimum. The value $F_K(t_K)$ of line L8 is then the optimum, and the back pointers of line L9 rebuild a threading that reaches it, since each $B[k][s]$ records a $q$ that reaches the minimum. The full proof is in the proof file below.

## Complexity

Line L1 computes $S_k(s)$ for each segment $k$ and each of at most $n$ starts, with $c_k$ terms each, so it costs $O(n \sum_k c_k) = O(nm)$. Lines L2 to L7 do $O(1)$ work for each pair $(k, s)$, so $O(Kn) \subseteq O(nm)$. Line L9 takes $O(K)$. The total is $O(nm)$ time and $O(nm)$ space for the tables, or $O(Kn)$ space if $S_k$ is computed one row at a time. Brute force over all threadings checks $O(n^K)$ threadings at $O(m + |P|)$ each.

With pair terms the problem is NP-complete (Lathrop 1994), so no polynomial algorithm is known. The idea of the hardness is short. Take a graph with vertices $1, \ldots, K$ and an alphabet with letters $x_{k,1}, x_{k,2}, x_{k,3}$ for each vertex. The sequence is the blocks $x_{1,1} x_{1,2} x_{1,3}, \ldots, x_{K,1} x_{K,2} x_{K,3}$, and segment $k$ has length 1 and $\varepsilon(k, x) = 0$ for the letters of block $k$ and a large value otherwise. A contact $(u, v)$ for each edge, with $\pi(x_{u,i}, x_{v,j}) = 1$ for $i = j$ and 0 otherwise, makes the least energy 0 exactly when the graph has a proper [3-coloring](/three-coloring/). This sketch uses an alphabet that grows with the graph; Lathrop proved hardness for the real setting with a fixed alphabet of amino acids.

## Properties

- **Exact in the singleton case.** The dynamic program returns a true optimum, with no heuristics.
- **An alignment in disguise.** The singleton case is an alignment of the sequence to a profile of the template with free loops and no gaps inside the segments, which is the 3D profile method of Bowie, Luthy and Eisenberg (1991).
- **Fold-level, not residue-level.** Threading is built to tell which fold fits. The alignment it gives is often worse than its fold assignment, especially in loops.
- **Score depends on length.** Raw energies of different templates are not comparable; programs compare them with a z-score against shuffled sequences or a trained classifier.

## Variants and improvements

- **Loop length limits.** With a maximum loop length as well, the prefix minimum becomes a minimum over a window, which a monotone queue keeps in $O(1)$ time per step, so the cost stays $O(nm)$.
- **Frozen approximation.** Score a pair term with the residue of the query at one position and the residue of the template at the other position. The pair terms become singleton terms, and the dynamic program applies again.
- **Branch and bound.** Lathrop and Smith (1996) split the set of threadings by the possible positions of a segment and bound each subset from below, which finds the global optimum of the pairwise problem fast on most protein instances ([branch and bound](/depth-first-branch-and-bound/)).
- **Integer programming.** RAPTOR (Xu, Li, Kim and Xu 2003) writes threading as an integer program with one 0/1 variable per segment position and per pair of positions, and solves its [linear relaxation](/lp-relaxation/). The relaxation is often integral on real templates, which certifies the optimum.
- **Profile threading.** GenTHREADER and HHpred add sequence profiles and secondary structure to the energy and use profile-profile alignment, which is now the main form of [fold recognition](/protein-fold-recognition/).

## When to use it

Use threading when the query has no clear homolog of known structure by sequence search, but may share a fold with one. If a close homolog exists, [comparative modeling](/comparative-modeling/) on a sequence alignment is more accurate. Today the deep learning predictors, such as [AlphaFold](/alphafold/), often beat threading on single proteins, but threading and profile alignment remain fast tools to assign templates and folds over whole genomes.

## Pitfalls

- **Treating the singleton optimum as the pairwise optimum.** The dynamic program ignores contacts. Its result is a feasible threading and an upper bound for the pairwise problem, not its optimum, as the example shows.
- **Unbounded loops.** Without a maximum loop length, two segments that are close in the template can sit far apart in the sequence, and the model is not physical.
- **Raw scores across templates.** A large template has more terms, so its raw score is larger in size. Normalize before ranking.
- **Off-by-one in the loop constraint.** The next segment starts at $t_k + c_k + g_k$ or later, not at $t_k + g_k$. A wrong bound lets two segments overlap.

## Implementations

## History

Bowie, Luthy and Eisenberg (1991) described each position of a structure by its environment and aligned sequences to this 3D profile, which is the singleton case. Jones, Taylor and Thornton (1992) threaded sequences through a library of folds with pairwise potentials of the kind that Sippl (1990) had derived from known structures. Lathrop (1994) proved that the problem with variable loop lengths and pair interactions is NP-complete. Lathrop and Smith (1996) gave a branch and bound method that finds the global optimum, and Xu, Li, Kim and Xu (2003) solved threading with linear and integer programming in RAPTOR.

## References
