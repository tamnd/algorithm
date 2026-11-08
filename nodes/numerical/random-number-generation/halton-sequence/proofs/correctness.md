---
title: The Halton algorithm computes the radical inverses, and the sequence has star discrepancy O((log N)^d / N)
proves: [correctness]
status: full
---

We use the pseudocode of the page. Bases $b_1, \ldots, b_d \ge 2$ are pairwise coprime. For a base $b$ and $i = \sum_{j \ge 0} a_j b^j$ with $0 \le a_j < b$ (finitely many nonzero), $\varphi_b(i) = \sum_{j \ge 0} a_j b^{-j-1}$, and $u_i = (\varphi_{b_1}(i), \ldots, \varphi_{b_d}(i))$.

**Lemma 1 (the loop).** For one coordinate with base $b$, before pass $j$ of the loop L3 to L5 (passes counted from 0), $n = \lfloor i / b^j \rfloor$, $f = b^{-j-1}$ and $x = \sum_{t < j} a_t b^{-t-1}$. The loop ends with $x = \varphi_b(i)$.

*Proof.* At $j = 0$ this is line L2. If it holds before pass $j$ and $n > 0$, then $n \bmod b = \lfloor i / b^j \rfloor \bmod b = a_j$, so L4 adds $a_j b^{-j-1}$, and L5 makes $n = \lfloor i / b^{j+1} \rfloor$ and $f = b^{-j-2}$. The loop stops at the first $j$ with $\lfloor i / b^j \rfloor = 0$, i.e., $b^j > i$, when $a_t = 0$ for all $t \ge j$. Then $x = \sum_{t \ge 0} a_t b^{-t-1} = \varphi_b(i)$. $\square$

So HALTON returns $u_i$ (with real arithmetic; the reference implementation uses exact integers).

**Lemma 2 (one coordinate).** Let $e \ge 0$ and $0 \le c < b^e$, with base-$b$ digits $c = \sum_{t<e} c_t b^{e-1-t}$. Then $\varphi_b(i) \in [c\, b^{-e}, (c+1)\, b^{-e})$ if and only if $i \equiv \sum_{t<e} c_t b^t \pmod{b^e}$.

*Proof.* Write $\varphi_b(i) = \sum_{t<e} a_t b^{-t-1} + \tau$ with $0 \le \tau = \sum_{t \ge e} a_t b^{-t-1}$. Since only finitely many $a_t$ are nonzero and each is at most $b - 1$, $\tau < \sum_{t \ge e} (b-1) b^{-t-1} = b^{-e}$. Hence $\lfloor b^e \varphi_b(i) \rfloor = \sum_{t<e} a_t b^{e-1-t}$, which equals $c$ if and only if $a_t = c_t$ for all $t < e$, that is, if and only if $i \bmod b^e = \sum_{t<e} a_t b^t = \sum_{t<e} c_t b^t$. $\square$

**Lemma 3 (elementary boxes).** Let $E = \prod_{k=1}^d [c_k b_k^{-e_k}, (c_k + 1) b_k^{-e_k})$ with $e_k \ge 0$, $0 \le c_k < b_k^{e_k}$, and $M = \prod_k b_k^{e_k}$, so $\operatorname{vol}(E) = 1/M$. For every integer $s \ge 0$ and $N \ge 1$, the number $A(E)$ of $i \in \{s, \ldots, s + N - 1\}$ with $u_i \in E$ satisfies $|A(E) - N/M| < 1$.

*Proof.* By Lemma 2, $u_i \in E$ if and only if $i \equiv r_k \pmod{b_k^{e_k}}$ for each $k$, for certain residues $r_k$. The moduli $b_k^{e_k}$ are pairwise coprime because the bases are, so by the Chinese remainder theorem the system is equivalent to $i \equiv r \pmod M$ for one residue $r$. Among $N$ consecutive integers, the number in a fixed residue class modulo $M$ is $\lfloor N/M \rfloor$ or $\lceil N/M \rceil$, both within distance less than 1 of $N/M$. $\square$

