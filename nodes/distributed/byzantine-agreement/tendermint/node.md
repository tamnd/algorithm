---
tag: 66KH53
kind: algorithm
slug: tendermint
name: Tendermint
aliases:
- Tendermint BFT
- Tendermint consensus
area: distributed/byzantine-agreement
level: advanced
summary: Round-based BFT consensus for n = 3f + 1 under partial synchrony with a rotating proposer, propose, prevote and precommit steps, polka locks and gossip.
solves: [consensus-problem]
model: partial-synchrony
complexity:
  vars: {n: the number of processes, f: the largest number of Byzantine processes, d: the largest message delay after GST}
  time: {best: 3d}
  messages: {best: Θ(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [consensus-problem, partial-synchrony, byzantine-failure-model, gossip-protocol]
see_also: [pbft, hotstuff, quorum-certificate, byzantine-state-machine-replication, gossip-protocol, proof-of-stake, view-change, quorum-intersection]
sources:
  - url: https://arxiv.org/abs/1807.04938
    title: Ethan Buchman, Jae Kwon and Zarko Milosevic, The latest gossip on BFT consensus, arXiv 1807.04938 (2018)
    locator: Algorithm 1 (the propose, prevote and precommit steps, locks, validValue and validRound, timeouts), and the proofs of agreement and termination
  - paper: "Ethan Buchman, Tendermint, Byzantine fault tolerance in the age of blockchains, MSc thesis, University of Guelph, 2016"
    locator: the earlier description of the protocol and of its use in blockchains
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: the round-based protocol with rotating coordinators and locks under partial synchrony
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the prepare and commit phases that correspond to prevote and precommit
---

Tendermint is a Byzantine [consensus](/consensus-problem/) algorithm for $n = 3f + 1$ processes under [partial synchrony](/partial-synchrony/), built to order the blocks of a blockchain. It decides one value per *height*. Each height runs in *rounds*, and each round has a proposer and three steps: propose, prevote and precommit. A process that sees $2f + 1$ prevotes for a value, a *polka*, locks on the value and precommits it; $2f + 1$ precommits decide. Locks keep a decided value safe across rounds, so Tendermint has no separate view-change protocol: a new round with a new proposer is the view change. Processes talk by [gossip](/gossip-protocol/), and timeouts grow with the round. Jae Kwon designed it in 2014, and Buchman, Kwon and Milosevic gave the current algorithm and its proofs in 2018.

## In plain words

A group of $3f + 1$ computers must agree on the next block, and up to $f$ of them may cheat. They work in rounds, and each round has a different leader, the proposer.

The proposer sends a block. Each computer votes for it in a first vote, the prevote. When a computer sees $2f + 1$ prevotes for the block, it "locks" the block and sends a second vote, the precommit. When it sees $2f + 1$ precommits for the block, the block is final. If anything goes wrong, a timer runs out, the computers vote for "nothing", and the next round starts with the next proposer.

A locked computer will only prevote for another block if it sees proof of a newer polka for that block. This lock stops two blocks from being final.

## The problem

There are $n = 3f + 1$ processes, at most $f$ [Byzantine](/byzantine-failure-model/), with signed messages. At each height each honest process has a way to make a value and a test $valid(v)$. The algorithm must give agreement (no two honest processes decide different values at a height), validity (a decided value is valid) and termination (every honest process decides). The network is partially synchronous: after an unknown time GST, a message between honest processes arrives within an unknown $\Delta$. Tendermint also assumes gossip: a message that one honest process receives reaches all of them. A sequence of heights gives [Byzantine state machine replication](/byzantine-state-machine-replication/).

## The algorithm

Each process keeps its height $h$, round $r$, step, $lockedValue$, $lockedRound$, $validValue$ and $validRound$, with rounds and values at $-1$ and $nil$ at the start of a height. The proposer of round $r$ at height $h$ is a fixed function of $(h, r)$; the implementation uses $(h + r) \bmod n$. Counts are over different senders.

```pseudo id=main
TENDERMINT(p)                                                       ▷ height h, round r; n = 3f + 1
L1  start round r: if p is the proposer: broadcast ⟨PROPOSAL, h, r, validValue or a new value, validRound⟩
L2  on PROPOSAL(v, -1), step propose: prevote v if lockedRound = -1 or lockedValue = v, else nil
L3  on PROPOSAL(v, vr) and 2f + 1 PREVOTE(vr, v), 0 ≤ vr < r, step propose: prevote v if lockedRound ≤ vr or lockedValue = v, else nil
L4  on PROPOSAL(v) and a polka for v in r, the first time, step ≥ prevote: if step = prevote: lock (v, r); precommit v
L5      validValue ← v; validRound ← r
L6  on 2f + 1 PREVOTE(r, nil), step prevote: precommit nil
L7  on PROPOSAL(v) of a round r' and 2f + 1 PRECOMMIT(r', v): decide v; h ← h + 1; reset; start round 0
L8  on f + 1 messages of a round r' > r: start round r'
L9  timeoutPropose(r) expires, step propose: prevote nil
L10 timeoutPrevote(r) expires, after 2f + 1 prevotes of any value: precommit nil
L11 timeoutPrecommit(r) expires, after 2f + 1 precommits of any value: start round r + 1
```

The prevote timeout starts only when $2f + 1$ prevotes of any values arrived, and the precommit timeout only when $2f + 1$ precommits of any values arrived. Every timeout is $timeout(r) = base + r \cdot inc$, so rounds get longer until they fit the real network delay.

## Example

**A correct proposer.** With $n = 4$, unit delays and $p_0$ the proposer, $p_0$ sends PROPOSAL at time 0. At time 1 every process has it and broadcasts PREVOTE. At time 2 every process has a polka, locks, and broadcasts PRECOMMIT. At time 3 every process has 4 precommits and decides. The implementation decides at time 3. Each process sends $2(n - 1)$ votes and the proposer $n - 1$ proposals, $2n(n - 1) + (n - 1) = 27$ messages of their own, and gossip relays them again.

**The lock at work.** Take $n = 4$ with $p_1$ Byzantine and an asynchronous schedule. The tests replay it step by step.

| round | events |
|---|---|
| 0 | $p_0$ proposes $v$. $p_0$ and $p_2$ get prevotes for $v$ from $p_0$, $p_1$, $p_2$: a polka. Both lock $(v, 0)$ and precommit $v$. |
| 0 | $p_0$ gets precommits for $v$ from $p_0$, $p_2$ and $p_1$ and decides $v$. |
| 0 | $p_3$ never got the proposal. It prevotes $nil$ on timeout, sees no polka and precommits $nil$. $p_1$ sends $nil$ votes to $p_2$ and $p_3$. |
| 1 | The faulty proposer $p_1$ proposes a new value $w$ with $vr = -1$. $p_3$ is not locked and prevotes $w$. |
| 1 | $p_2$ is locked on $v$, so by line L2 it prevotes $nil$. $w$ gets 2 prevotes, from $p_1$ and $p_3$, which is not a polka. |

Without the lock, $p_2$ prevotes $w$, $p_1$, $p_2$, $p_3$ form a polka and then $2f + 1$ precommits for $w$, and $p_2$ and $p_3$ decide $w$ while $p_0$ decided $v$. The test shows both outcomes.

## Correctness

The full proof is below.

- **One polka per round.** Two sets of $2f + 1$ prevotes share an honest process, which prevotes once per round. The same holds for precommits.
- **A decision locks $f + 1$ honest processes.** $2f + 1$ precommits for $v$ in round $r$ include $f + 1$ honest ones, and an honest process precommits $v$ only after a polka, when it locks $(v, r)$.
- **No later polka for another value.** By induction on the round: a locked process prevotes another value only on a polka for it in a round at or after its lock, which does not exist, so the other value gets at most $2f$ prevotes.
- **Termination** needs gossip, timeouts that grow, and the pair $validValue$, $validRound$: after GST some round with an honest proposer is long enough, its proposal carries the latest polka, and every locked process accepts it by line L3.

## Complexity

- **Latency.** Three message delays with a correct proposer after GST: proposal, prevote, precommit.
- **Messages.** In a round each process broadcasts one prevote and one precommit, $\Theta(n^2)$ messages. With gossip each message may be sent again by every honest process, so a simple gossip layer costs up to $O(n^3)$ transmissions per round.
- **Rounds.** A round with a faulty proposer costs at least $timeoutPropose(r)$. With $f$ faulty proposers in a row, the cost is $f$ rounds of growing length.
- **Space.** The votes of the current height, $O(n)$ per round.

## Properties

- **Deterministic and partially synchronous.** Safety in every run, termination after GST.
- **Not responsive.** A new proposer cannot know the highest lock from $n - f$ messages alone, so progress after a failure depends on the timeouts, not only on the real delay. This is the price of two voting steps; [HotStuff](/hotstuff/) adds a third step to avoid it.
- **Rotating proposer.** Every round, and every height, can have another proposer.
- **No separate view change.** Locks and $validRound$ carry the state from one round to the next.
- **Optimal resilience.** $n = 3f + 1$.

## Variants and improvements

- **Relation to PBFT.** Prevote and precommit play the roles of PREPARE and COMMIT in [PBFT](/pbft/), and a polka is a prepared certificate. PBFT moves to a new view with a [view change](/view-change/) that ships certificates to the new primary. Tendermint moves to a new round at once and relies on locks: a locked process refuses other values unless shown a newer polka. PBFT keeps one primary while it works; Tendermint rotates.
- **Relation to DLS.** The rounds with rotating proposers and locks follow the protocol of Dwork, Lynch and Stockmeyer for partial synchrony.
- **Weighted voting.** In blockchains each validator has a voting power, and the thresholds $2f + 1$ and $f + 1$ become "more than two thirds" and "more than one third" of the total power. This is the form used in [proof-of-stake](/proof-of-stake/) systems.
- **Evidence and accountability.** A signed vote for two values in one round is proof of misbehaviour that the chain can punish.
- **Earlier versions.** Earlier descriptions of Tendermint differ in details. The 2018 paper states the $validValue$ and $validRound$ rules, which make a proposer re-propose the value of the latest polka, and its termination proof depends on them.

## When to use it

Use Tendermint for a blockchain or replicated log run by a known set of validators, maybe weighted by stake, on a peer-to-peer network where gossip is the natural way to send messages and proposers should rotate. For a few replicas on a fast data-centre network, [PBFT](/pbft/) has a similar latency without gossip. For many validators and responsive leader changes, [HotStuff](/hotstuff/) and its descendants send fewer messages.

## Pitfalls

- **Prevoting without the lock check.** The trace above shows two decisions at one height.
- **Starting the timeouts too early.** The prevote and precommit timeouts must start only after $2f + 1$ messages of any value. Otherwise a process can leave a round before it sees a polka that others see, and the termination argument fails.
- **Forgetting validValue.** A proposer that always proposes a new value can keep locked processes from voting, and with $f$ faulty processes silent no polka forms.
- **Fixed timeouts.** Without growth, rounds may never be long enough after GST.
- **Counting messages instead of senders.** A faulty process can send many votes; each sender counts once per value.
- **No gossip.** Without relaying, a faulty proposer can send its proposal to some processes only, and a process may never see the polka that others locked on.

## Implementations

## History

Jae Kwon described Tendermint in 2014 as a proof-of-stake consensus engine. Ethan Buchman's master's thesis (Guelph, 2016) gave a fuller description, and the Cosmos network used it from 2019. In 2018 Buchman, Kwon and Milosevic published "The latest gossip on BFT consensus", which states the algorithm as Algorithm 1 with the $validValue$ mechanism and gives proofs of agreement and termination. The design goes back to the locking protocol of Dwork, Lynch and Stockmeyer (1988) and to PBFT (1999).

## References
