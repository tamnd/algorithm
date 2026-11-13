---
tag: GRM387
kind: concept
slug: mutex-relation
name: Mutex relation
aliases:
- mutual exclusion in planning
area: games-and-search/planning
level: core
summary: Pairs of facts or actions that cannot hold or be applied together at a given level.
prereqs: [strips, planning-graph]
see_also: [graphplan, invariant, sas-plus, satplan, temporal-planning, relaxed-planning-graph, blocks-world, state-space]
sources:
  - paper: doi:10.1016/S0004-3702(96)00047-1
    title: "Avrim L. Blum and Merrick L. Furst, Fast planning through planning graph analysis, Artificial Intelligence 90(1-2) (1997)"
    locator: pp. 281 to 300; Section 2 (the mutual exclusion rules for actions and for propositions), Section 5.2 (a goal set whose pairs are not mutex but which is unreachable)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 6 (planning-graph techniques; the mutual exclusion relations and their properties)
  - paper: "Patrik Haslum and Hector Geffner, Admissible heuristics for optimal planning, Proceedings of AIPS 2000"
    locator: the h^m heuristics, and the relation of h^2 to the planning-graph mutexes (general locator)
  - paper: doi:10.1016/j.artint.2008.10.013
    title: "Malte Helmert, Concise finite-domain representations for PDDL planning tasks, Artificial Intelligence 173(5-6) (2009)"
    locator: the invariant synthesis and the mutex groups that become finite-domain variables (general locator)
---

A mutex relation in planning marks pairs that cannot occur together. Two facts are mutex at level $k$ of a [planning graph](/planning-graph/) when no state reachable in $k$ parallel steps can make both true, as far as the pairwise rules can tell. Two actions are mutex at level $k$ when they cannot run in the same parallel step at that level. Blum and Furst (1997) gave the rules for [GRAPHPLAN](/graphplan/): actions are mutex by inconsistent effects, interference or competing needs, and facts are mutex when every pair of their achievers is mutex. The relation is sound: a marked pair is truly impossible. It is not complete: some impossible pairs are never marked. Once the graph levels off, the fact mutexes are [invariants](/invariant/) of the whole [state space](/state-space/), and planners use them to prune search, to strengthen SAT encodings and to build the finite-domain variables of [SAS+](/sas-plus/).

## In plain words

Some things cannot happen at the same time. A robot hand cannot hold two blocks. A block cannot be on the table and in the hand. A mutex is a note that says "these two never go together".

The notes are made from simple rules, one step at a time. Two actions clash if one undoes what the other needs or makes, or if they need things that clash. Two facts clash if every way to get the first clashes with every way to get the second.

The rules only ever look at two things at once. So every note is true, but some true clashes are missed: a clash that needs three things at once to see stays unmarked. Over time, notes only disappear, never appear on old pairs, and after a while they stop changing.

## The idea

Fix a [STRIPS](/strips/) task with initial state $I$ and the planning graph levels $P_0 = I, A_0, P_1, A_1, \ldots$, where $A_k$ includes a no-op for each fact of $P_k$. The relation has two parts, defined by induction on $k$.

**Action mutexes at level $k$.** Two actions $a \ne b$ of $A_k$ are mutex when one of these holds:

1. **inconsistent effects**: $\mathrm{del}(a) \cap \mathrm{add}(b) \ne \emptyset$ or $\mathrm{del}(b) \cap \mathrm{add}(a) \ne \emptyset$;
2. **interference**: $\mathrm{del}(a) \cap \mathrm{pre}(b) \ne \emptyset$ or $\mathrm{del}(b) \cap \mathrm{pre}(a) \ne \emptyset$;
3. **competing needs**: some $p \in \mathrm{pre}(a)$ and $q \in \mathrm{pre}(b)$ are mutex at fact level $k$.

Rules 1 and 2 depend only on the actions, so they hold at every level. Together they are the conflict that a parallel step forbids. If neither action deletes a precondition or an add effect of the other, both stay applicable after the other, and both orders give the same state. Rule 3 depends on the level and can stop holding at a later level.

**Fact mutexes at level $k + 1$.** Two facts $p \ne q$ of $P_{k+1}$ are mutex when every action of $A_k$ that adds $p$ is mutex with every action of $A_k$ that adds $q$. An action that adds both is never mutex with itself, so such a pair is not marked.

**Soundness.** If a state $s$ is reachable from $I$ by at most $k$ parallel steps, then no two facts of $s$ are mutex at level $k$, and no two actions of a parallel step applicable in $s$ are mutex at level $k$. The proof is an induction on $k$: a fact of the next state is added by an action of the step or carried by a no-op, and these achievers are pairwise not mutex. The [planning graph correctness proof](/planning-graph/proofs/correctness/) gives it in full.

