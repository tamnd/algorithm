---
title: Correctness of pYIN
proves: [correctness]
status: full
---

pYIN is an estimator, so we do not prove that its track is the true pitch. We prove two things. Stage 1 (lines L1 to L7) computes the candidate probabilities of equation 4 of Mauch and Dixon, and these sum to at most 1. Stage 2 (lines L8 to L14) returns a state sequence of largest weight under the HMM.

## Setup

Let $d'(\tau)$ for $0 \le \tau \le T + 1$ be the cumulative mean normalized difference of a frame, and let $\tau_{\min} \le \tau \le T$ be the lag range. For a threshold $s$, let $B(s) = \{\tau : \tau_{\min} \le \tau \le T,\ d'(\tau) < s\}$. The YIN period $Y(s)$ is defined as follows. If $B(s)$ is not empty, let $\tau_0$ be its smallest element, and let $Y(s)$ be the first $\tau \ge \tau_0$ with $\tau = T$ or $d'(\tau + 1) \ge d'(\tau)$; set $a(s) = 1$. If $B(s)$ is empty, let $Y(s)$ be the smallest lag of the minimum of $d'$ on the range, and set $a(s) = p_a$.

The prior $P(s_1), \ldots, P(s_N)$ is nonnegative and sums to 1. The candidate probability of a lag is

$$P(\tau) = \sum_{i=1}^{N} a(s_i)\, P(s_i)\, [Y(s_i) = \tau].$$

(When $B(s_i)$ is not empty, $d'(Y(s_i)) \le d'(\tau_0) < s_i$, so $a(s_i)$ agrees with the factor $a(s_i, \tau)$ of the paper evaluated at $\tau = Y(s_i)$.)

## Lemma 1 (line L4 computes Y)

The function yin_period returns $(Y(s), a(s) = 1)$ when $B(s)$ is not empty and $(Y(s), \text{false})$ otherwise.

*Proof.* The first loop scans $\tau$ upward from $\tau_{\min}$ and stops at the first $\tau$ with $d'(\tau) < s$, which is $\tau_0$. The inner loop then moves right while $\tau < T$ and $d'(\tau + 1) < d'(\tau)$, so it stops at the first $\tau \ge \tau_0$ with $\tau = T$ or $d'(\tau + 1) \ge d'(\tau)$. That is $Y(s)$. Along the way $d'$ only decreases, so $d'(Y(s)) \le d'(\tau_0) < s$, and the flag true is correct. If no $\tau$ has $d'(\tau) < s$, the second loop keeps the first lag of strictly smaller value, which is the smallest lag of the minimum. $\square$

The test of the code compares this with a different description: the smallest $\tau$ with $d'(\tau) < s$ and ($\tau = T$ or $d'(\tau + 1) \ge d'(\tau)$). The two agree. The lag $Y(s)$ above has both properties. Any smaller lag $\tau'$ with $d'(\tau') < s$ is at least $\tau_0$ and lies on the strictly decreasing run from $\tau_0$ to $Y(s)$, so $d'(\tau' + 1) < d'(\tau')$ and $\tau' < T$.

## Lemma 2 (lines L3 to L5 compute P)

After the loop, mass[$\tau$] $= P(\tau)$ for every $\tau$, where a missing key means 0.

*Proof.* By induction on $i$, after iteration $i$ the value mass[$\tau$] is $\sum_{k \le i} a(s_k) P(s_k) [Y(s_k) = \tau]$. Before the loop every value is 0. Iteration $i$ adds $a(s_i) P(s_i)$ to the key $Y(s_i)$ only, by Lemma 1. At $i = N$ this is $P(\tau)$. $\square$

## Lemma 3 (the mass is a subprobability)

$\sum_\tau P(\tau) \le 1$, with equality if and only if $B(s_i)$ is not empty for every $i$ with $P(s_i) > 0$. Hence the unvoiced weight $0.5 (1 - \sum_k p^*_k)$ of line L7 is nonnegative.

*Proof.* Exchange the sums: $\sum_\tau P(\tau) = \sum_i a(s_i) P(s_i) \sum_\tau [Y(s_i) = \tau] = \sum_i a(s_i) P(s_i)$, since each $s_i$ has exactly one $Y(s_i)$. Each $a(s_i) \le 1$ and the $P(s_i)$ sum to 1, so the total is at most 1. It equals 1 exactly when $a(s_i) = 1$ wherever $P(s_i) > 0$, since $p_a < 1$. Line L7 puts each candidate mass in at most one bin, so $\sum_k p^*_k \le \sum_\tau P(\tau) \le 1$. The code also clips at 0, which only guards against rounding. $\square$

