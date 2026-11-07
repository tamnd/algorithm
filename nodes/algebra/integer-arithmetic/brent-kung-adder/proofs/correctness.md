---
title: The Brent-Kung adder computes the sum of its inputs
proves: [correctness, termination]
status: full
---

Let $n \ge 1$, $a_i, b_i, c_{\text{in}} \in \{0, 1\}$, $g_i = a_i \wedge b_i$ and $p_i = a_i \oplus b_i$. Define the true carries $c^{\ast}_0 = c_{\text{in}}$ and $c^{\ast}_{i+1} = g_i \vee p_i c^{\ast}_i$. As in a full adder, $a_i + b_i + c^{\ast}_i = (p_i \oplus c^{\ast}_i) + 2c^{\ast}_{i+1}$, so the bits $p_i \oplus c^{\ast}_i$ for $i < n$ and $c^{\ast}_n$ represent $a + b + c_{\text{in}}$. It suffices to show that $G[i] = c^{\ast}_{i+1}$ for each $i$ at line L11.

**Termination.** The loop L4 to L6 doubles $d$ until $d \ge n$, and the loop L8 to L10 halves $d$ until it is 0. Each level updates finitely many positions.

**Block pairs.** Let $g'_0 = g_0 \vee p_0 c_{\text{in}}$ (line L2) and $g'_i = g_i$ for $i \ge 1$. For $k \le i$ define $(G_{i:k}, P_{i:k})$ by $(G_{i:i}, P_{i:i}) = (g'_i, p_i)$ and $G_{i:k} = g'_i \vee p_i G_{i-1:k}$, $P_{i:k} = p_i P_{i-1:k}$ for $k < i$.

**Lemma 1.** For $k \le j < i$, $(G_{i:k}, P_{i:k}) = (G_{i:j+1}, P_{i:j+1}) \circ (G_{j:k}, P_{j:k})$.

*Proof.* By induction on $i - j$. If $j = i - 1$, it is the definition. Otherwise, $G_{i:k} = g'_i \vee p_i G_{i-1:k}$, and by induction $G_{i-1:k} = G_{i-1:j+1} \vee P_{i-1:j+1} G_{j:k}$; substituting gives $G_{i:k} = (g'_i \vee p_i G_{i-1:j+1}) \vee p_i P_{i-1:j+1} G_{j:k} = G_{i:j+1} \vee P_{i:j+1} G_{j:k}$. The $P$ part is a product of the same $p$'s. $\square$

**Lemma 2.** $G_{i:0} = c^{\ast}_{i+1}$ for each $i$.

*Proof.* By induction on $i$. $G_{0:0} = g_0 \vee p_0 c_{\text{in}} = c^{\ast}_1$, and $G_{i:0} = g_i \vee p_i G_{i-1:0} = g_i \vee p_i c^{\ast}_i = c^{\ast}_{i+1}$. $\square$

Say that position $i$ *holds* $k..i$ when $(G[i], P[i]) = (G_{i:k}, P_{i:k})$, ignoring $P[i]$ when $k = 0$, since no later cell reads it: a cell reads $P[i - d]$ only to compute a $P$, and it computes $P$ only when the block of $i - d$ does not start at 0. After line L3, position $i$ holds $i..i$. By Lemma 1, a cell at position $i$ with distance $d$ that finds $i$ holding $j + 1..i$ and $i - d = j$ holding $k..j$ leaves $i$ holding $k..i$.

For $m \ge 1$ write $\nu(m)$ for the exponent of the largest power of 2 dividing $m$.

**Lemma 3 (up-sweep).** After the up-sweep level with distance $d = 2^t$, each position $i$ holds the block of length $2^{\min(\nu(i+1), t+1)}$ ending at $i$.

*Proof.* By induction on $t$; before the first level the claim holds with "$t = -1$", lengths $2^0 = 1$. Level $d = 2^t$ updates the positions with $2^{t+1} \mid i + 1$. For such $i$, by induction $i$ holds the block of length $2^t$ ending at $i$, and $i - d$, with $\nu(i - d + 1) = t$, holds the block of length $2^t$ ending at $i - d$, which is adjacent. So $i$ now holds the block of length $2^{t+1}$. Positions with $\nu(i + 1) \le t$ are not updated and already hold blocks of length $2^{\nu(i+1)}$. $\square$

Since the up-sweep runs up to the first $d \ge n$, and $2^{\nu(i+1)} \le i + 1 \le n$, after it each position $i$ holds the block of length $2^{\nu(i+1)}$ ending at $i$, that is, $i + 1 - 2^{\nu(i+1)} + 1 .. i$. If $i + 1$ is a power of 2, this is $0..i$.

**Lemma 4 (down-sweep).** After the down-sweep level with distance $d$, each position $i < n$ with $2^{\nu(i+1)} \ge d$ holds $0..i$.

*Proof.* Line L7 sets $d$ to $2^{L-2}$ where $2^L$ is the first power of 2 that is at least $n$, or to 0. Positions with $2^{\nu(i+1)} \ge 2^{L-1}$ have $i + 1 \in \{2^{L-1}, 2^L\}$ (any larger multiple would exceed $n \le 2^L$), so they are powers of 2 and hold $0..i$ after the up-sweep. This is the base. At level $d$, let $i$ satisfy $\nu(i + 1) = \log_2 d$ exactly. If $i + 1 = d$, it is a power of 2 and is done. Otherwise $i + 1 = (2m + 1)d$ with $m \ge 1$, so $i \ge 3d - 1$ and $i \equiv d - 1 \pmod{2d}$, and line L9 updates $i$. Position $i$ holds the block of length $d$ ending at $i$, which starts at $i - d + 1$. Position $i - d$ has $i - d + 1 = 2md$, so $2^{\nu(i - d + 1)} \ge 2d$, and by the induction hypothesis (the previous level, or the base) it holds $0..i - d$. The cell gives $i$ the block $0..i$. Positions with $\nu(i+1) > \log_2 d$ are not updated at this level and hold $0..i$ by induction. No other position is updated, since line L9 updates only $i$ with $\nu(i + 1) = \log_2 d$. $\square$

**Theorem.** BRENT-KUNG-ADD returns the bits of $a + b + c_{\text{in}}$.

*Proof.* After the level $d = 1$, or directly after the up-sweep when the down-sweep is empty ($n \le 2$, where every $i + 1 \le 2$ is a power of 2), every position $i$ holds $0..i$ by Lemma 4 or Lemma 3. So $G[i] = G_{i:0} = c^{\ast}_{i+1}$ by Lemma 2, line L11 sets $c[i] = c^{\ast}_i$, and line L12 computes $s_i = p_i \oplus c^{\ast}_i$. By the identity at the start, the output is $a + b + c_{\text{in}}$. $\blacksquare$
