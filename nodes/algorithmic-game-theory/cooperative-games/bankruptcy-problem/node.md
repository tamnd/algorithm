---
tag: 617NG0
kind: problem
slug: bankruptcy-problem
name: Bankruptcy problem
aliases:
- claims problem
area: algorithmic-game-theory/cooperative-games
level: core
summary: Divide an estate among claimants whose claims add up to at least the estate, so that no one gets more than its claim. Rules include proportional, CEA, CEL, Talmud and random arrival.
prereqs: [transferable-utility-game]
see_also: [talmud-rule, nucleolus, shapley-value, convex-game, core-of-a-cooperative-game, nucleolus-sequential-lp, airport-game]
sources:
  - paper: doi:10.1016/0165-4896(82)90029-4
    title: "Barry O'Neill, A problem of rights arbitration from the Talmud, Mathematical Social Sciences 2(4) (1982), 345-371"
    locator: the claims problem as a formal model, the bankruptcy game, and the random arrival rule as its Shapley value
  - paper: doi:10.1016/0022-0531(85)90102-4
    title: "Robert J. Aumann and Michael Maschler, Game theoretic analysis of a bankruptcy problem from the Talmud, Journal of Economic Theory 36(2) (1985), 195-213"
    locator: the Talmud examples, the contested garment consistent rule, and the nucleolus of the bankruptcy game
  - paper: doi:10.1007/BF02109593
    title: "Imma J. Curiel, Michael Maschler and Stef H. Tijs, Bankruptcy games, Zeitschrift fur Operations Research 31(5) (1987), A143-A159"
    locator: bankruptcy games are convex; which division rules are solutions of the bankruptcy game
  - paper: doi:10.1016/S0165-4896(02)00070-7
    title: "William Thomson, Axiomatic and game-theoretic analysis of bankruptcy and taxation problems, a survey, Mathematical Social Sciences 45(3) (2003), 249-297"
    locator: the main rules (proportional, constrained equal awards, constrained equal losses, Talmud, random arrival) and their axioms
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Section 20.8, The bankruptcy problem
---

The bankruptcy problem asks how to divide an estate among creditors whose claims add up to more than the estate. It is also called the claims problem, because the same question comes up for a budget that cannot meet all requests, a tax that must raise a fixed sum, or a resource that is short. This page states the problem and compares the rules. The [Talmud rule](/talmud-rule/) has its own page, with code and a proof that it is the [nucleolus](/nucleolus/) of the bankruptcy game. The problem connects division rules and cooperative games: each rule studied here is a solution of a [TU game](/transferable-utility-game/) built from the claims.

## In plain words

A company closes and owes more than it has. Each creditor has a claim, and the claims add up to more than the money. Every rule must hand out all the money, give no creditor more than its claim, and give no creditor a negative amount. Within these limits there are many fair-looking choices. Pay in proportion to the claims. Give everyone the same amount, but never more than its claim. Make everyone lose the same amount, but never more than its claim. Let the creditors come in a random order, and pay each one in full while money is left. These rules give different answers, and the question is which properties a rule should have.

## Definition

A bankruptcy problem with $n$ claimants is a pair $(c, E)$ of a claims vector $c = (c_1, \ldots, c_n)$ with $c_i \ge 0$ and an estate $E$ with $0 \le E \le C$, where $C = c_1 + \cdots + c_n$. An award vector for $(c, E)$ is an $x \in \mathbb{R}^n$ with

$$x_1 + \cdots + x_n = E \quad \text{and} \quad 0 \le x_i \le c_i \text{ for every } i.$$

A rule is a function $R$ that maps each problem to an award vector. Some authors require $E < C$, so that the problem is a real shortage; the case $E = C$ has the single award vector $c$.

The bankruptcy game of $(c, E)$ is the [TU game](/transferable-utility-game/) on the players $N = \{1, \ldots, n\}$ with

$$v(S) = \max\big(0,\ E - c(N \setminus S)\big), \qquad c(T) = \sum_{i \in T} c_i.$$

A coalition $S$ gets what is left after it pays the claims of all creditors outside $S$ in full, or 0 if nothing is left. This is the pessimistic value of $S$.

Two facts about this game are short to prove.

**The core is the set of award vectors.** If $x$ is an award vector and $S \subseteq N$, then $x(S) \ge 0$ and $x(S) = E - x(N \setminus S) \ge E - c(N \setminus S)$, so $x(S) \ge v(S)$, and $x(N) = E = v(N)$. So $x$ is in the [core](/core-of-a-cooperative-game/). Conversely, a core point has $x_i \ge v(\{i\}) \ge 0$ and $x(N \setminus \{i\}) \ge v(N \setminus \{i\}) \ge E - c_i$, that is, $x_i \le c_i$.

**The game is convex.** Write $v(S) = f(c(S) - (C - E))$ with $f(z) = \max(0, z)$. For $S \subseteq T$ and $i \notin T$, the marginal value of $i$ is $f(c(S) + c_i - k) - f(c(S) - k)$ for $S$ and the same expression with $c(T) \ge c(S)$ for $T$, where $k = C - E$. Since $f$ is convex, $f(a + c_i) - f(a)$ does not decrease in $a$, so the marginal value for $T$ is at least that for $S$. This is the definition of a [convex game](/convex-game/) (Curiel, Maschler and Tijs 1987).

