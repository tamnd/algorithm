---
tag: 40YNTR
kind: theorem
slug: arrow-debreu-existence-theorem
name: Arrow-Debreu existence theorem
aliases:
- existence of competitive equilibrium
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Under continuity, convexity, local nonsatiation and positive endowments, an exchange market has a competitive equilibrium, by a fixed-point argument.
prereqs: [arrow-debreu-market, brouwer-fixed-point-theorem, kakutani-fixed-point-theorem]
see_also: [competitive-equilibrium, first-welfare-theorem, fisher-market, nash-existence-theorem, scarf-algorithm, ppad-hardness-of-arrow-debreu, tatonnement, sperner-lemma]
sources:
  - paper: doi:10.2307/1907353
    title: "Kenneth J. Arrow and Gerard Debreu, Existence of an equilibrium for a competitive economy, Econometrica 22(3), 265-290 (1954)"
    locator: the whole paper (the existence theorems for an economy with consumers and producers, proved through an abstract economy and a fixed point theorem)
  - book: isbn:9780195073409
    title: Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, Microeconomic Theory, Oxford University Press, 1995
    locator: Chapter 17 (existence of Walrasian equilibrium, the proof with a continuous excess demand function and the truncated economy)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria, and Chapter 6, Bruno Codenotti and Kasturi Varadarajan, Computation of market equilibria by convex programming (existence as the starting point of the computational questions)
---

The Arrow-Debreu existence theorem says that an exchange market has a [competitive equilibrium](/competitive-equilibrium/) when the agents have continuous, convex and locally nonsatiated preferences and every agent owns a positive amount of every good. Arrow and Debreu (1954) proved it for economies with production as well, and McKenzie (1954) proved a similar theorem at the same time. The proof is not constructive. It turns the market into a fixed point problem, as Nash did for games, and uses the [Brouwer fixed point theorem](/brouwer-fixed-point-theorem/) or the [Kakutani fixed point theorem](/kakutani-fixed-point-theorem/). This is why the computation of equilibria belongs to the class PPAD, and why it can be hard: see [PPAD-hardness of market equilibria](/ppad-hardness-of-arrow-debreu/).

## Statement

Take an [Arrow-Debreu market](/arrow-debreu-market/) with $n$ agents and $m$ goods. Agent $i$ has an endowment $w_i \in \mathbb{R}^m_{\ge 0}$ and a utility function $u_i$ on $\mathbb{R}^m_{\ge 0}$. Prices lie in the simplex $\Delta_m = \{p \in \mathbb{R}^m : p \ge 0, \sum_j p_j = 1\}$, and the budget set and demand set of agent $i$ at $p$ are $B_i(p) = \{x \ge 0 : p \cdot x \le p \cdot w_i\}$ and $D_i(p) = \arg\max_{x \in B_i(p)} u_i(x)$.

**Theorem (Arrow and Debreu 1954).** Suppose that for every agent $i$

1. $u_i$ is continuous,
2. the preferences are convex in the sense of Arrow and Debreu: if $u_i(x) > u_i(y)$ and $0 < t < 1$, then $u_i(t x + (1 - t) y) > u_i(y)$ (for a continuous $u_i$ this implies that $u_i$ is quasi-concave),
3. $u_i$ is locally nonsatiated, and
4. $w_i > 0$ in every coordinate.

Then there are prices $p \in \Delta_m$ and an allocation $x$ such that $(p, x)$ is a competitive equilibrium: $x_i \in D_i(p)$ for every $i$, and $\sum_i x_{ij} \le \sum_i w_{ij}$ for every good $j$, with equality when $p_j > 0$.

Condition 4 can be replaced by weaker conditions that keep every agent's income positive where it matters, such as the irreducibility condition of McKenzie (1959). Arrow and Debreu also allow firms with closed convex production sets, owned in fixed shares by the agents.

## In plain words

If people have sensible tastes, like a mix of things better than extremes, and always want a little more, and if everybody owns a bit of everything, then there are prices at which everybody can buy what they want most and nothing runs short. The proof does not say how to find these prices. It builds a rule that raises the price of any good that is short, and shows that some set of prices is left unchanged by the rule. At such prices nothing is short.

## Proof

We prove the theorem when each $u_i$ is *strictly* quasi-concave: $u_i(t x + (1 - t) y) > \min(u_i(x), u_i(y))$ for $x \ne y$ and $0 < t < 1$. Then demand is a single bundle, and Brouwer's theorem is enough. The general case is at the end.

Let $W = \sum_i w_i$, so $W > 0$, and fix a number $c > \max_j W_j$. Let $K = [0, c]^m$.

