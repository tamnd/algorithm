---
title: The Blum-Micali generator outputs B(x_0), ..., B(x_(k-1)) along a permutation, and a perfect predictor for B computes discrete logarithms
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $p \ge 5$ be prime, $g$ a primitive root modulo $p$, $h = (p-1)/2$, $S = \{1, \ldots, p-1\}$, $f(x) = g^x \bmod p$ and $B(x) = 1$ if $x \le h$, else 0. For $y \in S$ write $\log y$ for the unique $x \in S$ with $g^x \equiv y \pmod p$. The full Blum-Micali security theorem, for predictors with small advantage, is cited on the page and not proved here.

**Lemma 1.** $f$ is a permutation of $S$, so $\log$ is well defined, and the state sequence $x_{i+1} = f(x_i)$ is purely periodic.

*Proof.* Since $g$ has order $p - 1$, the values $g^1, \ldots, g^{p-1}$ are distinct elements of $\mathbb{Z}_p^* = S$, so $f$ is injective, hence bijective on the finite set $S$. A sequence of iterates of a permutation of a finite set returns to its starting point. $\square$

**Lemma 2 (output).** Before iteration $i$ of line L2, $x = x_i = f^i(x_0)$. Hence BLUM-MICALI returns $B(x_0), \ldots, B(x_{k-1})$.

*Proof.* Line L1 sets $x = x_0$. Iteration $i$ records $B(x_i)$ at L3 and sets $x = f(x_i) = x_{i+1}$ at L4. $\square$

**Lemma 3 (parity and square roots).** Let $y \in S$, and let $e \in \{0, \ldots, p-2\}$ with $g^e \equiv y$. (a) $y^{h} \equiv 1$ if $e$ is even and $y^{h} \equiv -1$ if $e$ is odd. (b) If $e$ is even and $e \ge 2$, the square roots of $y$ modulo $p$ are $r_1 = g^{e/2}$ and $r_2 = g^{e/2 + h} \equiv -r_1$, with $\log r_1 = e/2$, $\log r_2 = e/2 + h$, $B(\log r_1) = 1$ and $B(\log r_2) = 0$.

*Proof.* (a) $y^h = g^{e h}$, and $g^h \equiv -1$ because $g^h$ squares to 1 and is not 1 ($g$ has order $2h$). So $y^h \equiv (-1)^e$. (b) $r_1^2 = g^e = y$ and $r_2 = r_1 g^h \equiv -r_1$; a nonzero residue has exactly two square roots modulo a prime, and $r_1 \ne r_2$ because $p$ is odd. From $2 \le e \le p - 3$ (as $e$ is even and $\le p - 2$) we get $1 \le e/2 \le h - 1$ and $h + 1 \le e/2 + h \le p - 2$. Both exponents lie in $S$, so they are the logarithms, and $B$ takes the values 1 and 0 on them. $\square$

**Proposition 4 (perfect predictor implies discrete logarithm).** Let $O$ be an oracle with $O(z) = B(\log z)$ for every $z \in S$. The procedure `dlog_with_oracle` of the implementation returns $\log y$ for every $y \in S$, after at most $\lceil \log_2 p \rceil$ rounds, each with one Legendre symbol, one square root modulo $p$ and one oracle call.

*Proof.* Let $e_0 \in \{0, \ldots, p-2\}$ with $g^{e_0} \equiv y$. The procedure keeps an accumulated value $a$ (initially 0), a place value $2^j$ (initially 1) and the current $y = g^{E}$ with $E \in \{0, \ldots, p-2\}$, and maintains the invariant $e_0 = a + 2^j E$. The loop runs while $y \ne 1$, i.e., $E \ne 0$. In a round: if $y^h \equiv -1$, then $E$ is odd by Lemma 3(a); the procedure adds $2^j$ to $a$ and multiplies $y$ by $g^{-1}$, so $E$ becomes $E - 1$ and the invariant holds; if now $y = 1$, it stops. Otherwise $E$ is even and at least 2. It computes a square root $r$ of $y$ and replaces it by $-r$ if $O(r) = 0$; by Lemma 3(b) the result is $g^{E/2}$. Setting $y = g^{E/2}$ and doubling the place value preserves $e_0 = a + 2^{j+1} (E/2)$. Each round at least halves $E$ (rounded down), so there are at most $\lfloor \log_2 (p-2) \rfloor + 1 \le \lceil \log_2 p \rceil$ rounds. At the end $E = 0$ and $a = e_0$. The procedure returns $e_0$ if $e_0 \ne 0$, and $p - 1$ if $e_0 = 0$; both equal $\log y \in S$. $\square$

**Consequence.** Lemma 2 and the identity $x_i = \log x_{i+1}$ (Lemma 1) show that $b_i = B(\log x_{i+1})$, while $b_{i+1}, b_{i+2}, \ldots$ are functions of $x_{i+1}$. A procedure that predicts $b_i$ from $x_{i+1}$ for all states is exactly the oracle $O$ of Proposition 4. Blum and Micali extend Proposition 4 to oracles that are correct on a fraction $\frac12 + \varepsilon$ of inputs; that extension is cited, not proved, on this page. $\blacksquare$
