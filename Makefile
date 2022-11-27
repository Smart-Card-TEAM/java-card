CC=javac
PROJECT_PATH=pwd

FLAGS=-source 1.2 -target 1.1 -g -cp

API_PATH=$(JC_HOME_TOOLS)/bin/api.jar
APPLET_ID=0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2


convert: compile
	java -classpath $(JC_HOME_TOOLS)/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath $(PWD)/smart_card/api_export_files:AppletJavaCard -classdir . -applet $(APPLET_ID) smart_card.AppletJavaCard smart_card 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0

compile:
	$(CC) $(FLAGS) $(API_PATH) $(PWD)/smart_card/AppletJavaCard.java

install:
	$(PWD)/install.sh

list_apps:
	gpshell gpshell_instr/list_applets
install_applet:
	gpshell gpshell_instr/install_applet
uninstall_applet:
	gpshell gpshell_instr/uninstall_applet

