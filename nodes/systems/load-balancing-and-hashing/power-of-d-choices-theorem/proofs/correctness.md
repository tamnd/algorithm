---
title: The layered induction proof of the bound ln ln n / ln d + O(1) on the maximum load with d choices
proves: [correctness]
status: full
---

**Statement.** Let $n \ge 16$ and $d \ge 2$ be integers. Throw $n$ balls into $n$ bins, one after another. For each ball draw $d$ bins independently and uniformly, with replacement, and put the ball into a drawn bin of least load, with ties broken by any rule. Define $\beta_6 = n/(2e)$ and $\beta_{i+1} = e\,\beta_i^d / n^{d-1}$, and let $i^\ast$ be the least $i \ge 6$ with $\beta_i^d/n^{d-1} < 2\ln n$. Then

$$ \Pr\bigl[\text{max load} \ge i^\ast + 3\bigr] \le \frac{i^\ast + 1}{n^2} + \binom n2 \Bigl(\frac{6\ln n}{n}\Bigr)^{2d}, $$

and $i^\ast \le 6 + \lceil \log_d \log_2 n \rceil$. So the maximum load is at most $\log_d \log_2 n + 9 = \ln\ln n/\ln d + O(1)$ with probability $1 - O((\ln n)^{2d}/n^{2d-2}) = 1 - o(1/n)$.

**Setup.** The *height* of a ball is the load of its bin just after the ball is placed. At time $t$ (after $t$ balls), let $\nu_i(t)$ be the number of bins with load at least $i$, and $\mu_i(t)$ the number of balls with height at least $i$. A bin with load at least $i$ holds a ball of height exactly $i$, and distinct bins hold distinct balls, so $\nu_i(t) \le \mu_i(t)$. Both are nondecreasing in $t$. Write $p_i = (\beta_i/n)^d$, so $\beta_{i+1} = e\,n\,p_i$. Let $E_i$ be the event $\nu_i(n) \le \beta_i$.

We use the [Chernoff bound](/chernoff-bound/) in the form $\Pr[X \ge (1+\delta)\mu] \le \bigl(e^\delta/(1+\delta)^{1+\delta}\bigr)^\mu$ for $X$ binomial with mean $\mu$ and $\delta > 0$.

## Lemma (sequential domination)

Let $Y_1, \ldots, Y_n \in \{0, 1\}$, where $Y_t$ depends on the choices of balls $1, \ldots, t$, and $\Pr[Y_t = 1 \mid \text{choices of balls } 1, \ldots, t-1] \le p$ for every history. Then for each $k$, $\Pr[\sum_t Y_t \ge k] \le \Pr[\mathrm{Bin}(n, p) \ge k]$.

*Proof.* We build the process from independent uniform variables $U_1, \ldots, U_n$ on $[0, 1)$ and extra randomness. At step $t$, given the history, let $q_t \le p$ be the conditional probability that $Y_t = 1$. Set $Y_t = 1$ if and only if $U_t < q_t$, then draw the choices of ball $t$ from their conditional law given the history and the value of $Y_t$. This gives the process its true joint law. Now $Y_t \le Z_t = [U_t < p]$ for each $t$, and $Z_1, \ldots, Z_n$ are independent Bernoulli($p$). So $\sum Y_t \le \sum Z_t \sim \mathrm{Bin}(n, p)$ on every outcome. $\square$

## The proof

1. *Base level.* At most $n/6$ bins can hold 6 or more of the $n$ balls, and $n/6 \le n/(2e)$. So $E_6$ holds always.

2. *One ball at level $i$.* Fix $i \ge 6$. Ball $t$ gets height at least $i + 1$ only if all $d$ drawn bins have load at least $i$ at time $t - 1$, because it joins a drawn bin of least load. Given the history, this happens with probability $(\nu_i(t-1)/n)^d$. Let $Y_t = 1$ if ball $t$ has height at least $i + 1$ and $\nu_i(t-1) \le \beta_i$. Then $\Pr[Y_t = 1 \mid \text{history}] \le p_i$.

3. *All balls at level $i$.* On $E_i$, we have $\nu_i(t-1) \le \nu_i(n) \le \beta_i$ for every $t$, so $Y_t = 1$ exactly when ball $t$ has height at least $i + 1$, and $\sum_t Y_t = \mu_{i+1}(n) \ge \nu_{i+1}(n)$. Therefore
$$ \Pr[\neg E_{i+1} \cap E_i] \le \Pr\Bigl[\sum_t Y_t > \beta_{i+1}\Bigr] \le \Pr[\mathrm{Bin}(n, p_i) \ge e\,n\,p_i] \le e^{-n p_i}, $$
by the lemma and the Chernoff bound with $1 + \delta = e$, where $e^{\delta}/(1+\delta)^{1+\delta} = e^{e-1}/e^{e} = e^{-1}$.

