---
title: The Arora-Ge linearization never returns a wrong secret
proves: [correctness]
status: full
---

We use the notation of the page. The input is $N'$ samples $(a_k, b_k)$ with $b_k = \langle a_k, s \rangle + e_k \bmod q$, a set $E \subset \mathbb{Z}_q$ of $D$ distinct values, and a prime $q$. $M$ is the list of exponent vectors $\alpha \in \mathbb{N}^n$ with $1 \le |\alpha| \le D$, and $N = |M|$. For $\alpha \in M$ write $s^\alpha = \prod_i s_i^{\alpha_i} \bmod q$, and let $y^\star = (s^\alpha)_{\alpha \in M}$.

**Lemma 1 (the expansion).** Fix $a \in \mathbb{Z}_q^n$ and $b \in \mathbb{Z}_q$, and let $P(t) = \sum_{j=0}^{D} p_j t^j$. Lines L4 and L5 compute $c_0$ and $c_\alpha$ such that, as polynomials in the variables $s_1, \ldots, s_n$ over $\mathbb{Z}_q$,

$$P\Bigl(b - \sum_i a_i s_i\Bigr) = c_0 + \sum_{\alpha \in M} c_\alpha s^\alpha.$$

*Proof.* Write $L = \sum_i a_i s_i$. By the binomial theorem, $(b - L)^j = \sum_{t=0}^{j} \binom{j}{t} b^{j-t} (-1)^t L^t$, so $P(b - L) = \sum_{t=0}^{D} c_t L^t$ with $c_t = (-1)^t \sum_{j \ge t} p_j \binom{j}{t} b^{j-t}$. By the multinomial theorem, $L^t = \sum_{|\alpha| = t} \binom{t}{\alpha} \prod_i a_i^{\alpha_i} s^\alpha$, where $\binom{t}{\alpha} = t!/\prod_i \alpha_i!$. Collecting terms gives $c_\alpha = c_{|\alpha|} \binom{|\alpha|}{\alpha} \prod_i a_i^{\alpha_i}$ for $\alpha \in M$, and the constant term is $c_0$. This is what `equation_row` computes. $\square$

**Lemma 2 (the true values solve the system).** If every error $e_k$ lies in $E$, then $y^\star$ satisfies every equation $\sum_{\alpha} c_{k,\alpha} y_\alpha = -c_{k,0}$ built in lines L3 to L5.

*Proof.* For sample $k$, substitute the true secret $s$ into the identity of Lemma 1. The left side becomes $P(b_k - \langle a_k, s \rangle) = P(e_k)$, which is 0 because $e_k \in E$ is a root of $P$ (line L1). The right side becomes $c_{k,0} + \sum_\alpha c_{k,\alpha} s^\alpha$. So $\sum_\alpha c_{k,\alpha} y^\star_\alpha = -c_{k,0}$. $\square$

**Lemma 3 (Gaussian elimination).** Over the field $\mathbb{Z}_q$, Gauss-Jordan elimination (line L6) either finds that the system has no solution, or finds its rank $r$. If $r = N$ and the system is consistent, it returns the unique solution.

*Proof.* This is the standard property of Gaussian elimination over a field: each row operation is invertible, so it keeps the solution set; at the end the system is in reduced row echelon form, from which consistency, rank and, when the rank is $N$, the unique solution can be read off. $\square$

**Theorem.** Assume every error lies in $E$. Then the algorithm returns either FAIL or the secret $s$. It returns $s$ if and only if the $N' \times N$ matrix $(c_{k,\alpha})$ has rank $N$.

*Proof.* By Lemma 2, the system has the solution $y^\star$, so it is consistent. If the rank is below $N$, the solution is not unique and line L7 returns FAIL. If the rank is $N$, Lemma 3 shows that line L6 returns the unique solution, which must be $y^\star$. For the unit vector $\alpha = e_i$, $y^\star_{e_i} = s_i$, so line L8 returns $s$. $\square$

**Errors outside $E$.** If some error lies outside $E$, Lemma 2 fails for that sample. The system may then be inconsistent, and the code returns FAIL. It may also have a unique solution that is not of the form $y^\star$; then line L8 returns a wrong vector. So the guarantee needs the promise that all errors lie in $E$. For Gaussian errors, $E$ must be an interval wide enough that all $N'$ errors fall in it with high probability.

**When the rank is full.** The theorem does not say how many samples make the rank equal to $N$. For uniform $a_k$ and $q$ larger than $D$, 10 samples more than $N$ gave full rank in almost all of our trials. Arora and Ge analyse this question; the number of samples they need is of order $n^D$, the same order as $N$ for a fixed $D$.

$\blacksquare$
