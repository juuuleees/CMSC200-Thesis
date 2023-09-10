package com.juuuleees.narcissa20;

import org.apache.commons.math3.stat.StatUtils;

import java.util.Vector;
import java.lang.Double;

public class State {

    private Vector<Vector<Double>> landmarkLocations;
    private Double x, y, theta;
    private int matrixSize;                     // it's a square matrix? don't overthink it
    private boolean isInitial;

//    getters and setters
    public Vector<Vector<Double>> getlandmarkLocations() { return this.landmarkLocations; }
    public Double getX() { return this.x; }
    public Double getY() { return this.y; }
    public Double getTheta() { return this.theta; }
    public int getMatrixSize() { return this.matrixSize; }
    public boolean getIsInitial() { return this.isInitial; }

    public void setLandmarkLocations(Vector<Vector<Double>> new_locs) { this.landmarkLocations = new_locs; }
    public void setX(Double new_x) { this.x = new_x; }
    public void setY(Double new_y) { this.y = new_y; }
    public void setTheta(Double new_theta) { this.theta = new_theta; }
    public void setMatrixSize(int new_ms) { this.matrixSize = new_ms; }
    public void setIsInitial(boolean is_init) { this.isInitial = is_init; }

//    mandatory constructor
    public State() {}
    public State(boolean initial) {

        this.isInitial = initial;

//        set initial pose
        this.x = new Double(0);
        this.y = new Double(0);
        this.theta = new Double(0);

//        set initial landmarks matrix
        this.matrixSize = 3;
        this.landmarkLocations = new Vector<Vector<Double>>();
        for (int i = 0; i < this.matrixSize; i++) {
            Vector<Double> row = new Vector<Double>();
            for (int j = 0; j < this.matrixSize; j++) {
                row.add(new Double(0));
            }
            this.landmarkLocations.add(row);
        }

    }

}
