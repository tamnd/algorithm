---
tag: ZB1TBC
kind: technique
slug: symmetry-breaking
name: Symmetry breaking
aliases:
- isomorph rejection
- lex-leader constraints
- symmetry breaking constraints
- symmetry-breaking constraints
- lex-leader method
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Adds constraints or search rules that remove solutions equivalent under a symmetry, so that search explores each symmetry class once. Lex-leader constraints keep at least one solution in every class.
prereqs: [constraint-satisfaction-problem, symmetric-group, lexicographic-order]
see_also: [graph-automorphism-group, orbital-branching, symmetry-reduction, n-queens-problem, graph-coloring, global-constraint, sat, constraint-programming]
sources:
  - paper: "James M. Crawford, Matthew L. Ginsberg, Eugene M. Luks and Amitabha Roy, Symmetry-breaking predicates for search problems, Proceedings of KR-96, Morgan Kaufmann, 1996, pages 148 to 159"
    locator: the lex-leader predicate, the proof that it keeps one solution in each orbit, and the use of a subset of the group
  - paper: "Jean-François Puget, On the satisfiability of symmetrical constrained satisfaction problems, Proceedings of ISMIS-93, Lecture Notes in Computer Science 689, 1993, pages 350 to 361"
    locator: ordering constraints that remove symmetric solutions in CSPs
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 10, Symmetry in constraint programming, by Ian P. Gent, Karen E. Petrie and Jean-François Puget (lex-leader, SBDS, SBDD, value symmetry)
  - paper: "Pierre Flener, Alan M. Frisch, Brahim Hnich, Zeynep Kiziltan, Ian Miguel, Justin Pearson and Toby Walsh, Breaking row and column symmetries in matrix models, Proceedings of CP 2002, Lecture Notes in Computer Science 2470, pages 462 to 476"
    locator: double-lex constraints for matrix models with interchangeable rows and columns
  - paper: "Ian P. Gent and Barbara M. Smith, Symmetry breaking in constraint programming, Proceedings of ECAI 2000, pages 599 to 603"
    locator: symmetry breaking during search (SBDS)
  - paper: "Yat Chiu Law and Jimmy H. M. Lee, Global constraints for integer and set value precedence, Proceedings of CP 2004, Lecture Notes in Computer Science 3258, pages 362 to 376"
    locator: value precedence constraints for interchangeable values
  - paper: "Fadi A. Aloul, Arathi Ramani, Igor L. Markov and Karem A. Sakallah, Solving difficult instances of Boolean satisfiability in the presence of symmetry, IEEE Transactions on Computer-Aided Design 22(9), 2003, pages 1117 to 1137"
    locator: finding symmetries of CNF formulas by graph automorphism and adding lex-leader clauses for the generators
---

Symmetry breaking removes redundant work from search when a problem has symmetries. A *symmetry* of a [CSP](/constraint-satisfaction-problem/) is a bijection on assignments that maps solutions to solutions. Examples are swapping two interchangeable colors in [graph coloring](/graph-coloring/), or rotating the board in [n-queens](/n-queens-problem/). Solutions related by symmetries form a *symmetry class*. A search that does not know the symmetries explores every symmetric copy of every failed branch, which can multiply the work by the size of the symmetry group. Static symmetry breaking adds constraints that only some members of each class meet. The *lex-leader* method (Crawford, Ginsberg, Luks and Roy, 1996) keeps the lexicographically smallest member of each class, and so it keeps at least one solution in each class. Dynamic methods, such as SBDS and SBDD, prune symmetric branches during the search instead. In combinatorial generation the same idea is called *isomorph rejection*.

## In plain words

Many puzzles have answers that are really the same answer seen in a mirror or with names swapped. If three colors play the same role, then any coloring can be turned into five others by renaming the colors. A search that does not know this tries all six versions of every dead end.

The fix is to agree on one favourite version of each answer and accept only that one. For colors, "the first node gets color 1, and color 3 is not used before color 2" picks one version. The general rule is "of all the versions of an answer, keep the one that comes first in dictionary order". Every answer has such a first version, so nothing is lost: each family of answers keeps a member.

## When it applies

