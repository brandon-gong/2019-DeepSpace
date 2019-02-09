/*
 * Copyright (c) 2019 Dragon Robotics
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

package org.dragonrobotics.deepspace.testbed;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;

import org.dragonrobotics.deepspace.Vision;

/**
 * Test class for Vision.
 *
 * This code shouldn't be deployed to the raspberry pi.  It will break.
 * But if you are testing, keep all StreamFrame and Swing stuff out of
 * Vision.java and put it in here instead. Vision.java should be pure Vision
 * code.
 *
 * @author Brandon Gong
 * @date 1-9-19
 */
public class Test {

    public static void main(String[] args) {

        // I believe the rasberry pi code already does this.
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

        VideoCapture v = new VideoCapture(2);
        v.set(Videoio.CAP_PROP_AUTO_EXPOSURE, 0);
        v.set(Videoio.CAP_PROP_EXPOSURE, -10);

        Mat input = new Mat();
        v.read(input);

        StreamFrame inputFrame = new StreamFrame(input.cols(), input.rows(), "input");
        StreamFrame preprocessFrame = new StreamFrame(input.cols() / Vision.SCALE_RATIO, input.rows() / Vision.SCALE_RATIO, "preprocess");

        inputFrame.setVisible(true);
        preprocessFrame.setVisible(true);

        while(true) {
            v.read(input);
            inputFrame.update(input);
            preprocessFrame.update(Vision.preprocess(input));
        }
    }

}
