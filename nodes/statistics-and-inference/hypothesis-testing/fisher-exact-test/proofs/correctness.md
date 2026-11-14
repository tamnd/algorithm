---
title: Given the margins the top-left cell is hypergeometric, the recurrence gives its exact weights, and each p-value is valid
proves: [correctness]
status: full
---

Write the table as $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ with row totals $r_1 = a + b$, $r_2 = c + d$, first column total $c_1 = a + c$ and $n = r_1 + r_2$. Let $k_{lo} = \max(0, c_1 - r_2)$ and $k_{hi} = \min(r_1, c_1)$ be the smallest and largest values of the top-left cell that the margins allow, and $w(k) = \binom{r_1}{k}\binom{r_2}{c_1 - k}$ for $k_{lo} \le k \le k_{hi}$.

**Claim 1 (the null law given the margins).** In each of these three sampling models, under the null hypothesis, the conditional law of the top-left cell $A$ given all four margins is

$$P(A = k \mid \text{margins}) = \frac{w(k)}{\binom{n}{c_1}}, \qquad k_{lo} \le k \le k_{hi},$$

and it does not depend on any unknown parameter.

- *Two independent binomial rows* (fixed $r_1$, $r_2$): $A \sim \text{Binomial}(r_1, p_1)$ and $C \sim \text{Binomial}(r_2, p_2)$, independent, with $H_0: p_1 = p_2 = p$.
- *One multinomial sample* (fixed $n$): the four cells are multinomial with probabilities $\pi_{ij}$, and $H_0$ is independence, $\pi_{ij} = \pi_{i\cdot}\pi_{\cdot j}$.
- *Both margins fixed by design*, as in the tea experiment, with the $c_1$ "first column" labels assigned to the $n$ units at random: every set of $c_1$ units is equally likely.

*Proof.* Binomial rows: for $k$ in range,

$$P(A = k, C = c_1 - k) = \binom{r_1}{k}\binom{r_2}{c_1 - k} p^{c_1}(1 - p)^{n - c_1} = w(k)\, p^{c_1}(1 - p)^{n - c_1}.$$

Summing over $k$ and using Vandermonde's identity $\sum_k \binom{r_1}{k}\binom{r_2}{c_1 - k} = \binom{n}{c_1}$ gives $P(A + C = c_1) = \binom{n}{c_1} p^{c_1}(1 - p)^{n - c_1}$. Dividing, the factor with $p$ cancels. Multinomial: given the row totals, the two rows are independent binomials with success probabilities $\pi_{11}/\pi_{1\cdot}$ and $\pi_{21}/\pi_{2\cdot}$, which under independence both equal $\pi_{\cdot 1}$; so the first case applies. Fixed margins: of the $\binom{n}{c_1}$ equally likely sets, exactly $w(k)$ put $k$ of the chosen units in row 1 and $c_1 - k$ in row 2. $\square$

**Claim 2 (lines L2 to L5 compute the weights exactly).** Line L2 sets $w(k_{lo})$ by its definition. For $k_{lo} \le k < k_{hi}$,

$$\frac{w(k + 1)}{w(k)} = \frac{\binom{r_1}{k + 1}}{\binom{r_1}{k}} \cdot \frac{\binom{r_2}{c_1 - k - 1}}{\binom{r_2}{c_1 - k}} = \frac{r_1 - k}{k + 1} \cdot \frac{c_1 - k}{r_2 - c_1 + k + 1}.$$

All four factors are positive in this range: $k < r_1$, $k < c_1$, and $r_2 - c_1 + k + 1 \ge 1$ because $k \ge c_1 - r_2$. So $w(k)(r_1 - k)(c_1 - k) = w(k + 1)(k + 1)(r_2 - c_1 + k + 1)$, an identity of integers. The left side is therefore a multiple of $(k + 1)(r_2 - c_1 + k + 1)$, and the integer division in line L4 is exact. By induction on $k$, line L4 produces $w(k)$ for every $k$ in range. Line L5 forms $N = \sum_k w(k) = \binom{n}{c_1}$ by Vandermonde's identity. No rounding happens anywhere. $\square$

