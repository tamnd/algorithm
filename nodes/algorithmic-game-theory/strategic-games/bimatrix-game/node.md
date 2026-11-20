---
tag: JZ9GG0
kind: definition
slug: bimatrix-game
name: Bimatrix game
aliases:
- two-player normal-form game
area: algorithmic-game-theory/strategic-games
level: intro
summary: A finite two-player game given by two m by n payoff matrices A and B, one for the row player and one for the column player.
prereqs: [normal-form-game]
see_also: [nash-equilibrium, zero-sum-game, support-enumeration, lemke-howson-algorithm, best-response-polytope, nash-equilibrium-computation, linear-complementarity-problem, mixed-strategy]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3, Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form (bimatrix games, the best response condition, nondegenerate games)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (normal-form games) and Chapter 4 (computing Nash equilibria of two-player games, the LCP form and the Lemke-Howson algorithm)
  - paper: "C. E. Lemke and J. T. Howson, Jr., Equilibrium points of bimatrix games, Journal of the Society for Industrial and Applied Mathematics 12(2) (1964), 413-423"
    title: Equilibrium points of bimatrix games
    locator: the term bimatrix game, the algorithm, and the odd number of equilibria in nondegenerate games
  - paper: doi:10.1145/1516512.1516516
    title: "Xi Chen, Xiaotie Deng and Shang-Hua Teng, Settling the complexity of computing two-player Nash equilibria, Journal of the ACM 56(3) (2009)"
    locator: PPAD-completeness of finding a Nash equilibrium of a bimatrix game, also to within 1/poly(n)
  - paper: doi:10.2307/1969529
    title: "John Nash, Non-cooperative games, Annals of Mathematics 54(2) (1951), 286-295"
    locator: the section on a three-man poker game, whose equilibrium probabilities are irrational
---

A bimatrix game is a finite [normal-form game](/normal-form-game/) with two players, written as a pair $(A, B)$ of $m \times n$ matrices: when the row player chooses row $i$ and the column player chooses column $j$, the row player gets $A_{ij}$ and the column player gets $B_{ij}$. It is the setting of most algorithms for [Nash equilibria](/nash-equilibrium/), such as [support enumeration](/support-enumeration/) and the [Lemke-Howson algorithm](/lemke-howson-algorithm/). The special case $B = -A$ is a [zero-sum game](/zero-sum-game/), which linear programming solves; the general case is PPAD-complete.

## Definition

Let $m, n \ge 1$. A *bimatrix game* is a pair $(A, B)$ of real $m \times n$ matrices. The row player has the pure strategies $1, \ldots, m$, the column player has $1, \ldots, n$, and the profile $(i, j)$ gives payoffs $A_{ij}$ and $B_{ij}$. Both players maximize. On two-player pages, $m$ and $n$ are these sizes; elsewhere $n$ is the number of players. In the notation of normal-form games, $N = \{1, 2\}$, $S_1 = \{1, \ldots, m\}$, $S_2 = \{1, \ldots, n\}$, $u_1(i, j) = A_{ij}$ and $u_2(i, j) = B_{ij}$.

A [mixed strategy](/mixed-strategy/) of the row player is a vector $x$ in the simplex $\Delta_m = \{x \in \mathbb{R}^m : x \ge 0, \sum_i x_i = 1\}$, and one of the column player is $y \in \Delta_n$. The expected payoffs are

$$u_1(x, y) = x^{\mathsf T} A y, \qquad u_2(x, y) = x^{\mathsf T} B y.$$

The vector $Ay$ lists the payoffs of the rows against $y$, and $x^{\mathsf T} B$ lists the payoffs of the columns against $x$. A pair $(x, y)$ is a Nash equilibrium if and only if

$$x^{\mathsf T} A y \ge (Ay)_i \ \text{ for every row } i, \qquad x^{\mathsf T} B y \ge (x^{\mathsf T} B)_j \ \text{ for every column } j.$$

Pure deviations are enough because $x'^{\mathsf T} A y$ is an average of the entries of $Ay$. The same fact gives the *best response condition*: $x$ is a best response to $y$ if and only if every row $i$ with $x_i > 0$ has $(Ay)_i = \max_k (Ay)_k$, and the same for $y$ ([best response](/best-response/)).

**Special cases.** The game is *zero-sum* if $B = -A$, and *constant-sum* if $A + B$ has all entries equal. It is *symmetric* if $m = n$ and $B = A^{\mathsf T}$, so that the two players face the same situation. A game with $A = B$ is a *coordination game* (a game of common interest).

