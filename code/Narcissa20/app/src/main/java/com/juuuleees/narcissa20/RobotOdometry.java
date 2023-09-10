package com.juuuleees.narcissa20;

public class RobotOdometry {

    private Double rx, ry, rTheta;
    public RobotOdometry() {}
    public RobotOdometry(State state) {
        this.rx = state.getX();
        this.ry = state.getY();
        this.rTheta = state.getTheta();

    }
}
