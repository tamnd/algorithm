---
tag: HCYFF2
kind: algorithm
slug: ef1-and-pareto-optimal-algorithm
name: Barman-Krishnamurthy-Vaish algorithm
aliases:
- EF1 and Pareto optimal allocation algorithm
area: algorithmic-game-theory/fair-division
level: research
summary: Finds an EF1 and Pareto optimal allocation of indivisible goods in pseudo-polynomial time by running a market with price rises.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of goods, V: "the largest value v_max (an integer)"}
  time: {worst: "poly(n, m, V)"}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness-up-to-one-good, pareto-optimality, pseudo-polynomial-time]
see_also: [fisher-market, competitive-equilibrium, first-welfare-theorem, unreasonable-fairness-of-mnw, maximum-nash-welfare, breadth-first-search, round-robin-allocation, dpsv-algorithm]
sources:
  - paper: "Siddharth Barman, Sanath Kumar Krishnamurthy and Rohit Vaish, Finding fair and efficient allocations, Proceedings of the 19th ACM Conference on Economics and Computation (EC 2018), 557-574 (arXiv:1707.04731)"
    locator: Section 4 (hierarchy, violators and path-violators, Algorithm 1 with its three phases), Lemma 2 (pEF1 with MBB gives EF1), Lemmas 3 to 5, Theorems 1 to 3 and Remarks 1 and 2
  - paper: "Ryoga Mahara, A polynomial-time algorithm for fair and efficient allocation with a fixed number of agents, arXiv:2411.01810 (November 2024)"
    locator: abstract (the open problem of polynomial time, and the algorithm for a fixed number of agents)
---

The Barman-Krishnamurthy-Vaish (BKV) algorithm finds an allocation of indivisible goods that is both [envy-free up to one good](/envy-freeness-up-to-one-good/) (EF1) and [Pareto optimal](/pareto-optimality/) (PO), for additive valuations, in time polynomial in $n$, $m$ and the largest value $v_{\max}$. It treats the goods as a [Fisher market](/fisher-market/): goods have prices, every agent holds only goods of maximum value per unit of price, so the allocation is efficient by the [first welfare theorem](/first-welfare-theorem/), and the algorithm moves goods and raises prices until the spending of the agents is balanced up to one good. [Maximum Nash welfare](/maximum-nash-welfare/) also gives EF1 and PO ([the unreasonable fairness of MNW](/unreasonable-fairness-of-mnw/)), but it is NP-hard to compute; BKV reaches the same two properties in [pseudo-polynomial time](/pseudo-polynomial-time/). Barman, Krishnamurthy and Vaish presented it at EC 2018. Whether EF1 and PO can be reached in polynomial time is open (open problem, Mahara, November 2024).

## In plain words

Put a price tag on every item. Each person looks at the value they get for each unit of money and only keeps items that are the best deal for them. When everybody holds only best deals, no trade can help someone without hurting someone else.

Now look at the money each person has spent on their items. If someone spent far more than the poorest person, even after ignoring their most expensive item, things are unfair. Then either an item moves from a rich person to a poorer person who also sees it as a best deal, or, when no such move is possible, the prices of the items held by the poorer group go up. Higher prices make other items better deals for that group, which opens new moves. When spending is balanced up to one item, the values are balanced up to one item too.

## The problem

There are $n$ agents and $m$ indivisible goods, with additive values $v_{ij} \ge 0$. The goal is an allocation $x = (x_1, \dots, x_n)$ of all goods that is EF1 and PO.

**Market terms.** Prices $p_j > 0$ are attached to the goods, and $p(S) = \sum_{j \in S} p_j$ is the *spending* on a set $S$. The bang per buck of agent $i$ for good $j$ is $v_{ij}/p_j$, its largest value is the MBB ratio $\beta_i = \max_j v_{ij}/p_j$, and the goods that reach it form the MBB set of $i$. An allocation satisfies the *MBB condition* if every agent owns only goods of its MBB set. A *least spender* is an agent of smallest spending $p_{\min} = \min_i p(x_i)$. The allocation is **price-EF1** (pEF1) if for all agents $i, k$ with $x_k \ne \emptyset$ some $j \in x_k$ has $p(x_i) \ge p(x_k \setminus \{j\})$; equivalently, $p(x_k) - \max_{j \in x_k} p_j \le p_{\min}$ for every agent $k$.

**Hierarchy.** Start from the least spenders at level 0. An agent $h$ at level $\ell$ adds to level $\ell + 1$ every agent not seen yet that owns an MBB good of $h$. This is a [breadth-first search](/breadth-first-search/) along MBB edges (from an agent to a good) and allocation edges (from a good to its owner). A *path violator* is an agent $h$ at level $\ell \ge 1$ with a good $j \in x_h$ that is an MBB good of some agent $g$ at level $\ell - 1$, such that $p(x_h \setminus \{j\}) > p_{\min}$.

