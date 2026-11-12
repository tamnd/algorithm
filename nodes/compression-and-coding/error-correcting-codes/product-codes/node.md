---
tag: XYNQ39
kind: definition
slug: product-codes
name: Product codes
aliases:
- direct product codes
- product code
- Elias product code
- tensor product code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "The code of n1 x n2 arrays whose columns lie in C1 and whose rows lie in C2. It has parameters [n1 n2, k1 k2, d1 d2] and is decoded row by row and column by column."
history:
  year: 1954
  people: [Peter Elias]
  note: Elias defined product codes in 1954 and iterated them with Hamming codes of growing length to get the first explicit codes with positive rate and an error probability that goes to 0 on the binary symmetric channel.
prereqs: [linear-code, minimum-distance, generator-matrix]
see_also: [concatenated-codes, interleaving, turbo-code, burst-errors, reed-solomon-code, hamming-code, kronecker-product, syndrome-decoding]
sources:
  - paper: doi:10.1109/TIT.1954.1057464
    title: P. Elias, Error-free coding, Transactions of the IRE Professional Group on Information Theory 4(4), 1954
    locator: pp. 29 to 37 (the product of two codes, its minimum distance, and the iterated product of Hamming codes)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 18, Section 2 (direct product codes, their minimum distance, and their decoding)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 4.7 (product codes, the encoding of rows and columns, and the decoding of rows then columns)
---

A product code arranges symbols in a rectangle. Each column is a codeword of a code $C_1$ and each row is a codeword of a code $C_2$. If $C_1$ is $[n_1, k_1, d_1]$ and $C_2$ is $[n_2, k_2, d_2]$, the product $C_1 \otimes C_2$ is a [linear code](/linear-code/) with parameters $[n_1 n_2, k_1 k_2, d_1 d_2]$. The [minimum distance](/minimum-distance/) multiplies, so short codes with simple decoders build a long code with a large distance. A decoder can work on rows and columns one at a time. The simple pass of columns then rows corrects only about a quarter of the distance, and iterated and soft decoders do much better. Elias introduced product codes in 1954, and products of [Reed-Solomon codes](/reed-solomon-code/) protect data on optical discs.

## Definition

Let $C_1 \subseteq \mathrm{GF}(q)^{n_1}$ and $C_2 \subseteq \mathrm{GF}(q)^{n_2}$ be linear codes with parameters $[n_1, k_1, d_1]$ and $[n_2, k_2, d_2]$. The **product code** is

$$C_1 \otimes C_2 = \{\, X \in \mathrm{GF}(q)^{n_1 \times n_2} : \text{every column of } X \text{ is in } C_1, \text{ every row of } X \text{ is in } C_2 \,\}.$$

**Generator matrix.** If $G_1$ ($k_1 \times n_1$) and $G_2$ ($k_2 \times n_2$) are [generator matrices](/generator-matrix/), then

$$C_1 \otimes C_2 = \{\, G_1^{\mathsf T} M G_2 : M \in \mathrm{GF}(q)^{k_1 \times k_2} \,\}.$$

Read row by row, the array $G_1^{\mathsf T} M G_2$ is the message $M$ times the [Kronecker product](/kronecker-product/) $G_1 \otimes G_2$, so the code is the tensor product of $C_1$ and $C_2$.

**Parameters.**

$$n = n_1 n_2, \qquad k = k_1 k_2, \qquad d = d_1 d_2, \qquad R = R_1 R_2, \qquad \delta = \delta_1 \delta_2 .$$

*Dimension.* The map $M \mapsto G_1^{\mathsf T} M G_2$ is one to one, because $G_1$ and $G_2$ have full rank. Each array of this form has columns in the span of the rows of $G_1$ and rows in the span of the rows of $G_2$. Conversely, an array with all rows in $C_2$ is $Y G_2$ for some $n_1 \times k_2$ matrix $Y$. The columns of $Y$ are linear combinations of the columns of the array at an information set of $C_2$, so they lie in $C_1$, and $Y = G_1^{\mathsf T} M$.

*Distance.* Let $X \ne 0$ be a codeword. Some row of $X$ is nonzero, and it lies in $C_2$, so it has at least $d_2$ nonzero entries. So at least $d_2$ columns of $X$ are nonzero. Each lies in $C_1$ and has at least $d_1$ nonzero entries. So $\mathrm{wt}(X) \ge d_1 d_2$. If $a \in C_1$ and $b \in C_2$ have weights $d_1$ and $d_2$, the array $a^{\mathsf T} b$ is a codeword of weight exactly $d_1 d_2$.

### Encoding

Put the $k_1 \times k_2$ message in a block. Encode each of the $k_1$ rows with $C_2$, then each of the $n_2$ columns with $C_1$. With systematic encoders, the message sits in the top left corner, the row checks to its right, the column checks below it, and the *checks on checks* in the bottom right corner. Encoding the columns first and then the rows gives the same array, because both orders give $G_1^{\mathsf T} M G_2$. So the bottom right block is consistent: its rows are codewords of $C_2$ and its columns are codewords of $C_1$.

### Row and column decoding

Let $t_i = \lfloor (d_i - 1)/2 \rfloor$, and let each component decoder correct up to $t_i$ errors. The simple decoder decodes every column with $C_1$, then every row with $C_2$.

