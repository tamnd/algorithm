---
tag: 3JK50G
kind: problem
slug: eulerian-superpath-problem
name: Eulerian superpath problem
aliases:
- Pevzner Eulerian superpath
area: biology/genome-assembly
level: advanced
summary: Find an Eulerian path in an assembly graph that contains every read-path as a subpath. It is easy when each edge is used once and NP-hard when edges have multiplicities.
prereqs: [de-bruijn-assembly, eulerian-path]
see_also: [repeat-resolution, de-bruijn-graph, hierholzer-algorithm, chinese-postman-problem, shortest-common-superstring-np-hard, sequencing-by-hybridization, paired-end-reads, unitig]
sources:
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753, section Eulerian Superpaths (problem statement, x,y-detachment, resolvable edges, x-cut, the open gap), and section EULER with Clone-End Data
  - paper: doi:10.1186/1471-2105-14-S5-S7
    title: Evgeny Kapun and Fedor Tsarev, De Bruijn superwalk with multiplicities problem is NP-hard, BMC Bioinformatics 14(Suppl 5) S7 (2013)
    locator: Theorem 1 (common superstring with multiplicities is NP-hard) and Theorem 2 (NP-hard for each fixed alphabet of size at least 2 and each k)
  - paper: doi:10.1007/978-3-540-74126-8_27
    title: Paul Medvedev, Konstantinos Georgiou, Gene Myers and Michael Brudno, Computability of models for sequence assembly, WABI 2007, LNCS 4645
    locator: pp. 289 to 301, Section 3 and Theorem 2 (the shortest de Bruijn superwalk is NP-hard, by reduction from shortest common superstring)
---

The Eulerian superpath problem asks for an Eulerian path in an assembly graph that contains each read, written as a path in the graph, as a contiguous part. Pevzner, Tang and Waterman stated it in 2001 for the EULER assembler. A plain [Eulerian path](/eulerian-path/) through a [de Bruijn graph](/de-bruijn-graph/) uses each $k$-mer but forgets which reads joined which $k$-mers, so at a repeat it can join the wrong entrance to the wrong exit. The read-paths carry that missing information. If each edge is used exactly once, the problem is polynomial, and a sequence of merges of consecutive edges turns it into an ordinary Eulerian path problem. If edges have multiplicities, as repeated $k$-mers do, the problem is NP-hard, and the EULER method is a heuristic that can stop before it reaches a solution.

## In plain words

You cut each read into $k$-mers and draw the de Bruijn graph. The genome is a walk that uses each edge once, or as many times as the $k$-mer occurs. Many such walks can exist when the genome has repeats, and they spell different genomes.

Each read is also a short walk in the graph. The true genome contains each read, so its walk contains each read walk without a break. The problem asks for a full walk with that property.

If no $k$-mer occurs twice, the reads tell you directly which edge must come after which, and you glue those pairs together. If some $k$-mers occur several times, you do not know which copy a read passes through, and the problem becomes as hard as the hardest search problems.

## Definition

A **graph with multiplicities** is a directed multigraph $G$ in which each edge $e$ has an integer $\mu(e) \ge 1$. A walk $W$ is **Eulerian** if it goes through each edge $e$ exactly $\mu(e)$ times. A **path system** is a finite set $\mathcal{P}$ of walks in $G$. A walk $P = e_1 e_2 \cdots e_p$ is a **subpath** of $W$ if $W$ contains $e_1, e_2, \ldots, e_p$ at consecutive positions.

**Eulerian superpath problem.** Given $G$, $\mu$ and $\mathcal{P}$, find an Eulerian walk $W$ such that each $P \in \mathcal{P}$ is a subpath of $W$, or report that there is none. Such a $W$ is an **Eulerian superpath**.

In assembly, $G$ is the de Bruijn graph of order $k$ of the reads, $\mu(e)$ is the estimated number of copies of the $k$-mer $e$ in the genome, and $\mathcal{P}$ holds the read-paths: the walk of $L - k + 1$ edges spelled by each read of length $L$. Pevzner, Tang and Waterman add each read and its reverse complement. An Eulerian superpath spells a string that contains each read and has each $k$-mer exactly $\mu$ times.

A path of one edge is a subpath of each Eulerian walk, so it adds no constraint. The constraints come from consecutive pairs of edges inside a read-path.

## Variants

- **Each edge once.** $\mu(e) = 1$ for each edge. This is the case of a genome in which no $k$-mer occurs twice. Repeated $(k-1)$-mers are still allowed: they are vertices that the walk visits several times. This case is polynomial.
- **With multiplicities.** The general case. On a de Bruijn graph, with $\mu$ written in unary, Kapun and Tsarev call it the *de Bruijn superwalk with multiplicities* problem.
- **Shortest superwalk.** Drop $\mu$ and ask for the shortest walk that contains each read-path and so goes through each edge at least once. Medvedev, Georgiou, Myers and Brudno call it the *de Bruijn superwalk problem*. If each read-path has one edge, this is the [Chinese postman problem](/chinese-postman-problem/).
- **With mate pairs.** EULER-DB maps both reads of a mate pair into the graph. If exactly one path between them has a length that matches the clone length, it turns the pair and that path into one long artificial read, a *mate-read*, and treats it as one more read-path.
- **Circular genomes.** Ask for an Eulerian circuit in place of a path. Bacterial genomes are circular.

