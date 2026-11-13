---
tag: K3AVD8
kind: algorithm
slug: snlp
name: SNLP (systematic nonlinear planner)
aliases:
- Systematic Nonlinear Planning
area: games-and-search/planning
level: advanced
summary: A causal-link planner for STRIPS that counts a step as a threat when it adds or deletes the linked fact. Sound and complete, and systematic, no two complete plans it reaches share a linearization.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the bound on the number of steps, a: the number of ground actions, p: the largest number of preconditions of an action or of the goal}
  time: {worst: O(n^2 (n + p) (n + a)^(n (n + p)))}
  space: {extra: O(n^2 (n + p)^2)}
properties: {deterministic: true, online: false, exact: true, recursive: true}
history:
  year: 1991
  people: [David McAllester, David Rosenblitt]
  note: A ground, simplified version of Tate's NONLIN with a stronger notion of threat, published at AAAI-91 with a separate lifting step for operator schemas.
prereqs: [pop-partial-order-planning, causal-link]
see_also: [tweak, ucpop, plan-space-planning, partial-order-plan, least-commitment-principle, sussman-anomaly, iterative-deepening-search, state-space-planning]
sources:
  - paper: "David McAllester and David Rosenblitt, Systematic nonlinear planning, Proceedings of AAAI-91"
    locator: pp. 634 to 639 (p. 635 causal links, threats that add or delete, complete nonlinear plans; p. 636 FIND-COMPLETION and the systematicity argument; pp. 636 to 637 the comparison with Tate's threat; pp. 637 to 638 lifting)
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (causal-link planning in the style of SNLP and POP; general locator)
  - paper: doi:10.1016/0004-3702(94)90012-4
    title: "Anthony Barrett and Daniel S. Weld, Partial-order planning: evaluating possible efficiency gains, Artificial Intelligence 67(1) (1994)"
    locator: pp. 71 to 112 (SNLP against total-order planners; general locator)
  - paper: doi:10.1016/0004-3702(94)00076-D
    title: "Subbarao Kambhampati, Craig A. Knoblock and Qiang Yang, Planning as refinement search: a unified framework for evaluating design tradeoffs in partial-order planning, Artificial Intelligence 76 (1995)"
    locator: pp. 167 to 238 (systematicity, redundancy and commitment in refinement planners; general locator)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (plan-space planning; general locator)
---

SNLP is the causal-link planner of McAllester and Rosenblitt (1991). It searches the space of [partial-order plans](/partial-order-plan/) for a [STRIPS](/strips/) task exactly as [POP](/pop-partial-order-planning/) does: it repairs open conditions by [causal links](/causal-link/) and threats by orderings, and a plan with no flaw has only valid linearizations. The one change is the notion of threat. In SNLP a step threatens a link $i \xrightarrow{p} j$ if it may lie between $i$ and $j$ and it deletes $p$ *or adds* $p$. With this rule the search is systematic: two different branches never reach complete plans that share a linearization, so no action sequence is found twice.

## In plain words

Think of POP with one stricter rule. An arrow from a giver to a taker says "this is where the taker gets its fact". In POP, only a step that could destroy the fact in the gap is a problem. In SNLP, a step that could give the same fact again in the gap is a problem too, and it must also move before the giver or after the taker.

Why bother? With the strict rule, the arrow always comes from the last giver before the taker. So if you look at any finished plan as a sequence, you can read the arrows off the sequence. Two different finished plans can then never stand for the same sequence, and the search never does the same work twice in different branches. The price is more problems to fix in each plan.

## The problem

The input is a ground STRIPS task $(F, A, I, G)$: a finite set $F$ of facts, a finite set $A$ of actions, each with a precondition $\mathit{pre}(a)$, an add list $\mathit{add}(a)$ and a delete list $\mathit{del}(a)$, an initial state $I \subseteq F$ and a goal $G \subseteq F$. The output is a partial-order plan whose every linearization is a plan, or the answer that no plan exists.

A partial plan has a START step that adds $I$, a FINISH step that needs $G$, other steps that are copies of actions, an acyclic ordering $\prec$ and causal links $i \xrightarrow{p} j$ with $p \in \mathit{add}(i) \cap \mathit{pre}(j)$ and $i \prec j$. Its flaws are:

- an **open condition** $(p, j)$: $p \in \mathit{pre}(j)$ and no link ends at $j$ with the fact $p$;
- a **threat** $(k, i \xrightarrow{p} j)$: $k \ne i, j$, $p \in \mathit{del}(k) \cup \mathit{add}(k)$, and neither $k \prec i$ nor $j \prec k$ holds.

The second line is the only difference from POP, where a threat needs $p \in \mathit{del}(k)$.

## The algorithm

The search is depth first with a bound $n$ on the number of steps other than START and FINISH, inside [iterative deepening](/iterative-deepening-search/) on $n$. McAllester and Rosenblitt state it as the procedure FIND-COMPLETION with a cost bound, to be used with iterative deepening. Here it has the same shape as the POP page, so the two can be compared line by line.

```pseudo id=main
SNLP(I, G, A)
L1  for n ← 0, 1, ..., 2^|F| − 1 do
L2      cut ← false
L3      Q ← REFINE(the plan START ≺ FINISH for I and G, A, n)
L4      if Q ≠ failure then return Q
L5      if cut = false then return failure          ▷ a larger n gives the same tree
L6  return failure
REFINE(P, A, n)
L7  if P has no open condition and no threat then return P
L8  f ← a flaw of P with the fewest resolvers
L9  if f is a threat (k, i -p-> j), where k adds or deletes p, then
L10     R ← the orderings k ≺ i (demotion) and j ≺ k (promotion) that keep ≺ acyclic
L11 else f is an open condition (p, j):
L12     R ← a link i -p-> j for each step i with p ∈ add(i) and not j ≺ i
L13     if P has fewer than n steps then add to R a new step of each action a with p ∈ add(a), linked to j
L14     else if some action adds p then cut ← true
L15 for each r in R do                              ▷ the choice point
L16     Q ← REFINE(P with r, A, n)
L17     if Q ≠ failure then return Q
L18 return failure
```

Line L9 is the change. A step that adds $p$ in the gap of a link on $p$ must be ordered out of the gap, even though it does no harm to the plan. In a complete plan this forces every link $i \xrightarrow{p} j$ to come from the last step before $j$ that adds $p$, in every linearization. Lines L12 and L13 choose the producer, and the choice is visible in every sequence below the branch. Line L10 chooses the side of a threat, and that is visible too. So the branches split the sequences into disjoint sets.

The cut test of line L5, the bound of line L1, the flaw rule of line L8 and the filter of useless actions are the same as for POP, and they keep the same guarantees.

## Example

Take three actions with no deletes: $A$ adds $p$; $R$ needs $p$ and adds $r$; $S$ needs $p$ and adds $s$. The initial state is empty and the goal is $\{p, r, s\}$. Enumerate all complete plans with at most 4 steps, once with the SNLP threat and once with the POP threat. Both searches find 4 complete plans, with the same steps and links. They differ in the orderings.

| plan | links for $p$ | SNLP sequences | POP sequences |
|---|---|---|---|
| 1 | $A_1$ to FINISH, $R$, $S$ | ARS, ASR | ARS, ASR |
| 2 | $A_1$ to FINISH, $R$; $A_2$ to $S$ | ASAR | AARS, AASR, ARAS, ASAR |
| 3 | $A_1$ to FINISH, $S$; $A_2$ to $R$ | ARAS | AARS, AASR, ARAS, ASAR |
| 4 | $A_1$ to FINISH; $A_2$ to $R$, $S$ | ARSA, ASRA | AARS, AASR, ARAS, ARSA, ASAR, ASRA |

In plan 2 under SNLP, $A_2$ adds $p$, so it threatens $A_1 \xrightarrow{p} R$ and $A_1 \xrightarrow{p} \text{FINISH}$, and it must come before $A_1$. Then $A_1$ threatens $A_2 \xrightarrow{p} S$, and $S$ must come before $A_1$. Only ASAR is left. POP has none of these orderings. Counted as action sequences plan by plan, its 4 plans have 16 linearizations but only 8 distinct sequences, and AARS appears in 3 of the plans. SNLP has 6 linearizations, all distinct. The sequences AARS and AASR are missing from SNLP, because the first $A$ in them is the last producer of nothing, so no complete SNLP plan reads that way. Without a bound, SNLP returns plan 1, the shortest, with the sequences ARS and ASR.

On the [Sussman anomaly](/sussman-anomaly/) SNLP finds the same plan as POP, $\mathit{move}(C, A, \mathit{table})$, $\mathit{move}(B, \mathit{table}, C)$, $\mathit{move}(A, \mathit{table}, B)$, with one linearization.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). There are five parts.

