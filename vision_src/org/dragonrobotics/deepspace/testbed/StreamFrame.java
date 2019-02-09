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

import javax.swing.*;
import java.awt.image.BufferedImage;
import java.awt.Graphics;
import java.awt.image.DataBufferByte;
import org.opencv.core.Mat;
import org.opencv.core.Core;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;

/**
 * Provides a very simple window to stream video or OpenCV output for
 * debugging purposes.  Multiple instances of StreamFrame can be used at one
 * time.
 *
 * @author Brandon Gong
 * @date 1-9-19
 */
public class StreamFrame extends JFrame {

    // internal image-showing panel.
    private ImgPanel panel;

    /**
     * Construct a new StreamFrame instance.
     *
     * This only does the minimal necessary things to set up a window.
     * Window is hidden by default. To show it, use StreamFrame.setVisible(true)
     *
     * @param width - The width of the new StreamFrame.
     * @param height - The height of the new StreamFrame.
     * @param title - The title of the new StreamFrame.
     */
    public StreamFrame(int width, int height, String title) {
        super();

        this.setSize(width, height);
        this.setTitle(title);
        this.setVisible(false);
        this.setResizable(false);
        this.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        // Don't need to re-add after this; panel will redraw on frame update.
        this.panel = new ImgPanel();
        this.getContentPane().add(this.panel);
    }

    /**
     * Update the StreamFrame with the new frame.
     * @param x - An OpenCV Mat containing the new frame.
     */
    public void update(Mat x) {
        this.panel.putFrame(this.fromMat(x));
    }

    /**
     * Internal method for converting OpenCV Mat to BufferedImage.
     * @param a - An OpenCV Mat containing the image to be converted.
     */
    private BufferedImage fromMat(Mat a) {

        // create a colored/grayscale bufferedimage accordingly
        int type = (a.channels() > 1) ?
            BufferedImage.TYPE_3BYTE_BGR :
            BufferedImage.TYPE_BYTE_GRAY;

        byte[] fromBuffer = new byte[a.rows() * a.cols() * a.channels()];
        a.get(0, 0, fromBuffer); // get all of the pixels from the mat

        BufferedImage image = new BufferedImage(a.cols(), a.rows(), type);
        final byte[] toBuffer =
            ((DataBufferByte) image.getRaster().getDataBuffer()).getData();

        // arraycopy is faster than just manually looping over it.
        System.arraycopy(fromBuffer, 0, toBuffer, 0, fromBuffer.length);
        return image;

    }
}

/**
 * Internal class for video stream.
 * Defines a custom JPanel for displaying BufferedImages.
 *
 * @author Brandon Gong
 * @date 1-9-19
 */
class ImgPanel extends JPanel {

    // Frame.  private to force the usage of putFrame()
    private BufferedImage frame;

    /**
     * Change the current Image stored within the ImgPanel.
     * This will force a repaint of the ImgPanel.
     * @param frame - the new image to show.
     */
    public void putFrame(BufferedImage frame) {
        this.frame = frame;
        repaint();
    }

    // override the default paint method to draw the BufferedImage.
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(frame, 0, 0, this);
    }

}
