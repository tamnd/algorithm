---
title: SC decoding computes the synthetic channel LLRs and re-encodes its decisions
proves: [correctness]
status: full
---

**Setting.** $N = 2^n$ and $F^{\otimes n}$ is the $n$-th Kronecker power of $F = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ over $\mathrm{GF}(2)$. Code bit $x_j$ goes through its own memoryless channel $W_j$, independent of the others, and $\lambda_j = \ln W_j(y_j \mid 0) / W_j(y_j \mid 1)$. The channels may differ from position to position; this makes the induction work, because the inner calls see the channels $W^-$ and $W^+$. For a bit $x$ and an LLR $\lambda$ let

$$\omega(\lambda, x) = e^{(1 - 2x)\lambda / 2}.$$

Then $W_j(y_j \mid x) = c_j\, \omega(\lambda_j, x)$ with $c_j = \sqrt{W_j(y_j \mid 0)\, W_j(y_j \mid 1)}$, which does not depend on $x$. (If one of the two values is 0, $\lambda_j = \pm\infty$ and the same holds with the usual limits; the argument below only uses ratios.)

Let $\hat u_0, \ldots, \hat u_{N-1}$ be the decisions of SC-DECODE$(\lambda, \mathcal{F})$ in the order in which the leaves are reached, and for $c \in \{0, 1\}$ let

$$S_i(\lambda; c) = \sum_{u_{i+1}, \ldots, u_{N-1}} \ \prod_{j=0}^{N-1} \omega\bigl(\lambda_j,\ ((\hat u_0, \ldots, \hat u_{i-1}, c, u_{i+1}, \ldots, u_{N-1}) F^{\otimes n})_j\bigr).$$

Since $W_j(y_j \mid x) = c_j\, \omega(\lambda_j, x)$, $S_i(\lambda; c)$ equals $W_N^{(i)}(y, \hat u_0^{i-1} \mid c)$ times a factor $2^{N-1} / \prod_j c_j$ that does not depend on $c$. So $\ln S_i(\lambda; 0) / S_i(\lambda; 1)$ is the LLR of the synthetic channel $W_N^{(i)}$ at the output $(y, \hat u_0^{i-1})$.

**Theorem.** With the exact $f$, SC-DECODE$(\lambda, \mathcal{F})$ returns $(\hat u, \hat x)$ such that:

1. the LLR that reaches leaf $i$ is $\ell_i = \ln S_i(\lambda; 0) / S_i(\lambda; 1)$, and $\hat u_i = 0$ if $i \in \mathcal{F}$, else $\hat u_i = 0$ if $\ell_i \ge 0$ and $1$ if $\ell_i < 0$;
2. $\hat x = \hat u F^{\otimes n}$.

Part 2 holds for each function $f$, the min-sum one included.

**Lemma 1 (the rule f).** For LLRs $a, b$ and $v \in \{0, 1\}$,

$$\sum_{w \in \{0, 1\}} \omega(a, v \oplus w)\, \omega(b, w) = K\, \omega\bigl(f(a, b), v\bigr)$$

for a constant $K > 0$ that does not depend on $v$.

*Proof.* For $v = 0$ the sum is $e^{(a+b)/2} + e^{-(a+b)/2} = 2\cosh\frac{a+b}{2}$. For $v = 1$ it is $e^{(b-a)/2} + e^{(a-b)/2} = 2\cosh\frac{a-b}{2}$. With $s = \tanh(a/2)$ and $t = \tanh(b/2)$, the identity $\cosh(p \pm q) = \cosh p \cosh q\,(1 \pm \tanh p \tanh q)$ gives the ratio

$$\frac{\cosh\frac{a+b}{2}}{\cosh\frac{a-b}{2}} = \frac{1 + st}{1 - st} = e^{2 \operatorname{artanh}(st)} = e^{f(a, b)}.$$

A positive function $p$ on $\{0, 1\}$ with $p(0)/p(1) = e^{\mu}$ is $\sqrt{p(0)p(1)}\ \omega(\mu, \cdot)$. Take $p$ as the sum and $\mu = f(a, b)$. $\square$

**Lemma 2 (the rule g).** For LLRs $a, b$ and bits $v, w$,

$$\omega(a, v \oplus w)\, \omega(b, w) = \omega\bigl(g(a, b, v), w\bigr), \qquad g(a, b, v) = b + (1 - 2v)a.$$

*Proof.* $1 - 2(v \oplus w) = (1 - 2v)(1 - 2w)$ for bits. So the left side is $e^{(1 - 2w)\,((1 - 2v)a + b)/2}$. $\square$

**Lemma 3.** Let $G = F^{\otimes (n-1)}$ and $h = N/2$. Then $F^{\otimes n} = \begin{pmatrix} G & 0 \\ G & G \end{pmatrix}$, and $b \mapsto bG$ is a bijection of $\mathrm{GF}(2)^h$.

*Proof.* $F^{\otimes n} = F \otimes F^{\otimes (n-1)}$ by the definition of the Kronecker power, which is the block form. $F^2 = I$ over $\mathrm{GF}(2)$, so $G^2 = (F^2)^{\otimes (n-1)} = I$ and $G$ is invertible. $\square$

