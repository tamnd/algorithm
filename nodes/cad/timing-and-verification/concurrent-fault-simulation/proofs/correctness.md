---
title: Concurrent fault simulation reports the same faults as serial simulation
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with lines $0, \ldots, L - 1$ in topological order, so every input of a line has a smaller index. Let $\Phi$ be the list of single stuck-at faults to simulate and $t_1, t_2, \ldots$ the two-valued vectors. For a vector $t$, write $g_t(k)$ for the value of line $k$ in the good circuit and $f_t(k)$ for its value in the circuit with fault $f$. Let $\mathrm{alive}_i$ be the set of faults alive while vector $t_i$ is simulated: $\Phi$ for $i = 1$, and with dropping, $\Phi$ minus the faults reported for $t_1, \ldots, t_{i-1}$.

The algorithm stores, for each line $k$, a good value $\mathrm{good}[k]$ and a list $\mathrm{lst}[k]$ of pairs (fault, value). Write $\mathrm{lst}[k]|_A$ for the pairs whose fault is in the set $A$. The *correct list* of $k$ for $t$ and $A$ is
$$E_t(k, A) = \{(f, f_t(k)) : f \in A,\ f_t(k) \ne g_t(k)\}.$$

**Lemma 1 (one line is a function of its inputs).** Let $k$ be a line that is not a primary input, and let $A$ be a set of faults. Then $g_t(k)$ and $E_t(k, A)$ depend only on the pairs $(g_t(j), E_t(j, A))$ for the inputs $j$ of $k$, on $A$ and on the gate of $k$. Lines L4 to L7 compute exactly them from these pairs. Moreover $E_t(k, A')$ is $E_t(k, A)|_{A'}$ for $A' \subseteq A$.

*Proof.* The good value is the gate applied to the good input values, which is line L4. For a fault $f \in A$, the value of input $j$ in the faulty circuit is the value of $f$ in $E_t(j, A)$ if $f$ appears there, and $g_t(j)$ otherwise. If $f$ sits on $k$, then $f_t(k)$ is its stuck value. Otherwise $f_t(k)$ is the gate applied to these input values, which is line L6. A fault $f \in A$ that does not sit on $k$ and appears in no input list has every input at the good value, so $f_t(k) = g_t(k)$, and it does not belong in the list. So the set $S$ of line L5 holds every fault that can belong, and line L7 keeps exactly those that do. The last claim holds because each fault's entry is computed from that fault's entries only. $\square$

**Lemma 2 (order of events).** During one vector, each line is taken at line L3 at most once, and when line $k$ is taken, no input of $k$ is taken later in the same vector.

*Proof.* Line L3 takes the scheduled line with the smallest index. Line L8 schedules only fanouts of the line just taken, which have larger indices. So after line $k$ is taken, every line that is scheduled has an index larger than $k$, and in particular no input of $k$ and not $k$ itself. $\square$

**Invariant.** After vector $t_i$ is processed, every line $k$ has $\mathrm{good}[k] = g_{t_i}(k)$ and $\mathrm{lst}[k]|_{\mathrm{alive}_i} = E_{t_i}(k, \mathrm{alive}_i)$.

*Proof.* Fix $i$, and assume the invariant for $i - 1$ (for $i = 1$ there is nothing to assume, since every good value starts at X, which differs from every two-valued value). We show the claim line by line in topological order. Since $\mathrm{alive}_i \subseteq \mathrm{alive}_{i-1}$, Lemma 1 lets us restrict the lists of vector $t_{i-1}$ to $\mathrm{alive}_i$ and keep them correct for that vector.

A primary input is scheduled at line L2, so it is taken. Line L4 reads its value from $t_i$, and its list holds the faults on it whose stuck value differs from that value, which is $E_{t_i}(k, \mathrm{alive}_i)$. Line L8 stores them if they differ from the old ones, and otherwise the old ones are already equal.

Let $k$ be a line that is not an input. If $k$ is taken, then by Lemma 2 its inputs are final for this vector, and correct by induction. Lines L4 to L7 compute $g_{t_i}(k)$ and $E_{t_i}(k, \mathrm{alive}_i)$ by Lemma 1, and line L8 stores them or finds them already stored. If $k$ is not taken, then no input of $k$ changed its good value or its restricted list during vector $t_i$, since a change schedules $k$ at line L8. For $i = 1$ this cannot happen, because every good value changes from X. For $i > 1$, the inputs of $k$ hold the same pairs as at the end of vector $t_{i-1}$, restricted to $\mathrm{alive}_i$, and by induction they are correct for both vectors. Then Lemma 1 says that the correct pair of $k$ is the same for $t_{i-1}$ and for $t_i$, and the stored pair of $k$, restricted to $\mathrm{alive}_i$, is correct for $t_{i-1}$. $\square$

**Theorem.** For each vector $t_i$, line L9 reports exactly the faults of $\mathrm{alive}_i$ that $t_i$ detects. So the output is the same as that of serial fault simulation, which simulates each faulty circuit on its own, with or without dropping.

*Proof.* A fault $f \in \mathrm{alive}_i$ is detected by $t_i$ exactly when $f_{t_i}(o) \ne g_{t_i}(o)$ for some primary output $o$, that is, when $f$ appears in $E_{t_i}(o, \mathrm{alive}_i)$, which by the invariant is $\mathrm{lst}[o]|_{\mathrm{alive}_i}$. Line L9 reads exactly these faults, and line L10 removes them from the alive set as serial simulation with dropping does. $\square$
