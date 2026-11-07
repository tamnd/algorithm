---
title: Correctness of Householder's methods
proves: [correctness, termination, convergence-rate]
status: full
---

We use the notation of the page: $e = x - x^*$, $a_j = f^{(j)}(x)/j!$, $b_n = (1/f)^{(n)}(x)/n!$ and $\beta_n = a_0^{n+1}b_n$. All statements are in exact arithmetic.

## Termination

Each pass of the loop L1 either returns at L3, L5, L6 or L8, or increases $k$ by one; after $K$ passes L9 returns. So there are at most $K$ calls of the derivative routine, that is $K(d + 1)$ values. Non-finite values or a non-finite step raise an error, which also ends the run.

## Lemma 1 (the recurrence computes the step)

If $f \in C^d$ near $x$ and $a_0 = f(x) \ne 0$, then the numbers $\beta_n$ of line L4 equal $a_0^{n+1}b_n$, and $a_0\beta_{d-1}/\beta_d = d\,(1/f)^{(d-1)}(x)/(1/f)^{(d)}(x)$ whenever $\beta_d \ne 0$.

*Proof.* Near $x$, $1/f$ is $C^d$, and by the Leibniz rule the derivatives of the product $f \cdot (1/f) = 1$ give $\sum_{j=0}^{n} a_j b_{n-j} = 0$ for $1 \le n \le d$, with $a_0b_0 = 1$. Hence $b_n = -a_0^{-1}\sum_{j=1}^n a_jb_{n-j}$. Multiplying by $a_0^{n+1}$ and writing $a_0^{n}b_{n-j} = a_0^{j-1}\cdot a_0^{n-j+1}b_{n-j}$ gives $\beta_n = -\sum_{j=1}^n a_ja_0^{j-1}\beta_{n-j}$ and $\beta_0 = 1$, the recurrence of L4. Finally $d\,(1/f)^{(d-1)}/(1/f)^{(d)} = d\,(d-1)!\,b_{d-1}/(d!\,b_d) = b_{d-1}/b_d = a_0\beta_{d-1}/\beta_d$. $\square$

So the code performs exactly the step $x \leftarrow x + d\,(1/f)^{(d-1)}/(1/f)^{(d)}$, and $\beta_d = 0$ exactly when $(1/f)^{(d)}(x) = 0$.

## Theorem 1 (order $d + 1$ at a simple root)

Let $f \in C^{d+1}$ near $x^*$ with $f(x^*) = 0 \ne f'(x^*)$. Let $\varphi(x) = \int_0^1 f'(x^* + t(x - x^*))\,dt$, so that $f = e\varphi$, and $\psi = 1/\varphi$. Then near $x^*$, for $e \ne 0$,
$$e_{\text{new}} = \frac{(-1)^d\,\psi^{(d)}(x)}{d!\,T_d(x)}\,e^{d+1}, \qquad T_d(x) = \sum_{i=0}^{d} \frac{\psi^{(i)}(x)}{i!}(-e)^i,$$
with $T_d(x) \to \psi(x^*) = 1/f'(x^*)$. Hence there is $\rho > 0$ such that from every $x_0$ with $|e_0| \le \rho$ the iterates converge to $x^*$ and $e_{k+1}/e_k^{d+1} \to (-1)^d f'(x^*)\psi^{(d)}(x^*)/d!$.

*Proof.* Since $f' \in C^d$, differentiation under the integral shows $\varphi \in C^d$, and $\varphi(x^*) = f'(x^*) \ne 0$, so $\psi \in C^d$ near $x^*$. For $e \ne 0$, $1/f = \psi \cdot e^{-1}$, and $(e^{-1})^{(j)} = (-1)^j j!\,e^{-j-1}$. The Leibniz rule gives
$$(1/f)^{(n)} = \sum_{i=0}^{n}\binom{n}{i}\psi^{(i)}(-1)^{n-i}(n-i)!\,e^{-(n-i)-1}, \quad\text{so}\quad \frac{(-1)^n e^{n+1}}{n!}(1/f)^{(n)} = \sum_{i=0}^{n}\frac{\psi^{(i)}}{i!}(-e)^i = T_n(x).$$
For $n = d$ every term with $i \ge 1$ tends to 0 as $x \to x^*$, so $T_d(x) \to \psi(x^*) \ne 0$, and $T_d \ne 0$ near $x^*$. Then the step is
$$s = d\,\frac{(1/f)^{(d-1)}}{(1/f)^{(d)}} = d\,\frac{(-1)^{d-1}(d-1)!\,T_{d-1}\,e^{-d}}{(-1)^d\,d!\,T_d\,e^{-d-1}} = -e\,\frac{T_{d-1}}{T_d},$$
and $e_{\text{new}} = e + s = e\,(T_d - T_{d-1})/T_d$. Since $T_d - T_{d-1} = \psi^{(d)}(x)(-e)^d/d!$, this is the identity claimed. It is exact, not asymptotic.

