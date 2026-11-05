---
title: The child table scans compute up, down and next, and give the child intervals
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** $L[0 \ldots N]$ has $L[0] = 0$, $L[r] \ge 0$ for $1 \le r < N$ and $L[N] = -1$. The fields $up$, $down$ and $next$ are defined as on the page. Write $\min L(a, b)$ for $\min\{L[r] : a < r < b\}$, with $+\infty$ for an empty range. So $up[q]$ is the smallest $k < q$ with $L[k] > L[q]$ and $\min L(k, q) \ge L[k]$; $down[p]$ is the largest $k > p$ with $L[k] > L[p]$ and $\min L(p, k) > L[k]$; $next[i]$ is the smallest $k > i$ with $L[k] = L[i]$ and $\min L(i, k) > L[i]$.

**Lemma 1 (first stack).** In the first scan, just before rank $i$ is processed, the stack holds, from the bottom, exactly the ranks $k < i$ with $\min L(k, i) \ge L[k]$, that is, the ranks with no smaller value after them before $i$, in increasing order of rank. Their values do not decrease from the bottom.

*Proof.* Induction on $i$. For $i = 1$ the stack is $[0]$ and the claim holds. Suppose it holds for $i$. Rank $k$ stays after step $i$ if and only if $L[k] \le L[i]$ (the pops remove exactly the top ranks with $L[k] > L[i]$, and since the values do not decrease from the bottom, these are all the ranks on the stack with a larger value), and then $i$ is pushed. So after step $i$ the stack holds the ranks $k < i$ with $\min L(k, i) \ge L[k]$ and $L[i] \ge L[k]$, and $i$ itself, which is the claim for $i + 1$. $\square$

**Lemma 2 (up).** The first scan sets $up[i]$ correctly for every $i$.

*Proof.* By Lemma 1, the candidates $k < i$ with $L[k] > L[i]$ and $\min L(k, i) \ge L[k]$ are exactly the stack ranks with a value above $L[i]$. They are the top part of the stack and are popped at step $i$, the smallest rank last. Line L6 stores the last one popped, so $up[i]$ is the smallest candidate. If no rank is popped there is no candidate, and $up[i]$ stays nil; the variable $last$ is reset after each use, so a pop at an earlier step does not leak. $\square$

**Lemma 3 (down).** The first scan sets $down[p]$ correctly for every $p$.

*Proof.* Call $k$ a *candidate* for $p$ if $k > p$, $L[k] > L[p]$ and $\min L(p, k) > L[k]$.

First, a write $down[p] \gets last$ in L5 is a write of a candidate. At that point $last$ was directly above $p$ on the stack, so $L[last] \ge L[p]$, and the test $L[p] \ne L[last]$ gives $L[last] > L[p]$. Take a rank $r$ with $p < r < last$ and suppose $L[r] \le L[last]$. If $r$ was popped before step $last$, it was popped by a rank $s$ with $r < s < last$ and $L[s] < L[r] \le L[last]$; repeat the argument with $s$. This ends with a rank $r^*$ between $p$ and $last$, with $L[r^*] \le L[last]$, that is still on the stack at step $last$. Step $last$ does not pop it, so it lies between $p$ and $last$ on the stack, which is false. So every value between $p$ and $last$ is larger than $L[last]$, and $last$ is a candidate.

Second, every candidate $k$ is pushed directly above $p$: all values between them are larger than $L[k] > L[p]$, so $p$ stays on the stack, and step $k$ pops every rank between them. If $k < k'$ are candidates, then $L[k] > L[k']$, so step $k'$ pops $k$, with $L[i] = L[k'] > L[p]$, and L5 does not write. Let $k^*$ be the largest candidate. It is popped at some step $i$, since $L[N] = -1$. Every rank between $k^*$ and $i$ has a value of at least $L[k^*]$, or it would have popped $k^*$ earlier. If $L[i] > L[p]$, then $i$ would be a candidate larger than $k^*$, so $L[i] \le L[p]$. After the pop, $p$ is the top and $L[p] \ne L[k^*]$, so L5 writes $down[p] \gets k^*$. By the first part no other write to $down[p]$ happens after this one, since $p$ has no candidate after $k^*$, and if $p$ has no candidate, nothing is written. $\square$