- **Soundness.** As for POP: in a complete plan no step that deletes $p$ can lie between the ends of a link on $p$, so each precondition holds when its step runs. The extra threats only add orderings.
- **Termination.** Each refinement adds a link, a step with a link, or a new pair to the ordering, and with at most $n$ steps there are finitely many of each.
- **Completeness.** Fix a plan $\sigma$ with at most $n$ actions. For an open condition $(p, j)$, link from the step for the last position of $\sigma$ before $j$ that adds $p$. A threatening step then never lies between the ends of a link in $\sigma$: if it adds $p$, the link would not come from the last adder, and if it only deletes $p$, $\sigma$ would not be a plan. So demotion or promotion agrees with $\sigma$.
- **Fewest steps.** Iterative deepening returns a plan in the first round $n$ that equals the length of a shortest plan.
- **Systematicity.** In a complete plan, the producer of every link is the last adder before the consumer in every linearization. So a sequence determines the position of each step, and two leaves below different resolvers of the same flaw cannot share a sequence.

The tests check these claims. On 400 random tasks with 3 or 4 facts, SNLP finds a plan if and only if breadth-first search finds one, with the same length, and every linearization is valid. On 200 random tasks with all complete plans of at most 4 steps, no sequence appears in two SNLP plans, and no partial plan is visited twice.