For the ball: choose $\rho$ so that on $[x^* - \rho, x^* + \rho]$ we have $|T_d| \ge |\psi(x^*)|/2$ and $|\psi^{(d)}| \le M$, and $\rho^d \le d!\,|\psi(x^*)|/(4M)$. Then $|e_{\text{new}}| \le 2M|e|^{d+1}/(d!\,|\psi(x^*)|) \le |e|/2$, so by induction the iterates stay in the ball and $|e_k| \le 2^{-k}\rho \to 0$. If some $e_k = 0$, then $f(x_k) = 0$ and the method stops at L3. Otherwise continuity of $\psi^{(d)}$ and $T_d$ gives the limit of $e_{k+1}/e_k^{d+1}$, using $\psi(x^*) = 1/f'(x^*)$. $\square$

For $d = 1$, $\psi = (1/f'(x^*))(1 - c_2e + \cdots)$ with $c_j = f^{(j)}(x^*)/(j!\,f'(x^*))$, and the constant is $c_2$, Newton's; for $d = 2$ it is $c_2^2 - c_3$, Halley's. The order is exactly $d + 1$ when $\psi^{(d)}(x^*) \ne 0$. The result is local; it says nothing about starts outside the ball.

## Theorem 2 (multiple roots)

Let $f = (x - x^*)^m h$ with $m \ge 2$, $h \in C^d$ near $x^*$ and $h(x^*) \ne 0$. Then $e_{\text{new}} = \frac{m-1}{m+d-1}e + O(e^2)$, and the iteration converges linearly with this rate from every start close enough to $x^*$.

*Proof.* Write $1/f = \psi\,e^{-m}$ with $\psi = 1/h \in C^d$, $\psi(x^*) \ne 0$. With the rising factorial $(m)_j = m(m+1)\cdots(m+j-1)$, $(e^{-m})^{(j)} = (-1)^j(m)_j\,e^{-m-j}$, and the Leibniz rule gives
$$(1/f)^{(n)} = (-1)^n(m)_n\,e^{-m-n}\Bigl(\psi(x) + \sum_{i=1}^{n}\binom{n}{i}\frac{(m)_{n-i}}{(m)_n}\psi^{(i)}(x)(-e)^i\Bigr) = (-1)^n(m)_n\,e^{-m-n}\bigl(\psi(x) + O(e)\bigr),$$
uniformly near $x^*$ because $\psi^{(i)}$ is bounded there. Therefore
$$s = d\,\frac{(1/f)^{(d-1)}}{(1/f)^{(d)}} = -\frac{d\,(m)_{d-1}}{(m)_d}\,e\,\bigl(1 + O(e)\bigr) = -\frac{d}{m+d-1}\,e\,\bigl(1 + O(e)\bigr),$$
and $e_{\text{new}} = e + s = \frac{m-1}{m+d-1}e + O(e^2)$. With $r = (m-1)/(m+d-1) < 1$, choose $\rho$ so that $|e_{\text{new}}| \le \frac{1+r}{2}|e|$ for $0 < |e| \le \rho$; induction gives $|e_k| \le (\frac{1+r}{2})^k\rho \to 0$, and then $e_{k+1}/e_k \to r$. $\square$

For $f = x^m$ the sum is empty ($\psi = 1$) and $x_{\text{new}} = \frac{m-1}{m+d-1}x$ exactly, which the tests check in rational arithmetic. Applying Theorem 1 to $F = f^{1/m}$, which has a simple root when $h > 0$, shows that Householder's method on $f^{1/m}$ has order $d + 1$.

## Floating point

The theorems are about exact arithmetic. In double precision, near a simple root the computed $f$ is dominated by rounding, and the run ends either at a computed zero of $f$ (status "exact") or with a step below the relative tolerance; near a root of multiplicity $m$ the attainable error is of order $u^{1/m}$ times the scale of the problem. These statements are observations on the test functions, not theorems.
