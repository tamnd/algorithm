---
title: IS-FREE detects repeated tests, COUNT counts the models of a free diagram, ARITH computes the multilinear extension, and PROBABLY-EQUAL has one-sided error at most (n/p)^t
proves: [correctness]
status: full
---

A diagram has the sinks 0 and 1 and inner nodes $u$ with a variable $\mathrm{var}(u)$ and children $\mathrm{lo}(u), \mathrm{hi}(u)$. The function of a node is $f_0 = 0$, $f_1 = 1$ and $f_u(x) = f_{\mathrm{lo}(u)}(x)$ if $x_{\mathrm{var}(u)} = 0$ and $f_{\mathrm{hi}(u)}(x)$ otherwise. The store is acyclic, since children have smaller ids. TOPO$(r)$ lists every inner node reachable from $r$ after its children, so in each loop below the values of the children are ready when a node is handled. For a node $u$, let $\mathrm{Var}(u)$ be the set of variables tested at some node reachable from $u$, with $u$ itself; $\mathrm{Var}$ of a sink is empty. The diagram below $r$ is *free* if no path from $r$ contains two nodes with the same variable.

**Lemma 1 (EVALUATE).** EVALUATE$(u, x)$ returns $f_u(x)$.

*Proof.* Each step of lines L1 and L2 replaces $u$ by the child that $x$ selects, which keeps the value $f_u(x)$ by the definition. The ids decrease, so the loop ends at a sink $c$, and $f_c(x) = c$. $\square$

**Lemma 2 (IS-FREE).** If IS-FREE$(r)$ reaches line L6 for $u$, then $\mathrm{below}[u] = \mathrm{Var}(u)$. IS-FREE$(r)$ returns true if and only if the diagram below $r$ is free.

*Proof.* The first claim is by induction along TOPO: the nodes reachable from $u$ are $u$ and the nodes reachable from its children, so $\mathrm{Var}(u) = \{\mathrm{var}(u)\} \cup \mathrm{Var}(\mathrm{lo}(u)) \cup \mathrm{Var}(\mathrm{hi}(u))$, which is line L6.

If a path from $r$ tests the same variable at $u$ and at a later node $w$, then $w$ is reachable from a child of $u$, so $\mathrm{var}(u) \in \mathrm{Var}(\mathrm{lo}(u)) \cup \mathrm{Var}(\mathrm{hi}(u))$. When the loop reaches $u$, line L5 returns false, unless it returned false earlier. Conversely, if line L5 returns false at a node $u$ reachable from $r$, some node $w$ reachable from a child of $u$ tests $\mathrm{var}(u)$, and a path from $r$ to $u$, then to that child, then to $w$, tests the variable twice. $\square$

**Lemma 3 (the free property below a node).** Let the diagram below $r$ be free, and let $u$ be reachable from $r$. Then $\mathrm{var}(u) \notin \mathrm{Var}(\mathrm{lo}(u)) \cup \mathrm{Var}(\mathrm{hi}(u))$, and in particular the functions $f_{\mathrm{lo}(u)}$ and $f_{\mathrm{hi}(u)}$ do not depend on $x_{\mathrm{var}(u)}$.

*Proof.* This is the converse direction of the proof of Lemma 2. A function that is computed by a diagram whose nodes do not test $x_v$ does not depend on $x_v$, by Lemma 1. $\square$

**Theorem 1 (COUNT).** If the diagram below $r$ is free, then for every node $u$ that the loop handles, $c[u] = N(u) := \lvert \{x \in \{0, 1\}^n : f_u(x) = 1\} \rvert$. So COUNT$(r)$ returns the number of models of $f_r$.

*Proof.* For the sinks, $N(0) = 0$ and $N(1) = 2^n$. Let $u$ be an inner node with $v = \mathrm{var}(u)$, and assume the claim for the children. The models of $f_u$ are the $x$ with $x_v = 0$ and $f_{\mathrm{lo}(u)}(x) = 1$, and the $x$ with $x_v = 1$ and $f_{\mathrm{hi}(u)}(x) = 1$. By Lemma 3, $f_{\mathrm{lo}(u)}$ does not depend on $x_v$, so flipping $x_v$ is a bijection between its models with $x_v = 0$ and its models with $x_v = 1$, and exactly $N(\mathrm{lo}(u))/2$ of its models have $x_v = 0$. In the same way, $N(\mathrm{hi}(u))/2$ models of $f_{\mathrm{hi}(u)}$ have $x_v = 1$. So $N(u) = (N(\mathrm{lo}(u)) + N(\mathrm{hi}(u)))/2$, which is line L8, and the division is exact. $\square$

