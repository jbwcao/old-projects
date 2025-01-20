#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978

int octave = 3;
bool tunerOn = false;

int o1[] = {NOTE_C1, NOTE_CS1, NOTE_D1, NOTE_DS1, NOTE_E1, NOTE_F1, NOTE_FS1, NOTE_G1, NOTE_GS1, NOTE_A1, NOTE_AS1, NOTE_B1, NOTE_C2, NOTE_CS2};
int o2[] = {NOTE_C2, NOTE_CS2, NOTE_D2, NOTE_DS2, NOTE_E2, NOTE_F2, NOTE_FS2, NOTE_G2, NOTE_GS2, NOTE_A2, NOTE_AS2, NOTE_B2, NOTE_C3, NOTE_CS3};
int o3[] = {NOTE_C3, NOTE_CS3, NOTE_D3, NOTE_DS3, NOTE_E3, NOTE_F3, NOTE_FS3, NOTE_G3, NOTE_GS3, NOTE_A3, NOTE_AS3, NOTE_B3, NOTE_C4, NOTE_CS4};
int o4[] = {NOTE_C4, NOTE_CS4, NOTE_D4, NOTE_DS4, NOTE_E4, NOTE_F4, NOTE_FS4, NOTE_G4, NOTE_GS4, NOTE_A4, NOTE_AS4, NOTE_B4, NOTE_C5, NOTE_CS5};
int o5[] = {NOTE_C5, NOTE_CS5, NOTE_D5, NOTE_DS5, NOTE_E5, NOTE_F5, NOTE_FS5, NOTE_G5, NOTE_GS5, NOTE_A5, NOTE_AS5, NOTE_B5, NOTE_C6, NOTE_CS6};
int o6[] = {NOTE_C6, NOTE_CS6, NOTE_D6, NOTE_DS6, NOTE_E6, NOTE_F6, NOTE_FS6, NOTE_G6, NOTE_GS6, NOTE_A6, NOTE_AS6, NOTE_B6, NOTE_C7, NOTE_CS7};
int o7[] = {NOTE_C7, NOTE_CS7, NOTE_D7, NOTE_DS7, NOTE_E7, NOTE_F7, NOTE_FS7, NOTE_G7, NOTE_GS7, NOTE_A7, NOTE_AS7, NOTE_B7, NOTE_C8, NOTE_CS8};


void resolveButton(int button){  
  Serial.println("Button " + String(button) + " is being pressed");

  if (button == 0 && octave > 0){
    octave--;
    delay(200);
  }
  if (button == 12 && octave < 6){
    octave++;
    delay(200);
  }

  if (tunerOn){
    noTone(10);
    tunerOn = false;
    delay(200);
    return;
  }

  if (button == 13){
    if (digitalRead(11) == 0){
      tone(10,466);
    }
    else{
      tone(10,440);
    }
    tunerOn = true;
    delay(200);
  }

  if (button < 10 && button > 1){
    int note = 0;
    switch(button){
      case 9:
        note = 0;
        break;
      case 8:
        note = 2;
        break;
      case 7:
        note = 4;
        break;
      case 6:
        note = 5;
        break;
      case 5:
        note = 7;
        break;
      case 4:
        note = 9;
        break;
      case 3:
        note = 11;
        break; 
      case 2:
        note = 12;
        break;
    }

    while(digitalRead(button) == 0){
      if (digitalRead(11) == 0 && (note == 0 || note == 2 || note == 5 || note == 7 || note == 9 || note == 12)){
        note ++;
      }
      if (octave == 0) {
        tone(10, o1[note]);
      } 
      else if (octave == 1) {
        tone(10, o2[note]);
      } 
      else if (octave == 2) {
        tone(10, o3[note]);
      } 
      else if (octave == 3) {
        tone(10, o4[note]);
      } 
      else if (octave == 4) {
        tone(10, o5[note]);
      } 
      else if (octave == 5) {
        tone(10, o6[note]);
      } 
      else if (octave == 6) {
        tone(10, o7[note]);
      }
      else{
        tone(10, o3[note]);
      }
    }
    //Serial.println("Button " + String(button) + " has stopped being pressed");
    delay(100);
    noTone(10);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(0, INPUT_PULLUP);
  pinMode(1, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);
  pinMode(13, INPUT_PULLUP);
}

void loop() {
  int buttonStatuses[] = {digitalRead(0), digitalRead(1), digitalRead(2), digitalRead(3), digitalRead(4), digitalRead(5), digitalRead(6), digitalRead(7), digitalRead(8), digitalRead(9), 1, 1, digitalRead(12), digitalRead(13)};
  
  /*
  for (int i = 0; i <= 13; i++) {
      Serial.print(' '); // Print a space between elements
      Serial.print(buttonStatuses[i]); // Print the element at index i
  }
  */
  Serial.println(); 

  for (int i = 0; i < 14; i++){
    if (buttonStatuses[i] == 0){ 
      resolveButton(i);
    }
  }
}
