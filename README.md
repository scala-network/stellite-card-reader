# stellite-card-reader
Human interface software to do transaction with stellite-card-applet installed javacard.

This is a merchant frontend software, to enable user to input and show transaction parameter, using any PC/SC API compatible smartcard reader. The software has main function to push back and forth encrypted data from/to stellitepay server and stellite-card-applet enabled javacard. There is no cryptographic task involved in this software at all as it should occur end to end between card and server.

Currently will be built as a CLI application using python3.
Dependencies: python3+, pyscard, requests 
