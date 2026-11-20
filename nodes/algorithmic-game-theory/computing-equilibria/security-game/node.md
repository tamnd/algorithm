---
tag: ZA3ZMX
kind: model
slug: security-game
name: Security game
aliases:
- Stackelberg security game
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: A Stackelberg game in which a defender commits to a randomized allocation of resources over targets and an attacker picks a target to attack.
prereqs: [stackelberg-commitment-algorithm, bimatrix-game, linear-programming-problem]
see_also: [stackelberg-equilibrium, stackelberg-commitment-algorithm, bayesian-game, mixed-integer-programming, indifference-principle, zero-sum-game-linear-programming, minimax-theorem, stackelberg-routing]
sources:
  - book: "Milind Tambe, Security and Game Theory, Algorithms, Deployed Systems, Lessons Learned, Cambridge University Press, 2011"
    title: Security and Game Theory
    locator: the security game model, coverage vectors, strong Stackelberg equilibria and the deployed systems
  - paper: "Christopher Kiekintveld, Manish Jain, Jason Tsai, James Pita, Fernando Ordonez and Milind Tambe, Computing optimal randomized resource allocations for massive security games, Proceedings of AAMAS 2009"
    locator: pp. 689 to 696 (compact formulations in terms of the coverage of each target, for games with many targets)
  - paper: "Dmytro Korzhyk, Vincent Conitzer and Ronald Parr, Complexity of computing optimal Stackelberg strategies in security resource allocation games, Proceedings of AAAI 2010"
    locator: the complexity of the optimal commitment when resources cover schedules of targets
  - paper: doi:10.1613/jair.3269
    title: "Dmytro Korzhyk, Zhengyu Yin, Christopher Kiekintveld, Vincent Conitzer and Milind Tambe, Stackelberg vs. Nash in security games: an extended investigation of interchangeability, equivalence, and uniqueness, Journal of Artificial Intelligence Research 41, 2011"
    locator: pp. 297 to 327 (Nash equilibria are interchangeable, and under a natural restriction every Stackelberg strategy is a Nash strategy)
---

A security game is a two-player game between a defender and an attacker. The defender has $k$ identical resources, such as patrols or guards, and $T$ targets to protect. The defender first commits to a randomized way to place the resources. The attacker observes the coverage probabilities, not the random draw, and attacks one target. The solution concept is the [Stackelberg equilibrium](/stackelberg-equilibrium/), and the general method for two-player games in normal form is the [multiple LPs algorithm](/stackelberg-commitment-algorithm/). This page is about the model: the payoffs depend only on the coverage of the attacked target, so the defender's exponentially many pure strategies reduce to $T$ coverage numbers. [Stackelberg routing](/stackelberg-routing/) is a different use of the word, for a leader who controls part of the traffic in a network.

Notation: targets are $t = 1, \ldots, T$. $U_d^c(t) > U_d^u(t)$ are the defender's payoffs when $t$ is attacked while it is covered or uncovered, and $U_a^c(t) < U_a^u(t)$ are the attacker's. $c_t$ is the probability that target $t$ is covered.

## The machine

The defender's pure strategies are the sets of at most $k$ targets; each resource covers one target. In some versions every resource must be used, and the sets have exactly $k$ targets. A mixed strategy is a distribution over these sets, and its coverage vector is $c = (c_1, \ldots, c_T)$, with $c_t$ the probability that $t$ is in the drawn set. The attacker's pure strategies are the targets. If the attacker hits $t$, the expected payoffs are

$$U_d(c, t) = c_t U_d^c(t) + (1 - c_t) U_d^u(t), \qquad U_a(c, t) = c_t U_a^c(t) + (1 - c_t) U_a^u(t).$$

They depend only on $c_t$, and not on the coverage of the other targets or on the correlation between them. The attacker plays a [best response](/best-response/) to $c$, and ties are broken in the defender's favor. This is the strong Stackelberg equilibrium. Without that rule the defender's optimum may not be attained, as in any Stackelberg game.

Two facts make the coverage vector the right state:

- **Every feasible vector can be sampled.** A vector $c$ with $0 \le c_t \le 1$ and $\sum_t c_t \le k$ is the coverage of some distribution over sets of at most $k$ targets. Comb sampling gives one: lay the $c_t$ end to end on the interval $[0, \sum_t c_t)$, draw $u$ uniformly from $[0, 1)$, and cover the targets whose pieces contain $u, u + 1, u + 2, \ldots$. Each piece has length at most 1, so no target is hit twice, and target $t$ is covered with probability exactly $c_t$. If $\sum_t c_t = k$, exactly $k$ targets are covered every time.
- **Only the coverage matters.** Two mixed strategies with the same $c$ give both players the same payoff on every target, so the defender can search over $c$ instead of over distributions.

## What it counts

The input is $4T$ payoffs and the number $k$. The normal form of the same game has $\binom{T}{k}$ rows (or more, with sets of all sizes up to $k$), so a direct use of the [multiple LPs algorithm](/stackelberg-commitment-algorithm/) on the [bimatrix game](/bimatrix-game/) is exponential in $k$. In the coverage form, the cost is counted in [linear programs](/linear-programming-problem/) with $T$ variables and $O(T)$ constraints, and in the arithmetic to sample a set from $c$, which is $O(T)$ operations.

