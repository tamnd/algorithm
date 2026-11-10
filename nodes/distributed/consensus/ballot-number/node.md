---
tag: D24C0R
kind: concept
slug: ballot-number
name: Ballot (proposal) number
aliases:
- proposal number
- round number
- term
area: distributed/consensus
level: core
summary: Totally ordered identifiers that let newer proposals override older ones.
prereqs: [consensus-problem, quorum]
see_also: [paxos, multi-paxos, raft, view-change, viewstamped-replication, fast-paxos, leader-lease, lamport-clocks]
sources:
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 2.2 (choosing a value, with numbered proposals and the invariant P2c), Section 2.3 (learning a chosen value) and Section 2.5 (implementing the algorithm, with disjoint sets of proposal numbers and stable storage)
  - paper: doi:10.1145/279227.279229
    title: Leslie Lamport, The part-time parliament, ACM Transactions on Computer Systems 16(2), 133-169, 1998
    locator: Section 2 (the ballots of the Synod protocol, each with a unique number, and the conditions on the ballots that keep the decree consistent)
  - paper: "Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX Annual Technical Conference (ATC), 2014"
    locator: Section 5.1 (terms as a logical clock, and a server that rejects a request with a stale term) and Section 5.2 (at most one leader per term)
  - url: https://pmg.csail.mit.edu/papers/vr-revisited.pdf
    title: Barbara Liskov and James Cowling, Viewstamped Replication Revisited, MIT technical report MIT-CSAIL-TR-2012-021, 2012
    locator: Section 4 (view numbers, and the primary of view v chosen by round robin)
---

A ballot number, also called a proposal number, round number, view number, epoch or term, is a label from a totally ordered set that a consensus protocol attaches to each attempt to decide a value. A node that has seen ballot $b$ ignores every message with a smaller ballot, so a newer attempt overrides older ones. In [Paxos](/paxos/), two properties make the protocol safe: no two proposers use the same ballot, and an acceptor never forgets the highest ballot it has promised. The usual way to get unique ballots is a pair (counter, node id) compared in lexicographic order.

## In plain words

A committee keeps rewriting a decision. To stop old drafts from undoing new ones, each draft gets a number, and every member follows one rule: once you have seen draft 7, you throw away any draft with a smaller number.

For this to work, two people must never use the same number, or nobody could tell which of the two drafts is newer. So each person adds their own name to the number, for example "7, Ann" and "7, Bob", and the name breaks the tie.

Members must also write down the highest number they have seen. A member who forgets it after a nap might accept an old draft again.

## The idea

### What a ballot number must give

Let $B$ be the set of ballot numbers. A protocol needs:

1. **A total order.** Any two ballots can be compared, so every node decides the same way which of two messages is newer.
2. **Uniqueness.** Each ballot belongs to at most one proposer (or leader). In Paxos, a ballot is the name of one proposal, and an acceptor may accept at most one value for it.
3. **No upper end.** A proposer can always find a ballot above any ballot it has seen. A proposer whose attempt failed must be able to try again with a higher one.

The order need not be dense, and gaps are harmless. Ballots also need not match real time: they are a logical clock, in the sense of [Lamport clocks](/lamport-clocks/), that only orders attempts.

### Two ways to make ballots unique

**Pairs.** A ballot is a pair $(k, p)$ of a natural number $k$ and a node id $p$, with $(k, p) < (k', p')$ if $k < k'$, or $k = k'$ and $p < p'$. Proposer $p$ uses only pairs with its own id. To go above a ballot $(k, q)$ that it has seen, it uses $(k + 1, p)$.

**Residue classes.** With $n$ proposers numbered $0$ to $n - 1$, proposer $p$ uses only the integers $b$ with $b \bmod n = p$. This is the same order as the pairs, with $b = kn + p$. It is the form in which "different proposers choose their numbers from disjoint sets of numbers" (Paxos Made Simple, Section 2.5). [Viewstamped Replication](/viewstamped-replication/) uses the same idea the other way round: the view number $v$ is not tied to a proposer, but the primary of view $v$ is the replica $v \bmod n$, so each view has exactly one primary.

[Raft](/raft/) uses plain integers, the terms, and does not tie them to nodes. A term can have many candidates, but each server votes at most once in each term, and a leader needs the votes of a majority, so each term has at most one leader (Ongaro and Ousterhout, Section 5.2). Here uniqueness comes from the votes instead of from the number.

### How Paxos uses them

