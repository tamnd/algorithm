---
tag: 3741KV
kind: algorithm
slug: stackelberg-commitment-algorithm
name: Computing an optimal strategy to commit to
aliases:
- Conitzer-Sandholm multiple LPs algorithm
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Finds the leader's optimal mixed commitment in a two-player normal-form game by one linear program per follower action.
model: real-ram
complexity:
  vars: {m: the number of pure strategies of the leader, n: the number of pure strategies of the follower, L: the bit length of the payoffs}
  time: {worst: "poly(m, n, L)"}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2006
  people: [Vincent Conitzer, Tuomas Sandholm]
  note: Conitzer and Sandholm gave the multiple LPs method for two-player normal-form games and the hardness results for Bayesian games at the ACM Conference on Electronic Commerce in 2006.
prereqs: [bimatrix-game, best-response, linear-programming-problem, zero-sum-game-linear-programming]
see_also: [stackelberg-equilibrium, security-game, indifference-principle, nash-equilibrium-computation, bayesian-game, mixed-integer-programming, minimax-theorem, stackelberg-routing]
sources:
  - paper: doi:10.1145/1134707.1134717
    title: "Vincent Conitzer and Tuomas Sandholm, Computing the optimal strategy to commit to, Proceedings of the 7th ACM Conference on Electronic Commerce (EC 2006), 82-90"
    locator: the multiple LPs algorithm for two-player normal-form games and the NP-hardness for Bayesian games with several follower types
  - book: "Milind Tambe, Security and Game Theory, Algorithms, Deployed Systems, Lessons Learned, Cambridge University Press, 2011"
    title: Security and Game Theory
    locator: Stackelberg security games, strong Stackelberg equilibria and the algorithms used in deployed systems
---

This algorithm computes the best mixed strategy for a leader to commit to in a two-player game in normal form, when the follower sees the commitment and plays a best response. It solves one linear program for each pure strategy $j$ of the follower: among the mixed strategies to which $j$ is a best response, find the one that is best for the leader; then take the best of these. The solution concept, the [Stackelberg equilibrium](/stackelberg-equilibrium/), has its own page, and [security games](/security-game/) are the model in which this computation is used most, with a compact strategy space for the defender. [Stackelberg routing](/stackelberg-routing/) is a different use of the word, for a leader who controls part of the traffic in a network.

## In plain words

Suppose you must announce how you will randomize before the other player moves, and the other player will then do what is best for them. You can use this to your advantage: you choose your mix so that the reply you like is the one they want. For each possible reply, ask: among all mixes that make this reply a best choice for them, which mix is best for me? Each question is a small linear program. Answer all of them and keep the best. If the other player is indifferent between replies, assume they pick the one you prefer; this is the usual rule, and without it the best mix may not exist.

## The problem

Input: an $m \times n$ [bimatrix game](/bimatrix-game/) $(A, B)$, where the leader (row player) has $m$ pure strategies and payoffs $A$, and the follower (column player) has $n$ pure strategies and payoffs $B$. Here $m$ and $n$ count strategies, not players. The leader commits to $x \in \Delta_m$. The follower sees $x$ and plays a [best response](/best-response/) $j \in \arg\max_k (B^{\mathsf T} x)_k$; a pure best response always exists, and ties are broken in the leader's favor. Output: an $x$ and $j$ that maximize the leader's payoff $(A^{\mathsf T} x)_j$, which is a strong Stackelberg equilibrium.

## The algorithm

```pseudo id=main
OPTIMAL-COMMITMENT(A, B)
L1  for each column j = 1..n:
L2      LP_j: maximize Σ_i x_i A[i][j]
              subject to Σ_i x_i (B[i][k] - B[i][j]) ≤ 0 for every k ≠ j   ▷ j is a best response
                         Σ_i x_i = 1, x ≥ 0
L3      if LP_j is infeasible: skip j          ▷ no mixed strategy makes j a best response
L4      keep (value of LP_j, its solution x, j) if the value is the largest so far
L5  return the kept (value, x, j)
```

The constraints of LP_j describe the region of the simplex where $j$ is a best response. These regions cover the simplex, so at least one LP is feasible. Each region is a polytope, and the leader's payoff against $j$ is linear on it, so each LP has an optimum at a vertex of its region.

## Example

Let $A = \begin{pmatrix} 1 & 3 \\ 0 & 2 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$, with rows $U$, $D$ for the leader and columns $l$, $r$ for the follower. For the leader, $U$ strictly dominates $D$, so the only Nash equilibrium is $(U, l)$, with payoff 1 to the leader.

| LP | best response region | objective | optimum |
|---|---|---|---|
| $j = l$ | $x_D \le x_U$ | $x_U$ | $x = (1, 0)$, value 1 |
| $j = r$ | $x_U \le x_D$ | $3 x_U + 2 x_D$ | $x = (1/2, 1/2)$, value $5/2$ |

