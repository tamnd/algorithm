---
title: The Fenwick tree keeps its invariant and returns prefix sums
proves: [correctness, termination]
status: full
---

Let $(G, +, 0)$ be an abelian group. For $i \ge 1$, $\operatorname{lowbit}(i)$ is the largest power of two that divides $i$, and $R(i) = (i - \operatorname{lowbit}(i), i] \cap \mathbb{Z}$. The invariant is

> **(F)** $T[i] = \sum_{k \in R(i)} A[k]$ for each $1 \le i \le n$.

**Lemma 1 (dyadic ranges).** Let $\operatorname{lowbit}(i) = 2^t$. Then $i = (2m + 1) 2^t$ for an integer $m \ge 0$, and $R(i) = (2m \cdot 2^t, (2m + 1) 2^t]$. For any $i, j \ge 1$, the ranges $R(i)$ and $R(j)$ are disjoint, or one is a subset of the other.

*Proof.* The first part is the definition of $\operatorname{lowbit}$: $i / 2^t$ is odd. Each range has the form $(a 2^t, (a + 1) 2^t]$ with integers $a \ge 0$ and $t \ge 0$. Take two such ranges with $t \le u$, say $(a 2^t, (a+1)2^t]$ and $(b 2^u, (b+1) 2^u]$. The points $b 2^u$ and $(b+1) 2^u$ are multiples of $2^t$, so they are not strictly inside the first range. Hence the first range lies entirely inside the second one or entirely outside it. $\square$

**Lemma 2 (the PREFIX chain).** Let $0 \le i \le n$, and let $i_0 = i$ and $i_{s+1} = i_s - \operatorname{lowbit}(i_s)$ while $i_s > 0$. The chain reaches 0 after exactly $p$ steps, where $p$ is the number of set bits of $i$, and $(0, i]$ is the disjoint union of $R(i_0), R(i_1), \ldots, R(i_{p-1})$.

*Proof.* Subtracting $\operatorname{lowbit}(i_s)$ clears the lowest set bit of $i_s$ and changes no other bit. So the number of set bits drops by exactly one at each step, and the chain reaches 0 after $p$ steps. By definition $R(i_s) = (i_{s+1}, i_s]$. These ranges are adjacent and in decreasing order, so their union is $(i_p, i_0] = (0, i]$, and they are disjoint. $\square$

**Lemma 3 (the ADD chain).** Let $1 \le i \le n$, and let $c_0 = i$ and $c_{s+1} = c_s + \operatorname{lowbit}(c_s)$. Then $\operatorname{lowbit}(c_{s+1}) \ge 2 \operatorname{lowbit}(c_s)$, and for $1 \le j \le n$: $i \in R(j)$ if and only if $j = c_s$ for some $s$.

*Proof.* Let $c = c_s$ and $\operatorname{lowbit}(c) = 2^t$. Write $c = P + (2^r - 1) 2^t$, where $r \ge 1$ is the number of consecutive set bits of $c$ from bit $t$ upwards, so bit $t + r$ of $c$ is 0 and $P$ is a multiple of $2^{t + r + 1}$. Then $c + 2^t = P + 2^{t+r}$, so $\operatorname{lowbit}(c_{s+1}) = 2^{t+r} \ge 2^{t+1}$. Also $c_{s+1} - \operatorname{lowbit}(c_{s+1}) = P \le c - 2^t$, so $R(c_s) \subseteq R(c_{s+1})$.

*If.* $i \in R(c_0)$, and the ranges grow along the chain, so $i \in R(c_s)$ for each $s$.

*Only if.* Let $i \in R(j)$ with $1 \le j \le n$. Then $j \ge i = c_0$. The chain increases strictly, so either $j = c_s$ for some $s$, or there is an $s$ with $c_s < j < c_{s+1}$. Assume the second case. The point $i$ lies in $R(c_s)$ and in $R(j)$, so by Lemma 1 one holds the other. $R(j)$ cannot lie inside $R(c_s)$, because $j \in R(j)$ and $j > c_s = \max R(c_s)$. So $R(c_s) \subsetneq R(j)$, which forces $\operatorname{lowbit}(j) > \operatorname{lowbit}(c_s) = 2^t$, so $j$ is a multiple of $2^{t+1}$. But $c_s$ is an odd multiple of $2^t$, so $c_{s+1} = c_s + 2^t$ is the least multiple of $2^{t+1}$ that is larger than $c_s$. Then $c_s < j < c_{s+1}$ is impossible. $\square$

**Theorem 1 (PREFIX).** If (F) holds, PREFIX$(T, i)$ returns $A[1] + \cdots + A[i]$ for $0 \le i \le n$, after at most $\lfloor \lg n \rfloor + 1$ rounds.

*Proof.* The loop of lines L5 to L7 visits the chain of Lemma 2 and stops when $i = 0$. Its invariant is $s = \sum_{k \in (i, i_0]} A[k]$ for the current $i$: it holds with $s = 0$ and $i = i_0$, and a round adds $T[i] = \sum_{k \in R(i)} A[k]$ by (F) and moves $i$ to the lower end of $R(i)$. At the end $i = 0$, so $s = \sum_{k \in (0, i_0]} A[k]$. The number of rounds is the number of set bits of $i_0 \le n$, which is at most $\lfloor \lg n \rfloor + 1$. $\square$

**Theorem 2 (ADD).** If (F) holds for $A$, then after ADD$(T, n, i, \delta)$ it holds for $A'$, where $A'[i] = A[i] + \delta$ and $A'[k] = A[k]$ for $k \ne i$. The loop runs at most $\lfloor \lg n \rfloor + 1$ times.