**What it guarantees.** Every pattern of at most $(t_1 + 1)(t_2 + 1) - 1$ errors is corrected. A column with at most $t_1$ errors is decoded correctly. So after the first pass, only columns that held at least $t_1 + 1$ errors can be wrong, and there are at most $t_2$ of them. Each row then has errors only in these columns, at most $t_2$ errors, and the row pass removes them.

**Its limit.** The code itself can correct $\lfloor (d_1 d_2 - 1)/2 \rfloor$ errors. For odd $d_1, d_2$ the simple decoder reaches $(d_1 + 1)(d_2 + 1)/4 - 1$, about half of that. A pattern of $(t_1 + 1)(t_2 + 1)$ errors on a rectangle of $t_1 + 1$ rows and $t_2 + 1$ columns can defeat it: each of these columns has too many errors and may be decoded to a wrong codeword, which adds errors in new rows, and then each row has too many errors.

**Better decoders, in outline.** Several methods correct more of the patterns within the full radius:

- *Iterate.* Repeat the column pass and the row pass until the array stops changing or a fixed number of rounds ends.
- *Pass erasures and weights.* Let the column decoder mark the columns it cannot decode, or give each column a weight from the number of errors it corrected, and decode the rows with errors and erasures. Reddy and Robinson (1972) showed that a decoder of this kind corrects every pattern up to the full radius $\lfloor (d_1 d_2 - 1)/2 \rfloor$.
- *Soft in, soft out.* Give each component decoder the reliabilities of the symbols and let it return new reliabilities, and iterate. This is the turbo product code, or block turbo code, of Pyndiah (1998), which comes close to capacity with short BCH and Hamming components. It uses the same exchange of extrinsic information as [turbo codes](/turbo-code/).

### Bursts

If the array is sent row by row, a burst of up to $n_2 t_1$ consecutive errors hits each column at most $t_1$ times, so the column pass corrects it. This is the [interleaving](/interleaving/) of $n_2$ codewords of $C_1$ with depth $n_2$, and a product code adds the row code on top. So product codes handle both random errors and [bursts](/burst-errors/).

## Examples and non-examples

**Two parity checks.** The product of the $[3, 2, 2]$ even weight code with itself is a $[9, 4, 4]$ code: a $2 \times 2$ message with one parity bit per row, one per column, and one check on checks. A single error is located by the one failed row and the one failed column.

**Hamming times Hamming.** The product of two $[7, 4, 3]$ [Hamming codes](/hamming-code/) is a $[49, 16, 9]$ code. The tests list all $2^{16}$ codewords and find minimum weight 9. With $t_1 = t_2 = 1$, the row and column decoder corrects every pattern of at most $(1 + 1)(1 + 1) - 1 = 3$ errors. The tests check all $1 + 49 + 1176 + 18424 = 19650$ such patterns.

**A pattern the simple decoder fails on.** Send the zero array and flip the four entries in rows 0, 1 and columns 0, 1. The code can correct 4 errors, since $d = 9$, and a search over all codewords returns the zero array. The column pass sees two errors in columns 0 and 1. The Hamming code is perfect, so it decodes each of them to the weight 3 codeword $1101000$ and adds an error in row 3. Now rows 0, 1 and 3 equal $1100000$, and the row pass decodes each of them to $1101000$. The output is the codeword $a^{\mathsf T} a$ with $a = 1101000$, of weight 9 and at distance 5 from the received word.

**Unequal components.** With $C_1$ the $[7, 4, 3]$ Hamming code and $C_2$ the $[5, 1, 5]$ repetition code, the product is $[35, 4, 15]$, and the simple decoder corrects every pattern of at most $(1 + 1)(2 + 1) - 1 = 5$ errors.

**Optical discs.** The DVD format uses a product of two Reed-Solomon codes over GF(256), with the outer code on columns and the inner code on rows, decoded as rows and then columns with erasures.

**Non-example: the dual of a product.** The dual of $C_1 \otimes C_2$ is not $C_1^\perp \otimes C_2^\perp$. That code has dimension $(n_1 - k_1)(n_2 - k_2)$, while the dual has dimension $n_1 n_2 - k_1 k_2$. The dual is the sum $C_1^\perp \otimes \mathrm{GF}(q)^{n_2} + \mathrm{GF}(q)^{n_1} \otimes C_2^\perp$ of the arrays whose columns are in $C_1^\perp$ and the arrays whose rows are in $C_2^\perp$.

**Non-example: a good family by products alone.** Repeated products of one fixed code have rate $R^j$ and relative distance $\delta^j$, which both go to 0. Products alone do not give asymptotically good codes. Elias used products of Hamming codes of growing lengths, so the rate stays positive, and showed that the probability of a decoding error still goes to 0 on the binary symmetric channel. The relative distance of these codes still goes to 0.

## Related definitions

- [Concatenated codes](/concatenated-codes/): an outer code over a large alphabet whose symbols are encoded by an inner code. A product code with the outer code on columns over symbols of $k_2$ bits is a close relative.
- [Interleaving](/interleaving/): the column code of a product code read row by row is an interleaved code.
- [Turbo code](/turbo-code/): parallel concatenation with iterative soft decoding, the same idea as block turbo codes.
- [Reed-Solomon code](/reed-solomon-code/) and [Hamming code](/hamming-code/): the most common component codes.
- [Kronecker product](/kronecker-product/): the generator matrix of the product is $G_1 \otimes G_2$.
- [Syndrome decoding](/syndrome-decoding/): a common decoder for short component codes.

## References
