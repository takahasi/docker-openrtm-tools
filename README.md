usage:
------
```shell
python rtmdocker.py [-v] [-n] [-t <tag>] [-x] [-c <comp>] [-r <comp>] [--help] command
```

positional arguments:
---------------------
```shell
  command               openrtp             : start OpenRTP
                        Controller          : start C++ ControllerComp
                        Motor               : start C++ MotorComp
                        ConsoleIn           : start C++ ConsoleInComp
                        ConsoleOut          : start C++ ConsoleOutComp
                        SeqIn               : start C++ SeqInComp
                        SeqOut              : start C++ SeqOutComp
                        MyServiceConsumer   : start C++ MyServiceConsumerComp
                        MyServiceProvider   : start C++ MyServiceProviderComp
                        ConsoleInPy         : start Python ConsoleIn.py
                        ConsoleOutPy        : start Python ConsoleOut.py
                        SeqInPy             : start Python SeqIn.py
                        SeqOutPy            : start Python SeqOut.py
                        MyServiceConsumerPy : start Python MyServiceConsumerComp
                        MyServiceProviderPy : start Python MyServiceProviderComp
                        TkJoyStick          : start Python TkJoyStickComp.py
                        TkLRFViewer         : start Python TkLRFViewer.py
                        bash                : start bash
```

optional arguments:
-------------------
```
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -n, --nameserver      run command with starting nameserver
  -t TAGNAME, --tag TAGNAME
                        tag name of image
  -r RUN_COMPONENT, --run RUN_COMPONENT
                        run your C++ component
  -c COMPILE_COMPONENT, --compile COMPILE_COMPONENT
                        compile your C++ component
  -x, --xforward        enable X forwarding
  ```
