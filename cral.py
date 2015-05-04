import string
import matplotlib.pyplot as plt

#frequencies of letters in english texts
hist_eng = [.08167, .01492, .02782, .04253, .012702, .02228, .02015, .06094,
            .06966, .00153, .00772, .04025, .02406, .06749, .07507, .01929,
            .00095, .05987, .06327, .09056, .02758, .00978, .02361, .00150,
            .01974, .00074]

class framework:
    """Cryptographic analysis class

    This class contains all implemented analysis functionality of
    this module. To start a cryptographic analysis, create an
    instance of this class. For arguments, see definition of
    __init__.
    """
    def __init__(self, alphabet=string.ascii_lowercase,
                 notinalph='convert, ignore'):
        """Initializes the class with the given parameters.

        Parameters:
        - alphabet:
            List of 'letters' of the alphabet. Could be a list of
            anything. If a 'letter' occurs more than once, it is
            ignored. Note that internally, cral works with indexes
            of the alphabet.
        - notinalph:
            What to do if a letter is encountered that is not in the
            alphabet:
            - 'ignore'
                cral ignores the unknown letter when counting,
                encrypting etc, but doesn't remove it. It will still
                be there when inputs are split, mutated etc.
            - 'convert'
                cral tries to convert the unknown letter to a known
                one, e.g. by converting from uppercase to lowercase.
                If that doesn't work, the behavior depends on wether
                'ignore' is in notinalph as well.
            - 'panic'
                cral throws an exception whenever it encounteres an
                unknown letter. 

        Default parameters:
        - The alphabet is the lowercase latin alphabet.
        - unknown letters are ignored.
        """
        self.notinalph = notinalph
        self.alphabet = []
        for c in alphabet:
            if c not in self.alphabet:
                self.alphabet.append(c)
        self.alphlen = len(self.alphabet)
        self.indexes = [x for x in range(self.alphlen)]

        #if the alphabet is an actual string, we shall output strings (see
        #_conv_out())
        if isinstance(alphabet, str):
            self.isstr = True
        else:
            self.isstr = False

    def _conv_in(self, inp):
        """Converts a list (or string) of letters to the internal
        representation of indexes."""

        res = []
        for c in inp:
            if c in self.alphabet:
                res.append(self.alphabet.index(c))
            elif 'convert' in self.notinalph:
                if c.lower() in self.alphabet:
                    res.append(self.alphabet.index(c.lower()))
                elif c.upper() in self.alphabet:
                    res.append(self.alphabet.index(c.upper()))
                elif 'ignore' in self.notinalph:
                    res.append(str(c))
                else: #includes 'panicÄ
                    raise Exception('Letter not in alphabet.')
            elif 'ignore' in self.notinalph:
                res.append(str(c))
            else: #includes 'panic'
                raise Exception('Letter not in alphabet.')
        return res

    def _conv_out(self, inp):
        """Converts a list of indexes (internal representation) to
        a list (or string) of letters."""

        res = []
        for c in inp:
            if isinstance(c, str):
                res.append(c) #ignored letter
            else:
                res.append(self.alphabet[c])
        if self.isstr:
            return ''.join(res)
        else:
            return res

    def add_str(self, in1, in2):
        """Adds the two input strings modulo size of alphabet.

        If in2 is longer than in1, the additional letters are
        ignored. If in2 is shorter than in1, it is repeated to fill
        the missing letters.
        If in1 contains ignored letters, these will reappear in the
        output without modification. If in2 contains ignored letters,
        the corresponding letters in in1 will reappear in the output
        without modification.
        """

        a = self._conv_in(in1)
        b = self._conv_in(in2)
        res = []

        for ind, letter1 in enumerate(a):
            letter2 = b[ind%len(b)]
            if isinstance(letter1, str) or isinstance(letter2, str):
                res.append(letter1)
            else:
                res.append((letter1+letter2)%self.alphlen)

        return(self._conv_out(res))

    def subs_str(self, in1, in2):
        """Substracts in2 from in1 modulo size of alphabet.

        If in2 is longer than in1, the additional letters are
        ignored. If in2 is shorter than in1, it is repeated to fill
        the missing letters.
        If in1 contains ignored letters, these will reappear in the
        output without modification. If in2 contains ignored letters,
        the corresponding letters in in1 will reappear in the output
        without modification.
        """

        a = self._conv_in(in1)
        b = self._conv_in(in2)
        res = []

        for ind, letter1 in enumerate(a):
            letter2 = b[ind%len(b)]
            if isinstance(letter1, str) or isinstance(letter2, str):
                res.append(letter1)
            else:
                res.append((letter1-letter2)%self.alphlen)

        return(self._conv_out(res))

    def hist(self, inp):
        """Counts how often each of the letters of the alphabet
        occurs in the inp string."""

        res = [inp.count(c) for c in self.alphabet]
        return res

    def norm_hist(self, inp):
        """Norms the given letter histogram so the sum is 1."""

        s = sum(inp)
        res = [val/s for val in inp]
        return res

    def norm_hist_sig(self, inp):
        """Norms the given letter histogram to [-1,1]."""

        hist = self.norm_hist(inp)
        avg = 1/self.alphlen
        res = [val-avg for val in hist]
        return res

    def plot_hist(self, inp):
        """Plots the given letter histogram."""

        plt.bar(self.indexes, inp, align='center')
        plt.xticks(self.indexes, self.alphabet) #label x values
        plt.gca().yaxis.grid(True) #horizontal grid
        valrng = max(inp)-min(inp)
        plt.ylim([min(inp)-.05*valrng, max(inp)+.05*valrng])
        plt.show()

    def hist_corr(self, hist1, hist2):
        """Calculates the cross correlation between hist1 and hist2."""

        res = []
        for i in range(self.alphlen):
            val = 0
            for j in range(self.alphlen):
                val += hist1[j]*hist2[(i+j)%self.alphlen]
            res.append(val)
        return res
