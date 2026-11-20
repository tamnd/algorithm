---
tag: 3CE8QF
kind: theorem
slug: robinson-fictitious-play-theorem
name: Robinson's theorem on fictitious play
aliases:
- convergence of fictitious play in zero-sum games
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: "In fictitious play on a two-player zero-sum game, the empirical frequencies of play converge to the set of optimal mixed strategies."
prereqs: [zero-sum-game, minimax-theorem, best-response-dynamics]
see_also: [no-regret-zero-sum-theorem, no-regret-dynamics, follow-the-leader, zero-sum-game-linear-programming, potential-game, replicator-dynamics, nash-equilibrium, multiplicative-weights-update]
sources:
  - paper: doi:10.2307/1969530
    title: "Julia Robinson, An iterative method of solving a game, Annals of Mathematics 54(2) (1951), 296-301"
    locator: the main theorem (the convergence of the iterative method for every matrix game) and its proof by induction on the number of rows and columns
  - book: "Tjalling C. Koopmans (ed.), Activity Analysis of Production and Allocation, Cowles Commission Monograph 13, Wiley, 1951"
    title: "George W. Brown, Iterative solution of games by fictitious play"
    locator: the definition of fictitious play as a method to compute the value of a matrix game
  - paper: "Ulrich Berger, Fictitious play in 2 x n games, Journal of Economic Theory 120(2) (2005), 139-154"
    title: Fictitious play in 2 x n games
    locator: the convergence of fictitious play in nondegenerate games in which one player has two strategies
  - paper: doi:10.1006/jeth.1996.0014
    title: "Dov Monderer and Lloyd S. Shapley, Fictitious play property for games with identical interests, Journal of Economic Theory 68(1) (1996), 258-265"
    locator: "the convergence of fictitious play in games with identical interests, and so in weighted potential games"
---

Fictitious play is the oldest learning rule for games: in each round, each player plays a best response to the empirical mix of the moves the opponent has made so far. Brown (1951) proposed it as a way to compute the value of a matrix game. Robinson (1951) proved that it works: in every two-player [zero-sum game](/zero-sum-game/), the empirical frequencies of play converge to the set of optimal strategies, and the payoffs they guarantee converge to the value. Fictitious play is [follow the leader](/follow-the-leader/) in a game, so it can have linear regret against an adversary, and the theorem does not follow from the [no-regret theorem for zero-sum games](/no-regret-zero-sum-theorem/). Robinson's proof is a careful induction on the size of the matrix. Outside zero-sum games, fictitious play converges in some classes, such as [potential games](/potential-game/) and games in which one player has two strategies, but Shapley (1964) found a $3 \times 3$ game in which it cycles forever.

## Statement

The game is a real $m \times n$ matrix $M$; the row player gets $M_{ij}$ and the column player pays it. Fictitious play starts from any pair of pure strategies $(i_1, j_1)$. After rounds $1, \ldots, t$, let $\bar x^t \in \Delta_m$ and $\bar y^t \in \Delta_n$ be the empirical frequencies of the rows and columns played. In round $t + 1$,

$$i_{t+1} \in \arg\max_i (M \bar y^t)_i, \qquad j_{t+1} \in \arg\min_j (\bar x^{t\top} M)_j,$$

with ties broken in any way.

**Theorem (Robinson 1951).** Let $v$ be the value of $M$. Then

$$\lim_{t \to \infty} \min_j (\bar x^{t\top} M)_j = v = \lim_{t \to \infty} \max_i (M \bar y^t)_i.$$

Equivalently, every limit point of $\bar x^t$ is an optimal strategy of the row player, every limit point of $\bar y^t$ is an optimal strategy of the column player, and the distances from $\bar x^t$ and $\bar y^t$ to the sets of optimal strategies tend to 0.

The two forms are equivalent because $\min_j (x^\top M)_j$ and $\max_i (M y)_i$ are continuous, and an $x$ with $\min_j (x^\top M)_j = v$ is optimal. The theorem does not say that $\bar x^t$ converges to one point, and it says nothing about the moves $i_t$, $j_t$ themselves, which keep changing when the optimal strategies are mixed.