In [Paxos](/paxos/), a proposer with ballot $b$ sends Prepare($b$). An acceptor whose highest promise is below $b$ promises not to take part in any ballot below $b$, and replies with the value it accepted with the highest ballot, if any. The proposer then proposes, in Accept($b$, $v$), the value of the highest ballot that it heard of, or its own value if there is none. Paxos Made Simple states the key invariant as P2c: for any $v$ and $b$, if a proposal with value $v$ and number $b$ is issued, then there is a majority $S$ such that either no acceptor in $S$ has accepted a proposal numbered less than $b$, or $v$ is the value of the highest-numbered proposal among all proposals numbered less than $b$ accepted by the acceptors in $S$. From it follows: if a value is chosen with ballot $b$, every proposal with a higher ballot carries the same value. The proof is by induction over the ballots in their order, so it needs the order to be total. It needs uniqueness because "the value of ballot $b$" must be one value.

The same pattern appears under other names. The [view change](/view-change/) of Viewstamped Replication and PBFT moves to a higher view number. Zab moves to a higher epoch. [Multi-Paxos](/multi-paxos/) keeps one ballot for a whole series of instances while the leader is stable, and a new leader takes a higher one. [Fast Paxos](/fast-paxos/) splits the ballots into fast and classic ones.

### Pitfalls

- **Forgetting promises.** An acceptor must write its highest promised ballot and its accepted ballot and value to stable storage before it replies. The example below shows two values chosen when one acceptor restarts with an empty state.
- **Reusing a ballot.** Two proposers with the same ballot can both get promises and both get a value accepted. The example below shows it.
- **Duelling proposers.** Two proposers that keep choosing a ballot just above the other's can block each other for ever: each Prepare cancels the other's Accept. This does not break safety, but it can stop progress. A single [leader](/omega-failure-detector/), or random backoff, fixes it.
- **Ballots from wall clocks.** A ballot made from the time of a clock is fine if a node id breaks ties and the node never goes back to a smaller ballot after a restart. A clock that is set back can make a node use a ballot below its own earlier one, which its own acceptors then ignore.

## Examples

**Pairs for three proposers.** With proposers A, B and C in this order, the ballots run $(1, A) < (1, B) < (1, C) < (2, A) < (2, B) < \cdots$. If B sees ballot $(4, C)$ in a rejection, its next ballot is $(5, B)$. With residue classes for $n = 3$, A uses $0, 3, 6, \ldots$, B uses $1, 4, 7, \ldots$ and C uses $2, 5, 8, \ldots$, and B, after it sees ballot $14 = 4 \cdot 3 + 2$, next uses $16 = 5 \cdot 3 + 1$.

**A reused ballot gives two decisions.** Three acceptors $a_1$, $a_2$, $a_3$, and two proposers that both use ballot 5.

1. P sends Prepare(5) to $a_1$ and $a_2$, and Q sends Prepare(5) to $a_2$ and $a_3$. No acceptor has promised anything above 5, so all of them promise, and $a_2$ promises to both.
2. P sends Accept(5, x) to $a_1$ and $a_2$. Both accept. Now x has been accepted by the majority $\{a_1, a_2\}$ with ballot 5, so x is chosen.
3. Q sends Accept(5, y) to $a_2$ and $a_3$. The ballot is not below their promise, so both accept. Now y has been accepted by the majority $\{a_2, a_3\}$, so y is chosen too.

**A forgotten promise gives two decisions.** The same acceptors, with unique ballots this time.

1. P sends Prepare(1) to $a_1$ and $a_2$, and both promise.
2. Q sends Prepare(2) to $a_2$ and $a_3$, and both promise. Then Q sends Accept(2, y) to them, and both accept. y is chosen.
3. $a_2$ restarts and has lost its state.
4. The Accept(1, x) of P now reaches $a_1$ and $a_2$. $a_1$ promised only 1, and $a_2$ remembers no promise, so both accept. x is chosen by $\{a_1, a_2\}$ with ballot 1.

In both runs, the two majorities share $a_2$, and the quorum argument fails only because $a_2$ could not tell the two proposals apart in the first run, or forgot the newer one in the second.

## Where it is used

- Every Paxos variant: [Multi-Paxos](/multi-paxos/), [Fast Paxos](/fast-paxos/), [Cheap Paxos](/cheap-paxos/), [Flexible Paxos](/flexible-paxos/), [Vertical Paxos](/vertical-paxos/), where each ballot also has its own configuration, and [EPaxos](/epaxos/), which uses ballots for each instance in recovery.
- [Raft](/raft/) terms, which servers also use to detect stale leaders: a leader that sees a higher term steps down.
- View numbers in [Viewstamped Replication](/viewstamped-replication/) and [PBFT](/pbft/), and epochs in [Zab](/zab/).
- Fencing tokens of lock services and [leader leases](/leader-lease/): a storage server that has seen token $b$ refuses writes with a smaller token, so a holder whose lease ran out cannot do damage.

## References
