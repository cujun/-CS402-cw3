####Instructions for invoking soot

The folder contains both soot.sh (for *nix, Linux and OS X) and soot.bat (for Windows).

1. Make sure that your current JVM is Java 7 (use java -version).
2. Update the JAVA_HOME variable in soot.sh or soot.bat
3. Run it  as follows (note that if you want to process Test.java you only need to use Test)

- soot.sh: $./soot.sh Test
- soot.bat: C:\> soot.bat Test

4. The .jimple file will be generated in the same folder.