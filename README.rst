install
-------
::
  $ sudo pip install rtmdocker

usage
-----
::
  $ rtmdocker [-h] [-v] [-n] [-t TAGNAME] [-r] [-d DEVICE]
                 [-e RUN_COMPONENT] [-c COMPILE_COMPONENT] [-x] [-U]
                 [--proxy PROXY] [--dryrun]
                 command

positional arguments
--------------------
::
  command               openrtp             : start OpenRTP
                        Controller          : start C++ ControllerComp
                        Motor               : start C++ MotorComp
                        ConsoleIn           : start C++ ConsoleInComp
                        ConsoleOut          : start C++ ConsoleOutComp
                        ConfigSample        : start C++ ConfigSampleComp
                        SeqIn               : start C++ SeqInComp
                        SeqOut              : start C++ SeqOutComp
                        MyServiceConsumer   : start C++ MyServiceConsumerComp
                        MyServiceProvider   : start C++ MyServiceProviderComp
                        ConsoleInPy         : start Python ConsoleIn.py
                        ConsoleOutPy        : start Python ConsoleOut.py
                        ConfigSamplePy      : start Python ConfigSampleComp
                        SeqInPy             : start Python SeqIn.py
                        SeqOutPy            : start Python SeqOut.py
                        MyServiceConsumerPy : start Python MyServiceConsumerComp
                        MyServiceProviderPy : start Python MyServiceProviderComp
                        TkJoyStick          : start Python TkJoyStickComp.py
                        TkLRFViewer         : start Python TkLRFViewer.py
                        Affine              : start OpenCV AffineComp
                        BackGroundSubtractionSimple : start OpenCV BackGroundSubtractionSimpleComp
                        Binarization        : start OpenCV BinarizationComp
                        CameraViewer        : start OpenCV CameraViewerComp
                        Chromakey           : start OpenCV ChromakeyComp
                        DilationErosion     : start OpenCV DilationErotionComp
                        Edge                : start OpenCV EdgeComp
                        Findcontour         : start OpenCV FindcontourComp
                        Flip                : start OpenCV FlipComp
                        Histogram           : start OpenCV HistogramComp
                        Hough               : start OpenCV HoughComp
                        ImageCalibration    : start OpenCV ImageCalibrationComp
                        ImageSubstraction   : start OpenCV ImageSubstractionComp
                        ObjectTracking      : start OpenCV ObjectTrackingComp
                        OpenCVCamera        : start OpenCV OpenCVCameraComp
                        Perspective         : start OpenCV PerspectiveComp
                        RockPaperScissors   : start OpenCV RockPaperScissorsComp
                        Rotate              : start OpenCV RotateComp
                        Scale               : start OpenCV ScaleComp
                        Sepia               : start OpenCV SepiaComp
                        SubstractCaptureImage : start OpenCV SubstractCaptureImageComp
                        Template            : start OpenCV TemplateComp
                        Translate           : start OpenCV TranslateComp
                        bash                : start bash

optional arguments
------------------
::
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n, --nameserver      run command with starting nameserver
  -t TAGNAME, --tag TAGNAME
                        tag name of image
  -r, --rdp             run command with start RDP server
  -d DEVICE, --device DEVICE
                        allow access to device from inside of container
  -e RUN_COMPONENT, --execute RUN_COMPONENT
                        run your C++ component
  -c COMPILE_COMPONENT, --compile COMPILE_COMPONENT
                        compile your C++ component
  -x, --xforward        enable X forwarding
  -U, --upgrade         upgrade target image before startup
  --proxy PROXY         set proxy server address
  --dryrun              dry run for debug
