---
title: The Calkin-Wilf tree lists each positive rational once in lowest terms, and its operations are correct
proves: [correctness, time.children, time.parent, time.next, time.at, time.index_of]
status: full
---

The tree $T$ has root $1/1$, and the node $(a, b)$ has left child $(a, a + b)$ and right child $(a + b, b)$. Nodes are numbered in breadth-first order: the root is $1$, and the children of node $m$ are $2m$ (left) and $2m + 1$ (right). We write $v(n)$ for the pair at node $n$. The pseudocode is that of the page.

**Lemma 1 (values are positive and reduced).** Every $v(n) = (a, b)$ has $a, b \ge 1$ and $\gcd(a, b) = 1$. Every node other than the root has $a \ne b$; left children have $a < b$ and right children $a > b$.

*Proof.* By induction on $n$. The root $(1, 1)$ is reduced. If $(a, b)$ is positive and reduced, then $\gcd(a, a + b) = \gcd(a, b) = 1$ and $\gcd(a + b, b) = \gcd(a, b) = 1$, and both children are positive. In the left child $a < a + b$, and in the right child $a + b > b$. $\square$

**Theorem 1 (every positive rational once).** For each pair $a, b \ge 1$ with $\gcd(a, b) = 1$ there is exactly one $n$ with $v(n) = (a, b)$.

*Proof.* By strong induction on $s = a + b$. If $s = 2$, then $(a, b) = (1, 1)$. It is $v(1)$, and by Lemma 1 no other node has $a = b$. Let $s \ge 3$, so $a \ne b$ (since $a = b$ and $\gcd(a, b) = 1$ give $a = b = 1$).

*Existence.* If $a < b$, the pair $(a, b - a)$ is positive, reduced (as $\gcd(a, b - a) = \gcd(a, b)$) and has sum $b < s$. By induction it is $v(m)$ for some $m$, and its left child is $(a, b) = v(2m)$. If $a > b$, the same argument with $(a - b, b)$ and the right child gives $(a, b) = v(2m + 1)$.

*Uniqueness.* Let $v(n) = (a, b)$. Then $n \ne 1$ since $(a, b) \ne (1, 1)$, so $v(n)$ is a child of $v(\lfloor n/2 \rfloor)$. By Lemma 1, it is a left child if $a < b$ and a right child if $a > b$; so $n$ is even exactly when $a < b$, and the parent $v(\lfloor n/2 \rfloor)$ is $(a, b - a)$ or $(a - b, b)$, determined by $(a, b)$. By induction, that parent pair is $v(m)$ for exactly one $m$, so $\lfloor n/2 \rfloor = m$, and the parity of $n$ is fixed, which determines $n$. $\square$

**Theorem 2 (fusc).** Let $f(0) = 0$, $f(1) = 1$, $f(2m) = f(m)$, $f(2m + 1) = f(m) + f(m + 1)$. Then $v(n) = (f(n), f(n + 1))$ for all $n \ge 1$.

*Proof.* By induction on $n$. $v(1) = (1, 1) = (f(1), f(2))$. If $v(m) = (f(m), f(m + 1))$, then $v(2m) = (f(m), f(m) + f(m + 1)) = (f(2m), f(2m + 1))$ and $v(2m + 1) = (f(m) + f(m + 1), f(m + 1)) = (f(2m + 1), f(2m + 2))$. $\square$

**Theorem 3 (CW-CHILDREN and CW-PARENT).** Line L1 returns the children by definition. For a node $(a, b)$, CW-PARENT returns NIL exactly at the root and the parent otherwise.

*Proof.* By Lemma 1, $a = b$ only at the root. If $a < b$, the node is a left child of $(a, b - a)$, and if $a > b$, a right child of $(a - b, b)$, as in the uniqueness part of Theorem 1. $\square$

**Theorem 4 (CW-AT).** For $n \ge 1$, CW-AT$(n)$ returns $v(n)$.

*Proof.* Write $n = 1 c_1 c_2 \cdots c_d$ in binary, and let $n_j = 1 c_1 \cdots c_j$, so $n_0 = 1$, $n_d = n$, and $n_j = 2 n_{j-1} + c_j$. Invariant: after processing $c_1, \ldots, c_j$, $(a, b) = v(n_j)$. It holds for $j = 0$ by line L5. If it holds for $j - 1$, then $n_j$ is the left child of $n_{j-1}$ when $c_j = 0$ and the right child when $c_j = 1$, and line L7 replaces $(a, b)$ by that child. After the last digit, $(a, b) = v(n)$. $\square$

**Theorem 5 (CW-INDEX).** For $a, b \ge 1$, CW-INDEX$(a, b)$ returns the $n$ with $v(n) = (a, b)$ if $\gcd(a, b) = 1$, and reports an error otherwise.

*Proof.* Let $(a_0, b_0)$ be the input and $g = \gcd(a_0, b_0)$. The loop keeps the invariant

> **(I)** $a, b \ge 1$, $\gcd(a, b) = g$, and if $g = 1$ then $(a, b) = v(m)$ for the $m$ such that $v(N) = (a_0, b_0)$ has the binary form $N = m \cdot 2^{len} + n$ with $0 \le n < 2^{len}$; that is, $n$ holds the last $len$ digits of the path and $m$ is the ancestor $len$ levels up.

