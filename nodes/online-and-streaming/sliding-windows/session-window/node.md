---
tag: 9SPQ0S
kind: concept
slug: session-window
name: Session window
aliases:
- activity window
- session
- gap-based window
area: online-and-streaming/sliding-windows
level: intro
summary: Windows of one key that group items whose timestamps are less than a gap g apart, so a session ends after g time units with no activity.
prereqs: [time-based-window, tumbling-window]
see_also: [tumbling-window, hopping-window, landmark-window, time-based-window, sliding-window-model, interval-tree]
sources:
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau et al., The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015
    locator: Section 1.2 (sessions with a timeout gap) and Section 2.2.2 (window merging, the example Sessions(30m))
  - paper: doi:10.1007/s00778-022-00778-6
    title: Juliane Verwiebe, Philipp M. Grulich, Jonas Traub and Volker Markl, Survey of window types for aggregation in stream processing systems, The VLDB Journal 32, 2023
    locator: the section on session windows among the window types
  - url: https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/
    title: Apache Flink documentation, Windows
    locator: Window Assigners, Session Windows (session gap)
---

A session window groups the items of one key into periods of activity: two items are in the same session when a chain of items links them with gaps less than a fixed timeout $g$, and a session ends when $g$ time units pass with no item. Unlike [tumbling](/tumbling-window/) and [hopping](/hopping-window/) windows, sessions are not aligned to the clock: their starts and lengths depend on the data, and they differ from key to key. The Dataflow model of Akidau et al. (2015) computes them by window merging: each item gets the window $[\tau, \tau + g)$, and overlapping windows merge. On this page an item of the stream $\sigma$ has a key and a timestamp $\tau$, and $g > 0$ is the gap.

## In plain words

Think of the visits of one user to a web site. The user clicks, reads, clicks again, and then goes away. A session is one visit: a run of clicks in which no pause is as long as the timeout. A long pause closes the session, and the next click starts a new one. Each user has their own sessions. A late click that arrives out of order can fill a pause, and then two sessions join into one. So a system cannot close a session at once: it must wait until it knows that no more clicks can come in the pause.

## The idea

Fix one key, and let its timestamps in sorted order be $\tau_{(1)} \le \tau_{(2)} \le \cdots \le \tau_{(m)}$. Each item gets the proto-window $[\tau, \tau + g)$. Two proto-windows $[a, a + g)$ and $[b, b + g)$ with $a \le b$ overlap if and only if $b < a + g$. The sessions are the unions of the groups of proto-windows that are linked by overlaps.

**Batch rule.** Cut the sorted list between $\tau_{(i)}$ and $\tau_{(i+1)}$ exactly when $\tau_{(i+1)} - \tau_{(i)} \ge g$. Each run between two cuts, from $\tau_{(p)}$ to $\tau_{(q)}$, is one session with window $[\tau_{(p)}, \tau_{(q)} + g)$. Proof: inside a run each gap is less than $g$, so consecutive proto-windows overlap and their union is the interval $[\tau_{(p)}, \tau_{(q)} + g)$. At a cut, every proto-window of an earlier item ends at most at $\tau_{(i)} + g \le \tau_{(i+1)}$, so it does not overlap any later one.

```pseudo id=main
SESSION-INSERT(S, τ, g)                 ▷ S: the sessions of one key, disjoint [a, b)
L1  new ← [τ, τ + g)
L2  for each [a, b) in S with a < τ + g and τ < b do
L3      remove [a, b) from S; new ← [min(a, start of new), max(b, end of new))
L4  insert new into S
```

**Online rule.** Lines L1 to L4 add one item in any order of arrival. They keep the invariant that $S$ is the set of sessions of the items so far. Each session is an interval of length at least $g$, and two sessions do not overlap. So the proto-window, of length $g$, overlaps at most two sessions: if it overlapped three, the middle one would start after $\tau$ and end before $\tau + g$, so it would be shorter than $g$. One insertion therefore merges the new item with at most two sessions, which costs $O(\log m)$ time with a balanced search tree or an [interval tree](/interval-tree/) on the sessions of the key. When timestamps arrive in order, only the last session of the key can merge, and the update is $O(1)$.

**Closing.** A session $[a, b)$ is final when the system knows that no item with a timestamp below $b$ will still arrive, for example when its watermark passes $b$. Until then, its aggregate is provisional.

## Examples

- The Dataflow example: gap 30 minutes, and items of one key at 13:02, 13:20 and 13:57. The proto-windows are $[13{:}02, 13{:}32)$, $[13{:}20, 13{:}50)$ and $[13{:}57, 14{:}27)$. The first two overlap and merge into $[13{:}02, 13{:}50)$. The third starts at 13:57, after 13:50, so it is a second session.
- Gap $g = 5$ and timestamps $1, 3, 9, 13, 20$. The gaps are $2, 6, 4, 7$, so the cuts are after 3 and after 13. The sessions are $[1, 8)$, $[9, 18)$ and $[20, 25)$.
- A late item at time 16 then arrives. Its proto-window $[16, 21)$ overlaps $[9, 18)$ and $[20, 25)$, and lines L2 and L3 merge all three into $[9, 25)$. Now the timestamps $9, 13, 16, 20$ form one session, with gaps $4, 3, 4$.

## Where it is used

- Stream processing systems: session windows in Dataflow and Apache Beam, in Apache Flink (with a session gap) and in Kafka Streams (with an inactivity gap). The systems differ in the details at the boundary: the reported end of a session, and whether a gap of exactly $g$ joins two items. Check the documentation of the system.
- Web and app analytics (visits, the length of a visit, the clicks per visit), and the grouping of log events into user sessions.
- Fraud and anomaly detection, where a burst of activity of one account is one unit of analysis.

## References
