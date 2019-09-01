import RPi.GPIO as GPIO

ledPin = 11  # define the ledPin
buttonPin = 12  # define the buttonPin


def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)


def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW:
            GPIO.output(ledPin, GPIO.HIGH)
            print ('led on ...')
        else: GPIO.output(ledPin, GPIO.LOW)
        print ('led off ...')


# Set buttonPin's mode is
def destroy():
    GPIO.output(ledPin, GPIO.LOW)  # led off
    GPIO.cleanup()  # Release resource

    
if __name__ == '__main__': # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the subprogram destroy() will be executed.
        destroy()
