---
tag: QN2M75
kind: definition
slug: least-core
name: Least core
aliases:
- strong epsilon-core
area: algorithmic-game-theory/cooperative-games
level: core
summary: The efficient payoff vectors that minimize the largest excess v(S) minus x(S) over the proper coalitions. It is never empty and one LP finds it.
prereqs: [core-of-a-cooperative-game, linear-programming-problem]
see_also: [nucleolus, nucleolus-sequential-lp, bondareva-shapley-theorem, transferable-utility-game, weighted-voting-game, separation-oracle, ellipsoid-method, lp-duality]
sources:
  - paper: doi:10.1287/moor.4.4.303
    title: "Michael Maschler, Bezalel Peleg and Lloyd S. Shapley, Geometric properties of the kernel, nucleolus, and related solution concepts, Mathematics of Operations Research 4(4) (1979), 303-338"
    locator: the epsilon-cores, the least core, and the nested sequence of least cores that ends in the nucleolus
  - paper: doi:10.1137/0117107
    title: "David Schmeidler, The nucleolus of a characteristic function game, SIAM Journal on Applied Mathematics 17(6) (1969), 1163-1170"
    locator: the nucleolus, whose first step is the least core
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 20, The nucleolus (Section 20.4, computing the nucleolus by a sequence of linear programs that starts with the least core)
  - book: "Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Synthesis Lectures on Artificial Intelligence and Machine Learning, Morgan and Claypool, 2011"
    title: Computational Aspects of Cooperative Game Theory
    locator: Chapter 2 (the epsilon-core and the least core) and Chapter 3 (their computation for compact representations)
---

The least core of a [TU game](/transferable-utility-game/) is the set of splits of $v(N)$ that make the worst-treated coalition as well off as possible. When the [core](/core-of-a-cooperative-game/) is empty, no split gives every coalition its value, and the least core relaxes all core constraints by the same smallest amount; when the core is not empty, it tightens them as far as it can and picks a central part of the core. It is never empty. The [nucleolus](/nucleolus/) is a single point inside the least core, found by repeating the same step on the coalitions that are left; the [sequential LP](/nucleolus-sequential-lp/) does this, and its first round is exactly the least core.

## Definition

Let $(N, v)$ be a TU game with $n \ge 2$ players, and write $x(S) = \sum_{i \in S} x_i$ and $e(S, x) = v(S) - x(S)$. For a real number $\varepsilon$, the $\varepsilon$-core is

$$C_\varepsilon(v) = \{x \in \mathbb{R}^n : x(N) = v(N) \text{ and } x(S) \ge v(S) - \varepsilon \text{ for every } S \text{ with } \emptyset \ne S \ne N\}.$$

Shapley and Shubik called it the strong $\varepsilon$-core. The core is $C_0$, and $C_\varepsilon$ grows with $\varepsilon$. The least core value is the smallest $\varepsilon$ with $C_\varepsilon$ not empty, and the least core is the $\varepsilon$-core for this value (Maschler, Peleg and Shapley 1979):

$$\varepsilon_1 = \min_{x(N) = v(N)}\ \max_{\emptyset \ne S \ne N} e(S, x), \qquad \mathrm{LC}(v) = C_{\varepsilon_1}(v).$$

So the least core value and the least core are the optimal value and the optimal $x$ of one linear program with $n + 1$ variables:

$$\min\ \varepsilon \quad \text{subject to} \quad x(N) = v(N), \quad x(S) + \varepsilon \ge v(S) \text{ for } \emptyset \ne S \ne N.$$

This LP is feasible, since any efficient $x$ with a large $\varepsilon$ works. It is bounded below: adding the constraints for the $n$ single players gives $v(N) + n \varepsilon \ge \sum_i v(\{i\})$. So the minimum is reached, and the least core is never empty. It is a bounded polytope, because $x_i \ge v(\{i\}) - \varepsilon_1$ and $x(N) = v(N)$.

Basic facts:

