---
title: The cycles of the LF mapping are the Lyndon factors, so the transform is a bijection
proves: [correctness]
status: full
---

We use the notation of the page. $T = w_1 w_2 \cdots w_m$ is the Lyndon factorization of $T \in \Sigma^n$, with $w_1 \ge w_2 \ge \cdots \ge w_m$. $R$ is the multiset of the $n$ rotations of the factors: for each factor $w_t$ and each $0 \le i < |w_t|$, one copy of $w_t[i \ldots]\,w_t[\ldots i-1]$. The rows are the words of $R$ in $\omega$ order, $L[r]$ is the last symbol of row $r$, and $\mathrm{word}(r)$ is the word of row $r$. For a nonempty word $u = x c$ with last symbol $c$, let $\rho(u) = c x$.

We use two standard facts about Lyndon words (Lothaire, Chapter 5). A Lyndon word is primitive, and so is each of its rotations. Two Lyndon words that are rotations of each other are equal, since each is the strictly smallest rotation of the same set.

**Lemma 1 (equal infinite powers).** If $u$ and $v$ are primitive and $u^\omega = v^\omega$, then $u = v$.

*Proof.* Let $p = |u|$, $q = |v|$, $X = u^\omega = v^\omega$, and $g = \gcd(p, q)$. $X$ has the periods $p$ and $q$: $X[i] = X[i + p] = X[i + q]$ for all $i \ge 0$. There are integers $a, b \ge 0$ with $g = a p - b q$. Then $X[i + g] = X[i + g + b q] = X[i + a p] = X[i]$, so $X$ has period $g$. Since $g$ divides $p$, $u = X[0 \ldots p-1] = z^{p/g}$ with $z = X[0 \ldots g-1]$, and $u$ is primitive, so $p = g$. In the same way $q = g$. So $u$ and $v$ are both the first $g$ symbols of $X$. $\square$

**Lemma 2 (equal lengths).** If $|u| = |v|$, then $u^\omega < v^\omega$ if and only if $u < v$.

*Proof.* If $u \ne v$, the first index where they differ is less than $|u|$, and $u^\omega$ and $v^\omega$ differ first at the same index with the same symbols. If $u = v$, both sides are false. $\square$

**Lemma 3 (the key of line L5).** For nonempty words $u$ and $v$ of length at most $n$, $u^\omega$ and $v^\omega$ compare in the same way as their prefixes of length $2n$.

*Proof.* If the prefixes differ, the first difference decides both comparisons. Suppose the prefixes are equal. Let $p = |u|$, $q = |v|$, $g = \gcd(p, q)$. The common prefix $Y$ of length $p + q - g \le 2n$ has the periods $p$ and $q$, so by the theorem of Fine and Wilf it has the period $g$. Since $|Y| \ge \max(p, q)$, $u = Y[0 \ldots p-1]$ and $v = Y[0 \ldots q-1]$ both have the period $g$, which divides $p$ and $q$, so both are powers of $z = Y[0 \ldots g-1]$. Then $u^\omega = z^\omega = v^\omega$. $\square$

By Lemma 3, line L5 sorts $R$ in $\omega$ order. Each word of $R$ is primitive, so by Lemma 1 two words of $R$ that are equal in $\omega$ order are equal words. So the sorted list of words is unique, and $L$ does not depend on how the sort breaks ties. If $a < b$ are rows, then $\mathrm{word}(a) \le_\omega \mathrm{word}(b)$, and equal words are on consecutive rows. For a word $u$, let $B(u)$ be the interval of rows that hold $u$.

**Lemma 4 (moving the last symbol to the front).** For words $x c$ and $y c$ of $R$, $x c <_\omega y c$ if and only if $c x <_\omega c y$.

*Proof.* $(c x)^\omega = c\,(x c)^\omega$ and $(c y)^\omega = c\,(y c)^\omega$. The two infinite words agree on the first symbol and then compare like $(x c)^\omega$ and $(y c)^\omega$. $\square$

**Lemma 5 (the LF mapping on blocks).** Let $\mathrm{LF}(i) = C[L[i]] + \mathrm{rank}_{L[i]}(L, i)$, where $C[c]$ counts the symbols of $L$ smaller than $c$. For each word $u$ of $R$, $\mathrm{LF}$ maps the $t$-th row of $B(u)$ to the $t$-th row of $B(\rho(u))$, for each $t$. In particular $\mathrm{word}(\mathrm{LF}(i)) = \rho(\mathrm{word}(i))$.

*Proof.* The map $\rho$ sends the rotation of $w_t$ at offset $i$ to the rotation of $w_t$ at offset $(i - 1) \bmod |w_t|$, so it is a bijection of the copies in the multiset $R$. So $u$ and $\rho(u)$ have the same number of copies in $R$, and the words of $R$ that start with $c$ are exactly the images $\rho(x c)$ of the words $x c$ of $R$ that end with $c$.

