---
tag: APVVSH
kind: technique
slug: smoothness-framework
name: Smooth games framework
aliases:
- Roughgarden smoothness
- robust price of anarchy
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: "A (lambda, mu) inequality on deviations that bounds the price of anarchy by lambda/(1-mu) for pure, mixed, correlated and no-regret outcomes alike."
prereqs: [price-of-anarchy, coarse-correlated-equilibrium, atomic-congestion-game]
see_also: [atomic-linear-congestion-price-of-anarchy, roughgarden-tardos-four-thirds-bound, no-regret-coarse-correlated-theorem, no-regret-dynamics, first-price-auction-price-of-anarchy, correlated-equilibrium, price-of-anarchy-of-load-balancing, pigou-bound]
sources:
  - paper: "Tim Roughgarden, Intrinsic robustness of the price of anarchy, Journal of the ACM 62(5) (2015), Article 32; STOC 2009, 513-522"
    locator: "the definition of smooth games, the extension theorem to mixed Nash, correlated and coarse correlated equilibria and to no-regret sequences, and the tightness of the robust bound for congestion games"
  - book: isbn:9781107172661
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: Lecture 14 (robust price-of-anarchy bounds in smooth games)
  - paper: "Avrim Blum, MohammadTaghi Hajiaghayi, Katrina Ligett and Aaron Roth, Regret minimization and the price of total anarchy, STOC 2008"
    locator: price of anarchy bounds for the outcomes of no-regret play
  - paper: "Adrian Vetta, Nash equilibria in competitive societies, with applications to facility location, traffic routing and auctions, FOCS 2002"
    locator: valid utility games and their bound 2
  - paper: "Vasilis Syrgkanis and Eva Tardos, Composable and efficient mechanisms, STOC 2013"
    locator: smooth mechanisms and the extension to Bayes-Nash equilibria and to composed mechanisms
  - paper: "Tim Roughgarden and Florian Schoppmann, Local smoothness and the price of anarchy in splittable congestion games, Journal of Economic Theory 156 (2015); SODA 2011"
    locator: "local smoothness, the variant for nonatomic and splittable flows"
---

The smoothness framework proves an upper bound on the [price of anarchy](/price-of-anarchy/) with one inequality on deviations, and the same bound then holds for pure Nash equilibria, mixed Nash equilibria, [correlated](/correlated-equilibrium/) and [coarse correlated equilibria](/coarse-correlated-equilibrium/), and the time averages of [no-regret dynamics](/no-regret-dynamics/). Roughgarden named it in 2009, after he saw that most known proofs of price of anarchy bounds had this form. The [no-regret convergence theorem](/no-regret-coarse-correlated-theorem/) says that no-regret play approaches the set of coarse correlated equilibria; this page says how good those outcomes are for the social cost. The [atomic linear congestion bound](/atomic-linear-congestion-price-of-anarchy/) is the main worked case of the method.

All games on this page are cost games: each player $i$ minimizes its cost $c_i(s)$, and the social cost is $C(s) = \sum_{i=1}^n c_i(s)$ for $n$ players. The price of anarchy of an equilibrium notion is the largest ratio $C(\text{outcome})/C(s^*)$ over its outcomes, where $s^*$ is an optimal profile, so it is at least 1.

## In plain words

To show that selfish play is never much worse than the best plan, look at one special move for each player: switch to what that player does in the best plan. If the total cost of these switches, each made while the others stay put, is at most a fixed multiple of the best cost plus a fraction of the current cost, then no stable state can be far from the best. The argument never asks which state the players are in, and never uses more than these single switches. So it also holds when the players mix at random, when a mediator suggests moves, and when the players learn over many rounds and keep the average cost low.

## When it applies

- The social cost is the sum of the player costs, or is at most that sum. Total latency, total delay and total cost are of this form; the makespan is not.
- There is a natural deviation $s_i^*$ for each player that does not depend on what the others do, usually the strategy of $i$ in an optimal profile.
- The cost of a deviation can be bounded resource by resource, as in congestion games, where a deviation changes each load by at most one unit.
- You want a bound that holds for every equilibrium notion at once, or for players who learn instead of reaching an equilibrium.

## The template

A cost game is $(\lambda, \mu)$-smooth, with $\lambda > 0$ and $0 \le \mu < 1$, if for every pair of profiles $s$ and $s^*$

