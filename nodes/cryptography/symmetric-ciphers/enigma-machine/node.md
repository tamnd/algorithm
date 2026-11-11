---
tag: 4QX9ZT
kind: algorithm
slug: enigma-machine
name: Enigma machine
aliases:
- Enigma
area: cryptography/symmetric-ciphers
level: intro
summary: The German rotor cipher machine of the Second World War. Rotors, a reflector and a plugboard give a new letter permutation at each key press; Rejewski and the bombe broke it.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of letters of the message}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
prereqs: [substitution-cipher, permutation-cycles]
see_also: [vigenere-cipher, known-plaintext-attack, ciphertext-only-attack, kerckhoffs-principle, symmetric-group, exhaustive-key-search, cryptanalysis, cipher-breaking]
sources:
  - url: https://en.wikipedia.org/wiki/Enigma_rotor_details
    title: Wikipedia, Enigma rotor details (wirings and turnover positions of the rotors and reflectors, citing the Crypto Museum)
    locator: the tables of the rotor wirings of the Enigma I (rotors I to V, reflectors A and B), the turnover positions, and the worked example AAAAA to BDZGO
  - paper: "Marian Rejewski, How Polish mathematicians deciphered the Enigma, Annals of the History of Computing 3(3), 1981, pp. 213-234"
    locator: the characteristic of a day (the cycle structure of the products of the permutations for the doubled message key) and the theorem that these products have cycles in pairs of equal length
  - paper: "Gordon Welchman, The Hut Six Story, Breaking the Enigma Codes, McGraw-Hill, 1982"
    locator: the account of the Turing bombe and of the diagonal board that Welchman added to it
  - book: isbn:9780198250807
    title: B. Jack Copeland (editor), The Essential Turing, Oxford University Press, 2004
    locator: the part on Enigma, with Copeland's introduction to the Polish work, the Turing bombe and the diagonal board
  - book: isbn:9780385495318
    title: Simon Singh, The Code Book, Anchor Books, 2000
    locator: Chapter 4, Cracking the Enigma (Rejewski, the bombes and Bletchley Park)
---

The Enigma machine is an electromechanical rotor cipher. The German armed forces used it before and during the Second World War. Each key press moves one or more rotors and then sends a current through a plugboard, three rotors, a reflector, the three rotors again and the plugboard again, to light a lamp. So each letter of a message is encrypted with a different [permutation](/permutation/) of the alphabet, and the sequence of permutations repeats only after 16,900 letters. The reflector makes each permutation its own inverse with no fixed point: the same setting decrypts, and no letter ever encrypts to itself. That second fact, the group structure of the permutations, and the doubled message keys of the 1930s let Marian Rejewski break Enigma in 1932, and later the bombes of Alan Turing and Gordon Welchman break it every day.

## In plain words

A typist presses a key, and a lamp lights under a different letter. Inside, three wheels with crossed wires sit side by side. The current enters through a board of cables that swaps some pairs of letters, goes through the three wheels, hits a fixed end piece that sends it back, goes through the three wheels again by another path, and passes the cable board again.

Before each key press, the right wheel turns by one step, and now and then it pushes the middle wheel, which now and then pushes the left one. So the same key gives a different lamp each time.

Because the current goes in and comes back, the machine works both ways: with the same starting setting, typing the secret text gives the message. And a key can never light its own lamp. Code breakers used that small fact a great deal.

## The problem

Write the alphabet as $\mathbb{Z}_{26}$ and let $\rho(x) = x + 1$ be the shift. The parts of the Army model, the Enigma I, are:

- **Rotors.** Three rotors chosen from five, each with a fixed wiring $W$, a permutation of $\mathbb{Z}_{26}$. A rotor in position $p$ with ring setting $r$ acts as $\rho^{-(p-r)} W \rho^{\,p-r}$, that is $x \mapsto W(x + p - r) - (p - r)$.
- **Reflector.** A fixed permutation $U$ with $U^2 = 1$ and $U(x) \ne x$ for every $x$: 13 swapped pairs.
- **Plugboard.** A permutation $S$ that swaps the letters of each cable, ten cables in the war years, and fixes the other letters.
- **Stepping.** A rule that moves the rotors before each key press (below).

With the rotor maps $R_L, R_M, R_R$ at the current positions, the letter map is
$$E = S\, R_R^{-1} R_M^{-1} R_L^{-1}\, U\, R_L R_M R_R\, S,$$
read from right to left: plugboard, right, middle and left rotor, reflector, and back. The key of a message is the rotor order, the ring settings, the plugboard and the start positions.

**Stepping and the double step.** Each rotor has a notch ring, and there are three pawls. The right pawl always pushes the right rotor. The middle pawl drops into the notch of the right rotor when that notch is under it, that is when the right rotor shows its turnover letter, and then it pushes the middle rotor. The left pawl drops into the notch of the middle rotor when the middle rotor shows its turnover letter, and then it pushes the left rotor. But this pawl also presses on the notch of the middle rotor, so the middle rotor moves with it. As a result, when the right rotor moves the middle rotor onto its turnover letter, the middle rotor moves again at the very next key press, together with the left rotor. The middle rotor thus steps on two key presses in a row. With rotors I, II and III (turnover letters Q, E and V), the windows go

