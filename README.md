# QTMWrapper
A toolkit to enable easy integration with Qualisys motion capture measurements. 

Have a look at `example.py` for information on usage. This repo is of use only if:

- You have a Qualisys motion capture system 
- You have a mobile robot for which you need position and/or orientation estimates
- You want to be able to access these estimates/values asynchronously at whatever frequency (although the values will be updated at the frequency the camera is running in)

For example, you could use this to run a control strategy that runs at 50 Hz while your motion capture is capturing things at 100 Hz. 

---

There are two wrappers: `QTMWrapper` and `QTMWrapper6DOF`. The former can provide position estimates *even if* the motion capture is unable to track the 6DOF position. In other words, the latter tracks the 6DOF pose while the former tracks the 3d position of the markers only. So you'll have fewer dropped frames with the first one and it's recommended to use that in cases where orientation information is not needed.

In the case of `6DOF`, the `.getpose()` method returns an object of class `Pose` that contains `.pos` a 1D array of size 3, and `.rot` a 3x3 2d array.

In the case of the 'normal' wrapper, the `.getpose()` method returns a tuple `(x, y, z)`. 