---
tag: 11NXM8
kind: theorem
slug: kuhn-theorem-behavioral-strategies
name: Kuhn's theorem on behavioral strategies
aliases:
- Kuhn's theorem
- behavioral strategy equivalence
area: algorithmic-game-theory/strategic-games
level: advanced
summary: In an extensive-form game with perfect recall, every mixed strategy has a behavioral strategy that induces the same distribution over outcomes.
prereqs: [perfect-recall, mixed-strategy]
see_also: [extensive-form-game, information-set, sequence-form, sequence-form-linear-program, counterfactual-regret-minimization, imperfect-information-game, nash-existence-theorem, subgame-perfect-equilibrium]
sources:
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (perfect recall and the theorem that every mixed strategy has an equivalent behavior strategy)
  - paper: doi:10.1006/game.1997.0536
    title: "Michele Piccione and Ariel Rubinstein, On the interpretation of decision problems with imperfect recall, Games and Economic Behavior 20(1) (1997), 3-24"
    locator: the absent-minded driver, a game without perfect recall where a behavior strategy beats all mixed strategies
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 11 (mixed and behavioral strategies, outcome equivalence under perfect recall)
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: the chapter on behavior strategies and Kuhn's theorem
---

Kuhn's theorem says that in an [extensive-form game](/extensive-form-game/) with [perfect recall](/perfect-recall/), a player loses nothing by randomizing separately at each [information set](/information-set/) instead of drawing a whole plan at the start. Every mixed strategy has a behavior strategy that gives the same probability to every leaf of the tree, against every strategy of the other players, and conversely. A behavior strategy needs one number per action, while a mixed strategy needs one per pure plan, and there are exponentially many plans. So the theorem is what lets equilibrium algorithms for game trees, such as the [sequence form](/sequence-form/) and [counterfactual regret minimization](/counterfactual-regret-minimization/), work on the tree. The name "Kuhn's theorem" is also used for another result of the same 1953 paper, that finite games of perfect information have pure equilibria; this page is about the first one.

## Statement

Let $\Gamma$ be a finite extensive-form game with players $N$, chance probabilities $p_c$, information sets $\mathcal{I}_i$ and action sets $A(I)$. A mixed strategy $\sigma_i$ of player $i$ is a distribution on the pure strategies $S_i = \prod_{I \in \mathcal{I}_i} A(I)$, and a behavior strategy $b_i$ gives a distribution $b_i(I) \in \Delta(A(I))$ at each $I \in \mathcal{I}_i$. For a profile $\tau$ of strategies, mixed or behavior, $P_\tau(z)$ is the probability that the play ends at the leaf $z$, with independent randomization by the players and by chance. Two strategies $\tau_i$ and $\tau_i'$ of player $i$ are *outcome equivalent* if $P_{(\tau_i, \tau_{-i})}(z) = P_{(\tau_i', \tau_{-i})}(z)$ for every leaf $z$ and every profile $\tau_{-i}$ of the others.

**Theorem (Kuhn 1953).** Let player $i$ have perfect recall.

1. For every mixed strategy $\sigma_i$ there is an outcome-equivalent behavior strategy $b_i$.
2. For every behavior strategy $b_i$ there is an outcome-equivalent mixed strategy $\sigma_i$.

Part 2 needs only that no path from the root meets an information set of $i$ twice, which perfect recall implies.

