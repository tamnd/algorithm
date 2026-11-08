---
title: A xorshift generator has full period exactly when its matrix has a primitive characteristic polynomial
proves: [correctness]
status: full
---

Fix a word size $w \ge 2$ and shift amounts $1 \le a, b, c < w$. Identify a $w$-bit word with a column vector in $V = \mathrm{GF}(2)^w$, so that XOR is vector addition. Let $L$ and $R$ be the matrices of the left and right shift by one place within $w$ bits. Lines L1 to L3 of XORSHIFT-NEXT compute $x \mapsto T x$ with

$$T = (I + L^c)(I + R^b)(I + L^a),$$

because line L1 replaces $x$ by $x + L^a x$, line L2 by $x + R^b x$ and line L3 by $x + L^c x$, each a linear map, and the masks keep each value in $V$.

**Lemma 1.** $T$ is invertible. Hence $T 0 = 0$, $T$ permutes $V \setminus \{0\}$, and every non-zero seed lies on a cycle: there is a least $\rho \ge 1$ with $T^\rho x = x$, and the sequence $x, T x, T^2 x, \ldots$ is purely periodic with period $\rho$.

*Proof.* $L^w = 0$ because $w$ shifts move every bit out of the word. Let $N = L^a$; then $N^k = 0$ for $k a \ge w$. Over $\mathrm{GF}(2)$, $(I + N)(I + N + N^2 + \cdots + N^{k-1}) = I + N^k = I$ for $k = \lceil w/a \rceil$, so $I + L^a$ is invertible. The same holds for $I + R^b$ and $I + L^c$, and a product of invertible matrices is invertible. A linear map fixes 0, and a bijection of $V$ that fixes 0 permutes $V \setminus \{0\}$. A permutation of a finite set splits it into cycles, so the orbit of each $x$ returns to $x$, and it is purely periodic. $\square$

**Lemma 2.** Let $T$ be an invertible $w \times w$ matrix over $\mathrm{GF}(2)$. Every non-zero $x$ has period $2^w - 1$ under $T$ if and only if $T$ has order $2^w - 1$ in the group of invertible matrices.

*Proof.* If every non-zero $x$ has period $2^w - 1$, then $T^{2^w - 1} x = x$ for every non-zero $x$ and also for $x = 0$, so $T^{2^w - 1} = I$. For $0 < k < 2^w - 1$, $T^k x \ne x$ for any non-zero $x$, so $T^k \ne I$. The order is $2^w - 1$.

Conversely, suppose that $T$ has order $N = 2^w - 1$. Fix a non-zero $x$ with period $\rho$. Then $\rho \le N$, since $T^N x = x$, and the vectors $x, T x, \ldots, T^{\rho - 1} x$ are distinct and non-zero. Consider the set $A = \mathrm{GF}(2)[T] = \{ h(T) : h \text{ a polynomial over } \mathrm{GF}(2) \}$. It is a commutative ring, and a vector space of dimension at most $w$ by the Cayley-Hamilton theorem, so $|A| \le 2^w$. The powers $I, T, \ldots, T^{N - 1}$ are $N = 2^w - 1$ distinct invertible elements of $A$, and $0 \in A$ is not invertible, so $A$ has exactly $2^w$ elements and every non-zero element of $A$ is invertible. Now $T^\rho - I \in A$ and $(T^\rho - I) x = 0$ with $x \ne 0$, so $T^\rho - I$ is not invertible, hence $T^\rho - I = 0$, and $N \mid \rho$. So $\rho = N$. $\square$

**Lemma 3.** Let $T$ be a $w \times w$ matrix over $\mathrm{GF}(2)$ with characteristic polynomial $P$. $T$ has order $2^w - 1$ if and only if $P$ is primitive, that is, $P$ is irreducible of degree $w$ and $z$ has order $2^w - 1$ modulo $P$.

