package com.vajra.service;

import org.opencv.core.Mat;
import org.springframework.stereotype.Service;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

@Service
public class FrameBufferQueue {

    private final BlockingQueue<Mat> buffer = new ArrayBlockingQueue<>(5);

    public boolean pushFrame(Mat frame) {
        if (!buffer.offer(frame)) {
            Mat dropped = buffer.poll();
            if (dropped != null) {
                dropped.release();
            }
            return buffer.offer(frame);
        }
        return true;
    }

    public Mat popFrame(long timeoutMs) throws InterruptedException {
        return buffer.poll(timeoutMs, TimeUnit.MILLISECONDS);
    }

    public int size() {
        return buffer.size();
    }

    public void drainAndRelease() {
        Mat m;
        while ((m = buffer.poll()) != null) {
            m.release();
        }
    }
}