## In plain words

Two players repeat a game where one player's gain is the other player's loss. Each player keeps a count of what the other player has done and, every round, plays the best answer to that history, as if the other player were a fixed random device with those frequencies. Neither player is clever, and the moves can swing back and forth. Still, the running frequencies of each player's moves get closer and closer to an optimal mixed strategy of the game.

## Proof

Write $U^t = M \sum_{s \le t} e_{j_s}$ and $V^t = \sum_{s \le t} e_{i_s}^\top M$, the cumulative payoff vectors, so that $M \bar y^t = U^t/t$ and $\bar x^{t\top} M = V^t/t$. The rule is: $i_{t+1}$ maximizes $U^t$, $j_{t+1}$ minimizes $V^t$, and then $U^{t+1} = U^t + M e_{j_{t+1}}$ and $V^{t+1} = V^t + e_{i_{t+1}}^\top M$. For every $t$,

$$\min_j V^t_j \le t\, v \le \max_i U^t_i,$$

by the minimax theorem, because $\bar x^t$ guarantees at most $v$ and $\bar y^t$ concedes at least $v$. So the theorem says exactly that the gap $\max_i U^t_i - \min_j V^t_j$ is $o(t)$. Robinson's proof of this has four steps; the full argument is in Robinson (1951), pp. 296-301.

1. **A more general object.** Robinson works with a *vector system* for $M$: a pair of sequences of vectors $(U^t, V^t)$, with start vectors that satisfy a simple compatibility condition, in which each step adds to $U$ a column of $M$ that is a minimizer of $V$, and adds to $V$ a row of $M$ that is a maximizer of $U$. Fictitious play gives such a system. The freedom in the start vectors lets the induction restart at any time.
2. **Eligible rows and columns.** Row $i$ is *eligible* in the interval $[s, s + \tau]$ if $U_i$ is a maximum at some time in it, and column $j$ if $V_j$ is a minimum at some time in it. If every row and every column is eligible in $[s, s + \tau]$, then $\max_i U^{s+\tau}_i - \min_j V^{s+\tau}_j \le 4 a \tau$, where $a = \max_{i,j} |M_{ij}|$. The reason is that the coordinates of $U$ and $V$ change by at most $a$ per step, so a row that was a maximum at some time in the interval is at most $2 a \tau$ below the maximum at its end, and in the same way for the columns; Robinson combines the two bounds.
3. **Induction on $m + n$.** The claim is: for every $\varepsilon > 0$ there is a $t_0$, depending on $M$ and $\varepsilon$, such that every vector system for $M$ has gap at most $\varepsilon t$ for all $t \ge t_0$. For a $1 \times 1$ matrix the gap is constant. If in some interval a row or a column is not eligible, then on that interval the system is a vector system for a proper submatrix, and the induction hypothesis for the submatrix bounds the growth of the gap over the interval.
4. **Combining the intervals.** Cut the time line into intervals of a fixed length $\tau$. In each interval, either all rows and columns are eligible and step 2 applies, or step 3 applies with a smaller matrix. In both cases the gap grows by at most $\varepsilon \tau$ over the interval, up to an additive constant, so the gap is at most $2 \varepsilon t$ for all large $t$.

**A continuous-time version.** The simplest way to see why the theorem holds is to make time continuous. Let the strategies move by $\dot x = e_{i(t)} - x$ and $\dot y = e_{j(t)} - y$, where $e_{i(t)}$ is a best response of the row player to $y(t)$ and $e_{j(t)}$ is a best response of the column player to $x(t)$. Let $a(t) = \max_i (M y)_i$, $b(t) = \min_j (x^\top M)_j$ and $w(t) = a(t) - b(t) \ge 0$. These functions are Lipschitz, so they are differentiable almost everywhere. At such a time, the derivative of the maximum equals the derivative of each active term, so