## The algorithm

The page gives the exact form of the algorithm, with no rounding, and with all least spenders at level 0; the paper's form is described after the walk-through.

```pseudo id=main
BKV-EXACT(v)                                   ▷ n agents, m goods, values v_ij > 0
L1  give each good j to an agent k of largest v_kj, and set p_j ← v_kj
L2  loop
L3      if x is pEF1 for p then exit the loop
L4      H ← the hierarchy of the least spenders (levels by BFS)
L5      look for a path violator h with its good j and a parent g one level above
L6      if one is found then give j to g, and go back to line L3
L7      α1 ← min over h ∈ H and goods j owned outside H of β_h p_j / v_hj
L8      α2 ← max over agents k ∉ H of (p(x_k) - max_{j ∈ x_k} p_j) / p_min
L9      α3 ← min over agents k ∉ H of p(x_k) / p_min
L10     α ← min(α1, α2, α3); multiply the price of every good owned in H by α
L11     if α = α2 then exit the loop
L12 return x
```

Line L1 is Phase 1 of the paper: each good goes to an agent that values it most, at a price equal to that value, so every owner gets bang per buck 1 from its goods and nobody gets more from any good. Lines L4 to L6 are Phase 2: a swap moves a good one level down the hierarchy, toward the least spenders, along an MBB edge, so the MBB condition stays true. Lines L7 to L10 are Phase 3: the prices of all goods held inside $H$ rise by the same factor. The three bounds stop the rise at the first event: at $\alpha_1$ a good outside $H$ becomes an MBB good of an agent in $H$, so $H$ grows; at $\alpha_2$ the least spenders have caught up with every agent outside $H$, up to one good; at $\alpha_3$ an agent outside $H$ becomes a least spender.

**The paper's version.** Barman, Krishnamurthy and Vaish run the same three phases with a parameter $\varepsilon > 0$ on a rounded instance, whose positive values are rounded up to integer powers of $1 + \varepsilon$, and test $\varepsilon$-versions of the violator conditions. They show that the run takes $\mathrm{poly}(m, n, 1/\varepsilon, \ln v_{\max})$ time (Lemma 4) and returns a $3\varepsilon$-EF1 and fractionally PO allocation of the rounded instance (Lemma 3). For $\varepsilon = 1/(14 m^3 v_{\max}^4)$, this allocation is EF1 and PO for the original integer values (Lemma 5 and Theorem 1). The paper also handles zero values and a single least spender chosen by a fixed order.

## Example

Three agents value four goods $a, b, c, d$:

| | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| agent 1 | 5 | 8 | 1 | 6 |
| agent 2 | 3 | 1 | 2 | 2 |
| agent 3 | 1 | 5 | 4 | 4 |

1. **Line L1.** Agent 1 gets $a, b, d$ and agent 3 gets $c$, at prices $(5, 8, 4, 6)$. Spending is 19, 0 and 4. Agent 1 spends $19 - 8 = 11 > 0$ without its most expensive good, so the allocation is not pEF1.
2. **Swap.** The least spender is agent 2. Its MBB ratio is $3/5$, reached by $a$, which agent 1 owns, so agent 1 is at level 1. Since $p(\{b, d\}) = 14 > 0$, agent 1 is a path violator, and $a$ moves to agent 2. Spending is now 14, 5 and 4.
3. **Price rise.** The least spender is agent 3, with $p_{\min} = 4$; its only MBB good is its own $c$, so $H = \{3\}$. Then $\alpha_1 = \min(5/1, 8/5, 6/4) = 3/2$, $\alpha_2 = \max(6/4, 0/4) = 3/2$ and $\alpha_3 = \min(14, 5)/4 = 5/4$. The price of $c$ rises by $5/4$ to 5.
4. **Price rise.** Agents 2 and 3 both spend 5 and form level 0, each holding only its own MBB good. Now $\alpha_1 = 6/5$ (agent 3 and good $d$: $(4/5) \cdot 6/4$), $\alpha_2 = (14 - 8)/5 = 6/5$ and $\alpha_3 = 14/5$. The prices of $a$ and $c$ rise to 6, and since $\alpha = \alpha_2$ the loop ends.

The output is $x_1 = \{b, d\}$, $x_2 = \{a\}$, $x_3 = \{c\}$ with prices $(6, 8, 6, 6)$ and values 14, 3 and 4. It is pEF1: $14 - 8 \le 6$. Agent 3 values $\{b, d\}$ at 9 but without $b$ at $4$, its own value, so it is EF1; and it is PO.

## Correctness

