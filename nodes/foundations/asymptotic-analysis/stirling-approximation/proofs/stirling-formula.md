---
title: The sharp form of Stirling's formula, with the constant and the error bounds
proves: [stirling-formula]
status: full
---

**Statement.** There is a real sequence $(r_n)_{n \ge 1}$ with $\frac{1}{12n+1} < r_n < \frac{1}{12n}$ for each $n \ge 1$, such that
$$ n! = \sqrt{2\pi n}\,\left(\frac{n}{e}\right)^n e^{r_n}. $$
In particular $n! \sim \sqrt{2\pi n}\,(n/e)^n$. The two-sided bound on $r_n$ is due to Robbins (1955). The proof below follows his method for the bounds and uses the Wallis integrals for the constant.

**Step 1: a convergent sequence.** For $n \ge 1$ let
$$ a_n = \ln n! - \left(n + \tfrac12\right)\ln n + n, \qquad\text{so that}\qquad n! = e^{a_n}\sqrt{n}\,(n/e)^n. $$
Then
$$ a_n - a_{n+1} = \left(n + \tfrac12\right)\ln\frac{n+1}{n} - 1. $$
To see this, expand $a_{n+1}$ and use $\ln (n+1)! = \ln n! + \ln(n+1)$: the terms $\ln n!$ cancel, and what remains is $-\ln(n+1) + (n + \frac32)\ln(n+1) - (n+\frac12)\ln n + n - (n+1)$, which is the right side.

**Step 2: a series for the difference.** Put $t = \frac{1}{2n+1}$, so $0 < t < 1$. Then $\frac{1+t}{1-t} = \frac{2n+2}{2n} = \frac{n+1}{n}$ and $n + \frac12 = \frac{1}{2t}$. For $0 \le t < 1$ we have $\ln\frac{1+t}{1-t} = 2\sum_{j \ge 0} \frac{t^{2j+1}}{2j+1}$. So
$$ a_n - a_{n+1} = \frac{1}{2t}\cdot 2\sum_{j \ge 0}\frac{t^{2j+1}}{2j+1} - 1 = \sum_{j \ge 1}\frac{t^{2j}}{2j+1}. $$

**Step 3: two-sided bound on the difference.** Every term of the series is positive, so $a_n - a_{n+1} > 0$. Also $\frac{1}{2j+1} \le \frac13$ for $j \ge 1$, with strict inequality for $j \ge 2$, so
$$ a_n - a_{n+1} < \frac13\sum_{j \ge 1} t^{2j} = \frac{t^2}{3(1-t^2)}. $$
Since $t^{-2} - 1 = (2n+1)^2 - 1 = 4n(n+1)$, we get $\frac{t^2}{1-t^2} = \frac{1}{4n(n+1)}$. Hence
$$ 0 < a_n - a_{n+1} < \frac{1}{12n(n+1)} = \frac{1}{12n} - \frac{1}{12(n+1)}. $$

**Step 4: the limit and the bounds on $r_n$.** Step 3 says two things. First, $(a_n)$ is strictly decreasing. Second, $a_n - \frac{1}{12n} < a_{n+1} - \frac{1}{12(n+1)}$, so $b_n = a_n - \frac{1}{12n}$ is strictly increasing. Also $b_n < a_n \le a_1$ for each $n$, so $(b_n)$ is increasing and bounded above. It converges to a limit $L$. Since $a_n = b_n + \frac{1}{12n}$ and $\frac1{12n} \to 0$, the sequence $(a_n)$ also converges to $L$. A strictly increasing sequence is smaller than its limit, and a strictly decreasing sequence is larger than its limit. So for each $n \ge 1$,
$$ L < a_n \quad\text{and}\quad a_n - \frac{1}{12n} < L. $$
Let $r_n = a_n - L$. Then $0 < r_n < \frac{1}{12n}$, and $n! = e^{L} e^{r_n}\sqrt n\,(n/e)^n$. Put $K = e^L$. It remains to sharpen the lower bound and to show $K = \sqrt{2\pi}$.

