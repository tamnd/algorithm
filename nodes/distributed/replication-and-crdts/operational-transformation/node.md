---
tag: C2XWTY
kind: technique
slug: operational-transformation
name: Operational transformation (OT)
aliases:
- OT
- operational transform
area: distributed/replication-and-crdts
level: advanced
summary: Apply each remote edit after changing it against the concurrent edits already applied, so that edits made on different states can run in any order and copies converge.
prereqs: [collaborative-text-editing, happened-before, vector-clocks]
see_also: [tp1-tp2-conditions, collaborative-text-editing, rga, yata, woot, crdt, total-order-broadcast, state-machine-replication]
sources:
  - paper: doi:10.1145/67544.66963
    title: Clarence A. Ellis and Simon J. Gibbs, Concurrency control in groupware systems, SIGMOD 1989
    locator: pages 399 to 407, the transformation matrix for insert and delete, state vectors, and the dOPT algorithm
  - paper: doi:10.1145/215585.215706
    title: David A. Nichols, Pavel Curtis, Michael Dixon and John Lamping, High-latency, low-bandwidth windowing in the Jupiter collaboration system, UIST 1995
    locator: pages 111 to 120, the two-party protocol between a client and the central server, with message counters and the xform function
  - paper: doi:10.1145/240080.240305
    title: Matthias Ressel, Doris Nitsche-Ruhland and Rul Gunzenhäuser, An integrating, transformation-oriented approach to concurrency control and undo in group editors, CSCW 1996
    locator: pages 288 to 297, the adOPTed algorithm, the transformation properties TP1 and TP2, and the transformation of inserts with a priority for ties
  - paper: doi:10.1145/274444.274447
    title: Chengzheng Sun, Xiaohua Jia, Yanchun Zhang, Yun Yang and David Chen, Achieving convergence, causality preservation, and intention preservation in real-time cooperative editing systems, ACM TOCHI 5(1), 1998
    locator: pages 63 to 108, inclusion and exclusion transformation, and the GOT algorithm with undo, do and redo
  - paper: doi:10.1145/289444.289469
    title: Chengzheng Sun and Clarence Ellis, Operational transformation in real-time group editors, issues, algorithms, and achievements, CSCW 1998
    locator: the dOPT puzzle and the GOTO algorithm
  - paper: doi:10.4204/EPTCS.107.5
    title: Aurel Randolph, Hanifa Boucheneb, Abdessamad Imine and Alejandro Quintero, On consistency of operational transformation approach, EPTCS 107, 2013
    locator: pages 45 to 59, which known transformation functions meet TP1 and TP2, and the result that none built on the classical parameters meets both
---

Operational transformation (OT) is a way to keep copies of a document consistent when users edit their own copy at once and send their edits to the others. An edit such as "insert x at index 2" is meant for the state on which it was made. When a site receives an edit made on a different state, because it has already applied other edits that the sender had not seen, it first transforms the edit against those edits: it shifts indices so that the edit has the same effect on the new state. The transformation function $T(a, b)$ takes two edits made on the same state and returns a version of $a$ to run after $b$. Ellis and Gibbs introduced the idea with the dOPT algorithm in 1989. dOPT fails in some cases, and later control algorithms fix it either with a central server, as Jupiter does (Nichols et al. 1995), or with conditions on $T$, the [TP1 and TP2](/tp1-tp2-conditions/) properties of Ressel et al. (1996).

## In plain words

You and a friend both edit "abc". You delete "a". At the same time your friend puts "x" after "b", at index 2. Your friend's message says "insert x at 2", but in your copy "c" is now at index 1, so index 2 is after "c", the wrong place.

The fix is to change the message before you use it: since you deleted a character before index 2, the insert moves one place to the left, to index 1. Now "x" goes between "b" and "c" in your copy too.

OT is a set of such rules for every pair of edit kinds, plus a method that decides which edits to change a message against, and in which order.

## When it applies

OT applies when the state is a sequence or a similar structure, edits are given by positions, users must see their own edits at once, and edits may reach the copies in different orders. It needs:

- **A transformation function** $T$ for every pair of edit kinds. For TP1, two edits $a$ and $b$ made on the same state $s$ must satisfy $s \cdot a \cdot T(b, a) = s \cdot b \cdot T(a, b)$.
- **A control algorithm** that knows which edits were concurrent, for example with [vector clocks](/vector-clocks/) or with a central server, and transforms each incoming edit only against edits made on its own state.
- **Either a server or TP2.** If all edits pass through one server, as in Jupiter, TP1 is enough. Without a server, an edit may be transformed along different paths at different sites, and the results agree only if $T$ also meets TP2.

