---
title: The Forney formula gives the error values
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $F$ be a finite field, $\alpha$ an element of order $n$, and let the code have the zeros $\alpha^b, \ldots, \alpha^{b+2t-1}$. The received word is $r = c + e$ with $c$ a codeword and $e$ nonzero exactly at the distinct positions $i_1, \ldots, i_\nu$, with $1 \le \nu \le 2t$. Put $X_k = \alpha^{i_k}$ and $Y_k = e_{i_k} \ne 0$. The $X_k$ are distinct because $0 \le i_k < n$. The input is $S_j = r(\alpha^j)$ for $b \le j \le b + 2t - 1$ and $\Lambda(x) = \prod_{k=1}^{\nu} (1 - X_k x)$, the locator of the given positions. (With erasures, $\Lambda$ is the locator of all the positions, errors and erasures together, and the proof is the same.)

**Syndromes.** Since $c(\alpha^j) = 0$ for these $j$,

$$S_j = e(\alpha^j) = \sum_{k=1}^{\nu} Y_k X_k^{\,j}.$$

**Lemma 1 (the evaluator).** Let $\Omega(x) = S(x)\Lambda(x) \bmod x^{2t}$ as in line L2. Then

$$\Omega(x) = \sum_{k=1}^{\nu} Y_k X_k^{\,b} \prod_{l \ne k} (1 - X_l x).$$

*Proof.* By line L1 and the syndrome formula,

$$S(x) = \sum_{i=0}^{2t-1} S_{b+i} x^i = \sum_{k=1}^{\nu} Y_k X_k^{\,b} \sum_{i=0}^{2t-1} (X_k x)^i .$$

For each $k$, $(1 - X_k x) \sum_{i=0}^{2t-1} (X_k x)^i = 1 - (X_k x)^{2t}$. Since $\Lambda(x) = (1 - X_k x) \prod_{l \ne k}(1 - X_l x)$,

$$S(x)\Lambda(x) = \sum_{k=1}^{\nu} Y_k X_k^{\,b} \bigl(1 - X_k^{2t} x^{2t}\bigr) \prod_{l \ne k}(1 - X_l x) \equiv \sum_{k=1}^{\nu} Y_k X_k^{\,b} \prod_{l \ne k}(1 - X_l x) \pmod{x^{2t}}.$$

The last sum has degree at most $\nu - 1 < 2t$, so it is its own remainder modulo $x^{2t}$, and it equals $\Omega(x)$. $\square$

**Lemma 2 (the derivative).** For each $j$, $\Lambda'(X_j^{-1}) = -X_j \prod_{l \ne j} (1 - X_l X_j^{-1})$, and this is not zero.

*Proof.* The formal derivative of line L3 is linear and obeys the product rule $(fg)' = f'g + fg'$ over every commutative ring; this follows from the rule on monomials, $(x^a x^c)' = (a + c)x^{a+c-1} = a x^{a-1} x^c + x^a c x^{c-1}$. By induction on the number of factors,

$$\Lambda'(x) = \sum_{k=1}^{\nu} (-X_k) \prod_{l \ne k} (1 - X_l x).$$

At $x = X_j^{-1}$, every term with $k \ne j$ has the factor $1 - X_j X_j^{-1} = 0$. The term $k = j$ remains. Each factor $1 - X_l X_j^{-1}$ with $l \ne j$ is nonzero because $X_l \ne X_j$, and $X_j \ne 0$. $\square$

**The formula.** By Lemma 1 at $x = X_j^{-1}$, again only the term $k = j$ remains:

$$\Omega(X_j^{-1}) = Y_j X_j^{\,b} \prod_{l \ne j} (1 - X_l X_j^{-1}).$$

Dividing by Lemma 2,

$$\frac{\Omega(X_j^{-1})}{\Lambda'(X_j^{-1})} = \frac{Y_j X_j^{\,b}}{-X_j} = -Y_j X_j^{\,b-1}, \qquad\text{so}\qquad Y_j = -X_j^{\,1-b}\,\frac{\Omega(X_j^{-1})}{\Lambda'(X_j^{-1})}.$$

This is the value that line L6 computes for $X = X_j$, with a nonzero denominator by Lemma 2.

**Other generators of the zeros.** If the zeros are $\beta^b, \ldots, \beta^{b+2t-1}$ for another element $\beta$ of order $n$ (CCSDS uses $\beta = \alpha^{11}$), the same proof holds with $X_k = \beta^{i_k}$.

**Termination.** Line L2 is a finite product, line L3 a finite list, and the loop of line L4 runs $\nu$ times. $\blacksquare$
