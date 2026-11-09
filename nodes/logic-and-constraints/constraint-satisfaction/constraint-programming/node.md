---
tag: VNC66K
kind: concept
slug: constraint-programming
name: Constraint programming
aliases:
- CP
- constraint logic programming
- CLP
- CLP(FD)
area: logic-and-constraints/constraint-satisfaction
level: intro
summary: A way to solve combinatorial problems in which the user states variables, domains and constraints, and a solver finds solutions by constraint propagation combined with search.
prereqs: [constraint-satisfaction-problem]
see_also: [global-constraint, constraint-propagation, maintaining-arc-consistency, minimum-remaining-values, logic-programming, mixed-integer-programming, sat, depth-first-branch-and-bound]
sources:
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 1, Introduction (the parts of a CP system and its history), and Chapter 12, Constraint logic programming, by Kim Marriott, Peter J. Stuckey and Mark Wallace
  - paper: doi:10.1145/41625.41635
    title: Joxan Jaffar and Jean-Louis Lassez, Constraint logic programming, Proceedings of the 14th ACM Symposium on Principles of Programming Languages (POPL), 1987
    locator: pages 111 to 119 (the CLP(X) scheme, which puts constraint solving over a domain X in the place of unification)
  - book: isbn:9780262081818
    title: Pascal Van Hentenryck, Constraint Satisfaction in Logic Programming, MIT Press, 1989
    locator: the finite domain part of CHIP, look-ahead and forward checking inside Prolog
  - book: isbn:9780262133418
    title: Kim Marriott and Peter J. Stuckey, Programming with Constraints, An Introduction, MIT Press, 1998
    locator: Chapters 3 and 4 (finite domain solving by propagation, and constraint logic programs)
  - paper: "Nicholas Nethercote, Peter J. Stuckey, Ralph Becket, Sebastian Brand, Gregory J. Duck and Guido Tack, MiniZinc, towards a standard CP modelling language, Proceedings of CP 2007, Lecture Notes in Computer Science 4741, pages 529 to 543"
    locator: the MiniZinc language and its translation to FlatZinc for different solvers
  - paper: "Eugene C. Freuder, In pursuit of the holy grail, Constraints 2(1), 1997, pages 57 to 61"
    locator: the view of CP as a way for the user to state a problem and the computer to solve it
---

Constraint programming (CP) is a way to solve combinatorial search and optimization problems. The user writes a *model*: variables, a finite domain for each, the [constraints](/constraint-satisfaction-problem/) that a solution must meet, and possibly an objective. A solver then finds a solution, all solutions, or an optimal one. It alternates two steps: [constraint propagation](/constraint-propagation/), which removes values that cannot be part of any solution, and search, which makes a choice when propagation can do no more and undoes it on failure. The model says *what* a solution is, and the solver decides *how* to find it, in the spirit that Freuder (1997) called the "holy grail" of programming. CP grew out of logic programming as *constraint logic programming* (CLP), and today it is mostly used through modelling languages and libraries.

## In plain words

You describe the puzzle, not the way to solve it. You say which unknowns there are, which values each may take, and which rules must hold. The solver does the rest.

The solver works like a careful person with a pencil. First it crosses out every value that clearly breaks a rule, and each cross can lead to more crosses. When nothing more can be crossed out, it guesses one value and goes on. If a guess leads to a contradiction, it rubs out everything since the guess and tries another value. Good crossing out makes the number of guesses small.

## The idea

**The model.** A CP model is a [constraint satisfaction problem](/constraint-satisfaction-problem/) $(X, D, C)$, often with an objective $f$ to minimize. Constraints are written at a high level: linear and nonlinear arithmetic, logical combinations, and [global constraints](/global-constraint/) such as all-different, element and cumulative. A good model uses global constraints for the main structure, adds *redundant* constraints that are implied but help propagation, and breaks symmetries (see [symmetry breaking](/symmetry-breaking/)).

**Propagation.** Each constraint has a *propagator*, an algorithm that removes values from the domains of its variables. A propagation engine keeps a queue of propagators whose variables have changed, and runs them until no domain changes, a *fixpoint*, or until a domain is empty, a *failure*. The strength of each propagator is a choice: [arc consistency](/arc-consistency/), [bounds consistency](/bounds-consistency/), or a cheaper rule. Since each propagator only removes values and the domains are finite, the loop always ends.