**Claim 3 (lines L6 to L8 return the p-values).** With $i = a - k_{lo}$ the index of the observed table, the three sums are

$$P_{hi} = \frac{\sum_{k \ge a} w(k)}{N}, \qquad P_{lo} = \frac{\sum_{k \le a} w(k)}{N}, \qquad p_{ml} = \frac{\sum_{k : w(k) \le w(a)} w(k)}{N},$$

which are $P(A \ge a)$, $P(A \le a)$ and $P(w(A) \le w(a))$ under the law of Claim 1. Because $w(k)$ and $w(a)$ are exact integers, the comparison in line L8 decides ties correctly; no tolerance is needed. The float result is $\text{num}/N$ with Python's correctly rounded integer division. $\square$

**Claim 4 (conditional and unconditional validity).** For every $\alpha \in [0, 1]$ and each of the three p-values, $P(p(A) \le \alpha \mid \text{margins}) \le \alpha$ under $H_0$, and hence $P(p \le \alpha) \le \alpha$ without conditioning.

*Proof.* Given the margins, $A$ takes finitely many values with the law of Claim 1, and each p-value has the form $P(T(A) \ge T(a))$ with $T(k) = k$, $T(k) = -k$ or $T(k) = -w(k)$. The lemma on the [binomial test](/binomial-test/) correctness page (a tail p-value over a finite space is valid) gives the conditional bound. Taking the expectation over the margins gives $P(p \le \alpha) = \mathbb{E}[P(p \le \alpha \mid \text{margins})] \le \alpha$. $\square$

The unconditional size is usually well below $\alpha$, because the conditional size is below $\alpha$ for every set of margins. The page measures it for two rows of 10.

**Claim 5 (the one-sided test is the right conditional test).** In the binomial-rows model with $p_1$, $p_2$ arbitrary, let $\psi = \frac{p_1/(1 - p_1)}{p_2/(1 - p_2)}$ be the odds ratio. Then

$$P(A = k \mid \text{margins}) = \frac{w(k)\psi^k}{\sum_j w(j)\psi^j},$$

which depends only on $\psi$. For $\psi' > \psi$ the likelihood ratio $(\psi'/\psi)^k$ times a constant is increasing in $k$. So the conditional family has a monotone likelihood ratio in $A$, and by the [Karlin-Rubin theorem](/karlin-rubin-theorem/) the test that rejects for large $A$ is uniformly most powerful for $H_0: \psi \le 1$ against $\psi > 1$, among the tests whose conditional size is at most its own conditional size. (Exact size $\alpha$ needs randomization at the boundary value, as for the binomial test.)

*Proof.* $P(A = k, C = c_1 - k) = w(k)\, p_1^k(1 - p_1)^{r_1 - k} p_2^{c_1 - k}(1 - p_2)^{r_2 - c_1 + k}$. Taking out the factors that do not depend on $k$ leaves $w(k)\big(\frac{p_1}{1 - p_1}\big)^k\big(\frac{1 - p_2}{p_2}\big)^k = w(k)\psi^k$, and conditioning divides by the sum over $k$. $\square$

**Cost.** Line L2 computes two binomial coefficients with $O(n)$ arithmetic operations. Lines L3 and L4 do $m - 1$ steps, where $m = k_{hi} - k_{lo} + 1 \le n + 1$, each with a fixed number of operations. Lines L5 to L8 are sums over at most $m$ terms. So the code does $O(n)$ operations on integers and $\Theta(m)$ integers are stored. Each weight is at most $\binom{n}{c_1} < 2^n$, so it has at most $n$ bits, and an operation of an $n$-bit integer with a small one costs $O(n)$ bit operations; in bit operations the time is $O(n^2)$. $\square$
