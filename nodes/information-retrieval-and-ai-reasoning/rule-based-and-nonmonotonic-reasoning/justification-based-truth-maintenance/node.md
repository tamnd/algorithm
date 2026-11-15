---
tag: 1C7A95
kind: algorithm
slug: justification-based-truth-maintenance
name: Justification-based truth maintenance
aliases:
- JTMS
- Doyle truth maintenance system
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Records a justification for each derived belief and relabels beliefs in and out when assumptions change, keeping the belief set well founded.
model: word-ram
complexity:
  vars: {n: the number of nodes, s: the total size of all justifications}
  time: {worst: O(n s)}
  space: {extra: O(n + s)}
properties: {deterministic: true, incremental: true}
history:
  year: 1979
  people: [Jon Doyle]
  note: Doyle's truth maintenance system, from his MIT work, kept for each belief the justifications that support it, with in-lists and out-lists, and relabelled the beliefs when a justification was added or retracted.
prereqs: [well-founded-semantics, nonmonotonic-reasoning]
see_also: [assumption-based-truth-maintenance, stable-model-semantics, alternating-fixpoint, negation-as-failure, stratified-logic-program, splitting-set-theorem, forward-chaining, production-system]
sources:
  - paper: doi:10.1016/0004-3702(79)90008-0
    title: "Jon Doyle, A truth maintenance system, Artificial Intelligence 12(3), 231 to 272 (1979)"
    locator: the definitions of nodes, SL justifications with in-lists and out-lists, well-founded support, the relabelling procedure and dependency-directed backtracking
  - paper: doi:10.1016/0004-3702(90)90086-F
    title: "Charles Elkan, A rational reconstruction of nonmonotonic truth maintenance systems, Artificial Intelligence 43(2), 219 to 234 (1990)"
    locator: the reading of the labellings of a nonmonotonic TMS as stable models, and the proof that finding one is NP-complete
  - book: isbn:9780262061575
    title: Kenneth D. Forbus and Johan de Kleer, Building Problem Solvers, MIT Press (1993)
    locator: the chapters on the justification-based TMS, its interface to a rule engine, and contradiction handling
  - paper: "Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)"
    locator: unfounded sets and the definition of the well-founded model as the least fixed point of the operator W
---

A justification-based truth maintenance system (JTMS) is a bookkeeping layer under a reasoner. The reasoner tells it the *justifications* of its beliefs, each of the form "believe $x$ if all of these nodes are IN and all of those are OUT", and the JTMS labels each node IN or OUT so that every IN node has a non-circular argument from the current premises. When a premise is retracted, or a new justification arrives, it relabels only the nodes that depend on the change. Doyle's system of 1979 allowed out-lists, which make the beliefs nonmonotonic: a node can go OUT because another node came IN. This page gives the logic behind the labels, the [well-founded semantics](/well-founded-semantics/) of the network read as a logic program, and an incremental relabelling procedure that computes it, with a third label UNDEC for the nodes that the semantics leaves open. The labels Doyle's own procedure picks on such nodes correspond to the stable models of the network.

## In plain words

A reasoning program draws many conclusions, and some of them rest on guesses that may turn out to be wrong. A truth maintenance system keeps, for each conclusion, the reasons that support it. A reason can say "believe this if those things are believed" and also "believe this unless that other thing is believed". When a guess is withdrawn, the system finds every conclusion that rested on it and checks again whether some other reason still supports it. A conclusion that only supports itself in a circle is not believed. When reasons contradict each other in a circle, as in "believe A unless B" and "believe B unless A", the system leaves both open in place of picking one at random.

## The problem

A network $N$ is a finite set of nodes and justifications $(x, I, O)$, read as the rule

$$x \leftarrow b_1, \ldots, b_k, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_l$$