## Relation to other models

- **Bimatrix Stackelberg games.** A security game is a bimatrix game with one row for each set of targets and one column for each target. The coverage form is a compact way to write the same LPs.
- **Bayesian attackers.** With several attacker types and a prior over them, the problem is NP-hard already in the bimatrix setting, and exact methods use a [mixed integer program](/mixed-integer-programming/) with binary variables for the attacked target of each type; see [Bayesian games](/bayesian-game/).
- **Zero-sum security games.** If $U_d^c(t) = -U_a^c(t)$ and $U_d^u(t) = -U_a^u(t)$ for every $t$, the defender's commitment value is the value of the zero-sum game, by the [minimax theorem](/minimax-theorem/), and it can be found by [one LP](/zero-sum-game-linear-programming/).
- **Schedules.** If a resource can cover a set of targets (a schedule), the coverage vectors that can be sampled form a smaller polytope, and the problem can become hard.

## Known results in the model

The optimal coverage comes from one LP for each target $t$: among the coverage vectors under which $t$ is a best target for the attacker, find the one that is best for the defender.

```pseudo id=main
SECURITY-GAME-SSE(Ud_c, Ud_u, Ua_c, Ua_u, k)
L1  for each target t = 1..T:
L2      LP_t: maximize c_t (Ud_c[t] - Ud_u[t]) + Ud_u[t]
              subject to c_s (Ua_c[s] - Ua_u[s]) + Ua_u[s] ≤ c_t (Ua_c[t] - Ua_u[t]) + Ua_u[t] for every s ≠ t   ▷ t is a best target
L3                       0 ≤ c_s ≤ 1 for every s, Σ_s c_s ≤ k   ▷ Σ_s c_s = k if no resource may stay idle
L4      if LP_t is infeasible: skip t
L5      keep (value of LP_t, its solution c, t) if the value is the largest so far
L6  return the kept (value, c, t); sample the set of covered targets from c by comb sampling
```

- **Polynomial time.** The algorithm solves $T$ LPs, each with $T$ variables, so the optimal commitment is found in time polynomial in $T$ and the bit length of the payoffs. The proof is the same as for the multiple LPs algorithm: every coverage vector makes some target a best target, so it is feasible for that LP, and the best LP optimum is attained with the tie rule. Kiekintveld and others (2009) gave compact formulations of this kind that scale to games with many targets.
- **Idle resources can help.** If the defender wants the attacker to hit a target with a high payoff when covered, full coverage of that target pushes the attacker away. Take $T = k = 3$ with $U_d^c = (6, 1, 0)$, $U_d^u = (0, 0, -4)$, $U_a^c = (-3, 0, 0)$ and $U_a^u = (2, 6, 3)$. If all three resources must be used, $c = (1, 1, 1)$, the attacker hits target 2 and the defender gets 1. With $\sum_t c_t \le 3$, the optimum is $c = (2/5, 1, 1)$: the attacker is indifferent between all three targets, hits target 1 by the tie rule, and the defender gets $12/5$.
- **More resources never hurt** when resources may stay idle, because the feasible sets of the LPs grow with $k$. The example above shows that this is false when every resource must be used.
- **Indifference at the optimum.** At an optimal $c$, the attacker is usually indifferent between several targets, and the defender's coverage on each of them is set by the [indifference principle](/indifference-principle/).
- **Schedules.** Korzhyk, Conitzer and Parr (2010) studied the complexity when resources cover schedules of targets: some cases have polynomial algorithms and others are NP-hard.
- **Stackelberg and Nash.** Korzhyk and others (2011) showed that the Nash equilibria of a security game are interchangeable, and that under a natural restriction on the schedules, every Stackelberg strategy of the defender is also a Nash equilibrium strategy. So the defender can commit without knowing whether the attacker observes the coverage.

Example. Take three targets and one resource, with $U_d^c = (1, 1, 0)$, $U_d^u = (-5, -3, -1)$, $U_a^c = (-1, -1, -1)$ and $U_a^u = (5, 3, 1)$.

| target | LP feasible | optimum of LP_t |
|---|---|---|
| 1 | yes | $c = (3/5, 2/5, 0)$, value $-7/5$ |
| 2 | yes | value $-7/5$ |
| 3 | no | the attacker gets at least $7/5 > 1$ elsewhere |

At $c = (3/5, 2/5, 0)$ the attacker gets $7/5$ on targets 1 and 2 and $1$ on target 3, and the defender gets $-7/5$ on targets 1 and 2. Target 3 cannot be the attacker's best target: with one resource, the attacker's payoffs on targets 1 and 2 cannot both drop to 1 or less, because that needs $c_1 \ge 2/3$ and $c_2 \ge 1/2$. Comb sampling covers target 1 with probability $3/5$ and target 2 with probability $2/5$.

The Python code solves LP_t for every target with the shared exact simplex code, with an option to require $\sum_t c_t = k$, and samples a set by comb sampling. The tests check the example, the idle resource example, monotonicity in $k$, the comb sampling marginals, and, on 40 random games, the same value as the multiple LPs algorithm on the full normal form, in both versions.

## References
