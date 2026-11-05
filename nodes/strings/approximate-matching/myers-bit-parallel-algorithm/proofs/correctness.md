---
title: Myers' bit vectors hold the vertical differences of the Sellers table
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m \ge 1$, $|T| = n$, $k \ge 0$. Let $C[i][j]$ be the Sellers table, so $C[0][j] = 0$, $C[i][0] = i$, and for $i, j \ge 1$

$$C[i][j] = \min\bigl(C[i-1][j-1] + \delta_{ij},\; C[i][j-1] + 1,\; C[i-1][j] + 1\bigr), \qquad \delta_{ij} = [P[i-1] \ne T[j-1]],$$

and $C[m][j] = \min_{0 \le h \le j} \operatorname{ed}(P, T[h..j))$, by the correctness proof of [Sellers' algorithm](/sellers-algorithm/). So the end positions to report are the $j$ with $C[m][j] \le k$. For $1 \le i \le m$ define the vertical difference $\Delta v_i(j) = C[i][j] - C[i-1][j]$, and for $0 \le i \le m$, $j \ge 1$, the horizontal difference $\Delta h_i(j) = C[i][j] - C[i][j-1]$. Then $\Delta h_0(j) = 0$.

The claim is: after column $j$ is processed (line L2 for $j = 0$, line L10 for $j \ge 1$), bit $i - 1$ of $Pv$ is set exactly when $\Delta v_i(j) = 1$, bit $i - 1$ of $Mv$ is set exactly when $\Delta v_i(j) = -1$, all $\Delta v_i(j)$ lie in $\{-1, 0, 1\}$, and $score = C[m][j]$. The claim gives the output, because line L11 reports $j$ exactly when $C[m][j] \le k$.

**Column 0.** $C[i][0] - C[i-1][0] = 1$ for all $i$, so $Pv = 1^m$, $Mv = 0$, and $score = m = C[m][0]$, as line L2 sets them.

From now on fix $j \ge 1$ and assume the claim for column $j - 1$. Write $v_i = \Delta v_i(j-1)$, $h_i = \Delta h_i(j)$, $Eq_i = 1 - \delta_{ij}$, and $d_i = C[i][j] - C[i-1][j-1]$ for $1 \le i \le m$.

**Lemma 1 (one cell).** Let $1 \le i \le m$ and $h_{i-1} \in \{-1, 0, 1\}$. Then

1. $d_i = \min(\delta_{ij}, v_i + 1, h_{i-1} + 1) \in \{0, 1\}$, and $d_i = 0$ exactly when $Eq_i = 1$ or $v_i = -1$ or $h_{i-1} = -1$;
2. $h_i = d_i - v_i$ and $\Delta v_i(j) = d_i - h_{i-1}$, and both lie in $\{-1, 0, 1\}$.

*Proof.* $C[i][j-1] = C[i-1][j-1] + v_i$ and $C[i-1][j] = C[i-1][j-1] + h_{i-1}$. Subtract $C[i-1][j-1]$ from the recurrence: $d_i = \min(\delta_{ij}, v_i + 1, h_{i-1} + 1)$. Each term is at least 0, and $\delta_{ij} \le 1$, so $d_i \in \{0, 1\}$, and $d_i = 0$ exactly when one term is 0. Next, $h_i = C[i][j] - C[i][j-1] = d_i - v_i$ and $\Delta v_i(j) = C[i][j] - C[i-1][j] = d_i - h_{i-1}$. Then $h_i \ge -1$ because $d_i \ge 0$ and $v_i \le 1$, and $h_i \le 1$ because $d_i \le v_i + 1$. The same bounds with $h_{i-1}$ in place of $v_i$ give $\Delta v_i(j) \in \{-1, 0, 1\}$. $\square$

Since $h_0 = 0$, induction on $i$ with Lemma 1 gives $h_i \in \{-1, 0, 1\}$ for all $i$, so Lemma 1 holds for all $1 \le i \le m$ and all differences in column $j$ lie in $\{-1, 0, 1\}$. Write $D_i = [d_i = 0]$, $Ph_i = [h_i = 1]$, $Mh_i = [h_i = -1]$, $Pv_i = [v_i = 1]$, $Mv_i = [v_i = -1]$, and $Ph_0 = Mh_0 = 0$.

**Lemma 2 (cell logic).** For $1 \le i \le m$:

1. $D_i = Eq_i \lor Mv_i \lor Mh_{i-1}$;
2. $Ph_i = Mv_i \lor \lnot(D_i \lor Pv_i)$ and $Mh_i = Pv_i \land D_i$;
3. $[\Delta v_i(j) = 1] = Mh_{i-1} \lor \lnot(D_i \lor Ph_{i-1})$ and $[\Delta v_i(j) = -1] = Ph_{i-1} \land D_i$.

*Proof.* Part 1 is Lemma 1, part 1. For part 2, $h_i = d_i - v_i$ with $d_i \in \{0, 1\}$. By part 1, $Mv_i$ implies $D_i$. So $h_i = 1$ holds when $v_i = -1$ (then $d_i = 0$), or when $v_i = 0$ and $d_i = 1$, which is $\lnot D_i \land \lnot Pv_i$ given $\lnot Mv_i$. No other pair gives 1. And $h_i = -1$ only for $d_i = 0$, $v_i = 1$. Part 3 is the same argument for $\Delta v_i(j) = d_i - h_{i-1}$, with $Mh_{i-1} \Rightarrow D_i$ from part 1. $\square$

**Lemma 3 (the carry chain).** Let $X_i = Eq_i \lor Mv_i$. For $1 \le i \le m$, $D_i = 1$ exactly when $X_i = 1$, or there is an $r < i$ with $Eq_r = 1$ and $Pv_q = 1$ for all $r \le q \le i - 1$.

*Proof.* By Lemma 2, $Mh_{i-1} = Pv_{i-1} \land D_{i-1}$ for $i \ge 2$, and $Mh_0 = 0$. So $D_1 = X_1$ and $D_i = X_i \lor (Pv_{i-1} \land D_{i-1})$. Induction on $i$ gives: $D_i = 1$ exactly when there is an $r \le i$ with $X_r = 1$ and $Pv_q = 1$ for $r \le q \le i - 1$. If such an $r$ is less than $i$, then $Pv_r = 1$, so $v_r = 1$, so $Mv_r = 0$ and $X_r = 1$ gives $Eq_r = 1$. $\square$

**Lemma 4 (addition).** Let $A$ and $B$ be $m$-bit vectors with $A \land \lnot B = 0$, and let $S = (A + B) \bmod 2^m$. For $0 \le b < m$, bit $b$ of $S \oplus B$ is $A_b \oplus c_b$, where $c_b = 1$ exactly when there is an $a < b$ with $A_a = 1$ and $B_q = 1$ for all $a \le q \le b - 1$.

*Proof.* Binary addition gives $S_b = A_b \oplus B_b \oplus c_b$, where $c_b$ is the carry into bit $b$: $c_0 = 0$ and $c_{b+1}$ is the majority of $A_b$, $B_b$, $c_b$. Reduction mod $2^m$ drops only the carry out of bit $m - 1$, so it changes no bit below $m$. So $(S \oplus B)_b = A_b \oplus c_b$. If $B_b = 0$ then $A_b = 0$ and $c_{b+1} = 0$, and if $B_b = 1$ then $c_{b+1} = A_b \lor c_b$. So $c_{b+1} = B_b \land (A_b \lor c_b)$, and induction on $b$ from $c_0 = 0$ gives the stated form of $c_b$. $\square$

**The step.** Bit $b = i - 1$ stands for row $i$. Line L6 computes $Xh = (((Eq \land Pv) + Pv) \oplus Pv) \lor Eq$. Apply Lemma 4 with $A = Eq \land Pv$ and $B = Pv$. If $Eq_i = 1$, bit $i - 1$ of $Xh$ is 1. If $Eq_i = 0$, then $A_{i-1} = 0$ and bit $i - 1$ of $Xh$ is $c_{i-1}$, which is 1 exactly when some $r < i$ has $Eq_r = Pv_r = 1$ and $Pv_q = 1$ for $r \le q \le i - 1$. By Lemma 3, $D = Xh \lor Mv$ bit by bit.

Line L7 sets $Ph = Mv \lor \lnot(Xh \lor Pv)$. Where $Mv_i = 1$ both this and $Mv_i \lor \lnot(D_i \lor Pv_i)$ are 1, and where $Mv_i = 0$, $Xh_i = D_i$. So $Ph$ holds $Ph_1, \ldots, Ph_m$ by Lemma 2. Line L7 sets $Mh = Pv \land Xh$, and $Pv \land Xh = Pv \land D$ because $Pv \land Mv = 0$. So $Mh$ holds $Mh_1, \ldots, Mh_m$.

Line L8 reads $h_m$ from bit $m - 1$ of $Ph$ and $Mh$, at most one of which is set, so $score$ becomes $C[m][j-1] + h_m = C[m][j]$.

After line L9, bit $i - 1$ of $Ph$ is $Ph_{i-1}$ and bit $i - 1$ of $Mh$ is $Mh_{i-1}$ for $1 \le i \le m$, since the shift puts bit $i - 2$ into bit $i - 1$, fills bit 0 with $0 = Ph_0 = Mh_0$, and the mask drops the old bit $m - 1$. Line L10 sets $Pv = Mh \lor \lnot(Xv \lor Ph)$ with $Xv = Eq \lor Mv$. Here $D_i = Xv_i \lor Mh_{i-1}$ by Lemma 2, so where $Mh_{i-1} = 1$ both sides of part 3 are 1, and elsewhere $Xv_i = D_i$. So the new bit $i - 1$ of $Pv$ is $[\Delta v_i(j) = 1]$. Line L10 sets $Mv = Ph \land Xv$, and $Ph_{i-1} \land Xv_i = Ph_{i-1} \land D_i$ because $Ph_{i-1}$ and $Mh_{i-1}$ are never both 1. So the new bit $i - 1$ of $Mv$ is $[\Delta v_i(j) = -1]$. This proves the claim for column $j$, and by induction for all columns.

**The distance version.** For $\operatorname{ed}(A, B)$ the first row is $C[0][j] = j$, so $h_0 = 1$, $Ph_0 = 1$ and $Mh_0 = 0$. Lemmas 1 to 3 hold with the same proofs, because they use $h_0 \in \{-1, 0, 1\}$ and $Mh_0 = 0$ only. The only change is that the shift of $Ph$ in line L9 fills bit 0 with 1. Then $score = C[m][n] = \operatorname{ed}(A, B)$. $\blacksquare$
