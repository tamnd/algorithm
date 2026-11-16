---
tag: 2N7G4M
kind: problem
slug: shape-analysis
name: Shape analysis
aliases:
- heap shape analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Infer the shape of heap data structures a program builds, such as acyclic lists or trees, to prove memory safety and data invariants.
prereqs: [abstract-interpretation, points-to-analysis, linked-list]
see_also: [three-valued-logic-shape-analysis, bi-abduction, separation-logic, alias-analysis, may-alias-undecidability, galois-connection, widening-operator, escape-analysis]
sources:
  - paper: doi:10.1145/567752.567776
    title: Neil D. Jones and Steven S. Muchnick, Flow analysis and optimization of LISP-like structures, Proceedings of the 6th ACM Symposium on Principles of Programming Languages (POPL '79), 1979, pages 244-256
    locator: the first analysis of the shapes that unbounded structures take, with bounded descriptions of the heap
  - paper: doi:10.1145/93542.93585
    title: David R. Chase, Mark N. Wegman and F. Kenneth Zadeck, Analysis of pointers and structures, Proceedings of the ACM SIGPLAN 1990 Conference on Programming Language Design and Implementation, ACM SIGPLAN Notices 25(6), 1990, pages 296-310
    locator: storage shape graphs, one node for many cells, and counts of heap references
  - paper: doi:10.1145/237721.237724
    title: Rakesh Ghiya and Laurie J. Hendren, Is it a tree, a DAG, or a cyclic graph? A shape analysis for heap-directed pointers in C, Proceedings of the 23rd ACM Symposium on Principles of Programming Languages (POPL '96), 1996, pages 1-15
    locator: the shape (tree, DAG or cycle) of the structure reached from each pointer, for dependence testing and parallelization
  - paper: doi:10.1145/271510.271517
    title: Mooly Sagiv, Thomas Reps and Reinhard Wilhelm, Solving shape-analysis problems in languages with destructive updating, ACM Transactions on Programming Languages and Systems 20(1), 1998, pages 1-50
    locator: shape graphs with sharing information that keep lists acyclic through destructive updates such as in-place reversal
  - paper: doi:10.1145/514188.514190
    title: Mooly Sagiv, Thomas Reps and Reinhard Wilhelm, Parametric shape analysis via 3-valued logic, ACM Transactions on Programming Languages and Systems 24(3), 2002, pages 217-298
    locator: heaps as logical structures, canonical abstraction and the embedding theorem
  - paper: doi:10.1007/11691372_19
    title: Dino Distefano, Peter W. O'Hearn and Hongseok Yang, A local shape analysis based on separation logic, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2006), LNCS 3920, pages 287-302
    locator: an abstract domain of separation logic formulas with list segments, and abstraction by rewriting
  - paper: doi:10.1145/161494.161501
    title: William Landi, Undecidability of static analysis, ACM Letters on Programming Languages and Systems 1(4), 1992, pages 323-337
    locator: may alias is undecidable and must alias is not recursively enumerable, for languages with loops, dynamic storage and recursive data structures
  - paper: doi:10.1007/978-3-540-30538-5_9
    title: Josh Berdine, Cristiano Calcagno and Peter W. O'Hearn, A decidable fragment of separation logic, FSTTCS 2004, LNCS 3328, pages 97-109
    locator: entailment for the list fragment of separation logic is decidable
  - paper: doi:10.1145/378795.378851
    title: Anders Møller and Michael I. Schwartzbach, The pointer assertion logic engine, Proceedings of the ACM SIGPLAN 2001 Conference on Programming Language Design and Implementation, pages 221-231
    locator: shape properties with user loop invariants, checked in monadic second-order logic with MONA
---

Shape analysis is the problem of finding, at each point of a program, a description of the heap that is good enough to prove facts about the *form* of its linked structures: this variable points to an acyclic list, these two lists share no cell, this structure is a tree, no dereference meets `null`, and no cell becomes unreachable without being freed. It differs from [points-to analysis](/points-to-analysis/), which names each cell by the line that allocated it. That cannot tell one cell of a list from the next, so it cannot see that a list stays acyclic. Shape analysis keeps enough about reachability and sharing to see it. The exact problem is undecidable, so every method computes a sound over-approximation, in the sense of [abstract interpretation](/abstract-interpretation/). [Three-valued logic shape analysis](/three-valued-logic-shape-analysis/) and [bi-abduction](/bi-abduction/) are two methods for it.

## In plain words

A program that builds lists and trees in memory makes a picture of boxes and arrows. The picture changes as the program runs, and it can grow without limit. Shape analysis wants to say what every picture at a given line looks like, for every input, without running the program. For example: the arrows from this variable lead through some boxes and end at nothing, and never loop back. To do this, it draws a small picture that stands for all the big ones. Boxes that look alike are folded into one box that means "one or more boxes like this". The hard part is to fold enough that the picture stays small, but not so much that the analysis forgets that the list has no loop.

## Definition

**Programs and states.** A program has pointer variables and cells with a field `n` (more fields for trees). The statements are `x = null`, `x = new`, `x = y`, `x = y.n`, `x.n = y`, `x.n = null` and branches on `x == null` or `x == y`, with control flow as in a [control flow graph](/control-flow-graph/). A *state* is a pair $(E, H)$: $E$ maps each variable to a cell or `null`, and $H$ maps each allocated cell to the value of its field. Reading `y.n` when $y$ is `null` is an *error*.

**Collecting semantics.** Let $\mathrm{Init}$ be a set of start states at the entry, for example all states where $x$ points to an acyclic list. Let $F$ map a family $X = (X_p)$ of sets of states, one per program point, to $\mathrm{Init}$ at the entry joined with the successors of the states in $X$ under each statement. The *reachable states* are $R = \mathrm{lfp}\, F$, the least fixed point in the order of inclusion, where $\bot$ (the empty set) means that a point is unreachable.

**Shape properties.** A *shape property* is a set $\Phi$ of states that is closed under renaming cells: it cares how the cells are linked, not which addresses they have. Examples:

- *acyclic list from x*: following `n` from $E(x)$ reaches `null`;
- *disjoint lists*: no cell is reachable both from $x$ and from $y$;
- *tree*: no cell has two incoming fields, and no cycle;
- *no leak*: every allocated cell is reachable from some variable;
- *safe dereference at p*: $E(y) \ne$ `null` whenever the statement at $p$ reads `y.n`.

**The problem.** Given a program, $\mathrm{Init}$, and a shape property $\Phi_p$ for some points $p$, decide whether $R_p \subseteq \Phi_p$ for each of them.

**The analysis version.** Choose an abstract domain $D^\sharp$ with a concretization $\gamma$ from abstract values to sets of states. A *shape analysis* computes an abstract value $a_p$ for each point with

$$\mathrm{lfp}\, F \subseteq \gamma(\mathrm{lfp}\, F^\sharp),$$

which holds when $F \circ \gamma \subseteq \gamma \circ F^\sharp$, or with a [Galois connection](/galois-connection/) when $\alpha \circ F \sqsubseteq F^\sharp \circ \alpha$. The property is *proved* when $\gamma(a_p) \subseteq \Phi_p$. A failure to prove it is not a proof of the opposite: the analysis is sound but not complete. In the convention used here, lower abstract values mean fewer states, $\bot$ means no state and $\top$ means any state.

## Variants

- **Which properties.** Acyclicity and sharing; reachability between variables; trees and DAGs; doubly linked lists, where `prev` must be the inverse of `next`; memory safety (no null dereference, no use after free, no leak); data in the cells, such as sortedness.
- **Intraprocedural or compositional.** A whole-program analysis follows each call into the callee. A compositional one infers a summary for each procedure once, which needs a way to guess the part of the heap a call does not touch; [bi-abduction](/bi-abduction/) is that guess in [separation logic](/separation-logic/).
- **Verification or inference.** With loop invariants and specifications written by the user, checking can be done in a decidable logic, as in PALE. Without them, the analysis must infer invariants, which needs abstraction and, for loops, joins or [widening](/widening-operator/).
- **May and must.** "x may point to a cyclic structure" and "x must point to an acyclic list" are the two sides of one sound answer. Proofs of safety use the must side.
- **Concurrency.** Threads that share a heap need the shapes of both the heap and the ownership of its parts.

## Examples

**List reversal.** The loop reverses a list in place:

```
// Init: x points to an acyclic list, y and t are null
y = null
while x != null:
    t = x.n
    x.n = y
    y = x
    x = t
// Goal: y points to an acyclic list, and x is null
```

On a list of three cells $a \to b \to c \to$ `null`, the states at the loop head are:

| trip | list from x | list from y |
|---|---|---|
| 0 | $a \to b \to c \to$ `null` | `null` |
| 1 | $b \to c \to$ `null` | $a \to$ `null` |
| 2 | $c \to$ `null` | $b \to a \to$ `null` |
| 3 | `null` | $c \to b \to a \to$ `null` |

The shape property that holds at the loop head in every trip, for every list length, is: *x and y point to two acyclic lists with no common cell*. At exit $x$ is `null`, so $y$ points to an acyclic list. The dereference `x.n` is safe because the loop test says $x \ne$ `null`.

**Why points-to analysis is not enough.** If all list cells come from one allocation site $L$, a points-to analysis has one abstract cell $L$ with $L.n \to \{L, \mathrm{null}\}$ and $x, y \to \{L, \mathrm{null}\}$. This is the same answer for an acyclic list, for a cyclic list, and for two lists that share their tail. So it cannot prove the goal.

**What a shape domain keeps.** In [separation logic](/separation-logic/), the loop invariant is $\mathrm{ls}(x, \mathrm{null}) * \mathrm{ls}(y, \mathrm{null})$: two list segments ending in `null`, in disjoint parts of the heap. In three-valued logic, the cells reachable from $x$ fold into one summary node and those from $y$ into another, and a predicate records that no cell is reachable from both. Either form is a finite description of infinitely many concrete heaps, and either keeps exactly the facts that the reversal needs.

## Known algorithms

| method | describes the heap by | notes |
|---|---|---|
| Jones and Muchnick (1979) | bounded graphs, cut off at depth $k$ | the first shape analysis; $k$-limiting loses all shape beyond depth $k$ |
| storage shape graphs (Chase, Wegman and Zadeck 1990) | one node per allocation site, with counts of heap references | keeps simple lists and trees, loses them under destructive update |
| Ghiya and Hendren (1996) | path facts between pointers | classifies each structure as a tree, a DAG or a cyclic graph, for parallelizing C |
| shape graphs (Sagiv, Reps and Wilhelm 1998) | nodes named by the variables that point to them, with sharing bits | proves in-place list reversal and insertion keep a list acyclic |
| [three-valued logic shape analysis](/three-valued-logic-shape-analysis/) (1999, 2002) | logical structures with a value for "unknown", canonical abstraction | parametric in the predicates; TVLA is the tool |
| separation logic with list segments (Distefano, O'Hearn and Yang 2006) | points-to facts and list segments, joined by $*$ | abstraction by rewriting long segments into one |
| [bi-abduction](/bi-abduction/) (Calcagno, Distefano, O'Hearn and Yang 2009) | the same formulas, per procedure | compositional; the basis of Infer |
| PALE (Møller and Schwartzbach 2001) | monadic second-order logic over graph types | checks given invariants; decidable but costly |

## Bounds

- **Undecidable in general.** Landi (1992) showed that may alias is undecidable for languages with `if`, loops, dynamic storage and recursive data structures, and must alias is not even recursively enumerable. Shape properties are at least as hard: "x and y never point to the same cell at $p$" is an alias question. The reduction under Reductions gives the same result for pointer programs without integers. See also [the undecidability of may alias](/may-alias-undecidability/) and [Rice's theorem](/rice-theorem/).
- **Finite abstractions terminate.** With canonical abstraction over $k$ unary predicates, each abstract heap has at most $3^k$ nodes, one per vector of values $0$, $1$ or $\tfrac12$ of the predicates ($2^k$ when every predicate is definite), so there are finitely many abstract heaps, and the fixed point is reached. The bound on the number of abstract heaps is doubly exponential in $k$; in practice the predicates are chosen so that it is much smaller.
- **Decidable entailment for lists.** Berdine, Calcagno and O'Hearn (2004) showed that entailment between separation logic formulas built from points-to facts and list segments is decidable, which lets an analysis check that one abstract heap is covered by another.
- **Bounded heaps.** If the number of cells is bounded, the state space is finite and every property is decidable by exploring it, but the bound is a restriction on the program, not an analysis.

## Reductions

- **From halting.** A two-counter machine runs as a pointer program: counter $c_i$ is the length of a list $l_i$; increment is `t = new; t.n = li; li = t`; decrement is `li = li.n`; the zero test is `li == null`. The machine halts if and only if the program reaches its halt point. Put `z = null` and then `w = z.n` at the halt point. The program has no null dereference if and only if the machine does not halt. So the problem is undecidable even without integers.
- **To alias analysis.** A shape answer gives alias answers: two variables that point into disjoint structures do not alias. So shape analysis is at least as precise as the [alias analysis](/alias-analysis/) it implies, and costs more.
- **To logic.** Checking that an abstract heap covers another is an entailment in the logic of the domain. In separation logic it is the entailment problem; in three-valued logic it is the embedding order between structures.

## Applications

- **Memory safety.** Proving the absence of null dereferences, leaks, use after free and double free. Infer, built on bi-abduction, runs on large code bases, and SLAyer and SpaceInvader checked device drivers.
- **Parallelization and dependence testing.** If two pointers reach disjoint trees, loops over them can run in parallel; this was the aim of Ghiya and Hendren.
- **Memory management.** Knowing that a cell is unreachable after some point lets a compiler free it at compile time, or allocate it on the stack, as in [escape analysis](/escape-analysis/). This was the aim of Jones and Muchnick.
- **Verification of data structure code.** TVLA proved properties of sorting routines on lists, and that list operations keep their structure.

## References
