---
tag: JG4KT0
kind: technique
slug: automated-mechanism-design
name: Automated mechanism design
aliases:
- Conitzer-Sandholm automated mechanism design
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: Computes an optimal mechanism for a given prior and objective by solving a linear or integer program over outcomes and payments.
prereqs: [linear-programming-problem, bayesian-incentive-compatibility, revelation-principle]
see_also: [border-theorem, differentiable-economics, myerson-optimal-auction, cremer-mclean-theorem, dominant-strategy-incentive-compatibility, truthful-in-expectation, np-complete, simplex-method]
sources:
  - paper: "Vincent Conitzer and Tuomas Sandholm, Complexity of mechanism design, Proceedings of the 18th Conference on Uncertainty in Artificial Intelligence (UAI 2002), 103-110 (arXiv:cs/0205075)"
    locator: the linear program for randomized mechanisms, and NP-completeness for deterministic mechanisms without payments under dominant-strategy and Bayes-Nash implementation
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the optimal single-item auction, used here as a reference answer for the linear program
  - paper: doi:10.1145/2213977.2214021
    title: "Yang Cai, Constantinos Daskalakis and S. Matthew Weinberg, An algorithmic characterization of multi-dimensional mechanisms, STOC 2012, 459-478"
    locator: linear programs over interim (reduced form) variables with a separation oracle, which avoid one variable per type profile
---

Automated mechanism design (AMD) computes a mechanism for one concrete instance instead of deriving it by hand. The designer writes down the finite type sets, the prior, the outcomes, the agents' values and its own objective, and a solver finds the mechanism that maximizes the objective under incentive and participation constraints. By the [revelation principle](/revelation-principle/), it is enough to search over direct mechanisms that are truthful. Conitzer and Sandholm (2002) observed that if the mechanism may randomize, every constraint and the objective are linear in the outcome probabilities and payments, so the optimal mechanism is the solution of one [linear program](/linear-programming-problem/). If the mechanism must be deterministic, the problem becomes [NP-complete](/np-complete/) in general.

## In plain words

Usually an expert designs an auction or a voting rule with pen and paper, and the result works only for the cases the expert studied. Automated mechanism design lets a computer do the design for the case at hand. You list the possible kinds of participants, how likely each one is, what each one wants, and what you want. The computer then searches over all rules that make honesty the best plan and that people are willing to join, and picks the best one for you. If the rule is allowed to flip coins, this search is a standard optimization problem that computers solve fast. If the rule may not flip coins, the search can be very hard.

## When it applies

- The type sets are finite and small, or can be discretized into a small grid, and the prior over type profiles is known. The prior may be correlated.
- The objective is linear in the outcome lottery and the payments: expected revenue, expected welfare, the designer's own utility for outcomes, or a weighted sum of these.
- The constraints are linear: Bayesian or dominant-strategy incentive compatibility, interim or ex post individual rationality, budget balance, or no payments at all.
- The designer accepts a randomized mechanism. If it must be deterministic, the same model with 0/1 outcome variables is an integer program, which may still be solved for small instances.

The method does not fit when the number of type profiles is huge, since it needs one block of variables per profile, or when types are continuous and a coarse grid would lose the structure of the optimal mechanism.

## The template

There are $n$ agents with finite type sets $T_1, \ldots, T_n$, a prior $\pi$ on $T = T_1 \times \cdots \times T_n$, outcomes $O$ and values $v_i(s, o)$ for type $s \in T_i$. The objective has weight $g(o)$ on each outcome, weight $a$ on the sum of values and weight $b$ on the payments. Write $U_i(s \to r; t)$ for the utility of agent $i$ of true type $s$ when it reports $r$ and the others report $t_{-i}$:

$$U_i(s \to r; t) = \sum_{o \in O} x((r, t_{-i}), o)\, v_i(s, o) - p_i(r, t_{-i}).$$

```pseudo id=main
AUTOMATED-MECHANISM-DESIGN(T, π, O, v, g, a, b, IC, IR)
L1  make variables x(t, o) ≥ 0 and free p_i(t) for every profile t, outcome o and agent i
L2  for each profile t: add Σ_o x(t, o) = 1
L3  for each agent i and types s ≠ r in T_i: add the IC constraint "s gains nothing by reporting r"
L4  for each agent i and type s: add the IR constraint "s gets utility at least 0"
L5  solve: maximize Σ_t π(t) [Σ_o x(t, o) (g(o) + a Σ_i v_i(t_i, o)) + b Σ_i p_i(t)]
L6  return the lottery x(t, ·) and the payments p(t) for every profile t
```

For Bayesian incentive compatibility (BIC), the constraint on line L3 is one row for each $(i, s, r)$:

$$\sum_{t : t_i = s} \pi(t) \big( U_i(s \to s; t) - U_i(s \to r; t) \big) \ \ge\ 0.$$

Multiplying by $\pi(t)$ instead of dividing by $\Pr[t_i = s]$ keeps the row linear and handles correlated priors, where the belief of agent $i$ depends on $s$. For dominant-strategy incentive compatibility (DSIC), the row is required separately for every $t_{-i}$. Interim individual rationality (IR) on line L4 is $\sum_{t : t_i = s} \pi(t)\, U_i(s \to s; t) \ge 0$, and ex post IR asks $U_i(s \to s; t) \ge 0$ for every $t$.

**Correctness.** Every truthful randomized direct mechanism is a feasible point of the LP, with the same objective value, and every feasible point is such a mechanism. So an optimal LP solution is an optimal mechanism. By the revelation principle, no other mechanism, direct or not, does better in equilibrium.

