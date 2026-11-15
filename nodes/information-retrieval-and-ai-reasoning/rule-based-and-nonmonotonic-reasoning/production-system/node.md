---
tag: W79EPH
kind: model
slug: production-system
name: Production system
aliases:
- production rule system
- rule-based system
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: intro
summary: A working memory of facts and a set of if-then rules, run by a cycle that matches rules, selects one and fires its actions.
history:
  year: 1972
  people: [Allen Newell, Herbert A. Simon]
  note: "Newell and Simon used sets of condition-action rules over a short-term memory as models of human problem solving; the name and the rewriting idea go back to Post's productions of 1943."
prereqs: [turing-machine, horn-clause]
see_also: [forward-chaining, backward-chaining, conflict-resolution-strategy, rete-algorithm, treat-algorithm, justification-based-truth-maintenance, strips, markov-algorithm]
sources:
  - book: isbn:9780134454030
    title: "Allen Newell and Herbert A. Simon, Human Problem Solving, Prentice-Hall (1972)"
    locator: "the production system models of problem solving behaviour"
  - paper: doi:10.2307/2371809
    title: "Emil L. Post, Formal reductions of the general combinatorial decision problem, American Journal of Mathematics 65(2), 197 to 215 (1943)"
    locator: "productions on strings and the normal form theorem"
  - paper: "Charles L. Forgy, OPS5 user's manual, technical report CMU-CS-81-135, Carnegie Mellon University (1981)"
    locator: "working memory elements and time tags, the recognize-act cycle, the actions, and the conflict resolution strategies"
  - book: isbn:9780201106473
    title: "Lee Brownston, Robert Farrell, Elaine Kant and Nancy Martin, Programming Expert Systems in OPS5, Addison-Wesley (1985)"
    locator: "the description of the OPS5 language and its recognize-act cycle"
  - paper: doi:10.1016/0004-3702(82)90020-0
    title: "Charles L. Forgy, Rete: a fast algorithm for the many pattern/many object pattern match problem, Artificial Intelligence 19(1), 17 to 37 (1982)"
    locator: "the match problem of production systems and the cost of the match step"
  - paper: doi:10.1145/800105.803397
    title: "Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the Ninth Annual ACM Symposium on Theory of Computing, 77 to 90 (1977)"
    locator: "the NP-completeness of answering conjunctive queries"
  - paper: doi:10.1145/502807.502810
    title: "Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)"
    locator: "the data and combined complexity of Datalog"
---

A production system is a model of computation with three parts: a *working memory* of facts, a *production memory* of condition-action rules, and an interpreter that runs the *recognize-act cycle*. In each cycle the interpreter finds every rule instance whose conditions hold in the working memory, picks one of them by a [conflict resolution strategy](/conflict-resolution-strategy/), and runs its actions, which add facts to the memory or remove facts from it. Newell and Simon used the model for human problem solving, and languages such as OPS5 and CLIPS made it a way to program expert systems. The model is Turing complete. Its monotone fragment, with additions only, is [Datalog](/datalog/) run by [forward chaining](/forward-chaining/).

## The machine

A *working memory element* (WME) is a ground fact, such as $(\mathit{counter}\ \mathit{value}\ 0)$, with a *time tag* that tells when it entered the memory. A *production* has the form

$$r:\ c_1, \ldots, c_k, \neg d_1, \ldots, \neg d_l \Rightarrow a_1, \ldots, a_p$$

where the conditions $c_i$ and $d_j$ are patterns with variables, and each action $a_q$ is *make* (add a WME), *remove* (delete the WME that matched a condition), *modify* (remove and make again with a new time tag), *write* or *halt*. An *instantiation* of $r$ is a pair of $r$ and a substitution $\sigma$ of constants for the variables such that each $c_i \sigma$ matches a WME, each test on the variables holds, and no $d_j \sigma$ matches a WME. The set of all instantiations is the *conflict set*. The interpreter runs this cycle:

1. **Match.** Compute the conflict set for the current working memory.
2. **Select.** If the conflict set is empty, stop. Otherwise choose one instantiation by the conflict resolution strategy. Refraction removes the instantiations that have already fired on the same WMEs.
3. **Act.** Run the actions of the chosen instantiation in order. Stop on *halt*; else go to step 1.

A configuration is the working memory with its time tags and the record of fired instantiations. The strategy makes the machine deterministic; without one, the machine is nondeterministic and each choice gives a different run.

For example, take the WMEs 1: $(\mathit{goal}\ \mathit{count}\ 2)$ and 2: $(\mathit{counter}\ \mathit{value}\ 0)$, and two rules: *step* says that if $(\mathit{goal}\ \mathit{count}\ N)$ and $(\mathit{counter}\ \mathit{value}\ V)$ with $V < N$, then modify the counter to $V + 1$; *stop* says that if $(\mathit{goal}\ \mathit{count}\ N)$ and $(\mathit{counter}\ \mathit{value}\ N)$, then write "done" and halt.

