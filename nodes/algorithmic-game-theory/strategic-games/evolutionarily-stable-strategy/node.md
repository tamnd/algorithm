---
tag: Z4BEF6
kind: definition
slug: evolutionarily-stable-strategy
name: Evolutionarily stable strategy
aliases:
- evolutionary stable strategy
area: algorithmic-game-theory/strategic-games
level: advanced
summary: A strategy of a symmetric game that, once adopted by a population, cannot be invaded by a small group of mutants playing another strategy.
prereqs: [nash-equilibrium, mixed-strategy]
see_also: [replicator-dynamics, prisoners-dilemma, mutation-selection-balance, lyapunov-function, polynomial-hierarchy, np-hard, best-response, trembling-hand-perfect-equilibrium]
sources:
  - paper: doi:10.1038/246015a0
    title: "John Maynard Smith and George R. Price, The logic of animal conflict, Nature 246 (1973), 15-18"
    locator: the definition of an evolutionarily stable strategy and the contests between animals that motivate it
  - book: isbn:9780521625708
    title: Josef Hofbauer and Karl Sigmund, Evolutionary Games and Population Dynamics, Cambridge University Press, 1998
    locator: Chapter 6 (evolutionarily stable strategies and states) and Theorem 7.2.4 (an evolutionarily stable state is asymptotically stable for the replicator dynamics)
  - paper: doi:10.1007/s00182-007-0095-0
    title: "Kousha Etessami and Andreas Lochbihler, The computational complexity of evolutionarily stable strategies, International Journal of Game Theory 37(1) (2008), 93-113"
    locator: the existence of an ESS is NP-hard and coNP-hard and in the second level of the polynomial hierarchy, and the existence of a regular ESS is NP-complete
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 29, Computational Evolutionary Game Theory, by Siddharth Suri, Section 29.2 (the complexity of evolutionarily stable strategies)
---

An evolutionarily stable strategy (ESS) is a strategy of a symmetric two-player game such that, if a whole population plays it, a small group of mutants that plays any other strategy earns strictly less than the rest of the population, so selection removes the mutants. Maynard Smith and Price (1973) defined it to explain why animals fight in limited ways. Every ESS is a symmetric [Nash equilibrium](/nash-equilibrium/), but not every symmetric Nash equilibrium is an ESS, and some games have none. The ESS is a static test on payoffs; the [replicator dynamics](/replicator-dynamics/) is the matching dynamic model, in which every ESS is an asymptotically stable rest point.

## Definition

Let $A$ be an $n \times n$ matrix. It defines a symmetric two-player game in which both players choose from the same $n$ pure strategies and a player using $i$ against $j$ gets $A_{ij}$. For mixed strategies $x, y \in \Delta_n$, write $u(x, y) = x^{\mathsf T} A y$ for the payoff of $x$ against $y$. Think of $x$ as the strategy of one animal, or as the shares of the strategies in a large population in which animals meet in random pairs.

**Definition (Maynard Smith and Price 1973).** A strategy $x \in \Delta_n$ is an *evolutionarily stable strategy* if for every $y \in \Delta_n$ with $y \ne x$,

1. $u(x, x) \ge u(y, x)$ (equilibrium), and
2. if $u(y, x) = u(x, x)$, then $u(x, y) > u(y, y)$ (stability).

Condition 1 says that $(x, x)$ is a symmetric Nash equilibrium. Condition 2 says that a mutant that does as well as $x$ against $x$ does worse against itself than $x$ does against it.

**The invasion form.** Suppose a share $\varepsilon$ of the population switches to $y$, so a random opponent plays $w = (1 - \varepsilon) x + \varepsilon y$. Then

$$u(x, w) - u(y, w) = (1 - \varepsilon)\big[u(x, x) - u(y, x)\big] + \varepsilon\big[u(x, y) - u(y, y)\big].$$

So $x$ is an ESS if and only if for every $y \ne x$ there is a barrier $\bar\varepsilon(y) > 0$ such that $u(x, w) > u(y, w)$ for all $0 < \varepsilon < \bar\varepsilon(y)$. If the first bracket is positive, small $\varepsilon$ keep the sum positive; if it is 0, the sign is that of the second bracket; this is exactly conditions 1 and 2.

**Local superiority.** An equivalent form, used for the dynamics: $x$ is an ESS if and only if $u(x, y) > u(y, y)$ for all $y \ne x$ in some neighbourhood of $x$ in $\Delta_n$ (Hofbauer and Sigmund 1998, who call such an $x$ an evolutionarily stable state).

**Basic facts.**

- *Strict equilibria are ESS.* If $u(x, x) > u(y, x)$ for every $y \ne x$, condition 2 is never needed. A strict equilibrium is pure.
- *An interior ESS is the only ESS.* If $x$ has full support and $(x, x)$ is a Nash equilibrium, then $u(y, x) = u(x, x)$ for every $y$, so condition 2 gives $u(x, y) > u(y, y)$ for all $y \ne x$. If $y \ne x$ were another ESS, condition 1 for $y$ would give $u(y, y) \ge u(x, y)$, a contradiction.
- *The test for a given $x$.* Let $T$ be the support of $x$ and $(x, x)$ a Nash equilibrium. The mutants $y$ that tie in condition 1 are those whose support lies in the set of best responses to $x$. Condition 2 then asks that the quadratic form $z^{\mathsf T} A z$ be negative for the directions $z = y - x$ of such mutants, a question about a quadratic form on a cone. For a $2 \times 2$ game it reduces to one sign; in general it is hard, see below.
- *Weaker forms.* With $\ge$ in place of $>$ in condition 2, $x$ is a *neutrally stable strategy*. Sets of strategies can be evolutionarily stable when no single strategy is.

