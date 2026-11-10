---
tag: RRVVVX
kind: algorithm
slug: online-threshold-knapsack
name: Threshold algorithm for online knapsack
aliases:
- threshold policy
- ZCL threshold algorithm
- online knapsack with bounded value densities
area: online-and-streaming/competitive-analysis
level: advanced
summary: Takes an arriving item when its value density is at least a threshold that rises exponentially with the used capacity; for small items with densities in [L, U] it is (1 + ln(U/L))-competitive.
solves: [online-knapsack-problem]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2008
  people: [Yunhong Zhou, Deeparnab Chakrabarty, Rajan Lukose]
  note: Zhou, Chakrabarty and Lukose gave the exponential threshold and the matching lower bound for online knapsack with bounded densities and small items, as a model of bidding under a budget in keyword auctions.
prereqs: [online-knapsack-problem, competitive-ratio, fractional-knapsack]
see_also: [knapsack-problem, greedy-fractional-knapsack, online-adwords-problem, balance-algorithm, online-primal-dual, ski-rental-problem, secretary-problem, oblivious-adversary]
sources:
  - paper: "Yunhong Zhou, Deeparnab Chakrabarty and Rajan Lukose, Budget constrained bidding in keyword auctions and online knapsack problems, Internet and Network Economics (WINE 2008), LNCS 5385, Springer, 566-576"
    title: Budget constrained bidding in keyword auctions and online knapsack problems
    locator: Section 2 (the threshold function, the upper bound ln(U/L) + 1 in Theorem 2.1 and the lower bound in Theorem 2.2)
  - paper: doi:10.1145/1367497.1367747
    title: "Yunhong Zhou, Deeparnab Chakrabarty and Rajan Lukose, Budget constrained bidding in keyword auctions and online knapsack problems, Proceedings of the 17th International World Wide Web Conference (WWW 2008), poster"
    locator: the short version, with the threshold algorithm and its ratio
---

The threshold algorithm of Zhou, Chakrabarty and Lukose is an online algorithm for the [online knapsack problem](/online-knapsack-problem/) under two assumptions: the value density of each item, its value divided by its weight, lies in a known range $[L, U]$, and each item is small compared with the capacity. It takes an item when its density is at least $\Psi(z)$ and it fits, where $z$ is the used fraction of the capacity. The threshold $\Psi$ stays at $L$ until a fraction $c = 1/(1 + \ln(U/L))$ is used, and then rises exponentially to $U$ at a full knapsack. The algorithm is $(1 + \ln(U/L))$-competitive in the limit of small items, and no online algorithm, deterministic or randomized, does better. Without such assumptions no online algorithm has a bounded ratio.

## In plain words

A buyer has a fixed budget and sees offers one at a time. Each offer has a price and a worth, and the buyer must say yes or no at once. The worth per unit of price is always between a known low and a known high.

At the start the buyer takes any offer, because an empty budget at the end is the worst outcome. After a set part of the budget is spent, the buyer gets choosier: the lowest acceptable worth per unit rises with the money spent, faster and faster, and it reaches the known high value when the budget is gone. This rule never collects less than a fixed share of the best possible worth. The share depends only on how far apart the low and the high are.

## The problem

The capacity is 1. Items arrive one at a time; item $i$ has weight $w_i \in (0, 1]$ and value $v_i$, with density $e_i = v_i / w_i \in [L, U]$, where $0 < L \le U$ are known. Each item must be taken or refused at its arrival, for good, and the taken items must have total weight at most 1. The goal is a large total value. $\mathrm{OPT}$ is the largest value of a set of items that fits. The ratio is $\mathrm{OPT} \le \rho \cdot \mathrm{ALG}$ with no additive term; in the convention $\mathrm{ALG} \ge c \cdot \mathrm{OPT}$ of the other maximization pages, $c = 1/\rho$. The small items assumption is that each $w_i \le \varepsilon$ for a small $\varepsilon$; the bound is stated for $\varepsilon \le 1 - c$ and becomes exact as $\varepsilon \to 0$.

## The algorithm

$z$ is the used fraction of the capacity, and $S$ is the set of taken items.

