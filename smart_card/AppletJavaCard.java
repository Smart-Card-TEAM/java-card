package smart_card;

import javacard.framework.*;
import javacard.security.*;

import java.util.Objects;

/**
 */
public class AppletJavaCard extends Applet {
    private byte[] echoBytes;
    private static final short LENGTH_ECHO_BYTES = 256;
    private boolean ACTIVATED = true;

    /**
     * Only this class's install method should create the applet object.
     */

    private static final byte[] helloWorld = {'H', 'e', 'l', 'l', 'o'};
    private static final byte HW_CLA = (byte) 0x80;
    private static final byte INS_HELLO = (byte) 0x00;
    // at first the card is unactivated, we will have to set up a pin to activate the card and go further1.
    private static final byte INS_ACTIVATION = (byte) 0x04;

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


    // RSAPrivateCrtKey rsa_PrivateCrtKey;
    // RSAPublicKey rsa_PublicKey;
    // KeyPair rsa_KeyPair;
    RSAPublicKey m_publicKey;
    RSAPrivateKey m_privateKey;
    KeyPair m_keyPair;
    Signature m_signature;

    Signature m_verify;

    final static byte GETPUBLICKEYMod_ = (byte) 0x01;
    final static byte GETPUBLICKEYExp_ = (byte) 0x02;

    final static byte INS_SIGN = (byte) 0x03;

    protected AppletJavaCard(byte[] bArray, short bOffset, byte bLength) {
        echoBytes = new byte[LENGTH_ECHO_BYTES];
        pin = new OwnerPIN(PIN_TRY_LIMIT, MAX_PIN_SIZE);

        // The installation parameters contain the PIN
        // initialization value
        pin.update(new byte[]{0x00, 0x01, 0x02, 0x03}, (short) 0, (byte) 4);
        // rsa_KeyPair = new KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_512);
        // rsa_KeyPair.genKeyPair();
        // rsa_PublicKey = (RSAPublicKey) rsa_KeyPair.getPublic();
        // rsa_PrivateCrtKey = (RSAPrivateCrtKey) rsa_KeyPair.getPrivate();
        m_privateKey
                = (RSAPrivateKey) KeyBuilder.buildKey
                (KeyBuilder.TYPE_RSA_PRIVATE,
                        KeyBuilder.LENGTH_RSA_512,false);
        m_publicKey
                = (RSAPublicKey) KeyBuilder.buildKey
                (KeyBuilder.TYPE_RSA_PUBLIC,
                        KeyBuilder.LENGTH_RSA_512,true);
        m_keyPair
                = new KeyPair
                (KeyPair.ALG_RSA_CRT, (short)
                        m_publicKey.getSize());
        m_keyPair.genKeyPair();
        m_publicKey
                = (RSAPublicKey) m_keyPair.getPublic();
        m_privateKey
                = (RSAPrivateKey) m_keyPair.getPrivate();
        m_signature = Signature.getInstance
                (Signature.ALG_RSA_SHA_PKCS1, false);
        m_signature.init(m_privateKey, Signature.MODE_SIGN);
        m_verify = Signature.getInstance
                (Signature.ALG_RSA_SHA_PKCS1, false);
        m_verify.init(m_publicKey, Signature.MODE_VERIFY);
        register(bArray, (short) (bOffset + 1), bArray[bOffset]);
    }

    public void exportPublicKeyExponentAPDU(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        short length = m_publicKey.getExponent(buffer, (short) 0);
        apdu.setOutgoingAndSend((short) 0, length);
    }

    public void exportPublicKeyModulusAPDU(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        short length = m_publicKey.getModulus(buffer, (short) 0);

        apdu.setOutgoingAndSend((short) 0, length);
    }

    private void getPublicKeyMod(APDU apdu) {
        byte[] buffer = apdu.getBuffer();

        short length = m_publicKey.getModulus(buffer, ISO7816.OFFSET_CDATA);
        apdu.setOutgoing();
        apdu.setOutgoingLength((short) length);
        apdu.sendBytesLong(buffer, ISO7816.OFFSET_CDATA, (short) length);
    }

    public void signBuffer(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
//        byte[] bufferSign = new byte[5];
        short length = m_signature.sign(
                helloWorld,
                (short) 0,
                (short) helloWorld.length,
                buffer,
                (short) 0) ;
        boolean verif = m_verify.verify(
                helloWorld,
                (short) 0,
                (short) helloWorld.length,
                buffer,
                (short) 0,
                length);
//        if (verif) {
//            getHelloWorld(apdu);
//        } else {
//            ISOException.throwIt(ISO7816.SW_FUNC_NOT_SUPPORTED);
//        }
//        apdu.setOutgoing();
//        apdu.setOutgoingLength((short) buffer.length);
//        apdu.sendBytesLong(buffer, ISO7816.OFFSET_CDATA, (short) buffer.length);
//        Util.arrayCopyNonAtomic(bufferSign, (short) 0, buffer, (short) 0, length);
        apdu.setOutgoingAndSend((short) 0, length);
//        apdu.setOutgoingAndSend((short) 0, (short) buffer.length);
    }
//    private void getPublicKeyExp(APDU apdu) {
//        byte[] buffer = apdu.getBuffer();
//        m_privateKey.getExponent(buffer, ISO7816.OFFSET_CDATA);
//        apdu.setOutgoing();
//        apdu.setOutgoingLength((short) 4);
//        apdu.sendBytesLong(buffer, (short) ISO7816.OFFSET_CDATA, (short) 4);
//
//    }

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
        return pin.getTriesRemaining() != 0;

    }// end of select method

    private void activate(APDU apdu) {
        if (!pin.isValidated())
            ISOException.throwIt(SW_PIN_VERIFICATION_REQUIRED);
        byte[] buffer = apdu.getBuffer();
        byte byteRead = (byte) (apdu.setIncomingAndReceive());
        byte[] Newpin = new byte[buffer[ISO7816.OFFSET_CDATA]];
        ACTIVATED = true;
        pin.update(buffer, ISO7816.OFFSET_CDATA, byteRead);
    }


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
        if (!pin.check(buffer, ISO7816.OFFSET_CDATA,
                byteRead))
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
                // getPublicKeyMod(apdu);
                break;
            case INS_ACTIVATION:
                activate(apdu);
                break;
            case VERIFY:
                verify(apdu);
                break;
            case GETPUBLICKEYMod_:
                exportPublicKeyModulusAPDU(apdu);
                // getHelloWorld(apdu);
                break;
            case GETPUBLICKEYExp_:
                exportPublicKeyExponentAPDU(apdu);
                break;
            case INS_SIGN:
                signBuffer(apdu);
                break;
            default:
                ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
        }

    }


}