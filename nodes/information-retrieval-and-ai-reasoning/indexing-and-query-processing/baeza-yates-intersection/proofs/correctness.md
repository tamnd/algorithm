---
title: Baeza-Yates intersection returns the intersection with at most 2 m log2(2 + n/m) + 6 m tests
proves: [correctness]
status: full
---

Both lists are strictly increasing. A call BY$(A[alo..ahi), B[blo..bhi))$ works on the two half-open ranges. A test is one two-way comparison of ids, $<$ or $=$. Line L4 is a binary search for the least index $p$ in $[blo, bhi]$ with $p = bhi$ or $B[p] \ge x$.

**Lemma 1 (binary search).** On a range of $s = bhi - blo$ indices, line L4 returns the index above and makes at most $\lceil \log_2(s + 1) \rceil$ tests.

*Proof.* This is Lemma 2 of the proof file of the [posting list](/posting-list/) page: each test keeps the answer in the range and cuts the size $s$ to at most $\lfloor s/2 \rfloor$, so the size reaches 0 after at most $\lfloor \log_2 s \rfloor + 1 = \lceil \log_2(s+1) \rceil$ tests when $s \ge 1$, and after 0 tests when $s = 0$. $\square$

**Theorem 1 (correctness).** A call BY on the ranges $A[alo..ahi)$ and $B[blo..bhi)$ appends to the output exactly the ids of $A[alo..ahi) \cap B[blo..bhi)$, in increasing order.

*Proof.* By strong induction on the total size $(ahi - alo) + (bhi - blo)$. Line L1 may swap the two ranges; the intersection does not change, so we may assume that $A[alo..ahi)$ is the smaller range. If it is empty, the intersection is empty and line L2 returns with no output. Else line L3 picks $x = A[mid]$ with $alo \le mid < ahi$, and line L4 finds $p$.

Split the common ids into three parts. An id $y < x$ that is in both ranges lies in $A[alo..mid)$, because $A$ is increasing, and in $B[blo..p)$, because each id of $B[p..bhi)$ is at least $x$. An id $y = x$ is in the $B$ range exactly when $p < bhi$ and $B[p] = x$. An id $y > x$ lies in $A[mid+1..ahi)$, and in $B[q..bhi)$, where $q = p + 1$ if $B[p] = x$ and $q = p$ otherwise, because each id of $B[blo..q)$ is at most $x$. Conversely, each id in one of these three parts is common to the two ranges.

Lines L5 and L7 are calls on ranges with a smaller total size, because the index $mid$ is in neither $A$ range. By the induction hypothesis, line L5 appends the ids of the first part in increasing order, line L6 appends $x$ if it is common, and line L7 appends the ids of the third part in increasing order. The ids of the first part are less than $x$ and those of the third part are greater, so the whole output of the call is in increasing order. $\square$

**Theorem 2 (count).** Let $m = \min(|A|, |B|) \ge 1$ and $n = \max(|A|, |B|)$. BY$(A, B)$ makes at most

$$2m \log_2\left(2 + \frac{n}{m}\right) + 6m \;\le\; 2m \log_2\left(1 + \frac{n}{m}\right) + 8m \;\le\; 10 \log_2 \binom{m+n}{m}$$

tests.

*Proof.* Call a node of the recursion tree *working* if, after line L1, its smaller range is not empty. Only working nodes make tests. A working node $v$ whose larger range has $s_v$ indices makes at most $\lceil \log_2(s_v + 1) \rceil$ tests in line L4 and one test in line L6, so at most $\log_2(s_v + 1) + 2$ tests.

*Depth.* Let $a_v$ be the size of the smaller range of $v$. The two children of $v$ get the parts of that range before and after $mid$, of sizes $\lfloor a_v / 2 \rfloor$ and $\lceil a_v / 2 \rceil - 1$, both at most $a_v / 2$. The smaller range of a child is at most the part it gets, so $a$ at least halves from a node to its child. The root has $a = m$, so a working node at depth $\ell$ has $1 \le a \le m / 2^\ell$, which gives $\ell \le L = \lfloor \log_2 m \rfloor$. A level $\ell$ has at most $2^\ell$ nodes.

*Disjoint ranges.* At one depth, the ranges of $A$ of the nodes do not overlap, and the ranges of $B$ do not overlap. This holds at the root, and a call passes to its two children disjoint parts of its own two ranges. So $\sum_v s_v \le m + n$ over the working nodes $v$ of one depth.

*One level.* Let $N_\ell \le 2^\ell$ be the number of working nodes at depth $\ell$. By Jensen's inequality for the concave function $\log_2(1 + y)$, and because $h(t) = t \log_2(1 + c/t)$ is nondecreasing in $t > 0$ for each $c \ge 0$ (its derivative is $\log_2(1 + y) - \frac{y}{(1+y)\ln 2} \ge 0$ with $y = c/t$),

$$\sum_{v \text{ at depth } \ell} \log_2(1 + s_v) \le N_\ell \log_2\left(1 + \frac{m+n}{N_\ell}\right) \le 2^\ell \log_2\left(1 + \frac{m+n}{2^\ell}\right).$$

*All levels.* Write $M = 2^L$, so $m/2 < M \le m$, and put $j = L - \ell$. Since $1 + 2^j y \le 2^j (1 + y)$ for $j \ge 0$ and $y \ge 0$,

$$\sum_{\ell=0}^{L} 2^\ell \log_2\left(1 + \frac{m+n}{2^\ell}\right) = \sum_{j=0}^{L} \frac{M}{2^j} \log_2\left(1 + 2^j \frac{m+n}{M}\right) \le \sum_{j \ge 0} \frac{M}{2^j} \left(\log_2\left(1 + \frac{m+n}{M}\right) + j\right).$$

With $\sum_{j \ge 0} 2^{-j} = 2$ and $\sum_{j \ge 0} j 2^{-j} = 2$, this is at most $2M \log_2(1 + (m+n)/M) + 2M$, and since $h$ is nondecreasing and $M \le m$, it is at most $2m \log_2(2 + n/m) + 2m$. The number of working nodes is at most $\sum_{\ell=0}^{L} 2^\ell = 2^{L+1} - 1 \le 2m - 1$, so the terms "$+2$" add at most $4m$. The total is at most $2m \log_2(2 + n/m) + 6m$.

*The other forms.* From $2 + y \le 2(1 + y)$ for $y \ge 0$, $\log_2(2 + n/m) \le \log_2(1 + n/m) + 1$, which gives the middle form. For the last form, $\binom{m+n}{m} = \prod_{i=1}^{m} \frac{n+i}{i} \ge \left(1 + \frac{n}{m}\right)^m$, so $\log_2 \binom{m+n}{m} \ge m \log_2(1 + n/m)$, and this is at least $m$ because $n \ge m$. So $2m \log_2(1 + n/m) + 8m \le 2 \log_2 \binom{m+n}{m} + 8 \log_2 \binom{m+n}{m}$. $\blacksquare$

**Remark.** The lower bound $\lceil \log_2 \binom{m+n}{m} \rceil$ for every algorithm in the comparison model is proved in the proof file of [adaptive set intersection](/adaptive-set-intersection/). So the method is optimal up to a constant factor of at most 10 for each ratio of the lengths. The constant comes from this proof and is not tight: on 3000 random pairs with $m \le 50$ and $m \le n \le 3000$, no pair used more than half of the bound $2m \log_2(2 + n/m) + 6m$.