The first symbol of $u^\omega$ is $u[0]$, so the rows that start with a symbol smaller than $c$ come before the rows that start with $c$. The multiset of the first symbols of $R$ and the multiset of the last symbols of $R$ are both the multiset of the symbols of $T$, so there are $C[c]$ rows before the first row that starts with $c$, and the rows that start with $c$ are the rows $C[c], C[c] + 1, \ldots, C[c] + m_c - 1$, where $m_c$ is the number of occurrences of $c$.

Let $i_0 < i_1 < \cdots < i_{m_c - 1}$ be the rows with $L[i_k] = c$, and write $\mathrm{word}(i_k) = x_k c$. These words are nondecreasing in $\omega$ order, so by Lemma 4 the words $c x_0, c x_1, \ldots$ are nondecreasing too. They are the words of $R$ that start with $c$, so this list is the sorted list of those words, which is unique. So row $C[c] + k$ holds $c x_k = \rho(\mathrm{word}(i_k))$, and $\mathrm{LF}(i_k) = C[c] + k$ by the definition of rank. The rows of $B(u)$, for $u$ ending with $c$, are consecutive rows among $i_0, i_1, \ldots$, say $i_s, \ldots, i_{s+b-1}$. They map to the consecutive rows $C[c] + s, \ldots, C[c] + s + b - 1$, which all hold $\rho(u)$. Since $B(\rho(u))$ has $b$ rows, these are all of its rows, in order. $\square$

**Lemma 6 (the cycles).** Let $i$ be a row with $\mathrm{word}(i) = u$, a rotation of the factor $w$, and let $\ell = |u|$. Then the cycle of $\mathrm{LF}$ through $i$ has length exactly $\ell$. Its rows hold the $\ell$ rotations of $w$, one each, and its smallest row holds $w$.

*Proof.* By Lemma 5, if $i$ is the $t$-th row of $B(u)$, then $\mathrm{LF}^j(i)$ is the $t$-th row of $B(\rho^j(u))$. Since $\rho^\ell(u) = u$, $\mathrm{LF}^\ell(i) = i$. For $0 < j < \ell$, $\rho^j(u)$ is a proper rotation of the primitive word $u$, which differs from $u$, so $\mathrm{LF}^j(i) \ne i$. So the cycle has length $\ell$ and its rows hold the words $\rho^j(u)$, $0 \le j < \ell$, which are the $\ell$ distinct rotations of $w$. Rows in increasing order hold words in nondecreasing $\omega$ order, so the smallest row of the cycle holds the smallest of these words in $\omega$ order. They all have length $\ell$, so by Lemma 2 this is the smallest rotation in the usual order, which is the Lyndon word $w$. $\square$

**Lemma 7 (reading a cycle).** If the walk of line I5 starts at the row $r_0$ that holds $w$, with $\ell = |w|$, the symbols it reads are $w[\ell-1], w[\ell-2], \ldots, w[0]$, so line I6 appends $w$.

*Proof.* By Lemma 5, the $j$-th row of the walk holds $\rho^j(w) = w[\ell-j \ldots \ell-1]\,w[0 \ldots \ell-j-1]$ for $0 \le j < \ell$, and its last symbol is $w[\ell - j - 1]$. $\square$

**Theorem (the inverse returns $T$, and the transform is a bijection).** For each $T \in \Sigma^n$, $\mathrm{INVERSE\text{-}BBWT}(\mathrm{BBWT}(T)) = T$. So $\mathrm{BBWT}$ is a bijection of $\Sigma^n$.

*Proof.* Line I1 computes the $\mathrm{LF}$ of Lemma 5 from $L$ alone. The loop of line I3 visits the rows in increasing order and starts a walk only at a row that is not visited yet, so each walk starts at the smallest row of its cycle, and by Lemmas 6 and 7 appends the factor of that cycle. Now count the cycles. Two factors that are rotations of each other are equal Lyndon words, so the rows that hold rotations of a factor $w$ are the $|w|$ rotations of the copies of $w$ in the factorization, and they number $|w|$ times the number $e_w$ of copies. By Lemma 6 each cycle on these rows has $|w|$ rows, so there are $e_w$ such cycles, and $W$ is the multiset $\{w_1, \ldots, w_m\}$. Words that are equal in the usual order are equal, so the nonincreasing order of $W$ is unique, and it is $w_1, w_2, \ldots, w_m$. Line I8 returns $w_1 w_2 \cdots w_m = T$.

So $\mathrm{BBWT}$ has a left inverse and is one to one. It maps $\Sigma^n$ into $\Sigma^n$, because its output is a permutation of its input. A one-to-one map of a finite set into itself is onto, so it is a bijection. $\blacksquare$
