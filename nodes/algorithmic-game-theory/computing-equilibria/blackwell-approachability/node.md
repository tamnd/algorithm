---
tag: QNGRA5
kind: theorem
slug: blackwell-approachability
name: Blackwell approachability theorem
aliases:
- approachability theorem
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: "In a repeated game with vector payoffs, a closed convex set can be approached by the average payoff if and only if every halfspace containing it can be."
prereqs: [minimax-theorem, convex-set, regret]
see_also: [regret-matching, no-regret-dynamics, separating-hyperplane-theorem, correlated-equilibrium, online-convex-optimization, expert-problem, no-regret-zero-sum-theorem, multiplicative-weights-update]
sources:
  - paper: doi:10.2140/pjm.1956.6.1
    title: "David Blackwell, An analog of the minimax theorem for vector payoffs, Pacific Journal of Mathematics 6(1) (1956), 1-8"
    locator: "the definition of approachable and excludable sets, the sufficient condition with the closest point and the separating hyperplane, and the characterization of approachable closed convex sets"
  - paper: doi:10.1111/1468-0262.00153
    title: "Sergiu Hart and Andreu Mas-Colell, A simple adaptive procedure leading to correlated equilibrium, Econometrica 68(5) (2000), 1127-1150"
    locator: "the use of Blackwell's approachability theorem for the vector of regrets, which gives regret matching and its convergence to the set of correlated equilibria"
  - book: isbn:9780521841085
    title: "Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006"
    locator: "Chapter 7 (prediction and playing games, Blackwell's approachability theorem and its use for regret)"
---

Blackwell's approachability theorem is the [minimax theorem](/minimax-theorem/) for repeated games with vector payoffs. In each round two players choose actions, and the outcome is a vector in $\mathbb{R}^d$, not a number. Player 1 wants the average outcome to get close to a target set $C$, and player 2 wants to prevent this. With one round and a vector payoff, the minimax theorem fails: player 1 may be able to reach $C$ against each mixed action of player 2, but not with one action against all of them. Blackwell (1956) showed that in the long run the gap closes for closed convex sets: $C$ can be approached exactly when every halfspace that contains $C$ can, and a halfspace is a one-dimensional zero-sum game. The proof gives a simple strategy: look at the closest point of $C$ to the current average, and play the optimal strategy of the scalar game in the direction of that point. Applied to the vector of [regrets](/regret/), the theorem gives algorithms with no regret, among them [regret matching](/regret-matching/).

## Statement

Player 1 has a finite action set $I$ and player 2 a finite action set $J$. The payoff is a vector $r(i, j) \in \mathbb{R}^d$, with $\|r(i, j)\| \le B$. For mixed actions $p \in \Delta(I)$ and $q \in \Delta(J)$, write $r(p, q) = \sum_{i,j} p_i q_j\, r(i, j)$. In rounds $t = 1, 2, \ldots$ both players choose actions at the same time, each possibly at random and using the history, and the average payoff is $\bar g_T = \frac1T \sum_{t=1}^T r(i_t, j_t)$.

A closed set $C \subseteq \mathbb{R}^d$ is *approachable* by player 1 if player 1 has a strategy such that $\mathbb{E}\, \mathrm{dist}(\bar g_T, C) \to 0$ uniformly over all strategies of player 2. (Blackwell also asks for almost sure convergence; his strategy gives both.)

**Theorem (Blackwell 1956).**

1. **(Sufficient condition.)** Let $C$ be closed, and suppose that for every point $z \notin C$ there is a closest point $c \in C$ and a mixed action $p$ with $\langle z - c,\, r(p, j) - c \rangle \le 0$ for every $j \in J$. Then $C$ is approachable. If player 1 plays such a $p$ for $z = \bar g_t$ in round $t + 1$, then $\mathbb{E}\, \mathrm{dist}(\bar g_T, C) \le K/\sqrt{T}$, where $K$ depends only on $B$ and $C$.
2. **(Convex sets.)** Let $C$ be closed, convex and nonempty. The following are equivalent:
   - (a) $C$ is approachable;
   - (b) every closed halfspace that contains $C$ is approachable;
   - (c) for every $q \in \Delta(J)$ there is a $p \in \Delta(I)$ with $r(p, q) \in C$.

