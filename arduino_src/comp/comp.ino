#include <FastLED.h>

int gHue = 0;

#define LED_PIN 6
#define NUM_LEDS 300
#define BRIGHTNESS 100
#define LED_TYPE WS2811
#define COLOR_ORDER GRB
#define UPDATES_PER_SECOND 100

CRGB leds[NUM_LEDS];
long startMillis;
int previous = 0;
boolean split;
boolean moving = true;
boolean scrolling;
boolean reverse = false;
int start;
boolean startCode = false;
static uint8_t startIndex = 0;
CRGBPalette16 currentPalette;
TBlendType currentBlending=LINEARBLEND;

int8_t function;
uint8_t currentPattern =0;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  //delay(3000);
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();
  Boot();  
}
typedef void (*PatternList[])();
PatternList patterns  = {
  switchMaroon, RedMotion,BlueMotion,armUp,armDown,runningBall,
  RedAllianceStandby,bpm, BlueAllianceStandby, stopLift,
  Hatch,shoemode,ChangePalettePeriodically
};

void loop() {
  /*while(!startCode){
    randomDot();
    FastLED.show();
    if(Serial.available()){
      
    int code =Serial.readString().toInt();
      if(code == 5002){
        startCode = true;
      }else{
        Serial.println(code);
      }
    }
  }*/
  if (Serial.available())
  {
  
    String ser = Serial.readString();
    function = ser.toInt();
    //Serial.println(function);
    //Serial.println(sizeof(patterns)/2 -1);
    if(function >=0 && function <=(sizeof(patterns)/2 -1)){
    currentPattern = function;
    }
  }
  EVERY_N_MILLISECONDS(50) {gHue++;}



    startIndex += 1;
  if(currentPattern == 10){
    startMillis = millis();
  }
  patterns[currentPattern]();
  //Serial.println(startIndex);
  FastLED.show();
  FastLED.delay(10);
}


void FillLEDsfromPalette(uint8_t colorIndex) {
  uint8_t brightness = 255;
  if (split){
    for(int i = NUM_LEDS / 2; i >=0; i--){
      leds[i] = ColorFromPalette(currentPalette, colorIndex, brightness, currentBlending);
      leds[NUM_LEDS-i] = ColorFromPalette(currentPalette, colorIndex, brightness, currentBlending);
      colorIndex -=3;
    }
  }
  else{
  for (int i = 0; i < (NUM_LEDS); i++)
  {
    leds[i] = ColorFromPalette(currentPalette, colorIndex, brightness, currentBlending);
    if (scrolling) {
      if (reverse){
        colorIndex -= 3;
      }else{
        colorIndex += 3;
      }
    }
  }
}
}

void switchMaroon(){
  previous = 0;
  static boolean flash = true;
  if (flash){
    FlashMaroonAndWhite();
  }else if(!flash){
    ScrollMaroonAndWhite();
  }
 
  EVERY_N_SECONDS(10) {flash = !flash;}
}
void FlashMaroonAndWhite()
{
  CRGB maroon = CRGB::Maroon;
  CRGB white = CRGB::Gray;
  CRGB black = CRGB::Black;
  currentPalette = CRGBPalette16(
      maroon, maroon, black, black,
      white, white, black, black,
      maroon, maroon, black, black,
      white, white, black, black);
  moving = true;
  scrolling = false;
  reverse = false;
  split = false;
  currentBlending = LINEARBLEND;
  FillLEDsfromPalette(startIndex);

}

void ScrollMaroonAndWhite()
{
  CRGB maroon = CRGB::Maroon;
  CRGB white = CRGB::Gray;
  CRGB black = CRGB::Black;
  currentPalette = CRGBPalette16(
      maroon, maroon, black, black,
      white, white, black, black,
      maroon, maroon, black, black,
      white, white, black, black);
  moving = true;
  scrolling = true;
  reverse = false;
  split = false;
  currentBlending = LINEARBLEND;
  FillLEDsfromPalette(startIndex);
}
void RedMotion(){
  previous = 1;
  int num = random16(NUM_LEDS);
  for(int i = 0; i< num; i++){
    leds[i] = CRGB::Red;
  }
  
  for (int i = NUM_LEDS; i > num; i--){
   //leds[i] = CRGB::Black; 
   leds[i].fadeLightBy( 98 );
  }
  delay(90);
}
void RedAllianceStandby()
{
  previous = 6;
  fill_solid( currentPalette, 16, CRGB::Black);
      // and set every fourth one to white.
      currentPalette[0] = CRGB::Red;
      currentPalette[8] = CRGB::Red;
      static int go = 0;
      go +=1;
      split = true;
      moving = true;
      scrolling = true;
      FillLEDsfromPalette(go);

}
void BlueMotion(){
  previous = 2;
  int num = random16(NUM_LEDS);
  for(int i = 0; i< num; i++){
    leds[i] = CRGB::Blue;
  }
  
  for (int i = NUM_LEDS; i > num; i--){
   //leds[i] = CRGB::Black; 
   leds[i].fadeLightBy( 98 );
  }
  delay(90);
}

