package com.juuuleees.narcissa20;

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
import android.hardware.camera2.params.SessionConfiguration;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.HandlerThread;
import android.util.Log;
import android.util.Size;
import android.util.SparseIntArray;
import android.view.Surface;
import android.view.TextureView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;

public class LiveFeed extends AppCompatActivity {

    private static final SparseIntArray ORIENTATIONS = new SparseIntArray();
    public static final String TIME_STRING = "HH-mm-ss";
    private TextureView texture_view;
    private String camera_ID;
    private CameraDevice cam_hardware;
    private CameraCaptureSession cam_session;
    private CaptureRequest request;
    private CaptureRequest.Builder req_builder;
    private Handler bg_handler;
    private HandlerThread bg_thread;
    private MediaRecorder video_recorder;
    private Size dimensions;
    private int surface_width;
    private int surface_height;
    private final int FPS = 30;


//    Getters and setters
    private MediaRecorder get_video_recorder() { return this.video_recorder; }
    private int get_surface_width() { return this.surface_width; }
    private int get_surface_height() { return this.surface_height; }

    private void set_video_recorder(MediaRecorder vr) { this.video_recorder = vr; }
    private void set_surface_width(int sw) { this.surface_width = sw; }
    private void set_surface_height(int sh) { this.surface_height = sh;}

    /*
    * TODOS:
    REQUIRED:
        TODO: [RQ] Use info from Arduino (wheel odometry) to determine
        when to start/stop recording.
        
    OPTIONAL:
        TODO: [OP] Disable MediaRecorder audio recording. Tutal di naman kailangan,
        kakainin pa niyan memory.

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

        texture_view = findViewById(R.id.livefeed);
        texture_view.setSurfaceTextureListener(textureListener);
    }

//    File handling functions
    public static String createVideoPath(String file_name, Context context) {
        long date_and_time = System.currentTimeMillis();
        String directory_path = Environment.getExternalStorageDirectory().toString();

        File video_dir = new File(directory_path);
        if (!video_dir.exists()) {
            video_dir.mkdirs();
        }

        String video_dir_path = video_dir.getAbsolutePath();
        SimpleDateFormat general_time = new SimpleDateFormat(TIME_STRING);
        Date specific_time = new Date(date_and_time);
        String time_part = general_time.format(specific_time);

        String final_file = video_dir_path + "/" + time_part + file_name;
        return final_file;
    }
//    Camera-related files
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

    private int senseDeviceRotation(CameraCharacteristics cam_char, int device_orientation) {
        int sensor_orientation = cam_char.get(CameraCharacteristics.SENSOR_ORIENTATION);
        return (sensor_orientation + device_orientation + 360) % 360;
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
            setUpMediaRecorder(this.get_surface_width(), this.get_surface_height());
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

            for (Size dimension_value : preview_sizes) {
                Log.i("PreviewSize", dimension_value.toString());
                if (dimension_value.toString().equals("1280x720")) {
                    dimensions = dimension_value;
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

                this.set_surface_height(current_height);
                this.set_surface_width(current_width);
            }

        } catch (CameraAccessException cae) {{
            String exception = cae.toString();
            Log.d("CameraAccessException", exception);
        }}
        
    }

//    Not yet secure
    private void setUpMediaRecorder(int width, int height) {

        try {
            File video_file = File.createTempFile("vid", ".mp4");

            this.video_recorder = new MediaRecorder(getApplicationContext());
            video_recorder.setVideoSource(MediaRecorder.VideoSource.SURFACE);
            video_recorder.setVideoSize(this.get_surface_width(), this.get_surface_height());
            video_recorder.setVideoFrameRate(FPS);
            video_recorder.setOutputFile(video_file.getAbsolutePath());
            video_recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
            video_recorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
            try {
                video_recorder.prepare();
            } catch (IOException ioe) {
                ioe.printStackTrace();
                Toast.makeText(this, ioe.getMessage(), Toast.LENGTH_SHORT).show();
            }

        } catch (IOException e) {
            Toast toast_msg = Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_SHORT);
            toast_msg.show();
        }
    }

    private void openCamera() {
        try {
            CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);

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


}