---
title: BISE decodes what it encodes, and a one-partition ASTC block decodes as a fixed function of its 128 bits
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The proof covers the subset of the code: BISE for every range of the format, and one 2D LDR block with one partition, one weight plane and the color endpoint modes 8 and 12. All arithmetic is on integers. Some facts are about finite tables of the format, and for those the proof is an enumeration that the code tests carry out. We say so where it happens.

A BISE range is $0..M$ with $M + 1 = 2^n$, $3 \cdot 2^n$ or $5 \cdot 2^n$. A value $x$ splits into its $n$ low bits $m = x \bmod 2^n$ and its high part $h = \lfloor x / 2^n \rfloor$, which is a bit-free number, a trit in $\{0, 1, 2\}$ or a quint in $\{0, \dots, 4\}$. A group holds 1 value (plain bits), 5 values (trits) or 3 values (quints). Its high parts are packed into a code $c$ of $p = 0$, 8 or 7 bits, and the group is written as $m_0$, then $s_0$ bits of $c$, then $m_1$, then $s_1$ bits of $c$, and so on, with $(s_j) = (2, 2, 1, 2, 1)$ for trits and $(3, 2, 2)$ for quints. Let $D$ be the table that maps a code to its tuple of high parts (lines L13), and let the encoder use $E(u) = \min \{c : D(c) = u\}$.

**Lemma 1 (the tables are onto).** The trit table $D$ maps the 256 codes of 8 bits onto all $3^5 = 243$ tuples, and the quint table maps the 128 codes of 7 bits onto all $5^3 = 125$ tuples. So $E$ is defined for every tuple.

*Proof.* By enumeration of the 384 codes, in `test_packed_fields_cover_every_tuple`. $\square$

**Theorem 1 (the layout and the rate).** A sequence of $V$ values in $0..M$ takes $\text{ISE-BITS}(V, M) = V n + \lceil 8V/5 \rceil$ bits for trits, $V n + \lceil 7V/3 \rceil$ for quints and $V n$ for plain bits. This is $\lceil V r \rceil$ with the exact rate $r = n + 8/5$, $n + 7/3$ or $n$ bits per value.

*Proof.* A full group of trits holds $5n + 8$ bits for 5 values, and a full group of quints $3n + 7$ for 3 values. A last group with $j$ values ends right after the $s_{j-1}$ code bits that follow $m_{j-1}$. Those are $j n + (s_0 + \dots + s_{j-1})$ bits. For trits the partial sums are $2, 4, 5, 7$ for $j = 1, \dots, 4$, which equal $\lceil 8j/5 \rceil$, and for quints they are $3, 5$ for $j = 1, 2$, which equal $\lceil 7j/3 \rceil$. Adding the full groups gives the formula, and $V n$ is an integer, so it equals $\lceil V r \rceil$. $\square$

The rate is close to the information content $n + \log_2 3 \approx n + 1.585$ or $n + \log_2 5 \approx n + 2.322$. The excess per value is $8/5 - \log_2 3 < 0.016$ bits for trits and $7/3 - \log_2 5 < 0.012$ bits for quints.

**Theorem 2 (round trip).** For every range and every sequence $x_0, \dots, x_{V-1}$ in it, the encoder writes no bit at or past position $\text{ISE-BITS}(V, M)$, and ISE-DECODE returns $x_0, \dots, x_{V-1}$, whatever the bits past the end hold.

*Proof.* Line L11 masks the stream to its length, so the bits past the end read as zero. Lines L12 and L14 read the low bits in the same places where the encoder wrote them, by Theorem 1, so $m_j$ comes back unchanged. In a full group, line L13 reads the code $c = E(u)$ and returns $D(c) = u$, the high parts.

In a last group with $j$ values, the encoder pads the tuple with zeros to $u = (h_0, \dots, h_{j-1}, 0, \dots, 0)$ and writes all of it. The bits past the end are the padded low bits, which are zero, and the code bits from position $q_j = s_0 + \dots + s_{j-1}$ upward. For every such tuple there is a code below $2^{q_j}$ that maps to it, by enumeration of the $3 + 9 + 27 + 81$ trit tuples and the $5 + 25$ quint tuples, in `test_round_trip_every_short_trit_and_quint_group`. Then the smallest code $E(u)$ is also below $2^{q_j}$, so its bits from $q_j$ upward are zero. The decoder therefore reads the code $E(u)$ in full, gets $u$ from line L13, and drops the padded values. The code asserts that no bit past the end is set. $\square$

**Lemma 2 (the unquantization).** For each color range of a trit or a quint, the map of line L5 to $0..255$ is one to one, has $0$ and $255$ in its image, and flipping the lowest bit $a$ of a value maps $y$ to $255 - y$.

