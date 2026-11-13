---
title: The midpoint Dyson series in the interaction picture gives e^(-i(A+B)t) within (1 + e)^r - 1
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = A + B$ with Hermitian $A$ and $B = \sum_lc_lP_l$, $\lambda_B = \sum_l|c_l| \ge \|B\|$, $\tau = t/r$ with $\lambda_B\tau \le \ln 2$, $h = \tau/M$, $s_q = (q + \tfrac{1}{2})h$, and $H_I(s) = e^{iAs}Be^{-iAs}$. The norm is the spectral norm. $\mathcal{T}\exp(-i\int_a^bH_I)$ is the solution at $b$ of $\tfrac{d}{ds}X(s) = -iH_I(s)X(s)$, $X(a) = I$.

**Lemma 1 (the frame).** $e^{-iH\tau} = e^{-iA\tau}\,U_I(\tau)$ with $U_I(\tau) = \mathcal{T}\exp(-i\int_0^\tau H_I)$.

*Proof.* Let $X(s) = e^{iAs}e^{-iHs}$. Then $X(0) = I$ and $X'(s) = e^{iAs}(iA - iH)e^{-iHs} = -ie^{iAs}Be^{-iAs}e^{iAs}e^{-iHs} = -iH_I(s)X(s)$. The solution of this linear equation is unique, so $X(\tau) = U_I(\tau)$, and $e^{-iH\tau} = e^{-iA\tau}X(\tau)$. $\square$

Since $H$ does not depend on time, all $r$ segments use the same $U_I(\tau)$, and $e^{-iHt} = (e^{-iA\tau}U_I(\tau))^r$.

**Lemma 2 (the weighted sum).** Let $H_q = H_I(s_q)$ and $P = e^{-ihH_{M-1}}\cdots e^{-ihH_0}$. Then $D_{K,M} = \sum_j\beta_jV_j$ (line L3, without the padding, which cancels) is the sum of the terms of degree at most $K$ in $h$ of the expansion of $P$, and $\|D_{K,M} - P\| \le \sum_{k > K}(\lambda_B\tau)^k/k!$.

*Proof.* Write $H_q = \sum_l|c_l|\,G_{q,l}$ with the unitaries $G_{q,l} = e^{iAs_q}\sigma_lP_le^{-iAs_q}$. Fix $k$ and the multiset of cells, with $j_q$ pairs in cell $q$ and $\sum_qj_q = k$. The tuples of $k$ pairs with these cells are obtained by choosing which $j_q$ of the $k$ positions hold cell $q$, in $k!/\prod_qj_q!$ ways, and a term for each position. The ordered product puts the cells in order and, inside cell $q$, keeps the order of the positions, so for a fixed choice of positions, the sum over the terms of the $j_q$ positions of cell $q$ gives $(\sum_l|c_l|G_{q,l})^{j_q} = H_q^{j_q}$. Each choice of positions gives the same product $\prod_q H_q^{j_q}$, later cells to the left. With the weight $h^k/k!$ and the phase $(-i)^k$, the multiset contributes
$$\frac{h^k}{k!}\cdot\frac{k!}{\prod_qj_q!}(-i)^k\prod_qH_q^{j_q} = \prod_q\frac{(-ih)^{j_q}H_q^{j_q}}{j_q!},$$
which is the term of $P = \prod_q\sum_{j_q}(-ihH_q)^{j_q}/j_q!$ with these powers. Summing over all multisets with $k \le K$ gives the part of $P$ of degree at most $K$. The part of degree $k$ has norm at most $\sum h^k\prod_q\lambda_B^{j_q}/j_q! = (Mh\lambda_B)^k/k! = (\lambda_B\tau)^k/k!$ by the multinomial theorem, which gives the bound. The weights of degree $k$ add up to $(\lambda_B\tau)^k/k!$ by the same count. $\square$

**Lemma 3 (one cell).** Let $H(u)$ be twice differentiable on $[c - h/2, c + h/2]$ with $\|H\| \le \lambda$, $\|H'\| \le \mu_1$, $\|H''\| \le \mu_2$, and let $V = \mathcal{T}\exp(-i\int_{c-h/2}^{c+h/2}H)$. Then
$$\|V - e^{-ihH(c)}\| \le h^3\Big(\frac{\mu_2}{24} + \frac{\lambda\mu_1}{4}\Big) + \frac{h^4\mu_1^2}{16}.$$

*Proof.* Let $H_c = H(c)$, $E(s) = e^{-isH_c}$, $V(s) = \mathcal{T}\exp(-i\int_{c-h/2}^{c-h/2+s}H)$ and $\Delta(s) = H(c - h/2 + s) - H_c$. Then $\tfrac{d}{ds}(E^\dagger V) = E^\dagger(iH_c - iH(c - h/2 + s))V = -iE^\dagger\Delta V$, so
$$E(h)^\dagger V(h) - I = -i\int_0^hE^\dagger\Delta V\,ds,$$
and $\|V(h) - E(h)\| = \|E(h)^\dagger V(h) - I\|$. Split $E^\dagger\Delta V = \Delta + (E^\dagger\Delta E - \Delta) + E^\dagger\Delta E(E^\dagger V - I)$.

