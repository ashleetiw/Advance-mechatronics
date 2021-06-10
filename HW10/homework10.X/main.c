#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro
#include<stdio.h>
#include "ws2812b.h"

// DEVCFG0
#pragma config DEBUG = OFF // disable debugging
#pragma config JTAGEN = OFF // disable jtag
#pragma config ICESEL = ICS_PGx1 // use PGED1 and PGEC1
#pragma config PWP = OFF // disable flash write protect
#pragma config BWP = OFF // disable boot write protect
#pragma config CP = OFF // disable code protect

// DEVCFG1
#pragma config FNOSC = FRCPLL // use internal pll
#pragma config FSOSCEN = OFF // disable secondary oscillator
#pragma config IESO = OFF // disable switching clocks
#pragma config POSCMOD = OFF // RC mode
#pragma config OSCIOFNC = OFF // disable clock output
#pragma config FPBDIV = DIV_1 // divide sysclk freq by 1 for peripheral bus clock
#pragma config FCKSM = CSDCMD // disable clock switch and FSCM
#pragma config WDTPS = PS1048576 // use largest wdt
#pragma config WINDIS = OFF // use non-window mode wdt
#pragma config FWDTEN = OFF // wdt disabled
#pragma config FWDTWINSZ = WINSZ_25 // wdt window at 25%

// DEVCFG2 - get the sysclk clock to 48MHz from the 8MHz crystal
#pragma config FPLLIDIV = DIV_2 // divide input clock to be in range 4-5MHz
#pragma config FPLLMUL = MUL_24 // multiply clock after FPLLIDIV
#pragma config FPLLODIV = DIV_2 // divide clock after FPLLMUL to get 48MHz

// DEVCFG3
#pragma config USERID = 0 // some 16bit userid, doesn't matter what
#pragma config PMDL1WAY = OFF // allow multiple reconfigurations
#pragma config IOL1WAY = OFF // allow multiple reconfigurations


int main() {
    
    __builtin_disable_interrupts(); // disable interrupts while initializing things

    
    // do your TRIS and LAT commands here
    TRISBbits.TRISB4 = 1; //B4 is input
    TRISAbits.TRISA4 = 0; //A4 is output
    LATAbits.LATA4 = 0; //A4 is low
    
    
    ws2812b_setup();
    __builtin_enable_interrupts();
    
    //initialize the hues here
    float hue1 = 0;
    float hue2 = 180;
    float hue3 = 270;
    float hue4 = 300;

    //reset the lights before use
    LATBbits.LATB6 = 0; 
    
    // set timer initial to 0
    TMR2 = 0;
    
    int LED_num = 4; // total number of LEDs
    float increment = 1;
    int counter = 2;
    
    while (1) {
        wsColor c1 = HSBtoRGB(hue1,1,0.1);
        wsColor c2 = HSBtoRGB(hue2,1,0.1);
        wsColor c3 = HSBtoRGB(hue3,1,0.1);
        wsColor c4 = HSBtoRGB(hue4,1,0.1);
        
//       if (counter%2 == 0){ // mix up the order every other time to make it look pretty 
//           c1 = c4;
//           c2 = c3;
//           c3 = c2;
//           c4 = c1;
//       } 

        
        wsColor color[4] = {c1, c2, c3, c4}; 
        
        hue1 = hue1 + increment;
        hue2 = hue2 + increment;
        hue3 = hue3 + increment;
        hue4 = hue4 + increment;
      
 
        if (hue1 > 360){
            hue1 = 0;
        }
        
        if (hue2 > 360){
            hue2 = 0;
        }
        
        if (hue3 > 360){
            hue3 = 0;
        }
        
        if (hue4 > 360){
            hue4 = 0;
        }
        
        ws2812b_setColor(color, LED_num);
        
        TMR2 = 0;
        counter = counter + 1;
        
        while(TMR2 < 40000){
        }  // delay
    }
    
    
}