| cycle | conflict set | fired | working memory after |
|---|---|---|---|
| 1 | step on 1 and 2 | step | 1, and 3: $(\mathit{counter}\ \mathit{value}\ 1)$ |
| 2 | step on 1 and 3 | step | 1, and 4: $(\mathit{counter}\ \mathit{value}\ 2)$ |
| 3 | stop on 1 and 4 | stop | halt |

The *modify* action gives the counter a new time tag in each cycle, so refraction does not block *step* from firing again on the new WME.

**The logic of the monotone fragment.** When the rules have no negated conditions and their only action is *make*, a rule $r$ reads as the Horn rule $h \leftarrow b_1, \ldots, b_k$ for each fact $h$ that it makes. Then a WME stays in the memory once it is there, every run ends with the same memory, and that memory is the least model of the rules and the initial facts. With *remove* and with negated conditions, a rule such as $h \leftarrow b_1, \ldots, b_k, \mathit{not}\ c_1$ no longer has a meaning on its own: the result depends on the order of firing, so the strategy is part of the program.

## What it counts

The cost of a run has two parts. The first is the number of cycles, one for each firing. The second is the work of the match step in each cycle: the instantiations, and the partial matches of the conditions of each rule, that the interpreter finds and stores. The [Rete](/rete-algorithm/) and [TREAT](/treat-algorithm/) algorithms keep match state from one cycle to the next, so that a cycle costs time in proportion to the change in the memory and not to its size. Forgy and later authors reported, from measurements on OPS-style programs, that the match step takes most of the running time; this is an observation about programs, not a theorem.

For complexity, the input is the rule set and the working memory. The *data complexity* fixes the rules and lets the memory of $n$ WMEs grow; the *combined complexity* lets both grow. A rule with $m$ positive conditions has at most $n^m$ instantiations, so for fixed rules the match step is polynomial.

## Relation to other models

- **[Post canonical systems](/post-canonical-system/)** rewrite strings by productions, and every applicable production may be used. A production system with no strategy is a nondeterministic rewriting system of this kind on sets of facts.
- **[Markov algorithms](/markov-algorithm/)** are ordered string-rewriting rules, where the first rule that applies fires. This is a production system whose strategy is a fixed priority on rules.
- **[Turing machines](/turing-machine/)** and production systems simulate each other with one cycle for each step (see below).
- **[Datalog](/datalog/) and [Horn clauses](/horn-clause/).** The monotone fragment is Datalog evaluated by [forward chaining](/forward-chaining/). [Backward chaining](/backward-chaining/) runs the same rules from the goal.
- **[STRIPS](/strips/).** A STRIPS operator, with preconditions, an add list and a delete list, is a production without negated conditions. A planner searches over the possible orders of firing; a production system commits to the choice of its strategy and does not go back.
- **[Truth maintenance](/justification-based-truth-maintenance/).** A truth maintenance system keeps the reasons for the facts that the rules made, so that a fact can go away when its reasons do.

## Known results in the model

**Turing completeness.** A production system with *make*, *remove* and a way to create new symbols, such as the *genatom* function of OPS5, can simulate a deterministic Turing machine. Represent each tape cell by a WME $(\mathit{cell}\ c\ s\ l\ r)$ with its identifier $c$, its symbol $s$ and the identifiers $l$ and $r$ of its neighbours, and the head by $(\mathit{head}\ c\ q)$. For each transition $(q, s) \to (q', s', \mathrm{R})$, one rule matches the head and its cell, writes $s'$ and moves the head to the right neighbour; a second rule with a negated condition handles the case where the right neighbour does not yet exist, and makes a new blank cell with a new identifier. Moves to the left are the same. At each moment at most one rule instance applies, so the strategy plays no part, and each step of the machine is one cycle. So whether a production system halts is undecidable.

**Finite systems.** If the actions cannot create new values, as with no new symbols and no arithmetic, every WME is one of finitely many ground facts. Then there are finitely many configurations, and whether a run halts is decidable.

**Order independence of the monotone fragment.** With *make* as the only action and no negated conditions, every fair run reaches the same final memory, the least model, after at most as many firings as there are ground facts. The [forward chaining](/forward-chaining/) page proves this. The result fails as soon as either feature is added. With the memory $\{a\}$ and the rules $a \Rightarrow \mathit{make}\ b$ and $a, \neg b \Rightarrow \mathit{make}\ c$, firing the first rule first ends with $\{a, b\}$, and firing the second rule first ends with $\{a, b, c\}$.

**The match problem.** Deciding whether one rule without negated conditions has an instantiation is the evaluation of a conjunctive query over the working memory. In combined complexity it is [NP-complete](/np-complete/) (Chandra and Merlin 1977); the [clique problem](/clique-problem/) reduces to it, since a graph without loops, stored as edge WMEs in both directions, has a clique of size $k$ exactly when the rule with the conditions $(\mathit{edge}\ x_i\ x_j)$ for all $i < j \le k$ has an instantiation. In data complexity it takes $O(n^m)$ time for a rule with $m$ conditions.

**The monotone fragment as Datalog.** Computing the final memory of a monotone system is P-complete in data complexity and [EXPTIME](/exptime/)-complete in combined complexity, the known results for Datalog (Dantsin, Eiter, Gottlob and Voronkov 2001).

## References
