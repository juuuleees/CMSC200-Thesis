package com.juuuleees.narcissa20;

import java.util.ArrayList;

public class EKF_SLAM {

    private ArrayList<State> statesList = new ArrayList<State>();
    public EKF_SLAM() {}

//    methods
    public void stateInitialization() {
        State initialState = new State(true);
        statesList.add(initialState);
    }

    public void predictionStep() {

    }

}