- The problem has a known or detectable group $G$ of symmetries: *variable symmetries* that permute the variables, *value symmetries* that permute the values, or symmetries that act on both.
- The goal is one solution, the proof that none exists, or one solution of each class. Symmetry breaking does not speed up a search for one solution when solutions are plentiful, but it helps a lot on unsatisfiable problems and when listing all solutions.
- The search is complete. A local search such as [min-conflicts](/min-conflicts/) gains nothing from it.

## The template

The holes are how the symmetries are found, which subset of them is broken, and how the constraints are written.

```pseudo id=main
LEX-LEADER SYMMETRY BREAKING
L1  find a group G of symmetries of the CSP, or a set of its generators   ▷ hole: by hand, or by graph automorphism
L2  fix an order x_1, ..., x_n of the variables and an order of the values
L3  choose a set S ⊆ G of symmetries to break                           ▷ hole: all of G, the generators, or a few
L4  for each g ∈ S: add the constraint (x_1, ..., x_n) ≤_lex g(x_1, ..., x_n)   ▷ hole: as LEX constraints, clauses or a propagator
L5  solve the new CSP with any complete search
L6  if all solutions are wanted, apply G to the solutions found to list the other members of their classes
```

Here $g(\sigma)$ is the image of the assignment $\sigma$ under $g$, written again as a tuple in the order $x_1, \ldots, x_n$, and $\le_{\text{lex}}$ is the [lexicographic order](/lexicographic-order/) on tuples, using the order of the values.

**Theorem (Crawford, Ginsberg, Luks and Roy, 1996).** Let $G$ be a group of symmetries of the CSP and $S \subseteq G$. Every symmetry class of solutions contains a solution that meets all the constraints of line L4. If $S = G$, it contains exactly one.

*Proof.* Let $\sigma$ be a solution. Its class is the orbit $G\sigma = \{ g(\sigma) : g \in G \}$. Every member is a solution, since every $g \in G$ maps solutions to solutions. The orbit is finite, since there are finitely many complete assignments, and $\le_{\text{lex}}$ is a total order, so the orbit has a smallest member $\tau$. For every $g \in S$, $g(\tau)$ is in the same orbit, because $G$ is a group: if $\tau = h(\sigma)$, then $g(\tau) = (g h)(\sigma)$ with $g h \in G$. So $\tau \le_{\text{lex}} g(\tau)$, and $\tau$ meets the constraint of $g$. This holds for all $g \in S$, so $\tau$ is a solution of the new CSP in the class of $\sigma$.

If $S = G$, let $\tau'$ be another member of the orbit that meets all constraints. Then $\tau' = g(\tau)$ for some $g \in G$, so $\tau = g^{-1}(\tau')$, and $g^{-1} \in G$. The constraints give $\tau \le_{\text{lex}} g(\tau) = \tau'$ and $\tau' \le_{\text{lex}} g^{-1}(\tau') = \tau$. So $\tau = \tau'$. $\square$

The proof needs one fixed order for all the constraints. Constraints from different orders can remove every member of a class, as the pitfalls show. For $S \ne G$, some classes may keep more than one member, but none loses all of them.

### A worked example

Color the path $a - b - c$ with the colors $\{1, 2, 3\}$, with $a \ne b$ and $b \ne c$. There are 12 solutions. Any permutation of the colors maps solutions to solutions, so $G$ is the [symmetric group](/symmetric-group/) on the three colors, with 6 elements. The classes are "$a = c$" (6 solutions) and "$a \ne c$" (6 solutions).

With the order $a, b, c$ and $1 < 2 < 3$, the lex-leader of a class is its smallest member: $(1, 2, 1)$ and $(1, 2, 3)$. For value symmetry, the lex-leader constraints for all of $G$ are equivalent to *value precedence*: $a = 1$, and the first use of each color comes after the first use of each smaller color. The search with these constraints tries $a = 1$ only, then $b = 2$ only, since $b = 3$ would use 3 before 2, and then $c \in \{1, 3\}$. It returns exactly the two class representatives, and applying the 6 color permutations to each gives back all 12 solutions.

