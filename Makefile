ARCHS = armv7 arm64
TARGET = iphone:clang:12.5:12.0

TWEAK_NAME = ActionButton12
ActionButton12_FILES = Tweak.xm AB12HUDView.m AB12Manager.m
ActionButton12_FRAMEWORKS = UIKit CoreGraphics AudioToolbox AVFoundation
ActionButton12_PRIVATE_FRAMEWORKS = SpringBoardUI SpringBoardServices
ActionButton12_CFLAGS = -fobjc-arc -I.

SUBPROJECTS += actionbutton12prefs

all: package

clean:
	@py -c "import os, glob; [os.remove(f) for f in glob.glob('*.o') + glob.glob('*.dylib') + glob.glob('actionbutton12prefs/*.o') if os.path.exists(f)]"
	@echo Cleaned build artifacts.

package:
	@py make_package.py

.PHONY: all clean package
