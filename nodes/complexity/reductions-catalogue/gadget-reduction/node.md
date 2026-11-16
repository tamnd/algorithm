---
tag: EF7D9Q
kind: technique
slug: gadget-reduction
name: Gadget reduction
aliases:
- gadget
- gadget construction
- local replacement
area: complexity/reductions-catalogue
level: core
summary: A reduction built from small fixed pieces of the target problem, one per variable and one per constraint, joined so that solutions of the whole match solutions of the source.
prereqs: [polynomial-time-reduction, 3-sat]
see_also: [np-hardness-reductions, np-completeness-proof, three-coloring, vertex-cover, hamiltonian-cycle-np-completeness, maximum-cut, gap-preserving-reduction, reduction]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.3 (VERTEX COVER from 3SAT), Section 3.1.4 (HAMILTONIAN CIRCUIT), Section 3.2.2, Local Replacement (p. 66), and Section 3.2.3, Component Design (p. 72)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 1972, 85-103"
    locator: the reductions from satisfiability, including chromatic number and the clique, node cover and Hamiltonian circuit problems
  - paper: doi:10.1137/S0097539797328847
    title: "Luca Trevisan, Gregory B. Sorkin, Madhu Sudan and David P. Williamson, Gadgets, approximation, and linear programming, SIAM Journal on Computing 29(6) (2000), 2074-2097"
    locator: the definition of gadgets for approximation-preserving reductions, optimal gadgets found by linear programming, and the hardness of Max Cut within 16/17 + epsilon and Max DiCut within 12/13 + epsilon
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage Learning, 2013
    locator: Section 7.5, Additional NP-complete problems (gadgets in the reductions to vertex cover and Hamiltonian path)
---

A gadget reduction builds an instance of the target problem out of small, fixed pieces called gadgets: one piece for each variable of the source instance, one piece for each constraint, and edges or shared elements that join them. Each variable gadget has exactly two kinds of good states, read as true and false, and each constraint gadget can be completed exactly when the states of its variables satisfy the constraint. Then a solution of the whole target instance is the same as a satisfying assignment of the source. Garey and Johnson (1979, Section 3.2) call this method component design, and the special case where each piece of the source is replaced by a fixed structure local replacement.

## In plain words

To show that a new puzzle is at least as hard as a known one, you build a machine out of the new puzzle's parts that imitates the old one. One small part acts as a switch that must be set on or off. Another small part acts as a checker for one rule of the old puzzle: it can be finished only if at least one of the switches it watches is in the right position. Wire one switch for each variable and one checker for each rule. If the old puzzle has a solution, set the switches to match it and finish every checker. If the new puzzle is solved, read the switch positions; every checker was finished, so every rule holds. The hard work is to design parts that cannot be used in any unplanned way.

## When it applies

Use a gadget reduction when the target problem has no obvious relation to the source, but it can express two things.

- **A binary choice.** A small structure whose good solutions fall into exactly two classes, such as an edge where a vertex cover of budget one takes one end or the other, or two adjacent vertices that must get different colors.
- **A local test.** A small structure attached to a few choices that can be completed if and only if a given constraint on them holds, such as a triangle that needs a free corner, or a sub-graph that can be colored only if one of its inputs has a given color.

The source is usually [3-SAT](/3-sat/), because its constraints are small and all of the same shape. If the target instance is a restricted version of the source, use restriction instead; if one constraint type can be replaced by a fixed formula of another type, use local replacement (see Variations and [elementary NP-hardness reductions](/np-hardness-reductions/)).

## The template

```pseudo id=template
GADGET-REDUCTION(φ)               ▷ φ: variables x1..xn, constraints C1..Cm
L1  H ← SHARED()                    ▷ hole: common structure, e.g. a palette
L2  for i ← 1 to n
L3      add VAR(i) to H              ▷ hole: two classes of good states
L4  for j ← 1 to m
L5      add CON(Cj) to H             ▷ hole: completable iff Cj holds
L6      join CON(Cj) to VAR(i) for each xi in Cj
L7  k ← BUDGET(n, m)                ▷ hole: the target size or bound
L8  return (H, k)
```

