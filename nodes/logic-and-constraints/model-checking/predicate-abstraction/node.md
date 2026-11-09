---
tag: BVH9J8
kind: technique
slug: predicate-abstraction
name: Predicate abstraction
aliases:
- Boolean abstraction
- Abstraction by predicates
area: logic-and-constraints/model-checking
level: advanced
summary: Abstract an infinite or large system to a finite Boolean one whose state records which of n chosen predicates hold; abstract transitions come from decision procedure queries.
prereqs: [abstract-interpretation, kripke-structure, sat, weakest-precondition]
see_also: [cegar, lazy-abstraction, interpolation-based-model-checking, abstract-interpretation, pushdown-system, hoare-logic, inductive-invariant, state-explosion-problem]
sources:
  - paper: doi:10.1007/3-540-63166-6_10
    title: Susanne Graf and Hassen Saïdi, Construction of abstract state graphs with PVS, CAV 1997, LNCS 1254
    locator: pages 72 to 83 (abstract states as monomials over predicates, the computation of abstract successors with the PVS theorem prover, and the abstract state graph)
  - paper: "Thomas Ball and Sriram K. Rajamani, Automatically validating temporal safety properties of interfaces, SPIN 2001, LNCS 2057"
    title: Automatically validating temporal safety properties of interfaces
    locator: the SLAM process, Boolean programs, the tools C2bp, Bebop and Newton, and the refinement loop
  - paper: "Thomas Ball, Andreas Podelski and Sriram K. Rajamani, Boolean and Cartesian abstraction for model checking C programs, TACAS 2001, LNCS 2031"
    title: Boolean and Cartesian abstraction for model checking C programs
    locator: the exact Boolean abstraction, the cheaper Cartesian abstraction, and the loss of precision between them
---

Predicate abstraction maps a system with a large or infinite state space to a finite one. One chooses predicates $p_1, \ldots, p_n$ over the concrete state, such as $x \ge 0$ or $\mathit{lock} = 1$. An abstract state is a vector $b \in \{0, 1\}^n$ that says which predicates hold, and it stands for the concrete states $\gamma(b) = \bigwedge_i (p_i \leftrightarrow b_i)$. There is an abstract transition from $b$ to $b'$ when some concrete state in $\gamma(b)$ has a successor in $\gamma(b')$; a theorem prover, an SMT solver or a SAT solver decides each such question. The result is an [existential abstraction](/cegar/) over $2^n$ abstract states, so a universal property that holds in it also holds in the concrete system. For programs, the abstraction keeps the control flow and replaces the data by Boolean variables, one per predicate: a *Boolean program*. Graf and Saïdi introduced the method in 1997, and Ball and Rajamani built the SLAM tool on Boolean programs. Predicate abstraction is the usual abstraction inside [CEGAR](/cegar/) for software, where refinement adds predicates, and [lazy abstraction](/lazy-abstraction/) uses different predicates at different program locations.

## In plain words

A program can have more states than we can ever list, because its variables hold large numbers. But often only a few facts matter for a property, such as "the lock is held" or "$x$ is positive". Predicate abstraction keeps only these facts, each as a yes or no bit, and forgets the rest.

The new system has at most $2^n$ states for $n$ facts, so a model checker can explore it completely. To build its steps, we ask a solver questions such as: if $x$ is positive now and the program adds 2 to $x$, can $x$ be negative afterwards? Whatever the solver cannot rule out becomes a possible step. So the small system can do everything the program can do, and if it is safe, the program is safe.

## When it applies

- **Software and infinite-state systems.** Integer and pointer variables make the concrete state space infinite or huge, but the property depends on a few relations between them.
- **A decision procedure exists for the predicates.** The queries are satisfiability checks of formulas in a theory such as linear arithmetic, bit-vectors or arrays.
- **Universal safety properties.** The abstraction over-approximates, so it can prove invariants and other universal properties and find candidate counterexamples, which must then be checked.
- **The right predicates can be found.** By hand, from the property and the guards of the program, or automatically by refinement from spurious counterexamples.

## The template

