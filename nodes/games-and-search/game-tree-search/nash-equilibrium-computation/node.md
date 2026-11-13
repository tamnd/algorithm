---
tag: EYAA2N
kind: problem
slug: nash-equilibrium-computation
name: Nash equilibrium computation
aliases:
- equilibrium computation
area: games-and-search/game-tree-search
level: research
summary: Given a finite game, find a Nash equilibrium; one LP for two-player zero-sum games, PPAD-complete for two-player general-sum games.
prereqs: [nash-equilibrium, nash-existence-theorem, linear-programming-problem, ppad]
see_also: [minimax-theorem, lp-duality, simplex-method, imperfect-information-game, counterfactual-regret-minimization, np-hard, regret]
sources:
  - paper: doi:10.1145/1516512.1516516
    title: "Xi Chen, Xiaotie Deng and Shang-Hua Teng, Settling the complexity of computing two-player Nash equilibria, Journal of the ACM 56(3) (2009), 1-57"
    locator: PPAD-completeness of two-player Nash, and of 1/poly approximate equilibria (no FPTAS unless PPAD is in P)
  - paper: doi:10.1137/070699652
    title: "Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009), 195-259"
    locator: PPAD-completeness of approximate Nash equilibria for three or more players, through graphical games
  - paper: doi:10.1137/080720826
    title: "Kousha Etessami and Mihalis Yannakakis, On the complexity of Nash equilibria and other fixed points, SIAM Journal on Computing 39(6) (2010), 2531-2597"
    locator: the class FIXP, and FIXP-completeness of exact equilibria for three or more players
  - paper: doi:10.1137/0112033
    title: "C. E. Lemke and J. T. Howson, Jr., Equilibrium points of bimatrix games, Journal of the Society for Industrial and Applied Mathematics 12(2) (1964), 413-423"
    locator: the complementary pivoting algorithm and the odd number of equilibria of nondegenerate games
  - paper: doi:10.1111/j.1468-0262.2006.00667.x
    title: "Rahul Savani and Bernhard von Stengel, Hard-to-solve bimatrix games, Econometrica 74(2) (2006), 397-429"
    locator: games where every Lemke and Howson path is exponentially long
  - paper: doi:10.1016/0899-8256(89)90006-7
    title: "Itzhak Gilboa and Eitan Zemel, Nash and correlated equilibria, some complexity considerations, Games and Economic Behavior 1(1) (1989), 80-93"
    locator: NP-hardness of equilibria with given properties, and the linear program for correlated equilibria
  - paper: doi:10.1016/j.geb.2008.02.015
    title: "Vincent Conitzer and Tuomas Sandholm, New complexity results about Nash equilibria, Games and Economic Behavior 63(2) (2008), 621-641"
    locator: NP-completeness for symmetric two-player games, inapproximability of optimal equilibria, and #P-hardness of counting
  - paper: doi:10.1145/779928.779933
    title: "Richard J. Lipton, Evangelos Markakis and Aranyak Mehta, Playing large games using simple strategies, Proceedings of the 4th ACM Conference on Electronic Commerce (EC 2003), 36-41"
    locator: epsilon-equilibria with supports of size O(log n / epsilon^2) and the quasi-polynomial algorithm
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 2 (Papadimitriou, the complexity of finding Nash equilibria) and Chapter 3 (von Stengel, equilibrium computation for two-player games, support enumeration and the Lemke and Howson algorithm)
---

