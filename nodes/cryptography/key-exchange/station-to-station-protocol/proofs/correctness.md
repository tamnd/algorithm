---
title: Honest STS parties accept the same key, each with the other as peer
proves: [correctness]
status: full
---

We use the notation of the page: $G = \langle g \rangle$ has prime order $q$, $(sk_A, pk_A)$ and $(sk_B, pk_B)$ are the signature key pairs, and the directory of each party maps $\hat A$ to $pk_A$ and $\hat B$ to $pk_B$. We assume two properties of the building blocks.

- **(S) Signature correctness.** For every key pair $(sk, pk)$ and message $m$, VERIFY$(pk, m, \mathrm{SIG}(sk, m))$ succeeds.
- **(E) Encryption correctness.** For every key $K$, nonce $n$ and string $s$, $D_K(n, E_K(n, s)) = s$.

For the code, (E) holds because $E_K$ XORs $s$ with a key stream that depends only on $K$ and $n$, and XOR with the same stream twice is the identity. (S) holds for Schnorr signatures: if $s = k + e \cdot sk \bmod q$ and $pk = g^{sk}$, then $g^s \cdot pk^{-e} = g^k$, so the check recomputes $e = H(g^k, m)$.

**Lemma 1 (honest values pass the checks).** If $1 \le x \le q - 1$, then $X = g^x$ lies in $G$ and $X \ne 1$.

*Proof.* $X$ is a power of $g$, so $X \in G$. The order of $g$ is $q$ and $q \nmid x$, so $X \ne 1$. $\blacksquare$

**Lemma 2 (equal keys).** If $\hat A$ uses $x$ and receives $Y = g^y$, and $\hat B$ uses $y$ and receives $X = g^x$, then the two keys of lines L3 and L5 are equal.

*Proof.* $G$ is commutative, so $X^y = (g^x)^y = g^{xy} = (g^y)^x = Y^x$. KDF is a function, so $\mathrm{KDF}(X^y) = \mathrm{KDF}(Y^x)$. $\blacksquare$

**Theorem.** Suppose both parties are honest and every message is delivered unchanged. Then neither party fails, $\hat A$ accepts at line L7 with key $K$ and peer $\hat B$, and $\hat B$ accepts at line L9 with the same key $K$ and peer $\hat A$.

*Proof.* At line L2, $\hat A$ is in $\hat B$'s directory, and $X \in G$ with $X \ne 1$ by Lemma 1, so $\hat B$ does not fail. At line L5, $\hat B$ is in $\hat A$'s directory and $Y \in G$ by Lemma 1, so $\hat A$ does not fail. By Lemma 2 both parties hold the same $K$.

At line L6, $\hat A$ computes $D_K(c_B)$. By (E), with the same $K$ and the nonce of the second message, this is $\mathrm{SIG}_B(Y, X)$, the signature that $\hat B$ made at line L4 on the string $(Y, X)$. $\hat A$ verifies it under $pk_B$ on the same string $(Y, X)$, since $\hat A$ received $Y$ and sent $X$. By (S) the check succeeds, so $\hat A$ sends $c_A$ and accepts $K$ with peer $\hat B$ at line L7.

At line L8, by (E) with the nonce of the third message, $D_K(c_A) = \mathrm{SIG}_A(X, Y)$. $\hat B$ verifies it under $pk_A$ on $(X, Y)$, the string that $\hat A$ signed, since $\hat B$ received $X$ and sent $Y$. By (S) the check succeeds, and $\hat B$ accepts $K$ with peer $\hat A$ at line L9.

So both parties accept, with the same key, and each names the other as its peer. $\blacksquare$

**Remark.** The theorem is about honest runs. It does not claim that the peer named at line L9 is right when an adversary changes the claimed identity: the unknown key-share attack on the page shows that it can be wrong if two names share a public key.
