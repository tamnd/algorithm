---
tag: J6984A
kind: algorithm
slug: combinatorial-extension
name: Combinatorial extension (CE)
aliases:
- CE alignment
area: biology/structure-prediction
level: advanced
summary: Aligns two protein structures by growing a path of aligned fragment pairs whose internal distances agree, then refines the result with superpositions.
solves: [structure-alignment]
model: real-ram
complexity:
  vars: {n: residues of the first structure, r: residues of the second structure, m: the length of an aligned fragment pair, G: the largest gap, L: the number of fragment pairs of the longest path}
  time: {worst: O(n r m² + n r G m L²), average: O(n r m² + n r G m L²)}
  space: {extra: O(n² + r² + n r)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1998
  people: [Ilya N. Shindyalov, Philip E. Bourne]
  note: Shindyalov and Bourne published CE in 1998, and the Protein Data Bank used it for pairwise structure comparison.
prereqs: [structure-alignment, rmsd]
see_also: [dali, tm-score, optimal-superposition, kabsch-algorithm, needleman-wunsch, contact-map, gdt-ts]
sources:
  - paper: doi:10.1093/protein/11.9.739
    title: Ilya N. Shindyalov and Philip E. Bourne, Protein structure alignment by incremental combinatorial extension (CE) of the optimal path, Protein Engineering 11(9), 1998, 739-747
    locator: the aligned fragment pairs, the path conditions (1) to (5), the distances of eqs. (6) and (7), the extension criteria (9) to (11), the search strategies, the Z-score and the final optimization
  - paper: doi:10.1006/jmbi.1993.1489
    title: Liisa Holm and Chris Sander, Protein structure comparison by alignment of distance matrices, Journal of Molecular Biology 233(1), 1993, 123-138
    locator: the comparison of intramolecular distances of fragment pairs (DALI), the method that CE is compared with
---

Combinatorial extension (CE) aligns two protein structures by chaining short pieces that match. An aligned fragment pair (AFP) matches $m$ consecutive residues of one chain with $m$ consecutive residues of the other, $m = 8$ in the paper. CE grows a path of AFPs one at a time, with no gap or a short gap in one chain between them, and it accepts the next AFP only if the internal distances of the whole path still agree in the two structures. Like [DALI](/dali/), it compares distances, so the search needs no superposition. Shindyalov and Bourne (1998) then refine the longest paths with [optimal superpositions](/optimal-superposition/) and dynamic programming, and they report the [RMSD](/rmsd/) and a Z-score. CE is a heuristic for the [structure alignment](/structure-alignment/) problem.

## In plain words

Cut both protein chains into short pieces of eight links. A pair of pieces, one from each chain, is a good pair when the distances between the links inside them agree.

Start with one good pair. Look at the good pairs that come right after it in both chains, or after a short skip in one chain. Of these, take the one that fits best with all the pairs already chosen, and add it if the chain of pairs as a whole still fits. Stop when nothing fits.

Do this from each start, and keep the longest chain of pairs. Starts that cannot give a longer chain are not tried. At the end, place one protein on the other and improve the matched residues.

## The problem

**Input.** Two $C_\alpha$ traces $A = (a_0, \ldots, a_{n-1})$ and $B = (b_0, \ldots, b_{r-1})$ in $\mathbb{R}^3$, in Å. The parameters of the paper are the AFP length $m = 8$, the largest gap $G = 30$ residues, and the thresholds $D_0 = 3$ Å and $D_1 = 4$ Å.

**Output.** A long path of AFPs $(p_1, \ldots, p_k)$, where $p_t = (p^A_t, p^B_t)$ matches $a_{p^A_t + x}$ with $b_{p^B_t + x}$ for $0 \le x < m$, and the alignment of $k m$ residue pairs that it gives.

Let $d^A(i, i') = |a_i - a_{i'}|$ and $d^B(j, j') = |b_j - b_{j'}|$. The self-distance of one AFP $p$ is eq. (7) of the paper,

$$D_{pp} = \frac{1}{m^2} \sum_{x=0}^{m-1} \sum_{y=0}^{m-1} \left| d^A(p^A + x, p^A + y) - d^B(p^B + x, p^B + y) \right|.$$

The distance of two AFPs $p \ne q$ is eq. (6). It uses only $m$ "independent" residue pairs: the two first residues, the two last residues, and the pairs that cross from the start of one fragment towards the end of the other,

$$D_{pq} = \frac{1}{m} \sum_{(x, y)} \left| d^A(p^A + x, q^A + y) - d^B(p^B + x, q^B + y) \right|, \quad (x, y) \in \{(0, 0), (m-1, m-1)\} \cup \{(k, m - 1 - k) : 1 \le k \le m - 2\}.$$

A path is valid when each step satisfies the path conditions (1) to (5): the next AFP starts exactly $m$ residues later in both chains, or $m$ later in one chain and $m + g$ later in the other with $1 \le g \le G$. Each AFP must satisfy criterion (9), $D_{pp} < D_0$. Each new AFP $q$ appended to a path $(p_1, \ldots, p_k)$ must satisfy criterion (10), $\frac{1}{k} \sum_{s} D_{p_s q} < D_1$, and the longer path must satisfy criterion (11), $\frac{1}{(k+1)^2} \sum_{s} \sum_{u} D_{p_s p_u} < D_1$, over all its AFPs and the diagonal included.

## The algorithm

The paper describes three strategies for the extension. The "all" strategy tries every extension that passes the criteria, the "best" strategy takes only the best candidate at each step, and the "intermediate" strategy lies between them. The paper uses "best", shown here.

```pseudo id=main
CE(A, B, m, G, D₀, D₁)
L1  D^A ← distance matrix of A ;  D^B ← distance matrix of B
L2  P ← all AFPs p with D_pp < D₀                                    ▷ criterion (9)
L3  best ← the empty path
L4  for each p ∈ P, in order
L5      if 1 + min(⌊(n − m − p^A)/m⌋, ⌊(r − m − p^B)/m⌋) ≤ |best| then skip p
L6      path ← (p) ;  T ← D_pp
L7      loop
L8          C ← the q ∈ P that follow the last AFP by (1) to (5), each with c_q = Σ_{s ∈ path} D_sq, kept if c_q / |path| < D₁   ▷ (10)
L9          if C is empty then leave the loop
L10         q ← the element of C with the least c_q / |path|
L11         if (T + 2 c_q + D_qq) / (|path| + 1)² ≥ D₁ then leave the loop          ▷ (11)
L12         append q to path ;  T ← T + 2 c_q + D_qq
L13     if |path| > |best| then best ← path
L14 return best
```

Line L5 is the pruning of the paper: a start is dropped when no path from it can be longer than the best path found so far. The bound counts AFPs that follow each other with no gap until one chain ends. The variable $T$ holds the double sum of criterion (11) for the current path, so line L11 costs $O(1)$ once line L8 has computed $c_q$; the factor 2 uses $D_{pq} = D_{qp}$.

**Final optimization.** After the search, the paper computes a Z-score for the best path from the scores of comparisons of unrelated structures; $z \ge 3.5$ corresponds to $p \le 10^{-3}$. Only when $z > 3.5$ does CE optimize further. It evaluates the 20 best paths by the RMSD after an optimal superposition, moves the gaps by up to $m/2$ residues, and then runs iterative [Needleman-Wunsch](/needleman-wunsch/) [global alignment](/global-alignment/) on the superposed structures, with the score $M_{ij} = d_0 - d_{ij}$ for the distance $d_{ij}$ between residue $i$ of $A$ and residue $j$ of $B$, a gap opening penalty of 5 and a gap extension penalty of 0.5. The value $d_0$ starts at 2 Å and grows by 0.5 Å in each cycle, and the cycles stop when the alignment length drops below 95% or the RMSD grows beyond 110%. This step is described here and is not part of the implementation.

## Example

Let $A$ be a chain of 32 residues with steps of 3.8 Å, made by a seeded random walk (the code is in the test file). Let $B$ be $A$ turned by 0.7 rad about the $z$ axis and moved, with 4 extra residues after residue 16 and Gaussian noise of standard deviation 0.3 Å on each coordinate, so $B$ has 36 residues. With $m = 8$, $G = 30$, $D_0 = 3$ Å and $D_1 = 4$ Å, and residues numbered from 1:

| step | result |
|---|---|
| L2 | of the $25 \times 29 = 725$ AFPs, 663 pass (9) |
| L4, L6 | the first start is $(1, 1)$, with $D_{pp} = 0.2938$ |
| L8 to L12 | 31 candidates; the least mean (10) is 0.3208, for $(9, 9)$; the next best is $(9, 10)$, at 1.4527; mean (11) is 0.3088, so append $(9, 9)$ |
| L8 to L12 | 17 candidates; the least mean is 0.3447, for $(17, 21)$, a gap of 4 in $B$; mean (11) is 0.3390, so append it |
| L8 to L12 | one candidate, $(25, 29)$, with mean 0.3666; mean (11) is 0.3504, so append it |
| L9 | no AFP can follow $(25, 29)$, so the path is complete |
| L5 | each other start has a bound of at most 4 AFPs, so all of them are skipped |
| L14 | the path $(1, 1), (9, 9), (17, 21), (25, 29)$ |

The path aligns residues 1 to 16 of $A$ with 1 to 16 of $B$, and 17 to 32 of $A$ with 21 to 36 of $B$: the 32 planted pairs, with the gap against the insertion. The RMSD of these pairs after the optimal superposition is 0.5196 Å, the effect of the noise. The shifted candidate $(9, 10)$ has a mean over four times larger, which is how the criteria keep the register of the alignment. With these lenient thresholds almost all AFPs of two chain-like traces pass (9), so it is the criteria between AFPs that do the work.

## Correctness

The "best" strategy is a heuristic, so the result need not be the longest path that the criteria allow. What holds is the following. Each step of the greedy loop appends an AFP that passes (9), follows the last one by (1) to (5), and passes (10); the running sum $T$ is exactly the double sum of (11), because the distance of eq. (6) is symmetric, so the appended AFP also passes (11). Hence the result is a valid path. The pruning of line L5 loses nothing: each AFP of a path starts at least $m$ residues after the one before it in both chains, so no path from a skipped start is longer than the best one. The result therefore has the greatest length among the greedy paths of all starts. The loop stops, because each appended AFP moves at least $m$ residues along $A$. The full proof is below.

## Complexity

Let $L$ be the number of AFPs of the longest path; $L \le \min(n, r)/m$. Line L1 costs $O(n^2 + r^2)$ time and space. Line L2 evaluates $(n - m + 1)(r - m + 1)$ AFPs at $O(m^2)$ each, $O(n r m^2)$. For one start, each pass of the loop examines at most $2G + 1$ successors, and each costs $O(k m)$ for a path of $k$ AFPs, so a start costs $O(G m L^2)$ over its at most $L$ passes. With $O(n r)$ starts, the worst case is $O(n r m^2 + n r G m L^2)$ in the real-RAM model. In practice line L5 skips most starts once a long path is found, as in the example, but there is no bound on the saving, so the faster running time is heuristic. The space is $O(n^2 + r^2)$ for the matrices and $O(n r)$ for the set $P$. The final optimization adds the superpositions, $O(L m)$ each, and the dynamic programming, $O(n r)$ for each cycle.

## Properties

- **Deterministic.** With a fixed order of the starts and ties broken by position, the result depends only on the input. There is no random search, as in [DALI](/dali/).
- **Sequential.** A path matches residues in the same order in both chains, so CE cannot find similarities that do not follow the order of the chain, such as a circular permutation. The paper notes that CE does not find such non-topological similarities.
- **Rigid fragments, flexible joints.** Criterion (11) compares distances across the whole path, so the path stays close to one rigid body. A hinge motion between two domains breaks the agreement of long distances and ends the path.
- **Gaps in one chain at a time.** Conditions (2) and (3) put a gap in one chain only, and the next AFP starts right after the last one in the other chain. A region that differs in both chains needs two steps, one with a gap in each chain, and an AFP between them.
- **Size of the result.** The length of the path is a multiple of $m$ before the final optimization, which can then add or remove single residues.

## Variants and improvements

- **"All" and "intermediate" strategies.** The "all" strategy searches every extension that passes the criteria and finds the longest valid path, at a cost that grows exponentially with the length of the path. The "best" strategy, the default of the paper, is the greedy loop above.
- **Final optimization.** The dynamic programming step of the paper, described above, refits the alignment to the superposition. It is the same idea as the alternation of TM-align, which scores alignments by the [TM-score](/tm-score/).
- **Rating the result.** A CE alignment can be rated afterwards by its RMSD, its TM-score or its [GDT-TS](/gdt-ts/), computed with the [Kabsch algorithm](/kabsch-algorithm/) or another superposition method.
- **Circular permutations and flexibility.** Later versions of CE add a search for circular permutations, and FATCAT chains AFPs with a small number of twists between rigid parts.
- **Multiple alignment.** The fragment-pair approach has also been used as the start of methods that align more than two structures.

## When to use it

Use CE to align two protein structures whose similar parts follow the same order along the chain, for example to find a structural relative in a database or to compare two models of the same fold. It is fast, it needs no starting superposition, and its output, a set of rigid fragment pairs with an RMSD, is easy to check. For structures with hinge motions, a flexible aligner fits better. For similarities that do not follow the order of the chain, use a method that allows non-sequential matches. For a score with the same meaning at each protein size, rate the result by the [TM-score](/tm-score/).

## Pitfalls

- **Coordinates in line L2.** Line L2 compares internal distances, which do not change when a structure is turned or moved. A test that compares the coordinates of the two fragments directly depends on the frame of each file, and it rejects good AFPs.
- **A gap in both chains in line L8.** Allowing $g^A > 0$ and $g^B > 0$ in the same step breaks conditions (2) and (3) and raises the number of successors from $2G + 1$ to $(G + 1)^2$. It is no longer the search of the paper.
- **The mean of (11) without the diagonal in line L11.** The paper divides the double sum by $(k + 1)^2$ with the terms $D_{pp}$ included. Leaving them out, or dividing by $k (k + 1)$, changes the threshold.
- **A wrong bound in line L5.** The bound must be at least the length of each valid path from the start. A smaller bound, for example $\lfloor (n - p^A)/m \rfloor - 1$, can skip the start of the longest greedy path, and the result is then shorter than it must be.
- **The AFP length in line L2.** With a large $m$, short secondary structures and loops cannot form AFPs, and the path breaks at each of them. With a small $m$, too many AFPs pass (9) by chance.
- **The RMSD alone after line L14.** The RMSD is small for short alignments. Compare results by length and RMSD together, or by the Z-score.

## Implementations

## History

Shindyalov and Bourne published CE in 1998. It joined two ideas of the time: the comparison of intramolecular distances of [DALI](/dali/) (Holm and Sander 1993), and the extension of a single path by fixed rules instead of a stochastic search. The CE server and its database of precomputed alignments were run by the Protein Data Bank, and a Java version became part of the RCSB PDB tools for pairwise structure comparison.

## References
