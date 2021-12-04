#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 5
#define RST_PIN 4

//Parameters
const int ipaddress[4] = {192, 168, 1, 6};
//Variables
byte nuidPICC[4] = {0, 0, 0, 0};
MFRC522::MIFARE_Key key;
MFRC522 mfrc522(SS_PIN, RST_PIN);  //--> Create MFRC522 instance.

#define ON_Board_LED 2  //--> Defining an On Board LED, used for indicators when the process of connecting to a wifi router

//----------------------------------------SSID and Password of your WiFi router-------------------------------------------------------------------------------------------------------------//
const char* ssid = "kecikoi14";
const char* password = "kucingpermai14";

int readsuccess;
byte readcard[4];
char str[32] = "";
String StrUID;

void setup() {
    //Init Serial USB
    Serial.begin(115200);
    Serial.println(F("Initialize System"));
    //init rfid D8,D5,D6,D7
    SPI.begin();
    mfrc522.PCD_Init();

    delay(500);

    WiFi.begin(ssid, password); //--> Connect to your WiFi router
    Serial.println("");

    pinMode(ON_Board_LED, OUTPUT);
    digitalWrite(ON_Board_LED, HIGH); //--> Turn off Led On Board

    Serial.print("Connecting");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        //----------------------------------------Make the On Board Flashing LED on the process of connecting to the wifi router.
        digitalWrite(ON_Board_LED, LOW);
        delay(250);
        digitalWrite(ON_Board_LED, HIGH);
        delay(250);
    }
    digitalWrite(ON_Board_LED, HIGH); //--> Turn off the On Board LED when it is connected to the wifi router.
  //----------------------------------------If successfully connected to the wifi router, the IP Address that will be visited is displayed in the serial monitor
    Serial.println("");
    Serial.print("Successfully connected to : ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    Serial.println("Please tag a card or keychain to see the UID !");
    Serial.println("");
}

void loop() {
    readsuccess = getid();
    
}
// void readRFID(void ) { /* function readRFID */
//     ////Read RFID card
//     for (byte i = 0; i < 6; i++) {
//     key.keyByte[i] = 0xFF;
//     }
//     // Look for new 1 cards
//     if ( ! rfid.PICC_IsNewCardPresent())
//     return;
//     // Verify if the NUID has been readed
//     if (  !rfid.PICC_ReadCardSerial())
//     return;
//     // Store NUID into nuidPICC array
//     for (byte i = 0; i < 4; i++) {
//     nuidPICC[i] = rfid.uid.uidByte[i];
//     }
//     Serial.print(F("RFID In dec: "));
//     printDec(rfid.uid.uidByte, rfid.uid.size);
//     Serial.println();
//     Serial.print(F("RFID In HEX: "));
//     printHex(rfid.uid.uidByte, rfid.uid.size);
//     Serial.println();
//     // Halt PICC
//     rfid.PICC_HaltA();
//     // Stop encryption on PCD
//     rfid.PCD_StopCrypto1();
// }
// /**
//    Helper routine to dump a byte array as hex values to Serial.
// */
// void printHex(byte *buffer, byte bufferSize) {
//     for (byte i = 0; i < bufferSize; i++) {
//     Serial.print(buffer[i] < 0x10 ? " 0" : " ");
//     Serial.print(buffer[i], HEX);
//     }
// }
// /**
//    Helper routine to dump a byte array as dec values to Serial.
// */
// void printDec(byte *buffer, byte bufferSize) {
//     for (byte i = 0; i < bufferSize; i++) {
//     Serial.print(buffer[i] < 0x10 ? " 0" : " ");
//     Serial.print(buffer[i], DEC);
//     }
// }