## Corollary (YIN is covered)

For every grid threshold $s_i$ with $P(s_i) > 0$, the YIN period $Y(s_i)$ is a candidate with positive probability, since $P(Y(s_i)) \ge a(s_i) P(s_i) > 0$. So if YIN with some grid threshold is right on a frame, the right period is among the pYIN candidates of that frame.

## Lemma 4 (the Viterbi recursion)

Let the states be $q \in \{0, \ldots, 2M - 1\}$, with start weights $\pi(q) \ge 0$, transition weights $A(q', q) \ge 0$ and observation weights $b_t(q) \ge 0$. The weight of a sequence $q_1, \ldots, q_F$ is

$$w(q_1, \ldots, q_F) = \pi(q_1) b_1(q_1) \prod_{t=2}^{F} A(q_{t-1}, q_t)\, b_t(q_t).$$

Let $V_t(q)$ be the largest weight of a sequence of length $t$ that ends in $q$. Then $\delta_t(q) = \log V_t(q)$ for all $t$ and $q$, with $\log 0 = -\infty$.

*Proof.* By induction on $t$. For $t = 1$ a sequence is one state, so $V_1(q) = \pi(q) b_1(q)$, which is line L8 in logs. For $t \ge 2$, a sequence of length $t$ ending in $q$ is a sequence of length $t - 1$ ending in some $q'$, followed by $q$, and its weight is the weight of the prefix times $A(q', q) b_t(q)$. These factors are nonnegative, so for a fixed $q'$ the largest weight comes from the best prefix, of weight $V_{t-1}(q')$. Hence

$$V_t(q) = b_t(q) \max_{q'} V_{t-1}(q') A(q', q).$$

The logarithm is increasing on $[0, \infty)$ with $\log 0 = -\infty$, so the log of this is $\log b_t(q) + \max_{q'} (\delta_{t-1}(q') + \log A(q', q))$, which is lines L10 and L11. The maximum may skip $q'$ with $A(q', q) = 0$, which add $-\infty$; the code loops only over the $q'$ in the band $|j - i| \le J$, where $A > 0$, and over states with $\delta_{t-1}(q') > -\infty$. If no term is finite, the code sets $\delta_t(q) = -\infty$, which is right, since then $V_t(q) = 0$. $\square$

## Theorem (the decoded track is a best sequence)

If some sequence has positive weight, the path returned by lines L12 and L13 has weight $\max_q V_F(q)$, the largest weight of any sequence. If every sequence has weight 0, the code raises an error.

*Proof.* Line L12 picks $q_F$ with $\delta_F(q_F) = \max_q \delta_F(q)$, which by Lemma 4 is the log of the best weight. If it is $-\infty$, every sequence has weight 0 and the code raises. Otherwise, for $t = F, F - 1, \ldots, 2$, the pointer $\psi_t(q_t)$ is a $q'$ that attains the maximum in the recursion for $V_t(q_t)$, so $V_t(q_t) = V_{t-1}(q_{t-1}) A(q_{t-1}, q_t) b_t(q_t)$ with $q_{t-1} = \psi_t(q_t)$, and $V_{t-1}(q_{t-1}) > 0$ because $V_t(q_t) > 0$. Unrolling this down to $V_1(q_1) = \pi(q_1) b_1(q_1)$ gives $w(q_1, \ldots, q_F) = V_F(q_F)$. Line L14 maps each state to its bin frequency if it is voiced and to unvoiced otherwise, which is the output. $\square$

## Remarks

The proof uses only that all weights are nonnegative. It does not need the $b_t$ to be probability distributions, which they are not here, or the rows of $A$ to sum to 1, which they do not near the ends of the bin range, where the part of the triangular window outside the range is dropped.

With the paper's start, $\pi(q) = 1/M$ on the unvoiced states and 0 on the voiced ones. If the first frame has $\sum_k p^*_k = 1$, then $b_1(q) = 0$ on every unvoiced state, so $V_1 \equiv 0$ and every sequence has weight 0. The theorem then gives the error, and the default start, uniform over all $2M$ states, avoids it.

In floating point, the sums of logs in lines L8 to L11 can lose a few units in the last place per frame, which can change the argmax only between sequences whose weights agree to that precision. The product form underflows to 0 after a few hundred frames of small weights, which would make every sequence look equal; the log form does not.
