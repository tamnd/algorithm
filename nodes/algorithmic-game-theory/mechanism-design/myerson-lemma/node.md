---
tag: EX9NTX
kind: theorem
slug: myerson-lemma
name: "Myerson's lemma"
aliases:
- payment identity
- characterization of truthful single-parameter mechanisms
area: algorithmic-game-theory/mechanism-design
level: core
summary: "In a single-parameter environment an allocation rule has DSIC payments if and only if it is monotone, and the payments are unique once a zero bid pays zero."
prereqs: [single-parameter-environment, monotone-allocation-rule, dominant-strategy-incentive-compatibility]
see_also: [myerson-optimal-auction, virtual-valuation, regular-distribution, ironing, revenue-equivalence-theorem, cycle-monotonicity, vickrey-auction, generalized-second-price-auction]
sources:
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the characterization of incentive-compatible single-item auctions by monotone allocation probabilities and the integral formula for payments
  - paper: "Aaron Archer and Eva Tardos, Truthful mechanisms for one-parameter agents, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001), 482-491"
    locator: the dominant-strategy version for one-parameter agents, with decreasing work curves and the integral payment formula
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 3 (Myerson's lemma, its proof, and the payment formula for piecewise constant allocation curves)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 9, Noam Nisan, Introduction to mechanism design (for computer scientists), the part on single-parameter domains
---

Myerson's lemma characterizes the truthful mechanisms of a [single-parameter environment](/single-parameter-environment/): an allocation rule can be paired with [DSIC](/dominant-strategy-incentive-compatibility/) payments if and only if it is [monotone](/monotone-allocation-rule/), and then the payments are forced by an integral formula. It is about truthfulness only and says nothing about revenue. The revenue result built on it is [Myerson's optimal auction](/myerson-optimal-auction/), which adds value distributions, expresses expected revenue through [virtual valuations](/virtual-valuation/), and handles distributions that are not [regular](/regular-distribution/) by [ironing](/ironing/). The lemma is the reason that algorithmic mechanism design for one-number types reduces to the design of monotone algorithms.

## Statement

Consider a single-parameter environment with $n$ agents and a feasible set $X \subseteq \mathbb{R}_{\ge 0}^n$. Each agent bids $b_i \in [0, \infty)$. A direct mechanism is a pair $(x, p)$ of an allocation rule $x(b) \in X$ and a payment rule $p(b) \in \mathbb{R}^n$, and agent $i$ with value $v_i$ has utility $v_i x_i(b) - p_i(b)$.

