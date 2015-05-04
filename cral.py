import string
import matplotlib.pyplot as plt

class framework:
    """Cryptographic analysis class

    This class contains all implemented analysis functionality of
    this module. To start a cryptographic analysis, create an
    instance of this class. For arguments, see definition of
    __init__.
    """
    def __init__(self, alphabet=string.ascii_lowercase, notinalph='ignore'):
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
                Throws an exception if that doesn't work.
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
            res.append(self.alphabet.index(c))
        return res

    def _conv_out(self, inp):
        """Converts a list of indexes (internal representation) to
        a list (or string) of letters."""

        res = []
        for c in inp:
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
        """

        a = self._conv_in(in1)
        b = self._conv_in(in2)
        res = []

        for ind, letter1 in enumerate(a):
            letter2 = b[ind%len(b)]
            res.append((letter1+letter2)%self.alphlen)

        return(self._conv_out(res))

    def subs_str(self, in1, in2):
        """Substracts in2 from in1 modulo size of alphabet.

        If in2 is longer than in1, the additional letters are
        ignored. If in2 is shorter than in1, it is repeated to fill
        the missing letters.
        """

        a = self._conv_in(in1)
        b = self._conv_in(in2)
        res = []

        for ind, letter1 in enumerate(a):
            letter2 = b[ind%len(b)]
            res.append((letter1-letter2)%self.alphlen)

        return(self._conv_out(res))

    def hist(self, inp):
        """Counts how often each of the letters of the alphabet
        occurs in the inp string."""

        res = [inp.count(c) for c in self.alphabet]
        return res

    def norm_hist(self, inp):
        """Norms the given letter history so the sum is 1."""

        s = sum(inp)
        res = [val/s for val in inp]
        return res

    def norm_hist_sig(self, inp):
        """Norms the given letter history to [-1,1]."""

        hist = self.norm_hist(inp)
        avg = 1/self.alphlen
        res = [val-avg for val in hist]
        return res

    def plot_hist(self, inp):
        """Plots the given letter history."""

        plt.bar(self.indexes, inp, align='center')
        plt.xticks(self.indexes, self.alphabet) #label x values
        plt.gca().yaxis.grid(True) #horizontal grid
        valrng = max(inp)-min(inp)
        plt.ylim([min(inp)-.05*valrng, max(inp)+.05*valrng])
        plt.show()
