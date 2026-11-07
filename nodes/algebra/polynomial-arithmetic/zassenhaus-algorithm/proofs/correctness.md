---
title: The Zassenhaus algorithm returns the irreducible factorization
proves: [correctness]
status: full
---

Let $f \in \mathbb{Z}[x]$ be primitive and square-free, of degree $n \ge 1$, with $\operatorname{lc}(f) > 0$. For $a = \sum a_i x^i$ write $\|a\|_1 = \sum |a_i|$, $\|a\|_\infty = \max |a_i|$ and $\|a\|_2 = (\sum a_i^2)^{1/2}$. For $a \ne 0$ with complex roots $\alpha_1, \ldots, \alpha_m$, the *Mahler measure* is $\mathrm{M}(a) = |\operatorname{lc}(a)| \prod_i \max(1, |\alpha_i|)$. A bar denotes reduction modulo $p$, and "$a$ mods $m$" is the representative with coefficients in $(-m/2, m/2]$.

## Step 1: a good prime exists (line L1)

Since $f$ is square-free over $\mathbb{Q}$, $\gcd(f, f') = 1$ in $\mathbb{Q}[x]$, so there are $s, t \in \mathbb{Q}[x]$ with $s f + t f' = 1$. Multiply by a common denominator: $s_1 f + t_1 f' = R$ with $s_1, t_1 \in \mathbb{Z}[x]$ and an integer $R \ne 0$. For a prime $p \nmid R \operatorname{lc}(f)$, reduction gives $\bar s_1 \bar f + \bar t_1 \bar f' = \bar R \ne 0$, so $\gcd(\bar f, \bar f') = 1$ and $\bar f$ is square-free, of degree $n$. Only finitely many primes divide $R \operatorname{lc}(f)$, so the search in line L1 stops.

Fix this $p$. Line L2 gives distinct monic irreducible $u_1, \ldots, u_r \in \mathbb{F}_p[x]$ with $\bar f = \overline{\operatorname{lc}(f)}\, u_1 \cdots u_r$; they are pairwise coprime because $\bar f$ is square-free.

## Step 2: Hensel lifting (line L4)

**Lemma 1 (one lifting step).** Let $F, g, h \in \mathbb{Z}[x]$ with $g$ monic, $\gcd(\bar g, \bar h) = 1$, and $F \equiv g h \pmod{p^j}$ for some $j \ge 1$. Then there are $a, b$ with $\deg a < \deg g$ such that $g^* = g + p^j a$ and $h^* = h + p^j b$ satisfy $F \equiv g^* h^* \pmod{p^{j+1}}$.

*Proof.* Let $e = (F - gh)/p^j \in \mathbb{Z}[x]$. Let $t \in \mathbb{F}_p[x]$ with $t \bar h \equiv 1 \pmod{\bar g}$, which exists as $\gcd(\bar g, \bar h) = 1$. Put $\bar a = (\bar e t) \bmod \bar g$, so $\bar a \bar h \equiv \bar e \pmod {\bar g}$, and $\bar b = (\bar e - \bar a \bar h) / \bar g$, an exact division. Lift $\bar a, \bar b$ to $a, b \in \mathbb{Z}[x]$ with coefficients in $[0, p)$. Then $a h + b g \equiv e \pmod p$ and
$$g^* h^* = g h + p^j (a h + b g) + p^{2j} a b \equiv g h + p^j e = F \pmod{p^{j+1}},$$
because $2j \ge j + 1$. $\square$

$g^*$ is monic and $g^* \equiv g$, $h^* \equiv h \pmod p$, so the step can be repeated. The implementation applies it $k - 1$ times to $\operatorname{lc}(f) u_1 \cdots u_r$ split as $u_1 \cdot (\operatorname{lc}(f) u_2 \cdots u_r)$, then splits the second factor in the same way, and so on. Comparing leading coefficients, the last cofactor has leading coefficient $\equiv \operatorname{lc}(f) \pmod {p^k}$, and dividing it by $\operatorname{lc}(f)$ modulo $p^k$ makes it monic. So line L4 returns monic $v_1, \ldots, v_r$ with $\bar v_i = u_i$ and
$$f \equiv \operatorname{lc}(f)\, v_1 \cdots v_r \pmod {p^k}. \tag{1}$$

**Lemma 2 (uniqueness).** Let $G, G^*$ be monic and $H, H^* \in \mathbb{Z}[x]$ with $\bar G = \bar G^*$, $\bar H = \bar H^*$, $\gcd(\bar G, \bar H) = 1$ and $G H \equiv G^* H^* \pmod{p^k}$. Then $G \equiv G^* \pmod{p^k}$.

*Proof.* Suppose not, and let $j < k$ be the largest integer such that $p^j$ divides both $G^* - G$ and $H^* - H$; $j \ge 1$. Write $G^* = G + p^j a$, $H^* = H + p^j b$; then $\deg a < \deg G$, as both are monic of the same degree. From $G^* H^* - G H = p^j(a H + b G) + p^{2j} a b \equiv 0 \pmod {p^{j+1}}$ we get $\bar a \bar H + \bar b \bar G = 0$. So $\bar G$ divides $\bar a \bar H$ and hence $\bar a$, which has smaller degree; so $\bar a = 0$. Then $\bar b \bar G = 0$ and $\bar G \ne 0$ is monic, so $\bar b = 0$. Thus $p^{j+1}$ divides both differences, against the choice of $j$. $\square$

## Step 3: the size bound

**Lemma 3.** (a) For nonzero $a \in \mathbb{Z}[x]$ of degree $m$, $\|a\|_1 \le 2^m \mathrm{M}(a)$. (b) $\mathrm{M}(ab) = \mathrm{M}(a)\mathrm{M}(b)$, and $\mathrm{M}(a) \ge |\operatorname{lc}(a)| \ge 1$ for nonzero $a \in \mathbb{Z}[x]$. (c) $\mathrm{M}(a) \le \|a\|_2$.

*Proof.* (a) By [Vieta's formulas](/vieta-formulas/), the coefficient of $x^{m-i}$ is $\pm \operatorname{lc}(a)\, e_i(\alpha_1, \ldots, \alpha_m)$, and $|e_i| \le \binom{m}{i} \prod_l \max(1, |\alpha_l|)$, since each of the $\binom{m}{i}$ products of $i$ roots has absolute value at most $\prod_l \max(1, |\alpha_l|)$. Summing over $i$ gives $2^m \mathrm{M}(a)$. (b) The roots of $ab$ are those of $a$ and of $b$, and $\operatorname{lc}(ab) = \operatorname{lc}(a)\operatorname{lc}(b)$; the second claim holds as every factor $\max(1, |\alpha|)$ is at least $1$ and $\operatorname{lc}(a)$ is a nonzero integer. (c) This is Landau's inequality; see von zur Gathen and Gerhard, Section 6.6. $\square$

Let $B$ be an integer with $B \ge 2^n \operatorname{lc}(f) \|f\|_2$; line L3 takes $B = 2^n \operatorname{lc}(f) (\lfloor \|f\|_2 \rfloor + 1)$. Let $k$ be such that $p^k > 2B$.

**Corollary 4.** Let $F \in \mathbb{Z}[x]$ divide $f$, and let $F = h h'$ in $\mathbb{Z}[x]$. Then
$$\Big\| \tfrac{\operatorname{lc}(F)}{\operatorname{lc}(h)} h \Big\|_1 \cdot \Big\| \tfrac{\operatorname{lc}(F)}{\operatorname{lc}(h')} h' \Big\|_1 \le 2^{\deg F} |\operatorname{lc}(F)|\, \mathrm{M}(F) \le B, \qquad \|\operatorname{lc}(F) F\|_\infty \le B.$$

*Proof.* By (a), the left side is at most $\frac{\operatorname{lc}(F)^2}{|\operatorname{lc}(h) \operatorname{lc}(h')|} 2^{\deg h + \deg h'} \mathrm{M}(h)\mathrm{M}(h') = |\operatorname{lc}(F)|\, 2^{\deg F} \mathrm{M}(F)$ by (b). Since $F \mid f$, (b) gives $\mathrm{M}(F) \le \mathrm{M}(f)$ and $|\operatorname{lc}(F)| \le \operatorname{lc}(f)$, and (c) gives $\mathrm{M}(f) \le \|f\|_2$; also $\deg F \le n$. For the second claim, $\|\operatorname{lc}(F) F\|_\infty \le |\operatorname{lc}(F)| \|F\|_1 \le |\operatorname{lc}(F)| 2^{\deg F} \mathrm{M}(F) \le B$. $\square$

## Step 4: the recombination loop (lines L5 to L10)

For $S \subseteq T$ write $g^*_S = \operatorname{lc}(F) \prod_{v \in S} v$ mods $p^k$ and $h^*_S = \operatorname{lc}(F) \prod_{v \in T \setminus S} v$ mods $p^k$. Every factor $h \in \mathbb{Z}[x]$ of $F$ has $p \nmid \operatorname{lc}(h)$, since $\operatorname{lc}(h) \mid \operatorname{lc}(f)$; so by unique factorization in $\mathbb{F}_p[x]$ there is a unique $S(h) \subseteq T$ with $\bar h = \overline{\operatorname{lc}(h)} \prod_{v \in S(h)} \bar v$, and $S(h h_2) = S(h) \sqcup S(h_2)$.

We show that the following hold each time line L6 is reached.

- (I1) $F$ is primitive, $\operatorname{lc}(F) > 0$, $f = F \prod_{g \in G} g$, and $F \equiv \operatorname{lc}(F) \prod_{v \in T} v \pmod {p^k}$; $T$ is not empty.
- (I2) Every $g \in G$ is irreducible, primitive, with $\operatorname{lc}(g) > 0$.
- (I3) Every irreducible factor $h$ of $F$ has $|S(h)| \ge s$.

At line L5 these hold by (1), with $T = \{v_1, \ldots, v_r\}$, $G$ empty and $s = 1$.

**Completeness of the test.** Let $h$ be a primitive factor of $F$ with $\operatorname{lc}(h) > 0$, $h' = F/h$, and $S = S(h)$. Then $g^*_S = \frac{\operatorname{lc}(F)}{\operatorname{lc}(h)} h$. Indeed, $F \equiv \big(\prod_S v\big) \cdot \big(\operatorname{lc}(F) \prod_{T \setminus S} v\big)$ by (I1), and also $F = \big(\operatorname{lc}(h)^{-1} h\big) \cdot \big(\operatorname{lc}(h) h'\big)$ modulo $p^k$, where $\operatorname{lc}(h)^{-1}$ is the inverse modulo $p^k$. Both first factors are monic and reduce to $\prod_S \bar v$, and the second factors reduce to the same polynomial and are coprime to it modulo $p$. Lemma 2 gives $\prod_S v \equiv \operatorname{lc}(h)^{-1} h$, so $\operatorname{lc}(F) \prod_S v \equiv \frac{\operatorname{lc}(F)}{\operatorname{lc}(h)} h \pmod{p^k}$. The right side has integer coefficients of absolute value at most $B < p^k/2$ by Corollary 4, so it is the symmetric representative $g^*_S$. In the same way $h^*_S = \frac{\operatorname{lc}(F)}{\operatorname{lc}(h')} h'$. By Corollary 4, $\|g^*_S\|_1 \|h^*_S\|_1 \le B$: the test of line L7 accepts $S$.

**Soundness of the test.** Let $S$ pass the test, $\|g^*_S\|_1 \|h^*_S\|_1 \le B$. By (I1), $g^*_S h^*_S \equiv \operatorname{lc}(F) F \pmod {p^k}$. Both sides have coefficients of absolute value at most $B < p^k / 2$: the left side because $\|a b\|_\infty \le \|a\|_1 \|b\|_1$, the right side by Corollary 4. So $g^*_S h^*_S = \operatorname{lc}(F) F$. The leading coefficient of $g^*_S$ is $\operatorname{lc}(F)$, because $0 < \operatorname{lc}(F) \le B < p^k/2$; the same holds for $h^*_S$. By Gauss's lemma, $\operatorname{pp}(g^*_S)\operatorname{pp}(h^*_S) = \operatorname{pp}(\operatorname{lc}(F) F) = F$, with positive leading coefficients. Here $\deg g^*_S = \sum_{v \in S} \deg v \ge 1$ and $S(\operatorname{pp}(g^*_S)) = S$.

**Line L8.** If some $S$ of size $s$ passes, let $g = \operatorname{pp}(g^*_S)$ and $F_{\text{new}} = \operatorname{pp}(h^*_S)$. Then $F = g F_{\text{new}}$, so $f = F_{\text{new}} \cdot g \cdot \prod_{G} g'$, the product over the old list $G$. Write $h^*_S = c F_{\text{new}}$ with $c > 0$; $c$ divides $\operatorname{lc}(F)$, so $p \nmid c$, and $F_{\text{new}} \equiv c^{-1} \operatorname{lc}(F) \prod_{T \setminus S} v = \operatorname{lc}(F_{\text{new}}) \prod_{T \setminus S} v \pmod{p^k}$. As $|S| = s \le |T|/2 < |T|$, the new $T$ is not empty. So (I1) holds. For (I2), suppose $g = h_1 h_2$ with $h_1, h_2$ not units; since $g$ is primitive, both have degree at least $1$, so $S(h_1)$ and $S(h_2)$ are nonempty and $S(h_1) \sqcup S(h_2) = S$. An irreducible factor of $h_1$ is an irreducible factor of $F$ with fewer than $s$ elements in its subset, which contradicts (I3). So $g$ is irreducible. (I3) still holds, because every factor of $F_{\text{new}}$ is a factor of $F$ with the same subset.

**Line L9.** If no $S$ of size $s$ passes, then by completeness no irreducible factor $h$ of $F$ has $|S(h)| = s$; with (I3), all have $|S(h)| \ge s + 1$. So (I3) holds for $s + 1$.

**Termination.** Each pass through the loop removes elements from $T$ or increases $s$, and the loop runs only while $2s \le |T| \le r$. So it stops.

**The output (line L10).** At the end $2s > |T|$. Suppose $F$ were reducible; then $F = h_1 h_2$ with nonconstant primitive $h_1, h_2$, and $S(h_1) \sqcup S(h_2) = T$, so one of them, say $S(h_1)$, has at most $|T|/2 < s$ elements. An irreducible factor of $h_1$ then violates (I3). So $F$ is irreducible; it is nonconstant because $T$ is not empty and $\deg F = \sum_{v \in T} \deg v$. With (I1) and (I2), the output $G$ followed by $F$ is a list of irreducible primitive polynomials with positive leading coefficients and product $f$. By unique factorization in $\mathbb{Z}[x]$, it is the factorization of $f$. $\blacksquare$
