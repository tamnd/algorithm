---
tag: HD9NSW
kind: model
slug: neural-probabilistic-language-model
name: Neural probabilistic language model
aliases:
- Bengio language model
- feedforward neural language model
area: natural-language-and-speech/language-modeling
level: core
summary: "Bengio's model that concatenates learned vectors of the previous n - 1 words and feeds them through a hidden layer to a softmax over the vocabulary."
history:
  year: 2003
  people: [Yoshua Bengio, Réjean Ducharme, Pascal Vincent, Christian Jauvin]
  note: A first version appeared at NIPS in 2000. The 2003 journal paper gave the full model, the parallel training and the results on the Brown and AP News corpora.
prereqs: [n-gram-language-model, backpropagation, softmax-regression]
see_also: [recurrent-neural-network-language-model, word-embedding, noise-contrastive-estimation, hierarchical-softmax, importance-sampling, n-gram-language-model, kneser-ney-smoothing, transformer]
sources:
  - paper: "Yoshua Bengio, Réjean Ducharme, Pascal Vincent and Christian Jauvin, A neural probabilistic language model, Journal of Machine Learning Research 3, 2003, pages 1137 to 1155"
    title: Bengio, Ducharme, Vincent and Jauvin 2003
    locator: the model y = b + W x + U tanh(d + H x) with a softmax output, the parameter count, the training by stochastic gradient ascent, the parallel implementation, the results on the Brown and AP News corpora, and Section 5 on speeding up the output with importance sampling
  - paper: "Yoshua Bengio, Réjean Ducharme and Pascal Vincent, A neural probabilistic language model, Advances in Neural Information Processing Systems 13 (NIPS 2000), 2001"
    title: Bengio, Ducharme and Vincent 2001
    locator: the first version of the model
  - paper: "Frederic Morin and Yoshua Bengio, Hierarchical probabilistic neural network language model, Proceedings of AISTATS 2005"
    title: Morin and Bengio 2005
    locator: a tree over the vocabulary that replaces the flat softmax of the model
  - paper: "Andriy Mnih and Yee Whye Teh, A fast and simple algorithm for training neural probabilistic language models, Proceedings of ICML 2012, pages 1751 to 1758, arXiv:1206.6426"
    title: Mnih and Teh 2012
    locator: noise-contrastive training of a log-bilinear neural language model, with the per-context normalizers fixed to 1
---

The neural probabilistic language model of Bengio, Ducharme, Vincent and Jauvin is the first widely used neural network language model. Like an [n-gram model](/n-gram-language-model/) it predicts the next word from the previous $n - 1$ words only. But instead of counting each n-gram, it maps each word to a learned real vector of $m$ dimensions, joins the $n - 1$ vectors, passes them through a hidden layer with $\tanh$ units, and gives a [softmax](/softmax-regression/) over the whole vocabulary. Words that are used alike get similar vectors, so what the model learns about one sequence carries over to sequences with similar words that it never saw. This answers the curse of dimensionality that the counts of an n-gram model suffer from. The vectors are the [word embeddings](/word-embedding/) that later models made a field of their own.

## The machine

**Parameters.** For a vocabulary $V$, an order $n$, a vector size $m$ and $h$ hidden units:

- $C$, a $|V| \times m$ table that holds the vector $C(w)$ of each word;
- $H$ ($h \times (n-1)m$) and $d$ ($h$), the hidden layer;
- $U$ ($|V| \times h$), the output weights of the hidden layer;
- $W$ ($|V| \times (n-1)m$), optional direct connections from the word vectors to the output;
- $b$ ($|V|$), the output biases.

**The prediction.** For the context $w_{t-n+1}, \ldots, w_{t-1}$:

$$x = \big(C(w_{t-1}), C(w_{t-2}), \ldots, C(w_{t-n+1})\big), \qquad y = b + W x + U \tanh(d + H x),$$

$$P(w_t = i \mid w_{t-n+1}, \ldots, w_{t-1}) = \frac{e^{y_i}}{\sum_{j \in V} e^{y_j}}.$$

The vector $x$ has $(n-1)m$ entries. With $W = 0$ there are no direct connections.

