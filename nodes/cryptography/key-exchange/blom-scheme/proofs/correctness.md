---
title: Blom's keys agree, k users learn nothing about another key, and k + 1 users learn all keys
proves: [correctness]
status: full
---

We use the notation of the page. $\mathbb{F}_q$ is a finite field, the identities $x_1, \dots, x_n$ are distinct, $g_i = (1, x_i, \dots, x_i^k)^T$, $D$ is a uniformly random symmetric $(k + 1) \times (k + 1)$ matrix over $\mathbb{F}_q$, $a_i = D g_i$ and $K_{ij} = a_i \cdot g_j$.

**Theorem 1 (agreement).** For all users $i$ and $j$, $K_{ij} = K_{ji}$.

*Proof.* $K_{ij} = a_i^T g_j = (D g_i)^T g_j = g_i^T D^T g_j = g_i^T D g_j$, using $D^T = D$. This is a $1 \times 1$ matrix, so it equals its transpose, $g_j^T D g_i = (D g_j)^T g_i = a_j^T g_i = K_{ji}$. $\blacksquare$

**Lemma 2 (Vandermonde).** For distinct $x_1, \dots, x_{k+1}$, the matrix with rows $g_1^T, \dots, g_{k+1}^T$ is invertible. For any set $C$ of at most $k$ identities, there is a nonzero vector $w$ with $w \cdot g_c = 0$ for all $c \in C$ and $w \cdot g_i \ne 0$ for every identity $x_i$ not in $C$.

*Proof.* A vector $v$ with $g_c^T v = 0$ for all $k + 1$ rows gives a polynomial $v_0 + v_1 t + \dots + v_k t^k$ of degree at most $k$ with $k + 1$ distinct roots, so $v = 0$, and the square matrix is invertible. For the second claim, let $w$ be the coefficient vector of $w(t) = \prod_{c \in C}(t - x_c)$, a nonzero polynomial of degree $|C| \le k$, padded with zeros to length $k + 1$. Then $w \cdot g = w(x)$ for $g = (1, x, \dots, x^k)$, so $w \cdot g_c = 0$ for $c \in C$, and $w(x_i) \ne 0$ for $x_i \notin \{x_c\}$. $\blacksquare$

**Theorem 3 ($k$-security).** Let $C$ be a set of at most $k$ users, and let $i \ne j$ be two users not in $C$. Then for every possible view $(a_c)_{c \in C}$ of the coalition that has positive probability, $K_{ij}$ is uniformly distributed on $\mathbb{F}_q$ given that view.

*Proof.* Take $w$ from Lemma 2 and, for $\lambda \in \mathbb{F}_q$, define the map $\phi_\lambda(D) = D + \lambda w w^T$. It sends symmetric matrices to symmetric matrices and is a bijection, with inverse $\phi_{-\lambda}$. For $c \in C$, $\phi_\lambda(D) g_c = D g_c + \lambda w (w^T g_c) = D g_c$, so $\phi_\lambda$ preserves the coalition's view. And

$$g_i^T \phi_\lambda(D) g_j = g_i^T D g_j + \lambda (w \cdot g_i)(w \cdot g_j) = K_{ij} + \lambda \beta,$$

with $\beta = w(x_i) w(x_j) \ne 0$ by Lemma 2. Fix a view $V$ and let $S_V$ be the set of symmetric matrices consistent with it. For two values $\kappa, \kappa' \in \mathbb{F}_q$, the map $\phi_\lambda$ with $\lambda = (\kappa' - \kappa)/\beta$ is a bijection from the matrices in $S_V$ with $K_{ij} = \kappa$ onto those with $K_{ij} = \kappa'$. So every key value has the same number of matrices in $S_V$. Since $D$ is uniform, its conditional distribution given $V$ is uniform on $S_V$, and $K_{ij}$ is uniform. $\blacksquare$

**Theorem 4 ($k + 1$ users learn everything).** If $C$ has $k + 1$ users, then $D$ is determined by $(a_c)_{c \in C}$, and so is every key.

*Proof.* Let $G_C$ be the $(k + 1) \times (k + 1)$ matrix with columns $g_c$, and $A_C$ the matrix with columns $a_c = D g_c$, so $A_C = D G_C$. Taking transposes, $A_C^T = G_C^T D^T = G_C^T D$. By Lemma 2, $G_C^T$ is invertible, so $D = (G_C^T)^{-1} A_C^T$. Then $K_{ij} = g_i^T D g_j$ for any $i$ and $j$. $\blacksquare$

**Remark (optimal storage).** Each user stores $k + 1$ elements of $\mathbb{F}_q$. HAC, Fact 12.34, due to Blom, states that any scheme in which coalitions of $k$ users learn nothing about other keys of $\log_2 q$ bits needs at least $(k + 1)\log_2 q$ bits per user; we do not prove this bound here. $\blacksquare$
