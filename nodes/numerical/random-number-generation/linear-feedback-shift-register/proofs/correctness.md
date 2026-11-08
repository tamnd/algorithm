---
title: An LFSR computes its linear recurrence, and its period is 2^k - 1 from each nonzero state exactly when the polynomial is primitive
proves: [correctness]
status: full
---

We work over GF(2), where $+$ is XOR. The characteristic polynomial is $P(x) = x^k + c_1 x^{k-1} + \cdots + c_{k-1} x + c_k$ with $k \ge 1$, and the recurrence is

$$s_{i+k} = c_1 s_{i+k-1} + c_2 s_{i+k-2} + \cdots + c_k s_i \qquad (i \ge 0). \tag{R}$$

A polynomial $P$ of degree $k$ is *primitive* if it is irreducible and $x$ has multiplicative order $2^k - 1$ modulo $P$. We use the ring $R = \mathrm{GF}(2)[x] / (P)$, whose elements are the $2^k$ polynomials of degree less than $k$.

**Lemma 1 (Fibonacci step).** If the state word holds $s_i, \ldots, s_{i+k-1}$ in bits $0, \ldots, k-1$, then FIB-LFSR-STEP returns $s_i$ and leaves $s_{i+1}, \ldots, s_{i+k}$ in bits $0, \ldots, k-1$.

*Proof.* The tap word $T$ has bit $k - j$ equal to $c_j$. Bit $k - j$ of the state holds $s_{i+k-j}$, so the parity of $s \mathbin{\&} T$ in line L1 is $\sum_j c_j s_{i+k-j} = s_{i+k}$ by (R). Line L2 reads bit 0, which is $s_i$. Line L3 moves bit $j+1$ to bit $j$ for $j = 0, \ldots, k-2$ and writes $s_{i+k}$ to bit $k - 1$. $\square$

By induction, the outputs of the Fibonacci form are $s_0, s_1, s_2, \ldots$, the solution of (R) with the seed as initial values.

**Lemma 2 (Galois step).** GAL-LFSR-STEP replaces the state $t \in R$ by $x t \bmod P$ and returns the coefficient of $x^{k-1}$ in $t$. The output sequence satisfies (R).

*Proof.* Let $t = \sum_{j<k} t_j x^j$. Line L6 forms $x t$, of degree at most $k$, whose coefficient of $x^k$ is $t_{k-1}$, the bit saved in line L5. If it is 0, then $x t$ already has degree less than $k$. If it is 1, then $x t - P$ has degree less than $k$ and is congruent to $x t$ modulo $P$; over GF(2) the subtraction is the XOR of line L8. So the new state is $x t \bmod P$.

Let $t^{(i)} = x^i t^{(0)} \bmod P$ and let $\lambda(r)$ be the coefficient of $x^{k-1}$ of $r \in R$, a GF(2)-linear map. The $i$-th output is $\lambda(t^{(i)})$. Since $P \equiv 0$, we have $x^{i+k} = \sum_j c_j x^{i+k-j}$ in $R$, so $t^{(i+k)} = \sum_j c_j t^{(i+k-j)}$, and applying $\lambda$ gives (R). $\square$

**Theorem.** Let $k \ge 1$. In the Galois form, the following are equivalent: (a) $P$ is primitive; (b) every nonzero state has period $2^k - 1$; (c) some nonzero state has period $2^k - 1$. The same holds for the Fibonacci form.

*Proof for the Galois form.* (a) implies (b): if $P$ is irreducible, $R$ is a field. For a nonzero $t$, $x^n t = t$ if and only if $(x^n - 1) t = 0$, if and only if $x^n = 1$, because $t$ is invertible. So the period of $t$ is the order of $x$, which is $2^k - 1$ by (a). (b) implies (c) at once.

(c) implies (a): let $t_0 \neq 0$ have period $N = 2^k - 1$. The states $x^j t_0$ for $0 \le j < N$ are pairwise distinct. None is 0, because 0 is a fixed point and the sequence returns to $t_0 \ne 0$. So they are all the $N$ nonzero elements of $R$. In particular $1 = x^j t_0$ for some $j$, so $t_0$ is a unit. Also $x \cdot (x^{N-1} t_0) = x^N t_0 = t_0$, so $x$ times the element $x^{N-1} t_0 t_0^{-1}$ is 1, and $x$ is a unit. Each nonzero element of $R$ is $x^j t_0$, a product of units, so $R$ is a field and $P$ is irreducible. Finally $x^n t_0 = t_0$ if and only if $x^n = 1$, so the order of $x$ is the period $N$. Thus $P$ is primitive.

*Proof for the Fibonacci form.* The Fibonacci state map is linear on $\mathrm{GF}(2)^k$: it sends $(s_0, \ldots, s_{k-1})$ to $(s_1, \ldots, s_{k-1}, \sum_j c_j s_{k-j})$. Its matrix $A$ has ones on the superdiagonal and the last row $(c_k, c_{k-1}, \ldots, c_1)$. The Galois map in the basis $1, x, \ldots, x^{k-1}$ has the matrix $C$ with ones on the subdiagonal and the last column $(c_k, c_{k-1}, \ldots, c_1)^{\mathsf T}$, because $x \cdot x^{k-1} = x^k = \sum_j c_j x^{k-j}$ in $R$. So $A = C^{\mathsf T}$. A square matrix over a field is similar to its transpose (they have the same invariant factors, see the [rational canonical form](/rational-canonical-form/)), so $A = Q C Q^{-1}$ for an invertible $Q$. Then $A^n v = v$ if and only if $C^n (Q^{-1} v) = Q^{-1} v$, so the period of $v$ under $A$ is the period of $Q^{-1} v$ under $C$, and $Q^{-1}$ is a bijection of the nonzero vectors. The three statements transfer. $\square$

**Corollary (the test of the implementation).** Let $N = 2^k - 1$. If $x^N \equiv 1 \pmod P$ and $x^{N/q} \not\equiv 1 \pmod P$ for each prime $q \mid N$, then $P$ is primitive; and a primitive $P$ passes this test.

*Proof.* The order of $x$ divides $N$ and divides no $N / q$, so it is $N$. Then the states $x^j \cdot 1$ for $0 \le j < N$ are distinct, so the state 1 has period $N$, and (c) gives (a). Conversely, if $P$ is primitive, the order of $x$ is $N$, so the test passes. $\square$

**Corollary (balance of an m-sequence).** If $P$ is primitive and the seed is nonzero, the $k$-bit windows $(s_i, \ldots, s_{i+k-1})$ for $0 \le i < 2^k - 1$ are the $2^k - 1$ nonzero $k$-tuples, each once, and one period of the output has $2^{k-1}$ ones and $2^{k-1} - 1$ zeros.

*Proof.* By Lemma 1 the windows are the Fibonacci states, and by the theorem they run through all nonzero states once per period. The output bit $s_i$ is the first entry of window $i$, and $2^{k-1}$ of the nonzero tuples begin with 1. $\blacksquare$