$$\sum_{i=1}^n c_i(s_i^*, s_{-i}) \le \lambda\, C(s^*) + \mu\, C(s).$$

The robust price of anarchy of the game is the smallest value of $\lambda/(1 - \mu)$ over all pairs $(\lambda, \mu)$ for which the game is smooth.

```pseudo id=main
SMOOTHNESS-BOUND(class of games, outcome σ)            ▷ σ is a distribution on profiles
L1  fix an optimal profile s* of the game
L2  hole: prove Σ_i c_i(s_i*, s_-i) ≤ λ C(s*) + μ C(s) for every profile s   ▷ the per-resource inequality
L3  hole: check that 0 ≤ μ < 1 and C(s) = Σ_i c_i(s)
L4  for each player i: E_σ[c_i(s)] ≤ E_σ[c_i(s_i*, s_-i)]                ▷ the only use of equilibrium
L5  E_σ[C(s)] = Σ_i E_σ[c_i(s)] ≤ E_σ[Σ_i c_i(s_i*, s_-i)]
L6  E_σ[C(s)] ≤ λ C(s*) + μ E_σ[C(s)]                                    ▷ L2 inside the expectation
L7  return E_σ[C(s)] ≤ λ/(1 - μ) · C(s*)
```

Line L4 is the definition of a coarse correlated equilibrium, restricted to the one deviation $s_i^*$. A pure Nash equilibrium is a coarse correlated equilibrium with one profile. A mixed Nash equilibrium is one too: a mixed best response has its support inside the set of pure best responses, so each pure strategy in its support costs no more than $s_i^*$ against the others, and the product distribution meets L4. A correlated equilibrium is a coarse correlated equilibrium. So the chain

pure Nash $\subseteq$ mixed Nash $\subseteq$ correlated $\subseteq$ coarse correlated

gives the bound to all four, and the bound is the same number for all of them.

Line L6 needs the smoothness inequality at every profile $s$ in the support of $\sigma$, with the same $s^*$. That is why the deviation must not depend on $s$.

**No-regret play.** Let the players choose profiles $s^1, \dots, s^T$ and let player $i$ have external regret $R_i(T)$: its total cost is at most $R_i(T)$ more than the cost of the best fixed strategy in hindsight. For the fixed strategy $s_i^*$ this gives $\sum_t c_i(s^t) \le \sum_t c_i(s_i^*, s_{-i}^t) + R_i(T)$. Summing over $i$ and applying smoothness at each $s^t$,

$$\frac{1}{T} \sum_{t=1}^T C(s^t) \le \frac{\lambda}{1 - \mu}\, C(s^*) + \frac{\sum_i R_i(T)}{(1 - \mu)\, T}.$$

When each $R_i(T) = o(T)$, the second term goes to 0. The players do not need to converge to anything.

## Classic examples

1. **Atomic congestion games with affine costs.** For integers $y, z \ge 0$, $y(z + 1) \le \tfrac{5}{3} y^2 + \tfrac{1}{3} z^2$. Applied resource by resource, it gives $(5/3, 1/3)$-smoothness and the bound $5/2$, which is tight ([atomic linear congestion bound](/atomic-linear-congestion-price-of-anarchy/)).
2. **Nonatomic routing with affine latencies.** For one edge with $\ell(x) = ax + b$, $y\,\ell(x) \le y\,\ell(y) + \tfrac{1}{4} x\,\ell(x)$. A single particle cannot change a load, so the deviation inequality is replaced by the variational inequality of a [Wardrop equilibrium](/wardrop-equilibrium/). This local form gives $(1, 1/4)$ and the bound $4/3$ of [Roughgarden and Tardos](/roughgarden-tardos-four-thirds-bound/). The [Pigou bound](/pigou-bound/) extends it to other latency classes.
3. **Valid utility games (Vetta 2002).** These are payoff games with a submodular social welfare, such as competitive facility location. They are $(1, 1)$-smooth in the payoff form below, which gives the bound 2.
4. **Auctions.** The first-price auction is smooth in the mechanism form of Syrgkanis and Tardos, and the bound extends to Bayes-Nash equilibria with independent values ([first-price auction price of anarchy](/first-price-auction-price-of-anarchy/)).

### Example by hand

Two players each choose link $A$, with cost $c_A(x) = x$ for load $x$, or link $B$, with constant cost 2. The game is an affine congestion game, so it is $(5/3, 1/3)$-smooth.

