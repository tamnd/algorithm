---
tag: 1VB5JR
kind: algorithm
slug: approximate-mms-allocation
name: Approximate maximin share allocation
aliases:
- Garg-Taki algorithm
- 3/4 MMS algorithm
area: algorithmic-game-theory/fair-division
level: research
summary: Gives every agent at least a constant fraction, such as 3/4, of its maximin share in polynomial time by reductions and bag filling.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of goods, T: the time of one maximin share computation}
  time: {worst: O(n^2 T + n m log m + n^2 (n + m))}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [maximin-share, approximation-ratio]
see_also: [mms-nonexistence-theorem, round-robin-allocation, envy-freeness-up-to-one-good, partition-problem, bin-packing, makespan-minimization, indivisible-goods-allocation]
sources:
  - paper: doi:10.1016/j.artint.2021.103547
    title: "Jugal Garg and Setareh Taki, An improved approximation algorithm for maximin shares, Artificial Intelligence 300 (2021), 103547"
    locator: Lemma 3.1 (valid reductions), the 3/4 + 1/(12n) existence result, and the strongly polynomial 3/4 algorithm
  - paper: "Hannaneh Akrami, Jugal Garg, Eklavya Sharma and Setareh Taki, Simplification and improvement of MMS approximation, IJCAI 2023 (arXiv:2303.16788)"
    locator: Definitions 1 to 5, Lemmas 1 to 5 (ordering, reductions and normalization), Algorithm 3 (bag filling), Lemmas 6 to 14, Theorem 1 (3/4 + min(1/36, 3/(16n - 4))) and Theorem 2 (tight example)
  - paper: "David Kurokawa, Ariel D. Procaccia and Junxing Wang, Fair enough: guaranteeing approximate maximin shares, Journal of the ACM 65(2) (2018), article 8"
    locator: the existence of 2/3-MMS allocations
  - paper: "Mohammad Ghodsi, Mohammad Taghi Hajiaghayi, Masoud Seddighin, Saeed Seddighin and Hadi Yami, Fair allocation of indivisible goods: improvements and generalizations, Proceedings of the 19th ACM Conference on Economics and Computation (EC 2018)"
    locator: the existence of 3/4-MMS allocations
  - paper: "Hannaneh Akrami and Jugal Garg, Breaking the 3/4 barrier for approximate maximin share, Proceedings of the 35th ACM-SIAM Symposium on Discrete Algorithms (SODA 2024)"
    locator: the existence of (3/4 + 3/3836)-MMS allocations
  - paper: "Heidari et al., arXiv:2510.10423 (2025), SODA 2026"
    locator: the existence of 10/13-MMS allocations
  - paper: "Uriel Feige, Ariel Sapir and Laliv Tauber, A tight negative example for MMS fair allocations, WINE 2021 (arXiv:2104.04977)"
    locator: the upper bounds 39/40 for three agents and 1 - 1/n^4 for n at least 4
  - paper: "Huang and Zhou, arXiv:2511.13056 (2025), preprint"
    locator: the claimed existence of 7/9-MMS allocations
  - paper: "Ezra and Garbuz, arXiv:2609.15085 (September 2026), preprint"
    locator: the claimed instance with four agents and eleven goods with no allocation better than 20/21-MMS
---

An approximate maximin share allocation gives every agent at least a fixed fraction $\alpha$ of its [maximin share](/maximin-share/) (MMS). Exact MMS allocations can fail to exist ([nonexistence of MMS allocations](/mms-nonexistence-theorem/)), so the goal is the largest $\alpha$ for which an $\alpha$-MMS allocation always exists, and an algorithm that finds one. This page gives the algorithm of Garg and Taki (2021) in the simplified form of Akrami, Garg, Sharma and Taki (2023): it sorts the instance, gives away a few large goods by fixed rules, scales the values so that every share is 1, and then fills $n$ bags with goods until each agent accepts one. It gives every agent $3/4$ of its share. The best published factor is $10/13 \approx 0.769$ (SODA 2026), and no factor above $39/40$ is possible.

## In plain words

Each person has a fair-share number: the value they could ensure by cutting the items into piles and taking the worst pile. We cannot always give everybody that much, so we aim for three quarters of it.

First, big items are handled. If one item, or a small fixed group of the largest items, already gives some person three quarters of their share, that person takes it and leaves. Taking big items away never hurts the others' shares.

After that, every item is small. Each remaining person scales their values so that their share is exactly 1. We prepare one bag per person, each with one large and one smaller item. Then we add items to a bag, one at a time, until some person says "this bag is worth three quarters to me" and leaves with it. The items never run out before everybody has a bag.

## The problem

