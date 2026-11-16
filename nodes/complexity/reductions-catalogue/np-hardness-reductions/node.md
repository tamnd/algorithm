---
tag: QB7YHZ
kind: technique
slug: np-hardness-reductions
name: Elementary NP-hardness reductions
aliases:
- Elementary hardness reductions
area: complexity/reductions-catalogue
level: core
summary: The three standard ways to build a Karp reduction for an NP-hardness proof, restriction, local replacement and component design, with the classic chain from SAT.
prereqs: [np-completeness-proof, gadget-reduction]
see_also: [karps-21-np-complete-problems, garey-johnson-compendium, strong-np-hardness, three-dimensional-matching, hamiltonian-cycle-np-completeness, traveling-salesman-decision, bin-packing-np-hardness, turing-reduction]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1, Six Basic NP-Complete Problems; Section 3.2, Some Techniques for Proving NP-Completeness (3.2.1 Restriction, p. 63; 3.2.2 Local Replacement, p. 66; 3.2.3 Component Design, p. 72); Section 4.2, Number Problems and Strong NP-Completeness; Section 5.1, Turing Reducibility and NP-Hard Problems
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 1972, 85-103"
    locator: the tree of reductions from satisfiability to 21 combinatorial problems
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage Learning, 2013
    locator: Section 7.5, Additional NP-complete problems
---

Most NP-hardness proofs build their [Karp reduction](/polynomial-time-reduction/) in one of three ways, which Garey and Johnson (1979, Section 3.2) name *restriction*, *local replacement* and *component design*. Restriction shows that the new problem contains a known NP-complete problem as a special case. Local replacement rewrites each basic piece of a known problem as a fixed structure of the new one. Component design builds the new instance from [gadgets](/gadget-reduction/) that act as variables and constraints. This page explains how to choose among the three and shows the classic chain of reductions from SAT that supplies the usual source problems.

## In plain words

There are three common ways to show that a new problem is hard. The first is to notice that a known hard problem is already hiding inside it, as a special case; then the new problem is at least as hard. The second is to take a known hard problem and swap each of its small pieces for a small piece of the new problem, the same way each time. The third, used when the two problems look nothing alike, is to build switches and checkers out of the new problem's parts and wire them together to imitate the old one. Try them in this order, since the first is the shortest proof and the third the longest.

## When it applies

Use these methods after the first two steps of an [NP-completeness proof](/np-completeness-proof/): you have a decision problem $L$, and you want a reduction to it from a known NP-complete problem $K$.

- **Restriction** applies when some known NP-complete problem is $L$ with extra conditions on the input, possibly after a trivial re-encoding.
- **Local replacement** applies when $K$ and $L$ have similar structure but different basic units, such as clauses of different widths, or directed and undirected graphs.
- **Component design** applies when no such likeness exists, and $L$ can express a binary choice and a local test ([gadget reduction](/gadget-reduction/)).

## The template

```pseudo id=template
CHOOSE-METHOD(L)
L1  if a known NP-complete K is a special case of L        ▷ restriction
L2      f(x) ← x written as an instance of L               ▷ hole: the embedding
L3  else if each unit of K maps to a fixed piece of L      ▷ local replacement
L4      f(x) ← x with each unit u replaced by REPLACE(u)   ▷ hole: REPLACE
L5  else                                                   ▷ component design
L6      f(x) ← VAR and CON gadgets for x, joined           ▷ holes: the gadgets
L7  prove the two directions for f and bound its cost
```

The holes are the source $K$, the embedding, REPLACE, and the gadgets.

- For **restriction**, the proof is short: the embedding is a polynomial-time map, and an instance of $K$ and its image have the same answer because the image *is* the same question in the language of $L$.
- For **local replacement**, each replacement must be correct in isolation: the replaced piece and its replacement have the same effect on the rest of the instance. Then the two directions follow piece by piece.
- For **component design**, use the four-part proof on [gadget reduction](/gadget-reduction/): consistency, local test, no leakage, both directions.

## Classic examples

### Restriction

- **[Traveling salesman](/traveling-salesman-decision/) from Hamiltonian cycle.** Give each edge of $G$ cost $1$ and each non-edge cost $2$, and ask for a tour of cost at most $n$. Such a tour uses only edges of $G$, so it is a Hamiltonian cycle. On the $5$-vertex house graph (a $5$-cycle with one chord) the cheapest tour costs $5$, a yes; on the $5$-vertex bowtie (two triangles sharing a vertex) it costs $6$, a no, since the shared vertex is a cut vertex.
- **[Exact cover by 3-sets](/exact-cover-by-3-sets/) from [3-dimensional matching](/three-dimensional-matching/).** A 3DM instance is an X3C instance whose ground set is split into three parts and whose sets take one element from each.
- **[Bin packing](/bin-packing-np-hardness/) from [partition](/partition-problem/).** Partition is bin packing with two bins of capacity half the total size.
- **[Hitting set](/hitting-set/) and [set cover](/set-cover/) from [vertex cover](/vertex-cover/).** A vertex cover is a hitting set for sets of size $2$, the edges.
- **[Knapsack (decision)](/knapsack-decision/) from [subset sum](/subset-sum-problem/).** Take each value equal to its weight and the value target equal to the capacity.

