---
title: Proof of Schützenberger's theorem
proves: [statement]
status: full
---

We prove that a regular language $L \subseteq \Sigma^*$ is star-free if and only if its syntactic monoid $M(L)$ is aperiodic. The second half follows the proof in Pin's book, by induction on the ideals of the monoid.

## Notation

$\Sigma$ is a finite alphabet. A finite monoid $M$ is *aperiodic* if there is an integer $N \ge 0$ with $m^N = m^{N + 1}$ for all $m \in M$; we fix such an $N$. For a language $L$, $\eta_L : \Sigma^* \to M(L)$ is the syntactic morphism, which is onto, and $u \equiv_L v$ means $\eta_L(u) = \eta_L(v)$, that is, $xuy \in L \Leftrightarrow xvy \in L$ for all strings $x, y$. A language $L$ is *$N$-aperiodic* if for all strings $x, u, y$:

$$x u^N y \in L \iff x u^{N + 1} y \in L.$$

For elements $s, t$ of a monoid $M$, write $sM = \{ sx : x \in M \}$, $Ms$ and $MsM$ in the same way, and

- $s \mathrel{\mathcal R} t$ if $sM = tM$,
- $s \mathrel{\mathcal L} t$ if $Ms = Mt$,
- $s \mathrel{\mathcal J} t$ if $MsM = MtM$.

These are equivalence relations, and $s \mathrel{\mathcal R} t$ or $s \mathrel{\mathcal L} t$ implies $s \mathrel{\mathcal J} t$. Since $sx \in sM$, we have $sxM \subseteq sM$ and $MsxM \subseteq MsM$ for all $x$.

**Lemma 0.** For a regular language $L$, $M(L)$ is aperiodic with constant $N$ if and only if $L$ is $N$-aperiodic.

*Proof.* $M(L)$ is finite since $L$ is regular. Each $m \in M(L)$ is $\eta_L(u)$ for some $u$, and $m^N = \eta_L(u^N)$, $m^{N + 1} = \eta_L(u^{N + 1})$. So $m^N = m^{N + 1}$ for all $m$ if and only if $u^N \equiv_L u^{N + 1}$ for all $u$, which is the definition of $N$-aperiodic. $\square$

## Part 1: star-free languages are aperiodic

Star-free languages are regular, since $\emptyset$ and $\{a\}$ are regular and regular languages are closed under union, complement and concatenation. By Lemma 0 it is enough to show that every star-free language is $N$-aperiodic for some $N$. We use induction on a star-free expression.

**Raising $N$.** If $K$ is $N$-aperiodic, it is $N'$-aperiodic for every $N' \ge N$: $x u^{N'} y = x u^N (u^{N' - N} y)$ and $x u^{N' + 1} y = x u^{N + 1} (u^{N' - N} y)$, so the definition with $y' = u^{N' - N} y$ gives the claim.

**Base cases.** $\emptyset$ is $0$-aperiodic, since both sides are false. $\{a\}$ is $2$-aperiodic: if $u = \varepsilon$, the two strings $x u^2 y$ and $x u^3 y$ are both $xy$; if $u \ne \varepsilon$, both have length at least 2, so neither is $a$.

**Complement.** If $K$ is $N$-aperiodic, so is $\Sigma^* \setminus K$, since the condition is symmetric in membership and non-membership.

**Union.** If $K$ is $N_K$-aperiodic and $L$ is $N_L$-aperiodic, both are $N$-aperiodic for $N = \max(N_K, N_L)$, by raising, and then $K \cup L$ is $N$-aperiodic.