4. *Induction up to $i^\ast$.* For $6 \le i < i^\ast$, the definition of $i^\ast$ gives $n p_i \ge 2\ln n$, so $\Pr[\neg E_{i+1} \cap E_i] \le n^{-2}$. Since $\Pr[\neg E_{i+1}] \le \Pr[\neg E_{i+1} \cap E_i] + \Pr[\neg E_i]$ and $\Pr[\neg E_6] = 0$, induction on $i$ gives $\Pr[\neg E_{i}] \le (i - 6)/n^2$ for $6 \le i \le i^\ast$.

5. *The step past $i^\ast$.* At level $i^\ast$, $n p_{i^\ast} < 2\ln n$. Run step 3 with $i = i^\ast$: on $E_{i^\ast}$, $\mu_{i^\ast+1}(n)$ is at most a sum dominated by $\mathrm{Bin}(n, p_{i^\ast})$, which is in turn dominated by $\mathrm{Bin}(n, 2\ln n/n)$. The Chernoff bound with $\mu = 2\ln n$ and $1 + \delta = 3$ gives
$$ \Pr[\mathrm{Bin}(n, 2\ln n/n) \ge 6\ln n] \le \Bigl(\frac{e^2}{27}\Bigr)^{2\ln n} = n^{-2(\ln 27 - 2)} \le n^{-2}, $$
because $\ln 27 - 2 = 1.296 > 1$. Let $F$ be the event $\mu_{i^\ast+1}(n) < 6\ln n$. Then $\Pr[\neg F] \le n^{-2} + \Pr[\neg E_{i^\ast}] \le (i^\ast - 5)/n^2$.

6. *The last two levels.* Let $Z_t = 1$ if ball $t$ has height at least $i^\ast + 2$ and $\nu_{i^\ast+1}(t-1) < 6\ln n$. As in step 2, $\Pr[Z_t = 1 \mid \text{history}] \le (6\ln n/n)^d$. By the lemma, $\Pr[\sum_t Z_t \ge 2] \le \Pr[\mathrm{Bin}(n, q) \ge 2] \le \binom n2 q^2$ with $q = (6\ln n/n)^d$, by a union bound over pairs of trials. On $F$, $\nu_{i^\ast+1}(t-1) \le \mu_{i^\ast+1}(n) < 6\ln n$ for every $t$, so $\sum_t Z_t$ is the number of balls of height at least $i^\ast + 2$.

7. *Conclusion of the bound.* A bin with load at least $i^\ast + 3$ holds a ball of height $i^\ast + 2$ and a ball of height $i^\ast + 3$, two balls of height at least $i^\ast + 2$. So the event "max load $\ge i^\ast + 3$" lies in $\neg F \cup \{\sum_t Z_t \ge 2\}$, and its probability is at most $(i^\ast - 5)/n^2 + \binom n2 (6\ln n/n)^{2d}$, which is below the bound of the statement.

8. *The size of $i^\ast$.* Let $\gamma_i = \beta_i/n$ and $\delta_i = e^{1/(d-1)}\gamma_i$. Then $\gamma_{i+1} = e\,\gamma_i^d$, and
$$ \delta_{i+1} = e^{\frac{1}{d-1}} e\,\gamma_i^d = e^{\frac{1}{d-1} + 1 - \frac{d}{d-1}}\,\delta_i^d = \delta_i^d. $$
So $\delta_{6+j} = \delta_6^{d^j}$ with $\delta_6 = e^{1/(d-1)}/(2e) \le 1/2$ for $d \ge 2$. Hence $\beta_{6+j} = n e^{-1/(d-1)}\delta_6^{d^j} \le n\,2^{-d^j}$. For $j = \lceil \log_d \log_2 n\rceil$ this gives $\beta_{6+j} \le 1$ and $\beta_{6+j}^d/n^{d-1} \le n^{1-d} < 2\ln n$, so $i^\ast \le 6 + j$.

9. *The final form.* The maximum load is at most $i^\ast + 2 \le 8 + \lceil \log_d \log_2 n \rceil \le 9 + \log_d \log_2 n$. Since $\log_d \log_2 n = (\ln\ln n - \ln\ln 2)/\ln d = \ln\ln n/\ln d + 0.367/\ln d$, this is $\ln\ln n/\ln d + O(1)$. For $d \ge 2$ the failure probability is $O(1/n^2) + O((\ln n)^{2d}/n^{2d-2}) = O((\ln n)^4/n^2) = o(1/n)$. $\blacksquare$

## The lower bound

Azar, Broder, Karlin and Upfal also prove that the maximum load is at least $\ln\ln n/\ln d - O(1)$ with probability $1 - o(1/n)$. The proof is a layered induction in the other direction: it shows that for each level $i$ up to $\ln\ln n/\ln d - O(1)$, many balls among the last part of the sequence find all $d$ choices at load at least $i$, so at least $\gamma_{i+1} \approx \gamma_i^d / n^{d-1}$ bins reach load $i + 1$, with a lower Chernoff bound at each level. This part is a sketch here; the full proof is in Section 17.2 of Mitzenmacher and Upfal (second edition) and in the paper.
