---
tag: Q90K2C
kind: concept
slug: read-modify-write
name: Read-modify-write (RMW) operations
aliases:
- RMW
- atomic read-modify-write
area: concurrency/lock-free-structures
level: intro
summary: Atomic steps that replace a word x by f(x) and return x. Any nontrivial one solves two-process consensus; commuting or overwriting ones solve no more than that.
prereqs: [compare-and-swap, fetch-and-add, consensus-number]
see_also: [compare-and-swap, fetch-and-add, test-and-set, load-linked-store-conditional, consensus-number, cas-has-infinite-consensus-number, combining-tree, registers-have-consensus-number-one]
sources:
  - paper: doi:10.1145/48022.48024
    title: Clyde P. Kruskal, Larry Rudolph and Marc Snir, Efficient synchronization of multiprocessors with shared memory, ACM Transactions on Programming Languages and Systems 10(4), 1988
    locator: pages 579 to 601 (the general read-modify-write operation with a function argument, and the combining of such operations)
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149, the section on read-modify-write operations (any nontrivial RMW register solves two-process consensus; an interfering set of functions cannot solve three-process consensus)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5, the sections on read-modify-write operations and on common2 RMW operations (the two theorems of this page, with proofs)
---

A read-modify-write (RMW) operation reads a memory word, computes a new value from the old one, writes the new value, and returns the old one, all in one atomic step. Kruskal, Rudolph and Snir (1988) described the general form RMW$(a, f)$, which applies any function $f$. [Test-and-set](/test-and-set/), swap, [fetch-and-add](/fetch-and-add/) and [compare-and-swap](/compare-and-swap/) are special cases with fixed functions. Herlihy (1991) measured their power with [consensus numbers](/consensus-number/): every RMW other than a plain read solves consensus for two processes, and RMW operations whose functions commute or overwrite each other solve it for no more than two. Compare-and-swap is neither, and it solves consensus for any number.

## In plain words

Many atomic instructions follow the same pattern. They look at a memory word, compute something from it, write the result back, and tell you what was there before. Nothing else can happen in the middle. Adding one is an example, and so is "set it to 1", and so is "replace 5 by 6 if it is still 5".

Since they all follow one pattern, you can ask one question about all of them: how many threads can use this instruction to agree on a value, without waiting for each other? The answer depends on the function. If the function always changes something, two threads can agree. If two calls can be swapped, or the later one wipes out the earlier one, three threads can not. Compare-and-swap is different, and works for any number.

## The idea

**Notation and model.** $n$ is the number of processes; $p$, $q$ and $r$ are processes. Processes are asynchronous and can crash between steps. Memory is sequentially consistent. A *RMW register* holds a value and supports RMW$(f)$ for each function $f$ in a fixed set $F$, plus a read.

```text
RMW(a, f):        ▷ one atomic step
    old := M[a]
    M[a] := f(old)
    return old
```

| Primitive | Function $f$ | Kind |
|---|---|---|
| read | $f(x) = x$ | trivial |
| [test-and-set](/test-and-set/) | $f(x) = 1$ | overwriting |
| swap$(v)$ | $f(x) = v$ | overwriting |
| [fetch-and-add](/fetch-and-add/)$(d)$ | $f(x) = x + d$ | commuting |
| fetch-and-or$(b)$ | $f(x) = x \lor b$ (bitwise) | commuting |
| [compare-and-swap](/compare-and-swap/)$(e, v)$ | $f(x) = v$ if $x = e$, else $x$ | neither |

A function $f$ is *trivial* if it is the identity: then RMW$(f)$ is just a read. A set $F$ is *commuting* if $f(g(x)) = g(f(x))$ for all $f, g \in F$ and all $x$. Function $f$ *overwrites* $g$ if $f(g(x)) = f(x)$ for all $x$. Herlihy calls $F$ *interfering* if, for each pair $f, g \in F$, either they commute or one overwrites the other. The Art of Multiprocessor Programming calls RMW registers with such a set *common2* registers.

**Theorem A (Herlihy 1991).** A RMW register with a nontrivial function $f$ solves wait-free consensus for two processes. So its consensus number is at least 2.

*Proof.* Since $f$ is not the identity, there is a value $v_0$ with $f(v_0) \ne v_0$. Start the register $r$ at $v_0$, and use two more registers $\mathit{prop}[0]$ and $\mathit{prop}[1]$.

```text
DECIDE(p, v):                 ▷ p is 0 or 1
R1  prop[p] := v
R2  old := RMW(r, f)
R3  if old = v0: return v
R4  return prop[1 − p]
```

