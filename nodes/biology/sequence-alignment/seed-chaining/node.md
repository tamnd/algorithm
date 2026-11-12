---
tag: 5R845S
kind: problem
slug: seed-chaining
name: Seed chaining
aliases:
- anchor chaining
- chaining with gap costs
area: biology/sequence-alignment
level: advanced
summary: Pick an ordered subset of seed matches that scores best, counting the bases they cover and charging for the gaps between them. It turns seed hits into a rough alignment.
prereqs: [colinear-chaining]
see_also: [minimap2, minimizer, seed-and-extend, maximal-exact-match, read-mapping, whole-genome-alignment, banded-alignment, dag-longest-path]
sources:
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pages 3094 to 3100, Section 2.1 (the chaining score with the gap cost, the heuristic with h predecessors, backtracking and primary chains)
  - paper: doi:10.1016/j.jda.2004.08.011
    title: Mohamed Ibrahim Abouelhoda and Enno Ohlebusch, Chaining algorithms for multiple genome comparison, Journal of Discrete Algorithms 3(2-4), 2005
    locator: pages 321 to 341, chaining without gap costs and with gap costs in the L1 and L-infinity metrics
  - paper: doi:10.1145/146637.146656
    title: David Eppstein, Zvi Galil, Raffaele Giancarlo and Giuseppe F. Italiano, Sparse dynamic programming II, convex and concave cost functions, Journal of the ACM 39(3), 1992
    locator: pages 546 to 567, fragment alignment with convex and concave gap costs
  - paper: arxiv:1303.3997
    title: Heng Li, Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM, 2013
    locator: Section 2 (chaining of SMEM seeds before extension)
---

Seed chaining is the problem of choosing, from many seed matches between a query and a reference, an ordered subset that forms a plausible rough alignment. The seeds of a true alignment lie in the same order in both sequences and close to one diagonal; chance seeds and seeds from repeats do not. A chain is scored by the bases its seeds cover minus a cost for each gap between consecutive seeds. Without gap costs the problem is solved exactly in $O(n \log n)$ time by the [colinear chaining algorithm](/colinear-chaining/). With the gap costs of real tools, such as [minimap2](/minimap2/), it is solved by a quadratic dynamic program, which tools cut down with a heuristic.

## In plain words

A read mapper first finds short exact matches, called seeds, between a read and the genome. A long read has hundreds of them, and many are wrong: they come from repeats or from chance. The right seeds form a line: they appear in the same order in the read and in the genome, and the distance between two of them is about the same in both.

Chaining picks the seeds that form the best such line. It rewards each seed for the letters it matches. It charges a penalty when the jump between two seeds is longer in the read than in the genome, or the other way round, because that means an insertion or a deletion. The best line tells the mapper where the read goes and which parts are left to align in detail.

## Definition

**Input.** A set of $N$ anchors. In the form of minimap2, an anchor is a triple $(x, y, w)$: the reference interval $[x - w + 1, x]$ matches the query interval $[y - w + 1, y]$ exactly, on one strand. Anchors are sorted by $x$. A gap cost function $\gamma$ and a maximum gap $G$ are also given.

**Chain.** A list of anchors $a_{j_1}, a_{j_2}, \ldots, a_{j_r}$ in the order of $x$, in which the query coordinate increases strictly: $y_{j_1} < y_{j_2} < \cdots$. Consecutive anchors must be at most $G$ apart in both sequences.

**Score.** Minimap2 defines the best score $f(i)$ of a chain that ends at anchor $i$ by

$$f(i) = \max\Bigl\{\ \max_{j < i}\bigl\{f(j) + \alpha(j, i) - \beta(j, i)\bigr\},\ w_i\ \Bigr\},$$

where $\alpha(j, i) = \min\{y_i - y_j,\ x_i - x_j,\ w_i\}$ is the number of new matched bases that anchor $i$ adds after anchor $j$, and the gap cost is

$$\beta(j, i) = \begin{cases} \infty & \text{if } y_j \ge y_i \text{ or } \max\{y_i - y_j,\ x_i - x_j\} > G, \\ \gamma_c\bigl((y_i - y_j) - (x_i - x_j)\bigr) & \text{otherwise,} \end{cases}$$

with $\gamma_c(0) = 0$ and $\gamma_c(\ell) = 0.01 \cdot \bar{w} \cdot |\ell| + 0.5 \log_2 |\ell|$ for $\ell \ne 0$, where $\bar{w}$ is the average seed length. The value $\ell$ is the change of diagonal between the two anchors, that is, the net length of the insertions or deletions between them. The seeds may overlap, since $\alpha$ counts only the new bases.

**Task.** Find the anchor $i$ with the largest $f(i)$, and a chain that ends at $i$ and reaches this score. Usually all good chains are wanted: after the best chain is taken, its anchors are marked used, and the next best chain is formed from the rest.

This is a longest path problem in the DAG of anchors, with an edge from $j$ to $i$ when $\beta(j, i) < \infty$; see [DAG longest path](/dag-longest-path/).

## Variants

