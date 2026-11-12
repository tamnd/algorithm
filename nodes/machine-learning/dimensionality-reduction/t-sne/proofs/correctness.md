---
title: The t-SNE affinities form a symmetric distribution and the t-SNE gradient is correct
proves: [correctness]
status: full
---

We use the notation of the page. The bandwidth search for the rows $p_{\cdot|i}$ is the one of [stochastic neighbor embedding](/stochastic-neighbor-embedding/), where it is proved that each row meets its target perplexity. Here we prove the two facts that are new in t-SNE.

## Part 1: the joint affinities

Let each row $p_{\cdot|i}$ be a probability distribution on $\{1, \ldots, n\} \setminus \{i\}$, and set $p_{ij} = (p_{j|i} + p_{i|j}) / 2n$ for $i \ne j$ and $p_{ii} = 0$.

**Lemma 1.** $p_{ij} = p_{ji} \ge 0$, $\sum_{i \ne j} p_{ij} = 1$, and $\sum_{j} p_{ij} > 1/(2n)$ for each $i$.

*Proof.* Symmetry and the sign are clear from the formula. For the sum, $\sum_{i}\sum_{j \ne i} p_{j|i} = \sum_i 1 = n$, and $\sum_i \sum_{j \ne i} p_{i|j} = \sum_j \sum_{i \ne j} p_{i|j} = n$ by the exchange of the order of summation. So the total is $(n + n)/2n = 1$. For one $i$, $\sum_j p_{ij} = \frac{1}{2n}\big(1 + \sum_{j \ne i} p_{i|j}\big)$. The second sum is positive, since each $p_{i|j}$ is a value of a Gaussian kernel and is positive. $\square$

The last property is the reason for the symmetrization: an outlier $x_i$ still carries at least the weight $1/2n$, so its map point is fixed by the cost.

## Part 2: the gradient

Let $d_{ij} = \|y_i - y_j\|^2$, $w_{ij} = (1 + d_{ij})^{-1}$ for $i \ne j$, $Z = \sum_{k \ne l} w_{kl}$ and $q_{ij} = w_{ij}/Z$. The cost is

$$C = \mathrm{KL}(P \,\|\, Q) = \sum_{i \ne j} p_{ij} \ln p_{ij} - \sum_{i \ne j} p_{ij} \ln q_{ij}.$$

**Theorem.** $\dfrac{\partial C}{\partial y_l} = 4 \sum_{j \ne l} (p_{lj} - q_{lj})\, w_{lj}\, (y_l - y_j)$.

*Proof.* The first sum of $C$ does not depend on $y$. Since $\ln q_{ij} = \ln w_{ij} - \ln Z$ and $\sum_{i \ne j} p_{ij} = 1$ by Lemma 1,

$$C = \text{const} + \sum_{i \ne j} p_{ij} \ln(1 + d_{ij}) + \ln Z.$$

We use $\partial d_{lj} / \partial y_l = 2(y_l - y_j)$, and $d_{lj} = d_{jl}$.

*The middle sum.* The ordered pairs that hold $y_l$ are $(l, j)$ and $(j, l)$ for $j \ne l$. They have the same value since $p$ and $d$ are symmetric, so the derivative is

$$2 \sum_{j \ne l} p_{lj} \frac{1}{1 + d_{lj}} \cdot 2 (y_l - y_j) = 4 \sum_{j \ne l} p_{lj} w_{lj} (y_l - y_j).$$

*The log of the normalizer.* $\partial w_{lj} / \partial d_{lj} = -(1 + d_{lj})^{-2} = -w_{lj}^2$. Again the pairs $(l, j)$ and $(j, l)$ hold $y_l$, so

$$\frac{\partial \ln Z}{\partial y_l} = \frac{1}{Z} \cdot 2 \sum_{j \ne l} (-w_{lj}^2) \cdot 2 (y_l - y_j) = -4 \sum_{j \ne l} q_{lj} w_{lj} (y_l - y_j).$$

Add the two parts. $\square$

**Corollary (early exaggeration).** For a factor $e > 0$, the vector $4 \sum_j (e\, p_{lj} - q_{lj}) w_{lj} (y_l - y_j)$ that the algorithm uses in the first steps is the exact gradient of $e \sum_{i \ne j} p_{ij} \ln(1 + d_{ij}) + \ln Z$. The same computation with $p$ replaced by $e\,p$ proves it, since Lemma 1 was used only to drop the factor $\sum p_{ij}$ in front of $\ln Z$, and here that factor is kept as 1 by the definition of the function. So the exaggerated phase is gradient descent on a different, fixed function, and not on $C$.

## What is not claimed

$C$ is not convex: it is unchanged when the map is moved, turned or mirrored, so a minimum is never an isolated point, and different starts can end in maps of different quality. The theorem shows only that each step moves along the exact gradient, with momentum and gains. The tree method of van der Maaten (2014) replaces the exact gradient by an approximation whose error depends on the parameter $\theta$, so for it even this statement holds only approximately.
