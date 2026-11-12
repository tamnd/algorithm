---
title: An ordered one-dimensional SOM stays ordered, and the batch step solves a weighted least squares problem
proves: [correctness]
status: full
---

We use the notation of the page: units $j = 1, \ldots, K$ at grid positions $r_j$, weights $w_j$, the best matching unit $c = \arg\min_j \|x - w_j\|$, and the online step

$$w_j \leftarrow w_j + \beta_j (x - w_j), \qquad \beta_j = \alpha\, h(\|r_j - r_c\|).$$

There is no general convergence theorem for the SOM. We prove two exact facts and then list what is known only in special cases.

## Part 1: in one dimension, order is never lost

Take a chain of units $r_j = j$ and scalar inputs and weights. Call the map *ordered* if $w_1 < w_2 < \cdots < w_K$ or $w_1 > w_2 > \cdots > w_K$.

**Theorem 1.** Let $h$ be nonincreasing in the grid distance, and let $0 \le \beta_j < 1$ for all $j$. If the map is ordered before an online step, it is ordered after it, for every input $x \in \mathbb{R}$.

*Proof.* By symmetry (replace $x$ and all $w_j$ by their negatives) we may take $w_1 < \cdots < w_K$. Write $w_j' = (1 - \beta_j) w_j + \beta_j x$. For each $j < K$,

$$w_{j+1}' - w_j' = (1 - \beta_{j+1})(w_{j+1} - w_j) + (\beta_j - \beta_{j+1})(w_j - x) \qquad (1)$$

$$\phantom{w_{j+1}' - w_j'} = (1 - \beta_j)(w_{j+1} - w_j) + (\beta_{j+1} - \beta_j)(x - w_{j+1}). \qquad (2)$$

Both lines follow by expanding the right side. Since $c$ is the best matching unit and the weights are sorted, $x$ is not past the midpoints next to $w_c$:

$$\tfrac{1}{2}(w_{c-1} + w_c) \le x \le \tfrac{1}{2}(w_c + w_{c+1}) \qquad (3)$$

(drop a side when $c = 1$ or $c = K$). There are four cases.

- *$j \ge c + 1$.* The grid distance grows from $j$ to $j + 1$, so $\beta_j \ge \beta_{j+1}$. By (3), $x \le w_{c+1} \le w_j$. Both terms of (1) are $\ge 0$ and the first is $> 0$.
- *$j = c$.* Again $\beta_c \ge \beta_{c+1}$. If $x \le w_c$, (1) is positive as before. If $x > w_c$, then $x - w_c \le \frac{1}{2}(w_{c+1} - w_c)$ by (3), and (1) gives
  $$w_{c+1}' - w_c' \ge (w_{c+1} - w_c)\Big(1 - \beta_{c+1} - \tfrac{1}{2}(\beta_c - \beta_{c+1})\Big) = (w_{c+1} - w_c)\Big(1 - \tfrac{\beta_c + \beta_{c+1}}{2}\Big) > 0.$$
- *$j + 1 \le c - 1$.* Now $\beta_{j+1} \ge \beta_j$, and by (3), $x \ge w_{c-1} \ge w_{j+1}$. Both terms of (2) are $\ge 0$ and the first is $> 0$.
- *$j + 1 = c$.* Again $\beta_c \ge \beta_{c-1}$. If $x \ge w_c$, (2) is positive. If $x < w_c$, then $w_c - x \le \frac{1}{2}(w_c - w_{c-1})$ by (3), and (2) gives $w_c' - w_{c-1}' \ge (w_c - w_{c-1})(1 - \frac{\beta_{c-1} + \beta_c}{2}) > 0$.

So $w_1' < \cdots < w_K'$. $\square$

The Gaussian neighborhood $h(d) = e^{-d^2/2\sigma^2}$ is nonincreasing, and $\beta_j \le \alpha < 1$ when the learning rate is below 1. So for the rule on the page, the ordered states are *absorbing*: once a chain is ordered, no input can undo it. Theorem 1 does not say that a chain reaches an ordered state. That is the hard part, discussed below.

## Part 2: the batch step

Fix the best matching units $c(1), \ldots, c(n)$ of the inputs, and let $h_{ij} = h(\|r_j - r_{c(i)}\|) \ge 0$.

**Theorem 2.** If $\sum_i h_{ij} > 0$, the batch weight $w_j = \sum_i h_{ij} x_i / \sum_i h_{ij}$ is the unique minimizer of

$$E_j(w) = \sum_{i=1}^{n} h_{ij} \|x_i - w\|^2.$$

*Proof.* $E_j$ is a quadratic with gradient $2 \sum_i h_{ij} (w - x_i)$ and Hessian $2 \sum_i h_{ij} I$, which is positive definite. The gradient is zero exactly at the weighted mean. $\square$

So the batch SOM alternates two steps, like [Lloyd's algorithm](/lloyds-algorithm/): it assigns each input to its best matching unit, and then minimizes $\sum_j E_j$ with the assignments fixed. With $h_{ij} = [j = c(i)]$ (no neighborhood) it is exactly Lloyd's algorithm for [k-means](/k-means/). With a real neighborhood, the assignment step picks the nearest weight and not the unit that minimizes $\sum_j h_{ij}\|x_i - w_j\|^2$, so the two steps do not minimize one common function, and we do not claim that the batch SOM decreases a cost.

## What is known only in special cases

- **Ordering from a random start.** Cottrell and Fort (1987) proved, for a one-dimensional chain, inputs uniform on an interval, a constant learning rate and a neighborhood of the two adjacent units, that the chain becomes ordered with probability 1 in finite time. Theorem 1 then keeps it ordered. There are later extensions in one dimension; in two or more dimensions, there is no general proof that the map unfolds.
- **No energy function.** Erwin, Obermayer and Schulten (1992) showed that for a continuous input distribution the online SOM is not gradient descent on any energy function. A modified rule that picks the winner by the neighborhood-weighted distance $\sum_j h_{cj}\|x - w_j\|^2$ does descend an energy function (Heskes 1999).
- **Convergence of the weights.** With a learning rate that falls to 0 and a fixed neighborhood, the weights follow an ordinary differential equation (the Robbins-Monro view), but its limits are known in closed form only in simple cases.

The tests check Theorem 1 on random ordered chains, the batch step of Theorem 2 against its formula, and, for one fixed seed, that a random chain becomes ordered.
