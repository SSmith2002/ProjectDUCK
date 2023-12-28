from PIL import Image
import qrcode
import sqlite3

PORT = 8350
DPI = 300
sizecm = 1
qrcodesize = 21

mydb = sqlite3.connect("ducksDB.db")

cursor = mydb.cursor()
cursor.execute("SELECT longid FROM ducks")

idList = cursor.fetchall()
qrcodes = []
url = "localhost:" + str(PORT) + "/setFound?%d"

for id in idList:
    id = id[0]

    qr = qrcode.QRCode(
        version=1,
        box_size=int(((DPI / 2.54) * sizecm)/qrcodesize)+1,
        border=1,
    )
    qr.add_data(url % (id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qrcodes.append(img)

width, height = int(8.27 * DPI), int(11.7 * DPI) # A4 at 300dpi
gridsize = len(qrcodes) ** 0.5
buffer = 50

page = Image.new('RGB', (width, height), 'white')
x = 0
y = 0
for qr in qrcodes:
    page.paste(qr,box=(buffer + int(x*(width-buffer)/gridsize),buffer + int(y*(height-buffer)/gridsize)))
    if x+1 == 8:
        x = 0
        y += 1
    else:
        x += 1

page.save("qrcodes.pdf")
page.save("qrcodes.png")