---
tag: K5P9JR
kind: problem
slug: difference-logic-satisfiability
name: Difference logic satisfiability
aliases:
- difference logic
- DL
- QF_IDL
- QF_RDL
area: logic-and-constraints/smt
level: advanced
summary: Decide conjunctions of constraints x - y <= c, reducible to negative-cycle detection.
prereqs: [difference-constraints, bellman-ford, negative-cycle, smt-problem]
see_also: [linear-real-arithmetic-satisfiability, simplex-for-smt, dpll-t, theory-conflict-explanation, theory-propagation, difference-bound-matrix, floyd-warshall, job-shop-scheduling]
sources:
  - paper: "Vaughan R. Pratt, Two easy theories whose combination is hard, technical report, Massachusetts Institute of Technology, 1977"
    locator: the decision procedure for separation (difference) constraints by cycles in a graph
  - paper: "Robert Nieuwenhuis and Albert Oliveras, DPLL(T) with exhaustive theory propagation and its application to difference logic, CAV 2005, Lecture Notes in Computer Science 3576"
    locator: the difference logic theory solver and its theory propagation (page numbers not checked)
  - paper: "Scott Cotton and Oded Maler, Fast and flexible difference constraint propagation for DPLL(T), SAT 2006, Lecture Notes in Computer Science 4121"
    locator: the incremental negative-cycle check after one new edge (page numbers not checked)
  - paper: "Boris V. Cherkassky and Andrew V. Goldberg, Negative-cycle detection algorithms, Mathematical Programming 85 (1999), 277 to 311"
    locator: the survey and comparison of negative-cycle detection methods
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 5, Linear Arithmetic, the section on difference logic
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 22.4, Difference constraints and shortest paths
---

Difference logic satisfiability is the problem of deciding a formula whose atoms all have the form $x - y \le c$, a bound on the difference of two variables. A conjunction of such atoms is satisfiable if and only if its constraint graph has no cycle of negative weight, so the [Bellman-Ford](/bellman-ford/) algorithm decides it in $O(n m)$ time, over the reals and over the integers alike. With Boolean structure (QF_RDL over the reals, QF_IDL over the integers) the problem is NP-complete, and SMT solvers decide it with [DPLL(T)](/dpll-t/) and a graph-based theory solver. The graph problem behind the conjunctive case is the [system of difference constraints](/difference-constraints/); this page is about the logic and its use in SMT.

## In plain words

Many rules about time have the form "this event happens at most five minutes after that one". Each rule only compares two unknowns. Draw a dot for each unknown and an arrow with a number for each rule.

The rules contradict each other exactly when you can walk around a loop of arrows and the numbers add up to less than zero. Such a loop says that some event happens before itself. If no such loop exists, the shortest walk to each dot gives a value for each unknown that obeys all the rules. A solver answers questions that join such rules with "or" by choosing rules, checking for loops, and learning from each loop it finds.

## Definition

The variables are $x_1, \ldots, x_n$, over $\mathbb{Z}$ (integer difference logic) or over $\mathbb{R}$ or $\mathbb{Q}$ (real difference logic). An *atom* is $x - y \le c$ with a constant $c$. Other forms reduce to it:

- $x - y \ge c$ is $y - x \le -c$, and $x - y = c$ is the pair $x - y \le c$, $y - x \le -c$.
- Over the integers, $x - y < c$ is $x - y \le c - 1$. Over the reals, $x - y < c$ is $x - y \le c - \delta$ with an infinitesimal $\delta > 0$, and weights are pairs $(c, k)$ compared lexicographically, as in the [general simplex](/simplex-for-smt/).
- A bound $x \le c$ uses a new variable $z$ for zero: $x - z \le c$. Each model stays a model when the same constant is added to all variables, so a model with $z \ne 0$ can be shifted to $z = 0$.

A formula is a Boolean combination of atoms. The *constraint graph* of a conjunction $\Phi$ has a vertex for each variable and an edge $y \to x$ with weight $c$ for each atom $x - y \le c$. Here $n$ is the number of variables and $m$ the number of atoms.

