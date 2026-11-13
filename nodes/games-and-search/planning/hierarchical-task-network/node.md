---
tag: 8H40VK
kind: model
slug: hierarchical-task-network
name: Hierarchical task network
aliases:
- HTN
area: games-and-search/planning
level: core
summary: A planning model in which the goal is a network of tasks, not a set of facts. Compound tasks are replaced by the subtasks of their methods until only executable actions remain.
history:
  year: 1994
  people: [Kutluhan Erol, James Hendler, Dana Nau]
  note: Erol, Hendler and Nau gave HTN planning its formal semantics and first complexity results in 1994, after two decades of HTN planners from NOAH and NONLIN to SIPE and O-Plan.
prereqs: [task-network, strips]
see_also: [htn-planning, htn-decomposition, classical-planning, context-free-grammar, plan-space-planning, macro-operators, pddl, undecidability]
sources:
  - paper: "Kutluhan Erol, James Hendler and Dana Nau, HTN planning: complexity and expressivity, Proceedings of AAAI-94"
    locator: pp. 1123 to 1128 (the formal model, undecidability in general, and the decidable restrictions)
  - paper: doi:10.1007/BF02136175
    title: "Kutluhan Erol, James Hendler and Dana Nau, Complexity results for HTN planning, Annals of Mathematics and Artificial Intelligence 18(1) (1996)"
    locator: pp. 69 to 93 (the full complexity analysis, by ordering, recursion and variables)
  - paper: doi:10.1609/icaps.v25i1.13721
    title: "Ron Alford, Pascal Bercher and David W. Aha, Tight bounds for HTN planning, Proceedings of ICAPS 2015"
    locator: pp. 7 to 15 (lifted HTN planning and the completeness results by variables, ordering and recursion)
  - paper: "Ron Alford, Pascal Bercher and David W. Aha, Tight bounds for HTN planning with task insertion, Proceedings of IJCAI 2015"
    locator: pp. 1502 to 1508 (Table 2, which lists the HTN results of the ICAPS paper next to those with task insertion)
  - paper: "Daniel Höller, Gregor Behnke, Pascal Bercher and Susanne Biundo, Language classification of hierarchical planning problems, Proceedings of ECAI 2014, IOS Press"
    locator: pp. 447 to 452 (solution sets as formal languages; HTN planning is more expressive than classical planning)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 11 (the HTN model, task networks, methods, and the relation to STRIPS)
---

A hierarchical task network (HTN) model describes a planning domain by what has to be done, not only by what has to hold at the end. Besides [STRIPS](/strips/) operators, which are the primitive tasks, it has compound tasks and methods. A method says how to do a compound task: under a precondition, replace it by a [task network](/task-network/) of subtasks with ordering constraints. A problem gives an initial state and an initial task network. A solution is a sequence of operators that arises from the initial network by repeated decomposition, respects the orderings, and is executable from the initial state. The model is strictly more expressive than classical planning: the plans of a STRIPS task always form a regular language, while an HTN can have exactly the plans $a^n b^n$.

## The machine

Fix a finite set $F$ of facts. An HTN domain is a tuple $(F, O, C, M)$:

- $O$ is a finite set of **primitive tasks**, each a STRIPS operator $o$ with $\mathit{pre}(o)$, $\mathit{add}(o)$, $\mathit{del}(o) \subseteq F$.
- $C$ is a finite set of **compound tasks**, disjoint from $O$.
- $M$ is a finite set of **methods**. A method $\mu$ has a task $\mathit{task}(\mu) \in C$, a precondition $\mathit{pre}(\mu) \subseteq F$, and a task network $\mathit{net}(\mu)$ over $O \cup C$.

A task network is a finite set of nodes, each labelled with a task, with a strict partial order on the nodes. A **problem** adds an initial state $s_0 \subseteq F$ and an initial task network $w_0$.

**Decomposition.** If a node $u$ of a network $w$ carries a compound task $c$ and $\mu$ is a method for $c$, then decomposing $u$ by $\mu$ removes $u$, adds a fresh copy of $\mathit{net}(\mu)$, and gives every new node all the orderings of $u$: whatever had to come before $u$ comes before each new node, and whatever had to come after $u$ comes after each new node. The orderings of $\mathit{net}(\mu)$ hold among the new nodes.

**Solutions.** A network is primitive if all its nodes carry primitive tasks. A sequence of operators $\pi$ is a solution if some primitive network $w$ arises from $w_0$ by finitely many decompositions, $\pi$ is the sequence of tasks of a linearization of $w$, every operator of $\pi$ applies in turn from $s_0$, and every method precondition holds at the right time. In the forward reading of SHOP, the right time is when the method is chosen, which is the state after all tasks that were executed before it. The formalization of Geier and Bercher, used for most complexity results, has no method preconditions at all; a precondition can be compiled into a primitive task with that precondition and no effects, placed before the subtasks.

