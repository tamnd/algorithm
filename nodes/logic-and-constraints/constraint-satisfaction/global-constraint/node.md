---
tag: 87YJB4
kind: concept
slug: global-constraint
name: Global constraint
aliases:
- global constraints catalogue
- global constraint catalog
- n-ary constraint with a dedicated propagator
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: A constraint over any number of variables, such as all-different or cumulative, with its own propagator. The propagator removes values that its decomposition into small constraints keeps.
prereqs: [constraint-satisfaction-problem, arc-consistency, constraint-propagation]
see_also: [all-different-constraint, regin-all-different-filtering, bounds-consistency, constraint-programming, deterministic-finite-automaton, resource-constrained-project-scheduling, bipartite-matching, ford-fulkerson]
sources:
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 6, Global constraints, by Willem-Jan van Hoeve and Irit Katriel (definitions, decompositions, and filtering for all-different, cardinality, sequence, regular and scheduling constraints)
  - paper: "Nicolas Beldiceanu, Mats Carlsson and Jean-Xavier Rampon, Global constraint catalog, SICS Technical Report T2005:08, Swedish Institute of Computer Science, 2005, with later revised editions"
    locator: the catalogue of several hundred global constraints, each with its meaning, graph description and known filtering algorithms
  - paper: "Jean-Charles Régin, A filtering algorithm for constraints of difference in CSPs, Proceedings of the 12th National Conference on Artificial Intelligence (AAAI-94), 1994, pages 362 to 367"
    locator: generalized arc consistency for all-different by matching, and the example where the clique of binary constraints prunes less
  - paper: "Gilles Pesant, A regular language membership constraint for finite sequences of variables, Proceedings of CP 2004, Lecture Notes in Computer Science 3258, pages 482 to 495"
    locator: the regular constraint and its filtering on a layered graph of automaton states
  - paper: "Abderrahmane Aggoun and Nicolas Beldiceanu, Extending CHIP in order to solve complex scheduling and placement problems, Mathematical and Computer Modelling 17(7), 1993, pages 57 to 73"
    locator: the cumulative constraint and its use in CHIP
  - paper: "Christian Bessière and Pascal Van Hentenryck, To be or not to be ... a global constraint, Proceedings of CP 2003, Lecture Notes in Computer Science 2833, pages 789 to 794"
    locator: semantic, operational and algorithmic notions of when a constraint is global
---