| profile | costs | social cost |
|---|---|---|
| $(A, A)$ | 2, 2 | 4 |
| $(A, B)$ | 1, 2 | 3 |
| $(B, A)$ | 2, 1 | 3 |
| $(B, B)$ | 2, 2 | 4 |

The optimum is 3, at $s^* = (A, B)$. The profile $(A, A)$ is a pure Nash equilibrium: a player who moves to $B$ pays 2, which is not less. With $s = (A, A)$ the template reads $C(s) = 4 \le c_1(A, A) + c_2(B, A) = 2 + 2 = 4 \le \tfrac{5}{3} \cdot 3 + \tfrac{1}{3} \cdot 4 = \tfrac{19}{3}$.

Now let $\sigma$ put probability $1/3$ on each of $(A, A)$, $(A, B)$ and $(B, A)$. Player 1 pays $(2 + 1 + 2)/3 = 5/3$ on average. If it always plays $A$, the other plays $A$ with probability $2/3$, so it pays $1 + 2/3 = 5/3$. If it always plays $B$, it pays 2. Player 2 is symmetric. So $\sigma$ is a coarse correlated equilibrium, with expected social cost $10/3$. The ratios $4/3$ and $10/9$ are both below the bound $5/2$, as the framework says. The bound is for the whole class, and this small game does not reach it.

## Variations

- **Payoff games.** A payoff game with welfare $W(s) \ge \sum_i u_i(s)$ is $(\lambda, \mu)$-smooth if $\sum_i u_i(s_i^*, s_{-i}) \ge \lambda W(s^*) - \mu W(s)$. Then every coarse correlated equilibrium has expected welfare at least $\tfrac{\lambda}{1 + \mu} W(s^*)$, so the ratio is at most $(1 + \mu)/\lambda$.
- **Smooth mechanisms.** Syrgkanis and Tardos (2013) replace $\mu W(s)$ by $\mu$ times the revenue, and the deviation may depend on the bidder's own value. This gives bounds for Bayes-Nash equilibria and for several mechanisms run at the same time or one after the other.
- **Bayes-Nash equilibria.** Roughgarden (EC 2012) showed that smoothness of the complete-information game extends to [Bayes-Nash equilibria](/bayes-nash-equilibrium/) when the player types are independent.
- **Local smoothness.** Roughgarden and Schoppmann use only deviations that change the load a little. This fits nonatomic and splittable flows and gives tight bounds there. The extension to other equilibrium notions is more limited than for the global form.
- **Tightness.** For congestion games whose cost functions come from a class with mild closure conditions, Roughgarden proved that the best smoothness bound equals the worst price of anarchy of pure Nash equilibria. So in these classes the extension to coarse correlated equilibria costs nothing.

## Pitfalls

- **The objective must be a sum.** In the [load balancing game](/load-balancing-game/) the social cost is the makespan. On 2 identical machines with 2 unit jobs, every pure Nash equilibrium puts one job on each machine, which is optimal. The mixed equilibrium in which each job picks a machine at random has expected makespan $3/2$. So the pure and the mixed bounds differ, and no smoothness argument can give both ([price of anarchy of load balancing](/price-of-anarchy-of-load-balancing/)).
- **The deviation must not depend on $s$.** A proof that sends player $i$ to its best response against $s$ uses the equilibrium more strongly. It bounds pure Nash equilibria, but it need not bound the other notions.
- **$\mu$ must be below 1.** If $\mu \ge 1$ the inequality gives nothing in the cost form.
- **The bound is for a class.** For one game, the exact price of anarchy can be far lower, as in the example above.
- **The price of stability is a different question.** Smoothness bounds the worst outcome. The best equilibrium can be much better; for affine atomic congestion games the [price of stability](/price-of-stability/) is about $1.577$, not $5/2$.

## Exercises

1. For $\ell(x) = ax + b$ with $a, b \ge 0$ and $x, y \ge 0$, prove $y\,\ell(x) \le y\,\ell(y) + \tfrac{1}{4} x\,\ell(x)$. (Hint: $axy \le ay^2 + ax^2/4$.)
2. Derive the payoff bound $(1 + \mu)/\lambda$ from the payoff form of smoothness, following lines L4 to L7.
3. In the example by hand, find all pure Nash equilibria and the exact price of anarchy and price of stability of the game.
4. Show that the uniform distribution on $(A, B)$ and $(B, A)$ is a correlated equilibrium of the example, and give its cost.

## References
