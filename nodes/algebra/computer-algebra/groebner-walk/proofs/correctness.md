---
title: The Gröbner walk returns the reduced Gröbner basis for the target order and stops
proves: [correctness, termination]
status: full
---

Let $K$ be a field, $R = K[x_1, \ldots, x_n]$, and $I \subseteq R$ an ideal. For a nonnegative weight $w$ and a monomial order $>$, write $(w; >)$ for the order that compares $w$-weights first and breaks ties by $>$; it is a monomial order because $w \ge 0$. A polynomial is *$w$-homogeneous* if all its terms have the same $w$-weight. $\operatorname{LM}_>(f)$ is the leading monomial of $f$ for $>$, and $\operatorname{LM}_>(J)$ is the monomial ideal spanned by the leading monomials of the elements of an ideal $J$. We use one known theorem: **an ideal has only finitely many distinct monomial ideals $\operatorname{LM}_>(I)$ as $>$ runs over all monomial orders** (Mora and Robbiano 1988; Sturmfels, *Gröbner Bases and Convex Polytopes*, Theorem 1.2).

**Lemma 1 (comparing initial ideals).** If $>_a$ and $>_b$ are monomial orders with $\operatorname{LM}_{>_a}(I) \subseteq \operatorname{LM}_{>_b}(I)$, then the two ideals are equal.

*Proof.* Suppose $m \in \operatorname{LM}_{>_b}(I)$ but $m \notin \operatorname{LM}_{>_a}(I)$. Reduce a polynomial of $I$ with leading monomial $m$ by the Gröbner basis for $>_b$, leaving its leading term: this gives $f \in I$ with $f = m + (\text{monomials not in } \operatorname{LM}_{>_b}(I))$. Those monomials are not in the smaller ideal $\operatorname{LM}_{>_a}(I)$ either, and neither is $m$. So every monomial of $f \ne 0$ is standard for $>_a$, and $\operatorname{LM}_{>_a}(f) \notin \operatorname{LM}_{>_a}(I)$, which contradicts $f \in I$. $\square$

**Lemma 2 (initial ideals).** For $w \ge 0$ and any monomial order $>$:

1. every $w$-homogeneous element of $\operatorname{in}_w(I)$ is $0$ or $\operatorname{in}_w(f)$ for some $f \in I$, and $\operatorname{in}_w(I)$ is spanned by such elements;
2. $\operatorname{LM}_{(w; >)}(I) = \operatorname{LM}_>(\operatorname{in}_w(I)) = \operatorname{LM}_{(w; >)}(\operatorname{in}_w(I))$;
3. the reduced Gröbner basis of $\operatorname{in}_w(I)$, for any order, consists of $w$-homogeneous polynomials.

*Proof.* (1) An element of $\operatorname{in}_w(I)$ is $\sum_i q_i \operatorname{in}_w(f_i)$ with $f_i \in I$. Its $w$-homogeneous component of weight $c$ is $h = \sum_i q_i' \operatorname{in}_w(f_i)$, where $q_i'$ is the part of $q_i$ of weight $c - w\cdot(\text{weight of } \operatorname{in}_w f_i)$. Then $f = \sum_i q_i' f_i \in I$ equals $h$ plus terms of weight less than $c$, so $h = \operatorname{in}_w(f)$ if $h \ne 0$.

(2) For $f \in I$, $\operatorname{LM}_{(w;>)}(f) = \operatorname{LM}_>(\operatorname{in}_w(f))$, since $(w;>)$ first selects the terms of largest weight. With (1), the leading monomials of elements of $\operatorname{in}_w(I)$ for $>$ are the leading monomials of their $w$-homogeneous components, which are the $\operatorname{LM}_>(\operatorname{in}_w(f))$. This gives the first equality. For a $w$-homogeneous $h$, $\operatorname{LM}_{(w;>)}(h) = \operatorname{LM}_>(h)$, which gives the second.