**Search.** At a fixpoint where some variable is not yet fixed, the solver *branches*. The usual branching chooses a variable, for example by [minimum remaining values](/minimum-remaining-values/) or dom/wdeg, and a value, for example the smallest or the [least constraining](/least-constraining-value/) one, and tries $x = a$ and then $x \neq a$. The search is depth first, and each branch runs propagation again. This is [maintaining arc consistency](/maintaining-arc-consistency/) in its general form. For optimization, the solver uses [depth-first branch and bound](/depth-first-branch-and-bound/): after each solution with cost $z$, it adds the constraint $f < z$, which propagates like any other. Modern solvers add restarts, [nogood learning](/nogood-learning/), and large neighbourhood search.

**Constraint logic programming.** Jaffar and Lassez (1987) defined the CLP($\mathcal{X}$) scheme: a [logic program](/logic-programming/) in which unification over terms is replaced, or extended, by solving constraints over a domain $\mathcal{X}$. Examples are CLP($\mathbb{R}$) for real linear arithmetic, CLP(FD) for finite domains, and CLP($\mathcal{B}$) for Booleans. The program builds a store of constraints as it runs, and a branch fails as soon as the store is shown to be unsatisfiable. Prolog's backtracking provides the search. CHIP, from the European Computer-Industry Research Centre, added finite domain propagation to Prolog in the late 1980s (Van Hentenryck, 1989).

**From languages to libraries.** In the 1990s CP moved into libraries for general languages, such as ILOG Solver in C++, and later Gecode, Choco and OR-Tools. Modelling languages such as OPL and MiniZinc (Nethercote and colleagues, 2007) let one model run on many solvers: MiniZinc translates a model into FlatZinc, a flat list of constraints that each solver supports or decomposes.

**Relation to other methods.** CP, [mixed integer programming](/mixed-integer-programming/) and [SAT](/sat/) solve the same kinds of problems. MIP is strongest when a linear relaxation gives a good bound. SAT is strongest when the problem is Boolean and learning pays off. CP is strongest when the problem has a rich combinatorial structure that a global constraint captures, as in scheduling and sequencing. Lazy clause generation joins CP propagation with SAT learning, and solvers such as CP-SAT combine all three.

## Examples

**SEND + MORE = MONEY.** Give each letter a different digit so that the sum is right, with $S \neq 0$ and $M \neq 0$. A CP model has eight variables with domains $\{0, \ldots, 9\}$, one all-different constraint, and one linear equation:

$$1000 S + 91 E - 90 N + D - 9000 M - 900 O + 10 R - Y = 0 .$$

Bounds reasoning on the equation and removal of fixed values for all-different, run to a fixpoint before any choice, gives the domains below. This was computed for this page.

| variable | $S$ | $E$ | $N$ | $D$ | $M$ | $O$ | $R$ | $Y$ |
|---|---|---|---|---|---|---|---|---|
| domain | $\{9\}$ | $4..7$ | $5..8$ | $2..8$ | $\{1\}$ | $\{0\}$ | $2..8$ | $2..8$ |

Propagation alone fixes $S = 9$, $M = 1$ and $O = 0$. The search then picks $E$, which has the smallest domain. With $E = 4$, propagation finds a failure. With $E = 5$, propagation fixes every other letter, which gives $9567 + 1085 = 10652$, the only solution. The whole search makes two choices.

**A scheduling model.** For a [job shop](/job-shop-scheduling/), the variables are the start times, the precedences inside each job are linear constraints, each machine has one disjunctive (or cumulative) global constraint, and the objective is the makespan. Edge finding in the machine constraints and branch and bound on the makespan do most of the work.

## Where it is used

- Scheduling and timetabling: production and project scheduling, sports schedules, school and university timetables, and crew rostering.
- Routing and logistics with complex side constraints, often through large neighbourhood search.
- Configuration of products and verification of hardware and software, where the constraints describe what is allowed.
- Puzzles and combinatorial design, such as [Sudoku](/sudoku/), Latin squares and Golomb rulers, which are the standard teaching examples.
- As a part of hybrid solvers that combine CP with MIP and SAT, such as OR-Tools CP-SAT.

## References
