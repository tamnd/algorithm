---
title: The Schnorr identification protocol is complete, special sound and honest-verifier zero knowledge
proves: [correctness]
status: full
---

Let $G$ be a cyclic group of prime order $q$ with generator $g$, so that $g^a = g^b$ if and only if $a \equiv b \pmod q$. Let $x \in [1, q-1]$, $y = g^x$, and let the challenge set be $C = [0, 2^t - 1]$ with $2^t \le q$. Line numbers refer to the pseudocode on the page.

**Lemma 1 (completeness).** If the prover follows lines L2 and L4, the verifier accepts at lines L5 and L6.

*Proof.* Line L2 gives $a = g^k \in G$, and $y = g^x \in G$, so the membership checks of line L5 pass. Line L4 gives $z \in [0, q-1]$, and the honest verifier picked $c \in C$ at line L3. By line L4 there is an integer $j$ with $z = k + cx - jq$. Then
$$g^z = g^k \cdot (g^x)^c \cdot (g^q)^{-j} = a \cdot y^c,$$
because $g^q = 1$. So line L6 accepts. $\square$

**Lemma 2 (special soundness).** If $(a, c_1, z_1)$ and $(a, c_2, z_2)$ are both accepted, with $c_1 \ne c_2$ in $C$, then $x = (z_1 - z_2)(c_1 - c_2)^{-1} \bmod q$.

*Proof.* Both checks give $g^{z_1} = a y^{c_1}$ and $g^{z_2} = a y^{c_2}$. Divide: $g^{z_1 - z_2} = y^{c_1 - c_2} = g^{x(c_1 - c_2)}$. So $z_1 - z_2 \equiv x (c_1 - c_2) \pmod q$. Since $0 < |c_1 - c_2| < 2^t \le q$ and $q$ is prime, $c_1 - c_2$ is invertible mod $q$, and the formula follows. $\square$

**Corollary 3 (knowledge error $2^{-t}$).** By Lemma 2 and the theorem on [proofs of knowledge](/proof-of-knowledge/) from special soundness, a prover that is accepted with probability $\varepsilon > 2^{-t}$ lets a rewinding extractor compute $x$ in expected time polynomial in $1/(\varepsilon - 2^{-t})$. The bound is tight: the prover that picks $c^* \in C$ and $z$ in advance and sends $a = g^z y^{-c^*}$ is accepted exactly when $c = c^*$, with probability $2^{-t}$.

*Proof of the tightness claim.* If $c = c^*$, then $a y^c = g^z y^{-c^*} y^{c^*} = g^z$, so line L6 accepts. If $c \ne c^*$ and line L6 also accepted, Lemma 2 applied to the two accepting transcripts $(a, c^*, z)$ and $(a, c, z)$ would give $x = 0$, but $x \ne 0$. So the prover is accepted for exactly one of the $2^t$ challenges. $\square$

**Lemma 4 (honest-verifier zero knowledge).** For each fixed $c \in C$, the real transcript $(g^k, c, k + cx \bmod q)$ with $k$ uniform in $\mathbb{Z}_q$ and the simulated transcript $(g^z y^{-c}, c, z)$ with $z$ uniform in $\mathbb{Z}_q$ have the same distribution.

*Proof.* In the real transcript, $k \mapsto z = k + cx \bmod q$ is a bijection of $\mathbb{Z}_q$, so $z$ is uniform. In both transcripts $a$ is a function of $z$: in the real one $a = g^k = g^{z - cx} = g^z y^{-c}$, and in the simulated one $a = g^z y^{-c}$ by definition. So both are the image of a uniform $z$ under the same map $z \mapsto (g^z y^{-c}, c, z)$. Since the honest verifier's $c$ is independent of $a$, averaging over $c$ also gives equal distributions. $\blacksquare$
