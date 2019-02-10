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
     */
    public static Mat preprocess(Mat input) {

        List<Mat> channels = new ArrayList<Mat>(3);
        Core.split(input, channels);

        Mat resized = new Mat();
        Size newSize = new Size(
            input.cols() / SCALE_RATIO,
            input.rows() / SCALE_RATIO
        );
        Imgproc.resize(channels.get(2), resized, newSize);

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

    public static boolean getVisionTape(Mat input,
        ArrayList<MatOfPoint> output) {

        List<MatOfPoint> contours = new ArrayList<>();
        Imgproc.findContours(
            input,
            contours,
            new Mat(),
            Imgproc.RETR_TREE,
            Imgproc.CHAIN_APPROX_SIMPLE
        );

        List<MatOfPoint> filteredContours = new ArrayList<>();
        List<MatOfPoint2f> simplifiedContours = new ArrayList<>();
        List<Point> centers = new ArrayList<>();
        List<Double> xorder = new ArrayList<>();

        for(MatOfPoint contour : contours) {
            if(Imgproc.contourArea(contour) < MIN_CONTOUR_AREA) continue;

            Moments moments = Imgproc.moments(contour);
            Point centroid = new Point();
            centroid.x = moments.get_m10() / moments.get_m00();
            centroid.y = moments.get_m01() / moments.get_m00();

            double epsilon = 0.05 * Imgproc.arcLength(
                new MatOfPoint2f(contour.toArray()), true);
            MatOfPoint2f approx = new MatOfPoint2f();
            Imgproc.approxPolyDP(
                new MatOfPoint2f(contour.toArray()), approx, epsilon, true);

            filteredContours.add(contour);
            simplifiedContours.add(approx);
            centers.add(centroid);
            xorder.add(centroid.x);
        }

        if(simplifiedContours.size() < 2) return false;

        filteredContours.sort(Comparator.comparingDouble(xorder::indexOf));
        simplifiedContours.sort(Comparator.comparingDouble(xorder::indexOf));
        centers.sort(Comparator.comparingDouble(xorder::indexOf));

        // List<Integer> slants = new ArrayList<>();
        // int longestIndex = 0;
        // for(MatOfPoint2f contour : simplifiedContours) {
        //     double longestLength = 0;
        //     Point[] vertices = contour.toArray();
        //     if(vertices.length < 3) {
        //         slants.add(0);
        //         continue;
        //     }
        //     for(int i = 0; i < vertices.length - 2; i++) {
        //         Point a = vertices[i];
        //         Point b = vertices[i+1];
        //         double segmentLength =
        //             Math.sqrt(Math.pow(b.y - a.y, 2) + Math.pow(b.x - a.x, 2));
        //
        //         if(segmentLength > longestLength) {
        //             longestLength = segmentLength;
        //             longestIndex = i;
        //         }
        //     }
        //
        //     Point a = vertices[longestIndex];
        //     Point b = vertices[longestIndex + 1];
        //
        //     // Try to avoid crashes due to zero divison.
        //     double denominator = ((b.x - a.x) == 0) ? 1 : b.x - a.x;
        //     slants.add( ((b.y - a.y) / denominator) < 0 ? 1 : -1 );
        // }
        //
        List<Integer> pairs = new ArrayList<>();
        // List<Integer> searchKey = new ArrayList<>();
        // searchKey.add(1);
        // searchKey.add(-1);
        // int[] search = {1, -1};
        // while(slants.size() > 1) {
        //      int pair = Collections.indexOfSubList(slants, searchKey);
        //      if(pair == -1) break;
        //      pairs.add(pair);
        //      slants.set(pair, 0);
        //      slants.set(pair + 1, 0);
        // }

        for(int i = 0; i < simplifiedContours.size() - 1; i++) {
            Point[] verticesLeft = simplifiedContours.get(i).toArray();
            double longestLengthLeft = 0;
            int longestIndexLeft = 0;
            for(int j = 0; j < verticesLeft.length - 2; j++) {
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
            for(int j = 0; j < verticesRight.length - 2; j++) {
                Point a = verticesRight[j];
                Point b = verticesRight[j+1];
                double segmentLength =
                    Math.sqrt(Math.pow(b.y - a.y, 2) + Math.pow(b.x - a.x, 2));

                if(segmentLength > longestLengthRight) {
                    longestLengthRight = segmentLength;
                    longestIndexRight = j;
                }
            }

            double slopeLeft = (verticesLeft[longestIndexLeft+1].y - verticesLeft[longestIndexLeft].y) / (verticesLeft[longestIndexLeft+1].x - verticesLeft[longestIndexLeft].x);
            double slopeRight = (verticesRight[longestIndexRight+1].y - verticesRight[longestIndexRight].y) / (verticesRight[longestIndexRight+1].x - verticesRight[longestIndexRight].x);

            if(slopeLeft < slopeRight) {
                pairs.add(i);
            }

        }
        if(pairs.size() < 1) {
            System.out.println("smol");
            return false;
        }

        // TODO add y-positional checks, relative contour size checks here.
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

        output.add(filteredContours.get(biggestIndex));
        output.add(filteredContours.get(biggestIndex+1));
        return true;
    }

}
