---
title: Two-party GMW outputs C(x, y) and uses one round per AND layer
proves: [correctness]
status: full
---

We prove that the protocol of lines L1 to L10 outputs $C(x, y)$ when both parties follow it, and that the AND gates use exactly $D$ rounds, where $D$ is the AND depth of $C$. We also prove that Beaver's triple method computes the same shares as the OT method computes.

**Setting.** $v_w$ is the value of wire $w$ in the plain evaluation of $C$ on $(x, y)$. $[w]_1$ and $[w]_2$ are the bits held by $P_1$ and $P_2$. The *AND depth* $\delta(w)$ is $0$ on input wires, $\max(\delta(a), \delta(b))$ for an XOR gate, $\delta(a)$ for an INV gate, and $\max(\delta(a), \delta(b)) + 1$ for an AND gate. $D = \max_w \delta(w)$.

**Invariant (S).** When wire $w$ has been processed, $[w]_1 \oplus [w]_2 = v_w$.

**Input wires.** Line L1: the owner of $w$ picks $r$ and the shares are $v_w \oplus r$ and $r$, which XOR to $v_w$.

**Order.** Line L2 runs $d = 0, 1, \ldots, D$. In step $d$, lines L3 to L6 process the AND gates with $\delta(c) = d$, and then lines L7 to L9 process the XOR and INV gates with $\delta(c) = d$ in topological order. We show that the inputs of each gate are processed before the gate. For an AND gate with $\delta(c) = d$, both inputs have depth at most $d - 1$, so they were processed in an earlier step (or are input wires). For an XOR or INV gate with $\delta(c) = d$, each input has depth at most $d$. An input of depth less than $d$ was processed in an earlier step. An input of depth exactly $d$ is either the output of an AND gate, processed earlier in step $d$, or of an XOR or INV gate of depth $d$ that comes before it in topological order. So every gate is processed once, after its inputs, and every wire is processed.

**XOR gate.** Line L8: $[c]_1 \oplus [c]_2 = [a]_1 \oplus [b]_1 \oplus [a]_2 \oplus [b]_2 = v_a \oplus v_b = v_c$.

**INV gate.** Line L9: $[c]_1 \oplus [c]_2 = [a]_1 \oplus 1 \oplus [a]_2 = v_a \oplus 1 = v_c$.

**AND gate, by OT.** Line L4 sets $[c]_1 = r$. Line L5 builds $T[i][j] = r \oplus (([a]_1 \oplus i) \wedge ([b]_1 \oplus j))$, and line L6 gives $P_2$ the entry with $i = [a]_2$ and $j = [b]_2$. So $[c]_1 \oplus [c]_2 = r \oplus r \oplus ([a]_1 \oplus [a]_2) \wedge ([b]_1 \oplus [b]_2) = v_a \wedge v_b = v_c$.

**AND gate, by a Beaver triple.** The dealer gives shares of $x, y, z$ with $z = x \wedge y$. The parties open $d = v_a \oplus x$ and $e = v_b \oplus y$ and set $[c]_1 = [z]_1 \oplus d[y]_1 \oplus e[x]_1 \oplus de$ and $[c]_2 = [z]_2 \oplus d[y]_2 \oplus e[x]_2$. Then
$$[c]_1 \oplus [c]_2 = z \oplus dy \oplus ex \oplus de.$$
Put $d = v_a \oplus x$ and $e = v_b \oplus y$ and expand over $\mathbb{F}_2$:
$$xy \oplus (v_a y \oplus xy) \oplus (v_b x \oplus xy) \oplus (v_a v_b \oplus v_a y \oplus x v_b \oplus xy) = v_a v_b,$$
since each of $xy$, $v_a y$ and $v_b x$ appears an even number of times. So $[c]_1 \oplus [c]_2 = v_c$.

**Output.** By (S) on the output wires, line L10 returns $[w]_1 \oplus [w]_2 = v_w$, which is $C(x, y)$.

**Rounds.** The AND gates in step $d$ only read wires of depth at most $d - 1$, which are fixed before step $d$ starts, so all their OTs (or openings) can be sent at once: one round per step that has an AND gate. Every $d$ from 1 to $D$ has an AND gate: take a wire $w$ of depth $D$; following back the AND gate that sets its depth, and then an input of that gate of depth one less, we find AND gates of every depth from $D$ down to 1. Step 0 has none. So the AND gates use exactly $D$ rounds. $\blacksquare$
