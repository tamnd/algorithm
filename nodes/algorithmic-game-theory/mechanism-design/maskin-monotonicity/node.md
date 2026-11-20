---
tag: 0YT05D
kind: theorem
slug: maskin-monotonicity
name: "Maskin's theorem"
aliases:
- Maskin monotonicity
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: A social choice rule implementable in Nash equilibrium must be Maskin monotonic, and with three or more agents and no veto power that suffices.
prereqs: [nash-equilibrium, preference-profile]
see_also: [gibbard-satterthwaite-theorem, revelation-principle, plurality-voting, pareto-optimality, subgame-perfect-equilibrium, arrow-impossibility-theorem, dominant-strategy-incentive-compatibility, bayesian-incentive-compatibility]
sources:
  - paper: doi:10.1111/1467-937X.00076
    title: "Eric Maskin, Nash equilibrium and welfare optimality, Review of Economic Studies 66(1) (1999), 23-38 (circulated as an MIT working paper in 1977)"
    locator: the necessity of monotonicity and its sufficiency with no veto power for three or more agents
  - paper: doi:10.1007/bf00433954
    title: "Rafael Repullo, A simple proof of Maskin's theorem on Nash implementation, Social Choice and Welfare 4(1) (1987), 39-41"
    locator: the mechanism with an integer game used in the proof of sufficiency
  - paper: doi:10.2307/2938301
    title: "John Moore and Rafael Repullo, Nash implementation: a full characterization, Econometrica 58(5) (1990), from p. 1083"
    locator: the necessary and sufficient condition for Nash implementation, including the case of two agents
---

Maskin's theorem says which social choice rules can be implemented in Nash equilibrium: a designer who does not know the agents' preferences, while the agents know each other's, wants a game whose Nash equilibrium outcomes are exactly the outcomes the rule selects, at every preference profile. The theorem gives a necessary condition, Maskin monotonicity: if an outcome is chosen and then no agent ranks it lower relative to any other outcome, it must still be chosen. With three or more agents, monotonicity and a weak condition called no veto power are also sufficient. This setting of complete information among the agents differs from the private-information setting of [dominant-strategy](/dominant-strategy-incentive-compatibility/) and [Bayesian](/bayesian-incentive-compatibility/) implementation.

## Statement

There is a set $N = \{1, \ldots, n\}$ of agents and a set $A$ of outcomes. A [preference profile](/preference-profile/) $R = (R_1, \ldots, R_n)$ gives each agent a weak order $R_i$ on $A$; $a\, R_i\, b$ means that agent $i$ finds $a$ at least as good as $b$, and $P_i$ is the strict part. The profiles come from a domain $\mathcal{R}$. A social choice rule $F$ assigns to each $R \in \mathcal{R}$ a nonempty set $F(R) \subseteq A$. The lower contour set of $a$ for agent $i$ is $L_i(a, R_i) = \{b \in A : a\, R_i\, b\}$.

A mechanism is a pair $(M, g)$ with message sets $M = M_1 \times \cdots \times M_n$ and an outcome function $g : M \to A$. At the profile $R$, a message profile $m$ is a [Nash equilibrium](/nash-equilibrium/) if $g(m)\, R_i\, g(m_i', m_{-i})$ for every $i$ and every $m_i' \in M_i$. The mechanism implements $F$ in Nash equilibrium if, for every $R \in \mathcal{R}$, the set of outcomes of the Nash equilibria at $R$ is exactly $F(R)$.

- $F$ is **Maskin monotonic** if, whenever $a \in F(R)$ and $L_i(a, R_i) \subseteq L_i(a, R_i')$ for every agent $i$, also $a \in F(R')$.
- $F$ satisfies **no veto power** if, whenever $a$ is a top outcome under $R_j$ for at least $n - 1$ agents $j$, then $a \in F(R)$.

**Theorem (Maskin).**

1. If $F$ is implementable in Nash equilibrium, then $F$ is Maskin monotonic.
2. If $n \ge 3$ and $F$ is Maskin monotonic and satisfies no veto power, then $F$ is implementable in Nash equilibrium.

### Example

Plurality voting with ties kept as a set is not Maskin monotonic, so no mechanism implements it in Nash equilibrium. Take three voters and the outcomes $a, b, c$.

| voter | profile $R$ | profile $R'$ |
|---|---|---|
| 1 | $a > b > c$ | $a > b > c$ |
| 2 | $b > c > a$ | $c > b > a$ |
| 3 | $c > b > a$ | $c > b > a$ |

At $R$ each outcome has one first place, so $F(R) = \{a, b, c\}$. At $R'$, $c$ has two first places, so $F(R') = \{c\}$. Voters 1 and 3 do not change. Voter 2 has $a$ at the bottom in both profiles, so $L_2(a, R_2) = L_2(a, R_2') = \{a\}$. No lower contour set of $a$ shrinks, and monotonicity would ask $a \in F(R')$, which fails.