First, with $u = s - h/2$, Taylor's theorem gives $\|\Delta(s) - uH'(c)\| \le u^2\mu_2/2$, and $\int_{-h/2}^{h/2}u\,du = 0$, so $\|\int_0^h\Delta\,ds\| \le \int_{-h/2}^{h/2}u^2\mu_2/2\,du = h^3\mu_2/24$.

Second, $\tfrac{d}{ds}E^\dagger XE = E^\dagger i[H_c, X]E$, so $\|E(s)^\dagger XE(s) - X\| \le s\|[H_c, X]\|$. With $X = \Delta(s)$, $\|[H_c, \Delta(s)]\| \le 2\lambda\|\Delta(s)\| \le 2\lambda\mu_1|u|$, and $\int_0^hs|s - h/2|\,ds = \int_{-h/2}^{h/2}(h/2 + u)|u|\,du = h^3/8$. So this part is at most $\lambda\mu_1h^3/4$.

Third, $\|E^\dagger V - I\| \le \int_0^s\|\Delta\| \le \mu_1\int_0^h|u|\,ds = \mu_1h^2/4$, so this part is at most $\int_0^h\mu_1|u|\cdot\mu_1h^2/4\,ds = \mu_1^2h^4/16$.

The sum of the three parts is the claim. $\square$

**Lemma 4 (the discretization).** $\|P - U_I(\tau)\| \le d_M$ with $d_M$ as on the page.

*Proof.* $H_I'(s) = ie^{iAs}[A, B]e^{-iAs}$ and $H_I''(s) = -e^{iAs}[A, [A, B]]e^{-iAs}$, so Lemma 3 applies to each cell with $\lambda = \lambda_B$, $\mu_1 = \|[A, B]\|$ and $\mu_2 = \|[A, [A, B]]\|$. $U_I(\tau)$ is the product of the $M$ cell evolutions, later cells to the left. For unitaries, $\|\prod_qX_q - \prod_qY_q\| \le \sum_q\|X_q - Y_q\|$ by a telescoping sum. $M$ times the bound of Lemma 3 with $h = \tau/M$ is $d_M$. $\square$

**Lemma 5 (one segment).** Let $\eta = \sum_{k > K}(\lambda_B\tau)^k/k! + d_M$. The index-0 part of $-WRW^\dagger RW$ on $|0\rangle|\psi\rangle$ is $S|\psi\rangle$ with $S = \tfrac{3}{2}D - \tfrac{1}{2}DD^\dagger D$, $D = D_{K,M}$, and $\|S - U_I(\tau)\| \le e = \eta + \tfrac{3}{2}\eta^2 + \tfrac{1}{2}\eta^3$.

*Proof.* The padded weights add up to 2, so $(\langle 0| \otimes I)W(|0\rangle \otimes I) = D/2$ by the computation of the [linear combination of unitaries](/linear-combination-of-unitaries/) page. Lemmas 3 and 4 of the proof on the page of [truncated Taylor series simulation](/truncated-taylor-series-simulation/) give the block $S$ of $-WRW^\dagger RW$ and, for $D = U + F$ with a unitary $U$ and $\|F\| \le \eta$, the bound $\|S - U\| \le e$; those proofs use only these two facts about $D$. By Lemmas 2 and 4, $D$ is within $\eta$ of $U = U_I(\tau)$. $\square$

**Theorem.** The unnormalized output of IP-SIM is $(e^{-iA\tau}S)^r|\psi\rangle$, and
$$\|(e^{-iA\tau}S)^r - e^{-iHt}\| \le (1 + e)^r - 1.$$
The outcome 0 in all $r$ segments has probability $\|(e^{-iA\tau}S)^r\psi\|^2$.

*Proof.* Each pass of lines L6 and L7 multiplies the system state by $e^{-iA\tau}S$ on outcome 0 (Lemma 5). By Lemma 1, $e^{-iHt} = Y^r$ with $Y = e^{-iA\tau}U_I(\tau)$, and $X = e^{-iA\tau}S$ has $\|X - Y\| = \|S - U_I(\tau)\| \le e$ and $\|X\| \le 1 + e$. Then $X^r - Y^r = \sum_{i=0}^{r-1}X^{r-1-i}(X - Y)Y^i$ has norm at most $e\sum_i(1 + e)^{r-1-i} = (1 + e)^r - 1$. The probability of a sequence of outcomes 0 is the squared norm of the unnormalized state that remains. $\blacksquare$

**Corollary (order 2).** If $K$ is large enough that the truncation term is smaller than $d_M$, the error of a segment is $O(1/M^2)$, so doubling $M$ divides it by about 4. Without the labels with repeated cells, the sum of degree 2 misses $\sum_q(-ih)^2H_q^2/2$, a term of norm up to $\|B\|^2\tau^2/(2M)$, and the order drops to 1.
