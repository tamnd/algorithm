---
title: Algorithm H visits each restricted growth string of length n once, in lexicographic order, in Theta(B_n) time
proves: [correctness, time.worst]
status: full
---

**Statement.** For each integer $n \ge 0$, SET-PARTITIONS$(n)$ visits each restricted growth string of length $n$ exactly once, in increasing lexicographic order, and stops. For $n \ge 1$ the loop body of line L6 runs $\sum_{i=1}^{n-1} B_i$ times in total, which is less than $B_n$ for $n \ge 2$, and the running time is $\Theta(B_n)$.

**Setup.** A restricted growth string (RGS) of length $n$ is a sequence $a_1 \ldots a_n$ with $a_1 = 0$ and $0 \le a_i \le \beta_i(a)$ for $i \ge 2$, where $\beta_i(a) = 1 + \max(a_1, \ldots, a_{i-1})$. All RGS of length $n$ have the same length, so $a < d$ in lexicographic order means $a_i < d_i$ at the first index $i$ where they differ. The RGS of length $n$ are in bijection with the partitions of $[n]$, so there are $B_n$ of them.

**Lemma 1 (first and last).** The smallest RGS of length $n \ge 1$ is $0^n$, and the largest is $\omega_n = 0\, 1\, 2 \cdots (n - 1)$. The string $\omega_n$ is the only RGS with $a_i = \beta_i(a)$ for all $i \ge 2$.

*Proof.* $0^n$ is an RGS and has the smallest value at each index. If $a_i = \beta_i(a)$ for all $i \ge 2$, then by induction $a_i = i - 1$, so $a = \omega_n$. For any RGS $a$, induction gives $a_i \le i - 1$, since $a_1 = 0$ and $a_i \le 1 + \max_{i' < i} a_{i'} \le 1 + (i - 2)$. So each RGS is at most $\omega_n$ at each index, and $\omega_n$ is the largest. $\square$

**Lemma 2 (successor).** Let $a \ne \omega_n$ be an RGS of length $n$, and let $j \ge 2$ be the largest index with $a_j < \beta_j(a)$. The smallest RGS larger than $a$ is

$$a^+ = a_1 \ldots a_{j-1}\, (a_j + 1)\, 0^{n-j}.$$

*Proof.* The index $j$ exists by Lemma 1. The string $a^+$ is an RGS: its prefix is that of $a$, $a_j + 1 \le \beta_j(a)$, and a $0$ is always allowed. It first differs from $a$ at $j$, where it is larger.

Let $d > a$ be an RGS that first differs from $a$ at $i$, so $d_i > a_i$. Since $d$ and $a$ agree before $i$, $\beta_i(d) = \beta_i(a)$, and $a_i < d_i \le \beta_i(a)$. So $i \ge 2$ is an index with $a_i < \beta_i(a)$, and $i \le j$. If $i < j$, then $a^+$ agrees with $a$ at $i$, so $a^+_i = a_i < d_i$ and $a^+ < d$. If $i = j$ and $d_j > a_j + 1$, then $a^+ < d$ at $j$. If $i = j$ and $d_j = a_j + 1$, then $d$ and $a^+$ agree up to $j$, and $a^+$ continues with zeros, the smallest possible entries, so $a^+ \le d$. $\square$

**Invariant (B).** At line L4, $b[i] = \beta_i(a)$ for $2 \le i \le n$.

*Proof.* Line L2 sets $a = 0^n$ and $b[i] = 1 = \beta_i(0^n)$. Suppose (B) holds at a visit, and the step changes $a$ at index $j$ (line L8) and resets indices $i > j$ (line L9). For $i \le j$ the prefix $a_1 \ldots a_{i-1}$ does not change, so $b[i]$ stays correct. For $i > j$, the new entries $a_{j+1}, \ldots, a_{i-1}$ are $0$, so $\beta_i = 1 + \max(a_1, \ldots, a_j)$ with the new $a_j$. Before the change $1 + \max(a_1, \ldots, a_{j-1}) = b[j]$, so the new value is $\max(b[j], a_j + 1) = c$, which line L9 writes. $\square$

**Theorem (correctness).** SET-PARTITIONS$(n)$ visits each RGS of length $n$ exactly once, in increasing lexicographic order, and stops.

*Proof.* For $n = 0$, line L1 visits the empty string, the one RGS of length $0$. For $n \ge 1$, the first visit is $0^n$, the smallest RGS by Lemma 1. By (B), lines L5 and L6 stop at the largest $j \ge 2$ with $a_j < \beta_j(a)$, or at $j = 1$ if there is none. If $j = 1$, then $a = \omega_n$ by Lemma 1, which is the largest RGS, and the algorithm stops. Otherwise lines L8 and L9 write $a^+$ of Lemma 2, the next RGS in lexicographic order. By induction on the number of steps, the visits are the RGS from $0^n$ up to $\omega_n$ in increasing order, each one time. $\square$

**Lemma 3 (Bell numbers double).** $B_{i+1} \ge 2 B_i$ for $i \ge 1$.

*Proof.* From each partition of $[i]$, form two partitions of $[i + 1]$: add the block $\{i + 1\}$, or add $i + 1$ to the block of $1$. In the first, $i + 1$ is alone in its block; in the second, it shares a block with $1 \ne i + 1$. Removing $i + 1$ gives the original partition back. So the $2 B_i$ partitions are distinct. $\square$

**Theorem (time).** For $n \ge 1$ the loop body of line L6 runs $\sum_{i=1}^{n-1} B_i$ times in total, and the loop of line L9 runs at most as often. For $n \ge 2$, $\sum_{i=1}^{n-1} B_i < B_n$, and SET-PARTITIONS$(n)$ runs in $\Theta(B_n)$ time.

*Proof.* At the visit of $a$, by (B), line L6 runs exactly $s(a)$ times, where $s(a)$ is the largest $s \le n - 1$ such that $a_i = \beta_i(a)$ for the last $s$ indices $i = n - s + 1, \ldots, n$. For $1 \le s \le n - 1$, the RGS with $s(a) \ge s$ are those whose last $s$ entries each equal the running maximum plus $1$. Each such RGS is an arbitrary RGS of length $n - s \ge 1$ followed by the $s$ forced entries, so there are $B_{n-s}$ of them. Hence

$$\sum_a s(a) = \sum_{s=1}^{n-1} \#\{a : s(a) \ge s\} = \sum_{s=1}^{n-1} B_{n-s} = \sum_{i=1}^{n-1} B_i.$$

At each step that does not stop, line L9 runs $n - j = s(a)$ times. So its total is at most the total of line L6.

For $n \ge 2$, Lemma 3 gives $B_i \le 2^{-(n-1-i)} B_{n-1}$ for $1 \le i \le n - 1$, so $\sum_{i=1}^{n-1} B_i < 2 B_{n-1} \le B_n$.

Line L2 takes $O(n)$ time, and each of the $B_n$ passes of the loop takes $O(1)$ time without the loops of lines L6 and L9. So the total time is $O(n + B_n)$. Since $B_n \ge 2^{n-1} \ge n$ for $n \ge 1$ by Lemma 3, this is $O(B_n)$. It is $\Omega(B_n)$ because there are $B_n$ visits. $\blacksquare$
