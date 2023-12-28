from PIL import Image
import qrcode
import sqlite3

PORT = 8350
DPI = 300
sizecm = 0.75
qrcodesize = 29

mydb = sqlite3.connect("ducksDB.db")

cursor = mydb.cursor()
cursor.execute("SELECT longid FROM ducks")

idList = cursor.fetchall()
qrcodes = []
url = "192.168.1.203:" + str(PORT) + "/f?id=%d"

for id in idList:
    id = id[0]

    qr = qrcode.QRCode(
        version=None,
        box_size=int(((DPI / 2.54) * sizecm)/qrcodesize)+1,
        border=0,
    )
    qr.add_data(url % (id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qrcodes.append(img)

qrcodes[0].save("single.png")

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