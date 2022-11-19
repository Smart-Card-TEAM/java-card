# JavaCard

- export JC_HOME_TOOLS=/home/kali/java-card/sdks/jc211_kit
- export JAVA_HOME=/usr/lib/jvm/zulu-8-amd64/
- export PATH=$JAVA_HOME/bin:$JC_HOME_TOOLS/bin:$PATH

# Exemple d'upload d'une applet sur smartcard



Il faut se mettre dans `./sdks/jc211_kit/samples/`
```
javac -source 1.2 -target 1.1 -g -cp ../bin/api.jar com/sun/javacard/samples/HelloWorld/HelloWorld.java
```

```
java -classpath $JC_HOME_TOOLS/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath $JC_HOME_TOOLS/api_export_files:HelloWorld -classdir . -applet 0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2 com.sun.javacard.samples.HelloWorld.HelloWorld com.sun.javacard.samples.HelloWorld 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0
```

## GPShell
Lister les applets sur la smartcard:
```
mode_201
gemXpressoPro
enable_trace
establish_context
card_connect
select -AID A000000018434D
open_sc -security 0 -keyind 0 -keyver 0 -keyDerivation visa2 -key 47454d5850524553534f53414d504c45
get_status -element 40
card_disconnect
release_context
```

Upload l'applet `HelloWorld.java`:

```
mode_201
enable_trace
enable_timer
establish_context
card_connect
select -AID A000000018434D00
open_sc -security 3 -keyind 0 -keyver 0 -key 47454d5850524553534f53414d504c45 -keyDerivation visa2
install -file HelloWorld.cap -sdAID A000000018434D00 -nvCodeLimit 4000
card_disconnect
release_context
```

Supprimer une applet via AID:
```
mode_201
gemXpressoPro
enable_trace
enable_timer
establish_context
card_connect
select -AID A000000018434D00
open_sc -security 0 -keyind 0 -keyver 0 -key 47454d5850524553534f53414d504c45
delete -AID a00000006203010c060102
delete -AID 0a0000006203010c0601
card_disconnect
release_context
```
