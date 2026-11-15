---
tag: BG84GN
kind: concept
slug: garey-johnson-compendium
name: Garey-Johnson compendium of NP-complete problems
aliases:
- Computers and Intractability
- Garey-Johnson catalogue
area: complexity/np-completeness
level: core
summary: "The appendix of Garey and Johnson's 1979 book: more than 300 NP-complete and NP-hard problems in 12 areas, each with its source and special cases, plus 12 open problems."
prereqs: [np-complete, karps-21-np-complete-problems]
see_also: [karp-21-np-complete, np-hard, strong-np-hardness, pseudo-polynomial-time, cook-levin-theorem, graph-isomorphism-problem, precedence-constrained-scheduling, np-intermediate]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman (1979)
    locator: Appendix, A List of NP-Complete Problems (from p. 187; A1 Graph Theory p. 190 to A12 Miscellaneous p. 279, A13 Open Problems p. 285); Section 3.1 (six basic NP-complete problems); Section 3.2 (restriction, local replacement, component design); Section 4.2 (strong NP-completeness); Update for the Current Printing (p. 339)
  - paper: doi:10.1145/1077464.1077476
    title: David S. Johnson, The NP-completeness column, ACM Transactions on Algorithms 1(1), 160 to 176 (2005)
    locator: the history of the column and Table I (the status of the open problems of Garey and Johnson and of the earlier columns)
  - paper: "David S. Johnson, A brief history of NP-completeness, 1954-2012, Documenta Mathematica, Extra Volume: Optimization Stories (2012), 359 to 376"
    locator: the section on the book and the status of its open problems
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press (1972), 85 to 103
    locator: the Main Theorem (the 21 problems that started the list)
---

The Garey-Johnson compendium is the appendix "A List of NP-Complete Problems" in Michael Garey and David Johnson's 1979 book *Computers and Intractability: A Guide to the Theory of NP-Completeness*. It lists more than 300 decision problems that are [NP-complete](/np-complete/) or [NP-hard](/np-hard/), sorted into 12 areas, from graph theory to automata theory. Each entry gives the instance, the question, the reduction that proves hardness and its source, and comments on special cases that are easy or still hard. A thirteenth part lists 12 problems in NP whose status was open in 1979. For decades the compendium was the first place to look before trying to prove a new problem hard, and the book is still the standard reference for its codes, such as GT1 for vertex cover.

## In plain words

When you meet a new problem and cannot find a fast method, you want to know if someone has already shown that the problem is hard. Garey and Johnson collected several hundred problems that are known to be as hard as any problem whose answers are easy to check. They wrote each one in the same short form: what the input is, what yes-or-no question is asked, who proved that it is hard and from which other problem, and which special cases are easy. The list is sorted by topic and each problem has a short code. So a reader can find a problem close to their own, take the known proof as a model, and often prove their problem hard in a few lines. The list also names a few problems that nobody could place.

## The idea

**The form of an entry.** Each entry has a code, a name in capitals, and fields: INSTANCE (the input), QUESTION (the yes-or-no question), Reference (the paper that proved hardness, with the problem it was reduced from), and Comment (variants, special cases in P, cases that stay hard, and whether the problem is hard in the strong sense). The code is two letters for the area and a number. For example:

- GT1 is VERTEX COVER, the first problem of the graph theory part.
- GT19 is CLIQUE.
- ND22 is the TRAVELING SALESMAN problem, in network design.
- LO1 is SATISFIABILITY, the first problem of the logic part.

**The parts.** The appendix has 12 parts of problems and one of open problems:

| Part | Area | Starts on page |
|---|---|---|
| A1 | Graph theory | 190 |
| A2 | Network design | 206 |
| A3 | Sets and partitions | 221 |
| A4 | Storage and retrieval | 226 |
| A5 | Sequencing and scheduling | 236 |
| A6 | Mathematical programming | 245 |
| A7 | Algebra and number theory | 249 |
| A8 | Games and puzzles | 254 |
| A9 | Logic | 259 |
| A10 | Automata and language theory | 265 |
| A11 | Program optimization | 272 |
| A12 | Miscellaneous | 279 |
| A13 | Open problems | 285 |

