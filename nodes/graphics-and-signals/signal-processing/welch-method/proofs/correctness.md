---
title: Welch's method returns the average of the segment periodograms, keeps the window-smoothed mean, and divides the white-noise variance by the effective number of segments
proves: [correctness]
status: full
---

The notation is that of the page: a record $x[0], \dots, x[N-1]$, segments of length $M$ with hop $D$, $K = \lfloor (N - M)/D \rfloor + 1$, a window $w$ with $U = \frac{1}{M}\sum_t w[t]^2 > 0$, a grid size $L \ge M$ and $\omega_b = 2\pi b / L$. Segment $i$ is $x_i[t] = x[iD + t]$, $0 \le t < M$, and $A_i(\omega) = \sum_{t<M} w[t]\,x_i[t]\,e^{-i\omega t}$.

**Claim 1 (the output).** The algorithm returns $\hat S[b] = \frac{1}{K}\sum_{i=0}^{K-1} \frac{|A_i(\omega_b)|^2}{MU}$ for every bin $b$.

*Proof.* The last segment starts at $(K-1)D \le N - M$, so all indices in line L5 are in range, and $K$ is the largest count with this property. Line L3 sets the sums to $0$. In the iteration $i$ of the loop of line L4, line L5 forms the windowed segment padded to length $L$ and line L6 transforms it, so that bin $b$ holds $A_i(\omega_b)$, because the padded samples are zero. Line L7 adds $|A_i(\omega_b)|^2/(MU)$ to the sum of bin $b$. After the loop each sum holds the $K$ terms, and line L8 divides by $K$. $\square$

**Claim 2 (the mean).** If $x$ is zero-mean WSS with autocorrelation $r$, then for every $\omega$

$$\mathbb{E}\,\hat S(\omega) = \sum_{|k|<M} v[k]\, r[k]\, e^{-i\omega k}, \qquad v[k] = \frac{1}{MU}\sum_{t} w[t+k]\,w[t].$$

So the mean is the true spectrum smoothed by the kernel $|W(\omega)|^2/(MU)$, whose inverse transform is $v$, and $v[0] = 1$. On white noise of variance $\sigma^2$ the mean is $\sigma^2$ exactly.

*Proof.* Each segment $x_i$ is a stretch of a WSS process, so $\mathbb{E}\,x_i[t+k]\overline{x_i[t]} = r[k]$ for every $i$. Expanding $|A_i|^2$ and grouping by the lag $k$ gives $\mathbb{E}\,|A_i(\omega)|^2/(MU) = \sum_k v[k]\,r[k]\,e^{-i\omega k}$, the same for each $i$; the mean of the average is this common value. For white noise only $k = 0$ remains, and $v[0]\,r[0] = \sigma^2$. $\square$

**Claim 3 (Bartlett's variance).** Let $x$ be real white Gaussian noise of variance $\sigma^2$, let $D = M$, $w = 1$ and $L = M$. For $0 < b < M/2$, $K\hat S[b]/\sigma^2$ has the gamma law with shape $K$ and scale $1$, so $\mathbb{E}\,\hat S[b] = \sigma^2$ and $\operatorname{Var}\hat S[b] = \sigma^4/K$.

*Proof.* With $D = M$ the segments use disjoint samples, so they are independent. By claim 3 of the [periodogram](/periodogram/) proof, each $|A_i(\omega_b)|^2/(M\sigma^2)$ is exponential with mean 1. A sum of $K$ independent exponentials with mean 1 has the gamma law with shape $K$, mean $K$ and variance $K$. Divide by $K$. $\square$

**Claim 4 (overlapping segments).** Let $x$ be circular complex white Gaussian noise of variance $\sigma^2$ (real and imaginary parts independent, each of variance $\sigma^2/2$). Then for every $\omega$

$$\operatorname{Var}\hat S(\omega) = \frac{\sigma^4}{K}\left(1 + 2\sum_{j=1}^{K-1}\left(1 - \frac{j}{K}\right)\rho_j\right), \qquad \rho_j = \frac{\left(\sum_t w[t]\,w[t + jD]\right)^2}{\left(\sum_t w[t]^2\right)^2},$$

where the inner sum runs over $0 \le t < M - jD$ and is $0$ when $jD \ge M$.

*Proof.* Each $A_i$ is a linear form in the circular Gaussian vector $x$, so $(A_i, A_l)$ is circular Gaussian, and for such variables $\operatorname{Cov}(|A_i|^2, |A_l|^2) = |\mathbb{E}\,A_i\overline{A_l}|^2$ (Isserlis' theorem; the term $|\mathbb{E}\,A_iA_l|^2$ vanishes by circularity). With $l = i + j$, a sample $x[n]$ appears in $A_i$ with the factor $w[n - iD]e^{-i\omega(n - iD)}$ and in $A_l$ with $w[n - lD]e^{-i\omega(n - lD)}$, so $\mathbb{E}\,A_i\overline{A_l} = \sigma^2 e^{-i\omega jD}\sum_t w[t + jD]\,w[t]$, whose squared modulus is $\sigma^4\left(\sum_t w[t]w[t+jD]\right)^2$. Dividing by $(MU)^2 = (\sum_t w[t]^2)^2$ gives $\operatorname{Cov}(P_i, P_{i+j}) = \sigma^4\rho_j$, and $\rho_0 = 1$. The variance of the average of $K$ terms whose covariance depends only on $j = |l - i|$ is $\frac{1}{K^2}\sum_{i,l}\sigma^4\rho_{|l-i|} = \frac{\sigma^4}{K^2}\left(K + 2\sum_{j \ge 1}(K - j)\rho_j\right)$, which is the formula. $\blacksquare$

For real noise, $\mathbb{E}\,A_iA_l$ is not zero, and the covariance gains the term $\sigma^4\left|\sum_t w[t]\,w[t+jD]\,e^{-2i\omega t}\right|^2/(MU)^2$. This term is the transform of a smooth product at the frequency $2\omega$, so it is small when $\omega$ is several bins away from $0$ and $\pi$, and the formula is then a close approximation. The page reports a measured check of the formula on real noise.
