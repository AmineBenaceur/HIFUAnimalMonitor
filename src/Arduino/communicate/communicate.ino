
#include <Adafruit_MCP9600.h>

#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>

//variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED13 = 13;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;  
#define I2C_ADDRESS (0x67)

// AB: Setup for K-type

#include <Adafruit_MAX31856.h>

// Use software SPI: CS, DI, DO, CLK
Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(10, 11, 12, 13);
// use hardware SPI, just pass in the CS pin
//Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(10);

PulseSensorPlayground pulseSensor;
Adafruit_MCP9600 mcp;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  //configure
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.blinkOnPulse(LED13);       //auto-magically blink Arduino's LED with heartbeat.
  pulseSensor.setThreshold(Threshold);   

  
  
  if (! mcp.begin(I2C_ADDRESS)) {
      //Serial.println("Sensor not found. Check wiring!");
      while (1);
   }
  if (pulseSensor.begin()){
      //Serial.println("pulse began");
   }
  //Serial.println("Found MCP9600!");
  
  mcp.setADCresolution(MCP9600_ADCRESOLUTION_18);
  //Serial.print("ADC resolution set to ");
  switch (mcp.getADCresolution()) {
    case MCP9600_ADCRESOLUTION_18:    break;
    case MCP9600_ADCRESOLUTION_16:    break;
    case MCP9600_ADCRESOLUTION_14:    break;
    case MCP9600_ADCRESOLUTION_12:    break;
  }
  //Serial.println(" bits");

  mcp.setThermocoupleType(MCP9600_TYPE_T);
  //Serial.print("Thermocouple type set to ");
  switch (mcp.getThermocoupleType()) {
    case MCP9600_TYPE_K:  Serial.print("K"); break;
    case MCP9600_TYPE_J:  Serial.print("J"); break;
    case MCP9600_TYPE_T:  Serial.print("T"); break;
    case MCP9600_TYPE_N:  Serial.print("N"); break;
    case MCP9600_TYPE_S:  Serial.print("S"); break;
    case MCP9600_TYPE_E:  Serial.print("E"); break;
    case MCP9600_TYPE_B:  Serial.print("B"); break;
    case MCP9600_TYPE_R:  Serial.print("R"); break;
  }
  //Serial.println(" type");

  mcp.setFilterCoefficient(3);
  Serial.print("Filter coefficient value set to: ");
  Serial.println(mcp.getFilterCoefficient());

  mcp.setAlertTemperature(1, 30);
  Serial.print("Alert #1 temperature set to ");
  Serial.println(mcp.getAlertTemperature(1));
  mcp.configureAlert(1, true, true);  // alert 1 enabled, rising temp

  mcp.enable(true);

  // AB: Setup for K-Type thermometer
  
  
  Serial.println("MAX31856 thermocouple test");

  maxthermo.begin();

  maxthermo.setThermocoupleType(MAX31856_TCTYPE_K);

  Serial.print("Thermocouple type: ");
  switch (maxthermo.getThermocoupleType() ) {
    case MAX31856_TCTYPE_B: Serial.println("B Type"); break;
    case MAX31856_TCTYPE_E: Serial.println("E Type"); break;
    case MAX31856_TCTYPE_J: Serial.println("J Type"); break;
    case MAX31856_TCTYPE_K: Serial.println("K Type"); break;
    case MAX31856_TCTYPE_N: Serial.println("N Type"); break;
    case MAX31856_TCTYPE_R: Serial.println("R Type"); break;
    case MAX31856_TCTYPE_S: Serial.println("S Type"); break;
    case MAX31856_TCTYPE_T: Serial.println("T Type"); break;
    case MAX31856_VMODE_G8: Serial.println("Voltage x8 Gain mode"); break;
    case MAX31856_VMODE_G32: Serial.println("Voltage x8 Gain mode"); break;
    default: Serial.println("Unknown"); break;
  Serial.println(F("Arduino completed setup"));
}
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  uint8_t fault = maxthermo.readFault();
  if (fault) {
    if (fault & MAX31856_FAULT_CJRANGE) Serial.println("Cold Junction Range Fault");
    if (fault & MAX31856_FAULT_TCRANGE) Serial.println("Thermocouple Range Fault");
    if (fault & MAX31856_FAULT_CJHIGH)  Serial.println("Cold Junction High Fault");
    if (fault & MAX31856_FAULT_CJLOW)   Serial.println("Cold Junction Low Fault");
    if (fault & MAX31856_FAULT_TCHIGH)  Serial.println("Thermocouple High Fault");
    if (fault & MAX31856_FAULT_TCLOW)   Serial.println("Thermocouple Low Fault");
    if (fault & MAX31856_FAULT_OVUV)    Serial.println("Over/Under Voltage Fault");
    if (fault & MAX31856_FAULT_OPEN)    Serial.println("Thermocouple Open Fault");
  }
  */
 int myBPM = pulseSensor.getBeatsPerMinute();
  if (pulseSensor.sawStartOfBeat()){
   
    //String line = String.format("BPM-%f-TMP-%f-",myBPM,mcp.readThermocouple());
    Serial.print("B:");                        // Print phrase "BPM: " 
    //delay(100);
    Serial.println(myBPM);
    //delay(100);
    Serial.print("T:");
    //delay(100);
    Serial.println(mcp.readThermocouple() ); 
    //delay(100);
    
    //Serial.println(line); 
    Serial.print("K:");
    Serial.println(maxthermo.readThermocoupleTemperature() ); 
    //delay(100);
    
     /*

     // AB: convert to proper format for sending through serial
     float val_t = mcp.readThermocouple();
     float val_k = 15.5;
     char str_T[5];
     char str_K[5];
     char str_bpm[5];
     char buff[20];
     
     sprintf(buff,":%s:%d:%s:\n",str_T,myBPM,str_K);
     dtostrf(val_t,4,2,str_T);
     dtostrf(val_k,4,2,str_K);
     
     Serial.print(buff);
     
     
     //char buff[20];
     //sprintf(buff,"%s:%d:%s:\n",str_T,myBPM,str_K);
     
     
     //Serial.print(buff);
    */
 }
 
  //delay(20);
  delay(20);
}


  
 
