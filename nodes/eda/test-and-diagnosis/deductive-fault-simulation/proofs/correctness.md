---
title: The deductive list rules are exact for every gate type
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with lines $0, \ldots, L - 1$ in topological order, so every input of a line has a smaller index. Fix a two-valued vector $t$ and a set $A$ of alive single stuck-at faults. Write $g(k)$ for the value of line $k$ in the good circuit under $t$ and $f(k)$ for its value in the circuit with fault $f$. The correct fault list of $k$ is
$$E_k = \{f \in A : f(k) \ne g(k)\}.$$
We show that line L5 and line L6 give $\mathcal{L}[k] = E_k$ for every line, and then that line L7 reports the detected faults.

**Lemma 1 (where a fault acts).** If $f = (\ell, v)$ and $\ell \ne k$, then $f(k)$ is the gate of $k$ applied to the values $f(j)$ of its inputs $j$. If $\ell = k$, then $f(k) = v$.

*Proof.* The faulty circuit is the good circuit with the value of $\ell$ replaced by $v$. Every other line computes its gate on its inputs, as in the good circuit. $\square$

For a fault $f$ that does not sit on the gate line $k$, let $I_f = \{j \text{ input of } k : f(j) \ne g(j)\}$ be the set of flipped inputs. Under $f$, input $j$ has the value $g(j) \oplus [j \in I_f]$. So, by Lemma 1, whether $f$ flips $k$ depends only on the gate type, the good input values and the set $I_f$. Each rule below says for which sets $I_f$ the output flips.

**Lemma 2 (buffer, inverter, branch).** For a gate with one input $j$, $f$ flips $k$ if and only if $j \in I_f$.

*Proof.* A buffer and a fanout branch copy their input, and an inverter complements it. Both maps are one to one, so the output changes exactly when the input does. $\square$

**Lemma 3 (AND, NAND, OR, NOR).** Let $c$ be the controlling value, and let $S$ be the set of inputs with $g(j) = c$. If $S = \emptyset$, $f$ flips $k$ if and only if $I_f \ne \emptyset$. If $S \ne \emptyset$, $f$ flips $k$ if and only if $S \subseteq I_f$ and $I_f \cap \bar{S} = \emptyset$, where $\bar{S}$ is the set of the other inputs.

*Proof.* The output of such a gate takes one value, the controlled value, when at least one input is at $c$, and the other value when no input is at $c$. So it flips exactly when the predicate "some input is at $c$" changes. If $S = \emptyset$, no input is at $c$ in the good circuit. Under $f$, an input is at $c$ exactly when it is flipped, so the predicate changes exactly when $I_f \ne \emptyset$. If $S \ne \emptyset$, the predicate is true in the good circuit. Under $f$, it is false exactly when every input of $S$ is flipped, away from $c$, and no input of $\bar{S}$ is flipped, to $c$. $\square$

**Lemma 4 (XOR, XNOR).** $f$ flips $k$ if and only if $|I_f|$ is odd.

*Proof.* XOR is the sum of the inputs modulo 2, and XNOR is its complement. Flipping the inputs in $I_f$ adds $|I_f|$ modulo 2 to the sum. $\square$

**Lemma 5 (set form).** Let $k$ be a gate line, and suppose $\mathcal{L}[j] = E_j$ for every input $j$ of $k$. Then the rule of line L5 gives exactly the set of faults $f \in A$ that do not sit on $k$ and flip $k$.

*Proof.* A fault $f$ that does not sit on $k$ is in $\mathcal{L}[j]$ exactly when $j \in I_f$. A fault that sits on $k$ is in no input list, since it does not change any line with a smaller index, so the rule never puts it in. For one input, the copy rule takes the faults with $j \in I_f$, which is Lemma 2. For AND-type gates with $S = \emptyset$, the union of the input lists is the set of faults with $I_f \ne \emptyset$. With $S \ne \emptyset$, the intersection over $S$ is the set of faults with $S \subseteq I_f$, and removing the union over $\bar{S}$ keeps those with $I_f \cap \bar{S} = \emptyset$, which is Lemma 3. For XOR and XNOR, the symmetric difference of the lists holds a fault exactly when it lies in an odd number of them, that is when $|I_f|$ is odd, which is Lemma 4. $\square$

**Lemma 6 (each line).** After line $k$ is processed at lines L4 to L6, $\mathcal{L}[k] = E_k$.

*Proof.* By induction over $k$ in topological order. Split $E_k$ into the faults that sit on $k$ and the others. A fault that sits on $k$ is $(k, v)$ for $v \in \{0, 1\}$, and by Lemma 1 it flips $k$ exactly when $v = \lnot g(k)$. Line L6 adds exactly this fault, if it is alive. A fault that sits elsewhere does not change a primary input $k$, so $E_k$ has no other fault when $k$ is an input, which is line L4. When $k$ is a gate line, all inputs are already processed and correct by induction, and Lemma 5 shows that line L5 gives exactly the other faults of $E_k$. $\square$

**Theorem.** For each vector, the algorithm reports exactly the alive faults that the vector detects, so its output is the same as that of serial fault simulation, with or without dropping.

*Proof.* A fault $f$ is detected by $t$ when $f(o) \ne g(o)$ for some primary output $o$, that is, when $f \in E_o$ for some $o$. By Lemma 6, line L7 computes the union of the sets $E_o$, which is exactly the set of alive faults that $t$ detects. With dropping, line L8 removes them, as serial simulation does, so by induction over the vectors each vector is simulated against the right set of alive faults. $\square$
