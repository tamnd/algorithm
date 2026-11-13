---
tag: N5Z9YX
kind: technique
slug: planning-as-model-checking
name: Planning as model checking
area: games-and-search/planning
level: research
summary: Treat a nondeterministic planning domain as a transition system, and compute weak, strong or strong cyclic plans as fixed points over sets of states, often with BDDs.
prereqs: [classical-planning, ctl-model-checking, fixed-point]
see_also: [symbolic-model-checking, binary-decision-diagram, modal-mu-calculus, fairness, conformant-planning, contingent-planning, games-on-graphs, linear-temporal-logic]
sources:
  - paper: doi:10.1016/S0004-3702(02)00374-0
    title: Alessandro Cimatti, Marco Pistore, Marco Roveri and Paolo Traverso, Weak, strong, and strong cyclic planning via symbolic model checking, Artificial Intelligence 147(1-2), 2003
    locator: pp. 35 to 84 (weak, strong and strong cyclic plans as state-action tables, computed by fixed points on BDDs)
  - paper: doi:10.1007/10720246_1
    title: Fausto Giunchiglia and Paolo Traverso, Planning as model checking, Recent Advances in AI Planning (ECP 1999), LNCS 1809, 2000
    locator: pp. 1 to 20 (the planning problem stated as a model checking problem)
  - paper: doi:10.1613/jair.774
    title: Alessandro Cimatti and Marco Roveri, Conformant planning via symbolic model checking, Journal of Artificial Intelligence Research 13, 2000
    locator: pp. 305 to 338 (conformant plans by symbolic search over sets of states)
  - paper: doi:10.1613/jair.649
    title: Rune M. Jensen and Manuela M. Veloso, OBDD-based universal planning for synchronized agents in non-deterministic domains, Journal of Artificial Intelligence Research 13, 2000
    locator: pp. 189 to 226 (strong and strong cyclic universal plans with OBDDs)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 17 (planning based on model checking, with Section 17.2 on strong and strong cyclic plans)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 5.6 (strong and strong cyclic plans)
---

Planning as model checking is a technique for planning under nondeterminism. It treats the planning domain as a transition system, like the [Kripke structures](/kripke-structure/) of verification, and the goal as a property of the runs. It then computes the set of states from which a plan exists as a [fixed point](/fixed-point/) of a preimage operator, in the same way that a [CTL model checker](/ctl-model-checking/) computes the states that satisfy a formula. Three kinds of plan come out of three fixed points: a weak plan may reach the goal, a strong plan must reach it, and a strong cyclic plan reaches it under a [fairness](/fairness/) assumption on the outcomes. With the sets stored as [binary decision diagrams](/binary-decision-diagram/), the computation handles very large state spaces without listing their states, as in [symbolic model checking](/symbolic-model-checking/).

## In plain words

Some actions do not always have the same result. A robot tries to pick up a block, and the block can slip. A planner for such a world cannot give a fixed list of actions. It gives a table that tells, for each situation, which actions are good.

The planner builds the table from the goal backward. First it marks the goal situations. Then it marks each situation with an action that surely leads to marked situations, and it repeats until nothing changes. This gives plans that always work. A weaker form marks a situation if the action can lead to a marked one. A middle form allows retries: it keeps actions that can fail but never lead to a bad place, so that trying again works in the end. The same backward marking is what tools that check hardware and software do.

## When it applies

- The domain is a nondeterministic transition system $F : S \times A \to 2^S$ with full observation: after each action the agent knows the state. The result of $F(s, a)$ is not known in advance, and $F(s, a) = \emptyset$ means that $a$ is not applicable in $s$. For partial observation, the same fixed points run over sets of states, as in [conformant planning](/conformant-planning/) and [contingent planning](/contingent-planning/).
- The goal is a set $G$ of states, or more generally a formula of a temporal logic such as [CTL](/computation-tree-logic/) or [LTL](/linear-temporal-logic/) over the runs.
- A plan may be a memoryless policy, a state-action table $\pi \subseteq S \times A$. For reachability goals no memory is needed. Temporally extended goals can need plans with an internal state.
- The state space is too large to list, but it has a compact description by state variables, so that sets of states and the transition relation fit in binary decision diagrams.
- Probabilities are not known or not wanted. With probabilities, the problem is [MDP planning](/mdp-planning/).