A smaller example with variable symmetry: $x_1, x_2, x_3 \in \{0, 1\}$ with $x_1 + x_2 + x_3 = 1$, which is symmetric under every permutation of the variables. The generators $(x_1\ x_2)$ and $(x_2\ x_3)$ give the constraints $x_1 x_2 x_3 \le_{\text{lex}} x_2 x_1 x_3$ and $x_1 x_2 x_3 \le_{\text{lex}} x_1 x_3 x_2$, which reduce to $x_1 \le x_2$ and $x_2 \le x_3$. Of the three solutions $100$, $010$, $001$, only $001$ is left.

## Classic examples

- **Interchangeable values.** In graph coloring and bin packing, colors or bins are interchangeable. Value precedence constraints (Law and Lee, 2004) break all of this symmetry with a linear number of constraints.
- **Matrix models.** When the rows and the columns of a matrix of variables can be permuted, *double-lex* constraints order the rows and the columns lexicographically (Flener and colleagues, 2002). They are a subset of the lex-leader constraints for a row-wise order, so they keep a member of each class, but they do not break all the symmetry.
- **N-queens.** The 8 symmetries of the square map solutions to solutions. Lex-leader constraints for the 7 non-identity elements leave one solution of each class. For $n = 8$, the 92 solutions fall into 12 classes.
- **SAT.** Tools find the symmetries of a CNF formula as automorphisms of a colored graph, and add lex-leader clauses for the generators before solving (Aloul and colleagues, 2003). See [graph automorphism group](/graph-automorphism-group/).
- **Integer programming.** Orbital branching and orbitopes break symmetry in [mixed integer programs](/mixed-integer-programming/). See [orbital branching](/orbital-branching/).
- **Model checking.** [Symmetry reduction](/symmetry-reduction/) explores one state of each orbit of the state space.

## Variations

- **Static constraints.** Add the constraints before the search, as in the template. Simple, and compatible with any solver, but they may conflict with the search order.
- **Symmetry breaking during search (SBDS).** After the search backtracks from $x = v$, add for each symmetry $g$ the constraint that the symmetric image of the current partial assignment with $x = v$ is not taken (Gent and Smith, 2000). This needs a list of the symmetries.
- **Symmetry breaking by dominance detection (SBDD).** At each node, check whether the current partial assignment is symmetric to a part of the tree that was already explored, and prune if it is. This needs a test for dominance, but no list of the symmetries.
- **Generators only.** Break only the generators of $G$, or a small set of elements, since $G$ can have exponentially many elements. The theorem still guarantees a member of each class.
- **Isomorph rejection in generation.** Orderly generation and canonical augmentation list combinatorial objects once each, up to isomorphism, by testing that each new object is in a canonical form.

## Pitfalls

- **Mixing orders.** Lex-leader constraints for one variable order, together with constraints from a different order or with value precedence for a different order, can remove every member of a class, and then the solver wrongly reports "no solution".
- **Fighting the search order.** Static constraints keep the lex-smallest member. If the search heuristic would reach a different member first, the constraints can slow the search down.
- **Symmetries of the problem, not of the model.** A symmetry must map solutions of the model to solutions. A symmetry that holds only for the problem in the head of the modeller, or only for some instances, can remove solutions.
- **Counting solutions.** After breaking symmetry, the number of solutions found is the number of classes (or more, with $S \ne G$), not the number of solutions. Use orbit sizes to get the full count.
- **Too many constraints.** Adding a constraint for every element of a large group costs more than it saves. Break the generators or a small subset.

## Exercises

1. Show that the lex-leader constraint for one transposition $(x_i\ x_j)$ with $i < j$ is equivalent to $x_i \le x_j$ when the transposition is a symmetry and only these two variables are swapped.
2. In the path coloring example, list the 12 solutions and check that exactly two meet value precedence.
3. Give a CSP with symmetries $g$ and $h$ (possibly equal) where the constraint $\sigma \le_{\text{lex}} g(\sigma)$ for the order $x_1, x_2$, together with $\sigma \le_{\text{lex}} h(\sigma)$ for the order $x_2, x_1$, removes every solution.
4. Prove that double-lex constraints on an $r \times c$ matrix with interchangeable rows and columns keep at least one member of each class, by showing that they are implied by the lex-leader constraints for the row-wise order of the matrix.

## References