**Size.** The parameter count is $|V|(1 + n m + h) + h(1 + (n-1)m)$: $b$, $W$, $U$ and $C$ give $|V| + |V|(n-1)m + |V| h + |V| m$, and $d$ and $H$ give $h + h(n-1)m$. It grows linearly in $|V|$ and in $n$, while an n-gram model may need a number for each of up to $|V|^n$ sequences. For example, $|V| = 10{,}000$, $n = 4$, $m = 60$ and $h = 100$ give $10{,}000 \cdot 341 + 100 \cdot 181 = 3{,}428{,}100$ parameters.

**Training.** All parameters, the word vectors included, maximize the log-likelihood of the training text plus a weight decay penalty, by stochastic gradient ascent with [backpropagation](/backpropagation/). Bengio and colleagues used a learning rate $\varepsilon_t = \varepsilon_0 / (1 + r t)$ with $\varepsilon_0 = 10^{-3}$ and $r = 10^{-8}$, and a [weight decay](/weight-decay/) of $10^{-4}$ on Brown and $10^{-5}$ on AP News. For their best results they mixed the network with an interpolated trigram model.

## What it counts

The model is measured by its [perplexity](/perplexity/) on test text. The cost of one prediction is the number of multiply-adds:

- the hidden layer, $(n-1) m h$;
- the output, $|V|(h + (n-1)m)$ with direct connections, $|V| h$ without;
- the softmax, $O(|V|)$.

The output dominates by far. In the example above it is $10{,}000 \cdot 280 = 2{,}800{,}000$ multiply-adds against $18{,}000$ for the hidden layer. Training has the same cost per word for the gradient, since every output weight gets a gradient through the normalizer. This is why the methods that followed attack the output: [importance sampling](/importance-sampling/) (Bengio and Senécal, discussed in Section 5 of the paper), the [hierarchical softmax](/hierarchical-softmax/) of Morin and Bengio, and [noise-contrastive estimation](/noise-contrastive-estimation/) (Mnih and Teh).

## Relation to other models

- **n-gram models.** Both models make the same Markov assumption of order $n - 1$. The n-gram model shares nothing between contexts except through backoff to shorter contexts; the neural model shares through the word vectors and the hidden layer.
- **Class-based models.** A class n-gram model, such as one built on [Brown clustering](/brown-clustering/), shares statistics between the words of one hard class. The word vectors are a soft, learned and many-dimensional version of the same idea.
- **Softmax regression.** Without the hidden layer, with only $W$ and $b$, the model is [softmax regression](/softmax-regression/) on the concatenated word vectors, with the vectors learned too.
- **Maximum entropy models.** A [maximum entropy language model](/maximum-entropy-language-model/) has the same softmax output over fixed hand-made features; the neural model learns its features.
- **Recurrent models.** A [recurrent neural network language model](/recurrent-neural-network-language-model/) replaces the fixed window of $n - 1$ words with a state that summarizes the whole history.
- **Word embedding models.** The [skip-gram](/skip-gram-model/) and [continuous bag of words](/continuous-bag-of-words/) models drop the hidden layer and the order of the words to learn vectors fast; they keep the idea of the table $C$.
- **Transformers.** A [transformer](/transformer/) language model also starts from a table of word vectors and ends with a softmax over the vocabulary, but it lets every position use all the earlier ones through attention.

## Known results in the model

- **Brown corpus.** With about 800,000 training words, 200,000 validation words and 181,041 test words, and $|V| = 16{,}383$, the best network, mixed with an interpolated trigram, reached a test perplexity of 252. The best n-gram model, a class-based model, had 312, and a [Kneser-Ney](/kneser-ney-smoothing/) backoff model had 321. The paper reports this as a difference of about 24 percent.
- **AP News.** With about 14 million training words and $|V| = 17{,}964$, the network reached 109 against 117 for the best n-gram model, a difference of about 8 percent. Five epochs took more than three weeks on 40 CPUs.
- **Direct connections.** Without the direct connections $W$, training took twice as many epochs (20 instead of 10), and reached a slightly lower perplexity.
- **Similar words.** The model generalizes because similar words get nearby vectors, and a change of one word for a similar word changes the probability little. The paper gives this as the reason for the gains.
- **The output bottleneck.** The softmax over the vocabulary is the main cost of both prediction and training, linear in $|V|$. Sampling methods cut the cost of training, and a tree cuts the cost of the probability of one word to $O(h \log |V|)$.

## References