void BlueAllianceStandby()
{
  previous = 8;
  fill_solid( currentPalette, 16, CRGB::Black);
      // and set every fourth one to white.
      currentPalette[0] = CRGB::Blue;
      currentPalette[8] = CRGB::Blue;
      static int go = 0;
      go +=1;
      split = true;
      moving = true;
      scrolling = true;
      FillLEDsfromPalette(go);

}


void bpm()
{
  previous = 7;
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = 62;
  CRGBPalette16 palette = PartyColors_p;
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for( int i = 0; i < NUM_LEDS; i++) { //9948
    leds[i] = ColorFromPalette(palette, gHue+(i*2), beat-gHue+(i*10));
  }
}
void stopLift(){
  previous = 9;
  fill_solid(currentPalette, 16, CRGB::DarkGray);
  FillLEDsfromPalette(currentPalette);
}

void Boot()
{
  //fill_solid(currentPalette,16,CRGB(150,75,0));

  // int pos = beatsin16(30, 14, NUM_LEDS - 1);
  //int sec = beatsin16(30,0,14,start);
  //if (sec == 14){
  //leds[14-sec] += CHSV(gHue,255,192);
  //leds[pos] += CHSV(gHue, 255, 192);
  //Ascend strip
  for (int i = NUM_LEDS / 2; i >= 0; i--)
  {
    //for (int i = 0; i < (NUM_LEDS / 2) + 1; i++) {
    //fadeToBlackBy(leds, NUM_LEDS, 75);
    leds[i] = CRGB(0, 255, 0);
    leds[NUM_LEDS - i] = CRGB(0, 255, 0);

    FastLED.show();
     FastLED.delay(10);
  }

  // Descend Strip
  /*for (int i = NUM_LEDS / 2; i >= 0; i--)
  {
    //for (int i = 0; i < (NUM_LEDS / 2) + 1; i++) {
    leds[i] = CRGB(0, 0, 0);
    leds[NUM_LEDS - i] = CRGB(0, 0, 0);
    FastLED.show();
    FastLED.delay(100);

  }*/
}

void randomDot(){
  for(int i = 0; i<NUM_LEDS;i++){
    leds[i].fadeLightBy( 64 );
  }
     if( random8() < 80) {
    leds[ random16(NUM_LEDS) ] += CRGB(random8(),random8(),random());
  }
  delay(100);
}

void armUp(){
  previous = 3;
  fill_solid(currentPalette,16, CRGB::Black);
  currentPalette[0]= CRGB::White;
  currentPalette[4]= CRGB::White;
  currentPalette[8]=CRGB::White;
  currentPalette[12]=CRGB::White;
  moving = true;
  scrolling = true;
  reverse = false;
  FillLEDsfromPalette(startIndex);
}
void armDown(){
  previous = 4;
  fill_solid(currentPalette,16, CRGB::Black);
  currentPalette[0]= CRGB::White;
  currentPalette[4]= CRGB::White;
  currentPalette[8]=CRGB::White;
  currentPalette[12]=CRGB::White;
  moving = true;
  scrolling = true;
  reverse = true;
  FillLEDsfromPalette(startIndex);
}
void Hatch(){
  previous = 10;
  CRGB black = CRGB::Black;
  CRGB purp = CRGB::Lavender;
  currentPalette = CRGBPalette16(
    purp,black,purp,black,
    purp,black,purp,black,
    purp,black,purp,black,
    purp,black,purp,black
  );
  moving = true;
  scrolling = false;
  FillLEDsfromPalette(startIndex);


  
}
void runningBall(){
  previous = 5;
  CRGB black = CRGB::Black;
  CRGB purp = CRGB::Lavender;
  currentPalette = CRGBPalette16(
    purp,black,purp,black,
    purp,black,purp,black,
    purp,black,purp,black,
    purp,black,purp,black
  );
  moving = true;
  scrolling = true;
  FillLEDsfromPalette(startIndex); 
}

