---
title: RFC 1624 Eqn. 3 and Eqn. 4 equal a full recompute, and RFC 1141 differs only at +0
proves: [correctness]
status: full
---

**Notation.** All words are in $[0, 65535]$. For an integer $X \ge 0$, let $\mathrm{oc}(X) = 0$ if $X = 0$, and otherwise the unique value in $[1, 65535]$ congruent to $X$ modulo 65535. On [ones' complement arithmetic](/ones-complement-arithmetic/) we show that a ones' complement sum $a_1 \oplus \cdots \oplus a_r$ equals $\mathrm{oc}(a_1 + \cdots + a_r)$. Write $\bar a = 65535 - a$ for the complement of a word $a$.

Let $T$ be the plain sum of the header words other than the checksum field, with $m$ among them, so $T \ge m$. The stored checksum is $HC = \overline{\mathrm{oc}(T)}$. After the change, the plain sum is $T' = T - m + m'$, and a full recompute gives $\overline{\mathrm{oc}(T')}$. Note that $\mathrm{oc}(T') = 0$ if and only if $T' = 0$, that is, if and only if every word of the new header other than the checksum is 0.

**Lemma 1.** Let $X, Y \ge 0$ with $X \equiv Y \pmod{65535}$. Then $\mathrm{oc}(X) = \mathrm{oc}(Y)$ unless one of $X, Y$ is 0 and the other is not. In that case one of $\mathrm{oc}(X), \mathrm{oc}(Y)$ is 0 and the other is 65535.

*Proof.* If both are 0, both values are 0. If both are positive, both values are the unique representative in $[1, 65535]$ of the same class. If $X = 0 < Y$, then $Y \equiv 0$, so $\mathrm{oc}(Y) = 65535$. $\square$

**Theorem 1 (Eqn. 3).** UPDATE returns $\overline{\mathrm{oc}(T')}$, the value of a full recompute, whenever $T' > 0$. If $T' = 0$, it returns 0x0000 while a full recompute returns 0xFFFF.

*Proof.* Line L1 gives $c = \overline{HC} = \mathrm{oc}(T)$. Lines L2 and L3 give $c = \mathrm{oc}(T) \oplus \bar m \oplus m' = \mathrm{oc}(X)$ with $X = \mathrm{oc}(T) + \bar m + m'$. Since $\mathrm{oc}(T) \equiv T$ and $\bar m \equiv -m$, we get $X \equiv T - m + m' = T' \pmod{65535}$.

We show that $X > 0$. If $X = 0$, then $\bar m = 0$, so $m = 65535$, and $\mathrm{oc}(T) = 0$, so $T = 0$. But $T \ge m = 65535$, a contradiction.

So $X > 0$. If $T' > 0$, Lemma 1 gives $\mathrm{oc}(X) = \mathrm{oc}(T')$, and line L4 returns $\overline{\mathrm{oc}(T')}$. If $T' = 0$, Lemma 1 gives $\mathrm{oc}(X) = 65535$, and line L4 returns 0, while the recompute gives $\overline{0} = 65535$. $\square$

In IPv4 the first word of the header holds the version 4, so $T' > 0$ always, and Eqn. 3 always equals a full recompute.

**Theorem 2 (RFC 1141, Eqn. 2).** The value $E_2 = HC \oplus m \oplus \bar{m'}$ equals the recompute, except when the recompute gives 0x0000 and not ($HC = 0$, $m = 0$, $m' = 65535$). In that case $E_2 = 0xFFFF$.

*Proof.* $E_2 = \mathrm{oc}(Y)$ with $Y = HC + m + \bar{m'}$. Since $HC \equiv -T$, $Y \equiv -(T - m + m') = -T'$. The recompute is $R = \overline{\mathrm{oc}(T')}$, and $R \equiv -T'$ as well. So $E_2 \equiv R \pmod{65535}$, and both lie in $[0, 65535]$. They can differ only if one is 0 and the other is 65535.

If $R = 65535$, then $\mathrm{oc}(T') = 0$, so $T' = 0$. Then $m' = 0$ and $T = m$, so $HC = \overline{\mathrm{oc}(m)}$ and $\bar{m'} = 65535$, so $Y \ge 65535 > 0$ and $E_2 \in [1, 65535]$ with $E_2 \equiv 0$, so $E_2 = 65535 = R$.

If $R = 0$, then $E_2 = 0$ exactly when $Y = 0$, that is, when $HC = 0$, $m = 0$ and $m' = 65535$. Otherwise $Y > 0$, $E_2 \equiv 0$, and $E_2 = 65535 \ne R$.

In every other case $R \in [1, 65534]$ and $E_2 \equiv R$ forces $E_2 = R$. $\square$

**Theorem 3 (Eqn. 4).** Define ones' complement subtraction by $a \ominus b = a - b$ if $a \ge b$, and $a - b + 65535$ otherwise. Then $E_4 = (HC \ominus \bar m) \ominus m'$ equals the recompute whenever $T' > 0$.

*Proof.* In both branches, $a \ominus b \in [0, 65535]$ and $a \ominus b \equiv a - b \pmod{65535}$. Also $a \ominus b = 65535$ only if $a = 65535$ and $b = 0$: in the first branch $a - b = 65535$ needs $a = 65535$, $b = 0$; in the second branch $a - b + 65535 \le 65534$. So $E_4 \equiv HC + m - m' \equiv -T' \equiv R \pmod{65535}$, and $E_4 = 65535$ needs $HC \ominus \bar m = 65535$ and $m' = 0$, hence $HC = 65535$ and $\bar m = 0$, that is, $m = 65535$. But $HC = 65535$ means $\mathrm{oc}(T) = 0$, so $T = 0 < m$, a contradiction. So $E_4 \in [0, 65534]$. If $T' > 0$, then $R = \overline{\mathrm{oc}(T')} \in [0, 65534]$, and two values in $[0, 65534]$ with the same residue modulo 65535 are equal. $\square$

**Cost.** UPDATE performs a fixed number of 16-bit operations, so it takes $\Theta(1)$ time and space, independent of the header length. $\blacksquare$