## The template

For a set $Z$ of states, the **weak preimage** is $\mathrm{WP}(Z) = \{(s, a) : F(s, a) \cap Z \ne \emptyset\}$ and the **strong preimage** is $\mathrm{SP}(Z) = \{(s, a) : \emptyset \ne F(s, a) \subseteq Z\}$. A strong plan is the least fixed point of $Z \mapsto G \cup \mathrm{states}(\mathrm{SP}(Z))$, and a weak plan is the least fixed point with $\mathrm{WP}$ in place of $\mathrm{SP}$. A strong cyclic plan is the greatest fixed point of two prunings of the state-action table.

```pseudo id=main
STRONG-PLAN(F, G)                                  ▷ least fixed point
L1  Z ← G; π ← ∅
L2  repeat
L3      P ← {(s, a) : s ∉ Z, ∅ ≠ F(s, a) ⊆ Z}       ▷ strong preimage of Z
L4      if P = ∅ then return π, Z
L5      π ← π ∪ P; Z ← Z ∪ states(P)

STRONG-CYCLIC-PLAN(F, G)                           ▷ greatest fixed point
L6  T ← {(s, a) : s ∉ G, F(s, a) ≠ ∅}
L7  repeat
L8      T_old ← T
L9      remove from T each (s, a) with F(s, a) ⊄ G ∪ states(T), until no change
L10     W ← least fixed point of Z ← G ∪ {s : (s, a) ∈ T, F(s, a) ∩ Z ≠ ∅}
L11     T ← {(s, a) ∈ T : s ∈ W}
L12 until T = T_old
L13 return the pairs (s, a) of T with an outcome closer to G than s, in the distance of L10
```

**Why the strong plan works.** Let $Z_0 = G$ and $Z_k$ be the set after $k$ rounds. A pair added in round $k$ has all its outcomes in $Z_{k-1}$, so by induction every run of $\pi$ from a state of $Z_k$ is in $G$ within $k$ steps, whatever the outcomes are. Each state gets its actions in the first round where it appears, so $\pi$ has no cycle. Conversely, if some policy reaches $G$ from $s$ on all runs within $k$ steps, then $s \in Z_k$, by induction on $k$. So the fixed point is the set of all states with a strong plan. In the notation of the [modal mu-calculus](/modal-mu-calculus/), it is $\mu Z.\, G \vee \bigvee_a (\langle a \rangle \top \wedge [a] Z)$.

**Why the strong cyclic plan works.** Line L9 keeps only the pairs whose outcomes stay inside the states that the table covers, or in $G$. Lines L10 and L11 keep only the states from which $G$ can be reached with the pairs that are left. When the loop stops, both conditions hold at the same time. So every run of the table stays in $\mathrm{states}(T) \cup G$, and from every state of a run some path of the table leads to $G$. Line L13 keeps at each state only the actions with an outcome that lowers the weak distance. Under the fairness assumption, every outcome of an action that is taken infinitely often in a state happens infinitely often there. Take a fair run that never reaches $G$, and among the states that it visits infinitely often take one, $s$, of least distance. Some action is taken infinitely often at $s$, and its lowering outcome then happens infinitely often, which contradicts the choice of $s$. So every fair run reaches $G$. The set $T$ only shrinks, and it keeps every pair that a strong cyclic policy uses on its runs, because these pairs pass both prunings. So the result covers all the states that have a strong cyclic plan.

**Cost.** With explicit sets, let $N$ be the number of state-action pairs and $M$ the total size of the outcome sets. Each round of STRONG-PLAN adds a state or stops, so it takes at most $|S|$ rounds of $O(M)$ each, $O(|S| M)$ in all. STRONG-CYCLIC-PLAN removes a pair in each outer round except the last, so it takes at most $N + 1$ outer rounds of $O(|S| M)$ each. A symbolic planner computes each preimage with one relational product on BDDs, and the cost depends on the BDD sizes, not on $|S|$.

**Example.** A robot picks up a block. From the table, pick gives held, or leaves the block on the table, or drops it on the floor. From the floor, pick gives held or floor, and push moves the block back to the table. The goal is held. STRONG-PLAN stops at once: no state has an action whose outcomes all lie in $\{\text{held}\}$, so there is no strong plan. The weak plan has table and floor at distance 1. In STRONG-CYCLIC-PLAN no pair is pruned, and line L13 drops push, which leads only to the table at the same distance 1. The plan is: at the table pick, and on the floor pick. Every fair run ends with the block held.