**Lemma 4 (splitting an interval).** Let $b \ge 2$, $L \ge 0$ and $0 \le y \le 1$. There are disjoint intervals $J_1, \ldots, J_m$, each of the form $[c\, b^{-e}, (c+1) b^{-e})$ with $0 \le e \le L$, and a set $I$ that is either empty or such an interval with $e = L$, such that $m + 1 \le (b-1) L + 1$, and $U = J_1 \cup \cdots \cup J_m$ satisfies $U \subseteq [0, y) \subseteq U \cup I$.

*Proof.* If $y = 1$ and $L \ge 1$, take $m = 1$, $J_1 = [0, 1)$ (level 0) and $I = \emptyset$; then $m = 1 \le (b-1)L$. If $y = 1$ and $L = 0$, take $m = 0$ and $I = [0, 1)$. Now let $y < 1$, and let $y = \sum_{t \ge 1} y_t b^{-t}$ be the base-$b$ expansion that does not end in an infinite run of digits $b - 1$; write $p_e = \sum_{t=1}^{e} y_t b^{-t}$, so $p_0 = 0$. For $1 \le e \le L$ and $0 \le v < y_e$, let $J_{e,v} = [p_{e-1} + v\, b^{-e}, p_{e-1} + (v+1)\, b^{-e})$. Since $p_{e-1}$ is a multiple of $b^{-(e-1)}$, hence of $b^{-e}$, each $J_{e,v}$ is elementary of level $e$. For fixed $e$ they tile $[p_{e-1}, p_e)$, so all of them together tile $[0, p_L)$, and their number is $\sum_{e=1}^{L} y_e \le (b-1) L$. Let $I = [p_L, p_L + b^{-L})$, elementary of level $L$. The tail $y - p_L = \sum_{t > L} y_t b^{-t}$ is at least 0 and, because the digits are not eventually all $b-1$, less than $b^{-L}$. So $[0, p_L) \subseteq [0, y) \subseteq [0, p_L) \cup I$. $\square$

**Theorem.** For every $s \ge 0$ and $N \ge 1$, the points $u_s, \ldots, u_{s+N-1}$ have star discrepancy
$$D_N^* \le \frac{1}{N} \left( d + \prod_{k=1}^d \big( (b_k - 1) L_k + 1 \big) \right), \qquad L_k = \lceil \log_{b_k} N \rceil.$$

*Proof.* Fix $y \in [0,1]^d$ and write $A(B)$ for the number of the $N$ points in a set $B$. For each $k$, Lemma 4 with $b = b_k$, $L = L_k$ gives $U_k \subseteq [0, y_k) \subseteq U_k \cup I_k$, where $U_k$ is a disjoint union of at most $n_k = (b_k - 1) L_k$ elementary intervals and $I_k$ is empty or has length $b_k^{-L_k} \le 1/N$. Let $P = \prod_k U_k$ and $Q = \prod_k (U_k \cup I_k)$. Then $P \subseteq [0, y) \subseteq Q$. Expanding the products, $P$ and $Q$ are disjoint unions of at most $\prod_k (n_k + 1)$ elementary boxes. By Lemma 3, $A(P) > N \operatorname{vol}(P) - \prod_k (n_k + 1)$ and $A(Q) < N \operatorname{vol}(Q) + \prod_k (n_k + 1)$. Also
$$\operatorname{vol}(Q) - \operatorname{vol}(P) \le \sum_{k=1}^d |I_k| \le \frac{d}{N},$$
since replacing one factor $|U_k|$ by $|U_k| + |I_k|$ at a time raises the product of numbers in $[0,1]$ by at most $|I_k|$ each time. Hence, with $\Pi = \prod_k (n_k + 1)$,
$$A([0,y)) \ge A(P) > N \operatorname{vol}(P) - \Pi \ge N \operatorname{vol}[0,y) - d - \Pi,$$
$$A([0,y)) \le A(Q) < N \operatorname{vol}(Q) + \Pi \le N \operatorname{vol}[0,y) + d + \Pi.$$
Dividing by $N$ and taking the supremum over $y$ gives the bound. $\square$

**Corollary.** $D_N^* = O((\log N)^d / N)$ with a constant depending only on $d$ and the bases; in particular $D_N^* \to 0$, so each Halton sequence is equidistributed in $[0, 1)^d$.