**Lemma 4 (multilinear polynomials).** Over any field, a polynomial of degree at most 1 in each variable that is 0 at every point of $\{0, 1\}^n$ is the zero polynomial.

*Proof.* By induction on $n$. For $n = 0$ it is a constant, which is 0. For $n \ge 1$, write $P = A + y_n B$, where $A$ and $B$ are multilinear in $y_1, \ldots, y_{n-1}$. Setting $y_n = 0$ gives $A = 0$ on $\{0, 1\}^{n-1}$, and setting $y_n = 1$ gives $A + B = 0$ there, so $B = 0$ there too. By induction, $A$ and $B$ are the zero polynomial, so $P$ is. $\square$

So each function $f : \{0, 1\}^n \to \{0, 1\}$ has exactly one multilinear polynomial over $\mathbb{F}_p$ that equals $f$ on $\{0, 1\}^n$: the polynomial $\hat f$ of the page has these properties, and two of them differ by a multilinear polynomial that is 0 on $\{0, 1\}^n$.

**Theorem 2 (ARITH).** If the diagram below $r$ is free, ARITH$(r, \rho, p)$ returns $\hat f_r(\rho) \bmod p$.

*Proof.* Assign to each node a polynomial over $\mathbb{F}_p$: $P_0 = 0$, $P_1 = 1$ and $P_u = (1 - y_v) P_{\mathrm{lo}(u)} + y_v P_{\mathrm{hi}(u)}$ for $v = \mathrm{var}(u)$. Line L10 evaluates exactly these polynomials at $y = \rho$, by induction along TOPO. We show that $P_u = \hat f_u$ for every node $u$ that the loop handles, by induction. The sinks are clear. For an inner node, $P_{\mathrm{lo}(u)}$ and $P_{\mathrm{hi}(u)}$ contain only the variables $y_i$ with $x_i \in \mathrm{Var}$ of the child, by induction on the construction, so by Lemma 3 they do not contain $y_v$, and they are multilinear by the induction hypothesis. Then $P_u$ is multilinear. At a point $a \in \{0, 1\}^n$, $P_u(a)$ is $P_{\mathrm{lo}(u)}(a) = f_{\mathrm{lo}(u)}(a)$ if $a_v = 0$ and $P_{\mathrm{hi}(u)}(a) = f_{\mathrm{hi}(u)}(a)$ if $a_v = 1$, which is $f_u(a)$. By the uniqueness after Lemma 4, $P_u = \hat f_u$. $\square$

**Theorem 3 (PROBABLY-EQUAL).** Let the diagrams below $f$ and $g$ be free, and let $p$ be a prime with $p > n$. If $f_f = f_g$, PROBABLY-EQUAL returns true. If $f_f \ne f_g$, it returns true with probability at most $(n/p)^t$.

*Proof.* If the functions are equal, they have the same multilinear extension, so by Theorem 2 line L11 never finds a difference, and line L12 returns true. If they differ at a point $a \in \{0, 1\}^n$, then $D = \hat f_f - \hat f_g$ is a nonzero polynomial over $\mathbb{F}_p$, since $D(a) = \pm 1 \ne 0$ in $\mathbb{F}_p$. It is multilinear, so its total degree is at most $n$. By the Schwartz-Zippel lemma, a uniform random point $\rho \in \mathbb{F}_p^n$ satisfies $D(\rho) = 0$ with probability at most $n/p$. The $t$ points are independent, so all of them are roots with probability at most $(n/p)^t$, and only then does the procedure return true. $\blacksquare$

**Remark (the reduction rules).** MK returns $l$ when $l = h$, and the unique table returns the stored node for a stored triple. Neither changes the function of any node, and neither adds a node to a path, so a diagram built with MK is free whenever the same diagram without the two rules is free. The HWB construction is proved correct and free on the page [hidden weighted bit lower bound](/hidden-weighted-bit-lower-bound/), part 2 of the theorem.
