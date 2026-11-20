---
tag: M509ET
kind: algorithm
slug: iterated-elimination-of-dominated-strategies
name: Iterated elimination of dominated strategies
aliases:
- iterated dominance
- IESDS
area: algorithmic-game-theory/strategic-games
level: intro
summary: Repeatedly removes strictly dominated actions from a finite game until none remains. Every Nash equilibrium survives, and the result does not depend on the order.
model: word-ram
complexity:
  vars: {k: "the total number of pure strategies of all players", t: "the number of pure profiles (the size of one payoff table)"}
  time: {worst: O(k^2 t)}
  space: {extra: O(k)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1979
  people: [Hervé Moulin]
  note: Moulin named the games that the procedure solves dominance solvable in 1979; Pearce in 1984 linked strict dominance by mixed strategies to best responses, and Gilboa, Kalai and Zemel in 1993 proved the weak form hard.
prereqs: [dominant-strategy, mixed-strategy, linear-programming-problem]
see_also: [best-response, pure-nash-equilibrium, nash-equilibrium, prisoners-dilemma, lp-duality, np-complete, zero-sum-game-linear-programming, normal-form-game]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 4, Section 4.2 (iterated elimination of strictly dominated actions, and its link to rationalizability) and Section 4.3 (weakly dominated actions)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 4 (computing solution concepts of normal-form games), the section on domination and iterated removal
  - paper: "Itzhak Gilboa, Ehud Kalai and Eitan Zemel, The complexity of eliminating dominated strategies, Mathematics of Operations Research 18(3) (1993), 553-565"
    title: The complexity of eliminating dominated strategies
    locator: the NP-completeness of questions about the iterated elimination of weakly dominated strategies, with dominance by pure strategies
  - paper: doi:10.1145/1064009.1064019
    title: "Vincent Conitzer and Tuomas Sandholm, Complexity of (iterated) dominance, Proceedings of the 6th ACM Conference on Electronic Commerce (EC 2005), 88-97"
    locator: one LP decides dominance by a mixed strategy; iterated strict dominance is path independent and polynomial; deciding if a strategy can be removed by iterated weak dominance is NP-complete
  - paper: "David G. Pearce, Rationalizable strategic behavior and the problem of perfection, Econometrica 52(4) (1984), 1029-1050"
    title: Rationalizable strategic behavior and the problem of perfection
    locator: the lemma that a strategy is never a best response if and only if a mixed strategy strictly dominates it
  - paper: "B. Douglas Bernheim, Rationalizable strategic behavior, Econometrica 52(4) (1984), 1007-1028"
    title: Rationalizable strategic behavior
    locator: the definition of rationalizable strategies
  - paper: "Hervé Moulin, Dominance solvable voting schemes, Econometrica 47(6) (1979), 1337-1351"
    title: Dominance solvable voting schemes
    locator: the definition of a dominance solvable game
---

Iterated elimination of dominated strategies is the procedure that removes, one at a time, a strategy of some player that another strategy beats against every remaining choice of the others, and repeats until no such strategy is left. It works on a finite [normal-form game](/normal-form-game/). With strict dominance it never removes a strategy that a [Nash equilibrium](/nash-equilibrium/) uses, and the set that survives does not depend on the order of removal. With weak dominance, the topic of the variant section, both properties fail. A [dominant strategy](/dominant-strategy/) is the special case in which one strategy beats all the others in one step.

## In plain words

Some choices are bad whatever the others do: another choice of the same player is better in every case. A sensible player never makes such a choice, so we can cross it out. Once it is gone, the other players know it is gone, and some of their own choices may now be bad in every remaining case, so we cross those out too. We repeat until nothing more can be crossed out. Sometimes one choice per player is left, and the game is solved. Often more is left, and the method only makes the game smaller. The method must compare against mixtures of choices too, not only single choices. It is safe when "better" means strictly better in every case. When "better" only means never worse, the order of crossing out changes the result.

## The problem

The input is a finite game with players $N = \{1, \ldots, n\}$, finite sets $S_i$ of pure strategies and utilities $u_i : S \to \mathbb{Q}$ on $S = S_1 \times \cdots \times S_n$, which each player maximizes. For sets $A_i \subseteq S_i$, write $A_{-i}$ for the product of the $A_j$ with $j \neq i$. A strategy $a \in A_i$ is *strictly dominated relative to $A$* if some mixed strategy $\sigma_i$ on $A_i$ has

$$\sum_{b \in A_i} \sigma_i(b)\, u_i(b, t) > u_i(a, t) \quad \text{for every } t \in A_{-i}.$$

If $\sigma_i$ can be taken pure, $a$ is strictly dominated *by a pure strategy*. The output is a product $A = A_1 \times \cdots \times A_n$ of nonempty sets, reached from $S$ by removing dominated strategies one at a time, such that no strategy in $A$ is strictly dominated relative to $A$. The game is *dominance solvable* if each $A_i$ has one element.

## The algorithm

```pseudo id=main
IESDS(G, DOMINATED)
L1  A_i ← S_i for every player i
L2  repeat
L3      for each player i and each a in A_i, in a fixed order:
L4          if DOMINATED(G, A, i, a) returns a witness w:
L5              A_i ← A_i minus {a}
L6              append (i, a, w) to the log and go back to L2
L7  until no call of line L4 returns a witness; return A and the log
```

The test DOMINATED decides one of three relations:

- **Strict, by a pure strategy.** Look for $b \in A_i$ with $u_i(b, t) > u_i(a, t)$ for every $t \in A_{-i}$. This is a direct comparison of two rows of the payoff table of player $i$.
- **Strict, by a mixed strategy.** Solve one linear program: maximize $z$ subject to $\sum_{b \neq a} x_b\,(u_i(b, t) - u_i(a, t)) \ge z$ for every $t \in A_{-i}$, $x \ge 0$ and $\sum_b x_b = 1$. The strategy $a$ is dominated exactly when the optimum $z^*$ is positive, and then $x$ is the witness. The program is the [linear program](/linear-programming-problem/) of a zero-sum game, so [LP duality](/lp-duality/) gives a certificate in the other case: a probability distribution $q$ on $A_{-i}$ against which $a$ is a [best response](/best-response/).
- **Weak, by a pure strategy.** Look for $b$ with $u_i(b, t) \ge u_i(a, t)$ for every $t \in A_{-i}$ and $>$ for at least one $t$. This is the variant whose result depends on the order.

Line L6 restarts the scan after each removal. That keeps the loop simple to analyze. An implementation may also continue the scan, since by the order independence below the result is the same for both strict tests.

## Example

Take the bimatrix game below, rows T, M, B for player 1 and columns L, C, R for player 2, row payoff first.

| | L | C | R |
| --- | --- | --- | --- |
| T | 4, 3 | 5, 1 | 6, 2 |
| M | 2, 1 | 8, 4 | 3, 6 |
| B | 3, 0 | 9, 6 | 2, 8 |

With the pure test and the order "player 1 first, strategies in order", the run is:

| step | rows left | columns left | removed | witness | why |
| --- | --- | --- | --- | --- | --- |
| 1 | T, M, B | L, C, R | column C | R | column payoffs 2, 6, 8 beat 1, 4, 6 |
| 2 | T, M, B | L, R | row M | T | against L and R, T gets 4, 6 and M gets 2, 3 |
| 3 | T, B | L, R | row B | T | T gets 4, 6 and B gets 3, 2 |
| 4 | T | L, R | column R | L | against T, L gives 3 and R gives 2 |
| 5 | T | L | none | | |

The game is dominance solvable, and (T, L) with payoffs (4, 3) is its only Nash equilibrium, pure or mixed. In the first step no row is dominated: M is the best row against C, and T is the best row against L and R. Only after C is gone do rows M and B become dominated.

**Mixed dominance.** In the game with rows T, M, B and columns L, R where the row payoffs are T = (3, 0), M = (0, 3) and B = (1, 1), no pure strategy dominates B: T loses to B against R, and M loses to B against L. The mix $\frac12 T + \frac12 M$ gets $3/2$ against each column, which beats 1, so B is strictly dominated by a mixed strategy. The pure test stops at once and keeps all three rows; the mixed test removes B.

**Order matters for weak dominance.** Take rows T, M, B and columns L, R with payoffs (1, 1), (0, 0) in row T, (1, 1), (2, 1) in row M and (0, 0), (2, 1) in row B. M weakly dominates both T and B. If T goes first, R weakly dominates L, and the result is rows M and B against R, with payoffs (2, 1). If B goes first, L weakly dominates R, and the result is rows T and M against L, with payoffs (1, 1). If T and then B go, the result is row M against both columns. Three orders give three different games.

## Correctness

The file proofs/correctness.md proves four claims for both strict tests. The loop stops after at most $\sum_i |S_i| - n$ removals, because each pass through line L5 removes one strategy and no set becomes empty: a strategy that is alone in $A_i$ cannot be dominated. When it stops, no remaining strategy is dominated relative to $A$, by the exit condition of line L7. No removed strategy is played with positive probability in any Nash equilibrium, because a dominated strategy is never a best response to a profile of the others that lives in $A_{-i}$, and a mixed strategy is a best response only if its support is inside the set of pure best responses $BR_i(\sigma_{-i})$. Finally, the result is the same for every order of removal, and every Nash equilibrium of the game restricted to $A$ is a Nash equilibrium of the full game. Together these say that the procedure loses no equilibrium and adds none.

## Complexity

Let $k = \sum_i |S_i|$ and let $t = |S|$ be the number of pure profiles, so the input holds $n t$ numbers. For the pure test, one call for the pair $(a, b)$ of player $i$ compares $|A_{-i}| \le t / |S_i|$ pairs of payoffs. One full scan of line L3 tries at most $|S_i|^2$ pairs for player $i$, which costs at most $|S_i| \cdot t$ comparisons, and $k\,t$ in total. There are at most $k - n + 1$ scans, so the time is $O(k^2 t)$ comparisons in the worst case, in the [word-RAM](/word-ram/) model with payoffs of bounded size. For a bimatrix game with $m$ rows and $n$ columns this is $O((m + n)^2 m n)$. The extra space is $O(k)$ for the sets $A_i$ and the log.

The mixed test solves one LP with $|A_i|$ variables and $|A_{-i}|$ constraints per call, so the whole procedure runs in time polynomial in the input size and its bit length $L$ with any polynomial LP method, such as the [ellipsoid method](/ellipsoid-method/) or an interior point method (Conitzer and Sandholm 2005). The [simplex method](/simplex-method/) is fast in practice but exponential in the worst case. The reference code solves the small LP by trying every vertex, which is exponential and meant only for the games of its tests.

## Properties

- **Equilibria survive.** Every mixed Nash equilibrium of $G$ has its support inside the result, and every equilibrium of the reduced game is an equilibrium of $G$. So a dominance solvable game has exactly one Nash equilibrium, and it is pure.
- **Order independence.** For strict dominance, by pure or by mixed strategies, every order of removal gives the same $A$ (Conitzer and Sandholm 2005; Osborne and Rubinstein, Section 4.2).
- **Mixed is stronger than pure.** The mixed test removes every strategy that the pure test removes, and sometimes more, as in the example. The result of the mixed test is always contained in the result of the pure test.
- **Rationalizability.** With two players, the strategies that survive mixed strict dominance are exactly the rationalizable ones of Bernheim and Pearce (1984). With three or more players this holds when beliefs about the others may be correlated; the LP certificate $q$ above is such a correlated belief.
- **Common knowledge.** Each round of removal uses one more level of "each player knows that the others are rational". The game is solved only if rationality is common knowledge up to the number of rounds.

## Variants and improvements

- **Weak dominance.** Remove weakly dominated strategies. The result depends on the order, as the example shows, and it can remove Nash equilibria: in the first order of the example, the pure equilibrium (T, L) is lost. Every equilibrium of the reduced game is still an equilibrium of $G$, so at least one equilibrium always survives. Conitzer and Sandholm (2005) proved that deciding if some order of weak removals eliminates a given strategy is [NP-complete](/np-complete/), and so is deciding if some order leaves one profile, both with and without mixed dominators. Gilboa, Kalai and Zemel (1993) had proved a version of these results for dominance by pure strategies.
- **Simultaneous removal.** Remove in each round all strategies that are weakly dominated relative to the current sets. This fixes one order, so the result is unique, and it is a common way to state weak iterated dominance.
- **Dominance in succinct games.** In Bayesian games and other games given succinctly, iterated dominance by pure strategies can need exponentially many rounds (Conitzer and Sandholm 2005).
- **Extensive games.** Backward induction in a finite game of perfect information removes, at each node, the moves that are worse for the mover; it is related to iterated weak dominance in the normal form, and it gives a [subgame perfect equilibrium](/subgame-perfect-equilibrium/).

## When to use it

Run strict elimination first on any game you want to solve. It is exact, it never loses an equilibrium, and it can shrink the game a lot before an expensive method such as [support enumeration](/support-enumeration/) or the [Lemke-Howson algorithm](/lemke-howson-algorithm/). Use the pure test when speed matters and the mixed test when you have an LP solver, since it removes more. Use weak dominance only with a stated order, and only when you accept that some equilibria may be lost.

## Pitfalls

- **Testing only pure dominators.** A strategy that no pure strategy dominates can still be dominated by a mix, as B in the example. A program that tests only pure strategies is correct but removes less; say which test it uses.
- **Weak for strict.** Writing $\ge$ in place of $>$ in the pure test turns the procedure into weak elimination, which depends on the order and can lose equilibria.
- **Dominance relative to the full game.** After a removal, the test must use the current sets $A_{-i}$ of the other players. A strategy that is not dominated against all of $S_{-i}$ can become dominated against $A_{-i}$, as rows M and B in the example.
- **Floating point.** The test $>$ compares exact payoffs. With floats, two equal sums can compare unequal, and a strategy can be removed by a tie. Keep payoffs rational, as the code does with Fraction.
- **Reading survival as play.** The surviving set is what rationality alone allows. A game where nothing is dominated, such as [matching pennies](/nash-equilibrium/), is not solved by the method at all.

## Implementations

## History

The removal of dominated strategies is part of the classical analysis of games in normal form; Osborne and Rubinstein (1994, Chapter 4) give the standard modern account. Moulin (1979) called a game dominance solvable when iterated removal of dominated strategies leaves one outcome, and used it for voting rules. Bernheim (1984) and Pearce (1984) defined rationalizability, and Pearce proved the lemma that a strategy is never a best response exactly when a mixed strategy strictly dominates it. Gilboa, Kalai and Zemel (1993) studied the complexity of the procedure and proved questions about the weak version NP-complete for pure dominators. Conitzer and Sandholm (2005) gave one LP for mixed dominance, path independence and polynomial time for strict iterated dominance, and NP-completeness for weak iterated dominance with and without mixed dominators.

## References