A concrete system has initial states $I(x)$ and transition relation $T(x, x')$. The predicates $p_1, \ldots, p_n$ are formulas over $x$. For an abstract state $b$, $\gamma(b)$ is the cube $\bigwedge_i \ell_i$ with $\ell_i = p_i$ if $b_i = 1$ and $\neg p_i$ otherwise.

```pseudo id=main
PREDICATE-ABSTRACTION(I, T, Bad, P)
L1  loop
L2      Î ← { b ∈ {0,1}^n : SAT(I(x) ∧ γ(b)(x)) }
L3      for each abstract state b reached so far, and each b' ∈ {0,1}^n do        ▷ the abstract post: up to 2^n queries per b
L4          if SAT(γ(b)(x) ∧ T(x, x') ∧ γ(b')(x')) then add the abstract edge b → b'
L5      if no abstract path leads from Î to a state b with SAT(γ(b) ∧ Bad) then return HOLDS
L6      take a shortest such abstract path; check it on the concrete system with one formula
L7      if it is feasible then return FAILS, with the concrete path
L8      P ← P ∪ new predicates that rule the path out                              ▷ for example weakest preconditions or interpolants
```

**Why it is sound.** Each concrete state $x$ lies in exactly one cell $\gamma(b)$. A concrete path $x_0, x_1, \ldots$ maps to the abstract path $b_0, b_1, \ldots$ of the cells, because each step is witnessed by the query of line L4. So if no abstract path reaches a cell that meets $\mathit{Bad}$, no concrete path reaches $\mathit{Bad}$.

**The cost of $2^n$ cubes.** Line L4 asks one question for each pair of cubes, so the exact abstract post of one abstract state can take $2^n$ queries, and the whole abstraction $4^n$. With $n$ in the tens this is already too much. Tools reduce the cost in several ways: they compute the post of a set of states as one formula and enumerate only its satisfying cubes, they use BDDs or all-solutions SAT and SMT to enumerate the cubes symbolically, or they give up precision. The *Cartesian abstraction* of Ball, Podelski and Rajamani asks, for each predicate separately, whether it must be true or must be false after the step. That is at most $2n$ queries, but the result is the smallest cube that contains the exact post, which can lose correlations between predicates.

**Boolean programs.** For a program, the predicates are attached to the program, and each statement becomes a parallel assignment to Boolean variables with nondeterministic choice where the solver cannot decide. Procedures stay procedures, so the abstraction is a recursive Boolean program, which is a [pushdown system](/pushdown-system/) and can be checked exactly. Ball and Rajamani's SLAM translated C to Boolean programs with C2bp, checked them with Bebop, and found new predicates with Newton.

## Classic examples

Take the program

```text
L0: x := 0
L1: while (*) x := x + 2
L2: assert x != 1
```

The concrete state space is infinite. With the single predicate $p_1 = (x \ge 0)$, the abstract state at L2 is $\{p_1\}$, which contains $x = 1$, so the abstract assert can fail. The shortest abstract path goes from L0 straight to L2. On the concrete program it gives $x = 0$, so it is spurious. The [weakest precondition](/weakest-precondition/) of the failure at L2 is $x = 1$, which becomes the predicate $p_2$. Now the four cubes over $p_1, p_2$ are checked at each location. After $x := 0$ only $p_1 \wedge \neg p_2$ is possible. The loop body from $p_1 \wedge \neg p_2$ gives $x + 2 \ge 2$, so again only $p_1 \wedge \neg p_2$. The abstract state at L2 is $p_1 \wedge \neg p_2$, and the assert holds. The invariant $x \ge 0 \wedge x \ne 1$ at L1 is the proof.

Without $p_1$ the refinement fails: from $\neg(x = 1)$ the loop can reach $x = 1$ from $x = -1$, so the next refinement adds $x = -1$, then $x = -3$, and so on forever. This shows that the result depends on which predicates the refinement finds.

Other classic uses:

- **Device drivers.** SLAM checked Windows device drivers for API usage rules, for example that a lock is acquired and released in alternation. It became the Static Driver Verifier.
- **Protocols with parameters.** Graf and Saïdi applied the method to protocols with unbounded data, with predicates chosen by hand and abstract successors computed by the PVS prover.
- **Hardware.** Predicate abstraction over word-level predicates, with SAT-based abstract post, abstracts large data paths in hardware verification.

## Variations

- **Lazy abstraction.** Predicates are local to program locations, and only the part of the reachability tree affected by a refinement is rebuilt; see [lazy abstraction](/lazy-abstraction/).
- **Interpolation for new predicates.** Craig interpolants of a spurious path formula give predicates that are often fewer and more local than weakest preconditions; see [interpolation-based model checking](/interpolation-based-model-checking/).
- **Predicate abstraction as abstract interpretation.** The lattice of sets of cubes is an abstract domain, and the exact abstract post is the best abstract transformer; see [abstract interpretation](/abstract-interpretation/).
- **Indexed predicates and quantified invariants.** For parameterized systems and arrays, predicates with free index variables give quantified invariants.

## Pitfalls

- **Exponential abstract post.** Computing the exact abstraction with one query per cube does not scale beyond a few predicates. Use symbolic enumeration or a cheaper abstraction.
- **Global predicates.** Adding every new predicate at every location multiplies the work at locations where it is irrelevant.
- **Divergent refinement.** As in the example, refinement can add infinitely many predicates. Heuristics, such as interpolants that generalize or templates such as $x \ge 0$, are needed for termination in practice.
- **Imprecise decision procedures.** If the solver answers "unknown" and the tool treats it as "unsatisfiable", an abstract edge is lost, and HOLDS becomes unsound. Unknown must count as satisfiable.
- **Existential properties.** An existential abstraction cannot prove a property such as "some path reaches the goal".

## Exercises

1. For two predicates $x > 0$ and $y > 0$ and the statement $x := x + y$, compute the exact abstract post of the cube $x > 0 \wedge y > 0$, and the Cartesian abstraction. *Answer:* both give $x > 0 \wedge y > 0$.
2. Find a statement and two predicates where the Cartesian abstraction is strictly less precise than the exact one. *Hint:* the statement $x := y; y := x_{\mathrm{old}}$ that swaps $x$ and $y$, with the predicates $x > 0$ and $y > 0$, from the set $\{x > 0 \wedge \neg (y > 0), \neg (x > 0) \wedge y > 0\}$.
3. Show that if the predicates include an inductive invariant that excludes the bad states, the abstraction proves the property.
4. How many queries does the exact abstract post need in the worst case for $n$ predicates, and how many does the Cartesian abstraction need?

## References
