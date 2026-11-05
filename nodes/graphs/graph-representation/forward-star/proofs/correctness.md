---
title: BUILD makes a valid forward and reverse star and the queries list the arcs of each vertex
proves: [correctness, termination]
status: full
---

Let $A$ be the input list of $m$ arcs $(t, h, \mathit{data})$ with $0 \le t, h < n$; repeats are allowed. Write $d^+(i)$ and $d^-(j)$ for the number of arcs of $A$ with tail $i$ and with head $j$. The invariant (F) is (F1), arcs sorted by tail with $\mathit{point}$ marking the blocks, and (F2), $\mathit{trace}$ split by $\mathit{rpoint}$ into increasing segments of the names of the arcs into each vertex.

**Lemma 1 (prefix counts).** If $p[i]$ is the number of keys less than $i$ for $0 \le i \le n$, then $p[0] = 0$, $p[n]$ is the number of keys, $p$ is non-decreasing, and $p[i+1] - p[i]$ is the number of keys equal to $i$.

*Proof.* Direct from the definition, since each key is in $\{0, \ldots, n-1\}$. $\square$

**Lemma 2 (line L1).** After line L1, the arcs are a permutation of $A$, named $0, \ldots, m-1$, with non-decreasing tails, and arcs with the same tail are in their input order.

*Proof.* Line L1 is a counting sort by tail. Let $s[i]$ be the number of arcs with tail less than $i$. The arcs with tail $i$ are written, in input order, into the slots $s[i], s[i] + 1, \ldots$, since the counter of tail $i$ starts at $s[i]$ and is increased after each write. By Lemma 1 these slots form the block $[s[i], s[i+1])$ of length $d^+(i)$, and the blocks of different tails are disjoint and cover $[0, m)$. So each slot is written once, the result is a permutation of $A$, tails increase from block to block, and each block keeps the input order. The loop has $m$ steps, so it stops. $\square$

By Lemma 2 and Lemma 1 applied to the tails, line L2 sets $\mathit{point}[i] = s[i]$, the start of the block of tail $i$, and the arcs out of $i$ are the names in $[\mathit{point}[i], \mathit{point}[i+1])$. So (F1) holds.

**Lemma 3 (lines L3 to L6).** After line L6, (F2) holds.

*Proof.* By Lemma 1 applied to the heads, line L3 gives $\mathit{rpoint}$ with $\mathit{rpoint}[0] = 0$, $\mathit{rpoint}[n] = m$, non-decreasing, and segments of lengths $d^-(j)$. We claim that before step $e$ of the loop of line L5, for each $j$, $\mathit{rpos}[j] = \mathit{rpoint}[j] + k_j$, where $k_j$ is the number of names below $e$ with head $j$, and slots $\mathit{rpoint}[j], \ldots, \mathit{rpos}[j] - 1$ hold these names in increasing order. Line L4 makes this true for $e = 0$. Step $e$ writes $e$, which is larger than all names written before, into slot $\mathit{rpos}[j]$ for $j = \mathit{head}[e]$, and increases $\mathit{rpos}[j]$, which keeps the claim for $e + 1$. Since $k_j \le d^-(j)$, each write stays in the segment of $j$. After step $m - 1$, $k_j = d^-(j)$ for each $j$, so each segment is full, holds exactly the names of the arcs into $j$, each once, in increasing order. The loop has $m$ steps, so it stops. $\square$

**Theorem.** After BUILD, (F) holds; OUT-ARCS$(i)$ outputs exactly the names of the arcs out of $i$, each once; IN-ARCS$(j)$ outputs exactly the names of the arcs into $j$, each once; and OUT-DEGREE and IN-DEGREE return $d^+(i)$ and $d^-(j)$. Each query stops.

*Proof.* (F) holds by Lemma 2 with line L2, and Lemma 3. Line L7 outputs the names in $[\mathit{point}[i], \mathit{point}[i+1])$, which by (F1) are the arcs out of $i$. Line L8 outputs the segment of $j$ of $\mathit{trace}$, which by (F2) lists the arcs into $j$, each once. Lines L9 and L10 return the lengths of the block and of the segment, which by Lemma 1 are $d^+(i)$ and $d^-(j)$. Each query runs over a finite range. Since both stars return names and the data of an arc is stored once, at its name, a write to the data of arc $e$ is read back the same way through either star. $\blacksquare$
