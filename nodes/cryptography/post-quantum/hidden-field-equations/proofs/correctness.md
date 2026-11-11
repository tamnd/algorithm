---
title: HFE decryption finds the plaintext among the roots of F(X) = Y, and it returns the message unless another root passes the redundancy check
proves: [correctness]
status: full
---

We use the notation of the page. $K = \mathbb{F}_2[t]/(g(t))$ with $g$ irreducible of degree $n$, so $K = \mathbb{F}_{2^n}$, and $\varphi : K \to \mathbb{F}_2^n$ maps an element to its coordinates in the basis $1, t, \ldots, t^{n-1}$. $S$ and $T$ are invertible affine maps of $\mathbb{F}_2^n$, and the central polynomial is

$$F(X) = \sum_{2^i + 2^j \le d} a_{ij} X^{2^i + 2^j} + \sum_{2^i \le d} b_i X^{2^i} + c,$$

with a nonzero term of degree at least 1. We write $S$ also for $\varphi^{-1} \circ S$ and so on when the meaning is clear.

**Lemma 1 (the public map is quadratic).** The map $x \mapsto T(\varphi(F(\varphi^{-1}(S(x)))))$ from $\mathbb{F}_2^n$ to $\mathbb{F}_2^n$ is given by $n$ polynomials of degree at most 2 over $\mathbb{F}_2$.

*Proof.* The Frobenius map $X \mapsto X^2$ is additive in characteristic 2 and fixes $\mathbb{F}_2$, so $X \mapsto X^{2^i}$ is $\mathbb{F}_2$-linear, and in coordinates each output bit is a linear form in the input bits. Multiplication in $K$ is $\mathbb{F}_2$-bilinear, so in coordinates $X^{2^i + 2^j} = X^{2^i} \cdot X^{2^j}$ is a product of two linear forms, which is quadratic. So $F$ is quadratic in the coordinates. An affine change of the input keeps the degree at most 2, and an affine map of the output takes linear combinations of the polynomials. $\square$

**Lemma 2 (interpolation).** Let $f : \mathbb{F}_2^n \to \mathbb{F}_2^m$ be given by polynomials of degree at most 2, reduced with $x_j^2 = x_j$: $f(x) = c + \sum_j \ell_j x_j + \sum_{j < k} q_{jk} x_j x_k$ with $c, \ell_j, q_{jk} \in \mathbb{F}_2^m$. Then $c = f(0)$, $\ell_j = f(e_j) + c$ and $q_{jk} = f(e_j + e_k) + f(e_j) + f(e_k) + c$, so the public key computed in line L3 is exactly the map of Lemma 1.

*Proof.* Put the points in the formula: $f(0) = c$, $f(e_j) = c + \ell_j$, and $f(e_j + e_k) = c + \ell_j + \ell_k + q_{jk}$. Solve, using $-1 = 1$. $\square$

**Lemma 3 (root finding).** For $f \in K[X]$ of degree at least 1, ROOTS returns the set of roots of $f$ in $K$.

*Proof.* $X^{2^n} - X = \prod_{a \in K} (X - a)$, because every $a \in K$ satisfies $a^{2^n} = a$ and the polynomial has degree $2^n$. So $h = \gcd(f, X^{2^n} - X) = \prod_{a \in K,\, f(a) = 0} (X - a)$, with each root once; computing $X^{2^n} \bmod f$ by $n$ squarings does not change the gcd. Let $\mathrm{Tr}(z) = \sum_{i=0}^{n-1} z^{2^i}$, the trace from $K$ to $\mathbb{F}_2$, and $T_\beta(X) = \sum_{i=0}^{n-1} (\beta X)^{2^i}$. For a root $a$ of $h$, $T_\beta(a) = \mathrm{Tr}(\beta a) \in \{0, 1\}$, so $\gcd(h, T_\beta) = \prod_{a : \mathrm{Tr}(\beta a) = 0} (X - a)$. If $a \ne b$ are two roots, the map $\beta \mapsto \mathrm{Tr}(\beta (a - b))$ is a nonzero $\mathbb{F}_2$-linear form, because the trace is not identically zero and $\beta (a - b)$ runs over all of $K$. A nonzero linear form is nonzero on some basis element, so one of $\beta = 1, t, \ldots, t^{n-1}$ separates $a$ from $b$ and gives a proper factor. The recursion ends at linear factors $X + a_0$, whose root is $a_0$ in characteristic 2. $\square$

**Theorem (correctness).** Let $(pk, sk)$ come from KEYGEN, $m$ a message of $n - r$ bits, $x = m \,\|\, H(m)_r$ as in line L5, and $y = \mathcal{P}(x)$. Then $X_0 = S(x)$ is a root of $F(X) - Y$ with $Y = T^{-1}(y)$, and DECRYPT returns $m$ unless a root $X' \ne X_0$ processed before $X_0$ gives $x' = S^{-1}(X')$ whose last $r$ bits equal $H$ of its first $n - r$ bits. If $H$ is a random function, this happens with probability at most $(d - 1)\, 2^{-r}$.

*Proof.* By Lemmas 1 and 2, $y = T(F(S(x)))$, so line L7 gives $Y = F(S(x))$ and $X_0$ is a root of $F(X) - Y$, a polynomial of degree between 1 and $d$. By Lemma 3, line L8 lists all roots, among them $X_0$. For $X_0$, line L9 computes $S^{-1}(X_0) = x$, which passes the check by line L5, and returns $m$. DECRYPT returns another value only if an earlier root $X'$ passes the check. There are at most $d - 1$ other roots. For each, $x' \ne x$ since $S$ is a bijection; if the first $n - r$ bits of $x'$ differ from $m$, the check holds with probability $2^{-r}$ over the random function, and if they equal $m$, the check bits of $x'$ differ from those of $x$, so it fails. A union bound gives $(d - 1) 2^{-r}$. $\blacksquare$

**Remark (C*).** For C*, $F(X) = X^{2^\theta + 1}$ with $\gcd(2^\theta + 1, 2^n - 1) = 1$, so $F$ is a permutation of $K$ with inverse $Y \mapsto Y^h$, $h (2^\theta + 1) \equiv 1 \pmod{2^n - 1}$, and decryption needs no root finding and no redundancy. Patarin's relation follows from $B = A^{2^\theta + 1}$: raising to the power $2^\theta - 1$ gives $B^{2^\theta - 1} = A^{2^{2\theta} - 1}$, and multiplying by $AB$ gives $A B^{2^\theta} = A^{2^{2\theta}} B$. Both sides are $\mathbb{F}_2$-bilinear in $(A, B)$ by the argument of Lemma 1, so each of the $n$ coordinates gives a relation $\sum_{i,j} \gamma_{ij} x_i y_j + \sum_i \alpha_i x_i + \sum_j \beta_j y_j + \delta = 0$ that holds for every plaintext $x$ and its ciphertext $y$.
