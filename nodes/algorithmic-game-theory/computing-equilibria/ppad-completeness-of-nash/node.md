---
tag: C5WB5A
kind: theorem
slug: ppad-completeness-of-nash
name: PPAD-completeness of Nash equilibrium
aliases:
- Daskalakis-Goldberg-Papadimitriou theorem
- Chen-Deng theorem
area: algorithmic-game-theory/computing-equilibria
level: research
summary: Finding a Nash equilibrium of a game is PPAD-complete, already for two players and for inverse-polynomial approximation.
prereqs: [ppad, end-of-the-line-problem, nash-existence-theorem, epsilon-nash-equilibrium, bimatrix-game]
see_also: [sperner-lemma, lemke-howson-algorithm, graphical-game, rubinstein-approximate-nash-lower-bound, lipton-markakis-mehta-algorithm, hardness-of-optimal-nash-equilibria, ppad-hardness-of-arrow-debreu, nash-equilibrium-computation]
sources:
  - paper: doi:10.1137/070699652
    title: "Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009), 195-259"
    locator: the reduction from END OF THE LINE through a 3-dimensional Brouwer problem and arithmetic circuits to graphical games and to games with 3 or more players; conference version in STOC 2006
  - paper: doi:10.1145/1516512.1516516
    title: "Xi Chen, Xiaotie Deng and Shang-Hua Teng, Settling the complexity of computing two-player Nash equilibria, Journal of the ACM 56(3) (2009), article 14"
    locator: two-player Nash and its 1/poly(n) approximation are PPAD-complete, and the consequences for an FPTAS and for smoothed complexity; conference versions in FOCS 2006
  - paper: doi:10.1016/S0022-0000(05)80063-7
    title: "Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3) (1994), 498-532"
    locator: the class PPAD and the membership of Nash equilibria and Brouwer fixed points in it
  - paper: doi:10.1137/080720826
    title: "Kousha Etessami and Mihalis Yannakakis, On the complexity of Nash equilibria and other fixed points, SIAM Journal on Computing 39(6) (2010), 2531-2597"
    locator: the class FIXP and the FIXP-completeness of exact Nash equilibria for 3 or more players
---

