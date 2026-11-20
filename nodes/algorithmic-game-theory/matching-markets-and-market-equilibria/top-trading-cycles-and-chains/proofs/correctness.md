---
title: TTCC terminates and returns a feasible, individually rational outcome of the TTCC procedure
proves: [correctness, termination]
status: full
---

Pair $i$ has patient $t_i$ and kidney $k_i$, for $i = 1, \dots, n$. Each list ranks kidneys and $w$ strictly and contains $k_i$. A kidney is *free* while its pair is ACTIVE or TAIL. An *outcome* gives each patient a kidney or $w$, with each kidney given to at most one patient; together with it the algorithm returns the set $K_w$ of kidneys that go to the waiting list.

We prove that the algorithm stops, that it carries out the TTCC procedure of Roth, Sonmez and Unver with chain rule e (if keep is true) or d (if keep is false), and that its outcome is feasible and individually rational. The efficiency of rule e and the strategyproofness of rules d and e are the theorems of Roth, Sonmez and Unver (2004); we cite them and do not prove them here.

**Claim 1 (free kidneys only shrink, and pointers stay in range).** A pair never becomes ACTIVE again after it stops being ACTIVE, and a DONE pair never changes state. So a kidney that is not free never becomes free again. While pair $i$ is ACTIVE, its own kidney $k_i$ is free, so the scan of line L4 stops at or before $k_i$, at the first free kidney or $w$ on the list. This is the best free item of $t_i$. *Proof.* The only state changes are ACTIVE to DONE (lines L6 and L10), ACTIVE to TAIL or DONE (line L11), and TAIL to DONE (line L10). Entries before $\text{ptr}[i]$ were skipped because their kidneys were not free, and they stay not free. $\square$

**Claim 2 (the arcs of a round).** In a round, each ACTIVE pair $i$ has one arc, to the pair that owns $\text{target}[i]$, or to $w$. If the target is a kidney, its pair is ACTIVE or TAIL, by Claim 1. Restricted to the ACTIVE pairs, this is a functional graph in which some arcs leave the set: to $w$ or to TAIL pairs. The cycles of line L5 are exactly the cycles of this graph, and they are the cycles of the TTCC procedure in this round. *Proof.* The search of line L5 follows each arc from each ACTIVE pair that it has not yet seen, colouring the pairs of the current walk. It stops at $w$, at a TAIL pair, or at a pair that has a colour. If that pair is on the current walk, the end of the walk from it is a cycle, and every cycle is found this way when the search first enters it. $\square$

**Claim 3 (chains).** If line L5 finds no cycle, the walk of line L9 from $a$ visits distinct ACTIVE pairs and stops at a pair $q_m$ whose target is $w$ or the kidney of a TAIL pair. The sequence $k_a, t_a = t_{q_1}, k_{q_2}, t_{q_2}, \dots, t_{q_m}$, followed by $w$ or by the TAIL kidney, is the $w$-chain that starts at pair $a$. *Proof.* A repeated ACTIVE pair would close a cycle among the ACTIVE pairs, which line L5 did not find, so the walk visits distinct pairs and stops after at most $n$ steps. It can only stop where line L9 says. With a TAIL pair $z$ at the end, its patient already has its item and its free kidney is the end of an earlier kept chain, so the new chain continues the earlier one, which ends in $w$, as in the procedure with kept chains. Line L8 picks the ACTIVE pair of highest priority, which is the chain choice of rules d and e. $\square$

**Termination.** Every round either removes at least one cycle (line L6) or changes at least the pair $a$ from ACTIVE to TAIL or DONE (line L11). By Claim 1 no pair becomes ACTIVE again, so there are at most $n$ rounds, and each round is finite by Claims 1 and 3.

**Feasibility.** We show that each kidney ends up given to exactly one patient or in $K_w$.

- In line L6, the patients of a cycle get the kidneys of the next pairs on the cycle. These kidneys are free and belong to the cycle itself, and all pairs of the cycle become DONE, so no later round uses them.
- In line L10, patient $q_l$ gets the kidney of $q_{l+1}$ for $l < m$, and these pairs become DONE. If the chain ends at a TAIL pair $z$, patient $q_m$ gets $k_z$, which was free, and $z$ becomes DONE. If it ends at $w$, patient $q_m$ gets $w$. Kidney $k_a$ is not given in this round: with rule d it goes to $K_w$ and $a$ is DONE, and with rule e pair $a$ becomes TAIL and $k_a$ stays free.
- Line L12 puts the kidneys of the remaining TAIL pairs into $K_w$.

Every pair passes through these lines, since at the end no pair is ACTIVE. Only free kidneys are ever given, and a kidney stops being free when it is given or sent to $K_w$, so no kidney is used twice. A TAIL kidney is either given in a later chain (and its pair becomes DONE) or sent to $K_w$ in line L12. So every kidney is given exactly once. Each chain that ends at $w$ gives $w$ to one patient and creates one tail kidney that eventually goes to a patient or to $K_w$; a chain that ends at a TAIL pair gives $w$ to nobody, uses the old tail kidney and creates one new tail kidney. Counting, the number of patients with $w$ equals $|K_w|$.

**Individual rationality.** Each patient $t_i$ gets $\text{target}[i]$ from the round in which pair $i$ stops being ACTIVE. By Claim 1 this is its best free item at that time, which is at least as good as $k_i$, because $k_i$ is still free then.

**Agreement with top trading cycles.** If no list has $w$ before the own kidney, no target is ever $w$ (Claim 1), and no pair ever becomes TAIL, since that needs a chain, which needs an arc to $w$ or to a TAIL pair. So every round has a cycle, and line L6 removes the cycles of the pointer graph of the remaining pairs, which is the round version of top trading cycles. $\blacksquare$

**Cost.** By termination there are at most $n$ rounds. In a round, line L4 costs $O(n)$ plus the pointer moves, line L5 visits each ACTIVE pair once ($O(n)$, plus the cost of cutting the cycle out of the walk, which is at most the length of the walk), and lines L8 to L11 cost $O(n)$. By Claim 1 each pointer moves only forward inside its list, so all pointer moves together cost $O(L)$. The total time is $O(n^2 + L)$ and the extra space is $O(n)$.
