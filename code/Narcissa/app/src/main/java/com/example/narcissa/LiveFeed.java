package com.example.narcissa;

import android.content.Context;
import android.hardware.camera2.CameraManager;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;

import androidx.appcompat.app.AppCompatActivity;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.core.CvType;
import org.opencv.core.Mat;

public class LiveFeed extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {

    private CameraBridgeViewBase cameraBridgeView;
    private Mat mat1, mat2, mat3;

//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        cameraBridgeView = (JavaCameraView) findViewById(R.id.narcissaVision);
//        cameraBridgeView.setVisibility(SurfaceView.VISIBLE);
//        cameraBridgeView.setCvCameraViewListener(this);
//        cameraBridgeView.enableView();
//    }

    public LiveFeed() {}

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
//        get the frames
        mat1 = inputFrame.rgba();

        return mat1;
    }

    @Override
    public void onCameraViewStopped() {
        mat1.release();
        mat2.release();
        mat3.release();
    }

    @Override
    public void onCameraViewStarted(int width, int height) {
//        CV_8UC4 is Mat type
        mat1 = new Mat(width, height, CvType.CV_8UC4);
        mat2 = new Mat(width, height, CvType.CV_8UC4);
        mat3 = new Mat(width, height, CvType.CV_8UC4);
    }


}