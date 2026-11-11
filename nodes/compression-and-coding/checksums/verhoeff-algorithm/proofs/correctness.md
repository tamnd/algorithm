---
title: The Verhoeff check digit is valid by construction and catches every single error and every adjacent transposition
proves: [correctness]
status: full
---

Write $a \ast b$ for $D[a][b]$ and $\sigma$ for the permutation in row 1 of $P$. The tests verify, on all elements, the facts used below:

- (G) $(\{0, \ldots, 9\}, \ast)$ is a group with identity 0 and inverse $\mathrm{INV}$: $0 \ast a = a \ast 0 = a$, $(a \ast b) \ast c = a \ast (b \ast c)$ for all 1,000 triples, and $a \ast \mathrm{INV}[a] = \mathrm{INV}[a] \ast a = 0$.
- (P) Row $i$ of $P$ is $\sigma^i$, and $\sigma^8$ is the identity, so $P[i \bmod 8] = \sigma^i$ for every $i \ge 0$.
- (A) $a \ast \sigma(b) \ne b \ast \sigma(a)$ for all digits $a \ne b$.

In a group, $u \ast v = u \ast w$ implies $v = w$ (multiply by $u^{-1}$ on the left), and $v \ast u = w \ast u$ implies $v = w$. We call this cancellation.

**Lemma 1 (the loop).** For a digit string $y$ read from the right as $y_0, y_1, \ldots, y_k$, STATE$(y, s)$ returns $\sigma^{s}(y_0) \ast \sigma^{s+1}(y_1) \ast \cdots \ast \sigma^{s+k}(y_k)$.

*Proof.* By induction on the digits read. Before the loop $c = 0$, the empty product. If after $j$ digits $c$ is the product of the first $j$ factors, line L3 sets $c \leftarrow c \ast P[(s + j) \bmod 8][y_j] = c \ast \sigma^{s+j}(y_j)$ by (P), which is the product of the first $j + 1$ factors. By (G) the product is well defined without brackets. $\square$

**Theorem 1 (generation).** For every payload $p$, the code word $w = p\,c$ with $c$ from line L5 passes line L6.

*Proof.* Read $w$ from the right: $w_0 = c$ and $w_{j} = p_{j-1}$, where $p_0, p_1, \ldots$ are the payload digits from the right. By Lemma 1, STATE$(w, 0) = \sigma^0(c) \ast q = c \ast q$, where $q = \sigma^1(p_0) \ast \sigma^2(p_1) \ast \cdots =$ STATE$(p, 1)$. Line L5 sets $c = \mathrm{INV}[q]$, so $c \ast q = 0$ by (G). $\square$

**Corollary 1 (uniqueness).** For each payload exactly one digit $c$ makes $p\,c$ valid.

*Proof.* The map $c \mapsto c \ast q$ is injective by cancellation, so exactly one $c$ gives 0. $\square$

**Theorem 2 (single errors).** If one digit of a valid code word changes, the result is invalid.

*Proof.* Let the digit at position $i$ change from $a$ to $b \ne a$. By Lemma 1 the product changes from $L \ast \sigma^i(a) \ast R$ to $L \ast \sigma^i(b) \ast R$, where $L$ and $R$ are the products of the factors before and after position $i$. Since $\sigma^i$ is a permutation, $\sigma^i(a) \ne \sigma^i(b)$, and by cancellation on both sides the two products differ. The first one is 0, so the second is not. $\square$

**Theorem 3 (adjacent transpositions).** If two adjacent digits $a \ne b$ of a valid code word are swapped, the result is invalid.

*Proof.* Let $a$ be at position $i$ and $b$ at position $i + 1$. The product changes from $L \ast \sigma^i(a) \ast \sigma^{i+1}(b) \ast R$ to $L \ast \sigma^i(b) \ast \sigma^{i+1}(a) \ast R$. Let $u = \sigma^i(a)$ and $v = \sigma^i(b)$. Then $u \ne v$, $\sigma^{i+1}(b) = \sigma(v)$ and $\sigma^{i+1}(a) = \sigma(u)$. By (A) applied to $u \ne v$, $u \ast \sigma(v) \ne v \ast \sigma(u)$, and by cancellation the two full products differ. So the new product is not 0. $\square$

**Remark (why the permutation is needed).** Without $\sigma$, a swap is missed whenever $a \ast b = b \ast a$, which holds for example for all pairs of rotations $0, \ldots, 4$. The permutation breaks this symmetry, and the non-commutativity of $D_5$ is what makes (A) possible. The only abelian group of order 10 is $\mathbb{Z}_{10}$, and there no permutation satisfies (A). In $\mathbb{Z}_{10}$, (A) says that $h(x) = \sigma(x) - x$ takes distinct values, so $h$ is a bijection of $\mathbb{Z}_{10}$. Then $\sum_x h(x) \equiv 0 + 1 + \cdots + 9 = 45 \equiv 5 \pmod{10}$. But $\sum_x h(x) = \sum_x \sigma(x) - \sum_x x = 0$, a contradiction. This extends the bound for weighted sums on the [check digit computation](/check-digit-computation/) page.

**Cost.** By Lemma 1, each digit costs two table lookups, so STATE, CHECK-DIGIT and IS-VALID take $\Theta(n)$ time and $O(1)$ extra space. $\blacksquare$
