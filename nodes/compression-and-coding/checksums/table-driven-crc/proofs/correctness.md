---
title: One table lookup advances the CRC register by one byte, and the CRC of a concatenation follows from the two CRCs
proves: [correctness, termination]
status: full
---

Notation. $G(x) = x^r + P(x)$ is the generator, $r \ge 8$, and a word of $r$ bits is the polynomial with bit $i$ as the coefficient of $x^i$. The bit-by-bit register of the [cyclic redundancy check](/cyclic-redundancy-check/) maps a register $R$ and an input bit $b$ to $(xR + b x^r) \bmod G$. By that page, after the message $M$ of $k$ bits it holds $(I x^k + M x^r) \bmod G$, where $I$ is init.

**Lemma 1 (the table).** Lines L1 to L4 set $T[v] = v(x)\, x^r \bmod G$ for each byte $v$.

*Proof.* Line L2 sets the register to $v x^{r-8}$, which has degree less than $r$. Each of the 8 steps of line L3 is the bit step with input 0, which maps $R$ to $xR \bmod G$. So after line L3 the register is $v x^{r-8} \cdot x^8 \bmod G = v x^r \bmod G$. $\square$

**Lemma 2 (one byte).** Let the register be $R$ and let the next byte, after the reversal of line L7, be $v$, top bit first. Let $u = \lfloor R / x^{r-8} \rfloor + v$, the top 8 bits of $R$ XOR $v$, and $R_{\mathrm{low}} = R \bmod x^{r-8}$. Then the register after the 8 bit steps is $x^8 R_{\mathrm{low}} + T[u]$, and $\deg(x^8 R_{\mathrm{low}}) < r$.

*Proof.* After 8 bit steps the register is $(x^8 R + v x^r) \bmod G$. Write $R = R_{\mathrm{high}} x^{r-8} + R_{\mathrm{low}}$. Then $x^8 R + v x^r = (R_{\mathrm{high}} + v) x^r + x^8 R_{\mathrm{low}} = u\, x^r + x^8 R_{\mathrm{low}}$. Since $\deg R_{\mathrm{low}} < r - 8$, the term $x^8 R_{\mathrm{low}}$ has degree less than $r$ and is its own remainder. So the remainder is $(u x^r \bmod G) + x^8 R_{\mathrm{low}} = T[u] + x^8 R_{\mathrm{low}}$ by Lemma 1. $\square$

In words of the code, $x^8 R_{\mathrm{low}}$ is `(reg << 8) & mask` and $u$ is `(reg >> (r - 8)) ^ v`. So line L8 does exactly the 8 bit steps of one byte.

**Theorem 1.** `crc_table` returns the same value as the bit-by-bit CRC with the same parameters.

*Proof.* Both start with $R = I$ (line L5). By Lemma 2 and induction on the number of bytes, after each byte the two registers are equal. Lines L9 and L10 are the same final steps as in the bit-by-bit CRC. $\square$

**Termination.** Line L1 runs 256 times with 8 inner steps. Line L8 runs once for each of the $n$ bytes.

**Theorem 2 (the reflected form).** For refin and refout true, `crc_table_reflected` returns the same value. Let $\rho$ reverse $r$ bits. Its table is $T'[w] = \rho(T[\rho_8(w)])$, where $\rho_8$ reverses 8 bits.

*Proof.* Reversal is a bijection of words that maps XOR to XOR, maps `(R << 8) & mask` to `rho(R) >> 8`, and maps the top 8 bits of $R$, reversed, to the low 8 bits of $\rho(R)$. Keep $S = \rho(R)$ in place of $R$. The byte that enters is $v = \rho_8(w)$ for the stored byte $w$, by line L7. Then $u = \mathrm{top}_8(R) \oplus \rho_8(w) = \rho_8(\mathrm{low}_8(S) \oplus w)$, and $\rho(T[u]) = T'[\mathrm{low}_8(S) \oplus w]$. So the image of line L8 under $\rho$ is `S = (S >> 8) ^ T'[(S ^ w) & 0xFF]`, which is line L13. At the start $S = \rho(I)$ (line L11). At the end refout applies $\rho$ to $R$, which is $S$, so line L14 returns $S \oplus X$. The loop of `make_table_reflected` is the image under $\rho$ of the loop of Lemma 1 for the byte $\rho_8(w)$, by Lemma 4 of the page on the bit-by-bit CRC, so it computes $T'$. $\square$

**Theorem 3 (combine).** Let $A$ and $B$ be messages of $a$ and $b$ bits, and let $\mathrm{reg}(\cdot)$ be the register before refout and xorout. Then $\mathrm{reg}(AB) = \big((\mathrm{reg}(A) + I)\, x^{b} + \mathrm{reg}(B)\big) \bmod G$.

*Proof.* The polynomial of $AB$ is $A x^b + B$. So $\mathrm{reg}(AB) = (I x^{a+b} + A x^{b+r} + B x^r) \bmod G$. Also $\mathrm{reg}(A) x^b \equiv I x^{a+b} + A x^{r+b}$ and $\mathrm{reg}(B) \equiv I x^b + B x^r$. The sum of $\mathrm{reg}(A) x^b$, $I x^b$ and $\mathrm{reg}(B)$ is congruent to $I x^{a+b} + A x^{b+r} + B x^r$, because the two terms $I x^b$ cancel. $\square$

The function `crc_combine` gets $\mathrm{reg}(A)$ and $\mathrm{reg}(B)$ from the two CRCs by an XOR with xorout and a reversal when refout is true, both of which are bijections. It computes $x^{8 \cdot \mathrm{len2}} \bmod G$ by square and multiply, then applies Theorem 3 and the final steps. For CRC-32/ISO-HDLC, init and xorout are both all ones. Then the output-domain form is $\mathrm{crc}(AB) = \rho\big(\rho(c_1) \cdot x^{b} \bmod G\big) \oplus c_2$, because $\rho(c_1 \oplus X) \oplus I = \rho(c_1)$, and the two copies of $\rho(X) = I$ that come from $c_2$ and from the final xorout cancel. This is the formula of `crc32_combine` in zlib.
