---
title: Correctness of the VCG mechanism
proves: [correctness]
status: full
---

Let $O$ be a finite nonempty set of outcomes, and let $b_1, \ldots, b_n : O \to \mathbb{R}$ be the reports. Write $T(o) = \sum_j b_j(o)$ and, for each agent $i$, $T_{-i}(o) = T(o) - b_i(o) = \sum_{j \ne i} b_j(o)$. The algorithm returns $x$ and $p_1, \ldots, p_n$ with $p_i = W_{-i} - T_{-i}(x)$, where $W_{-i} = \max_{o \in O} T_{-i}(o)$. Agent $i$ with true valuation $v_i$ has utility $u_i = v_i(x) - p_i$.

## Claim 1: lines L1 and L2 return an outcome of maximum reported welfare

Line L1 computes $T(o)$ for every $o$. Line L2 starts with the first outcome and replaces the current $x$ by $o$ only when $T(o) > T(x)$. After it has seen a prefix of the list, $x$ is the first outcome of the prefix with the largest $T$, by induction on the length of the prefix. At the end, $T(x) = \max_{o \in O} T(o)$. If every report is true, $T$ is the true welfare, so $x$ maximizes the true welfare.

## Claim 2: lines L4 and L5 compute the Clarke pivot payment

Line L4 computes $\max_o (T(o) - b_i(o)) = \max_o T_{-i}(o) = W_{-i}$, and line L5 sets $p_i = W_{-i} - (T(x) - b_i(x)) = W_{-i} - T_{-i}(x)$. This is the Groves payment $h_i(b_{-i}) - T_{-i}(x)$ with $h_i(b_{-i}) = W_{-i}$. The value $W_{-i}$ is a function of $b_{-i}$ only, since $T_{-i}$ does not contain $b_i$.

## Claim 3: truth telling is a dominant strategy

Fix an agent $i$, its true valuation $v_i$, and any reports $b_{-i}$ of the others. Let $x$ be the outcome when $i$ reports $v_i$, and let $y$ be the outcome when $i$ reports any $b_i$. The term $W_{-i}$ is the same in both cases, by Claim 2. So

$$u_i(\text{truth}) = v_i(x) + T_{-i}(x) - W_{-i}, \qquad u_i(b_i) = v_i(y) + T_{-i}(y) - W_{-i}.$$

When $i$ reports $v_i$, the reported welfare is $v_i(o) + T_{-i}(o)$, and by Claim 1, $x$ maximizes it over $O$. In particular $v_i(x) + T_{-i}(x) \ge v_i(y) + T_{-i}(y)$, so $u_i(\text{truth}) \ge u_i(b_i)$. The argument does not use the tie rule of line L2, only that $x$ is some maximizer, and it uses no assumption on $v_i$ or on $b_{-i}$.

## Claim 4: no positive transfers, and individual rationality for nonnegative valuations

Since $W_{-i}$ is the maximum of $T_{-i}$ over all of $O$, $W_{-i} \ge T_{-i}(x)$, so $p_i \ge 0$ for every input. No agent receives money.

Now let every report be true and let every valuation be nonnegative. Let $z$ maximize $T_{-i}$, so $W_{-i} = T_{-i}(z)$. Then

$$u_i = v_i(x) + T_{-i}(x) - T_{-i}(z) = T(x) - T(z) + v_i(z) \ge v_i(z) \ge 0,$$

because $T(x) \ge T(z)$ by Claim 1 and $v_i(z) \ge 0$. So a truthful agent never ends with negative utility. The bound $v_i(z) \ge 0$ is the only place where nonnegativity is used. With $v_i(z) < 0$ the utility can be negative: for $O = \{0, 1\}$, $v_1 = (0, 5)$ and $v_2 = (0, -2)$, the mechanism picks 1, $W_{-2} = 5 = T_{-2}(1)$, so $p_2 = 0$ and $u_2 = -2$.

## Claim 5: the mechanism is weakly budget balanced

By Claim 4, each $p_i \ge 0$, so $\sum_i p_i \ge 0$ and the mechanism never runs a deficit. It is not strongly budget balanced in general. With one item and values $(10, 7, 3)$, the payments are $(7, 0, 0)$ and their sum is 7, not 0. By the Green-Laffont theorem on budget balance, no choice of $h_i$ makes the sum 0 on every input when the valuations are unrestricted.

## Running time

Line L1 does $n$ additions for each of the $k$ outcomes. Line L2 does $k$ comparisons. For each of the $n$ agents, line L4 takes $k$ subtractions and a maximum over $k$ values, and line L5 takes constant time. The total is $O(nk)$ arithmetic operations and the table $T$ needs $O(k)$ extra space.
