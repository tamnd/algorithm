---
title: The exact search gives the Smatch score, hill climbing gives a lower bound and stops, and the best mapping is NP-hard to find
proves: [correctness, termination]
status: full
---

We use the definitions and the pseudocode of the page. The test graph $T$ and the gold graph $G$ are sets of triples. $T$ has $m$ variables and $G$ has $n$ variables, and the two sets of variables are disjoint. A mapping $\varphi$ sends each test variable to a gold variable or to nothing, and no two test variables go to the same gold variable. A constant maps to itself. A test triple matches under $\varphi$ if all its variables are mapped and its image is a triple of $G$. $M(\varphi)$ is the number of matched test triples, and $M^* = \max_\varphi M(\varphi)$.

## Part 1: the score is a function of the best match count

For a mapping $\varphi$ the precision is $P = M(\varphi)/|T|$, the recall is $R = M(\varphi)/|G|$, and

$$F = \frac{2PR}{P + R} = \frac{2 M(\varphi)^2 / (|T|\,|G|)}{M(\varphi)\,(|T| + |G|)/(|T|\,|G|)} = \frac{2 M(\varphi)}{|T| + |G|}$$

when $M(\varphi) > 0$, and $F = 0$ when $M(\varphi) = 0$. The sizes $|T|$ and $|G|$ do not depend on $\varphi$, so $P$, $R$ and $F$ all grow with $M(\varphi)$, and one mapping maximizes all three. Smatch is $F$ at $M^*$.

The match count is symmetric. If $\varphi$ is a mapping from $T$ to $G$, its inverse $\varphi^{-1}$ on the image is a mapping from $G$ to $T$. A test triple $t$ matches the gold triple $\varphi(t)$ exactly when $\varphi^{-1}$ maps $\varphi(t)$ to $t$, and $\varphi$ is one to one on triples because it is one to one on variables. So the matched triples of the two directions are in bijection, and $M^*$ is the same in both directions.

For a corpus of pairs $(T_i, G_i)$ the score is computed from the sums, $P = \sum_i M^*_i / \sum_i |T_i|$, $R = \sum_i M^*_i / \sum_i |G_i|$ and $F = 2 \sum_i M^*_i / (\sum_i |T_i| + \sum_i |G_i|)$, by the same algebra. This is in general not the mean of the sentence scores.

## Part 2: the exact search is correct

The function `match_count` looks at each test triple once. It skips a triple whose first variable is unmapped, or whose second field is an unmapped variable. Otherwise it forms the image and tests it against $G$. This is the definition of a match, so it returns $M(\varphi)$.

`smatch_brute_force` enumerates every one to one partial map from the $m$ test variables to the $n$ gold variables: it chooses an ordered list of $m$ slots from the $n$ gold variables and $m$ copies of "nothing", and it removes repeated lists. There are $\sum_{k} \binom{m}{k} \frac{n!}{(n-k)!}$ of them, where $k$ is the number of mapped variables. It keeps the largest count, so it returns $M^*$.

