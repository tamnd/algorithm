---
tag: QHEC5S
kind: definition
slug: feed-forward-loop
name: Feed-forward loop
aliases:
- FFL motif
area: biology/systems-biology
level: core
summary: The three-gene motif where X regulates Y and both regulate Z. Coherent loops delay responses and incoherent ones make pulses.
prereqs: [gene-regulatory-network, hill-equation]
see_also: [network-motif, network-motif-enumeration, genetic-toggle-switch, repressilator, random-boolean-network, aracne, triangle-counting, directed-graph]
sources:
  - paper: doi:10.1038/ng881
    title: Shai S. Shen-Orr, Ron Milo, Shmoolik Mangan and Uri Alon, Network motifs in the transcriptional regulation network of Escherichia coli, Nature Genetics 31(1), 64-68, 2002
    locator: the feed-forward loop as a motif of the E. coli transcription network
  - paper: doi:10.1073/pnas.2133841100
    title: Shmoolik Mangan and Uri Alon, Structure and function of the feed-forward loop network motif, PNAS 100(21), 11980-11985, 2003
    locator: the eight sign types, coherent and incoherent loops, their relative abundance in E. coli and yeast, and the dynamics with AND and OR input functions
  - paper: doi:10.1126/science.298.5594.824
    title: Ron Milo, Shai Shen-Orr, Shalev Itzkovitz, Nadav Kashtan, Dmitri Chklovskii and Uri Alon, Network motifs, simple building blocks of complex networks, Science 298(5594), 824-827, 2002
    locator: the definition of network motifs and the feed-forward loop in several kinds of networks
  - book: isbn:9781439837177
    title: Uri Alon, An Introduction to Systems Biology, Design Principles of Biological Circuits, 2nd edition, CRC Press, 2019
    locator: the chapter on the feed-forward loop, with the sign-sensitive delay of the coherent loop and the pulse of the incoherent loop
---

A feed-forward loop (FFL) is a pattern of three genes $X$, $Y$ and $Z$ in a [gene regulatory network](/gene-regulatory-network/): $X$ regulates $Y$, and both $X$ and $Y$ regulate $Z$. So $X$ acts on $Z$ along two paths, one direct and one through $Y$. Each of the three edges is an activation or a repression, which gives eight types, and the loop is *coherent* when the two paths have the same overall sign and *incoherent* when they have opposite signs. In the transcription networks of E. coli and yeast the FFL occurs much more often than in random networks, so it is a [network motif](/network-motif/), and two of its types, called C1 and I1, are the most common. With an AND input at $Z$, the all-activating C1 type delays the response to a signal that turns on but not to one that turns off; the I1 type makes a pulse. Counting FFLs in a network and testing them against random networks is [network motif enumeration](/network-motif-enumeration/), which this page does not repeat.

## Definition

**The pattern.** In a directed graph of genes with signed edges, a feed-forward loop is a set of three distinct genes $X$, $Y$, $Z$ with edges $X \to Y$, $X \to Z$ and $Y \to Z$. In the strict, induced form used for motif counts, the graph has no other edges among the three: no edge back from $Z$ or $Y$, so the pattern contains no feedback circuit. $X$ is the *general regulator*, $Y$ the *specific regulator* and $Z$ the *target*.

**Signs and the eight types.** Write $\sigma_{XY}$, $\sigma_{XZ}$ and $\sigma_{YZ}$ in $\{+1, -1\}$ for the signs of the edges. The loop is

- *coherent* if $\sigma_{XZ} = \sigma_{XY} \sigma_{YZ}$, that is, the direct path has the same sign as the indirect one;
- *incoherent* if $\sigma_{XZ} = -\sigma_{XY} \sigma_{YZ}$.

Each of the $2^3 = 8$ sign choices is one type, four coherent and four incoherent. Two have standard names:

- **C1** (coherent type 1): all three edges are activations.
- **I1** (incoherent type 1): $X$ activates $Y$ and $Z$, and $Y$ represses $Z$.

**The input function.** $Z$ has two regulators, so the definition of its dynamics needs a rule that combines them. The two common idealized rules are AND, where $Z$ is made only when both inputs are in their active state, and OR, where either is enough.

**The dynamics in the logic approximation.** Take steep input functions with thresholds, so that a regulator is active when its level is above a threshold $K$. Let a signal $S_x$ make $X$ active from time 0. In the C1 loop with AND, $Y$ follows $dY/dt = \beta_Y - \alpha_Y Y$, rising as $Y(t) = Y_{\mathrm{st}}(1 - e^{-\alpha_Y t})$, and $Z$ starts to be made only when $Y$ passes its threshold $K_{YZ}$ for $Z$.