**Nondegenerate games.** A bimatrix game is *nondegenerate* if, for every mixed strategy of either player with a support of size $k$, the other player has at most $k$ pure best responses. In a nondegenerate game every equilibrium has supports of equal size, and the equilibria are finitely many.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Battle of the sexes.** $A = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$. The game has two pure equilibria, rows and columns $(1, 1)$ with payoffs $(2, 1)$ and $(2, 2)$ with payoffs $(1, 2)$. In the mixed one, $y = (1/3, 2/3)$ makes the row player indifferent ($Ay = (2/3, 2/3)$), and $x = (2/3, 1/3)$ makes the column player indifferent ($x^{\mathsf T} B = (2/3, 2/3)$). Each player gets $2/3$. Three equilibria: an odd number, as in every nondegenerate game (Lemke and Howson 1964).

**Matching pennies.** $A = \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$ and $B = -A$. It is zero-sum, has no pure equilibrium, and its unique equilibrium is $x = y = (1/2, 1/2)$ with value 0 ([minimax theorem](/minimax-theorem/)).

**The identity coordination game.** Let $A = B = I_n$, the $n \times n$ identity matrix: both players get 1 if they choose the same index. For every nonempty set $T$ of indices, the pair in which both players are uniform on $T$ is an equilibrium, since each index in $T$ gets $1/|T|$ and every other index gets 0. These are all the equilibria, so the game has $2^n - 1$ of them: 3, 7 and 15 for $n = 2, 3, 4$. A bimatrix game can have exponentially many equilibria, which is one reason why enumerating them is slow.

**A degenerate game.** Take the normal form of an entry game:

| | Fight | Accommodate |
| --- | --- | --- |
| Out | 0, 2 | 0, 2 |
| In | -1, -1 | 1, 1 |

Against the pure strategy Out, both columns give 2, so the column player has two best responses to a strategy with support size 1, and the game is degenerate. Its equilibria form an infinite set: (In, Accommodate), and every pair (Out, $y$) where $y$ plays Fight with probability at least $1/2$, because In then gives the row player $1 - 2 y_{\text{Fight}} \le 0$. Algorithms that assume nondegeneracy, such as the basic Lemke-Howson algorithm, need a perturbation or a lexicographic rule on such games.

**Non-example: three players.** A game with three players cannot be written as a pair of matrices: each payoff needs three indices, and the payoff of a player is a multilinear function of degree 3 in the mixed strategies. The two-player case is special. With rational entries, a bimatrix game has an equilibrium with rational entries of polynomial bit length, because each equilibrium on given supports solves a system of linear equations. Nash (1951) gave a simplified three-player poker game with rational payoffs whose only equilibrium uses irrational probabilities.

## Related definitions

- **Zero-sum games.** The case $B = -A$; an equilibrium is a pair of maximin strategies, computed by one linear program ([zero-sum game linear programming](/zero-sum-game-linear-programming/)).
- **Best response polytopes.** For a game with positive payoffs, the polytopes $\{x \ge 0 : B^{\mathsf T} x \le \mathbf{1}\}$ and $\{y \ge 0 : A y \le \mathbf{1}\}$ encode the best responses; equilibria are the completely labeled pairs of vertices ([best response polytope](/best-response-polytope/)).
- **Linear complementarity.** Finding an equilibrium of $(A, B)$ is a [linear complementarity problem](/linear-complementarity-problem/), which the [Lemke-Howson algorithm](/lemke-howson-algorithm/) solves by pivoting.
- **Complexity.** Finding one equilibrium is PPAD-complete, also to within an additive $1/\mathrm{poly}(n)$ (Chen, Deng and Teng 2009); no polynomial algorithm is known ([computation](/nash-equilibrium-computation/)). For a constant additive $\varepsilon$ with payoffs in $[0, 1]$, the [Lipton-Markakis-Mehta algorithm](/lipton-markakis-mehta-algorithm/) runs in quasi-polynomial time. Questions about the best equilibrium, such as whether one gives the row player at least a given payoff, are NP-complete ([hardness of optimal Nash equilibria](/hardness-of-optimal-nash-equilibria/)).
- **Stackelberg commitment.** If one player commits to a mixed strategy first, the best commitment is found with $n$ linear programs ([Stackelberg equilibrium](/stackelberg-equilibrium/)).

## References
