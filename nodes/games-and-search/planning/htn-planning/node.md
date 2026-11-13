---
tag: 1801NR
kind: problem
slug: htn-planning
name: HTN planning
aliases:
- hierarchical task network planning
area: games-and-search/planning
level: core
summary: Given HTN methods, an initial state and an initial task network, decide whether decomposition yields an executable primitive plan. It is undecidable in general and has tight bounds by restriction.
prereqs: [hierarchical-task-network]
see_also: [htn-decomposition, task-network, classical-planning, strips-plan-existence-pspace-complete, context-free-grammar, post-correspondence-problem, undecidability, plan-recognition]
sources:
  - paper: "Kutluhan Erol, James Hendler and Dana Nau, HTN planning: complexity and expressivity, Proceedings of AAAI-94"
    locator: pp. 1123 to 1128 (plan existence, undecidability by the intersection of context-free languages, and the decidable restrictions)
  - paper: doi:10.1007/BF02136175
    title: "Kutluhan Erol, James Hendler and Dana Nau, Complexity results for HTN planning, Annals of Mathematics and Artificial Intelligence 18(1) (1996)"
    locator: pp. 69 to 93 (the complexity of plan existence by ordering, recursion and variables)
  - paper: doi:10.1609/icaps.v25i1.13721
    title: "Ron Alford, Pascal Bercher and David W. Aha, Tight bounds for HTN planning, Proceedings of ICAPS 2015"
    locator: pp. 7 to 15 (completeness results for acyclic, regular, tail-recursive and arbitrary domains, ground and lifted, total and partial order)
  - paper: "Ron Alford, Pascal Bercher and David W. Aha, Tight bounds for HTN planning with task insertion, Proceedings of IJCAI 2015"
    locator: pp. 1502 to 1508 (Table 2, the bounds with and without task insertion side by side)
  - paper: "Daniel Höller, Gregor Behnke, Pascal Bercher and Susanne Biundo, Language classification of hierarchical planning problems, Proceedings of ECAI 2014, IOS Press"
    locator: pp. 447 to 452 (the solution sets of HTN problems as formal languages)
  - paper: doi:10.1613/jair.1141
    title: "Dana Nau, Tsz-Chiu Au, Okhtay Ilghami, Ugur Kuter, J. William Murdock, Dan Wu and Fusun Yaman, SHOP2: an HTN planning system, Journal of Artificial Intelligence Research 20 (2003)"
    locator: pp. 379 to 404 (a forward decomposition planner for the problem)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 11 (HTN planning problems, solutions, and the planners for them)
---

HTN planning is the planning problem of the [hierarchical task network](/hierarchical-task-network/) model. The input is a set of primitive tasks, which are [STRIPS](/strips/) operators, a set of compound tasks, a set of methods that decompose compound tasks into [task networks](/task-network/), an initial state and an initial task network. The question is whether the initial network can be decomposed, by methods, into a primitive network that has an executable linearization. Unlike [classical planning](/classical-planning/), the problem asks for a plan of a given shape, not for any plan that reaches a goal. This changes its complexity a lot. With partially ordered networks and recursive methods, plan existence is undecidable. Under restrictions on the ordering, on recursion and on variables, Alford, Bercher and Aha gave a tight bound for each case. This page is about the question; the planners for it are listed under Known algorithms.

## In plain words

You are given a to-do list and a recipe book. Some items on the list are simple actions that you can do at once if the situation allows. Others are big jobs, and the recipe book lists one or more ways to break each big job into smaller items, some of them big jobs again.

Some items on the list must come before others, and some may be done in any order.

The question is whether you can keep breaking jobs down until only simple actions are left, and then do all of them in some allowed order, each one possible when its turn comes.

You may not add an action that no recipe asked for, even if it would help. The answer is a plan that follows the recipes, not just any plan that gets the job done.

## Definition

**Input.** An HTN problem $\Pi = (F, O, C, M, s_0, w_0)$:

- a finite set $F$ of facts and an initial state $s_0 \subseteq F$;
- a finite set $O$ of primitive tasks, each a STRIPS operator with precondition, add list and delete list in $F$;
- a finite set $C$ of compound tasks, disjoint from $O$;
- a finite set $M$ of methods $\mu = (c, \mathit{pre}, w)$, with $c \in C$, a precondition $\mathit{pre} \subseteq F$, and a task network $w$ over $O \cup C$;
- an initial task network $w_0$ over $O \cup C$.

**Decomposition.** For a node $u$ of a network $w$ that is labelled with $c$, and a method $(c, \mathit{pre}, w')$, the network $w[u / w']$ replaces $u$ by a fresh copy of $w'$, whose nodes inherit the orderings of $u$; the exact rule is on the [task network](/task-network/) page. Write $w \to^* w''$ if $w''$ arises from $w$ by finitely many decompositions.

**Solution.** A sequence $\pi = o_1, \ldots, o_k$ of operators is a solution of $\Pi$ if there is a primitive network $w''$ with $w_0 \to^* w''$ and a linearization of $w''$ with task sequence $\pi$ such that

