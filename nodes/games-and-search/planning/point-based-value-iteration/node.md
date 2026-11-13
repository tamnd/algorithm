---
tag: M7E96B
kind: algorithm
slug: point-based-value-iteration
name: Point-based value iteration
aliases:
- PBVI
area: games-and-search/planning
level: research
summary: Approximate POMDP planning that keeps one alpha vector for each belief of a finite set, backs up only at these beliefs, and grows the set by simulation. Its values are lower bounds.
solves: [pomdp-planning]
model: real-ram
complexity:
  vars: {S: the number of states, A: the number of actions, Z: the number of observations, B: the number of beliefs in the set (the time bound is for one sweep)}
  time: {worst: "O(A Z B S^2 + A Z B^2 S)"}
  space: {extra: O(B S)}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 2003
  people: [Joelle Pineau, Geoffrey Gordon, Sebastian Thrun]
  note: Pineau, Gordon and Thrun introduced PBVI at IJCAI 2003 as an anytime POMDP solver, with point backups, belief expansion by simulation and an error bound in the density of the belief set.
prereqs: [pomdp-planning, belief-space, value-iteration]
see_also: [pomdp, real-time-dynamic-programming, monte-carlo-tree-search, particle-filter, mdp-planning, bellman-contraction, stochastic-shortest-path]
sources:
  - paper: "Joelle Pineau, Geoffrey Gordon and Sebastian Thrun, Point-based value iteration: an anytime algorithm for POMDPs, Proceedings of IJCAI 2003"
    locator: pp. 1025 to 1032 (the point backup, the expansion of the belief set and the error bound)
  - paper: "Joelle Pineau, Geoffrey Gordon and Sebastian Thrun, Anytime point-based approximations for large POMDPs, Journal of Artificial Intelligence Research 27, 2006"
    locator: pp. 335 to 380, Section 2.4 with Table 1 (the cost of exact and point-based backups), Section 3 with Lemma 1 and Theorem 3.1 (the error bound) and Section 4 (the ways to expand the belief set)
  - paper: doi:10.1016/S0004-3702(98)00023-X
    title: Leslie Pack Kaelbling, Michael L. Littman and Anthony R. Cassandra, Planning and acting in partially observable stochastic domains, Artificial Intelligence 101(1-2), 1998
    locator: pp. 99 to 134 (alpha vectors, policy trees and the tiger problem)
  - paper: doi:10.1287/opre.21.5.1071
    title: Richard D. Smallwood and Edward J. Sondik, The optimal control of partially observable Markov processes over a finite horizon, Operations Research 21(5), 1973
    locator: pp. 1071 to 1088 (the value as a maximum of linear functions of the belief)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 7.3 (approximate and online algorithms for POMDPs)
---

Point-based value iteration (PBVI) is an approximate method for [POMDP planning](/pomdp-planning/). The optimal finite-horizon value of a POMDP is the maximum of a set of linear functions of the belief, the alpha vectors, and exact value iteration builds all the vectors that are best somewhere in the [belief space](/belief-space/). That set can grow exponentially at each step. PBVI keeps a finite set $B$ of beliefs and computes one vector for each of them. The backup at a belief is exact at that belief, and each vector is the value of a real plan, so the result is a lower bound on the optimal value. PBVI grows $B$ by simulation from the start belief, and the error is bounded by the distance from the reachable beliefs to $B$ (Pineau, Gordon and Thrun 2003).

## In plain words

A plan for a robot with noisy sensors must say what to do for every state of knowledge the robot can have, and there are too many of them. PBVI picks a few typical states of knowledge and finds a good plan for each one. Each plan also gives an answer for the other states of knowledge, and the robot uses the best of these answers.

To find the plans, PBVI improves them again and again, like value iteration, but it does the work only at the chosen points. To choose the points, it imagines the robot acting from the start, and adds the states of knowledge that the robot reaches and that are far from the points it already has. More points give a better answer and cost more time.

## The problem

The input is a POMDP $(S, A, \Omega, P, O, R, \gamma)$ with finite sets, as on the [POMDP](/pomdp/) page, and a start belief $b_0$. For a finite horizon $H$, the aim is the optimal value $V_H$ and a policy. For $\gamma < 1$, the aim is $V^*$. Both are piecewise linear and convex: $V(b) = \max_{\alpha \in \Gamma} \alpha \cdot b$ for a finite set $\Gamma$ (for $V^*$, only in the limit). PBVI returns a set $\Gamma$ of at most $|B|$ vectors, and the policy that at $b$ takes the action stored with the best vector.

## The algorithm

For a vector $\alpha$, an action $a$ and an observation $o$, let $g^\alpha_{a,o}(s) = \sum_{s'} P(s' \mid s, a) \, O(o \mid a, s') \, \alpha(s')$. This is the value of "do $a$, see $o$, then follow the plan of $\alpha$", without the first reward. $\Gamma_0$ is $\{0\}$ for a finite horizon, or the vector $R_{\min}/(1-\gamma)$ in each entry for a discounted problem.

