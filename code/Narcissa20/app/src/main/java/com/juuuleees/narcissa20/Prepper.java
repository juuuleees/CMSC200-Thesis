package com.juuuleees.narcissa20;

import org.opencv.core.Mat;
import java.io.File;

public class Prepper {

    private final float THRESHOLD = 0.05f;
//    private final File DIRECTORY_PATH;

    private File videoInput;
    private float minEuclideanDistance;
    private int featureCount;

//    getters and setters
    public File getVideoInput() { return this.videoInput; }
    public float getMinEuclideanDistance() { return this.minEuclideanDistance; }
    public int getFeatureCount() { return this.featureCount; }

    public void setVideoInput(File v_in) { this.videoInput = v_in; }
    public void setMinEuclideanDistance(float m_ed) { this.minEuclideanDistance = m_ed; }
    public void setFeatureCount(int fc) { this.featureCount = fc; }

    public Prepper() {}




}