## The template

The transformation function below is for strings, with edits ins$(p, c, u)$, del$(p)$ and nop, where $p$ is a 0-based index and $u$ is the id of the user who made the insert. It is the inclusion transformation of Ressel et al. (1996), with ties between inserts at one index broken by user id. The second half is one end of a Jupiter link between a client and the server.

```pseudo id=main
T(a, b)                                               ▷ a and b made on the same state; a to run after b
L1  if a = nop or b = nop then return a
    if a and b insert then
L2      if p(a) < p(b) or (p(a) = p(b) and u(a) < u(b)) then return a
L3      return ins(p(a) + 1, c(a), u(a))
    if a inserts and b deletes then
L4      if p(a) ≤ p(b) then return a else return ins(p(a) − 1, c(a), u(a))
    if a deletes and b inserts then
L5      if p(a) < p(b) then return a else return del(p(a) + 1)
    if p(a) < p(b) then return a                      ▷ both delete
L6  if p(a) > p(b) then return del(p(a) − 1)
L7  return nop                                        ▷ both deleted the same character
SEND(op)                                              ▷ one end of a Jupiter link
L8  send (op, my, other);  append (my, op) to outgoing;  my ← my + 1
RECEIVE((op, m, o))                                   ▷ the sender had seen o of our messages
L9  drop from outgoing every entry (k, x) with k < o
L10 for each entry (k, x) in outgoing, in order do
L11     op′ ← T(op, x);  x′ ← T(x, op)
L12     replace x by x′;  op ← op′
    other ← other + 1
L13 return op                                         ▷ ready to apply here
```

Lines L2 and L3 put the insert with the smaller user id first when two inserts hit one index; without the tie rule, both sites would shift their own insert and TP1 would fail. Line L4 moves an insert left past a delete before it, line L5 moves a delete right past an insert at or before it, and lines L6 and L7 handle two deletes.

**Jupiter.** A client applies its own edit, then sends it with SEND. The server keeps one link per client. When an edit arrives from client $k$, the server runs RECEIVE on link $k$, applies the result, and sends it with SEND on every other link. A client runs RECEIVE on its link and applies the result. Each side counts the messages it has sent ($\mathit{my}$) and received ($\mathit{other}$), and keeps the messages the other side has not yet acknowledged. An incoming message names how many of our messages its sender had seen (line L9), so the rest are exactly the ones concurrent with it. Lines L10 to L12 transform the incoming edit through them and, at the same time, transform each of them against the incoming edit, so the outgoing list stays defined on the latest state. The links must be FIFO.

**Why Jupiter needs only TP1.** Each link has two parties, and the server applies all edits in one order. On a link, every state is reached by some number of client edits and some number of server edits, so the states form a two-dimensional grid. Line L11 always transforms two edits made at the same grid point, and both sides walk paths through the grid whose squares are closed by TP1. No edit is ever transformed against two different sequences that reach the same state along two paths of a third dimension, which is the case that TP2 governs. This is the argument of Nichols et al. (1995).

**Cost.** One transformation takes $O(1)$ time. A message is transformed against the unacknowledged messages of its link, so its cost is linear in their number. The server stores one outgoing list per client.

## Classic examples

**dOPT (Ellis and Gibbs 1989).** Each site keeps a log and a state vector, as in [vector clocks](/vector-clocks/). On receipt, dOPT transforms the edit against every logged edit that the sender had not seen, using each logged edit in the form in which it was applied locally. This is wrong when the logged edit was itself made on a different state from the incoming one. A search over small cases, run by the tests, finds the first such case for the transform above: on the empty string, site 1 runs $o_1 = $ ins$(0, x, 1)$ and then $o_3 = $ ins$(1, z, 1)$, and site 2 runs $o_2 = $ ins$(0, y, 2)$ at the same time.

| site | applies | result |
| --- | --- | --- |
| 1 | $o_1$, $o_3$, then $T(T(o_2, o_1), o_3) = $ ins$(2, y)$ | "xzy" |
| 2, dOPT | $o_2$, $T(o_1, o_2) = $ ins$(0, x)$, then $T(o_3, o_2) = $ ins$(2, z)$ | "xyz" |
| 2, correct | $o_2$, ins$(0, x)$, then $T(o_3, T(o_2, o_1)) = $ ins$(1, z)$ | "xzy" |

