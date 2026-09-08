package com.vajra;

import nu.pattern.OpenCV;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class VajraEyeApplication {

    static {
        OpenCV.loadLocally();
    }

    public static void main(String[] args) {
        SpringApplication.run(VajraEyeApplication.class, args);
    }
}
