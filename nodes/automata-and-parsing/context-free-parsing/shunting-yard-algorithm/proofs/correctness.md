---
title: The shunting-yard algorithm outputs the postfix form of the precedence parse tree
proves: [correctness, termination]
status: full
---

We use the pseudocode and the relation $o \sqsupset t$ of the page. The precedence levels are $1, \ldots, m$, and all operators of one level have the same associativity. A **primary** is an operand or a group $(\,e\,)$ where $e$ is an expression. A **flat sequence** is $\sigma = x_0\, o_1\, x_1\, o_2 \cdots o_k\, x_k$ with $k \ge 0$, primaries $x_i$ and binary operators $o_i$. Write $P(\cdot)$ for the postfix form of a tree, and $P(x)$ for the postfix form of the tree of a primary $x$ (the operand itself, or $P$ of the tree of $e$ for $x = (\,e\,)$).

## The tree of a flat sequence

**Definition.** The tree $\tau(\sigma)$ is defined by induction on $k$. If $k = 0$, $\tau(\sigma)$ is the tree of $x_0$. If $k \ge 1$, let $p$ be the least precedence among $o_1, \ldots, o_k$. The root is $o_r$, where $r$ is the largest index with $\text{prec}(o_r) = p$ if level $p$ is left associative, and the smallest such index if it is right associative. The left subtree is $\tau(x_0 \cdots x_{r-1})$ and the right subtree is $\tau(x_r \cdots x_k)$.

This is the parse tree of the precedence grammar, whose level $p$ is $E_p \to E_p\, o\, E_{p+1} \mid E_{p+1}$ when it is left associative and $E_p \to E_{p+1}\, o\, E_p \mid E_{p+1}$ when it is right associative, with $E_{m+1} \to (\,E_1\,) \mid \text{id}$. A string derived from $E_{q}$ contains, outside parentheses, only operators of level at least $q$. So in a derivation from $E_p$ of a flat sequence whose least level is $p$, the topmost production of level $p$ splits at the last operator of level $p$ (left associative: its right part comes from $E_{p+1}$ and has no operator of level $p$) or at the first one (right associative: its left part comes from $E_{p+1}$). By induction on $k$ this split is forced at every node, so the parse tree exists, is unique, and equals $\tau(\sigma)$.

**Right spine.** The right spine of a tree is its root, the root of its right subtree, and so on, down to the last leaf. In $\tau(\sigma)$ the spine operators are $o_{s_1}, \ldots, o_{s_h}$ from the root down, with $s_1 < \cdots < s_h$, and the last primary is $x_k$. Let $\lambda_i$ be the left subtree of $o_{s_i}$. Applying the definition of postfix form $h$ times gives

$$P(\tau(\sigma)) = P(\lambda_1)\, P(\lambda_2) \cdots P(\lambda_h)\, P(x_k)\; o_{s_h}\, o_{s_{h-1}} \cdots o_{s_1}. \tag{1}$$

The same formula holds for the subtree rooted at any spine node $o_{s_i}$, with $\lambda_i, \ldots, \lambda_h$.

**Lemma 1 (spine order).** For consecutive spine operators $a = o_{s_i}$ and $b = o_{s_{i+1}}$, not $a \sqsupset b$.

*Proof.* Let $a$ be the root of the subsequence $\rho$ whose tree is rooted at $a$, with least level $p = \text{prec}(a)$, and let $b$ be the root of the right part of $\rho$. If level $p$ is left associative, $a$ is the last operator of level $p$ in $\rho$, so every operator of the right part, $b$ among them, has $\text{prec}(b) > p$; then not $a \sqsupset b$. If level $p$ is right associative, $\text{prec}(b) \ge p$; if $\text{prec}(b) > p$ we are done, and if $\text{prec}(b) = p$ then $b$ is right associative, so again not $a \sqsupset b$. $\square$

