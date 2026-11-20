---
tag: SW1NKP
kind: definition
slug: best-response
name: Best response
aliases:
- best reply
area: algorithmic-game-theory/strategic-games
level: intro
summary: A strategy that gives a player the highest payoff against fixed strategies of the other players.
prereqs: [normal-form-game, mixed-strategy]
see_also: [nash-equilibrium, dominant-strategy, iterated-elimination-of-dominated-strategies, best-response-dynamics, best-response-polytope, kakutani-fixed-point-theorem, robinson-fictitious-play-theorem, indifference-principle]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (the best-response function and Nash equilibrium as its fixed point) and Chapter 4 (never-best responses and strictly dominated actions)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (best response and Nash equilibrium)
  - paper: doi:10.1073/pnas.36.1.48
    title: "John F. Nash, Equilibrium points in n-person games, Proceedings of the National Academy of Sciences 36(1) (1950), 48-49"
    locator: the correspondence of best responses and its fixed point
  - paper: "David G. Pearce, Rationalizable strategic behavior and the problem of perfection, Econometrica 52(4) (1984), 1029-1050"
    title: Rationalizable strategic behavior and the problem of perfection
    locator: the lemma that a strategy is never a best response if and only if a mixed strategy strictly dominates it
---

A best response of a player is a strategy that gives the player the highest payoff when the strategies of the other players are held fixed. A [Nash equilibrium](/nash-equilibrium/) is a profile in which every player plays a best response to the others, so best responses are the building block of equilibrium, of [dominance](/dominant-strategy/) and of learning rules such as [best-response dynamics](/best-response-dynamics/). A dominant strategy is a best response to every profile of the others, while a best response is optimal against one given profile only.

## Definition

Let $G = (N, (S_i), (u_i))$ be a finite [normal-form game](/normal-form-game/) and let $\sigma_{-i}$ be a profile of [mixed strategies](/mixed-strategy/) of the players other than $i$. The set of *pure best responses* of player $i$ to $\sigma_{-i}$ is

$$\mathrm{BR}_i(\sigma_{-i}) = \arg\max_{s_i \in S_i} u_i(s_i, \sigma_{-i}).$$

