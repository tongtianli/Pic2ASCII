from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image

class ASCIIparser(QThread):
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    parseConpeleted = pyqtSignal()
    def __init__(self,filepath : str, outpath : str, width = 240, height = 80, parent = None):
        super(ASCIIparser,self).__init__(parent)
        self.filePath = filepath
        self.width = width
        self.height = height
        self.outPath = outpath

    def get_char(self, r, g, b, alpha=256):
        if alpha == 0:
            return ' '
        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        unit = (256.0 + 1) / length
        return self.ascii_char[int(gray / unit)]

    def run(self):
        im = Image.open(self.filePath)
        im = im.resize((self.width, self.height), Image.NEAREST)

        txt = ""

        for i in range(self.height):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j, i)))
            txt += '\n'

        output = self.filePath.split("/")[-1].split(".")[0]+".txt"
        with open(self.outPath+"/"+output, 'w') as f:
            f.write(txt)
        self.parseConpeleted.emit()