(3) Let $J = \operatorname{in}_w(I)$ and $h$ an element of its reduced Gröbner basis. Let $h_c$ be the $w$-homogeneous component of $h$ that contains $\operatorname{LM}(h)$; by (1), $h_c \in J$, and $\operatorname{LM}(h_c) = \operatorname{LM}(h)$. All monomials of $h - h_c$ are non-leading monomials of $h$, so they are standard for $J$. Since $h - h_c \in J$, it is $0$. $\square$

**Lemma 3 (one step).** Suppose that at line L4, $G$ is the reduced Gröbner basis of $I$ for $M_{\text{old}}$, and $\operatorname{LM}_{M_{\text{old}}}(g)$ is a monomial of $\operatorname{in}_w(g)$ for every $g \in G$. Then lines L4 to L6 make $G$ the reduced Gröbner basis of $I$ for $M_{\text{new}} = (w; M_t)$.

*Proof.* By hypothesis, $\operatorname{LM}_{M_{\text{old}}}(g) = \operatorname{LM}_{(w; M_{\text{old}})}(g)$ for every $g \in G$. So $\operatorname{LM}_{M_{\text{old}}}(I)$, which these monomials generate, is contained in $\operatorname{LM}_{(w; M_{\text{old}})}(I)$, and by Lemma 1 the two are equal. By Lemma 2(2) this is $\operatorname{LM}_{M_{\text{old}}}(\operatorname{in}_w(I))$. The $\operatorname{in}_w(g)$ lie in $\operatorname{in}_w(I)$ and their leading monomials for $M_{\text{old}}$ generate this ideal, so they form a Gröbner basis of $\operatorname{in}_w(I)$ for $M_{\text{old}}$.

The ideal $\langle \operatorname{in}_w(g) \rangle$ is therefore $\operatorname{in}_w(I)$, and line L4 computes its reduced Gröbner basis $H$ for $M_{\text{new}}$. Take $h \in H$; it is $w$-homogeneous of some weight $c$, by Lemma 2(3). Division by a Gröbner basis leaves remainder 0 on an element of the ideal, so line L5 writes $h = \sum_g p_g \operatorname{in}_w(g)$. Each step of the division subtracts a multiple $a x^\mu \operatorname{in}_w(g)$ whose leading monomial is a monomial of the current dividend, which stays $w$-homogeneous of weight $c$; so every term of $p_g \operatorname{in}_w(g)$ has weight $c$. Then

$$h' = \sum_g p_g g = h + \sum_g p_g \bigl(g - \operatorname{in}_w(g)\bigr),$$

