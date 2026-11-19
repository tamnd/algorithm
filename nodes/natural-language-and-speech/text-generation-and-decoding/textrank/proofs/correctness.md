---
title: The TextRank iteration converges to the unique fixed point, with a bound for its stopping rule
proves: [correctness]
status: full
---

Let $W = (w_{ij})$ be the $n \times n$ weight matrix built by line L1. It is symmetric, nonnegative and has a zero diagonal. Let $\mathrm{out}_j = \sum_k w_{jk}$ (line L2), and let $M$ be the $n \times n$ matrix with $M_{ij} = w_{ji} / \mathrm{out}_j$ when $\mathrm{out}_j > 0$ and $M_{ij} = 0$ otherwise. Fix $0 \le d < 1$. Line L5 computes $F(x) = (1 - d)\mathbf{1} + d M x$ from $x = WS$, because the terms with $w_{ji} = 0$ are 0. The norm is $\|x\|_1 = \sum_i |x_i|$.

**Lemma 1 (column sums).** Column $j$ of $M$ sums to 1 if $\mathrm{out}_j > 0$ and to 0 otherwise. Hence $\|M y\|_1 \le \|y\|_1$ for every vector $y$.

*Proof.* If $\mathrm{out}_j > 0$, then $\sum_i M_{ij} = \sum_i w_{ji} / \mathrm{out}_j = 1$. Otherwise the column is 0. Since $M \ge 0$, $\|My\|_1 = \sum_i |\sum_j M_{ij} y_j| \le \sum_j |y_j| \sum_i M_{ij} \le \|y\|_1$. $\square$

**Lemma 2 (contraction).** $\|F(x) - F(y)\|_1 \le d \|x - y\|_1$.

*Proof.* $F(x) - F(y) = dM(x - y)$; apply Lemma 1. $\square$

**Theorem 1 (fixed point and convergence).** $F$ has exactly one fixed point $WS^*$. The sequence $x_0 = \mathbf{1}$, $x_{t+1} = F(x_t)$ of lines L3 to L7 satisfies $\|x_t - WS^*\|_1 \le d^t \|x_0 - WS^*\|_1$.

*Proof.* $\mathbb{R}^n$ with the 1-norm is complete, and $F$ is a contraction with factor $d < 1$ by Lemma 2, so the Banach fixed point theorem gives one fixed point and convergence from any start. The rate follows by induction: $\|x_{t+1} - WS^*\|_1 = \|F(x_t) - F(WS^*)\|_1 \le d \|x_t - WS^*\|_1$. Equivalently, $I - dM$ is invertible (its Neumann series $\sum_t d^t M^t$ converges), and $WS^* = (1 - d)(I - dM)^{-1}\mathbf{1}$. $\square$

**Theorem 2 (stopping rule).** If line L8 stops after computing $x_{t+1}$ with $\delta = \|x_{t+1} - x_t\|_1 < \varepsilon$, then $\|x_{t+1} - WS^*\|_1 \le \frac{d}{1 - d}\,\delta$.

*Proof.* Let $e = \|x_{t+1} - WS^*\|_1$. By Lemma 2, $e \le d\|x_t - WS^*\|_1 \le d(\|x_t - x_{t+1}\|_1 + e) = d(\delta + e)$. Rearranging gives $e(1 - d) \le d\delta$. $\square$

**Theorem 3 (mass).** Let $Z$ be the set of isolated vertices ($\mathrm{out}_j = 0$) and $A$ the rest. Then $WS^*(i) = 1 - d$ for $i \in Z$, and $\sum_{i \in A} WS^*(i) = |A|$.

*Proof.* For $i \in Z$, $w_{ji} = w_{ij} = 0$ for every $j$, so row $i$ of $M$ is 0 and the fixed point equation gives $WS^*(i) = 1 - d$. For $i \in A$, row $i$ of $M$ has nonzero entries only in columns $j$ with $w_{ji} > 0$, and those $j$ are in $A$. Summing the fixed point equation over $i \in A$ gives $\sum_{i \in A} WS^*(i) = (1 - d)|A| + d \sum_{j \in A} WS^*(j) \sum_{i \in A} M_{ij}$. For $j \in A$, every $i$ with $M_{ij} > 0$ has $w_{ji} > 0$, so $i \in A$, and by Lemma 1 the inner sum is 1. So $s = \sum_{i \in A} WS^*(i)$ satisfies $s = (1 - d)|A| + ds$, which gives $s = |A|$. $\blacksquare$

**Remark (scale).** Replacing $W$ by $cW$ for a constant $c > 0$ leaves every $M_{ij}$ unchanged, so the scores do not depend on the base of the logarithm in line L1.

**Remark (output).** Line L9 sorts the indices by (score descending, index ascending) and returns the first $k$ sorted by index, which is the set of the definition. The scores used are those of the final iterate, which are within the bound of Theorem 2 of $WS^*$; since the errors of two coordinates add up to at most that bound, two sentences can be ranked in the wrong order only if their true scores differ by at most the bound. A smaller $\varepsilon$ makes this gap as small as needed.

**Remark (keywords).** The keyword graph is the same construction with weights 0 or 1, so Theorems 1 to 3 hold for it too.