There are $n$ agents and $m$ indivisible goods, with additive values $v_{ij} \ge 0$. For $n$ bundles, the maximin share of agent $i$ is $\mathrm{MMS}_i = \max_{(P_1, \dots, P_n)} \min_k v_i(P_k)$, the maximum over all partitions of the goods. The goal is an allocation $A$ with $v_i(A_i) \ge \frac{3}{4} \mathrm{MMS}_i$ for every agent.

Three tools reduce the instance.

- **Ordering.** An instance is *ordered* if one order of the goods sorts every agent's values in decreasing order. The ordered version of an instance gives position $q$ to every agent at the value of its $q$-th largest good. An $\alpha$-MMS allocation of the ordered version gives one of the original: go through the positions in increasing order, and let the owner of each position take its most valuable free good.
- **Reduction rules.** In an ordered instance with $k$ agents and goods $g_1, g_2, \dots$, let $S_1 = \{g_1\}$, $S_2 = \{g_k, g_{k+1}\}$, $S_3 = \{g_{2k-1}, g_{2k}, g_{2k+1}\}$ and $S_4 = \{g_1, g_{2k+1}\}$. Rule $R_r$ gives $S_r$ to an agent $i$ with $v_i(S_r) \ge \frac{3}{4} \mathrm{MMS}_i$. Removing the agent and $S_r$ does not lower the share of any other agent for $k - 1$ bundles (Garg and Taki, Lemma 3.1); for $R_4$ this needs $R_1$ and $R_3$ not to apply.
- **Normalization.** Agent $i$ takes an MMS partition $P$ and divides the value of each good in $P_j$ by $v_i(P_j)$. Every share becomes 1, and each new value is at most the old value divided by $\mathrm{MMS}_i$.

## The algorithm

```pseudo id=main
APPROX-MMS(v)                                  ▷ n agents, m goods, additive values v_ij ≥ 0
L1  w_i ← the values of agent i in decreasing order (the ordered instance)
L2  while some agent and some good remain do              ▷ k agents left, goods g_1, g_2, ... by rank
L3      MMS_i ← the maximin share of agent i for k bundles of the remaining goods
L4      find the first rule r in R1, R2, R3, R4 and the first agent i with w_i(S_r) ≥ (3/4) MMS_i
L5      if found then give S_r to i and remove i and S_r
L6      else exit the loop
L7  for each agent i left: u_i(g) ← w_i(g)/w_i(P_j) for every g in P_j, P an MMS partition of i
L8  u_i ← the normalized values in decreasing order (ordered again); k ← the number of agents left
L9  bags B_t ← {position t, position 2k + 1 - t} for t = 1, ..., k
L10 while some agent left has no bag do
L11     if some agent i without a bag has u_i(B) ≥ 3/4 for a free bag B then give B to i
L12     else add the next unused position to the first free bag
L13 give unused positions to one agent; map positions back to goods by picking, first with u, then with w
L14 return the allocation
```

Lines L1 to L6 shrink the instance until no rule applies. Lines L7 and L8 normalize and sort it again; sorting is needed because normalization can break the order. The bag of line L9 pairs the $t$-th largest position with the $(2k + 1 - t)$-th, so the bags start with similar values. When no rule applies, at least $2k$ goods remain, because an MMS partition with fewer goods would have a bundle of one good worth $\mathrm{MMS}_i$, and rule $R_1$ would apply (Akrami et al., Lemma 3). Line L12 adds the free goods in order of position. Line L13 undoes the two orderings with the picking step described above.

## Example

Agent 1 values each of ten goods at 1, and agent 2 values them at $3, 3, 2, 2, 2, 2, 1, 1, 1, 1$. Both lists are already sorted. The maximin shares for two bundles are 5 and 9, so the targets are $3.75$ and $6.75$.

1. **Rules.** $S_1 = \{g_1\}$ is worth 1 and 3, $S_2 = \{g_2, g_3\}$ is worth 2 and 5, $S_3 = \{g_3, g_4, g_5\}$ is worth 3 and 6, and $S_4 = \{g_1, g_5\}$ is worth 2 and 5. All are below the targets, so both agents go to bag filling.
2. **Normalization.** Agent 1 gets $1/5$ per good. Agent 2 has an MMS partition into two bundles worth 9, so its values become $3/9, 3/9, 2/9, \dots, 1/9$.
3. **Bags.** $B_1 = \{1, 4\}$ and $B_2 = \{2, 3\}$. Agent 1 values both at $2/5$ and agent 2 values both at $5/9$; nobody accepts.
4. **Filling.** Position 5 joins $B_1$. Agent 2 now values $B_1$ at $7/9 \ge 3/4$ and takes it. Positions 6 and 7 join $B_2$, and agent 1 values it at $4/5 \ge 3/4$ and takes it. The unused positions 8 to 10 go to agent 1.
5. **Mapping back.** Agent 2 gets goods $g_1, g_4, g_5$, worth 7, and agent 1 gets the other seven goods, worth 7.

