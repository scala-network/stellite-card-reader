# stellite-card-reader
Trustless merchant application to bridge transaction between stellitepay and stellite-card-applet enabled javacard.

This is a merchant frontend application, to enable user (merchant) to input and show transaction parameter to payer. There is no cryptographic task involved as it should occur end to end between payer's stellitecard and server. All it needs is just this software, a smartcard readers, your (merchant) XTL address, and you are automagically a trusted merchant.

Usage are extra easy. You (merchant) input some XTL amount to be paid, payer tap/slide their card. Done. Payment is made.

The smartcard reader can be use any [PC/SC API](https://en.wikipedia.org/wiki/PC/SC) compatible smartcard readers. The software main function is to push back and forth encrypted data between stellitepay server and stellite-card-applet enabled javacard.

Currently will be built as a CLI application using python2.7x and python3 (compatible for both).

Dependencies: python2.7x/3x, pyscard, requests 

*NOTE : see [wiki](https://github.com/stellitecoin/stellite-card-reader/wiki/StelliteCard-reader-WIKI) on how to use thi application *