**Corollary.** If every player has perfect recall, then for every mixed profile there is a behavior profile with the same distribution on the leaves, and so the same expected payoffs, and conversely. A behavior profile is a [Nash equilibrium](/nash-equilibrium/) against behavior deviations if and only if an outcome-equivalent mixed profile is a Nash equilibrium of the normal form. By [Nash's theorem](/nash-existence-theorem/), every finite extensive game with perfect recall has a Nash equilibrium in behavior strategies.

### Example

Player 1 moves at the root, L or R. After L, player 1 moves again, $\ell_1$ or $r_1$; after R, player 1 moves again, $\ell_2$ or $r_2$. Each node is its own information set, so recall is perfect, and player 1 has $2^3 = 8$ pure strategies. Take the mixed strategy

$$\sigma_1 = \tfrac12 (L, \ell_1, \ell_2) + \tfrac14 (L, r_1, r_2) + \tfrac14 (R, \ell_1, r_2).$$

The proof below builds $b_1$ from the probabilities of the own sequences: L has weight $3/4$, (L, $\ell_1$) has $1/2$, R has $1/4$ and (R, $r_2$) has $1/4$. So $b_1$ plays L with probability $3/4$, $\ell_1$ with probability $(1/2)/(3/4) = 2/3$ after L, and $r_2$ with probability $(1/4)/(1/4) = 1$ after R. Both strategies reach the leaves $L\ell_1$, $Lr_1$, $R\ell_2$ and $Rr_2$ with the probabilities $1/2$, $1/4$, $0$ and $1/4$. The behavior strategy needs 3 numbers; a mixed strategy needs 7.

## In plain words

A player can plan in two ways. The first way is to pick a complete plan at random before the game starts, from a list of all plans. The second way is to wait, and at each point where the player must move, toss a separate coin for that point only. The second way looks weaker, because the coins at different points cannot depend on each other. The theorem says that it is not weaker, as long as the player never forgets their own past moves or what they saw. The reason is that a player who remembers their past knows which parts of the plan still matter, and can toss each coin with the odds that the plan gives, given what has happened so far.

## Proof

Fix player $i$ with perfect recall. For a node $h$, let $X_i(h) = ((I_1, a_1), \ldots, (I_k, a_k))$ be the experience of $i$ at $h$: the information sets of $i$ that the path to $h$ passes, before $h$, with the actions taken there. By perfect recall, $X_i(h)$ is the same for all $h \in I$; write it $X_i(I)$. Also by perfect recall, the sets $I_1, \ldots, I_k$ are distinct, and $X_i(I_t) = ((I_1, a_1), \ldots, (I_{t-1}, a_{t-1}))$.

**The factorization.** For a leaf $z$, let $p_c(z)$ be the product of the chance probabilities on the path to $z$. Given a pure profile $s$, the play reaches $z$ exactly when every player $j$ chooses, at each of their own information sets on the path, the action on the path. So

$$P_s(z) = p_c(z) \prod_{j \in N} [s_j \text{ is consistent with } X_j(z)],$$

where $s_j$ is *consistent* with a sequence $x = ((I_1, a_1), \ldots, (I_k, a_k))$ if $s_j(I_t) = a_t$ for all $t$. Since the players randomize independently, a mixed profile gives

$$P_\sigma(z) = p_c(z) \prod_{j \in N} \mu_j(X_j(z)), \qquad \mu_j(x) = \sigma_j(\{s_j : s_j \text{ is consistent with } x\}).$$

The number $\mu_j(x)$ is the *realization weight* of $x$. In the same way, a behavior strategy $b_j$ contributes the factor $\beta_j(X_j(z)) = \prod_{t} b_j(I_t)(a_t)$, and mixed and behavior strategies can be combined across players. So two strategies of player $i$ are outcome equivalent if they give the same factor for every sequence $X_i(z)$.

**Part 1.** Given $\sigma_i$, write $\mu = \mu_i$. For $I \in \mathcal{I}_i$ and $a \in A(I)$, let $x = X_i(I)$ and define

$$b_i(I)(a) = \frac{\mu(x, (I, a))}{\mu(x)} \quad \text{if } \mu(x) > 0,$$

and let $b_i(I)$ be any distribution on $A(I)$ if $\mu(x) = 0$. This is a distribution: $I$ does not occur in $x$, so the events $\{s_i(I) = a\}$, $a \in A(I)$, split the event that $s_i$ is consistent with $x$ into disjoint parts, and $\sum_a \mu(x, (I, a)) = \mu(x)$.

Now let $z$ be a leaf with $X_i(z) = ((I_1, a_1), \ldots, (I_k, a_k))$, and write $x_t$ for its first $t$ pairs, so $x_0$ is empty, $\mu(x_0) = 1$, and $X_i(I_t) = x_{t-1}$. If $\mu(x_t) > 0$ for all $t$, the product telescopes:

$$\beta_i(X_i(z)) = \prod_{t=1}^{k} \frac{\mu(x_t)}{\mu(x_{t-1})} = \mu(x_k).$$

Otherwise, let $t$ be the first index with $\mu(x_t) = 0$. Then $\mu(x_{t-1}) > 0$, so $b_i(I_t)(a_t) = 0$ and $\beta_i(X_i(z)) = 0$. The events of consistency shrink as $t$ grows, so $\mu(x_k) \le \mu(x_t) = 0$ as well. In both cases $\beta_i(X_i(z)) = \mu_i(X_i(z))$, and by the factorization $b_i$ and $\sigma_i$ are outcome equivalent.

**Part 2.** Given $b_i$, let $\sigma_i$ draw the action at every information set independently in advance: $\sigma_i(s_i) = \prod_{I \in \mathcal{I}_i} b_i(I)(s_i(I))$. For a sequence $x = ((I_1, a_1), \ldots, (I_k, a_k))$ with distinct sets $I_t$, independence gives $\mu_i(x) = \prod_t b_i(I_t)(a_t) = \beta_i(x)$. The sets on a path are distinct when no path meets an information set twice, so the factors agree for every leaf. $\blacksquare$

**The corollary.** The expected payoff $u_j(\tau) = \sum_z P_\tau(z) u_j(z)$ depends only on the distribution on the leaves. So outcome-equivalent profiles give the same payoffs to all players, and a deviation of player $i$ of one kind has an equivalent deviation of the other kind. Hence the equilibrium conditions agree.

## Consequences

- **Equilibria in behavior strategies.** Every finite extensive game with perfect recall has a Nash equilibrium in behavior strategies, with the same payoffs as a mixed equilibrium of its normal form. In two-player zero-sum games, the maximin value over behavior strategies equals the value of the normal form ([minimax theorem](/minimax-theorem/)).
- **Small strategy spaces.** A behavior strategy of player $i$ has $\sum_{I} |A(I)|$ numbers, while a mixed strategy has $\prod_I |A(I)| - 1$ free numbers. For Kuhn poker this is 12 numbers against 63. The [sequence form](/sequence-form/) uses the realization weights $\mu_i$ of the proof as variables; they satisfy linear constraints, and the payoff is bilinear in them. This gives a polynomial-size [linear program](/sequence-form-linear-program/) for two-player zero-sum games with perfect recall (Koller, Megiddo and von Stengel 1996).
- **Local learning.** [Counterfactual regret minimization](/counterfactual-regret-minimization/) runs a regret minimizer at each information set and combines the average strategies into a behavior strategy. The realization weights give the average in the right form.
- **Many to one.** The map from mixed to behavior strategies is many to one. In the example, the mixed strategy $\tfrac12 (L, \ell_1, \ell_2) + \tfrac14 (L, r_1, \ell_2) + \tfrac14 (R, \ell_1, r_2)$ gives the same $b_1$, since the action at the node after R matters only when the plan plays R.

## Tightness

- **Part 1 fails without perfect recall.** In the game of the forgetful player on [perfect recall](/perfect-recall/), player 1 chooses L or R and later chooses l or r at one information set that contains both nodes. The mixed strategy $\tfrac12 (L, l) + \tfrac12 (R, r)$ gives the leaves Ll and Rr with probability $1/2$ each. A behavior strategy plays L with some probability $\alpha$ and l with some probability $\gamma$, independently, and gives Lr and Rl the probabilities $\alpha(1 - \gamma)$ and $(1 - \alpha)\gamma$. Both are 0 only if $\alpha = \gamma \in \{0, 1\}$, and then Ll or Rr has probability 0.
- **Part 2 fails if a path meets an information set twice.** In the absent-minded driver (Piccione and Rubinstein 1997), the exits X and Y form one information set on one path. The behavior strategy that continues with probability $2/3$ reaches X, Y and the end with the probabilities $(1/3, 2/9, 4/9)$ and pays $4/3$, while every mixed strategy is a mix of "exit at once" and "never exit", pays at most 1, and never ends at Y. In the same game, the mixed strategy $\tfrac12$ exit plus $\tfrac12$ continue gives $(1/2, 0, 1/2)$, which no behavior strategy gives, so part 1 also fails.
- **Without perfect recall, computation is hard.** For two-player zero-sum extensive games without perfect recall, computing the value is NP-hard (Koller and Megiddo 1992), while with perfect recall the sequence form LP solves it in polynomial time. So the hypothesis is also what separates easy from hard instances.
- **Infinite games.** The theorem above is for finite trees. Aumann (1964) extended it to extensive games with infinitely many moves and infinite action sets, where measurability needs care.

## History

Von Neumann and Morgenstern (1944) described games in extensive form but worked mostly with the normal form. Kuhn's 1953 paper in the second volume of the Princeton *Contributions to the Theory of Games* gave the general tree model with chance moves and information sets that is used today, defined perfect recall, and proved the equivalence of mixed and behavior strategies under it. The same paper proved that every finite game of perfect information has an equilibrium in pure strategies, by backward induction, which extends Zermelo's 1913 argument for chess; both results are called Kuhn's theorem. The theorem became central to computation in the 1990s, when Koller, Megiddo and von Stengel built the sequence form on the realization weights, and later in poker programs based on counterfactual regret minimization.

## References
