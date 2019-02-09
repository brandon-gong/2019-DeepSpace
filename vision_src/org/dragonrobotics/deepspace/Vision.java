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

package org.dragonrobotics.deepspace;

import java.util.List;
import java.util.ArrayList;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;
import org.opencv.imgproc.Imgproc;

/**
 * Defines helper methods for vision processing.
 * Preprocess, find tapes, and get heading error should all be implemented
 * here.
 *
 * @author Brandon Gong
 * @date 1-9-19
 */
public class Vision {

    public static final int SCALE_RATIO = 2;
    public static final double LOWER_THRESHOLD = 240;

    /**
     * Preprocess the Mat.
     * Isolate the green channel, resize, and binarize the image.
     */
    public static Mat preprocess(Mat input) {

        List<Mat> channels = new ArrayList<Mat>(3);
        Core.split(input, channels);

        Mat resized = new Mat();
        Size newSize = new Size(input.cols() / SCALE_RATIO, input.rows() / SCALE_RATIO);
        Imgproc.resize(channels.get(2), resized, newSize);

        Mat thresholded = new Mat();
        Imgproc.threshold(resized, thresholded, LOWER_THRESHOLD, 255, Imgproc.THRESH_BINARY);

        return thresholded;
    }

}
