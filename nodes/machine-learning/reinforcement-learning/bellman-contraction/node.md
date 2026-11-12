---
tag: Z62P7P
kind: theorem
slug: bellman-contraction
name: Contraction property of the Bellman operator
aliases:
- Banach fixed-point theorem for MDPs
- Bellman operator contraction
area: machine-learning/reinforcement-learning
level: core
summary: "For a discount gamma < 1, the Bellman operators T^pi and T* are gamma-contractions in the max norm. So each has one fixed point, and value iteration converges geometrically."
prereqs: [bellman-optimality-equation, banach-fixed-point-theorem]
see_also: [value-iteration, iterative-policy-evaluation, policy-iteration, fixed-point-iteration, bellman-expectation-equation, markov-game, stochastic-shortest-path, deadly-triad]
sources:
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Theorem 6.2.3 (Banach fixed point theorem), Proposition 6.2.4 (the contraction), Theorem 6.3.1 (value iteration and its stopping rule)"
  - book: isbn:9781886529106
    title: Dimitri P. Bertsekas and John N. Tsitsiklis, Neuro-Dynamic Programming, Athena Scientific, 1996
    locator: "Chapter 2, Section 2.2"
  - paper: "Ronald J. Williams and Leemon C. Baird III, Tight Performance Bounds on Greedy Policies Based on Imperfect Value Functions, Technical Report NU-CCS-93-14, Northeastern University, College of Computer Science, 1993"
    title: Tight Performance Bounds on Greedy Policies Based on Imperfect Value Functions
    locator: "the bound in terms of the Bellman residual"
  - paper: "Satinder P. Singh and Richard C. Yee, An Upper Bound on the Loss from Approximate Optimal-Value Functions, Machine Learning 16, 227-233, 1994"
    title: An Upper Bound on the Loss from Approximate Optimal-Value Functions
    locator: "the main theorem"
  - paper: doi:10.1137/1009030
    title: Eric V. Denardo, Contraction Mappings in the Theory Underlying Dynamic Programming, SIAM Review 9(2), 165-177, 1967
    locator: "the abstract model with monotone contraction operators"
  - paper: doi:10.1073/pnas.39.10.1095
    title: Lloyd S. Shapley, Stochastic Games, Proceedings of the National Academy of Sciences 39(10), 1095-1100, 1953
    locator: "the contraction argument for the value of a stochastic game"
---

The Bellman operators of a discounted [Markov decision process](/markov-decision-process/) shrink the max-norm distance between any two value functions by at least the factor $\gamma$. With the [Banach fixed point theorem](/banach-fixed-point-theorem/), this one fact gives the existence and uniqueness of the solutions of the [Bellman expectation equation](/bellman-expectation-equation/) and the [Bellman optimality equation](/bellman-optimality-equation/), the geometric convergence of [value iteration](/value-iteration/), a stopping rule with a guarantee, and bounds on the loss of a greedy policy.

## Statement

Let $(S, A, P, R, \gamma)$ be a finite MDP with $0 \le \gamma < 1$. For $v : S \to \mathbb{R}$ write $\|v\|_\infty = \max_s |v(s)|$. For a stationary policy $\pi$ define

