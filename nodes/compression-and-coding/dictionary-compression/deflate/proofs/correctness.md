---
title: INFLATE inverts DEFLATE, and INFLATE is linear in its input and output
proves: [correctness]
status: full
---

We use the two pseudocode blocks of the page: INFLATE (lines L1 to L23 of the main block) and DEFLATE (lines L1 to L13 of the block `encode`). Let $x = x[0 \ldots n-1]$ be the input bytes.

**Claim.** For each byte string $x$ and each choice of the chain limit, the lazy flag and the block split, INFLATE(DEFLATE($x$)) $= x$.

The proof has four parts: the tokens describe $x$; each code is a prefix code; each block decodes to its tokens; the blocks join up.

### 1. The tokens describe the input

Let the *expansion* of a token list be the byte string that the rule "a literal $b$ appends $b$; a match $(\ell, d)$ appends, $\ell$ times, the byte at distance $d$ from the end" builds from the empty string. This is exactly what lines L15 and L21 of INFLATE do.

> **(T)** Before each iteration of the loop of line L2 of DEFLATE, the expansion of tokens is $x[0 \ldots p-1]$.

*Initialization.* $p = 0$ and tokens is empty, so both sides are the empty string.

*Maintenance.* A literal step (line L6 or L10) appends $x[p]$ to the expansion and increases $p$ by 1, so (T) holds again. In a match step (line L8), line L3 returned $(\ell, d)$ with $\ell \ge 3$, $1 \le d \le p$ and $x[p + i] = x[p - d + i]$ for $0 \le i < \ell$, because the match length is the length of the common prefix of $x[p - d \ldots]$ and $x[p \ldots]$, cut at $n - p$. The rule appends bytes $e_0, \ldots, e_{\ell - 1}$, where $e_i$ is the byte at position $p + i - d$ of the string built so far. We show $e_i = x[p + i]$ by induction on $i$. Position $p + i - d$ is below $p + i$, so it holds $x[p + i - d]$: for $p + i - d < p$ by (T), and for $p + i - d \ge p$ by the induction hypothesis for the index $i - d < i$. Then $e_i = x[p + i - d] = x[p + i]$. So the expansion becomes $x[0 \ldots p + \ell - 1]$ and $p$ becomes $p + \ell$.

*Termination.* Each iteration increases $p$ by at least 1, so the loop stops after at most $n$ iterations, with $p = n$. By (T) the expansion is $x$.

The lazy step of line L6 is a literal step, so it keeps (T). The length $\ell \le 258$ and the distance $d \le 32768$ are bounded by line L3, so each match has a length symbol and a distance symbol in the tables of the page.

### 2. Each code is a prefix code, and DECODE reads one codeword

Let lengths $\ell_1, \ldots, \ell_k \ge 1$ satisfy the Kraft inequality $\sum_j 2^{-\ell_j} \le 1$. The canonical construction of RFC 1951 Section 3.2.2 gives the codes of length $b$ the consecutive values $c_b, c_b + 1, \ldots$ where $c_1 = 0$ and $c_{b} = 2(c_{b-1} + N_{b-1})$, with $N_b$ the number of codes of length $b$.

*No code is a prefix of another.* Take two codes $u$ of length $a$ and $v$ of length $b \ge a$. If $a = b$, they are distinct values of the same length. If $a < b$, the first $a$ bits of $v$ form the number $\lfloor v / 2^{b-a} \rfloor$. By the recurrence, the smallest code of length $b$ is $c_b \ge 2^{b - a}(c_a + N_a)$, so the first $a$ bits of each code of length $b$ are at least $c_a + N_a$, which is larger than $u \le c_a + N_a - 1$. Hence $u$ is not a prefix of $v$.

*The values fit.* The Kraft inequality gives $c_b + N_b \le 2^b$ for each $b$, by induction on $b$: $c_b + N_b = 2^b \sum_{a \le b} N_a 2^{-a} \le 2^b$. So each code of length $b$ is a $b$-bit string.

The decoder rejects lengths with a Kraft sum above 1. The encoder makes its lengths with package-merge, whose result satisfies the Kraft inequality with equality when at least two symbols are used; the encoder adds a dummy symbol when only one is used, so the code is complete. The fixed codes have Kraft sum $144 \cdot 2^{-8} + 112 \cdot 2^{-9} + 24 \cdot 2^{-7} + 8 \cdot 2^{-8} = 1$.

Since the code is prefix-free, at most one codeword is a prefix of the remaining input bits. DECODE with the table returns that codeword's symbol: the table entry at index $r$ (the next $L$ bits, read least significant first) was filled by the unique symbol whose bit-reversed code of length $\ell$ equals the low $\ell$ bits of $r$, and two symbols cannot fill the same entry, because then one code would be a prefix of the other.

### 3. A block decodes to its tokens

*Stored block.* The encoder writes BFINAL, BTYPE = 00, pads to the byte boundary, writes LEN and NLEN = LEN xor FFFF, and then the bytes. Lines L5 to L8 read the same fields from the same bit positions and append the same bytes.

*Fixed or dynamic block.* The encoder writes, for each token, the codeword of its literal/length symbol, then the extra bits of the length, the codeword of the distance symbol and the extra bits of the distance, and finally the codeword of symbol 256. By part 2, line L14 reads the same symbol. The number of extra bits is a function of the symbol, so line L18 reads exactly the extra bits that the encoder wrote, and LBASE plus the extra value is the length; the same holds for line L19 and the distance. So the loop of line L13 sees the tokens of the block in order and stops at symbol 256.

*The dynamic header.* The encoder writes HLIT, HDIST and HCLEN, the code length code lengths in the order 16, 17, 18, 0, 8, ..., then the sequence of code lengths as run-length symbols. Each run-length symbol expands to exactly the values it was made from: a value 0 to 15 is itself, 16 with extra value $v$ is $v + 3$ copies of the previous length, 17 and 18 are $v + 3$ and $v + 11$ zeros. The encoder only uses 16 after a written length, so READ-DYNAMIC-CODES rebuilds the same HLIT + HDIST lengths, and by part 2 the same two codes. Its code length code is complete too, by the same dummy rule.

### 4. The blocks join up

The encoder writes BFINAL = 1 on the last block only. So the loop of line L2 of INFLATE reads the blocks in order and stops after the last. The expansion rule of part 1 does not depend on where a block ends, because line L21 reads from all of out, which holds all earlier blocks. Line L20 never fails, since $d \le p$. By parts 1 and 3 the output is the expansion of all tokens, which is $x$. $\square$

### The cost of INFLATE

Let the input have $m$ bytes and the output $n$ bytes. Each pass of the loop of line L13 reads at least one bit and appends at least one byte, except the pass for symbol 256, which ends a block. A block costs at least 3 bits, so there are at most $8m/3$ blocks. Each pass reads at most 48 bits, so the time of all passes is $O(n + m)$ in the word RAM, with a constant number of operations per bit or byte. Building a table costs $O(2^{15})$ per block, a constant. A stored block costs $O(1 + \mathrm{LEN})$. Line L21 costs $O(len)$, which is the number of bytes it writes. So the total time is $\Theta(n + m)$: it is at least linear because each input byte is read and each output byte written.
