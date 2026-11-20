---
tag: EB3XKT
kind: definition
slug: nucleolus
name: Nucleolus
aliases:
- Schmeidler nucleolus
area: algorithmic-game-theory/cooperative-games
level: core
summary: "The unique imputation that lexicographically minimizes the sorted vector of coalition excesses, when the imputation set is nonempty. It lies in the core when that is nonempty."
prereqs: [transferable-utility-game, core-of-a-cooperative-game, least-core, lexicographic-order]
see_also: [nucleolus-sequential-lp, talmud-rule, bankruptcy-problem, assignment-game, shapley-value, minimum-cost-spanning-tree-game, bondareva-shapley-theorem, convex-game]
sources:
  - paper: doi:10.1137/0117107
    title: "David Schmeidler, The nucleolus of a characteristic function game, SIAM Journal on Applied Mathematics 17(6) (1969), 1163-1170"
    locator: the definition of the nucleolus, the proof that it exists and is unique, and the proof that it lies in the kernel
  - paper: doi:10.1137/0120009
    title: "Elon Kohlberg, On the nucleolus of a characteristic function game, SIAM Journal on Applied Mathematics 20(1) (1971), 62-66"
    locator: the characterization of the nucleolus by balanced collections of coalitions
  - paper: doi:10.1287/moor.4.4.303
    title: "Michael Maschler, Bezalel Peleg and Lloyd S. Shapley, Geometric properties of the kernel, nucleolus, and related solution concepts, Mathematics of Operations Research 4(4) (1979), 303-338"
    locator: the nucleolus as the end of a nested sequence of least cores
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 20, The nucleolus (Section 20.1 definition, Section 20.2 nonemptiness and uniqueness, Section 20.5 the prenucleolus, Section 20.8 the bankruptcy problem)
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 5 (the prekernel, kernel and nucleolus) and Chapter 6 (the prenucleolus, with Kohlberg's criterion and the reduced game property)
  - paper: doi:10.1016/0022-0531(85)90102-4
    title: "Robert J. Aumann and Michael Maschler, Game theoretic analysis of a bankruptcy problem from the Talmud, Journal of Economic Theory 36(2) (1985), 195-213"
    locator: the nucleolus of the bankruptcy game is the Talmud rule
  - paper: doi:10.1007/BF01240179
    title: "Tamas Solymosi and T. E. S. Raghavan, An algorithm for finding the nucleolus of assignment games, International Journal of Game Theory 23 (1994), 119-143"
    locator: a polynomial algorithm for the nucleolus of the assignment game
  - paper: "Ulrich Faigle, Walter Kern and Jeroen Kuipers, Computing the nucleolus of min-cost spanning tree games is NP-hard, International Journal of Game Theory 27(3) (1998), 443-450"
    locator: the NP-hardness of the nucleolus of minimum cost spanning tree games
---

The nucleolus of a [TU game](/transferable-utility-game/) is the split of $v(N)$ that treats the most unhappy coalition as well as possible, then the next most unhappy one, and so on. Schmeidler defined it in 1969 and proved that it is a single point whenever an imputation exists. It always lies in the [least core](/least-core/) when the least core contains an imputation, and in the [core](/core-of-a-cooperative-game/) whenever the core is not empty, so it is a canonical choice of one core point. The [sequential LP](/nucleolus-sequential-lp/) computes it from a table of $v$; for the [bankruptcy game](/bankruptcy-problem/) it is the [Talmud rule](/talmud-rule/).

## Definition

Let $(N, v)$ be a TU game with $N = \{1, \ldots, n\}$, and let the excess of a coalition $S$ at a payoff vector $x$ be $e(S, x) = v(S) - x(S)$, where $x(S) = \sum_{i \in S} x_i$. A large excess means that $S$ has a strong complaint against $x$. Let $\theta(x)$ be the vector of the $2^n$ excesses $e(S, x)$, over all $S \subseteq N$, sorted in nonincreasing order. Compare such vectors in the [lexicographic order](/lexicographic-order/): $\theta(x) <_{\mathrm{lex}} \theta(y)$ if at the first index where they differ, $\theta(x)$ has the smaller entry.

Let $I(v) = \{x : x(N) = v(N),\ x_i \ge v(\{i\}) \text{ for all } i\}$ be the set of imputations. It is not empty exactly when $v(N) \ge \sum_i v(\{i\})$. The nucleolus is

$$\nu(v) = \{x \in I(v) : \theta(x) \le_{\mathrm{lex}} \theta(y) \text{ for every } y \in I(v)\}.$$

The prenucleolus is defined in the same way over all preimputations, $x(N) = v(N)$, with no lower bound on $x_i$; it exists for every game.

**Theorem (Schmeidler 1969).** If $I(v)$ is not empty, the nucleolus consists of exactly one point. The same holds for the prenucleolus with no condition.

*Existence.* Let $\theta_k(x)$ be the $k$-th entry of $\theta(x)$. It is a continuous function of $x$, because the $k$-th largest of finitely many continuous functions is continuous. Minimize $\theta_1$ over the compact set $I(v)$, then minimize $\theta_2$ over the set of minimizers, and so on. Each step minimizes a continuous function over a nonempty compact set, so each set of minimizers is nonempty and compact. The last set is the nucleolus. For the prenucleolus, the first step can be done over a compact part of the preimputations, because $\theta_1(x) \ge v(\{i\}) - x_i$ makes all $x_i$ bounded below once $\theta_1$ is bounded above.

*Uniqueness.* Let $x$ and $y$ both be in the nucleolus, so $\theta(x) = \theta(y) = t$, and let $z = (x + y)/2$, which is again an imputation. Each excess is linear in the payoff, so $e(S, z) = (e(S, x) + e(S, y))/2$. For each $k$, the sum of any $k$ entries of $e(\cdot, z)$ is at most the average of the sums of the $k$ largest entries at $x$ and at $y$, so $\theta_1(z) + \cdots + \theta_k(z) \le t_1 + \cdots + t_k$. If $\theta(z) \ne t$, let $k$ be the first index where they differ; then $\theta_k(z) < t_k$ by the partial sums, which contradicts the minimality of $t$. So $\theta(z) = t$: the excesses at $z$, at $x$ and at $y$ are the same multiset. Then $\sum_S e(S, z)^2 = \sum_S e(S, x)^2 = \sum_S e(S, y)^2$. But $u \mapsto u^2$ is strictly convex, so $e(S, z)^2 \le (e(S, x)^2 + e(S, y)^2)/2$, with strict inequality whenever $e(S, x) \ne e(S, y)$. So $e(S, x) = e(S, y)$ for every $S$; taking $S = \{i\}$ gives $x = y$. $\square$

Basic facts:

- **In the core when the core is not empty.** A core point $c$ has $\theta_1(c) \le 0$, so $\theta_1(\nu) \le \theta_1(c) \le 0$, and $\nu$ has no positive excess. The coalitions $\emptyset$ and $N$ have excess 0 at every efficient $x$, so the nucleolus also minimizes, in the lexicographic order, the sorted excesses of the proper coalitions alone. So its largest proper excess is the least core value whenever the least core contains an imputation, and it is then in the least core.
- **Kohlberg's criterion.** For a preimputation $x$ and a real $\alpha$, let $D(\alpha, x) = \{S : \emptyset \ne S \ne N,\ e(S, x) \ge \alpha\}$. Then $x$ is the prenucleolus exactly when every nonempty $D(\alpha, x)$ is a balanced collection (Kohlberg 1971). A similar test, with the singletons $\{i\}$ where $x_i = v(\{i\})$ added, describes the nucleolus. The criterion gives a short certificate that a given vector is the prenucleolus.
- **Symmetry and covariance.** Players with the same role get the same payoff, and the nucleolus of $\alpha v + a$, for $\alpha > 0$ and additive $a$, is $\alpha \nu(v) + a$.
- **In the kernel.** The nucleolus lies in the kernel of the game (Schmeidler 1969).
- **Not additive.** Unlike the [Shapley value](/shapley-value/), the nucleolus of $v + w$ is in general not the sum of the nucleoli.

## Examples and non-examples

- **The glove game.** Player 1 holds a left glove and players 2 and 3 hold right gloves; $v(\{1, 2\}) = v(\{1, 3\}) = v(N) = 1$, and 0 otherwise. The core is the point $(1, 0, 0)$, so this is the nucleolus. The Shapley value $(2/3, 1/6, 1/6)$ is different.
- **The majority game.** $v(S) = 1$ when $|S| \ge 2$. By symmetry and uniqueness the nucleolus is $(1/3, 1/3, 1/3)$. The pairs have excess $1/3$ and the single players $-1/3$; both $D(1/3, x)$, the three pairs, and $D(-1/3, x)$, all proper coalitions, are balanced, as Kohlberg's criterion asks.
- **A segment of the core.** With $v(\{1, 2\}) = v(N) = 1$ and 0 otherwise, the core and the least core are the points $(t, 1 - t, 0)$. The largest excess is 0 at every one of them, for $\{1, 2\}$ and $\{3\}$. The next excesses are those of $\{1\}$, $\{2\}$, $\{1, 3\}$ and $\{2, 3\}$, which are $-t$ or $-(1 - t)$; they are lexicographically smallest at $t = 1/2$. The nucleolus is $(1/2, 1/2, 0)$.
- **The bankruptcy game.** For claims $(100, 200, 300)$ and estate $200$, $v(\{2, 3\}) = 100$, $v(N) = 200$ and 0 otherwise. The nucleolus is $(50, 75, 75)$, the Talmud rule of the Mishna (Aumann and Maschler 1985).
- **When the nucleolus and the prenucleolus differ.** Let $v(\{1, 2\}) = 2$, $v(\{1, 3\}) = 3$, $v(\{2, 3\}) = 4$, $v(N) = 2$ and $v(\{i\}) = 0$. The core is empty. The prenucleolus is $(-1/3, 2/3, 5/3)$, which gives player 1 less than $v(\{1\}) = 0$. The nucleolus is $(0, 1/2, 3/2)$.
- **Not the nucleolus: a lexicographic minimum of the unsorted vector.** The order of coalitions must come from the sizes of the excesses, not from a fixed list. Fixing a list of coalitions and minimizing their excesses in that order depends on the list and does not give the nucleolus.

## Related definitions

- **Least core.** The first step of the definition, minimizing $\theta_1$ over the proper coalitions, gives the [least core](/least-core/). Maschler, Peleg and Shapley show that the nucleolus is the end of a nested sequence of least cores, each defined on the coalitions whose excess is not yet fixed.
- **Sequential LP.** The [sequential LP](/nucleolus-sequential-lp/) turns this sequence into at most $n - 1$ rounds of linear programs, with exponentially many constraints in general.
- **Talmud rule.** On bankruptcy games the nucleolus is the [Talmud rule](/talmud-rule/), which takes $O(n \log n)$ time.
- **Assignment games.** For the [assignment game](/assignment-game/), Solymosi and Raghavan (1994) compute the nucleolus in polynomial time.
- **Hard cases.** For [minimum cost spanning tree games](/minimum-cost-spanning-tree-game/), computing the nucleolus is NP-hard (Faigle, Kern and Kuipers 1998).
- **Shapley value.** The [Shapley value](/shapley-value/) is the other standard one-point solution. It is linear in the game but need not be in the core; the nucleolus is in the core when the core is not empty but is not linear.

## References
