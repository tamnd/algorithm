---
title: F4 terminates and returns the reduced Gröbner basis
proves: [correctness, termination]
status: full
---

Let $K$ be a field, $R = K[x_1, \ldots, x_n]$ with a monomial order $>$, and $I = \langle f_1, \ldots, f_s \rangle$. We say that $f$ *reduces to zero modulo* a finite set $G$, written $f \to_G 0$, if $f = \sum_k c_k u_k g_k$ with $c_k \in K$, monomials $u_k$, $g_k \in G$, and $\operatorname{LM}(u_k g_k) \le \operatorname{LM}(f)$ for all $k$. This is a standard representation, and it remains one when $G$ grows. We use two facts.

- **Buchberger's criterion** (CLO Chapter 2, Section 6, Theorem 6 and Chapter 2, Section 10). A finite $G \subseteq I$ that generates $I$ is a Gröbner basis if the S-polynomial of every pair has a standard representation, or more generally an lcm-representation, with respect to $G$.
- **Gebauer and Möller** (1988). The pairs removed by UPDATE are covered: if all pairs that are never removed have S-polynomials with standard representations with respect to the final $G$, then so do the removed pairs, through lcm-representations. This is the theorem behind the [Gebauer-Möller criteria](/gebauer-moller-criteria/).

**Lemma 1 (rows lie in the ideal).** At all times $G \subseteq I$, and $G$ generates $I$.

*Proof.* Line L1 puts the nonzero $f_i$ into $G$. Every row of $H$ is a monomial multiple $u g$ of some $g \in G$: the halves at line L4 by construction, and the reducers at line L5 by construction. The row echelon form $\tilde N$ consists of $K$-linear combinations of rows of $H$, so $\tilde N \subseteq I$. $\square$

**Lemma 2 (symbolic preprocessing).** SYMBOLIC-PREPROCESSING terminates, and its output $H$ has this property: for every monomial $m$ that occurs in some row of $H$ and is divisible by $\operatorname{LM}(g)$ for some $g \in G$, there is a row of $H$ of the form $u g'$ with $g' \in G$ and $\operatorname{LM}(u g') = m$.

*Proof.* Each step marks one monomial as handled and possibly adds a row $u g$ whose leading monomial is that monomial $m$, so every other monomial of the new row is smaller than $m$. Consider the graph whose nodes are the handled monomials, with an edge from $m$ to each monomial of the row added for $m$. Each node has finitely many successors, and every path is strictly decreasing for $>$. A monomial order is a well-order, so there is no infinite path, and by König's lemma only finitely many monomials are reached from the finitely many monomials of $L$. So the loop ends. At the end every monomial of every row is handled. For a monomial $m$ in $\operatorname{LM}(L)$, the half itself is a row $u g$ with leading monomial $m$; for every other handled $m$ divisible by some $\operatorname{LM}(g)$, the reducer was added. $\square$

**Lemma 3 (the span reduces to zero).** Let $G$ be the basis before line L8, $H$ the rows of a round, $\tilde N$ the row echelon form and $\tilde N^+$ the new rows. Then every $f$ in the $K$-span of $H$ satisfies $f \to_{G \cup \tilde N^+} 0$.

*Proof.* By induction on $\operatorname{LM}(f)$, which is well founded. If $f = 0$ there is nothing to show. Otherwise $\tilde N$ is a basis of the span with distinct leading monomials, so $\operatorname{LM}(f) = \operatorname{LM}(h)$ for some $h \in \tilde N$, and $m = \operatorname{LM}(f)$ is a monomial of some row of $H$.

- If $m \in \operatorname{LM}(H)$, then $m$ is the leading monomial of a row $r = u g$ of $H$, and every element of $\operatorname{LM}(H)$ is divisible by the leading monomial of an element of $G$ (by Lemma 2 and the form of the halves). Then $f' = f - (\operatorname{LC}(f)/\operatorname{LC}(r))\, r$ is in the span of $H$ and has $\operatorname{LM}(f') < m$.
- If $m \notin \operatorname{LM}(H)$, then $h \in \tilde N^+$, and $f' = f - (\operatorname{LC}(f)/\operatorname{LC}(h))\, h$ is in the span and has $\operatorname{LM}(f') < m$.

In both cases the subtracted term is $c\, u g$ with $g \in G \cup \tilde N^+$ and $\operatorname{LM}(u g) = m \le \operatorname{LM}(f)$, and by induction $f'$ has a standard representation with terms of leading monomial at most $\operatorname{LM}(f') < m$. Adding the two gives one for $f$. $\square$

**Lemma 4 (new leading monomials).** For $h \in \tilde N^+$, $\operatorname{LM}(h)$ is divisible by no $\operatorname{LM}(g)$ with $g \in G$.

*Proof.* $\operatorname{LM}(h)$ is a monomial of some row of $H$, since $h$ is a combination of rows. If $\operatorname{LM}(g) \mid \operatorname{LM}(h)$ for some $g \in G$, Lemma 2 gives a row of $H$ with leading monomial $\operatorname{LM}(h)$, so $\operatorname{LM}(h) \in \operatorname{LM}(H)$, which contradicts $h \in \tilde N^+$. $\square$

**Theorem.** F4 terminates and returns the reduced Gröbner basis of $I$.

*Proof.* *Termination.* Let $J = \langle \operatorname{LM}(G) \rangle$ at the start of a round. By Lemma 4, every $h \in \tilde N^+$ has $\operatorname{LM}(h) \notin J$, so a round with $\tilde N^+ \ne \emptyset$ makes $J$ strictly larger. By Dickson's lemma (equivalently, $R$ is Noetherian) a strictly ascending chain of monomial ideals is finite, so only finitely many rounds add elements, each adds finitely many, and $G$ stays finite. Pairs are created only by UPDATE, at most $|G|$ for each new element, and each round removes at least one pair from $P$ at line L3. So the loop ends.

*Correctness.* Every pair $(i, j)$ that is selected at line L3 has its two halves in $L \subseteq H$, so its S-polynomial is in the span of $H$, and by Lemma 3 it reduces to zero modulo $G \cup \tilde N^+$, which is contained in the final $G$. Every pair that is never selected was removed by UPDATE, and by the theorem of Gebauer and Möller its S-polynomial also has an lcm-representation with respect to the final $G$. By Lemma 1 the final $G$ lies in $I$ and generates it, so by Buchberger's criterion it is a Gröbner basis. Line L9 removes elements whose leading monomial is divisible by another one, makes the rest monic, and reduces their tails, which gives the reduced Gröbner basis; it is unique (CLO Chapter 2, Section 7). $\blacksquare$
