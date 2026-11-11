---
title: The eight tables advance the CRC register by eight bytes in one step
proves: [correctness, termination]
status: full
---

Notation. $G(x) = x^{32} + P(x)$ is the generator, and $\rho$ reverses 32 bits. We argue in the normal domain, where the register $R$ is a polynomial of degree less than 32, then move to the reflected domain of the code at the end. By the [cyclic redundancy check](/cyclic-redundancy-check/) page, feeding a message $M$ of $k$ bits to the register $R$ gives $(R x^k + M x^{32}) \bmod G$. The bytes of a block are $d_0, d_1, \ldots, d_7$ in the order of the data. With refin, byte $d_j$ enters as the polynomial $\bar d_j$ of its reversed bits.

**Lemma 1 (the tables).** In the normal domain let $U_k[v] = v(x)\, x^{32 + 8k} \bmod G$. Then $U_0$ is the table of the [table-driven CRC](/table-driven-crc/), and $U_k[v] = x^8 \cdot U_{k-1}[v] \bmod G$, which is one step of the byte-wise CRC with input byte 0 applied to $U_{k-1}[v]$. In the reflected domain the code stores $T_k[w] = \rho(U_k[\rho_8(w)])$, and line L3 is the reflected byte step with input 0, so the code builds exactly these tables.

*Proof.* $U_k[v] = x^8 \cdot (v x^{32 + 8(k-1)}) \bmod G$. By Lemma 2 of the table-driven proof, a byte step with input 0 from register $R$ gives $x^8 R \bmod G$. In the reflected form this step is `(R >> 8) ^ T0[R & 0xFF]`, which is line L3. The base $T_0$ is built by line L1 as in the table-driven CRC. $\square$

**Lemma 2 (eight bytes).** Let $D(x) = \sum_{j=0}^{7} \bar d_j\, x^{8(7-j)}$ be the 64-bit block in the normal domain. Feeding the 8 bytes to register $R$ gives

$$R' = \bigoplus_{j=0}^{3} U_{7-j}[c_j] \;\oplus\; \bigoplus_{j=4}^{7} U_{7-j}[\bar d_j],$$

where $c_j$ is byte $j$ (from the top) of $R \oplus \sum_{j<4} \bar d_j x^{8(3-j)}$.

*Proof.* $R' = (R x^{64} + D x^{32}) \bmod G$. Split $D = D_{\mathrm{high}} x^{32} + D_{\mathrm{low}}$, where $D_{\mathrm{high}}$ holds bytes 0 to 3 and $D_{\mathrm{low}}$ bytes 4 to 7. Then $R x^{64} + D x^{32} = (R + D_{\mathrm{high}}) x^{64} + D_{\mathrm{low}} x^{32}$. Write $R + D_{\mathrm{high}} = \sum_{j<4} c_j x^{8(3-j)}$. The term $c_j x^{8(3-j)} x^{64} = c_j x^{32 + 8(7 - j)}$ has remainder $U_{7-j}[c_j]$. The term $\bar d_j x^{8(7-j)} x^{32}$ for $j \ge 4$ has remainder $U_{7-j}[\bar d_j]$. The remainder of a sum is the sum of the remainders. $\square$

**Theorem.** `crc32_slicing8` returns the CRC of the data, for a reflected CRC with init and xorout all ones.

*Proof.* Apply $\rho$ to Lemma 2. In the reflected domain the register is $S = \rho(R)$. The top byte of $R$ is the low byte of $S$, reversed, and the first data byte is the low byte of a little-endian load, so $S \oplus$ (the first 4 bytes, loaded little-endian) has $\rho_8(c_j)$ as byte $j$ from the low end. This is line L6. Then $\rho(U_{7-j}[c_j]) = T_{7-j}[\rho_8(c_j)]$, and $\rho(U_{7-j}[\bar d_j]) = T_{7-j}[d_j]$. So line L8 computes $\rho(R')$. By induction over the blocks, after line L5 the register equals the register of the byte-wise CRC after the same bytes. Line L9 finishes the last $n \bmod 8$ bytes with the byte-wise step, which is correct by the table-driven proof, and line L10 applies xorout. The initial value 0xFFFFFFFF is its own reversal. $\square$

Slicing-by-4 is the same argument with a block of 4 bytes: $R' = (R + D) x^{32} \bmod G = \bigoplus_{j<4} U_{3-j}[c_j]$.

**Termination.** The loop of line L5 runs $\lfloor n/8 \rfloor$ times and the loop of line L9 runs $n \bmod 8 < 8$ times. Each step does a fixed number of operations.
