---
tag: J10R8B
kind: definition
slug: stackelberg-equilibrium
name: Stackelberg equilibrium
aliases:
- leader-follower equilibrium
- strong Stackelberg equilibrium
area: algorithmic-game-theory/strategic-games
level: core
summary: An outcome of a game in which a leader commits to a strategy first and a follower best responds to it, with the leader choosing the best commitment.
prereqs: [best-response, subgame-perfect-equilibrium]
see_also: [stackelberg-commitment-algorithm, security-game, stackelberg-routing, bimatrix-game, nash-equilibrium, correlated-equilibrium, minimax-theorem, bayesian-game]
sources:
  - book: "Heinrich von Stackelberg, Marktform und Gleichgewicht, Julius Springer, Vienna and Berlin, 1934"
    title: Marktform und Gleichgewicht
    locator: the duopoly in which one firm leads and the other follows, the origin of the name
  - paper: "Vincent Conitzer and Tuomas Sandholm, Computing the optimal strategy to commit to, Proceedings of the 7th ACM Conference on Electronic Commerce (EC 2006), 82-90"
    title: Computing the optimal strategy to commit to
    locator: commitment to pure and to mixed strategies in normal-form and Bayesian games, and the complexity of finding the best commitment
  - paper: doi:10.1016/j.geb.2009.11.008
    title: "Bernhard von Stengel and Shmuel Zamir, Leadership games with convex strategy sets, Games and Economic Behavior 69(2) (2010), 446-457"
    locator: the payoff of the leader under mixed commitment is at least its payoff in any Nash or correlated equilibrium of a two-player game
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 6 (subgame perfect equilibria of extensive games with perfect information, with the Stackelberg duopoly as an example)
---

A Stackelberg equilibrium is the outcome of a two-player game in which one player, the leader, commits to a strategy first, the other player, the follower, sees the commitment and plays a [best response](/best-response/) to it, and the leader picks the commitment that is best for itself when it foresees that response. The strong form breaks ties of the follower in favor of the leader. This page is about the solution concept. The linear programs that compute the best mixed commitment are on [computing an optimal strategy to commit to](/stackelberg-commitment-algorithm/), the defender and attacker model in which they are used most is the [security game](/security-game/), and [Stackelberg routing](/stackelberg-routing/) is a different use of the name, for a leader who controls part of the traffic in a network.

## Definition

Let $(A, B)$ be an $m \times n$ [bimatrix game](/bimatrix-game/). The row player is the leader, with payoffs $A$, and the column player is the follower, with payoffs $B$. The leader commits to a mixed strategy $x \in \Delta_m$. The follower sees $x$ and chooses a column from its best response set

$$\mathrm{BR}(x) = \arg\max_{j} (B^{\mathsf T} x)_j .$$

A pure best response always exists, and a mixed best response puts weight only on $\mathrm{BR}(x)$, so it is enough to consider pure replies.

**Definition.** A *strong Stackelberg equilibrium* is a pair $(x^*, j^*)$ with $j^* \in \mathrm{BR}(x^*)$ that maximizes the payoff $(A^{\mathsf T} x)_j$ of the leader over all pairs $(x, j)$ with $j \in \mathrm{BR}(x)$. Its value is

$$V_{\mathrm{SSE}} = \max_{x \in \Delta_m} \ \max_{j \in \mathrm{BR}(x)} (A^{\mathsf T} x)_j .$$

So the leader chooses the commitment, and when the follower is indifferent, the follower takes the reply that the leader prefers.

**Existence.** For each column $j$, the set $X_j = \{x \in \Delta_m : j \in \mathrm{BR}(x)\}$ is given by the linear inequalities $(B^{\mathsf T} x)_j \ge (B^{\mathsf T} x)_k$ for all $k$, so it is a closed polytope, and the sets $X_1, \ldots, X_n$ cover $\Delta_m$. The payoff $(A^{\mathsf T} x)_j$ is linear in $x$, so its maximum over each nonempty $X_j$ is attained, and $V_{\mathrm{SSE}}$ is the largest of these at most $n$ maxima. This is also how it is computed, by one linear program for each $j$ ([computing an optimal strategy to commit to](/stackelberg-commitment-algorithm/)).

**The weak form.** In a *weak Stackelberg equilibrium*, the follower breaks ties against the leader, so the leader gets $\min_{j \in \mathrm{BR}(x)} (A^{\mathsf T} x)_j$. This function of $x$ need not be upper semicontinuous, and its supremum may not be attained, as in the example below. The strong form is the usual one in the computational literature.

**As a subgame perfect equilibrium.** Consider the two-stage game in which the leader chooses $x$, the follower observes it and then chooses $j$. A strategy of the follower is a map $g$ from commitments to replies. A pair $(x^*, g)$ in which $g(x) \in \mathrm{BR}(x)$ for every $x$, $g$ breaks ties for the leader, and $x^*$ maximizes $(A^{\mathsf T} x)_{g(x)}$ is a [subgame perfect equilibrium](/subgame-perfect-equilibrium/) of this game. The follower's best response must hold at every $x$, also at commitments the leader does not make, which is the point of subgame perfection.

**Pure commitment.** If the leader may commit only to a pure row $i$, the value is $\max_i \max_{j \in \mathrm{BR}(e_i)} A_{ij}$. Mixed commitment is at least as good and can be strictly better.