**Step 5: the lower bound of Robbins.** For $j \ge 1$ we have $2j + 1 \le 3^j$, with equality only at $j = 1$ (induction: $2(j+1) + 1 = 2j + 3 \le 3^j + 2 < 3^{j+1}$). So the series of Step 2 satisfies
$$ a_n - a_{n+1} = \sum_{j \ge 1}\frac{t^{2j}}{2j+1} > \sum_{j \ge 1}\left(\frac{t^2}{3}\right)^{j} = \frac{t^2/3}{1 - t^2/3} = \frac{1}{3t^{-2} - 1} = \frac{1}{12n^2 + 12n + 2}, $$
where the inequality is strict because the terms with $j \ge 2$ are strictly smaller, and the last step uses $t^{-2} = (2n+1)^2 = 4n^2 + 4n + 1$. On the other side,
$$ \frac{1}{12n+1} - \frac{1}{12(n+1)+1} = \frac{12}{(12n+1)(12n+13)} = \frac{1}{12n^2 + 14n + \frac{13}{12}}. $$
For $n \ge 1$ we have $12n^2 + 12n + 2 < 12n^2 + 14n + \frac{13}{12}$, because this is $\frac{11}{12} < 2n$. So
$$ a_n - a_{n+1} > \frac{1}{12n+1} - \frac{1}{12(n+1)+1}, $$
that is, $c_n = a_n - \frac{1}{12n+1}$ is strictly decreasing. It converges to $L$, because $\frac{1}{12n+1} \to 0$. A strictly decreasing sequence is larger than its limit, so $c_n > L$, which is $r_n = a_n - L > \frac{1}{12n+1}$.

**Step 6: Wallis integrals.** For integers $m \ge 0$ let $I_m = \int_0^{\pi/2}\sin^m x\,dx$. Then $I_0 = \pi/2$ and $I_1 = 1$. For $m \ge 2$ write $\sin^m x = \sin^{m-1}x\cdot\sin x$ and integrate by parts: $I_m = (m-1)\int_0^{\pi/2}\sin^{m-2}x\cos^2x\,dx = (m-1)(I_{m-2} - I_m)$, because the boundary term $-\sin^{m-1}x\cos x$ is 0 at both ends. So $I_m = \frac{m-1}{m}I_{m-2}$. Since $0 \le \sin x \le 1$ on $[0, \pi/2]$, the sequence $(I_m)$ is non-increasing. By induction on $m$, $I_m I_{m+1} = \frac{\pi}{2(m+1)}$: for $m = 0$ the product is $\pi/2$, and if it holds for $m$, then $I_{m+1}I_{m+2} = \frac{m+1}{m+2}I_{m+1}I_m = \frac{\pi}{2(m+2)}$.

For $n \ge 1$ the monotonicity gives $I_{2n+1} \le I_{2n} \le I_{2n-1}$. Multiply by $I_{2n} > 0$:
$$ \frac{\pi}{2(2n+1)} \le I_{2n}^2 \le \frac{\pi}{4n}. $$
Multiply by $4n/\pi$: the left side becomes $\frac{2n}{2n+1}$ and the right side becomes 1. Both tend to 1, so $I_{2n}^2 \sim \frac{\pi}{4n}$, that is $I_{2n} \sim \frac12\sqrt{\pi/n}$.

**Step 7: the central binomial coefficient.** The recurrence gives $I_{2n} = \frac\pi2\prod_{j=1}^{n}\frac{2j-1}{2j}$. Now $\prod_{j=1}^n (2j-1) = \frac{(2n)!}{2^n n!}$ and $\prod_{j=1}^n 2j = 2^n n!$, so $I_{2n} = \frac{\pi}{2}\cdot\frac{(2n)!}{4^n (n!)^2} = \frac\pi2\binom{2n}{n}4^{-n}$. With Step 6,
$$ \binom{2n}{n}4^{-n} = \frac{2}{\pi}I_{2n} \sim \frac{2}{\pi}\cdot\frac{\sqrt\pi}{2\sqrt n} = \frac{1}{\sqrt{\pi n}}. $$

**Step 8: the constant.** By Step 4, $n! \sim K\sqrt n\,(n/e)^n$. So $(2n)! \sim K\sqrt{2n}\,(2n/e)^{2n}$ and $(n!)^2 \sim K^2 n\,(n/e)^{2n}$. Dividing,
$$ \binom{2n}{n} \sim \frac{K\sqrt{2n}\,(2n)^{2n}}{K^2 n\, n^{2n}} = \frac{\sqrt2\,4^n}{K\sqrt n}. $$
Compare with Step 7: $\frac{\sqrt 2}{K\sqrt n} \sim \frac{1}{\sqrt{\pi n}}$, so $K = \sqrt{2\pi}$. Then $n! = \sqrt{2\pi n}\,(n/e)^n e^{r_n}$ with $\frac{1}{12n+1} < r_n < \frac1{12n}$ by Steps 4 and 5, and $e^{r_n} \to 1$. $\blacksquare$

**Remark.** The values of $r_n$ are $0.0811$ at $n = 1$ (between $1/13 = 0.0769$ and $1/12 = 0.0833$), $0.04134$ at $n = 2$ and $0.0083306$ at $n = 10$ (between $0.0082645$ and $0.0083333$). The bounds hold strictly for every $n$ from 1 to 199 in a check with the log-gamma function. The two bounds differ by $\frac{1}{12n(12n+1)}$, so they pin $r_n$ to a relative error of about $1/(12n)$, and $r_n \sim \frac{1}{12n}$.
