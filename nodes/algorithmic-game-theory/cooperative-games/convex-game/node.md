---
tag: W0X4VA
kind: definition
slug: convex-game
name: Convex game
aliases:
- supermodular TU game
area: algorithmic-game-theory/cooperative-games
level: core
summary: "A TU game with v(S) + v(T) at most v(S union T) + v(S intersect T), so a player adds more to a larger coalition. Its core is never empty."
prereqs: [transferable-utility-game, core-of-a-cooperative-game]
see_also: [shapley-convex-games-theorem, bondareva-shapley-theorem, shapley-value, nucleolus, bankruptcy-problem, airport-game, submodular-function, matroid]
sources:
  - paper: doi:10.1007/BF01753431
    title: "Lloyd S. Shapley, Cores of convex games, International Journal of Game Theory 1(1) (1971), 11-26"
    locator: the definition of convex games, the equivalent condition on marginal contributions, and the structure of their core
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Section 17.7 (convex games and their core) and Section 18.7 (the Shapley value of a convex game)
  - paper: doi:10.1007/BF02109593
    title: "Imma J. Curiel, Michael Maschler and Stef H. Tijs, Bankruptcy games, Zeitschrift fur Operations Research 31(5) (1987), A143-A159"
    locator: bankruptcy games are convex
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 3, The core (pp. 27-49), the core of convex games
---

A convex game is a [TU game](/transferable-utility-game/) in which a player adds more to a larger coalition than to a smaller one. The characteristic function is supermodular, the mirror image of a [submodular function](/submodular-function/). Convexity is a strong form of increasing returns, and it makes the [core](/core-of-a-cooperative-game/) as nice as it can be: [Shapley's theorem](/shapley-convex-games-theorem/) says that the core is not empty, that its corners are the marginal vectors, and that it contains the [Shapley value](/shapley-value/). The [Bondareva-Shapley theorem](/bondareva-shapley-theorem/) is the test for a nonempty core in every game; convexity is a simple sufficient condition.

## Definition

A TU game $(N, v)$ is convex if

$$v(S \cup T) + v(S \cap T) \ge v(S) + v(T) \quad \text{for all } S, T \subseteq N.$$

An equivalent condition uses marginal contributions. The game is convex if and only if

$$v(S \cup \{i\}) - v(S) \le v(T \cup \{i\}) - v(T) \quad \text{whenever } S \subseteq T \subseteq N \setminus \{i\}.$$

The first condition gives the second with $S' = S \cup \{i\}$ and $T$: their union is $T \cup \{i\}$ and their intersection is $S$. For the converse, list $T \setminus S = \{j_1, \ldots, j_k\}$ and add these players one at a time to $S \cap T$ and to $S$. Each one adds at least as much to the larger set, and the sums telescope to $v(T) - v(S \cap T) \le v(S \cup T) - v(S)$.

It is enough to check the condition for two players at a time: the game is convex exactly when $v(S \cup \{i\}) + v(S \cup \{j\}) \le v(S \cup \{i, j\}) + v(S)$ for every $S$ and every pair $i \ne j$ outside $S$. Given a table of $v$, this is $\binom{n}{2} 2^{n-2}$ checks.

A cost game $c$ is called concave, or submodular, when $c(S \cup T) + c(S \cap T) \le c(S) + c(T)$. Its savings game $v(S) = \sum_{i \in S} c(\{i\}) - c(S)$ is then convex.

Basic facts:

- A convex game is superadditive: for disjoint $S$ and $T$ the condition reads $v(S \cup T) + v(\emptyset) \ge v(S) + v(T)$.
- Convexity is kept under strategic equivalence: $\alpha v + a$ is convex for $\alpha > 0$ and additive $a$.
- The convex games on $N$ form a convex cone. Every subgame of a convex game is convex.
- The core of a convex game is not empty and equals the convex hull of the $n!$ marginal vectors, so every convex game is totally balanced. The Shapley value is in the core, and so is the [nucleolus](/nucleolus/), since the core is not empty.
- The core is the base polytope of the supermodular function $v$. So a linear function $c \cdot x$ can be minimized over the core by a greedy rule: sort the players by decreasing $c_i$ and take the marginal vector of that order. This is Edmonds' greedy algorithm for polymatroids, in the language of games.

## Examples and non-examples

- **Symmetric games with convex growth.** If $v(S) = f(|S|)$ and $f(k + 1) - f(k)$ grows with $k$, the game is convex. With $v(S) = |S|^2$ on three players the marginal vector of the order $1, 2, 3$ is $(1, 3, 5)$, and the Shapley value is $(3, 3, 3)$.
- **Unanimity games.** For a nonempty $T \subseteq N$, let $u_T(S) = 1$ if $T \subseteq S$ and 0 otherwise. Then $u_T$ is convex, and so is every sum of unanimity games with nonnegative weights.
- **Bankruptcy games.** For claims $c$ and estate $E$, $v(S) = \max(0, E - c(N \setminus S))$ is convex (Curiel, Maschler and Tijs 1987); the [bankruptcy problem](/bankruptcy-problem/) page has the short proof.
- **Airport games.** The [airport game](/airport-game/) cost $c(S) = \max_{i \in S} r_i$, the longest runway that a plane in $S$ needs, is concave, so its savings game is convex.
- **Not convex: the glove game.** With $v(\{1, 2\}) = v(\{1, 3\}) = v(N) = 1$ and 0 otherwise, take $S = \{1, 2\}$ and $T = \{1, 3\}$: $v(S) + v(T) = 2 > 1 = v(S \cup T) + v(S \cap T)$. The core is the point $(1, 0, 0)$, so a game can have a nonempty core without being convex. It is also an [assignment game](/assignment-game/), and assignment games are usually not convex.
- **Not convex: the majority game.** The same $S$ and $T$ give $2 > 1$. The game is superadditive, so superadditivity does not imply convexity. Here the core is empty.

## Related definitions

- **Supermodular and submodular functions.** A convex game is a supermodular set function with $v(\emptyset) = 0$; $-v$ is a [submodular function](/submodular-function/).
- **Strictly convex games.** The inequality is strict whenever neither of $S$ and $T$ contains the other. Then the $n!$ marginal vectors are distinct, and the core has exactly $n!$ corners.
- **Weber set.** The convex hull of the marginal vectors. It contains the core of every game, and equals the core exactly when the game is convex (Shapley 1971; Ichiishi 1981 for the converse).
- **Totally balanced games.** Games in which every subgame has a nonempty core. Convex games are totally balanced, but many totally balanced games, such as assignment games, are not convex.
- **Polymatroids.** A polymatroid is given by a monotone submodular function; the core of a convex game is the base polytope of a supermodular function, the same object turned around. The rank function of a [matroid](/matroid/) is the basic example.

## References
