from math import inf
from matplotlib.lines import lineStyles
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from numpy import Inf
from numpy.core.shape_base import block


LINES = ['-', ':', '--']

def main():
    string_by_author = dict()
    string_by_author['doyle'] = text_to_string('hound.txt')
    string_by_author['wells'] = text_to_string('war.txt')
    string_by_author['unknown'] = text_to_string('lost.txt')

    print(string_by_author['doyle'][:300])

    words_by_author = make_word_dict(string_by_author)
    len_shortest_corpus = find_shortest_corpus(words_by_author)
    word_length_test(words_by_author, len_shortest_corpus)
    stopwords_test(words_by_author, len_shortest_corpus)
    parts_of_speech_test(words_by_author, len_shortest_corpus)
    vocab_test(words_by_author)
    jaccard_test(words_by_author, len_shortest_corpus)



def text_to_string(filename):
    """Read a text file and return a string."""

    with open(filename, encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def make_word_dict(string_by_author):
    """Read dictionary of tokenized words by corpus by author."""
    words_by_author = dict()
    for author in string_by_author:
        tokens = nltk.word_tokenize(string_by_author[author])
        words_by_author[author] = ([token.lower() for token in tokens if token.isalpha()])

    return words_by_author

def find_shortest_corpus(words_by_author):
    """Returns shortest length corpus."""
    shortest_corpus = Inf
    for author in words_by_author:
        if len(words_by_author[author]) < shortest_corpus:
            shortest_corpus = len(words_by_author[author])
    return shortest_corpus

def word_length_test(words_by_author, len_shortest_corpus):
    """Plot word length freq by author, truncated to shortest corpus length."""
    by_author_length_freq_dist = dict()
    plt.figure(1)
    plt.ion()

    for i, author in enumerate(words_by_author):
        word_lengths = [len(word) for word in words_by_author[author][:len_shortest_corpus]]
        by_author_length_freq_dist[author] = nltk.FreqDist(word_lengths)
        by_author_length_freq_dist[author].plot(15, linestyle=LINES[i], label=author, title='Word Length')

    plt.legend()
    #plt.show(block=True)

def stopwords_test(words_by_author, len_shortest_corpus):
    """Plot stopwords freq by author , truncated to shortest corpus length."""

    stopwords_by_author_freq_dist = dict()
    plt.figure(2)
    stop_words = set(stopwords.words('english'))

    for i, author in enumerate(words_by_author):
        stopwords_by_author = [word for word in words_by_author[author][:len_shortest_corpus] if word in stop_words]
        stopwords_by_author_freq_dist[author] = nltk.FreqDist(stopwords_by_author)
        stopwords_by_author_freq_dist[author].plot(50, label=author, linestyle=LINES[i], title='50 Most Common Stopwords')

    plt.legend()
    #plt.show(block=True)

def parts_of_speech_test(words_by_author, len_shortest_corpus):
    """Plot author use of parts-of-speech such as nouns, verbs, adverbs."""

    by_author_pos_freq_dist = dict()
    plt.figure(3)
    for i, author in enumerate(words_by_author):
        pos_by_author = [pos[1] for pos in nltk.pos_tag(words_by_author[author])[:len_shortest_corpus]]
        by_author_pos_freq_dist[author] = nltk.FreqDist(pos_by_author)
        by_author_pos_freq_dist[author].plot(35, label=author, linestyle=LINES[i], title='Part of Speech')

    plt.legend()
    #plt.show(block=True)

def vocab_test(words_by_author):
    """Compare author vocabularies using the chi-squared statistical test."""

    chisquared_by_author = dict()
    for author in words_by_author:
        if author != 'unknown':
            combined_corpus = (words_by_author[author] + words_by_author['unknown'])
            author_proportion = (len(words_by_author[author])/len(combined_corpus))
            combine_freq_dist = nltk.FreqDist(combined_corpus)
            most_common_words = list(combine_freq_dist.most_common(1000))
            chisquared = 0
            for word, combined_count in most_common_words:
                observed_count_author = words_by_author[author].count(word)
                expected_count_author = combined_count * author_proportion
                chisquared += ((observed_count_author - expected_count_author)**2 / expected_count_author)
                chisquared_by_author[author] = chisquared
            print(f'Chi-squared for {author} = {chisquared:.1f}')

    most_likely_author = min(chisquared_by_author, key=chisquared_by_author.get)
    print(f'Most-likely author by vocbulary is {most_likely_author}')

def jaccard_test(words_by_author, len_shortest_corpus):
    """Calculate Jaccard similarity of each known corpus to unkown corpus."""

    jaccard_by_author = dict()
    unique_words_unkown = set(words_by_author['unknown'][:len_shortest_corpus])
    authors = [author for author in words_by_author if author != 'unknown']
    for author in authors:
        unique_words_author = set(words_by_author[author][:len_shortest_corpus])
        shared_words = unique_words_author.intersection(unique_words_unkown)
        jaccard_sim = (float(len(shared_words)) / (len(unique_words_author) + len(unique_words_unkown) - len(shared_words)))
        jaccard_by_author[author] = jaccard_sim
        print(f'Jaccard similarity for {author} = {jaccard_sim}')
    most_likely_author = max(jaccard_by_author, key=jaccard_by_author.get)
    print(f'Most-likely author by similarity is {most_likely_author}')

if __name__ == '__main__':
    main()
