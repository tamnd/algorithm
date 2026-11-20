---
tag: 424DRB
kind: theorem
slug: condorcet-jury-theorem
name: Condorcet jury theorem
aliases:
- "Condorcet's jury theorem"
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: If voters are independently right with probability above 1/2, the chance that the majority is right tends to 1 as the electorate grows.
prereqs: [binomial-distribution, hoeffding-inequality]
see_also: [may-theorem, condorcet-winner, law-of-large-numbers, chernoff-bound, ensemble-learning, bagging, weighted-majority, central-limit-theorem]
sources:
  - book: "Marie Jean Antoine Nicolas de Caritat, marquis de Condorcet, Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix, Imprimerie Royale, Paris, 1785"
    title: Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix
    locator: the probability that a majority of an assembly decides correctly when each member is right with the same probability
  - paper: doi:10.1007/BF00125672
    title: "Bernard Grofman, Guillermo Owen and Scott L. Feld, Thirteen theorems in search of the truth, Theory and Decision 15(3) (1983), 261-278"
    locator: the modern statement and its extensions to voters of unequal competence
  - paper: doi:10.2307/2082796
    title: "David Austen-Smith and Jeffrey S. Banks, Information aggregation, rationality, and the Condorcet jury theorem, American Political Science Review 90(1) (1996), 34-45"
    locator: the result that sincere voting need not be a Nash equilibrium when voters have private information and a common goal
---

The Condorcet jury theorem says that if each voter in a group is right with the same probability $p > 1/2$, and the voters err independently, then a majority vote is right more often than any single voter, and the probability that the majority is right grows with the size of the group and tends to 1. Condorcet stated it in 1785. It is the probabilistic argument for majority rule, and the same computation explains why a majority vote of many weak but independent classifiers can be very accurate.

## Statement

There are two options, one of them correct. Each of $n$ voters votes for one option. Let $X_i = 1$ if voter $i$ votes for the correct option and $X_i = 0$ otherwise, and assume:

1. **Independence.** $X_1, \ldots, X_n$ are independent.
2. **Equal competence.** $\Pr[X_i = 1] = p$ for every $i$, with $\tfrac12 < p < 1$.
3. **Odd size.** $n = 2k + 1$, so there are no ties.

Let $S_n = X_1 + \cdots + X_n$, which has the [binomial distribution](/binomial-distribution/) $B(n, p)$, and let

$$P_n = \Pr[S_n \ge k + 1] = \sum_{j = k + 1}^{n} \binom{n}{j} p^j (1 - p)^{n - j}$$

be the probability that the majority is right.

**Theorem.** Under assumptions 1 to 3:

- (a) $P_{n+2} - P_n = \binom{n}{k} p^{k+1} (1 - p)^{k+1} (2p - 1) > 0$, so $P_n$ is strictly increasing over odd $n$, and $P_n > p$ for every $n \ge 3$.
- (b) $P_n \ge 1 - e^{-2n(p - 1/2)^2}$, so $P_n \to 1$ as $n \to \infty$.

If $p < 1/2$ the same identity shows that $P_n$ decreases to 0, and if $p = 1/2$ then $P_n = 1/2$ for every odd $n$.

## In plain words

Suppose each juror is a bit better than a coin flip at finding the truth, and the jurors make their mistakes on their own, not by copying each other. Then the verdict of the majority is more reliable than any one juror. The bigger the jury, the more reliable it gets: the mistakes of some jurors cancel out, and the small edge that each one has adds up. With enough jurors the majority is almost never wrong. If each juror is worse than a coin flip, the same effect works the other way.

## Proof

*Part (a).* Compare a jury of $n = 2k + 1$ voters with the same jury plus two more voters. The majority of $n + 2$ voters can differ from the majority of the first $n$ only if the first $n$ voters are split $k + 1$ to $k$, one way or the other.

- If exactly $k + 1$ of the first $n$ are right and both new voters are wrong, the majority changes from right to wrong. This has probability $\binom{n}{k+1} p^{k+1} q^{k} \cdot q^2$, where $q = 1 - p$.
- If exactly $k$ of the first $n$ are right and both new voters are right, the majority changes from wrong to right. This has probability $\binom{n}{k} p^{k} q^{k+1} \cdot p^2$.

In every other case the two majorities agree. Since $\binom{n}{k} = \binom{n}{k+1}$,

$$P_{n+2} - P_n = \binom{n}{k} p^{k+2} q^{k+1} - \binom{n}{k} p^{k+1} q^{k+2} = \binom{n}{k} p^{k+1} q^{k+1} (p - q),$$