*Proof.* Suppose that $T$ has order $2^w - 1$. The proof of Lemma 2 shows that $A = \mathrm{GF}(2)[T]$ has $2^w$ elements and that every non-zero element is invertible, so $A$ is a field. $A \cong \mathrm{GF}(2)[z] / (\mu)$, where $\mu$ is the minimal polynomial of $T$, so $\mu$ is irreducible and $\deg \mu = w$. Since $\mu$ divides $P$ and both have degree $w$ and are monic, $\mu = P$. The isomorphism maps $T$ to $z$, so $z$ has order $2^w - 1$ modulo $P$, and $P$ is primitive.

Conversely, suppose that $P$ is primitive. Then $P$ is irreducible, so the minimal polynomial $\mu$, a non-constant divisor of $P$, equals $P$. The map $h(z) \mapsto h(T)$ gives an isomorphism of $\mathrm{GF}(2)[z]/(P)$ onto $A$, which sends $z$ to $T$, so $T$ has the same order as $z$ modulo $P$, namely $2^w - 1$. $\square$

**Theorem.** Let $T$ be the matrix of XORSHIFT-NEXT with shift amounts $(a, b, c)$ and word size $w$. Every non-zero seed has period exactly $2^w - 1$, and the sequence visits every non-zero word once per period, if and only if the characteristic polynomial of $T$ is primitive. In that case each output bit sequence $s_i = e^\top T^i x$ satisfies the linear recurrence with characteristic polynomial $P$.

*Proof.* By Lemma 1 each non-zero orbit is a cycle. By Lemmas 2 and 3, all non-zero orbits have length $2^w - 1$ if and only if $P$ is primitive. An orbit of length $2^w - 1$ inside the set $V \setminus \{0\}$ of size $2^w - 1$ is the whole set, so it visits each non-zero word exactly once. Finally, $P(T) = 0$ by the Cayley-Hamilton theorem. If $P(z) = \sum_{j} p_j z^j$, then $\sum_j p_j s_{i + j} = e^\top T^i P(T) x = 0$ for every $i$. $\square$

**Lemma 4 (the test used for the implementation).** Let $x \ne 0$ and $s_i = e^\top T^{i+1} x$ for $i = 0, 1, \ldots, 2w - 1$. If the Berlekamp-Massey algorithm finds that the sequence has linear complexity $w$, with characteristic polynomial $Q$ of degree $w$, and $Q$ is primitive, then the characteristic polynomial $P$ of $T$ equals $Q$, and the generator has full period.

*Proof.* By the theorem's last part, the infinite sequence $(s_i)$ satisfies the recurrence of $P$, so its linear complexity is at most $w$. A sequence of linear complexity at most $w$ is determined by any $2w$ consecutive terms, and the Berlekamp-Massey algorithm returns its unique shortest recurrence from them. So $Q$ is the minimal polynomial of the whole sequence, and $Q$ divides every polynomial that annihilates it, in particular $P$. Both are monic of degree $w$, so $P = Q$, which is primitive, and the theorem applies. $\square$

The primitivity of a polynomial $Q$ of degree $w$ over $\mathrm{GF}(2)$ is decided by the criterion: $z^{2^w - 1} \equiv 1 \pmod Q$ and $z^{(2^w - 1)/q} \not\equiv 1 \pmod Q$ for each prime $q$ dividing $2^w - 1$. Write $N = 2^w - 1$. If these hold, $z$ is invertible modulo $Q$, since $z \cdot z^{N - 1} \equiv 1$, and its order $d$ divides $N$. If $d < N$, some prime $q$ divides $N / d$, so $d \mid N / q$ and $z^{N/q} \equiv 1$, a contradiction. So $z$ has order exactly $N$. Then the powers of $z$ give $N$ distinct non-zero residues, so every non-zero residue is a power of $z$, hence invertible, and $\mathrm{GF}(2)[z]/(Q)$ is a field, so $Q$ is irreducible. For $(13, 17, 5)$ with $w = 32$, $(13, 7, 17)$ with $w = 64$, and xor128 with $n = 128$, the implementation's tests carry out this check in exact integer arithmetic. $\blacksquare$