The error is in $T(o_3, o_2)$: $o_3$ was made after $o_1$ and $o_2$ was not, so they were made on different states and $T$ does not apply to them. Sun and Ellis (1998) call this the dOPT puzzle.

**Jupiter (Nichols et al. 1995).** The template above, with a central server. A run on "ab" with clients A (id 0) and B (id 1):

| step | where | event | result |
| --- | --- | --- | --- |
| 1 | A | ins$(0, x)$, sent with $(\mathit{my}, \mathit{other}) = (0, 0)$ | "xab" |
| 2 | B | del$(1)$, deletes "b", sent with $(0, 0)$ | "a" |
| 3 | server | receives A's edit, nothing to transform, forwards it to B as $(0, 0)$ | "xab" |
| 4 | server | receives B's edit; B had seen 0 server messages, so transform against ins$(0, x)$: del$(2)$; forward to A as $(0, 1)$ | "xa" |
| 5 | B | receives ins$(0, x)$; transform against its pending del$(1)$: stays ins$(0, x)$ | "xa" |
| 6 | A | receives del$(2)$; the server had seen A's one message, so drop it; apply del$(2)$ | "xa" |

All three copies end as "xa". Server-based OT of this kind is the design of many online editors, since the server also gives a natural place for storage and access control; see [state machine replication](/state-machine-replication/) for the general pattern of a single order of commands.

**adOPTed (Ressel et al. 1996).** A peer-to-peer algorithm that keeps the states of the whole system as a grid indexed by state vectors and transforms an edit along any path to the current state. Ressel et al. stated TP1 and TP2 and proved that adOPTed converges when $T$ meets both. The insert rule with user ids in the template is theirs. It meets TP1, but not TP2: see [TP1 and TP2](/tp1-tp2-conditions/) for a counterexample found by search.

**GOT and GOTO (Sun et al. 1998; Sun and Ellis 1998).** GOT orders all edits by a [total order](/total-order/) on timestamps. To apply an edit that comes early in that order, a site undoes the later edits it has applied, applies the new one, and redoes the others after transforming them. It adds the exclusion transformation, the inverse of inclusion. GOT avoids TP2 by always transforming in the total order, at the cost of undo and redo. GOTO avoids undo and redo by reordering the history with transpositions, and needs TP1 and TP2.

## Variations

- **Tombstone transforms.** Keeping deleted characters as hidden entries makes positions stable and lets $T$ meet TP2; this moves OT close to the sequence CRDTs.
- **Context-based OT.** Later control algorithms track for each edit the set of edits it was made after and check this context before every transform, which rules out the dOPT error by construction.
- **Edits on ranges and on trees.** Practical systems transform edits that insert or delete whole strings, apply formatting, or change trees, with a larger table of cases.
- **CRDTs instead of OT.** Sequence CRDTs such as [RGA](/rga/), [YATA](/yata/) and [WOOT](/woot/) give each character a unique id, so an edit names characters, not indices, and needs no transform.

## Pitfalls

- **Transforming edits made on different states.** $T(a, b)$ is defined only when $a$ and $b$ were made on the same state. This is the dOPT puzzle.
- **No tie rule for inserts at one index.** Without a fixed order, both sites shift their own insert, or both keep it, and TP1 fails: "xy" at one site and "yx" at the other.
- **Trusting TP2.** Randolph et al. (2013) show that the known transforms with the classical parameters fail TP2, and that no such transform meets both TP1 and TP2. Peer-to-peer control algorithms that depend on TP2 then need more state, such as tombstones.
- **Non-FIFO links in Jupiter.** The counters assume that messages arrive in order on each link.
- **Forgetting to transform the pending edits.** In line L12 the outgoing list must also be transformed. Otherwise the next incoming message is transformed against stale edits.

## Exercises

1. Show that the transform of the template meets TP1 for two inserts at the same index by working out both orders on "ab" for ins$(1, x, 1)$ and ins$(1, y, 2)$.
2. Remove the tie rule in line L2, so that an insert moves whenever $p(a) \ge p(b)$. Find two edits on the empty string for which TP1 fails.
3. In the Jupiter run above, swap steps 3 and 4: the server receives B's edit first. Work out the messages and check that all copies still end as "xa".
4. Explain why a peer-to-peer system that transforms edits in a fixed total order, as GOT does, does not need TP2.
5. Rerun the dOPT search with only deletes allowed. Can dOPT diverge? Why or why not?

## References