Each process takes at most 3 steps, so the protocol is wait-free. The first RMW on $r$ returns $v_0$ and sets $r$ to $f(v_0) \ne v_0$. The second RMW returns $f(v_0)$, which is not $v_0$. So exactly one process, the first, gets $v_0$; call it $w$. It returns its own input. The other process returns $\mathit{prop}[w]$, which $w$ wrote at R1 before its RMW, which came before the other RMW, which came before the read at R4. So both return the input of $w$: agreement and validity hold. A crash at any point only removes decisions. $\square$

**Theorem B (Herlihy 1991).** No wait-free protocol for three processes solves consensus with RMW registers whose function sets are interfering, plus read/write registers. So such registers have consensus number exactly 2 (if some function is nontrivial).

The proof is cited, and here only sketched. Assume a protocol for $p$, $q$ and $r$. As in the proof for [registers](/registers-have-consensus-number-one/), there is a *critical* state $s$: the decision is open in $s$, the next step of $p$ makes it 0 (say), and the next step of $q$ makes it 1. Both steps must be RMW on the same register, with functions $f$ (of $p$) and $g$ (of $q$); the other cases (different registers, reads, writes) are as in the register proof.

- If $f$ and $g$ commute, $s \cdot p \cdot q$ and $s \cdot q \cdot p$ leave the same memory. Only $p$ and $q$ know the order. Run $r$ alone from each: it sees the same memory and decides the same value. But the first state is 0-valent and the second is 1-valent.
- If $f$ overwrites $g$, then $s \cdot q \cdot p$ leaves $f(g(x)) = f(x)$, the same memory as $s \cdot p$. Run $r$ alone from each, with the same contradiction.

A third process is what makes this work: $r$ cannot see the local states of $p$ and $q$. With two processes there is no such witness, which is why Theorem A holds.

**What Theorem B does not cover.** CAS functions are neither commuting nor overwriting: CAS$(0, 1)$ followed by CAS$(1, 2)$ gives 2 from 0, the other order gives 1. And CAS solves consensus for any $n$ (see [CAS has infinite consensus number](/cas-has-infinite-consensus-number/)). A set that mixes fetch-and-add and fetch-and-multiply is not interfering either, so Theorem B says nothing about it; its consensus number needs its own argument.

**Combining.** Kruskal, Rudolph and Snir studied RMW for a different reason. If the functions of $F$ are closed under composition, then two requests RMW$(a, f)$ and RMW$(a, g)$ that meet in a switch of the network can be sent on as one request RMW$(a, g \circ f)$. The reply $v$ goes back as $v$ to the first and $f(v)$ to the second. This generalizes the combining of fetch-and-add in the NYU Ultracomputer and is the idea behind a software [combining tree](/combining-tree/).

## Examples

The tests in the implementation folder run Theorem A's protocol in the interleaving explorer for seven nontrivial functions: increment, set to 1, set to 7, doubling, bitwise or with 2, CAS$(0, 1)$ and CAS$(3, 5)$. For each function, the protocol starts at the first value $v_0$ in $0, 1, \ldots, 7$ with $f(v_0) \ne v_0$ (for doubling that is 1, since $2 \cdot 0 = 0$). For each of the four input pairs over a and b, every reachable state is checked: deciders agree on an input, and no process takes more than 3 steps.

With the identity function the same protocol fails at once. Both processes read $v_0$, both think they came first, and they decide differently.

The tests also check the classes on the values $0, \ldots, 7$: additions of 1, 2 and 3 commute; the constants 1 and 7 overwrite each other but do not commute; or with 1, 2 and 4 commute; the CAS functions $(e, v)$ with $e \ne v$ in $\{0, 1, 2\}$ form a set that is not interfering; and increment together with doubling is not interfering.

## Where it is used

- Every atomic instruction of a processor other than load and store is a RMW: `XCHG`, `LOCK XADD`, `LOCK CMPXCHG` and `LOCK OR` on x86, and the `LDADD`, `SWP` and `CAS` family of Armv8.1. On machines with [load-linked/store-conditional](/load-linked-store-conditional/), each RMW is a short LL/SC loop, which is how one pair of instructions gives all of them.
- Programming languages expose them as atomic operations: `fetch_add`, `exchange` and `compare_exchange` in C++, and `getAndAdd`, `getAndSet` and `compareAndSet` in Java.
- The [consensus number](/consensus-number/) hierarchy uses the two theorems of this page to place test-and-set, swap and fetch-and-add at level 2.
- Combining networks and [combining trees](/combining-tree/) rely on the closure of the function set under composition.

## References