**Lemma 4 (next).** The second scan sets $next[i]$ correctly for every $i$.

*Proof.* As in Lemma 1, with one change: a rank with a value equal to $L[i]$ is popped by line L11 and replaced by $i$. So before step $i$, the stack holds the ranks $k < i$ with $\min L(k, i) > L[k]$, with strictly increasing values. At step $i$, after the pops of larger values, the top has $L[top] \le L[i]$. If $L[top] = L[i]$, the top $k$ satisfies $\min L(k, i) > L[k] = L[i]$, and it is the only such rank with this value, so $next[k] = i$, and no smaller $i$ was possible since $k$ was not popped before. If no top has the value $L[i]$, no earlier rank has $next = i$. Each rank is set at most once, when it is popped by an equal value; it is popped by a smaller value otherwise and keeps nil, which is right since every later rank with an equal value has the smaller value in between. $\square$

**Theorem (children).** Let $[i..j]$ be an $\ell$-interval with $\ell$-indices $k_1 < \cdots < k_r$. Then ESA-CHILDREN emits $[i..k_1 - 1], [k_1..k_2 - 1], \ldots, [k_r..j]$.

*Proof.* The $\ell$-indices are the ranks in $i+1 \ldots j$ with $L = \ell$, and all values there are at least $\ell$. For $t < r$, $next[k_t] = k_{t+1}$, since all values between are larger than $\ell$; and $next[k_r]$ is nil, since $L[j+1] < \ell$ lies between $k_r$ and any later rank with the value $\ell$. So L16 and L17 emit the right intervals once $k = k_1$.

For the root $[0..n]$, $\ell = 0 = L[0]$, and $k_1 = next[0]$ is the first rank after 0 with $L = 0$; the chain ends because $L[N] = -1$.

Otherwise $i \ge 1$ or $j < n$, and $L[i] < \ell$, $L[j+1] < \ell$. If $L[i] \le L[j+1]$, then $L[j+1] < \ell$, and the smallest $k < j + 1$ with $L[k] > L[j+1]$ and $\min L(k, j+1) \ge L[k]$ is $k_1$: it qualifies since everything between $k_1$ and $j + 1$ is at least $\ell$; every rank in $i + 1 \ldots k_1 - 1$ has a value above $\ell$ and then $k_1$, with value $\ell$, lies between it and $j + 1$; and rank $i$ and those before it have $L[i] \le L[j+1]$ between or on them. So $up[j+1] = k_1$, which lies in $i + 1 \ldots j$. If $L[i] > L[j+1]$, then rank $j + 1$ has the smaller value $L[j+1] < L[i]$, and $up[j+1]$, if defined, is at most $i$: rank $i$ itself qualifies as a candidate when $\min L(i, j+1) \ge L[i]$, which holds as all values there are at least $\ell > L[i]$. So the test in L14 fails and the algorithm uses $down[i]$. By definition, $down[i]$ is the largest $k > i$ with $L[k] > L[i]$ and only larger values between $i$ and $k$. The rank $k_1$ qualifies. A rank $k > k_1$ inside the interval has $k_1$ between with $\ell \le L[k]$, so it fails, and a rank beyond $j$ has $L[j+1] < \ell$, so either $L[j+1] \le L[i]$ blocks it or $j+1$ itself fails when $L[j+1] < L[i]$, and later ranks have $j + 1$ between. So $down[i] = k_1$.

The case $L[i] \le L[j+1]$ also needs $up[j+1] > i$: any $k \le i$ has rank $i$ or a smaller value between, and $L[i] \le L[j+1]$ is not larger than $L[j+1]$, so $k = i$ fails the first condition, and a $k < i$ with $L[k] > L[j+1] \ge L[i]$ fails the second, since $L[i] < L[k]$ lies between. $\square$

**Time and termination.** Each scan pushes each rank once and pops it at most once, so each takes $O(N)$ time and ends. ESA-CHILDREN takes $O(1)$ time per child, since every $next$ step moves to a larger rank inside $[i..j]$. Find takes $O(\sigma)$ time per node for the child scan, at most $m + 1$ nodes, and $O(m)$ symbol comparisons in all, so $O(m\sigma)$. $\blacksquare$