A halfspace $H = \{w : \langle \lambda, w \rangle \le \alpha\}$ is approachable exactly when the scalar zero-sum game with payoff $\langle \lambda, r(i, j) \rangle$ to be kept low has value at most $\alpha$, that is, $\min_p \max_q \langle \lambda, r(p, q) \rangle \le \alpha$. So condition (b) is a family of scalar minimax conditions, one per direction.

## In plain words

In a game where each round produces a list of numbers instead of one number, a player may want the running average of these lists to end up inside some target region. For a single round, it can happen that the player has a good answer to every plan of the opponent, but no move that is good against all plans at once. Over many rounds this problem disappears when the target region is convex. The player looks at where the average is now, finds the nearest point of the target, and plays as if the game were only about the one direction from the average to that point. Each round then pulls the average toward the target, and the distance shrinks like one over the square root of the number of rounds.

## Proof

**Part 1.** Let $d_t = \mathrm{dist}(\bar g_t, C)$, let $c_t$ be the closest point of $C$ to $\bar g_t$, and let $r_{t+1} = r(i_{t+1}, j_{t+1})$. Since $\bar g_{t+1} = \frac{t}{t+1} \bar g_t + \frac{1}{t+1} r_{t+1}$,

$$d_{t+1}^2 \le \|\bar g_{t+1} - c_t\|^2 = \frac{t^2}{(t+1)^2} d_t^2 + \frac{2t}{(t+1)^2} \langle \bar g_t - c_t,\, r_{t+1} - c_t \rangle + \frac{\|r_{t+1} - c_t\|^2}{(t+1)^2}.$$

Given the history, $i_{t+1}$ is drawn from the chosen $p$ independently of $j_{t+1}$, so the conditional expectation of the middle term is a mixture over $j$ of $\langle \bar g_t - c_t, r(p, j) - c_t \rangle \le 0$; if $\bar g_t \in C$ it is 0. Every average $\bar g_t$ lies in the ball of radius $B$, so with $D = \max_{\|z\| \le B} \mathrm{dist}(z, C)$ we have $\|r_{t+1} - c_t\| \le \|r_{t+1} - \bar g_t\| + d_t \le 2B + D =: K$. Taking expectations and multiplying by $(t+1)^2$,

$$\mathbb{E}[(t+1)^2 d_{t+1}^2] \le \mathbb{E}[t^2 d_t^2] + K^2.$$

With $d_1 \le D \le K$, induction gives $\mathbb{E}[T^2 d_T^2] \le T K^2$, so $\mathbb{E}[d_T^2] \le K^2/T$ and $\mathbb{E}\, d_T \le K/\sqrt{T}$ for every strategy of player 2.

**Part 2.** (a) implies (b) because a set that contains $C$ is at distance at most $\mathrm{dist}(\cdot, C)$.

(b) implies (c). Suppose that for some $q$, the set $R_q = \{r(p, q) : p \in \Delta(I)\}$ does not meet $C$. It is compact and convex, so by the [separating hyperplane theorem](/separating-hyperplane-theorem/) there are $\lambda$, $\alpha$ and $\delta > 0$ with $\langle \lambda, w \rangle \le \alpha$ on $C$ and $\langle \lambda, w \rangle \ge \alpha + \delta$ on $R_q$. Let $H = \{w : \langle \lambda, w \rangle \le \alpha\} \supseteq C$. If player 2 plays $q$ in every round, then $\mathbb{E}[\langle \lambda, r_t \rangle \mid \text{history}] \ge \alpha + \delta$ whatever player 1 does, so $\mathbb{E}\, \langle \lambda, \bar g_T \rangle \ge \alpha + \delta$. Since $\mathrm{dist}(w, H) \ge (\langle \lambda, w \rangle - \alpha)/\|\lambda\|$, we get $\mathbb{E}\, \mathrm{dist}(\bar g_T, H) \ge \delta/\|\lambda\|$ for all $T$, so $H$ is not approachable.

