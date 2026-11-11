---
title: Honest Diffie-Hellman parties get the same secret, and validated values give a secret of full order
proves: [correctness]
status: full
---

We use the notation of the page: $p = 2q + 1$ with $p$ and $q$ prime, $q > 2$, $G$ the subgroup of order $q$ of $\mathbb{Z}_p^*$, and $g$ a generator of $G$.

**Lemma 1 (the subgroup).** $G = \{ a \in \mathbb{Z}_p^* : a^q = 1 \}$, and every $a \in G$ with $a \ne 1$ has order exactly $q$.

*Proof.* $\mathbb{Z}_p^*$ is cyclic of order $p - 1 = 2q$. A cyclic group has exactly one subgroup of each order that divides its order, and the subgroup of order $q$ is the set of solutions of $a^q = 1$. The order of an element of $G$ divides $q$, which is prime, so it is 1 or $q$, and only $a = 1$ has order 1. $\blacksquare$

**Lemma 2 (honest values pass).** If $1 \le x \le q - 1$ and $X = g^x \bmod p$, then $2 \le X \le p - 2$ and $X^q \bmod p = 1$.

*Proof.* $X \in G$, so $X^q = 1$ by Lemma 1. Since $q \nmid x$, $X \ne 1$, and by Lemma 1 $X$ has order $q$. The element $p - 1 \equiv -1$ has order 2, and $q > 2$, so $X \ne p - 1$. The residue $X$ lies in $[1, p - 1]$, so $2 \le X \le p - 2$. $\blacksquare$

**Theorem (agreement).** Let Alice run lines L1 to L3 and get $(x, X)$, and Bob run them and get $(y, Y)$. Then Alice's call DH-SHARED$(x, Y)$ and Bob's call DH-SHARED$(y, X)$ both pass lines L4, L5 and L7, and return the same string, the encoding of $g^{xy} \bmod p$.

*Proof.* By Lemma 2, $Y$ passes lines L4 and L5 in Alice's call, and $X$ passes them in Bob's call. Multiplication in $\mathbb{Z}_p^*$ is commutative and associative, so

$$Y^x = (g^y)^x = g^{yx} = g^{xy} = (g^x)^y = X^y \pmod p.$$

So line L6 gives the same $Z$ in both calls. Since $1 \le x, y \le q - 1$ and $q$ is prime, $q \nmid xy$, so $Z = g^{xy} \ne 1$ and line L7 does not fail. Line L8 encodes $Z$ with a fixed length that depends only on $p$, so the two strings are equal. $\blacksquare$

**Theorem (validated values).** If $Y$ passes lines L4 and L5 and $1 \le x \le q - 1$, then $Z = Y^x$ has order $q$, so line L7 does not fail. The map $x \mapsto Y^x$ is a bijection from $[1, q - 1]$ onto $G \setminus \{1\}$.

*Proof.* Line L5 gives $Y \in G$ by Lemma 1, and line L4 gives $Y \ne 1$, so $Y$ has order $q$ and generates $G$. The map $x \mapsto Y^x$ from $\mathbb{Z}_q$ to $G$ is then a bijection, and it sends 0 to 1, so it sends $[1, q - 1]$ onto $G \setminus \{1\}$. Hence $Z \ne 1$, and by Lemma 1 $Z$ has order $q$. $\blacksquare$

So a uniform $x$ gives a $Z$ that is uniform on $G \setminus \{1\}$ for every value $Y$ that passes validation. In particular, a peer that sends a value of small order, such as $p - 1$, is rejected at line L4 or L5 instead of fixing $Z$ to a small set. $\blacksquare$
