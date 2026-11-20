---
tag: 4BQP88
kind: algorithm
slug: top-trading-cycles-and-chains
name: Top trading cycles and chains
aliases:
- TTCC
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Extends top trading cycles to kidney exchange with a deceased-donor waiting list by also trading along chains that end in the list. With a suitable chain rule it is efficient and strategyproof.
solves: [kidney-exchange-problem]
model: word-ram
complexity:
  vars: {n: the number of patient-donor pairs, L: the total length of the preference lists}
  time: {worst: O(n^2 + L)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2004
  people: [Alvin E. Roth, Tayfun Sonmez, M. Utku Unver]
  note: Roth, Sonmez and Unver proposed the mechanism in 2004 for kidney exchange with a link to the deceased-donor waiting list, and proved efficiency and strategyproofness for some chain selection rules.
prereqs: [top-trading-cycles, kidney-exchange-problem]
see_also: [top-trading-cycles, shapley-scarf-housing-market, kidney-exchange-cycle-formulation, roth-postlewaite-theorem, pareto-optimality, dominant-strategy-incentive-compatibility, individual-rationality, functional-graph]
sources:
  - paper: doi:10.1162/0033553041382157
    title: Alvin E. Roth, Tayfun Sonmez and M. Utku Unver, Kidney exchange, Quarterly Journal of Economics 119(2), 457 to 488 (2004)
    locator: the TTCC mechanism, the chain selection rules a to f, and Theorems 1 and 2 (efficiency for rules that keep the chains, strategyproofness for rules a, d, e and f)
  - paper: doi:10.1016/0304-4068(74)90033-0
    title: Lloyd Shapley and Herbert Scarf, On cores and indivisibility, Journal of Mathematical Economics 1(1), 23 to 37 (1974)
    locator: the housing market and the top trading cycle algorithm that TTCC extends
---

Top trading cycles and chains (TTCC) is a mechanism for kidney exchange. Each patient has a willing donor whose kidney does not fit, and the pair can trade with other pairs as in a [housing market](/shapley-scarf-housing-market/). In addition, a patient can accept the option $w$: high priority on the waiting list for a kidney from a deceased donor, in return for its donor giving a kidney to a patient on that list. Roth, Sonmez and Unver (2004) extended [top trading cycles](/top-trading-cycles/) to this setting. Cycles of pairs trade as before. When no cycle is left, the mechanism picks a $w$-chain: a path of pairs where each patient gets the next pair's kidney and the last patient gets $w$, and the kidney at the start of the chain goes to the waiting list. With chain rule e (pick the chain that starts at the pair of highest priority, and keep it), the result is Pareto efficient and strategyproof. A run with rounds takes $O(n^2 + L)$ time.

## In plain words

Each patient points either to the donor kidney it likes best among those still free, or to the waiting list. Kidneys point to their own patients. If there is a loop, its patients swap kidneys and leave, exactly as in top trading cycles. If there is no loop, every path of arrows ends at the waiting list. Pick one such path by a fixed rule. Each patient on it gets the kidney it points to, the last one goes to the top of the waiting list, and the donor at the start of the path gives to the waiting list. Repeat until every patient is served.

## The problem

There are $n$ pairs. Pair $i$ has patient $t_i$ and donor kidney $k_i$. Patient $t_i$ has a strict ranking of the kidneys and the option $w$. The list contains $k_i$, which stands for no exchange: the patient keeps its own donor and stays on the waiting list as before. Items after $k_i$ are never used. A fixed priority order of the pairs is given. The output gives each patient a kidney or $w$, with each kidney going to at most one patient, and also lists the kidneys that go to the deceased-donor waiting list.

## The algorithm

A pair is ACTIVE while its patient has no assignment, TAIL if its patient is assigned but its kidney is still free, and DONE when both are settled. A kidney is free while its pair is ACTIVE or TAIL.

```pseudo id=main
TTCC(lists, priority, keep)
L1  for each pair i do ptr[i] ← 1;  state[i] ← ACTIVE
L2  for each pair i do x[i] ← NIL
L3  while some pair is ACTIVE do
L4      for each ACTIVE pair i do move ptr[i] forward to the first free kidney or w;  target[i] ← that item
L5      if the arcs i → target[i] between ACTIVE pairs contain cycles then
L6          for each cycle, each pair i on it gets x[i] ← target[i] and becomes DONE
L7      else
L8          a ← the ACTIVE pair that comes first in priority
L9          follow targets from a through ACTIVE pairs: a = q1, q2, …, qm, until target[qm] is w or the kidney of a TAIL pair z
L10         for each ql, x[ql] ← target[ql];  q2, …, qm become DONE, and so does z if it exists
L11         if keep then a becomes TAIL else a becomes DONE and kidney a goes to the waiting list
L12 the kidneys of the TAIL pairs go to the waiting list;  return x
```

Line L5 looks for cycles in a [functional graph](/functional-graph/) in which some arcs leave the ACTIVE pairs: arcs to $w$ and arcs to the free kidneys of TAIL pairs. When there is no cycle, every path from an ACTIVE pair leaves the ACTIVE pairs, so line L9 stops. The path $q_1, \dots, q_m$ with the tail kidney $k_a$ is the $w$-chain that starts at pair $a$. With $\text{keep}$ true, this is chain rule e of Roth, Sonmez and Unver: the kidney $k_a$ stays free, so later patients can still get it. With $\text{keep}$ false it is rule d: the chain is removed, and $k_a$ goes to the waiting list at once.

## Example

Five pairs with priority 1, 2, 3, 4, 5. Patient 1 ranks $k_2 \succ k_1$, patient 2 ranks $k_1 \succ k_2$, patient 3 ranks $k_1 \succ w \succ k_3$, patient 4 ranks $k_3 \succ k_4$, and patient 5 ranks $k_3 \succ k_4 \succ w \succ k_5$.

With rule e:

| round | targets of the ACTIVE pairs | action |
|---|---|---|
| 1 | 1 → $k_2$, 2 → $k_1$, 3 → $k_1$, 4 → $k_3$, 5 → $k_3$ | cycle 1, 2: patients 1 and 2 swap |
| 2 | 3 → $w$, 4 → $k_3$, 5 → $k_3$ | no cycle; chain from pair 3: patient 3 gets $w$, pair 3 becomes TAIL |
| 3 | 4 → $k_3$, 5 → $k_3$ | no cycle; chain from pair 4: patient 4 gets $k_3$, pair 3 is DONE, pair 4 becomes TAIL |
| 4 | 5 → $k_4$ | no cycle; chain from pair 5: patient 5 gets $k_4$, pair 4 is DONE, pair 5 becomes TAIL |

At the end $k_5$ goes to the waiting list. Four patients get a living donor kidney, patient 3 gets $w$, and the waiting list gets $k_5$.

With rule d, round 2 removes the chain of pair 3, so $k_3$ goes to the waiting list at once. In round 3 patient 4 points to its own kidney, a cycle of length one, so it gets no exchange. Then patient 5 finds $k_3$ and $k_4$ gone and gets $w$, and $k_5$ goes to the waiting list. Only two patients get a living donor kidney. The tests check both runs.

**Edge cases.** A single pair whose patient prefers $w$ gets $w$, and its kidney goes to the waiting list. If no patient ranks $w$ above its own kidney, no chain ever forms and TTCC is top trading cycles.

## Correctness

The output is feasible: line L4 only points to free kidneys, line L6 gives each cycle the kidneys of the cycle, and line L10 gives each patient of the chain the kidney of the next pair or the kidney of a TAIL pair, which then becomes DONE. Each kidney goes to one patient or to the waiting list, and the number of patients with $w$ equals the number of kidneys given to the list. The result is individually rational, since a patient never points past its own kidney, which stays free while its pair is ACTIVE.

Roth, Sonmez and Unver (2004) proved two properties. If every chain selected before the last round stays in the procedure, so that its tail kidney remains free, the result is Pareto efficient (their Theorem 1); rule e is such a rule. With rules a, d, e and f, truth-telling is a dominant strategy for each patient (their Theorem 2). Rule d is strategyproof but not efficient. Let patient 1 rank only $k_1$, patient 2 rank $w \succ k_2$, and patient 3 rank $k_2 \succ k_3$. Rule d sends $k_2$ to the waiting list with the chain of pair 2, and patient 3 keeps $k_3$. Rule e keeps $k_2$ free and gives it to patient 3, which is better for patient 3 and the same for the others.

The proof file shows that the algorithm terminates and returns a feasible, individually rational outcome, and that it follows the TTCC procedure with the chosen rule.

## Complexity

The model is the [word RAM](/word-ram/). Each round makes at least one ACTIVE pair TAIL or DONE, and no pair becomes ACTIVE again, so there are at most $n$ rounds. In a round, line L4 costs $O(n)$ besides pointer moves, the cycle search of line L5 visits each ACTIVE pair once, in $O(n)$ time, and lines L8 to L11 cost $O(n)$. A kidney that is not free never becomes free again, so the pointers only move forward, at most $L$ steps in total. The total time is $O(n^2 + L)$ and the extra space is $O(n)$.

## Properties

- **Individually rational.** No patient gets an item it ranks below its own donor's kidney.
- **Pareto efficient with rule e**, and with every rule that keeps the selected chains until the last round (Theorem 1 of the 2004 paper).
- **Strategyproof with rules a, d, e and f** (Theorem 2). The theorem does not cover rules b and c, which pick the longest chain.
- **Top trading cycles as a special case.** If no patient ranks $w$ above its own kidney, every round removes cycles only, and the result is the [top trading cycles](/top-trading-cycles/) allocation.
- **Cycles can be long.** As in top trading cycles, nothing bounds the length of a cycle or a chain.

## Variants and improvements

- **Chain selection rules.** Rule a removes minimal chains one at a time, rules b and c take the longest chain and remove or keep it, rules d and e take the chain from the pair of highest priority and remove or keep it, and rule f is a priority rule that also takes blood types into account.
- **Bounded cycles.** Clinics need short cycles, because all operations of a cycle take place at the same time. The optimization version with a length bound is the [kidney exchange problem](/kidney-exchange-problem/), solved in practice by the [cycle formulation](/kidney-exchange-cycle-formulation/).
- **Pairwise exchange.** If only swaps of two pairs are allowed and patients are indifferent among compatible kidneys, maximum matching gives an efficient outcome; Roth, Sonmez and Unver studied this case in 2005.

## When to use it

Use TTCC as a model for kidney exchange with a connection to the deceased-donor list, where strategyproofness and efficiency for the patients are the goals, and where the lengths of cycles and chains are not a concern. In practice the length limit dominates, and clinics use integer programming on the [kidney exchange problem](/kidney-exchange-problem/) instead.

## Pitfalls

- **Removing chains too early.** With rule d the tail kidney leaves at once, and patients that would want it later lose it; this is why rule d is not efficient.
- **Looking for chains while cycles exist.** The procedure removes all cycles first. Picking a chain while a cycle exists can change the result and break the theorems.
- **Forgetting the tail kidney.** With rule e the tail pair's patient is served, but its kidney is still free. It must go to the waiting list at the end, or the donor is lost.
- **Using it with a length bound.** Cutting cycles and chains after the fact loses efficiency and strategyproofness.

## Implementations

The Python version takes the lists as lists of kidney indices with $-1$ for $w$, each containing the own kidney, an optional priority order and a flag for rule e or rule d. It returns the item of each patient and the kidneys that go to the waiting list. The tests check the example, the inefficiency of rule d, feasibility and individual rationality on random cases, efficiency of rule e against a brute force search over all outcomes, strategyproofness for both rules over all false lists of three pairs, and agreement with top trading cycles when no patient lists $w$ before its own kidney.

## History

Before 2004, kidney exchange was done in small numbers, mostly as swaps between two incompatible pairs and as exchanges with the waiting list. Roth, Sonmez and Unver (2004) modelled kidney exchange as a housing market with an extra option, introduced TTCC with six chain selection rules, and proved efficiency and strategyproofness for some of them. Their later work on pairwise and short exchanges led to the clearinghouses that now use bounded cycles and chains.

## References
