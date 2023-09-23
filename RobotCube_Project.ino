// A0 = L
// A1 = R
// A2 = B
// A3 = F
// int bL = 23;
// int bR = 19;
// int bB = 18;
// int bF = 5;

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <ESP32Servo.h>
#include <WebServer.h>
#include <WiFi.h>

const char* ssid = "Robot_Cube";
const char* password = "11111111";

WebServer server(80);
IPAddress local_IP(192, 168, 4, 184);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 120
#define SERVOMAX 520

uint8_t servonum = 0;

const char* status = "unready";     // ready or unready
const char* spinValue = "notspin";  // spin or notspin

//================================= L ==================
int servo_L = 0;

int servo_L_0 = 5;
int servo_L_90 = 90;
int servo_L_180 = 180;
//================================= R ==================
int servo_R = 3;
int servo_R_0 = 6;
int servo_R_90 = 80;
int servo_R_180 = 160;
//================================= B ==================
int servo_B = 4;
int servo_B_0 = 0;
int servo_B_90 = 95;
int servo_B_180 = 190;
//================================= F ==================
int servo_F = 5;
int servo_F_0 = 0;
int servo_F_90 = 90;
int servo_F_180 = 180;
//================================= bL ==================
int servo_front_L = 0;
int servo_back_L = 90;
//================================= bR ==================
int servo_front_R = 10;
int servo_back_R = 90;
//================================= bB ==================
int servo_front_B = 0;
int servo_back_B = 90;
//================================= bF ==================
int servo_front_F = 0;
int servo_back_F = 90;
//======================================================
Servo baseL;
Servo baseR;
Servo baseB;
Servo baseF;
int bL = 23;
int bR = 19;
int bB = 18;
int bF = 5;
//=============================== servoPosition =====================
void servoPosition(int servoChannel, int angle) {
  int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(servoChannel, 0, pulse);
}

