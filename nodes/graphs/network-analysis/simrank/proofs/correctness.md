---
title: The SimRank iteration converges from below to the unique SimRank matrix
proves: [correctness, termination]
status: full
---

We use the notation of the page. $G = (V, E)$ is a directed graph with $n$ vertices, $I(v)$ is the list of in-neighbours of $v$ (with repeats if arcs repeat), and $0 < C < 1$. Let $\mathcal M$ be the set of real $n \times n$ matrices with the max norm $\|X\| = \max_{a, b} |X_{ab}|$. Define the map $F : \mathcal M \to \mathcal M$ by

$$F(X)_{ab} = \begin{cases} 1 & a = b, \\ 0 & a \ne b \text{ and } (I(a) = \emptyset \text{ or } I(b) = \emptyset), \\ \dfrac{C}{|I(a)|\,|I(b)|} \displaystyle\sum_{i \in I(a)} \sum_{j \in I(b)} X_{ij} & \text{otherwise.} \end{cases}$$

The SimRank matrix is a matrix $S$ with $F(S) = S$. Lines L3 to L6 compute $R' = F(R)$, so after line L1 and $k$ rounds of lines L2 to L7 the matrix is $R_k = F^k(R_0)$, where $R_0$ is the identity matrix.

**Lemma 1 (contraction).** For all $X, Y \in \mathcal M$, $\|F(X) - F(Y)\| \le C\, \|X - Y\|$.

*Proof.* In the first two cases $F(X)_{ab} - F(Y)_{ab} = 0$. In the third case,

$$|F(X)_{ab} - F(Y)_{ab}| \le \frac{C}{|I(a)|\,|I(b)|} \sum_{i \in I(a)} \sum_{j \in I(b)} |X_{ij} - Y_{ij}| \le \frac{C}{|I(a)|\,|I(b)|} \cdot |I(a)|\,|I(b)|\, \|X - Y\| = C\, \|X - Y\|. \quad \square$$

**Lemma 2 (existence and uniqueness).** $F$ has exactly one fixed point $S$, and $R_k \to S$.

*Proof.* $\mathcal M$ with the max norm is a complete metric space, and $F$ is a contraction with factor $C < 1$ by Lemma 1. By the Banach fixed-point theorem, $F$ has a unique fixed point $S$, and $F^k(X) \to S$ for every starting matrix $X$, in particular for $X = R_0$. $\square$

**Lemma 3 (order).** $F$ is monotone: if $X \le Y$ entrywise then $F(X) \le F(Y)$. Moreover $R_0 \le R_1 \le R_2 \le \cdots \le S$, and $0 \le S_{ab} \le 1$ with $S_{ab} \le C$ for $a \ne b$.

*Proof.* Monotonicity is clear from the definition, since the coefficients $C/(|I(a)||I(b)|)$ are positive. $R_1$ has ones on the diagonal, like $R_0$, and non-negative entries elsewhere, where $R_0$ has zeros, so $R_0 \le R_1$. Applying $F^k$ and monotonicity gives $R_k \le R_{k+1}$ for all $k$. The limit of a non-decreasing sequence is above each term, so $R_k \le S$. Let $J$ be the matrix with ones on the diagonal and $C$ elsewhere. Then $F(J) \le J$, because each average of entries of $J$ is at most 1, times $C$. Since $R_0 \le J$, induction with monotonicity gives $R_k = F^k(R_0) \le F^k(J) \le J$ for all $k$, and in the limit $S \le J$. Finally $S \ge R_0 \ge 0$. $\square$

**Lemma 4 (error bound).** For every $k \ge 0$ and all $a, b$: $0 \le S_{ab} - (R_k)_{ab} \le C^{k+1}$.

*Proof.* The lower bound is Lemma 3. For the upper bound, $\|S - R_0\| \le C$, since the diagonals agree and $0 \le S_{ab} \le C$ elsewhere by Lemma 3. By Lemma 1 and $S = F(S)$, $\|S - R_k\| = \|F^k(S) - F^k(R_0)\| \le C^k \|S - R_0\| \le C^{k+1}$. $\square$

**Theorem.** SIMRANK$(G, C, K)$ stops after $K$ rounds and returns a symmetric matrix $R_K$ with $S_{ab} - C^{K+1} \le (R_K)_{ab} \le S_{ab}$ for all $a, b$, where $S$ is the unique SimRank matrix. If $K \ge \lceil \log \varepsilon / \log C \rceil - 1$, every entry is within $\varepsilon$ of the exact score.

*Proof.* Termination: line L2 runs $K$ times, and each round runs over the $n^2$ pairs and, for each pair, over the finite lists $I(a)$ and $I(b)$. The bounds are Lemma 4. Symmetry: $R_0$ is symmetric, and if $X$ is symmetric then so is $F(X)$, because swapping $a$ and $b$ swaps the two sums and $X_{ij} = X_{ji}$; by induction every $R_k$ is symmetric. For the last claim, $K + 1 \ge \log \varepsilon / \log C$ gives $C^{K+1} \le \varepsilon$, since $\log C < 0$. $\blacksquare$
