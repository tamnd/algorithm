---
title: EVAL, SUBS and DIFF on expression trees are correct
proves: [correctness, termination]
status: full
---

Let $e$ satisfy the invariant (T). For a node $u$ write $\ell(u)$ and $i(u)$ for the numbers of leaves and of operator nodes in the subtree of $u$, counting a shared child once per occurrence. Since each operator has two children, $\ell(u) = i(u) + 1$. Write $[\![u]\!]_\rho$ for the value of $u$, defined by structural recursion as on the main page.

**Lemma 1 (stack lemma for EVAL).** Suppose that at the start of a pass of the loop of line L2 the stacks are $S = S_0 \cdot (u, \text{false})$ and $V = W$. Then after exactly $p(u) = \ell(u) + 2 i(u)$ passes the stacks are $S = S_0$ and $V = W \cdot [\![u]\!]_\rho$, and at no time in between is $S$ shorter than $S_0$ or $V$ shorter than $W$, so no entry of $S_0$ or $W$ is read or changed.

*Proof.* By induction on the height of $u$. If $u$ is a constant $c$, the pass pops $(u, \text{false})$ at line L3 and pushes $c$ at line L4, so after $1 = p(u)$ pass $S = S_0$ and $V = W \cdot c$. A symbol $s$ is the same with line L5 and $\rho(s)$. If $u = a \circ b$ is an operator node, the first pass pops $(u, \text{false})$ and line L6 leaves $S = S_0 \cdot (u, \text{true}) \cdot (b, \text{false}) \cdot (a, \text{false})$ with $V = W$. By induction for $a$, with $S_0 \cdot (u, \text{true}) \cdot (b, \text{false})$ in the role of $S_0$, after $p(a)$ passes $S = S_0 \cdot (u, \text{true}) \cdot (b, \text{false})$ and $V = W \cdot [\![a]\!]_\rho$. By induction for $b$, after $p(b)$ more passes $S = S_0 \cdot (u, \text{true})$ and $V = W \cdot [\![a]\!]_\rho \cdot [\![b]\!]_\rho$. The next pass pops $(u, \text{true})$; the tests of lines L4 to L6 fail, since $u$ is an operator and done is true, so line L7 pops $b' = [\![b]\!]_\rho$, then $a' = [\![a]\!]_\rho$, and pushes $a' \circ b' = [\![u]\!]_\rho$. The total is $1 + p(a) + p(b) + 1 = \ell(a) + \ell(b) + 2(i(a) + i(b) + 1) = p(u)$ passes. During the passes for $a$ and $b$, the induction hypothesis keeps $S$ and $V$ at least as long as the stated prefixes, which contain $S_0$ and $W$. $\square$

**Theorem 1.** EVAL$(e, \rho)$ terminates after $p(e) = n + i(e)$ passes and returns $[\![e]\!]_\rho$, provided $\rho$ defines every symbol of $e$.

*Proof.* Line L1 sets $S = (e, \text{false})$ with $S_0$ empty and $V$ empty. By Lemma 1, after $p(e)$ passes $S$ is empty, so the loop of line L2 stops, and $V = [\![e]\!]_\rho$ has one element, which line L8 returns. Since $n = \ell(e) + i(e)$, the count is $n + i(e)$. $\blacksquare$ for EVAL.

**Lemma 2 (postorder).** The walk used by SUBS and DIFF lists every node occurrence of $e$ exactly once, and each operator node after both of its children.

*Proof.* The walk is EVAL with "append $u$ to the output" in place of lines L4, L5 and L7. Lemma 1, with the output list in place of $V$, shows that the occurrences in the subtree of $u$ are output during its $p(u)$ passes, with $u$ itself last. By induction this lists the occurrences of the left subtree, then of the right subtree, then $u$. $\square$

**Theorem 2.** SUBS$(e, x, r)$ returns $e[x := r]$, the tree obtained by replacing each leaf $x$ by $r$. Hence, by the substitution lemma, $[\![\text{SUBS}(e, x, r)]\!]_\rho = [\![e]\!]_{\rho[x \mapsto [\![r]\!]_\rho]}$.

*Proof.* We show $R[u] = u[x := r]$ for each node $u$, by induction along the postorder of Lemma 2. A leaf that is the symbol $x$ gets $r$ at line S2, and every other leaf gets itself at line S3; this is the definition of substitution on leaves. For an operator node $u = a \circ b$, both children were processed earlier, so $R[a] = a[x := r]$ and $R[b] = b[x := r]$, and line S4 gives $R[a] \circ R[b] = (a \circ b)[x := r]$. A node that occurs more than once gets the same result each time, since the computation depends only on its subtree. Line S5 returns $R[e]$. The substitution lemma follows by induction on $e$: for $u = x$ both sides are $[\![r]\!]_\rho$, for other leaves both are the value of the leaf, and for $u = a \circ b$ both sides are computed from the children by the same operation. $\square$

**Theorem 3.** For each environment $\rho$, $[\![\text{DIFF}(e, x)]\!]_\rho = \frac{\partial}{\partial x} [\![e]\!]$ evaluated at $\rho$, where $[\![e]\!]$ is the polynomial function that $e$ denotes.

*Proof.* The smart constructors return an expression with the same value as the plain node: folding two constants computes the value, and the rules $0 + u = u$, $u - 0 = u$, $0 \cdot u = 0$, $1 \cdot u = u$ and their mirror images hold in every ring. So it suffices to check lines D2 to D6 with plain nodes, by induction along the postorder. Constants have derivative 0 and a symbol $s$ has derivative 1 if $s = x$ and 0 otherwise (lines D2, D3). For $u = a \pm b$ and $u = a \times b$, lines D4 and D5 are the sum and product rules applied to the children's derivatives, which are correct by induction. For $u = a^k$, the power rule $\partial(a^k) = k a^{k-1} \partial a$ holds for $k \ge 1$, where $a^0$ means 1, and $\partial(a^0) = \partial 1 = 0$; line D6 and the code use the factor 1 for $k = 1$ and $a$ for $k = 2$, both of which equal $a^{k-1}$. $\square$

**Termination and cost.** Each walk is the loop of Lemma 1, which performs $n + i(e) \le 2n$ passes, and each pass does $O(1)$ stack and dictionary operations and at most a constant number of node constructions. So SUBS and DIFF stop after $O(n)$ steps and create $O(n)$ nodes. $\blacksquare$