The holes are SHARED, VAR, CON, the joins in L6 and BUDGET. Each gadget has constant size, so $H$ has size $O(n + m)$ and is built in linear time.

A proof that the reduction is correct has four parts.

1. **Consistency.** In every solution of $(H, k)$, each VAR gadget is in one of its two good states. The budget or the shared structure must force this.
2. **Local test.** A CON gadget can be completed, given the states of the VAR gadgets it is joined to, if and only if those states satisfy the constraint.
3. **No leakage.** The gadgets interact only through the joins in L6, so completing one CON gadget does not affect another.
4. **Both directions.** From a satisfying assignment, set each VAR gadget and complete each CON gadget (by 2). From an arbitrary solution of $(H, k)$, read an assignment from the VAR gadgets (by 1); it satisfies every constraint (by 2 and 3).

## Classic examples

### 3-SAT to vertex cover

This is the component design proof of Garey and Johnson (Section 3.1.3). For a formula with $n$ variables and $m$ clauses:

- VAR($i$) is an edge between vertices $u_i$ and $\bar u_i$.
- CON($C_j$) is a triangle on three new vertices, one for each literal of $C_j$.
- L6 joins the triangle vertex of literal $\ell$ to the vertex of $\ell$ in its VAR edge.
- BUDGET is $k = n + 2m$.

Every vertex cover takes at least one end of each VAR edge and at least two corners of each triangle, which is already $n + 2m$ vertices. So a cover of size $k$ takes exactly one end of each VAR edge (consistency) and exactly two corners of each triangle. The uncovered corner's join edge must be covered from the VAR side, so its literal is the chosen end, which means true (local test). Conversely, from a satisfying assignment, take the true end of each VAR edge and, in each clause, all corners except one whose literal is true.

For $\varphi = (x_1 \lor x_2 \lor \neg x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor \neg x_3)$ the graph has $15$ vertices, $21$ edges and $k = 9$, and it has a vertex cover of size $9$. For the formula with all $8$ clauses on $x_1, x_2, x_3$, which is unsatisfiable, the graph has $30$ vertices, $51$ edges and $k = 19$, and it has no cover of size $19$. On all $255$ formulas made of distinct clauses on three variables, the graph has a cover of size $k$ exactly when the formula is satisfiable.

### 3-SAT to 3-coloring

- SHARED is a palette triangle with vertices named T, F and B; in any 3-coloring they get three different colors, which we call true, false and base.
- VAR($i$) is two vertices $v_i$ and $v_{\neg i}$, joined to each other and to B. So one is colored true and the other false (consistency).
- CON($a \lor b \lor c$) uses an *OR gadget*: a triangle $p, q, r$ with edges $a$-$p$ and $b$-$q$, whose output is $r$. If $a$ and $b$ are both true, then $p$ and $q$ avoid true, so $r$ is true. If both are false, $r$ is false. If they differ, $r$ can take any color. So $r$ can be true if and only if $a$ or $b$ is true. The clause gadget is two OR gadgets in series, OR(OR($a$, $b$), $c$), with $6$ new vertices, and the final output is joined to F and B, which forces it to be true.

Over all $8$ colorings of the inputs $a$, $b$ and $c$ with the colors true and false, the clause gadget extends to a proper coloring if and only if at least one input is true. The graph has $3 + 2n + 6m$ vertices and $3 + 3n + 12m$ edges; for the $\varphi$ above that is $27$ vertices and $48$ edges, and it is 3-colorable. The same equivalence held on all $255$ formulas made of distinct clauses on three variables. The page [3-coloring](/three-coloring/) gives the full proof.

### 3-SAT to independent set