- each $o_i$ is applicable in the state $s_{i-1}$ reached by $o_1, \ldots, o_{i-1}$ from $s_0$, and
- each method used holds its precondition in the state just before the first operator that it produced, directly or indirectly.

The second clause is the forward reading used by SHOP-style planners. The formalization behind the tight bounds has no method preconditions; a precondition becomes a primitive task with that precondition and no effects, placed before all other subtasks of the method.

**The questions.**

- **Plan existence.** Does $\Pi$ have a solution? This is the decision problem of the bounds below.
- **Plan generation.** Output a solution, or report that none exists.
- **Optimal planning.** Output a solution of least length, or of least total cost when operators have costs.

The problem has no goal formula. A goal can be added as a primitive task with the goal as its precondition, ordered after all other nodes of $w_0$.

## Variants

The complexity depends on four features of the input.

- **Ordering.** *Totally ordered*: $w_0$ and all method networks are totally ordered, so every network that arises is a sequence. *Partially ordered*: any strict partial order is allowed.
- **Recursion.** Draw a graph on tasks with an edge from $c$ to every task in a method network of $c$. *Acyclic*: this graph has no cycle, so every decomposition ends after at most $|C|$ levels. *Regular*: every method network contains at most one compound task, and it comes after all other tasks of that network. *Tail-recursive*: roughly, only the last task of a method network may lead back, through decomposition, to the task of the method. *Arbitrary*: no restriction.
- **Variables.** *Ground*: tasks and methods are propositional, as above. *Lifted*: tasks have arguments, methods are schemas with variables, and grounding them can make the problem exponentially larger.
- **Task insertion.** In HTN planning with task insertion, a solution may also contain operators that no method produced, inserted anywhere. The hierarchy then only says what must be done, not what may not be done.

Further variants add the state constraints of Erol, Hendler and Nau to networks, or ask for plan verification: given $\Pi$ and a sequence $\pi$, is $\pi$ a solution?

## Examples

**The travel problem.** The initial state is $\{\mathit{at\text{-}home}, \mathit{have\text{-}cash}\}$ and $w_0$ is the single task $\mathit{travel}$. Its methods are *by-foot* (precondition park-is-near, subtask walk), *by-bus* (subtasks go-to-stop, buy-ticket, ride-bus) and *by-taxi* (precondition have-cash, subtasks call-taxi, ride-taxi, pay-driver), with the operators of the [HTN decomposition](/htn-decomposition/) page. The bus plan fails, since buying a ticket needs a coin, and the only solution is call-taxi, ride-taxi, pay-driver. A classical planner with the same operators and the goal at-park might return any plan that reaches the park; here the methods are the only allowed shapes.

**A non-regular solution set.** Primitive tasks $a$ and $b$ need and change nothing. The compound task $S$ has the methods $S \to a, S, b$ and $S \to a, b$, both totally ordered, and $w_0 = \{S\}$. The solutions are exactly $a^n b^n$ for $n \ge 1$. So $a a a b b b$ is a solution and $a a b$ is not, and no STRIPS problem over the actions $a$ and $b$ has exactly these plans, as shown on the [hierarchical task network](/hierarchical-task-network/) page.

**The hierarchy forbids a plan.** A package must go from city $x$ to city $y$. The operators are $\mathit{load\text{-}truck}$, $\mathit{drive}$, $\mathit{unload\text{-}truck}$ and a direct $\mathit{fly}$, and $w_0$ is the task $\mathit{deliver}$ with a single method $\mathit{deliver} \to \mathit{load\text{-}truck}, \mathit{drive}, \mathit{unload\text{-}truck}$. The one-step plan $\mathit{fly}$ reaches the same final state, but it is not a solution, because no decomposition of $w_0$ produces it. With task insertion, the solutions still must contain the three truck operators.

**No solution, although the tasks look easy.** Let $w_0$ contain two unordered primitive tasks, $o_1$ with precondition $p$ and delete list $\{p\}$, and $o_2$ with precondition $p$. From $s_0 = \{p\}$, the order $o_2, o_1$ works and $o_1, o_2$ does not, so the problem has a solution. If $w_0$ orders $o_1 \prec o_2$, it has none.

## Known algorithms

- **Forward decomposition.** [HTN decomposition](/htn-decomposition/) in the style of SHOP and SHOP2 decomposes tasks in the order in which they will be executed, so it always knows the current state. It is sound, and complete for solutions up to a bound on the depth of decomposition; without a bound it can run forever on recursive domains, as it must, since the problem is undecidable.
- **Plan-space decomposition.** UMCP, and the older planners NOAH, NONLIN, SIPE and O-Plan, refine a partially ordered network with methods and repair the interactions between tasks with critics or with the flaws of [plan-space planning](/plan-space-planning/).
- **Hybrid planning.** Planners that combine methods with causal links and threats solve a variant in which the plan may also contain inserted steps.
- **Compilation.** For the bounded or tail-recursive cases, an HTN problem can be compiled into a classical planning task or a propositional formula, and solved with a classical planner or a SAT solver; the bounds below say how large such a translation must be.