ADU → ADV → AEW → BFX → BFY.

At ADV the right rotor leaves V, and the middle rotor moves from D to E. At AEW the middle rotor shows E, its own turnover letter, so it moves again to F and moves the left rotor from A to B. Because of the double step, the middle rotor stays at its turnover letter for one key press instead of 26. So each turn of the middle rotor takes $25 \cdot 26 = 650$ key presses instead of $26 \cdot 26 = 676$, and the period of the positions is $26 \cdot 650 = 16{,}900$ instead of $26^3 = 17{,}576$.

## The algorithm

```pseudo id=main
ENIGMA(P, rotors, reflector, rings, plugs, start)
L1  pos ← start
L2  for each letter x of P do
L3      pos ← STEP(pos)                     ▷ right always; middle at a turnover; the double step
L4      y ← S(x)                            ▷ plugboard
L5      y ← R_L(R_M(R_R(y)))                ▷ right, middle, left rotor at pos and rings
L6      y ← U(y)                            ▷ reflector
L7      y ← R_R⁻¹(R_M⁻¹(R_L⁻¹(y)))          ▷ back through the rotors
L8      output S(y)
L9  return the output letters
```

The rotors step *before* the current flows, so the first letter is encrypted at the start position plus one step. Decryption is the same procedure with the same settings.

The code uses the standard wirings of the Enigma I, as listed in the Wikipedia article on Enigma rotor details, which takes them from the Crypto Museum: rotor I is EKMFLGDQVZNTOWYHXUSPAIBRCJ with turnover Q, rotor II AJDKSIRUXBLHWTMCQGZNPYFVOE with turnover E, rotor III BDFHJLCPRTXVZNYEIWGAKMUSQO with turnover V, and reflector B is YRUHQSLDPXNGOKMIEBFZCWVJAT. The code also has rotors IV and V and reflector A. No official test vectors for the Enigma exist. The tests use two widely published examples: the example of the Wikipedia article (rotors I, II, III, reflector B, rings AAA, start AAA, no plugs: AAAAA gives BDZGO), and the example of the German instruction manual of 1930, as reproduced on simulator and museum sites, which tests the rings and the plugboard.

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

Take rotors I, II, III from left to right, reflector B, ring settings AAA, no plugs, and start AAA. Press A.

1. **Step.** The right rotor moves, and the windows show AAB.
2. **Right rotor** III at offset 1: the input A enters contact B, which is wired to D, and leaves at C.
3. **Middle rotor** II at offset 0: C goes to D.
4. **Left rotor** I at offset 0: D goes to F.
5. **Reflector** B: F goes to S.
6. **Back through** rotor I: S comes from S. Rotor II: S comes from E. Rotor III at offset 1: E enters as F, which comes from contact C, and leaves at B.

The lamp B lights. Four more presses of A give D, Z, G and O, so AAAAA encrypts to BDZGO. Typing BDZGO from AAA gives AAAAA back.

**Counting the keys.** For the Army Enigma I with three of five rotors, ten plugboard cables, ring settings and start positions:

$$N = \underbrace{5 \cdot 4 \cdot 3}_{\text{rotor orders}} \cdot \underbrace{26^3}_{\text{start}} \cdot \underbrace{26^2}_{\text{rings}} \cdot \underbrace{\frac{26!}{6! \cdot 10! \cdot 2^{10}}}_{\text{plugboard}} = 60 \cdot 17{,}576 \cdot 676 \cdot 150{,}738{,}274{,}937{,}250.$$

The plugboard term counts the ways to choose 20 of the 26 letters and pair them: $\binom{26}{20}$ choices times $20!/(10! \cdot 2^{10})$ pairings, which gives $26!/(6! \cdot 10! \cdot 2^{10}) \approx 1.5 \times 10^{14}$. Only two ring settings count, because the ring of the left rotor has the same effect as a change of its start position: the left rotor has no rotor to its left to push. The product is $N = 107{,}458{,}687{,}327{,}250{,}619{,}360{,}000 \approx 1.07 \times 10^{23} \approx 2^{76.5}$. Without the rings the count is $158{,}962{,}555{,}217{,}826{,}360{,}000 \approx 1.6 \times 10^{20}$, the figure most books quote. Ten cables do not give the largest plugboard term: eleven cables would give $2.06 \times 10^{14}$. The code computes each term, checks the plugboard formula against an enumeration of all pairings for small alphabets, and checks that the left ring is redundant.

**Crib placement.** Encrypt a weather report that contains WETTERBERICHT at offset 16 with some setting. Slide the crib along the 51 letters of ciphertext. At 18 of the 39 offsets some crib letter equals the cipher letter above it, which Enigma can never produce, so those offsets are ruled out at once; the true offset is among the 21 that remain.

## Correctness

