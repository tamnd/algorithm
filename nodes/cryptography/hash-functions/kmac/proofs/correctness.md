---
title: The KMAC input encoding is injective, and KMAC never shares an input with SHAKE or SHA-3
proves: [correctness]
status: full
---

We work with byte strings. For a byte string $Z$, $|Z|$ is its length in bytes. Fix the rate $r \in \{168, 136\}$. Assume every integer that is encoded is less than $2^{2040}$, so that its byte count $n$ fits in one byte, $1 \le n \le 255$, as SP 800-185, Section 2.3.1, requires.

**Lemma 1 (left_encode is prefix-free).** If $\mathrm{left\_encode}(x) \| U = \mathrm{left\_encode}(x') \| U'$ for integers $x, x'$ and byte strings $U, U'$, then $x = x'$ and $U = U'$.

*Proof.* The first byte of $\mathrm{left\_encode}(x)$ is its byte count $n$, and the first byte of the other side is $n'$. The two strings are equal, so $n = n'$. The next $n$ bytes are the big-endian form of $x$ and of $x'$, so $x = x'$. Removing the first $n + 1$ bytes from both sides gives $U = U'$. $\square$

**Lemma 2 (encode_string is prefix-free).** If $\mathrm{encode\_string}(S) \| U = \mathrm{encode\_string}(S') \| U'$, then $S = S'$ and $U = U'$.

*Proof.* By Lemma 1, the bit lengths are equal, $8|S| = 8|S'|$, and the rest is $S \| U = S' \| U'$. Since $|S| = |S'|$, the first $|S|$ bytes give $S = S'$, and the rest gives $U = U'$. $\square$

**Lemma 3 (right_encode can be read from the end).** If $U \| \mathrm{right\_encode}(x) = U' \| \mathrm{right\_encode}(x')$, then $x = x'$ and $U = U'$.

*Proof.* The last byte of each side is the byte count, so $n = n'$. The $n$ bytes before it are the big-endian form of $x$ and $x'$, so $x = x'$. What remains in front is $U = U'$. $\square$

**Lemma 4 (bytepad can be removed).** Let $Y = \mathrm{bytepad}(\mathrm{encode\_string}(K), r)$. Then $|Y|$ is a multiple of $r$, and $K$ and $|Y|$ can be read from any string that starts with $Y$.

*Proof.* By definition $Y = \mathrm{left\_encode}(r) \| \mathrm{encode\_string}(K) \| 0^{j}$, with $j$ the least number of zero bytes that makes $|Y|$ a multiple of $r$. By Lemma 1 the reader skips $\mathrm{left\_encode}(r)$. By Lemma 2 it reads $K$ from $\mathrm{encode\_string}(K)$, and then it knows $p = |\mathrm{left\_encode}(r)| + |\mathrm{encode\_string}(K)|$. The value $j$ is $(-p) \bmod r$, a function of $p$, so $|Y| = p + j$ is known too. $\square$

**Theorem 1 (injectivity).** For byte strings $K, X, S$ and integers $L$, let
$$E(K, X, L, S) = \mathrm{bytepad}(\mathrm{encode\_string}(\text{KMAC}) \| \mathrm{encode\_string}(S), r) \,\|\, \mathrm{bytepad}(\mathrm{encode\_string}(K), r) \,\|\, X \,\|\, \mathrm{right\_encode}(L).$$
If $E(K, X, L, S) = E(K', X', L', S')$, then $(K, X, L, S) = (K', X', L', S')$.

*Proof.* Read both sides from the left. After $\mathrm{left\_encode}(r)$, Lemma 2 applied twice gives the name `KMAC` on both sides and then $S = S'$. The first bytepad block has length $p_1 + j_1$, where $p_1$ is now known on both sides and equal, so the rest after the first bytepad is equal on both sides. Lemma 4 applied to this rest gives $K = K'$ and the length of the second bytepad, equal on both sides. What remains is $X \| \mathrm{right\_encode}(L) = X' \| \mathrm{right\_encode}(L')$, and Lemma 3 gives $L = L'$ and $X = X'$. $\blacksquare$

The same proof works for KMACXOF, with $L$ replaced by 0, and the output length then is not part of the input.

**Theorem 2 (domain separation).** Let $M$ be any byte string. The sponge input of KMAC is $E \| d$ followed by pad10*1, where the domain bits are $d = 00$. For SHA-3 the input is $M \| 01$ followed by pad10*1, and for SHAKE it is $M \| 1111$ followed by pad10*1. No KMAC input equals a SHA-3 or a SHAKE input with the same rate.

*Proof.* The padding pad10*1 appends a 1 bit, the least number of 0 bits, and a final 1 bit. It can be removed from the end without ambiguity: drop the last bit, then all 0 bits before it, then the 1 bit before those. So two equal padded inputs come from equal unpadded bit strings. The unpadded KMAC input $E \| 00$ has $8|E| + 2$ bits. Suppose it equals the SHA-3 string $M \| 01$, of $8|M| + 2$ bits. Then $|E| = |M|$, and the last two bits are $00$ on one side and $01$ on the other, a contradiction. The SHAKE string $M \| 1111$ has $8|M| + 4$ bits, and $8|E| + 2 \ne 8|M| + 4$ because the two numbers differ modulo 8. So no KMAC input equals a SHA-3 or SHAKE input. In the byte form of the code, the byte after the message is `04` for cSHAKE, `06` for SHA-3 and `1f` for SHAKE (FIPS 202 bit order, domain bits plus the first padding bit). $\blacksquare$

**A note on cSHAKE with other names.** A cSHAKE input with name $N \ne$ `KMAC` and the same $S$ differs from the KMAC input in the encoded name, which by Lemma 2 is read at the same place in both, so the inputs differ.
