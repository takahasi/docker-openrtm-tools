#!/bin/bash

example="/usr/share/openrtm-1.1/example"

command="rtm-naming &&"
command+="($example/ControllerComp &) &&"
command+="($example/MotorComp &) &&"
comamnd+="($example/ConsoleInComp &) &&"
command+="($example/ConsoleOutComp &) &&"
command+="($example/SeqInComp &) &&"
command+="($example/SeqOutComp &) &&"
command+="($example/MyServiceConsumerComp &) &&"
command+="($example/MyServiceProviderComp &) &&"
command+="bash"

bash -c "$command"

exit 0