and every term of the sum has weight less than $c$. So $h' \in I$, $\operatorname{in}_w(h') = h$, and $\operatorname{LM}_{M_{\text{new}}}(h') = \operatorname{LM}_{M_{\text{new}}}(h)$ because $M_{\text{new}}$ compares weights first. These monomials generate $\operatorname{LM}_{M_{\text{new}}}(\operatorname{in}_w(I))$, which by Lemma 2(2) with $> = M_t$ equals $\operatorname{LM}_{M_{\text{new}}}(I)$. So the $h'$ form a Gröbner basis of $I$ for $M_{\text{new}}$, and the interreduction at line L6 (removing elements whose leading monomial is divisible by another's, reducing tails and making the result monic) turns it into the reduced one. $\square$

**Lemma 4 (the invariant).** The hypothesis of Lemma 3 holds at every execution of line L4. The value $u$ of line L8 satisfies $0 < u \le 1$.

*Proof.* At the first execution, $w = \sigma$ is the first row of $M_{\text{old}} = M_s$, so $\operatorname{LM}_{M_s}(g)$ has the largest $\sigma$-weight among the terms of $g$ and lies in $\operatorname{in}_\sigma(g)$.

After lines L4 to L6, $G$ is reduced for $M_{\text{new}} = (w; M_t)$ by Lemma 3. Let $g \in G$, $\alpha = \operatorname{LM}_{M_{\text{new}}}(g)$, and $\beta \ne \alpha$ a monomial of $g$; put $a = w \cdot (\alpha - \beta)$ and $b = \tau \cdot (\alpha - \beta)$. Then $a \ge 0$. If $b < 0$, then $a > 0$: if $a = 0$, the tie is broken by $M_t$, whose first row is $\tau$, so $\alpha >_{M_t} \beta$ forces $b \ge 0$. So each candidate $a / (a - b)$ of line L8 lies in $(0, 1)$, and $0 < u \le 1$. The next weight is $w' = (1 - u) w + u\tau \ge 0$, and

$$w' \cdot (\alpha - \beta) = (1 - u) a + u b \ge 0,$$

which is clear if $b \ge 0$ and holds if $b < 0$ because $u \le a/(a - b)$. So $\alpha$ is a monomial of $\operatorname{in}_{w'}(g)$, and line L9 sets $M_{\text{old}} = M_{\text{new}}$, for which $\alpha$ is the leading monomial. Replacing $w'$ by a positive multiple, as the implementation does, changes neither initial forms nor the order $(w'; M_t)$. $\square$

**Lemma 5 (termination).** The loop runs a finite number of times.

*Proof.* Write $w(s) = (1 - s)\sigma + s\tau$ for $s \in [0, 1]$. Every weight used is a positive multiple of some $w(s)$, because a nonnegative combination of a multiple of $w(s)$ and $\tau$ is a multiple of a point of the segment from $w(s)$ to $\tau$. Let $s_0 = 0 < s_1 < s_2 < \cdots$ be the parameters of the weights used; they increase strictly because $u > 0$, unless $w(s_k)$ is already a multiple of $\tau$, in which case no candidate exists, $u = 1$, and the next step has $w = \tau$ and stops. Let $L(s) = \operatorname{LM}_{(w(s); M_t)}(I)$.

The set of $s$ with $L(s) = L^*$ for a fixed monomial ideal $L^*$ is an interval. Let $G^*$ be the reduced Gröbner basis for an order with that initial ideal; each $g \in G^*$ is $\alpha_g$ plus monomials outside $L^*$. If $L(s) = L^*$, the reduced basis for $(w(s); M_t)$ is $G^*$, since a reduced basis is determined by its initial ideal (each element is $m$ minus the unique combination of standard monomials congruent to $m$ modulo $I$). Its leading monomials are then the $\alpha_g$, because the other monomials are not in $L^*$. Conversely, if $\operatorname{LM}_{(w(s); M_t)}(g) = \alpha_g$ for all $g \in G^*$, then $L^* \subseteq L(s)$ and Lemma 1 gives equality. So $L(s) = L^*$ exactly when, for every $g \in G^*$ and every other monomial $\beta$ of $g$, either $w(s) \cdot (\alpha_g - \beta) > 0$, or it is $0$ and $\alpha_g >_{M_t} \beta$. Each condition defines an interval of $s$, since $w(s)$ is affine in $s$; so does their intersection.

At step $k$ the algorithm computes the reduced basis $G_k$ for $(w(s_k); M_t)$. The step from $s_k$ to $s_{k+1}$ is chosen at a value where some $g \in G_k$ and monomial $\beta$ satisfy $w(s_{k+1}) \cdot (\alpha_g - \beta) = 0$ and $\tau \cdot (\alpha_g - \beta) < 0$, so $\beta >_{(w(s_{k+1}); M_t)} \alpha_g$. By the characterization above, $L(s_{k+1}) \ne L(s_k)$. Since each value of $L$ occupies an interval of $s$ and the $s_k$ increase, the values $L(s_0), L(s_1), \ldots$ are pairwise distinct. By the theorem of Mora and Robbiano there are finitely many, so the loop stops. $\square$

**Theorem.** Let $G$ be the reduced Gröbner basis of $I$ for $M_s$, where the first rows of $M_s$ and $M_t$ are nonnegative. Then GROEBNER-WALK$(G, M_s, M_t)$ terminates and returns the reduced Gröbner basis of $I$ for $M_t$.

*Proof.* By Lemma 5 the loop ends, and it can only end at line L7, with $w = \tau$. By Lemmas 3 and 4, at that moment $G$ is the reduced Gröbner basis of $I$ for $(\tau; M_t)$. Since $\tau$ is the first row of $M_t$, the order $(\tau; M_t)$ is the order $M_t$, so $G$ is the reduced Gröbner basis for $M_t$. $\blacksquare$