**Lemma 2 (suffix).** Let $t$ be an operator. If $o_{s_i} \sqsupset t$, then $o_{s_{i'}} \sqsupset t$ for every $i' > i$.

*Proof.* It suffices to take $i' = i + 1$ and then repeat. Write $a = o_{s_i}$ and $b = o_{s_{i+1}}$. By Lemma 1, $\text{prec}(b) > \text{prec}(a)$, or $\text{prec}(b) = \text{prec}(a)$ and the level of $a$ is right associative. If $\text{prec}(a) > \text{prec}(t)$, then $\text{prec}(b) > \text{prec}(t)$ and $b \sqsupset t$. Otherwise $\text{prec}(a) = \text{prec}(t)$ and $t$ is left associative, so the level of $a$, which is the level of $t$, is left associative; then the second case of Lemma 1 is impossible, so $\text{prec}(b) > \text{prec}(t)$ and $b \sqsupset t$. $\square$

So the spine operators that pop $t$ are exactly $o_{s_g}, \ldots, o_{s_h}$ for some $g$ with $1 \le g \le h + 1$ (the set is empty when $g = h + 1$). Define the **graft** of $t$ and a primary $y$ onto $\tau(\sigma)$: take the spine node $o_{s_g}$, or the last leaf $x_k$ when $g = h + 1$, and replace the subtree $\theta$ rooted there by the node $t(\theta, y)$.

**Lemma 3 (graft).** $\tau(\sigma\, t\, y) = $ the graft of $t$ and $y$ onto $\tau(\sigma)$.

*Proof.* Induction on $k$. If $k = 0$, then $\tau(x_0\, t\, y) = t(x_0, y)$, the spine has no operator, $g = 1 = h + 1$, and the graft at the leaf $x_0$ gives the same tree. Let $k \ge 1$, let $p$ be the least level in $\sigma$, $o_r$ the root of $\tau(\sigma)$, $\sigma = L\, o_r\, R$. Four cases.

1. $\text{prec}(t) < p$. In $\sigma\, t\, y$ the operator $t$ is the only one of least level, so the root is $t$ with the subtrees $\tau(\sigma)$ and $y$. Every spine operator has level at least $p > \text{prec}(t)$, so it pops $t$; then $g = 1$, and the graft at the root gives the same tree.
2. $\text{prec}(t) = p$ and level $p$ is left associative. The root of $\sigma\, t\, y$ is the last operator of level $p$, which is $t$, with left part $\sigma$. The root $o_r$ pops $t$ (equal precedence, $t$ left associative), so $g = 1$ by Lemma 2, and the graft gives the same tree.
3. $\text{prec}(t) = p$ and level $p$ is right associative. The root of $\sigma\, t\, y$ is the first operator of level $p$, which is $o_r$, with left part $L$ and right part $R\, t\, y$. The root $o_r$ does not pop $t$. So the graft point is on the spine of $\tau(R)$, and it is the same node as the graft point of $t$ in $\tau(R)$, because the spine of $\tau(\sigma)$ is $o_r$ followed by the spine of $\tau(R)$. By the induction hypothesis for $R$, which has fewer operators, $\tau(R\, t\, y)$ is the graft onto $\tau(R)$, and so $\tau(\sigma\, t\, y)$ is the graft onto $\tau(\sigma)$.
4. $\text{prec}(t) > p$. The least level of $\sigma\, t\, y$ is still $p$, and $t$ is not of level $p$, so the root is still $o_r$ (the last or the first operator of level $p$ does not change), with left part $L$ and right part $R\, t\, y$. The root does not pop $t$, since $\text{prec}(o_r) < \text{prec}(t)$. The rest is as in case 3. $\square$

## The invariant

Fix a flat sequence $\sigma = x_0\, o_1 \cdots o_k\, x_k$ that the algorithm reads with a stack whose top part, before $x_0$, is a base: either the bottom of the stack or a `(`. We assume the claim of the theorem below for every group $(\,e\,)$ among the $x_i$ (induction on the nesting depth, see the end), so reading a primary $x$ appends $P(x)$ to the output and leaves the stack as it was.

**Invariant (S).** After the algorithm reads $x_0\, o_1 \cdots o_j\, x_j$, the stack above the base holds exactly the spine operators $o_{s_1}, \ldots, o_{s_h}$ of $\tau(x_0 \cdots x_j)$, with $o_{s_1}$ at the bottom and $o_{s_h}$ on top, and the output written since the base is $P(\lambda_1) \cdots P(\lambda_h)\, P(x_j)$.

*Initialization.* After $x_0$, the stack above the base is empty, the tree is the tree of $x_0$ with no spine operator, and the output is $P(x_0)$.

*Maintenance.* Let (S) hold after $x_j$, and let $t = o_{j+1}$ and $y = x_{j+1}$. The loop of lines L9 and L10 pops operators from the top while the top is an operator that pops $t$; it stops at the base, since a `(` is not an operator and the bottom ends the loop. By Lemma 2 the operators popped are exactly $o_{s_h}, o_{s_{h-1}}, \ldots, o_{s_g}$, in this order. The output becomes

$$P(\lambda_1) \cdots P(\lambda_{g-1})\; \bigl[P(\lambda_g) \cdots P(\lambda_h)\, P(x_j)\, o_{s_h} \cdots o_{s_g}\bigr],$$

and by (1) applied to the subtree $\theta$ at $o_{s_g}$, the bracket is $P(\theta)$; if $g = h + 1$ the bracket is $P(x_j)$ and $\theta$ is the leaf $x_j$. Line L11 pushes $t$, and reading $y$ appends $P(y)$. By Lemma 3, the new tree is the graft: its spine is $o_{s_1}, \ldots, o_{s_{g-1}}, t$, the left subtree of $t$ is $\theta$, and the last primary is $y$. So the stack is the new spine and the output is $P(\lambda_1) \cdots P(\lambda_{g-1})\, P(\theta)\, P(y)$, which is (S) for $j + 1$.

*End of the sequence.* A flat sequence ends at a `)` (line L6) or at the end of the input (line L12). Both pop all operators above the base, from the top: line L6 stops at the `(`, and line L14 empties the stack. They append $o_{s_h} \cdots o_{s_1}$, so by (1) the output written since the base is $P(\tau(\sigma))$. Line L7 then removes the `(`, so the stack is as it was before the group.

## The theorem

**Theorem.** If the input is an expression $e$ of the precedence grammar, SHUNTING-YARD returns $P$ of the parse tree of $e$.

*Proof.* By induction on the nesting depth of parentheses. An expression is a flat sequence of primaries, and the groups among them have smaller depth, so by the induction hypothesis reading a group $(\,e'\,)$ pushes `(`, appends $P$ of the tree of $e'$ (by the argument above with the `(` as base), and pops the `(`, which is the assumption used for (S). The whole input is a flat sequence with the bottom of the stack as base, so the output is $P(\tau(e))$, which is $P$ of the parse tree by the definition section. Line L13 never fires, because each `(` was removed by its `)`. $\square$

**Rejection.** The implementation keeps a flag that is true exactly when the next token must start a primary. It accepts a token only if the token sequence so far is a prefix of the form $x_0\, o_1\, x_1 \cdots$ with matched parentheses at each `)`, and at the end it requires the flag to be false and no `(` on the stack. Every expression of the grammar passes these checks, and every token sequence that passes them is a flat sequence of primaries with matched parentheses, which is an expression of the grammar. So the implementation raises an error exactly on the inputs that are not expressions.

**Termination.** Each token is read once. Each loop of lines L6, L9 and L12 pops one token at each run, and each token is pushed at most once, so the loops run at most $n$ times in total. $\blacksquare$
