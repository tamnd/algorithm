---
title: EME-OAEP decoding inverts the encoding, and the parse of the data block is unique
proves: [correctness]
status: full
---

Let $N$ be an RSA modulus with $k = \lceil \log_{256} N \rceil$ octets, let $e$ and $d$ be the exponents, so that $\mathrm{RSADP}(\mathrm{RSAEP}(m)) = m$ for every $0 \le m < N$, and let $\mathrm{Hash}$ be a function with an output of $h$ octets, with $k \ge 2h + 2$. Write $\oplus$ for the octet by octet exclusive or of two strings of equal length, $\varepsilon$ for the empty string and $\mathrm{MGF1}$ for the function of lines L1 to L3. All strings are octet strings, indexed from 0.

## Part 1: the mask function is well defined

**Lemma 1.** For every seed $s$ and every $0 \le \ell \le 2^{32} h$, $\mathrm{MGF1}(s, \ell)$ has exactly $\ell$ octets, and it is a function of $s$ and $\ell$ alone. Moreover, for $\ell \le \ell'$ the string $\mathrm{MGF1}(s, \ell)$ is the prefix of $\mathrm{MGF1}(s, \ell')$ of length $\ell$.

*Proof.* Line L2 appends $\lceil \ell/h \rceil$ blocks of $h$ octets, so $T$ has at least $\ell$ octets, and line L3 cuts it to $\ell$. The $i$-th block is $\mathrm{Hash}(s \Vert \mathrm{I2OSP}(i, 4))$, which depends on $s$ and $i$ only, so the blocks for the longer output extend the blocks for the shorter one, and both outputs are prefixes of the same infinite string. $\square$

## Part 2: the encoding

**Lemma 2 (the shape of the encoded message).** Let $M$ have $\mathrm{mLen} \le k - 2h - 2$ octets and let $\mathrm{EM}$ be the output of line L10 for a seed of $h$ octets. Then $\mathrm{EM}$ has $k$ octets, its first octet is $\texttt{0x00}$, and $m = \mathrm{OS2IP}(\mathrm{EM}) < 256^{k-1} \le N$.

*Proof.* On line L5 the string $\mathrm{PS}$ has $k - \mathrm{mLen} - 2h - 2 \ge 0$ octets, so line L6 gives
$$|\mathrm{DB}| = h + (k - \mathrm{mLen} - 2h - 2) + 1 + \mathrm{mLen} = k - h - 1 .$$
The mask on line L8 has the same length by Lemma 1, so $|\mathrm{maskedDB}| = k - h - 1$, and $|\mathrm{maskedSeed}| = h$ on line L9. Line L10 therefore returns $1 + h + (k - h - 1) = k$ octets, with a leading $\texttt{0x00}$. A $k$ octet string with a zero leading octet is an integer below $256^{k-1}$, and $256^{k-1} \le N$ by the definition of $k$. $\square$

**Lemma 3 (the parse of the data block is unique).** Let $\mathrm{DB} = \mathrm{lHash} \Vert \mathrm{PS} \Vert \texttt{0x01} \Vert M$ as on line L6, with $\mathrm{PS}$ a run of zero octets. Then, given $\mathrm{DB}$ and $h$, the three parts $\mathrm{lHash}$, $\mathrm{PS}$ and $M$ are determined.

*Proof.* The first $h$ octets are $\mathrm{lHash}$. In the rest, every octet of $\mathrm{PS}$ is zero and the octet after $\mathrm{PS}$ is $\texttt{0x01}$, so the least index of a nonzero octet in the rest is the index of that $\texttt{0x01}$ octet. The octets after it are $M$. The rest is nonempty, because it holds at least the $\texttt{0x01}$ octet. $\square$

Note that the first octet of $M$ may be zero; the parse looks for the first nonzero octet, not the first zero octet, which is the difference from the v1.5 encoding.

**Theorem 4 (the encoding and the decoding are inverse).** For every $M$ with $\mathrm{mLen} \le k - 2h - 2$, every label $L$ and every seed of $h$ octets, the decoding of lines L13 to L18, applied to the encoding of lines L4 to L10 with the same $L$ and $\mathrm{Hash}$, returns $M$.

