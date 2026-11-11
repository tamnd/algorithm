---
tag: WQ62KQ
kind: theorem
slug: forking-lemma
name: Forking lemma
aliases:
- Pointcheval-Stern forking lemma
- general forking lemma
area: cryptography/signatures
level: advanced
summary: "Run an algorithm twice with the same coins and new oracle answers after one point. Both runs succeed at that point with probability at least acc (acc/q - 1/h). It proves Schnorr secure."
prereqs: [random-oracle-model, schnorr-signature, discrete-logarithm-problem]
see_also: [fiat-shamir-heuristic, existential-unforgeability, proof-of-knowledge, sigma-protocol, multisignature-problem, musig, generic-group-model, schnorr-identification-protocol]
sources:
  - paper: "David Pointcheval and Jacques Stern, Security proofs for signature schemes, EUROCRYPT 1996, LNCS 1070, Springer, 1996, pages 387 to 398"
    locator: the forking lemma and the proof of the Schnorr signature in the random oracle model
  - paper: doi:10.1007/s001450010003
    title: David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), 2000, pages 361 to 396
    locator: the full version, with the forking lemma for generic signature schemes and the splitting lemma
  - paper: doi:10.1145/1180405.1180453
    title: Mihir Bellare and Gregory Neven, Multi-signatures in the plain public-key model and a general forking lemma, ACM CCS 2006, pages 390 to 399
    locator: the general forking lemma (the forking algorithm F_A and the bound frk >= acc (acc/q - 1/h)) and its proof
  - paper: "Pascal Paillier and Damien Vergnaud, Discrete-log-based signatures may not be equivalent to discrete log, ASIACRYPT 2005, LNCS 3788, Springer, 2005"
    locator: no algebraic reduction from discrete log to Schnorr forgery in the standard model, under the one-more discrete log assumption
  - paper: "Yannick Seurin, On the exact security of Schnorr-type signatures in the random oracle model, EUROCRYPT 2012, LNCS 7237, Springer, 2012, pages 554 to 571"
    locator: the lower bound that every algebraic reduction from discrete log to Schnorr forgery in the random oracle model loses a factor of about q_h, under the one-more discrete log assumption
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 19, the rewinding lemma and the security proof of the Schnorr signature
---

The forking lemma says that if an algorithm with access to a random oracle succeeds with probability $acc$, then running it a second time with the same random coins, and with new oracle answers from its critical query on, gives two successes at the same query with different answers with probability at least about $acc^2/q$. Pointcheval and Stern introduced it in 1996 to prove the [Schnorr signature](/schnorr-signature/) and other [Fiat-Shamir](/fiat-shamir-heuristic/) signatures secure in the [random oracle model](/random-oracle-model/). This page states and proves the general form of Bellare and Neven (2006), which separates the probability argument from the signature scheme.

**Notation.** $q \ge 1$ is the number of oracle answers that the algorithm uses (for a forger, $q = q_h + 1$ with $q_h$ the hash queries), $\mathcal{H}$ is the set of oracle answers and $h = |\mathcal{H}| \ge 2$. $[q] = \{1, \ldots, q\}$. In the section on the Schnorr signature below, $q$ is the group order, as on the [Schnorr signature](/schnorr-signature/) page, and the lemma is applied with $q_h + 1$ answers from $\mathcal{H} = \mathbb{Z}_q$, so $h$ is the group order there.

## Statement

Let $\mathsf{IG}$ be a randomized algorithm (the input generator), and let $A$ be a randomized algorithm that takes an input $x$ and answers $h_1, \ldots, h_q \in \mathcal{H}$ and returns a pair $(J, \sigma)$ with $J \in \{0\} \cup [q]$. Let

$$acc = \Pr\big[J \ge 1 \;:\; x \leftarrow \mathsf{IG};\ h_1, \ldots, h_q \leftarrow \mathcal{H};\ (J, \sigma) \leftarrow A(x, h_1, \ldots, h_q)\big].$$

The forking algorithm $F_A$, on input $x$, works as follows.

```pseudo id=main
F_A(x)
L1  pick coins ρ for A at random
L2  h_1, …, h_q ← uniform in ℋ
L3  (I, σ) ← A(x, h_1, …, h_q; ρ)
L4  if I = 0 then return (0, ⊥, ⊥)
L5  h'_I, …, h'_q ← uniform in ℋ
L6  (I', σ') ← A(x, h_1, …, h_{I−1}, h'_I, …, h'_q; ρ)
L7  if I' = I and h_I ≠ h'_I then return (1, σ, σ')
L8  return (0, ⊥, ⊥)
```

