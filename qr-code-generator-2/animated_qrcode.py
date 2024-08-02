from urllib.request import urlopen

import segno

slts_qrcode = segno.make_qr("https://nepaliroots.org/")
# gif_url = urlopen(
#    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXN2dXNiNnpya2JldjBqd21hbmw1MGNrOWozeTJmc3hoazI3djFxMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1Jcl9QfKC9CMRPp7II/giphy.gif")

slts_qrcode.to_artistic(
    background="logowave.gif",
    target="animated_qrcode.gif",
    light="white",
    scale=8,
    dark='red',
    border=2
)