*Step 1: truncated demand.* For $p \in \Delta_m$, let $\hat{x}_i(p)$ maximize $u_i$ over $\hat{B}_i(p) = B_i(p) \cap K$. This set is compact and convex and contains $0$, so a maximizer exists, and it is unique: if $x \ne y$ were both maximizers, their midpoint would be in $\hat{B}_i(p)$ and strictly better.

*Step 2: $\hat{x}_i$ is continuous on $\Delta_m$.* Let $p^k \to p$ and let $x^*$ be the limit of a convergent subsequence of $\hat{x}_i(p^k)$ (one exists because $K$ is compact). Then $x^* \in K$ and $p \cdot x^* \le p \cdot w_i$, so $x^* \in \hat{B}_i(p)$. Take any $y \in \hat{B}_i(p)$ and $0 < t < 1$. Because $w_i > 0$ and $p \ne 0$, the income $p \cdot w_i$ is positive, so $p \cdot (t y) \le t \, p \cdot w_i < p \cdot w_i$. Hence $p^k \cdot (t y) < p^k \cdot w_i$ for all large $k$, and $t y \in K$, so $u_i(\hat{x}_i(p^k)) \ge u_i(t y)$. Letting $k \to \infty$ and then $t \to 1$ gives $u_i(x^*) \ge u_i(y)$. So $x^*$ is the unique maximizer $\hat{x}_i(p)$. Every subsequence has a further subsequence with this limit, so $\hat{x}_i(p^k) \to \hat{x}_i(p)$. This step is where condition 4 is used: with zero income the budget set can jump when a price becomes $0$.

*Step 3: a fixed point.* Let $\hat{z}(p) = \sum_i \hat{x}_i(p) - W$, a continuous function, and define $g : \Delta_m \to \Delta_m$ by
$$
g_j(p) = \frac{p_j + \max(0, \hat{z}_j(p))}{1 + \sum_k \max(0, \hat{z}_k(p))} .
$$
The map $g$ is continuous and its values lie in $\Delta_m$. By Brouwer's theorem it has a fixed point $p^*$. Write $\hat{z} = \hat{z}(p^*)$ and $s = \sum_k \max(0, \hat{z}_k)$. The fixed point equation says $p^*_j s = \max(0, \hat{z}_j)$ for every $j$. Multiply by $\hat{z}_j$ and add over $j$:
$$
s \, (p^* \cdot \hat{z}) = \sum_j \max(0, \hat{z}_j)^2 .
$$
Each agent stays in her budget, so $p^* \cdot \hat{z} \le 0$, and the left side is at most $0$. So every $\max(0, \hat{z}_j)$ is $0$, that is, $\hat{z} \le 0$.

*Step 4: the truncation does not bind.* By Step 3, $\sum_i \hat{x}_i(p^*) \le W$, so every coordinate of every $\hat{x}_i(p^*)$ is at most $\max_j W_j < c$. Suppose some $x \in B_i(p^*)$ had $u_i(x) > u_i(\hat{x}_i(p^*))$. For small $t > 0$ the point $x_t = t x + (1 - t) \hat{x}_i(p^*)$ is still in $K$, it is in $B_i(p^*)$ because the budget set is convex, and by strict quasi-concavity $u_i(x_t) > u_i(\hat{x}_i(p^*))$. This contradicts Step 1. So $x_i = \hat{x}_i(p^*)$ is in $D_i(p^*)$.

*Step 5: clearing.* By local nonsatiation each agent spends her whole income at her demand: if $p^* \cdot x_i < p^* \cdot w_i$, a nearby bundle would still be affordable and better. So $p^* \cdot \hat{z} = 0$. Since $\hat{z} \le 0$ and $p^* \ge 0$, every term $p^*_j \hat{z}_j$ is at most $0$ and they add to $0$, so $\hat{z}_j = 0$ whenever $p^*_j > 0$. Hence $(p^*, x)$ is a competitive equilibrium. $\square$

*The general case (sketch).* Under condition 2 alone, the truncated demand $\hat{D}_i(p)$ is a nonempty, convex, compact set (convex because $u_i$ is quasi-concave) that depends upper hemicontinuously on $p$ (Berge's maximum theorem, with Step 2's use of positive income). Apply Kakutani's theorem to the correspondence that maps $(p, x_1, \dots, x_n)$ to the product of the sets $\hat{D}_i(p)$ and the set of prices that maximize $q \cdot (\sum_i x_i - W)$ over $q \in \Delta_m$. At a fixed point, the prices maximize the value of the excess demand $z$ over $\Delta_m$, so $\max_j z_j = p^* \cdot z \le 0$ by the budgets, and $z \le 0$. Step 4 goes through as written, because condition 2 makes $x_t$ strictly better than $\hat{x}_i(p^*)$, and Step 5 is unchanged. This is the abstract economy argument of Arrow and Debreu (1954), in which a price player chooses prices to maximize the value of excess demand. $\blacksquare$