$$\dot a = (M \dot y)_{i(t)} = M_{i(t)\, j(t)} - a, \qquad \dot b = (\dot x^\top M)_{j(t)} = M_{i(t)\, j(t)} - b,$$

and $\dot w = -w$. Hence $w(t) = e^{-t} w(0)$, and $b(t) \le v \le a(t)$ squeezes both to $v$. Discrete fictitious play is this process with step $1/(t + 1)$, so continuous time $\tau$ corresponds to round $e^\tau$, and $e^{-\tau}$ to $1/t$. The discrete process does not follow the continuous one exactly, and the theory of stochastic approximation for differential inclusions is needed to turn this argument into a proof of the discrete theorem. That theory is longer than Robinson's direct induction. $\blacksquare$

## Consequences

- **An algorithm for the value.** Fictitious play computes the value and approximately optimal strategies of a matrix game with one matrix-vector update per round and no linear programming, which is what Brown proposed it for. It is simple and needs only best responses, so it applies when $M$ is given implicitly.
- **Learning that is not no-regret.** Fictitious play is [follow the leader](/follow-the-leader/) for both players. Against an adversary it can have regret linear in $t$, but in self-play on a zero-sum game the theorem shows that both players' average payoffs approach the value, as for [no-regret dynamics](/no-regret-dynamics/).
- **Other classes of games.** Fictitious play also converges, in the sense that the empirical frequencies approach the set of Nash equilibria, in games with identical interests and in weighted [potential games](/potential-game/) (Monderer and Shapley 1996), and in nondegenerate games in which one of the two players has only two strategies (Berger 2005), which includes $2 \times 2$ games. In a general-sum game, if the empirical frequencies converge, the limit is a [Nash equilibrium](/nash-equilibrium/).

## Tightness

- **Cycling in general-sum games.** Shapley (1964) gave a $3 \times 3$ game in which fictitious play does not converge. One version: the row player gets 1 if the two strategies are equal, and the column player gets 1 if its strategy is one step ahead of the row player's (column $i + 1 \bmod 3$ against row $i$), and 0 otherwise. The only Nash equilibrium is uniform. Fictitious play from (0, 0) goes around a cycle of profiles, each run of the same profile is longer than the run before by a factor of about 1.47, and the empirical frequencies swing around the equilibrium forever without converging. A simulation of $2 \times 10^5$ rounds shows the frequencies of the row player at about (0.49, 0.16, 0.35) at round $10^5$ and about (0.37, 0.45, 0.17) at round $2 \times 10^5$.
- **Slow convergence.** The theorem gives no useful rate. Robinson's induction gives a bound that gets worse quickly with $m + n$; Shapiro (1958) derived the rate $O(t^{-1/(m+n-2)})$ from it. Karlin conjectured that the rate is always $O(t^{-1/2})$, as for no-regret dynamics. Daskalakis and Pan (2014) showed that with adversarial tie-breaking, the convergence can be much slower than this in the identity game. With multiplicative weights, the error is $O(\sqrt{\log(m+n)/t})$ in every game.
- **Averages, not moves.** Even in zero-sum games, the moves $i_t$, $j_t$ are pure, and they keep changing when the optimal strategies are mixed. Only the frequencies converge.

## History

Brown (1951) introduced fictitious play in the Cowles Commission volume on activity analysis, as an iterative method to compute the value of a game, and Robinson (1951) proved its convergence in zero-sum games in the same year. Miyasawa (1961) proved convergence in $2 \times 2$ games, and Shapley (1964) found the $3 \times 3$ game in which it cycles. Interest returned with the theory of learning in games in the 1990s: Monderer and Shapley (1996) proved convergence in games with identical interests, and Berger (2005) in nondegenerate $2 \times n$ games. Fictitious play is also the ancestor of the learning methods used to solve large zero-sum games, such as [counterfactual regret minimization](/counterfactual-regret-minimization/), which replace best responses by no-regret updates.

## References
