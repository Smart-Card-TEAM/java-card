/*
 * $Workfile: HelloWorld.java $	$Revision: 17 $, $Date: 5/02/00 9:05p $
 *
 * Copyright (c) 1999 Sun Microsystems, Inc. All Rights Reserved.
 *
 * This software is the confidential and proprietary information of Sun
 * Microsystems, Inc. ("Confidential Information").  You shall not
 * disclose such Confidential Information and shall use it only in
 * accordance with the terms of the license agreement you entered into
 * with Sun.
 *
 * SUN MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
 * SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE, OR NON-INFRINGEMENT. SUN SHALL NOT BE LIABLE FOR ANY DAMAGES
 * SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
 * THIS SOFTWARE OR ITS DERIVATIVES.
 */

// /*
// $Workfile: HelloWorld.java $
// $Revision: 17 $
// $Date: 5/02/00 9:05p $
// $Author: Akuzmin $
// $Archive: /Products/Europa/samples/com/sun/javacard/samples/HelloWorld/HelloWorld.java $
// $Modtime: 5/02/00 7:18p $
// Original author:  Mitch Butler
// */

package api_export_files;

import javacard.framework.*;
import javacard.security.*;

/**
 *
 */

public class AppletJavaCard extends Applet {
    private byte[] echoBytes;
    private static final short LENGTH_ECHO_BYTES = 256;

    /**
     * Only this class's install method should create the applet object.
     */

    private static final byte[] helloWorld = {'H', 'e', 'l', 'l', 'o'};
    private static final byte HW_CLA = (byte) 0x80;
    private static final byte INS_HELLO = (byte) 0x00;

    final static byte PIN_TRY_LIMIT = (byte) 0x03;
    // maximum size PIN
    final static byte MAX_PIN_SIZE = (byte) 0x08;
    // signal that the PIN verification failed
    final static short SW_VERIFICATION_FAILED = 0x6300;
    // signal the the PIN validation is required
    // for a credit or a debit transaction
    final static short SW_PIN_VERIFICATION_REQUIRED = 0x6301;
    OwnerPIN pin;
    final static byte VERIFY = (byte) 0x20;

    final static byte INS_GET_PUBLIC_KEY = (byte) 0x01;

    RSAPrivateCrtKey rsa_PrivateCrtKey;
    RSAPublicKey rsa_PublicKey;
    KeyPair rsa_KeyPair;

    final static byte GETPUBLICKEYMod_ = (byte) 0x01;
    final static byte GETPUBLICKEYExp_ = (byte) 0x02;

    protected AppletJavaCard(byte[] bArray, short bOffset, byte bLength) {
        echoBytes = new byte[LENGTH_ECHO_BYTES];
        pin = new OwnerPIN(PIN_TRY_LIMIT, MAX_PIN_SIZE);

        // The installation parameters contain the PIN
        // initialization value
        pin.update(new byte[]{0x00, 0x01, 0x02, 0x03}, (short) 0, (byte) 4);
        rsa_KeyPair = new KeyPair(KeyPair.ALG_RSA_CRT, KeyBuilder.LENGTH_RSA_1024);
        rsa_KeyPair.genKeyPair();
        rsa_PublicKey = (RSAPublicKey) rsa_KeyPair.getPublic();
        rsa_PrivateCrtKey = (RSAPrivateCrtKey) rsa_KeyPair.getPrivate();

        register(bArray, (short) (bOffset + 1), bArray[bOffset]);
    }

    private void getPublicKeyMod(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        rsa_PublicKey.getModulus(buffer, ISO7816.OFFSET_CDATA);
        apdu.setOutgoing();
        apdu.setOutgoingLength((short) 128);
        apdu.sendBytesLong(buffer, ISO7816.OFFSET_CDATA, (short) 128);
    }

    private void getPublicKeyExp(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        rsa_PublicKey.getExponent(buffer, ISO7816.OFFSET_CDATA);
        apdu.setOutgoing();
        apdu.setOutgoingLength((short) 4);
        apdu.sendBytesLong(buffer, (short) ISO7816.OFFSET_CDATA, (short) 4);

    }

    /**
     * Installs this applet.
     *
     * @param bArray  the array containing installation parameters
     * @param bOffset the starting offset in bArray
     * @param bLength the length in bytes of the parameter data in bArray
     */
    public static void install(byte[] bArray, short bOffset, byte bLength) {
        new AppletJavaCard(bArray, bOffset, bLength);
    }

    public void deselect() {

        // reset the pin value
        pin.reset();

    }

    public boolean select() {

        // The applet declines to be selected
        // if the pin is blocked.
        if (pin.getTriesRemaining() == 0) {
            return false;
        }
        return true;

    }// end of select method


    private void getHelloWorld(APDU apdu) {
        if (!pin.isValidated())
            ISOException.throwIt(SW_PIN_VERIFICATION_REQUIRED);
        byte[] buffer = apdu.getBuffer();
        short numBytes = (short) helloWorld.length;
        Util.arrayCopyNonAtomic(helloWorld, (short) 0, buffer, (short) 0, numBytes);
        apdu.setOutgoingAndSend((short) 0, numBytes);
    }

    private void verify(APDU apdu) {

        byte[] buffer = apdu.getBuffer();
        // retrieve the PIN data for validation.
        byte byteRead = (byte) (apdu.setIncomingAndReceive());

        // check pin
        // the PIN data is read into the APDU buffer
        // at the offset ISO7816.OFFSET_CDATA
        // the PIN data length = byteRead
        if (pin.check(buffer, ISO7816.OFFSET_CDATA,
                byteRead) == false)
            ISOException.throwIt(SW_VERIFICATION_FAILED);

    }

    /**
     * Processes an incoming APDU.
     *
     * @param apdu the incoming APDU
     * @throws ISOException with the response bytes per ISO 7816-4
     * @see APDU
     */
    public void process(APDU apdu) {
        if (selectingApplet()) {
            return;
        }
        byte[] buffer = apdu.getBuffer();
        byte CLA = buffer[ISO7816.OFFSET_CLA];
        byte INS = buffer[ISO7816.OFFSET_INS];

        if (CLA != HW_CLA) {
            ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED);
        }
        switch (INS) {
            case INS_HELLO:
                getHelloWorld(apdu);
                break;
            case VERIFY:
                verify(apdu);
                break;
            case GETPUBLICKEYMod_:
                getPublicKeyMod(apdu);
                // getHelloWorld(apdu);
                break;
            case GETPUBLICKEYExp_:
                getPublicKeyExp(apdu);
                break;
            default:
                ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
        }
    }

}