At the start $n = len = 0$, $(a, b) = (a_0, b_0)$, and (I) holds with $m = N$.

Consider one pass with $a > b$ (line L11). Let $q = \lceil a/b \rceil - 1$, so $q \ge 1$ and $0 < a - qb \le b$. For $0 \le j < q$, the pair $(a - jb, b)$ has first entry $a - jb > b$, so it is a right child and its parent is $(a - (j + 1)b, b)$. So $q$ parent steps from $v(m)$ pass through right children only, and reach $(a - qb, b) = v(\lfloor m / 2^q \rfloor)$, with $m \bmod 2^q = 2^q - 1$, the $q$ digits $1$. Line L11 adds these digits above the $len$ digits already found, and line L13 increases $len$ by $q$, so (I) holds again. The gcd is kept since $\gcd(a - qb, b) = \gcd(a, b)$. The case $a < b$ of line L12 is symmetric, with left children and digits $0$.

*Termination.* Each pass lowers $a + b$ by at least $\min(a, b) \ge 1$, so the loop stops, with $a = b$. Then $\gcd(a, b) = a = g$. If $g \ne 1$, line L14 reports the error, which is right by Theorem 1 and Lemma 1, since non-reduced pairs are not nodes. If $g = 1$, then $(a, b) = (1, 1) = v(1)$, so $m = 1$ and $N = 2^{len} + n$, which line L15 returns. $\square$

**Theorem 6 (CW-NEXT, Newman's formula).** For $n \ge 1$ let $x_n = f(n)/f(n + 1)$ be the value of node $n$. Then $x_{n+1} = 1/(2\lfloor x_n \rfloor - x_n + 1)$, and line L17 returns $v(n + 1)$.

*Proof.* Let $N(x) = 1/(2\lfloor x \rfloor - x + 1)$; the denominator is positive because $x - \lfloor x \rfloor < 1$. We use induction on $n$. For $n = 1$: $N(1) = 1/2 = x_2$.

*Case $n = 2m$ even.* Node $n$ is the left child of node $m$; write $x_m = u/w$. Then $x_n = u/(u + w) < 1$, $\lfloor x_n \rfloor = 0$, and $N(x_n) = 1/(1 - u/(u + w)) = (u + w)/w$, which is the right child of node $m$, node $2m + 1 = n + 1$.

*Case $n = 2m + 1$ odd, $m \ge 1$.* Node $n$ is the right child of node $m$, so $x_n = x_m + 1$ and $\lfloor x_n \rfloor = \lfloor x_m \rfloor + 1$. Node $n + 1 = 2(m + 1)$ is the left child of node $m + 1$, and a left child of a node with value $y$ has value $y/(1 + y) = 1/(1 + 1/y)$. By induction, $x_{m+1} = N(x_m)$, so $1/x_{m+1} = 2\lfloor x_m \rfloor - x_m + 1$ and

$$x_{n+1} = \frac{1}{1 + 2\lfloor x_m \rfloor - x_m + 1} = \frac{1}{2(\lfloor x_n \rfloor - 1) - (x_n - 1) + 2} = \frac{1}{2\lfloor x_n \rfloor - x_n + 1} = N(x_n).$$

*Integers.* For $x_n = a/b$ in lowest terms and $q = \lfloor a/b \rfloor$, $N(a/b) = b/((2q + 1)b - a)$, and $(2q + 1)b - a > (2q + 1)b - (q + 1)b = qb \ge 0$ because $a < (q + 1)b$. And $\gcd(b, (2q + 1)b - a) = \gcd(b, a) = 1$, so line L17 returns the reduced pair, which by Theorem 1 is $v(n + 1)$. $\square$

**Theorem 7 (depth and cost).** Let $a/b = [a_0; a_1, \ldots, a_k]$ be the regular continued fraction, with $a_k \ge 2$ unless $a/b = 1$. The loop of CW-INDEX runs at most $k + 1$ times, and the depth of $a/b$ is $a_0 + \cdots + a_k - 1$. Each of CW-CHILDREN, CW-PARENT and CW-NEXT uses $O(1)$ arithmetic operations, and CW-AT$(n)$ uses $\lfloor \lg n \rfloor$ additions.

*Proof.* The values of $q$ in the passes are the non-zero quotients of the Euclidean algorithm on $(a, b)$ (only $a_0$ can be zero), except that when $b \mid a$ (or $a \mid b$) the quotient is reduced by $1$ and the pass ends at $(b, b)$ instead of $(b, 0)$. So the passes correspond to the division steps, at most $k + 1$, and the sum of the $q$ is $a_0 + \cdots + a_k - 1$: all quotients, with the last one reduced by $1$. By Theorem 5 this sum is $len$, the depth. The other counts are read from the pseudocode: CW-AT does one addition for each of the $\lfloor \lg n \rfloor$ digits after the leading one, and each other operation is a fixed number of additions, subtractions, comparisons and at most one division. $\blacksquare$
