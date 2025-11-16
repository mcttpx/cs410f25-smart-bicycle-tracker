#include <TinyGPSPlus.h>
#include <HardwareSerial.h>

TinyGPSPlus gps;                // GPS object
HardwareSerial GPSSerial(1);    // Use UART1 on ESP32

// GPS wiring (for your HiLetgo ESP-WROOM-32 + GY-NEO6MV2)
const int GPS_RX = 16;   // ESP32 receives from GPS TX
const int GPS_TX = 17;   // ESP32 sends to GPS RX (optional)
const int GPS_BAUD = 9600;

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println("Starting ESP32 + GY-NEO6MV2 GPS Test...");
  Serial.println("Waiting for GPS data...");

  // Start GPS serial connection
  GPSSerial.begin(GPS_BAUD, SERIAL_8N1, GPS_RX, GPS_TX);
}

void loop() {
  while (GPSSerial.available() > 0) {
    char c = GPSSerial.read();
    gps.encode(c);

    // When GPS provides new, valid location data
    if (gps.location.isUpdated()) {
      Serial.println("===== GPS FIX =====");

      Serial.print("Latitude : ");
      Serial.println(gps.location.lat(), 6);

      Serial.print("Longitude: ");
      Serial.println(gps.location.lng(), 6);

      Serial.print("Satellites: ");
      Serial.println(gps.satellites.value());

      Serial.print("Accuracy (HDOP): ");
      Serial.println(gps.hdop.hdop());

      Serial.println("====================");
    }
  }

  delay(10);
}