*Proof.* For each $j$, $\sum_{k \in R(j)} A'[k]$ is $\sum_{k \in R(j)} A[k] + \delta$ if $i \in R(j)$, and is unchanged otherwise. Lines L1 to L3 add $\delta$ to $T[c_s]$ for each $c_s \le n$ of the chain of Lemma 3, and to no other cell. By Lemma 3 these are exactly the $j \le n$ with $i \in R(j)$. By Lemma 3 again, $\operatorname{lowbit}(c_s) \ge 2^s$, and $c_s \ge \operatorname{lowbit}(c_s)$, so $c_s > n$ once $2^s > n$. So at most $\lfloor \lg n \rfloor + 1$ indices of the chain are at most $n$. $\square$

**Theorem 3 (RANGE).** If (F) holds, RANGE$(T, l, r)$ returns $A[l] + \cdots + A[r]$.

*Proof.* By Theorem 1, line L9 computes $\sum_{k=1}^{r} A[k] - \sum_{k=1}^{l-1} A[k] = \sum_{k=l}^{r} A[k]$. The subtraction is defined because $G$ is a group. $\square$

**Theorem 4 (BUILD).** After BUILD$(A, n)$, (F) holds.

*Proof.* For $j \le n$, call $i < j$ a *child* of $j$ if $i + \operatorname{lowbit}(i) = j$. We first show that $R(j) = \{j\} \cup \bigcup_{i \text{ child of } j} R(i)$, with a disjoint union. Let $\operatorname{lowbit}(j) = 2^u$. If $u = 0$, then $R(j) = \{j\}$, and $j$ has no child, because $i + \operatorname{lowbit}(i)$ is even for each $i$. If $u \ge 1$, the children of $j$ are $j - 2^v$ for $0 \le v < u$: for such $i = j - 2^v$, $\operatorname{lowbit}(i) = 2^v$ and $i + 2^v = j$, and conversely $i + \operatorname{lowbit}(i) = j$ with $\operatorname{lowbit}(i) = 2^v$ gives $i = j - 2^v$ and needs $v < u$. Then $R(j - 2^v) = (j - 2^{v+1}, j - 2^v]$, and these ranges for $v = 0, \ldots, u - 1$ together with $\{j\}$ are disjoint and cover $(j - 2^u, j] = R(j)$.

Line L10 sets $T[j] = A[j]$. In the loop, $T[j]$ changes only at line L13, in the round of a child $i$ of $j$, and each child has $i < j$. So after round $j - 1$, the cell $T[j]$ never changes again. We claim that when round $i$ starts, $T[i] = \sum_{k \in R(i)} A[k]$, by strong induction on $i$. When round $i$ starts, the rounds of all children $i'$ of $i$ are done, and each of them added the value $T[i']$ that it had at the start of its own round, which is $\sum_{k \in R(i')} A[k]$ by the hypothesis. No other round has changed $T[i]$. So $T[i] = A[i] + \sum_{i' \text{ child of } i} \sum_{k \in R(i')} A[k]$. By the decomposition, this is $\sum_{k \in R(i)} A[k]$. After the last round, each $T[i]$ keeps this value, so (F) holds. $\square$

**Theorem 5 (SEARCH).** Assume (F) and $A[k] \ge 0$ for each $k$, in an ordered abelian group. Let $s_0$ be the input $s$. SEARCH returns the least $i \in \{1, \ldots, n\}$ with PREFIX$(i) \ge s_0$, or $n + 1$ if there is none.

*Proof.* Let $2^K$ be the largest power of two at most $n$. Write $P(i)$ for PREFIX$(i)$. Since $A \ge 0$, $P$ does not decrease. Let $q$ be the largest index in $\{0, \ldots, n\}$ with $P(q) < s_0$, which exists if $s_0 > 0$; if $s_0 \le 0$, put $q = 0$. The answer is $q + 1$. We show by a loop invariant that $pos = q$ at the end. Before the test with $step = 2^t$:

> **(S)** $pos$ is a multiple of $2^{t+1}$, $pos \le q < pos + 2^{t+1}$, and $s = s_0 - P(pos)$.

At the start, $pos = 0$, $t = K$, and $q \le n < 2^{K+1}$, so (S) holds. Assume (S) before a test. Since $pos$ is a multiple of $2^{t+1}$, $\operatorname{lowbit}(pos + 2^t) = 2^t$ and $R(pos + 2^t) = (pos, pos + 2^t]$. So, if $pos + 2^t \le n$, then $T[pos + 2^t] = P(pos + 2^t) - P(pos)$, and the test $T[pos + 2^t] < s$ is the test $P(pos + 2^t) < s_0$.

- If $pos + 2^t \le n$ and $P(pos + 2^t) < s_0$, then $q \ge pos + 2^t$ by the choice of $q$, and line L17 sets $pos \leftarrow pos + 2^t$ and keeps $s = s_0 - P(pos)$.
- If $pos + 2^t \le n$ and $P(pos + 2^t) \ge s_0$, then $q < pos + 2^t$, because $P$ does not decrease, and $pos$ does not change.
- If $pos + 2^t > n$, then $q \le n < pos + 2^t$, and $pos$ does not change.

In each case $pos$ is now a multiple of $2^t$ and $pos \le q < pos + 2^t$, which is (S) for the next value $t - 1$ of the exponent. After the test with $step = 1$, this gives $pos \le q < pos + 1$, so $pos = q$, and line L19 returns $q + 1$. The loop makes $K + 1 = \lfloor \lg n \rfloor + 1$ tests. $\blacksquare$
