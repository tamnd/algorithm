---
title: The interpolative decoder returns the coded list
proves: [correctness]
status: full
---

Fix integers $l \le h$ and a strictly increasing list $S[0] < \cdots < S[n-1]$ with $l \le S[0]$ and $S[n-1] \le h$ (for $n = 0$ the list is empty). Call a tuple $(i, j, l', h')$ *valid* if either $i > j$, or $i \le j$ and $l' \le S[i]$ and $S[j] \le h'$.

**Lemma 1 (the offset fits).** Let $(i, j, l', h')$ be valid with $i \le j$, let $m = i + \lfloor (j - i)/2 \rfloor$ and $r = h' - l' - (j - i)$. Then $r \ge 0$ and $0 \le S[m] - l' - (m - i) \le r$.

*Proof.* The elements $S[i], \ldots, S[m]$ are $m - i + 1$ distinct integers, increasing, with $S[i] \ge l'$, so $S[m] \ge S[i] + (m - i) \ge l' + (m - i)$. In the same way $S[m] \le S[j] - (j - m) \le h' - (j - m)$. Subtract $l' + (m - i)$: the offset is between 0 and $h' - (j - m) - l' - (m - i) = r$. In particular $r \ge 0$. $\square$

**Lemma 2 (runs).** If $(i, j, l', h')$ is valid, $i \le j$ and $h' - l' = j - i$, then $S[i + t] = l' + t$ for $0 \le t \le j - i$.

*Proof.* The $j - i + 1$ distinct integers $S[i], \ldots, S[j]$ lie in $[l', h']$, which has exactly $h' - l' + 1 = j - i + 1$ integers. So they are all of them, and since they are increasing, $S[i + t] = l' + t$. $\square$

**Lemma 3 (the children are valid).** If $(i, j, l', h')$ is valid with $i \le j$ and $m$ is as above, then $(m + 1, j, S[m] + 1, h')$ and $(i, m - 1, l', S[m] - 1)$ are valid.

*Proof.* If $m + 1 \le j$, then $S[m + 1] \ge S[m] + 1$ because the list is strictly increasing, and $S[j] \le h'$. If $i \le m - 1$, then $l' \le S[i]$ and $S[m - 1] \le S[m] - 1$. $\square$

**Lemma 4 (the minimal binary code).** For each $r \ge 0$, the code of a value $v \in [0, r]$ written by line L5 is read back as $v$ by the reader for $r$ in line L10, and the reader consumes exactly the bits written.

*Proof.* For $r = 0$ nothing is written or read and the value is 0. For $r \ge 1$ let $k = \lceil \log(r + 1) \rceil$ and $c = 2^k - (r + 1)$, so $0 \le c < 2^{k-1}$. The writer maps $v$ to $y = (v - s) \bmod (r + 1)$, a bijection of $[0, r]$. If $y < c$ it writes $y$ in $k - 1$ bits; else it writes $y + c$ in $k$ bits, and $y + c \ge 2c$, so the first $k - 1$ bits form $t = \lfloor (y + c)/2 \rfloor \ge c$. The reader reads $t$ in $k - 1$ bits. If $t < c$ the codeword was short and $y = t$. If $t \ge c$ the codeword was long, the reader reads one more bit to form $y + c$, and subtracts $c$. Then $(y + s) \bmod (r + 1) = v$. In plain mode, $v \le r < 2^k$ is written and read in exactly $k$ bits. $\square$

**Lemma 5 (the two loops run in lockstep).** Let the encoder of lines L1 to L6 and the decoder of lines L7 to L11 run on the same $n$, $l$, $h$, with the decoder reading the bits that the encoder wrote. Before each iteration of the two loops, the two stacks hold the same tuples in the same order, every tuple is valid, the decoder's read position is at the start of the codeword the encoder writes in the matching iteration, and the decoder has set $S'[x] = S[x]$ for every index $x$ that is not in the index range $[i, j]$ of some tuple on the stack and that the encoder's loop has finished with.

*Proof.* By induction on the iterations. At the start, both stacks hold $(0, n - 1, l, h)$, which is valid by the input condition, no bits are read, and no index has been finished. Suppose the claim holds and both loops pop the same valid tuple $(i, j, l', h')$.

- If $i > j$, both loops go on with no change.
- If $i \le j$ and $h' - l' = j - i$, line L3 writes nothing and line L9 sets $S'[i + t] = l' + t$, which is $S[i + t]$ by Lemma 2. Both push nothing.
- Otherwise both compute the same $m$ and the same $r$. By Lemma 1 the encoder writes a value in $[0, r]$, and by Lemma 4 the decoder reads the same value and its read position moves to the next codeword. So line L10 sets $S'[m] = l' + (m - i) + (S[m] - l' - (m - i)) = S[m]$. Both loops then push the same two tuples, built from the same $S[m]$, in the same order, and both are valid by Lemma 3.

In every case the claim holds before the next iteration. $\square$

**Theorem.** BIC-DECODE$(n, l, h, R)$, run on the output of BIC-ENCODE$(S, l, h, W)$, returns $S$, and the encoder's stack never holds more than $\lfloor \log n \rfloor + 2$ tuples.

*Proof.* Each popped tuple with $i \le j$ either fills its whole index range by Lemma 2 or sets $S'[m]$ and pushes two tuples whose index ranges are $[i, m - 1]$ and $[m + 1, j]$. So the index ranges of the tuples on the stack and the finished indices always partition $[0, n - 1]$, and each pop with $i \le j$ finishes at least one index. Each index is finished once, so the loops stop after at most $2n + 1$ iterations with an empty stack, and then every index is finished. By Lemma 5, $S'[x] = S[x]$ for every $x$.

For the stack size, a tuple with $k \ge 1$ elements pushes two tuples with at most $\lfloor k/2 \rfloor$ elements each. The tuples on the stack at any time are the right children of the tuples on the current path from the root, plus at most one left child just pushed, and each step down the path halves the number of elements at least. A path of nonempty tuples from a root with $n$ elements has at most $\lfloor \log n \rfloor + 1$ tuples, so the stack holds at most $\lfloor \log n \rfloor + 2$ tuples. $\blacksquare$
