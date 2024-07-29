import pyshorteners


def generate_short_url(long_url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(long_url)


# https://medium.com/@maryam-bit/offset-vs-cursor-based-pagination-choosing-the-best-approach-2e93702a118b
long_url = input('Paste Long URl \n')
short_url = generate_short_url(long_url)
print(short_url)