```pseudo id=main
PBVI(M, b0, E, K, Γ)                             ▷ E expansions, K sweeps per round
L1  B ← {b0}
L2  repeat E + 1 times
L3      repeat K times: Γ ← { BACKUP(Γ, b) : b ∈ B }
L4      if this is not the last round then B ← EXPAND(B)
L5  return Γ

BACKUP(Γ, b)
L6  for each a ∈ A and o ∈ Ω: g_{a,o} ← the g^α_{a,o}, α ∈ Γ, of largest b · g^α_{a,o}
L7      α_a ← R(·, a) + γ Σ_o g_{a,o}
L8  return the α_a of largest b · α_a, with its action a

EXPAND(B)
L9  for each b ∈ B: for each a ∈ A, sample s ~ b, s' ~ P(· | s, a), o ~ O(· | a, s') and form b^{a,o}
L10     add to B the b^{a,o} that is farthest from B in L1 distance, if it is not in B
```

Line L6 picks, for each observation, the old vector that is best after that observation from $b$. The choices for different observations do not depend on each other, because $b \cdot \sum_o g_{a,o} = \sum_o b \cdot g_{a,o}$. So the backup at $b$ needs one maximum for each pair $(a, o)$, and not the maximum over all $|\Gamma|^{|\Omega|}$ combinations that exact value iteration builds. Line L3 replaces $\Gamma$ with the new vectors. Two beliefs can give the same vector, so $|\Gamma| \le |B|$.

Line L9 is the stochastic simulation with exploratory action of Pineau, Gordon and Thrun. Each belief tries each action once by simulation. Line L10 keeps the successor that is farthest from the set, so $B$ spreads over the reachable part of the simplex. At most $|B|$ beliefs are added in one expansion, so $B$ can double.

## Example

The tiger problem of the [POMDP](/pomdp/) page, with no discount: listen costs 1 and is correct with probability $17/20$; opening the right door gives 10, and opening the tiger door gives $-100$. A belief is the probability $p$ that the tiger is on the left. The exact values at $p = 1/2$ are $V_1, V_2, V_3, V_4 = -1, -2, 68/25, 1937/800$. The table gives the PBVI value at $p = 1/2$ after $k$ sweeps, from $\Gamma_0 = \{0\}$, for three fixed sets $B$.

| the set $B$ | $k = 1$ | $k = 2$ | $k = 3$ | $k = 4$ |
|---|---|---|---|---|
| $\{1/2\}$ | $-1$ | $-2$ | $-3$ | $-4$ |
| $\{1/2, 17/20, 3/20\}$ | $-1$ | $-2$ | $-3$ | $-4$ |
| $\{1/2, 17/20, 3/20, 289/298, 9/298\}$ | $-1$ | $-2$ | $68/25$ | $1937/800$ |

With $B = \{1/2\}$, every backup picks listen, and PBVI only knows the plan "listen for ever". Adding the beliefs after one listen does not help. At $p = 17/20$, opening the right door has the value $17/20 \cdot 10 - 3/20 \cdot 100 = -13/2$ with one step to go, which is worse than listening, so no vector for opening is made. The beliefs $289/298$ and $9/298$ come after two listens that agree. There, opening the door is best with one step to go: $(289 \cdot 10 - 9 \cdot 100)/298 = 995/149 \approx 6.68$. With these two points, PBVI has the vectors for opening, and it finds the optimal plan from $1/2$: listen twice, and open the door opposite the sound if both sounds agree. The third set contains every belief that $1/2$ reaches by listening at most twice, and the values for $k = 3$ and $k = 4$ are exact.

From $p = 1/2$, the expansion of line L9 cannot add a belief after opening a door, because opening resets the belief to $1/2$, which is in $B$ already. So the first expansion adds $17/20$ or $3/20$, whichever sound the simulation draws.

## Correctness

Three facts hold, and the proof of each is below. First, the vector of BACKUP$(\Gamma, b)$ has the value $(H V_\Gamma)(b)$ at $b$, where $H$ is the exact Bellman backup of the belief MDP and $V_\Gamma(b) = \max_{\alpha \in \Gamma} \alpha \cdot b$. Second, each vector that PBVI makes is the value vector of a plan: do $a$, and after $o$ follow the plan of the vector that line L6 chose. So $V_\Gamma \le V_k$ after $k$ sweeps on the whole simplex, and $V_\Gamma \le V^*$ in the discounted case from the start $R_{\min}/(1-\gamma)$. Third, if $B$ contains every belief that $b_0$ reaches in fewer than $H$ steps, then $H$ sweeps give $V_H(b_0)$ exactly.

