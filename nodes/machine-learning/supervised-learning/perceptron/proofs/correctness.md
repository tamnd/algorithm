---
title: The perceptron returns a separator, and on separable data it returns one
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $z_i = (x_i, 1) \in \mathbb{R}^{d+1}$ for the augmented examples and $v = (w, b)$ for the augmented weights. Then line L5 tests $y_i\, v \cdot z_i \le 0$, and lines L6 and L7 together do $v \leftarrow v + y_i z_i$.

**Lemma 1 (soundness).** If PERCEPTRON returns at line L9, then $y_i (w \cdot x_i + b) > 0$ for each $i$.

*Proof.* Line L9 returns after an epoch with $errors = 0$. In that epoch the test of line L5 failed for each $i$, so lines L6 to L8 never ran, and $v$ had the same value $v^\ast$ during the whole epoch. The failed test for example $i$ says $y_i\, v^\ast \cdot z_i > 0$. The returned pair is $v^\ast$. $\square$

**Lemma 2 (mistake bound).** Let $R' = \max_i \lVert z_i \rVert$. Suppose a unit vector $u \in \mathbb{R}^{d+1}$ and a $\gamma > 0$ satisfy $y_i\, u \cdot z_i \ge \gamma$ for each $i$. Then lines L6 and L7 run at most $(R'/\gamma)^2$ times in total, over all epochs.

*Proof.* Let $v_k$ be the value of $v$ after the $k$-th update, with $v_0 = 0$. The $k$-th update uses some example $(z, y)$ from $S$ with $y\, v_{k-1} \cdot z \le 0$, and sets $v_k = v_{k-1} + y z$.

First, $u \cdot v_k = u \cdot v_{k-1} + y\, u \cdot z \ge u \cdot v_{k-1} + \gamma$. By induction from $u \cdot v_0 = 0$, $u \cdot v_k \ge k \gamma$.

Second, $\lVert v_k \rVert^2 = \lVert v_{k-1} \rVert^2 + 2 y\, v_{k-1} \cdot z + \lVert z \rVert^2 \le \lVert v_{k-1} \rVert^2 + R'^2$, because the middle term is at most 0 at a mistake and $y^2 = 1$. By induction, $\lVert v_k \rVert^2 \le k R'^2$.

By the Cauchy-Schwarz inequality and $\lVert u \rVert = 1$, $k \gamma \le u \cdot v_k \le \lVert v_k \rVert \le \sqrt{k}\, R'$. For $k \ge 1$ this gives $k \le (R'/\gamma)^2$. So no $k$-th update exists for $k > (R'/\gamma)^2$. $\square$

**Theorem.** If $S$ is separated by some $(w^\ast, b^\ast)$, that is $y_i (w^\ast \cdot x_i + b^\ast) > 0$ for each $i$, and $T > M = (R'/\gamma)^2$ with $u = (w^\ast, b^\ast)/\lVert (w^\ast, b^\ast) \rVert$ and $\gamma = \min_i y_i\, u \cdot z_i$, then PERCEPTRON returns at line L9 a pair that separates $S$, after at most $M + 1$ epochs.

*Proof.* Since $S$ is finite and each $y_i\, u \cdot z_i$ is positive, $\gamma > 0$, and Lemma 2 applies. Each epoch that does not return at line L9 has $errors \ge 1$, so it runs at least one update. By Lemma 2, at most $\lfloor M \rfloor$ epochs can do so. So one of the epochs $1, \ldots, \lfloor M \rfloor + 1$ has no update and returns at line L9, and $\lfloor M \rfloor + 1 \le T$. By Lemma 1 the returned pair separates $S$. $\blacksquare$

**Remark.** Lemma 2 never uses the order of the examples, nor that they come from a finite set: it holds for any sequence of examples, each with $\lVert z \rVert \le R'$ and $y\, u \cdot z \ge \gamma$. This is the online form of the [perceptron convergence theorem](/perceptron-convergence-theorem/).
