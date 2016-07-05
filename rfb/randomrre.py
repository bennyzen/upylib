import rfb

try:
    from urandom import getrandbits
except:
    from random import getrandbits

class Randomise(rfb.RfbSession):

    def __init__(self, conn, w, h, name):
        super().__init__(conn, w, h, name)
        self.rectangles = []
    
        for i in range( getrandbits(8) ):
            x, y = getrandbits(8), getrandbits(8)
            w = h = getrandbits(5)
            x = x if x<self.w-w else x-w
            y = y if y<self.h-h else y-h
            bgcolour = (
                getrandbits(8),
                getrandbits(8),
                getrandbits(8)
            )
            self.rectangles.append(
                rfb.RRERect(
                    x, y,
                    w, h,
                    bgcolour,
                    self.bpp, self.depth, 
                    self.big, self.true,
                    self.masks, self.shifts
                )
            )

    def update(self):
        self.send( rfb.ServerFrameBufferUpdate( self.rectangles ) )
        for rect in self.rectangles:
            rect.bgcolour = (
                getrandbits(8),
                getrandbits(8),
                getrandbits(8),
            )


svr = rfb.RfbServer(255, 255, name=b'random', handler=Randomise)
svr.serve()