(c) implies (a). Fix $z \notin C$, let $c$ be its closest point in $C$ (unique, since $C$ is closed and convex), and let $\lambda = z - c$. For every $w \in C$, $\langle \lambda, w - c \rangle \le 0$. Consider the scalar zero-sum game with payoff $\langle \lambda, r(p, q) - c \rangle$, which player 1 minimizes. By (c), for every $q$ some $p$ has $r(p, q) \in C$ and so payoff at most 0. Hence $\max_q \min_p \le 0$, and by the minimax theorem $\min_p \max_q \le 0$: some $p$ has $\langle z - c, r(p, j) - c \rangle \le 0$ for every $j$. This is the condition of part 1, so $C$ is approachable. $\blacksquare$

## Consequences

- **The minimax theorem.** For $d = 1$ and $C = (-\infty, \alpha]$, part 2 says that player 1 can keep the average payoff at most $\alpha$ in the long run exactly when, for every $q$, some $p$ gives at most $\alpha$; with part 1 and the scalar game, this is the minimax theorem in repeated form.
- **No external regret.** Let player 1 choose among $k$ actions against payoff vectors $u_t \in [0, 1]^k$ that player 2 picks from a finite set, and let the vector payoff be the regret vector $r(i, u) = (u(a) - u(i))_{a = 1}^k$. Approaching the nonpositive orthant means that the average regret against every fixed action goes to 0. Condition (c) holds: against a mixed $q$, play the best action against its mean. Part 1 gives an explicit strategy: with $z^+$ the positive part of the current average regret vector, the closest point of the orthant is $\min(z, 0)$, and $p = z^+ / \sum_a z_a^+$ satisfies the condition, since $\langle z^+, r(p, u) \rangle = \sum_a z_a^+ u(a) - (\sum_a z_a^+)\, u(p) = 0$. This is [regret matching](/regret-matching/), and the regret is $O(\sqrt{k/T})$ on average.
- **Correlated equilibria.** With one coordinate $u(l) - u(j)$ for each pair of actions, counted only in rounds where $j$ is played, the same construction removes internal regret. Hart and Mas-Colell (2000) used this to show that regret matching leads the empirical distribution of play to the set of [correlated equilibria](/correlated-equilibrium/).
- **Online learning.** Approachability is one of the general tools for building no-regret algorithms, next to [online convex optimization](/online-convex-optimization/) and the [experts setting](/expert-problem/). It handles goals with several criteria at once, such as regret against several benchmarks or calibrated forecasts, where a single scalar loss does not fit.

## Tightness

- **Convexity matters.** For a set that is not convex, condition (c) does not imply approachability: player 1 can reach the set against each mixed action of player 2 but not along the average, because the average of points of $C$ can lie outside $C$. Part 1 still applies to such sets when its condition holds.
- **One round is not enough.** In one round, condition (c) does not give one $p$ that works against all $q$. Take $I = J = \{1, 2\}$ and $r(i, j) = e_j$ if $i = j$ and $0$ otherwise, in $\mathbb{R}^2$, with $C = \{w : w_1 = w_2\}$. Against each $q$, the mixed action $p$ proportional to $(q_2, q_1)$ gives equal coordinates, so (c) holds, but every fixed $p$ is beaten by a pure $j$, which gives a payoff on one axis. Over many rounds, part 2 shows that $C$ is approachable.
- **The rate.** The rate $K/\sqrt{T}$ cannot be improved in general: for the regret vector of the experts problem, it would give regret $o(\sqrt{T})$, which is impossible against an adversary.

## History

Blackwell (1956) introduced approachability and proved the theorem in an eight-page paper whose title presents it as an analog of the minimax theorem for vector payoffs. Hannan (1957) found strategies with no regret in the same years, and the link between the two lines of work became central in the 1990s. Approachability gave a proof that calibrated forecasts exist, and Hart and Mas-Colell (2000) derived regret matching from it and proved its convergence to the set of correlated equilibria. Later work showed that approachability and online convex optimization can be reduced to each other.

## References
