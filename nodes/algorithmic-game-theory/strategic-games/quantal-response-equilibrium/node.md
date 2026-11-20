---
tag: 63CNKF
kind: definition
slug: quantal-response-equilibrium
name: Quantal response equilibrium
aliases:
- QRE
- logit equilibrium
area: algorithmic-game-theory/strategic-games
level: advanced
summary: A profile in which each player plays each action with a probability that rises smoothly with its payoff, for example by a logit rule.
prereqs: [nash-equilibrium, best-response]
see_also: [trembling-hand-perfect-equilibrium, logistic-regression, shannon-entropy, brouwer-fixed-point-theorem, homotopy-continuation, fixed-point-iteration, multiplicative-weights-update, nash-equilibrium-computation]
sources:
  - paper: doi:10.1006/game.1995.1023
    title: "Richard D. McKelvey and Thomas R. Palfrey, Quantal response equilibria for normal form games, Games and Economic Behavior 10(1) (1995), 6-38"
    locator: the definition of quantal response equilibrium, the logit form, existence, the convergence of logit equilibria to Nash equilibria as lambda grows, and the selection of one Nash equilibrium by a branch of the logit equilibria in generic games
  - paper: doi:10.1023/A:1009905800005
    title: "Richard D. McKelvey and Thomas R. Palfrey, Quantal response equilibria for extensive form games, Experimental Economics 1 (1998), 9-41"
    locator: the agent quantal response equilibrium of extensive form games
  - book: "Jacob K. Goeree, Charles A. Holt and Thomas R. Palfrey, Quantal Response Equilibrium, A Stochastic Theory of Games, Princeton University Press, 2016"
    title: Quantal Response Equilibrium
    locator: the general theory of quantal response functions and the use of logit equilibria to fit data from experiments
---

A quantal response equilibrium is a mixed strategy profile in which every player plays every action with positive probability, and the probability of an action rises smoothly with the expected payoff of that action against the others, instead of jumping to the best action. The usual form is the logit rule, which plays an action with probability proportional to $e^{\lambda \cdot \text{payoff}}$ for a precision parameter $\lambda \ge 0$. McKelvey and Palfrey (1995) introduced it to describe play with errors, and it is fitted to data from experiments. At $\lambda = 0$ every player mixes uniformly, and as $\lambda \to \infty$ the logit equilibria approach [Nash equilibria](/nash-equilibrium/). It differs from a [trembling-hand perfect equilibrium](/trembling-hand-perfect-equilibrium/), whose mistakes are arbitrary small probabilities that vanish in the limit, in that the size of a mistake here is fixed by its cost.

## Definition

Let $G$ be a finite normal-form game with players $N$, pure strategies $S_i$ and payoffs $u_i$. For a mixed profile $\sigma$, let $U_i(\sigma) \in \mathbb{R}^{S_i}$ be the vector of expected payoffs $U_i(s_i, \sigma_{-i})$ of the pure strategies of player $i$ against the others.

**Quantal response functions.** A *quantal response function* of player $i$ is a continuous map $R_i : \mathbb{R}^{S_i} \to \Delta(S_i)$ such that

- every action gets positive probability: $R_i(v)(s_i) > 0$;
- it is monotone: $v(s_i) > v(s_i')$ implies $R_i(v)(s_i) > R_i(v)(s_i')$.

McKelvey and Palfrey derive such maps from random utility: the player observes $v(s_i) + \varepsilon(s_i)$ with a random noise vector $\varepsilon$ with a density, and picks the largest; $R_i(v)(s_i)$ is the probability that $s_i$ is picked.

**Definition.** A profile $\sigma$ is a *quantal response equilibrium* for the maps $R = (R_i)_{i \in N}$ if, for every player $i$,

$$\sigma_i = R_i\big(U_i(\sigma)\big).$$

**The logit form.** If the noise terms are independent with the extreme value (Gumbel) distribution with scale $1/\lambda$, the response is

$$R_i^\lambda(v)(s_i) = \frac{e^{\lambda v(s_i)}}{\sum_{s'_i \in S_i} e^{\lambda v(s'_i)}},$$

the same rule as in multinomial [logistic regression](/logistic-regression/), often called softmax. A fixed point of $R^\lambda$ is a *logit equilibrium* with precision $\lambda$.

