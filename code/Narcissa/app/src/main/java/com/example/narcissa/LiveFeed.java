package com.example.narcissa;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.ImageFormat;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CameraMetadata;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.util.Log;
import android.util.Size;
import android.util.SparseIntArray;
import android.view.Surface;
import android.view.TextureView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.core.CvType;
import org.opencv.core.Mat;

import java.util.Arrays;
import java.util.List;

public class LiveFeed extends AppCompatActivity {

    private TextureView texture_view;
    private String camera_ID;
    private CameraDevice cam_hardware;
    private CameraCaptureSession cam_session;
    private CaptureRequest request;
    private CaptureRequest.Builder req_builder;
    private Handler bg_handler;
    private HandlerThread bg_thread;
    private Size dimensions;
    private int surface_width;
    private int surface_height;
    private static final SparseIntArray ORIENTATIONS = new SparseIntArray();

    /*
    * TODOS:
    * TODO: make camera landscape and full screen
    * */

    static {
        ORIENTATIONS.append(Surface.ROTATION_0, 0);
        ORIENTATIONS.append(Surface.ROTATION_90, 90);
        ORIENTATIONS.append(Surface.ROTATION_180, 180);
        ORIENTATIONS.append(Surface.ROTATION_270, 270);
    }

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.live_feed);

        texture_view = (TextureView) findViewById(R.id.livefeed);
        texture_view.setSurfaceTextureListener(textureListener);
    }

    // setup callback to receive updates about camera device
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

    TextureView.SurfaceTextureListener textureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
            setupCamera(height, width);
            openCamera();
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

    @Override
    protected void onResume() {
        super.onResume();

        startBackgroundThread();
        if (texture_view.isAvailable()) {
            setupCamera(texture_view.getHeight(), texture_view.getWidth());
            openCamera();
        } else {
            texture_view.setSurfaceTextureListener(textureListener);
        }
    }

    @Override
    protected void onPause() {
        stopBackgroundThread();
        super.onPause();
    }

    private void startBackgroundThread() {
        bg_thread = new HandlerThread("Camera background");
        bg_thread.start();
        bg_handler = new Handler(bg_thread.getLooper());
    }

    private void stopBackgroundThread() {
        bg_thread.quitSafely();

        try {
            bg_thread.join();
        } catch (Exception e) {
            e.printStackTrace();
        }
        bg_thread = null;
        bg_handler = null;
    }

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
                    cam_session = session;
                    updatePreview();
                }

                @Override
                public void onConfigureFailed(CameraCaptureSession session) {
                    Log.i("CameraSensor", "ay wasak");
                }
            }, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void setupCamera(int height, int width) {
        try {
            CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
            camera_ID = manager.getCameraIdList()[0];           // use rear camera
            CameraCharacteristics characteristics = manager.getCameraCharacteristics(camera_ID);

            
            Size[] preview_sizes = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP)
                    .getOutputSizes(ImageFormat.JPEG);

            for (int i = 0; i < preview_sizes.length; i++) {
                Log.i("PreviewSize", preview_sizes[i].toString());
                if (preview_sizes[i].toString().equals("1280x720")) {
                    dimensions = preview_sizes[i];
                    Log.i("Dimensions", "Dimensions changed");
                }
            }

            int device_orientation = getWindowManager().getDefaultDisplay().getRotation();
            int current_orientation = senseDeviceRotation(characteristics, device_orientation);

            int current_width = width;
            int current_height = height;
            Log.i("CameraOrie: ", Integer.toString(current_orientation));
            if (current_orientation == 90) {
                current_height = width;
                current_width = height;
            }

        } catch (CameraAccessException cae) {{
            String exception = cae.toString();
            Log.d("CameraAccessException", exception);
        }}
        
    }

    private void openCamera() {
        try {
            CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
            CameraCharacteristics characteristics = manager.getCameraCharacteristics(camera_ID);
            StreamConfigurationMap map = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);

//            dimensions = map.getOutputSizes(SurfaceTexture.class)[0];
            Log.i("OpenCamera", dimensions.toString());

            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(LiveFeed.this, new String[]{Manifest.permission.CAMERA}, 101);
                return;
            }

            manager.openCamera(camera_ID, stateCallback, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }

    }

    private void updatePreview() {
        if (cam_hardware != null) {
            req_builder.set(CaptureRequest.CONTROL_MODE, CameraMetadata.CONTROL_MODE_AUTO);

            try {
                cam_session.setRepeatingRequest(req_builder.build(), null, bg_handler);
            } catch (CameraAccessException e) {
                e.printStackTrace();
            }

        }
    }

    private int senseDeviceRotation(CameraCharacteristics cam_char, int device_orientation) {
        int sensor_orientation = cam_char.get(CameraCharacteristics.SENSOR_ORIENTATION);
//        Log.i("sensorDebug", "Sensor orientation: " + Integer.toString(sensor_orientation));
        int orientation_value = (sensor_orientation + device_orientation + 360) % 360;
//        Log.i("sensorDebug", "Final orientation: " + Integer.toString(final_orientation));
        return orientation_value;
    }
}