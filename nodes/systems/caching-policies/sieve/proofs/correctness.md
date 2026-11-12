---
title: The hand of SIEVE stops and the queue keeps insertion order
proves: [correctness]
status: full
---

We use the pseudocode of the page with a cache of $c \ge 1$ objects. Write $T$ for the queue, $p$ for the hand, and say that an object $o$ is *older* than $o'$ if $o$ is nearer the tail. The invariants are:

- (I1) $|T| \le c$, and $T$ holds no key twice;
- (I2) the order of $T$ from tail to head is the order in which its objects were last inserted;
- (I3) $p$ is NULL or an object of $T$;
- (I4) an object has visited $= 1$ only if it was requested since it was last inserted or since the hand last cleared its bit.

**Lemma 1 (the loop stops).** Suppose $|T| = c \ge 1$ when line L4 runs. Each pass of the loop on lines L8 to L12 clears the bit of the current object and moves one step toward the head, wrapping from the head to the tail. No pass sets a bit. So after at most $|T|$ passes every object has been visited once by the loop, and its bit is $0$. The loop then stops at an object $o$ with visited $= 0$. In total the loop runs at most $c$ times in one call.

*Proof.* By (I3) and lines L6 and L7, $o$ starts as an object of $T$. Lines L10 to L12 keep $o$ in $T$, since $o.\mathit{prev}$ is NULL only at the head and then $o$ becomes the tail. The objects with a set bit form a finite set that only shrinks during the loop, and the loop condition is false at an object whose bit is $0$. The loop visits the objects of $T$ in cyclic order, so it meets every object within $|T|$ steps. If all bits are set at the start, it clears all of them in the first $|T|$ steps and stops at the object where it began. $\square$

**Theorem.** (I1) to (I4) hold after every request, and a request is a hit if and only if its object is in $T$.

*Proof.* By induction over the requests. All four hold for the empty queue with $p = $ NULL.

*Hit (lines L1 and L2).* Only the bit of $x$ changes, and it changes because $x$ was requested, so (I4) holds. The queue and the hand do not change.

*Miss with $|T| < c$.* Lines L15 and L16 insert $x$ at the head with its bit clear. $x$ was not in $T$, so no key appears twice, and $|T| \le c$. The newest inserted object is at the head, so (I2) holds. The hand does not change.

*Miss with $|T| = c$.* By Lemma 1 the loop stops at an object $o$ of $T$. The bits it clears were cleared by the hand, so (I4) holds. Line L13 sets $p$ to the object just newer than $o$, or to NULL if $o$ is the head. Line L14 then removes $o$. The new $p$ is not $o$, so it is NULL or an object of $T$, and (I3) holds. Removing one object keeps the order of the others, so (I2) holds. Now $|T| = c - 1$, and lines L15 and L16 act as in the case above, so $|T| = c$ after the request.

The hit test on line L1 checks membership in $T$, and the only objects in the cache are those in $T$, so a request is a hit exactly when its object is cached. $\blacksquare$

**Consequences.**

1. *Survivors never move.* No line moves an object inside $T$. An object leaves its place only when line L14 evicts it. This is the difference from CLOCK, which moves a survivor to the head.
2. *The cache size.* The cache never holds more than $c$ objects, and once it is full each miss evicts exactly one object.
3. *Total time.* Every pass of the loop clears a bit that is $1$. By (I4) each such bit was set by a hit after the last time it was cleared, and a hit sets one bit. So the passes over all $n$ requests number at most the number of hits, at most $n$. With a hash table from keys to nodes, every other line takes $O(1)$ time, so the total time is $O(n)$.

**The test file.** It compares the hit sequence with a separate list-based version of Algorithm 1 on 80 seeded random traces, checks (I1) to (I3) and the bit of the requested object after every request, checks every row of the worked example, and checks that a larger cache can have fewer hits.