The algorithm returns $x = (1/2, 1/2)$ with the follower playing $r$: the follower is indifferent and breaks the tie for the leader, who gets $5/2$. Committing to the pure strategy $D$ gives 2, and the Nash equilibrium gives 1. The optimal commitment puts as much weight on $U$ as it can while $r$ stays a best response, which is an instance of the [indifference principle](/indifference-principle/) at the boundary of a region.

## Correctness

For every $x \in \Delta_m$, the follower's choice $j$ is a best response to $x$, so $x$ is feasible for LP_j, and the leader's payoff $(A^{\mathsf T} x)_j$ is at most the value of LP_j. So no commitment gives more than the largest LP value. Conversely, the optimal $x$ of the LP with the largest value makes $j$ a best response, and if the follower has another best response $k$ that is better for the leader, $x$ is also feasible for LP_k with a larger value, which is impossible. So with ties broken for the leader, the follower plays a column that gives the leader exactly the largest LP value. The proof file has the details, and also shows that this value is at least the leader's payoff in every Nash equilibrium.

## Complexity

The algorithm solves $n$ linear programs, each with $m$ variables and $n$ constraints, so the time is $n$ times the time of one LP. With a polynomial-time LP method this is polynomial in $m$, $n$ and the bit length $L$ of the payoffs. The code uses the exact [simplex method](/simplex-method/) with rational numbers. The space is $O(m n)$ for one LP at a time.

For comparison, finding a Nash equilibrium of a bimatrix game is [PPAD](/ppad/)-complete, so commitment is easier to compute than a Nash equilibrium of the same game.

## Properties

- **At least as good as any Nash equilibrium.** The leader's commitment value is at least the leader's payoff in every Nash equilibrium of $(A, B)$, and at least the value of the best pure commitment.
- **Zero-sum games.** If $B = -A$, the commitment value is the value of the game: committing to a maximin strategy is optimal, and the [minimax theorem](/minimax-theorem/) says the leader cannot do better.
- **Exact.** All LP data are rational, so the optimal $x$ is rational and the code finds it exactly.
- **Follower plays pure.** It is enough to consider pure best responses: a mixed best response is a mixture of pure ones and gives the leader at most the best of them.

## Variants and improvements

- **One LP.** The $n$ LPs can be merged into one LP over a correlated distribution of the pairs (leader action, follower action), with a best response constraint for each recommended follower action. For two players its value equals the best value of the $n$ LPs: in a feasible distribution, the leader's conditional strategy given each recommended follower action $j$ is feasible for LP_j, so the leader's payoff is an average of values that are each at most the best LP value.
- **Bayesian followers.** With several follower types and a prior over them, finding the optimal commitment is NP-hard (Conitzer and Sandholm). The usual exact method is a [mixed integer program](/mixed-integer-programming/) with one binary variable for each type and action, as in the DOBSS algorithm of Paruchuri and others; see [Bayesian games](/bayesian-game/).
- **Security games.** When the leader's pure strategies are allocations of $k$ resources to $T$ targets, $m$ is exponential, but the payoffs depend only on the coverage of each target, so the LPs can be written with $T$ coverage variables; see [security games](/security-game/).
- **Weak Stackelberg.** If the follower breaks ties against the leader, the supremum of the leader's payoff need not be attained. The strong value can be approached from inside a region by moving slightly away from its boundary, where the follower's best response is unique.

## When to use it

Use it when one player can credibly announce a randomized policy before the other acts, as in patrols, inspections, audits and screening, and the game is given in normal form with a modest number of actions for both players. For many follower types or compact strategy spaces, use the MIP and security game methods instead.

## Pitfalls

- **Tie-breaking.** The optimum usually makes the follower indifferent between two or more actions, so the tie rule matters. In practice the leader moves a little into the region of the preferred action, at a small loss, so that the follower's best response is strict.
- **Leader's payoffs, follower's constraints.** The objective of LP_j uses $A$ and the constraints use $B$; mixing them up gives the follower's commitment problem instead.
- **Not a Nash equilibrium.** The pair $(x, j)$ need not be a Nash equilibrium of the simultaneous game: in the example, the leader's commitment $x = (1/2, 1/2)$ is not a best response to $r$.
- **Commitment must be credible.** The model assumes the follower observes the mixed strategy, or learns it over time, but not the outcome of the randomization before acting.

## Implementations

The Python code builds LP_j for each column and solves it with the shared exact simplex code. A helper computes the follower's best response with ties broken for the leader. The tests check the example above, an infeasible LP for a dominated column, and the tie rule. On 150 random games, the result is compared with a brute-force search over the vertices of all best response regions. The tests also check that the commitment value is at least every Nash equilibrium payoff found by support enumeration and every pure commitment, and that it equals the minimax value on 100 random zero-sum games.

## History

Heinrich von Stackelberg studied leader-follower competition in markets in 1934, with pure strategies. Conitzer and Sandholm (2006) gave the multiple LPs algorithm for mixed commitments in two-player normal-form games and showed that the problem is NP-hard for Bayesian games with several follower types. Mixed integer programs for Bayesian followers and compact programs for resource allocation followed, and were used in deployed security systems; see [security games](/security-game/).

## References