**Variants of the machine.** Erol, Hendler and Nau allowed state constraints in a network: a fact must hold just before a node, just after it, or between two nodes. Lifted models put variables in tasks and methods, and ground them like action schemas. With **task insertion**, a solution may also contain operators that no decomposition produced; this weakens the hierarchy.

## What it counts

The model asks which operator sequences are solutions, so its basic object is the **solution set**, a set of words over the alphabet $O$. Four measures matter.

- **Plan length**, the number of operators in a solution. Unlike classical planning, there is no a priori bound in terms of $|F|$: a recursive method can be required to run many times before the network becomes primitive.
- **Decomposition depth**, the length of the longest chain of methods from a node of $w_0$ to a primitive node. A search bounded by depth $d$, as in the [HTN decomposition planner](/htn-decomposition/), finds exactly the solutions of depth at most $d$.
- **Network size** at each point of a decomposition. For totally ordered networks it is the stack depth of a recursive procedure; for partially ordered networks it can grow without bound while the plan prefix stays the same.
- **Input size**, the total size of $F$, $O$, $C$, $M$, $s_0$ and $w_0$, in which the complexity of plan existence is measured.

## Relation to other models

**Classical planning is a special case.** Given a STRIPS task with operators $O$ and goal $G$, make one compound task *solve* with a method *stop*, with precondition $G$ and no subtasks, and for each operator $o$ a method with no precondition and the subtasks $o$, *solve*, in this order. Start with the network $\{\mathit{solve}\}$. Each decomposition either stops in a goal state or applies one more operator, so the solutions are exactly the STRIPS plans. This network is totally ordered and tail-recursive.

**The converse fails.** The plans of a STRIPS task form a regular language: a finite automaton with one state per subset of $F$ accepts exactly the plans. Take the HTN with primitive tasks $a$ and $b$, which need and change nothing, and one compound task $S$ with two methods, $S \to a, S, b$ and $S \to a, b$, both totally ordered. Its solutions are $a^n b^n$ for $n \ge 1$, which is not regular. So no STRIPS task over the actions $a$ and $b$ has these plans. The general picture, due to Höller, Behnke, Bercher and Biundo, places the formalisms in the Chomsky hierarchy: classical planning gives regular languages, totally ordered HTN planning gives context-free languages, and partially ordered HTN planning reaches beyond them.

**Context-free grammars.** A totally ordered HTN without preconditions or effects is a [context-free grammar](/context-free-grammar/): compound tasks are nonterminals, primitive tasks are terminals, and methods are productions. Partial order adds interleaving, the shuffle of the words of several nonterminals, and this is what makes the model undecidable.

**Plan-space and macro planning.** A method is like a [macro operator](/macro-operators/) whose body is a network and not a fixed sequence, and whose use is forced by the task, not chosen by the planner. Hybrid planning combines HTN decomposition with the open preconditions and threats of [plan-space planning](/plan-space-planning/).

**Languages.** The [PDDL](/pddl/) family has no tasks or methods. HDDL, an extension of PDDL, describes HTN domains and problems for the hierarchical track of the International Planning Competition.

## Known results in the model

**Plan existence.** Erol, Hendler and Nau proved that it is [undecidable](/undecidability/) whether an HTN problem has a solution, even without variables, as soon as networks may be partially ordered and methods recursive. The proof encodes whether two context-free grammars generate a common word. They also showed that plan existence becomes decidable for totally ordered networks, for acyclic domains, in which no task can be reached again from itself by decomposition, and for regular domains, in which every method network has at most one compound task and it comes after all others.

**Tight bounds.** Alford, Bercher and Aha completed the picture with completeness results along three axes. The table below gives them as listed in their IJCAI 2015 paper, Table 2. "Tail" means tail-recursive domains, a generalization of regular ones in which recursion happens only in the last task of a method.

| variables | ordering | acyclic | regular | tail | arbitrary |
|---|---|---|---|---|---|
| no | total | PSPACE | PSPACE | PSPACE | EXPTIME |
| no | partial | NEXPTIME | PSPACE | EXPSPACE | undecidable |
| yes | total | EXPSPACE | EXPSPACE | EXPSPACE | 2-EXPTIME |
| yes | partial | 2-NEXPTIME | EXPSPACE | 2-EXPSPACE | undecidable |

Each entry is the class for which plan existence is complete. For comparison, ground STRIPS plan existence is PSPACE-complete; see [STRIPS plan existence is PSPACE-complete](/strips-plan-existence-pspace-complete/). So ground totally ordered HTN planning with arbitrary recursion is harder than classical planning unless PSPACE equals EXPTIME, while the ground totally ordered tail-recursive class, which contains the STRIPS encoding above, is exactly as hard.

**Task insertion.** If a solution may contain extra operators, plan existence becomes decidable in all cases; in the ground case with partial order it is NEXPTIME-complete, by the same IJCAI 2015 paper.

**Expressivity.** The $a^n b^n$ example shows that the solution sets of HTN problems include languages that no classical problem has, and Höller et al. showed that the inclusion of classical in totally ordered in partially ordered HTN planning is strict at the level of languages.

## References