**Size.** With $k$ types per agent, $m$ outcomes and $N = k^n$ profiles, the LP has $N (m + n)$ variables, $N$ equations, $n k^2$ BIC rows (each with up to $N m$ terms) or about $N n k$ DSIC rows, and $n k$ or $N n$ IR rows. The size is polynomial in the size of the prior when the prior is given as a full table, but exponential in $n$.

## Classic examples

**Randomization helps, worked by hand.** One agent has type L or H with probability $1/2$ each. There are three outcomes and no payments. The values are $v(L, \cdot) = (3, 4, 0)$ and $v(H, \cdot) = (1, 5, 0)$ for $(a, b, c)$, and the designer maximizes the agent's value plus $g = (0, -3, -1)$, so its payoff is $(3, 1, -1)$ for type L and $(1, 2, -1)$ for type H. The designer would like L to get $a$ and H to get $b$, for $\frac{1}{2} \cdot 3 + \frac{1}{2} \cdot 2 = \frac{5}{2}$, but then L reports H, since it values $b$ at 4 and $a$ at 3. The best deterministic mechanism gives $a$ to both types, for $\frac{1}{2} \cdot 3 + \frac{1}{2} \cdot 1 = 2$. The LP gives $a$ to L and the lottery $\frac{3}{4} b + \frac{1}{4} c$ to H. Type L values that lottery at $3$, exactly its value for $a$, so it does not lie; type H values it at $\frac{15}{4} > 1$. The designer gets $\frac{1}{2} \cdot 3 + \frac{1}{2} \big(\frac{3}{4} \cdot 2 - \frac{1}{4}\big) = \frac{17}{8} > 2$.

**Optimal auctions.** With outcomes "bidder $i$ wins" and "no sale", $a = 0$, $b = 1$, BIC and interim IR, the LP finds the revenue-optimal auction. For one buyer it returns the best posted price, with revenue $\max_j v_j \Pr[v \ge v_j]$. For independent bidders its value equals the expected maximum of the ironed virtual values in [Myerson's optimal auction](/myerson-optimal-auction/), with both BIC and DSIC constraints. The tests check both facts against direct formulas.

**Correlated types.** For two bidders with values 1 or 2 and the prior $\pi(1, 1) = \pi(2, 2) = \frac{1}{3}$, $\pi(1, 2) = \pi(2, 1) = \frac{1}{6}$, the same LP returns revenue $\frac{5}{3}$, the full expected surplus, as the [Cremer-McLean theorem](/cremer-mclean-theorem/) predicts. The LP finds the side bets on the other bidder's report without being told about them.

**Applications.** In later papers, Conitzer and Sandholm applied the method to small instances such as a divorce settlement and auctions of a few items with complements, with a designer that may be self-interested.

## Variations

- **Deterministic mechanisms.** Requiring $x(t, o) \in \{0, 1\}$ gives an integer program. Without payments this problem is NP-complete, for both dominant-strategy and Bayes-Nash implementation (Conitzer and Sandholm, 2002). Later work showed hardness in some settings with payments too.
- **Interim (reduced form) variables.** For auctions with independent types, the incentive constraints depend only on the interim allocation and payment of each agent. An LP over these $\sum_i |T_i|$ variables, plus [Border's theorem](/border-theorem/) or a separation oracle for the feasibility of the interim rule, avoids the $k^n$ blow-up. This is the approach of Cai, Daskalakis and Weinberg (2012).
- **Incremental and search-based solvers.** Branch-and-bound over deterministic mechanisms and constraint generation, which adds only the incentive constraints that the current solution violates, scale to larger instances.
- **Learning the mechanism.** When types are continuous or many, the mechanism can be a parameterized function trained on samples, as in [deep learning for auction design](/differentiable-economics/). This trades the exactness of the LP for scale, and incentive compatibility then holds only approximately.
- **Other solution concepts.** Ex post IC, IR with outside options that depend on the type, budget balance and caps on payments are all linear constraints and fit the same template.

## Pitfalls

- **The result is only as good as the prior.** The LP fits the prior exactly, and a mechanism that is BIC for one prior can fail to be BIC for a slightly different one. Full surplus extraction with correlated types is the extreme case: the side bets can be huge, and they rely on the exact conditional beliefs.
- **Randomization may not be acceptable.** The optimal LP solution may use lotteries, as in the example. If the setting forbids them, the LP value is only an upper bound, and the integer program can be hard.
- **Free payments must be split.** An LP solver with nonnegative variables needs $p_i = p_i^+ - p_i^-$. Forgetting this forbids subsidies and changes the answer.
- **Exponential size.** The number of profiles grows as $k^n$. Three agents with ten types each already give 1000 profiles, and the BIC rows are dense.
- **Zero-probability profiles.** Profiles with $\pi(t) = 0$ do not enter the objective or the BIC rows, so their outcomes are arbitrary. Under DSIC they still matter, because a lie can lead to them.
- **Discretization.** A grid on continuous types gives a mechanism that is IC only on the grid points. Between them, an agent may want to lie, so the mechanism must be extended with care.

## Exercises

1. Write the LP for one buyer, one item and types $1 < 2 < 3$ with equal probability, and show that its optimum is the posted price $2$ with revenue $\frac{4}{3}$.
2. In the worked example, show that every lottery $\lambda b + (1 - \lambda) c$ with $\lambda \le \frac{3}{4}$ keeps type L honest, and that $\lambda = \frac{3}{4}$ is optimal.
3. Prove that if the objective depends only on the outcome ($a = b = 0$) and there are no payments, then giving the best outcome to every profile is optimal, so randomization never helps.
4. Show that for a single agent, BIC and DSIC are the same constraints, and so are interim and ex post IR.
5. Count the variables and BIC rows of the LP for three bidders with four types each and four outcomes.

## References
