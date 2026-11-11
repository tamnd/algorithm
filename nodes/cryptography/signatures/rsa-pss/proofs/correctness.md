---
title: Every RSASSA-PSS signature made by the signer verifies
proves: [correctness]
status: full
---

We use the notation of the page. $N = pq$ with distinct primes, $\mathit{modBits}$ is the length of $N$ in binary digits, $k = \lceil \mathit{modBits}/8 \rceil$, $\mathit{emBits} = \mathit{modBits} - 1$, $\mathit{emLen} = \lceil \mathit{emBits}/8 \rceil$, and $t = 8\,\mathit{emLen} - \mathit{emBits}$, so $0 \le t \le 7$. For an octet string $X$, $T(X)$ is $X$ with the $t$ leftmost binary digits set to zero. $T$ is a bitwise AND with a fixed mask, so $T(X \oplus Y) = T(X) \oplus T(Y)$ and $T(T(X)) = T(X)$ for strings of equal length. The signer and the verifier use the same hash, the same MGF1 and the same $\mathit{sLen}$, and $\mathit{emLen} \ge \mathit{hLen} + \mathit{sLen} + 2$, so line L2 does not stop.

**Lemma 1 (the encoded message is below $N$).** Let $EM$ be the output of line L9 and $m = \mathrm{OS2IP}(EM)$. Then $m < 2^{\mathit{emBits}} \le N$.

*Proof.* $EM$ has $\mathit{emLen}$ octets, so $m < 2^{8\,\mathit{emLen}}$. Line L8 sets the $t$ leftmost binary digits of $EM$ to zero, so $m < 2^{8\,\mathit{emLen} - t} = 2^{\mathit{emBits}}$. $N$ has exactly $\mathit{modBits}$ binary digits, so $N \ge 2^{\mathit{modBits} - 1} = 2^{\mathit{emBits}}$. $\square$

**Lemma 2 (the RSA layer).** Line L10 outputs a string $S$ of $k$ octets with $s = \mathrm{OS2IP}(S) < N$, and line L12 computes $s^e \bmod N = m$ and accepts the length of the result.

*Proof.* By Lemma 1, $0 \le m < N$. Line L10 computes $s = m^d \bmod N$ with the Chinese remainder theorem; Lemmas 1 and 2 of the [correctness proof of RSA signatures](/rsa-signature/) show that this is $m^d \bmod N$ and that $(m^d)^e \equiv m \pmod N$. As $s < N < 2^{8k}$, $S = \mathrm{I2OSP}(s, k)$ is defined, so line L11 passes, and line L12 computes $s^e \bmod N = m$ because $m < N$. By Lemma 1, $m < 2^{\mathit{emBits}} \le 2^{8\,\mathit{emLen}}$, so the test of line L12 passes and $\mathrm{I2OSP}(m, \mathit{emLen}) = EM$. $\square$

**Lemma 3 (the encoding is recovered).** EMSA-PSS-VERIFY with input $M$ and the string $EM$ of line L9 returns consistent.

*Proof.* Let $\mathit{mHash}$, $\mathit{salt}$, $M'$, $H$, $DB$ and $\mathit{dbMask} = \mathrm{MGF1}(H, \mathit{emLen} - \mathit{hLen} - 1)$ be the values of lines L1 to L7. Then $EM = T(DB \oplus \mathit{dbMask}) \,\|\, H \,\|\, \mathtt{bc}$.

- Line L13: the last octet of $EM$ is $\mathtt{bc}$ and the length test is the one of line L2, so the verifier continues.
- Line L14: the verifier takes the first $\mathit{emLen} - \mathit{hLen} - 1$ octets as $\mathit{maskedDB} = T(DB \oplus \mathit{dbMask})$ and the next $\mathit{hLen}$ octets as $H$. The $t$ leftmost binary digits of $\mathit{maskedDB}$ are zero because of $T$, so the test passes.
- Line L15: the verifier computes $\mathrm{MGF1}(H, \cdot)$ from the same $H$, so it gets the same $\mathit{dbMask}$, and then $T(\mathit{maskedDB} \oplus \mathit{dbMask}) = T(DB \oplus \mathit{dbMask}) \oplus T(\mathit{dbMask}) = T(DB)$. Now $DB = PS \,\|\, \mathtt{01} \,\|\, \mathit{salt}$. If $PS$ is not empty, the first octet of $DB$ is zero. If $PS$ is empty, the first octet is $\mathtt{01}$, whose only nonzero binary digit is the rightmost one, and $t \le 7$ does not reach it. In both cases $T(DB) = DB$, so the verifier recovers $DB$.
- Line L16: the first $\mathit{emLen} - \mathit{hLen} - \mathit{sLen} - 2$ octets of $DB$ are $PS$, which is all zero, and the next octet is $\mathtt{01}$, so the test passes.
- Line L17: the last $\mathit{sLen}$ octets of $DB$ are $\mathit{salt}$. The verifier hashes the same $M$ to the same $\mathit{mHash}$ and forms $M'' = \mathtt{00}^8 \,\|\, \mathit{mHash} \,\|\, \mathit{salt} = M'$, so $H' = \mathrm{Hash}(M') = H$.
- Line L18 compares $H$ with $H'$, which are equal, and returns consistent. $\square$

**Theorem (correctness).** For every message $M$ and every salt of $\mathit{sLen}$ octets, PSS-VERIFY$((N, e), M, \mathrm{PSS\text{-}SIGN}(sk, M))$ returns valid.

*Proof.* By Lemma 2, the verifier passes lines L11 and L12 and obtains the string $EM$ that the signer encoded. By Lemma 3, EMSA-PSS-VERIFY returns consistent on it, so the verifier returns valid. The argument does not use the value of the salt, so it holds for a fresh random salt, a fixed salt and the empty salt. $\blacksquare$

**Why $\mathit{emBits} = \mathit{modBits} - 1$.** If the encoded message had $\mathit{modBits}$ binary digits, it could be $N$ or more, and RSA would return $m \bmod N$ instead of $m$. One binary digit less makes Lemma 1 hold for every $N$ of that length. When $\mathit{modBits} \equiv 1 \pmod 8$, as for the 1025-bit key of Example 2 in the test vectors, $\mathit{emLen} = k - 1$; line L12 then requires the leading octet of the $k$-octet value to be zero.
