package com.example.narcissa;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.hoho.android.usbserial.driver.UsbSerialDriver;
import com.hoho.android.usbserial.driver.UsbSerialProber;

import java.util.List;

public class BotConnector extends AppCompatActivity {

    private Button connect_arduino;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bot_connector);

        connect_arduino = (Button)findViewById(R.id.connect_arduino_btn);
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