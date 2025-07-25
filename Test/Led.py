# -*-coding: utf-8 -*-
import time
from rpi_ws281x import *
# LED strip configuration:
LED_COUNT      = 4      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
# Define functions which animate LEDs in various ways.
class Led:
    def __init__(self):
        #Control the sending order of color data
        self.LedMod='0'
        self.index=0
        self.colour=[0,0,0]
        self.ORDER = "RGB"  
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.start = time.time()
        self.next=0
        self.ws2812_breathe_flag = 0;
        self.breathe_brightness = 0;
    def LED_TYPR(self,order,R_G_B):
        B=R_G_B & 255
        G=R_G_B >> 8 & 255
        R=R_G_B >> 16 & 255 
        Led_type=["GRB","GBR","RGB", "RBG","BRG","BGR"]
        color = [Color(G,R,B),Color(G,B,R),Color(R,G,B),Color(R,B,G),Color(B,R,G),Color(B,G,R)]
        if order in Led_type:
            return color[Led_type.index(order)]
    def colorWipe(self,strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        color=self.LED_TYPR(self.ORDER,color)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)              
        
    def Blink(self,strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        color=self.LED_TYPR(self.ORDER,color)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
        time.sleep(wait_ms/1000.0)

    def theaterChase(self,strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        color=self.LED_TYPR(self.ORDER,color)
        for j in range(iterations):
            for q in range(3):
                for i in range(0,self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos<0 or pos >255:
            r=g=b=0
        elif pos < 85:
            r=pos * 3
            g=255 - pos * 3
            b=0
        elif pos < 170:
            pos -= 85
            r=255 - pos * 3
            g=0
            b=pos * 3
        else:
            pos -= 170
            r=0
            g=pos * 3
            b=255 - pos * 3
        return self.LED_TYPR(self.ORDER,Color(r,g,b))

    def rainbow(self,strip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                 self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def Breating(self,strip,data):
        self.next= time.time()
        if (self.next- self.start>0.003) and (self.ws2812_breathe_flag==0):
            self.start=self.next
            self.breathe_brightness=self.breathe_brightness+1
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i,Color((int)(data[0]*self.breathe_brightness  / 255),(int)(data[1]*self.breathe_brightness  / 255),(int)(data[2]*self.breathe_brightness  / 255)))
            self.strip.show()
            if self.breathe_brightness >= 255:
                self.ws2812_breathe_flag=1
        if (self.next- self.start>0.003) and (self.ws2812_breathe_flag==1):
            self.start=self.next
            self.breathe_brightness=self.breathe_brightness-1
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color((int)(data[0]*self.breathe_brightness  / 255),(int)(data[1]*self.breathe_brightness  / 255),(int)(data[2]*self.breathe_brightness  / 255)))
            self.strip.show()
            if self.breathe_brightness <= 0:
                self.ws2812_breathe_flag=0
    
    def rainbowCycle(self,strip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)
    def theaterChase(self,strip,data, wait_ms=50):
        for q in range(3):
            for i in range(0, self.strip.numPixels(), 3):
                self.strip.setPixelColor(i+q,Color(data[0],data[1],data[2]))
            self.strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

    def theaterChaseRainbow(self,strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, 0)
    
    def policeLightsThreaded(self, duration=5, interval=0.1):
        red = self.LED_TYPR(self.ORDER, Color(255, 0, 0))
        blue = self.LED_TYPR(self.ORDER, Color(0, 0, 255))
        end_time = time.time() + duration
        while time.time() < end_time:
            # Red front, blue back
            self.strip.setPixelColor(0, red)
            self.strip.setPixelColor(1, blue)
            self.strip.setPixelColor(2, red)
            self.strip.setPixelColor(3, blue)
            self.strip.show()
            time.sleep(interval)

            # Swap: blue front, red back
            self.strip.setPixelColor(0, blue)
            self.strip.setPixelColor(1, red)
            self.strip.setPixelColor(2, blue)
            self.strip.setPixelColor(3, red)
            self.strip.show()
            time.sleep(interval)

        # Clear lights
        self.colorWipe(self.strip, Color(0, 0, 0), 10)
    
    def ledIndex(self,index,R,G,B):
        color=self.LED_TYPR(self.ORDER,Color(R,G,B))
        for i in range(4):
            if index & 0x01 == 1:
                self.strip.setPixelColor(i,color)
                self.strip.show()
            index=index >> 1
           
    def ledMode(self,data):
        self.LedMod='0'
        if len(data) <5:
            self.LedMod=data[1]
        else:
            self.LedMod=data[1]
            for i in range(3):
                self.colour[i]=int(data[i+2])
        while True:
            if self.LedMod=='1':
                self.ledIndex(int(data[5]),self.colour[0],self.colour[1],self.colour[2])
            elif self.LedMod=='2':
                self.colorWipe(self.strip, Color(255, 0, 0),120)  # Red wipe
                self.colorWipe(self.strip, Color(0, 255, 0),120)  # Green wipe
                self.colorWipe(self.strip, Color(0, 0, 255),120)  # Blue wipe
                self.colorWipe(self.strip, Color(0,0,0),50)
            elif self.LedMod=='3':
                self.Blink(self.strip,Color(self.colour[0],self.colour[1],self.colour[2]),50)
                self.Blink(self.strip, Color(0,0,0),50)
            elif self.LedMod=='4':
                self.Breating(self.strip,(self.colour[0],self.colour[1],self.colour[2]))
            elif self.LedMod=='5':
                self.rainbowCycle(self.strip)
                self.colorWipe(self.strip, Color(0,0,0),10)
            else:
                self.colorWipe(self.strip, Color(0,0,0),10)
                break
led=Led()                 
# Main program logic follows:
if __name__ == '__main__':
    print('Police light mode starting...')
    led.policeLights(interval=0.1)
    '''
    print ('Program is starting ... ')
    try:
        while True:
            print ("Chaser animation")
            led.colorWipe(led.strip, Color(255,0, 0))   # Red wipe
            led.colorWipe(led.strip, Color(0, 255, 0))  # Green wipe
            led.colorWipe(led.strip, Color(0, 0, 255))  # Blue wipe
            led.theaterChaseRainbow(led.strip)
            print ("Rainbow animation")
            led.rainbow(led.strip)
            led.rainbowCycle(led.strip)
            led.colorWipe(led.strip, Color(0,0,0),10)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        led.colorWipe(led.strip, Color(0,0,0),10)
    '''
