//  NOTE: "OpenCV error: Cannot load info library for OpenCV"
//        is only applicable to special Android configs like builds with CUDA support
package com.example.narcissa;

import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CaptureRequest;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.util.Size;
import android.view.SurfaceView;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.hoho.android.usbserial.driver.UsbSerialDriver;
import com.hoho.android.usbserial.driver.UsbSerialProber;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;

import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private static final int REQUEST_CAMERA_OPEN = 100;
//    private static Context context;
    private Button connect_arduino;
    private LiveFeed vision;
    private boolean driver_present = false;

    private TextureView textureView;
    private String cameraID;
    private CameraDevice cam_hardware;
    private CameraCaptureSession session;
    private CaptureRequest request;
    private CaptureRequest.Builder req_builder;
    private Size dimensions;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Configuration config = getResources().getConfiguration();
        if (!OpenCVLoader.initDebug()) {
            Log.i("OpenCV", "Couldn't initialize OpenCV.");
        } else {
            Log.i("OpenCV", "OpenCV initialized.");
        }

        connect_arduino = (Button) findViewById(R.id.bot_connect);
        connect_arduino.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        show_available_drivers();
        if (driver_present) {
//                    vision = new LiveFeed(this);
//            JavaCameraView cameraBridgeView = (JavaCameraView) findViewById(R.id.live_feed);
//            cameraBridgeView.setVisibility(SurfaceView.VISIBLE);
//            cameraBridgeView.setCvCameraViewListener(
//                    (CameraBridgeViewBase.CvCameraViewListener) context);
//            cameraBridgeView.enableView();

//            TODO: Access the camera via button click like in Torchic
            open_camera_sensor();
            Log.i("CameraSensor", "Camera active.");
            // hoy git ano ba
        } else {
            Log.i("CameraSensor", "Camera not found.");
        }
    }

    public void show_available_drivers() {
        UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE);
        List<UsbSerialDriver> available_drivers = UsbSerialProber.getDefaultProber()
                .findAllDrivers(manager);
        if (available_drivers.isEmpty()) {
            Log.i("ArduinoConnect","No available drivers.");
        } else {
            this.driver_present = true;
            for (int i = 0; i < available_drivers.size(); i++) {
                Log.i("ArduinoConnect", "Driver: " + available_drivers.get(i));
            }
        }
    }

    public void open_camera_sensor() {
//        Intent camera_sensor_intent = new Intent(MediaStore.INTENT_ACTION_VIDEO_CAMERA);
//        if (camera_sensor_intent.resolveActivity(getPackageManager()) != null) {
//            startActivityForResult(camera_sensor_intent, REQUEST_CAMERA_OPEN);
//        }
    }

}