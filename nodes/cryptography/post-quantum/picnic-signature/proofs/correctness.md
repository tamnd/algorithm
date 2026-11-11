---
title: Honest ZKB++ signatures verify, and three opened pairs reveal the key
proves: [correctness]
status: full
---

We prove completeness of SIGN and VERIFY (lines L1 to L12) and the extraction property that gives soundness. Zero knowledge is stated with its simulator at the end. Indices of players are taken mod 3. The circuit $E_k(p)$ consists of XOR gates, XOR with public constants, rotations, and AND gates; the toy cipher of the code and LowMC both have this form.

**Invariant of the protocol.** For every wire $w$ of the circuit, write $w_0, w_1, w_2$ for the values that the three players hold. We claim $w_0 \oplus w_1 \oplus w_2 = w$, the value of the wire in the plain evaluation of $E_k(p)$.

*Proof.* By induction over the gates in order. Input wires: the key wires hold $k_0, k_1, k_2$ with $k_2 = k \oplus k_0 \oplus k_1$ (line L2), so they XOR to $k$; the plaintext enters only share 0, and $p \oplus 0 \oplus 0 = p$. XOR gate $c = a \oplus b$: each player sets $c_i = a_i \oplus b_i$, and $\bigoplus_i c_i = \bigoplus_i a_i \oplus \bigoplus_i b_i = a \oplus b$. Constant $c = a \oplus K$: only player 0 adds $K$, so the XOR of shares gains $K$ once. Rotation: it is linear over $\mathbb{F}_2$, so it commutes with XOR of shares. AND gate $c = a \wedge b$: by the formula,

$$\bigoplus_{i=0}^{2} c_i = \bigoplus_{i} (a_i b_i \oplus a_{i+1} b_i \oplus a_i b_{i+1}) \oplus \bigoplus_i (R_i \oplus R_{i+1}).$$

The second sum is 0 because each $R_i$ appears twice. In the first sum, the terms $a_i b_i$ give the pairs $(0,0), (1,1), (2,2)$; the terms $a_{i+1} b_i$ give $(1,0), (2,1), (0,2)$; and $a_i b_{i+1}$ gives $(0,1), (1,2), (2,0)$. These are all nine pairs once, so the sum is $\bigoplus_{i,j} a_i b_j = (\bigoplus_i a_i)(\bigoplus_j b_j) = a \wedge b$. $\square$

**Lemma 1 (locality).** The view of player $e$, that is all its wire values, is a function of $\mathrm{seed}_e$ (and $k_2$ if $e = 2$), $\mathrm{seed}_{e+1}$ (and $k_2$ if $e + 1 = 2$), and the AND outputs of player $e + 1$.

*Proof.* Player $e$'s input share comes from its seed or is $k_2$. Its random tape comes from its seed. Its XOR, constant and rotation gates use only its own values. At an AND gate it uses its own shares, the shares $a_{e+1}, b_{e+1}$ of player $e + 1$, and the tape bits $R_e, R_{e+1}$. So it is enough that player $e + 1$'s input wires to each AND gate are known. Player $e + 1$'s values are functions of its input share and seed through linear gates, and of its own earlier AND outputs, which are given. By induction over the gates, all of player $e + 1$'s wire values are known, and so all of player $e$'s. $\square$

**Theorem 1 (completeness).** For an honest signer with $y = E_k(p)$, VERIFY accepts.

*Proof.* Fix a repetition $j$ with challenge $e$. By Lemma 1, line L10 computes the same view of player $e$ as line L3 did, and the same values of player $e + 1$, since the AND outputs of $e + 1$ are copied from the true view at line L7. So the recomputed $y_e$, $y_{e+1}$ equal those of line L4, and the recomputed $C_e$, $C_{e+1}$ equal those of line L4, because $H$ is a function and its inputs are the same. By the invariant applied to the output wires, $y_0 \oplus y_1 \oplus y_2 = E_k(p) = y$, so line L11 gives $y_{e+2} = y \oplus y_e \oplus y_{e+1}$, the true share. $C_{e+2}$ is copied from line L4. So the input of the hash at line L12 is exactly the input at line L5, and the challenges agree. $\blacksquare$

**Theorem 2 (extraction).** Suppose that for one repetition three responses, one for each $e \in \{0, 1, 2\}$, all pass line L10 and line L11 against the same commitments $C_0, C_1, C_2$ and the same output shares $y_0, y_1, y_2$. If no two different openings of a commitment are known (the hash is collision resistant), the three openings define $k_0, k_1, k_2$ with $E_{k_0 \oplus k_1 \oplus k_2}(p) = y$.

*Proof.* Each $C_i$ is opened in two of the three responses (as player $e = i$ and as player $e + 1 = i$). Without a collision, both openings of $C_i$ give the same seed, the same $k_2$ if $i = 2$, and the same AND outputs $c_i$. So there is one well-defined view per player, and from the seeds one input share $k_i$ per player. Response $e$ passing line L10 means that the AND outputs of player $e$ are exactly those that the AND formula gives from the views of $e$ and $e + 1$; this holds for every $e$, so the three views are a correct run of the protocol on the input shares $k_0, k_1, k_2$. Passing line L11 and the hash means $y_0 \oplus y_1 \oplus y_2 = y$. By the invariant, a correct run outputs shares that XOR to $E_{k_0 \oplus k_1 \oplus k_2}(p)$. $\square$

So a cheater without a key can make at most two of the three challenges pass in each repetition, and passes all $t$ with probability at most $(2/3)^t$ against random challenges. With Fiat-Shamir the attacker can also try many commitment sets, and $t$ must cover that search: for $t = 219$, $(2/3)^{219} < 2^{-128}$.

**Zero knowledge (statement).** Given $e$, a simulator picks random seeds for players $e$ and $e + 1$, a random $k_2$ if needed, and random AND outputs for player $e + 1$; it computes view $e$ by Lemma 1 and sets $C_{e+2}$ to a commitment of zeros. In the real protocol the AND outputs of player $e + 1$ contain the tape bit $R_{e+2}$, which comes from the closed seed, so they look uniformly random to anyone who does not know $\mathrm{seed}_{e+2}$; the shares $k_e, k_{e+1}$ are uniform and independent of $k$; and the hiding of the commitment covers $C_{e+2}$. Chase and others (CCS 2017) prove this in full, with the pseudorandom generator and the random oracle.
