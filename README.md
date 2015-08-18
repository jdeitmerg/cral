#cral
####Cryptographic Analysis Framework

##About
This is a collection of methods for cryptographical analysis, written in Python. With its currently very limited functionality, attacks on simple classical ciphers can be performed. cral is not programmed for speed, so if you're looking for a framework to bruteforce binary ciphers, this is not it.

##Documentation
There is no documentation yet, but the docstrings and the example below should get you started.

##Dependencies
* matplotlib

##Installation
Download (or clone) this repository and put cral.py into the folder which contains the scripts in
which you want to use it. If you want to use it from the python interactive promt, make sure you
start python from a directory containing cral.py.

##Example Usage
All that cral contains is the framework class. Create an instance of it to use any of the provided functionality. Here's how you could break a caesar cipher:

```python
import cral

#With default arguments the alphabet will be string.ascii_lowercase (a..z)
#and cral will try to handle letters which are not in the alphabet reasonably.
f = cral.framework()

cipher = 'rgpa xh p rdaatrixdc du btiwdsh udg rgneidvgpewxrpa pcpanhxh.'

#To get an idea of the letter frequencies in cipher, we first let cral
#calculate the histogram...
hist = f.hist(cipher)

#...norm it (now we have actual frequencies)
hist = f.norm_hist(hist)

#...and calculate the cross correlation between our histogram and one of
#an average english text.
corr = f.hist_corr(cral.hist_eng, hist)

#If everything worked, the maximum value of the correlation should
#reveal the key
key, frequency = f.max_hist(corr)
print("The key is probably '", key, "'.", sep='')

#Decrypting the caesar cipher is as easy as substracting the key from
#the cipher.
plaintext = f.subs_str(cipher, key)
print("Which yields the plaintext:\n", plaintext, sep='')
```

Output:

```
The key is probably 'p'.
Which yields the plaintext:
cral is a collection of methods for cryptographical analysis.
```

We can also easily view the three histograms (cipher, english, crosscorrelation):

```python
f.plot_hist(hist)
```

![hist](https://cloud.githubusercontent.com/assets/7459936/7499969/15b9422a-f42b-11e4-8039-69760924bdb7.png)

```python
f.plot_hist(cral.hist_eng)
```

![hist_eng](https://cloud.githubusercontent.com/assets/7459936/9335347/cb9e5eaa-45d3-11e5-93f5-5a3f3626429f.png)

```python
f.plot_hist(corr)
```

![corr](https://cloud.githubusercontent.com/assets/7459936/9335350/cebe261a-45d3-11e5-8b6e-7152584a796c.png)


##Pull Requests
You are very welcome to contribute to this project, just open pull requests for bugfixes, new features etc. If you want to completely change the design (there is a lot of potential for that!) please create an issue first.