*Proof.* The one to one part and the end values are by enumeration of the 17 color ranges, in `test_unquantization_tables`. For the mirror, line L5 computes $T = D C + B$, where $B$ does not depend on $a$, then $T \oplus A$ with $A = 0$ or $A = 511$, then $(A \wedge 128) \vee \lfloor T/4 \rfloor$. For every range in the table, $T \le 507 < 512$, since $D \le 4$ and the largest $D C + B$ is $2 \cdot 5 + 497$. So $T \oplus 511 = 511 - T$ and $\lfloor (511 - T)/4 \rfloor = 127 - \lfloor T/4 \rfloor$. With $a = 0$ the result is $\lfloor T/4 \rfloor \le 127$, and with $a = 1$ it is $128 + 127 - \lfloor T/4 \rfloor$, which is $255$ minus the first. $\square$

The weight tables of line L7 have the same form with 7 bits and the bound $T < 128$, and then add 1 to every value above 32, which maps them into $0..64$. The test checks that each is one to one with the end values $0$ and $64$.

**Lemma 3 (the infill).** For a grid of $N \times M$ weights in $0..64$ and a legal footprint $B_s \times B_t$ with $N \le B_s$ and $M \le B_t$, line L8 returns a value in $0..64$. The four factors are nonnegative and sum to 16, so a constant grid gives the same constant. A neighbor past the grid always has the factor 0. The corner texels $(0, 0)$ and $(B_s - 1, B_t - 1)$ get the corner weights.

*Proof.* Let $f_s, f_t \in \{0, \dots, 15\}$ and $w_{11} = \lfloor (f_s f_t + 8)/16 \rfloor$. The sum $w_{00} + w_{01} + w_{10} + w_{11}$ is $(16 - f_s - f_t + w_{11}) + (f_s - w_{11}) + (f_t - w_{11}) + w_{11} = 16$. Since $f_s f_t \le 15 \min(f_s, f_t)$, we get $w_{11} \le \min(f_s, f_t)$, so $w_{01}, w_{10} \ge 0$. Since $w_{11} \ge (f_s f_t - 7)/16$, we get $w_{00} \ge ((16 - f_s)(16 - f_t) - 7)/16 > -1$, and $w_{00}$ is an integer, so $w_{00} \ge 0$. A weighted sum with these factors of values in $0..64$, plus 8 and divided by 16, lies in $0..64$. For a constant $c$ it is $\lfloor (16c + 8)/16 \rfloor = c$.

The step is $d_s = \lfloor (1024 + \lfloor B_s/2 \rfloor)/(B_s - 1) \rfloor$. For the widths 4, 5, 6, 8, 10 and 12, the product $d_s (B_s - 1)$ is 1026, 1024, 1025, 1022, 1026 and 1023. So for every $s$, $g_s \le \lfloor (1026 (N - 1) + 32)/64 \rfloor = 16 (N - 1)$, because $2 (N - 1) \le 22 < 32$. Then $j_s \le N - 1$, and $j_s = N - 1$ forces $f_s = 0$, so the right neighbor has the factor 0. The same holds for $t$. At $s = 0$, $g_s = 0$. At $s = B_s - 1$, also $g_s \ge \lfloor (1022 (N - 1) + 32)/64 \rfloor = 16 (N - 1)$, so $g_s = 16(N - 1)$, $j_s = N - 1$ and $f_s = 0$. $\square$

When the grid has the size of the block, the infill is the identity. This is by enumeration over the 14 footprints, in `test_infill_identity_and_constants`.

**Lemma 4 (the interpolation).** With $C_k = 257 E_k$, line L9 gives $C_0$ at $i = 0$, $C_1$ at $i = 64$, and a value that moves monotonically from $C_0$ to $C_1$ as $i$ grows.

*Proof.* At $i = 0$ it is $\lfloor (64 C_0 + 32)/64 \rfloor = C_0$, and at $i = 64$ it is $C_1$. The numerator is $64 C_0 + i (C_1 - C_0) + 32$, monotone in $i$, and the floor keeps the order. $\square$

**Theorem 3 (decoding is a fixed function of the block).** Lines L1 to L10 read only the 128 bits of the block and the footprint. For every block in the subset they return either the error color for every texel or one RGBA value of 16 bits per channel for each texel. The color stream and the weight stream do not overlap.

*Proof.* Lines L1 to L4 read fixed fields and fixed tables, and each test that fails returns the error color. The color range of line L4 is chosen so that its stream fits in $128 - 17 - \text{wbits}$ bits, so it ends at bit $17 + (\text{its length}) \le 128 - \text{wbits}$, below the first weight bit $128 - \text{wbits}$. Line L5 uses Theorem 2 on the bits from 17 upward, and line L7 on the bits from 127 downward. Lines L6, L8 and L9 are integer formulas, defined for all inputs, by Lemmas 3 and 4. No step reads another block. $\square$

So any texel at $(x, y)$ needs only the block $(\lfloor x / B_s \rfloor, \lfloor y / B_t \rfloor)$, at a fixed address, and the rate is $128 / (B_s B_t)$ bits per texel.

**Cost.** A block holds at most 64 weights and here 6 or 8 color values, so lines L1 to L7 take $O(1)$ time, and lines L8 and L9 take $O(1)$ per texel. Decoding one texel alone needs only the weights of its four neighbors, so it is $O(1)$ too.