with in-list $I = \{b_1, \ldots, b_k\}$ and out-list $O = \{c_1, \ldots, c_l\}$. A *premise* has both lists empty; an *assumption* is a premise that the reasoner can retract. The network is a ground normal logic program. Its semantics here is the well-founded model $(T, F)$, the least fixed point of the operator $W(T, F) = (T_N(T, F), U_N(T, F))$, where $T_N$ gives the nodes with a justification whose in-list is in $T$ and whose out-list is in $F$, and $U_N$ is the greatest *unfounded set*: the largest set $U$ such that each justification of a node of $U$ has an in-node in $F \cup U$ or an out-node in $T$. The labels are IN for $T$, OUT for $F$ and UNDEC for the rest.

The task is incremental: keep the labels equal to the well-founded model while justifications are added and removed one at a time. For a network without a cycle through an out-list the model is two-valued and equals the unique stable model, and so the unique labelling in Doyle's sense. With even cycles through out-lists there can be several stable models, and with odd cycles there can be none; deciding whether a network has a stable model is NP-complete (Elkan 1990), while the well-founded model can be computed in polynomial time.

## The algorithm

After a justification of $x$ is added or removed, RELABEL$(x)$ runs. The affected set $S$ is $x$ and every node that depends on $x$, directly or through other nodes, through the in-list or the out-list of a justification. The labels outside $S$ stay as they are.

```pseudo id=main
RELABEL(x)
L1  S ← x and every node that depends on x through in-lists or out-lists, transitively
L2  remove the labels of the nodes of S
L3  repeat
L4      while some unlabeled node y of S has a justification whose in-list is all IN and whose out-list is all OUT do
L5          label y IN
L6      P ← the least set of nodes of S that are not OUT such that y ∈ P when y has a justification whose in-nodes are each IN, UNDEC or in P, and whose out-nodes are not IN
L7      label OUT each unlabeled node of S that is not in P
L8  until line L7 labels no node
L9  label UNDEC each node of S that is still unlabeled
```

Lines L4 and L5 are the step $T_N$: a node with a valid justification is IN. Lines L6 and L7 are the step $U_N$: $P$ holds the nodes that could still get a non-circular argument, and every unlabeled node outside $P$ is in an unfounded set, so it is OUT. A positive loop, such as $s \leftarrow s$, never enters $P$ and goes OUT. This is the [alternating fixpoint](/alternating-fixpoint/) of the well-founded semantics, run only on the affected nodes. A node with no justification is OUT from the start.

## Example

The network has the justifications $\mathit{flies} \leftarrow \mathit{bird}, \mathit{not}\ \mathit{abnormal}$ and $\mathit{abnormal} \leftarrow \mathit{penguin}$.

| change | affected set $S$ | rounds | labels after |
|---|---|---|---|
| assume $\mathit{bird}$ | bird, flies | bird IN by the premise; flies IN: bird is IN and abnormal is OUT | bird IN, flies IN, abnormal OUT, penguin OUT |
| assume $\mathit{penguin}$ | penguin, abnormal, flies | penguin IN, abnormal IN; flies has the out-node abnormal IN, so it is not in $P$ and goes OUT | penguin IN, abnormal IN, flies OUT |
| retract $\mathit{penguin}$ | penguin, abnormal, flies | round 1: no node gets IN; $P = \{\mathit{flies}\}$, so penguin and abnormal go OUT; round 2: flies IN | penguin OUT, abnormal OUT, flies IN |

Now add $p \leftarrow \mathit{not}\ q$ and $q \leftarrow \mathit{not}\ p$. Neither justification is valid while both nodes are unlabeled, and both nodes are in $P$, so both end UNDEC. The network has two stable models here, and Doyle's procedure would pick one of them. Assuming $q$ makes $q$ IN and then $p$ OUT.

## Correctness

The [correctness proof](proofs/correctness.md) has three parts. First, the nodes outside $S$ do not depend on the change, so by the splitting set theorem their old labels are still their well-founded labels. Second, each IN label is given by a justification whose nodes are already correctly IN and OUT, and each OUT label goes to a set that is unfounded for the current labels, so every label is a well-founded label (soundness). Third, when the loop stops, the IN and OUT sets form a fixed point of $W$, and since the well-founded model is the least fixed point and the labels lie below it, the two are equal.

