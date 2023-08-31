//  NOTE: "OpenCV error: Cannot load info library for OpenCV"
//        is only applicable to special Android configs like builds with CUDA support
package com.juuuleees.narcissa20;

import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CaptureRequest;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.util.Log;
import android.util.Size;
import android.view.TextureView;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.hoho.android.usbserial.driver.UsbSerialDriver;
import com.hoho.android.usbserial.driver.UsbSerialProber;

import org.opencv.android.OpenCVLoader;

import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private static final int REQUEST_CAMERA_OPEN = 100;
    private static final int BAUD_RATE = 115200;
//    private static Context context;
    private Button connect_arduino;
    private LiveFeed vision;
    private TextureView textureView;
    private String cameraID;
    private CameraDevice cam_hardware;
    private CameraCaptureSession session;
    private CaptureRequest request;
    private CaptureRequest.Builder req_builder;
    private Size dimensions;
    private boolean driver_present = false;
    private int deviceID;

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
            open_camera_sensor();
            Log.i("CameraSensor", "Camera active.");
        } else {
            Log.i("CameraSensor", "Camera not found.");
        }
    }

//    Make sure the drivers for connecting to Arduino and accessing phone camera
//    are available
    public void show_available_drivers() {
        UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE);
        List<UsbSerialDriver> available_drivers = UsbSerialProber.getDefaultProber()
                .findAllDrivers(manager);
        if (available_drivers.isEmpty()) {
            Log.i("AvailableDrivers", "No available drivers.");
//            next line only for testing camera
//            this.driver_present = true;
        } else {
            this.driver_present = true;
            for (int i = 0; i < available_drivers.size(); i++) {
                Log.i("ArduinoConnect", "Driver: " + available_drivers.get(i));
            }

        }
    }

    public void open_camera_sensor() {
        Intent livefeed_intent = new Intent(this, LiveFeed.class);
        startActivity(livefeed_intent);
    }

    public void connect_to_arduino() {

    }

}