// 有線控制ABB <_9_line control ABB>
#include <Servo.h>  
Servo leftMotor;
Servo rightMotor;

const int stopPWM = 1500;
const int maxForwardPWM = 1700;
const int maxBackwardPWM = 1300;
const int leftMotorPin = 13;
const int rightMotorPin = 12;

void setup() 
{ 
  // 初始化伺服马达
  leftMotor.attach(leftMotorPin);
  rightMotor.attach(rightMotorPin);

  // 设置初始状态为停止
  leftMotor.writeMicroseconds(stopPWM);
  rightMotor.writeMicroseconds(stopPWM);
  Serial.begin(115200); 
}  

void loop()
{ 
  char c;              
  // 讀取串列阜資料
  String inputString = "";
  if(Serial.available()){
    c = Serial.read();
    while (c != '\n') 
    {
        inputString += c;
        delay(5);
        c = Serial.read();
    }

    int spaceIndex = inputString.indexOf('_');
    String linearSpeedStr = inputString.substring(0, spaceIndex);
    String angularSpeedStr = inputString.substring(spaceIndex + 1);
    float linearSpeed = linearSpeedStr.toFloat();
    float angularSpeed = angularSpeedStr.toFloat();

    int leftMotorPWM = 0;
    int rightMotorPWM = 0;

    if(linearSpeed == float(0)){
      leftMotorPWM = stopPWM - angularSpeed*50;
      rightMotorPWM = stopPWM - angularSpeed*50;
    }
    else if(angularSpeed == float(0)){
      leftMotorPWM = stopPWM + linearSpeed*150;
      rightMotorPWM = stopPWM - linearSpeed*150;
    }
    else{
      leftMotorPWM = stopPWM + linearSpeed*150 - angularSpeed*50;
      rightMotorPWM = stopPWM - linearSpeed*150 - angularSpeed*50;
    }
    
    leftMotor.writeMicroseconds(leftMotorPWM);
    rightMotor.writeMicroseconds(rightMotorPWM);
 
    while(Serial.read() >= 0){}
  }
}