## Examples and non-examples

**Hawk and Dove.** Two animals contest a resource of value $V = 2$. A Hawk fights, a Dove shows and retreats, and a fight costs the loser $C = 4$. Two Hawks get $(V - C)/2 = -1$ each, a Hawk gets 2 against a Dove, a Dove gets 0 against a Hawk, and two Doves share, 1 each:

$$A = \begin{pmatrix} -1 & 2 \\ 0 & 1 \end{pmatrix}.$$

Neither pure strategy is a Nash equilibrium against itself: against Hawk, Dove does better ($0 > -1$), and against Dove, Hawk does better ($2 > 1$). Let $x = (1/2, 1/2)$. Then $Ax = (1/2, 1/2)$, so every $y$ ties against $x$ and condition 2 decides. For $y = (q, 1 - q)$, a short computation gives $u(x, y) - u(y, y) = (x - y)^{\mathsf T} A y = (1/2 - q)(1 - 2q) = 2 (1/2 - q)^2 > 0$ for $q \ne 1/2$. So $x$ is an ESS: the population keeps half Hawks. In general, for $0 < V < C$, the ESS plays Hawk with probability $V/C$.

**The prisoner's dilemma.** Defection strictly dominates cooperation, so (D, D) is a strict equilibrium, and D is an ESS, as on [prisoner's dilemma](/prisoners-dilemma/).

**Non-example: the mixed equilibrium of a coordination game.** For $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$, both pure strategies are strict equilibria and so ESS. The mixed $x = (1/2, 1/2)$ is a symmetric Nash equilibrium, but for $y = (q, 1 - q)$ the same computation gives $u(x, y) - u(y, y) = (1/2 - q)(2q - 1) = -2(1/2 - q)^2 < 0$. Every mutant that is closer to one pure strategy does better, so $x$ is not an ESS.

**Non-example: rock, paper, scissors has no ESS.** With 1 for a win, $-1$ for a loss and 0 for a tie, the only symmetric Nash equilibrium is the uniform $x$, and no pure strategy is one. The mutant $y = $ rock ties against $x$, and $u(x, \text{rock}) = 0 = u(\text{rock}, \text{rock})$, so condition 2 fails. The game has no ESS.

**A small change gives an ESS.** Subtract $\varepsilon > 0$ from each diagonal entry, so a tie costs $\varepsilon$: $A = C - \varepsilon I$, where $C$ is the matrix above, with $C^{\mathsf T} = -C$. The uniform $x$ is still a Nash equilibrium, since $Ax = -\varepsilon/3$ in every row. Because $y^{\mathsf T} C y = 0$ and the columns of $C$ sum to 0, $u(x, y) - u(y, y) = -\varepsilon/3 + \varepsilon \lVert y \rVert^2 = \varepsilon(\lVert y \rVert^2 - 1/3)$, which is positive for every $y \ne x$, since $\lVert y \rVert^2 \ge 1/3$ with equality only at $x$. So $x$ is an ESS. With $\varepsilon < 0$, a bonus for a tie, the sign flips and there is no ESS.

## Related definitions

- **Replicator dynamics.** In the [replicator dynamics](/replicator-dynamics/), every ESS is an asymptotically stable rest point (Taylor and Jonker 1978, Hofbauer and Sigmund 1998, Theorem 7.2.4). For an ESS $\hat x$, the proof uses the relative entropy $\sum_{i : \hat x_i > 0} \hat x_i \log(\hat x_i / x_i)$ of $\hat x$ with respect to the state $x$ as a [Lyapunov function](/lyapunov-function/). The converse fails: some games have an interior rest point that is asymptotically stable but not an ESS.
- **Complexity.** Checking whether a given strategy is an ESS is coNP-complete (Nisan 2006, and also by the reduction of Etessami and Lochbihler 2008). Deciding whether an ESS exists is [NP-hard](/np-hard/) and coNP-hard, and it lies in the second level of the [polynomial hierarchy](/polynomial-hierarchy/) (Etessami and Lochbihler 2008); Conitzer later showed that it is complete for that level. Deciding whether a regular ESS exists is NP-complete.
- **Population genetics.** In a model of [mutation and selection](/mutation-selection-balance/), the fitness of a genotype is fixed; an ESS is the analogue when the fitness of a strategy depends on the shares of the other strategies.
- **Refinements of Nash equilibrium.** An ESS is a refinement of symmetric Nash equilibrium, like [trembling-hand perfection](/trembling-hand-perfect-equilibrium/) for general games: an ESS is a [best response](/best-response/) to itself that also beats every alternative best response in the play against that alternative.

## References