Every finite game has a [Nash equilibrium](/nash-equilibrium/) by [Nash's theorem](/nash-existence-theorem/), so the question is not whether one exists but how fast one can be found. This theorem says that the search problem is complete for the class [PPAD](/ppad/), the problems that reduce to [END OF THE LINE](/end-of-the-line-problem/). Daskalakis, Goldberg and Papadimitriou proved it for games with 3 or more players, and Chen, Deng and Teng for two players, also for approximation within an inverse polynomial. So a polynomial algorithm for two-player games would give one for every problem in PPAD, which includes Brouwer fixed points and the [Sperner lemma](/sperner-lemma/). The result is the main evidence that no polynomial algorithm for Nash equilibria exists. It is not a proof, because P versus PPAD is open.

## Statement

A game in normal form has $k$ players, a finite set of pure strategies for each, and rational payoffs. For two players it is a [bimatrix game](/bimatrix-game/) $(A, B)$ of size $m \times n$, where $m$ and $n$ are the numbers of pure strategies. A profile of [mixed strategies](/mixed-strategy/) is an $\varepsilon$-Nash equilibrium if no player gains more than $\varepsilon$ by a change of strategy, with payoffs scaled to $[0, 1]$ ([epsilon-Nash equilibrium](/epsilon-nash-equilibrium/)). Pure deviations are enough for this test, because a mixed strategy is a [best response](/best-response/) if and only if its support is inside the set of pure best responses.

**Theorem 1 (Daskalakis, Goldberg and Papadimitriou 2009).** For every fixed $k \ge 3$, the problem "given a $k$-player game in normal form and $\varepsilon > 0$ in binary, find an $\varepsilon$-Nash equilibrium" is PPAD-complete. The same holds for [graphical games](/graphical-game/) of bounded degree with 2 strategies for each player.

**Theorem 2 (Chen, Deng and Teng 2009).** The problem "given an $n \times n$ bimatrix game, find a Nash equilibrium" is PPAD-complete. For every constant $c > 0$, the problem "given an $n \times n$ bimatrix game with payoffs in $[0, 1]$, find an $n^{-c}$-Nash equilibrium" is also PPAD-complete.

Membership in PPAD and hardness are both under polynomial-time reductions between search problems. For two players the exact problem makes sense, because there is always an equilibrium with rational entries of polynomial bit length. For 3 or more players an equilibrium can be irrational, so Theorem 1 is about approximation. The exact problem for $k \ge 3$ is complete for the class FIXP (Etessami and Yannakakis 2010), which is believed to be harder.

## In plain words

Finding a point where every player is happy with its choice is a search with a guaranteed answer. Such searches can be hard even though an answer must exist. There is a basic hard search of this kind: follow a very long path in a huge graph to its end. The theorem says that any method that finds equilibria of two-player games, even rough ones, also finds the ends of such paths. So games are as hard as that basic search, and a fast method for games would make many other hard searches fast too. Nobody has a proof that the basic search is hard, but decades of work have found no fast method.

## Proof

The full proofs are long. Here are the steps and the main ideas.

**Membership.** For two players, the [Lemke-Howson algorithm](/lemke-howson-algorithm/) follows a path of complementary pivots on the [best-response polytopes](/best-response-polytope/). The paths form an undirected graph of degree at most 2, whose ends are the artificial equilibrium and the Nash equilibria. A sign rule (the index of an equilibrium, due to Shapley, with a pivoting form by Todd) gives each path a direction that can be computed locally, so the graph is a directed instance of END OF THE LINE with polynomial-size circuits. For any number of players, the approximate problem reduces to an approximate Brouwer fixed point of Nash's map, and that reduces to a Sperner problem on a fine grid, which is in PPAD by the path proof of the [Sperner lemma](/sperner-lemma/). The grid must be fine enough that a fully colored cell gives an $\varepsilon$-Nash equilibrium. A Lipschitz bound of Nash's map in terms of the payoffs gives the size.

**Hardness for 3 or more players.**

1. *END OF THE LINE to a 3-dimensional Brouwer problem.* The unit cube is divided into small cubes, and each path of the instance is embedded as a thin tube. Each small cube gets one of four displacement vectors. Far from the tubes the map moves points toward one corner, and inside each tube it moves points along the tube. A point where all four colors meet, an approximate fixed point, can only appear at the end of a tube, and its position gives an end of a line. A circuit computes the color of each small cube from the circuits $S$ and $P$.
2. *Brouwer to arithmetic circuits.* The color circuit is turned into an arithmetic circuit on real values in $[0, 1]$ with the gates assignment, addition, subtraction, multiplication by a constant and comparison. A fixed point of the circuit, with every gate correct up to a small error, is an approximate fixed point of the map. The comparison gate is the brittle part: it can be wrong when its inputs are very close. Averaging over many nearby points makes the result robust.
3. *Arithmetic circuits to graphical games.* Each value is the probability that one player with 2 strategies plays its first strategy. Each gate is a small game gadget whose equilibria force the output player to play the gate value. So the $\varepsilon$-Nash equilibria of the graphical game, of degree 3, encode approximate fixed points.
4. *Graphical games to normal form.* The graph is colored so that no two players with the same color are near each other, with a constant number of colors. One "lawyer" player represents each color class, and a matching-pennies game between the lawyers forces each lawyer to spread its probability almost uniformly over the players it represents. This gives 4 players. Daskalakis and Papadimitriou, and Chen and Deng, reduced the number to 3 in 2005.

**Hardness for 2 players (Chen, Deng and Teng).** The two players play the roles of all the lawyers at once: each node of the circuit owns a pair of strategies of each player, and each gate value is coded by the probabilities that the players put on these pairs. Payoff entries between the pairs implement the gates, and a large matching-pennies part forces each player to spread its probability almost evenly over the pairs. Chen and Deng first proved the exact case from a 2-dimensional discrete fixed-point problem. For the approximate case, Chen, Deng and Teng start from a discrete fixed-point problem in high dimension, with a constant number of grid points on each side. Then the gates may make errors that are polynomially small instead of exponentially small, and the reduction works for $\varepsilon = n^{-c}$. Since an exact equilibrium is an $n^{-c}$-equilibrium, the exact problem is hard too, and it is in PPAD by Lemke-Howson.

## Consequences

- **No FPTAS.** If the $\varepsilon$-Nash problem for two players had an algorithm polynomial in $n$ and $1/\varepsilon$, then Theorem 2 would put PPAD in P. So no [FPTAS](/fptas/) exists unless PPAD is contained in P.
- **Smoothed complexity.** Chen, Deng and Teng also showed that Lemke-Howson, or any algorithm, cannot have polynomial [smoothed complexity](/smoothed-analysis/) for bimatrix games unless PPAD is contained in RP.
- **Not NP-hard.** The Nash problem is in [TFNP](/tfnp/), so it is not [NP-hard](/np-hard/) unless NP equals coNP. Questions about a Nash equilibrium with a given property are NP-hard instead ([hardness of optimal Nash equilibria](/hardness-of-optimal-nash-equilibria/)).
- **Markets and other equilibria.** The same techniques show that Arrow-Debreu equilibria with piecewise-linear concave utilities are PPAD-complete ([PPAD-hardness of Arrow-Debreu](/ppad-hardness-of-arrow-debreu/)).
- **Special classes.** Win-lose games, with payoffs 0 and 1, are still PPAD-complete (Abbott, Kane and Valiant 2005). Zero-sum games are solved in polynomial time by linear programming ([zero-sum games by LP](/zero-sum-game-linear-programming/)), and so are games of rank 1 (Adsul, Garg, Mehta and Sohoni 2011).

## Tightness

Theorem 2 needs $\varepsilon$ to go to 0 with $n$. For a constant $\varepsilon$, the [Lipton-Markakis-Mehta algorithm](/lipton-markakis-mehta-algorithm/) finds an $\varepsilon$-Nash equilibrium in time $n^{O(\log n / \varepsilon^2)}$, which is [quasi-polynomial](/quasi-polynomial-time/). So constant-$\varepsilon$ Nash for two players is not PPAD-complete unless every problem in PPAD has quasi-polynomial algorithms. Rubinstein (2016) showed the matching lower bound under an exponential-time hypothesis for PPAD ([Rubinstein's lower bound](/rubinstein-approximate-nash-lower-bound/)). Simple polynomial methods reach constant $\varepsilon$, such as $1/2$ ([DMP algorithm](/dmp-half-approximate-nash/)) and about $1/3$. For games with many players and 2 strategies each, Rubinstein (2015) showed that some constant $\varepsilon$ is already PPAD-hard. The question whether P equals PPAD is open, as of November 2026.

## History

Nash (1950, 1951) proved existence with fixed-point theorems. Lemke and Howson (1964) gave a path-following algorithm for two players, and Savani and von Stengel (2006) showed that it can take exponential time from every start ([Savani-von Stengel theorem](/savani-von-stengel-theorem/)). Papadimitriou (1994) defined PPAD and showed that Nash is in it. In 2005 Daskalakis, Goldberg and Papadimitriou proved hardness for 4 players, and within weeks Daskalakis and Papadimitriou, and Chen and Deng, independently proved it for 3. Chen and Deng proved it for 2 players in 2006, and with Teng extended it to inverse-polynomial approximation. The journal versions appeared in 2009.

## References