**Commitment never hurts in two-player games.** Let $(x, y)$ be any Nash equilibrium. Every column $j$ with $y_j > 0$ is a best response to $x$, so

$$x^{\mathsf T} A y = \sum_j y_j (A^{\mathsf T} x)_j \le \max_{j \in \mathrm{BR}(x)} (A^{\mathsf T} x)_j \le V_{\mathrm{SSE}} .$$

So the leader gets at least its payoff in any [Nash equilibrium](/nash-equilibrium/). Von Stengel and Zamir (2010) show the same bound for every [correlated equilibrium](/correlated-equilibrium/), and that much of this fails with three or more players.

**Zero-sum games.** If $B = -A$, every tie of the follower is also a tie for the leader, and the leader gets $\max_x \min_j (A^{\mathsf T} x)_j$, the value of the game. So by the [minimax theorem](/minimax-theorem/), commitment gives the same payoff as simultaneous play, and the best commitment is a maximin strategy.

**Other settings.** The same idea applies with continuous actions, as in the original duopoly of Stackelberg (1934), with several follower types drawn from a prior (a [Bayesian game](/bayesian-game/), where the follower knows its own type), and with several followers who play an equilibrium among themselves.

## Examples and non-examples

**Mixed commitment beats both Nash and pure commitment.** Take the game

| | L | R |
| --- | --- | --- |
| U | $(2, 1)$ | $(4, 0)$ |
| D | $(1, 0)$ | $(3, 1)$ |

- *Nash.* U strictly dominates D for the leader ($2 > 1$ and $4 > 3$), so the leader plays U and the follower answers L. The unique Nash equilibrium is (U, L), and the leader gets 2.
- *Pure commitment.* Committing to U gives L and 2. Committing to D gives R, since $1 > 0$ for the follower, and the leader gets 3. So pure commitment to the dominated row D is better than playing U.
- *Mixed commitment.* Let the leader play U with probability $p$. The follower gets $p$ from L and $1 - p$ from R, so R is a best response if and only if $p \le 1/2$. Against R the leader gets $4p + 3(1 - p) = 3 + p$, and against L it gets $2p + (1 - p) = 1 + p$. The best is $p = 1/2$ with the reply R, and the strong Stackelberg value is $7/2$.
- *Weak form.* At $p = 1/2$ the follower is indifferent. If it breaks the tie against the leader, it plays L and the leader gets $3/2$. For $p < 1/2$ the reply is R and the leader gets $3 + p < 7/2$. So the supremum $7/2$ is not attained, and no weak Stackelberg equilibrium exists. In practice the leader plays $p = 1/2 - \varepsilon$ and gets $7/2 - \varepsilon$.

**The Stackelberg duopoly.** Two firms with the unit cost $c$ choose quantities $q_1, q_2 \ge 0$, and the price is $a - q_1 - q_2$ with $a > c$. The follower's best response to $q_1$ is $q_2 = (a - c - q_1)/2$. The leader foresees it and gets $q_1 (a - c - q_1)/2$, which is largest at $q_1 = (a - c)/2$. Then $q_2 = (a - c)/4$, and the profits are $(a - c)^2/8$ for the leader and $(a - c)^2/16$ for the follower. In the Cournot equilibrium, where both choose at the same time, each firm makes $(a - c)/3$ and earns $(a - c)^2/9$. Leading pays: $1/8 > 1/9$, and the follower loses: $1/16 < 1/9$.

**Non-example: a pure commitment can be worse than simultaneous play.** In matching pennies, with payoff $1$ to the leader on a match and $-1$ otherwise, a pure commitment lets the follower mismatch, and the leader gets $-1$. In the Nash equilibrium both mix $1/2$ and the leader gets 0, which is also the strong Stackelberg value, since the game is zero-sum. The bound "commitment never hurts" needs mixed commitment.

**Non-example: a Nash equilibrium is not a Stackelberg equilibrium.** In the first example, (U, L) is the Nash equilibrium, but the leader can do better by committing, so it is not the outcome of the commitment game. The two notions differ because the follower in a Stackelberg equilibrium answers a commitment it sees, while in a Nash equilibrium each player answers a strategy it only expects.

## Related definitions

- **Computing the best commitment.** For a two-player game in normal form, the best mixed commitment is found in polynomial time by one linear program for each pure strategy of the follower (Conitzer and Sandholm 2006, [computing an optimal strategy to commit to](/stackelberg-commitment-algorithm/)). With several follower types drawn from a prior, the problem is NP-hard (same paper).
- **Security games.** In a [security game](/security-game/), a defender commits to a random allocation of resources over targets, an attacker observes the distribution and attacks one target, and the strong Stackelberg equilibrium is the usual solution.
- **Stackelberg routing.** In [Stackelberg routing](/stackelberg-routing/), a central authority controls a fraction of the traffic and routes it first, and the rest of the traffic then reaches a selfish equilibrium. The leader there controls flow, not the strategy of a player in a bimatrix game.
- **Subgame perfection.** The Stackelberg equilibrium is the [subgame perfect equilibrium](/subgame-perfect-equilibrium/) of the commitment game; the difference from simultaneous play is in the order of moves and in the observation of the commitment.

## References