Each letter map has the form $E = T^{-1} U T$ with $T = R_L R_M R_R S$, a conjugate of the reflector. A conjugate of a permutation has the same cycle type, so $E$ is, like $U$, a product of 13 disjoint swaps. So $E^2 = 1$, which makes decryption equal to encryption, and $E(x) \ne x$ for every $x$, which is the property the code breakers used. The stepping depends only on the start positions and the number of key presses, never on the text, so the sender and the receiver go through the same maps. The full proof, with Rejewski's theorem on the cycles of his products, is in the proof file below.

## Complexity

Each key press does a constant amount of work: one step and a fixed number of table lookups. So encryption and decryption take $\Theta(n)$ time for $n$ letters and $\Theta(1)$ extra space, with the alphabet size 26 treated as a constant.

| claim | value |
|---|---|
| encryption and decryption | $\Theta(n)$ |
| period of the rotor positions | $26 \cdot 25 \cdot 26 = 16{,}900$ |
| settings of the Army Enigma I, 3 of 5 rotors, 10 cables | $\approx 1.07 \times 10^{23} \approx 2^{76.5}$ |
| without the ring settings | $\approx 1.59 \times 10^{20}$ |
| rotor orders, start positions and rings only | $60 \cdot 26^5 \approx 7.1 \times 10^8 \approx 2^{29.4}$ |

The large number comes mostly from the plugboard, which is only a fixed substitution at both ends. The code breakers split the key: the rotor part, about $7 \times 10^8$ settings, is small enough to search with machines, and the plugboard is found from the surviving settings.

## Properties

- **An involution with no fixed point.** At each position, $E(E(x)) = x$ and $E(x) \ne x$. So the machine decrypts in the same setting, and a crib can never sit over a matching cipher letter.
- **A polyalphabetic substitution.** Each letter uses a different permutation, like a [Vigenère cipher](/vigenere-cipher/) with a very long and complex period.
- **The plugboard conjugates.** Changing the plugboard replaces each $E$ by a conjugate $S E S$. Cycle types of products of these maps do not depend on the plugboard. Rejewski built his catalogue on this fact.
- **Cycles in pairs.** For two letter maps $A$ and $B$, both fixed-point-free involutions, the product $BA$ has its cycles in pairs of equal length.

## Variants and improvements

- **Commercial and early models.** The first machines of the 1920s had no plugboard, and some used a reflector that could be set.
- **Naval Enigma.** The Navy had three more rotors, VI to VIII, with two notches each. The four-rotor M4 of 1942 added a thin fourth rotor next to a thin reflector, which did not step.
- **The indicator procedure.** The procedures for sending the message key changed many times. Until 1940 the Army operators enciphered the message key twice at the start of each message, which gave Rejewski the products $A_4 A_1$, $A_5 A_2$ and $A_6 A_3$.
- **SIGABA.** The American SIGABA was a rotor machine with no reflector, so a letter could encrypt to itself, and it stepped its rotors irregularly. No wartime break of it is known.

## When to use it

Use it to teach rotor machines, the role of permutation group theory in cryptanalysis, known plaintext attacks with cribs, and the gap between a large key space and real security. Never use it to protect data.

## Pitfalls

- **Stepping before the encryption.** The rotors move when the key goes down, before the current flows. Stepping after the letter gives a different and wrong ciphertext.
- **Forgetting the double step.** An odometer model of the stepping agrees with the real machine until the middle rotor reaches its turnover letter, and then all later letters are wrong.
- **Rings and offsets.** The ring setting shifts the wiring against the letter ring and the notch, so the wiring offset is the position minus the ring setting. The notch moves with the letter ring, not with the wiring.
- **Trusting the key count.** $10^{23}$ keys do not make a cipher strong. The plugboard is a fixed substitution, the reflector forbids fixed points, and operators repeated keys and stereotyped texts.

## Implementations

## History

Arthur Scherbius patented a rotor machine in 1918, and the company that sold it called it Enigma. The German Navy adopted a version in 1926 and the Army in 1928; the plugboard came with the Army models. In the Polish Cipher Bureau, Marian Rejewski worked on the Army machine from late 1932. He modelled each letter map as a product of permutations, and he used the doubled message key: the first and fourth letters of each indicator were the same letter under two maps $A_1$ and $A_4$, so many indicators of one day gave the product $A_4 A_1$, and in the same way $A_5 A_2$ and $A_6 A_3$. The cycle lengths of these three products, the *characteristic* of the day, do not depend on the plugboard. With the help of documents that French intelligence had bought from Hans-Thilo Schmidt, he solved the equations for the wiring of the rotors around the end of 1932. Later the Poles catalogued the characteristics of all rotor positions with a machine called the cyclometer, and in 1938 they built the *bomba*. In July 1939 they gave their results and copies of the machine to the French and the British. At Bletchley Park, Alan Turing designed a new bombe that searched for rotor settings consistent with a crib, a guessed piece of plaintext, and it used the fact that no letter encrypts to itself to place the crib. Gordon Welchman added the diagonal board, which made the bombe much stronger. Welchman described this work in The Hut Six Story (1982), and Copeland gives a modern account. The bombes, the operating errors of the German side, and captured key lists let the Allies read much of the Enigma traffic for most of the war.

## References
