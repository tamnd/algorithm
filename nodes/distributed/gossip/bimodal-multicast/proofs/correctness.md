---
title: Bimodal multicast never delivers twice, repairs every loss without garbage collection, and its abstract model is a chain-binomial process
proves: [correctness]
status: full
---

**Setting.** Processes $0, \dots, n - 1$ run lines L1 to L7 in lock-step rounds, with $n \ge 2$. Every packet (multicast copy, DIGEST, SOLICIT, DATA) is lost independently with probability $\lambda < 1$. In the abstract protocol of Birman et al. (Appendix A, Figure 15), a process that first receives the message in round $t$ sends it in round $t + 1$ to each other process independently with probability $\beta$, each such packet is lost independently with probability $\varepsilon$, and nobody crashes. Let $p = \beta(1 - \varepsilon)$ and $q = 1 - p$.

**Lemma 1 (integrity).** In every run, every process delivers each message at most once, and only messages that the sender broadcast.

*Proof.* Delivery happens only at line L2, which first checks that the id is not in the set of seen ids and then adds it, so a second receipt of the same id does nothing. The payload of a delivery comes from the multicast at line L1 or from a DATA packet. DATA is sent only at line L6, for a message in the sender's buffer, and a message enters a buffer only at line L2. By induction on the order of events, every delivered message was multicast at line L1. $\square$

**Theorem 1 (repair without garbage collection).** Let $G = \infty$ and let the sender not crash. Then for every message $m$, with probability 1, every process delivers $m$ after a finite number of rounds.

*Proof.* After the round of its broadcast, the sender holds $m$ in its buffer forever. Fix a process $u$ that has not delivered $m$ at the start of a round. In that round, the sender picks $u$ at line L3 with probability $1/(n - 1)$, its DIGEST lists $m$ (line L4), $u$ lists $m$ as missing (line L5), and the sender answers with DATA for $m$ if $m$ is among the $L$ most recent ids that $u$ asks for (line L6). If it is not, $u$ gets a more recent missing message instead. Since the sender broadcasts finitely many messages before any given round, and every message above $m$ that $u$ lacks is repaired by the same argument (by induction on the messages from the newest down), after finitely many rounds $m$ is among the $L$ most recent ids that $u$ lacks. From then on, in each round, $u$ receives $m$ with probability at least $(1 - \lambda)^3/(n - 1) > 0$, independently of earlier rounds given the state. So the number of further rounds is at most geometric and finite with probability 1. A finite union over the processes and messages keeps probability 1. $\square$

The argument needs a finite stream, or at least that $u$ eventually lacks only finitely many messages newer than $m$; with an endless stream at a rate higher than the repair rate, a process can stay behind, which is why the protocol gives up on old messages.

**Lemma 2 (the chain-binomial step).** In the abstract protocol, let $s_t$ be the number of processes that gossip in round $t$ and $r_t$ the number that have not received the message, with $s_0 = 1$, $r_0 = n - 1$. Given $(s_t, r_t)$ and the history, the number $s_{t+1}$ of processes that first receive the message in round $t + 1$ has the binomial distribution with parameters $r_t$ and $1 - q^{s_t}$, and $r_{t+1} = r_t - s_{t+1}$.

*Proof.* Fix a process $u$ among the $r_t$ that lack the message. Each of the $s_t$ gossiping processes sends to $u$ and the packet arrives with probability $\beta(1 - \varepsilon) = p$, independently of the others and of the history, since the coins and the losses of round $t + 1$ are fresh. So $u$ receives no packet with probability $q^{s_t}$ and at least one with probability $1 - q^{s_t}$. For two different processes $u \ne u'$, the events depend on disjoint sets of coins and losses, so they are independent. The sum of $r_t$ independent indicators with the same probability is binomial. The processes that received the message are exactly those that gossip in round $t + 1$ and stop lacking it. $\square$

**Corollary 1.** The probability that no process other than the sender ever receives the message is exactly $q^{n - 1}$. For $n = 50$, $\beta n = 5$ and $\varepsilon = 0.05$ this is $0.905^{49} \approx 0.0075$.

*Proof.* By Lemma 2 with $s_0 = 1$, $s_1 = 0$ with probability $(1 - (1 - q))^{n - 1} = q^{n - 1}$, and when $s_1 = 0$ nobody gossips again. If $s_1 > 0$, some other process has received the message. $\square$

**Corollary 2 (the exact distribution).** The distribution of $n - r_R$, the number of processes that have the message after $R$ rounds, is obtained by summing over the states $(s_t, r_t)$ with the binomial transition of Lemma 2; the implementation does exactly this. Once $s_t = 0$ the state does not change. $\square$

**What is not proved.** That the distribution is bimodal for given parameters is a computation, not a general theorem; Birman et al. also compute it from the recurrence, and they bound the probability of a failed run with the inequalities (1) and (2) of their Appendix A, which cover crashes and loss rates below $\varepsilon$. Those bounds are cited, not proved here.
