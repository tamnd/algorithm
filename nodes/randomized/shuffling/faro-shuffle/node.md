---
tag: 0P38K0
kind: algorithm
slug: faro-shuffle
name: Faro shuffle
aliases:
- perfect shuffle
- in-shuffle
- out-shuffle
- weave shuffle
- perfect riffle shuffle
area: randomized/shuffling
level: intro
summary: The deterministic shuffle that cuts a deck into equal halves and interleaves them one card at a time. Its order is the order of 2 modulo n − 1; eight out-shuffles restore 52 cards.
solves: [card-shuffling]
model: word-ram
complexity:
  vars: {n: the number of cards, even}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {in_place: false, online: false, deterministic: true, recursive: false}
history:
  year: 1957
  people: [Alex Elmsley]
  note: The shuffle is older, from card play and magic. Elmsley named the in- and out-shuffle and found the binary rule that moves the top card to any position.
prereqs: [permutation, multiplicative-order]
see_also: [gilbert-shannon-reeds-model, card-shuffling, permutation-cycles, cycle-leader-permutation, in-place-permutation, symmetric-group, sorting-network, modular-exponentiation]
sources:
  - paper: "Persi Diaconis, Ronald L. Graham and William M. Kantor, The mathematics of perfect shuffles, Advances in Applied Mathematics 4(2), 1983"
    locator: pp. 175 to 196 (the orders of the in- and out-shuffle and the group they generate for each deck size)
  - paper: "Solomon W. Golomb, Permutations by cutting and shuffling, SIAM Review 3(4), 1961"
    locator: pp. 293 to 297 (to be checked)
  - paper: "Harold S. Stone, Parallel processing with the perfect shuffle, IEEE Transactions on Computers C-20(2), 1971"
    locator: pp. 153 to 161 (the perfect shuffle as an interconnection network)
  - paper: "Peiyush Jain, A simple in-place algorithm for in-shuffle, arXiv:0805.1598, 2008"
    locator: the whole note (an in-shuffle in linear time and constant extra space)
---

A faro shuffle, or perfect shuffle, cuts a deck of $n = 2m$ cards into two halves of exactly $m$ cards and interleaves them perfectly, one card from each half in turn. It is **deterministic**: there is no randomness in it at all, which makes it the opposite extreme of the random riffle of the [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/). An **out-shuffle** keeps the top card on top; an **in-shuffle** puts the top card second. Repeated out-shuffles return the deck to its start after $\operatorname{ord}_{n-1}(2)$ shuffles, the [multiplicative order](/multiplicative-order/) of 2 modulo $n - 1$, and in-shuffles after $\operatorname{ord}_{n+1}(2)$. For 52 cards these are 8 and 52.

## In plain words

Cut a deck exactly in half and push the two halves together so that the cards alternate perfectly: one from the left half, one from the right half, and so on. A skilled card handler can do this every time. Since nothing is left to chance, the result is always the same, and a few perfect shuffles in a row can bring the deck back to its first order. Eight perfect shuffles do this for an ordinary deck of fifty-two cards, if the top card stays on top each time.

So this shuffle does not mix a deck at all. It moves cards in a fixed pattern, which magicians use for tricks. It is on these pages to show what a random shuffle is not, and because the same pattern is useful in computers to move data around.

## The problem

The input is a deck $A[0 \ldots n-1]$ with $n = 2m$ even, where $A[0]$ is the top card. The top half is $A[0 \ldots m-1]$ and the bottom half is $A[m \ldots n-1]$. The output is the deck after one perfect interleaving. This is not a solution to the [random permutation](/random-permutation/) problem; it is a fixed permutation that is studied as one move of [card shuffling](/card-shuffling/).

## The algorithm

```pseudo id=main
FARO-SHUFFLE(A, kind)                      ▷ A[0 .. n − 1], n = 2m; A[0] is the top card
L1  m ← n / 2; let B[0 .. n − 1] be a new array
L2  for k ← 0 to m − 1 do
L3      if kind = OUT then B[2k] ← A[k]; B[2k + 1] ← A[m + k]
L4      else B[2k] ← A[m + k]; B[2k + 1] ← A[k]       ▷ IN
L5  return B
```

**Position maps.** With 0-based positions, the out-shuffle moves the card at position $p$ to
$$\text{out}(p) = 2p \bmod (n-1) \text{ for } p \le n - 2, \qquad \text{out}(n-1) = n - 1,$$
so the top and bottom cards stay in place. The in-shuffle moves it to $\text{in}(p) = (2p + 1) \bmod (n+1)$; in 1-based positions $q = p + 1$ this is $q \mapsto 2q \bmod (n+1)$.

## Example

Eight cards $0, 1, \ldots, 7$, with 0 on top. The halves are $0\,1\,2\,3$ and $4\,5\,6\,7$.

| shuffles | out-shuffles | in-shuffles |
|---|---|---|
| 0 | 0 1 2 3 4 5 6 7 | 0 1 2 3 4 5 6 7 |
| 1 | 0 4 1 5 2 6 3 7 | 4 0 5 1 6 2 7 3 |
| 2 | 0 2 4 6 1 3 5 7 | 6 4 2 0 7 5 3 1 |
| 3 | 0 1 2 3 4 5 6 7 | 7 6 5 4 3 2 1 0 |

Three out-shuffles restore 8 cards, since $2^3 = 8 \equiv 1 \pmod 7$. Three in-shuffles reverse them, since $2^3 = 8 \equiv -1 \pmod 9$, and six in-shuffles restore them.

**Orders for some deck sizes.** Each value was computed from the formula and checked against direct simulation in the test file.

