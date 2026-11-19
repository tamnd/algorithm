---
title: Correctness of the CELP codebook search
proves: [correctness]
status: full
---

CELP is a lossy coder, so we prove the claims each step makes: the weighted error is affine in the excitation, the score picks the vector and gain of least weighted error, the sequential search is bounded by the joint search, the decoder reproduces the encoder's output, and an excitation that is in the codebook is found exactly.

## Setup

In one subframe of $L$ samples, let $s$ be the input, $e$ the excitation, $\hat s$ the output of the synthesis filter $1/A(z)$ from its current state, and $e_w$ the output of the weighting filter $W(z) = A(z/\gamma_1)/A(z/\gamma_2)$ applied to $s - \hat s$ from its current state. All three filters are linear, causal and time-invariant within the subframe.

## Lemma 1 (the weighted error is affine)

Let $t$ be $e_w$ when $e = 0$, and let $h$ be the first $L$ samples of the zero-state impulse response of $W(z)/A(z)$, with $H$ the $L \times L$ lower triangular matrix $H_{n,j} = h[n - j]$ for $j \le n$. Then for every $e$,

$$e_w(e) = t - H e .$$

*Proof.* A linear filter that starts from a state $\sigma$ and gets an input $u$ produces the sum of its zero-input response to $\sigma$ and its zero-state response to $u$. Apply this to the synthesis filter: $\hat s(e) = \hat s(0) + G e$, where $G$ is the zero-state response matrix of $1/A(z)$. So $s - \hat s(e) = (s - \hat s(0)) - G e$. Apply it again to the weighting filter, whose state is the same in both cases: $e_w(e) = e_w(0) - K G e$, where $K$ is the zero-state matrix of $W(z)$. The product $KG$ of two lower triangular Toeplitz matrices is the zero-state matrix of the cascade $W(z)/A(z)$, whose first column is $h$. So $KG = H$ and $e_w(0) = t$. $\square$

The test of the code checks this identity on random states, inputs and excitations.

## Lemma 2 (the best gain for one vector)

For $t, y \in \mathbb{R}^L$ with $y \ne 0$,

$$\min_{g \in \mathbb{R}} \|t - g y\|^2 = \|t\|^2 - \frac{\langle t, y \rangle^2}{\langle y, y \rangle},$$

attained only at $g^* = \langle t, y \rangle / \langle y, y \rangle$.

*Proof.* $\|t - g y\|^2 = \|t\|^2 - 2g \langle t, y \rangle + g^2 \langle y, y \rangle$ is a quadratic in $g$ with positive leading coefficient $\langle y, y \rangle$, so its unique minimum is where the derivative $-2\langle t, y \rangle + 2g \langle y, y \rangle$ is 0, at $g^*$. Substituting gives the value. $\square$

## Theorem 1 (the search is exact)

Let $y_k = H c_k$ for $k = 1, \ldots, N$. The function search returns $k^*$ and $g^*$ with

$$\|t - g^* y_{k^*}\|^2 = \min_{k} \min_{g} \|t - g y_k\|^2,$$

over all $k$ with $y_k \ne 0$, together with this least error.

*Proof.* By Lemma 2, $\min_g \|t - g y_k\|^2 = \|t\|^2 - \sigma_k$ with the score $\sigma_k = \langle t, y_k \rangle^2 / \langle y_k, y_k \rangle$. The minimum over $k$ of $\|t\|^2 - \sigma_k$ is attained at a $k$ of largest $\sigma_k$, which is the $k$ the loop keeps (the first one, on ties). The gain it returns is $\langle t, y_{k^*} \rangle / \langle y_{k^*}, y_{k^*} \rangle$, which attains the minimum by Lemma 2, and the error it returns is $\|t\|^2 - \sigma_{k^*}$. $\square$

By Lemma 1, the vector $y_k = H c_k$ is exactly the change in the weighted error caused by the excitation $c_k$, so Theorem 1 is a statement about the weighted error of the coded speech: among single vectors of the codebook with free gain, the chosen one leaves the least weighted error in this subframe.

## Theorem 2 (sequential search versus joint search)

Let the adaptive search choose $T$ and $g_a$ by Theorem 1 on $t$, and the fixed search choose $k$ and $g_f$ by Theorem 1 on $t' = t - g_a y_T$. Then the joint optimum

$$E_{\text{joint}} = \min_{T', k', g_1, g_2} \|t - g_1 y_{T'} - g_2 y_{k'}\|^2$$

is at most the sequential error $E_{\text{seq}} = \|t' - g_f y_k\|^2$.

*Proof.* The sequential choice $(T, k, g_a, g_f)$ is one of the choices over which the joint minimum is taken, and $E_{\text{seq}} = \|t - g_a y_T - g_f y_k\|^2$. $\square$

The inequality can be strict, so the sequential search is a heuristic for the joint problem. It is used because it costs $Q + C$ filterings, for $Q$ lags and $C$ code vectors, instead of $Q C$ pairs.

## Theorem 3 (the decoder reproduces the encoder)

If the decoder gets the same $a$, $T$, $g_a$, $k$ and $g_f$ for every subframe, its output equals the $\hat s$ computed in the encoder, sample by sample.

*Proof.* By induction on the subframes. Before the first subframe both have zero synthesis states and zero past excitation. If the states and the past excitation agree before a subframe, both build the same $v_T$ from the same past excitation, the same $e = g_a v_T + g_f c_k$, and run the same recursion $\hat s[n] = e[n] + \sum_k a_k \hat s[n - k]$ from the same state, with the same floating point operations in the same order. So the outputs, the new states and the new past excitation agree. $\square$

## Theorem 4 (exact recovery)

Suppose $A$ is known, the adaptive codebook is off, the input is $s = \frac{1}{A(z)} e^{\text{true}}$ from a zero state, and in each subframe $e^{\text{true}} = g c_j$ for some code vector $c_j$ and gain $g \ne 0$, with no other code vector $c_i$ such that $H c_i$ is a multiple of $H c_j$. Then the encoder finds $j$ and $g$ in every subframe, and $\hat s = s$.

*Proof.* By induction on the subframes, assume that $\hat s = s$ up to the current subframe. Then the synthesis filter of the encoder has the same state as the filter that made $s$, and the weighting filter has been fed $s - \hat s = 0$, so its state is 0. With $e = 0$, the output $\hat s(0)$ is the zero-input response of that state, and $s = \hat s(0) + G e^{\text{true}}$. Hence $t = W(z)$ applied to $G e^{\text{true}}$ from a zero state, that is $t = H e^{\text{true}} = g H c_j$. The score of $c_j$ is $\langle t, y_j \rangle^2 / \langle y_j, y_j \rangle = g^2 \|y_j\|^2 = \|t\|^2$, the largest possible by the Cauchy-Schwarz inequality, and equality for another $c_i$ would need $y_i$ to be a multiple of $y_j$, which is excluded. So the search picks $j$ with gain $\langle t, y_j \rangle / \|y_j\|^2 = g$, the excitation is $e^{\text{true}}$, and $\hat s = s$ on this subframe as well. $\square$

## Remarks

The matrix $H$ is invertible, since its diagonal is $h[0] = 1$, so distinct code vectors $c_i \ne \lambda c_j$ give $y_i \ne \lambda y_j$. The condition of Theorem 4 therefore holds when no two code vectors are multiples of each other, which is true with probability 1 for a Gaussian codebook.

In floating point, Theorem 4 holds up to rounding: the test asks for the indices exactly and for the gains and the output within $10^{-9}$.
