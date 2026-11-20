---
title: The NACK fraction of outer loop link adaptation tends to the target whenever the offset stays bounded
proves: [correctness]
status: full
---

**Setting.** Fix a target $\beta_T \in (0, 1)$ and an up step $\Delta_{\mathrm{up}} > 0$, and put $\Delta_{\mathrm{down}} = \Delta_{\mathrm{up}}\, \beta_T/(1 - \beta_T)$, as line L1 does. The loop starts from an offset $\Delta_0$. After transmission $n$ it receives $a_n = 1$ for a NACK or $a_n = 0$ for an ACK, and lines L6 and L7 set

$$\Delta_n = \Delta_{n-1} + a_n \Delta_{\mathrm{up}} - (1 - a_n) \Delta_{\mathrm{down}}.$$

This section treats the loop without the bounds of line L8; the last remark covers them. Let $A_n = a_1 + \cdots + a_n$ be the number of NACKs among the first $n$ transmissions. Nothing is assumed about how the channel, the reports or the schemes produce the feedback: the sequence $a_1, a_2, \ldots$ is arbitrary, and may depend on the past offsets in any way.

**Lemma 1 (the balance of the steps).** $\Delta_{\mathrm{down}}/(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}}) = \beta_T$.

*Proof.* $\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}} = \Delta_{\mathrm{up}}(1 - \beta_T + \beta_T)/(1 - \beta_T) = \Delta_{\mathrm{up}}/(1 - \beta_T)$, and dividing $\Delta_{\mathrm{down}} = \Delta_{\mathrm{up}}\beta_T/(1 - \beta_T)$ by it gives $\beta_T$. $\square$

**Lemma 2 (the offset counts the NACKs).** For every $n \ge 1$, $\Delta_n = \Delta_0 + A_n \Delta_{\mathrm{up}} - (n - A_n)\Delta_{\mathrm{down}}$.

*Proof.* By induction on $n$. For $n = 1$ this is the update rule. If it holds for $n - 1$, then adding $a_n\Delta_{\mathrm{up}} - (1 - a_n)\Delta_{\mathrm{down}}$ gives $\Delta_0 + (A_{n-1} + a_n)\Delta_{\mathrm{up}} - (n - 1 - A_{n-1} + 1 - a_n)\Delta_{\mathrm{down}}$, which is the claim for $n$. $\square$

**Theorem (the NACK fraction).** For every $n \ge 1$,

$$\frac{A_n}{n} = \beta_T + \frac{\Delta_n - \Delta_0}{n(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}})} = \beta_T + \frac{(1 - \beta_T)(\Delta_n - \Delta_0)}{n\,\Delta_{\mathrm{up}}}.$$

Hence, if the offsets stay in an interval $[L, U]$, then $|A_n/n - \beta_T| \le (1 - \beta_T)(U - L)/(n \Delta_{\mathrm{up}})$, and $A_n/n \to \beta_T$. More generally $A_n/n \to \beta_T$ whenever $\Delta_n/n \to 0$.

*Proof.* Lemma 2 gives $\Delta_n - \Delta_0 = A_n(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}}) - n\Delta_{\mathrm{down}}$. Divide by $n(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}})$ and use Lemma 1 for $\Delta_{\mathrm{down}}/(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}})$; the second form uses $\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}} = \Delta_{\mathrm{up}}/(1 - \beta_T)$ from the proof of Lemma 1. If $\Delta_0$ and $\Delta_n$ are both in $[L, U]$, then $|\Delta_n - \Delta_0| \le U - L$, which gives the bound. If $\Delta_n/n \to 0$, the second term tends to 0. $\square$

**Remark (the converse).** The identity also shows what happens when the target cannot be met. If the NACK fraction stays above $\beta_T + \epsilon$ for a long stretch, then $\Delta_n$ grows at least linearly, by $\epsilon n(\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}})$, and the loop backs off more and more; if it stays below $\beta_T - \epsilon$, the offset falls linearly and the loop picks faster schemes. So an offset that drifts without bound is the sign that no offset meets the target, for example because even the slowest scheme fails too often.

**Remark (why the offset stays bounded in practice).** Suppose that, given the offset $\Delta$, a NACK has a probability $p(\Delta)$ that does not increase with $\Delta$ (more backoff means slower schemes and fewer errors), with $p(\Delta) > \beta_T$ for all small enough $\Delta$ and $p(\Delta) < \beta_T$ for all large enough $\Delta$. The expected change of the offset is $p\Delta_{\mathrm{up}} - (1 - p)\Delta_{\mathrm{down}} = (\Delta_{\mathrm{up}} + \Delta_{\mathrm{down}})(p(\Delta) - \beta_T)$ by Lemma 1, which is positive below the balance point and negative above it, so the offset drifts back toward the set where $p(\Delta) = \beta_T$. This is a stochastic approximation argument with a constant step; it gives an offset that stays near the balance point with high probability, with a spread that grows with $\Delta_{\mathrm{up}}$. The theorem itself does not need it, and this proof does not claim it.

**Remark (bounds).** With the bounds of line L8, write $\Delta_n = \Delta_0 + A_n\Delta_{\mathrm{up}} - (n - A_n)\Delta_{\mathrm{down}} + C_n$, where $C_n$ is the total amount removed or added by clamping. The theorem then holds with $\Delta_n - \Delta_0 - C_n$ in place of $\Delta_n - \Delta_0$. If the offset rarely touches the bounds, $C_n/n \to 0$ and the conclusion is unchanged. If it sits at the upper bound, the NACK fraction can stay above the target, and the bound is the reason.
