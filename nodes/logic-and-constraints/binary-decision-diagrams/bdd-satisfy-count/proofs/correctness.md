---
title: SATCOUNT returns the number of satisfying assignments of f
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order. Each node $u$ of an [ordered BDD](/ordered-binary-decision-diagram/) has a level $\mathrm{var}(u)$, and a terminal has level $n + 1$. The function of an inner node $u = (i, l, h)$ is $f_u = (\neg x_i \wedge f_l) \vee (x_i \wedge f_h)$, with $i < \mathrm{var}(l)$ and $i < \mathrm{var}(h)$. The terminal $0$ has the function $0$, and the terminal $1$ has the function $1$. For a level $k$, let $V_k = \{x_k, \ldots, x_n\}$, so $V_{n+1}$ is empty.

**Lemma 1 (support).** $f_u$ depends only on the variables in $V_{\mathrm{var}(u)}$.

*Proof.* By induction from the bottom. A terminal depends on no variable. For $u = (i, l, h)$, $f_l$ depends only on $V_{\mathrm{var}(l)} \subseteq V_{i+1}$ and $f_h$ depends only on $V_{\mathrm{var}(h)} \subseteq V_{i+1}$, so $f_u$ depends only on $\{x_i\} \cup V_{i+1} = V_i$. $\square$

Because of Lemma 1, $f_u$ is a function on the assignments to $V_{\mathrm{var}(u)}$. Let $N(u)$ be the number of these assignments where $f_u = 1$.

**Lemma 2 (free variables).** If $g$ depends only on $V_k$ and $j \leq k$, then the number of assignments to $V_j$ where $g = 1$ is $2^{k - j}$ times the number of assignments to $V_k$ where $g = 1$.

*Proof.* An assignment to $V_j$ is a pair: an assignment to $x_j, \ldots, x_{k-1}$, and an assignment to $V_k$. The value of $g$ depends only on the second part. There are $2^{k-j}$ choices for the first part. $\square$

**Lemma 3 (COUNT).** COUNT$(u)$ returns $N(u)$.

*Proof.* By induction on the number of nodes below $u$. Lines L2 and L3 handle the terminals: $V_{n+1}$ is empty, so it has one assignment, and $N(0) = 0$ and $N(1) = 1$. A memo hit at line L4 returns a value that line L7 stored for the same $u$. Now let $u = (i, l, h)$ at line L5. Split the assignments to $V_i$ by the value of $x_i$. The assignments with $x_i = 0$ are the assignments to $V_{i+1}$, and on them $f_u = f_l$. By Lemma 1, $f_l$ depends only on $V_{\mathrm{var}(l)}$, and $\mathrm{var}(l) \geq i + 1$. By Lemma 2 with $j = i + 1$ and $k = \mathrm{var}(l)$, the number of these assignments where $f_u = 1$ is $N(l) \cdot 2^{\mathrm{var}(l) - i - 1}$, and by induction COUNT$(l) = N(l)$. In the same way, the assignments with $x_i = 1$ give $N(h) \cdot 2^{\mathrm{var}(h) - i - 1}$. Line L6 adds the two parts, so $c = N(u)$. $\square$

**Theorem.** SATCOUNT$(f)$ returns $\lvert \{ a \in \{0,1\}^n : f(a) = 1 \} \rvert$.

*Proof.* By Lemma 3, COUNT$(f) = N(f)$, the count over $V_{\mathrm{var}(f)}$. The full set of variables is $V_1$, and by Lemma 1 and Lemma 2 with $j = 1$ and $k = \mathrm{var}(f)$, the count over $V_1$ is $N(f) \cdot 2^{\mathrm{var}(f) - 1}$. This is the value that line L1 returns. $\blacksquare$

The proof does not use the reduction rules. The algorithm is correct on every ordered BDD, reduced or not.

**Cost.** A node passes line L4 without a memo hit at most once, because line L7 stores its value. Each such pass makes two recursive calls, so there are at most $2\lvert f \rvert + 1$ calls in total. Each call does $O(1)$ steps and at most two shifts and one addition. With a memo indexed by node number, SATCOUNT does $O(\lvert f \rvert)$ arithmetic operations. Every value is at most $2^n$, so each operation is on integers of at most $n + 1$ bits, and the bit cost is $O(n \cdot \lvert f \rvert)$.

**The 1986 formula.** Bryant (1986) printed the exponents as $\mathrm{var}(l) - i$ and $\mathrm{var}(h) - i$, without the $-1$. With that formula, an induction like the one in Lemma 3 shows that the value of an inner node $u$ is the sum, over the paths from $u$ to the terminal $1$, of $2^{k}$ times the number of models that the path gives, where $k$ is the number of inner nodes on the path. So every function that is not a constant gets a count that is too large. For example, for $f = x_n$ the formula gives $\alpha = 2$ and $|S_f| = 2 \cdot 2^{n-1} = 2^n$, but $x_n$ has $2^{n-1}$ models.
