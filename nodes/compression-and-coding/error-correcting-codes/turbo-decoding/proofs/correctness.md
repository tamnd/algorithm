---
title: What each step of turbo decoding computes exactly, and where it is approximate
proves: [correctness]
status: full
---

Turbo decoding is not an exact decoder of the turbo code. This proof shows what each line computes exactly, why the values that the two decoders exchange contain no information that the receiving decoder already has, and in which case the result would be the exact posterior of the whole code.

**Setting.** The message is $u = (u_0, \ldots, u_{N-1})$, and $u'_i = u_{\pi(i)}$. Encoder 1 is an RSC encoder on $u$ with parity stream $p^1$, encoder 2 is the same kind of encoder on $u'$ with parity stream $p^2$. Each is terminated by its own tail. The channel is memoryless with BPSK, and each received bit has a channel LLR. Write $L_s(t)$ for the channel LLR of the systematic bit $u_t$, $L_s'(i) = L_s(\pi(i))$, and $L_{p1}$, $L_{p2}$ for the parity LLRs. All LLRs are $\ln P(0) / P(1)$.

**Lemma 1 (exact constituent posteriors).** Let $\lambda_t$ be any real numbers. Lines L3 and L6 return, for each $t$,

$$L(u_t) = \ln \frac{\sum_{u : u_t = 0} \exp\bigl(\sum_j \tfrac12 (1 - 2u_j)(L_s(j) + \lambda_j) + \sum_j \tfrac12 (1 - 2p^1_j(u)) L_{p1}(j)\bigr)}{\sum_{u : u_t = 1} (\text{the same sum})},$$

the posterior LLR of $u_t$ in the model where the bits $u_j$ are independent with prior LLRs $\lambda_j$, and only the systematic and parity bits of encoder 1 are observed. The same holds for line L6 with $u'$, $L_s'$ and $L_{p2}$.

*Proof.* This is the theorem of the [BCJR correctness proof](/bcjr-algorithm/) in its log-MAP form, applied to the trellis of the RSC encoder with the branch weight $\tfrac12 (1 - 2u)(L_s + \lambda) + \tfrac12 (1 - 2p) L_p$. The tail steps get $\lambda = 0$; they are part of the paths, and the sum over paths that end in state 0 is the sum over messages $u$, since each message has exactly one terminated path. $\square$

**Lemma 2 (the extrinsic value).** For each $t$, the value $L_e(t) = L(u_t) - \lambda_t - L_s(t)$ of lines L4 and L7 does not depend on $\lambda_t$ or on $L_s(t)$.

*Proof.* In the sum of Lemma 1, the factor that involves $\lambda_t$ and $L_s(t)$ is $\exp\bigl(\tfrac12 (1 - 2u_t)(L_s(t) + \lambda_t)\bigr)$. In the numerator $u_t = 0$, so it is the constant $e^{(L_s(t) + \lambda_t)/2}$, which comes out of the sum. In the denominator it is the constant $e^{-(L_s(t) + \lambda_t)/2}$. So

$$L(u_t) = L_s(t) + \lambda_t + \ln \frac{\sum_{u : u_t = 0} W_t(u)}{\sum_{u : u_t = 1} W_t(u)},$$

where $W_t(u)$ is the weight without the factor of position $t$. The last term is $L_e(t)$, and it involves only $\lambda_j$ and $L_s(j)$ for $j \ne t$ and the parity LLRs. $\square$

So the extrinsic value of a bit is what the code constraint and the other observations say about it. Line L5 gives it to decoder 2 as a prior, and decoder 2 adds its own copy of the systematic LLR; by Lemma 2 decoder 2 does not receive $L_s(t)$ a second time through the prior. Lines L7 and L8 do the same in the other direction.

**Lemma 3 (exactness with independent evidence).** Suppose the prior $\lambda'_i$ that decoder 2 receives on line L5 is the LLR of an observation of $u_{\pi(i)}$ that is independent, given $u$, of all the other observations used by decoder 2, and that the different $\lambda'_i$ come from independent observations. Then line L6 returns the exact posterior LLR of $u'_i$ given all these observations.

*Proof.* Under the assumption, the likelihood of all the observations factors over the bits and the parity stream of encoder 2, as $\prod_i e^{(1 - 2u'_i)\lambda'_i / 2} \cdot \prod_i e^{(1 - 2u'_i) L_s'(i)/2} \cdot \prod_j e^{(1 - 2p^2_j) L_{p2}(j)/2}$ up to factors that do not depend on $u$. With a uniform prior on $u$, the posterior of $u'_i$ is then exactly the expression of Lemma 1 for decoder 2 with $\lambda = \lambda'$. $\square$

**Theorem.** (a) The first iteration gives each bit, at line L6, the exact constituent posterior of decoder 2 with the extrinsic values of decoder 1 as priors, and these priors contain no copy of the bit's own systematic LLR. (b) For $N \ge 2$ the hypothesis of Lemma 3 fails, so the output of turbo decoding is not in general the exact posterior of the turbo code.

*Proof.* (a) Line L1 sets $\lambda = 0$, so line L3 is Lemma 1 for decoder 1, and line L4 gives $L_e^1(t)$, which by Lemma 2 does not depend on $L_s(t)$. Line L5 permutes these values, so the prior of $u'_i$ is $L_e^1(\pi(i))$, a function of $L_s(j)$ for $j \ne \pi(i)$ and of $L_{p1}$. Line L6 is Lemma 1 for decoder 2 with these priors.

(b) $L_e^1(0)$ depends on $L_s(1)$, because the posterior of $u_0$ in the code of encoder 1 depends on the evidence about $u_1$ (the trellis links them). Decoder 2 also uses $L_s(1)$ directly, as the systematic LLR of $u'_{\pi^{-1}(1)}$. So the prior of one bit is not independent of the other observations of decoder 2, the hypothesis of Lemma 3 fails, and the evidence $L_s(1)$ is counted twice. In the language of graphical models, the factor graph of the turbo code has the two trellis chains joined at every message bit, so it has cycles: bit 0, the chain of encoder 1, bit 1, the chain of encoder 2, back to bit 0. The algorithm is belief propagation on this graph with a schedule that runs one whole chain at a time, as McEliece, MacKay and Cheng showed, and belief propagation is exact on trees but not on graphs with cycles. $\blacksquare$

**What the algorithm does guarantee.** Each half iteration is exact for its own constituent code (Lemma 1), the exchanged values exclude the evidence of the bit itself (Lemma 2), and the decision on line L9 is the sign of an LLR whose systematic, prior and extrinsic parts are each computed exactly. Its quality as a decoder is an empirical fact and the subject of EXIT chart and density evolution analysis, not a theorem about each block. The implementation tests check Lemma 1 against a brute-force sum over all messages to $10^{-9}$, check Lemma 2 by changing the bit's own prior and systematic LLR, and measure the gain of the iterations by simulation.