Three facts hold whenever the algorithm returns. First, the MBB condition holds at every step: line L1 makes it true, a swap moves a good to an agent for which it is an MBB good, and the bound $\alpha \le \alpha_1$ keeps the MBB goods of agents in $H$ ahead of goods outside $H$, while agents outside $H$ own only goods whose prices do not change. Second, the output is pEF1: either line L3 saw it, or the rise stopped at $\alpha_2$ and the least spenders, which are inside $H$ because $\alpha \le \alpha_3$, now spend at least as much as every agent's spending minus its most expensive good. Third, pEF1 with the MBB condition gives EF1, because agent $i$ values any set $S$ at most $\beta_i p(S)$ and its own bundle at exactly $\beta_i p(x_i)$ (Lemma 2 of the paper). The MBB condition also gives PO by the first welfare theorem: an allocation that some agent prefers and nobody likes less would cost more than the total price of all goods. The full proof of these facts is in [proofs/correctness.md](proofs/correctness.md). That the exact form ends is not proved; the paper proves termination for its rounded form.

## Complexity

One step, a swap or a price rise, costs $O(n m)$ time: the MBB sets, the BFS of line L4 and the three bounds each read the value table once. The paper bounds the number of steps for the rounded form by $\mathrm{poly}(m, n, 1/\varepsilon, \ln v_{\max})$, and its choice of $\varepsilon$ makes the whole run pseudo-polynomial, $\mathrm{poly}(n, m, v_{\max})$ (Theorem 1). When values are bounded by a polynomial in $n$ and $m$, this is polynomial time (Remark 1). With exact rational arithmetic, as in the exact form, the bit length of the prices also matters. On 2000 random instances with 2 to 5 agents, 2 to 10 goods and integer values from 1 to 30, the exact form ended after at most 18 swaps and rises (measurement).

## Properties

- **EF1 and PO**, and in fact fractionally PO: no fractional allocation is better for some agent and worse for none (Theorem 2 of the paper states that EF1 and fPO allocations always exist).
- **Market equilibrium.** The output with its prices is an equilibrium of a Fisher market in which each agent's budget is its final spending.
- **Approximate Nash welfare.** A version of the same algorithm gives an $e^{1/e} \approx 1.45$ approximation of the maximum Nash welfare (Theorem 3).
- **Approximate inputs run fast.** For $\varepsilon$-EF1 and $\varepsilon$-PO, the time is $\mathrm{poly}(m, n, 1/\varepsilon, \ln v_{\max})$ (Remark 2).
- **Deterministic.** Ties are broken by index.

## Variants and improvements

- **Fixed number of agents.** Mahara (2024) gives a polynomial-time algorithm for EF1 and fPO when $n$ is fixed, by adding agents one at a time.
- **Maximum Nash welfare.** For small instances, an exact MNW allocation, for example from a mixed integer program, also gives EF1 and PO.
- **Divisible goods.** For divisible goods, the market equilibrium with equal budgets, computed for example by the [DPSV algorithm](/dpsv-algorithm/), is envy-free and PO.

## When to use it

Use it when valuations are additive with small integer values, for example points that each agent spreads over the goods, and both EF1 and Pareto optimality are needed with a proof. For large instances where only EF1 is needed, [round-robin allocation](/round-robin-allocation/) is simpler. When the Nash welfare itself matters, compute MNW directly if the instance is small.

## Pitfalls

- **A single least spender with ties in the exact form.** If line L4 starts the hierarchy from only one least spender when several exist, then $\alpha_3 = 1$ for a tied agent outside $H$, the rise of line L10 changes nothing, and the loop can stall. Starting from all least spenders, as here, avoids this; the paper avoids it by its order on agents and its $\varepsilon$ margins.
- **Breaking on $\alpha_1$ or $\alpha_3$.** Line L11 may stop only when the rise reached $\alpha_2$. A rise that stopped at $\alpha_1$ or $\alpha_3$ has not balanced the spending, and the output need not be pEF1.
- **Raising prices of goods outside $H$.** Line L10 must scale exactly the goods owned by agents of $H$. Scaling more breaks the MBB condition of agents outside $H$; scaling less breaks it inside $H$.
- **Swapping across a level.** In line L5 the good must go from a level-$\ell$ agent to an agent at level $\ell - 1$ for which it is an MBB good. Moving a good to an agent that does not see it as an MBB good destroys the MBB condition and with it Pareto optimality.

## Implementations

## History

Barman, Krishnamurthy and Vaish presented the algorithm at EC 2018 (arXiv 2017). They write that establishing its running time is an intricate task, which their analysis does for the rounded instance. Before it, the only general route to EF1 and PO was maximum Nash welfare, from Caragiannis et al. (EC 2016), which is NP-hard to compute.

## References
