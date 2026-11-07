---
title: FGLM returns the reduced Gröbner basis for the new order and terminates
proves: [correctness, termination]
status: full
---

Let $K$ be a field, $R = K[x_1, \ldots, x_n]$, and $I \subseteq R$ a zero-dimensional ideal with reduced Gröbner basis $G_1$ for the monomial order $>_1$. Let $B_1$ be the standard monomials of $G_1$, $D = |B_1| = \dim_K R/I$, and $\varphi : R \to K^D$ the coordinates of $\operatorname{NF}_{G_1}(f)$ in the basis $B_1$. Write $>$ for the target order $>_2$, $\operatorname{LM}$ for leading monomials with respect to $>$, $L = \langle \operatorname{LM}(f) : f \in I \setminus \{0\} \rangle$ for the leading monomial ideal, and $N$ for the set of monomials not in $L$.

**Lemma 1 (the map $\varphi$).** $\varphi$ is $K$-linear, $\ker \varphi = I$, and $\varphi(x_i f) = M_i \varphi(f)$, where column $b$ of $M_i$ is $\varphi(x_i b)$ for $b \in B_1$.

*Proof.* Since $G_1$ is a Gröbner basis, $f - \operatorname{NF}_{G_1}(f) \in I$ and $\operatorname{NF}_{G_1}(f)$ is the unique combination of $B_1$ congruent to $f$ modulo $I$ (CLO Chapter 2, Section 6). Uniqueness gives linearity, and $\operatorname{NF}_{G_1}(f) = 0$ iff $f \in I$. If $\operatorname{NF}_{G_1}(f) = \sum_b c_b b$, then $x_i f \equiv \sum_b c_b\, x_i b \equiv \sum_b c_b \operatorname{NF}_{G_1}(x_i b)$ modulo $I$, and the right side is a combination of $B_1$, so it is $\operatorname{NF}_{G_1}(x_i f)$. In coordinates this is $M_i \varphi(f)$. $\square$

**Lemma 2 (leading monomials by linear algebra).** For a monomial $m$, $m \in L$ if and only if $\varphi(m)$ is a $K$-linear combination of $\{\varphi(u) : u \in N,\ u < m\}$.

*Proof.* If $m \in L$, then $m = \operatorname{LM}(f)$ for some $f \in I$, because $\{\operatorname{LM}(f)\}$ is closed under multiplication by monomials ($\operatorname{LM}(u f) = u \operatorname{LM}(f)$). Reduce $f$ by a Gröbner basis of $I$ for $>$: the result $f' = m + \sum c_u u$ (after scaling) lies in $I$, has $\operatorname{LM}(f') = m$, and every $u$ in its tail is in $N$ and smaller than $m$. Applying $\varphi$ gives $\varphi(m) = -\sum c_u \varphi(u)$. Conversely, if $\varphi(m) = \sum c_u \varphi(u)$ with $u \in N$, $u < m$, then $f = m - \sum c_u u \in \ker\varphi = I$ and $\operatorname{LM}(f) = m$, so $m \in L$. $\square$

**Lemma 3 (the vectors of $N$ are independent).** The vectors $\varphi(u)$, $u \in N$, are linearly independent. In particular $|N| \le D$.

*Proof.* A nontrivial relation $\sum c_u \varphi(u) = 0$ gives $f = \sum c_u u \in I$, a nonzero polynomial whose leading monomial is in $N$, a contradiction. $\square$

**Lemma 4 (order of processing).** The monomials removed from $C$ at line L4 are strictly increasing for $>$, and each monomial is removed at most once.

*Proof.* When $m$ is removed, it is the smallest element of $C$. Line L8 inserts only $x_j m > m$ (a monomial order satisfies $x_j m > m$). So every element of $C$ after the step is greater than $m$, and the next removed monomial is greater than $m$. A monomial cannot be inserted again after its removal, because the insertions after that point are greater than it; the implementation also ignores duplicates in $C$. $\square$

**Lemma 5 (invariant).** When a monomial $m$ reaches line L6 (it was not skipped at line L5), $S$ is exactly $\{u \in N : u < m\}$ listed in increasing order, the stored vector of each $s \in S$ is $\varphi(s)$, and $G_2$ consists of one polynomial $g_w = w - \sum_j c_j s_j$ for each minimal generator $w < m$ of $L$, with $s_j \in N$, $s_j < w$, and $g_w \in I$.