```pseudo id=main
ONLINE-THRESHOLD-KNAPSACK(L, U, σ)             ▷ σ = items (w_i, v_i), revealed one at a time
L1  c ← 1 / (1 + ln(U/L));  z ← 0;  S ← ∅
L2  for each arriving item i do
L3      Ψ ← L if z ≤ c, else (Ue/L)^z · L/e
L4      if v_i / w_i ≥ Ψ and z + w_i ≤ 1 then
L5          S ← S ∪ {i};  z ← z + w_i
L6  return S
```

The two forms of L3 agree at $z = c$, because $(Ue/L)^c = e$, so $\Psi$ is continuous, with $\Psi(c) = L$ and $\Psi(1) = U$. The constant $c$ and the base $Ue/L$ are chosen so that the area under $\Psi$ from 0 to $z$ is exactly $c\,\Psi(z)$ for each $z \ge c$; this identity is the whole proof. If $U = L$, then $c = 1$ and the algorithm takes each item that fits.

## Example

Take $L = 1$ and $U = 10$, so $c = 1/(1 + \ln 10) = 0.3028$ and the ratio is $1 + \ln 10 = 3.3026$. Fourteen items of weight $0.1$ arrive with the densities in the table.

| item | density | $z$ before | $\Psi(z)$ | decision |
|---|---|---|---|---|
| 1 to 3 | 1, 1, 1 | 0, 0.1, 0.2 | 1 | take |
| 4 | 2 | 0.3 | 1 | take |
| 5 | 1.5 | 0.4 | 1.3786 | take |
| 6 | 5 | 0.5 | 1.9180 | take |
| 7 | 1.2 | 0.6 | 2.6686 | refuse (density) |
| 8 | 3 | 0.6 | 2.6686 | take |
| 9 | 8 | 0.7 | 3.7129 | take |
| 10 | 10 | 0.8 | 5.1658 | take |
| 11 | 2.5 | 0.9 | 7.1874 | refuse (density) |
| 12 | 9 | 0.9 | 7.1874 | take |
| 13, 14 | 10, 10 | 1.0 | 10 | refuse (no room) |

The algorithm collects $0.1 \cdot (1 + 1 + 1 + 2 + 1.5 + 5 + 3 + 8 + 10 + 9) = 4.15$. The best packing takes the ten items of highest density and gets $6.1$, a ratio of $1.47$, well below $3.3026$. The early items of density 1 cost room that the two last items could have used; the threshold limits such losses but cannot avoid them, because the algorithm cannot know that the last items will come.

## Correctness

The [proof](proofs/correctness.md) has two halves. For the upper bound, Claim 3 shows that each taken item pays at least the threshold at the time it was taken, so the value collected is at least the area under $\Psi$ up to the final fill $Z$, up to a factor $(Ue/L)^{-\varepsilon}$. The area identity turns this into $\mathrm{ALG} \gtrsim c\,\Psi(Z)$. Each item of the optimum that was refused had density below $\Psi(Z)$, or the knapsack was nearly full and the density was at most $U \approx \Psi(Z)$. So $\mathrm{OPT}$ is at most about $\Psi(Z)$, and the ratio is at most $1/c = 1 + \ln(U/L)$, precisely

$$\mathrm{OPT} \le \Bigl(1 + \ln \frac{U}{L}\Bigr) \Bigl(\frac{Ue}{L}\Bigr)^{2 \varepsilon} \mathrm{ALG} \qquad \text{when every } w_i \le \varepsilon \le 1 - c.$$

For the lower bound, the adversary sends batches of tiny items with densities that rise geometrically from $L$ to $U$, each batch able to fill the knapsack, and may stop after any batch. Summation by parts shows that an algorithm that keeps the ratio $\alpha$ after each batch fills at least $\frac{1}{\alpha}(1 + N(1 - (L/U)^{1/N}))$ of the knapsack, so $\alpha \ge 1 + \ln(U/L)$ in the limit. The argument uses only expected fills, so it holds for randomized algorithms too.

## Complexity