It is nonempty because $S_i$ is finite. A mixed strategy $\sigma_i$ is a *best response* to $\sigma_{-i}$ if $u_i(\sigma_i, \sigma_{-i}) \ge u_i(\sigma_i', \sigma_{-i})$ for every $\sigma_i' \in \Delta(S_i)$. It is a *strict* best response if the inequality is strict for every $\sigma_i' \ne \sigma_i$; a strict best response is pure.

**The support condition.** $\sigma_i$ is a best response to $\sigma_{-i}$ if and only if its support is inside $\mathrm{BR}_i(\sigma_{-i})$.

*Proof.* Let $v = \max_{s_i} u_i(s_i, \sigma_{-i})$. By linearity, $u_i(\sigma_i, \sigma_{-i}) = \sum_{s_i} \sigma_i(s_i)\, u_i(s_i, \sigma_{-i}) \le v$, with equality exactly when every $s_i$ with $\sigma_i(s_i) > 0$ has $u_i(s_i, \sigma_{-i}) = v$. A pure strategy reaches $v$, so the best responses are exactly the mixed strategies that reach $v$. $\square$

So the mixed best responses form the face $\Delta(\mathrm{BR}_i(\sigma_{-i}))$ of the simplex. This is why a claimed equilibrium is checked with pure deviations only: $\sigma$ is a Nash equilibrium if and only if $u_i(\sigma) \ge u_i(s_i', \sigma_{-i})$ for every player $i$ and every $s_i' \in S_i$.

**The best-response correspondence.** $B_i(\sigma_{-i}) = \Delta(\mathrm{BR}_i(\sigma_{-i}))$ maps each profile of the others to a set of mixed strategies, and $B(\sigma) = B_1(\sigma_{-1}) \times \cdots \times B_n(\sigma_{-n})$. A profile $\sigma$ is a Nash equilibrium if and only if $\sigma \in B(\sigma)$, a fixed point of $B$. Each $B(\sigma)$ is nonempty, convex and compact, and the graph $\{(\sigma, \tau) : \tau \in B(\sigma)\}$ is closed: if $\sigma^k \to \sigma$, $\tau^k \to \tau$ and $u_i(\tau^k_i, \sigma^k_{-i}) \ge u_i(s_i', \sigma^k_{-i})$ for all $k$ and $s_i'$, then the same inequalities hold in the limit, because $u_i$ is a polynomial. These are the hypotheses of the [Kakutani fixed point theorem](/kakutani-fixed-point-theorem/), and Nash's 1950 proof of [existence](/nash-existence-theorem/) applies it to $B$. The correspondence is not continuous in general: the set of best responses jumps where a player is indifferent.

**Cost of a best response.** In a game given as a table with $n$ players, the values $u_i(s_i, \sigma_{-i})$ for all $s_i$ come from one pass over the $|S|$ profiles, with $n$ multiplications per profile. Against a pure profile $s_{-i}$, it takes $|S_i|$ lookups.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Chicken.** Each driver can dare (D) or chicken out (C).

| | D | C |
| --- | --- | --- |
| D | 0, 0 | 7, 2 |
| C | 2, 7 | 6, 6 |

If the column player chickens out with probability $q$, the row player gets $7q$ from D and $2 + 4q$ from C. So $\mathrm{BR}_1 = \{D\}$ for $q > 2/3$, $\{C\}$ for $q < 2/3$, and $\{D, C\}$ at $q = 2/3$, where every mix is a best response. The best response falls from "always D" to "always C" as $q$ crosses $2/3$. The game is symmetric, and the three points where the two best-response graphs meet are the three equilibria: (D, C), (C, D) and the mixed profile in which both chicken out with probability $2/3$.

**Prisoner's dilemma.** With payoffs (C, C) = (3, 3), (C, D) = (0, 5), (D, C) = (5, 0) and (D, D) = (1, 1), defecting gives the row player 2 more than cooperating against C and 1 more against D. So D is the unique best response to every mixed strategy of the other player: it is a [dominant strategy](/dominant-strategy/).

**A mix that is not a best response.** In the battle of the sexes, with $A = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ for the row player, let the column player be uniform, $y = (1/2, 1/2)$. Then Opera gives 1 and Football gives $1/2$, so $\mathrm{BR}_1 = \{\text{Opera}\}$. The mix $x = (2/3, 1/3)$ gives $5/6 < 1$: its support contains Football, which is not a best response. Against $y = (1/3, 2/3)$ instead, both rows give $2/3$, and every $x$ is a best response.

**Non-example: a safe strategy.** A maximin strategy maximizes the worst case $\min_{s_{-i}} u_i(\sigma_i, s_{-i})$, not the payoff against a given $\sigma_{-i}$. In the battle of the sexes, the row player's maximin mix plays Opera with probability $1/3$ and guarantees $2/3$; against the column player's maximin mix, which plays Opera with probability $2/3$, it gets $2/3$ while Opera gets $4/3$. Only in [zero-sum games](/zero-sum-game/) do the maximin strategies form an equilibrium ([minimax theorem](/minimax-theorem/)).

**Never a best response.** In a game where the row player's three rows pay $(3, 0)$, $(0, 3)$ and $(1, 1)$ against two columns, row 3 is a best response to no column mix, since the better of rows 1 and 2 gives at least $3/2$. It is strictly dominated by the mix $(1/2, 1/2, 0)$. Pearce (1984) proved that in two-player games these two properties are the same: a pure strategy is never a best response to any mixed strategy of the opponent if and only if some mixed strategy strictly dominates it. The proof is [LP duality](/lp-duality/). With three or more players the same holds if beliefs about the others may be correlated; with independent beliefs it can fail.

## Related definitions

- **Dominant strategy.** A strategy that is a best response to every profile of the others ([dominant strategy](/dominant-strategy/)); removing strategies that are never best responses is [iterated dominance](/iterated-elimination-of-dominated-strategies/).
- **epsilon-best response.** A strategy within $\varepsilon$ of the best payoff; an [epsilon-Nash equilibrium](/epsilon-nash-equilibrium/) is a profile of $\varepsilon$-best responses.
- **Best-response dynamics and fictitious play.** Players repeatedly switch to a best response to the current profile ([best-response dynamics](/best-response-dynamics/)) or to the empirical mix of past play ([Robinson's theorem](/robinson-fictitious-play-theorem/)).
- **Best response polytope.** For bimatrix games, the polyhedron whose vertices encode the sets of pure best responses ([best response polytope](/best-response-polytope/)).
- **Indifference.** In a mixed equilibrium each player is indifferent among the pure strategies in the support ([indifference principle](/indifference-principle/)).

## References