| cards $n$ | 2 | 4 | 6 | 8 | 10 | 12 | 20 | 32 | 50 | 52 | 54 | 64 | 100 | 1024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| out-shuffles to restore | 1 | 2 | 4 | 3 | 6 | 10 | 18 | 5 | 21 | 8 | 52 | 6 | 30 | 10 |
| in-shuffles to restore | 2 | 4 | 3 | 6 | 10 | 12 | 6 | 10 | 8 | 52 | 20 | 12 | 100 | 20 |

## Correctness

**Theorem.** For even $n \ge 2$, $k$ out-shuffles restore the deck if and only if $2^k \equiv 1 \pmod{n-1}$, and $k$ in-shuffles restore it if and only if $2^k \equiv 1 \pmod{n+1}$. So the orders are $\operatorname{ord}_{n-1}(2)$ and $\operatorname{ord}_{n+1}(2)$.

The position maps follow from lines L3 and L4: a card from the top half at $p = k$ goes to $2k$ or $2k + 1$, and a card from the bottom half at $p = m + k$ goes to $2k + 1 = 2p - (n-1)$ or $2k = 2p + 1 - (n+1)$. Then $k$ out-shuffles send $p$ to $2^k p \bmod (n-1)$, which is $p$ for all $p$ exactly when $2^k \equiv 1$; the in-shuffle is the same with $n + 1$. The proof file has the details, the rule of Elmsley below, and the reversal by in-shuffles.

## Complexity

One shuffle is $\Theta(n)$ time and $\Theta(n)$ extra space with the array $B$. The in-place versions below use $O(1)$ extra words. The order $\operatorname{ord}_{n \pm 1}(2)$ is at most $n$ and can be found by $O(n)$ multiplications modulo $n \pm 1$, or faster from the factorization of $\varphi(n \pm 1)$ with [modular exponentiation](/modular-exponentiation/).

## Properties

- **Deterministic.** The output is a fixed permutation of the input. A perfect shuffle does not mix: the [total variation distance](/total-variation-distance/) to uniform stays $1 - 1/n!$ after any number of shuffles.
- **Out-shuffle and in-shuffle.** An out-shuffle of $n$ cards is an in-shuffle of the $n - 2$ middle cards, with the top and bottom cards fixed. So the out-shuffle order for $n$ equals the in-shuffle order for $n - 2$; for example both are 8 for 52 and 50 cards.
- **Power-of-two decks.** For $n = 2^k$, the out-shuffle maps the $k$-bit number of a position to its cyclic rotation by one bit to the left, so $k$ out-shuffles restore the deck. The group that the two shuffles generate has $k \cdot 2^k$ elements for $n = 2^k$ (checked by search for $k \le 4$ in the test file).
- **Reversal.** If $\operatorname{ord}_{n+1}(2)$ is even and $n + 1$ is prime, half that many in-shuffles reverse the deck. For 52 cards, 26 in-shuffles reverse it.
- **Elmsley's rule.** To move the top card to position $p$, write $p$ in binary and read it from the most significant bit: do an in-shuffle for each 1 and an out-shuffle for each 0. For example $p = 6 = 110_2$ needs in, in, out.
- **A riffle with one outcome.** In the [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/), an out-shuffle and an in-shuffle are particular riffles, each with probability $2^{-n}$.

## Variants and improvements

- **Odd decks.** For $n = 2m + 1$, cut so that one half has the extra card and interleave; the position maps become multiplication by 2 modulo $n$.
- **In place.** A perfect shuffle can be done in $O(n)$ time with $O(1)$ extra words. Jain's method uses that 2 is a primitive root modulo $3^k$, so for a deck of $3^k - 1$ cards the shuffle has $k$ simple cycles that start at $1, 3, 9, \ldots$, and it splits other sizes into such pieces with rotations. See [cycle-leader permutation](/cycle-leader-permutation/) and [in-place permutation](/in-place-permutation/).
- **Multi-way faro.** Cut into $k$ equal packets and take one card from each in turn; the position map is multiplication by $k$.
- **Inverse.** The inverse of the out-shuffle takes the cards at even positions, in order, as the new top half and the cards at odd positions as the new bottom half. This is the "unshuffle" of the [inverse riffle](/gilbert-shannon-reeds-model/) with a fixed bit pattern.

## When to use it

Use a perfect shuffle when a fixed, known interleaving is wanted: in card magic, in the shuffle-exchange networks of parallel computers (Stone), where it routes the data of the fast Fourier transform and of bitonic [sorting networks](/sorting-network/), and in the "unzip" and "zip" of arrays of pairs. Do not use it to randomize anything; for that see the [Fisher-Yates shuffle](/fisher-yates-shuffle/).

## Pitfalls

- **Taking it as a model of a real riffle.** A real riffle is not perfect, and a model with perfect riffles predicts no mixing at all. The random model is the [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/).
- **Out and in mixed up.** The orders differ much: 8 out-shuffles but 52 in-shuffles restore 52 cards.
- **Off-by-one in the moduli.** The out-shuffle works modulo $n - 1$ on 0-based positions with the last card fixed; the in-shuffle works modulo $n + 1$ on 1-based positions.

## Implementations

## History

The perfect shuffle is old in card play and in the game of faro, from which it took its name. Alex Elmsley named the in- and out-shuffle in the 1950s and found the binary rule to move the top card to any position. Golomb studied the permutations made by cutting and shuffling in 1961. Stone used the perfect shuffle as a network for parallel processing in 1971. Diaconis, Graham and Kantor found in 1983 the group that the two shuffles generate for every deck size.

## References