$$(T^\pi v)(s) = \sum_a \pi(a \mid s)\left[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, v(s')\right],$$

$$(T^* v)(s) = \max_a \left[R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, v(s')\right].$$

**Theorem.** For all $u, w : S \to \mathbb{R}$,

$$\|T^\pi u - T^\pi w\|_\infty \le \gamma\, \|u - w\|_\infty, \qquad \|T^* u - T^* w\|_\infty \le \gamma\, \|u - w\|_\infty.$$

So $T^\pi$ and $T^*$ are $\gamma$-contractions on $(\mathbb{R}^S, \|\cdot\|_\infty)$, a complete metric space. Each has exactly one fixed point, $V^\pi$ and $V^*$, and for any $v_0$ the iterates $v_{k+1} = T v_k$ satisfy

$$\|v_k - v^\star\|_\infty \le \gamma^k\, \|v_0 - v^\star\|_\infty$$

where $T$ is $T^\pi$ or $T^*$ and $v^\star$ is its fixed point. The same holds for the operators on action values, with $\max_{a'} q(s', a')$ or $\sum_{a'} \pi(a' \mid s') q(s', a')$ in place of $v(s')$.

## In plain words

Take two guesses of the long term worth of each situation. Apply one step of the update rule to both: each guess becomes the reward of one step plus the discounted guess at the next situation. The rewards are the same for both guesses, so they cancel in the difference. What is left is a discounted average of the old differences, and an average is never larger than the largest difference. So after the update, the largest gap between the two guesses has shrunk by at least the discount factor. Picking the best choice in each situation does not break this, because the best of two lists differ by at most the largest gap between them. Repeated updates therefore pull every guess toward one and the same answer, and the gap to that answer shrinks by a fixed factor at each step.

## Proof

**Lemma.** For functions $f, g$ on a finite set $A$, $\left|\max_a f(a) - \max_a g(a)\right| \le \max_a |f(a) - g(a)|$.

*Proof.* Let $a^*$ maximize $f$. Then $\max f - \max g \le f(a^*) - g(a^*) \le \max_a |f(a) - g(a)|$. Swap $f$ and $g$ for the other sign. $\blacksquare$

**The policy operator.** The reward terms cancel:

$$(T^\pi u - T^\pi w)(s) = \gamma \sum_a \pi(a \mid s) \sum_{s'} P(s' \mid s, a)\, \left(u(s') - w(s')\right).$$

The weights $\pi(a \mid s) P(s' \mid s, a)$ are nonnegative and sum to 1 over $(a, s')$. So the absolute value is at most $\gamma \max_{s'} |u(s') - w(s')|$. Take the max over $s$.

**The optimality operator.** Fix $s$ and let $f(a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) u(s')$ and $g(a)$ the same with $w$. By the lemma,

$$|(T^* u)(s) - (T^* w)(s)| \le \max_a |f(a) - g(a)| = \gamma \max_a \left|\sum_{s'} P(s' \mid s, a) (u(s') - w(s'))\right| \le \gamma\, \|u - w\|_\infty.$$

Take the max over $s$.

**Fixed points and convergence.** $\mathbb{R}^S$ with the max norm is complete. By the Banach fixed point theorem (Puterman, Theorem 6.2.3) a $\gamma$-contraction with $\gamma < 1$ has exactly one fixed point $v^\star$, and $\|v_k - v^\star\| = \|T v_{k-1} - T v^\star\| \le \gamma \|v_{k-1} - v^\star\|$ gives the geometric bound by induction. That the fixed point of $T^\pi$ is $V^\pi$ follows from the Bellman expectation equation, and that the fixed point of $T^*$ is $V^*$ is shown on the [Bellman optimality equation](/bellman-optimality-equation/) page. For $\gamma = 0$ both operators are constant maps, and the claims hold at once. $\blacksquare$

The proof for the action-value operators is the same, with the lemma applied to $\max_{a'}$ inside the sum.

## Consequences

**A posteriori bound.** From $\|v_{k+1} - v^\star\| \le \gamma \|v_k - v^\star\| \le \gamma \|v_k - v_{k+1}\| + \gamma \|v_{k+1} - v^\star\|$,

$$\|v_{k+1} - v^\star\|_\infty \le \frac{\gamma}{1-\gamma}\, \|v_{k+1} - v_k\|_\infty.$$

So the change between two sweeps, which an algorithm can see, bounds the error, which it cannot see.

**The stopping rule** (Puterman, Theorem 6.3.1). Run value iteration $v_{k+1} = T^* v_k$ and stop at the first $k$ with

$$\|v_{k+1} - v_k\|_\infty < \frac{\varepsilon (1-\gamma)}{2\gamma}.$$

Let $d$ be greedy for $v_{k+1}$. Then $\|v_{k+1} - V^*\|_\infty < \varepsilon/2$ and $\|V^d - V^*\|_\infty < \varepsilon$, so $d$ is $\varepsilon$-optimal.

*Proof.* The first claim is the a posteriori bound. For the second, $T^d v_{k+1} = T^* v_{k+1}$ by the choice of $d$, so

$$\|V^d - v_{k+1}\| \le \|T^d V^d - T^d v_{k+1}\| + \|T^* v_{k+1} - T^* v_k\| \le \gamma \|V^d - v_{k+1}\| + \gamma \|v_{k+1} - v_k\|,$$

and $\|V^d - v_{k+1}\| \le \frac{\gamma}{1-\gamma}\|v_{k+1} - v_k\| < \varepsilon/2$. The triangle inequality through $v_{k+1}$ gives $\|V^d - V^*\| < \varepsilon$. $\blacksquare$

Since $\|v_{k+1} - v_k\| \le \gamma^k \|v_1 - v_0\|$, the rule stops at an index $k \le \lfloor x \rfloor + 1$ with $x = \log\frac{2\gamma\|v_1 - v_0\|}{\varepsilon(1-\gamma)} \big/ \log\frac{1}{\gamma}$, for $0 < \gamma < 1$.

**The loss of a greedy policy.** Let $v$ be any value function, $d$ greedy for it, and $\varepsilon = \|T^* v - v\|_\infty$ the Bellman residual. Williams and Baird (1993) show

$$\|V^* - V^d\|_\infty \le \frac{2\gamma\varepsilon}{1-\gamma}.$$

*Proof.* As above, $\|V^d - v\| \le \|T^d V^d - T^d v\| + \|T^d v - v\| \le \gamma\|V^d - v\| + \varepsilon$, so $\|V^d - v\| \le \varepsilon/(1-\gamma)$. In the same way $\|V^* - v\| \le \varepsilon/(1-\gamma)$. Now $T^d v = T^* v$, so

$$V^* - V^d = (T^* V^* - T^* v) + (T^d v - T^d V^d),$$

and each term has norm at most $\gamma \varepsilon/(1-\gamma)$. $\blacksquare$

If instead $\delta = \|v - V^*\|_\infty$ is known, the same three-term split $V^* - V^d = (T^* V^* - T^* v) + (T^d v - T^d V^*) + (T^d V^* - T^d V^d)$ gives $\|V^* - V^d\| \le 2\gamma\delta + \gamma\|V^* - V^d\|$, so $\|V^* - V^d\|_\infty \le 2\gamma\delta/(1-\gamma)$ (Singh and Yee 1994).

**An example.** Take the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$, where $V^* = (360/31, 440/31) \approx (11.613, 14.194)$. Value iteration from $v_0 = 0$ with $\varepsilon = 0.01$ stops when the change is below $0.01 \cdot 0.1 / 1.8 \approx 5.6 \cdot 10^{-4}$. In floating point this happens after 75 sweeps. The error is then about 0.0045 in both states, below $\varepsilon/2$, and the greedy policy is the optimal (switch, stay).

**Other uses.**

- [Policy iteration](/policy-iteration/) and [modified policy iteration](/modified-policy-iteration/) converge, because their iterates are squeezed between value iteration iterates by the monotonicity of $T^*$.
- Asynchronous and stochastic versions, such as [Q-learning](/q-learning/), converge because each update moves one entry toward the fixed point of a contraction, under step size conditions ([tabular Q-learning convergence](/tabular-q-learning-convergence/)).
- In a [Markov game](/markov-game/) the max is replaced by the value of a matrix game, which also changes by at most the largest entry change. Shapley's operator is then a contraction by the same proof.

## Tightness

- **The factor $\gamma$ cannot be smaller.** Take one state, one action and the reward $r$. Then $T v = r + \gamma v$ and $|T u - T w| = \gamma |u - w|$ for all $u, w$. More generally, if $u - w$ is a constant vector $c\mathbf{1}$, then $T^\pi u - T^\pi w = \gamma c \mathbf{1}$ for every MDP.
- **The norm matters.** In the Euclidean norm $T^\pi$ need not be a contraction. Take two states that both move to state 2 with probability 1, zero rewards, and $u - w = (0, 1)$. Then $T^\pi u - T^\pi w = (\gamma, \gamma)$, of Euclidean length $\gamma\sqrt{2}$, which is larger than 1 for $\gamma > 1/\sqrt{2}$. With function approximation and a projection in a weighted Euclidean norm, this is one source of divergence ([deadly triad](/deadly-triad/)).
- **No discount.** For $\gamma = 1$ the bound gives nothing, and $T^\pi$ can have no fixed point (a positive reward on a loop) or many (zero rewards). In a [stochastic shortest path](/stochastic-shortest-path/) problem where every policy reaches the goal with probability 1, $T^*$ is a contraction in a weighted max norm instead (Bertsekas and Tsitsiklis, Chapter 2).
- **The rate in practice.** The bound $\gamma^k$ is for the worst case. The span seminorm $\max_s v(s) - \min_s v(s)$ can shrink by a smaller factor, which gives sharper stopping rules (Puterman, Section 6.6).

## History

Shapley (1953) proved the value of a discounted stochastic game exists with a successive approximation argument that is a contraction argument, and an MDP is the case of a game with one player. Bellman (1957) used successive approximation for the discounted MDP. Blackwell (1965) gave monotonicity and discounting as conditions that make an operator a contraction. Denardo (1967) built an abstract theory of dynamic programming on monotone contraction operators, which covers MDPs and stochastic games. The loss bounds for greedy policies from approximate values are due to Williams and Baird (1993) and Singh and Yee (1994), and became a basic tool for approximate dynamic programming.

## References
