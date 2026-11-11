---
title: Honest SIGMA-I parties accept the same session key, each with the other as peer
proves: [correctness]
status: full
---

We use the notation of the page. Party $\hat P$ has signature key pair $(sk_P, pk_P)$, and the directory of each party maps each name to its public key. The building blocks satisfy three correctness properties.

- **(S)** For every key pair and message $m$, VERIFY$(pk, m, \mathrm{SIG}(sk, m))$ succeeds.
- **(E)** For every key $K$, nonce $n$ and string $w$, $D_K(n, E_K(n, w)) = w$.
- **(C)** The encoding $\langle w_1, w_2, w_3 \rangle$ of a triple can be decoded: from $\langle w_1, w_2, w_3 \rangle$ the receiver gets back $w_1$, $w_2$ and $w_3$. In the code each part has a two-byte length prefix.

MAC and KDF are deterministic functions.

**Lemma 1.** If $1 \le x, y \le q - 1$, $X = g^x$ and $Y = g^y$, then $X, Y \in G \setminus \{1\}$ and $X^y = Y^x$.

*Proof.* Powers of $g$ lie in $G$; since $g$ has prime order $q$ and $q \nmid x$, $X \ne 1$, and likewise $Y \ne 1$. $G$ is commutative, so $X^y = g^{xy} = Y^x$. $\blacksquare$

**Theorem.** Suppose $\hat A$ and $\hat B$ are honest and every message arrives unchanged. Then neither party fails, $\hat A$ accepts $K_s$ with peer $\hat B$ at line L7, and $\hat B$ accepts the same $K_s$ with peer $\hat A$ at line L9.

*Proof.* By Lemma 1, $X$ passes the check of line L2 and $Y$ passes the check of line L5. Both parties apply KDF to the same pair $(g^{xy}, s)$ by Lemma 1, so they hold the same $K_e$, $K_m$ and $K_s$.

*Line L6.* $\hat A$ decrypts the third part of $m_2$ with $K_e$. By (E) it gets $\langle \hat B, \sigma_B, \tau_B \rangle$ and by (C) the three values, where $\sigma_B = \mathrm{SIG}_B(\text{"1"}, s, X, Y)$ and $\tau_B = \mathrm{MAC}_{K_m}(\text{"1"}, s, \hat B)$ as made at line L4. $\hat A$ looks up $pk_B$ under the decoded name $\hat B$, and rebuilds the string $(\text{"1"}, s, X, Y)$ from its own $s$ and $X$ and the received $Y$, which is the string that $\hat B$ signed. By (S), the verification succeeds. $\hat A$ computes $\mathrm{MAC}_{K_m}(\text{"1"}, s, \hat B)$ with the same $K_m$ and the same inputs, so it equals $\tau_B$. So $\hat A$ does not fail, sends $m_3$ and accepts $K_s$ with peer $\hat B$.

*Line L8.* In the same way, by (E) and (C), $\hat B$ gets $\hat A$, $\sigma_A = \mathrm{SIG}_A(\text{"0"}, s, Y, X)$ and $\tau_A = \mathrm{MAC}_{K_m}(\text{"0"}, s, \hat A)$. $\hat B$ rebuilds $(\text{"0"}, s, Y, X)$ from its own $s$ and $Y$ and the received $X$; this is the string that $\hat A$ signed, so by (S) the check under $pk_A$ succeeds. The tag check succeeds because $K_m$ and the inputs are the same. So $\hat B$ accepts $K_s$ with peer $\hat A$ at line L9.

Both parties accept the same $K_s$, and each names the other. $\blacksquare$

**Remark (the role of the MAC in the misbinding test).** If an adversary replaces the name in $m_3$ by $\hat E \ne \hat A$, then at line L8 $\hat B$ checks the tag against $\mathrm{MAC}_{K_m}(\text{"0"}, s, \hat E)$. The honest tag is $\mathrm{MAC}_{K_m}(\text{"0"}, s, \hat A)$ on a different input. An adversary who does not know $K_m$ can make the right tag only by forging the MAC. This is the step that the security proof of Canetti and Krawczyk uses; the theorem above covers only honest runs.
