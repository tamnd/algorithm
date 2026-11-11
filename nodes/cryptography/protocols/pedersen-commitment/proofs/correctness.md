---
title: Pedersen commitments open correctly, hide perfectly and bind under discrete log
proves: [correctness]
status: full
---

Let $G$ be a cyclic group of prime order $q$ with generators $g$ and $h$. Since $q$ is prime, every element other than 1 generates $G$, and $g^a = g^b$ if and only if $a \equiv b \pmod q$. Let $t = \log_g h$, which exists because $g$ generates $G$, and $t \ne 0$ because $h \ne 1$. The commitment to $m \in \mathbb{Z}_q$ with randomness $r \in \mathbb{Z}_q$ is $C = g^m h^r$ (line L3), and the opening $(m, r)$ is accepted if $C \in G$ and $C = g^m h^r$ (lines L4 to L6).

**Lemma 1 (correctness).** For every $m, r \in \mathbb{Z}_q$, OPEN$(\mathrm{COMMIT}(m; r), m, r)$ accepts.

*Proof.* $C = g^m h^r$ is a product of elements of $G$, so it is in $G$ and line L5 does not reject. Line L6 computes the same product from the same $m$ and $r$, so the comparison holds. $\square$

**Lemma 2 (perfect hiding).** For every $m \in \mathbb{Z}_q$, if $r$ is uniform in $\mathbb{Z}_q$ then $C = g^m h^r$ is uniform in $G$. So the distribution of $C$ does not depend on $m$.

*Proof.* Write $C = g^{m + t r}$. The map $r \mapsto m + t r \bmod q$ is a bijection of $\mathbb{Z}_q$, because $t$ is invertible mod $q$ ($q$ is prime and $t \not\equiv 0$); its inverse is $u \mapsto (u - m) t^{-1}$. The map $u \mapsto g^u$ is a bijection from $\mathbb{Z}_q$ onto $G$. So $r \mapsto C$ is a bijection from $\mathbb{Z}_q$ onto $G$, and a uniform $r$ gives a uniform $C$. $\square$

The hiding holds against an adversary with unlimited time, and it also holds if the receiver knows $t$: the proof used only that $t \ne 0$.

**Lemma 3 (binding from discrete log).** Let $A$ be an adversary that, on input $(g, h)$, outputs $(C, m, r, m', r')$ with $m \ne m'$ and two accepted openings, with probability $\varepsilon$ and in time $T$. Then there is an algorithm $B$ that computes $\log_g h$ for a uniform $h \in G \setminus \{1\}$ with probability $\varepsilon$ and in time $T$ plus one inversion and two multiplications mod $q$.

*Proof.* $B$ receives $h$, runs $A(g, h)$, and gets $(C, m, r, m', r')$. If both openings are accepted then $g^m h^r = C = g^{m'} h^{r'}$, so $g^{m - m'} = h^{r' - r} = g^{t (r' - r)}$, and $m - m' \equiv t (r' - r) \pmod q$. Since $m \not\equiv m'$, the left side is not 0, so $r' \not\equiv r$, and $B$ outputs $t = (m - m')(r' - r)^{-1} \bmod q$. $B$ succeeds whenever $A$ does. $\square$

The reduction is tight: it runs $A$ once and loses nothing in probability. It needs $h$ to be distributed as in the real scheme. If $h$ is the output of a hash function modelled as a random oracle, or is sampled by a party that does not reveal its randomness and is trusted to forget it, then $h$ is uniform in $G \setminus \{1\}$ up to a negligible error.

**Lemma 4 (homomorphism).** $\mathrm{COMMIT}(m_1; r_1) \cdot \mathrm{COMMIT}(m_2; r_2) = \mathrm{COMMIT}(m_1 + m_2; r_1 + r_2)$, with the sums mod $q$.

*Proof.* $g^{m_1} h^{r_1} g^{m_2} h^{r_2} = g^{m_1 + m_2} h^{r_1 + r_2}$ because $G$ is commutative, and exponents may be reduced mod $q$ because $g^q = h^q = 1$. $\square$

**Lemma 5 (the trapdoor).** A committer who knows $t$ can open $C = g^m h^r$ to every $m'$, with $r' = r + (m - m')t^{-1} \bmod q$.

*Proof.* $g^{m'} h^{r'} = g^{m' + t r + (m - m')} = g^{m + t r} = C$. $\square$

**Vector form.** For $C = h^r \prod_{i=1}^{n} g_i^{m_i}$, Lemmas 1, 2 and 4 hold with the same proofs (the factor $h^r$ alone makes $C$ uniform). For binding, write $g_i = g^{a_i}$ and $h = g^{a_0}$. Two openings give a non-zero vector $(\delta_0, \ldots, \delta_n)$ with $\sum_i a_i \delta_i \equiv 0$, a non-trivial discrete log relation among the generators. Finding such a relation is as hard as computing discrete logs: given $y$, a reduction sets each $g_i = g^{u_i} y^{v_i}$ with uniform $u_i, v_i$, and a relation gives $\sum u_i \delta_i + \log_g y \sum v_i \delta_i \equiv 0$. The values $v_i$ are hidden from the adversary by the uniform $u_i$, so $\sum v_i \delta_i \not\equiv 0$ with probability at least $1 - 1/q$, and then $\log_g y$ follows. $\blacksquare$