## Complexity

The bounds are those of POP, with the same variables. A branch has depth $O(n (n + p))$, a flaw has at most $n + a + 2$ resolvers, and a node costs $O(n^2 (n + p))$. Systematicity adds one bound that POP lacks: the complete plans of one bounded search have nonempty, pairwise disjoint sets of sequences of at most $n$ actions, so there are at most $\sum_{m \le n} a^m$ of them. The dead-end nodes are not bounded this way, and the worst case stays exponential, as it must, since [plan existence is PSPACE-complete](/strips-plan-existence-pspace-complete/).

In practice the effect goes both ways. On the example above SNLP visits 15 partial plans and POP 10, because the adder threats are extra flaws. On the 200 random tasks with 4 facts and full enumeration at bound 4, SNLP visits 5,883 nodes and finds 834 complete plans, while POP visits 20,469 nodes and finds 11,344 complete plans with only 1,196 distinct sequences among their 14,682 linearizations. To find the first plan with iterative deepening on the 400 test tasks, SNLP needs 6,156 nodes in total and POP 10,622.

## Properties

- **Systematic.** No sequence is a linearization of two complete plans that the search reaches. McAllester and Rosenblitt call two sequences equivalent when they have the same least complete plan, and show that equivalent plans are found down one branch.
- **Not exhaustive over sequences.** A sequence with a step that is the last producer of no needed fact has no complete SNLP plan. Shortest plans are never lost, but an enumeration of SNLP plans is not an enumeration of all plans.
- **Sound and complete.** Like POP, within the step bound.
- **More orderings.** SNLP plans are more ordered than POP plans with the same links, so they are less flexible to execute.
- **Ground first, lifted after.** The paper gives the ground procedure and then lifts it to operator schemas by replacing ground instances with variables, unification and disequality constraints.

## Variants and improvements

- **Lifted SNLP.** The version of the paper with variables. Step 4b picks an operator schema in place of a ground action, so in the blocks world the branching of that step is 1. See [TWEAK](/tweak/) for an older lifted planner.
- **POP.** Weld (1994) uses the weaker threat of Tate's NONLIN, where only deleters threaten. McAllester and Rosenblitt already guessed that the weaker threat "works just as well, if not better, in practice". See [POP](/pop-partial-order-planning/).
- **UCPOP.** Penberthy and Weld extend the SNLP and POP style to conditional and quantified effects. See [UCPOP](/ucpop/).
- **Abstraction.** The paper notes that the flaw choice of steps 3 and 4 may prefer abstract preconditions first, which gives planning in a hierarchy of abstraction spaces.
- **Refinement search.** Kambhampati, Knoblock and Yang (1995) describe POP, SNLP, TWEAK and others as refinement search and separate systematicity from the other design choices.

## When to use it

Use SNLP when the plans found must be counted or enumerated without repeats, for example to compare search spaces, to sample plans, or to prove that a search covers each solution once. For finding one plan fast, POP with a good flaw rule, or [state-space planning](/state-space-planning/) with a heuristic, is usually better. Use the lifted version when the ground action set is too large.

## Pitfalls

- **Reading systematic as "never revisits a node".** In this tree form, POP also never visits the same partial plan twice, because each open condition gets one link. Systematicity is about complete plans and their sequences, not about nodes.
- **Reading systematic as "smaller search".** The extra threats are flaws to resolve. On some tasks SNLP visits more nodes than POP.
- **Expecting every plan.** SNLP covers every sequence at most once, not at least once. Redundant steps are never explained by a link and do not appear.
- **Forgetting the producer.** A step that adds $p$ is not a threat to a link it produces, and the consumer is not a threat to its own link. Only $k \ne i, j$ counts.
- **Testing only direct orderings.** As for POP, "possibly between" must use the transitive closure of the orderings.

## Implementations

## History

Tate's NONLIN (1977) recorded for each precondition the step that achieves it, which it called a range. McAllester and Rosenblitt (1991) gave a simplified ground version of NONLIN, proved it sound and complete, and changed the threat so that a step that adds the fact also threatens. This made the search systematic in their sense: every branch divides the remaining solutions into disjoint sets. They also gave a lifting transformation in the style of Robinson's resolution, and noted a safe partial order, due to Kambhampati, that is not the order of any complete plan. The name SNLP comes from the title of the paper. Barrett and Weld (1994) used SNLP as their partial-order planner in comparisons with total-order planners, and Weld (1994) based the tutorial planner POP on the same scheme with the weaker threat.

## References