## Variants

- **Conjunctions.** The theory solver case. This is the [system of difference constraints](/difference-constraints/) from the shortest path literature.
- **Full QF_IDL and QF_RDL.** Boolean combinations of atoms, the SMT-LIB logics.
- **Incremental checks.** Atoms arrive one by one from a SAT solver and leave on backtracking. After one new edge $y \to x$, only cycles through that edge can be new, so the check can be local (Cotton and Maler 2006).
- **UTVPI.** Atoms $\pm x \pm y \le c$ (unit two variables per inequality). Each variable gets two vertices, $+x$ and $-x$, and the real case is again a negative-cycle test.
- **All implied bounds.** The tightest bound on each difference is the all-pairs shortest path matrix, which is the [difference bound matrix](/difference-bound-matrix/) used for the zones of [timed automata](/timed-automata/).

## Examples

The examples were checked by a script, and they are also tests of the implementation.

**Unsatisfiable.** Take the three atoms $a - b \le 1$, $b - c \le -2$ and $c - a \le 0$. The edges are $b \to a$ (weight 1), $c \to b$ (weight $-2$) and $a \to c$ (weight 0). The cycle $a \to c \to b \to a$ has weight $0 - 2 + 1 = -1$. Adding the three atoms gives $(a - b) + (b - c) + (c - a) = 0 \le -1$, which is false. The cycle is the conflict, and the clause that DPLL(T) learns is the negation of the three atoms.

**Satisfiable.** Change the third atom to $c - a \le 2$. The cycle now has weight 1. Bellman-Ford starts all distances at 0 (a virtual source with an edge of weight 0 to each vertex) and relaxes the edges in the order of the atoms:

| round | $d(a)$ | $d(b)$ | $d(c)$ | change |
|---|---|---|---|---|
| start | 0 | 0 | 0 | |
| 1 | 0 | $-2$ | 0 | edge $c \to b$: $0 - 2 < 0$ |
| 2 | $-1$ | $-2$ | 0 | edge $b \to a$: $-2 + 1 < 0$ |
| 3 | $-1$ | $-2$ | 0 | none, so stop |

The model $a = -1$, $b = -2$, $c = 0$ meets $a - b = 1 \le 1$, $b - c = -2 \le -2$ and $c - a = 1 \le 2$.

**Boolean structure.** Two jobs $J_1$ and $J_2$ of lengths 3 and 2 share one machine, with start times $s_1$ and $s_2$. "They do not overlap" is $s_1 - s_2 \le -3 \vee s_2 - s_1 \le -2$. Together with $s_1 - s_0 \ge 0$, $s_2 - s_0 \ge 0$ and the deadlines $s_1 - s_0 \le 2$, $s_2 - s_0 \le 2$, the first branch gives $s_2 \ge s_1 + 3 \ge s_0 + 3$, against $s_2 \le s_0 + 2$, and the second branch gives $s_1 \ge s_0 + 2$, which fits: $s_0 = 0$, $s_2 = 0$, $s_1 = 2$.

## Known algorithms

| method | case | worst-case time | notes |
|---|---|---|---|
| [Bellman-Ford](/bellman-ford/) with a virtual source | conjunction | $O(n m)$ | returns a model or a negative cycle |
| [Floyd-Warshall](/floyd-warshall/) | conjunction, all implied bounds | $O(n^3)$ | gives the tightest bound on each difference |
| incremental check (Cotton and Maler 2006) | one new atom | $O(m + n \log n)$ | a [Dijkstra](/dijkstra/)-like search with the current model as a potential |
| [DPLL(T)](/dpll-t/) with a graph theory solver | full QF_IDL, QF_RDL | exponential | conflicts are negative cycles; [theory propagation](/theory-propagation/) by shortest paths |
| [general simplex](/simplex-for-smt/) | any linear atoms | exponential | correct, but slower than the graph methods here |

