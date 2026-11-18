---
title: Punycode decoding inverts Punycode encoding
proves: [correctness, termination]
status: full
---

**Claim.** Let $s$ be a string of $N$ scalar values, $b$ of them basic (below U+0080). If PUNYCODE-ENCODE$(s)$ (lines L1 to L14) does not stop with an overflow, it stops, its output consists of basic code points only, and PUNYCODE-DECODE (lines L15 to L24) applied to it stops and returns $s$. So the encoding is injective on these strings.

**Notation.** Number the positions of $s$ from 0. Order the $N - b$ non-basic positions by (value, position), and call them insertion $1, \ldots, N - b$. Insertion $t$ is at position $\mathrm{pos}_t$ and has value $n_t$. Let $h_t = b + t - 1$, the number of code points already placed before insertion $t$, and let

$$p_t = \#\{\, q < \mathrm{pos}_t : s[q] \le n_t \,\}.$$

**Lemma 1 (what the decoder builds).** Suppose the decoder starts with the basic code points of $s$ in order and, for $t = 1, 2, \ldots$, inserts $n_t$ at index $p_t$. Then after insertion $t$ its string is the subsequence of $s$ made of the basic code points and insertions $1$ to $t$. At the end it is $s$.

*Proof.* By induction on $t$. Before insertion $t$, the placed code points are those of $s$ with value below $n_t$, and those with value $n_t$ at positions before $\mathrm{pos}_t$, in the order of $s$. Exactly $p_t$ of them lie before $\mathrm{pos}_t$ in $s$, so inserting $n_t$ at index $p_t$ puts it in its place. $\square$

**The decoder state.** The decoder keeps a pair $(n, i)$. After insertion $t$ it has $(n_t, p_t + 1)$, and its string has $h_t + 1$ code points, so an insertion index is one of $0, \ldots, h_t + 1$, which is $h_{t+1} + 1$ choices. Lines L18 to L21 read a number $\delta$ and add it to $i$. Line L23 carries $i \operatorname{div} (h_{t+1} + 1)$ into $n$ and keeps $i \bmod (h_{t+1} + 1)$, and line L24 inserts $n$ at index $i$. So insertion $t + 1$ lands at $(n_{t+1}, p_{t+1})$ exactly when

$$\delta_{t+1} = (n_{t+1} - n_t)(h_{t+1} + 1) + p_{t+1} - p_t - 1, \qquad (1)$$

and the first insertion lands at $(n_1, p_1)$ from the start state $(128, 0)$ exactly when $\delta_1 = (n_1 - 128)(b + 1) + p_1$.

**Lemma 2 (the encoder writes these deltas).** The value of $\delta$ that line L10 writes for insertion $t$ is $\delta_t$ as above.

*Proof.* The encoder handles the values $m$ in increasing order (line L5 takes the least value not below $n$). For each $m$ it scans all of $s$ (line L7). It adds 1 to $\delta$ for each code point below $m$ (line L8), writes $\delta$ and resets it to 0 at each code point equal to $m$ (line L9), and adds 1 at the end of the scan (line L14). Before the scan it adds $(m - n)(h + 1)$, where $n$ is the old value plus 1 and $h$ counts the code points placed so far (line L6).

First insertion: $\delta = (n_1 - 128)(b + 1)$, plus one for each code point below $n_1$ before $\mathrm{pos}_1$. No value of $s$ lies in $128 \ldots n_1 - 1$, so these are the basic code points before $\mathrm{pos}_1$, and their count is $p_1$.

Insertion $t + 1$ with $n_{t+1} = n_t$: since insertion $t$, the scan has passed the positions strictly between $\mathrm{pos}_t$ and $\mathrm{pos}_{t+1}$. None of them has the value $n_t$, so $\delta$ counts those with a value below $n_t$. That is $p_{t+1} - p_t - 1$, because the extra $-1$ removes position $\mathrm{pos}_t$ itself, which $p_{t+1}$ counts and $p_t$ does not. The first term of (1) is 0.

Insertion $t + 1$ with $n_{t+1} = m > n_t$: insertion $t$ is the last one of value $n_t$. The rest of that scan adds $r = \#\{\, q > \mathrm{pos}_t : s[q] < n_t \,\}$, line L14 adds 1, line L6 adds $(m - n_t - 1)(h_{t+1} + 1)$, and the new scan adds $\#\{\, q < \mathrm{pos}_{t+1} : s[q] < m \,\} = p_{t+1}$. All code points of value at most $n_t$ are placed, so $h_{t+1} = p_t + 1 + r$. The total is $r + 1 + (m - n_t - 1)(h_{t+1} + 1) + p_{t+1}$, and with $r = h_{t+1} - p_t - 1$ this equals (1). $\square$

**Lemma 3 (variable-length integers).** Fix thresholds $t_0, t_1, \ldots$ with $1 \le t_j \le 26$, and let $w_0 = 1$ and $w_{j+1} = w_j (36 - t_j)$. Lines L10 to L12 write $q \ge 0$ as digits $d_0, \ldots, d_r$ with $d_j \ge t_j$ for $j < r$, $d_r < t_r$, and $q = \sum_j d_j w_j$. Lines L18 to L21 read these digits back, stop after $d_r$, and get $q$.

*Proof.* Let $q_0 = q$. While $q_j \ge t_j$, the encoder writes $d_j = t_j + (q_j - t_j) \bmod (36 - t_j)$, which lies in $t_j \ldots 35$, and sets $q_{j+1} = (q_j - t_j) \operatorname{div} (36 - t_j)$. Then $q_j = d_j + (36 - t_j)\, q_{j+1}$. Also $q_{j+1} < q_j$, so the loop stops, with a last digit $d_r = q_r < t_r$. Unfolding gives $q = \sum_j d_j w_j$. The decoder adds $d_j w_j$ and stops at the first digit below its threshold, which is $d_r$. $\square$

Both sides compute the thresholds from $k$ and the bias in the same way. The bias is the initial bias for the first delta. After each delta, both sides call ADAPT with the same arguments: the delta, the number of code points after the insertion ($h + 1$ in line L13, the output length plus 1 in line L22), and a flag that is true only for the first delta ($h = b$ in the encoder, $\mathit{oldi} = 0$ in the decoder, since later deltas start from $i = p_t + 1 \ge 1$). So by induction the thresholds agree for every delta. Digits map to the characters a to z and 0 to 9, a bijection on $0 \ldots 35$, and none of them is the delimiter "-".

**Proof of the claim.** The output of the encoder is the basic code points of $s$, then "-" if $b > 0$, then the digits. Digits are never "-", so the last "-" of the output is the one after the basic code points, and if $b = 0$ the output has no "-". Line L15 therefore recovers exactly the basic code points. By Lemma 3, the decoder reads exactly the deltas that the encoder wrote, and by Lemma 2 and (1) each delta brings the decoder state to $(n_t, p_t)$. By Lemma 1 the decoder then returns $s$. The values $n_t$ are non-basic scalar values, so the checks after line L23 never reject them.

Termination. Each pass of the loop of line L4 handles at least one code point, because line L5 picks a value that occurs in $s$, so $h$ grows and the loop stops when $h = N$. The digit loop stops by Lemma 3. The decoder moves $\mathit{pos}$ forward with each digit it reads and stops when the input ends. With the overflow checks of RFC 3492 section 6.4, every intermediate value fits in 32 bits, and if one would not, the procedure stops with an error instead. $\blacksquare$