and $p - q = 2p - 1 > 0$. So $P_n$ is strictly increasing over odd $n$. With $P_1 = p$ this gives $P_n > p$ for $n \ge 3$. The same formula gives $P_{n+2} < P_n$ when $p < 1/2$, and $P_n = 1/2$ for all odd $n$ when $p = 1/2$, by the symmetry of $B(n, 1/2)$.

*Part (b).* The majority is wrong exactly when $S_n \le k < n/2$, that is, when $S_n - np < -n(p - \tfrac12)$. The variables $X_i$ are independent and take values in $[0, 1]$, so [Hoeffding's inequality](/hoeffding-inequality/) gives, for $t > 0$,

$$\Pr[S_n - np \le -t] \le e^{-2t^2/n}.$$

With $t = n(p - \tfrac12)$ this is $\Pr[S_n \le k] \le e^{-2n(p - 1/2)^2}$, so $P_n \ge 1 - e^{-2n(p - 1/2)^2} \to 1$. $\blacksquare$

The identity in part (a) was checked in exact rational arithmetic for $p = 3/5$ and all odd $n$ up to 39. A weaker form of part (b), $1 - P_n \le p(1 - p) / (n (p - \frac12)^2)$, follows from [Chebyshev's inequality](/chebyshev-inequality/) and is enough for the limit; it is the [law of large numbers](/law-of-large-numbers/) applied to the share of correct votes.

## Consequences

- **Numbers for $p = 0.6$.** $P_1 = 0.6$, $P_3 = 0.648$, $P_5 \approx 0.683$, $P_{11} \approx 0.753$, $P_{51} \approx 0.926$ and $P_{101} \approx 0.979$. The smallest odd jury with $P_n \ge 0.99$ has 133 voters. The bound of part (b) asks for $n \ge \ln(100) / (2 \cdot 0.1^2) \approx 230.3$, so it is safe but not tight.
- **Sample size for a target error.** To make the majority wrong with probability at most $\delta$, part (b) shows that $n \ge \ln(1/\delta) / (2 (p - 1/2)^2)$ voters suffice. The number grows as the inverse square of the edge $p - 1/2$, as in every [Chernoff bound](/chernoff-bound/) argument.
- **Majority votes of classifiers.** If several classifiers each have error below $1/2$ on an example and their errors are independent, their majority vote has a smaller error. This is the idea behind [ensemble learning](/ensemble-learning/) and [bagging](/bagging/), which try to make the errors as independent as possible. In practice the errors are correlated, and the gain is smaller.
- **Two arguments for majority rule.** [May's theorem](/may-theorem/) justifies majority rule on two options by fairness axioms. The jury theorem justifies it when there is a correct answer and the voters try to find it.

## Tightness

Each assumption matters.

- **Independence.** If all voters copy one of them, every $P_n$ equals $p$. Correlated errors can make large juries no better, or worse, than one voter.
- **Competence above one half.** If $p = 1/2$ the majority is a coin flip for every $n$, and if $p < 1/2$ the majority is wrong more often as $n$ grows. For $p = 0.4$ and $n = 101$, $P_n \approx 0.021$.
- **Equal competence.** It can be relaxed. If the $X_i$ are independent with $\Pr[X_i = 1] = p_i$ and mean $\bar p = \frac1n \sum_i p_i > \tfrac12$, Hoeffding's inequality, which does not need equal distributions, still gives $1 - P_n \le e^{-2n(\bar p - 1/2)^2}$. So the limit holds when $\bar p$ stays above $\tfrac12$ by a fixed amount. Part (a) does not hold in this form, though: adding two weak voters to a jury can lower $P_n$. Grofman, Owen and Feld (1983) studied such extensions.
- **Odd size.** For even $n = 2k$, with ties broken by a fair coin, the probability that the decision is right is exactly $P_{2k-1}$, the value for one voter fewer. So an even jury gains nothing over the odd jury below it.
- **Sincere voting.** The theorem treats each vote as an honest guess. If voters have private signals and the same goal, a voter's vote matters only when the others are tied, and a rational voter may then vote against their own signal. Austen-Smith and Banks (1996) showed that sincere voting need not be a Nash equilibrium in this setting, so the theorem does not apply directly to strategic voters.

## History

Condorcet stated and computed the theorem in his Essai of 1785, the same work that describes the [Condorcet paradox](/condorcet-paradox/) and the [Condorcet winner](/condorcet-winner/). It was little known for a long time, and twentieth-century political science and economics took it up as an argument for democratic decisions. Grofman, Owen and Feld (1983) collected the modern forms and extensions, and later work studied correlated voters, unequal competence and strategic voting, starting with Austen-Smith and Banks (1996).

## References