The incremental check works because the current model $\pi$ of the old atoms is a feasible potential: the reduced weights $c + \pi(y) - \pi(x)$ of the old edges are not negative ([reduced costs](/potential-function-reduced-costs/)), so Dijkstra's algorithm can search from the head of the new edge. This is the same idea as in [Johnson's algorithm](/johnson/). Cherkassky and Goldberg (1999) compare negative-cycle detection methods; their comparison is a measured study.

## Bounds

**Theorem.** A conjunction $\Phi$ of atoms $x - y \le c$ is satisfiable over $\mathbb{R}$ if and only if its constraint graph has no cycle of negative weight. If all constants are integers and $\Phi$ is satisfiable, it has an integer model, so $\Phi$ is satisfiable over $\mathbb{Z}$ if and only if it is satisfiable over $\mathbb{R}$.

*Proof.* Suppose a model exists and the graph has a cycle $v_0 \to v_1 \to \cdots \to v_k = v_0$, where the edge $v_{i-1} \to v_i$ with weight $c_i$ comes from the atom $v_i - v_{i-1} \le c_i$. Add the $k$ atoms. The left sides telescope to $v_k - v_0 = 0$, so $0 \le \sum_i c_i$, and the cycle is not negative.

Suppose the graph has no negative cycle. Add a source $s$ with an edge $s \to v$ of weight 0 to each vertex. This adds no cycle, since no edge enters $s$. Each vertex is reachable from $s$ and no cycle is negative, so the shortest path distance $d(v)$ is a finite number, the weight of a simple path. For each edge $y \to x$ with weight $c$, a shortest path to $y$ followed by the edge is a path to $x$, so $d(x) \le d(y) + c$. Hence $x := d(x)$ meets each atom $x - y \le c$. If all weights are integers, each $d(v)$ is a sum of integers. $\square$

**Corollary.** The conjunctive case is decidable in $O(n m)$ time, over $\mathbb{Z}$ and over $\mathbb{R}$, by Bellman-Ford from the virtual source (see [negative cycle detection](/negative-cycle-detection/) for the proof that $n$ rounds find a negative cycle if one exists). The answer comes with a model or a negative cycle, and both can be checked in $O(m)$ time.

So integer difference logic avoids the hardness of [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/): each row of the constraint matrix of a difference system has one $+1$ and one $-1$, so the matrix is the transpose of the incidence matrix of a directed graph, and it is [totally unimodular](/total-unimodularity/).

**Theorem.** Satisfiability of QF_IDL and of QF_RDL formulas is NP-complete.

*Proof.* Membership: guess the truth value of each atom, check the Boolean part, and decide the chosen literals by the theorem above (a false atom $x - y \le c$ becomes $y - x < -c$). Hardness: map each propositional variable $p$ to the atom $x_p - z \le 0$, with a new variable $x_p$ for each $p$ and one shared variable $z$. Each truth assignment of the atoms has a model: $z = 0$, $x_p = 0$ if $p$ is true and $x_p = 1$ if $p$ is false. So a CNF formula is satisfiable if and only if its image is. $\square$

## Reductions

- **To shortest paths.** The conjunctive case is negative-cycle detection on the constraint graph, as proved above. The [LP formulation of shortest paths](/shortest-paths-lp-formulation/) is the dual view.
- **To LRA.** Difference logic is a fragment of [linear real arithmetic](/linear-real-arithmetic-satisfiability/), so the general simplex also decides it.
- **From SAT.** The hardness proof above maps CNF formulas to QF_IDL with one atom per variable.
- **From scheduling.** [Job shop scheduling](/job-shop-scheduling/) with a deadline maps to QF_IDL: precedences are atoms, and each pair of jobs on one machine gives a disjunction of two atoms.

## Applications

- Scheduling with precedences, time windows and resource conflicts, as in the job shop example.
- The verification of [timed automata](/timed-automata/), where clock constraints are difference constraints.
- Bounded model checking of software with array bounds and loop counters, where many constraints compare two variables.

## References
