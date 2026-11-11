---
title: A Hill key must have a determinant coprime to 26, decryption inverts encryption, and the known plaintext attack is exact
proves: [correctness]
status: full
---

All matrices have entries in $\mathbb{Z}_{26}$, and $n \ge 1$. For a square matrix $K$, $\operatorname{adj}(K)$ is the transpose of its matrix of cofactors.

**Claim 1.** The map $p \mapsto Kp$ on $\mathbb{Z}_{26}^n$ is a bijection if and only if $\gcd(\det K, 26) = 1$. In that case $K^{-1} = (\det K)^{-1} \operatorname{adj}(K)$ modulo 26.

*Proof.*

1. The identity $K \operatorname{adj}(K) = \operatorname{adj}(K) K = \det(K) I$ is a polynomial identity in the entries of $K$ with integer coefficients, so it holds over every commutative ring, and in particular modulo 26.
2. If $d = \det K$ is coprime to 26, then $d$ has an inverse $d^{-1}$ modulo 26, and step 1 gives $K \cdot d^{-1}\operatorname{adj}(K) = d^{-1} d I = I$, and the same on the other side. So $p \mapsto Kp$ has the inverse $c \mapsto d^{-1}\operatorname{adj}(K) c$ and is a bijection.
3. Conversely, let $\gcd(d, 26) > 1$. Then a prime $q \in \{2, 13\}$ divides $d$. Reduce $K$ modulo $q$: its determinant is $d \bmod q = 0$, so $K$ is singular over the field $\mathbb{Z}_q$, and there is a vector $v \in \{0, \ldots, q - 1\}^n$, not all zero, with $Kv \equiv 0 \pmod q$. Let $x = (26/q) v$. Since some entry of $v$ lies in $\{1, \ldots, q - 1\}$, that entry of $x$ lies in $\{26/q, \ldots, 26 - 26/q\}$, so $x \not\equiv 0 \pmod{26}$. And $Kx = (26/q)(Kv)$, where each entry of $Kv$ is a multiple of $q$, so $Kx \equiv 0 \pmod{26}$. Thus $Kx = K0$ with $x \ne 0$, and the map is not injective. $\square$

**Claim 2.** If $K$ is a key, HILL-ENCRYPT with $K^{-1}$ applied to the output of HILL-ENCRYPT with $K$ returns the padded plaintext.

*Proof.* Line L1 pads to a multiple of $n$, so lines L2 to L4 map each block $p$ to $Kp$. The output has a multiple of $n$ letters, so the second run pads nothing and maps each block $Kp$ to $K^{-1} K p = p$, by Claim 1. $\square$

**Claim 3 (the number of keys).** For a prime $q$, the number of invertible $n \times n$ matrices over $\mathbb{Z}_q$ is $\prod_{i=0}^{n-1}(q^n - q^i)$, and the number of keys modulo 26 is the product of these numbers for $q = 2$ and $q = 13$. For $n = 2$ it is $6 \cdot 26{,}208 = 157{,}248$.

*Proof.* Over a field, a matrix is invertible exactly when its columns are linearly independent. The first column can be any of the $q^n - 1$ nonzero vectors. If the first $i$ columns are independent, they span $q^i$ vectors, and the next column can be any of the other $q^n - q^i$ vectors. This gives the product. By the Chinese remainder theorem, the reduction $K \mapsto (K \bmod 2, K \bmod 13)$ is a bijection from $\mathbb{Z}_{26}^{n \times n}$ to $\mathbb{Z}_2^{n \times n} \times \mathbb{Z}_{13}^{n \times n}$, and $\det K$ is coprime to 26 exactly when it is nonzero modulo 2 and modulo 13, that is, when both reductions are invertible. So the count is the product. For $n = 2$: $(4 - 1)(4 - 2) = 6$ and $(169 - 1)(169 - 13) = 168 \cdot 156 = 26{,}208$. $\square$

**Claim 4 (the known plaintext attack).** Let $K$ be a key, let $P$ be an $n \times m$ matrix of plaintext blocks, and let $C = KP$. If the columns of $P$ span $(\mathbb{Z}_q)^n$ for both $q = 2$ and $q = 13$, then $K$ is the only matrix with $K'P \equiv C \pmod{26}$. Otherwise, and if $n \ge 2$, at least one other key $K' \ne K$ satisfies $K'P \equiv C$. HILL-KPA returns $K$ in the first case and "not unique" otherwise. In particular, if $m = n$ and $\gcd(\det P, 26) = 1$, then $K = C P^{-1}$.

*Proof.*