- **Time.** $O(1)$ per item: one power for the threshold, one comparison and one addition. $O(n)$ for $n$ items.
- **Space.** $O(1)$ beyond the output: the constants $c$, $L$, $U$ and the fill $z$.
- **Numbers.** The threshold can be written as $L \exp((z - c)/c)$ for $z \ge c$, which avoids large powers when $U/L$ is large.

## Properties

- **Deterministic and online.** Each decision depends only on $z$ and the current item.
- **Optimal.** The ratio $1 + \ln(U/L)$ matches the lower bound for all online algorithms, randomized ones included, in the limit of small items.
- **Monotone threshold.** $\Psi$ is non-decreasing in $z$, so an item that is refused would also be refused later, at the same density.
- **Worst case over orders.** The bound holds for every arrival order. In random order a much better ratio is possible; see the [problem page](/online-knapsack-problem/).
- **Needs both $L$ and $U$.** If densities can be below $L$ the first phase can fill the knapsack with useless items, and if they can be above $U$ the last part of the knapsack is given away too cheaply.

## Variants and improvements

- **Fractional knapsack.** If items may be taken in part, the same threshold, applied to each infinitesimal unit, gives the ratio $1 + \ln(U/L)$ with no small items assumption.
- **Primal-dual view.** The threshold is a dual price on the capacity. The analysis is the same pattern as the [online primal-dual method](/online-primal-dual/) for packing, and the shape $\Psi$ is close to the trade-off function of the [adwords problem](/online-adwords-problem/), where the budgets play the role of capacities and the bids are the values.
- **One-way trading.** The problem of El-Yaniv, Fiat, Karp and Turpin, converting money at rates that arrive online and lie in a known range, has a threshold algorithm of the same form and a logarithmic ratio in the ratio of the largest to the smallest rate.
- **Many knapsacks.** When items can be assigned to one of several budgets, as in budgeted ad allocation, the idea of an exponential price on the used part of each budget is the basis of the adwords algorithms, and [Balance](/balance-algorithm/) is the case of unit values.
- **Unknown bounds.** If $L$ and $U$ are unknown, no bounded ratio is possible in general, as the problem page shows; estimates or predictions of $L$ and $U$ are used in practice.

## When to use it

Use it for online packing of a single budget or capacity when each request is small, the value per unit lies in a known range, and decisions are final: buying advertising slots under a daily budget, admitting jobs into a fixed capacity, or accepting bookings. If items are large, the guarantee fails, and the [problem page](/online-knapsack-problem/) has the results for that case. If the arrival order is random, secretary-style algorithms do better.

## Pitfalls

- **Large items.** The bound needs $w_i \le \varepsilon$ with $\varepsilon \le 1 - c$, and its error factor $(Ue/L)^{2\varepsilon}$ grows fast with $\varepsilon$. An item of weight near 1 that arrives early can block the knapsack.
- **Threshold on value, not on density.** The test in L4 is on $v_i / w_i$. A test on $v_i$ favours heavy items and has no bounded ratio.
- **No flat part.** The simpler threshold $L (U/L)^z$ equals $L$ only at $z = 0$. On an input whose items all have density $L$, it takes the first item and refuses the rest, so its ratio grows like $1/\varepsilon$. The flat part must last until $z = c = 1/(1 + \ln(U/L))$.
- **Rounding at $\Psi = L$.** Items of density exactly $L$ must be taken in the first phase. Floating-point division can make $v_i / w_i$ slightly below $L$, so the implementation compares with a tiny relative slack.
- **Measuring against the integral optimum only.** The fractional optimum is easier to compute and is also bounded by the theorem, so it is the right yardstick in tests.

## Implementations

## History

Online knapsack has no bounded ratio in general, as Marchetti-Spaccamela and Vercellis observed in 1995. Zhou, Chakrabarty and Lukose (WINE 2008, with a short version at WWW 2008) studied it as a model of an advertiser who bids for keywords under a budget, where each keyword query is small compared with the budget and the value per cost is bounded. They gave the exponential threshold, the ratio $\ln(U/L) + 1$, and a matching lower bound. The same exponential shape appears earlier in the one-way trading algorithm of El-Yaniv, Fiat, Karp and Turpin, and it is related to the trade-off function of Mehta, Saberi, Vazirani and Vazirani for adwords.

## References