**Existence.** The map $\sigma \mapsto (R_i(U_i(\sigma)))_{i}$ is continuous from the product of the simplices to itself, so it has a fixed point by [Brouwer's theorem](/brouwer-fixed-point-theorem/). Every finite game has a quantal response equilibrium for every choice of the maps, and a logit equilibrium for every $\lambda \ge 0$.

**A smoothed best response.** The logit response to $v$ is the unique maximizer over $\Delta(S_i)$ of $\sum_{s_i} \sigma_i(s_i) v(s_i) + \frac{1}{\lambda} H(\sigma_i)$, where $H$ is the [Shannon entropy](/shannon-entropy/). So a logit equilibrium is a Nash equilibrium of the game in which each player also earns $\frac{1}{\lambda}$ times the entropy of its own mixed strategy. This is the same regularized response that [multiplicative weights](/multiplicative-weights-update/) uses.

**Limits are Nash equilibria.** Let $\sigma^{\lambda}$ be logit equilibria with $\lambda \to \infty$ and $\sigma^\lambda \to \sigma$. Suppose $\sigma_i(s_i) > 0$ but $s_i$ is not a best response to $\sigma_{-i}$, so some $s^*_i$ is better by $\delta > 0$. By continuity, $U_i(s^*_i, \sigma^\lambda_{-i}) - U_i(s_i, \sigma^\lambda_{-i}) > \delta/2$ for large $\lambda$, and then $\sigma^\lambda_i(s_i) \le e^{-\lambda \delta/2} \sigma^\lambda_i(s^*_i) \le e^{-\lambda\delta/2} \to 0$, which contradicts $\sigma_i(s_i) > 0$. So every limit point is a Nash equilibrium (McKelvey and Palfrey 1995).

**A branch that selects one equilibrium.** At $\lambda = 0$ the only logit equilibrium is the uniform profile. McKelvey and Palfrey show that for almost all games the set of pairs $(\lambda, \sigma)$ of logit equilibria contains a unique branch, often called the principal branch, that starts at the uniform profile and leads to one Nash equilibrium as $\lambda \to \infty$. Following this branch numerically is a [homotopy](/homotopy-continuation/) method that both computes and selects a Nash equilibrium, in the spirit of the tracing procedure of Harsanyi and Selten. It gives no bound on the running time, which is consistent with the hardness results on [Nash equilibrium computation](/nash-equilibrium-computation/).

## Examples and non-examples

**Matching pennies.** The row player gets $1$ on a match and $-1$ otherwise, and the column player the opposite. By symmetry the uniform profile is a logit equilibrium for every $\lambda$, and it is also the unique Nash equilibrium. Logit play does not change the prediction here.

**Asymmetric matching pennies.** Change the row payoff at (U, L) from 1 to 9, with all other row payoffs $0$ except $1$ at (D, R), and let the column player get $1$ at (U, R) and (D, L) and 0 otherwise. Let $p$ be the probability of U and $q$ that of L.

- In the Nash equilibrium the column player must be indifferent, so $p = 1/2$, and the row player must be indifferent, $9q = 1 - q$, so $q = 1/10$. Changing the row player's own payoff changes only the other player's mix.
- In the logit equilibrium, U beats D by $10q - 1$ and L beats R by $1 - 2p$, so $p = 1/(1 + e^{-\lambda(10q - 1)})$ and $q = 1/(1 + e^{-\lambda(1 - 2p)})$. For each $\lambda$ there is exactly one solution, found by [bisection](/bisection-method/) on $p$:

| $\lambda$ | $p$ | $q$ |
| --- | --- | --- |
| 0 | 0.5 | 0.5 |
| 0.5 | 0.83067 | 0.41808 |
| 1 | 0.89358 | 0.31278 |
| 2 | 0.86075 | 0.19108 |
| 5 | 0.70198 | 0.11714 |
| 10 | 0.60748 | 0.10437 |
| 100 | 0.51098 | 0.10004 |

So $p > 1/2$ for every $\lambda > 0$: the row player plays U, which can give 9, more often than in the Nash equilibrium. Such an effect of a player's own payoff appears in experiments with games of this kind, and it is one reason for the use of QRE in experimental economics. As $\lambda$ grows, $(p, q)$ tends to the Nash equilibrium $(1/2, 1/10)$.

**Non-example: iterating the response.** A logit equilibrium is a fixed point, but plain [fixed point iteration](/fixed-point-iteration/) $\sigma \leftarrow R^\lambda(U(\sigma))$, with both players updating at the same time, need not converge to it. In matching pennies, U beats D by $4q - 2$ and L beats R by $2 - 4p$. The derivative of $1/(1 + e^{-z})$ at $z = 0$ is $1/4$, so at the uniform profile the update has the derivatives $\partial p'/\partial q = \lambda$ and $\partial q'/\partial p = -\lambda$. Its linear part has the eigenvalues $\pm i\lambda$, so for $\lambda > 1$ the iteration moves away from the equilibrium even when it starts close to it.

**Non-example: a QRE is not a Nash equilibrium.** For finite $\lambda$, every action has positive probability, also a strictly dominated one, so a logit equilibrium of a game with a strictly dominated strategy is never a Nash equilibrium. The equilibrium of the game above with $\lambda = 1$ has $p \approx 0.894$, while the column player's best response to that $p$ is R alone.

## Related definitions

- **Trembling-hand perfection.** A [trembling-hand perfect equilibrium](/trembling-hand-perfect-equilibrium/) is a limit of best responses to profiles in which every strategy has positive probability. In a QRE the positive probabilities are part of the prediction, and costlier mistakes are less likely.
- **Extensive form.** McKelvey and Palfrey (1998) apply the logit rule at every information set, to the agent normal form, which gives the agent quantal response equilibrium of a game tree.
- **Learning.** The logit response is the smoothed best response of stochastic fictitious play and of regularized learning dynamics; their rest points are logit equilibria.
- **Data.** In experiments, $\lambda$ is estimated by maximum likelihood from the observed choice frequencies, and a larger $\lambda$ means less noisy play.

## References
