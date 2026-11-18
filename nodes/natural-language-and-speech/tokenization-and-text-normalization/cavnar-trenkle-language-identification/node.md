---
tag: 2S4GCR
kind: algorithm
slug: cavnar-trenkle-language-identification
name: Cavnar-Trenkle n-gram text categorization
aliases:
- out-of-place measure
- character n-gram rank profiles
area: natural-language-and-speech/tokenization-and-text-normalization
level: core
summary: Identify the language of a text by comparing the rank order of its most frequent character n-grams with stored profiles under the out-of-place distance.
solves: [language-identification]
model: word-ram
complexity:
  vars: {n: the number of characters of the input text, G: the number of distinct n-grams of the input, L: the profile length, k: the number of languages}
  time: {profile: O(n + G log G), compare: O(k L)}
  space: {extra: O(G + k L)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1994
  people: [William B. Cavnar, John M. Trenkle]
  note: Cavnar and Trenkle presented the method at SDAIR-94 for language and subject classification of Usenet articles.
prereqs: [language-identification]
see_also: [spearman-rank-correlation, naive-bayes-classifier, n-gram-language-model, top-k-selection, zipfs-law, k-nearest-neighbors, multiclass-classification, shingling]
sources:
  - paper: "William B. Cavnar and John M. Trenkle, N-gram-based text categorization, Proceedings of the Third Annual Symposium on Document Analysis and Information Retrieval (SDAIR-94), Las Vegas, 1994, pages 161 to 175"
    title: William B. Cavnar and John M. Trenkle, N-gram-based text categorization, SDAIR-94
    locator: Section 2.0 (the padded n-grams), Section 3.1 (the profiles and the remarks on rank 300), Section 3.2 and Figure 3 (the out-of-place measure), Section 4 and Table 2 (the language test on 3478 articles)
  - paper: doi:10.1613/jair.1.11675
    title: Tommi Jauhiainen, Marco Lui, Marcos Zampieri, Timothy Baldwin and Krister Lindén, Automatic language identification in texts, a survey, Journal of Artificial Intelligence Research 65, 2019
    locator: pages 675 to 782 (the section on the out-of-place method and its relation to rank statistics)
  - paper: "Timothy Baldwin and Marco Lui, Language identification, the long and the short of the matter, NAACL HLT 2010, Los Angeles, pages 229 to 237"
    title: Timothy Baldwin and Marco Lui, Language identification, the long and the short of the matter, NAACL HLT 2010
    locator: the comparison of the out-of-place method with other classifiers on short and long documents
---

The Cavnar-Trenkle method identifies the language of a text by its most frequent character n-grams. It builds a ranked list, a profile, of the most frequent n-grams of length 1 to 5 for each language and for the input, and it returns the language whose profile is closest under the out-of-place distance, a sum of rank differences. It is one algorithm for the [language identification](/language-identification/) problem, which is the task of choosing the language of a text; the problem page lists other methods, such as [naive Bayes](/naive-bayes-classifier/) over n-grams. The same procedure also sorts texts by subject, which is why the paper calls it text categorization.

## In plain words

Each language has letter groups that it uses a lot. English has "th" and "the", German has "sch" and "en", French has "es" and "le". Count the short letter groups in a sample of each language, and keep a list of the most common ones, from the most common down. Do the same for the text you want to identify.

Then compare the lists. For each letter group in the list of the text, see how far its place is from its place in the list of a language. Add up these distances. A group that the language list does not have adds a fixed large amount. The language with the smallest total wins.

The method only looks at the order of the lists, not at the counts, so a short text and a long sample can be compared directly.

## The problem

The input is a text $x$ and, for each of $k$ languages $c$, a profile $C[c]$ built from training text in that language. The output is one language. A token is a maximal run of letters and apostrophes; digits, punctuation and white space separate tokens (Section 3.1 of the paper). For $n \ge 2$, a token $w$ is padded with one blank in front and $n - 1$ blanks after it, written $\_$, so the token TEXT gives the bigrams $\_T$, TE, EX, XT, $T\_$ and the trigrams $\_TE$, TEX, EXT, $XT\_$, $T\_\_$, as in Section 2.0 of the paper. A token of $k$ characters gives $k + 1$ n-grams of each length $n \ge 2$. For $n = 1$ this page uses the letters alone.

The profile $P_L(x)$ is the list of the $L$ most frequent n-grams of $x$, from the most frequent down, with ranks $0, 1, 2, \ldots$. The paper gives no rule for equal counts; this page breaks ties by the n-gram string in code point order, so that the profile is a function of the text. The out-of-place distance of a document profile $P$ from a category profile $Q$ is

$$\operatorname{oop}(P, Q) = \sum_{r} \begin{cases} |r - \operatorname{rank}_Q(P[r])| & \text{if } P[r] \text{ is in } Q, \\ L & \text{otherwise.} \end{cases}$$

The paper says that a missing n-gram takes "some maximum out-of-place value" and gives no number. This page uses $L$, which is at least as large as any rank difference between two profiles of length $L$.

## The algorithm

```pseudo id=main
CT-CLASSIFY(x, C, L)                       ▷ C maps each language to a profile of length at most L
L1  P ← PROFILE(x, L)
L2  best ← none, d* ← ∞
L3  for each language c of C, in sorted order do
L4      d ← 0
L5      for r ← 0 to |P| - 1 do
L6          if P[r] has the rank r' in C[c] then d ← d + |r - r'|
L7          else d ← d + L                 ▷ the maximum out-of-place penalty
L8      if d < d* then best ← c, d* ← d
L9  return best

PROFILE(x, L)
L10 count ← empty map
L11 for each token w of x do
L12     for n ← 1 to 5 do
L13         u ← w if n = 1, else "_" + w + "_" repeated n - 1 times
L14         for each window g of length n in u do count[g] ← count[g] + 1
L15 sort the keys of count by decreasing count, and equal counts by the string
L16 return the first L keys
```

Training is PROFILE on the sample text of each language. Line L6 needs the rank of an n-gram in a category profile, so each category profile is stored with a hash map from n-gram to rank. Line L8 uses a strict comparison, so on equal distances the first language in sorted order wins.

## Example

Three training texts of about 150 characters each, all lower case:
- en: "the cat and the dog are in the house. the children play with the ball in the garden. this is the end of the story and the start of the next one."
- fr: "le chat et le chien sont dans la maison. les enfants jouent avec la balle dans le jardin. ceci est la fin de l histoire et le debut de la suivante."
- de: "die katze und der hund sind in dem haus. die kinder spielen mit dem ball in dem garten. das ist das ende der geschichte und der anfang der naechsten."

With $L = 6$, the profiles are the following, with the counts in brackets:
- en: e (17), t (17), h (14), e_ (13), e__ (13), e___ (13)
- fr: e (19), a (13), l (12), n (11), _l (10), t (10)
- de: e (20), d (17), n (14), _d (11), i (10), a (9)

In the English profile, e and t have the same count and e comes first by the tie rule. The input "the house" has the profile e, e_, e__, e___, e____, h, each with count 2. The trailing blanks come from the padding: both words end in e, and both contain h. The table gives the cost of each n-gram for each language.

| $r$ | n-gram | rank in en | cost en | cost fr | cost de |
|---|---|---|---|---|---|
| 0 | e | 0 | 0 | 0 | 0 |
| 1 | e_ | 3 | 2 | 6 | 6 |
| 2 | e__ | 4 | 2 | 6 | 6 |
| 3 | e___ | 5 | 2 | 6 | 6 |
| 4 | e____ | missing | 6 | 6 | 6 |
| 5 | h | 2 | 3 | 6 | 6 |
| | sum | | 15 | 30 | 30 |

So CT-CLASSIFY returns en. With the default $L = 300$, the same three profiles also give the right language for "the end of the day", "in the garden", "la fin du jour", "dans la maison", "das ende des tages", "und der hund" and "in dem garten". The tests of the implementation check all these numbers.

## Correctness

The proof in proofs/correctness.md shows that lines L10 to L14 count each padded n-gram once for each window, that lines L15 and L16 return the first $L$ n-grams in a strict total order, so the profile is well defined, and that lines L4 to L7 compute the sum in the definition. An induction over the loop of line L3 shows that best is the first language in sorted order with the least distance. This is a statement about the rule, not about the true language: the method is a heuristic classifier, and its accuracy is a measurement.

## Complexity

- **Profile.** A token of $k$ characters gives at most $5(k + 1)$ windows, so lines L11 to L14 make $O(n)$ map updates for a text of $n$ characters, and the map holds $G \le 5n$ keys. The sort of line L15 takes $O(G \log G)$ comparisons; a selection of the top $L$ keys with a heap ([top-k selection](/top-k-selection/)) takes $O(G \log L)$.
- **Comparison.** With a rank map per language, each of the $k$ languages costs $O(L)$, so lines L3 to L8 take $O(k L)$ time.
- **Space.** $O(G)$ for the counts of the input and $O(k L)$ for the stored profiles. With $L = 300$ and 8 languages, the model is 2400 n-grams.

## Properties

- **Rank based.** Only the order of the profile matters, not the counts. This makes a short input comparable with a long training text, but it throws away how much more frequent one n-gram is than the next.
- **Not a metric.** $\operatorname{oop}(P, Q) = 0$ exactly when $P$ is a prefix of $Q$, and $\operatorname{oop}(P, Q)$ and $\operatorname{oop}(Q, P)$ can differ. Without missing n-grams, the sum of $|r - r'|$ is Spearman's footrule between the two rankings, which is related to [Spearman's rank correlation](/spearman-rank-correlation/); Jauhiainen et al. (2019) make the same link.
- **Bounded.** With profiles of length $L$, the distance lies between 0 and $L^2$.
- **Robust to small errors.** A typing error changes a few n-grams of one word, so it moves a few terms of the sum. The paper names this tolerance as a design goal.
- **Deterministic.** With the tie rules of lines L8 and L15, the result is a function of the input and the training texts.

## Variants and improvements

- **Probabilistic models.** A [naive Bayes classifier](/naive-bayes-classifier/) or a character [n-gram language model](/n-gram-language-model/) per language uses the counts, not only the ranks. Tools such as langid.py (Lui and Baldwin 2012) use a multinomial naive Bayes model over selected byte n-grams.
- **Other distances.** The survey of Jauhiainen et al. (2019) lists many other distances and classifiers that replace the out-of-place measure, for example the [cosine similarity](/cosine-similarity/) of n-gram count vectors.
- **Profile length.** Cavnar and Trenkle tested profiles of 100, 200, 300 and 400 n-grams. In their test the accuracy rose from 100 to 300 and changed little from 300 to 400. They write that the top 300 or so n-grams depend mostly on the language and that there is nothing special about rank 300 itself. So 300 is a rule of thumb from their data, not a derived constant.
- **Case folding and normalization.** The paper does not say whether it folds case. Folding both the training text and the input, and normalizing the Unicode form, removes differences that say nothing about the language.

## When to use it

Use it as a small, transparent baseline: it needs a few kilobytes of training text per language, no tuning beyond $L$, and its decision can be explained with a table like the one above. For short inputs, such as a tweet or a search query, the input has only a few dozen distinct n-grams, so the decision rests on little evidence. Baldwin and Lui (2010) study how the accuracy of several methods, this one included, changes with the length of the document and the number of languages. For a production system, compare it on your own data with a probabilistic model.

## Pitfalls

- **A profile that is too short.** With the training texts of the example and $L = 8$, the input "the end of the day" gets the distances 46 (en), 40 (fr) and 52 (de), so line L9 returns fr. The test of the implementation shows that $L$ from 4 to 10 gives a wrong language, and $L$ from 11 to 20 gives en. The fix is a larger $L$ in lines L1 and L16, not a change of the penalty.
- **A penalty that is too small.** If line L7 adds less than the largest possible rank difference, a profile that shares few n-grams with the input can beat a profile that shares many n-grams at slightly different ranks. Use a penalty of at least $L$.
- **No tie rule.** Many n-grams have the same count, as in the example, where all six n-grams of "the house" have count 2. Without the tie rule of line L15, the profile, and so the answer, depends on the order of a hash map.
- **Different preprocessing for training and input.** If line L11 tokenizes or folds case one way at training time and another way at test time, the profiles do not match. Use the same PROFILE for both.
- **Closely related languages.** Languages that share most frequent n-grams, such as Danish and Norwegian Bokmål, or Croatian and Serbian in Latin script, are hard for every method, because their profiles share most of their top ranks. Train on texts that show the differences, and check the confusion between such pairs on held-out data.

## Implementations

## History

Cavnar and Trenkle presented the method at the Third Annual Symposium on Document Analysis and Information Retrieval in 1994. Their language test used 3478 Usenet articles in 8 languages (English, Portuguese, French, German, Italian, Spanish, Dutch and Polish), with training samples of 20K to 120K bytes. With profiles of 300 n-grams, they report 98.6% correct classification for articles of at most 300 bytes and 99.8% for longer articles; with 100 n-grams, the numbers were 92.9% and 97.2% (Table 2). A second test sorted articles from computer newsgroups by subject, with up to 80% correct. Later work replaced the rank distance with probabilistic models, but the method remains a common reference point in language identification surveys.

## References
