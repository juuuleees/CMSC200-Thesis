package com.example.narcissa;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Camera;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.os.Bundle;
import android.util.Log;
import android.util.Size;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.TextureView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.core.CvType;
import org.opencv.core.Mat;

import java.util.Arrays;

public class LiveFeed extends AppCompatActivity {

    private TextureView texture_view;
    private String camera_ID;
    private CameraDevice cam_hardware;
    private CameraCaptureSession session;
    private CaptureRequest request;
    private CaptureRequest.Builder req_builder;
    private Size dimensions;
    private final CameraDevice.StateCallback stateCallback = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(@NonNull CameraDevice cameraDevice) {
            cam_hardware = cameraDevice;
            createCameraPreview();
        }

        @Override
        public void onDisconnected(@NonNull CameraDevice cameraDevice) {
            cam_hardware.close();
        }

        @Override
        public void onError(@NonNull CameraDevice cameraDevice, int i) {
            cam_hardware.close();
            cam_hardware = null;
        }
    };

    private void createCameraPreview() {
        try {
            SurfaceTexture texture = texture_view.getSurfaceTexture();
            texture.setDefaultBufferSize(dimensions.getWidth(), dimensions.getHeight());
            Surface surface = new Surface(texture);

            req_builder = cam_hardware.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);
            req_builder.addTarget(surface);
            cam_hardware.createCaptureSession(Arrays.asList(surface), new CameraCaptureSession.StateCallback() {
                @Override
                public void onConfigured(CameraCaptureSession session) {
//                    if (cam_hardware == null) {
//                        return;
//                    }

                }

                @Override
                public void onConfigureFailed(CameraCaptureSession session) {

                }
            }, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }


    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.live_feed);

        texture_view = (TextureView) findViewById(R.id.livefeed);
        texture_view.setSurfaceTextureListener(textureListener);
    }

    TextureView.SurfaceTextureListener textureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
            openCamera();
//            try {
//                openCamera();
//            } catch (CameraAccessException e) {
//                e.printStackTrace();
//            }
        }

        @Override
        public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {

        }

        @Override
        public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
            return false;
        }

        @Override
        public void onSurfaceTextureUpdated(SurfaceTexture surface) {

        }
    };



    public void openCamera() {
        try {
            CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
            camera_ID = manager.getCameraIdList()[0];
            CameraCharacteristics characteristics = manager.getCameraCharacteristics(camera_ID);
            StreamConfigurationMap map = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);

            dimensions = map.getOutputSizes(SurfaceTexture.class)[0];

            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(LiveFeed.this, new String[]{Manifest.permission.CAMERA}, 101);
                return;
            }

            manager.openCamera(camera_ID, stateCallback, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }

    }

}