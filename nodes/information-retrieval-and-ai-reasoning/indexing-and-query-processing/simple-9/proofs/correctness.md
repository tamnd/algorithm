---
title: Simple-9 decoding inverts encoding, and the word count for values of one width
proves: [correctness]
status: full
---

Let $x_0, \ldots, x_{n-1}$ be integers with $0 \le x_i < 2^{28}$. The layouts are the pairs $(c_s, w_s)$ for $s = 0, \ldots, 8$: $(28, 1), (14, 2), (9, 3), (7, 4), (5, 5), (4, 7), (3, 9), (2, 14), (1, 28)$. For each of them $c_s w_s \le 28$.

1. **Each step of the encoder ends and makes progress.** At line L3, selector $s = 8$ has $c_8 = 1$ and $w_8 = 28$, and $x_i < 2^{28}$ by the precondition, so the test of line L5 holds for $s = 8$ at the latest. So the loop of line L3 always stops with some $s$ and $k = \min(c_s, n - i) \ge 1$, since $i < n$. Line L8 adds $k$ to $i$, so the loop of line L2 ends after at most $n$ words.

2. **Each word is a valid 32-bit word.** Line L5 ensures that $x_{i+j} < 2^{w_s}$ for $0 \le j < k$. Line L7 puts $x_{i+j}$ in bits $j w_s$ to $(j+1) w_s - 1$. These fields are disjoint and all lie below bit $k w_s \le c_s w_s \le 28$. Line L6 puts $s \le 8 < 16$ in bits 28 to 31. So the word is below $2^{32}$, its top four bits are $s$, its field $j$ holds $x_{i+j}$ for $j < k$, and its bits from $k w_s$ to 27 are zero.

3. **The decoder reads back the same values.** Let the encoder write words $u_1, \ldots, u_W$ with selectors $s_1, \ldots, s_W$ and counts $k_1, \ldots, k_W$, so that $k_1 + \cdots + k_W = n$, and only the last word can have $k_W < c_{s_W}$, because $k < c_s$ only when $k = n - i$. By induction on $q$, before the decoder reads word $u_q$ the list holds $x_0, \ldots, x_{K-1}$ with $K = k_1 + \cdots + k_{q-1}$. Line L12 recovers $s_q$ from the top four bits, by step 2. For $q < W$, $k_q = c_{s_q}$ and $K + k_q \le n$, so line L13 reads all $c_{s_q}$ fields, which by step 2 are $x_K, \ldots, x_{K + k_q - 1}$. For $q = W$, line L13 reads fields until the list has $n$ values, that is the first $k_W = n - K$ fields, and these are the last values. So line L14 returns $x_0, \ldots, x_{n-1}$.

4. **Word count for values of one width.** Suppose every value has bit length exactly $w$, with $1 \le w \le 28$ (for $w = 1$, the values 0 and 1). Let $s^\ast$ be the least selector with $w_{s^\ast} \ge w$, and $c = c_{s^\ast}$. A selector $s < s^\ast$ has $w_s < w$, so it fails at line L5 on the first value. Selector $s^\ast$ fits any $k$ values. So every word takes $\min(c, n - i)$ values, and the encoding has $\lceil n / c \rceil$ words and $32 \lceil n / c \rceil$ bits. $\blacksquare$

The greedy choice of line L3 takes the selector with the most values that fit. This is not always the fewest words. For $x = (7, 300, 0, 2, 5, 3, 12, 3, 0, 100, 1, 300)$ the encoder writes 4 words, in the layouts $3 \times 9$, $5 \times 5$ and $3 \times 9$, and a last word in layout $3 \times 9$ that holds only 300. The split $2 \times 14$, $7 \times 4$, $3 \times 9$ uses 3 words. Correctness does not depend on this choice: step 3 holds for any rule that picks, at each word, a selector whose test at line L5 holds.
