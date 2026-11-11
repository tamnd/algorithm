---
title: Cramer-Shoup decryption accepts honest ciphertexts and returns the message
proves: [correctness]
status: full
---

**Setting.** Let $p$ be a prime and let $G \subseteq \mathbb{Z}_p^*$ be a subgroup of prime order $q$, with elements $g_1, g_2 \in G$. Every element $a \in G$ satisfies $a^q \equiv 1 \pmod p$, so exponents of elements of $G$ may be reduced modulo $q$. The private key is $x_1, x_2, y_1, y_2, z \in \mathbb{Z}_q$ (line L1), and the public key is $c = g_1^{x_1} g_2^{x_2}$, $d = g_1^{y_1} g_2^{y_2}$, $h = g_1^{z}$ (line L2). $H$ is any function from triples of elements of $G$ to $\mathbb{Z}_q$.

**Claim.** For every message $m \in G$ and every $r \in \mathbb{Z}_q$, the ciphertext $(u_1, u_2, e, v)$ of lines L4 to L9 passes the tests of lines L10 and L12, and line L13 returns $m$.

*Proof.*

*Step 1: line L10 accepts.* $G$ is a group, so it is closed under products and powers. Then $u_1 = g_1^r$, $u_2 = g_2^r$, $e = h^r m$ and $v = c^r d^{r\alpha}$ are all in $G$, where $\alpha = H(u_1, u_2, e)$ (line L7). Each is reduced modulo $p$ and is a unit, so it lies in $\{1, \ldots, p-1\}$, and the membership test of line L10 holds for all four.

*Step 2: line L12 accepts.* Line L11 computes the same $\alpha$ as line L7, because $H$ is a function and its inputs $u_1, u_2, e$ are the same. Then

$$u_1^{x_1 + y_1 \alpha} \, u_2^{x_2 + y_2 \alpha} = g_1^{r x_1 + r y_1 \alpha} \, g_2^{r x_2 + r y_2 \alpha} = \left(g_1^{x_1} g_2^{x_2}\right)^{r} \left(g_1^{y_1} g_2^{y_2}\right)^{r\alpha} = c^{r} d^{r\alpha} = v,$$

using only that $\mathbb{Z}_p^*$ is commutative. Reducing the exponents $x_1 + y_1\alpha$ and $x_2 + y_2\alpha$ modulo $q$, as the code does, does not change the powers, because $u_1$ and $u_2$ have order dividing $q$. So the test of line L12 holds.

*Step 3: line L13 returns $m$.* Line L13 computes $e \cdot u_1^{\,q - z}$ (with the exponent taken modulo $q$). Now

$$u_1^{\,q - z} = g_1^{r(q - z)} = \left(g_1^{q}\right)^{r} g_1^{-rz} \equiv g_1^{-rz} \pmod p,$$

and $e = h^r m = g_1^{zr} m$. So $e \cdot u_1^{\,q-z} \equiv g_1^{zr} \, g_1^{-rz} \, m = m \pmod p$. Both sides lie in $\{1, \ldots, p-1\}$, so line L13 returns exactly $m$. $\blacksquare$