Agent 2 gets $7 \ge 6.75$ but less than its share of 9; agent 1 gets $7 \ge 5$.

## Correctness

The output is $3/4$-MMS if each step keeps the guarantee and bag filling never runs out of goods. A rule gives agent $i$ value at least $\frac{3}{4}\mathrm{MMS}_i$ in the current instance, and the shares of the other agents do not drop (the validity of the rules). Normalization and the second sorting turn a bag worth $3/4$ under $u_i$ into a bundle worth $\frac{3}{4}\mathrm{MMS}_i$ under $w_i$. The picking step maps positions back to goods without loss, because at the $q$-th position at most $q - 1$ goods are gone, so the picker gets a good worth at least its $q$-th largest value. That bag filling never runs out is the core of the analysis; Akrami et al. split the agents into those who value every initial bag at most 1 (Lemma 8) and the others (Lemma 14), and show that each assigned bag takes little value from the agents still waiting. The full proof of the transfers, with the cited lemmas, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Line L1 sorts in $O(n m \log m)$ time. The loop of line L2 runs at most $n$ times, and each run computes up to $n$ maximin shares in line L3 and tests four rules in $O(n)$ time. Line L7 computes one MMS partition per agent left. So the run needs $O(n^2)$ maximin share computations, which cost $T$ each, and $O(n m \log m + n^2(n + m))$ other steps for the rules, the sorting, the bags and the picking. Computing a maximin share is NP-hard, so with exact shares this is not polynomial; Garg and Taki give a strongly polynomial version for $3/4$ that does not need exact shares (theorem). The implementation computes shares by branch and bound, which is fast for small instances.

## Properties

- **$3/4$-MMS for every agent**, for additive valuations (theorem).
- **Close to $3/4$ in the worst case.** Akrami et al. (Theorem 2 and Example 1) give an instance with identical valuations on which the output of the algorithm is at most $\frac{3n}{4n - 1}$-MMS. This tends to $3/4$ as $n$ grows, so the analysis is nearly tight.
- **No fairness between agents.** The output need not be [EF1](/envy-freeness-up-to-one-good/); the leftover goods of line L13 can go to anyone.
- **Deterministic** with the fixed orders of the pseudocode.

## Variants and improvements

The factor has risen over time (all theorems unless marked):

| factor | source |
|---|---|
| $2/3$ | Kurokawa, Procaccia and Wang (JACM 2018) |
| $3/4$ | Ghodsi et al. (EC 2018) |
| $3/4 + 1/(12n)$ | Garg and Taki (AI 2021) |
| $3/4 + \min(1/36, 3/(16n - 4))$ | Akrami, Garg, Sharma and Taki (IJCAI 2023), by adding dummy goods to rule $R_4$ |
| $3/4 + 3/3836$ | Akrami and Garg (SODA 2024) |
| $10/13$ | Heidari et al. (SODA 2026, arXiv:2510.10423) |
| $7/9$ | Huang and Zhou (arXiv:2511.13056), preprint |

Upper bounds: Feige, Sapir and Tauber (2021) give an instance with three agents and nine goods where no allocation is better than $39/40$-MMS, and instances with $1 - 1/n^4$ for $n \ge 4$ (theorems). A preprint by Ezra and Garbuz (arXiv:2609.15085, September 2026) gives $20/21$ with four agents and eleven goods.

## When to use it

Use it when a provable share for every agent matters more than comparisons between agents, for example when agents state values for many goods and each must be sure of a minimum. For small instances, an exact search may find a full MMS allocation; the algorithm is the fallback with a guarantee.

## Pitfalls

- **Skipping the second sort.** Line L8 must sort the normalized values again. Normalization by the MMS partition can make a later good worth more than an earlier one, and the bag analysis needs an ordered instance.
- **Applying rule $R_4$ too early.** Line L4 must try $R_1$ and $R_3$ before $R_4$. Rule $R_4$ is valid only when $R_1$ and $R_3$ do not apply; otherwise the shares of the other agents can drop.
- **Using the original shares after a reduction.** Line L3 must recompute each share for the remaining agents and goods, with $k$ bundles. The old shares are lower bounds only.
- **Filling with a factor above $3/4$.** With $\alpha > 3/4$ in lines L4 and L11, rule $R_4$ is no longer valid as stated, and Akrami et al. add a dummy good to repair it.
- **Mapping positions straight to goods.** Line L13 must let owners pick in the order of the positions; giving each agent the goods at its positions in the original numbering loses the guarantee.

## Implementations

## History

Kurokawa, Procaccia and Wang showed that MMS allocations need not exist and that $2/3$-MMS allocations do, and Ghodsi et al. reached $3/4$. Garg and Taki (2021) gave the simple algorithm of this page with the factor $3/4 + 1/(12n)$, and Akrami, Garg, Sharma and Taki (2023) simplified its analysis to the bag-filling lemmas used here.

## References
