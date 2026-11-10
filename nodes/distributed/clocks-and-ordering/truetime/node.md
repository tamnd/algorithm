---
tag: SPFG5M
kind: concept
slug: truetime
name: TrueTime
aliases:
- TrueTime API
- commit wait
area: distributed/clocks-and-ordering
level: advanced
summary: The clock API of Google Spanner. TT.now() returns an interval [earliest, latest] that holds the real time. Waiting out its width before a commit becomes visible gives external consistency.
prereqs: [clock-skew, external-consistency]
see_also: [external-consistency, clock-skew, clock-drift, marzullo-algorithm, ntp, hybrid-logical-clocks, linearizability, leader-lease]
sources:
  - url: https://www.usenix.org/conference/osdi12/technical-sessions/presentation/corbett
    title: James C. Corbett, Jeffrey Dean, Michael Epstein and others, Spanner, Google's globally-distributed database, OSDI 2012
    locator: Section 3 (the TrueTime API, time masters, the sawtooth of ε) and Section 4.1.2 (the start rule, commit wait and the proof of external consistency)
  - paper: doi:10.1145/2491245
    title: James C. Corbett and others, Spanner, Google's globally distributed database, ACM Transactions on Computer Systems 31(3), 2013
    locator: the journal version, Sections 3 and 4.1.2 (DOI from memory, to be checked)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 8, Unreliable Clocks (clock readings have a confidence interval; synchronized clocks for global snapshots)
---

*TrueTime* is the clock interface of Google's Spanner database (Corbett et al., 2012). Instead of one time value, `TT.now()` returns an interval $[\mathit{earliest}, \mathit{latest}]$ that is guaranteed to hold the real time, and the width $2\varepsilon$ of the interval is kept small, a few milliseconds, by GPS and atomic clocks in every data center. Spanner gives each transaction a timestamp from this interval and does not make the commit visible until the timestamp is surely in the past. This *commit wait* turns bounded clock uncertainty into [external consistency](/external-consistency/).

## In plain words

An ordinary clock says "it is 10:00:00.000", and you do not know how wrong it is. TrueTime says "it is now somewhere between 10:00:00.000 and 10:00:00.008", and it promises that the true time is in that range.

Spanner uses this when it saves a transaction. It stamps the transaction with the late end of the range. Then it waits until even the early end of the range is past the stamp. After that wait, the stamp is surely in the past everywhere. So any transaction that starts later, on any machine, gets a larger stamp. The order of the stamps then agrees with the real order of the transactions, and the cost is a short wait on each commit.

## The idea

**The API.** For a real time $t$ and a server clock $C$:

- `TT.now()` returns an interval $[\mathit{earliest}, \mathit{latest}]$ with $\mathit{earliest} \le t \le \mathit{latest}$, where $t$ is the real time of the call.
- `TT.after(s)` is true if $s$ has surely passed, that is, if $s < \mathit{earliest}$.
- `TT.before(s)` is true if $s$ has surely not arrived, that is, if $s > \mathit{latest}$.

The *instantaneous error bound* $\varepsilon$ is half the width of the interval.

