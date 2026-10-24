#define HID_CUSTOM_MFG_STRING     "aeksco"
#define HID_CUSTOM_PRODUCT_STRING "MouseMover"

#include <HID-Project.h>
#include <HID-Settings.h>

const bool DEBUG = false;

unsigned long lastMove = 0;
// 5s while debugging, otherwise 45s
const unsigned long interval = (DEBUG ? 5UL : 45UL) * 1000UL;
const unsigned long moveDelay = DEBUG ? 1000UL : 20UL;
const int moveStep = DEBUG ? 50 : 1;

void setup() {
  // Start HID mouse
  BootMouse.begin();
}

void loop() {
  unsigned long now = millis();

  if (now - lastMove >= interval) {

    // Nudge right, then back left by the same amount to avoid drift
    BootMouse.move(moveStep, 0);
    delay(moveDelay);
    BootMouse.move(-moveStep, 0);

    lastMove = now;
  }
}
