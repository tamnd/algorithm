---
tag: C14532
kind: theorem
slug: minimax-theorem
name: Minimax theorem
aliases:
- von Neumann minimax theorem
area: games-and-search/game-tree-search
level: intro
summary: In a finite two-player zero-sum game with mixed strategies, the maximin and minimax values are equal.
prereqs: [zero-sum-game, lp-duality, strong-duality]
see_also: [yao-minimax-principle, nash-equilibrium, nash-existence-theorem, nash-equilibrium-computation, linear-programming-problem, separating-hyperplane-theorem, multiplicative-weights-update, markov-game]
sources:
  - paper: doi:10.1007/BF01448847
    title: "John von Neumann, Zur Theorie der Gesellschaftsspiele, Mathematische Annalen 100(1) (1928), 295-320"
    locator: the minimax theorem for finite two-person zero-sum games and its first proof
  - book: isbn:9780691130613
    title: John von Neumann and Oskar Morgenstern, Theory of Games and Economic Behavior, 60th anniversary edition, Princeton University Press, 2007 (first edition 1944)
    locator: Chapter III, Zero-sum two-person games, theory (mixed strategies and the proof of the theorem from the theorem of the supporting hyperplanes)
  - book: "Émile Borel, Traité du calcul des probabilités et de ses applications, Tome IV, fascicule 2, Applications aux jeux de hasard, Gauthier-Villars, 1938"
    title: "Jean Ville, Sur la théorie générale des jeux où intervient l'habileté des joueurs, note in Borel's Traité, 1938"
    locator: pp. 105 to 113 (the first elementary proof, by convexity)
  - book: "Tjalling C. Koopmans (ed.), Activity Analysis of Production and Allocation, Cowles Commission Monograph 13, Wiley, 1951"
    title: "George B. Dantzig, A proof of the equivalence of the programming problem and the game problem"
    locator: pp. 330 to 335 (a matrix game is a linear program, and the reduction back)
  - paper: doi:10.1007/s00182-012-0328-8
    title: "Ilan Adler, The equivalence of linear programs and zero-sum games, International Journal of Game Theory 42(1) (2013), 165-177"
    locator: the gap in Dantzig's reduction from linear programs to games, and a full reduction
  - paper: doi:10.2140/pjm.1958.8.171
    title: "Maurice Sion, On general minimax theorems, Pacific Journal of Mathematics 8(1) (1958), 171-176"
    locator: the main theorem (the quasi-concave and quasi-convex form on convex sets, one of them compact)
  - paper: doi:10.1215/S0012-7094-41-00838-4
    title: "Shizuo Kakutani, A generalization of Brouwer's fixed point theorem, Duke Mathematical Journal 8(3) (1941), 457-459"
    locator: the fixed point theorem for set-valued maps and its corollary, the minimax theorem
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (maxmin and minmax strategies and the minimax theorem) and Chapter 4 (the linear program of a two-player zero-sum game)
---

The minimax theorem says that a finite two-player [zero-sum game](/zero-sum-game/) has one value when the players may randomize. The row player can make sure to win at least $v$ on average, the column player can make sure to lose at most $v$, and the two guarantees meet. Von Neumann proved it in 1928. The shortest modern proof is [linear programming duality](/lp-duality/).

## Statement

A *matrix game* is a real $m \times n$ matrix $M$. The row player picks a row $i$, the column player picks a column $j$ at the same time, and the column player pays $M_{ij}$ to the row player. A *mixed strategy* of the row player is a vector $x$ in the simplex $\Delta_m = \{x \in \mathbb{R}^m : x \ge 0,\ \sum_i x_i = 1\}$, and a mixed strategy of the column player is a $y \in \Delta_n$. With independent choices, the expected payment is $x^{\mathsf T} M y$.

**Theorem (von Neumann 1928).** For every real $m \times n$ matrix $M$,

$$\max_{x \in \Delta_m} \min_{y \in \Delta_n} x^{\mathsf T} M y \;=\; \min_{y \in \Delta_n} \max_{x \in \Delta_m} x^{\mathsf T} M y .$$

The maxima and minima exist. The common number $v$ is the *value* of the game. A strategy $x^*$ that reaches the maximum on the left is *maximin* (optimal for the row player), and a $y^*$ that reaches the minimum on the right is *minimax* (optimal for the column player).

Since $x^{\mathsf T} M y$ is linear in $y$, the inner minimum is at a pure strategy: $\min_{y} x^{\mathsf T} M y = \min_j (x^{\mathsf T} M)_j$. In the same way $\max_x x^{\mathsf T} M y = \max_i (M y)_i$. So the theorem says that there are $x^*$, $y^*$ and $v$ with

$$(x^{*\mathsf T} M)_j \ge v \text{ for every column } j \qquad\text{and}\qquad (M y^*)_i \le v \text{ for every row } i .$$

The pair $(x^*, y^*)$ is a certificate: each inequality is easy to check, and together they prove that $v$ is the value.

### Example

Take

$$M = \begin{pmatrix} 3 & -1 \\ -2 & 1 \end{pmatrix}.$$

