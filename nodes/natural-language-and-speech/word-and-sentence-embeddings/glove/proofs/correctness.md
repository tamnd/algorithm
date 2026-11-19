---
title: GloVe counts the co-occurrences exactly and each step is a descent step on the weighted least squares cost
proves: [correctness]
status: full
---

GloVe has no guarantee of a global minimum, because its cost is not convex. We prove the three facts that the algorithm relies on: line L1 computes the co-occurrence matrix of the definition, lines L5 to L7 use the exact gradient of one term of the cost, and each such step lowers that term for a small enough step size. We also prove the two facts about the minimum that the page states.

**Notation.** A sentence is a token sequence $t_1, \ldots, t_n$. For words $i$ and $j$, the definition is

$$X_{ij} = \sum_{1 \le p < q \le n,\ q - p \le K} \frac{1}{q - p}\Big([t_q = i][t_p = j] + [t_p = i][t_q = j]\Big),$$

summed over the sentences. The cost is $J = \sum_{(i, j) \in S} J_{ij}$ with $S = \{(i, j) : X_{ij} > 0\}$, $J_{ij} = f_{ij}\, e_{ij}^2$, $f_{ij} = f(X_{ij}) > 0$ and the residual $e_{ij} = \vec w_i \cdot \tilde{\vec w}_j + b_i + \tilde b_j - \log X_{ij}$.

## Claim 1. Line L1 computes $X$.

The loop visits every position $q$ and, for $r = 1, \ldots, K$ with $q - r \ge 1$, the position $p = q - r$. So it visits each pair $p < q$ with $q - p \le K$ exactly once, from its later position. For that pair it adds $1/(q - p)$ to the cell $(t_q, t_p)$ and to the cell $(t_p, t_q)$. The cell $(i, j)$ therefore receives $1/(q - p)$ once for each such pair with $t_q = i, t_p = j$ and once for each such pair with $t_p = i, t_q = j$. When $t_p = t_q = i$, both additions go to the cell $(i, i)$, which matches the two indicator terms of the definition that are both 1. The sum is the definition of $X_{ij}$. Since the definition is symmetric in $i$ and $j$, so is $X$. $\square$

## Claim 2. Lines L5 to L7 use the gradient of $J_{ij}$.

Only $J_{ij}$ is touched in a visit of cell $(i, j)$. With $e = e_{ij}$ and $f = f_{ij}$, the chain rule gives

$$\frac{\partial J_{ij}}{\partial \vec w_i} = 2 f e\, \tilde{\vec w}_j, \quad \frac{\partial J_{ij}}{\partial \tilde{\vec w}_j} = 2 f e\, \vec w_i, \quad \frac{\partial J_{ij}}{\partial b_i} = \frac{\partial J_{ij}}{\partial \tilde b_j} = 2 f e,$$

and every other partial derivative of $J_{ij}$ is zero. When $i = j$, $\vec w_i$ and $\tilde{\vec w}_i$ are still different parameters, so the formulas hold unchanged. Line L6 sets $g = f e$, which is half of the common factor, and line L7 moves each of these parameters by $-\eta g / \sqrt{G}$ times the matching vector, with all quantities taken at the point before the step. So the step is $\Delta = -\frac{\eta}{2} D \nabla J_{ij}$, where $D$ is the diagonal matrix of the values $1/\sqrt{G} > 0$ of the touched coordinates and is zero elsewhere. $\square$

## Claim 3. For a small enough $\eta$ the step lowers $J_{ij}$.

If $\nabla J_{ij} = 0$ there is nothing to show. Otherwise, $J_{ij}$ is a polynomial in the parameters, so it is differentiable, and by Taylor's theorem

$$J_{ij}(\theta + \Delta) = J_{ij}(\theta) + \nabla J_{ij} \cdot \Delta + o(\eta) = J_{ij}(\theta) - \frac{\eta}{2} \nabla J_{ij}^\top D \nabla J_{ij} + o(\eta).$$

The gradient is zero outside the touched coordinates, and $D$ is positive on them, so $\nabla J_{ij}^\top D \nabla J_{ij} > 0$. For $\eta$ small enough, the negative term is larger than the remainder, and $J_{ij}(\theta + \Delta) < J_{ij}(\theta)$. The values of $G$ only grow during the run (line L7 adds squares), so $D$ stays bounded by its start value, which is the identity on the touched coordinates because $G$ starts at 1. $\square$

## Claim 4. $J \ge 0$, with $J = 0$ exactly at an exact fit.

Every term is $f_{ij} e_{ij}^2$ with $f_{ij} > 0$, so $J \ge 0$, and $J = 0$ if and only if $e_{ij} = 0$ for every $(i, j) \in S$. So if some parameters fit every nonzero cell exactly, they are a global minimum, and every global minimum with value 0 is such a fit. $\square$

## Claim 5. $J$ is a convex quadratic in each $\vec w_i$ with the rest fixed.

Fix all parameters except $\vec w_i$. Then $J = \sum_{j : (i, j) \in S} f_{ij} (\tilde{\vec w}_j \cdot \vec w_i - c_j)^2 + \text{const}$ with $c_j = \log X_{ij} - b_i - \tilde b_j$. This is a weighted least squares cost in $\vec w_i$, with Hessian $2 \sum_j f_{ij} \tilde{\vec w}_j \tilde{\vec w}_j^\top$, which is positive semidefinite. So $J$ is convex in $\vec w_i$, and the same argument applies to $\tilde{\vec w}_j$ and to the biases. $\blacksquare$
