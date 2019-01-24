# QuickMandlebrot
Attempt to reduce computational complexity of generating full mandlebrot set by mapping from point to point instead of iterating on each point


Traditional mandlebrot set takes each pixel, maps it to the complex plane, iterates function on it, and returns a value. Quick mandlebrot set instead starts at a given pixel, maps it to the complex plane, and moves through the complex plane using the generating function, assigning each new point its value based on the cycle generated at that origin. 