void shoemode(){
previous = 0;
  static boolean shoe = true;
  if (shoe){
    shoemode2();
  }else if(!shoe){
    shoemode1();
  }
 
  EVERY_N_SECONDS(4) {shoe = !shoe;}
  
}
void shoemode1(){
  static int val = 0;
  CRGB purp = CRGB(255,0,255);
  //CRGB green = CRGB::Green;
  CRGB blue = CRGB(255,255,0);
  CRGB white = CRGB(0,255,255);
  /*currentPalette = CRGBPalette16(
    purp,purp,purp,purp,
    blue,blue,blue,blue,
    white,white,white,white
  );
  moving = true;
  scrolling = false;
  FillLEDsfromPalette(startIndex);*/
  for(int i=0; i<NUM_LEDS; i++){
    leds[i] =CRGB(triwave8(val),triwave8(val+85),triwave8(val+170));
  }
  val+=10;
  delay(10);
}
void shoemode2(){
  CRGB red = CRGB::Red;
  CRGB blue = CRGB::Blue;
  CRGB green = CRGB::Green;
  static int color = 0;
  if (color == 0){
    fill_solid(currentPalette,16,red);
    color = 1;
  }else if (color == 1){
    fill_solid(currentPalette,16,green);
    color = 2;
  }else if(color == 2){
    fill_solid(currentPalette,16,blue);
    color = 0;
  }
  moving = false;
  scrolling = false;
  FillLEDsfromPalette(startIndex);
  delay(1000/6 -10);
  
}

const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM =
{
    CRGB::Red,
    CRGB::Gray, // 'white' is too bright compared to red and blue
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Red,
    CRGB::Gray,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Blue,
    CRGB::Black,
    CRGB::Black
};


void ChangePalettePeriodically()
{
    uint8_t secondHand = (millis() / 1000) % 60;
    static uint8_t lastSecond = 99;
    static int index = 0;
    index += 1;
    moving = true;
    scrolling = true;
    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand ==  0)  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND;  FillLEDsfromPalette(index); }
        if( secondHand == 10)  { currentPalette = RainbowStripeColors_p;   currentBlending = NOBLEND;   FillLEDsfromPalette(index);}
        if( secondHand == 15)  { currentPalette = RainbowStripeColors_p;   currentBlending = LINEARBLEND;  FillLEDsfromPalette(index); }
        if( secondHand == 20)  { SetupPurpleAndGreenPalette();             currentBlending = LINEARBLEND; FillLEDsfromPalette(index); }
        if( secondHand == 25)  { SetupTotallyRandomPalette();              currentBlending = LINEARBLEND; FillLEDsfromPalette(index); }
        if( secondHand == 30)  { SetupBlackAndWhiteStripedPalette();       currentBlending = NOBLEND; FillLEDsfromPalette(index); }
        if( secondHand == 35)  { SetupBlackAndWhiteStripedPalette();       currentBlending = LINEARBLEND;  FillLEDsfromPalette(index);}
        if( secondHand == 40)  { currentPalette = CloudColors_p;           currentBlending = LINEARBLEND; FillLEDsfromPalette(index); }
        if( secondHand == 45)  { currentPalette = PartyColors_p;           currentBlending = LINEARBLEND;  FillLEDsfromPalette(index);}
        if( secondHand == 50)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = NOBLEND;  FillLEDsfromPalette(index); }
        if( secondHand == 55)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = LINEARBLEND;  FillLEDsfromPalette(index);}
    }
     FillLEDsfromPalette(index); 
}

// This function fills the palette with totally random colors.
void SetupTotallyRandomPalette()
{
    for( int i = 0; i < 16; i++) {
        currentPalette[i] = CHSV( random8(), 255, random8());
    }
}

// This function sets up a palette of black and white stripes,
// using code.  Since the palette is effectively an array of
// sixteen CRGB colors, the various fill_* functions can be used
// to set them up.
void SetupBlackAndWhiteStripedPalette()
{
    // 'black out' all 16 palette entries...
    fill_solid( currentPalette, 16, CRGB::Black);
    // and set every fourth one to white.
    currentPalette[0] = CRGB::White;
    currentPalette[4] = CRGB::White;
    currentPalette[8] = CRGB::White;
    currentPalette[12] = CRGB::White;
    
}

// This function sets up a palette of purple and green stripes.
void SetupPurpleAndGreenPalette()
{
    CRGB purple = CHSV( HUE_PURPLE, 255, 255);
    CRGB green  = CHSV( HUE_GREEN, 255, 255);
    CRGB black  = CRGB::Black;
    
    currentPalette = CRGBPalette16(
                                   green,  green,  black,  black,
                                   purple, purple, black,  black,
                                   green,  green,  black,  black,
                                   purple, purple, black,  black );
}


// This example shows how to set up a static color palette
// which is stored in PROGMEM (flash), which is almost always more
// plentiful than RAM.  A static PROGMEM palette like this
// takes up 64 bytes of flash.