## Bounds

The following table gives the class in which plan existence is complete, for each combination of the variants, as listed in Table 2 of Alford, Bercher and Aha (IJCAI 2015), which collects the results of their ICAPS 2015 paper.

| variables | ordering | acyclic | regular | tail-recursive | arbitrary |
|---|---|---|---|---|---|
| ground | total | PSPACE | PSPACE | PSPACE | EXPTIME |
| ground | partial | NEXPTIME | PSPACE | EXPSPACE | undecidable |
| lifted | total | EXPSPACE | EXPSPACE | EXPSPACE | 2-EXPTIME |
| lifted | partial | 2-NEXPTIME | EXPSPACE | 2-EXPSPACE | undecidable |

Some consequences:

- The undecidable case, partially ordered with arbitrary recursion, was shown by Erol, Hendler and Nau; it stays undecidable without variables.
- Ground totally ordered planning with arbitrary recursion is EXPTIME-complete, so it is harder than [STRIPS plan existence](/strips-plan-existence-pspace-complete/), which is PSPACE-complete, unless PSPACE equals EXPTIME.
- In an acyclic problem each chain of decompositions passes through at most $|C|$ compound tasks, so a solution has at most $|w_0| \cdot k^{|C|}$ operators, where $k$ is the largest number of tasks in a method network. Solutions can be exponentially long, but there are only finitely many.
- With task insertion, plan existence is decidable in every case; for ground partially ordered problems it is NEXPTIME-complete, by the same IJCAI 2015 paper.

## Reductions

**From classical planning.** A STRIPS task $(F, O, s_0, G)$ becomes an HTN problem with one compound task $\mathit{solve}$, a method with precondition $G$ and the empty network, and for each operator $o$ a method $\mathit{solve} \to o, \mathit{solve}$. With $w_0 = \{\mathit{solve}\}$, the solutions are exactly the plans of the STRIPS task. The result is ground, totally ordered and tail-recursive, and of linear size. So HTN plan existence is PSPACE-hard already in that class, and the PSPACE upper bound shows that the class is no harder than STRIPS. The implementation tests of the [hierarchical task network](/hierarchical-task-network/) page check this encoding on 150 random STRIPS tasks with 3 facts: the solutions found by bounded decomposition equal the plans of length at most 3 found by enumerating all operator sequences.

**From the intersection of context-free languages.** Given two context-free grammars $G_1$ and $G_2$ over an alphabet $\Sigma$, it is undecidable whether $L(G_1) \cap L(G_2)$ is empty, by a reduction from the [Post correspondence problem](/post-correspondence-problem/). Build an HTN problem in the spirit of Erol, Hendler and Nau:

- each nonterminal of $G_i$ becomes a compound task, and each production a totally ordered method;
- each terminal $a$ of $G_1$ becomes an operator $a_1$ with precondition $\mathit{turn}_1$, which deletes $\mathit{turn}_1$ and adds $\mathit{turn}_2$ and $\mathit{last}_a$;
- each terminal $a$ of $G_2$ becomes an operator $a_2$ with precondition $\mathit{turn}_2$ and $\mathit{last}_a$, which deletes both and adds $\mathit{turn}_1$;
- $s_0 = \{\mathit{turn}_1\}$, and $w_0$ holds the start symbols $S_1$ and $S_2$, unordered, and an operator $\mathit{check}$ with precondition $\mathit{turn}_1$, ordered after both.

The facts force every executable linearization to alternate a letter of $G_1$ with the same letter of $G_2$, and $\mathit{check}$ forces both words to end together. So the problem has a solution if and only if some word is in both languages. The networks are partially ordered only because $S_1$ and $S_2$ are unordered, and both grammars are recursive in general. This proves that the partially ordered case with arbitrary recursion is [undecidable](/undecidability/).

**To context-free grammars.** A totally ordered problem whose operators have no preconditions or effects is a context-free grammar, with compound tasks as nonterminals and methods as productions, and plan existence is the emptiness test of the grammar. Preconditions and effects make the totally ordered case harder, EXPTIME-complete when ground, but keep it decidable.

## Applications

- **Domain-configurable planning.** The methods hold expert knowledge about how tasks are usually done, which makes a planner for one domain fast and its plans predictable. SHOP2 is the standard example and shared a distinguished performance award at the 2002 International Planning Competition.
- **Logistics, manufacturing and operations.** SIPE and O-Plan were built for large military and industrial planning problems, where plans must follow standard procedures.
- **Games and interactive agents.** Non-player characters in video games are often controlled by HTN planners with totally ordered methods, because the designer can say exactly how a behaviour may unfold.
- **Plan recognition.** The same methods can be read backwards: given observed actions, find the task whose decomposition explains them; see [plan recognition](/plan-recognition/).
- **Web service composition.** Composite services are described as methods over atomic services, and composition becomes HTN planning.

## References
