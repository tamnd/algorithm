---
tag: W8A3HT
kind: definition
slug: transaction-schedule
name: Schedule (transaction history)
aliases:
- transaction schedule
- history of transactions
area: databases/transactions-and-concurrency
level: intro
summary: An interleaving of the read, write, commit and abort actions of several transactions that keeps the order within each transaction.
prereqs: [acid-properties]
see_also: [serializability, conflict-serializability, recoverable-schedule, cascadeless-schedule, strict-schedule, concurrency-control, isolation-levels, linearizability]
sources:
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 1 (transactions, recoverability) and Chapter 2 (histories as partial orders, committed projections, the reads-from relation)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (the page model, transactions, histories and schedules, committed projection)
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the model of transactions as sequences of actions and of schedules as their interleavings
---

A *schedule* (also called a *history*) is a sequence of the read, write, commit and abort actions of several [transactions](/transaction/) that holds every action once and keeps the order of the actions inside each transaction. It is the object that a database scheduler produces and that the correctness classes judge: [serializability](/serializability/) asks whether the schedule has the effect of some serial order, and the recovery classes ([recoverable](/recoverable-schedule/), [cascadeless](/cascadeless-schedule/) and [strict](/strict-schedule/) schedules) ask whether aborts can be handled safely. The model keeps only which item each action touches and whether it reads or writes; the values and the program logic are abstracted away.

## Definition

**Items and actions.** Fix a set $D$ of data items $x, y, z, \ldots$. For a transaction index $i$, an *action* is one of $r_i(x)$ (a read of $x$), $w_i(x)$ (a write of $x$), $c_i$ (commit) and $a_i$ (abort). This is the *page model* or read-write model: $r_i(x)$ returns the current value of $x$, and $w_i(x)$ sets a new value that may depend on everything that $T_i$ has read before.

**Transaction.** A transaction $T_i$ is a finite sequence of reads and writes of $T_i$, followed by at most one *terminal action* $c_i$ or $a_i$. Bernstein, Hadzilacos and Goodman allow a partial order inside a transaction instead of a sequence; every definition below carries over if "the order of $T_i$" means that partial order.

**Schedule.** Let $\mathcal{T} = \{T_1, \ldots, T_n\}$. A *complete schedule* (history) over $\mathcal{T}$ is a sequence $S$ of actions such that:

1. every action of every $T_i$ occurs in $S$ exactly once, and $S$ has no other actions;
2. for all actions $p, q$ of the same $T_i$: if $p$ comes before $q$ in $T_i$, then $p$ comes before $q$ in $S$;
3. every $T_i$ has a terminal action.

A *schedule* is a prefix of a complete schedule. So in a schedule a transaction may still be *active* (no terminal action yet), and no action of $T_i$ follows $c_i$ or $a_i$. We write $p <_S q$ when $p$ comes before $q$ in $S$. Weikum and Vossen use "history" for a complete schedule and "schedule" for a prefix; many texts use the two words as synonyms.

**Derived notions.** For a schedule $S$:

- $T_i$ is *committed* in $S$ if $c_i \in S$, *aborted* if $a_i \in S$, and *active* otherwise.
- The *committed projection* $C(S)$ is the subsequence of $S$ that keeps exactly the actions of the committed transactions. The [serializability](/serializability/) classes are defined on $C(S)$.
- $S$ is *serial* if, for every two transactions $T_i \ne T_j$, all actions of $T_i$ come before all actions of $T_j$ or the other way round.
- Two actions *conflict* if they belong to different transactions, touch the same item, and at least one of them is a write.
- $T_i$ *reads $x$ from* $T_j$ in $S$ ($i \ne j$) if $w_j(x) <_S r_i(x)$, $a_j \not<_S r_i(x)$, and every $w_k(x)$ with $w_j(x) <_S w_k(x) <_S r_i(x)$ has $a_k <_S r_i(x)$. An abort restores the value that its transaction overwrote, so a write of an aborted transaction stops counting from the moment of the abort. The [recovery classes](/recoverable-schedule/) are defined with this relation.

**Counting.** If $T_i$ has $l_i$ actions and $N = l_1 + \cdots + l_n$, then the number of complete schedules over $\mathcal{T}$ is the multinomial coefficient

$$\frac{N!}{l_1!\, l_2! \cdots l_n!},$$

