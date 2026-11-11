---
title: Semi-honest BGW outputs C(x) and keeps every sharing at degree t
proves: [correctness]
status: full
---

We prove that the protocol of lines L1 to L11 outputs $C(x)$ when all parties follow it and $2t < n$, and that every wire is shared with a polynomial of degree at most $t$. We prove the same for the GRR degree reduction.

**Setting.** $\mathbb{F} = \mathbb{F}_p$ with $p > n$, and party $P_i$ has the point $i$. A *$d$-sharing* of $v$ is a vector $(g(1), \ldots, g(n))$ for a polynomial $g$ of degree at most $d$ with $g(0) = v$. Let $v_w$ be the value of wire $w$ in the plain evaluation of $C$.

**Fact 1 (interpolation).** If $g$ has degree at most $n - 1$, then $g$ is determined by $g(1), \ldots, g(n)$, and $g(0) = \sum_{i=1}^n \lambda_i g(i)$ with the Lagrange coefficients $\lambda_i = \prod_{j \ne i} j / (j - i)$. This is the uniqueness of the interpolating polynomial through $n$ distinct points.

**Fact 2 (linearity).** If $(g(i))_i$ is a $d$-sharing of $u$ and $(g'(i))_i$ is a $d$-sharing of $u'$, then for constants $\alpha, \beta$ the vector $(\alpha g(i) + \beta g'(i))_i$ is a $d$-sharing of $\alpha u + \beta u'$, by the polynomial $\alpha g + \beta g'$.

**Invariant (D).** When wire $w$ has been processed, the parties hold a $t$-sharing of $v_w$.

**Inputs.** Line L1 deals $f_w(1), \ldots, f_w(n)$ for a polynomial $f_w$ of degree $t$ with $f_w(0) = x_w$: a $t$-sharing.

**Linear gates.** Lines L3 and L4 apply Fact 2 with $(\alpha, \beta) = (1, 1)$ or $(\kappa, 0)$.

**Multiplication gate.** Let $f_a, f_b$ be the degree-$t$ polynomials of the inputs. Line L6 gives $h_i = f_a(i) f_b(i) = h(i)$ for $h = f_a f_b$, which has degree at most $2t$ and $h(0) = v_a v_b$.

*Randomization (line L7).* Each $P_i$ deals a $2t$-sharing of $0$ by a polynomial $q_i$. By Fact 2 the vector $\tilde h_j = h(j) + \sum_i q_i(j)$ is a $2t$-sharing of $v_a v_b$, by $\tilde h = h + \sum_i q_i$.

*Truncation (lines L8 to L10).* Since $2t \le n - 1$, Fact 1 says that $\tilde h$ is determined by $\tilde h(1), \ldots, \tilde h(n)$. Write $\tilde h(z) = \sum_{m=0}^{2t} c_m z^m$ and let $g(z) = \sum_{m=0}^{t} c_m z^m$, the truncation. With $V$ the $n \times n$ Vandermonde matrix $V_{jm} = j^m$ ($m = 0, \ldots, n-1$) and $P$ the diagonal matrix that keeps coordinates $0, \ldots, t$, we have $(c_0, \ldots, c_{n-1}) = V^{-1}(\tilde h(1), \ldots, \tilde h(n))$ (with $c_m = 0$ for $m > 2t$), so the vector $(g(1), \ldots, g(n))$ equals $A (\tilde h(1), \ldots, \tilde h(n))$ with $A = V P V^{-1}$. Line L8 has each $P_i$ deal a $t$-sharing $([\tilde h(i)]_1, \ldots, [\tilde h(i)]_n)$ of $\tilde h(i)$. Fix a receiving party $P_r$. By Fact 2, the values $\sum_i A_{ri} [\tilde h(i)]_j$ for $j = 1, \ldots, n$ that line L9 computes form a $t$-sharing of $\sum_i A_{ri} \tilde h(i) = g(r)$. In line L10, $P_r$ gets all $n \ge t + 1$ of these shares and, by Fact 1 for a polynomial of degree $t \le n - 1$, reconstructs exactly $g(r)$. So after line L10 each $P_r$ holds $g(r)$. The polynomial $g$ has degree at most $t$ and $g(0) = c_0 = \tilde h(0) = v_a v_b$, so $(g(1), \ldots, g(n))$ is a $t$-sharing of $v_c$.

*GRR instead of lines L7 to L10.* Each $P_i$ deals a $t$-sharing of $h(i)$ by a polynomial $s_i$, and $P_j$ sets $[c]_j = \sum_i \lambda_i s_i(j)$. By Fact 2 this is a $t$-sharing, by the polynomial $\sum_i \lambda_i s_i$, of $\sum_i \lambda_i h(i)$, and by Fact 1 (with $\deg h \le 2t \le n - 1$) this equals $h(0) = v_a v_b$.

So (D) holds after every gate, by induction over the gates in topological order (line L2).

**Output.** Line L11 reconstructs each output wire from its $n$ shares. By (D) and Fact 1, the result is $f_w(0) = v_w$. So the protocol outputs $C(x)$. $\blacksquare$

**Remark on $t < n/2$.** The argument used $2t \le n - 1$ twice: to recover $h(0)$ from $n$ points of the degree-$2t$ product, and to recover $\tilde h$ for the truncation. With $2t \ge n$, the $n$ products no longer determine $h$, and the multiplication fails.
