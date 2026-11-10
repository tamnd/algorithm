---
title: The polynomial design has small intersections, and the Nisan-Wigderson generator is pseudorandom if f is hard on average
proves: [correctness]
status: full
---

The proof has two parts. Part 1 shows that POLY-DESIGN (lines L5 to L7) outputs a design. Part 2 is the reconstruction argument: a test that tells NW (lines L1 to L4) from uniform gives a small circuit that computes $f$ well on average.

**Definition.** Sets $S_1, \ldots, S_m \subseteq [d]$ form an *$(\ell, a)$ design* if $|S_i| = \ell$ for every $i$ and $|S_i \cap S_j| \le a$ for all $i \ne j$.

## Part 1: the polynomial design

Let $q$ be a prime and $1 \le r \le q$. Line L6 builds, for each polynomial $p$ over $\mathrm{GF}(q)$ of degree less than $r$, the set $S_p = \{(\alpha, p(\alpha)) : \alpha \in \mathrm{GF}(q)\}$ in the ground set $\mathrm{GF}(q)^2$ of size $d = q^2$.

- *Size.* The points $(\alpha, p(\alpha))$ have different first coordinates, so $|S_p| = q = \ell$.
- *Intersections.* If $p \ne p'$, then $p - p'$ is a nonzero polynomial of degree at most $r - 1$, so it has at most $r - 1$ roots. A common point $(\alpha, \beta)$ of $S_p$ and $S_{p'}$ needs $p(\alpha) = p'(\alpha)$, so $|S_p \cap S_{p'}| \le r - 1 = a$.
- *Number of sets.* There are $q^r$ coefficient lists. Two different lists give different polynomials of degree less than $r \le q$, which differ at some $\alpha$ because a nonzero polynomial of degree less than $q$ cannot vanish at all $q$ points. So the sets are different, and $m = q^r$.

So POLY-DESIGN outputs a $(q, r - 1)$ design of $q^r$ sets in a ground set of size $q^2$. $\square$

## Part 2: the reconstruction argument

**Notation.** $f : \{0,1\}^\ell \to \{0,1\}$. For $y \in \{0,1\}^d$, $y|_S$ is the string of the bits of $y$ at the positions in $S$, in increasing order. $\mathrm{NW}(y) = (f(y|_{S_1}), \ldots, f(y|_{S_m}))$. Circuits have gates AND and OR of fan-in 2 and NOT gates, and constants are free.

**Fact.** Every function of $a$ bits has a circuit of size at most $(a + 1)2^a$. *Proof.* Write it as an OR of at most $2^a$ terms, one per accepted input. Each term is an AND of $a$ literals: $a - 1$ AND gates, with the $a$ NOT gates shared by all terms. The OR needs fewer than $2^a$ gates. The total is at most $a + 2^a(a - 1) + 2^a = a + a 2^a \le (a + 1) 2^a$. $\square$

**Theorem.** Let $S_1, \ldots, S_m$ be an $(\ell, a)$ design in $[d]$, and let $t, \varepsilon > 0$. Suppose every circuit $C$ of size at most $t + (m - 1)(a + 1)2^a + 2$ has

$$\Pr_{z \in \{0,1\}^\ell}[C(z) = f(z)] < \frac12 + \frac{\varepsilon}{m}.$$

Then every circuit $D$ of size at most $t$ has $|\Pr[D(\mathrm{NW}(U_d)) = 1] - \Pr[D(U_m) = 1]| < \varepsilon$.

*Proof.* Suppose $D$ has size at most $t$ and $|\Pr[D(\mathrm{NW}(U_d)) = 1] - \Pr[D(U_m) = 1]| \ge \varepsilon$. Negate $D$ if needed, at the cost of one gate, so that the difference is at least $\varepsilon$ with the sign $+$.

*Step 1: a next-bit predictor.* Let $Y = \mathrm{NW}(U_d)$ and $p_i = \Pr[D(Y_1, \ldots, Y_i, R_{i+1}, \ldots, R_m) = 1]$ with $R$ uniform bits. By [Yao's theorem](/yao-next-bit-unpredictability/), part 1, there is an $i$ with $p_i - p_{i-1} \ge \varepsilon/m$, and the randomized predictor that draws $r = (r_i, \ldots, r_m)$ and outputs $r_i$ if $D(Y_{<i}, r) = 1$ and $1 - r_i$ otherwise has

$$\Pr_{y, r}\big[\text{output} = f(y|_{S_i})\big] = \frac12 + p_i - p_{i-1} \ge \frac12 + \frac{\varepsilon}{m}.$$

*Step 2: split the seed.* Write $y = (z, w)$, where $z = y|_{S_i} \in \{0,1\}^\ell$ and $w$ is the string of the other $d - \ell$ bits. Under $U_d$, $z$ and $w$ are independent and uniform. The success above is an average over $(w, r)$ of the success over $z$ alone, so there are fixed values $w^*$ and $r^*$ with

$$\Pr_z\big[\text{output on } y = (z, w^*), r = r^* \text{ equals } f(z)\big] \ge \frac12 + \frac{\varepsilon}{m}.$$

*Step 3: the earlier bits are cheap.* For $j < i$, let $g_j(z) = f((z, w^*)|_{S_j})$. The bits of $(z, w^*)$ at positions in $S_j \setminus S_i$ are fixed bits of $w^*$. So $g_j$ depends only on the bits of $z$ at the positions in $S_i \cap S_j$, and there are at most $a$ of them by the design property. By the fact, $g_j$ has a circuit of size at most $(a + 1)2^a$.

*Step 4: the circuit.* Let $C(z)$ compute $g_1(z), \ldots, g_{i-1}(z)$, feed them with the constants $r^*$ to $D$, and output the result if $r^*_i = 1$ and its negation if $r^*_i = 0$. On input $z$, the predictor of Step 2 sees exactly $Y_{<i} = (g_1(z), \ldots, g_{i-1}(z))$, so $C$ computes the same output. The size of $C$ is at most $(t + 1) + (i - 1)(a + 1)2^a + 1 \le t + (m - 1)(a + 1)2^a + 2$, and

$$\Pr_z[C(z) = f(z)] \ge \frac12 + \frac{\varepsilon}{m}.$$

This contradicts the hypothesis on $f$. $\blacksquare$

**Where the design property is used.** Only in Step 3, and only through the bound $|S_i \cap S_j| \le a$ for $j < i$. The size $|S_i| = \ell$ makes $z$ an input of $f$. The ground set size $d$ is the seed length and plays no part in the argument.
