#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>

#define FIREBASE_HOST "test-381c5-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "A6WrmdY4n8sHOXMMRsqDulEFsXDrLNWnu1IFVMfu"
#define WIFI_SSID "Sharma 2.4G"
#define WIFI_PASSWORD "Sharma86161"

String values, sensor_data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while(WiFi.status()!= WL_CONNECTED){
    Serial.print('.');
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

}

void loop() {
  bool serial_check= false;
  while(Serial.available()){
    sensor_data=Serial.readString();
    serial_check=true;
  }
  delay(1000);
  if(serial_check==true){
    Firebase.pushString("Sensor Data",sensor_data);
  }
  if (Firebase.failed()) {
    Serial.print("setting /number failed:");
    return;
  }

}
