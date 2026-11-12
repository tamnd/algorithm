---
tag: DGVSB7
kind: definition
slug: ephemeron
name: Ephemeron
aliases:
- ephemeral key-value pair
- ephemeron table
area: systems/garbage-collection
level: advanced
summary: "A key-value pair that keeps its value alive only while the key is reachable by some other path. A value that refers to its own key does not keep the pair alive."
prereqs: [weak-reference]
see_also: [weak-reference, finalization, heap-reachability, tracing-garbage-collection, tricolor-marking, knaster-tarski-theorem, hash-table, garbage]
sources:
  - paper: doi:10.1145/263698.263733
    title: "Barry Hayes, Ephemerons: a new finalization mechanism, OOPSLA 1997, 176-183"
    locator: the definition of ephemerons, the problem of key-value tables whose values refer to their keys, and the change to the marking phase of the collector
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 12.2 (weak references, the subsection on ephemerons and weak tables)
  - url: https://docs.oracle.com/javase/8/docs/api/java/util/WeakHashMap.html
    title: Java Platform SE 8 API, class WeakHashMap
    locator: "the implementation note: the values are held by ordinary strong references, so a value that refers to its own key prevents the key from being discarded"
---

An *ephemeron* is a pair of a key and a value, held by the garbage collector in a special way: the pair keeps its value alive only while the key is alive for some other reason. The key itself is held weakly, as by a [weak reference](/weak-reference/). If the key becomes unreachable, the collector clears the pair, and the value is freed unless something else holds it. The important case is a value that refers to its own key. With a weak key and a strong value, the value would keep the key alive forever; with an ephemeron, it does not. Hayes (1997) introduced ephemerons to build tables that attach data to objects without keeping the objects alive.

## Definition

Use the heap model of [reachability in the heap](/heap-reachability/), with strong edges and, in addition, a set of ephemeron objects. Each ephemeron $e$ has a key $k(e)$ and a value $v(e)$. Neither field is an ordinary strong edge.

**The live set.** Let $\mathrm{Roots}$ be the root objects and $\mathrm{succ}(S)$ the targets of the strong edges from $S$. The *live set* $L$ is the least set of objects such that:

1. $\mathrm{Roots} \subseteq L$;
2. $\mathrm{succ}(L) \subseteq L$;
3. for each ephemeron $e \in L$ with $k(e) \in L$, also $v(e) \in L$.

The map $\Psi(S) = \mathrm{Roots} \cup \mathrm{succ}(S) \cup \{ v(e) : e \in S, \ k(e) \in S \}$ is monotone, so by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) $L$ exists: it is the least fixed point of $\Psi$, and the intersection of all sets that satisfy the three rules. Rule 3 is a conditional edge: the value counts only when both the ephemeron and its key are already live.

**Clearing.** After the collector computes $L$, each ephemeron $e \in L$ with $k(e) \notin L$ is *cleared*: both its fields become null, and the runtime may run a finalizer or a callback for it. The key and, unless otherwise reachable, the value are garbage.

**Why a least fixed point.** The key can be reachable only through the value of this or another ephemeron. If the rule were "the value is live if the key is reachable by any path", the path from the value to the key would justify itself, and nothing would ever be freed. The least fixed point admits a value only after the key has been shown live without it.

**Proposition (marking cost).** $L$ can be computed in $O(n + m + p)$ time, where $n$ is the number of objects, $m$ the number of strong edges and $p$ the number of ephemerons, with one traversal.

*Proof.* Run a graph search from the roots with a stack. When the search pops an ephemeron $e$ and $k(e)$ is marked, mark $v(e)$; otherwise put $e$ on a waiting list of $k(e)$. When the search pops an object $x$, mark the values of all ephemerons on the waiting list of $x$, and delete the list. Each object is pushed once, each strong edge and each ephemeron is handled once, and each ephemeron is on at most one list, once, so the time is $O(n + m + p)$. Every marked object is in $L$: a root is, and each other object is marked by a strong edge from a marked object or by rule 3 with a marked ephemeron and a marked key. Conversely, the marked set $M$ satisfies the three rules: rules 1 and 2 as in a plain search, and for rule 3, if $e$ and $k(e)$ are both marked, then $v(e)$ is marked when the later of the two is popped. So $L \subseteq M$, since $L$ is the least such set. $\square$

A simpler method, which marks without ephemerons, then scans all ephemerons again and again until no new value is marked, gives the same set. It can take time proportional to $p$ times the length of a chain of ephemerons whose values are the keys of other ephemerons.

## Examples and non-examples

**A value that refers to its key.** A root refers to a table object $T$, which holds an entry $E$ with key $K$ and value $V$. The value $V$ has a field that refers to $K$. Nothing else refers to $K$.

- *As a weak pair*, with a weak key and a strong value: the search reaches $T$, $E$ and $V$, and then $K$ through $V$. All five objects stay, forever. The Java documentation of `WeakHashMap` warns about exactly this case.
- *As an ephemeron*: the search reaches $T$ and $E$. Its key $K$ is not marked, so $E$ waits on $K$, which is never marked. The live set is $\{\text{root}, T, E\}$, $E$ is cleared, and $K$ and $V$ are freed.
- If the program also stores $K$ in a root, then $K$ is marked, $E$ is released from the waiting list, and $V$ is marked. Nothing is cleared.

**A chain.** Ephemeron $e_1$ has key $k_1$ and value $k_2$, and ephemeron $e_2$ has key $k_2$ and value $v$. Both ephemerons are live. If $k_1$ is dead, so are $k_2$ and $v$. If a root path reaches $k_1$, then $k_2$ becomes live through $e_1$, and $v$ through $e_2$. The search must be able to release $e_2$ after it has popped $e_2$, which is what the waiting lists do.

**A property table.** A compiler attaches extra data to syntax nodes in a table keyed by the node. The data refers back to the node. An ephemeron table frees each entry when the node itself is no longer used. The `WeakMap` of JavaScript and similar tables in other runtimes give this behavior.

**Non-example: a weak reference.** A weak reference has no value field. It keeps nothing alive, so it cannot express "keep $V$ while $K$ lives", and a table built from a weak reference to the key and a strong reference to the value has the leak above.

**Non-example: an ephemeron that is itself dead.** If no path reaches the ephemeron $e$, rule 3 never applies, even if its key is live. The value of a dead ephemeron is held by nothing.

## Related definitions

- **Weak reference.** A reference that keeps nothing alive: [weak reference](/weak-reference/). An ephemeron is a weak reference to the key, plus a value that is held under a condition.
- **Finalization.** Hayes proposed ephemerons as a finalization mechanism too: clearing an ephemeron tells the program that its key has died. See [finalization](/finalization/).
- **Reachability.** The live set with ephemerons is a least fixed point, like plain [reachability in the heap](/heap-reachability/), of a larger map.
- **Concurrent and incremental marking.** With [tricolor marking](/tricolor-marking/), an ephemeron cannot be scanned in one step, because its value may need to be marked later, when its key turns black or gray.

## References
