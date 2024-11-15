#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

float beatsPerMinute;
int beatAvg;

void setup()
{
  Serial.begin(115200);

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  
  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
  particleSensor.enableDIETEMPRDY();
}

void loop()
{
  long irValue = particleSensor.getIR();
  long redValue = particleSensor.getRed();
  float temperature = particleSensor.readTemperature();
  
  if (checkForBeat(irValue) == true){
    long delta = millis() - lastBeat;
    lastBeat = millis();

    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20)
    {
      rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
      rateSpot %= RATE_SIZE; //Wrap variable

      //Take average of readings
      beatAvg = 0;
      for (byte x = 0 ; x < RATE_SIZE ; x++)
        beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }

  Serial.print(irValue);// Valor del led infrarojo
  Serial.print(",");
  Serial.print(beatsPerMinute);// Valor de los latidos por minutos
  Serial.print(",");
  Serial.print(beatAvg);// Valor del promedio de los latidos por minuto
  Serial.print(",");
  Serial.print(redValue);// Valor del led rojo
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");

  if (irValue < 50000){
    Serial.print("No finger?");
  }else{
    Serial.print("¡Yes finger!");  
  }
  Serial.println();
}