*Proof.* Let $\mathrm{EM} = \texttt{0x00} \Vert \mathrm{maskedSeed} \Vert \mathrm{maskedDB}$ be the output of line L10. Line L13 splits $\mathrm{EM}$ at the same two places, because the lengths $1$, $h$ and $k - h - 1$ are fixed, so it reads $Y = \texttt{0x00}$ and the same two strings. Line L14 computes
$$\mathrm{maskedSeed} \oplus \mathrm{MGF1}(\mathrm{maskedDB}, h) = \bigl(\mathrm{seed} \oplus \mathrm{MGF1}(\mathrm{maskedDB}, h)\bigr) \oplus \mathrm{MGF1}(\mathrm{maskedDB}, h) = \mathrm{seed} ,$$
by line L9 and because $x \oplus y \oplus y = x$. The mask is the same string on both sides, by Lemma 1, since the seed of the mask is $\mathrm{maskedDB}$, which both sides hold. Line L15 then computes
$$\mathrm{maskedDB} \oplus \mathrm{MGF1}(\mathrm{seed}, k - h - 1) = \mathrm{DB} ,$$
by line L8 and the same cancellation, now with the seed recovered on line L14. Line L16 splits off the first $h$ octets of $\mathrm{DB}$, which are $\mathrm{Hash}(L)$ by line L5, so the label test passes, and $Y = \texttt{0x00}$, so that test passes too. By Lemma 3 the rest is a run of zero octets, then $\texttt{0x01}$, then $M$, so the test of line L17 passes and line L18 returns $M$. $\square$

**Theorem 5 (correctness of the scheme).** With the same hypotheses, $\mathrm{RSAES\text{-}OAEP\text{-}DECRYPT}$ applied to $\mathrm{RSAES\text{-}OAEP\text{-}ENCRYPT}((N, e), M, L)$ returns $M$.

*Proof.* Line L11 gives $C = \mathrm{I2OSP}(m^e \bmod N, k)$ with $m = \mathrm{OS2IP}(\mathrm{EM}) < N$ by Lemma 2, so $|C| = k$ and line L12 passes, since $k \ge 2h + 2$. Line L13 recovers $\mathrm{RSADP}(\mathrm{OS2IP}(C)) = m$ and then $\mathrm{I2OSP}(m, k) = \mathrm{EM}$, because $\mathrm{I2OSP}$ and $\mathrm{OS2IP}$ are inverse on $[0, 256^k)$ and $\mathrm{EM}$ has $k$ octets. Theorem 4 finishes the proof. $\square$

## Part 3: what this proof does not say

Correctness is the easy half. The security claim of the page, that RSA-OAEP is IND-CCA2 in the random oracle model under the RSA assumption, is a different statement with a different proof:

- Bellare and Rogaway (1994) proved a weaker statement than they claimed. Shoup (2001) showed that their plaintext awareness argument gives security against a non adaptive chosen ciphertext attack only, and that relative to an oracle there is a trapdoor permutation for which OAEP is not IND-CCA2. So no proof of this kind can work from one-wayness alone.
- Fujisaki, Okamoto, Pointcheval and Stern (2001) proved IND-CCA2 in the random oracle model from the *partial domain* one-wayness of the permutation, and then proved that partial domain one-wayness of RSA follows from the RSA assumption. The second step squares the advantage, so the reduction is loose: an adversary with advantage $\varepsilon$ in time $t$ yields an RSA inverter with success of order $\varepsilon^2/4$ in time of order $2t + q_H(q_H + 2q_G) \cdot O(b^3)$, where $q_G$ and $q_H$ count the queries to the two oracles.
- Both results live in the random oracle model, so they say nothing about a concrete MGF1. In the standard model only an IND-CPA result is known, under a lossiness assumption on RSA (Kiltz, O'Neill and Smith, 2010).

The correctness proof above also says nothing about the implementation requirement of line L17: the three failures must be told apart by nobody, which is a statement about the program, not about the mathematics. Manger's attack of 2001 is the price of breaking it.
