package com.example.narcissa;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

public class Portrait_Frag extends Fragment implements View.OnClickListener {

    private Button video_demo;

    public Portrait_Frag() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View video_demo_view = inflater.inflate(R.layout.portrait_frag, container, false);
//        Remember that findViewById() needs to be attached to the view na gagamitin mo
        video_demo = (Button)video_demo_view.findViewById(R.id.vid_demo);
        video_demo.setOnClickListener(this);

        return video_demo_view;
    }

    @Override
    public void onClick(View v) {
        access_video_demo(v);
    }

    public void access_video_demo(View view) {
//        getActivity() gets the the activity that the fragment's connected to
        Intent intent = new Intent(getActivity(), VideoDemonstrations.class);
        startActivity(intent);
    }



}