package com.vajra.util;

import org.opencv.core.Mat;

import java.util.function.Consumer;

/**
 * RAII helper: always release native cv::Mat storage.
 */
public final class NativeScope {

    private NativeScope() {
    }

    public static void usingMat(Consumer<Mat> block) {
        Mat mat = new Mat();
        try {
            block.accept(mat);
        } finally {
            mat.release();
        }
    }
}