1. Let $K'P \equiv C$ and $\Delta = K' - K$, so $\Delta P \equiv 0 \pmod{26}$, and hence modulo $q$ for $q = 2, 13$. Each row $r$ of $\Delta \bmod q$ satisfies $r \cdot w = 0$ for each column $w$ of $P$. If the columns span $(\mathbb{Z}_q)^n$, then $r$ is orthogonal to every vector, including the unit vectors, so $r = 0$. If this holds for both $q$, then $\Delta \equiv 0$ modulo 2 and modulo 13, hence modulo 26, and $K' = K$.
2. Let the columns of $P$ not span $(\mathbb{Z}_q)^n$ for some $q \in \{2, 13\}$, and let $n \ge 2$. Their span is a proper subspace, so over the field $\mathbb{Z}_q$ some $u \ne 0$ satisfies $u^T w = 0$ for each column $w$ of $P$. Let $s = 26/q$, which is a unit modulo $q$. For a vector $a \in \mathbb{Z}_q^n$, put $K' = K + s\, a u^T$ (with $a$ and $u$ lifted to $\{0, \ldots, q - 1\}$). Then:
    - $K'P = C + s\, a (u^T P)$, and each entry of $u^T P$ is a multiple of $q$, so $K'P \equiv C \pmod{26}$.
    - If $a \ne 0$, some entry $a_i u_j$ is nonzero modulo $q$, so $s\, a_i u_j \not\equiv 0 \pmod{26}$ and $K' \ne K$.
    - Modulo $s$, $K' \equiv K$, which is invertible. Modulo $q$, the matrix determinant lemma gives $\det K' \equiv \det K \cdot (1 + s\, v^T a)$ with $v^T = u^T K^{-1} \ne 0$, because $K$ is invertible modulo $q$.
   So $K'$ is a key other than $K$ as soon as $a \ne 0$ and $v^T a \not\equiv -s^{-1} \pmod q$. Since $v \ne 0$, the vectors $a$ with $v^T a \not\equiv -s^{-1}$ number $q^n - q^{n-1} = q^{n-1}(q - 1)$, and they include $a = 0$. So such an $a \ne 0$ exists when $q^{n-1}(q - 1) \ge 2$, which holds for $n \ge 2$. (For $n = 1$ and $q = 2$ the bound fails: the second matrix $K + 13$ is even, so it is not a key. Then the data fix the key but not the matrix, and HILL-KPA answers "not unique", which is cautious but not wrong about the matrix.)
3. Lines L7 to L9 run Gaussian elimination over the field $\mathbb{Z}_q$ on the equations $P^T (K_q)^T = C^T$. Elimination finds a pivot in each of the $n$ columns exactly when $P^T$ has rank $n$, that is, when the columns of $P$ span $(\mathbb{Z}_q)^n$; then the reduced system gives the unique solution $K_q = K \bmod q$ by step 1. Otherwise line L9 reports that the solution is not unique. Line L10 joins $K_2$ and $K_{13}$ by the Chinese remainder theorem: the entry $x = k_{13} + 13 \cdot ((k_2 - k_{13}) \bmod 2)$ satisfies $x \equiv k_{13} \pmod{13}$ and $x \equiv k_{13} + (k_2 - k_{13}) = k_2 \pmod 2$, because $13$ is odd. So the result is $K$.
3. Lines L7 to L9 run Gaussian elimination over the field $\mathbb{Z}_q$ on the equations $P^T (K_q)^T = C^T$. Elimination finds a pivot in each of the $n$ columns exactly when $P^T$ has rank $n$, that is, when the columns of $P$ span $(\mathbb{Z}_q)^n$; then the reduced system gives the unique solution $K_q = K \bmod q$ by step 1. Otherwise line L9 reports that the solution is not unique. Line L10 joins $K_2$ and $K_{13}$ by the Chinese remainder theorem: the entry $x = k_{13} + 13 \cdot ((k_2 - k_{13}) \bmod 2)$ satisfies $x \equiv k_{13} \pmod{13}$ and $x \equiv k_{13} + (k_2 - k_{13}) = k_2 \pmod 2$, because $13$ is odd. So the result is $K$.
4. If $m = n$ and $\det P$ is a unit, then $P$ is invertible modulo 26 by Claim 1, and $C P^{-1} = K P P^{-1} = K$. Its columns span both $(\mathbb{Z}_q)^n$, since $P$ is invertible modulo each $q$. $\square$

Claim 1 proves that the keys are exactly the matrices whose determinant is coprime to 26, Claim 2 that decryption inverts encryption, Claim 3 the key count, and Claim 4 that the known plaintext attack returns the key exactly when the data determine the matrix. $\blacksquare$