**Concatenation.** Let $K$ be $N_K$-aperiodic and $L$ be $N_L$-aperiodic; by raising, we may take $N_K, N_L \ge 1$. Let $N = N_K + N_L + 1$. We show that $KL$ is $N$-aperiodic. Fix $x, u, y$. If $u = \varepsilon$ there is nothing to show, so let $u \ne \varepsilon$. Consider a string $x u^e y$ with $e \in \{N, N + 1\}$, and a factorization $x u^e y = vz$ with $v \in K$, $z \in L$. The cut between $v$ and $z$ lies inside $x$, inside one of the $e$ copies of $u$, at a border between them, or inside $y$. Let $i$ be the number of copies of $u$ that lie entirely in $v$ and $j$ the number that lie entirely in $z$. At most one copy is cut, so $i + j \ge e - 1$. If $i \ge 1$, then $v$ contains $x$ and the first $i$ copies, so $v = x u^i r$ for some string $r$; likewise, if $j \ge 1$, then $z = r' u^j y$ for some string $r'$. Below, $i \ge N_K$ or $j \ge N_L$ always gives $i \ge 1$ or $j \ge 1$ respectively.

- *From $e = N + 1$ to $N$.* Here $i + j \ge N = N_K + N_L + 1$, so $i \ge N_K + 1$ or $j \ge N_L + 1$. If $i \ge N_K + 1$, then $i - 1 \ge N_K$, and since $K$ is $(i - 1)$-aperiodic by raising, $x u^{i - 1} r \in K$. Removing one copy of $u$ from $v$ gives $x u^N y = (x u^{i - 1} r) z \in KL$. If $j \ge N_L + 1$, remove one copy from $z$ in the same way.
- *From $e = N$ to $N + 1$.* Here $i + j \ge N - 1 = N_K + N_L$, so $i \ge N_K$ or $j \ge N_L$. If $i \ge N_K$, then $x u^{i + 1} r \in K$, since $K$ is $i$-aperiodic, and $x u^{N + 1} y = (x u^{i + 1} r) z \in KL$. If $j \ge N_L$, add one copy to $z$.

So $x u^N y \in KL$ if and only if $x u^{N + 1} y \in KL$. By induction, every star-free language is $N$-aperiodic for some $N$, and its syntactic monoid is aperiodic by Lemma 0.

## Part 2: aperiodic languages are star-free

Let $L$ be regular with $M = M(L)$ aperiodic, and let $\varphi = \eta_L$. Since $L = \varphi^{-1}(\varphi(L))$ and $\varphi(L)$ is finite, it is enough to show that $\varphi^{-1}(m)$ is star-free for every $m \in M$. The argument uses only that $\varphi : \Sigma^* \to M$ is an onto morphism to a finite aperiodic monoid. Fix $N$ with $m^N = m^{N + 1}$ for all $m \in M$.

**Lemma 1 (stability).** For $s, t \in M$: if $s \in MstM$, then $s \mathrel{\mathcal R} st$; if $s \in MtsM$, then $s \mathrel{\mathcal L} ts$.

*Proof.* Let $s = x s t y$. By induction on $k$, $s = x^k s (ty)^k$ for all $k \ge 0$. With $k = N + 1$ and $x^{N + 1} = x^N$,

$$s = x^N s (ty)^{N + 1} = \bigl(x^N s (ty)^N\bigr) ty = s t y.$$

So $s \in stM$, hence $sM \subseteq stM$; also $stM \subseteq sM$. So $sM = stM$. The second claim is the mirror image. $\square$

**Lemma 2.** Let $m, s \in M$ with $s \in mM \cap Mm$ and $m \in MsM$. Then $s = m$.

*Proof.* Write $s = mp = qm$ and $m = usv$ with $p, q, u, v \in M$.

1. $m = usv = u m (pv)$. By induction on $k$, $m = u^k m (pv)^k$. With $k = N + 1$ and $u^{N + 1} = u^N$, $m = u^N m (pv)^{N + 1} = \bigl(u^N m (pv)^N\bigr) pv = m p v = s v$.
2. $s = q m = q s v$, using step 1. By induction on $k$, $s = q^k s v^k$. With $k = N + 1$ and $q^{N + 1} = q^N$, $s = q^N s v^{N + 1} = \bigl(q^N s v^N\bigr) v = s v$.

So $s = sv = m$. $\square$

**Corollary 3.** If $1 \in MsM$, then $s = 1$. *Proof.* Lemma 2 with $m = 1$: $s \in 1M \cap M1$ holds for every $s$. $\square$

