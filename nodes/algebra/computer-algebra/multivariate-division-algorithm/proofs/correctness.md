---
title: The division algorithm stops and returns a valid quotient and remainder
proves: [correctness, termination]
status: full
---

Fix a field $K$, a monomial order $>$ on $\mathbb{N}^n$, a polynomial $f \in K[x_1, \ldots, x_n]$ and nonzero $f_1, \ldots, f_s$. We write $\operatorname{LM}$, $\operatorname{LT}$ and $\operatorname{LC}$ for the leading monomial, term and coefficient for $>$, and we use two facts about a monomial order. (O1) If $x^\beta \le x^\alpha$ then $x^\gamma x^\beta \le x^\gamma x^\alpha$ for each $\gamma$, by compatibility with multiplication. (O2) There is no infinite strictly descending sequence of monomials, because $>$ is a well-ordering.

**Invariant.** At each test of line L2:

> **(D1)** $f = q_1 f_1 + \cdots + q_s f_s + p + r$.
> **(D2)** No term of $r$ is divisible by any $\operatorname{LT}(f_i)$.
> **(D3)** If $p \ne 0$, then $\operatorname{LM}(p) \le \operatorname{LM}(f)$. Each monomial of each $q_i f_i$ is at most $\operatorname{LM}(f)$.

*Initialization.* Line L1 sets $q_i = 0$, $r = 0$ and $p = f$. Then (D1) reads $f = f$, (D2) holds because $r$ has no terms, and (D3) holds because $\operatorname{LM}(p) = \operatorname{LM}(f)$ and each $q_i f_i = 0$.

*Maintenance, division step.* Assume $p \ne 0$ and that line L5 finds the first $i$ with $\operatorname{LT}(f_i) \mid \operatorname{LT}(p)$. Let $u = \operatorname{LT}(p)/\operatorname{LT}(f_i)$, a term $c\,x^\gamma$. Lines L6 and L7 replace $q_i$ by $q_i + u$ and $p$ by $p - u f_i$. The sum $q_i f_i + p$ becomes $(q_i + u) f_i + p - u f_i = q_i f_i + p$, so (D1) still holds. The remainder does not change, so (D2) holds. The term $u \operatorname{LT}(f_i) = \operatorname{LT}(p)$, so $\operatorname{LT}(u f_i) = \operatorname{LT}(p)$ by the product rule for leading terms. Each other monomial of $u f_i$ is $x^\gamma m'$ with $m' < \operatorname{LM}(f_i)$, so $x^\gamma m' < x^\gamma \operatorname{LM}(f_i) = \operatorname{LM}(p)$ by (O1) with strict inequality (a monomial order is compatible with strict inequality too, because it is a total order and $x^\gamma$ times two distinct monomials gives two distinct monomials). So in $p - u f_i$ the term $\operatorname{LT}(p)$ cancels and every other monomial is smaller than the old $\operatorname{LM}(p)$. Hence the new $p$ is $0$ or has $\operatorname{LM}(p_{\text{new}}) < \operatorname{LM}(p_{\text{old}}) \le \operatorname{LM}(f)$. The new monomials of $q_i f_i$ are those of $u f_i$, all at most $\operatorname{LM}(p_{\text{old}}) \le \operatorname{LM}(f)$. So (D3) holds.

*Maintenance, remainder step.* Assume $p \ne 0$ and no $\operatorname{LT}(f_i)$ divides $\operatorname{LT}(p)$. Lines L11 and L12 add $\operatorname{LT}(p)$ to $r$ and subtract it from $p$. The sum $p + r$ does not change, so (D1) holds. The new term of $r$ is not divisible by any $\operatorname{LT}(f_i)$, and the monomial $\operatorname{LM}(p)$ is not yet in $r$, because every earlier term of $r$ was a leading monomial of an earlier $p$ and these are strictly larger (see below). So (D2) holds. The new $p$ is $0$ or has a smaller leading monomial. So (D3) holds.

**Termination.** In both steps, the new $p$ is $0$ or $\operatorname{LM}(p_{\text{new}}) < \operatorname{LM}(p_{\text{old}})$. Suppose the loop of line L2 ran forever. Then the leading monomials of $p$ in successive passes would form an infinite strictly descending sequence, which (O2) forbids. So the loop stops after finitely many passes, and the inner loop of line L4 stops after at most $s$ steps in each pass. For a graded order the number of passes is at most the number of monomials of degree at most $\deg f$, which is $\binom{n + \deg f}{n}$, because the leading monomials of $p$ are distinct monomials of degree at most $\deg f$ (the degree argument is in the Complexity section of the page). This gives an explicit bound in that case.

**The output.** When the loop stops, $p = 0$. Then (D1) is $f = \sum q_i f_i + r$, (D2) is condition 2 of the output, and (D3) gives condition 3: if $q_i f_i \ne 0$ then its leading monomial is one of its monomials, so it is at most $\operatorname{LM}(f)$. If $f = 0$, the loop does not run and the output is $q_i = 0$, $r = 0$, which meets the specification. $\blacksquare$

**Uniqueness for a Gröbner basis.** Let $G = \{f_1, \ldots, f_s\}$ be a Gröbner basis of $I = \langle f_1, \ldots, f_s \rangle$, and let $r, r'$ be two outputs of the algorithm for $f$ with two orders of the divisors or two choices at line L5. Then $r - r' = \sum (q'_i - q_i) f_i \in I$. If $r \ne r'$, then $\operatorname{LT}(r - r') \in \operatorname{LT}(I)$ is divisible by some $\operatorname{LT}(f_i)$, by the definition of a Gröbner basis. But $\operatorname{LM}(r - r')$ is a monomial of $r$ or of $r'$, and by (D2) no $\operatorname{LT}(f_i)$ divides it. This is a contradiction, so $r = r'$. If $f \in I$, then $r = f - \sum q_i f_i \in I$, and the same argument with $r' = 0$ gives $r = 0$. $\blacksquare$