**Theorem (Myerson's lemma).**

1. An allocation rule $x$ is implementable, that is, some payment rule $p$ makes $(x, p)$ DSIC, if and only if $x$ is monotone: $x_i(z, b_{-i})$ is nondecreasing in $z$ for every $i$ and $b_{-i}$.
2. If $x$ is monotone, a payment rule $p$ makes $(x, p)$ DSIC if and only if there are functions $h_i$ with
$$p_i(b) = h_i(b_{-i}) + b_i \, x_i(b) - \int_0^{b_i} x_i(z, b_{-i}) \, dz \quad \text{for every } i \text{ and } b.$$
In particular there is exactly one DSIC payment rule with $p_i(0, b_{-i}) = 0$, the one with $h_i = 0$.
3. With $h_i = 0$, the mechanism is ex post [individually rational](/individual-rationality/) for truthful agents, and all payments are nonnegative.

If the allocation curve $z \mapsto x_i(z, b_{-i})$ is a step function with jumps of sizes $g_1, \dots, g_\ell$ at the points $z_1 < \dots < z_\ell$ in $[0, b_i]$, the formula with $h_i = 0$ becomes
$$p_i(b) = \sum_{j=1}^{\ell} z_j \, g_j.$$
For a win or lose rule there is one jump, of size 1, at the threshold bid, so a winner pays its threshold.

## In plain words

Look at one bidder and fix what everyone else says. As this bidder raises its bid, the amount it receives must never go down. If it ever went down, some bidder would gain by bidding less than its true value, whatever the prices. When the amount never goes down, there is always a way to set prices that makes honesty the best plan, and there is only one such way once a bidder who bids nothing pays nothing. The price is easy to describe when the amount changes in steps. Each step happens at some bid. The bidder pays, for each step it has passed, the bid at which the step happens times the size of the step. In a single-item auction this is the second-highest bid.

## Proof

Fix an agent $i$ and the other bids $b_{-i}$, and write $x(z) = x_i(z, b_{-i})$ and $p(z) = p_i(z, b_{-i})$.

**Monotonicity is necessary.** Suppose $(x, p)$ is DSIC, and let $y < z$ be two bids. An agent with value $z$ must not gain by bidding $y$, and an agent with value $y$ must not gain by bidding $z$:
$$z \, x(z) - p(z) \ge z \, x(y) - p(y), \qquad y \, x(y) - p(y) \ge y \, x(z) - p(z).$$
Rearranging both gives the *sandwich*
$$y \, (x(z) - x(y)) \;\le\; p(z) - p(y) \;\le\; z \, (x(z) - x(y)). \tag{1}$$
The outer terms give $(z - y)(x(z) - x(y)) \ge 0$, so $x(z) \ge x(y)$. This proves the "only if" part of item 1.

**The payment formula is necessary.** Let $(x, p)$ be DSIC, so $x$ is monotone. Fix a bid $b > 0$, split $[0, b]$ into $k$ equal parts $0 = z_0 < z_1 < \dots < z_k = b$, and apply (1) to each pair $z_{j-1} < z_j$. Summing over $j$,
$$\sum_{j=1}^{k} z_{j-1} \bigl(x(z_j) - x(z_{j-1})\bigr) \;\le\; p(b) - p(0) \;\le\; \sum_{j=1}^{k} z_j \bigl(x(z_j) - x(z_{j-1})\bigr).$$
Summation by parts rewrites the two sums. With the left Riemann sum $L_k = \sum_j (z_j - z_{j-1}) \, x(z_{j-1})$ and the right Riemann sum $R_k = \sum_j (z_j - z_{j-1}) \, x(z_j)$, the left side equals $b \, x(b) - R_k$ and the right side equals $b \, x(b) - L_k$. So
$$b \, x(b) - R_k \;\le\; p(b) - p(0) \;\le\; b \, x(b) - L_k.$$
Because $x$ is nondecreasing, $L_k \le \int_0^b x(z) \, dz \le R_k$ and $R_k - L_k = \frac{b}{k} (x(b) - x(0))$, which tends to 0. Letting $k \to \infty$ gives $p(b) = p(0) + b \, x(b) - \int_0^b x(z) \, dz$. This is the formula of item 2 with $h_i(b_{-i}) = p_i(0, b_{-i})$.

**Monotonicity with the formula is sufficient.** Let $x$ be monotone and define $p$ by the formula with any $h_i$. An agent with value $v$ who bids $b$ gets
$$u(v, b) = v \, x(b) - b \, x(b) + \int_0^b x(z) \, dz - h_i(b_{-i}),$$
and the truthful bid gives $u(v, v) = \int_0^v x(z) \, dz - h_i(b_{-i})$. Subtracting,
$$u(v, v) - u(v, b) = \int_b^v \bigl(x(z) - x(b)\bigr) \, dz.$$
If $v > b$, the integrand is nonnegative on $[b, v]$ because $x$ is nondecreasing. If $v < b$, the integral equals $\int_v^b (x(b) - x(z)) \, dz$, and this integrand is nonnegative too. So the truthful bid is a best response for every $b_{-i}$, and $(x, p)$ is DSIC. This proves the "if" part of item 1 and the "if" part of item 2. Uniqueness under $p_i(0, b_{-i}) = 0$ follows because then $h_i = 0$.

**Individual rationality.** With $h_i = 0$, a truthful agent has utility $\int_0^v x(z) \, dz \ge 0$, and the payment is $p(b) = \int_0^b (x(b) - x(z)) \, dz \ge 0$.

**Step functions.** If $x$ is a step function with jumps $g_j$ at $z_j \le b$, the region under the curve $x$ on $[0, b]$ is $b \, x(b)$ minus the region to the left of the curve, and the region to the left is $\sum_j z_j g_j$. $\square$

## Consequences

**Vickrey auction.** One item, bids $(10, 7, 3)$. Bidder 1's allocation curve is 0 below 7 and 1 above 7, so its payment is $7 \cdot 1 = 7$, the second-highest bid. This is the [Vickrey auction](/vickrey-auction/), and Myerson's lemma shows it is the only DSIC mechanism that gives the item to the highest bidder and charges losers nothing.

**A position auction, worked by hand.** Two slots get 2 and 1 clicks, and three advertisers bid $(10, 7, 3)$ per click. Higher bids get better slots.

- Advertiser 1 faces the bids $7$ and $3$. Its clicks are 0 for a bid below 3, then 1 up to 7, then 2. The jumps are of size 1 at 3 and at 7, so it pays $3 \cdot 1 + 7 \cdot 1 = 10$, or 5 per click.
- Advertiser 2 faces $10$ and $3$. Its clicks are 0 below 3 and 1 from 3 to 10, so it pays 3.
- Advertiser 3 gets no clicks and pays 0.

Advertiser 1 has utility $10 \cdot 2 - 10 = 10$. If it bid 5 instead, it would get slot 2 and pay 3, for utility $10 - 3 = 7$, so the lie loses. The [generalized second price auction](/generalized-second-price-auction/) charges each advertiser the next bid per click, which here is $7 \cdot 2 = 14$ for advertiser 1. That is not the Myerson payment, which is why GSP is not DSIC.

**Monotone algorithms become mechanisms.** For a computationally hard problem, a designer can use any monotone approximation algorithm as the allocation rule and get a DSIC mechanism with the same approximation ratio for welfare. For win or lose rules the payment of a winner is its threshold, which can be found by binary search with calls to the algorithm. The greedy knapsack rule on the page [monotone allocation rule](/monotone-allocation-rule/) is an example: the bidder whose threshold is 18 pays 18.

**Revenue equivalence and optimal auctions.** The payments are fixed by the allocation rule and the payment of a zero bid. So two DSIC mechanisms with the same allocation rule and $p_i(0, b_{-i}) = 0$ have the same payments and the same expected revenue under any value distributions. This is the dominant-strategy form of the [revenue equivalence theorem](/revenue-equivalence-theorem/). Taking expectations of the formula over a value distribution gives expected revenue as expected virtual welfare, which is the starting point of [Myerson's optimal auction](/myerson-optimal-auction/).

## Tightness

**Bids must form an interval.** If an agent can bid only $1$ or $3$ and the rule gives the item at bid 3 and not at bid 1, the sandwich (1) only says $1 \le p(3) - p(1) \le 3$. Every payment of the winner between 1 and 3, with $p(1) = 0$, is DSIC. So the uniqueness in item 2 fails without an interval of bids, while item 1 still holds on such sets.

**One number per agent is needed.** If types are vectors, a rule can be monotone in each coordinate and still have no DSIC payments, and the payments, when they exist, need not be unique. The right condition there is [cycle monotonicity](/cycle-monotonicity/), with weak monotonicity as its 2-cycle case.

**The normalization is needed for uniqueness.** Without $p_i(0, b_{-i}) = 0$, any $h_i(b_{-i})$ can be added. With $h_i > 0$ the mechanism is not individually rational, and with $h_i < 0$ it pays agents for nothing.

**Quasilinear utility is needed.** If an agent has a budget or is risk averse, its utility is not $v_i x_i - p_i$, and the formula no longer gives the incentive constraints.

**Randomized rules.** For a randomized allocation, the theorem holds with $x_i$ replaced by the expected allocation and $p_i$ by the expected payment. The result is [truthful in expectation](/truthful-in-expectation/), which assumes agents are risk neutral.

## History

Myerson (1981) proved the characterization in the Bayesian single-item setting, as the first step of his optimal auction. There, incentive compatibility is Bayesian, the condition is monotonicity of the expected probability of winning, and the payment is the same integral formula. Archer and Tardos (2001) proved the dominant-strategy version for one-parameter agents with private costs and used it to design truthful approximation mechanisms for scheduling on related machines. The name *Myerson's lemma* for the dominant-strategy statement is used in Roughgarden's lectures, where it is the basic tool for single-parameter mechanism design.

## References
