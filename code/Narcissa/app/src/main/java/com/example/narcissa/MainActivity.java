//  NOTE: "OpenCV error: Cannot load info library for OpenCV"
//        is only applicable to special Android configs like builds with CUDA support
package com.example.narcissa;

import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
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

    static Context context;
    private Button connect_arduino;
    private LiveFeed vision;
    private boolean driver_present = false;

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
//            Intent intent = new Intent("android.media.action.IMAGE_CAPTURE");
//            startActivity(intent);
            Log.i("Camera", "Camera active.");
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

}