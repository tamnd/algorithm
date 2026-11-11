---
title: Tendermint never decides two values at one height
proves: [correctness]
status: full
---

**Claim.** Let $n = 3f + 1$ processes run Algorithm 1 of Tendermint, with at most $f$ Byzantine processes and unforgeable signatures. (Agreement) In every run, no two honest processes decide different values at the same height. (Validity) Every decided value was proposed by the proposer of some round and passed the check $valid(v)$. (Termination) Under partial synchrony with gossip, every honest process decides at every height; this part is a sketch of the argument in the paper.

Agreement uses no timing assumption. Fix a height $h$; heights are separate instances, and the messages of one height are never counted at another.

**Setup.** A *polka* for $v$ in round $r$ is a set of $2f + 1$ PREVOTE messages for $v$ in round $r$ from different processes. Two sets of $2f + 1$ processes share at least $f + 1$, so an honest one. The rules of an honest process that the proof uses:

- (T1) In each round it sends at most one PREVOTE and at most one PRECOMMIT.
- (T2) It sends PRECOMMIT for a value $v \ne nil$ in round $r$ only at line L4, when it sees a polka for $v$ in round $r$, and then it sets $lockedValue = v$ and $lockedRound = r$.
- (T3) Its $lockedRound$ never decreases, and it changes $lockedValue$ only at line L4.
- (T4) It sends PREVOTE for $v$ in round $r$ only by line L2, if $lockedRound = -1$ or $lockedValue = v$, or by line L3, if there is a polka for $v$ in a round $vr$ with $0 \le vr < r$ and ($lockedRound \le vr$ or $lockedValue = v$).
- (T5) It decides $v$ at line L7 only with $2f + 1$ PRECOMMIT messages for $v$ in one round.

**Lemma 1.** In one round there is at most one value with a polka, and at most one value with $2f + 1$ PRECOMMIT messages.

*Proof.* Two such sets share an honest process, which by (T1) sent one PREVOTE (or one PRECOMMIT) in the round. $\square$

**Lemma 2.** If an honest process decides $v$ in round $r$, then a set $R$ of at least $f + 1$ honest processes locked $v$ in round $r$.

*Proof.* By (T5) there are $2f + 1$ PRECOMMIT messages for $v$ in round $r$. At least $f + 1$ come from honest processes, and by (T2) each of them locked $(v, r)$. $\square$

**Lemma 3.** Let an honest process decide $v$ in round $r$. Then for every round $r' > r$ there is no polka for any $v' \ne v$, and every process of $R$ has $lockedValue = v$ and $lockedRound \ge r$ at the end of round $r'$.

*Proof.* By induction on $r'$. Assume the claim for all rounds in $(r, r')$, and take $p \in R$. At the start of round $r'$, $p$ has $lockedValue = v$ and $lockedRound \ge r$: it locked $v$ in round $r$, and a later change of the lock needs a polka in a round of $(r, r')$ (T2, T3), which is for $v$ by the induction hypothesis.

Suppose that $p$ sends PREVOTE for $v' \ne v$ in round $r'$. Not by line L2, because $lockedRound \ne -1$ and $lockedValue \ne v'$. By line L3, it needs a polka for $v'$ in a round $vr < r'$ with $lockedRound \le vr$, so $r \le vr < r'$. In round $r$ the polka is for $v$, because $p$ locked $v$ there after a polka (T2) and Lemma 1 allows one value. In rounds of $(r, r')$ the induction hypothesis rules out a polka for $v'$. So $p$ sends PREVOTE for $v$ or for $nil$ in round $r'$.

So at most $n - |R| \le 3f + 1 - (f + 1) = 2f$ processes send PREVOTE for $v'$ in round $r'$, and there is no polka for $v'$. Then no process of $R$ locks another value in round $r'$. $\square$

**Theorem (agreement).** No two honest processes decide different values at height $h$.

*Proof.* Let honest processes decide $v$ in round $r$ and $v'$ in round $r'$, with $r \le r'$. If $r = r'$, Lemma 1 gives $v = v'$. If $r < r'$, the decision on $v'$ needs $2f + 1$ PRECOMMIT messages for $v'$ in round $r'$, so by (T2) an honest process saw a polka for $v'$ in round $r'$. Lemma 3 then gives $v' = v$. $\blacksquare$

**Validity.** An honest process decides at line L7 only on a PROPOSAL message of the proposer of the round, and only if $valid(v)$ holds. $\square$

## Where the lock is used

Lemma 3 is the only place where the locks matter. Without them, the tests of the implementation replay this asynchronous schedule with $n = 4$ and $p_1$ faulty: in round 0, $p_0$ and $p_2$ see a polka for $v$ and precommit it, $p_0$ gets the PRECOMMIT of $p_2$ and a PRECOMMIT from $p_1$ and decides $v$, while $p_3$ sees no polka; in round 1, the faulty proposer $p_1$ proposes a new value $w$, and $p_2$, $p_3$ and $p_1$ form a polka and a commit for $w$. With the lock, $p_2$ sends PREVOTE for $nil$ in round 1, $w$ gets only 2 prevotes, and nothing else is decided.

## Termination (sketch)

The argument of the paper uses three properties.

- **Gossip.** A message that one honest process receives is received by all honest processes; after GST it arrives within $\Delta$ (the implementation relays every new message once).
- **Timeouts that grow with the round.** $timeoutPropose(r)$, $timeoutPrevote(r)$ and $timeoutPrecommit(r)$ grow linearly in $r$, so after GST some round lasts long enough that all honest processes, joined by the round skip of line L8, see all messages of the round before they leave it.
- **validValue and validRound.** A process that sees a polka for $v$ in its current round keeps $v$ as $validValue$ (line L5), and as a proposer it proposes $validValue$ with $validRound$. A locked process accepts it by line L3, because $lockedRound \le validRound$ when the proposer saw the latest polka.

In a long enough round after GST with an honest proposer, all honest processes have seen the latest polka, so the proposal passes line L2 or L3 at every honest process. Then all $2f + 1$ honest processes send PREVOTE and PRECOMMIT for it, and all decide. Proposers rotate, so such a round comes. The implementation checks this: in all runs of its tests, every honest process decides every height after GST.