**The rank.** For $m \in M$ let $r(m) = |M \setminus MmM|$. We show that $\varphi^{-1}(m)$ is star-free by induction on $r(m)$. If $MnM \supsetneq MmM$ then $r(n) < r(m)$. By Corollary 3, $r(m) = 0$, that is $MmM = M \ni 1$, holds only for $m = 1$.

**The element 1.** Let $B = \{ a \in \Sigma : \varphi(a) = 1 \}$. Then $\varphi^{-1}(1) = B^*$. Indeed, if $\varphi(w) = 1$ and $w = x a y$ with $a \in \Sigma$, then $1 = \varphi(x) \varphi(a) \varphi(y) \in M \varphi(a) M$, so $\varphi(a) = 1$ by Corollary 3; and every string over $B$ maps to 1. The language $B^* = \Sigma^* \setminus \bigcup_{a \in \Sigma \setminus B} \Sigma^* a \Sigma^*$ is star-free, with $\Sigma^* = \overline{\emptyset}$.

**An element $m \ne 1$.** Define the finite sets

- $E = \{ (n, a) \in M \times \Sigma : n \varphi(a) \mathrel{\mathcal R} m,\ n \notin mM \}$,
- $F = \{ (a, n) \in \Sigma \times M : \varphi(a) n \mathrel{\mathcal L} m,\ n \notin Mm \}$,
- $C = \{ a \in \Sigma : m \notin M \varphi(a) M \}$,
- $G = \{ (a, n, b) \in \Sigma \times M \times \Sigma : m \in M \varphi(a) n M \cap M n \varphi(b) M,\ m \notin M \varphi(a) n \varphi(b) M \}$,

and the languages

$$U = \bigcup_{(n, a) \in E} \varphi^{-1}(n) \, a, \qquad V = \bigcup_{(a, n) \in F} a \, \varphi^{-1}(n), \qquad W = \bigcup_{(a, n, b) \in G} a \, \varphi^{-1}(n) \, b.$$

**Lemma 4.** Every $n$ that occurs in $E$, $F$ or $G$ satisfies $MnM \supsetneq MmM$.

*Proof.* Case $(n, a) \in E$. From $n \varphi(a) \mathrel{\mathcal R} m$, $m \in n \varphi(a) M \subseteq nM$, so $MmM \subseteq MnM$. Suppose $MmM = MnM$. Then $n \in MmM = M n \varphi(a) M$, since $n \varphi(a) \mathrel{\mathcal J} m$, and Lemma 1 gives $n \mathrel{\mathcal R} n \varphi(a) \mathrel{\mathcal R} m$. So $n \in nM = mM$, which contradicts $n \notin mM$.

Case $(a, n) \in F$: the mirror image, with Lemma 1 for $\mathcal L$.

Case $(a, n, b) \in G$. From $m \in M n \varphi(b) M \subseteq MnM$, $MmM \subseteq MnM$. Suppose $MmM = MnM$. Then $n \in MmM \subseteq M n \varphi(b) M$, and Lemma 1 gives $n \mathrel{\mathcal R} n \varphi(b)$, so $n = n \varphi(b) t$ for some $t \in M$. Then $\varphi(a) n = \varphi(a) n \varphi(b) t$, so $m \in M \varphi(a) n M \subseteq M \varphi(a) n \varphi(b) M$, which contradicts the definition of $G$. $\square$

By Lemma 4 and the induction hypothesis, each $\varphi^{-1}(n)$ in $U$, $V$ and $W$ is star-free. So $U$, $V$ and $W$ are finite unions of concatenations of star-free languages and letters, and they are star-free; so is the finite set $C$ of one-letter strings.

**Lemma 5.** For $m \ne 1$,

$$\varphi^{-1}(m) = \bigl( U \Sigma^* \cap \Sigma^* V \bigr) \setminus \Sigma^* (C \cup W) \Sigma^*.$$

*Proof of $\subseteq$.* Let $\varphi(w) = m$.