**Where the bound comes from.** Each data center has time masters. Most have GPS receivers; the others, called Armageddon masters, have atomic clocks, so that the two kinds fail in different ways. A daemon on each machine polls several masters every 30 seconds, rejects liars with a variant of [Marzullo's algorithm](/marzullo-algorithm/), and sets its clock. Between polls it assumes a worst-case [drift](/clock-drift/) of 200 µs per second. So $\varepsilon$ grows from about 1 ms (the delay to the masters) to about 7 ms just before the next poll, a sawtooth with a mean $\bar\varepsilon$ of about 4 ms in the paper's measurements.

**The commit rules.** A read-write transaction $T_i$ has a *start* event, when the client sends the commit request, and a *commit* event, when its writes become visible. Its leader picks the commit timestamp $s_i$ and waits:

```pseudo id=main
TT.NOW at real time t                          ▷ C is the server clock, |C(t) − t| ≤ ε
L1  return [C(t) − ε, C(t) + ε]
TT.AFTER(s)
L2  return TT.NOW().earliest > s

COMMIT(T)                                       ▷ run by the leader of T
L3  s ← TT.NOW().latest, read after the commit request arrives   ▷ start rule
    apply the writes at timestamp s
L4  wait until TT.AFTER(s), then make the writes visible          ▷ commit wait
```

Spanner also keeps the timestamps of each leader increasing across its leader leases; the code of this page has one transaction per leader at a time and leaves this out.

**Theorem (external consistency).** If the commit of $T_1$ happens before the start of $T_2$ in real time, then $s_1 < s_2$.

*Proof.* Let $t(e)$ be the real time of event $e$, and let $e_2^{\mathrm{server}}$ be the arrival of the commit request of $T_2$ at its leader.

1. $s_1 < t(e_1^{\mathrm{commit}})$, by commit wait: the writes become visible only when $\mathit{earliest} > s_1$, and $\mathit{earliest}$ is at most the real time.
2. $t(e_1^{\mathrm{commit}}) < t(e_2^{\mathrm{start}})$, by the assumption.
3. $t(e_2^{\mathrm{start}}) \le t(e_2^{\mathrm{server}})$, because the request is sent before it arrives.
4. $t(e_2^{\mathrm{server}}) \le s_2$, by the start rule: $s_2$ is the $\mathit{latest}$ of a `TT.now()` call made at or after $e_2^{\mathrm{server}}$, and $\mathit{latest}$ is at least the real time of that call.

The chain gives $s_1 < s_2$. $\square$

The proof uses only the guarantee of `TT.now()`. It does not need the clocks of the two leaders to agree, only that each interval holds the real time.

**The cost.** By the start rule, $s \le t(e^{\mathrm{server}}) + 2\varepsilon$, and $\mathit{earliest} \ge t - 2\varepsilon$ at every real time $t$. So commit wait ends at most $4\varepsilon$ after the request arrives, and it lasts at least until the real time passes $s$. Spanner reports an expected wait of at least $2\bar\varepsilon$, and it overlaps the wait with the Paxos round that replicates the commit, so in practice much of it is hidden.

**How TrueTime differs from external consistency.** [External consistency](/external-consistency/) is a property of a database: the commit order agrees with the real-time order. TrueTime is one way to get it, with a clock that exposes its uncertainty and a rule that waits it out. Other systems get the same property without TrueTime, for example with a single timestamp oracle or with [consensus](/paxos/) on the order.

## Examples

**Without commit wait.** Let $\varepsilon = 7$ ms. Leader A's clock runs 7 ms fast and leader B's clock 7 ms slow; requests arrive at once and need 1 ms of work.

| event | real time | value |
|---|---|---|
| $T_1$ starts, A computes $s_1$ = latest | 0.000 | $0.000 + 0.007 + 0.007 = 0.014$ |
| $T_1$ commits (no wait) | 0.001 | |
| $T_2$ starts, B computes $s_2$ = latest | 0.003 | $0.003 - 0.007 + 0.007 = 0.003$ |

$T_1$ committed before $T_2$ started, but $s_2 = 0.003 < s_1 = 0.014$. A reader at timestamp 0.010 would see $T_2$ and not $T_1$, which breaks the real-time order.

**With commit wait.** A's earliest is $C(t) - \varepsilon = t$, so `TT.after(0.014)` first holds at real time 0.014, and $T_1$ becomes visible then. If $T_2$ starts at 0.015 on B, $s_2 = 0.015 > s_1$. The code of this page also runs 40 seeded workloads with four servers whose clock errors vary in time: with commit wait no pair is out of order, and without it some runs break the order.

**Snapshot reads.** A read-only transaction takes $s_{\mathrm{read}} = $ `TT.now().latest` and reads the data as of that timestamp, without locks. By the theorem it sees every transaction that committed before it started.

## Where it is used

- Google Spanner, for read-write transactions, lock-free snapshot reads at a timestamp, and schema changes at a future timestamp.
- Cloud Spanner, the public service built on it.
- Leader leases in Spanner use TrueTime intervals, so that two leaders of one Paxos group never have overlapping leases.
- Systems without atomic clocks, such as CockroachDB, use [hybrid logical clocks](/hybrid-logical-clocks/) and an assumed maximum offset instead, and give a weaker guarantee or retry reads in an uncertainty window.

## References
