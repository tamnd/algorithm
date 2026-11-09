---
title: The counter and the recursion visit each subset once, in binary counting order
proves: [correctness]
status: full
---

For a bit vector $x[0 \ldots n-1]$ let $\mathrm{val}(x) = \sum_{j=0}^{n-1} x[j]\, 2^j$. The map $x \mapsto \{j + 1 : x[j] = 1\}$ is a bijection from $\{0, 1\}^n$ to the subsets of $[n]$, and $\mathrm{val}$ is a bijection from $\{0, 1\}^n$ to $\{0, 1, \ldots, 2^n - 1\}$. So it is enough to show that both procedures visit the vectors with values $0, 1, \ldots, 2^n - 1$, in this order, each once.

**Lemma 1 (one increment).** Assume that $x[n] = 0$ and $v = \mathrm{val}(x)$ before line L4. If $v < 2^n - 1$, then after lines L4 to L7 we have $\mathrm{val}(x) = v + 1$ and $x[n] = 0$. If $v = 2^n - 1$, line L6 returns.

*Proof.* Let $t$ be the number of trailing ones of $x$: $x[0] = \cdots = x[t-1] = 1$ and $x[t] = 0$. Such a $t \le n$ exists because $x[n] = 0$. The loop of line L5 keeps this invariant: at its test, $x[0 \ldots j-1]$ are $0$, $x[j \ldots t-1]$ are still $1$, and the other entries are not changed. The loop stops exactly when $j = t$.

If $v = 2^n - 1$, then $x[0 \ldots n-1]$ are all $1$, so $t = n$, and line L6 returns. Otherwise $x$ has a $0$ in $x[0 \ldots n-1]$, so $t < n$, and line L7 sets $x[t] \leftarrow 1$. The new value is
$$v - \sum_{j=0}^{t-1} 2^j + 2^t = v - (2^t - 1) + 2^t = v + 1.$$
Line L7 writes an index $t < n$, so $x[n]$ stays $0$. $\square$

**Theorem 1 (counter).** SUBSETS-COUNTER$(n)$ visits the vectors with values $0, 1, \ldots, 2^n - 1$, in this order, and then stops.

*Proof.* Line L1 makes $\mathrm{val}(x) = 0$ and $x[n] = 0$. By Lemma 1 and induction on the number of visits, the $v$-th visit, counted from $0$, sees $\mathrm{val}(x) = v$, for $v = 0, 1, \ldots, 2^n - 1$. After the visit with $v = 2^n - 1$, Lemma 1 says that line L6 returns. The values are distinct, so no vector is visited twice. $\blacksquare$

**Theorem 2 (recursion).** Let $0 \le i \le n$ and let the entries $x[i \ldots n-1]$ be fixed, with $F = \sum_{j=i}^{n-1} x[j]\, 2^j$. Then EXTEND$(i)$ visits the $2^i$ vectors with these entries at positions $i$ to $n-1$, in increasing order of value, that is, the values $F, F + 1, \ldots, F + 2^i - 1$. It does not change $x[i \ldots n-1]$.

*Proof.* By induction on $i$. For $i = 0$, line L9 visits the one vector, with value $F$, and returns.

For $i \ge 1$, line L10 sets $x[i-1] = 0$ and calls EXTEND$(i - 1)$. The fixed part of that call is $x[i-1 \ldots n-1]$, with value $F$. By the induction hypothesis the call visits the values $F, \ldots, F + 2^{i-1} - 1$ in order and does not change $x[i-1 \ldots n-1]$. Line L11 sets $x[i-1] = 1$, so the fixed part has value $F + 2^{i-1}$, and the second call visits $F + 2^{i-1}, \ldots, F + 2^i - 1$ in order. Together, the two calls visit $F, \ldots, F + 2^i - 1$ in order. Lines L10 and L11 write only $x[i-1]$, and the calls write only entries below $i - 1$, so $x[i \ldots n-1]$ does not change. $\square$

**Corollary.** SUBSETS-RECURSIVE$(n)$ calls EXTEND$(n)$ with an empty fixed part, $F = 0$. By Theorem 2 it visits the values $0, \ldots, 2^n - 1$ in order. So it visits each subset once, in the same order as SUBSETS-COUNTER. $\blacksquare$

**Cost.** In SUBSETS-COUNTER, line L7 runs once for each visit except the last, so $2^n - 1$ times. Each run of the body of line L5 changes a $1$ to a $0$, and each $1$ was made by line L7, because line L1 makes all entries $0$. After the final scan all entries are $0$ again, so the number of runs of the body of line L5 is also $2^n - 1$. EXTEND$(i)$ for $i \ge 1$ makes two calls with argument $i - 1$, so the calls form a complete binary tree of height $n$, with $2^{n+1} - 1$ nodes.
