---
tag: HH185A
kind: algorithm
slug: fci-algorithm
name: FCI algorithm
aliases:
- fast causal inference
area: statistics-and-inference/causal-inference-and-experimental-design
level: research
summary: Extends the PC algorithm to allow latent confounders, and outputs a partial ancestral graph of the features all compatible models share.
model: real-ram
complexity:
  vars: {n: the number of observed variables}
  time: {worst: "O(n^2 2^n)", best: "Θ(n^2)"}
  space: {extra: "O(n^3)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1993
  people: [Peter Spirtes, Clark Glymour, Richard Scheines]
  note: Spirtes, Glymour and Scheines gave FCI in Causation, Prediction, and Search; Zhang (2008) added the rules that make the orientation complete.
prereqs: [pc-algorithm, d-separation, conditional-independence, directed-acyclic-graph, structural-causal-model]
see_also: [greedy-equivalence-search, lingam, front-door-criterion, instrumental-variables-estimation, backdoor-criterion, do-calculus, bayesian-network-structure-learning, markov-blanket]
sources:
  - book: isbn:9780262194402
    title: "Peter Spirtes, Clark Glymour and Richard Scheines, Causation, Prediction, and Search, 2nd edition, MIT Press, 2000"
    locator: Chapter 6 (causal discovery with latent variables, with the FCI algorithm and Possible-D-SEP; general locator)
  - paper: "Peter Spirtes, Christopher Meek and Thomas Richardson, Causal inference in the presence of latent variables and selection bias, Proceedings of the 11th Conference on Uncertainty in Artificial Intelligence (UAI 1995), Morgan Kaufmann, pp. 499 to 506"
    locator: The whole paper (FCI with selection bias, and the correctness of its skeleton and orientation steps)
  - paper: doi:10.1214/aos/1031689015
    title: "Thomas Richardson and Peter Spirtes, Ancestral graph Markov models, The Annals of Statistics 30(4), 2002, pp. 962 to 1030"
    locator: The whole paper (maximal ancestral graphs, m-separation, and the MAG of a DAG with latent and selection variables)
  - paper: doi:10.1016/j.artint.2008.08.001
    title: "Jiji Zhang, On the completeness of orientation rules for causal discovery in the presence of latent confounders and selection bias, Artificial Intelligence 172(16-17), 2008, pp. 1873 to 1896"
    locator: The whole paper (the rules R1 to R10, their soundness, and the completeness of the augmented FCI)
  - paper: doi:10.1214/11-AOS940
    title: "Diego Colombo, Marloes H. Maathuis, Markus Kalisch and Thomas S. Richardson, Learning high-dimensional directed acyclic graphs with latent and selection variables, The Annals of Statistics 40(1), 2012, pp. 294 to 321"
    locator: The whole paper (the RFCI variant and the consistency of FCI and RFCI in high dimensions)
---

The FCI algorithm (fast causal inference) learns causal structure from [conditional independence](/conditional-independence/) when some common causes are not measured. Like the [PC algorithm](/pc-algorithm/), it removes the edge between two variables when some set makes them independent, and then reads directions from the colliders that the removals reveal. Hidden variables make two changes. A pair can need a separating set with variables that are not its neighbours, so FCI searches a larger set called Possible-D-SEP. And an edge can stand for a hidden common cause, so FCI puts a mark at each end of an edge: an arrowhead, a tail, or a circle for "not known". The output is a partial ancestral graph (PAG), the features that all models compatible with the independences share.

## In plain words

Suppose some causes in the system were never measured. Two measured variables can then be linked only because a hidden variable drives both. FCI first removes links between variables that some other variables make unrelated, as PC does, but it also searches farther away for those other variables, because hidden causes can hide the separating ones. Then it marks each end of each link. An arrowhead at a variable says that it does not cause the variable at the other end. A tail says that it does cause it. A circle says that the data cannot decide. Arrowheads at both ends say that neither causes the other, so a hidden cause links them.

## The problem

The input is a finite set $V$ of $n$ observed variables and a test $\mathrm{CI}(a, b, S)$ for $a \perp b \mid S$ with $S \subseteq V$. The analysis assumes a DAG $G$ on $V \cup L$, where $L$ is a set of latent variables, such that among the observed variables the independences are exactly the [d-separations](/d-separation/) of $G$. Unlike PC, FCI does not assume causal sufficiency: latent variables can be common causes of observed ones. This page and the implementation also assume no selection bias. The general algorithm allows it and has three more rules for it.

Many DAGs with latent variables give the same independences, so FCI works with a summary of them. The maximal ancestral graph (MAG) of $G$ over $V$ has an edge between $a$ and $b$ when no set of other observed variables separates them. The edge is $a \to b$ when $a$ is an ancestor of $b$ in $G$, and $a \leftrightarrow b$ when neither is an ancestor of the other. In a MAG an arrowhead at $b$ thus means "$b$ is not an ancestor of $a$", and a tail at $a$ means "$a$ is an ancestor of $b$". Separation in a MAG (m-separation) is d-separation with $\leftrightarrow$ edges allowed, and it gives the same answers as d-separation in $G$. Two MAGs are Markov equivalent when they give the same separations.

The output is the PAG of the class of the MAG of $G$: the common skeleton of the class, with an arrowhead or a tail at an end when every MAG of the class has that mark there, and a circle where two MAGs of the class differ. In text form an edge is written with its two marks, such as `A o-> B` (circle at $A$, arrowhead at $B$), `B <-> C` and `A --> D`. The symbol `*` below stands for any mark.

## The algorithm

Two definitions are needed. A triple $a, c, b$ is unshielded when $a - c$ and $c - b$ are edges and $a$ and $b$ are not adjacent. The set $\mathrm{PDS}(a)$ (Possible-D-SEP) of the graph after line L3 holds every node $b \ne a$ joined to $a$ by a path on which every inner triple $x, y, z$ has a collider at $y$ (arrowheads at $y$ on both edges) or has $x$ and $z$ adjacent.

```pseudo id=main
FCI(V, CI)
L1  run the skeleton phase of PC on V, which gives a skeleton C and sepsets
L2  give every edge of C the mark o at both ends
L3  for each unshielded triple a, c, b with c ∉ sepset(a, b), orient a *→ c ←* b
L4  for each edge a - b of C and each x in {a, b} do
L5      for each S ⊆ PDS(x) \ {a, b}, smallest first do
L6          if CI(a, b, S) then delete a - b; sepset(a, b) ← S; go to the next edge
L7  set every mark back to o
L8  for each unshielded triple a, c, b with c ∉ sepset(a, b), orient a *→ c ←* b
L9  repeat
L10     apply R1, R2, R3 and R4 where they match
L11     apply R8, R9 and R10 to the edges a o→ c
L12 until no rule applies;  return the PAG
```

Line L1 is lines L1 to L6 of PC. Lines L2 and L3 make a first PAG, used only to compute $\mathrm{PDS}$. Lines L4 to L6 test sets inside it. Lines L7 and L8 orient the colliders again on the final skeleton. The rules of lines L10 and L11 are those of Zhang (2008), with the edge to change written last:

- **R1.** If `a *-> b o-* c` and $a$, $c$ are not adjacent, orient `b --> c`.
- **R2.** If `a --> b *-> c` or `a *-> b --> c`, and `a *-o c`, orient `a *-> c`.
- **R3.** If `a *-> b <-* c`, `a *-o d o-* c`, $a$ and $c$ are not adjacent, and `d *-o b`, orient `d *-> b`.
- **R4.** A discriminating path for $b$ is a path $\theta, \dots, \alpha, b, c$ on which $\theta$ is not adjacent to $c$ and every node between $\theta$ and $b$ is a collider on the path and a parent of $c$. If `b o-* c` ends such a path, orient `b --> c` when $b \in \mathrm{sepset}(\theta, c)$, and `α <-> b <-> c` otherwise.
- **R8.** If `a --> b --> c` or `a -o b --> c`, and `a o-> c`, orient `a --> c`.
- **R9.** If `a o-> c` and there is an uncovered potentially directed path $a, b, \theta, \dots, c$ with $b$ and $c$ not adjacent, orient `a --> c`.
- **R10.** If `a o-> c`, `b --> c <-- t`, and there are uncovered potentially directed paths from $a$ to $b$ and from $a$ to $t$ whose second nodes are distinct and not adjacent, orient `a --> c`.

A path is uncovered when every two nodes two steps apart on it are not adjacent, and potentially directed when no edge on it has an arrowhead pointing back or a tail pointing forward. R5 to R7 handle selection bias and are not needed here.

## Example

**PC fails, FCI does not.** Let $G$ be $A \to B \leftarrow L \to C \leftarrow D$ with $L$ latent. The skeleton phase removes $A - C$, $A - D$ and $B - D$, each with the empty set as separating set, and leaves $A - B - C - D$. Both unshielded triples are colliders: $A, B, C$ puts arrowheads at $B$, and $B, C, D$ puts arrowheads at $C$. FCI returns

`A o-> B`, `B <-> C`, `C <-o D`.

The edge `B <-> C` says correctly that neither of $B$, $C$ causes the other. PC on the same oracle meets two colliders that direct $B - C$ both ways, keeps the first arrow, and returns $A \to B \leftarrow C \leftarrow D$, a false claim that $C$ causes $B$. PC makes 13 calls to the oracle here, and FCI makes 37.

**The Possible-D-SEP phase.** Let $G$ have the arrows $C \to B \to A \to D$ and $E \to F$, and the latent variables $L_1$ with children $A, F$, $L_2$ with children $C, E$ and $L_3$ with children $D, E$. Its MAG is `A --> D`, `A <-- B`, `A <-> F`, `B <-- C`, `C <-> E`, `D <-> E`, `E --> F`.

- After line L1 the skeleton still has $D - F$. The sets that PC tries are subsets of the other neighbours $\{A, E\}$ of $D$ or of $F$, and none of them works. The empty set and $\{E\}$ leave $D \leftarrow A \leftarrow L_1 \to F$ open, $\{A\}$ leaves $D \leftarrow L_3 \to E \to F$ open, and $\{A, E\}$ leaves $D \leftarrow L_3 \to E \leftarrow L_2 \to C \to B \to A \leftarrow L_1 \to F$ open, because its colliders $E$ and $A$ are in the set.
- After line L3 the graph is `A <-> F`, `A <-o B`, `A o-> D`, `B o-o C`, `C o-> E`, `D <-> E`, `D o-o F`, `E o-> F`. The node $B$ is in $\mathrm{PDS}(D)$ through the path $D, F, A, B$: the triple $D, F, A$ is shielded by the edge $A - D$, and $A$ is a collider on $F, A, B$.
- Line L6 finds $D \perp F \mid \{A, B, E\}$ and removes $D - F$.
- Line L8 orients the colliders again, which gives `A o-> D` and `E o-> F`. The triple $F, A, D$ is now unshielded, and `F <-> A o-> D` matches R1, so the edge becomes `A --> D`. In the same way `D <-> E o-> F` gives `E --> F`.

The output is `A --> D`, `A <-> F`, `A <-o B`, `B o-o C`, `C o-> E`, `D <-> E`, `E --> F`, after 329 calls. Every non-circle mark agrees with the MAG, and the circles are where MAGs of the class differ. Without lines L4 to L6, the output keeps a false edge `D <-> F`.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is partial. With a perfect oracle it proves:

1. **Termination and skeleton.** All phases stop. No edge of the MAG is removed, because adjacent nodes of the MAG are not separated by any set, and each removed pair has a true separating set.
2. **Colliders.** In every MAG of the class, a node $c$ of an unshielded triple $a, c, b$ is a collider exactly when $c$ is outside one (and then every) separating set of $a$ and $b$. So line L8 puts arrowheads only where every MAG of the class has them.
3. **R1 to R3.** These rules are sound. An arrowhead at $b$ means that $b$ is not an ancestor of the other end, and a tail means that it is. With these readings, R1 avoids a collider that the class does not have, and R2 and R3 avoid an arrowhead at a node that is an ancestor.

Cited, not proved: that the Possible-D-SEP phase removes every edge not in the MAG (Spirtes, Meek and Richardson 1995; Spirtes, Glymour and Scheines 2000), the soundness of R4 and R8 to R10, and the completeness theorem of Zhang (2008): with no selection bias, R1 to R4 and R8 to R10 leave a circle exactly where two MAGs of the class differ. The tests check the full output against the PAG of every class of MAGs on three and four nodes.

## Complexity

The cost is counted in calls to the test. Line L1 makes at most $n(n - 1)\sum_{k}\binom{n - 2}{k} = n(n - 1)2^{n - 2}$ tests, as PC does. Lines L4 to L6 test at most $2 \cdot 2^{n - 2}$ sets for each of at most $\binom n2$ edges, which is again at most $n(n - 1)2^{n - 2}$. So the worst case is $O(n^2 2^n)$ tests. Unlike in PC, this bound does not become polynomial for sparse graphs: in the second example every node has all other nodes in its $\mathrm{PDS}$. The best case is the empty graph, with $\binom n2$ tests and nothing for lines L4 to L6. The separating sets take $O(n^3)$ space.

The rules cost no tests. The implementation finds discriminating paths and uncovered potentially directed paths by depth-first search over simple paths, which is short to write but exponential in the worst case.

## Properties

- **Exact with an oracle.** With a perfect test and no selection bias, the output is the PAG of the class of the true MAG. Part of this is proved here, and the rest is cited.
- **Causal reading of marks.** A tail at $a$ on an edge to $b$ says that $a$ causes $b$, directly or through other variables, in every model of the class. `a <-> b` says that neither causes the other, so a latent variable links them. A circle says nothing.
- **Weaker than PC without latent variables.** When $G$ has no latent variables, the output has the skeleton and the colliders of the CPDAG of $G$, but with fewer tails. For $A \to C \leftarrow B$ it gives `A o-> C <-o B`, because the model `A <-> C <-- B` has the same independences.
- **Order dependent with data.** As in PC, the skeleton depends on the order of the tests when the tests make errors.

## Variants and improvements

- **Selection bias.** The full algorithm of Zhang (2008) adds rules R5 to R7 for undirected edges, which appear when the sample was selected on a variable that the causes affect.
- **RFCI.** Colombo, Maathuis, Kalisch and Richardson (2012) replace the Possible-D-SEP phase by a few extra tests on the triples that the orientation uses. The output can have extra edges but its marks are still correct as ancestral claims, and it runs much faster. They also proved high-dimensional consistency of FCI and RFCI for sparse graphs.
- **Stable versions.** Colombo and Maathuis (2014) gave FCI-stable and conservative versions that do not depend on the order of the variables.
- **Other methods.** [Greedy equivalence search](/greedy-equivalence-search/) uses a score but assumes no latent variables. [LiNGAM](/lingam/) finds a full DAG from non-Gaussian data, also without latent variables.

## When to use it

Use FCI when hidden common causes are likely and you want only claims that hold whatever the hidden structure is. The output tells which causal claims the independences support, and which pairs share a hidden cause. For a target effect, a tail or an arrowhead can be enough to choose an [adjustment set](/backdoor-criterion/) or to rule one out. If all common causes are measured, PC gives more directed edges for less work. With many variables, use RFCI or limit the size of the conditioning sets.

## Pitfalls

- **Circles are not arrows.** `a o-> b` does not say that $a$ causes $b$; it says only that $b$ does not cause $a$.
- **The rules matter.** On the 2492 MAGs on four nodes, the output after line L8 without the rules differed from the PAG on 552 of them.
- **Large conditioning sets.** The Possible-D-SEP phase tests sets of any size. With data, these tests have little power, and a wrong removal spreads through the rules. The phase is rarely needed in small graphs: it removed an edge for 0 of 3000 random DAGs with one or two latent variables and five or six observed ones, and for 10 of 2362 random MAGs on seven nodes. These rates are measured, not proved.
- **Faithfulness.** As in PC, near cancellations of paths make tests remove true edges.
- **Selection bias.** The implementation assumes there is none. If the sample is selected on an effect, use the full rule set.

## Implementations

## History

Spirtes, Glymour and Scheines gave the FCI algorithm in *Causation, Prediction, and Search* (1993). Spirtes, Meek and Richardson (1995) extended it to selection bias. Richardson and Spirtes (2002) put the output on the footing of maximal ancestral graphs. Zhang (2008) added the rules R5 to R10 and proved that the augmented rules are complete, so that each remaining circle is a real ambiguity. Colombo, Maathuis, Kalisch and Richardson (2012) gave the faster RFCI and proved high-dimensional consistency.

## References
