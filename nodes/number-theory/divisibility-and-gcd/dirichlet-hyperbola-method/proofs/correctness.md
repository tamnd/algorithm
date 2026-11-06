---
title: The hyperbola method returns D(n) after exactly floor(sqrt n) divisions
proves: [correctness, termination, time.worst, time.best]
status: full
---

We use the pseudocode HYPERBOLA-D of the page. For an integer $n$, $D(n) = \sum_{k=1}^{n} d(k)$, where $d(k)$ is the number of positive divisors of $k$, and $D(n) = 0$ for $n \le 0$.

**Lemma 1 (pairs).** For $n \ge 1$ let $P = \{ (a, b) \in \mathbb{Z}_{\ge 1}^2 : ab \le n \}$. Then $|P| = D(n)$.

*Proof.* The map $(a, b) \mapsto ab$ sends $P$ to $\{1, \ldots, n\}$. The pairs with $ab = k$ are the $(a, k/a)$ with $a$ a positive divisor of $k$, so there are $d(k)$ of them. Summing over $k \le n$ gives $|P| = D(n)$. $\square$

**Lemma 2 (columns).** For $a \ge 1$, the number of $b \ge 1$ with $ab \le n$ is $\lfloor n/a \rfloor$.

*Proof.* $ab \le n$ if and only if $b \le n/a$, and the positive integers $b \le n/a$ are $1, \ldots, \lfloor n/a \rfloor$. $\square$

**Theorem 1 (correctness).** HYPERBOLA-D$(n)$ returns $D(n)$.

*Proof.* If $n \le 0$, line L1 returns $0 = D(n)$. Let $n \ge 1$. Line L2 sets $s$ with $s^2 \le n < (s + 1)^2$, so $s \ge 1$.

*Loop invariant.* At the start of the iteration with value $a$ of line L4, $t = \sum_{a' = 1}^{a - 1} \lfloor n/a' \rfloor$. It holds for $a = 1$ with $t = 0$ (line L3), and line L5 adds the term for $a$, so it holds for $a + 1$. When the loop ends, $t = \sum_{a=1}^{s} \lfloor n/a \rfloor$.

Let $A = \{ (a, b) \in P : a \le s \}$ and $B = \{ (a, b) \in P : b \le s \}$.

1. By Lemma 2, $|A| = \sum_{a \le s} \lfloor n/a \rfloor = t$.
2. The swap $(a, b) \mapsto (b, a)$ is a bijection of $P$ onto itself, since $ab = ba$, and it maps $A$ onto $B$. So $|B| = t$.
3. $A \cup B = P$: if $(a, b) \in P$ with $a \ge s + 1$ and $b \ge s + 1$, then $ab \ge (s + 1)^2 > n$, which is false.
4. $A \cap B = \{1, \ldots, s\}^2$: each pair with $a, b \le s$ has $ab \le s^2 \le n$, so it is in $P$, and it is in $A$ and in $B$; the converse is the definition. So $|A \cap B| = s^2$.

By inclusion and exclusion and Lemma 1, $D(n) = |P| = |A| + |B| - |A \cap B| = 2t - s^2$, which line L6 returns. $\square$

**Theorem 2 (general form).** Let $f, g$ be functions on the positive integers, $F(x) = \sum_{a \le x} f(a)$ and $G(x) = \sum_{b \le x} g(b)$. For $n \ge 1$ and $s = \lfloor \sqrt n \rfloor$,

$$\sum_{(a, b) \in P} f(a) g(b) = \sum_{a \le s} f(a) G(\lfloor n/a \rfloor) + \sum_{b \le s} g(b) F(\lfloor n/b \rfloor) - F(s) G(s).$$

*Proof.* Give the point $(a, b)$ the weight $f(a) g(b)$. By Lemma 2, the weight of the column $a$ is $f(a) G(\lfloor n/a \rfloor)$, so the weight of $A$ is the first sum. In the same way the weight of the row $b$ is $g(b) F(\lfloor n/b \rfloor)$, and the weight of $B$ is the second sum. The weight of $A \cap B = \{1, \ldots, s\}^2$ is $\sum_{a \le s} \sum_{b \le s} f(a) g(b) = F(s) G(s)$. Facts 3 and 4 above hold as before, so inclusion and exclusion for weights gives the formula. With $f = g = 1$ the left side is $D(n)$ and the formula reduces to Theorem 1. $\square$

**Theorem 3 (cost).** For $n \ge 1$ the loop of lines L4 and L5 runs exactly $\lfloor \sqrt n \rfloor$ times, with one division and one addition per iteration, and the algorithm uses $O(1)$ words besides the input.

*Proof.* The loop runs over $a = 1, \ldots, s$ with no early exit, so it terminates after exactly $s$ iterations, and $\sqrt n - 1 < s \le \sqrt n$. The variables are $s$, $t$ and $a$. So the time is $\Theta(\sqrt n)$ word operations in every case, best and worst alike, plus the cost of the integer square root of line L2, which Newton's method computes in $O(\log n)$ steps. For $n \le 0$ the time is $O(1)$. $\blacksquare$