For the discounted case with a fixed $B$, Pineau, Gordon and Thrun bound the error. Let $\delta_B$ be the largest L1 distance from a reachable belief to the nearest point of $B$. Then the error after convergence is at most $(R_{\max} - R_{\min}) \, \delta_B / (1 - \gamma)^2$ on the reachable beliefs.

## Complexity

Each sweep first computes the projections $g^\alpha_{a,o}$ for all $\alpha \in \Gamma$, $a$ and $o$. There are $|A||\Omega||\Gamma|$ of them, and each costs $O(|S|^2)$. Then each belief of $B$ takes, for each $(a, o)$, the maximum of $|\Gamma|$ dot products of length $|S|$. With $|\Gamma| \le |B|$ this gives

$$O(|A||\Omega||B||S|^2 + |A||\Omega||B|^2|S|)$$

time for one sweep, which is polynomial in the size of the model and of $B$. An exact backup can make $|A||\Gamma|^{|\Omega|}$ vectors before pruning, and needs a linear program to prune each of them. The space is $O(|B||S|)$ for the vectors and the beliefs, plus the projections. The implementation computes the projections again for each belief, which is simpler and slower by a factor of $|B|$ in the first term.

An expansion costs $O(|B||A|(|S|^2 + |B||S|))$, for the updates and the distances. The number of rounds sets the size of $B$, and $|B|$ can double in each round.

## Properties

- **Lower bound.** Each vector is the value of a plan, so $V_\Gamma$ is a lower bound on the optimal value at every belief, not only at the points of $B$.
- **Anytime.** After each sweep and each expansion, $\Gamma$ gives a policy and a valid lower bound. More expansions give a denser $B$ and a smaller error bound.
- **Bounded size.** $|\Gamma| \le |B|$, so the value function never grows beyond the size of the belief set.
- **Focused on reachable beliefs.** Expansion from $b_0$ puts $B$ where the policies go. Beliefs that no policy reaches from $b_0$ need no point.
- **No guaranteed rise.** Nothing in the method makes the value at a point of $B$ rise in each sweep, since the new vector at $b$ is built from vectors that were chosen at other points. Keeping the old vector when it is better at $b$ makes the values at $B$ non-decreasing.

## Variants and improvements

- **Other expansions.** Pineau, Gordon and Thrun also study random beliefs, and successors chosen greedily by the error bound. Each choice trades time against coverage.
- **Randomized point-based backups.** Perseus backs up beliefs of $B$ in random order, and stops a sweep when no belief of $B$ has a lower value than before, so one vector often serves many points.
- **Search with two bounds.** HSVI and SARSOP keep an upper bound as well as the lower bound, and choose the beliefs by search from $b_0$ where the gap between the bounds is large. The gap at $b_0$ gives a stopping rule.
- **Grids.** Older methods put the beliefs on a fixed grid of the simplex and interpolate. A grid grows exponentially in the number of states.
- **Online planning.** Methods such as POMCP do no offline work and search from the current belief with samples, as in [Monte Carlo tree search](/monte-carlo-tree-search/). A PBVI lower bound can serve as a value at the leaves of such a search.

## When to use it

Use PBVI when the POMDP is too large for exact value iteration but small enough to write the vectors over $S$, from tens to thousands of states, and when a policy is needed before acting. Use it when a lower bound is useful, for example to compare with a heuristic upper bound. If the start belief is known and only a short horizon matters, search from the current belief may be simpler. If the model has many state variables, use a factored or sampled method, because a vector over $S$ is then too large.

## Pitfalls

- **Missing key beliefs.** If $B$ has no belief where an important action is best, no vector for that action is made. In the tiger example, the points after one listen are not enough.
- **Duplicate beliefs in floating point.** The same belief can arrive with small rounding errors and be added twice. Use a tolerance in the distance test of line L10, or exact arithmetic.
- **The start vectors.** With $\gamma < 1$, start from $R_{\min}/(1-\gamma)$, not from 0. The zero vector is not a lower bound when rewards are negative, and then the values are not lower bounds.
- **Reading the error bound.** The bound uses the distance from every reachable belief to $B$. A set $B$ that is dense near $b_0$ but misses far beliefs that good policies reach can still give a large error.
- **Projections for each belief.** Computing $g^\alpha_{a,o}$ again for each belief multiplies the cost. Compute them once per sweep.

## Implementations

## History

Sondik (1971) and Smallwood and Sondik (1973) showed that the finite-horizon value of a POMDP is piecewise linear and convex, and that the gradient at a belief can be computed by a backup at that belief. Exact algorithms, from enumeration to the witness algorithm and incremental pruning in the 1990s, build the whole set of useful vectors. Pineau, Gordon and Thrun (2003) restricted the backups to a set of beliefs grown by simulation, proved the error bound in the density of the set, and called the method PBVI. Their 2006 paper in JAIR gives the full analysis. Later point-based methods, among them Perseus, HSVI and SARSOP, changed how the beliefs are chosen and backed up.

## References