- The core is not empty exactly when $\varepsilon_1 \le 0$. If $\varepsilon_1 < 0$, the least core is a part of the core; if $\varepsilon_1 > 0$, the core is empty and the least core is the set of splits that are closest to stable in this sense.
- The least core is defined on the preimputations: it does not ask $x_i \ge v(\{i\})$. When $\varepsilon_1 > 0$ a least core point can give a player less than $v(\{i\})$, but by at most $\varepsilon_1$.
- The prenucleolus is always in the least core. The nucleolus is in it whenever the least core contains an imputation, in particular when the core is not empty.
- The least core is covariant under strategic equivalence $w = \alpha v + a$, with least core value $\alpha \varepsilon_1$.

To compute the least core from a table of $v$, solve the LP above, with $2^n - 2$ constraints. For a game with a short description the LP has exponentially many constraints, but it can be solved by the [ellipsoid method](/ellipsoid-method/) when a [separation oracle](/separation-oracle/) is available: given $(x, \varepsilon)$, find a coalition $S$ that maximizes $v(S) - x(S)$, and compare with $\varepsilon$. So the least core is as easy to compute as this maximization, up to polynomial factors. For [weighted voting games](/weighted-voting-game/), for example, the maximization is a knapsack problem, which is NP-hard in general but solvable in pseudo-polynomial time.

## Examples and non-examples

- **The majority game.** $v(S) = 1$ when $|S| \ge 2$. The pair constraints give $2 x(N) \ge 3(1 - \varepsilon)$, so $\varepsilon \ge 1/3$. At $\varepsilon = 1/3$ each pair needs at least $2/3$, and the three pairs sum to exactly $2$, so each pair gets exactly $2/3$. The least core value is $1/3$ and the least core is the single point $(1/3, 1/3, 1/3)$.
- **A game with a large core.** Let $v(\{i\}) = 0$, $v(S) = 1/2$ for each pair and $v(N) = 1$. The same sum gives $2 \ge 3(1/2 - \varepsilon)$, so $\varepsilon \ge -1/6$. At $\varepsilon = -1/6$ each pair gets exactly $2/3$, so the least core is again $(1/3, 1/3, 1/3)$, now strictly inside the core. The least core value $-1/6$ says that every proper coalition gets at least $1/6$ more than its value.
- **The glove game.** With $v(\{1, 2\}) = v(\{1, 3\}) = v(N) = 1$, the pair constraints give $x_3 \le \varepsilon$ and $x_2 \le \varepsilon$, and the single constraints give $x_2, x_3 \ge -\varepsilon$. So $\varepsilon \ge 0$, and the least core is the core $\{(1, 0, 0)\}$.
- **A least core with more than one point.** Let $v(\{1, 2\}) = v(N) = 1$ and $v = 0$ for every other coalition. Then $x_3 = 1 - x(\{1, 2\}) \le \varepsilon$ and $x_3 \ge -\varepsilon$, so $\varepsilon_1 = 0$. The least core is the segment of points $(t, 1 - t, 0)$ with $0 \le t \le 1$, equal to the core. The nucleolus picks its midpoint $(1/2, 1/2, 0)$ in the next round.
- **Not the least core: the minimizers over all coalitions.** If $N$ is not left out of the max, the excess $e(N, x) = 0$ puts a floor of 0 under the objective. Then every core point would be optimal when the core is not empty, and the least core would no longer pick a central part of the core.

## Related definitions

- **Weak $\varepsilon$-core.** Shapley and Shubik also used the weak $\varepsilon$-core, with $x(S) \ge v(S) - \varepsilon |S|$, which scales the relaxation with the size of the coalition.
- **Nucleolus.** The least core minimizes the largest excess. The [nucleolus](/nucleolus/) then minimizes the second largest, and so on, which leaves one point. Maschler, Peleg and Shapley describe it as the end of a nested sequence of least cores.
- **Core.** The [core](/core-of-a-cooperative-game/) is $C_0$. The [Bondareva-Shapley theorem](/bondareva-shapley-theorem/) is LP duality for the LP above with $\varepsilon$ fixed at 0.
- **Cost of stability.** Instead of relaxing every coalition, one can add an outside payment to $v(N)$ and ask for the smallest payment that makes the core nonempty. This is another LP over the same constraints.

## References