A global constraint is a constraint that relates any number of variables, together with a filtering algorithm made for it. The standard example is [all-different](/all-different-constraint/)$(x_1, \ldots, x_n)$. The same relation can be written as $\binom{n}{2}$ constraints $x_i \neq x_j$, but [arc consistency](/arc-consistency/) on those small constraints sees each pair alone and misses facts that hold for the group. [Régin's algorithm](/regin-all-different-filtering/) looks at all the variables at once through a matching and removes every value that no solution of the whole constraint uses. Global constraints are the main way in which [constraint programming](/constraint-programming/) solvers bring algorithms from graph theory, flows, automata and scheduling into a general search. The *Global Constraint Catalog* of Beldiceanu, Carlsson and Rampon lists several hundred of them.

## In plain words

Some rules talk about a whole group of variables: "these nine cells hold different digits", "these tasks never use more than three machines at once", "this sequence of shifts follows the work rules". You can split such a rule into many small rules about two variables each, but then each small rule only sees its own pair.

A global constraint keeps the rule whole and gives it its own algorithm. The algorithm can see, for example, that three cells share only two possible digits, so the rule cannot hold. The small rules cannot see this. So the solver removes more wrong values early and searches less.

## The idea

**Definition.** A global constraint is a family of constraints $C(x_1, \ldots, x_n)$, one for each arity $n$, often with extra parameters, such as a table, an automaton or a capacity. A solver gives it a *propagator*: a procedure that takes the current domains and removes values, and that is

- *correct*: it never removes a value that some solution of $C$ within the current domains uses,
- *checking*: when all the variables are fixed, it fails exactly when $C$ is violated.

The strongest propagator enforces *generalized arc consistency* (GAC): every value left in a domain is part of a tuple of $C$ whose values are all in the current domains. Weaker propagators enforce [bounds consistency](/bounds-consistency/) or a problem-specific rule.

**Why it prunes more than a decomposition.** Let $C$ be equivalent to a conjunction of constraints $C_1, \ldots, C_m$ on the same variables, with no new variables. GAC on $C$ always removes at least as much as arc consistency on all the $C_i$:

1. Take domains on which $C$ is GAC, and a value $a$ of $x$. There is a tuple $\tau$ of $C$ with $\tau(x) = a$ and every value in the current domains.
2. Since $\tau$ satisfies $C$, it satisfies each $C_i$, so its restriction to the scope of $C_i$ supports $a$ in $C_i$.
3. So these domains are arc consistent for every $C_i$. Arc consistency keeps the largest arc consistent domains inside the start domains, so its result contains the GAC result.

The inclusion is often strict. With $x_1, x_2 \in \{1, 2\}$ and $x_3 \in \{1, 2, 3\}$, each of the three constraints $x_i \neq x_j$ is arc consistent and nothing is removed. All-different needs three different values, and $x_1, x_2$ use both 1 and 2, so GAC removes 1 and 2 from $x_3$. With $x_3 \in \{1, 2\}$ as well, the decomposition still removes nothing, while GAC finds that there is no solution. The reason is [Hall's theorem](/hall-theorem/): a set of $k$ variables whose domains together have fewer than $k$ values cannot all differ.

Some decompositions do reach GAC. If new variables are allowed and the decomposition is *Berge-acyclic* (its hypergraph has no cycles), arc consistency on it equals GAC on the whole. The regular constraint, written as a chain of transition constraints $q_{i+1} = \delta(q_i, x_i)$ with state variables $q_i$, is the main example.

**The cost of GAC.** For some constraints GAC is cheap. For others it is NP-hard, for example for cumulative, where even deciding whether the constraint has a solution is NP-complete. Solvers then use weaker rules that run in polynomial time.

**Common global constraints.**

| constraint | meaning | filtering method | GAC in polynomial time |
|---|---|---|---|
| all-different$(x_1, \ldots, x_n)$ | the values differ | [bipartite matching](/bipartite-matching/) and strongly connected components (Régin 1994) | yes |
| gcc$(x, \ell, u)$, global cardinality | value $v$ is used between $\ell_v$ and $u_v$ times | flows (Régin 1996) | yes |
| element$(i, A, x)$ | $x = A[i]$ | direct support check | yes |
| table$(x, T)$ | the tuple of $x$ is a row of the table $T$ | GAC-schema, simple tabular reduction, compact table | yes, in the size of $T$ |
| regular$(x, M)$ | the word $x_1 \cdots x_n$ is accepted by the [automaton](/deterministic-finite-automaton/) $M$ | forward and backward passes over a layered graph of states (Pesant 2004) | yes |
| sum or linear $\sum a_i x_i \le b$ | a linear inequality | bounds reasoning | bounds only; GAC on an equality is NP-hard in general |
| cumulative$(s, d, r, c)$ | tasks with starts $s$, durations $d$ and demands $r$ never use more than $c$ at a time | time-tabling, edge finding, energy reasoning | no, unless P = NP |
| circuit$(x_1, \ldots, x_n)$ | the successor variables form one Hamiltonian cycle | all-different plus removal of short cycles | no, unless P = NP |

## Examples

**All-different in Sudoku.** Each row, column and box of a [Sudoku](/sudoku/) is one all-different constraint on nine cells. If two cells of a row can only hold $\{4, 7\}$, Régin's filter removes 4 and 7 from the other seven cells of the row. Puzzle solvers call this a "naked pair". The 14 binary constraints between those two cells and the other seven do not find it, since each of them still has a support.

**Element.** Let $A = [3, 5, 3, 7]$, $i \in \{1, 2, 3, 4\}$ and $x \in \{3, 4, 5\}$. GAC keeps $i = 1, 2, 3$, since $A[1] = 3$, $A[2] = 5$ and $A[3] = 3$ are in the domain of $x$, and it removes $i = 4$, since $A[4] = 7$ is not. It removes $x = 4$, since no entry of $A$ is 4. The result is $i \in \{1, 2, 3\}$ and $x \in \{3, 5\}$. Element is how a model uses a variable as an index, for example to look up the cost of the job that a variable chooses.

**Cumulative with capacity 1.** Task A has start $s_A \in [0, 1]$ and duration 3, and task B has start $s_B \in [0, 5]$ and duration 2. Whatever its start, A runs during $[1, 3)$, its *compulsory part*. Every start of B in $\{0, 1, 2\}$ overlaps this part, so time-tabling raises the earliest start of B to 3. The result is $s_A \in [0, 1]$ and $s_B \in [3, 5]$.

## Where it is used

- In every CP solver, such as Gecode, Choco, OR-Tools CP-SAT and the solvers behind MiniZinc, which offer dozens of global constraints and translate others into them.
- In scheduling: cumulative, disjunctive and their filters are the core of CP for [job shop](/job-shop-scheduling/) and [resource-constrained project scheduling](/resource-constrained-project-scheduling/).
- In rostering and sequencing, where regular and sequence constraints state the work rules.
- In modelling languages, where a global constraint is both a short way to say a common structure and a hint that lets each solver choose its best method, or a decomposition when it has none.

## References