## Complexity

The repeat loop runs at most $|S| + 1$ rounds, since each round but the last labels a node OUT. With a counter for each justification, as in [Horn-SAT forward chaining](/horn-sat-forward-chaining/), lines L4 to L7 cost $O(s)$ in each round. So one change costs $O(n\, s)$ in the worst case, and $O(|S| \cdot s_S)$ when only the affected part $S$, with justifications of total size $s_S$, is scanned. The implementation rescans the affected justifications without counters, for clarity. The space is $O(n + s)$ for the nodes, the justifications and the lists of dependents. The computation is polynomial because it does not choose between stable models; finding a two-valued labelling of the kind that Doyle's procedure looks for is NP-complete (Elkan 1990).

## Properties

- **Incremental.** Only the nodes that depend on the change are relabelled.
- **Well founded.** An IN node has a non-circular argument from the premises; a node that only supports itself is OUT.
- **Cautious.** Where the network leaves a choice, as in an even loop through out-lists, the labels say UNDEC. Doyle's labelling instead picks a stable model.
- **Order independent.** The labels depend only on the current network, not on the order of past changes.
- **Single context.** A JTMS holds one set of beliefs at a time. To compare different sets of assumptions, it must relabel each time; the [ATMS](/assumption-based-truth-maintenance/) keeps all contexts at once.

## Variants and improvements

- **Contradictions and dependency-directed backtracking.** A *contradiction node* marks a set of beliefs that cannot hold together. When it goes IN, Doyle's system traces its justifications back to the assumptions under it, records a *nogood*, and adds a justification that makes one of those assumptions OUT. This is smarter than [chronological backtracking](/chronological-backtracking/), which undoes the last choice whatever it was. This page describes it but does not implement it.
- **Monotonic JTMS.** With empty out-lists, labelling is [forward chaining](/forward-chaining/) on Horn clauses, and retraction is the removal of the nodes that lost all support, as in [incremental view maintenance](/incremental-view-maintenance/).
- **Stable labellings.** Doyle's procedure, and later TMS designs, choose a two-valued labelling on even loops; these labellings are the stable models of the network (Elkan 1990). See [stable model semantics](/stable-model-semantics/).
- **LTMS.** McAllester's logic-based TMS takes clauses in place of justifications and labels nodes by unit propagation.
- **ATMS.** The [assumption-based TMS](/assumption-based-truth-maintenance/) of de Kleer labels each node with the minimal sets of assumptions under which it holds.

## When to use it

Use a JTMS under a rule engine or a planner that makes assumptions and must withdraw them cheaply, when one set of beliefs is active at a time. It is the cache of a [production system](/production-system/) whose conclusions must disappear when their premises do. Use an ATMS when many alternative sets of assumptions must be compared at the same time, as in diagnosis.

## Pitfalls

- **Circular support.** A naive relabeller that keeps a node IN while some justification is valid can keep a self-supporting loop IN after its real support is gone. The unfounded step of lines L6 and L7 is what rules this out.
- **Odd loops.** A justification such as $r \leftarrow \mathit{not}\ r$ has no two-valued labelling, so a procedure that looks for one, as Doyle's does, cannot succeed on such a network. The well-founded labels give UNDEC.
- **Relabelling too much.** Relabelling the whole network after each change is correct but slow; the affected set must include the nodes that depend through out-lists too, or the labels go wrong.
- **Mixing up OUT and false.** OUT means "not believed now", not "believed false". A node and its negation are two separate nodes, tied together only by a contradiction node.

## Implementations

## History

Doyle (1979) introduced the truth maintenance system at MIT, with SL justifications that have in-lists and out-lists, the requirement of well-founded support, and dependency-directed backtracking from the work of Stallman and Sussman. McAllester gave the logic-based TMS around 1980, and de Kleer (1986) the assumption-based TMS. Elkan (1990) showed that the labellings of a nonmonotonic TMS are the stable models of the network read as a logic program, and that finding one is NP-complete. Forbus and de Kleer (1993) gave the standard textbook treatment.

## References
