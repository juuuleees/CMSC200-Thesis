// Github token: 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
// Expires 8/19/2022

// Specialized thesis token: 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
// Expires 7/20/2022

//  NOTE: "OpenCV error: Cannot load info library for OpenCV"
//        is only applicable to special Android configs like builds with CUDA support
package com.example.narcissa;

import android.content.Context;
import android.content.res.Configuration;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.hoho.android.usbserial.driver.UsbSerialDriver;
import com.hoho.android.usbserial.driver.UsbSerialProber;

import org.opencv.android.OpenCVLoader;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private Button connect_arduino;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Configuration config = getResources().getConfiguration();
        if (!OpenCVLoader.initDebug()) {
            Log.i("OpenCV", "Couldn't initialize OpenCV.");
        } else {
            Log.i("OpenCV", "OpenCv initialized.");
        }

        connect_arduino = (Button) findViewById(R.id.bot_connect);
        connect_arduino.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                show_available_drivers();
            }
        });

    }

    public void show_available_drivers() {
        UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE);
        List<UsbSerialDriver> available_drivers = UsbSerialProber.getDefaultProber()
                .findAllDrivers(manager);
        if (available_drivers.isEmpty()) {
            Log.i("ArduinoConnect","No available drivers.");
        } else {
            for (int i = 0; i < available_drivers.size(); i++) {
                Log.i("ArduinoConnect", "Driver: " + available_drivers.get(i));
            }
        }
    }
}