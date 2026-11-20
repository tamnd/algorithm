---
tag: YFD0RC
kind: concept
slug: condorcet-paradox
name: Condorcet paradox
aliases:
- voting paradox
- cyclic majorities
area: algorithmic-game-theory/social-choice-and-voting
level: intro
summary: Majority preferences between pairs of candidates can form a cycle even when every voter's ranking is transitive.
prereqs: [preference-profile]
see_also: [condorcet-winner, arrow-impossibility-theorem, smith-set, social-welfare-function, single-peaked-preferences, median-voter-theorem, ranked-pairs, election-control-problem]
sources:
  - book: "Marie Jean Antoine Nicolas de Caritat, marquis de Condorcet, Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix, Imprimerie Royale, Paris, 1785"
    title: Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix
    locator: the observation that the majority decisions on pairs of candidates can contradict each other
  - paper: "Georges-Théodule Guilbaud, Les théories de l'intérêt général et le problème logique de l'agrégation, Économie Appliquée 5 (1952), 501-584"
    locator: the limit probability of a majority cycle among three candidates under the uniform distribution of rankings
  - paper: doi:10.2307/1907926
    title: "David C. McGarvey, A theorem on the construction of voting paradoxes, Econometrica 21(4) (1953), 608-610"
    locator: the theorem that every complete asymmetric relation on the candidates is the majority relation of some profile
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 2 (William S. Zwicker, Introduction to the theory of voting)"
---

The Condorcet paradox is the fact that pairwise majority votes can form a cycle: a majority prefers $a$ to $b$, a majority prefers $b$ to $c$, and a majority prefers $c$ to $a$, although every single voter has a consistent ranking. Condorcet described it in 1785. It means that "the candidate the majority prefers" can fail to exist, so there is no [Condorcet winner](/condorcet-winner/), and that majority rule does not give a [social welfare function](/social-welfare-function/) once there are three candidates. [Arrow's impossibility theorem](/arrow-impossibility-theorem/) shows that the problem is not special to majority rule.

## In plain words

Three friends choose a film. The first likes action best, then comedy, then drama. The second likes comedy, then drama, then action. The third likes drama, then action, then comedy. Two of the three prefer action to comedy, two prefer comedy to drama, and two prefer drama to action. Whatever film they pick, two of them prefer some other film. Each friend is reasonable, but the group, deciding by majority, goes round in a circle.

## The idea

Let three voters rank three candidates as follows.

| voter | ranking |
|---|---|
| 1 | $a \succ b \succ c$ |
| 2 | $b \succ c \succ a$ |
| 3 | $c \succ a \succ b$ |

Count each pair. Voters 1 and 3 rank $a$ above $b$, voters 1 and 2 rank $b$ above $c$, and voters 2 and 3 rank $c$ above $a$. So $a$ beats $b$, $b$ beats $c$, and $c$ beats $a$, each by 2 to 1, with margin 1. The majority relation is the cycle $a \to b \to c \to a$. Each candidate loses to another one, so none of them is a Condorcet winner, not even a weak one.

The structure behind it is a Latin square: each candidate is in each position for exactly one voter. The profile is symmetric under the rotation $a \to b \to c \to a$, so no neutral and anonymous rule can choose among the three candidates without breaking a tie.

Three consequences follow.

- **Majority is not transitive.** Individual transitivity does not carry over to the group. So a rule that ranks the candidates by majority on each pair does not always give a ranking.
- **The agenda decides.** Vote on two candidates, then pit the winner against the third. With the agenda "$a$ against $b$, then the winner against $c$", $a$ wins the first vote and $c$ wins the second. Each of the three orders of the agenda elects the candidate that enters last, so whoever sets the agenda chooses the winner. This is the basis of agenda control, one form of the [election control problem](/election-control-problem/).
- **Every pattern is possible.** McGarvey (1953) proved that for every complete asymmetric relation on the candidates there is a profile whose majority relation is that relation. A cycle can involve any number of candidates, and long cycles need more voters.

The paradox goes away on restricted domains. If all voters have [single-peaked preferences](/single-peaked-preferences/) on one axis and $n$ is odd, the majority relation is transitive and the median voter's top choice is the Condorcet winner ([median voter theorem](/median-voter-theorem/)). The profile above is not single-peaked on any axis: each of the three candidates is ranked last by some voter, and on a single-peaked profile one candidate, the middle one of the axis, is ranked last by no voter.

## Examples

**The basic cycle.** The three-voter profile above has margins $+1$ on each edge of the cycle. It is the check value used in the tests of this area.

**A cycle with unequal margins.** Take 4 voters $a \succ b \succ c$, 3 voters $b \succ c \succ a$ and 2 voters $c \succ a \succ b$. Then $a$ beats $b$ by 6 to 3, $b$ beats $c$ by 7 to 2, and $c$ beats $a$ by 5 to 4. The margins 3, 5 and 1 still form a cycle, and there is no Condorcet winner. Condorcet methods resolve it in different ways. [Ranked pairs](/ranked-pairs/) locks the strongest majorities first, $b$ over $c$ (5) and then $a$ over $b$ (3), skips $c$ over $a$ (1), and returns $a \succ b \succ c$. The [Copeland method](/copeland-method/) gives every candidate one win and returns a three-way tie. The [Smith set](/smith-set/) is all three candidates.

**A cycle below a Condorcet winner.** Take the 4 candidates $a, b, c, d$ and the voters $d \succ a \succ b \succ c$, $d \succ b \succ c \succ a$ and $c \succ a \succ b \succ d$. Candidate $d$ beats every other candidate by 2 to 1 and is the Condorcet winner, but among $a$, $b$ and $c$ the majorities are again the cycle $a \to b \to c \to a$. So a Condorcet winner can exist while the majority relation is still not a ranking.

**How often.** If every voter's ranking is uniform and independent (impartial culture), the probability that three candidates have no Condorcet winner, which for an odd $n$ means a cycle, is exactly $1/18 \approx 0.056$ for 3 voters, $5/72 \approx 0.069$ for 5 voters and $875/11664 \approx 0.075$ for 7 voters, by enumeration of all profiles. As $n \to \infty$ it tends to

$$\frac{1}{4} - \frac{3}{2\pi} \arcsin\frac{1}{3} \approx 0.0877$$

(Guilbaud 1952). For 51 voters the exact value is about 0.0861. These numbers hold for this model only; when the voters' rankings are correlated, the probability can be much smaller or larger.

## Where it is used

- **Arrow's theorem.** The paradox shows that majority rule on pairs fails to give a ranking. [Arrow's impossibility theorem](/arrow-impossibility-theorem/) shows that every rule with Pareto and independence of irrelevant alternatives, other than a dictatorship, fails in a similar way, and its proofs use the same cyclic profiles.
- **Design of Condorcet methods.** Rules that elect the [Condorcet winner](/condorcet-winner/) when it exists, such as [ranked pairs](/ranked-pairs/), the [Schulze method](/schulze-method/) and the [Copeland method](/copeland-method/), differ only in how they break cycles. The [Smith set](/smith-set/) is the smallest set of candidates that wins against every candidate outside it, and it contains the whole top cycle.
- **Rank aggregation.** The cycles of the majority graph are why the [Kemeny ranking](/kemeny-rank-aggregation/) is hard to compute: it must give up some majorities, and the cheapest choice is a feedback arc set problem.
- **Strategic voting and agenda setting.** Cycles create the room for manipulation that the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) makes general, and they give the agenda setter power, as above.
- **Ensembles and committees.** Pairwise majority among several classifiers or experts can also cycle, so an ensemble that compares options in pairs needs an explicit tie and cycle rule.

## References
