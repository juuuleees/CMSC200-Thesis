// Github token: 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
// Expires 8/19/2022

// Specialized thesis token: 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
// Expires 7/20/2022

package com.example.narcissa;

import android.content.res.Configuration;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Configuration config = getResources().getConfiguration();

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