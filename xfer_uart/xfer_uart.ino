
#include <SD.h>
File myFile;
    


void setup(){
  Serial.begin(9600);
  pinMode(10, OUTPUT);
  if (!SD.begin(10)) {
    Serial.println("initialization failed!");
    return;
  }    
  Serial.print("hello dave.\n");
}


uint8_t byteRead;

int byteBUffer;


void loop(){
 if (Serial.available()) {
    byteRead = Serial.read();
    /*****************/
    //if "a" is sent 
    if (byteRead==0x61)
    {
      Serial.write("reading SD data\n");
      myFile = SD.open("test1.bmp");
      if (myFile) {
         Serial.println("test.txt:");
         while (myFile.available()) {
          Serial.write(myFile.read());
         }
         myFile.close();
         Serial.write("\nDONE\n");
      }else{
        Serial.println("error opening test.txt\n");
      }  
    }
    /*****************/    
    if (byteRead==0x62){Serial.write("recieved test command \n");}

    /*****************/   
    //C triggers a byte by byte xfer, d indicates next byte 
    if (byteRead==0x63)
    {
      Serial.write("reading one byte of SD data \n");
      myFile = SD.open("test1.bmp");
      if (myFile) {
         while (myFile.available()) {
           char sample = Serial.read(); 
           if (sample == 0x65){Serial.write("terminatad.\n");break;}
           if ( sample == 0x64  )
           { 
            Serial.write(myFile.read());
            //delay(10); 
           }
          
         }
         myFile.close();
      }else{
        Serial.println("error opening test.txt\n");
      }  
  
    }
    
  }

}