## Variants

- **Taxation problem.** The claims are incomes and $E$ is a tax to raise. Dividing the tax and dividing the after-tax incomes are dual problems: a rule for one gives the dual rule $R^d(c, E) = c - R(c, C - E)$ for the other. CEA and CEL are dual to each other, and the proportional and Talmud rules are self-dual.
- **Surplus sharing.** The estate exceeds the total claims, and the surplus must be divided. It needs other rules.
- **Claims with priorities.** Some claims must be paid before others, as in bankruptcy law. Inside each class the same question comes back.
- **Rationing.** The estate is a scarce good, such as a supply of a drug or the capacity of a link, and the claims are demands.

## Examples

Take the claims $(100, 200, 300)$ of the Mishna, so $C = 600$. The bankruptcy game for $E = 200$ has $v(\{2, 3\}) = 200 - 100 = 100$ and $v(N) = 200$; every other coalition, including each single creditor, has value 0. The table gives five rules for three estates.

| estate | proportional | CEA | CEL | Talmud | random arrival |
|---|---|---|---|---|---|
| 100 | $(50/3, 100/3, 50)$ | $(100/3, 100/3, 100/3)$ | $(0, 0, 100)$ | $(100/3, 100/3, 100/3)$ | $(100/3, 100/3, 100/3)$ |
| 200 | $(100/3, 200/3, 100)$ | $(200/3, 200/3, 200/3)$ | $(0, 50, 150)$ | $(50, 75, 75)$ | $(100/3, 250/3, 250/3)$ |
| 300 | $(50, 100, 150)$ | $(100, 100, 100)$ | $(0, 100, 200)$ | $(50, 100, 150)$ | $(50, 100, 150)$ |

Every entry is an award vector, so every entry is in the core of its game. For $E = 200$, the random arrival rule averages over the 6 orders: creditor 1 gets 100 when it comes first (2 orders) and 0 otherwise, so $200/6 = 100/3$.

For two claimants with claims $(1, 1/2)$ and estate 1, the contested garment of the Mishna, the Talmud rule gives $(3/4, 1/4)$, the proportional rule gives $(2/3, 1/3)$, CEA gives $(1/2, 1/2)$ and CEL gives $(3/4, 1/4)$.

## Known algorithms

- **Proportional rule.** $x_i = E c_i / C$, in $O(n)$ time.
- **Constrained equal awards (CEA).** $x_i = \min(c_i, \lambda)$ with $\sum_i x_i = E$. Sort the claims and fill from the smallest, in $O(n \log n)$ time; the [Talmud rule](/talmud-rule/) page gives the loop and its proof. It is often attributed to Maimonides.
- **Constrained equal losses (CEL).** $x_i = \max(0, c_i - \mu)$ with $\sum_i x_i = E$. It is the dual of CEA: $\mathrm{CEL}(c, E) = c - \mathrm{CEA}(c, C - E)$.
- **Talmud rule.** CEA on the half claims while $E \le C/2$, and half claims plus CEL on the other halves above. It is the nucleolus of the bankruptcy game (Aumann and Maschler 1985). Time $O(n \log n)$.
- **Random arrival rule.** The average, over all $n!$ orders of arrival, of the award vector that pays each creditor in full or with what is left. It is the [Shapley value](/shapley-value/) of the bankruptcy game (O'Neill 1982). The Shapley formula computes it in $O(n 2^n)$ time. For integer claims, a dynamic program that counts, for each creditor, the subsets of the others by their size and total claim gives a pseudo-polynomial time $O(n^3 C)$.
- **Any solution of the game.** The nucleolus can also be computed from the table of $v$ by the [sequential LP](/nucleolus-sequential-lp/), which is how the tests check the Talmud rule; this is exponential in $n$ and useful only as a check.

## Bounds

Every rule must output $n$ numbers, so $\Omega(n)$ time is needed. The proportional rule meets this bound. CEA, CEL and the Talmud rule also run in $O(n)$ time without sorting: the level $\lambda$ is found by repeated median selection over the claims, which halves the candidates in each step, as in the linear-time weighted median. Sorting gives the simpler $O(n \log n)$. The methods above for the random arrival rule are exponential in $n$ or pseudo-polynomial in $C$.

## Reductions

- **To a TU game.** The bankruptcy game turns each problem into a convex TU game. Under this map the random arrival rule is the Shapley value and the Talmud rule is the nucleolus. Curiel, Maschler and Tijs characterize the rules that are game solutions in this sense.
- **Between rules by duality.** A rule for awards gives a rule for losses with $R^d(c, E) = c - R(c, C - E)$. So any algorithm for CEA is an algorithm for CEL.
- **From the Talmud rule to two claimants.** The Talmud rule is the only rule that divides between every pair of claimants as the contested garment rule does (Aumann and Maschler 1985). So a rule for two claimants together with consistency fixes the rule for $n$ claimants.

## Applications

The problem models the division of the estate of a bankrupt firm or a deceased person among creditors, the cut of budget requests when the budget is short, the rationing of a scarce good among demands, and the division of a tax among incomes. The axioms used to compare rules (self-duality, consistency, order preservation, monotonicity in the estate) come from these uses; Thomson's survey of 2003 lists them with the rules that satisfy them.

## References
