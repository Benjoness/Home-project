import RPi.GPIO as GPIO
import pigpio
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

speed = 0
DC1 = 1500
DC2 = 1500

spd=GPIO.PWM(4,100)
ser1=pigpio.pi()
ser2=pigpio.pi()

spd.start(speed)
ser1.set_servo_pulsewidth(5,DC1)
ser2.set_servo_pulsewidth(6,DC2)


request = None

try:
    class RequestHandler_httpd(BaseHTTPRequestHandler):
      def do_GET(self):
        global request
        global speed
        global DC1
        global DC2
        messagetosend = bytes('I am Back',"utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        request = self.requestline
        request = request[5 : int(len(request)-9)]
        print(request)
        if request == 'forward':
          GPIO.output(17,True)
          GPIO.output(22,True)
          GPIO.output(27,False)
          GPIO.output(23,False)
        if request == 'backward':
          GPIO.output(27,True)
          GPIO.output(23,True)
          GPIO.output(17,False)
          GPIO.output(22,False)
        if request == 'left':
          GPIO.output(17,True)
          GPIO.output(23,True)
          GPIO.output(27,False)
          GPIO.output(22,False) 
        if request == 'right':
          GPIO.output(22,True)
          GPIO.output(27,True)
          GPIO.output(17,False)
          GPIO.output(23,False)
        if request == 'stop':
          GPIO.output(22,False)
          GPIO.output(23,False)
          GPIO.output(17,False)
          GPIO.output(27,False)
        if request == 'inc':
            speed += 5
            spd.ChangeDutyCycle(speed)
        if request == 'dec':
            speed -= 5
            spd.ChangeDutyCycle(speed)
        if request == 'sleft':
            DC1 += 100
            if DC1 >= 2400:
                DC1 = 2500
            ser1.set_servo_pulsewidth(5,DC1)
        if request == 'sright':
            DC1 -= 100
            if DC1 <= 600:
                DC1 = 500
            ser1.set_servo_pulsewidth(5,DC1)
        if request == 'sdown':
            DC2 += 100
            if DC2 >= 2400:
                DC2 = 2500
            ser2.set_servo_pulsewidth(6,DC2)
        if request == 'sup':
            DC2 -= 100
            if DC2 <= 600:
                DC2 = 500
            ser2.set_servo_pulsewidth(6,DC2)
        if request == 'center':
            ser1.set_servo_pulsewidth(5,1500)
            ser2.set_servo_pulsewidth(6,1500)
            
        return


    server_address_httpd = ('192.168.43.192',8082)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
    print('Starting Server')
    httpd.serve_forever()
except KeyboardInterrupt:
    spd.stop()
    ser1.stop()
    ser2.stop()
    GPIO.cleanup()
    