Nash equilibrium computation asks for an equilibrium of a given finite game. An equilibrium always exists ([Nash's theorem](/nash-existence-theorem/)), so this is a search problem with a guaranteed answer, not a decision problem. The answer is easy for two-player [zero-sum games](/zero-sum-game/), where one linear program solves the game. For two-player general-sum games, and for approximate equilibria with more players, the problem is complete for the class [PPAD](/ppad/), and the known exact algorithms take exponential time in the worst case.

## In plain words

You are given the rules and the scores of a game. You must find a way for each player to mix their choices so that nobody wants to change their own mix. We know that such a mix always exists, so the question is only how fast we can find it. If one player's gain is the other's loss, a standard optimization method finds it quickly. In other games, all known methods can be very slow on some games, and there is strong evidence that every method is. Even checking whether some stable mix gives a good score to everybody is as hard as the hardest puzzle problems.

## Definition

**Input.** A finite game in normal form: players $1, \ldots, n$, pure strategy sets $S_1, \ldots, S_n$, and rational payoffs $u_i(s)$ for every player $i$ and profile $s$. The input size is the number of bits of the payoff tables, about $n \prod_i |S_i|$ numbers. For two players it is a *bimatrix game* $(A, B)$ of size $m \times n$, with $A_{ij}$ the payoff of the row player and $B_{ij}$ that of the column player.

**Output.** A [Nash equilibrium](/nash-equilibrium/) $\sigma$: mixed strategies such that $u_i(s_i, \sigma_{-i}) \le u_i(\sigma)$ for all $i$ and all $s_i \in S_i$.

**Model.** The cost is counted in bit operations as a function of the input size. The output must be checkable in polynomial time, which the pure deviation test gives: at most $\sum_i |S_i|$ comparisons of exact rational numbers.

**Exact and approximate output.** For two players, an equilibrium with rational probabilities of polynomial bit size exists, so an exact output is possible. For three or more players there are games with rational payoffs whose only equilibria are irrational, so the problem is posed in an approximate form:

- an *$\varepsilon$-equilibrium* ("weak" approximation): no player gains more than $\varepsilon$ by a deviation, with payoffs scaled to $[0, 1]$;
- a profile within distance $\varepsilon$ of an exact equilibrium ("strong" approximation), which is much harder.

## Variants

- **Two-player zero-sum ($B = -A$).** Solved by one linear program. Also its extensive form with perfect recall, through the sequence form ([imperfect-information games](/imperfect-information-game/)).
- **Two-player general sum (2-NASH).** Find any equilibrium of a bimatrix game.
- **Three or more players (k-NASH).** Find an $\varepsilon$-equilibrium, or a point near an exact one.
- **All equilibria.** List all equilibria of a nondegenerate bimatrix game, or all extreme points of the equilibrium components.
- **An equilibrium with a property.** Decide whether there is an equilibrium where a given player gets at least $k$, the total payoff is at least $k$, a given strategy is played, the equilibrium is unique, and so on.
- **Correlated equilibrium.** Find a distribution on profiles from which no player wants to deviate after hearing their own part. It is a linear feasibility problem, so it is easy, even with an objective.
- **Succinct games.** Graphical, polymatrix or congestion games, where the input is much smaller than the payoff table.

## Examples

**Battle of the sexes.** $A = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$. Support enumeration tries the $\binom{4}{2} - 1 = 5$ pairs of nonempty supports of equal size. Of the four pure pairs, (1, 1) and (2, 2) pass the deviation test, and (1, 2) and (2, 1) fail. For the full supports, the column player's mix $y = (q, 1-q)$ must make the two rows equal for the row player, $2q = 1 - q$, so $q = 1/3$, and the row player's mix must make the columns equal for the column player, $p = 2(1-p)$, so $p = 2/3$. The answer is three equilibria: the two pure ones and $((2/3, 1/3), (1/3, 2/3))$, with payoffs $(2/3, 2/3)$.

**Random games.** On 200 random $3 \times 3$ games with integer payoffs from $-9$ to 9 (seed 1951), filtered so that no pure strategy has two best responses, support enumeration found 1 equilibrium in 146 games, 3 in 52, 5 in 1 and 7 in 1. The number is always odd, as the theory of Lemke and Howson predicts for nondegenerate games. Every profile it returned passed the exact deviation test.

**A degenerate game.** If every payoff is 1 for both players, every profile is an equilibrium, a continuum. Square supports of size 2 give singular systems, and support enumeration returns only the four pure equilibria. Complete lists for degenerate games need the equilibrium components, for example by enumerating the vertices of the best-response polytopes.

**Zero sum.** Matching pennies, $A = \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$ and $B = -A$, has the single equilibrium $((1/2, 1/2), (1/2, 1/2))$, which the linear program of the [minimax theorem](/minimax-theorem/) also returns.

## Known algorithms

- **Linear programming (zero sum).** Write the row player's problem as $\max v$ subject to $x^{\mathsf T} A \ge v \mathbf{1}$, $x \in \Delta_m$; the dual is the column player's problem ([minimax theorem](/minimax-theorem/), [LP duality](/lp-duality/)). The [simplex method](/simplex-method/) is fast in practice, and the ellipsoid or interior point methods give polynomial time.
- **Support enumeration (two players).** For each pair of supports $I \subseteq [m]$, $J \subseteq [n]$ with $|I| = |J|$, solve the linear equations that make each player indifferent on their support, and keep the solution if it is a probability vector, positive on the support, and no pure strategy outside the support does better. In a nondegenerate game every equilibrium has supports of equal size, so this lists all equilibria. There are $\sum_{k \ge 1} \binom{m}{k}\binom{n}{k} = \binom{m+n}{m} - 1$ pairs, each solved in $O((m+n)^3)$ arithmetic operations, so the time is exponential. Porter, Nudelman and Shoham (2008) showed that trying small and balanced supports first finds an equilibrium fast on many generated games.
- **Lemke and Howson (two players).** Complementary pivoting on the two best-response polytopes. From an artificial start it follows a path of almost complementary vertices that must end at an equilibrium, which is a constructive version of the parity argument behind PPAD. It also shows that a nondegenerate game has an odd number of equilibria. Savani and von Stengel (2006) built games where every Lemke and Howson path is exponentially long.
- **Vertex enumeration (two players).** Enumerate the vertices of the best-response polytopes and match complementary pairs. It finds all extreme equilibria, also for degenerate games.
- **Approximation (two players).** Lipton, Markakis and Mehta (2003) showed that an $\varepsilon$-equilibrium with supports of size $O(\log n / \varepsilon^2)$ exists, so trying all such supports finds one in time $n^{O(\log n / \varepsilon^2)}$, which is quasi-polynomial for fixed $\varepsilon$. Simple polynomial methods give constant $\varepsilon$, for example $1/2$, and the best known constant is near $1/3$.
- **Learning dynamics.** Regret-minimizing players, such as [counterfactual regret minimization](/counterfactual-regret-minimization/) in game trees or [multiplicative weights](/multiplicative-weights-update/) in matrix games, have average strategies that converge to an equilibrium in two-player zero-sum games. In general-sum games they converge only to the larger set of coarse correlated equilibria ([regret](/regret/)).
- **Three or more players.** Homotopy and simplicial methods (Scarf's algorithm, the global Newton method of Govindan and Wilson), and polynomial system solving for exact equilibria. All take exponential time in the worst case.

## Bounds

- **Zero sum: polynomial.** Two-player zero-sum games, and their extensive forms with perfect recall, are solved in polynomial time by linear programming.
- **Two players: PPAD-complete.** Chen, Deng and Teng (2009) proved that 2-NASH is PPAD-complete, and that finding a $1/n^{\Theta(1)}$-approximate equilibrium is too, so there is no fully polynomial approximation scheme unless every PPAD problem is in P. Rubinstein (2016) showed that, under an exponential time hypothesis for PPAD, constant $\varepsilon$ needs quasi-polynomial time, which matches the algorithm of Lipton, Markakis and Mehta.
- **Three or more players.** Finding an $\varepsilon$-equilibrium is PPAD-complete (Daskalakis, Goldberg and Papadimitriou 2009, through graphical games). Finding an exact equilibrium, or a point near one, is FIXP-complete (Etessami and Yannakakis 2010), and the strong approximation is at least as hard as the square-root sum problem.
- **NP-hard properties.** Deciding whether a bimatrix game has an equilibrium with a given property is NP-complete for many properties: payoff at least $k$ for a player, uniqueness, a given strategy in or out of the support, Pareto optimality (Gilboa and Zemel 1989; Conitzer and Sandholm 2008, already for symmetric games). Finding an optimal equilibrium is also hard to approximate, and counting the equilibria is #P-hard.
- **Correlated equilibria: polynomial.** A correlated equilibrium, also one that maximizes a linear objective, is found by one linear program in the size of the payoff table (Gilboa and Zemel 1989).
- **Why not NP-hard.** If 2-NASH were NP-hard under the usual reductions, then NP would equal coNP, because every instance has a solution that is easy to check. This is why the right class is a subclass of TFNP, the total search problems, and PPAD is that subclass.

## Reductions

- **To and from PPAD.** End-of-the-line reduces to 2-NASH (Chen, Deng and Teng, through the circuit games of Daskalakis, Goldberg and Papadimitriou), and 2-NASH reduces to end-of-the-line through Lemke and Howson, so they are equivalent.
- **k players to 2 players.** Approximate equilibria of games with any fixed number of players reduce to the two-player case, by the same PPAD-completeness.
- **Zero sum to linear programming and back.** A zero-sum matrix game is a linear program, and Dantzig (1951) reduced linear programs to symmetric zero-sum games, a reduction that Adler (2013) completed ([minimax theorem](/minimax-theorem/)).
- **Symmetrization.** A bimatrix game $(A, B)$ with positive payoffs becomes the symmetric game $\begin{pmatrix} 0 & A \\ B^{\mathsf T} & 0 \end{pmatrix}$, whose symmetric equilibria give equilibria of $(A, B)$ after normalization.

## Applications

- **Poker and other card games.** Two-player zero-sum games of [imperfect information](/imperfect-information-game/) are solved by the sequence-form linear program or approximated by [counterfactual regret minimization](/counterfactual-regret-minimization/); heads-up limit Texas hold'em was essentially solved this way in 2015.
- **Security games.** Stackelberg and zero-sum models for patrols and inspections are solved by linear and integer programs.
- **Markets and mechanism design.** Equilibrium computation checks predictions of auction and market models, and its hardness limits the claim that real players reach equilibria.
- **Lower bounds.** In complexity theory, the zero-sum case gives lower bounds on randomized algorithms through [Yao's minimax principle](/yao-minimax-principle/).

## References
