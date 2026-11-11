---
title: The Damm check digit is valid by construction and catches every single error and every adjacent transposition
proves: [correctness]
status: full
---

Write $a \ast b$ for $Q[a][b]$. The tests verify, on all elements, the facts used below:

- (L) Every row and every column of $Q$ is a permutation of $\{0, \ldots, 9\}$. So $a \ast u = a \ast v$ implies $u = v$, and $u \ast a = v \ast a$ implies $u = v$.
- (Z) $x \ast x = 0$ for every digit $x$.
- (W) For all digits $c, x, y$: if $(c \ast x) \ast y = (c \ast y) \ast x$ then $x = y$.

For a digit string $y_1 \ldots y_k$ read from the left and a start value $s$, let $W(s; y_1 \ldots y_k)$ be defined by $W(s; \varepsilon) = s$ and $W(s; y_1 \ldots y_k) = W(s; y_1 \ldots y_{k-1}) \ast y_k$. This is the walk.

**Lemma 1 (the loop).** INTERIM$(y)$ returns $W(0; y)$.

*Proof.* By induction on the digits read. Line L1 sets $c = 0 = W(0; \varepsilon)$. If after $j$ digits $c = W(0; y_1 \ldots y_j)$, line L3 sets $c \leftarrow c \ast y_{j+1} = W(0; y_1 \ldots y_{j+1})$. Line L4 returns the value after all digits. $\square$

**Lemma 2 (the walk keeps differences).** If $s \ne t$ then $W(s; y) \ne W(t; y)$ for every string $y$.

*Proof.* By induction on the length of $y$. For the empty string the claim is $s \ne t$. If $W(s; y') \ne W(t; y')$, then $W(s; y' d) = W(s; y') \ast d$ and $W(t; y' d) = W(t; y') \ast d$ differ by (L), because column $d$ is a permutation. $\square$

Note that $W(s; uv) = W(W(s; u); v)$ for strings $u, v$, by the definition.

**Theorem 1 (generation).** For every payload $p$, the code word $w = p\,c$ with $c$ from line L5 passes line L6.

*Proof.* By Lemma 1 and line L5, $c = W(0; p)$. Then $W(0; p\,c) = W(0; p) \ast c = c \ast c = 0$ by (Z), so line L6 returns true. $\square$

**Corollary 1 (uniqueness).** For each payload exactly one digit $c$ makes $p\,c$ valid.

*Proof.* Let $q = W(0; p)$. Then $W(0; p\,c) = q \ast c$. Row $q$ is a permutation by (L), so exactly one $c$ gives 0, and by (Z) it is $c = q$. $\square$

**Theorem 2 (single errors).** If one digit of a valid code word changes, the result is invalid.

*Proof.* Write the code word as $u\,a\,v$ and the changed word as $u\,b\,v$ with $a \ne b$. Let $s = W(0; u)$. Then $s \ast a \ne s \ast b$ by (L), because row $s$ is a permutation. By Lemma 2, $W(s \ast a; v) \ne W(s \ast b; v)$. The first value is $W(0; u\,a\,v) = 0$, so the second, $W(0; u\,b\,v)$, is not 0. $\square$

**Theorem 3 (adjacent transpositions).** If two adjacent digits $x \ne y$ of a valid code word are swapped, the result is invalid.

*Proof.* Write the code word as $u\,x\,y\,v$ and the changed word as $u\,y\,x\,v$. Let $s = W(0; u)$. By (W), since $x \ne y$, $(s \ast x) \ast y \ne (s \ast y) \ast x$. By Lemma 2 applied to $v$, $W(0; u\,x\,y\,v) \ne W(0; u\,y\,x\,v)$. The first value is 0, so the second is not. This covers every position, including a swap at the start, where $s = 0$, and a swap of the check digit with the last payload digit, where $v$ is empty. $\square$

**Remark (leading zeros).** By (Z), $0 \ast 0 = 0$, so $W(0; 0^k y) = W(0; y)$ for every $k$. So leading zeros change neither the check digit nor the result of the test.

**Remark (no identity needed).** The proof uses no associativity and no identity element. Only (L), (Z) and (W) are used, and each is a finite condition on the table that the tests check over all 10, 100 or 1,000 cases.

**Cost.** By Lemma 1, each digit costs one table lookup, so INTERIM, CHECK-DIGIT and IS-VALID take $\Theta(n)$ time and $O(1)$ extra space. $\blacksquare$
