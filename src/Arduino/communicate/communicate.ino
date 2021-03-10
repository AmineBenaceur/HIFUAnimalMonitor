#include <Adafruit_MCP9600.h>

#define USE_ARDUINO_INTERRUPTS true  
#include <PulseSensorPlayground.h>

//variables
const int PulseWire = 0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED13 = 13;          // The on-board Arduino LED, close to PIN 13.
int Threshold = 550;  
#define I2C_ADDRESS (0x67)

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
      Serial.println("Sensor not found. Check wiring!");
      while (1);
   }
  if (pulseSensor.begin()){
      Serial.println("pulse began");
   }
  Serial.println("Found MCP9600!");
  
  mcp.setADCresolution(MCP9600_ADCRESOLUTION_18);
  Serial.print("ADC resolution set to ");
  switch (mcp.getADCresolution()) {
    case MCP9600_ADCRESOLUTION_18:   Serial.print("18"); break;
    case MCP9600_ADCRESOLUTION_16:   Serial.print("16"); break;
    case MCP9600_ADCRESOLUTION_14:   Serial.print("14"); break;
    case MCP9600_ADCRESOLUTION_12:   Serial.print("12"); break;
  }
  Serial.println(" bits");

  mcp.setThermocoupleType(MCP9600_TYPE_T);
  Serial.print("Thermocouple type set to ");
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
  Serial.println(" type");

  mcp.setFilterCoefficient(3);
  Serial.print("Filter coefficient value set to: ");
  Serial.println(mcp.getFilterCoefficient());

  mcp.setAlertTemperature(1, 30);
  Serial.print("Alert #1 temperature set to ");
  Serial.println(mcp.getAlertTemperature(1));
  mcp.configureAlert(1, true, true);  // alert 1 enabled, rising temp

  mcp.enable(true);

  Serial.println(F("------------------------------"));
}

void loop() {
  // put your main code here, to run repeatedly:

 int myBPM = pulseSensor.getBeatsPerMinute();
  if (pulseSensor.sawStartOfBeat()){
    //String line = String.format("BPM-%f-TMP-%f-",myBPM,mcp.readThermocouple());
    Serial.print("BPM:");                        // Print phrase "BPM: " 
    //delay(100);
    Serial.println(myBPM);
    //delay(100);
    Serial.print("TMP:");
    //delay(100);
    Serial.println(mcp.readThermocouple() ); 
    //delay(100);
    
    //Serial.println(line); 
    
 }
 

  delay(20);
}
