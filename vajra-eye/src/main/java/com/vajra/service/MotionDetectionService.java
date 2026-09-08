package com.vajra.service;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class MotionDetectionService {

    private Mat previousFrame;

    @Value("${vajra.motion.pixel-threshold:25}")
    private int pixelThreshold;

    @Value("${vajra.motion.min-area:1000}")
    private double minArea;

    @Value("${vajra.motion.pan-fraction:0.60}")
    private double panFraction;

    private volatile double lastMotionArea;

    public synchronized void resetBaseline() {
        if (previousFrame != null) {
            previousFrame.release();
            previousFrame = null;
        }
    }

    public synchronized boolean detectMotion(Mat frame) {
        Mat gray = new Mat();
        Mat delta = new Mat();
        Mat thresh = new Mat();
        try {
            Imgproc.cvtColor(frame, gray, Imgproc.COLOR_BGR2GRAY);
            Imgproc.GaussianBlur(gray, gray, new Size(21, 21), 0);

            if (previousFrame == null) {
                previousFrame = gray.clone();
                return false;
            }

            Core.absdiff(previousFrame, gray, delta);
            Imgproc.threshold(delta, thresh, pixelThreshold, 255, Imgproc.THRESH_BINARY);
            Imgproc.dilate(thresh, thresh, new Mat());

            previousFrame.release();
            previousFrame = gray.clone();

            List<MatOfPoint> contours = new ArrayList<>();
            Imgproc.findContours(thresh, contours, new Mat(),
                    Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);

            double totalMotionArea = 0.0;
            for (MatOfPoint contour : contours) {
                totalMotionArea += Imgproc.contourArea(contour);
                contour.release();
            }
            lastMotionArea = totalMotionArea;

            double frameArea = (double) frame.rows() * frame.cols();
            if (totalMotionArea > frameArea * panFraction) {
                return false;
            }
            return totalMotionArea >= minArea;
        } finally {
            gray.release();
            delta.release();
            thresh.release();
        }
    }

    public double getLastMotionArea() {
        return lastMotionArea;
    }

    public int getPixelThreshold() {
        return pixelThreshold;
    }

    public double getMinArea() {
        return minArea;
    }

    public double getPanFraction() {
        return panFraction;
    }

    public synchronized void setPixelThreshold(int pixelThreshold) {
        this.pixelThreshold = pixelThreshold;
    }

    public synchronized void setMinArea(double minArea) {
        this.minArea = minArea;
    }

    public synchronized void setPanFraction(double panFraction) {
        this.panFraction = panFraction;
    }
}
