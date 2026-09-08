package com.vajra.model;

public class SceneObject {

    private String className;
    private double probability;
    private double x;
    private double y;
    private double w;
    private double h;
    private boolean threat;

    public SceneObject() {
    }

    public SceneObject(String className, double probability, double x, double y, double w, double h, boolean threat) {
        this.className = className;
        this.probability = probability;
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.threat = threat;
    }

    public String getClassName() {
        return className;
    }

    public double getProbability() {
        return probability;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getW() {
        return w;
    }

    public double getH() {
        return h;
    }

    public boolean isThreat() {
        return threat;
    }
}
