---
title: BOSTAN-MORI returns the coefficient of x^N in P/Q with two products per halving of N
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $P, Q \in R[x]$ with $Q(0)$ a unit, and $N \ge 0$. A polynomial or power series $F$ with $F(0)$ a unit is invertible in $R[[x]]$, and $[x^n] F$ denotes the coefficient of $x^n$. For a polynomial $U$, $U_{\mathrm{even}}(y) = \sum_i u_{2i} y^i$ and $U_{\mathrm{odd}}(y) = \sum_i u_{2i+1} y^i$, so $U(x) = U_{\mathrm{even}}(x^2) + x\, U_{\mathrm{odd}}(x^2)$.

**Lemma 1 (the product is even).** $V = Q(x) Q(-x)$ satisfies $V(x) = V_{\mathrm{even}}(x^2)$, and $V_{\mathrm{even}}(0) = Q(0)^2$ is a unit.

*Proof.* Replacing $x$ by $-x$ is a ring endomorphism of $R[x]$ that maps $V$ to $Q(-x) Q(x) = V$. Comparing coefficients, $v_i (-1)^i = v_i$, so $2 v_i = 0$ for odd $i$. This does not yet give $v_i = 0$ when $2$ is a zero divisor, so we compute directly: $v_i = \sum_{j + l = i} (-1)^l q_j q_l$. For odd $i$, the pairs $(j, l)$ and $(l, j)$ are distinct, since $j = l$ would make $i$ even, and they contribute $(-1)^l q_j q_l + (-1)^j q_l q_j = ((-1)^l + (-1)^j) q_j q_l = 0$, because $j + l$ odd means $j$ and $l$ have different parity. So $v_i = 0$ for odd $i$, and $V(x) = V_{\mathrm{even}}(x^2)$. The constant term is $v_0 = q_0 \cdot q_0$, a product of units. $\square$

**Lemma 2 (one step).** Let $U = P(x) Q(-x)$, $W = V_{\mathrm{even}}$, and $M \ge 0$. Then $[x^{2M}]\, P/Q = [y^M]\, U_{\mathrm{even}}/W$ and $[x^{2M+1}]\, P/Q = [y^M]\, U_{\mathrm{odd}}/W$.

*Proof.* $Q(-x)$ has constant term $Q(0)$, a unit, so it is invertible in $R[[x]]$ and $P/Q = P(x) Q(-x) / (Q(x) Q(-x)) = U / W(x^2)$ by Lemma 1. The map $y \mapsto x^2$ is a ring homomorphism $R[[y]] \to R[[x]]$, so $1/W(x^2) = (1/W)(x^2)$, a series with only even powers of $x$. Hence
$$\frac{P}{Q} = \Big(\frac{U_{\mathrm{even}}}{W}\Big)(x^2) + x \Big(\frac{U_{\mathrm{odd}}}{W}\Big)(x^2).$$
The first series has only even powers of $x$ and the second only odd powers. The coefficient of $x^{2M}$ comes from the first, and equals $[y^M]\, U_{\mathrm{even}}/W$. The coefficient of $x^{2M+1}$ comes from the second, and equals $[y^M]\, U_{\mathrm{odd}}/W$. $\square$

**Theorem (correctness).** BOSTAN-MORI$(P, Q, N)$ returns $[x^N]\, P/Q$.

*Proof.* Let $c = [x^N]\, P/Q$ for the input. We claim that at each test of line L1, $Q(0)$ is a unit and $[x^{N}]\, P/Q = c$ for the current values. This holds at the start. If $N \ge 1$, lines L2 to L7 replace $(P, Q, N)$ by $(U_{\mathrm{even}}, W, N/2)$ for even $N$, or by $(U_{\mathrm{odd}}, W, (N-1)/2)$ for odd $N$. In both cases the coefficient is kept by Lemma 2, and $W(0)$ is a unit by Lemma 1. Each step replaces $N \ge 1$ by $\lfloor N/2 \rfloor < N$, so the loop ends with $N = 0$. Then $[x^0]\, P/Q = P(0)\, Q(0)^{-1}$, because the constant term of a product of series is the product of the constant terms. Line L8 returns it. The early exit of the implementation when $P = 0$ returns $0$, which is correct, since then $P/Q = 0$. $\square$

**Theorem (cost).** Let $d = \deg Q$ and $\deg P < d$, and assume $M$ is nondecreasing. For $N \ge 1$, the algorithm runs $\lfloor \log_2 N \rfloor + 1$ steps, each with two products of polynomials with at most $d + 1$ coefficients and $O(d)$ other operations, and one inversion at the end. So it uses at most $2M(d + 1)(\log_2 N + 1) + O(d \log N)$ ring operations.

*Proof.* *Steps.* $N \mapsto \lfloor N/2 \rfloor$ reaches $0$ from $N \ge 1$ after exactly $\lfloor \log_2 N \rfloor + 1$ steps.

*Degrees stay bounded.* Suppose $\deg Q \le d$ and $\deg P \le d - 1$ at the start of a step. Then $\deg Q(-x) \le d$, $\deg U \le 2d - 1$ and $\deg V \le 2d$. The new $P$ is $U_{\mathrm{even}}$ or $U_{\mathrm{odd}}$, whose degree is at most $\lfloor (2d - 1)/2 \rfloor = d - 1$. The new $Q$ is $V_{\mathrm{even}}$, of degree at most $d$. By induction these bounds hold at every step.

*One step.* Line L2 negates at most $d$ coefficients. Lines L3 and L4 multiply polynomials with at most $d$ and $d + 1$ coefficients, and $d + 1$ and $d + 1$ coefficients, so they cost at most $2M(d + 1)$. Lines L5 to L7 only select coefficients. Adding the steps and line L8 gives the bound. $\blacksquare$