void SPINservoPosition() {
  int pulseL = map(servo_L_90, 0, 180, SERVOMIN, SERVOMAX);
  int pulseR = map(servo_R_90, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(servo_L, 0, pulseL);
  pwm.setPWM(servo_R, 0, pulseR);
}

void SPINOFFservoPosition() {
  int pulseL = map(servo_L_0, 0, 180, SERVOMIN, SERVOMAX);
  int pulseR = map(servo_R_0, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(servo_L, 0, pulseL);
  pwm.setPWM(servo_R, 0, pulseR);
}

void servoPositionB(int servoChannel, int angle) {
  int pulse = map(angle, 0, 180, 100, 520);
  pwm.setPWM(servoChannel, 0, pulse);
}
//=================================BACK-FRONT==================
void backL() {
  baseL.write(servo_back_L);
  delay(200);
}
void frontL() {
  baseL.write(servo_front_L);
  delay(500);
}
//=============
void backR() {
  baseR.write(servo_back_R);
  delay(500);
}
void frontR() {
  baseR.write(servo_front_R);
  delay(500);
}
//=============
void backB() {
  baseB.write(servo_back_B);
  delay(200);
}
void frontB() {
  baseB.write(servo_front_B);
  delay(500);
}
//=============
void backF() {
  baseF.write(servo_back_F);
  delay(200);
}
void frontF() {
  baseF.write(servo_front_F);
  delay(500);
}
//==================================Function L ==============
void CHECK() {
  if (spinValue == "spin") {
    spinoff();
  }
}
void L() {
  servoPosition(servo_L, servo_L_90);
  delay(500);
  backL();
  servoPosition(servo_L, servo_L_0);
  delay(500);
  frontL();
}
void LL() {
  backL();
  servoPosition(servo_L, servo_L_90);
  delay(400);
  frontL();
  servoPosition(servo_L, servo_L_0);
  delay(200);
}
void L2() {
  servoPosition(servo_L, servo_L_180);
  delay(400);
  backL();
  servoPosition(servo_L, servo_L_0);
  delay(400);
  frontL();
}
//==================================Function R ==============
void R() {
  backR();
  servoPosition(servo_R, servo_R_90);
  delay(400);
  baseR.write(25);
  delay(400);
  servoPosition(servo_R, 0);
  delay(400);
  servoPosition(servo_R, servo_R_0);
  frontR();
}
void RR() {
  baseR.write(25);
  delay(300);
  servoPosition(servo_R, servo_R_90);
  delay(400);
  backR();
  servoPosition(servo_R, servo_R_0);
  delay(400);
  frontR();
}
void R2() {
  baseR.write(25);
  delay(200);
  servoPosition(servo_R, 170);
  delay(600);
  servoPosition(servo_R, 160);
  delay(200);
  backR();
  servoPosition(servo_R, servo_R_0);
  delay(400);
  frontR();
}
//==================================Function B ==============
void BB() {
  backB();
  servoPositionB(servo_B, servo_B_90);
  delay(400);
  frontB();
  servoPositionB(servo_B, servo_B_0);
  delay(200);
}
void B() {
  servoPositionB(servo_B, servo_B_90);
  delay(500);
  backB();
  servoPositionB(servo_B, servo_B_0);
  delay(400);
  frontB();
}
void B2() {
  servoPositionB(servo_B, servo_B_180);
  delay(400);
  backB();
  servoPositionB(servo_B, servo_B_0);
  delay(400);
  frontB();
}
//==================================Function F ==============
void front_F() {
  servoPosition(servo_F, servo_F_90);
  delay(400);
  backF();
  servoPosition(servo_F, servo_F_0);
  delay(400);
  frontF();
}
void FF() {
  backF();
  servoPosition(servo_F, servo_F_90);
  delay(400);
  frontF();
  servoPosition(servo_F, servo_F_0);
  delay(200);
}
void F2() {
  servoPosition(servo_F, servo_F_180);
  delay(400);
  backF();
  servoPosition(servo_F, servo_F_0);
  delay(400);
  frontF();
}
//==================================Function U ==============
void CHECK_spin() {
  if (spinValue == "notspin") {
    spin();
  }
}

void spin() {
  spinValue = "spin";
  baseL.write(servo_back_L);
  baseR.write(servo_back_R);
  delay(100);
  SPINservoPosition();
  delay(500);
  baseL.write(servo_front_L);
  baseR.write(servo_front_R);
  delay(400);
  baseB.write(servo_back_B);
  baseF.write(servo_back_F);
  delay(300);
  SPINOFFservoPosition();
  delay(600);
  baseF.write(servo_front_F);
  baseB.write(servo_front_B);
  delay(400);
  baseL.write(servo_back_L);
  baseR.write(servo_back_R);
  delay(200);
  baseR.write(servo_front_R);
  baseL.write(servo_front_L);
  delay(200);
}

void spinoff() {
  spinValue = "notspin";
  baseB.write(servo_back_B);
  baseF.write(servo_back_F);
  delay(300);
  SPINservoPosition();
  delay(100);
  baseB.write(servo_front_B);
  baseF.write(servo_front_F);
  delay(300);
  baseL.write(servo_back_L);
  baseR.write(servo_back_R);
  delay(300);
  SPINOFFservoPosition();
  delay(300);
  baseL.write(servo_front_L);
  baseR.write(servo_front_R);
  delay(500);
  baseF.write(servo_back_F);
  baseB.write(servo_back_B);
  delay(300);
  baseF.write(servo_front_F);
  baseB.write(servo_front_B);
  delay(200);
}

void U() {
  CHECK_spin();
  B();
}
void UU() {
  CHECK_spin();
  BB();
}
void U2() {
  CHECK_spin();
  B2();
}
//==================================Function D ==============
void D() {
  CHECK_spin();
  front_F();
}
void DD() {
  CHECK_spin();
  FF();
}
void D2() {
  CHECK_spin();
  F2();
}
//============================================================================
void STOP() {
  status = "unready";
  delay(500);
  baseB.write(servo_back_B);
  baseF.write(servo_back_F);
  delay(3000);
  baseL.write(servo_back_L);
  baseR.write(servo_back_R);
  delay(2000);
  baseL.write(servo_front_L);
  baseR.write(servo_front_R);
  baseB.write(servo_front_B);
  baseF.write(servo_front_F);
  delay(100);
}

void START() {
  status = "ready";
  spinValue = "notspin";
  baseL.write(servo_back_F);
  baseR.write(servo_back_R);
  baseB.write(servo_back_B);
  baseF.write(servo_back_F);
  delay(500);
  servoPosition(servo_L, servo_L_0);
  servoPosition(servo_R, servo_R_0);
  servoPositionB(servo_B, servo_B_0);
  servoPosition(servo_F, servo_F_0);
  delay(4000);
  baseL.write(servo_front_L);
  baseR.write(servo_front_R);
  delay(1000);
  baseB.write(servo_front_B);
  baseF.write(servo_front_F);
  delay(1000);
}

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html><head>
  <title>Rubik's Cube Robot</title>
  <style>button{height: 50px;width: 200px;margin-bottom: 20px;}</style>
  </head><body><center>
  <h1>Rubik's Cube Solving Robot</h1>
  <a href="http://192.168.4.1/control?result=L%20L%27%20L2%20R%20R%27%20R2%20B%20B%27%20B2%20F%20F%27%20F2%20U%20U%27%20U2%20D%20D%27%20D2"><button>Robot test</button></a>
  
</center></body></html>)rawliteral";

void handleRoot() {
  server.send(200, "text/html", index_html);
}
void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void setup(void) {
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(10);
  baseL.attach(bL);
  baseR.attach(bR);
  baseB.attach(bB);
  baseF.attach(bF);
  delay(10);
  servoPosition(servo_L, servo_L_0);
  servoPosition(servo_R, servo_R_0);
  servoPositionB(servo_B, servo_B_0);
  servoPosition(servo_F, servo_F_0);
  delay(100);
  WiFi.mode(WIFI_AP);

  WiFi.softAP(ssid, password);

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.println("succeed!!");
  STOP();
  server.on("/", handleRoot);

  server.on("/control", []() {
    String result = server.arg("result");
    server.send(200, "text/plain", result);
    Serial.println("");
    char* token = strtok(const_cast<char*>(result.c_str()), " ");
    int count = 0;
    const int MAX_TOKENS = 100;
    char* tokens[MAX_TOKENS];
    while (token != NULL && count < MAX_TOKENS) {
      tokens[count] = token;
      Serial.print(tokens[count]);
      Serial.print(" ");
      count++;
      token = strtok(NULL, " ");
    }
    Serial.println("");
    for (int i = 0; i < count; i++) {
      String data = tokens[i];
      if (data == "START") {
        Serial.print("START ");
        status = "ready";
        START();
      } else if (data == "STOP") {
        Serial.print("STOP ");
        status = "unready";
        STOP();
      }
      if (status == "ready") {
        if (data == "L") {
          Serial.print("L ");
          L();
        } else if (data == "L'") {
          Serial.print("L' ");
          LL();
        } else if (data == "L2") {
          Serial.print("L2 ");
          L2();
        } else if (data == "R") {
          Serial.print("R ");
          R();
        } else if (data == "R'") {
          Serial.print("R' ");
          RR();
        } else if (data == "R2") {
          Serial.print("R2 ");
          R2();
        } else if (data == "B") {
          Serial.print("B ");
          CHECK();
          B();
        } else if (data == "B'") {
          Serial.print("B' ");
          CHECK();
          BB();
        } else if (data == "B2") {
          Serial.print("B2 ");
          CHECK();
          B2();
        } else if (data == "F") {
          Serial.print("F ");
          CHECK();
          front_F();
        } else if (data == "F'") {
          Serial.print("F' ");
          CHECK();
          FF();
        } else if (data == "F2") {
          Serial.print("F2 ");
          CHECK();
          F2();
        } else if (data == "U") {
          Serial.print("U ");
          U();
        } else if (data == "U'") {
          Serial.print("U' ");
          UU();
        } else if (data == "U2") {
          Serial.print("U2 ");
          U2();
        } else if (data == "D") {
          Serial.print("D ");
          D();
        } else if (data == "D'") {
          Serial.print("D' ");
          DD();
        } else if (data == "D2") {
          Serial.print("D2 ");
          D2();
        } else {
          Serial.println("Error");
        }
      }
    }
    Serial.println("");
  });
  //=============================================================================================================================
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