**The on delay (theorem).** If $K_{YZ} < Y_{\mathrm{st}}$, then in the C1 loop with AND, $Z$ starts at

$$T_{\mathrm{on}} = \frac{1}{\alpha_Y} \ln \frac{1}{1 - K_{YZ} / Y_{\mathrm{st}}},$$

and if $K_{YZ} \ge Y_{\mathrm{st}}$, $Z$ never turns on. When the signal is removed, $X$ becomes inactive at once, and $Z$ production stops with no delay.

*Proof.* $Y(T) = K_{YZ}$ gives $1 - e^{-\alpha_Y T} = K_{YZ} / Y_{\mathrm{st}}$, which has a solution $T > 0$ exactly when $K_{YZ} / Y_{\mathrm{st}} < 1$, and solving for $T$ gives the formula. Before $T_{\mathrm{on}}$ the AND input lacks $Y$, after it both inputs are active. When $S_x$ is removed, the AND input lacks $X$, whatever the level of $Y$. $\square$

So the C1 loop with AND is a *sign-sensitive delay*: it delays the ON step and not the OFF step. A pulse of the signal shorter than $T_{\mathrm{on}}$ gives no output at all, so the loop acts as a filter that ignores brief signals. With OR in place of AND, the delay moves to the OFF step: $Z$ turns on as soon as $X$ is active and stays on until $Y$ has decayed below $K_{YZ}$.

## Examples and non-examples

**Example: the delay with numbers.** Take $\alpha_Y = 1$, $Y_{\mathrm{st}} = 1$ and $K_{YZ} = 0.5$. Then $T_{\mathrm{on}} = \ln 2 \approx 0.69$, in units of the time scale $1 / \alpha_Y$. With $K_{YZ} = 0.9$ the delay grows to $\ln 10 \approx 2.30$, so the threshold tunes the delay.

**Example: the I1 pulse.** In the I1 loop, $X$ activates $Z$ at once, and $Y$ rises at the same time as above. When $Y$ passes its threshold $K_{YZ}$, at the time given by the same formula, it represses $Z$, whose level then falls toward a lower steady state. So $Z$ first rises and then falls back: a pulse. If the repression is complete, $Z$ returns to 0. With incomplete repression, the I1 loop reaches its final level faster than a simple gene with the same final level, since it starts with the larger production rate.

**Example: a loop in a real network.** Alon's book describes the arabinose system of E. coli as a C1 loop with AND: the general regulator CRP activates both the specific regulator AraC and the arabinose genes, and AraC also activates those genes.

**Example: in the motif counts.** Shen-Orr et al. (2002) and Milo et al. (2002) found the FFL over-represented in the E. coli transcription network, and Mangan and Alon (2003) found that C1 and I1 are the most common of the eight types in E. coli and yeast. These are measurements on particular networks, not consequences of the definition.

**Non-example: a cascade.** $X \to Y \to Z$ with no edge from $X$ to $Z$ is not an FFL; $X$ reaches $Z$ by one path only.

**Non-example: a single input module.** $X \to Y$ and $X \to Z$ with no edge between $Y$ and $Z$ is a fan, not an FFL.

**Non-example: the [repressilator](/repressilator/).** Its three genes form the cycle $X \dashv Y \dashv Z \dashv X$. Each gene has one input and one output, and the cycle is a negative feedback circuit that can oscillate, while an FFL has no circuit and a gene with two inputs.

**Non-example: the [genetic toggle switch](/genetic-toggle-switch/).** Two genes that repress each other form a positive feedback circuit with two stable states. An FFL has no circuit, so its steady state is unique for each value of the signal, and its role is in the timing of responses, not in memory.

## Related definitions

- **[Network motif](/network-motif/).** A pattern that occurs more often than in random networks with the same degrees. The FFL is the motif in this sense in transcription networks; as a pattern, it is the transitive triangle of a directed graph.
- **[Network motif enumeration](/network-motif-enumeration/).** The algorithms that count the FFLs and other patterns, and the random networks used for comparison.
- **Feedback circuit.** A directed cycle of regulation, as in the toggle switch and the repressilator. An induced FFL contains none.
- **Autoregulation.** An edge from a gene to itself. Some FFLs in real networks also have autoregulation on $Y$ or $Z$, which changes their timing but not the pattern.
- **Multi-output FFL.** One pair $X$, $Y$ regulating several targets $Z_1, \ldots, Z_k$, each forming an FFL with them.
- **[Gene regulatory network](/gene-regulatory-network/).** The whole network that contains the loops, with the dynamic models used above.

## References