**Decision problems and reductions.** Every entry is a [decision problem](/decision-problem/). An optimization problem appears as its threshold form ("is there a vertex cover of size $K$ or less?"). The hardness proofs are polynomial-time many-one ([Karp](/polynomial-time-reduction/)) reductions, which Garey and Johnson call polynomial transformations. Some entries are NP-hard problems that are not known to be in NP, for example some games and some problems on automata; Chapter 5 of the book treats NP-hardness and Turing ([Cook](/turing-reduction/)) reductions. For problems with numbers, the comments often say whether the problem is NP-complete in the strong sense (Section 4.2). A number problem that is not strongly NP-complete may have a [pseudo-polynomial-time](/pseudo-polynomial-time/) algorithm.

**How the list grew.** The 21 problems of [Karp's 1972 paper](/karps-21-np-complete-problems/) are all in the list or close to entries in it. Section 3.1 of the book proves six basic problems NP-complete: 3-SAT, 3-dimensional matching, vertex cover, clique, Hamiltonian circuit and partition. Section 3.2 describes three methods of proof that most entries use: restriction, local replacement and component design.

## Examples

**A proof by restriction.** Hitting set asks: given subsets $C_1, \ldots, C_m$ of a set $S$ and a number $K$, is there a set $S' \subseteq S$ with $|S'| \le K$ that contains at least one element of each $C_i$? It is in NP: the set $S'$ is a certificate. If every $C_i$ has exactly 2 elements, the sets are the edges of a graph on $S$ and $S'$ is a vertex cover. So vertex cover (GT1) is a special case of hitting set, and the identity map is a Karp reduction from vertex cover to hitting set. Hence hitting set is NP-complete. A script checked the identity on two graphs. The 5-cycle, seen as 5 sets of size 2, has smallest hitting set size 3, and there are 5 hitting sets of that size, the first being $\{0, 1, 3\}$; this is the smallest vertex cover. The Petersen graph, as 15 sets of size 2, has smallest hitting set size 6, with 5 hitting sets of that size. The restriction goes one way only: the instance $\{0,1,2\}, \{2,3\}, \{3,4\}, \{0,4\}$ has a set of size 3, so it is not a graph, and the script found its smallest hitting sets $\{0, 3\}$ and $\{2, 4\}$ directly. This is the shortest kind of NP-completeness proof, and the compendium makes it easy because it lists the special cases.

**The open problems of 1979.** Part A13 lists 12 problems in NP that were not known to be in P or NP-complete: graph isomorphism, subgraph homeomorphism, graph genus, chordal graph completion, chromatic index, spanning tree parity, partial order dimension, precedence constrained 3-processor scheduling, linear programming, total unimodularity, composite number and minimum length triangulation. Johnson's 2005 column records that 9 of the 12 were settled by then. His 2012 history says that only two remain open: [graph isomorphism](/graph-isomorphism-problem/) and [precedence constrained 3-processor scheduling](/precedence-constrained-scheduling/). Some of the settled ones:

- Linear programming is [in P](/lp-in-p/).
- Composite number is in P, because primality is ([AKS primality test](/aks-primality-test/)).
- [Chromatic index](/chromatic-index/) is NP-complete, even for 3 colors on cubic graphs ([edge coloring](/edge-coloring/)).
- [Graph genus](/graph-genus/) is NP-complete.

Graph isomorphism is now known to be solvable in [quasi-polynomial time](/quasi-polynomial-time/), which makes it unlikely to be NP-complete, but it is still not known to be in P.
## Where it is used

- **Before a hardness proof.** A researcher who suspects that a problem is NP-complete looks for an entry with the same structure and reduces from it. The codes (GT1, ND22, LO1) are still used in papers to name problems without ambiguity.
- **In teaching.** The book teaches the method of NP-completeness proofs, and the compendium gives many problems on which to practice it.
- **For special cases.** The comments of an entry often say which restrictions are in P (for example planar graphs, bounded degree, or trees) and which stay NP-complete. This helps a designer choose between an exact algorithm for a special case and an approximation or a heuristic for the general case.
- **Updates.** Johnson kept the list up to date in "The NP-completeness column", first in the Journal of Algorithms from 1981 and later in ACM Transactions on Algorithms. The 2005 column gives a table of the status of the open problems. The compendium covers only results up to the book, so later results must be found in these columns and in the literature. Later printings of the book also have an "Update for the Current Printing" (p. 339).

## References
