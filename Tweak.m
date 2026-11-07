// Generated from Tweak.xm
#import <UIKit/UIKit.h>
#import <objc/runtime.h>
#import "AB12Common.h"
#import "AB12Manager.h"

#ifdef __cplusplus
extern "C" {
#endif
void MSHookMessageEx(Class _class, SEL sel, IMP imp, IMP *result);
#ifdef __cplusplus
}
#endif

// Forward declarations
@interface SpringBoard : UIApplication
- (void)_hardwareButtonLongPressed:(id)btn;
- (void)_hardwareButtonPressed:(id)btn;
@end

@interface SBUIController : NSObject
+ (instancetype)sharedInstance;
- (void)launchApplicationWithIdentifier:(NSString *)bundleID suspended:(BOOL)suspended;
- (void)launchApplicationWithIdentifier:(NSString *)bundleID;
@end

@interface SBHomeHardwareButtonActions : NSObject
- (void)performDoublePressActions;
@end

@interface SBHomeHardwareButton : NSObject
- (void)doublePress:(id)sender;
@end

static NSTimeInterval lastHomePressTime = 0;

// SpringBoard _hardwareButtonLongPressed:
static void (*orig_SpringBoard_longPress)(id self, SEL _cmd, id btn);
static void hook_SpringBoard_longPress(id self, SEL _cmd, id btn) {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerPower || mgr.trigger == AB12TriggerBoth)) {
        [mgr toggleHUD];
        return;
    }
    if (orig_SpringBoard_longPress) {
        orig_SpringBoard_longPress(self, _cmd, btn);
    }
}

// SpringBoard _hardwareButtonPressed:
static void (*orig_SpringBoard_press)(id self, SEL _cmd, id btn);
static void hook_SpringBoard_press(id self, SEL _cmd, id btn) {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerHome || mgr.trigger == AB12TriggerBoth)) {
        NSTimeInterval now = [NSDate timeIntervalSinceReferenceDate];
        if (now - lastHomePressTime < 0.4) {
            lastHomePressTime = 0;
            [mgr toggleHUD];
            return;
        } else {
            lastHomePressTime = now;
        }
    }
    if (orig_SpringBoard_press) {
        orig_SpringBoard_press(self, _cmd, btn);
    }
}

// SBHomeHardwareButtonActions performDoublePressActions
static void (*orig_SBHomeHardwareButtonActions_doublePress)(id self, SEL _cmd);
static void hook_SBHomeHardwareButtonActions_doublePress(id self, SEL _cmd) {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerHome || mgr.trigger == AB12TriggerBoth)) {
        [mgr toggleHUD];
        return;
    }
    if (orig_SBHomeHardwareButtonActions_doublePress) {
        orig_SBHomeHardwareButtonActions_doublePress(self, _cmd);
    }
}

// SBHomeHardwareButton doublePress:
static void (*orig_SBHomeHardwareButton_doublePress)(id self, SEL _cmd, id sender);
static void hook_SBHomeHardwareButton_doublePress(id self, SEL _cmd, id sender) {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerHome || mgr.trigger == AB12TriggerBoth)) {
        [mgr toggleHUD];
        return;
    }
    if (orig_SBHomeHardwareButton_doublePress) {
        orig_SBHomeHardwareButton_doublePress(self, _cmd, sender);
    }
}

// SBUIController launchApplicationWithIdentifier:suspended:
static void (*orig_SBUIController_launch)(id self, SEL _cmd, NSString *bundleID, BOOL suspended);
static void hook_SBUIController_launch(id self, SEL _cmd, NSString *bundleID, BOOL suspended) {
    if (orig_SBUIController_launch) {
        orig_SBUIController_launch(self, _cmd, bundleID, suspended);
    }
}

static __attribute__((constructor)) void AB12Init(void) {
    @autoreleasepool {
        // Initialize AB12Manager
        [AB12Manager sharedManager];

        // Hook SpringBoard
        Class sbClass = objc_getClass("SpringBoard");
        if (sbClass) {
            MSHookMessageEx(sbClass, @selector(_hardwareButtonLongPressed:), (IMP)&hook_SpringBoard_longPress, (IMP*)&orig_SpringBoard_longPress);
            MSHookMessageEx(sbClass, @selector(_hardwareButtonPressed:), (IMP)&hook_SpringBoard_press, (IMP*)&orig_SpringBoard_press);
        }

        // Hook SBHomeHardwareButtonActions
        Class actionsClass = objc_getClass("SBHomeHardwareButtonActions");
        if (actionsClass) {
            MSHookMessageEx(actionsClass, @selector(performDoublePressActions), (IMP)&hook_SBHomeHardwareButtonActions_doublePress, (IMP*)&orig_SBHomeHardwareButtonActions_doublePress);
        }

        // Hook SBHomeHardwareButton
        Class btnClass = objc_getClass("SBHomeHardwareButton");
        if (btnClass) {
            MSHookMessageEx(btnClass, @selector(doublePress:), (IMP)&hook_SBHomeHardwareButton_doublePress, (IMP*)&orig_SBHomeHardwareButton_doublePress);
        }

        // Hook SBUIController
        Class uiControllerClass = objc_getClass("SBUIController");
        if (uiControllerClass) {
            MSHookMessageEx(uiControllerClass, @selector(launchApplicationWithIdentifier:suspended:), (IMP)&hook_SBUIController_launch, (IMP*)&orig_SBUIController_launch);
        }
    }
}