Let $frk = \Pr[b = 1 : x \leftarrow \mathsf{IG};\ (b, \sigma, \sigma') \leftarrow F_A(x)]$.

**Theorem (general forking lemma, Bellare and Neven 2006).** For every $\mathsf{IG}$ and $A$ as above,

$$frk \;\ge\; acc \cdot \left(\frac{acc}{q} - \frac{1}{h}\right).$$

Hence $acc \le q/h + \sqrt{q \cdot frk}$. The running time of $F_A$ is about twice the running time of $A$. The statement is purely probabilistic: it makes no assumption on what $A$ computes.

## In plain words

Think of a program that asks an oracle a fixed number of questions, gets random answers, and at the end either fails or points at one of its questions. Run it once. Then run it again with the same internal dice and the same answers to all questions before the one it pointed at, but with fresh answers from that question on.

The second run starts like the first one, so it asks the same question at that point. If the program succeeds often, it also succeeds often on the second run at the same question, now with a different answer. A proof needs exactly this: for Schnorr, two signatures with the same commitment and different challenges, which reveal the secret key. The price is that the chance of a double success is about the square of the single chance, divided by the number of questions.

## Proof

Fix the input $x$ for now and drop it from the notation. The coins $\rho$ and the answers $h_1, \ldots, h_q$ are independent and uniform. Write $acc(x) = \Pr[I \ge 1]$ for this fixed $x$.

**Step 1: split by the fork index.** The events $\{I = i, I' = i, h_i \ne h'_i\}$ for $i \in [q]$ are disjoint, and $F_A$ returns $b = 1$ exactly on their union. So

$$frk(x) = \sum_{i=1}^{q} \Pr[I = i \wedge I' = i \wedge h_i \ne h'_i] \;\ge\; \sum_{i=1}^{q} \Big(\Pr[I = i \wedge I' = i] - \Pr[I = i \wedge h_i = h'_i]\Big),$$

because for events $E \subseteq \{I = i\}$ and $F$, $\Pr[E \wedge \neg F] = \Pr[E] - \Pr[E \wedge F] \ge \Pr[E] - \Pr[(I = i) \wedge F]$, here with $E = \{I = i, I' = i\}$ and $F = \{h_i = h'_i\}$.

**Step 2: the collision term.** In line L5, $h'_i$ is drawn uniformly and independently of $\rho$ and of $h_1, \ldots, h_q$, and the event $I = i$ depends only on those. So $\Pr[I = i \wedge h_i = h'_i] = \Pr[I = i] \cdot \frac{1}{h}$. (When $I \ne i$, line L5 draws no $h'_i$; define $h'_i$ to be an independent uniform value in that case, which changes no event that $F_A$ uses.) Summed over $i$ this gives at most $acc(x)/h$.

**Step 3: the two runs at a fixed index.** For $i \in [q]$, let $p_i(\rho, h_1, \ldots, h_{i-1})$ be the probability, over the values $h_i, \ldots, h_q$, that $A$ returns $I = i$, with the coins and the first $i - 1$ answers fixed. On the event $I = i$, the second run of line L6 uses the same $\rho$ and $h_1, \ldots, h_{i-1}$, and fresh independent values in place of $h_i, \ldots, h_q$. So, conditioned on $(\rho, h_1, \ldots, h_{i-1})$, the events $I = i$ and $I' = i$ are independent and each has probability $p_i$. Hence

$$\Pr[I = i \wedge I' = i] = \mathbb{E}\big[p_i^2\big] \;\ge\; \big(\mathbb{E}[p_i]\big)^2 = \Pr[I = i]^2,$$

where the expectation is over $(\rho, h_1, \ldots, h_{i-1})$ and the inequality is Jensen's inequality for the convex function $t \mapsto t^2$ (equivalently, $\mathrm{Var}[p_i] \ge 0$).

**Step 4: sum over the indices.** By the Cauchy-Schwarz inequality, $\sum_{i=1}^{q} a_i^2 \ge \frac{1}{q}\big(\sum_{i=1}^{q} a_i\big)^2$ for real $a_i$. With $a_i = \Pr[I = i]$ and $\sum_i a_i = acc(x)$, Steps 1 to 3 give

$$frk(x) \;\ge\; \frac{acc(x)^2}{q} - \frac{acc(x)}{h}.$$

**Step 5: average over the input.** Now let $x \leftarrow \mathsf{IG}$. Then $frk = \mathbb{E}_x[frk(x)]$ and $acc = \mathbb{E}_x[acc(x)]$, so by Jensen's inequality again,

$$frk \;\ge\; \frac{\mathbb{E}_x[acc(x)^2]}{q} - \frac{acc}{h} \;\ge\; \frac{acc^2}{q} - \frac{acc}{h} = acc\left(\frac{acc}{q} - \frac{1}{h}\right).$$

**The second form.** From $frk \ge acc^2/q - acc/h$ we get $acc^2 - (q/h)\,acc - q \cdot frk \le 0$, so $acc$ is at most the positive root $\frac{q}{2h} + \sqrt{\frac{q^2}{4h^2} + q \cdot frk} \le \frac{q}{h} + \sqrt{q \cdot frk}$. $\blacksquare$

### Use for the Schnorr signature

Let a forger $\mathcal{F}$ break the [Schnorr signature](/schnorr-signature/) with probability $\varepsilon$ after $q_h$ hash queries and $q_s$ signing queries. Build $A$ on input $y = g^x$ as follows. $A$ runs $\mathcal{F}$, answers its $i$-th new hash query with $h_i$, and answers each signing query on $m$ with the honest-verifier simulator: pick $e, s$, set $R = g^s y^{-e}$, and program $H(R \| m) = e$; it aborts if this point was already set, which happens with probability at most $q_s(q_h + q_s)/q$ in total. When $\mathcal{F}$ outputs a valid $(m^*, R^*, s^*)$, $A$ makes sure that $H(R^* \| m^*)$ was asked (one extra query, so $q = q_h + 1$) and returns $J$ = the index of that query. So $acc \ge \varepsilon - q_s(q_h + q_s)/q$.

Both runs in $F_A$ are identical up to the $J$-th query, so they ask the same $J$-th query $(R^*, m^*)$. On success they return $s_1 = k + e_1 x$ and $s_2 = k + e_2 x$ with $e_1 \ne e_2$, where $k = \log_g R^*$. Then $x = (s_1 - s_2)(e_1 - e_2)^{-1} \bmod q$, so the [discrete logarithm](/discrete-logarithm-problem/) is solved with probability $frk \ge acc(acc/(q_h + 1) - 1/q)$, in about twice the time of $\mathcal{F}$.

**Example.** In the code of this page, the group has order $1019$ in $\mathbb{Z}_{2039}^*$ with $g = 4$ and $y = 572 = 4^{123}$. A toy forger makes 4 hash queries and forges on one of them. In one run of $F_A$ the forgery sits at query $J = 2$ with $R = 1066$; the first run gets $e_1 = 160$ and returns $s_1 = 301$, and the second run gets $e_2 = 480$ and returns $s_2 = 939$. Then $x = (301 - 939)(160 - 480)^{-1} \bmod 1019 = 381 \cdot 699^{-1} \bmod 1019 = 123$, the secret key. The forger in the code finds the key by brute force, which works only in this tiny group; the reduction treats it as a black box.

## Consequences

- **Schnorr and Fiat-Shamir signatures.** The bound above proves the [Schnorr signature](/schnorr-signature/) EUF-CMA in the random oracle model under discrete log, and the same argument covers the signatures of the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) built on a sigma protocol with special soundness, including [EdDSA](/ed25519/).
- **Proofs of knowledge.** For a non-interactive proof made by Fiat-Shamir, the lemma gives an extractor that rewinds the prover, so the proof is a [proof of knowledge](/proof-of-knowledge/) in the random oracle model.
- **Multi-signatures.** Bellare and Neven stated the general form to prove their multi-signature scheme in the plain public key model, where the forger's output depends on several oracle answers. The proof of [MuSig](/musig/) forks twice (a double forking lemma), once at the key aggregation hash and once at the signature hash, which costs about the fourth power of the success probability.
- **Blind signatures.** Pointcheval and Stern used the same rewinding in their 2000 paper to prove blind signatures secure against a polylogarithmic number of parallel sessions.

## Tightness

**The lemma itself is close to tight.** Let $A$ ignore its input and its coins, and return $J$ = the first index $i$ with $h_i \in S$ for a fixed set $S \subseteq \mathcal{H}$ of size $s$ (and $J = 0$ if there is none). Then $acc = 1 - (1 - s/h)^q$. The fork succeeds at $J = i$ exactly when $h'_i$ is a different element of $S$, so $frk = acc \cdot (s - 1)/h$. With $q = 8$, $h = 64$ and $s = 8$, this gives $acc \approx 0.656$ and $frk \approx 0.0718$, while the bound gives $0.0436$. With $s/h = 1/q$ in general, $frk \approx acc/q$ and the bound is $acc^2/q - acc/h$: the two differ by a factor of about $1/acc$, so the loss of the factor $q$ cannot be removed from the lemma. The tests of this page check these numbers by simulation.

**The reduction for Schnorr cannot be much tighter.** The forking reduction turns a forger with success $\varepsilon$ into a discrete log solver with success about $\varepsilon^2/q_h$. Seurin (2012) showed that every algebraic reduction from discrete log to Schnorr forgery in the random oracle model loses a factor of about $q_h$, if the one-more discrete log problem is hard. Earlier, Paillier and Vergnaud (2005) showed that no algebraic reduction from discrete log works in the standard model under the same assumption. Tight proofs exist only with stronger tools: in the [generic group model](/generic-group-model/), in the algebraic group model, or from other assumptions.

## History

Pointcheval and Stern introduced the forking lemma at Eurocrypt 1996 in "Security proofs for signature schemes" and gave the full treatment, with blind signatures, in the Journal of Cryptology in 2000. Their statement was tied to signature forgers and carried explicit constants for the number of replays. Bellare and Neven isolated the probability argument as the general forking lemma at ACM CCS 2006, in a paper on multi-signatures in the plain public key model, and their form with the bound $acc(acc/q - 1/h)$ is the one most proofs cite today. Paillier and Vergnaud (2005) and Seurin (2012) showed the limits of such reductions for Schnorr.

## References