### Local replacement

- **[3-SAT](/3-sat/) from SAT.** A clause $(\ell_1 \lor \cdots \lor \ell_k)$ with $k \ge 4$ becomes $k - 2$ clauses of width three with $k - 3$ new variables; $(x_1 \lor \neg x_2 \lor x_3 \lor x_4 \lor \neg x_5)$ becomes $(x_1 \lor \neg x_2 \lor z_1) \land (\neg z_1 \lor x_3 \lor z_2) \land (\neg z_2 \lor x_4 \lor \neg x_5)$. Each of the $32$ assignments to $x_1, \ldots, x_5$ satisfies the clause exactly when some values of $z_1, z_2$ satisfy the replacement. Clauses with one or two literals are padded with new variables (Garey and Johnson, Section 3.1.1).
- **Undirected from directed Hamiltonian cycle.** Replace each vertex $v$ by a path $v_{\text{in}} - v_{\text{mid}} - v_{\text{out}}$ and each arc $(u, v)$ by the edge $u_{\text{out}} - v_{\text{in}}$. The middle vertex has degree $2$, which forces every Hamiltonian cycle to go through each triple in order, in one direction.
- **[Circuit satisfiability](/circuit-sat/) to SAT.** The [Tseitin transformation](/tseitin-transformation/) replaces each gate by a fixed set of clauses on its input and output variables.

### Component design

- **Vertex cover from 3-SAT** (Garey and Johnson, Section 3.1.3): an edge per variable, a triangle per clause, and budget $n + 2m$. Worked with numbers on [gadget reduction](/gadget-reduction/).
- **3-dimensional matching from 3-SAT** (Section 3.1.2): a truth-setting component per variable, a ring of triples whose two ways of covering its inner elements encode true and false; a satisfaction-testing component per clause; and a garbage-collection component that covers the elements left over.
- **Hamiltonian cycle from vertex cover** (Section 3.1.4): a $12$-vertex gadget per edge; see [Hamiltonian cycle NP-completeness](/hamiltonian-cycle-np-completeness/).
- **[3-coloring](/three-coloring/) from 3-SAT**: a palette triangle, a pair of vertices per variable and OR gadgets per clause.

### The basic chain

Garey and Johnson (Section 3.1) prove six basic problems NP-complete in a tree rooted at SAT: SAT to 3-SAT; 3-SAT to 3-dimensional matching and to vertex cover; 3-dimensional matching to partition; vertex cover to Hamiltonian cycle and to clique. Most later proofs start from one of these six. Karp's paper gives a similar tree for $21$ problems ([Karp's 21 NP-complete problems](/karps-21-np-complete-problems/), and the reductions on [Karp's 21 reductions](/karp-21-np-complete/)).

## Variations

- **Strong NP-hardness.** Partition has a pseudo-polynomial algorithm, so a reduction from it may produce numbers exponentially large in the input size, and then the target may still have a pseudo-polynomial algorithm. To rule out pseudo-polynomial algorithms, reduce from a [strongly NP-hard](/strong-np-hardness/) source such as [3-partition](/three-partition/), with all numbers bounded by a polynomial in the input size (Garey and Johnson, Section 4.2).
- **Hardness under Cook reductions.** For search and optimization problems, Garey and Johnson (Section 5.1) define NP-hardness with [Cook reductions](/turing-reduction/), which may ask many questions.
- **Variants of satisfiability as sources.** [Not-all-equal SAT](/not-all-equal-sat/), [one-in-three SAT](/one-in-three-sat/) and [0-1 equations](/zero-one-equations/) have more symmetric constraints than 3-SAT and often give simpler gadgets.
- **Approximation hardness.** The same methods with [gap-preserving reductions](/gap-preserving-reduction/) carry hardness of approximation instead of hardness of exact solution.

## Pitfalls

- **Restriction in the wrong direction.** Restriction proves $L$ hard when the *known* problem is a special case of $L$. If $L$ is a special case of a hard problem, nothing follows: 2-SAT is a special case of SAT and is in P.
- **The embedding must be exact.** In restriction, the special case must be a set of instances of $L$ with exactly the same yes-instances, and the encoding change must be polynomial. Weights $1$ and $2$ for TSP are fine; weights that list all paths would not be.
- **Edge cases in local replacement.** A replacement that assumes long clauses fails on clauses of width $1$ or $2$, or on clauses with a repeated variable. Handle every unit shape.
- **Gadget leakage.** In component design, solutions can use a gadget in an unplanned state or share parts between gadgets. Prove consistency and no leakage, not only the intended behavior.
- **Weak results for number problems.** A reduction from partition only gives weak NP-hardness; do not claim more.

## Exercises

1. Use restriction to show that the problem "does a graph have a simple path with at least $k$ edges?" is NP-complete.
2. Use local replacement to reduce 3-SAT to the version of 3-SAT where every variable occurs at most three times. Hint: replace the occurrences of a variable by new variables joined in a cycle of implications.
3. Use component design to show [dominating set](/dominating-set/) NP-complete, starting from vertex cover. Hint: add a new vertex for each edge, joined to both of its ends.
4. Explain why restriction from partition shows bin packing NP-hard only in the weak sense, and what source would give strong NP-hardness.

## References