## Examples

**One vertex visited three times.** Take the edges $a = (s, v)$, $b_1 = (v, p)$, $b_2 = (p, v)$, $c_1 = (v, q)$, $c_2 = (q, v)$ and $d = (v, t)$, each with $\mu = 1$. The vertex $v$ is a repeated $(k-1)$-mer. There are two Eulerian paths:

| Eulerian path | order of the loops |
|---|---|
| $a\,b_1 b_2\,c_1 c_2\,d$ | loop through $p$ first |
| $a\,c_1 c_2\,b_1 b_2\,d$ | loop through $q$ first |

With $\mathcal{P} = \{a b_1\}$, only the first is a superpath: in the second, $a$ is followed by $c_1$. With $\mathcal{P} = \{b_2 c_1\}$, only the first is a superpath. With $\mathcal{P} = \{a b_1, a c_1\}$ there is no superpath, because the edge $a$ occurs once and cannot be followed by two different edges.

**The same case solved by merging.** For $\mathcal{P} = \{a b_1, b_2 c_1\}$ the forced pairs are $a \to b_1$ and $b_2 \to c_1$. Merge each pair into one edge: $z_1 = a b_1$ from $s$ to $p$, and $z_2 = b_2 c_1$ from $p$ to $q$. The new graph has the edges $z_1 = (s, p)$, $z_2 = (p, q)$, $c_2 = (q, v)$ and $d = (v, t)$, which form a single path. Its only Eulerian path $z_1 z_2 c_2 d$ expands to $a\,b_1 b_2\,c_1 c_2\,d$.

**A repeat edge with multiplicity 3.** Let the genome be $A R B R C R D$, where the repeat $R$ is longer than $k$, so its $k$-mers form an edge $x = (v, w)$ with $\mu(x) = 3$ after the unitig is compressed. The edge into $v$ from $A$ is $a$, from $B$ is $b$ and from $C$ is $c$. The edges out of $w$ into $B$, $C$ and $D$ are $b'$, $c'$ and $d$. Two genomes have the same graph and multiplicities:

| genome | order of the walk |
|---|---|
| $A R B R C R D$ | $a\,x\,b' \cdots b\,x\,c' \cdots c\,x\,d$ |
| $A R C R B R D$ | $a\,x\,c' \cdots c\,x\,b' \cdots b\,x\,d$ |

If each read is shorter than $R$, each read-path that touches $x$ has $x$ at its start or its end, for example $a x$ or $x c'$. Both walks contain all such read-paths, so the reads cannot decide. This is a *tangle* in the sense of EULER: a repeat that no read-path spans. One read that spans $R$ and gives the read-path $a\,x\,b'$ decides: after $B$, the walk must take $c'$, since taking $d$ ends the walk with $C$ unused. So only the first genome remains.

## Known algorithms

