package api_export_files;

import javacard.security.KeyBuilder;
import javacard.security.KeyPair;
import javacard.security.PrivateKey;
import javacard.security.PublicKey;


public class RSAKeyPair {
    private KeyPair RSAkeyPair;
    public RSAKeyPair() {
        // TODO Auto-generated constructor stub
        this.RSAkeyPair = new KeyPair(KeyPair.ALG_RSA_CRT, KeyBuilder.LENGTH_RSA_512);
        this.RSAkeyPair.genKeyPair();


    }
    public PrivateKey getPrivate() {
        return this.RSAkeyPair.getPrivate();
    }
    public PublicKey getPublicKey() {
        return this.RSAkeyPair.getPublic();
    }
}