In pure strategies the row player can guarantee $\max(-1, -2) = -1$ and the column player $\min(3, 1) = 1$, so there is no saddle point. With $x = (p, 1-p)$ the row player gets $5p - 2$ against column 1 and $1 - 2p$ against column 2. The minimum of the two is largest where they meet, at $p = 3/7$, with value $1/7$. With $y = (q, 1-q)$ the column player pays $4q - 1$ against row 1 and $1 - 3q$ against row 2, and these meet at $q = 2/7$, again at $1/7$. So $v = 1/7$, $x^* = (3/7, 4/7)$ and $y^* = (2/7, 5/7)$.

A brute force over a grid shows both sides close in on the value. With the strategies restricted to multiples of $1/N$:

| $N$ | best guarantee of the row player | best guarantee of the column player |
| --- | --- | --- |
| 7 | 1/7 | 1/7 |
| 10 | 0 | 1/5 |
| 100 | 7/50 | 4/25 |

The grid for $N = 7$ contains $x^*$ and $y^*$, so both columns give the exact value. For other $N$ the row side stays below $1/7$ and the column side above it, as the easy half of the proof says. Rock, paper, scissors, with $M_{ij} = 1$ for a win, $-1$ for a loss and 0 for a tie, has value 0 and the uniform strategy $(1/3, 1/3, 1/3)$ for both players.

## In plain words

Two players play a game where one player's gain is the other player's loss. If a player must announce a fixed choice in advance, the other player can exploit it, so going second is an advantage. Now let each player choose with a well-made dice roll. The theorem says that the advantage of going second then disappears. Each player has a best way to mix the choices. With it, the first player gets a certain average amount whatever the opponent does, and the opponent can hold the first player to exactly that amount. So the game has one fair price, and no player can do better against a careful opponent.

## Proof

