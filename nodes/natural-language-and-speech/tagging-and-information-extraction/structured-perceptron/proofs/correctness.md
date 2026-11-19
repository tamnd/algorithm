---
title: "Viterbi decoding is exact, the perceptron makes a bounded number of mistakes on separable data, and lazy averaging is exact"
proves: [correctness]
status: full
---

Setting. A training set has pairs $(x_i, y_i)$ for $i = 1, \ldots, N$, where $x_i$ is a sentence and $y_i$ its gold tags. $\mathrm{GEN}(x)$ is the set of all tag sequences of the length of $x$ over the $k$ tags. $\Phi(x, y)$ is the global feature vector: the counts of the transition features $(y_{j-1}, y_j)$, with $y_0 = \langle s \rangle$ and $y_{n+1} = \langle /s \rangle$, and of the emission features $(y_j, x_j)$. The score of $y$ is $w \cdot \Phi(x, y)$.

## Claim 1: Viterbi returns a highest-scoring tag sequence

The score splits into local terms: $w \cdot \Phi(x, y) = \sum_{j=1}^{n} \bigl(w_{T}(y_{j-1}, y_j) + w_{E}(y_j, x_j)\bigr) + w_{T}(y_n, \langle /s \rangle)$. Let $\delta_j(t)$ be the largest value of the first $j$ local terms over the prefixes $y_1 \ldots y_j$ with $y_j = t$. Then $\delta_1(t) = w_T(\langle s \rangle, t) + w_E(t, x_1)$ and $\delta_j(t) = \max_g (\delta_{j-1}(g) + w_T(g, t)) + w_E(t, x_j)$, because the terms of a prefix ending in $g$ at $j - 1$ do not depend on $t$, and any prefix ending in $g$ can be replaced by a best one without changing the new terms. The best total is $\max_t (\delta_n(t) + w_T(t, \langle /s \rangle))$, and following the stored maximizers back gives a sequence with this score. This is the same argument as for the [Viterbi algorithm](/viterbi-algorithm/), with sums of weights in place of log probabilities. The test file checks the score against all $k^n$ sequences for $n \le 6$ and $k \le 3$. $\square$

## Claim 2: the mistake bound (Collins 2002, Theorem 1)

Suppose there is a vector $U$ with $\lVert U \rVert = 1$ and a $\delta > 0$ such that $U \cdot \Phi(x_i, y_i) - U \cdot \Phi(x_i, z) \ge \delta$ for all $i$ and all $z \in \mathrm{GEN}(x_i)$ with $z \ne y_i$. Let $R$ be a number with $\lVert \Phi(x_i, y_i) - \Phi(x_i, z) \rVert \le R$ for all such $i$ and $z$. Then the perceptron, run for any number of epochs, makes at most $R^2 / \delta^2$ mistakes.

Proof. Let $w^k$ be the weights before the $k$-th mistake, with $w^1 = 0$. At the $k$-th mistake, on example $i$, the decoder returns $z \ne y_i$ with $w^k \cdot \Phi(x_i, z) \ge w^k \cdot \Phi(x_i, y_i)$, since $z$ has the highest score under $w^k$ (Claim 1). The update is $w^{k+1} = w^k + d$ with $d = \Phi(x_i, y_i) - \Phi(x_i, z)$.

Lower bound. $U \cdot w^{k+1} = U \cdot w^k + U \cdot d \ge U \cdot w^k + \delta$, so by induction $U \cdot w^{k+1} \ge k \delta$. By the Cauchy-Schwarz inequality, $\lVert w^{k+1} \rVert \ge U \cdot w^{k+1} \ge k \delta$.

Upper bound. $\lVert w^{k+1} \rVert^2 = \lVert w^k \rVert^2 + 2 w^k \cdot d + \lVert d \rVert^2 \le \lVert w^k \rVert^2 + R^2$, because $w^k \cdot d \le 0$ by the choice of $z$. By induction $\lVert w^{k+1} \rVert^2 \le k R^2$.

Together, $k^2 \delta^2 \le k R^2$, so $k \le R^2 / \delta^2$. $\square$

Consequence. When the bound holds, there is an epoch with no mistakes after at most $R^2/\delta^2 + 1$ epochs, and from then on the weights do not change, so every later epoch is also clean and the final $w$ tags every training sentence correctly. The test file builds separable data from a random integer vector $u$, keeps only sentences whose best tagging under $u$ is unique, and checks the bound in the integer form $\text{mistakes} \cdot m^2 \le R^2 \lVert u \rVert^2$, where $m$ is the smallest score gap under $u$, so that $\delta = m / \lVert u \rVert$. It also checks that the last epoch is clean.

Collins also proves a bound for data that is not separable (Theorem 2) and a bound on the generalization error of the voted perceptron (Theorem 3, from Freund and Schapire 1999). These are not checked by the test file.

## Claim 3: lazy averaging is exact

Number the examples processed in all epochs $1, \ldots, J$, with $J = T N$. Let $d_j$ be the update at step $j$ ($d_j = 0$ if there was no mistake), so the weights after step $j$ are $w_j = \sum_{i \le j} d_i$. The averaged weights of Collins (2002, Section 2.5) are

$$\bar w = \frac{1}{J} \sum_{j=1}^{J} w_j = \frac{1}{J} \sum_{i=1}^{J} (J - i + 1) d_i = \sum_{i=1}^{J} d_i - \frac{1}{J} \sum_{i=1}^{J} (i - 1) d_i = w_J - \frac{u}{J},$$

where $u = \sum_i (i - 1) d_i$. The code keeps $c = i - 1$, the number of examples seen before step $i$, and adds $c \, d_i$ to $u$ at line L7; at the end $c = J$ and line L9 returns $w - u / c$. This needs work only for the features in each update, while the direct sum needs work for every feature after every example. The test file checks the two in exact rational arithmetic. $\square$