- *$w \in U \Sigma^*$.* Let $p$ be the shortest prefix of $w$ with $\varphi(p) \mathrel{\mathcal R} m$; it exists, since $w$ itself qualifies. $p \ne \varepsilon$: else $1 \mathrel{\mathcal R} m$, so $1 \in mM \subseteq MmM$ and $m = 1$ by Corollary 3. Write $p = p' a$ with $a \in \Sigma$, and $n = \varphi(p')$. Then $n \varphi(a) = \varphi(p) \mathrel{\mathcal R} m$. If $n \in mM$, then $nM \subseteq mM = \varphi(p) M \subseteq nM$, so $n \mathrel{\mathcal R} m$, and the shorter prefix $p'$ qualifies, a contradiction. So $(n, a) \in E$ and $p \in \varphi^{-1}(n) a \subseteq U$.
- *$w \in \Sigma^* V$*, by the mirror argument with the shortest suffix $s$ with $\varphi(s) \mathrel{\mathcal L} m$.
- *$w \notin \Sigma^* C \Sigma^*$.* If $w = x a y$ with $a \in C$, then $m = \varphi(x) \varphi(a) \varphi(y) \in M \varphi(a) M$, a contradiction.
- *$w \notin \Sigma^* W \Sigma^*$.* If $w = x a g b y$ with $(a, \varphi(g), b) \in G$, then $m \in M \varphi(a) \varphi(g) \varphi(b) M$, a contradiction.

*Proof of $\supseteq$.* Let $w$ be in the right side and $s = \varphi(w)$. Since $w \in U \Sigma^*$, $w = p a x$ with $(\varphi(p), a) \in E$, so $s \in \varphi(p) \varphi(a) M = mM$, where the equality is $\varphi(p) \varphi(a) \mathrel{\mathcal R} m$. In the same way $w \in \Sigma^* V$ gives $s \in Mm$.

We show $m \in MsM$. Suppose not. Then some factor $f$ of $w$ has $m \notin M \varphi(f) M$, for example $f = w$; take a shortest one. $f \ne \varepsilon$, since $M \varphi(\varepsilon) M = M \ni m$. If $|f| = 1$, then $f \in C$ and $w \in \Sigma^* C \Sigma^*$, a contradiction. If $|f| \ge 2$, write $f = a g b$ with $a, b \in \Sigma$ and $n = \varphi(g)$. The factors $ag$ and $gb$ are shorter than $f$, so $m \in M \varphi(a) n M$ and $m \in M n \varphi(b) M$; and $m \notin M \varphi(a) n \varphi(b) M$. So $(a, n, b) \in G$, $f \in W$, and $w \in \Sigma^* W \Sigma^*$, a contradiction.

So $s \in mM \cap Mm$ and $m \in MsM$, and Lemma 2 gives $s = m$, that is, $w \in \varphi^{-1}(m)$. $\square$

**Conclusion.** The right side of Lemma 5 is built from star-free languages by concatenation, intersection and difference, so it is star-free. By induction on $r(m)$, $\varphi^{-1}(m)$ is star-free for every $m \in M$, and $L = \bigcup_{m \in \varphi(L)} \varphi^{-1}(m)$ is star-free. Together with Part 1, this proves the theorem. $\blacksquare$

## A worked case

For $L = (ab)^*$ over $\{a, b\}$, $M(L) = \{1, a, b, ab, ba, 0\}$ (see the [syntactic monoid](/syntactic-monoid/) page), and no letter maps to 1, so $B = \emptyset$ and $\varphi^{-1}(1) = \{\varepsilon\}$. For $m = ab$: the $\mathcal R$-class of $ab$ is $\{a, ab\}$ and its $\mathcal L$-class is $\{b, ab\}$, which give $E = \{(1, a)\}$ and $F = \{(b, 1)\}$. Both letters satisfy $ab \in M \varphi(c) M$, so $C = \emptyset$, and $G = \{(a, 1, a), (b, 1, b)\}$. So $U = \{a\}$, $V = \{b\}$, $W = \{aa, bb\}$, and Lemma 5 gives

$$\varphi^{-1}(ab) = \bigl(a \Sigma^* \cap \Sigma^* b\bigr) \setminus \Sigma^* \{aa, bb\} \Sigma^* = (ab)^+.$$

With $\varphi(L) = \{1, ab\}$, $L = \{\varepsilon\} \cup (ab)^+$.