- **No gap costs.** Take fragments as rectangles, let a chain need strict precedence in both coordinates with no overlap, and maximize the total weight. This is *colinear chaining*, solved exactly in $\Theta(n \log n)$ time by the [colinear chaining algorithm](/colinear-chaining/).
- **Linear gap costs.** A cost proportional to the gap in the $L_1$ or $L_\infty$ metric. Abouelhoda and Ohlebusch (2005) reduce it to the case without costs by a shift of the scores, and keep $O(n \log n)$ time for two sequences.
- **Concave and convex gap costs.** Costs such as $a + b \log \ell$ grow more slowly for long gaps. The sparse dynamic programs of Eppstein, Galil, Giancarlo and Italiano (1992) handle these costs in time near $O(n \log n)$. Minimap2's $\gamma_c$ is a sum of a linear and a logarithmic term in the diagonal change, and it also counts overlaps through $\alpha$, so it does not fit these methods directly.
- **Overlapping anchors.** Seeds from overlapping k-mers overlap. Some formulations allow overlaps and count only the bases not already covered, as $\alpha$ does.
- **Local chains.** A chain may start at any anchor, which the term $w_i$ in the maximum allows. A chain of low score is dropped.
- **Many sequences.** Anchors are boxes in $d$ dimensions, for chaining matches among $d$ genomes.

## Examples

Six anchors of length $w = 5$, given by their end points $(x, y)$ on the reference and on the query, with $G$ large:

| anchor | $(x, y)$ | diagonal $y - x$ | best predecessor | $f$ |
|---|---|---|---|---|
| 1 | (10, 5) | $-5$ | none | 5 |
| 2 | (14, 9) | $-5$ | 1 | 9 |
| 3 | (25, 30) | $5$ | 2 | 11.84 |
| 4 | (30, 24) | $-6$ | 2 | 13.95 |
| 5 | (36, 31) | $-5$ | 4 | 18.90 |
| 6 | (50, 44) | $-6$ | 5 | 23.85 |

From anchor 1 to anchor 2, both coordinates grow by 4, so $\alpha = 4$ (one base of overlap) and there is no gap cost: $f(2) = 5 + 4 = 9$. Anchor 3 jumps 10 diagonals away. Its gap cost is $0.01 \cdot 5 \cdot 10 + 0.5 \log_2 10 \approx 2.16$, so $f(3) = 9 + 5 - 2.16 = 11.84$. Anchor 4 is one diagonal from anchor 2: its cost is $0.05$, and $f(4) = 13.95$. Anchor 5 could follow anchor 3, but $y$ grows by only 1, so $\alpha = 1$ and the score is $11.84 + 1 - 2.16 = 10.68$; after anchor 4 it gets $13.95 + 5 - 0.05 = 18.90$. The best chain is $1, 2, 4, 5, 6$ with score 23.85. It moves between diagonals $-5$ and $-6$, which is a deletion of one base in the query. Anchor 3, ten diagonals away, is a chance hit.

## Known algorithms

| method | time | exact? | notes |
|---|---|---|---|
| full dynamic program | $O(N^2)$ | yes | evaluates every pair $j < i$ |
| bounded gap $G$ | $O(N \cdot q)$ | yes | only predecessors within distance $G$; $q$ is the largest number of anchors in such a range |
| minimap2 heuristic | $O(h N)$ | no | tries predecessors from $i - 1$ backwards and stops after $h$ tries without a better score; $h = 50$ in the paper |
| [colinear chaining](/colinear-chaining/) | $\Theta(n \log n)$ | yes, for the variant without gap costs | sweep with range maximum queries |
| sparse dynamic programming | near $O(n \log n)$ | yes, for linear, concave or convex costs | Eppstein et al. (1992), Abouelhoda and Ohlebusch (2005) |

Minimap2 finds a chain by backtracking: it stores for each $i$ the predecessor $P(i)$ that gave $f(i)$, and starts from the largest $f$. It then marks the anchors of that chain as used, and the next chain stops when it reaches a used anchor. A chain that overlaps a better one on the query by half or more of the shorter chain is *secondary*; the rest are *primary*. The mapping quality of a primary chain comes from the scores of the best and of the second best chain at that place.

## Bounds

- **Lower bound.** The variant without gap costs contains the [longest increasing subsequence](/longest-increasing-subsequence/) problem (anchors $(i, a_i)$ of length 1), so it needs $\Omega(n \log n)$ comparisons in the comparison model, by Fredman's bound for that problem.
- **Upper bound.** The full dynamic program takes $O(N^2)$ time for any gap cost, because each pair is examined once.
- **Heuristic gap.** With $h$ predecessors the minimap2 recurrence can miss the best chain, for example when more than $h$ anchors from a repeat lie between two consecutive anchors of the true chain. In practice the anchors are sorted by reference position and the true predecessor is usually close.

## Reductions

- **To DAG longest path.** Anchors are nodes, feasible pairs are edges with weight $\alpha - \beta$, and each node has a start weight $w_i$. A longest path gives the best chain. Since the order by $x$ is a topological order, one pass suffices.
- **From longest increasing subsequence.** A sequence $a_1, \ldots, a_n$ gives the anchors $(i, a_i, 1)$ with zero gap costs; a best chain is a longest increasing subsequence.
- **To alignment.** A chain fixes a narrow band around its anchors. Aligning the gaps between consecutive anchors with [banded alignment](/banded-alignment/) or [extension](/x-drop-extension/) gives a full base-level alignment.

## Applications

- **Long-read and assembly mapping.** [Minimap2](/minimap2/) chains [minimizer](/minimizer/) hits of a read against the reference, then aligns the gaps between the anchors of the chain.
- **Short-read mapping.** BWA-MEM chains its SMEM seeds and extends the chains; see [BWA](/bwa/) and [read mapping](/read-mapping/).
- **Whole-genome alignment.** [MUMmer](/mummer/) chains maximal unique matches, and the chain-and-net pipeline of the UCSC genome browser chains gapless blocks. See [whole-genome alignment](/whole-genome-alignment/).

## References
