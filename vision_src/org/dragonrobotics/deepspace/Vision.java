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
import java.util.Comparator;
import java.util.Collections;
import java.util.Arrays;
import org.opencv.core.*;
import org.opencv.imgproc.*;

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
    public static final double LOWER_THRESHOLD = 150;
    public static final double MIN_CONTOUR_AREA = 70;

    /**
     * Preprocess the Mat.
     * Isolate the green channel, resize, and binarize the image.
     * @param input the input image.
     * @return The preprocessed result.
     */
    public static Mat preprocess(Mat input) {

        // split into BGR color channels to isolate green later
        List<Mat> channels = new ArrayList<Mat>(3);
        Core.split(input, channels);

        // scale only the green channel of the input image.
        Mat resized = new Mat();
        Size newSize = new Size(
            input.cols() / SCALE_RATIO,
            input.rows() / SCALE_RATIO
        );
        Imgproc.resize(channels.get(1), resized, newSize);

        // Binarize the scaled result to isolate brightest pixels
        Mat thresholded = new Mat();
        Imgproc.threshold(
            resized,
            thresholded,
            LOWER_THRESHOLD,
            255,
            Imgproc.THRESH_BINARY
        );

        return thresholded;
    }

    /**
     * Find the vision tapes and calculate heading error.
     * @param input the preprocessed, binarized input image.
     * @param output a list to which the tapes will be added (if found).
     * @return -100000 if no tapes are found, error value if tapes are found.
     */
    public static double getVisionTape(Mat input,
        ArrayList<MatOfPoint> output) {

        // Find contours of input image. Will crash if input is not preprocessed
        List<MatOfPoint> contours = new ArrayList<>();
        Imgproc.findContours(
            input,
            contours,
            new Mat(),
            Imgproc.RETR_TREE,
            Imgproc.CHAIN_APPROX_SIMPLE
        );

        // These lists will be used throughout the code
        List<MatOfPoint> filteredContours = new ArrayList<>();
        List<MatOfPoint2f> simplifiedContours = new ArrayList<>();
        List<Point> centers = new ArrayList<>();
        List<Double> xorder = new ArrayList<>();
        List<Integer> pairs = new ArrayList<>();

        // Filter out contours and extract info into the lists defined above.
        for(MatOfPoint contour : contours) {
            // TODO is contourArea very expensive? Consider using morphology
            if(Imgproc.contourArea(contour) < MIN_CONTOUR_AREA) continue;

            // Calculate the center of mass for each contour.
            Moments moments = Imgproc.moments(contour);
            Point centroid = new Point();
            centroid.x = moments.get_m10() / moments.get_m00();
            centroid.y = moments.get_m01() / moments.get_m00();

            // calculate the simplified polygon for each contour.
            double epsilon = 0.05 * Imgproc.arcLength(
                new MatOfPoint2f(contour.toArray()), true);
            MatOfPoint2f approx = new MatOfPoint2f();
            Imgproc.approxPolyDP(
                new MatOfPoint2f(contour.toArray()), approx, epsilon, true);

            // add all information to lists
            filteredContours.add(contour);
            simplifiedContours.add(approx);
            centers.add(centroid);
            xorder.add(centroid.x);
        }

        // If there are less than two contours, why bother with the rest?
        if(simplifiedContours.size() < 2) return -100000;

        // Java 8 magic for sorting each list based on the xorder list.
        // After this step, the contours will be sorted from left to right
        // (instead of bottom-to-top as OpenCV does by default)
        filteredContours.sort(Comparator.comparingDouble(xorder::indexOf));
        simplifiedContours.sort(Comparator.comparingDouble(xorder::indexOf));
        centers.sort(Comparator.comparingDouble(xorder::indexOf));

        // Most of the important stuff happens in this loop.
        for(int i = 0; i < simplifiedContours.size() - 1; i++) {

            // Find the longest line segment of each pair of contours.

            // There is a more elegant way to do this than repreating the
            // same code twice.  But for readability purposes, I dont feel like
            // nesting it in yet another loop.
            Point[] verticesLeft = simplifiedContours.get(i).toArray();
            double longestLengthLeft = 0;
            int longestIndexLeft = 0;
            for(int j = 0; j < verticesLeft.length - 1; j++) {
                Point a = verticesLeft[j];
                Point b = verticesLeft[j+1];
                double segmentLength =
                    Math.sqrt(Math.pow(b.y - a.y, 2) + Math.pow(b.x - a.x, 2));

                if(segmentLength > longestLengthLeft) {
                    longestLengthLeft = segmentLength;
                    longestIndexLeft = j;
                }
            }

            Point[] verticesRight = simplifiedContours.get(i+1).toArray();
            double longestLengthRight = 0;
            int longestIndexRight = 0;
            for(int j = 0; j < verticesRight.length - 1; j++) {
                Point a = verticesRight[j];
                Point b = verticesRight[j+1];
                double segmentLength =
                    Math.sqrt(Math.pow(b.y - a.y, 2) + Math.pow(b.x - a.x, 2));

                if(segmentLength > longestLengthRight) {
                    longestLengthRight = segmentLength;
                    longestIndexRight = j;
                }
            }

            // Calculate the slope of each tape (y2-y1)/(x2-x1).
            double slopeLeft = (verticesLeft[longestIndexLeft+1].y
                             - verticesLeft[longestIndexLeft].y)
                             / (verticesLeft[longestIndexLeft+1].x
                             - verticesLeft[longestIndexLeft].x);
            double slopeRight = (verticesRight[longestIndexRight+1].y
                              - verticesRight[longestIndexRight].y)
                              / (verticesRight[longestIndexRight+1].x
                              - verticesRight[longestIndexRight].x);

            // derived from setting two slope-point equations equal to each
            // other.  x = (y2-y1+m1x1-m2x2) / (m1-m2).
            double x_intersect = (centers.get(i+1).y - centers.get(i).y
                + slopeLeft*centers.get(i).x - slopeRight*centers.get(i+1).x)
                / (slopeLeft - slopeRight);

            // plug x-intersection back into one of the original slope point
            // equations to get the y-intersection.
            double y_intersect =
                slopeLeft * (x_intersect - centers.get(i).x) + centers.get(i).y;

            // if they y-intersection of the two tapes is above the average
            // of the tapes' y-positions, consider it a valid pair.
            if(y_intersect < (centers.get(i+1).y + centers.get(i).y)/2 ) {
                pairs.add(i);
            }

        }
        if(pairs.size() < 1) return -100000;

        // TODO add y-positional checks, relative contour size checks here.

        // Isolate the biggest tapes.
        double largestArea = 0;
        int biggestIndex = 0;
        for(int pair : pairs) {
            double totalArea = Imgproc.contourArea(filteredContours.get(pair))
            + Imgproc.contourArea(filteredContours.get(pair+1));
            if(totalArea > largestArea) {
                largestArea = totalArea;
                biggestIndex = pair;
            }
        }

        // add to output.
        output.add(filteredContours.get(biggestIndex));
        output.add(filteredContours.get(biggestIndex+1));

        // calculate offset from center of image and return.
        // You can use this returned error in conjunction with a PIDController
        // to adjust the robot accordingly.
        double xCenter =
            (centers.get(biggestIndex).x + centers.get(biggestIndex+1).x) / 2;
        double trueCenter = input.size().width / 2;
        return xCenter - trueCenter;
    }

}
