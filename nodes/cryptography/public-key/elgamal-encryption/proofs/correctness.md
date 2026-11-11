---
title: ElGamal decryption inverts ElGamal encryption
proves: [correctness]
status: full
---

**Setting.** Let $p$ be a prime and let $g \in \mathbb{Z}_p^*$ have order $q$, so that $g^q \equiv 1 \pmod p$ and $G = \langle g \rangle = \{g^0, g^1, \ldots, g^{q-1}\}$ has $q$ elements. In the main setting $p = 2q + 1$ is a safe prime and $q$ is prime, but the proof uses only that $q$ is the order of $g$. The private key is $x \in \{0, \ldots, q-1\}$ and the public key is $h = g^x \bmod p$ (lines L1 and L2).

**Claim.** For every $m \in G$ and every $r \in \{0, \ldots, q-1\}$, line L8 accepts the output $(c_1, c_2)$ of lines L4 to L7, and line L9 returns $m$.

*Proof.* We use one fact about $G$.

**Fact.** For $a \in \mathbb{Z}_p^*$, $a \in G$ if and only if $a^q \equiv 1 \pmod p$. *Proof of the fact.* If $a = g^k$, then $a^q = (g^q)^k \equiv 1$. Conversely, $\mathbb{Z}_p^*$ is cyclic of order $p - 1$, and $q$ divides $p - 1$ because the order of an element divides the order of the group ([Lagrange's theorem](/lagranges-theorem-group-theory/)). A cyclic group of order $p - 1$ has exactly one subgroup of each order that divides $p - 1$, and that subgroup is the set of solutions of $a^q = 1$, which has exactly $q$ elements. $G$ is a subgroup of order $q$, so $G$ is that set. $\square$

*Step 1: line L8 accepts.* $c_1 = g^r \in G$. Also $h^r = g^{xr} \in G$ and $m \in G$, and $G$ is closed under multiplication, so $c_2 = m h^r \in G$. Both values lie in $\{1, \ldots, p-1\}$ because they are reduced modulo $p$ and are units. By the fact, both pass the test of line L8.

*Step 2: line L9 returns $m$.* Line L9 computes $c_2 \cdot c_1^{\,q - x} \bmod p$. We have $q - x \ge 1$ because $x \le q - 1$. Then

$$c_1^{\,q-x} = g^{r(q - x)} = (g^q)^r \cdot g^{-rx} \equiv g^{-rx} \pmod p,$$

where $g^{-rx}$ denotes the inverse of $g^{rx}$ in $G$. So

$$c_2 \cdot c_1^{\,q-x} \equiv m \cdot g^{xr} \cdot g^{-rx} = m \pmod p.$$

Since $1 \le m \le p - 1$, the reduced value is exactly $m$. $\blacksquare$

**Remarks.**

- The value $c_1^{\,x} = g^{xr} = h^r$ is the Diffie-Hellman value of $h = g^x$ and $c_1 = g^r$. Encryption multiplies $m$ by it and decryption divides by it. This is the whole scheme.
- The claim holds for every $r$, including $r = 0$, where $c = (1, m)$ shows the message in clear. A uniform $r$ takes this value with probability $1/q$, which the security bound absorbs.
- The textbook scheme of Handbook of Applied Cryptography Algorithm 8.18 is the case $q = p - 1$ with $g$ a generator of $\mathbb{Z}_p^*$. The proof above covers it: there $G = \mathbb{Z}_p^*$ and the test of line L8 accepts every unit. Correctness holds in both settings; only security differs (see the page).
- **Exponential ElGamal.** For $m = g^v$ the same proof gives $g^v$ back, and $v$ follows by a discrete logarithm of size at most the bound on $v$. Baby-step giant-step finds it with $O(\sqrt{V})$ multiplications for $0 \le v \le V$.