and exactly $n!$ of them are serial. *Proof.* Map a schedule to the word $u_1 \cdots u_N$ where $u_k$ is the index of the transaction of the $k$-th action. Condition 2 means that the actions of $T_i$ fill the positions with $u_k = i$ in their own order, so the word fixes the schedule. Every word with $l_i$ letters $i$ arises. The number of such words is the multinomial coefficient. A serial schedule is fixed by the order of its $n$ blocks, and different orders give different schedules, so there are $n!$ of them. $\square$

## Examples and non-examples

**All schedules of two small transactions.** Let $T_1 = r_1(x)\ w_1(x)\ c_1$ and $T_2 = r_2(x)\ w_2(x)\ c_2$, two transactions that each add 1 to $x$. There are $6!/(3!\,3!) = 20$ complete schedules. Two are serial. Eight are [conflict serializable](/conflict-serializability/): the two serial ones, and six in which one transaction finishes its read and write of $x$ before the other reads $x$, but commits later. In the other twelve, both transactions read $x$ before either one writes it, so one of the two updates is lost.

**A schedule with an active transaction.** $S = r_1(x)\ w_2(x)\ r_2(y)\ c_2\ w_1(y)$ is a schedule but not a complete one: $T_1$ is active. Its committed projection is $C(S) = w_2(x)\ r_2(y)\ c_2$.

**Reads-from across an abort.** In $S = w_1(x)\ w_2(x)\ r_3(x)\ a_2\ c_1\ c_3$, the read $r_3(x)$ comes after $w_2(x)$ and before $a_2$, so $T_3$ reads $x$ from $T_2$, and it has seen a value that the abort later erases. The committed projection is $C(S) = w_1(x)\ r_3(x)\ c_1\ c_3$, and in $C(S)$ the same read seems to read from $T_1$. So $C(S)$ is serial, but $S$ is not [recoverable](/recoverable-schedule/): $T_3$ committed after reading from a transaction that aborted. Correctness needs both kinds of condition.

**Non-examples.**

- With $T_1 = r_1(x)\ w_1(x)\ c_1$, the sequence $w_1(x)\ r_1(x)\ c_1$ is not a schedule over $\{T_1\}$, because it breaks condition 2: the program of $T_1$ reads before it writes.
- $r_1(x)\ c_1\ w_1(y)$ is not a schedule: an action of $T_1$ follows its terminal action.
- $w_1(x)\ c_1\ a_1$ is not a schedule: a transaction ends at most once.
- $r_1(x)\ r_1(x)\ c_1$ over $T_1 = r_1(x)\ c_1$ is not a schedule over $\{T_1\}$: an action occurs twice. (It is a schedule over a different transaction that reads $x$ twice.)

## Related definitions

- **[Serializability](/serializability/), [conflict serializability](/conflict-serializability/) and [view serializability](/view-serializability/)** are properties of $C(S)$. They say whether the committed work has the effect of a serial order.
- **[Recoverable](/recoverable-schedule/), [cascadeless](/cascadeless-schedule/) and [strict](/strict-schedule/) schedules** are properties of the whole of $S$, with its aborts. They say whether an abort can be handled without undoing a commit, without forcing other aborts, or by restoring before images. They are independent of serializability, as the reads-from example shows.
- **Prefix closure.** A class of schedules is *prefix closed* if every prefix of a member is a member. A scheduler that decides online must aim at such a class, since it sees only a prefix. The recovery classes and conflict serializability of $C(S)$ are prefix closed; view serializability is not. For example, $w_1(x)\ w_2(x)\ w_2(y)\ c_2\ w_1(y)\ c_1$ is not view serializable (the last write of $x$ asks for $T_1$ before $T_2$, the last write of $y$ for the opposite), but it is a prefix of the same schedule followed by $w_3(x)\ w_3(y)\ c_3$, which is view equivalent to $T_1 T_2 T_3$.
- **[Concurrency control](/concurrency-control/)** is the problem of building a scheduler: a program that receives actions one by one and outputs a schedule in a chosen class, by running, delaying or rejecting each action. [Isolation levels](/isolation-levels/) are weaker classes that a scheduler may aim at instead.
- **Multiversion schedules** add a version function that says which write each read sees. They are judged by [multiversion serializability](/multiversion-serializability/).
- **Histories in distributed computing.** A history for [linearizability](/linearizability/) is a sequence of invocation and response events of operations on shared objects, with real time. It is a different model: there are no transactions over many items, and the real-time order matters.

## References