**The easy half.** For all $x$ and $y$, $\min_{y'} x^{\mathsf T} M y' \le x^{\mathsf T} M y \le \max_{x'} x'^{\mathsf T} M y$. Take the maximum over $x$ on the left and the minimum over $y$ on the right:

$$\max_x \min_y x^{\mathsf T} M y \;\le\; \min_y \max_x x^{\mathsf T} M y .$$

Both sides exist: $x \mapsto \min_j (x^{\mathsf T} M)_j$ is a minimum of finitely many linear functions, so it is continuous, and $\Delta_m$ is compact. The same holds for the right side.

**The hard half, by duality.** Write the problem of the row player as a linear program in the variables $x \in \mathbb{R}^m$ and $v \in \mathbb{R}$:

$$\text{(P)}\qquad \max\ v \quad\text{subject to}\quad v - (M^{\mathsf T} x)_j \le 0 \ \ (j = 1, \ldots, n),\qquad \textstyle\sum_i x_i = 1,\qquad x \ge 0 .$$

For a fixed $x \in \Delta_m$, the largest feasible $v$ is $\min_j (x^{\mathsf T} M)_j$, so the optimum of (P) is $\max_x \min_y x^{\mathsf T} M y$. Give a multiplier $y_j \ge 0$ to the $j$-th inequality and a free multiplier $w$ to the equation. The dual program, by the rules on the page [LP duality](/lp-duality/), has one constraint for each primal variable. The variable $v$ is free with objective coefficient 1, which gives the equation $\sum_j y_j = 1$. Each $x_i \ge 0$ has objective coefficient 0, which gives $w - (M y)_i \ge 0$. So the dual is

$$\text{(D)}\qquad \min\ w \quad\text{subject to}\quad (M y)_i \le w \ \ (i = 1, \ldots, m),\qquad \textstyle\sum_j y_j = 1,\qquad y \ge 0 ,$$

and its optimum is $\min_y \max_i (M y)_i = \min_y \max_x x^{\mathsf T} M y$. Both programs are feasible: any $x \in \Delta_m$ with $v = \min_{i,j} M_{ij}$ satisfies (P), and any $y \in \Delta_n$ with $w = \max_{i,j} M_{ij}$ satisfies (D). By [strong duality](/strong-duality/), when a linear program and its dual are both feasible, both have optimal solutions and the two optimal values are equal. So the optimum of (P) equals the optimum of (D), which is the theorem, and an optimal solution of (P) or (D) is an optimal strategy. $\blacksquare$

The proof hides the real work in strong duality, which in turn rests on [Farkas' lemma](/farkas-lemma/) or the [separating hyperplane theorem](/separating-hyperplane-theorem/). The other classical proofs use the same geometry directly or use a fixed point theorem:

- **Separating hyperplane (Ville 1938, von Neumann and Morgenstern 1944).** Let $w = \min_y \max_i (M y)_i$. The convex set $C = \{M y : y \in \Delta_n\}$ does not meet the convex set $O = \{z : z_i < w \text{ for all } i\}$, so a hyperplane separates them: there is a vector $x \ne 0$ with $x^{\mathsf T} z \le x^{\mathsf T} c$ for all $z \in O$ and $c \in C$. Since $O$ goes to $-\infty$ in every coordinate, $x \ge 0$, and we can scale it to $x \in \Delta_m$. Then $x^{\mathsf T} M y \ge \sup_{z \in O} x^{\mathsf T} z = w$ for every $y$, so the row player can guarantee $w$. Ville's note was the first proof of this kind.
- **Fixed points.** Von Neumann's 1928 proof was topological. [Kakutani's 1941 fixed point theorem](/nash-existence-theorem/) for set-valued maps was made to give a short proof: a fixed point of the best-response map is a pair of optimal strategies.
- **Learning.** If both players run a no-regret method such as [multiplicative weights](/multiplicative-weights-update/), the averages of their strategies have payoff guarantees that approach each other, which proves the theorem again with an algorithm inside the proof.

## Consequences

- **A value and a certificate.** Every finite zero-sum game has one value $v$. An optimal pair $(x^*, y^*)$ proves it: $\min_j (x^{*\mathsf T}M)_j = v = \max_i (M y^*)_i$. For the matrix of the example above, $x^* = (3/7, 4/7)$ and $y^* = (2/7, 5/7)$ give 1/7 in all four positions.
- **Equilibria of zero-sum games.** A pair $(x, y)$ is a [Nash equilibrium](/nash-equilibrium/) of the zero-sum game if and only if $x$ is maximin and $y$ is minimax. So all equilibria give the same payoff $v$, and if $(x, y)$ and $(x', y')$ are equilibria, so are $(x, y')$ and $(x', y)$. The sets of optimal strategies are convex polytopes. General-sum games have none of these properties.
- **Polynomial time.** The proof is an algorithm: one linear program of size $O(mn)$ gives the value and both strategies, so a zero-sum matrix game is solved in polynomial time with the [ellipsoid](/ellipsoid-method/) or an [interior point method](/interior-point-method/). The [problem page](/nash-equilibrium-computation/) compares this with the general-sum case. Dantzig (1951) also gave a reduction in the other direction, from linear programs to symmetric games. His reduction misses one case, and Adler (2013) closed the gap.
- **Lower bounds for randomized algorithms.** [Yao's minimax principle](/yao-minimax-principle/) is the theorem applied to the matrix of costs of deterministic algorithms on inputs.
- **Game trees.** In a finite game of [perfect information](/perfect-information-game/), pure strategies already reach the value, by backward induction ([minimax](/minimax/)). The mixed strategies of the theorem are needed for simultaneous moves and for [hidden information](/imperfect-information-game/).
- **Repeated stages.** Shapley's stochastic games ([Markov games](/markov-game/)) solve one matrix game per state in each step of value iteration, and the theorem gives the value of each stage.

## Tightness

- **Pure strategies are not enough.** In matching pennies, $M = \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$. In pure strategies the row player can guarantee only $\max_i \min_j M_{ij} = -1$ and the column player only $\min_j \max_i M_{ij} = 1$. With mixed strategies the value is 0, with $x^* = y^* = (1/2, 1/2)$.
- **Finiteness matters.** Let each player name a positive integer, and let the larger number win 1 (a tie pays 0). Whatever distribution $x$ the row player uses, the column player can name a number so large that the row player wins with probability less than $\varepsilon$, so the row player cannot guarantee more than $-1$. In the same way the column player cannot guarantee less than $1$. The strategy sets are not compact and there is no value.
- **Concavity and convexity matter.** On $[0,1]^2$ let $f(x, y) = (x - y)^2$, with $x$ maximizing. Then $\max_x \min_y f = 0$, since $y = x$ answers every $x$, and $\min_y \max_x f = \min_y \max(y^2, (1-y)^2) = 1/4$. The function is convex in $y$ but not concave in $x$.
- **Zero sum matters.** In a general-sum game the two security levels need not form an equilibrium, and equilibria give different payoffs. What survives is [Nash's theorem](/nash-existence-theorem/): an equilibrium exists.
- **Sion's form.** Sion (1958) proved $\sup_x \inf_y f = \inf_y \sup_x f$ for $x$ in a convex set $X$ and $y$ in a convex set $Y$, one of them compact, when $f$ is upper semicontinuous and quasi-concave in $x$, and lower semicontinuous and quasi-convex in $y$. The bilinear $x^{\mathsf T} M y$ on two simplices is the first example.

## History

Borel wrote about mixed strategies in a series of notes from 1921 and solved small symmetric games, but he did not prove the general result. Von Neumann proved the theorem in 1928, with a topological argument, as part of the paper that started the theory of games. Ville (1938) gave the first proof that uses only convexity, in a note in Borel's treatise, and von Neumann and Morgenstern (1944) built their book on a proof of this kind. Kakutani (1941) proved his fixed point theorem to give a short proof, and Nash used the same fixed point theorem in 1950 for games that are not zero sum. The link to linear programming came in 1947, when von Neumann saw duality in Dantzig's problem (the story is on the page [strong duality](/strong-duality/)). Dantzig published the equivalence of the two problems in 1951, and Adler (2013) completed the reduction from linear programs to games. Sion (1958) gave the quasi-concave and quasi-convex form used in optimization and in learning theory today.

## References