**Monotonicity.** Let $\varphi$ leave a test variable $v$ unmapped, and let $g$ be a gold variable outside the image of $\varphi$. Let $\varphi'$ agree with $\varphi$ and send $v$ to $g$. Every triple that matches under $\varphi$ does not contain $v$, because a triple with an unmapped variable never matches, so it has the same image under $\varphi'$ and still matches. Hence $M(\varphi') \ge M(\varphi)$. Repeating this, a mapping that is maximal (it maps $\min(m, n)$ variables) reaches $M^*$. So an exact search may restrict itself to maximal mappings. When $m \le n$, these are the $n!/(n-m)!$ one to one maps of all test variables.

## Part 3: hill climbing stops and gives a lower bound

`climb` starts from a mapping and looks at two kinds of moves: send one test variable to an unused gold variable or to nothing, and swap the images of two test variables. Each move gives a one to one mapping again. Line L5 stops when no move raises $M$. Otherwise line L6 takes the move with the largest gain.

**Termination.** The gain of a taken move is a positive integer, so $M$ rises by at least 1 at each step. $M$ is at most $|T|$. So `climb` takes at most $|T|$ steps. Each step looks at $m(n + 1) + \binom{m}{2}$ moves. `smatch_hill_climb` runs `climb` once from the concept-matching start and once from each of a fixed number of random starts, so it stops.

**Lower bound.** Every mapping that `climb` holds is a one to one partial map, so its count is $M(\varphi) \le M^*$. The result of `smatch_hill_climb` is the count of one such mapping, so it is at most $M^*$, and the score it reports is at most the true Smatch score.

**Not always optimal.** The result of one climb is a local maximum: no single move raises $M$. It need not be $M^*$. Take

- $T$: `instance(t0, p)`, `instance(t1, q)`, `r(t0, t1)`,
- $G$: `instance(g0, q)`, `instance(g1, q)`, `r(g0, g1)`.

The concept-matching start finds no gold variable with concept $p$ for $t_0$, and gives $t_1$ the first gold variable with concept $q$. So it is $t_0 \mapsto$ nothing, $t_1 \mapsto g_0$, with $M = 1$. The moves are: $t_0 \mapsto g_1$ (the relation goes to `r(g1, g0)`, which is not in $G$, so $M = 1$), $t_1 \mapsto g_1$ ($M = 1$), $t_1 \mapsto$ nothing ($M = 0$), and the swap ($t_0 \mapsto g_0$, $t_1 \mapsto$ nothing, $M = 0$). None of them raises $M$, so the climb stops at 1. The mapping $t_0 \mapsto g_0$, $t_1 \mapsto g_1$ matches `instance(t1, q)` and `r(t0, t1)`, so $M^* = 2$. The tests check this case and also check, on random graphs, that random restarts find $M^*$ where one climb does not.

## Part 4: the best mapping is NP-hard

The decision problem asks, for graphs $T$ and $G$ and an integer $k$, whether some mapping has $M(\varphi) \ge k$.

**It is in NP.** A mapping is a certificate of size $O(m)$, and `match_count` checks it in time polynomial in $|T| + |G|$.

**It is NP-hard.** We reduce from [subgraph isomorphism](/subgraph-isomorphism/): given undirected graphs $H$ and $K$, is there a one to one map $f$ from the vertices of $H$ to the vertices of $K$ that sends every edge of $H$ to an edge of $K$? This problem is NP-complete, since it contains the clique problem. Build $T$ from $H$: a variable $x_v$ with the triple `instance(x_v, node)` for each vertex $v$, and the two triples `edge(x_u, x_v)` and `edge(x_v, x_u)` for each edge $\{u, v\}$. Build $G$ from $K$ in the same way. Let $k = |V(H)| + 2|E(H)| = |T|$. The construction takes linear time.

If $f$ exists, the mapping $x_v \mapsto x_{f(v)}$ is one to one. Every instance triple matches, because all concepts are `node`. Each edge triple `edge(x_u, x_v)` maps to `edge(x_{f(u)}, x_{f(v)})`, which is in $G$ because $\{f(u), f(v)\}$ is an edge of $K$. So $M = |T| = k$.

If some mapping has $M \ge k = |T|$, every test triple matches. An instance triple matches only if its variable is mapped, so every test variable is mapped, and $f(v) =$ the vertex of the image of $x_v$ is one to one. An edge triple matches only if its image is an edge triple of $G$, so $f$ sends every edge of $H$ to an edge of $K$. So $H$ is isomorphic to a subgraph of $K$.

Hence the decision problem is NP-complete, even with one concept and one role. Computing $M^*$ is therefore NP-hard, and no polynomial time exact algorithm exists unless P = NP. The tests run this reduction on random small graphs and compare it with a direct search for the subgraph. ∎