VAR has no separate structure: the joins are edges between opposite literals. CON($C_j$) is a triangle, and BUDGET is $m$. An independent set of size $m$ takes one vertex per triangle, and the conflict edges keep the chosen literals consistent. For the $\varphi$ above, the graph has $9$ vertices and $15$ edges. The two directions are worked out on [polynomial-time reduction](/polynomial-time-reduction/).

### Vertex cover to Hamiltonian cycle

Garey and Johnson (Section 3.1.4) use a $12$-vertex gadget for each edge of the source graph. A Hamiltonian cycle can pass through this gadget in exactly three ways, which record whether one end, the other end or both ends of the edge are in the cover. For a cover budget $K$, there are $K$ selector vertices, and paths through the gadgets close the cycle. See [Hamiltonian cycle NP-completeness](/hamiltonian-cycle-np-completeness/).

## Variations

- **Local replacement.** Replace each piece of the source by a fixed structure, with no separate consistency gadgets. SAT to 3-SAT replaces a clause $(\ell_1 \lor \cdots \lor \ell_k)$ with $k \ge 4$ by $k - 2$ clauses of three literals and $k - 3$ new variables $z_1, z_2, \ldots$. For example, $(x_1 \lor \neg x_2 \lor x_3 \lor x_4 \lor \neg x_5)$ becomes $(x_1 \lor \neg x_2 \lor z_1) \land (\neg z_1 \lor x_3 \lor z_2) \land (\neg z_2 \lor x_4 \lor \neg x_5)$ (Garey and Johnson, Section 3.2.2).
- **Gadgets for approximation.** A gap-preserving reduction needs gadgets that keep a fraction of the satisfied constraints, not only satisfiability. Trevisan, Sorkin, Sudan and Williamson (2000) wrote the search for the best gadget as a linear program and obtained the hardness of [Max Cut](/maximum-cut/) within $16/17 + \varepsilon$ and of Max DiCut within $12/13 + \varepsilon$. See [gap-preserving reduction](/gap-preserving-reduction/).
- **Planar gadgets.** For [planar graphs](/planar-graph/), the joins of L6 may cross. A *crossover gadget* replaces each crossing by a planar piece that passes two signals through each other. This shows, for example, that 3-coloring stays NP-complete on planar graphs.
- **Gadgets from a different source.** Source problems other than 3-SAT give simpler gadgets for some targets: [3-dimensional matching](/three-dimensional-matching/) for packing and partition problems, and [vertex cover](/vertex-cover/) for Hamiltonian cycle.

## Pitfalls

- **Unplanned states.** A gadget may have good states besides "true" and "false". In the vertex cover example, a cover may take both ends of a VAR edge; only the exact count $k = n + 2m$ rules this out. Check every state, or force consistency with the budget.
- **Leakage between gadgets.** If two gadgets share a vertex that is not a join, a solution may use it to satisfy both at once. Give each CON gadget its own new vertices.
- **One direction only.** Showing that a satisfying assignment gives a target solution is the easy half. The second direction must start from an arbitrary target solution, not from one built by the first direction.
- **Non-constant gadgets.** If a gadget grows with a number in the input, as in reductions to number problems, the instance can become exponential. Encode numbers in binary and bound their length, or use a [strongly NP-hard](/strong-np-hardness/) source.
- **Literal repeated in a clause.** A clause with a repeated literal or with $x$ and $\neg x$ can break a gadget proof that assumes three distinct variables. Clean the formula first, or check that the gadget still works.

## Exercises

1. In the vertex cover reduction, show that from any vertex cover of size exactly $n + 2m$ you can read a satisfying assignment, and give the polynomial-time map.
2. Prove the OR gadget claim: in every proper 3-coloring with fixed palette colors, $r$ can be colored true if and only if $a$ or $b$ is colored true.
3. Give a gadget reduction from 3-SAT to [clique](/clique-problem/) directly, without going through independent set.
4. Show that the clause-splitting replacement for SAT to 3-SAT is not [parsimonious](/parsimonious-reduction/), and change it so that it is.

## References