*Proof.* By induction on the steps. Initially $S = G_2 = \emptyset$ and $C = \{1\}$.

First, every element of $N \cup \operatorname{mingens}(L)$ is eventually removed from $C$ and is not skipped at line L5, as long as all smaller elements of $N$ are put into $S$. Indeed, $N$ is closed under division (if $u \notin L$, no divisor of $u$ is in $L$). Hence if $u \ne 1$ lies in $N \cup \operatorname{mingens}(L)$, then $u = x_i u'$ with $u' \in N$: for $u \in N$ any $u' = u/x_i$ works, and for a minimal generator every proper divisor is in $N$. Since $u' < u$, by induction $u'$ is put into $S$, and line L8 then inserts $u$ into $C$. The loop runs until $C$ is empty, so $u$ is removed. It is not skipped at line L5: every $\operatorname{LM}(g)$ with $g \in G_2$ lies in $\operatorname{mingens}(L)$, and a monomial of $N$ is divisible by no element of $L$. A minimal generator $u$ is divisible by no other minimal generator, and by Lemma 4 it is not equal to an earlier one.

Second, every other monomial $m$ that is removed is skipped. Such an $m$ is in $L$ but is not minimal, so it is divisible by some $w \in \operatorname{mingens}(L)$ with $w \ne m$, hence $w < m$ (a proper divisor is smaller in a monomial order). By Lemma 4 and the first part, $w$ was processed before $m$ and contributed $g_w$ with $\operatorname{LM}(g_w) = w$ at line L7 (shown below), so $m$ is skipped at line L5.

Now take a monomial $m$ that reaches line L6, so $m \in N \cup \operatorname{mingens}(L)$. By Lemma 4 and the two parts above, every $u \in N$ with $u < m$ was processed earlier and not skipped, and by the induction hypothesis it was put into $S$, in increasing order; the elements of $S$ are in $N$ by the step below. So $S = \{u \in N : u < m\}$. Line L6 computes $M_i \varphi(m') = \varphi(x_i m') = \varphi(m)$ by Lemma 1, where $m' \in S$ is the element that inserted $m$ (or $\varphi(1)$ if $m = 1$).

- If $m \in L$, Lemma 2 says that $\varphi(m)$ is a combination of $\{\varphi(s) : s \in S\}$, so line L7 appends $g_m = m - \sum c_j s_j$. It lies in $\ker\varphi = I$ and has $\operatorname{LM}(g_m) = m$, because every $s_j < m$. Here $m$ is a minimal generator.
- If $m \in N$, Lemma 3 says that $\varphi(m)$ is independent of $\{\varphi(s)\}$, so line L8 appends $m$ to $S$ with its vector $\varphi(m)$.

The echelon form at line L7 decides membership in the span exactly: it is Gaussian elimination over $K$, and it records the combination of the original vectors $\varphi(s_j)$. This keeps the invariant. $\square$

**Theorem.** FGLM$(G_1, >_1, >_2)$ terminates, and it returns the reduced Gröbner basis of $I$ for $>_2$.

*Proof.* Termination: each element of $S$ inserts at most $n$ monomials into $C$, and $|S| \le |N| \le D$ by Lemma 3, so at most $nD + 1$ monomials ever enter $C$. Each iteration removes one, so the loop stops. Lines L1 and L6 terminate because $B_1$ is finite, which holds since $I$ is zero-dimensional.

When the loop stops, the first part of the proof of Lemma 5 shows that every minimal generator $w$ of $L$ has been processed, so $G_2 = \{g_w : w \in \operatorname{mingens}(L)\}$. Each $g_w$ lies in $I$, has leading monomial $w$ and leading coefficient 1, and its other monomials lie in $N$, so they are divisible by no leading monomial of $G_2$. The leading monomials of $G_2$ generate $L$, so $G_2$ is a Gröbner basis of $I$ for $>_2$. It is minimal, since no $w$ divides another, and reduced, since no tail monomial is in $L$. The reduced Gröbner basis is unique (CLO Chapter 2, Section 7), so $G_2$ is that basis. $\blacksquare$
