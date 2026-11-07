#import <UIKit/UIKit.h>
#import "AB12Common.h"
#import "AB12Manager.h"

// Forward declarations for SpringBoard classes
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

// Double tap tracker for Home button
static NSTimeInterval lastHomePressTime = 0;

%hook SpringBoard

- (void)_hardwareButtonLongPressed:(id)btn {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerPower || mgr.trigger == AB12TriggerBoth)) {
        [mgr toggleHUD];
        return;
    }
    %orig;
}

- (void)_hardwareButtonPressed:(id)btn {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerHome || mgr.trigger == AB12TriggerBoth)) {
        NSTimeInterval now = [NSDate timeIntervalSinceReferenceDate];
        if (now - lastHomePressTime < 0.4) {
            // Double press detected
            lastHomePressTime = 0;
            [mgr toggleHUD];
            return;
        } else {
            lastHomePressTime = now;
        }
    }
    %orig;
}

%end

%hook SBHomeHardwareButtonActions

- (void)performDoublePressActions {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerHome || mgr.trigger == AB12TriggerBoth)) {
        [mgr toggleHUD];
        return;
    }
    %orig;
}

%end

%hook SBHomeHardwareButton

- (void)doublePress:(id)sender {
    AB12Manager *mgr = [AB12Manager sharedManager];
    if (mgr.enabled && (mgr.trigger == AB12TriggerHome || mgr.trigger == AB12TriggerBoth)) {
        [mgr toggleHUD];
        return;
    }
    %orig;
}

%end

%hook SBUIController

- (void)launchApplicationWithIdentifier:(NSString *)bundleID suspended:(BOOL)suspended {
    %orig;
}

%end

%ctor {
    @autoreleasepool {
        // Initialize manager on SpringBoard launch
        [AB12Manager sharedManager];
    }
}