## Classic examples

- **The MBP planner.** The Model Based Planner of Bertoli, Cimatti, Pistore, Roveri and Traverso implements weak, strong and strong cyclic planning with BDDs on top of the NuSMV model checker. The algorithms of the template are those of Cimatti, Pistore, Roveri and Traverso (2003).
- **Universal planning with OBDDs.** UMOP (Jensen and Veloso 2000) computes strong and strong cyclic universal plans, which are policies for all states, for several agents that act at the same time.
- **Conformant planning.** Cimatti and Roveri (2000) find [conformant plans](/conformant-planning/) by symbolic breadth-first search over sets of states, the [belief states](/belief-space/) without observations.
- **Contingent planning.** The same fixed points over beliefs, with a branch for each observation, give [contingent plans](/contingent-planning/) that are strong on every branch.
- **Games.** A strong plan is a winning strategy for the planner in a reachability game against nature, and STRONG-PLAN computes the attractor of $G$, as in [games on graphs](/games-on-graphs/).

## Variations

- **Temporally extended goals.** Goals in CTL or LTL, such as "reach $A$ and then stay in $B$", need plans with memory. Pistore and Traverso extend the method to CTL goals with plans as finite automata, and others compile [LTL](/linear-temporal-logic/) goals into automata that are run with the domain, as in [LTL model checking](/ltl-model-checking/).
- **Strong cyclic in CTL terms.** On the structure that the plan induces, with the goal states absorbing, a strong plan makes $\mathrm{AF}\, G$ true, a weak plan makes $\mathrm{EF}\, G$ true, and a strong cyclic plan makes $\mathrm{AG}\, \mathrm{EF}\, G$ true.
- **Optimal plans.** The rounds of STRONG-PLAN give the least worst-case number of steps to $G$ for each state, so the first-round actions form a plan of least worst-case length.
- **Explicit-state search.** Forward search in the AND-OR graph of the domain, with heuristics, often beats the backward fixed point when few states are reachable from the start.
- **Partial observability.** The fixed points run over sets of beliefs, and each belief is itself a set of states. Symbolic planners store each belief as a BDD and search forward over the beliefs that are reachable from the start.
- **Adversarial domains.** When the environment is an opponent and not a fair nature, only strong plans are safe, and strong cyclic plans give no guarantee.

## Pitfalls

- **Fairness is an assumption.** A strong cyclic plan works only if each outcome of a retried action happens in the end. A domain with an adversary, or with an outcome that is possible but never happens, breaks the guarantee.
- **Progress is needed.** The result of the two prunings alone can contain actions that loop without progress. If $F(s, a) = \{s\}$ and $F(s, b) = \{g\}$ with $g \in G$, both pairs pass the prunings, and a run that always takes $a$ is fair but never reaches $G$. Line L13 removes $a$.
- **Weak plans are not safe.** A weak plan says only that some run can reach $G$. Its other runs can end in a dead end.
- **BDD sizes.** The BDDs of the preimages can grow exponentially with a bad variable order or with some transition relations, the [state explosion problem](/state-explosion-problem/) in another form.
- **Memoryless plans are not enough for all goals.** For goals such as "visit $A$ and then $B$", a state-action table can fail where a plan with memory succeeds.
- **Applicability.** An action with $F(s, a) = \emptyset$ must not count as a strong preimage, though $\emptyset \subseteq Z$ for every $Z$.

## Exercises

1. Show that a state has a strong plan if and only if it is in the least fixed point of $Z \mapsto G \cup \mathrm{states}(\mathrm{SP}(Z))$.
2. Give a domain with at least three states in which the two prunings of STRONG-CYCLIC-PLAN keep a pair that has fair runs that never reach $G$, and check that line L13 removes it.
3. Prove that every strong plan is a strong cyclic plan, and every strong cyclic plan is a weak plan, and give domains that separate the three.
4. Write the strong cyclic condition as a formula of the modal mu-calculus with a nested greatest and least fixed point.
5. For a reachability game, show that STRONG-PLAN computes the attractor of $G$ for the player who chooses the actions.

## References