The weak Pareto rule, which keeps every outcome $a$ such that no $b$ is strictly better than $a$ for all agents, is Maskin monotonic and has no veto power, so it is implementable when $n \ge 3$. If $b\, P_i'\, a$ for all $i$ at $R'$, then $b \notin L_i(a, R_i')$, so $b \notin L_i(a, R_i)$ and $b\, P_i\, a$ for all $i$ at $R$. So $a$ was not weakly Pareto at $R$ either.

## In plain words

A planner wants a fair choice, but only the people know their tastes, and they all know each other's tastes. The planner sets up a game and hopes that its stable outcomes are exactly the fair ones. Maskin found a test that every such rule must pass. Suppose an option is chosen. Then tastes change, but nobody likes that option less compared with anything else. The option must still be chosen. The reason is simple: the old stable play is still stable, because no one found a better move before and no one finds one now. With three or more people, this test plus one mild extra condition is also enough to build the game.

## Proof

**Part 1.** Let $(M, g)$ implement $F$, and let $a \in F(R)$ and $L_i(a, R_i) \subseteq L_i(a, R_i')$ for every $i$. Since $a \in F(R)$, there is a Nash equilibrium $m$ at $R$ with $g(m) = a$. Take any agent $i$ and any $m_i'$, and let $b = g(m_i', m_{-i})$. Because $m$ is an equilibrium at $R$, $a\, R_i\, b$, so $b \in L_i(a, R_i) \subseteq L_i(a, R_i')$, that is $a\, R_i'\, b$. So no agent gains by a deviation at $R'$ either, $m$ is a Nash equilibrium at $R'$, and its outcome $a$ is in $F(R')$.

**Part 2.** This is Repullo's mechanism. A message of agent $i$ is a triple $m_i = (R^i, a^i, k^i)$ of a profile $R^i \in \mathcal{R}$, an outcome $a^i \in A$ and an integer $k^i \ge 0$. Call a message $(R, a, k)$ valid if $a \in F(R)$. The outcome function has three rules.

1. If all agents send the same valid message $(R, a, k)$, the outcome is $a$.
2. If all agents except one agent $i$ send the same valid message $(R, a, k)$, and $m_i$ is different, the outcome is $a^i$ if $a^i \in L_i(a, R_i)$, and $a$ otherwise.
3. In every other case, the outcome is $a^j$ for the agent $j$ with the largest integer $k^j$, with ties broken by the smallest index.

Since $n \ge 3$, the agent $i$ in rule 2 is unique, so $g$ is well defined. In rule 2, the odd agent can get exactly the outcomes in $L_i(a, R_i)$, the lower contour set of $a$ in the reported profile.

Let $R$ be the true profile.

*Every $a \in F(R)$ is an equilibrium outcome.* Let all agents send $(R, a, 0)$. Rule 1 gives $a$. A deviation by agent $i$ moves to rule 2, since the other $n - 1 \ge 2$ agents still agree, and gives an outcome in $L_i(a, R_i)$, which $i$ does not prefer to $a$. So this is a Nash equilibrium with outcome $a$.

*Every equilibrium outcome is in $F(R)$.* Let $m$ be a Nash equilibrium at $R$ with outcome $a$.

- If $m$ is in rule 1, all agents send $(R', a, k)$ with $a \in F(R')$. Each agent $i$ can deviate to $(R', b, k + 1)$ and get any $b \in L_i(a, R_i')$ by rule 2. As $m$ is an equilibrium, $a\, R_i\, b$ for all such $b$, so $L_i(a, R_i') \subseteq L_i(a, R_i)$ for every $i$. Maskin monotonicity, applied from $R'$ to $R$, gives $a \in F(R)$.
- If $m$ is in rule 2 with odd agent $i$, take any $j \ne i$ and any outcome $b$. Agent $j$ can send $(R^j, b, K)$ with $K$ larger than all the integers in $m$. Now no $n - 1$ agents send the same message, because $j$'s message differs from all others and $i$'s message differs from the remaining agents' message. So rule 3 applies and gives $b$. As $m$ is an equilibrium, $a\, R_j\, b$ for every $b$. So $a$ is a top outcome for all $n - 1$ agents $j \ne i$, and no veto power gives $a \in F(R)$.
- If $m$ is in rule 3, then for every agent $j$ the messages $m_{-j}$ are not all equal to one valid message, or $m$ would be in rule 1 or 2. So agent $j$ can send $(R^j, b, K)$ with a large $K$ and stay in rule 3, and get any $b$. Then $a$ is a top outcome for every agent, and no veto power gives $a \in F(R)$.

So the Nash equilibrium outcomes at $R$ are exactly $F(R)$. $\blacksquare$

## Consequences

- **Strong limits for functions.** If $F$ is single-valued, the domain holds all strict orders, $|A| \ge 3$ and $F$ is onto, then Maskin monotonicity forces $F$ to be dictatorial (Muller and Satterthwaite, 1977). This is close to the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/): Nash implementation of a single-valued rule on the full domain is no easier than implementation in dominant strategies.
- **Correspondences do much better.** Many natural correspondences are Maskin monotonic and have no veto power, for example the weak Pareto rule, and in exchange economies the Walrasian rule, with some care at the boundary of the consumption sets. All of these are implementable in Nash equilibrium with three or more agents.
- **Voting rules fail.** [Plurality voting](/plurality-voting/), used as a correspondence, is not Maskin monotonic, as the example shows, so it is not implementable in Nash equilibrium. Other scoring rules, such as the Borda count, fail in the same way.
- **Refinements help.** Implementation in [subgame perfect equilibrium](/subgame-perfect-equilibrium/) with sequential mechanisms, and implementation in undominated strategies, can reach rules that are not monotonic. This is one reason why the theory moved to refinements after Maskin's result.

## Tightness

- **Monotonicity is not sufficient alone.** With $n = 2$, a monotonic rule need not be implementable. Moore and Repullo (1990) and Dutta and Sen (1991) give the exact conditions for two agents, which add requirements to monotonicity.
- **No veto power is not necessary.** A constant rule $F(R) = \{a\}$ is implemented by the mechanism whose outcome is always $a$, yet it fails no veto power when all agents put another outcome first. Moore and Repullo (1990) give a condition that is both necessary and sufficient for $n \ge 3$.
- **The mechanism is not practical.** The integer game in rule 3 has no equilibrium, and it is used only to rule out unwanted equilibria. Jackson (1992) and others criticized such constructions. Later work gives bounded mechanisms under extra assumptions, but the general theorem needs an infinite message space or a similar device.

## History

Maskin proved the theorem in an MIT working paper in 1977, which was widely cited and published in 1999. Repullo gave the short proof with the integer game in 1987, and Saijo, Williams and others reduced the size of the message space. Moore and Repullo found the full characterization in 1990, and Dutta and Sen handled two agents in 1991. Maskin received the 2007 Nobel Memorial Prize in Economic Sciences with Hurwicz and Myerson, for work that includes this result.

## References