**Merging forced pairs when each edge is used once.** Collect each pair $(e_i, e_{i+1})$ of consecutive edges in a read-path. If an edge has two different forced successors, or two different forced predecessors, report that there is no solution. Otherwise the pairs link the edges into chains. If the pairs close a cycle, report that there is no Eulerian superpath that is a path (a circuit is possible only if the cycle holds all edges). Replace each chain by one edge from the start of its first edge to the end of its last edge, and run [Hierholzer's algorithm](/hierholzer-algorithm/) on the result. The time is $O(m + \sum_{P} |P|)$ for $m$ edges. This is the repeated x,y-detachment of EULER in the case without multiple edges. The proof is in Bounds.

**Detachments and cuts (EULER).** EULER applies two transformations, which the paper calls *equivalent* because each keeps a one-to-one correspondence between Eulerian superpaths before and after:

1. **x,y-detachment.** For consecutive edges $x = (v_{in}, v_{mid})$ and $y = (v_{mid}, v_{out})$, add an edge $z = (v_{in}, v_{out})$, delete $x$ and $y$ (or one copy of each, if $\mu > 1$), and route the paths through $z$. If $\mu(x) > 1$, a path that ends with $x$ can continue on several edges after $x$. The paper calls such a path *resolvable* if it is consistent with the paths through exactly one of the next edges. It calls an edge resolvable if all paths that end in it are resolvable, and it detaches only resolvable edges. It postpones the other edges and tries them again later, because detachments elsewhere often make them resolvable.
2. **x-cut.** An edge $x = (v, w)$ is *removable* if it is the only edge out of $v$ and the only edge into $w$, and it is the first or the last edge of each path that contains it. An x-cut deletes $x$ from those paths and does not change the graph. Each walk that enters $v$ must continue on $x$, and each walk that leaves $w$ came in on $x$, so the deleted constraints hold in every Eulerian walk.

When all paths have one edge, any Eulerian path of the transformed graph is a solution. For the *N. meningitidis* project, the paper reports that 18,026 of the 18,962 edges of the graph were resolvable. It also states that detachments and cuts reduced the assembly of all bacterial genomes it studied to the Eulerian path problem, and that there is "still a gap in the theoretical analysis" for path systems on which neither transformation applies. So EULER is a heuristic: it has no guarantee that it finishes, and it can stop with unresolvable edges and no single-edge path system.

**Exhaustive search.** Backtracking over the Eulerian walks, with a check of the read-path constraints at each step, is exact but takes exponential time in the worst case.

## Bounds

**Theorem (each edge once).** If $\mu(e) = 1$ for each edge, the problem can be solved in time $O(m + \sum_{P \in \mathcal{P}} |P|)$, and the Eulerian superpaths correspond one to one to the Eulerian paths of the merged graph.

*Proof.* Each edge occurs exactly once in an Eulerian walk $W$. So $P = e_1 \cdots e_p$ is a subpath of $W$ if and only if, for each $i < p$, the edge $e_{i+1}$ comes directly after $e_i$ in $W$. Let $F$ be the set of these pairs over all $P$. Then $W$ is a superpath if and only if each pair of $F$ is consecutive in $W$. An edge that occurs once has at most one successor and one predecessor in $W$, so if $F$ gives an edge two successors or two predecessors, there is no superpath. Otherwise $F$ splits the edges into disjoint chains and cycles. The last edge of $W$ has no successor in $W$, so if $F$ contains a cycle, there is no superpath. Merge each chain into one edge with the same first tail and last head. A walk in the merged graph expands to a walk in $G$ in which each chain is consecutive, and a walk in $G$ in which each chain is consecutive contracts to a walk in the merged graph. Both maps keep each edge used exactly once, so they are inverse bijections between the Eulerian superpaths and the Eulerian paths of the merged graph. Building $F$ and the chains takes $O(m + \sum |P|)$ time, and Hierholzer's algorithm takes $O(m)$. $\square$

By the BEST theorem, the number of Eulerian circuits of a directed graph can be computed in polynomial time. Add one edge from the end vertex to the start vertex of the merged graph; its Eulerian circuits correspond to the Eulerian paths, so in this case the number of superpaths can also be counted. If the count is above 1, the reads do not determine the genome.

**Hardness with multiplicities.** Kapun and Tsarev prove that the de Bruijn superwalk with multiplicities problem is NP-hard for each fixed alphabet with at least 2 letters and each positive $k$ (Theorem 2). This is the Eulerian superpath problem on de Bruijn graphs with $\mu$ in unary. So, unless P = NP, no polynomial algorithm solves the Eulerian superpath problem with multiplicities, and EULER's gap cannot be closed by a polynomial exact method.

**Hardness of the shortest superwalk.** Medvedev, Georgiou, Myers and Brudno prove that the shortest de Bruijn superwalk is NP-hard for alphabets with at least 3 letters (Theorem 2), by reduction from the [shortest common superstring](/shortest-common-superstring-np-hard/) problem.

**What is proved and what is not.** Proved: the case with each edge used once is polynomial; a cut of a removable edge is an equivalent transformation, by the argument in Known algorithms; the general problem with multiplicities is NP-hard. Stated in the EULER paper with an informal argument: a detachment of a resolvable edge is equivalent. Not proved: that the EULER sequence of detachments and cuts finishes, or that it finishes on real data. The success on bacterial genomes is an observation in the paper.

## Reductions

- **To the [Eulerian path problem](/eulerian-path-problem/).** With each edge used once, merging the forced pairs reduces the problem to an Eulerian path, as in the theorem above. With multiplicities, each successful detachment is a step of the same reduction.
- **From common superstring with multiplicities.** Kapun and Tsarev reduce from this problem: given binary strings and the numbers $l_0$ and $l_1$, find a binary string with $l_0$ zeros and $l_1$ ones that contains each given string. Take the graph with one vertex and two loops, one for the letter 0 with $\mu = l_0$ and one for the letter 1 with $\mu = l_1$. Each binary string is a walk, so the given strings become the path system, and the Eulerian superpaths are exactly the required strings.
- **From the shortest common superstring.** Medvedev and others insert a new letter between consecutive letters of each string and at both ends, so that a superwalk of the de Bruijn graph of the new strings corresponds to a superstring of the old ones.
- **To the [Chinese postman problem](/chinese-postman-problem/).** The shortest superwalk with single-edge read-paths is a Chinese postman tour.

## Applications

EULER (Pevzner, Tang and Waterman, 2001) used the problem as its model of assembly. It first corrected read errors, then built the de Bruijn graph of the reads and their reverse complements, and then applied detachments and cuts. EULER-DB added the mate-reads from clone-end pairs as more paths, which resolves tangles that no single read spans, and EULER-SF used the remaining mate pairs as bridges between contigs: it combined 91 contigs of *N. meningitidis* into 60 scaffolds. The later practice of [repeat resolution](/repeat-resolution/) in de Bruijn assemblers, which threads reads and read pairs through the graph, solves the same problem by heuristics. The hardness results explain why exact methods do not appear in these assemblers.

## References
