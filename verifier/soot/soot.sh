#!/bin/bash
#set java 7 as JAVA_HOME
#JAVA_HOME = "your java 7 home"

java -cp ./soot-trunk.jar soot.Main -cp .:lib/scala-library.jar:$JAVA_HOME/jre/lib/rt.jar -output-dir . -output-format jimple -p jb use-original-names:true $@
# java -cp ./soot-trunk.jar soot.Main -cp .:lib/scala-library.jar:$JAVA_HOME/jre/lib/rt.jar -output-dir . -output-format jimple -print-tags -keep-line-number -p jb use-original-names:true $@