**Monotonicity and invariants.** A pair that is not mutex at level $k$ is not mutex at level $k + 1$. So mutexes only disappear on old pairs, and the relation reaches a fixed point when the graph levels off, at some level $L$. A fact pair mutex at level $L$ is mutex at every level after it, so by soundness no reachable state contains it. Such a pair is an invariant, of the form "not both $p$ and $q$". The converse is false: an invariant need not be found.

**Why it is incomplete.** The rules see pairs only. If a set of three facts is impossible but each of its pairs is possible, an action that needs all three still enters the graph, and its effects then look possible with everything else. Blum and Furst (1997, Section 5.2) give a three-block goal $\mathit{on}(A, B)$, $\mathit{on}(B, C)$, $\mathit{on}(C, A)$ whose pairs are all achievable but which is not. Mutexes over $t$ facts, as in the $h^m$ family of Haslum and Geffner (2000), catch more impossible sets at a cost that grows like $n^t$ for $n$ facts.

The relation here is a property of one task and one level. It differs from a mutex in concurrent programming, a lock that lets one thread at a time into a critical section. The name is the same because both say "not both at once".

## Examples

**Blocks world.** In the blocks world with three blocks on the table at the start, the graph has 16 facts. The fact mutexes per level are 0, 12, 57, 51, 45 and then 45 again, so the graph levels off at level 4 with 45 mutex pairs. The facts all appear by level 2, but mutexes keep disappearing for two more levels. The 22 reachable states never contain exactly 45 of the fact pairs, so here the mutexes at the level off are all the pair invariants of the task. With four blocks the same holds: 25 facts, 96 mutex pairs at the level off (reached at level 4), 125 reachable states, and the 96 pairs are exactly the pairs that never occur together. Typical marked pairs are $\mathit{holding}(A)$ with $\mathit{handempty}$, $\mathit{on}(A, B)$ with $\mathit{ontable}(A)$, and $\mathit{on}(A, B)$ with $\mathit{on}(C, B)$.

**Two tokens and three slots.** Two token facts $t_1, t_2$ hold at the start. For each token $t$ and slot $x \in \{x, y, z\}$, an action $\mathit{put}(t, x)$ needs $t$, adds $x$ and deletes $t$. The action $\mathit{make}_u$ needs $x$ and $y$ and adds $u$. The action $\mathit{make}_v$ needs $z$ and adds $v$. The graph marks no fact mutex at any level: every pair of slots can be filled with the two tokens, so every action enters, and the achievers of any two facts include a pair that is not mutex. But the 19 reachable states never contain these 4 pairs: $u$ with $v$, $u$ with $z$, $u$ with $t_1$ and $u$ with $t_2$. Each needs three tokens' worth of work, and the pair rules cannot see it.

**Two actions in one step.** In the gripper task, $\mathit{pick}(b_1, a, \mathit{left})$ and $\mathit{pick}(b_2, a, \mathit{right})$ are not mutex: they share the precondition $\mathit{robby}(a)$, and neither deletes it. So [GRAPHPLAN](/graphplan/) can put both in one step. The actions $\mathit{pick}(b_1, a, \mathit{left})$ and $\mathit{pick}(b_2, a, \mathit{left})$ are mutex by interference, because each deletes $\mathit{free}(\mathit{left})$, a precondition of the other.

## Where it is used

- **[GRAPHPLAN](/graphplan/).** The goal set must be pairwise non-mutex before the backward search starts at a level, and the search only picks pairwise non-mutex actions. This is the main source of its pruning.
- **[SATPLAN](/satplan/) and Blackbox.** Action mutexes become binary clauses $\neg a_t \vee \neg b_t$. Fact mutexes at the level off are valid at every time step and can be added as clauses $\neg p_t \vee \neg q_t$; they are redundant for correctness but help unit propagation.
- **[SAS+](/sas-plus/) translation.** A set of facts that are pairwise mutex and of which exactly one is always true is a mutex group, and it becomes one finite-domain variable. Fast Downward finds such groups by invariant synthesis on the lifted task (Helmert 2009).
- **Pruning in forward and backward search.** A regressed goal set that contains a mutex pair can be discarded at once, because no reachable state satisfies it. This is a standard use in [backward state-space search](/backward-state-space-search/).
- **[Temporal planning](/temporal-planning/).** TGP (Smith and Weld 1999) extends the mutex rules to actions with durations, and its planning graph records when two actions or facts stop being mutex in time.

## References