## Consequences

- **Total search problems.** For each class of markets that satisfies the hypotheses, "find an equilibrium" always has an answer. With the right input format the problem lies in [TFNP](/tfnp/), and for many classes in [PPAD](/ppad/), the class of problems whose existence proof is a fixed point or parity argument. The proof above is the source of that membership.
- **Equivalence with Brouwer.** Uzawa (1962) showed that the existence of equilibria for all continuous excess demand functions that satisfy Walras' law implies Brouwer's theorem. So no proof can avoid a fixed point argument in general.
- **Computation.** [Scarf's algorithm](/scarf-algorithm/) (1967) finds approximate fixed points by simplicial pivoting, in the style of [Sperner's lemma](/sperner-lemma/), and was designed for this problem. For special classes there are fast exact algorithms: linear [Fisher markets](/fisher-market/) by the [Eisenberg-Gale program](/eisenberg-gale-program/) and the [DPSV algorithm](/dpsv-algorithm/), and linear exchange markets by convex programs and combinatorial algorithms (see [Arrow-Debreu market](/arrow-debreu-market/)).
- **Efficiency.** With the [first welfare theorem](/first-welfare-theorem/), the theorem says that a Pareto optimal allocation supported by prices exists.

## Tightness

- **Positive endowments.** Agent 1 owns $w_1 = (1, 0)$ and has $u_1 = y_1 + y_2$; agent 2 owns $w_2 = (1, 1)$ and has $u_2 = y_2$. All utilities are continuous, concave and locally nonsatiated, but $w_1$ has a zero. If $p_2 = 0$, agent 2 wants unboundedly much of good 2. If $p_2 > 0$, agent 2 spends $p_1 + p_2$ on good 2 and asks for $(p_1 + p_2)/p_2$ units, while only $1$ unit exists, so $p_1 = 0$. But then agent 1 has income $p_1 = 0$ and still wants unboundedly much of good 1, which is free. So there is no equilibrium.
- **Convexity.** Agent 1 has $u_1 = y_1^2 + y_2^2$, which is not quasi-concave, and agent 2 has $u_2 = \sqrt{y_1} + \sqrt{y_2}$; both own $(1, 1)$. At prices $p_1 < p_2$, agent 1 puts her whole income $p_1 + p_2$ on good 1 and asks for more than the total supply $2$; the case $p_1 > p_2$ is symmetric, and a zero price makes demand unbounded. At $p = (1/2, 1/2)$, agent 2 demands $(1, 1)$ and agent 1 demands $(2, 0)$ or $(0, 2)$, so the total demand is $(3, 1)$ or $(1, 3)$, not $(2, 2)$. So there is no equilibrium.
- **Indivisible goods.** With indivisible goods the demand sets are not convex, and equilibria may fail to exist: see the non-examples on [competitive equilibrium](/competitive-equilibrium/). Approximate notions such as [approximate CEEI](/approximate-ceei/) are the usual answer.
- **Uniqueness and stability.** The theorem gives existence only. Equilibria can be many, and [tatonnement](/tatonnement/) may not reach any of them (Scarf 1960). The Sonnenschein-Mantel-Debreu results show that the market excess demand can be almost any continuous function that satisfies Walras' law, so no general uniqueness or stability theorem is possible without further assumptions such as gross substitutes.

## History

Walras (1874) counted equations and unknowns and argued that equilibrium prices should exist. Wald (1935, 1936) proved existence for special models. Arrow and Debreu (1954), and independently McKenzie (1954), gave the first general proofs, using the fixed point theorems that von Neumann, Kakutani and Nash had brought into economics; Arrow and Debreu used Debreu's (1952) existence theorem for abstract economies. Gale (1955) and Nikaido (1956) found the short excess demand lemma behind Step 3, and McKenzie (1959) weakened the endowment condition to irreducibility. Uzawa (1962) showed the converse link to Brouwer's theorem, and Scarf (1967) gave the first general algorithm for approximate equilibria. The computational complexity of the problem became a topic of algorithmic game theory after 2000, with polynomial algorithms for linear utilities and PPAD-hardness for piecewise-linear concave utilities (Chen, Dai, Du and Teng 2009).

## References
