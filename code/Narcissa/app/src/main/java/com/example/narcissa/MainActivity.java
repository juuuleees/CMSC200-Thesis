// Github token: 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
// Expires 8/19/2022

// Specialized thesis token: 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
// Note: key need repo, gist, add:org, workflow
// Expires 8/3/2022

//  NOTE: "OpenCV error: Cannot load info library for OpenCV"
//        is only applicable to special Android configs like builds with CUDA support
package com.example.narcissa;

import android.content.res.Configuration;
import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import org.opencv.android.OpenCVLoader;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Configuration config = getResources().getConfiguration();
        if (!OpenCVLoader.initDebug()) {
            Log.i("OpenCV", "Couldn't initialize OpenCV.");
        } else {
            Log.i("OpenCV", "OpenCv initialized.");
        }

//        Adjust to device orientation
//        NOTE: use getSupportFragmentManager() for androidx.fragment
        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();

        if (config.orientation == Configuration.ORIENTATION_LANDSCAPE) {
            // landscape mode
            Landscape_Frag landscape_orientation = new Landscape_Frag();
            fragmentTransaction.replace(android.R.id.content, landscape_orientation);

        } else {
            // portrait mode
            Portrait_Frag portrait_orientation = new Portrait_Frag();
            fragmentTransaction.replace(android.R.id.content, portrait_orientation);
        }
        fragmentTransaction.commit();
    }
}