So for $u = (a, b)$ with halves of length $h$, and $v = aG$, $w = bG$,

$$u F^{\otimes n} = (v \oplus w,\ w). \tag{1}$$

**Proof of the theorem.** Induction on $n$.

*Base, $N = 1$.* Lines L1 to L4 run. The only leaf gets $\ell_0 = \lambda_0$, and $S_0(\lambda; c) = \omega(\lambda_0, c)$, so $\ln S_0(\lambda; 0)/S_0(\lambda; 1) = \lambda_0$. Line L3 sets $b$ by the rule of part 1, and line L4 returns $\hat u = \hat x = (b)$. Since $F^{\otimes 0} = (1)$, part 2 holds.

*Step, $N = 2h \ge 2$.* Assume the theorem for length $h$ and each list of LLRs. Line L5 sets $h$. The leaves of the call at line L7 are reached first, and they are the leaves $0, \ldots, h - 1$ with the flags $\mathcal{F}[0 \ldots h-1]$. The leaves of the call at line L9 are the leaves $h, \ldots, N - 1$. Write $\hat u = (\hat a, \hat b)$ for the two halves of the decisions.

*Leaves in the first half.* Fix $i < h$ and $c$. In $S_i(\lambda; c)$ the sum runs over $a_{i+1}, \ldots, a_{h-1}$ and over all of $b$. By (1), the product splits into the pairs of positions $j$ and $j + h$:

$$S_i(\lambda; c) = \sum_{a_{i+1}^{h-1}} \sum_{b} \prod_{j=0}^{h-1} \omega(\lambda_j, v_j \oplus w_j)\, \omega(\lambda_{j+h}, w_j), \qquad v = (\hat a_0^{i-1}, c, a_{i+1}^{h-1})\, G,\ w = bG.$$

By Lemma 3, as $b$ runs over $\mathrm{GF}(2)^h$, $w$ runs over $\mathrm{GF}(2)^h$ once each. So the sum over $b$ is a sum over $w$, and it factors over $j$. By Lemma 1 each factor is $K_j\, \omega(\alpha_j, v_j)$ with $\alpha_j = f(\lambda_j, \lambda_{j+h})$, which is line L6. So

$$S_i(\lambda; c) = \Bigl(\prod_j K_j\Bigr) \sum_{a_{i+1}^{h-1}} \prod_{j=0}^{h-1} \omega\bigl(\alpha_j, ((\hat a_0^{i-1}, c, a_{i+1}^{h-1}) G)_j\bigr) = \Bigl(\prod_j K_j\Bigr) S'_i(\alpha; c),$$

where $S'_i$ is the sum for length $h$. The constant cancels in the ratio. By the induction hypothesis for the call at line L7, its leaf $i$ gets $\ln S'_i(\alpha; 0)/S'_i(\alpha; 1) = \ln S_i(\lambda; 0)/S_i(\lambda; 1)$ and decides by the rule of part 1. Also $x_a = \hat a G$.

*Leaves in the second half.* Fix $i < h$ and $c$, and look at leaf $h + i$. The earlier decisions are all of $\hat a$ and $\hat b_0, \ldots, \hat b_{i-1}$. By (1) with $\hat v = \hat a G = x_a$,

$$S_{h+i}(\lambda; c) = \sum_{b_{i+1}^{h-1}} \prod_{j=0}^{h-1} \omega(\lambda_j, x_a[j] \oplus w_j)\, \omega(\lambda_{j+h}, w_j), \qquad w = (\hat b_0^{i-1}, c, b_{i+1}^{h-1})\, G.$$

By Lemma 2 each factor is $\omega(\beta_j, w_j)$ with $\beta_j = g(\lambda_j, \lambda_{j+h}, x_a[j])$, which is line L8. So $S_{h+i}(\lambda; c) = S'_i(\beta; c)$, the sum for length $h$ with the LLRs $\beta$. By the induction hypothesis for the call at line L9, its leaf $i$ gets the right LLR and decides by the rule of part 1, and $x_b = \hat b G$.

*Re-encoding.* By (1), $\hat u F^{\otimes n} = (\hat a G \oplus \hat b G,\ \hat b G) = (x_a \oplus x_b,\ x_b)$, which line L10 returns together with $\hat u = \hat a \,\|\, \hat b$. This step uses only the induction hypothesis of part 2, so part 2 holds for each $f$.

Each call halves the length, so the recursion stops after $n$ levels. This completes the induction. $\square$

**Consequences.** Part 1 says that leaf $i \in \mathcal{A}$ takes the maximum likelihood decision for $u_i$ on the synthetic channel $W_N^{(i)}$, with the earlier decisions in place of the true earlier bits (ties go to 0). If $\hat u_0^{i-1} = u_0^{i-1}$, this is the decision of the genie-aided decoder that knows the true earlier bits. So if SC makes an error, its first wrong decision is at some $i \in \mathcal{A}$ where the genie-aided decision is also wrong. By the union bound, the block error probability is at most $\sum_{i \in \mathcal{A}} P_e(W_N^{(i)})$, and $P_e(W_N^{(i)}) \le Z(W_N^{(i)})$ for the maximum likelihood decision on a binary-input channel. This is Arıkan's bound. $\blacksquare$
